// =============================================================================
// MAIN.JS - Application Bootstrap con Subdomain Routing Split
// =============================================================================
// Este archivo detecta el subdominio y carga la aplicación correspondiente:
// - B2C (dominio principal): Tienda retail para consumidores
// - B2B (pro.*): Portal exclusivo para mayoristas
// =============================================================================

import { createApp } from 'vue'
import './style.css'
import { getAppContext, debugSubdomain, APP_CONTEXT } from './utils/subdomain'

// Importar utilidades de debug (solo en desarrollo)
if (import.meta.env.DEV) {
  import('./utils/debugAuth.js')
}

/**
 * Bootstrap de la aplicación según el contexto detectado
 */
async function bootstrap() {
  let context = getAppContext()
  const currentPath = window.location?.pathname || '/'

  // Si la ruta es /portal, forzar contexto B2B
  if (currentPath.startsWith('/portal')) {
    context = APP_CONTEXT.B2B
  }
  
  let App, router

  switch (context) {
    // =========================================================================
    // B2B - Portal Mayoristas (pro.dominio.com)
    // =========================================================================
    case APP_CONTEXT.B2B:
      // Importar dinámicamente App y Router B2B
      const b2bModule = await import('./AppB2B.vue')
      const b2bRouter = await import('./router/b2b.js')
      
      App = b2bModule.default
      router = b2bRouter.default
      
      // Agregar clase al body para estilos específicos B2B
      document.body.classList.add('app-b2b')
      document.title = 'Kharis Pro | Portal Mayoristas'
      break

    // =========================================================================
    // B2C - Tienda Retail (dominio principal, www, o localhost)
    // =========================================================================
    case APP_CONTEXT.B2C:
    default:
      console.log('🛒 Iniciando aplicación B2C (Retail)')
      
      // Importar App y Router B2C (tienda actual)
      const b2cModule = await import('./App.vue')
      const b2cRouter = await import('./router/b2c.js')
      
      App = b2cModule.default
      router = b2cRouter.default
      
      // Clase para estilos B2C
      document.body.classList.add('app-b2c')
      break
  }

  // Crear y montar la aplicación
  const app = createApp(App)
  
  // Proveer el contexto globalmente (útil para componentes)
  app.provide('appContext', context)
  app.provide('isB2B', context === APP_CONTEXT.B2B)
  app.provide('isB2C', context === APP_CONTEXT.B2C)
  
  app.use(router)
  app.mount('#app')
}

// Ejecutar bootstrap
bootstrap().catch((error) => {
  console.error('❌ Error al inicializar la aplicación:', error)
  
  // Mostrar error amigable al usuario
  document.getElementById('app').innerHTML = `
    <div style="display: flex; align-items: center; justify-content: center; height: 100vh; font-family: system-ui;">
      <div style="text-align: center; padding: 2rem;">
        <h1 style="color: #1A1A1A; margin-bottom: 1rem;">Oops! Algo salió mal</h1>
        <p style="color: #7A7A7A;">Por favor, recarga la página o intenta más tarde.</p>
        <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.75rem 1.5rem; background: #1A1A1A; color: white; border: none; cursor: pointer;">
          Recargar
        </button>
      </div>
    </div>
  `
})
