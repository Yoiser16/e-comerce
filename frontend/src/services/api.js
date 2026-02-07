import axios from 'axios'

// URL base del backend
export const API_BASE_URL = 'http://localhost:8000'

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
  // Si ya es una URL absoluta (http/https), devolverla tal cual
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  // Si es relativa, construir URL absoluta con el backend
  return `${API_BASE_URL}${url}`
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
        console.warn('Error parsing user data:', e)
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
      const refreshToken = localStorage.getItem('refresh_token')
      
      // Si no hay refresh token, simplemente rechazar (no redirigir)
      if (!refreshToken) {
        localStorage.removeItem('access_token')
        return Promise.reject(error)
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const response = await axios.post('http://localhost:8000/api/v1/auth/refresh', {
          refresh: refreshToken
        })

        const { access } = response.data
        localStorage.setItem('access_token', access)
        isRefreshing = false

        originalRequest.headers.Authorization = `Bearer ${access}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        isRefreshing = false
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        // NO redirigir automáticamente - esto causaba el loop infinito
        // Solo limpiar tokens y rechazar el error
        console.warn('Sesión expirada. Token refresh falló.')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
