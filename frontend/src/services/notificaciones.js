import apiClient from './api'

export async function listarNotificaciones({ limit = 10, offset = 0, soloNoLeidas = false } = {}) {
  const response = await apiClient.get('/notificaciones', {
    params: { limit, offset, solo_no_leidas: soloNoLeidas }
  })
  return response.data
}

export async function marcarNotificacionLeida(id) {
  const response = await apiClient.post(`/notificaciones/${id}/leer`)
  return response.data
}

export async function marcarTodasLeidas() {
  const response = await apiClient.post('/notificaciones/leer-todas')
  return response.data
}

export default {
  listarNotificaciones,
  marcarNotificacionLeida,
  marcarTodasLeidas
}
