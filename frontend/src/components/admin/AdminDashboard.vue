<template>
  <div class="space-y-8">
    <!-- Welcome Banner -->
    <div class="bg-gradient-to-r from-brand-600 to-brand-700 rounded-2xl p-6 lg:p-8 text-white">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h2 class="text-2xl lg:text-3xl font-bold mb-2">¡Bienvenido, {{ userName }}!</h2>
          <p class="text-white/80">Aquí tienes un resumen de tu tienda hoy.</p>
        </div>
        <div class="flex gap-3">
          <router-link 
            to="/admin/productos/nuevo"
            class="flex items-center gap-2 bg-white text-brand-600 font-semibold px-5 py-2.5 rounded-xl hover:bg-brand-50 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Nuevo Producto
          </router-link>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Total Ventas -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <span class="text-green-600 text-sm font-medium flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
            </svg>
            +12.5%
          </span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900">${{ formatNumber(stats.totalVentas) }}</h3>
        <p class="text-gray-500 text-sm">Ventas este mes</p>
      </div>

      <!-- Órdenes -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <span class="text-blue-600 text-sm font-medium">{{ stats.ordenesPendientes }} pendientes</span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900">{{ stats.totalOrdenes }}</h3>
        <p class="text-gray-500 text-sm">Órdenes totales</p>
      </div>

      <!-- Productos -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
          <span class="text-orange-600 text-sm font-medium">{{ stats.stockBajo }} stock bajo</span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900">{{ stats.totalProductos }}</h3>
        <p class="text-gray-500 text-sm">Productos activos</p>
      </div>

      <!-- Clientes -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-pink-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <span class="text-green-600 text-sm font-medium">+{{ stats.clientesNuevos }} nuevos</span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900">{{ stats.totalClientes }}</h3>
        <p class="text-gray-500 text-sm">Clientes registrados</p>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid lg:grid-cols-3 gap-8">
      <!-- Recent Orders -->
      <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100">
        <div class="flex items-center justify-between p-6 border-b border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900">Últimas Órdenes</h3>
          <router-link to="/admin/ordenes" class="text-brand-600 text-sm font-medium hover:underline">
            Ver todas
          </router-link>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Orden</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Cliente</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Estado</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Total</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Fecha</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="orden in recentOrders" :key="orden.id" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <span class="font-medium text-gray-900">#{{ orden.id.slice(0, 8) }}</span>
                </td>
                <td class="px-6 py-4 text-gray-600">{{ orden.cliente }}</td>
                <td class="px-6 py-4">
                  <span :class="getStatusClass(orden.estado)" class="px-3 py-1 text-xs font-medium rounded-full">
                    {{ orden.estado }}
                  </span>
                </td>
                <td class="px-6 py-4 font-medium text-gray-900">${{ formatNumber(orden.total) }}</td>
                <td class="px-6 py-4 text-gray-500 text-sm">{{ orden.fecha }}</td>
              </tr>
              <tr v-if="recentOrders.length === 0">
                <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                  No hay órdenes recientes
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Low Stock Products -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100">
        <div class="flex items-center justify-between p-6 border-b border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900">Stock Bajo</h3>
          <router-link to="/admin/inventario" class="text-brand-600 text-sm font-medium hover:underline">
            Ver todo
          </router-link>
        </div>
        <div class="p-4 space-y-4">
          <div 
            v-for="product in lowStockProducts" 
            :key="product.id"
            class="flex items-center gap-4 p-3 bg-red-50 rounded-xl"
          >
            <div class="w-12 h-12 bg-white rounded-lg overflow-hidden flex-shrink-0">
              <img :src="product.imagen" :alt="product.nombre" class="w-full h-full object-cover">
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-gray-900 truncate">{{ product.nombre }}</p>
              <p class="text-sm text-red-600">Solo {{ product.stock }} unidades</p>
            </div>
            <button class="text-brand-600 hover:text-brand-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
          </div>
          <div v-if="lowStockProducts.length === 0" class="text-center py-8 text-gray-500">
            <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Todo el inventario OK
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <router-link 
          to="/admin/productos/nuevo"
          class="flex flex-col items-center gap-3 p-4 bg-gray-50 rounded-xl hover:bg-brand-50 hover:text-brand-600 transition-colors group"
        >
          <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
            <svg class="w-6 h-6 text-gray-600 group-hover:text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </div>
          <span class="text-sm font-medium text-gray-700 group-hover:text-brand-600">Nuevo Producto</span>
        </router-link>

        <router-link 
          to="/admin/ordenes"
          class="flex flex-col items-center gap-3 p-4 bg-gray-50 rounded-xl hover:bg-blue-50 hover:text-blue-600 transition-colors group"
        >
          <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
            <svg class="w-6 h-6 text-gray-600 group-hover:text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <span class="text-sm font-medium text-gray-700 group-hover:text-blue-600">Ver Órdenes</span>
        </router-link>

        <router-link 
          to="/admin/inventario"
          class="flex flex-col items-center gap-3 p-4 bg-gray-50 rounded-xl hover:bg-orange-50 hover:text-orange-600 transition-colors group"
        >
          <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
            <svg class="w-6 h-6 text-gray-600 group-hover:text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
          <span class="text-sm font-medium text-gray-700 group-hover:text-orange-600">Inventario</span>
        </router-link>

        <router-link 
          to="/admin/clientes"
          class="flex flex-col items-center gap-3 p-4 bg-gray-50 rounded-xl hover:bg-pink-50 hover:text-pink-600 transition-colors group"
        >
          <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
            <svg class="w-6 h-6 text-gray-600 group-hover:text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <span class="text-sm font-medium text-gray-700 group-hover:text-pink-600">Clientes</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'AdminDashboard',
  setup() {
    // Stats
    const stats = ref({
      totalVentas: 45890,
      totalOrdenes: 156,
      ordenesPendientes: 5,
      totalProductos: 87,
      stockBajo: 3,
      totalClientes: 432,
      clientesNuevos: 12
    })

    // Recent orders (mock data)
    const recentOrders = ref([
      { id: 'abc12345-6789', cliente: 'María García', estado: 'PENDIENTE', total: 2450, fecha: 'Hace 2 horas' },
      { id: 'def12345-6789', cliente: 'Ana López', estado: 'CONFIRMADA', total: 1890, fecha: 'Hace 5 horas' },
      { id: 'ghi12345-6789', cliente: 'Carmen Ruiz', estado: 'ENVIADA', total: 3200, fecha: 'Ayer' },
      { id: 'jkl12345-6789', cliente: 'Laura Sánchez', estado: 'COMPLETADA', total: 1560, fecha: 'Hace 2 días' },
    ])

    // Low stock products (mock data)
    const lowStockProducts = ref([
      { id: 1, nombre: 'Extensiones Brasileñas 24"', stock: 2, imagen: 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=100' },
      { id: 2, nombre: 'Peluca Lace Front Natural', stock: 3, imagen: 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=100' },
      { id: 3, nombre: 'Clip-in Extensions Rubio', stock: 1, imagen: 'https://images.unsplash.com/photo-1580618672591-eb180b1a973f?w=100' },
    ])

    // User name
    const userName = computed(() => {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        return user.nombre || user.email?.split('@')[0] || 'Admin'
      } catch {
        return 'Admin'
      }
    })

    const formatNumber = (num) => {
      return new Intl.NumberFormat('es-MX').format(num)
    }

    const getStatusClass = (status) => {
      const classes = {
        'PENDIENTE': 'bg-yellow-100 text-yellow-700',
        'CONFIRMADA': 'bg-blue-100 text-blue-700',
        'EN_PROCESO': 'bg-purple-100 text-purple-700',
        'ENVIADA': 'bg-indigo-100 text-indigo-700',
        'COMPLETADA': 'bg-green-100 text-green-700',
        'CANCELADA': 'bg-red-100 text-red-700'
      }
      return classes[status] || 'bg-gray-100 text-gray-700'
    }

    return {
      stats,
      recentOrders,
      lowStockProducts,
      userName,
      formatNumber,
      getStatusClass
    }
  }
}
</script>
