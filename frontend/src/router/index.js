import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'

// Cliente imports (lazy loaded)
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
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

// Navigation guard for admin routes
router.beforeEach((to, from, next) => {
  // PRIMERO: Capturar tokens de la URL (para login de admin en nueva pestaña)
  if (to.query.token && to.query.refresh) {
    console.log('Procesando tokens de URL para admin...')
    localStorage.setItem('access_token', to.query.token)
    localStorage.setItem('refresh_token', to.query.refresh)
    
    // Decodificar el JWT para obtener info del usuario
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
    
    // Limpiar los tokens de la URL y continuar a la ruta limpia
    const cleanPath = to.path
    next({ path: cleanPath, replace: true })
    return
  }
  
  const accessToken = localStorage.getItem('access_token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  if (to.meta.requiresAuth && !accessToken) {
    // Redirect to login if not authenticated
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && !['ADMIN', 'OPERADOR'].includes(user.rol)) {
    // Redirect non-admins/operadores away from admin pages
    console.warn('Acceso denegado: Se requiere rol ADMIN o OPERADOR')
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
