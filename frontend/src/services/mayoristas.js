/**
 * Servicio para gestionar operaciones B2B (Mayoristas)
 * Conecta con el backend FastAPI para obtener productos, órdenes, etc.
 */

// URL del backend - en desarrollo apunta a localhost:8000
const BACKEND_URL = 'http://localhost:8000'
const API_BASE = `${BACKEND_URL}/api/v1`

console.log('🔌 API Service - Backend URL:', API_BASE)

/**
 * Obtiene los headers con el token de autenticación B2B
 */
function getAuthHeaders() {
  const token = localStorage.getItem('b2b_access_token')
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  }
}

/**
 * Maneja errores de autenticación y respuestas
 */
function handleAuthError(error) {
  console.error('❌ Error de respuesta:', error)
  if (error.status === 401) {
    // Token expirado o inválido - limpiar sesión
    localStorage.removeItem('b2b_access_token')
    localStorage.removeItem('b2b_refresh_token')
    localStorage.removeItem('b2b_user')
    
    // Redirigir a login
    window.location.href = '/login?app=b2b&expired=true'
  }
  throw error
}

/**
 * Obtiene el catálogo completo de productos
 * @param {Object} filters - Filtros opcionales (categoria, precio_min, precio_max, buscar, limit, etc.)
 * @returns {Promise<Array>}
 */
export async function obtenerProductos(filters = {}) {
  try {
    const params = new URLSearchParams()
    
    if (filters.categoria) params.append('categoria', filters.categoria)
    if (filters.activo !== undefined) params.append('activo', filters.activo)
    if (filters.limite) params.append('limite', filters.limite)
    if (filters.limit) params.append('limite', filters.limit)
    if (filters.buscar) params.append('buscar', filters.buscar)
    if (filters.oferta) params.append('oferta', 'true')
    if (filters.nuevo) params.append('nuevo', 'true')
    
    const queryString = params.toString()
      const url = `${API_BASE}/b2b/productos${queryString ? '?' + queryString : ''}`
    
    console.log('📡 GET:', url)
    const response = await fetch(url, {
      method: 'GET',
      headers: getAuthHeaders()
    })
    
    console.log('📦 Respuesta:', response.status, response.statusText)
    
    if (!response.ok) {
      handleAuthError({ status: response.status })
    }
    
    const data = await response.json()
    console.log('✅ Productos cargados:', data.length)
    return data
  } catch (error) {
    console.error('Error al obtener productos:', error)
    throw error
  }
}

/**
 * Obtiene productos destacados
 * @returns {Promise<Array>}
 */
export async function obtenerProductosDestacados() {
  try {
      const response = await fetch(`${API_BASE}/b2b/productos/destacados`, {
      method: 'GET',
      headers: getAuthHeaders()
    })
    
    if (!response.ok) {
      handleAuthError({ status: response.status })
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error al obtener productos destacados:', error)
    throw error
  }
}

/**
 * Obtiene detalle de un producto específico con precios mayoristas
 * @param {string} productoId - ID del producto
 * @returns {Promise<Object>}
 */
export async function obtenerProducto(productoId) {
  try {
    const response = await fetch(`${API_BASE}/b2b/productos/${productoId}`, {
      method: 'GET',
      headers: getAuthHeaders()
    })
    
    if (!response.ok) {
      handleAuthError({ status: response.status })
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error al obtener producto:', error)
    throw error
  }
}

/**
 * Obtiene las órdenes del usuario mayorista
 * @param {string} email - Email del mayorista
 * @returns {Promise<Array>}
 */
export async function obtenerMisPedidos(email) {
  try {
    const response = await fetch(`${API_BASE}/ordenes/mis-ordenes?email=${email}`, {
      method: 'GET',
      headers: getAuthHeaders()
    })
    
    if (!response.ok) {
      handleAuthError({ status: response.status })
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error al obtener pedidos:', error)
    throw error
  }
}

/**
 * Crea una nueva orden
 * @param {Object} ordenData - Datos de la orden
 * @returns {Promise<Object>}
 */
export async function crearOrden(ordenData) {
  try {
    const response = await fetch(`${API_BASE}/ordenes`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(ordenData)
    })
    
    if (!response.ok) {
      handleAuthError({ status: response.status })
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error al crear orden:', error)
    throw error
  }
}

/**
 * Valida el stock de productos antes de crear orden
 * @param {Array} items - Array de { producto_id, cantidad }
 * @returns {Promise<Object>}
 */
export async function validarStock(items) {
  try {
    const response = await fetch(`${API_BASE}/ordenes/validar-stock`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ items })
    })
    
    if (!response.ok) {
      handleAuthError({ status: response.status })
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error al validar stock:', error)
    throw error
  }
}

/**
 * Obtiene detalle de una orden específica
 * @param {string} ordenId - ID de la orden
 * @returns {Promise<Object>}
 */
export async function obtenerOrden(ordenId) {
  try {
    const response = await fetch(`${API_BASE}/ordenes/${ordenId}`, {
      method: 'GET',
      headers: getAuthHeaders()
    })
    
    if (!response.ok) {
      handleAuthError({ status: response.status })
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error al obtener orden:', error)
    throw error
  }
}

export default {
  obtenerProductos,
  obtenerProductosDestacados,
  obtenerProducto,
  obtenerMisPedidos,
  crearOrden,
  validarStock,
  obtenerOrden
}
