// =============================================================================
// WOMPI PAYMENT SERVICE - Pasarela de Pagos Colombia
// Modo: Sandbox/Test
// =============================================================================

const WOMPI_CONFIG = {
  publicKey: import.meta.env.VITE_WOMPI_PUBLIC_KEY || 'pub_test_ZVH2hPZRCY7iVcPAyCCh53E5cS2SUFmW',
  environment: import.meta.env.VITE_WOMPI_ENVIRONMENT || 'sandbox',
  currency: 'COP',
  get baseUrl() {
    return this.environment === 'production'
      ? 'https://production.wompi.co/v1'
      : 'https://sandbox.wompi.co/v1'
  },
  get checkoutUrl() {
    return 'https://checkout.wompi.co/p/'
  }
}

/**
 * Genera una referencia única para la transacción
 * Formato: B2B-{timestamp}-{random}
 */
export function generateReference(prefix = 'B2B') {
  const timestamp = Date.now()
  const random = Math.random().toString(36).substring(2, 8).toUpperCase()
  return `${prefix}-${timestamp}-${random}`
}

/**
 * Convierte pesos colombianos a centavos (Wompi requiere centavos)
 */
export function toCents(amount) {
  return Math.round(amount * 100)
}

/**
 * Convierte centavos a pesos colombianos
 */
export function fromCents(amountInCents) {
  return amountInCents / 100
}

/**
 * Carga el SDK de Wompi Widget en el DOM
 */
export function loadWompiSDK() {
  return new Promise((resolve, reject) => {
    if (document.querySelector('script[src*="checkout.wompi.co"]')) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = 'https://checkout.wompi.co/widget.js'
    script.async = true
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

/**
 * Obtiene la firma de integridad del backend
 * La firma se calcula server-side para no exponer el secreto de integridad
 * 
 * @param {string} reference - Referencia de la transacción
 * @param {number} amountInCents - Monto en centavos
 * @param {string} currency - Moneda (default: COP)
 * @returns {Promise<string>} Hash SHA-256 de integridad
 */
export async function getIntegritySignature(reference, amountInCents, currency = 'COP') {
  const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/api\/v1\/?$/, '')
  const response = await fetch(`${API_URL}/api/v1/wompi/integrity-signature`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reference, amount_in_cents: amountInCents, currency })
  })
  if (!response.ok) throw new Error(`Error obteniendo firma: HTTP ${response.status}`)
  const data = await response.json()
  return data.signature
}

/**
 * Construye la URL de redirección a Wompi Checkout
 * ASYNC porque necesita obtener la firma de integridad del backend
 * 
 * @param {Object} params - Parámetros del checkout
 * @param {number} params.amountInCents - Monto en centavos
 * @param {string} params.reference - Referencia única de la transacción
 * @param {string} params.redirectUrl - URL a la que redirigir después del pago
 * @param {string} params.email - Email del cliente
 * @param {string} params.fullName - Nombre completo del cliente
 * @param {string} params.phone - Teléfono del cliente
 * @returns {Promise<string>} URL completa del checkout de Wompi
 */
export async function buildCheckoutUrl({
  amountInCents,
  reference,
  redirectUrl,
  email,
  fullName,
  phone
}) {
  // Obtener firma de integridad del backend
  const signature = await getIntegritySignature(reference, amountInCents, WOMPI_CONFIG.currency)
  
  // Construir URL manualmente para evitar que URLSearchParams
  // codifique los ":" en los nombres de parámetros customer-data:xxx
  const cleanPhone = phone.replace(/\D/g, '').slice(-10)
  
  const params = [
    `public-key=${encodeURIComponent(WOMPI_CONFIG.publicKey)}`,
    `currency=${WOMPI_CONFIG.currency}`,
    `amount-in-cents=${amountInCents}`,
    `reference=${encodeURIComponent(reference)}`,
    `signature:integrity=${signature}`,
    `redirect-url=${encodeURIComponent(redirectUrl)}`,
    `customer-data:email=${encodeURIComponent(email)}`,
    `customer-data:full-name=${encodeURIComponent(fullName)}`,
    `customer-data:phone-number=${cleanPhone}`,
    `customer-data:phone-number-prefix=57`
  ].join('&')

  return `${WOMPI_CONFIG.checkoutUrl}?${params}`
}

/**
 * Consulta el estado de una transacción en Wompi
 * 
 * @param {string} transactionId - ID de la transacción de Wompi
 * @returns {Promise<Object>} Datos de la transacción
 */
export async function getTransactionStatus(transactionId) {
  try {
    const response = await fetch(`${WOMPI_CONFIG.baseUrl}/transactions/${transactionId}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const data = await response.json()
    return data.data
  } catch (error) {
    console.error('Error consultando transacción Wompi:', error)
    throw error
  }
}

/**
 * Consulta una transacción por su referencia
 * 
 * @param {string} reference - Referencia de la transacción
 * @returns {Promise<Object>} Datos de la transacción
 */
export async function getTransactionByReference(reference) {
  try {
    const response = await fetch(`${WOMPI_CONFIG.baseUrl}/transactions?reference=${reference}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const data = await response.json()
    return data.data?.[0] || null
  } catch (error) {
    console.error('Error consultando transacción por referencia:', error)
    throw error
  }
}

/**
 * Mapea el estado de Wompi a un estado legible
 */
export function mapTransactionStatus(wompiStatus) {
  const statusMap = {
    'APPROVED': { status: 'approved', label: 'Aprobado', color: 'green' },
    'DECLINED': { status: 'rejected', label: 'Rechazado', color: 'red' },
    'VOIDED': { status: 'rejected', label: 'Anulado', color: 'red' },
    'ERROR': { status: 'rejected', label: 'Error', color: 'red' },
    'PENDING': { status: 'pending', label: 'Pendiente', color: 'amber' }
  }
  return statusMap[wompiStatus] || { status: 'unknown', label: 'Desconocido', color: 'gray' }
}

/**
 * Obtiene los medios de pago aceptados por Wompi
 */
export async function getAcceptedPaymentMethods() {
  try {
    const response = await fetch(`${WOMPI_CONFIG.baseUrl}/merchants/${WOMPI_CONFIG.publicKey}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const data = await response.json()
    return data.data?.accepted_payment_methods || []
  } catch (error) {
    console.error('Error obteniendo métodos de pago:', error)
    return []
  }
}

export default {
  ...WOMPI_CONFIG,
  generateReference,
  toCents,
  fromCents,
  loadWompiSDK,
  getIntegritySignature,
  buildCheckoutUrl,
  getTransactionStatus,
  getTransactionByReference,
  mapTransactionStatus,
  getAcceptedPaymentMethods
}
