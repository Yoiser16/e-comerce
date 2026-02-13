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
 * Convierte una URL relativa de imagen a URL absoluta del backend
 * @param {string} url - URL de la imagen (puede ser relativa o absoluta)
 * @returns {string} URL absoluta
 */
export const getImageUrl = (url) => {
  if (!url) return null
  if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
    return url
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
      // IMPORTANTE: El endpoint /favoritos/ no soporta autenticación B2B
      // No intentar refresh ni limpiar tokens en este caso
      if (originalRequest.url?.includes('/favoritos')) {
        return Promise.reject(error)
      }
      
      // Buscar refresh token en ambas ubicaciones (B2C y B2B)
      const refreshToken = localStorage.getItem('refresh_token') || localStorage.getItem('b2b_refresh_token')
      const isB2B = !!localStorage.getItem('b2b_refresh_token')
      
      // Si no hay refresh token, limpiar todo y rechazar
      if (!refreshToken) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('b2b_access_token')
        localStorage.removeItem('b2b_refresh_token')
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
        
        // Limpiar TODOS los tokens (B2C y B2B)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('b2b_access_token')
        localStorage.removeItem('b2b_refresh_token')
        
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
