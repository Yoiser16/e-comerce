<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Inventario</h2>
        <p class="text-gray-500">Control de stock y alertas</p>
      </div>
      <button class="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold px-5 py-3 rounded-xl transition-colors">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Ajuste de Stock
      </button>
    </div>

    <!-- Alert Cards -->
    <div class="grid md:grid-cols-3 gap-6">
      <div class="bg-red-50 border border-red-200 rounded-2xl p-6">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <p class="text-3xl font-bold text-red-700">{{ stats.agotados }}</p>
            <p class="text-red-600 font-medium">Productos Agotados</p>
          </div>
        </div>
      </div>

      <div class="bg-orange-50 border border-orange-200 rounded-2xl p-6">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-3xl font-bold text-orange-700">{{ stats.stockBajo }}</p>
            <p class="text-orange-600 font-medium">Stock Bajo</p>
          </div>
        </div>
      </div>

      <div class="bg-green-50 border border-green-200 rounded-2xl p-6">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div>
            <p class="text-3xl font-bold text-green-700">{{ stats.saludables }}</p>
            <p class="text-green-600 font-medium">Stock Saludable</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Inventory Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Producto</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">SKU</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-gray-500 uppercase">Stock Actual</th>
              <th class="px-6 py-4 text-center text-xs font-semibold text-gray-500 uppercase">Stock Mínimo</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="item in inventario" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 bg-gray-100 rounded-lg overflow-hidden">
                    <img :src="item.imagen" :alt="item.nombre" class="w-full h-full object-cover">
                  </div>
                  <span class="font-medium text-gray-900">{{ item.nombre }}</span>
                </div>
              </td>
              <td class="px-6 py-4 font-mono text-sm text-gray-600">{{ item.sku }}</td>
              <td class="px-6 py-4 text-center">
                <span :class="getStockTextClass(item)" class="text-xl font-bold">{{ item.stock }}</span>
              </td>
              <td class="px-6 py-4 text-center text-gray-500">{{ item.stockMinimo }}</td>
              <td class="px-6 py-4">
                <span :class="getStockBadgeClass(item)" class="px-3 py-1 text-xs font-medium rounded-full">
                  {{ getStockLabel(item) }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button class="inline-flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-brand-600 bg-brand-50 rounded-lg hover:bg-brand-100">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Ajustar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'AdminInventario',
  setup() {
    const stats = ref({
      agotados: 2,
      stockBajo: 5,
      saludables: 80
    })

    const inventario = ref([
      { id: '1', nombre: 'Extensiones Brasileñas 24"', sku: 'EXT-BR-24', stock: 0, stockMinimo: 5, imagen: 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=100' },
      { id: '2', nombre: 'Peluca Lace Front Natural', sku: 'PEL-LF-001', stock: 3, stockMinimo: 5, imagen: 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=100' },
      { id: '3', nombre: 'Clip-in Extensions 18"', sku: 'EXT-CL-18', stock: 25, stockMinimo: 10, imagen: 'https://images.unsplash.com/photo-1580618672591-eb180b1a973f?w=100' },
      { id: '4', nombre: 'Shampoo Sin Sulfatos 500ml', sku: 'COS-SH-001', stock: 50, stockMinimo: 15, imagen: 'https://images.unsplash.com/photo-1556227702-d1e4e7b5c232?w=100' },
      { id: '5', nombre: 'Extensiones Peruanas 26"', sku: 'EXT-PE-26', stock: 2, stockMinimo: 5, imagen: 'https://images.unsplash.com/photo-1562322140-8baeececf3df?w=100' },
    ])

    const getStockTextClass = (item) => {
      if (item.stock === 0) return 'text-red-600'
      if (item.stock <= item.stockMinimo) return 'text-orange-600'
      return 'text-green-600'
    }

    const getStockBadgeClass = (item) => {
      if (item.stock === 0) return 'bg-red-100 text-red-700'
      if (item.stock <= item.stockMinimo) return 'bg-orange-100 text-orange-700'
      return 'bg-green-100 text-green-700'
    }

    const getStockLabel = (item) => {
      if (item.stock === 0) return 'Agotado'
      if (item.stock <= item.stockMinimo) return 'Stock Bajo'
      return 'Disponible'
    }

    return { stats, inventario, getStockTextClass, getStockBadgeClass, getStockLabel }
  }
}
</script>
