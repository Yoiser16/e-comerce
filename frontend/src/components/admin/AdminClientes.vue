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
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredClients.length === 0" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-12 text-center">
      <svg class="mx-auto h-16 w-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <p class="mt-4 text-gray-500">No se encontraron clientes</p>
    </div>

    <!-- Content -->
    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
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
import { ref, computed, onMounted } from 'vue'
import { clientesService } from '../../services/clientes'

export default {
  name: 'AdminClientes',
  setup() {
    const searchQuery = ref('')
    const loading = ref(true)
    const clientes = ref([])

    const cargarClientes = async () => {
      try {
        loading.value = true
        const data = await clientesService.obtenerTodos()
        
        // Transformar datos al formato del componente
        clientes.value = data.map(cliente => ({
          id: cliente.id,
          nombre: cliente.nombre || `${cliente.nombre_pila || ''} ${cliente.apellidos || ''}`.trim(),
          email: cliente.email,
          telefono: cliente.telefono || 'No especificado',
          ordenes: cliente.total_ordenes || 0,
          totalCompras: cliente.total_compras || 0,
          iniciales: obtenerIniciales(cliente.nombre || cliente.nombre_pila || cliente.email)
        }))
      } catch (error) {
        console.error('Error al cargar clientes:', error)
        clientes.value = []
      } finally {
        loading.value = false
      }
    }

    const obtenerIniciales = (nombre) => {
      if (!nombre) return '??'
      const parts = nombre.trim().split(' ')
      if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase()
      }
      return nombre.substring(0, 2).toUpperCase()
    }

    const filteredClients = computed(() => {
      if (!searchQuery.value) return clientes.value
      const query = searchQuery.value.toLowerCase()
      return clientes.value.filter(c => 
        c.nombre.toLowerCase().includes(query) ||
        c.email.toLowerCase().includes(query)
      )
    })

    const formatNumber = (num) => new Intl.NumberFormat('es-CO').format(num)

    onMounted(() => {
      cargarClientes()
    })

    return { searchQuery, loading, clientes, filteredClients, formatNumber, cargarClientes }
  }
}
</script>

