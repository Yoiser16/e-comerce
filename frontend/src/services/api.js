import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar el token JWT
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
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
        const response = await axios.post('http://localhost:8000/api/v1/auth/token/refresh', {
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
