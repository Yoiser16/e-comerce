import apiClient from './api'

export const ordenesService = {
  /**
   * Obtener todas las órdenes (admin)
   */
  async obtenerTodas() {
    const response = await apiClient.get('/ordenes')
    return response.data
  },

  /**
   * Crear nueva orden
   */
  async crear(ordenData) {
    const response = await apiClient.post('/ordenes', ordenData)
    return response.data
  },

  /**
   * Confirmar una orden
   */
  async confirmar(ordenId) {
    const response = await apiClient.post(`/ordenes/${ordenId}/confirmar`)
    return response.data
  },

  /**
   * Actualizar estado de una orden
   */
  async actualizarEstado(ordenId, estado) {
    const response = await apiClient.patch(`/ordenes/${ordenId}`, { estado })
    return response.data
  },

  /**
   * Obtener detalles de una orden
   */
  async obtenerPorId(ordenId) {
    const response = await apiClient.get(`/ordenes/${ordenId}`)
    return response.data
  },

  /**
   * Obtener órdenes recientes (dashboard)
   */
  async obtenerRecientes(limite = 5) {
    const response = await apiClient.get(`/dashboard/ordenes/recientes?limite=${limite}`)
    return response.data
  }
}
