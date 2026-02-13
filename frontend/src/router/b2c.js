// =============================================================================
// B2C ROUTER - Tienda Retail (dominio principal)
// Este es el router original de la tienda, extraído para modularidad
// =============================================================================

import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'

// Cliente imports (lazy loaded)
const Catalogo = () => import('../components/Catalogo.vue')
const ProductoDetalle = () => import('../components/ProductoDetalle.vue')
const MiCuenta = () => import('../components/MiCuenta.vue')
const Checkout = () => import('../components/Checkout.vue')
const PagoExitoso = () => import('../components/PagoExitoso.vue')
const PedidoConfirmado = () => import('../components/PedidoConfirmado.vue')

// Admin imports (lazy loaded)
const AdminLayout = () => import('../components/admin/AdminLayout.vue')
const AdminDashboard = () => import('../components/admin/AdminDashboard.vue')
const AdminProductos = () => import('../components/admin/AdminProductos.vue')
const ProductoForm = () => import('../components/admin/ProductoForm.vue')
const AdminOrdenes = () => import('../components/admin/AdminOrdenes.vue')
const AdminClientes = () => import('../components/admin/AdminClientes.vue')
const AdminInventario = () => import('../components/admin/AdminInventario.vue')
const AdminUsuarios = () => import('../components/admin/AdminUsuarios.vue')
const AdminConfig = () => import('../components/admin/AdminConfig.vue')
const AdminCategorias = () => import('../components/admin/AdminCategorias.vue')
const AdminMayoristas = () => import('../components/admin/AdminMayoristas.vue')
const AdminResenas = () => import('../components/admin/AdminResenas.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/catalogo',
    name: 'Catalogo',
    component: Catalogo
  },
  {
    path: '/producto/:id',
    name: 'ProductoDetalle',
    component: ProductoDetalle
  },
  {
    path: '/mi-cuenta',
    name: 'MiCuenta',
    component: MiCuenta,
    meta: { requiresAuth: true }
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: Checkout
  },
  {
    path: '/pago-exitoso',
    name: 'PagoExitoso',
    component: PagoExitoso
  },
  {
    path: '/pedido-confirmado',
    name: 'PedidoConfirmado',
    component: PedidoConfirmado
  },
  // Admin routes
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { title: 'Dashboard' }
      },
      {
        path: 'productos',
        name: 'AdminProductos',
        component: AdminProductos,
        meta: { title: 'Productos' }
      },
      {
        path: 'productos/nuevo',
        name: 'ProductoNuevo',
        component: ProductoForm,
        meta: { title: 'Nuevo Producto' }
      },
      {
        path: 'productos/:id/editar',
        name: 'ProductoEditar',
        component: ProductoForm,
        meta: { title: 'Editar Producto' }
      },
      {
        path: 'ordenes',
        name: 'AdminOrdenes',
        component: AdminOrdenes,
        meta: { title: 'Órdenes' }
      },
      {
        path: 'clientes',
        name: 'AdminClientes',
        component: AdminClientes,
        meta: { title: 'Clientes' }
      },
      {
        path: 'inventario',
        name: 'AdminInventario',
        component: AdminInventario,
        meta: { title: 'Inventario' }
      },
      {
        path: 'categorias',
        name: 'AdminCategorias',
        component: AdminCategorias,
        meta: { title: 'Categorías' }
      },
      {
        path: 'usuarios',
        name: 'AdminUsuarios',
        component: AdminUsuarios,
        meta: { title: 'Usuarios' }
      },
      {
        path: 'config',
        name: 'AdminConfig',
        component: AdminConfig,
        meta: { title: 'Configuración' }
      },
      {
        path: 'mayoristas',
        name: 'AdminMayoristas',
        component: AdminMayoristas,
        meta: { title: 'Mayoristas B2B' }
      },
      {
        path: 'resenas',
        name: 'AdminResenas',
        component: AdminResenas,
        meta: { title: 'Reseñas' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return false
    }
    return { top: 0 }
  }
})

// Navigation guard for auth routes
router.beforeEach((to, from, next) => {
  // =========================================================================
  // REDIRECCIÓN B2B: Si intenta acceder a /portal en B2C, redirigir a B2B login
  // =========================================================================
  if (to.path.startsWith('/portal')) {
    console.log('⚠️ Intento de acceso a /portal en contexto B2C - Redirigiendo a B2B login')
    // Redirigir a login B2B en /portal
    window.location.href = `/portal/login?redirect=${encodeURIComponent(to.fullPath)}`
    return
  }
  
  // Capturar tokens de la URL (para login de admin en nueva pestaña)
  if (to.query.token && to.query.refresh) {
    console.log('Procesando tokens de URL para admin...')
    localStorage.setItem('access_token', to.query.token)
    localStorage.setItem('refresh_token', to.query.refresh)
    
    try {
      const payload = JSON.parse(atob(to.query.token.split('.')[1]))
      const user = {
        id: payload.user_id,
        email: payload.email,
        nombre: payload.nombre,
        rol: payload.rol
      }
      localStorage.setItem('user', JSON.stringify(user))
      console.log('Token procesado, usuario:', user)
    } catch (e) {
      console.warn('No se pudo decodificar el token:', e)
    }
    
    const cleanPath = to.path
    next({ path: cleanPath, replace: true })
    return
  }
  
  const accessToken = localStorage.getItem('access_token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  if (to.meta.requiresAuth && !accessToken) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && !['ADMIN', 'OPERADOR'].includes(user.rol)) {
    console.warn('Acceso denegado: Se requiere rol ADMIN o OPERADOR')
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
