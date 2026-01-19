<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Clientes</h2>
        <p class="text-gray-500">Gestiona tu base de clientes</p>
      </div>
    </div>

    <!-- Search -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4">
      <div class="relative">
        <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Buscar clientes..."
          class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
        >
      </div>
    </div>

    <!-- Clients Grid -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="cliente in filteredClients" 
        :key="cliente.id"
        class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start gap-4">
          <div class="w-14 h-14 bg-brand-100 rounded-full flex items-center justify-center text-brand-600 font-bold text-lg">
            {{ cliente.iniciales }}
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-gray-900 truncate">{{ cliente.nombre }}</h3>
            <p class="text-sm text-gray-500 truncate">{{ cliente.email }}</p>
            <p class="text-sm text-gray-500">{{ cliente.telefono }}</p>
          </div>
        </div>
        
        <div class="mt-4 pt-4 border-t border-gray-100 grid grid-cols-2 gap-4 text-center">
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ cliente.ordenes }}</p>
            <p class="text-xs text-gray-500">Órdenes</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-brand-600">${{ formatNumber(cliente.totalCompras) }}</p>
            <p class="text-xs text-gray-500">Total compras</p>
          </div>
        </div>

        <div class="mt-4 flex gap-2">
          <button class="flex-1 py-2 text-sm font-medium text-brand-600 bg-brand-50 rounded-lg hover:bg-brand-100 transition-colors">
            Ver detalle
          </button>
          <button class="px-3 py-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'AdminClientes',
  setup() {
    const searchQuery = ref('')

    const clientes = ref([
      { id: '1', nombre: 'María García López', email: 'maria@email.com', telefono: '+52 55 1234 5678', ordenes: 12, totalCompras: 15680, iniciales: 'MG' },
      { id: '2', nombre: 'Ana López Ruiz', email: 'ana@email.com', telefono: '+52 55 2345 6789', ordenes: 8, totalCompras: 9450, iniciales: 'AL' },
      { id: '3', nombre: 'Carmen Ruiz Sánchez', email: 'carmen@email.com', telefono: '+52 55 3456 7890', ordenes: 23, totalCompras: 32100, iniciales: 'CR' },
      { id: '4', nombre: 'Laura Sánchez Martínez', email: 'laura@email.com', telefono: '+52 55 4567 8901', ordenes: 5, totalCompras: 4560, iniciales: 'LS' },
      { id: '5', nombre: 'Patricia Martínez', email: 'patricia@email.com', telefono: '+52 55 5678 9012', ordenes: 15, totalCompras: 18900, iniciales: 'PM' },
      { id: '6', nombre: 'Sofía Hernández', email: 'sofia@email.com', telefono: '+52 55 6789 0123', ordenes: 3, totalCompras: 2340, iniciales: 'SH' },
    ])

    const filteredClients = computed(() => {
      if (!searchQuery.value) return clientes.value
      const query = searchQuery.value.toLowerCase()
      return clientes.value.filter(c => 
        c.nombre.toLowerCase().includes(query) ||
        c.email.toLowerCase().includes(query)
      )
    })

    const formatNumber = (num) => new Intl.NumberFormat('es-CO').format(num)

    return { searchQuery, clientes, filteredClients, formatNumber }
  }
}
</script>
