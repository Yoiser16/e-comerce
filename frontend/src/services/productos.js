import apiClient from './api'

export const productosService = {
  // Listar productos
  async getProductos(params = {}) {
    const response = await apiClient.get('/productos', { params })
    return response.data
  },

  // Buscar productos
  async buscarProductos(params = {}) {
    const response = await apiClient.get('/productos/buscar', { params })
    return response.data
  },

  // Productos destacados
  async getDestacados() {
    const response = await apiClient.get('/productos/destacados')
    return response.data
  },

  // Detalle de producto
  async getProducto(id) {
    const response = await apiClient.get(`/productos/${id}`)
    return response.data
  },

  // Autocompletar búsqueda
  async autocompletar(termino) {
    const response = await apiClient.get('/productos/autocompletar', {
      params: { termino }
    })
    return response.data
  }
}

export const authService = {
  // Login
  async login(email, password) {
    const response = await apiClient.post('/auth/token', {
      username: email,
      password
    })
    
    const { access, refresh } = response.data
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    
    return response.data
  },

  // Logout
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },

  // Verificar si está autenticado
  isAuthenticated() {
    return !!localStorage.getItem('access_token')
  }
}

export const carritoService = {
  // Obtener carrito
  async getCarrito() {
    const response = await apiClient.get('/carrito')
    return response.data
  },

  // Agregar producto
  async agregarProducto(productoId, cantidad = 1) {
    const response = await apiClient.post('/carrito/items', {
      producto_id: productoId,
      cantidad
    })
    return response.data
  },

  // Actualizar cantidad
  async actualizarCantidad(productoId, cantidad) {
    const response = await apiClient.patch(`/carrito/items/${productoId}`, {
      cantidad
    })
    return response.data
  },

  // Quitar producto
  async quitarProducto(productoId) {
    const response = await apiClient.delete(`/carrito/items/${productoId}`)
    return response.data
  },

  // Resumen del carrito (para el badge)
  async getResumen() {
    const response = await apiClient.get('/carrito/resumen')
    return response.data
  }
}
