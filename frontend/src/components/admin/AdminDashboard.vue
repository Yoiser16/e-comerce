<template>
  <div class="space-y-8">
    
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
      <p class="text-red-600 mb-4">{{ error }}</p>
      <button @click="cargarDatos" class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
        Reintentar
      </button>
    </div>

    <!-- Content -->
    <div v-else>
    
    <!-- Welcome Section - Clean & Elegant -->
    <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6">
      <div>
        <h1 class="font-luxury text-3xl lg:text-4xl text-text-dark mb-2">
          Hola, {{ userName }}
        </h1>
        <p class="text-text-medium text-lg">Aquí está el resumen de tu tienda hoy.</p>
      </div>
      <router-link 
        to="/admin/productos/nuevo"
        class="inline-flex items-center gap-2.5 bg-text-dark hover:bg-black text-white font-medium px-6 py-3.5 rounded-xl transition-all hover:shadow-lg hover:shadow-black/10"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        Nuevo Producto
      </router-link>
    </div>

    <!-- Stats Grid - Clean Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <!-- Total Ventas -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_4px_20px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.08)] transition-shadow">
        <div class="flex items-start justify-between mb-6">
          <svg class="w-7 h-7 text-text-light" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-green-600 text-sm font-medium flex items-center gap-1">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" />
            </svg>
            +12.5%
          </span>
        </div>
        <h3 class="text-3xl font-light text-text-dark tracking-tight">${{ formatNumber(stats.totalVentas) }}</h3>
        <p class="text-text-light text-sm mt-1">Ventas este mes</p>
      </div>

      <!-- Órdenes -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_4px_20px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.08)] transition-shadow">
        <div class="flex items-start justify-between mb-6">
          <svg class="w-7 h-7 text-text-light" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
          </svg>
          <span class="text-blue-600 text-sm font-medium">{{ stats.ordenesPendientes }} pendientes</span>
        </div>
        <h3 class="text-3xl font-light text-text-dark tracking-tight">{{ stats.totalOrdenes }}</h3>
        <p class="text-text-light text-sm mt-1">Órdenes totales</p>
      </div>

      <!-- Productos -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_4px_20px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.08)] transition-shadow">
        <div class="flex items-start justify-between mb-6">
          <svg class="w-7 h-7 text-text-light" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
          </svg>
          <span class="text-amber-600 text-sm font-medium">{{ stats.stockBajo }} stock bajo</span>
        </div>
        <h3 class="text-3xl font-light text-text-dark tracking-tight">{{ stats.totalProductos }}</h3>
        <p class="text-text-light text-sm mt-1">Productos activos</p>
      </div>

      <!-- Clientes -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_4px_20px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.08)] transition-shadow">
        <div class="flex items-start justify-between mb-6">
          <svg class="w-7 h-7 text-text-light" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
          </svg>
          <span class="text-green-600 text-sm font-medium">+{{ stats.clientesNuevos }} nuevos</span>
        </div>
        <h3 class="text-3xl font-light text-text-dark tracking-tight">{{ stats.totalClientes }}</h3>
        <p class="text-text-light text-sm mt-1">Clientes registrados</p>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid lg:grid-cols-3 gap-8">
      
      <!-- Recent Orders - Magazine Style -->
      <div class="lg:col-span-2 bg-white rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.04)]">
        <div class="flex items-center justify-between p-6 border-b border-gray-50">
          <h3 class="text-lg font-medium text-text-dark">Últimas Órdenes</h3>
          <router-link to="/admin/ordenes" class="text-brand-600 text-sm font-medium hover:text-brand-700 transition-colors">
            Ver todas
          </router-link>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-50">
                <th class="px-6 py-4 text-left text-xs font-semibold text-text-light uppercase tracking-wider">Orden</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-text-light uppercase tracking-wider">Cliente</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-text-light uppercase tracking-wider">Estado</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-text-light uppercase tracking-wider">Total</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-text-light uppercase tracking-wider">Fecha</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="orden in recentOrders" :key="orden.id" class="hover:bg-gray-50/50 transition-colors">
                <td class="px-6 py-4">
                  <span class="font-mono text-sm text-text-dark">#{{ orden.id.slice(0, 8) }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-text-dark">{{ orden.cliente }}</span>
                </td>
                <td class="px-6 py-4">
                  <span :class="getStatusClass(orden.estado)" class="px-3 py-1.5 text-xs font-medium rounded-full">
                    {{ getStatusLabel(orden.estado) }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span class="font-medium text-text-dark">${{ formatNumber(orden.total) }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-text-light text-sm">{{ orden.fecha }}</span>
                </td>
              </tr>
              <tr v-if="recentOrders.length === 0">
                <td colspan="5" class="px-6 py-12 text-center text-text-light">
                  No hay órdenes recientes
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Low Stock Products - Magazine Style -->
      <div class="bg-white rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.04)]">
        <div class="flex items-center justify-between p-6 border-b border-gray-50">
          <h3 class="text-lg font-medium text-text-dark">Stock Bajo</h3>
          <router-link to="/admin/inventario" class="text-brand-600 text-sm font-medium hover:text-brand-700 transition-colors">
            Ver todo
          </router-link>
        </div>
        <div class="p-4 space-y-3">
          <div 
            v-for="product in lowStockProducts" 
            :key="product.id"
            class="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-50 transition-colors group"
          >
            <!-- Larger Product Image -->
            <div class="w-16 h-16 bg-gray-100 rounded-xl overflow-hidden flex-shrink-0 shadow-sm">
              <img 
                :src="product.imagen" 
                :alt="product.nombre" 
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              >
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-text-dark truncate">{{ product.nombre }}</p>
              <p class="text-sm text-brand-600 font-medium">Solo {{ product.stock }} unidades</p>
            </div>
            <button class="p-2 text-text-light hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
            </button>
          </div>
          
          <div v-if="lowStockProducts.length === 0" class="text-center py-10">
            <svg class="w-12 h-12 mx-auto mb-3 text-green-200" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-text-light">Todo el inventario OK</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions - Minimal -->
    <div class="bg-white rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.04)] p-6">
      <h3 class="text-lg font-medium text-text-dark mb-6">Acciones Rápidas</h3>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        
        <router-link 
          to="/admin/productos/nuevo"
          class="flex flex-col items-center gap-3 p-5 border border-gray-100 rounded-2xl hover:border-brand-200 hover:bg-brand-50/30 transition-all group"
        >
          <div class="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center group-hover:bg-brand-100 transition-colors">
            <svg class="w-5 h-5 text-text-light group-hover:text-brand-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
          </div>
          <span class="text-sm font-medium text-text-medium group-hover:text-brand-600 transition-colors">Nuevo Producto</span>
        </router-link>

        <router-link 
          to="/admin/ordenes"
          class="flex flex-col items-center gap-3 p-5 border border-gray-100 rounded-2xl hover:border-blue-200 hover:bg-blue-50/30 transition-all group"
        >
          <div class="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center group-hover:bg-blue-100 transition-colors">
            <svg class="w-5 h-5 text-text-light group-hover:text-blue-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
            </svg>
          </div>
          <span class="text-sm font-medium text-text-medium group-hover:text-blue-600 transition-colors">Ver Órdenes</span>
        </router-link>

        <router-link 
          to="/admin/inventario"
          class="flex flex-col items-center gap-3 p-5 border border-gray-100 rounded-2xl hover:border-amber-200 hover:bg-amber-50/30 transition-all group"
        >
          <div class="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center group-hover:bg-amber-100 transition-colors">
            <svg class="w-5 h-5 text-text-light group-hover:text-amber-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
            </svg>
          </div>
          <span class="text-sm font-medium text-text-medium group-hover:text-amber-600 transition-colors">Inventario</span>
        </router-link>

        <router-link 
          to="/admin/clientes"
          class="flex flex-col items-center gap-3 p-5 border border-gray-100 rounded-2xl hover:border-brand-200 hover:bg-brand-50/30 transition-all group"
        >
          <div class="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center group-hover:bg-brand-100 transition-colors">
            <svg class="w-5 h-5 text-text-light group-hover:text-brand-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
            </svg>
          </div>
          <span class="text-sm font-medium text-text-medium group-hover:text-brand-600 transition-colors">Clientes</span>
        </router-link>
      </div>
    </div>

    </div><!-- End v-else content -->
  </div><!-- End main container -->
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import apiClient from '../../services/api'

export default {
  name: 'AdminDashboard',
  setup() {
    // Stats
    const stats = ref({
      totalVentas: 0,
      totalOrdenes: 0,
      ordenesPendientes: 0,
      totalProductos: 0,
      productosActivos: 0,
      stockBajo: 0,
      totalClientes: 0,
      clientesNuevos: 0
    })

    const loading = ref(true)
    const error = ref(null)

    // Recent orders
    const recentOrders = ref([])

    // Low stock products
    const lowStockProducts = ref([])

    // User name
    const userName = computed(() => {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        return user.nombre || user.email?.split('@')[0] || 'Administrador Sistema'
      } catch {
        return 'Administrador Sistema'
      }
    })

    // Cargar estadísticas del backend
    const cargarEstadisticas = async () => {
      try {
        const response = await apiClient.get('/dashboard/estadisticas')
        stats.value = {
          totalVentas: response.data.total_ventas || 0,
          totalOrdenes: response.data.total_ordenes || 0,
          ordenesPendientes: response.data.ordenes_pendientes || 0,
          totalProductos: response.data.total_productos || 0,
          productosActivos: response.data.productos_activos || 0,
          stockBajo: response.data.stock_bajo || 0,
          totalClientes: response.data.total_clientes || 0,
          clientesNuevos: response.data.clientes_nuevos || 0
        }
      } catch (err) {
        console.error('Error al cargar estadísticas:', err)
        error.value = 'No se pudieron cargar las estadísticas'
      }
    }

    // Cargar órdenes recientes
    const cargarOrdenesRecientes = async () => {
      try {
        const response = await apiClient.get('/dashboard/ordenes/recientes?limite=5')
        recentOrders.value = response.data.map(orden => ({
          id: orden.id,
          cliente: orden.cliente_nombre,
          estado: orden.estado,
          total: orden.total,
          fecha: orden.tiempo_transcurrido
        }))
      } catch (err) {
        console.error('Error al cargar órdenes recientes:', err)
      }
    }

    // Cargar productos con stock bajo
    const cargarProductosStockBajo = async () => {
      try {
        const response = await apiClient.get('/dashboard/productos/stock-bajo?umbral=5&limite=10')
        lowStockProducts.value = response.data.map(producto => ({
          id: producto.id,
          nombre: producto.nombre,
          stock: producto.stock_actual,
          imagen: producto.imagen_url || 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=150'
        }))
      } catch (err) {
        console.error('Error al cargar productos con stock bajo:', err)
      }
    }

    // Cargar todos los datos
    const cargarDatos = async () => {
      loading.value = true
      error.value = null
      
      await Promise.all([
        cargarEstadisticas(),
        cargarOrdenesRecientes(),
        cargarProductosStockBajo()
      ])
      
      loading.value = false
    }

    // Cargar datos al montar
    onMounted(() => {
      cargarDatos()
    })

    const formatNumber = (num) => {
      return new Intl.NumberFormat('es-CO').format(num)
    }

    // Pastel status styles - Magazine aesthetic
    const getStatusClass = (status) => {
      const classes = {
        'PENDIENTE': 'bg-rose-50 text-rose-600',
        'CONFIRMADA': 'bg-sky-50 text-sky-600',
        'EN_PROCESO': 'bg-violet-50 text-violet-600',
        'ENVIADA': 'bg-indigo-50 text-indigo-600',
        'COMPLETADA': 'bg-emerald-50 text-emerald-600',
        'CANCELADA': 'bg-gray-100 text-gray-500'
      }
      return classes[status] || 'bg-gray-50 text-gray-600'
    }

    const getStatusLabel = (status) => {
      const labels = {
        'PENDIENTE': 'Pendiente',
        'CONFIRMADA': 'Confirmada',
        'EN_PROCESO': 'En proceso',
        'ENVIADA': 'Enviada',
        'COMPLETADA': 'Completada',
        'CANCELADA': 'Cancelada'
      }
      return labels[status] || status
    }

    return {
      stats,
      recentOrders,
      lowStockProducts,
      userName,
      loading,
      error,
      formatNumber,
      getStatusClass,
      getStatusLabel,
      cargarDatos
    }
  }
}
</script>
