<template>
  <div class="space-y-6">
    <!-- Welcome Banner -->
    <div class="bg-gradient-to-r from-[#1A1A1A] to-[#2D2D2D] rounded-xl p-6 sm:p-8 text-white">
      <h1 class="text-2xl sm:text-3xl font-luxury mb-2">
        Bienvenido, <span class="text-[#C9A962]">{{ user.nombre }}</span>
      </h1>
      <p class="text-white/60">Panel de control de tu cuenta mayorista</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div 
        v-for="stat in stats" 
        :key="stat.label"
        class="bg-white rounded-lg p-4 sm:p-6 shadow-sm"
      >
        <div class="flex items-center gap-3 mb-2">
          <div :class="['w-10 h-10 rounded-full flex items-center justify-center', stat.bgColor]">
            <component :is="stat.icon" :class="['w-5 h-5', stat.iconColor]" />
          </div>
        </div>
        <p class="text-2xl sm:text-3xl font-bold text-text-dark">{{ stat.value }}</p>
        <p class="text-sm text-text-light">{{ stat.label }}</p>
      </div>
    </div>

    <!-- Quick Actions & Recent Orders -->
    <div class="grid lg:grid-cols-2 gap-6">
      <!-- Quick Actions -->
      <div class="bg-white rounded-lg p-6 shadow-sm">
        <h2 class="text-lg font-medium text-text-dark mb-4">Acciones Rápidas</h2>
        <div class="grid grid-cols-2 gap-3">
          <router-link 
            to="/portal/catalogo"
            class="flex items-center gap-3 p-4 border border-gray-100 rounded-lg hover:border-[#C9A962] hover:bg-[#C9A962]/5 transition-all"
          >
            <div class="w-10 h-10 bg-[#C9A962]/10 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-[#C9A962]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </div>
            <span class="text-sm font-medium text-text-dark">Ver Catálogo</span>
          </router-link>
          
          <router-link 
            to="/portal/carrito"
            class="flex items-center gap-3 p-4 border border-gray-100 rounded-lg hover:border-[#C9A962] hover:bg-[#C9A962]/5 transition-all"
          >
            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <span class="text-sm font-medium text-text-dark">Mi Carrito</span>
          </router-link>
          
          <router-link 
            to="/portal/pedidos"
            class="flex items-center gap-3 p-4 border border-gray-100 rounded-lg hover:border-[#C9A962] hover:bg-[#C9A962]/5 transition-all"
          >
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <span class="text-sm font-medium text-text-dark">Mis Pedidos</span>
          </router-link>
          
          <router-link 
            to="/portal/cuenta"
            class="flex items-center gap-3 p-4 border border-gray-100 rounded-lg hover:border-[#C9A962] hover:bg-[#C9A962]/5 transition-all"
          >
            <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <span class="text-sm font-medium text-text-dark">Mi Cuenta</span>
          </router-link>
        </div>
      </div>

      <!-- Recent Orders -->
      <div class="bg-white rounded-lg p-6 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-medium text-text-dark">Pedidos Recientes</h2>
          <router-link to="/portal/pedidos" class="text-sm text-[#C9A962] hover:underline">
            Ver todos
          </router-link>
        </div>
        
        <div v-if="recentOrders.length === 0" class="text-center py-8 text-text-light">
          <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p>Aún no tienes pedidos</p>
          <router-link to="/portal/catalogo" class="text-[#C9A962] hover:underline text-sm mt-2 inline-block">
            Explorar catálogo
          </router-link>
        </div>

        <div v-else class="space-y-3">
          <div 
            v-for="order in recentOrders" 
            :key="order.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div>
              <p class="font-medium text-text-dark">#{{ order.id }}</p>
              <p class="text-sm text-text-light">{{ order.date }}</p>
            </div>
            <div class="text-right">
              <p class="font-medium text-text-dark">${{ order.total.toLocaleString() }}</p>
              <span :class="['text-xs px-2 py-1 rounded-full', getStatusClass(order.status)]">
                {{ order.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Promotional Banner -->
    <div class="bg-gradient-to-r from-[#C9A962] to-[#D4A85A] rounded-xl p-6 sm:p-8 text-white">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h3 class="text-xl font-medium mb-1">🎉 Descuento Especial Mayorista</h3>
          <p class="text-white/80">Obtén 15% de descuento en pedidos mayores a $500.000</p>
        </div>
        <router-link 
          to="/portal/catalogo"
          class="shrink-0 px-6 py-3 bg-white text-[#1A1A1A] font-medium rounded-md hover:bg-white/90 transition-colors"
        >
          Comprar Ahora
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'B2BDashboard',
  setup() {
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{"nombre": "Mayorista"}')
    })

    const stats = ref([
      { 
        label: 'Pedidos Totales', 
        value: '24', 
        bgColor: 'bg-blue-100', 
        iconColor: 'text-blue-600',
        icon: 'div'
      },
      { 
        label: 'Pedidos Pendientes', 
        value: '3', 
        bgColor: 'bg-yellow-100', 
        iconColor: 'text-yellow-600',
        icon: 'div'
      },
      { 
        label: 'Total Comprado', 
        value: '$2.4M', 
        bgColor: 'bg-green-100', 
        iconColor: 'text-green-600',
        icon: 'div'
      },
      { 
        label: 'Descuento Actual', 
        value: '15%', 
        bgColor: 'bg-purple-100', 
        iconColor: 'text-purple-600',
        icon: 'div'
      },
    ])

    const recentOrders = ref([
      { id: 'B2B-001245', date: '2 Feb 2026', total: 450000, status: 'Entregado' },
      { id: 'B2B-001244', date: '28 Ene 2026', total: 680000, status: 'En Camino' },
      { id: 'B2B-001243', date: '25 Ene 2026', total: 320000, status: 'Procesando' },
    ])

    function getStatusClass(status) {
      const classes = {
        'Entregado': 'bg-green-100 text-green-700',
        'En Camino': 'bg-blue-100 text-blue-700',
        'Procesando': 'bg-yellow-100 text-yellow-700',
        'Pendiente': 'bg-gray-100 text-gray-700',
        'Cancelado': 'bg-red-100 text-red-700',
      }
      return classes[status] || classes['Pendiente']
    }

    return {
      user,
      stats,
      recentOrders,
      getStatusClass
    }
  }
}
</script>
