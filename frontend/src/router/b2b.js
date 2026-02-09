// =============================================================================
// B2B ROUTER - Portal Mayoristas (pro.dominio.com)
// Rutas exclusivas para el portal de mayoristas
// =============================================================================

import { createRouter, createWebHistory } from 'vue-router'

// B2B Layouts
const B2BLayout = () => import('../components/b2b/B2BLayout.vue')

// B2B Views (lazy loaded)
const B2BLogin = () => import('../components/b2b/B2BLogin.vue')
const B2BDashboard = () => import('../components/b2b/B2BDashboard.vue')
const B2BCatalogo = () => import('../components/b2b/B2BCatalogo.vue')
const B2BProductoDetalle = () => import('../components/b2b/B2BProductoDetalle.vue')
const B2BCarrito = () => import('../components/b2b/B2BCarrito.vue')
const B2BCheckoutPending = () => import('../components/b2b/B2BCheckoutPending.vue')
const B2BCheckout = () => import('../components/b2b/B2BCheckout.vue')
const B2BPedidos = () => import('../components/b2b/B2BPedidos.vue')
const B2BCuenta = () => import('../components/b2b/B2BCuenta.vue')
const B2BFavoritos = () => import('../components/b2b/B2BFavoritos.vue')
const B2BRegistro = () => import('../components/b2b/B2BRegistro.vue')
const B2BAyuda = () => import('../components/b2b/B2BAyuda.vue')
const B2BCupones = () => import('../components/b2b/B2BCupones.vue')
const B2BPagoResultado = () => import('../components/b2b/B2BPagoResultado.vue')

// Variable global para acceder al router desde listeners
let routerInstance = null
const routes = [
  // =========================================================================
  // RUTAS PÚBLICAS B2B
  // =========================================================================
  {
    path: '/',
    name: 'B2BHome',
    redirect: '/portal/login'  // B2B siempre inicia en login
  },
  {
    path: '/login',
    redirect: '/portal/login'
  },
  {
    path: '/registro',
    redirect: '/portal/registro'
  },
  {
    path: '/portal/login',
    name: 'B2BLogin',
    component: B2BLogin,
    meta: { 
      public: true,
      title: 'Acceso Mayoristas | Kharis Pro'
    }
  },
  {
    path: '/portal/registro',
    name: 'B2BRegistro',
    component: B2BRegistro,
    meta: { 
      public: true,
      title: 'Solicitar Cuenta Mayorista | Kharis Pro'
    }
  },

  // =========================================================================
  // RUTAS PROTEGIDAS B2B (requieren autenticación de mayorista)
  // =========================================================================
  {
    path: '/portal',
    component: B2BLayout,
    meta: { requiresB2BAuth: true },
    children: [
      {
        path: '',
        name: 'B2BDashboard',
        component: B2BDashboard,
        meta: { title: 'Mi Portal | Kharis Pro' }
      },
      {
        path: 'catalogo',
        name: 'B2BCatalogo',
        component: B2BCatalogo,
        meta: { title: 'Catálogo Mayorista | Kharis Pro' }
      },
      {
        path: 'producto/:id',
        name: 'B2BProductoDetalle',
        component: B2BProductoDetalle,
        meta: { title: 'Producto | Kharis Pro' }
      },
      {
        path: 'carrito',
        name: 'B2BCarrito',
        component: B2BCarrito,
        meta: { title: 'Mi Pedido | Kharis Pro' }
      },
      {
        path: 'checkout',
        name: 'B2BCheckoutPending',
        component: B2BCheckoutPending,
        meta: { title: 'Procesando... | Kharis Pro' }
      },
      {
        path: 'checkout/confirmar',
        name: 'B2BCheckout',
        component: B2BCheckout,
        meta: { title: 'Confirmar Pedido | Kharis Pro' }
      },
      {
        path: 'pedidos',
        name: 'B2BPedidos',
        redirect: '/portal/cuenta?tab=pedidos'
      },
      {
        path: 'favoritos',
        name: 'B2BFavoritos',
        component: B2BFavoritos,
        meta: { title: 'Mis Favoritos | Kharis Pro' }
      },
      {
        path: 'cuenta',
        name: 'B2BCuenta',
        component: B2BCuenta,
        meta: { title: 'Mi Cuenta | Kharis Pro' }
      },
      {
        path: 'pago-resultado',
        name: 'B2BPagoResultado',
        component: B2BPagoResultado,
        meta: { title: 'Resultado del Pago | Kharis Pro' }
      },
      {
        path: 'ayuda',
        name: 'B2BAyuda',
        component: B2BAyuda,
        meta: { title: 'Ayuda y PQR | Kharis Pro' }
      },
      {
        path: 'cupones',
        name: 'B2BCupones',
        redirect: '/portal/cuenta?tab=cupones'
      }
    ]
  },

  // =========================================================================
  // CATCH-ALL: Redirigir rutas no encontradas al login
  // =========================================================================
  {
    path: '/:pathMatch(.*)*',
    redirect: '/portal/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

// Guardar referencia al router para uso en listeners
routerInstance = router

// =============================================================================
// SINCRONIZACIÓN ENTRE PESTAÑAS
// Detectar cuando la sesión se cierra en otra pestaña
// =============================================================================
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (event) => {
    // Detectar cuando se elimina el token en otra pestaña
    if (event.key === 'b2b_access_token' && !event.newValue) {
      console.log('🔐 Sesión cerrada en otra pestaña - redirigiendo a login')
      
      // Limpiar estado
      localStorage.removeItem('b2b_user')
      localStorage.removeItem('b2b_refresh_token')
      
      // Redirigir a login si estamos en una ruta protegida
      if (routerInstance && routerInstance.currentRoute.value.meta?.requiresB2BAuth) {
        routerInstance.push({
          name: 'B2BLogin',
          query: { app: 'b2b' }
        })
      }
    }
  })
}

// =============================================================================
// NAVIGATION GUARDS B2B
// =============================================================================

router.beforeEach((to, from, next) => {
  // Actualizar título de la página
  if (to.meta.title) {
    document.title = to.meta.title
  }

  // Si la ruta es pública, permitir acceso
  if (to.meta.public) {
    next()
    return
  }

  // Verificar autenticación B2B - RUTAS PROTEGIDAS
  if (to.meta.requiresB2BAuth) {
    const b2bToken = localStorage.getItem('b2b_access_token')
    const b2bUserStr = localStorage.getItem('b2b_user')
    const b2bUser = JSON.parse(b2bUserStr || '{}')

    // Sin token → acceso denegado
    if (!b2bToken || !b2bUserStr) {
      next({ 
        name: 'B2BLogin',
        query: { 
          redirect: to.fullPath,
          app: 'b2b'
        } 
      })
      return
    }

    // Token existe pero sin usuario válido → acceso denegado
    if (!b2bUser.id && !b2bUser.es_mayorista && b2bUser.tipo !== 'MAYORISTA') {
      localStorage.removeItem('b2b_access_token')
      localStorage.removeItem('b2b_user')
      localStorage.removeItem('b2b_refresh_token')
      next({ 
        name: 'B2BLogin',
        query: { app: 'b2b' }
      })
      return
    }
  }

  next()
})

// Interceptar errores de navegación
router.onError((error) => {
  console.error('❌ [B2B Router Error]:', error)
})

export default router
