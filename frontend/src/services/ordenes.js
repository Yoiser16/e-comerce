import apiClient from './api'

export const ordenesService = {
  /**
   * Obtener todas las órdenes (admin) - Versión optimizada con items incluidos
   * @param {boolean} includeItems - Si es true, incluye los items de cada orden
   */
  async obtenerTodas(includeItems = true) {
    const response = await apiClient.get(`/ordenes?include_items=${includeItems}`)
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
   * Actualizar estado de pago de una orden
   */
  async actualizarEstadoPago(ordenId, estadoPago) {
    const response = await apiClient.patch(`/ordenes/${ordenId}`, { estado_pago: estadoPago })
    return response.data
  },

  /**
   * Actualizar estado de envío de una orden
   */
  async actualizarEstadoEnvio(ordenId, estadoEnvio) {
    const response = await apiClient.patch(`/ordenes/${ordenId}`, { estado_envio: estadoEnvio })
    return response.data
  },

  /**
   * Obtener detalles de una orden
   * NOTA: Si ya tienes los datos del listado con include_items=true,
   * no necesitas llamar este endpoint
   */
  async obtenerPorId(ordenId) {
    const response = await apiClient.get(`/ordenes/${ordenId}`)
    return response.data
  },

  /**
   * Obtener órdenes del usuario autenticado por email
   */
  async obtenerPorEmail(email) {
    const response = await apiClient.get(`/ordenes/mis-ordenes?email=${encodeURIComponent(email)}`)
    return response.data
  },

  /**
   * Obtener productos frecuentes del usuario (basado en historial de compras)
   * @param {string} email - Email del usuario
   * @param {number} limit - Cantidad máxima de productos (default: 10)
   * @returns {Promise<Array>} Lista de productos frecuentes con cantidad total comprada
   */
  async obtenerProductosFrecuentes(email, limit = 10) {
    const response = await apiClient.get(`/ordenes/mis-productos-frecuentes?email=${encodeURIComponent(email)}&limit=${limit}`)
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
