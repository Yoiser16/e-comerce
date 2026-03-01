import axios from 'axios'

// URL base del backend
export const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace('/api/v1', '')

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * Verifica si hay un token de acceso válido (no expirado)
 * @returns {boolean} true si hay token válido
 */
export const hasValidToken = () => {
  const token = localStorage.getItem('access_token') || localStorage.getItem('b2b_access_token')
  if (!token) return false
  
  try {
    // Decodificar payload del JWT (sin verificar firma)
    const payload = JSON.parse(atob(token.split('.')[1]))
    const exp = payload.exp
    if (!exp) return false
    
    // Verificar si expiró (con 30 segundos de margen)
    const now = Math.floor(Date.now() / 1000)
    return exp > (now + 30)
  } catch {
    return false
  }
}

/**
 * Limpia todos los tokens y datos de sesión
 */
export const clearSession = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('b2b_access_token')
  localStorage.removeItem('b2b_refresh_token')
  localStorage.removeItem('user')
  localStorage.removeItem('b2b_user')
}

/**
 * Convierte una URL relativa de imagen a URL absoluta del backend
 * @param {string} url - URL de la imagen (puede ser relativa o absoluta)
 * @returns {string} URL absoluta
 */
export const getImageUrl = (url) => {
  if (!url) return null
  
  // Strip localhost/dev URLs - convert to relative path
  if (url.includes('localhost') || url.includes('127.0.0.1')) {
    try {
      const parsed = new URL(url)
      url = parsed.pathname // e.g. "/static/uploads/productos/xxx.png"
    } catch {
      url = url.replace(/https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?/g, '')
    }
  }
  
  if (url.startsWith('https://') || url.startsWith('data:')) {
    return url
  }
  // For http:// on production (mixed content), convert to relative
  if (url.startsWith('http://')) {
    try {
      const parsed = new URL(url)
      url = parsed.pathname
    } catch {
      return url
    }
  }
  const normalized = url.startsWith('/') ? url : `/${url}`
  return `${API_BASE_URL}${normalized}`
}

// Interceptor para agregar el token JWT y email
apiClient.interceptors.request.use(
  (config) => {
    // Buscar token en ambas ubicaciones (B2C y B2B)
    const token = localStorage.getItem('access_token') || localStorage.getItem('b2b_access_token')
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Agregar email del usuario en header X-User-Email si está disponible
    const user = localStorage.getItem('user') || localStorage.getItem('b2b_user')
    if (user) {
      try {
        const userData = JSON.parse(user)
        if (userData.email) {
          config.headers['X-User-Email'] = userData.email
        }
      } catch (e) {
        // Error silencioso
      }
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar refresh token
let isRefreshing = false

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Solo intentar refresh si es 401, no es un retry, y hay refresh token
    if (error.response?.status === 401 && !originalRequest._retry && !isRefreshing) {
      // Buscar refresh token en ambas ubicaciones (B2C y B2B)
      const refreshToken = localStorage.getItem('refresh_token') || localStorage.getItem('b2b_refresh_token')
      const isB2B = !!localStorage.getItem('b2b_refresh_token')
      
      // Si no hay refresh token, limpiar sesión y rechazar silenciosamente
      if (!refreshToken) {
        clearSession()
        // Emitir evento de sesión expirada (los componentes pueden escuchar esto)
        window.dispatchEvent(new CustomEvent('session-expired'))
        return Promise.reject(error)
      }

      originalRequest._retry = true
      isRefreshing = true
      
      try {
        const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, {
          refresh: refreshToken
        })

        const { access } = response.data
        
        // Guardar token en la ubicación correcta según el tipo
        if (isB2B) {
          localStorage.setItem('b2b_access_token', access)
        } else {
          localStorage.setItem('access_token', access)
        }
        
        isRefreshing = false

        originalRequest.headers.Authorization = `Bearer ${access}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        isRefreshing = false
        
        // Refresh falló - limpiar sesión
        clearSession()
        // Emitir evento de sesión expirada
        window.dispatchEvent(new CustomEvent('session-expired'))
        
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient