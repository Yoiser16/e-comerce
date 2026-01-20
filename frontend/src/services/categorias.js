/**
 * Servicio para gestión de Categorías
 */
import api from './api'

export const categoriasService = {
  /**
   * Lista todas las categorías
   * @param {Object} filtros - Filtros opcionales
   * @param {boolean} filtros.soloActivas - Solo categorías activas
   * @param {boolean} filtros.soloHome - Solo las que se muestran en home
   */
  async listar(filtros = {}) {
    const params = new URLSearchParams()
    if (filtros.soloActivas) params.append('solo_activas', 'true')
    if (filtros.soloHome) params.append('solo_home', 'true')
    
    const query = params.toString()
    const url = query ? `/categorias/?${query}` : '/categorias/'
    const response = await api.get(url)
    return response.data
  },

  /**
   * Lista categorías para el home del ecommerce
   */
  async listarHome() {
    const response = await api.get('/categorias/home')
    return response.data
  },

  /**
   * Obtiene una categoría por ID
   */
  async obtener(id) {
    const response = await api.get(`/categorias/${id}`)
    return response.data
  },

  /**
   * Crea una nueva categoría
   * @param {Object} datos
   * @param {string} datos.nombre - Nombre de la categoría
   * @param {string} datos.descripcion - Descripción
   * @param {string} datos.descripcion_corta - Descripción corta para tarjetas
   * @param {string} datos.imagen - URL de la imagen
   * @param {number} datos.prioridad - 1=grande, 2-3=pequeño
   * @param {number} datos.orden - Orden dentro del nivel de prioridad
   * @param {boolean} datos.activo - Estado activo
   * @param {boolean} datos.mostrar_en_home - Mostrar en página principal
   */
  async crear(datos) {
    const response = await api.post('/categorias/', datos)
    return response.data
  },

  /**
   * Actualiza una categoría existente
   */
  async actualizar(id, datos) {
    const response = await api.put(`/categorias/${id}`, datos)
    return response.data
  },

  /**
   * Elimina una categoría
   */
  async eliminar(id) {
    await api.delete(`/categorias/${id}`)
  }
}

export default categoriasService
