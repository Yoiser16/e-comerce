import apiClient from './api'

export const usuariosService = {
  /**
   * Obtener todos los usuarios del sistema (admin)
   * Nota: Este endpoint necesita ser creado en el backend
   */
  async obtenerTodos() {
    try {
      const response = await apiClient.get('/usuarios')
      return response.data
    } catch (error) {
      // Si el endpoint no existe, retornar datos del usuario actual
      console.warn('Endpoint /usuarios no disponible, retornando datos mock')
      return []
    }
  },

  /**
   * Crear nuevo usuario
   */
  async crear(usuarioData) {
    const response = await apiClient.post('/usuarios', usuarioData)
    return response.data
  },

  /**
   * Actualizar usuario
   */
  async actualizar(usuarioId, usuarioData) {
    const response = await apiClient.put(`/usuarios/${usuarioId}`, usuarioData)
    return response.data
  },

  /**
   * Eliminar usuario
   */
  async eliminar(usuarioId) {
    const response = await apiClient.delete(`/usuarios/${usuarioId}`)
    return response.data
  },

  /**
   * Cambiar estado activo/inactivo
   */
  async cambiarEstado(usuarioId, activo) {
    const response = await apiClient.patch(`/usuarios/${usuarioId}/estado`, { activo })
    return response.data
  }
}
