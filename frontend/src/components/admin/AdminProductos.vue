<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Productos</h2>
        <p class="text-gray-500">Gestiona tu catálogo de productos</p>
      </div>
      <router-link 
        to="/admin/productos/nuevo"
        class="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold px-5 py-3 rounded-xl transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Nuevo Producto
      </router-link>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4">
      <div class="flex flex-col lg:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1 relative">
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Buscar productos..."
            class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
          >
        </div>

        <!-- Category Filter -->
        <select 
          v-model="filterCategory"
          class="px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 min-w-[180px]"
        >
          <option value="">Todas las categorías</option>
          <option value="extensiones">Extensiones</option>
          <option value="pelucas">Pelucas</option>
          <option value="cosmeticos">Cosméticos</option>
          <option value="accesorios">Accesorios</option>
        </select>

        <!-- Stock Filter -->
        <select 
          v-model="filterStock"
          class="px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 min-w-[150px]"
        >
          <option value="">Todo el stock</option>
          <option value="available">Disponible</option>
          <option value="low">Stock bajo</option>
          <option value="out">Agotado</option>
        </select>
      </div>
    </div>

    <!-- Products Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <!-- Loading State -->
      <div v-if="loading" class="p-8">
        <div class="animate-pulse space-y-4">
          <div v-for="i in 5" :key="i" class="flex items-center gap-4">
            <div class="w-16 h-16 bg-gray-200 rounded-xl"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-200 rounded w-1/3"></div>
              <div class="h-3 bg-gray-200 rounded w-1/4"></div>
            </div>
            <div class="h-8 bg-gray-200 rounded w-20"></div>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Producto</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">SKU</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Categoría</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Precio</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Stock</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="producto in filteredProducts" :key="producto.id" class="hover:bg-gray-50">
              <!-- Product -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-4">
                  <div class="w-14 h-14 bg-gray-100 rounded-xl overflow-hidden flex-shrink-0">
                    <img 
                      :src="producto.imagen || 'https://via.placeholder.com/100'" 
                      :alt="producto.nombre"
                      class="w-full h-full object-cover"
                    >
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ producto.nombre }}</p>
                    <p class="text-sm text-gray-500 truncate max-w-[200px]">{{ producto.descripcion }}</p>
                  </div>
                </div>
              </td>
              
              <!-- SKU -->
              <td class="px-6 py-4">
                <span class="font-mono text-sm text-gray-600">{{ producto.codigo }}</span>
              </td>
              
              <!-- Category -->
              <td class="px-6 py-4">
                <span class="px-3 py-1 bg-gray-100 text-gray-700 text-xs font-medium rounded-full">
                  {{ producto.categoria }}
                </span>
              </td>
              
              <!-- Price -->
              <td class="px-6 py-4">
                <span class="font-semibold text-gray-900">${{ formatNumber(producto.precio) }}</span>
              </td>
              
              <!-- Stock -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <span :class="getStockClass(producto.stock)" class="font-medium">
                    {{ producto.stock }}
                  </span>
                  <span v-if="producto.stock <= producto.stockMinimo" class="text-orange-500">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                  </span>
                </div>
              </td>
              
              <!-- Status -->
              <td class="px-6 py-4">
                <span 
                  :class="producto.activo ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                  class="px-3 py-1 text-xs font-medium rounded-full"
                >
                  {{ producto.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              
              <!-- Actions -->
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button 
                    @click="editProduct(producto)"
                    class="p-2 text-gray-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="Editar"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button 
                    @click="deleteProduct(producto)"
                    class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Eliminar"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Empty State -->
            <tr v-if="filteredProducts.length === 0">
              <td colspan="7" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center">
                  <svg class="w-16 h-16 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                  <p class="text-gray-500 mb-4">No se encontraron productos</p>
                  <router-link 
                    to="/admin/productos/nuevo"
                    class="text-brand-600 font-medium hover:underline"
                  >
                    Agregar primer producto
                  </router-link>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-between p-4 border-t border-gray-100">
        <p class="text-sm text-gray-500">
          Mostrando {{ filteredProducts.length }} de {{ productos.length }} productos
        </p>
        <div class="flex items-center gap-2">
          <button 
            class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50"
            :disabled="currentPage === 1"
          >
            Anterior
          </button>
          <button 
            class="px-4 py-2 text-sm font-medium text-white bg-brand-600 rounded-lg hover:bg-brand-700"
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { productosService } from '../../services/productos'

export default {
  name: 'AdminProductos',
  setup() {
    const loading = ref(true)
    const productos = ref([])
    const searchQuery = ref('')
    const filterCategory = ref('')
    const filterStock = ref('')
    const currentPage = ref(1)

    // Mock data for now
    const mockProductos = [
      { id: '1', codigo: 'EXT-BR-24', nombre: 'Extensiones Brasileñas 24"', descripcion: 'Cabello 100% natural brasileño', categoria: 'Extensiones', precio: 2450, stock: 15, stockMinimo: 5, activo: true, imagen: 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=100' },
      { id: '2', codigo: 'PEL-LF-001', nombre: 'Peluca Lace Front Natural', descripcion: 'Peluca con lace frontal invisible', categoria: 'Pelucas', precio: 3890, stock: 3, stockMinimo: 5, activo: true, imagen: 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=100' },
      { id: '3', codigo: 'EXT-CL-18', nombre: 'Clip-in Extensions 18"', descripcion: 'Set de 7 piezas clip-in', categoria: 'Extensiones', precio: 1560, stock: 25, stockMinimo: 10, activo: true, imagen: 'https://images.unsplash.com/photo-1580618672591-eb180b1a973f?w=100' },
      { id: '4', codigo: 'COS-SH-001', nombre: 'Shampoo Sin Sulfatos 500ml', descripcion: 'Ideal para extensiones', categoria: 'Cosméticos', precio: 350, stock: 50, stockMinimo: 15, activo: true, imagen: 'https://images.unsplash.com/photo-1556227702-d1e4e7b5c232?w=100' },
      { id: '5', codigo: 'EXT-PE-26', nombre: 'Extensiones Peruanas 26"', descripcion: 'Cabello virgen peruano', categoria: 'Extensiones', precio: 2890, stock: 0, stockMinimo: 5, activo: false, imagen: 'https://images.unsplash.com/photo-1562322140-8baeececf3df?w=100' },
    ]

    const filteredProducts = computed(() => {
      let result = productos.value

      // Search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo.toLowerCase().includes(query) ||
          p.descripcion.toLowerCase().includes(query)
        )
      }

      // Category filter
      if (filterCategory.value) {
        result = result.filter(p => p.categoria.toLowerCase() === filterCategory.value)
      }

      // Stock filter
      if (filterStock.value === 'available') {
        result = result.filter(p => p.stock > p.stockMinimo)
      } else if (filterStock.value === 'low') {
        result = result.filter(p => p.stock > 0 && p.stock <= p.stockMinimo)
      } else if (filterStock.value === 'out') {
        result = result.filter(p => p.stock === 0)
      }

      return result
    })

    const formatNumber = (num) => {
      return new Intl.NumberFormat('es-MX').format(num)
    }

    const getStockClass = (stock) => {
      if (stock === 0) return 'text-red-600'
      if (stock <= 5) return 'text-orange-600'
      return 'text-gray-900'
    }

    const editProduct = (producto) => {
      console.log('Edit:', producto)
      // router.push(`/admin/productos/${producto.id}/editar`)
    }

    const deleteProduct = (producto) => {
      if (confirm(`¿Estás seguro de eliminar "${producto.nombre}"?`)) {
        console.log('Delete:', producto)
      }
    }

    const loadProducts = async () => {
      loading.value = true
      try {
        // Try to load from API
        const data = await productosService.listar()
        productos.value = data.productos || data.results || data || []
        if (productos.value.length === 0) {
          productos.value = mockProductos
        }
      } catch (err) {
        console.error('Error loading products:', err)
        productos.value = mockProductos
      } finally {
        loading.value = false
      }
    }

    onMounted(loadProducts)

    return {
      loading,
      productos,
      searchQuery,
      filterCategory,
      filterStock,
      currentPage,
      filteredProducts,
      formatNumber,
      getStockClass,
      editProduct,
      deleteProduct
    }
  }
}
</script>
