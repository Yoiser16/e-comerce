import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'

// Admin imports (lazy loaded)
const AdminLayout = () => import('../components/admin/AdminLayout.vue')
const AdminDashboard = () => import('../components/admin/AdminDashboard.vue')
const AdminProductos = () => import('../components/admin/AdminProductos.vue')
const AdminOrdenes = () => import('../components/admin/AdminOrdenes.vue')
const AdminClientes = () => import('../components/admin/AdminClientes.vue')
const AdminInventario = () => import('../components/admin/AdminInventario.vue')
const AdminUsuarios = () => import('../components/admin/AdminUsuarios.vue')
const AdminConfig = () => import('../components/admin/AdminConfig.vue')

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
  const accessToken = localStorage.getItem('access_token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  if (to.meta.requiresAuth && !accessToken) {
    // Redirect to login if not authenticated
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && user.rol !== 'ADMIN') {
    // Redirect non-admins away from admin pages
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
