import apiClient from './api'

export const inventarioService = {
  // Obtener movimientos de inventario (Kardex)
  async obtenerMovimientos(params = {}) {
    const {
      fechaDesde = '',
      fechaHasta = '',
      tipo = '',
      productoId = '',
      limite = 100
    } = params

    const queryParams = new URLSearchParams()
    if (fechaDesde) queryParams.append('fecha_desde', fechaDesde)
    if (fechaHasta) queryParams.append('fecha_hasta', fechaHasta)
    if (tipo) queryParams.append('tipo', tipo)
    if (productoId) queryParams.append('producto_id', productoId)
    queryParams.append('limite', limite)

    const response = await apiClient.get(`/inventario/movimientos?${queryParams}`)
    return response.data
  },

  // Obtener estadísticas de inventario
  async obtenerEstadisticas() {
    const response = await apiClient.get('/inventario/stats')
    return response.data
  }
}
