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
const B2BPedidos = () => import('../components/b2b/B2BPedidos.vue')
const B2BCuenta = () => import('../components/b2b/B2BCuenta.vue')
const B2BRegistro = () => import('../components/b2b/B2BRegistro.vue')

const routes = [
  // =========================================================================
  // RUTAS PÚBLICAS B2B
  // =========================================================================
  {
    path: '/',
    name: 'B2BHome',
    redirect: '/login'  // B2B siempre inicia en login
  },
  {
    path: '/login',
    name: 'B2BLogin',
    component: B2BLogin,
    meta: { 
      public: true,
      title: 'Acceso Mayoristas | Kharis Pro'
    }
  },
  {
    path: '/registro',
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
        path: 'pedidos',
        name: 'B2BPedidos',
        component: B2BPedidos,
        meta: { title: 'Mis Pedidos | Kharis Pro' }
      },
      {
        path: 'cuenta',
        name: 'B2BCuenta',
        component: B2BCuenta,
        meta: { title: 'Mi Cuenta | Kharis Pro' }
      }
    ]
  },

  // =========================================================================
  // CATCH-ALL: Redirigir rutas no encontradas al login
  // =========================================================================
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
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

  // Verificar autenticación B2B
  if (to.meta.requiresB2BAuth) {
    const b2bToken = localStorage.getItem('b2b_access_token')
    const b2bUser = JSON.parse(localStorage.getItem('b2b_user') || '{}')

    if (!b2bToken) {
      // No autenticado → redirigir a login
      next({ 
        name: 'B2BLogin', 
        query: { redirect: to.fullPath } 
      })
      return
    }

    // Verificar que el usuario tenga rol de mayorista
    if (!b2bUser.es_mayorista && b2bUser.tipo !== 'MAYORISTA') {
      console.warn('Acceso denegado: Se requiere cuenta de mayorista')
      localStorage.removeItem('b2b_access_token')
      localStorage.removeItem('b2b_user')
      next({ name: 'B2BLogin' })
      return
    }
  }

  next()
})

// Interceptar errores de navegación
router.onError((error) => {
  console.error('B2B Router Error:', error)
})

export default router
