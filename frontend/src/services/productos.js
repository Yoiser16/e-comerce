import apiClient from './api'

export const productosService = {
  // ===== MÉTODOS PÚBLICOS =====
  
  // Listar productos disponibles (para tienda)
  async getProductos(params = {}) {
    const response = await apiClient.get('/productos/', { params })
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
      params: { q: termino }
    })
    return response.data
  },

  // ===== MÉTODOS ADMIN (CRUD) =====
  
  // Listar TODOS los productos (para admin)
  async listarTodos(params = {}) {
    const { limite = 100, offset = 0 } = params
    const response = await apiClient.get('/productos/admin/todos', {
      params: { limite, offset }
    })
    return response.data
  },

  // Alias para obtenerTodos (mismo que listarTodos)
  async obtenerTodos(params = {}) {
    return this.listarTodos(params)
  },

  // Crear producto
  async crear(producto) {
    const response = await apiClient.post('/productos/', producto)
    return response.data
  },

  // Actualizar producto
  async actualizar(id, datos) {
    const response = await apiClient.put(`/productos/${id}`, datos)
    return response.data
  },

  // Eliminar producto (soft delete)
  async eliminar(id) {
    await apiClient.delete(`/productos/${id}`)
    return true
  },

  // Eliminar producto permanentemente (hard delete - solo para inactivos)
  async eliminarPermanentemente(id) {
    await apiClient.delete(`/productos/${id}?permanente=true`)
    return true
  },

  // Subir imagen de producto
  async subirImagen(file) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post('/upload/imagen', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
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

  // Alias para eliminar producto (mismo que quitar)
  async eliminarProducto(productoId) {
    return this.quitarProducto(productoId)
  },

  // Resumen del carrito (para el badge)
  async getResumen() {
    const response = await apiClient.get('/carrito/resumen')
    return response.data
  }
}

// ===== SERVICIO DE FAVORITOS =====
export const favoritosService = {
  // Listar favoritos del usuario
  async listar() {
    // FastAPI define el endpoint en "/favoritos/" (barra final requerida)
    const response = await apiClient.get('/favoritos/')
    return response.data
  },

  // Agregar a favoritos
  async agregar(productoId) {
    // Usar barra final para coincidir con el backend
    const response = await apiClient.post('/favoritos/', {
      producto_id: productoId
    })
    return response.data
  },

  // Eliminar de favoritos
  async eliminar(productoId) {
    const response = await apiClient.delete(`/favoritos/${productoId}`)
    return response.data
  },

  // Toggle favorito (agregar/quitar)
  async toggle(productoId) {
    const response = await apiClient.post(`/favoritos/toggle/${productoId}`)
    return response.data
  },

  // Verificar si es favorito
  async verificar(productoId) {
    const response = await apiClient.get(`/favoritos/check/${productoId}`)
    return response.data.es_favorito
  }
}

// ===== SERVICIO DE PRODUCTOS VISTOS =====
export const vistosService = {
  /**
   * Listar productos vistos recientemente
   * @param {string} email - Email del usuario
   * @param {number} limit - Cantidad máxima (default: 10)
   */
  async listar(email, limit = 10) {
    const response = await apiClient.get('/productos-vistos/', {
      params: { email, limit }
    })
    return response.data
  },

  /**
   * Registrar vista de un producto
   * @param {string} productoId - UUID del producto
   * @param {string} email - Email del usuario
   */
  async registrar(productoId, email) {
    const response = await apiClient.post('/productos-vistos/registrar', {
      producto_id: productoId,
      email: email
    })
    return response.data
  },

  /**
   * Limpiar historial de vistos
   * @param {string} email - Email del usuario
   */
  async limpiar(email) {
    const response = await apiClient.delete('/productos-vistos/limpiar', {
      params: { email }
    })
    return response.data
  }
}
