// =============================================================================
// ROUTER INDEX - Re-export del router B2C para compatibilidad
// =============================================================================
// Este archivo mantiene la compatibilidad con imports existentes.
// La lógica real de routing ahora está en:
// - b2c.js: Rutas de la tienda retail (dominio principal)
// - b2b.js: Rutas del portal mayoristas (pro.*)
// 
// La selección del router se hace en main.js basándose en el subdominio.
// =============================================================================

// Re-exportar el router B2C como default para compatibilidad
export { default } from './b2c.js'

