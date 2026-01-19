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

        <!-- Refresh button -->
        <button
          @click="loadProducts"
          class="px-4 py-3 bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors"
          :disabled="loading"
        >
          <svg class="w-5 h-5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
      <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
      <div class="flex-1">
        <p class="text-red-800 font-medium">Error al cargar productos</p>
        <p class="text-red-600 text-sm">{{ error }}</p>
      </div>
      <button @click="loadProducts" class="text-red-600 hover:text-red-800 font-medium text-sm">
        Reintentar
      </button>
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
                      :src="producto.imagen_principal || 'https://via.placeholder.com/100?text=Sin+Imagen'" 
                      :alt="producto.nombre"
                      class="w-full h-full object-cover"
                      @error="handleImageError"
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
                  {{ getCategoryLabel(producto) }}
                </span>
              </td>
              
              <!-- Price -->
              <td class="px-6 py-4">
                <span class="font-semibold text-gray-900">${{ formatNumber(producto.precio_monto) }}</span>
              </td>
              
              <!-- Stock -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <span :class="getStockClass(producto.stock_actual, producto.stock_minimo)" class="font-medium">
                    {{ producto.stock_actual }}
                  </span>
                  <span v-if="producto.stock_actual <= producto.stock_minimo && producto.stock_actual > 0" class="text-orange-500">
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
                  <router-link 
                    :to="`/admin/productos/${producto.id}/editar`"
                    class="p-2 text-gray-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="Editar"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </router-link>
                  <button 
                    @click="confirmDelete(producto)"
                    class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Eliminar"
                    :disabled="deleting === producto.id"
                  >
                    <svg v-if="deleting !== producto.id" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Empty State -->
            <tr v-if="filteredProducts.length === 0 && !loading">
              <td colspan="7" class="px-6 py-12 text-center">
                <div class="flex flex-col items-center">
                  <svg class="w-16 h-16 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                  <p class="text-gray-500 mb-4">
                    {{ productos.length === 0 ? 'No hay productos en la base de datos' : 'No se encontraron productos con los filtros aplicados' }}
                  </p>
                  <router-link 
                    v-if="productos.length === 0"
                    to="/admin/productos/nuevo"
                    class="text-brand-600 font-medium hover:underline"
                  >
                    Agregar primer producto
                  </router-link>
                  <button 
                    v-else
                    @click="clearFilters"
                    class="text-brand-600 font-medium hover:underline"
                  >
                    Limpiar filtros
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="productos.length > 0" class="flex items-center justify-between p-4 border-t border-gray-100">
        <p class="text-sm text-gray-500">
          Mostrando {{ filteredProducts.length }} de {{ productos.length }} productos
        </p>
        <div class="flex items-center gap-2">
          <button 
            class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50"
            :disabled="currentPage === 1"
            @click="currentPage--"
          >
            Anterior
          </button>
          <button 
            class="px-4 py-2 text-sm font-medium text-white bg-brand-600 rounded-lg hover:bg-brand-700"
            @click="currentPage++"
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Eliminar Producto</h3>
            <p class="text-gray-500 text-sm">Esta acción no se puede deshacer</p>
          </div>
        </div>
        
        <p class="text-gray-700">
          ¿Estás seguro de que deseas eliminar <span class="font-semibold">{{ productToDelete?.nombre }}</span>?
        </p>
        
        <div class="flex gap-3 justify-end">
          <button 
            @click="showDeleteModal = false"
            class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
          >
            Cancelar
          </button>
          <button 
            @click="deleteProduct"
            :disabled="deleting"
            class="px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            {{ deleting ? 'Eliminando...' : 'Eliminar' }}
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
    const error = ref(null)
    const searchQuery = ref('')
    const filterCategory = ref('')
    const filterStock = ref('')
    const currentPage = ref(1)
    const deleting = ref(null)
    const showDeleteModal = ref(false)
    const productToDelete = ref(null)

    const filteredProducts = computed(() => {
      let result = productos.value

      // Search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo.toLowerCase().includes(query) ||
          (p.descripcion && p.descripcion.toLowerCase().includes(query))
        )
      }

      // Category filter
      if (filterCategory.value) {
        result = result.filter(p => {
          const cat = getCategoryLabel(p).toLowerCase()
          return cat === filterCategory.value.toLowerCase()
        })
      }

      // Stock filter
      if (filterStock.value === 'available') {
        result = result.filter(p => p.stock_actual > p.stock_minimo)
      } else if (filterStock.value === 'low') {
        result = result.filter(p => p.stock_actual > 0 && p.stock_actual <= p.stock_minimo)
      } else if (filterStock.value === 'out') {
        result = result.filter(p => p.stock_actual === 0)
      }

      return result
    })

    const formatNumber = (num) => {
      return new Intl.NumberFormat('es-CO').format(num)
    }

    const getStockClass = (stock, stockMinimo) => {
      if (stock === 0) return 'text-red-600'
      if (stock <= stockMinimo) return 'text-orange-600'
      return 'text-gray-900'
    }

    const getCategoryLabel = (producto) => {
      // Intentar obtener categoría de diferentes fuentes
      if (producto.categoria) return producto.categoria
      if (producto.metodo) {
        const metodoLabels = {
          'clip_in': 'Extensiones',
          'tape_in': 'Extensiones',
          'keratin_bond': 'Extensiones',
          'wig': 'Pelucas',
          'frontal': 'Pelucas',
          'closure': 'Pelucas',
        }
        return metodoLabels[producto.metodo] || 'Extensiones'
      }
      return 'Sin categoría'
    }

    const handleImageError = (e) => {
      e.target.src = 'https://via.placeholder.com/100?text=Sin+Imagen'
    }

    const confirmDelete = (producto) => {
      productToDelete.value = producto
      showDeleteModal.value = true
    }

    const deleteProduct = async () => {
      if (!productToDelete.value) return
      
      deleting.value = productToDelete.value.id
      try {
        await productosService.eliminar(productToDelete.value.id)
        // Remover de la lista local
        productos.value = productos.value.filter(p => p.id !== productToDelete.value.id)
        showDeleteModal.value = false
        productToDelete.value = null
      } catch (err) {
        console.error('Error deleting product:', err)
        error.value = 'Error al eliminar el producto: ' + (err.response?.data?.detail || err.message)
      } finally {
        deleting.value = null
      }
    }

    const clearFilters = () => {
      searchQuery.value = ''
      filterCategory.value = ''
      filterStock.value = ''
    }

    const loadProducts = async () => {
      loading.value = true
      error.value = null
      
      try {
        const data = await productosService.listarTodos()
        // La API puede devolver array directo o objeto con lista
        productos.value = Array.isArray(data) ? data : (data.productos || data.results || [])
        console.log('Productos cargados:', productos.value.length)
      } catch (err) {
        console.error('Error loading products:', err)
        error.value = err.response?.data?.detail || err.message || 'Error de conexión con el servidor'
        productos.value = []
      } finally {
        loading.value = false
      }
    }

    onMounted(loadProducts)

    return {
      loading,
      productos,
      error,
      searchQuery,
      filterCategory,
      filterStock,
      currentPage,
      filteredProducts,
      deleting,
      showDeleteModal,
      productToDelete,
      formatNumber,
      getStockClass,
      getCategoryLabel,
      handleImageError,
      confirmDelete,
      deleteProduct,
      clearFilters,
      loadProducts
    }
  }
}
</script>
