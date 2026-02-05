<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-luxury text-text-dark">Mis Pedidos</h1>
    
    <!-- Filters -->
    <div class="flex flex-wrap gap-2">
      <button 
        v-for="status in statuses" 
        :key="status.value"
        @click="selectedStatus = status.value"
        :class="[
          'px-4 py-2 rounded-full text-sm font-medium transition-colors',
          selectedStatus === status.value 
            ? 'bg-[#1A1A1A] text-white' 
            : 'bg-white text-text-medium hover:bg-gray-100'
        ]"
      >
        {{ status.label }}
      </button>
    </div>

    <!-- Orders List -->
    <div class="space-y-4">
      <div 
        v-for="order in filteredOrders" 
        :key="order.id"
        class="bg-white rounded-lg shadow-sm p-4 sm:p-6"
      >
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <div>
            <div class="flex items-center gap-2">
              <h3 class="font-medium text-text-dark">Pedido #{{ order.id }}</h3>
              <span :class="['text-xs px-2 py-1 rounded-full', getStatusClass(order.status)]">
                {{ order.status }}
              </span>
            </div>
            <p class="text-sm text-text-light">{{ order.date }}</p>
          </div>
          <div class="text-right">
            <p class="text-lg font-bold text-text-dark">${{ order.total.toLocaleString() }}</p>
            <p class="text-sm text-text-light">{{ order.items }} productos</p>
          </div>
        </div>
        
        <div class="flex flex-wrap gap-2">
          <button class="px-4 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">
            Ver Detalle
          </button>
          <button 
            v-if="order.status === 'Entregado'"
            class="px-4 py-2 text-sm border border-[#C9A962] text-[#C9A962] rounded-lg hover:bg-[#C9A962]/10"
          >
            Repetir Pedido
          </button>
          <button 
            v-if="order.tracking"
            class="px-4 py-2 text-sm bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100"
          >
            Rastrear Envío
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredOrders.length === 0" class="text-center py-12 bg-white rounded-lg">
      <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
      <h3 class="text-lg font-medium text-text-dark mb-2">No hay pedidos</h3>
      <p class="text-text-light">{{ selectedStatus === 'all' ? 'Aún no has realizado ningún pedido' : 'No hay pedidos con este estado' }}</p>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'B2BPedidos',
  setup() {
    const selectedStatus = ref('all')

    const statuses = [
      { value: 'all', label: 'Todos' },
      { value: 'Pendiente', label: 'Pendientes' },
      { value: 'Procesando', label: 'Procesando' },
      { value: 'En Camino', label: 'En Camino' },
      { value: 'Entregado', label: 'Entregados' },
    ]

    // Mock orders - TODO: Conectar con API
    const orders = ref([
      { id: 'B2B-001245', date: '2 Feb 2026', total: 450000, items: 12, status: 'Entregado', tracking: null },
      { id: 'B2B-001244', date: '28 Ene 2026', total: 680000, items: 18, status: 'En Camino', tracking: 'TRACK123' },
      { id: 'B2B-001243', date: '25 Ene 2026', total: 320000, items: 8, status: 'Procesando', tracking: null },
      { id: 'B2B-001242', date: '20 Ene 2026', total: 520000, items: 15, status: 'Entregado', tracking: null },
      { id: 'B2B-001241', date: '15 Ene 2026', total: 280000, items: 7, status: 'Entregado', tracking: null },
    ])

    const filteredOrders = computed(() => {
      if (selectedStatus.value === 'all') return orders.value
      return orders.value.filter(o => o.status === selectedStatus.value)
    })

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
      selectedStatus,
      statuses,
      filteredOrders,
      getStatusClass
    }
  }
}
</script>
