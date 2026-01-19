import apiClient from './api'

export const clientesService = {
  /**
   * Obtener todos los clientes (admin)
   */
  async obtenerTodos() {
    const response = await apiClient.get('/clientes')
    return response.data
  },

  /**
   * Obtener un cliente por ID
   */
  async obtenerPorId(clienteId) {
    const response = await apiClient.get(`/clientes/${clienteId}`)
    return response.data
  },

  /**
   * Crear nuevo cliente
   */
  async crear(clienteData) {
    const response = await apiClient.post('/clientes', clienteData)
    return response.data
  },

  /**
   * Actualizar cliente
   */
  async actualizar(clienteId, clienteData) {
    const response = await apiClient.put(`/clientes/${clienteId}`, clienteData)
    return response.data
  },

  /**
   * Eliminar cliente
   */
  async eliminar(clienteId) {
    const response = await apiClient.delete(`/clientes/${clienteId}`)
    return response.data
  }
}
