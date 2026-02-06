// =============================================================================
// SUBDOMAIN DETECTION UTILITY
// Detecta el subdominio actual y determina el contexto de la aplicación
// =============================================================================

/**
 * Subdominios reconocidos por el sistema
 */
export const SUBDOMAINS = {
  PRO: 'pro',        // B2B - Mayoristas
  ADMIN: 'admin',    // Panel administrativo (futuro)
  WWW: 'www',        // Principal (equivale a sin subdominio)
}

/**
 * Contextos de aplicación
 */
export const APP_CONTEXT = {
  B2C: 'b2c',        // Tienda retail (default)
  B2B: 'b2b',        // Portal mayoristas
  ADMIN: 'admin',    // Panel admin (futuro, si se separa)
}

/**
 * Extrae el subdominio del hostname actual
 * @returns {string|null} El subdominio o null si no hay
 * 
 * Ejemplos:
 * - "pro.kharisdistribuidora.com" → "pro"
 * - "www.kharisdistribuidora.com" → "www"
 * - "kharisdistribuidora.com" → null
 * - "pro.localhost" → "pro"
 * - "localhost" → null
 * - "127.0.0.1" → null
 * 
 * DEV MODE: Usa ?app=b2b o ?app=b2c en la URL para forzar el modo
 */
export function getSubdomain() {
  // =========================================================================
  // DEV MODE: Permitir forzar el contexto via URL params
  // Ejemplo: http://localhost:5173/?app=b2b
  // =========================================================================
  if (typeof window !== 'undefined') {
    const urlParams = new URLSearchParams(window.location.search)
    const forceApp = urlParams.get('app')
    if (forceApp === 'b2b') return SUBDOMAINS.PRO
    if (forceApp === 'b2c') return null
  }
  
  const hostname = window.location.hostname
  
  // Caso: IP directa (desarrollo local)
  if (/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(hostname)) {
    return null
  }
  
  // Caso: localhost con subdominio (pro.localhost)
  if (hostname.endsWith('.localhost')) {
    return hostname.replace('.localhost', '')
  }
  
  // Caso: localhost sin subdominio
  if (hostname === 'localhost') {
    return null
  }
  
  // Caso: Dominio real
  const parts = hostname.split('.')
  
  // dominio.com (2 partes) → sin subdominio
  if (parts.length <= 2) {
    return null
  }
  
  // sub.dominio.com (3+ partes) → subdominio
  // Excluir 'www' como subdominio real
  const subdomain = parts[0]
  return subdomain === 'www' ? null : subdomain
}

/**
 * Determina el contexto de aplicación basado en el subdominio
 * @returns {string} El contexto de la aplicación (b2c, b2b, admin)
 */
export function getAppContext() {
  const subdomain = getSubdomain()
  
  switch (subdomain) {
    case SUBDOMAINS.PRO:
      return APP_CONTEXT.B2B
    case SUBDOMAINS.ADMIN:
      return APP_CONTEXT.ADMIN
    default:
      return APP_CONTEXT.B2C
  }
}

/**
 * Verifica si estamos en contexto B2B (mayoristas)
 * @returns {boolean}
 */
export function isB2B() {
  return getAppContext() === APP_CONTEXT.B2B
}

/**
 * Verifica si estamos en contexto B2C (retail)
 * @returns {boolean}
 */
export function isB2C() {
  return getAppContext() === APP_CONTEXT.B2C
}

/**
 * Obtiene la URL base para el contexto opuesto
 * Útil para enlaces entre B2C ↔ B2B
 * @param {string} targetContext - El contexto destino ('b2b' o 'b2c')
 * @returns {string} La URL base del contexto destino
 */
export function getCrossContextUrl(targetContext) {
  const { protocol, hostname, port } = window.location
  const portSuffix = port ? `:${port}` : ''
  
  // Extraer dominio base
  let baseDomain = hostname
  const subdomain = getSubdomain()
  
  if (subdomain) {
    // Remover subdominio actual
    baseDomain = hostname.substring(subdomain.length + 1)
  }
  
  // Construir URL según contexto destino
  if (targetContext === APP_CONTEXT.B2B) {
    if (baseDomain === 'localhost') {
      return `${protocol}//pro.localhost${portSuffix}`
    }
    return `${protocol}//pro.${baseDomain}${portSuffix}`
  }
  
  // B2C - dominio sin subdominio
  if (baseDomain === 'localhost') {
    return `${protocol}//localhost${portSuffix}`
  }
  return `${protocol}//${baseDomain}${portSuffix}`
}

/**
 * Debug: Imprime información del contexto actual
 */
export function debugSubdomain() {
  console.group('🌐 Subdomain Detection')
  console.log('Hostname:', window.location.hostname)
  console.log('Subdomain:', getSubdomain())
  console.log('App Context:', getAppContext())
  console.log('Is B2B:', isB2B())
  console.log('Is B2C:', isB2C())
  console.groupEnd()
}

export default {
  getSubdomain,
  getAppContext,
  isB2B,
  isB2C,
  getCrossContextUrl,
  debugSubdomain,
  SUBDOMAINS,
  APP_CONTEXT,
}
