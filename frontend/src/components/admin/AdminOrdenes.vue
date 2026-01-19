<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Órdenes</h2>
        <p class="text-gray-500">Gestiona los pedidos de tus clientes</p>
      </div>
      <div class="flex items-center gap-3">
        <button class="inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-4 py-2.5 rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Exportar
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
      <div 
        v-for="stat in orderStats" 
        :key="stat.status"
        @click="filterStatus = stat.status"
        :class="[
          'p-4 rounded-2xl border-2 cursor-pointer transition-all',
          filterStatus === stat.status ? 'border-brand-500 bg-brand-50' : 'border-gray-100 bg-white hover:border-gray-200'
        ]"
      >
        <p class="text-2xl font-bold" :class="stat.color">{{ stat.count }}</p>
        <p class="text-sm text-gray-500">{{ stat.label }}</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4">
      <div class="flex flex-col lg:flex-row gap-4">
        <div class="flex-1 relative">
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por # orden o cliente..."
            class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
          >
        </div>
        <input 
          type="date" 
          v-model="filterDate"
          class="px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
        >
        <button 
          @click="clearFilters"
          class="px-4 py-3 text-gray-600 hover:text-gray-900 font-medium"
        >
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Orders Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Orden</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Cliente</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Productos</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Total</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Fecha</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="orden in filteredOrders" :key="orden.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <span class="font-mono font-medium text-gray-900">#{{ orden.id.slice(0, 8) }}</span>
              </td>
              <td class="px-6 py-4">
                <div>
                  <p class="font-medium text-gray-900">{{ orden.cliente.nombre }}</p>
                  <p class="text-sm text-gray-500">{{ orden.cliente.email }}</p>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-gray-600">{{ orden.items }} productos</span>
              </td>
              <td class="px-6 py-4">
                <span class="font-semibold text-gray-900">${{ formatNumber(orden.total) }}</span>
              </td>
              <td class="px-6 py-4">
                <select 
                  v-model="orden.estado"
                  @change="updateOrderStatus(orden)"
                  :class="getStatusClass(orden.estado)"
                  class="px-3 py-1.5 text-xs font-medium rounded-full border-0 cursor-pointer"
                >
                  <option value="PENDIENTE">Pendiente</option>
                  <option value="CONFIRMADA">Confirmada</option>
                  <option value="EN_PROCESO">En Proceso</option>
                  <option value="ENVIADA">Enviada</option>
                  <option value="COMPLETADA">Completada</option>
                  <option value="CANCELADA">Cancelada</option>
                </select>
              </td>
              <td class="px-6 py-4 text-gray-500 text-sm">{{ orden.fecha }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button 
                    @click="viewOrder(orden)"
                    class="p-2 text-gray-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="Ver detalle"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button 
                    @click="printOrder(orden)"
                    class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Imprimir"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'AdminOrdenes',
  setup() {
    const searchQuery = ref('')
    const filterStatus = ref('')
    const filterDate = ref('')

    const orderStats = ref([
      { status: '', label: 'Todas', count: 156, color: 'text-gray-900' },
      { status: 'PENDIENTE', label: 'Pendientes', count: 5, color: 'text-yellow-600' },
      { status: 'CONFIRMADA', label: 'Confirmadas', count: 12, color: 'text-blue-600' },
      { status: 'ENVIADA', label: 'Enviadas', count: 8, color: 'text-indigo-600' },
      { status: 'COMPLETADA', label: 'Completadas', count: 131, color: 'text-green-600' }
    ])

    const ordenes = ref([
      { id: 'abc12345-6789-0123', cliente: { nombre: 'María García', email: 'maria@email.com' }, items: 3, total: 2450, estado: 'PENDIENTE', fecha: '17 Ene 2026, 14:30' },
      { id: 'def12345-6789-0123', cliente: { nombre: 'Ana López', email: 'ana@email.com' }, items: 2, total: 1890, estado: 'CONFIRMADA', fecha: '17 Ene 2026, 10:15' },
      { id: 'ghi12345-6789-0123', cliente: { nombre: 'Carmen Ruiz', email: 'carmen@email.com' }, items: 5, total: 4200, estado: 'EN_PROCESO', fecha: '16 Ene 2026, 18:45' },
      { id: 'jkl12345-6789-0123', cliente: { nombre: 'Laura Sánchez', email: 'laura@email.com' }, items: 1, total: 890, estado: 'ENVIADA', fecha: '16 Ene 2026, 09:20' },
      { id: 'mno12345-6789-0123', cliente: { nombre: 'Patricia Martínez', email: 'patricia@email.com' }, items: 4, total: 3560, estado: 'COMPLETADA', fecha: '15 Ene 2026, 16:00' },
    ])

    const filteredOrders = computed(() => {
      let result = ordenes.value

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(o => 
          o.id.toLowerCase().includes(query) ||
          o.cliente.nombre.toLowerCase().includes(query) ||
          o.cliente.email.toLowerCase().includes(query)
        )
      }

      if (filterStatus.value) {
        result = result.filter(o => o.estado === filterStatus.value)
      }

      return result
    })

    const formatNumber = (num) => new Intl.NumberFormat('es-CO').format(num)

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

    const clearFilters = () => {
      searchQuery.value = ''
      filterStatus.value = ''
      filterDate.value = ''
    }

    const updateOrderStatus = (orden) => {
      console.log('Update status:', orden.id, orden.estado)
    }

    const viewOrder = (orden) => {
      console.log('View order:', orden)
    }

    const printOrder = (orden) => {
      console.log('Print order:', orden)
    }

    return {
      searchQuery,
      filterStatus,
      filterDate,
      orderStats,
      ordenes,
      filteredOrders,
      formatNumber,
      getStatusClass,
      clearFilters,
      updateOrderStatus,
      viewOrder,
      printOrder
    }
  }
}
</script>
