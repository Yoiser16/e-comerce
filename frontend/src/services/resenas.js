import apiClient from './api'

export const resenasService = {
  async getDestacadas(limit = 6) {
    const response = await apiClient.get('/resenas/destacadas', { params: { limit } })
    return response.data
  },

  async getResumenProducto(productoId) {
    const response = await apiClient.get(`/resenas/producto/${productoId}/resumen`)
    return response.data
  },

  async getResenasProducto(productoId, params = {}) {
    const { limit = 6, offset = 0 } = params
    const response = await apiClient.get(`/resenas/producto/${productoId}`, {
      params: { limit, offset }
    })
    return response.data
  },

  async crearResena(productoId, rating) {
    const response = await apiClient.post('/resenas', {
      producto_id: productoId,
      rating
    })
    return response.data
  },

  async listarAdmin(estado = 'pendiente') {
    const response = await apiClient.get('/resenas/admin', { params: { estado } })
    return response.data
  },

  async cambiarEstado(resenaId, estado) {
    const response = await apiClient.patch(`/resenas/${resenaId}/estado`, { estado })
    return response.data
  }
}
