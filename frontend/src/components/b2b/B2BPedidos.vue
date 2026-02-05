<template>
  <div class="max-w-5xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Historial de Pedidos</h1>
        <p class="text-gray-500 mt-1">Gestiona y rastrea tus pedidos mayoristas</p>
      </div>
      <router-link
        to="/portal/catalogo"
        class="inline-flex items-center gap-2 px-5 py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-lg transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Nuevo Pedido
      </router-link>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-xl border border-gray-100 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
            <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wider">Entregados</p>
            <p class="text-xl font-bold text-gray-900">{{ stats.delivered }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-100 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wider">En Camino</p>
            <p class="text-xl font-bold text-gray-900">{{ stats.shipping }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-100 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
            <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wider">Procesando</p>
            <p class="text-xl font-bold text-gray-900">{{ stats.processing }}</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-100 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-[#C9A962]/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-[#C9A962]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wider">Total Compras</p>
            <p class="text-xl font-bold text-gray-900">${{ formatCompact(stats.totalSpent) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl border border-gray-100 p-4 mb-6">
      <div class="flex flex-col sm:flex-row sm:items-center gap-4">
        <!-- Status Tabs -->
        <div class="flex-1 flex flex-wrap gap-2">
          <button 
            v-for="status in statuses" 
            :key="status.value"
            @click="selectedStatus = status.value"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all',
              selectedStatus === status.value 
                ? 'bg-[#1A1A1A] text-white shadow-sm' 
                : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
            ]"
          >
            {{ status.label }}
            <span 
              v-if="status.count > 0"
              :class="[
                'ml-1.5 text-xs px-1.5 py-0.5 rounded-full',
                selectedStatus === status.value ? 'bg-white/20 text-white' : 'bg-gray-200 text-gray-600'
              ]"
            >
              {{ status.count }}
            </span>
          </button>
        </div>

        <!-- Search -->
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Buscar pedido..."
            class="w-full sm:w-48 pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
          />
        </div>
      </div>
    </div>

    <!-- Orders List -->
    <div class="space-y-4">
      <div 
        v-for="order in filteredOrders" 
        :key="order.id"
        class="bg-white rounded-xl border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
      >
        <!-- Order Header -->
        <div class="p-4 sm:p-5 border-b border-gray-50">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center">
                <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
              <div>
                <div class="flex items-center gap-2 flex-wrap">
                  <h3 class="font-bold text-gray-900">Pedido #{{ order.id }}</h3>
                  <span :class="['text-xs px-2.5 py-1 rounded-full font-medium', getStatusClass(order.status)]">
                    {{ order.status }}
                  </span>
                </div>
                <div class="flex items-center gap-3 mt-1 text-sm text-gray-500">
                  <span class="flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ order.date }}
                  </span>
                  <span class="flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                    {{ order.items }} productos
                  </span>
                </div>
              </div>
            </div>
            <div class="text-right sm:text-right">
              <p class="text-2xl font-bold text-gray-900">${{ formatPrice(order.total) }}</p>
              <p class="text-xs text-emerald-600">Ahorraste ${{ formatPrice(order.savings || order.total * 0.15) }}</p>
            </div>
          </div>
        </div>

        <!-- Order Items Preview -->
        <div class="px-4 sm:px-5 py-3 bg-gray-50/50 flex items-center gap-3 overflow-x-auto">
          <div 
            v-for="(product, idx) in order.products?.slice(0, 5)" 
            :key="idx"
            class="w-12 h-12 rounded-lg bg-gray-100 overflow-hidden flex-shrink-0"
          >
            <img :src="product.image || `https://placehold.co/100x100/f5f5f5/1a1a1a?text=${idx+1}`" :alt="product.name" class="w-full h-full object-cover" />
          </div>
          <span v-if="order.items > 5" class="text-xs text-gray-400 flex-shrink-0">+{{ order.items - 5 }} más</span>
        </div>

        <!-- Order Actions -->
        <div class="p-4 sm:px-5 flex flex-wrap gap-2">
          <button 
            @click="viewOrderDetail(order)"
            class="px-4 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 font-medium transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            Ver Detalle
          </button>
          <button 
            v-if="order.status === 'Entregado'"
            @click="reorderItems(order)"
            class="px-4 py-2 text-sm border border-[#C9A962] text-[#C9A962] rounded-lg hover:bg-[#C9A962]/10 font-medium transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Repetir Pedido
          </button>
          <button 
            v-if="order.tracking"
            @click="trackOrder(order)"
            class="px-4 py-2 text-sm bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 font-medium transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Rastrear Envío
          </button>
          <a 
            v-if="order.invoice"
            :href="order.invoice"
            target="_blank"
            class="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100 font-medium transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Factura
          </a>
        </div>

        <!-- Tracking Progress (if in transit) -->
        <div v-if="order.status === 'En Camino' && order.tracking" class="px-4 sm:px-5 pb-4">
          <div class="p-4 bg-blue-50 rounded-xl">
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm font-medium text-blue-900">Seguimiento: {{ order.tracking }}</p>
              <p class="text-xs text-blue-600">Entrega estimada: {{ order.estimatedDelivery || 'Mañana' }}</p>
            </div>
            <div class="flex items-center gap-2">
              <div class="flex-1 h-2 bg-blue-200 rounded-full overflow-hidden">
                <div class="h-full bg-blue-600 rounded-full" :style="{ width: '65%' }"></div>
              </div>
              <span class="text-xs text-blue-600 font-medium">65%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredOrders.length === 0" class="text-center py-16 bg-white rounded-2xl border border-gray-100">
      <div class="w-20 h-20 mx-auto mb-6 bg-gray-100 rounded-2xl flex items-center justify-center">
        <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      </div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">
        {{ selectedStatus === 'all' ? 'No hay pedidos todavía' : `No hay pedidos "${selectedStatus}"` }}
      </h3>
      <p class="text-gray-500 mb-6 max-w-md mx-auto">
        {{ selectedStatus === 'all' ? 'Comienza explorando nuestro catálogo mayorista y crea tu primer pedido' : 'Prueba cambiando los filtros o realiza un nuevo pedido' }}
      </p>
      <router-link 
        to="/portal/catalogo"
        class="inline-flex items-center gap-2 px-6 py-3 bg-[#1A1A1A] hover:bg-black text-white font-bold rounded-xl transition-colors"
      >
        Explorar Catálogo
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </router-link>
    </div>

    <!-- Order Detail Modal -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="showDetailModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50" @click.self="showDetailModal = false">
          <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden shadow-2xl">
            <!-- Modal Header -->
            <div class="p-5 border-b border-gray-100 flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-gray-900">Pedido #{{ selectedOrder?.id }}</h2>
                <p class="text-sm text-gray-500">{{ selectedOrder?.date }}</p>
              </div>
              <button @click="showDetailModal = false" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <!-- Modal Body -->
            <div class="p-5 overflow-y-auto max-h-[60vh]">
              <div class="space-y-4">
                <div v-for="(item, idx) in selectedOrder?.products || []" :key="idx" class="flex gap-4 p-3 bg-gray-50 rounded-xl">
                  <div class="w-16 h-16 rounded-lg bg-gray-200 overflow-hidden">
                    <img :src="item.image || `https://placehold.co/100x100/f5f5f5/1a1a1a?text=${idx+1}`" class="w-full h-full object-cover" />
                  </div>
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-900">{{ item.name }}</h4>
                    <p class="text-sm text-gray-500">Cantidad: {{ item.quantity }}</p>
                  </div>
                  <div class="text-right">
                    <p class="font-bold text-gray-900">${{ formatPrice(item.price * item.quantity) }}</p>
                    <p class="text-xs text-gray-400">${{ formatPrice(item.price) }}/ud</p>
                  </div>
                </div>
              </div>
            </div>
            <!-- Modal Footer -->
            <div class="p-5 border-t border-gray-100 bg-gray-50">
              <div class="flex justify-between items-center">
                <span class="font-semibold text-gray-700">Total del Pedido</span>
                <span class="text-2xl font-bold text-gray-900">${{ formatPrice(selectedOrder?.total) }}</span>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'B2BPedidos',
  setup() {
    const selectedStatus = ref('all')
    const searchQuery = ref('')
    const showDetailModal = ref(false)
    const selectedOrder = ref(null)

    // Mock orders - TODO: Conectar con API
    const orders = ref([
      { 
        id: 'B2B-001245', 
        date: '2 Feb 2026', 
        total: 1250000, 
        savings: 187500,
        items: 12, 
        status: 'Entregado', 
        tracking: null,
        invoice: '#',
        products: [
          { name: 'Extensión Tape-in Premium 60cm', quantity: 4, price: 245000, image: null },
          { name: 'Shampoo Profesional 1L', quantity: 8, price: 68000, image: null },
        ]
      },
      { 
        id: 'B2B-001244', 
        date: '28 Ene 2026', 
        total: 680000, 
        savings: 102000,
        items: 18, 
        status: 'En Camino', 
        tracking: 'TRK-2026-00874',
        estimatedDelivery: '30 Ene 2026',
        invoice: '#',
        products: [
          { name: 'Kit Coloración Profesional', quantity: 3, price: 189000, image: null },
          { name: 'Mascarilla Reparadora 500ml', quantity: 15, price: 45000, image: null },
        ]
      },
      { 
        id: 'B2B-001243', 
        date: '25 Ene 2026', 
        total: 320000, 
        savings: 48000,
        items: 8, 
        status: 'Procesando', 
        tracking: null,
        invoice: null,
        products: [
          { name: 'Aceite Argán Premium 100ml', quantity: 8, price: 40000, image: null },
        ]
      },
      { 
        id: 'B2B-001242', 
        date: '20 Ene 2026', 
        total: 920000, 
        savings: 138000,
        items: 15, 
        status: 'Entregado', 
        tracking: null,
        invoice: '#',
        products: []
      },
      { 
        id: 'B2B-001241', 
        date: '15 Ene 2026', 
        total: 540000, 
        savings: 81000,
        items: 7, 
        status: 'Entregado', 
        tracking: null,
        invoice: '#',
        products: []
      },
    ])

    // Stats
    const stats = computed(() => ({
      delivered: orders.value.filter(o => o.status === 'Entregado').length,
      shipping: orders.value.filter(o => o.status === 'En Camino').length,
      processing: orders.value.filter(o => o.status === 'Procesando' || o.status === 'Pendiente').length,
      totalSpent: orders.value.reduce((sum, o) => sum + o.total, 0)
    }))

    const statuses = computed(() => [
      { value: 'all', label: 'Todos', count: orders.value.length },
      { value: 'Pendiente', label: 'Pendientes', count: orders.value.filter(o => o.status === 'Pendiente').length },
      { value: 'Procesando', label: 'Procesando', count: orders.value.filter(o => o.status === 'Procesando').length },
      { value: 'En Camino', label: 'En Camino', count: orders.value.filter(o => o.status === 'En Camino').length },
      { value: 'Entregado', label: 'Entregados', count: orders.value.filter(o => o.status === 'Entregado').length },
    ])

    const filteredOrders = computed(() => {
      let result = orders.value
      if (selectedStatus.value !== 'all') {
        result = result.filter(o => o.status === selectedStatus.value)
      }
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(o => o.id.toLowerCase().includes(query))
      }
      return result
    })

    function getStatusClass(status) {
      const classes = {
        'Entregado': 'bg-emerald-100 text-emerald-700',
        'En Camino': 'bg-blue-100 text-blue-700',
        'Procesando': 'bg-amber-100 text-amber-700',
        'Pendiente': 'bg-gray-100 text-gray-600',
        'Cancelado': 'bg-red-100 text-red-700',
      }
      return classes[status] || classes['Pendiente']
    }

    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

    function formatCompact(value) {
      if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
      if (value >= 1000) return (value / 1000).toFixed(0) + 'K'
      return value?.toString() || '0'
    }

    function viewOrderDetail(order) {
      selectedOrder.value = order
      showDetailModal.value = true
    }

    function reorderItems(order) {
      alert(`Agregando ${order.items} productos al carrito...`)
    }

    function trackOrder(order) {
      alert(`Rastreando envío: ${order.tracking}`)
    }

    return {
      selectedStatus, searchQuery, stats, statuses, filteredOrders,
      showDetailModal, selectedOrder,
      getStatusClass, formatPrice, formatCompact,
      viewOrderDetail, reorderItems, trackOrder
    }
  }
}
</script>
