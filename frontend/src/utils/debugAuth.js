/**
 * Utilidad de debugging para autenticación B2B/B2C
 * 
 * Para usar en la consola del navegador:
 * window.debugAuth()
 */

export function debugAuth() {
  console.log('🔍 ========== DEBUG DE AUTENTICACIÓN ==========')
  
  // Tokens B2B
  const b2bAccess = localStorage.getItem('b2b_access_token')
  const b2bRefresh = localStorage.getItem('b2b_refresh_token')
  const b2bUserStr = localStorage.getItem('b2b_user')
  
  console.log('\n📦 Tokens B2B:')
  console.log('   Access Token:', b2bAccess ? `✅ Presente (${b2bAccess.substring(0, 30)}...)` : '❌ No encontrado')
  console.log('   Refresh Token:', b2bRefresh ? `✅ Presente (${b2bRefresh.substring(0, 30)}...)` : '❌ No encontrado')
  console.log('   User Data:', b2bUserStr ? '✅ Presente' : '❌ No encontrado')
  
  if (b2bUserStr) {
    try {
      const b2bUser = JSON.parse(b2bUserStr)
      console.log('   User Info:', {
        id: b2bUser.id,
        email: b2bUser.email,
        nombre: b2bUser.nombre,
        es_mayorista: b2bUser.es_mayorista,
        tipo: b2bUser.tipo
      })
    } catch (e) {
      console.error('   ❌ Error parseando user data:', e)
    }
  }
  
  // Tokens B2C
  const b2cAccess = localStorage.getItem('access_token')
  const b2cRefresh = localStorage.getItem('refresh_token')
  const b2cUserStr = localStorage.getItem('user')
  
  console.log('\n📦 Tokens B2C:')
  console.log('   Access Token:', b2cAccess ? `✅ Presente (${b2cAccess.substring(0, 30)}...)` : '❌ No encontrado')
  console.log('   Refresh Token:', b2cRefresh ? `✅ Presente (${b2cRefresh.substring(0, 30)}...)` : '❌ No encontrado')
  console.log('   User Data:', b2cUserStr ? '✅ Presente' : '❌ No encontrado')
  
  // URL y contexto
  console.log('\n🌐 Contexto de la Aplicación:')
  console.log('   URL:', window.location.href)
  console.log('   Hostname:', window.location.hostname)
  console.log('   Pathname:', window.location.pathname)
  
  // Resumen
  console.log('\n📊 Resumen:')
  const isB2B = !!b2bAccess || !!b2bRefresh
  const isB2C = !!b2cAccess || !!b2cRefresh
  console.log('   Tipo de sesión:', isB2B ? '🏭 B2B (Mayorista)' : isB2C ? '🛍️ B2C (Cliente)' : '❌ Sin sesión')
  console.log('   Estado:', (isB2B && b2bAccess && b2bRefresh) || (isB2C && b2cAccess && b2cRefresh) 
    ? '✅ Válida' 
    : '⚠️ Incompleta o expirada')
  
  console.log('\n💡 Comandos disponibles:')
  console.log('   window.clearB2BAuth() - Limpia sesión B2B')
  console.log('   window.clearB2CAuth() - Limpia sesión B2C')
  console.log('   window.clearAllAuth() - Limpia todas las sesiones')
  console.log('===========================================\n')
}

export function clearB2BAuth() {
  console.log('🧹 Limpiando autenticación B2B...')
  localStorage.removeItem('b2b_access_token')
  localStorage.removeItem('b2b_refresh_token')
  localStorage.removeItem('b2b_user')
  localStorage.removeItem('b2b_remember')
  console.log('✅ Sesión B2B limpiada')
}

export function clearB2CAuth() {
  console.log('🧹 Limpiando autenticación B2C...')
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  console.log('✅ Sesión B2C limpiada')
}

export function clearAllAuth() {
  console.log('🧹 Limpiando TODAS las sesiones...')
  clearB2BAuth()
  clearB2CAuth()
  localStorage.clear()
  console.log('✅ Todas las sesiones limpiadas')
  console.log('💡 Recarga la página para aplicar cambios')
}

// Exponer funciones globalmente para debugging
if (typeof window !== 'undefined') {
  window.debugAuth = debugAuth
  window.clearB2BAuth = clearB2BAuth
  window.clearB2CAuth = clearB2CAuth
  window.clearAllAuth = clearAllAuth
}
