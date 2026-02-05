<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-luxury text-text-dark">Catálogo Mayorista</h1>
        <p class="text-text-light">Precios exclusivos para distribuidores</p>
      </div>
      
      <!-- Search & Filters -->
      <div class="flex items-center gap-3">
        <div class="relative flex-1 sm:w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar productos..."
            class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none"
          />
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        
        <button 
          @click="showFilters = !showFilters"
          class="p-2 border border-gray-200 rounded-lg hover:bg-gray-50"
        >
          <svg class="w-5 h-5 text-text-medium" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Filters Panel -->
    <transition name="slide-down">
      <div v-if="showFilters" class="bg-white rounded-lg p-4 shadow-sm">
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-text-medium mb-1">Categoría</label>
            <select v-model="filters.category" class="w-full px-3 py-2 border border-gray-200 rounded-lg">
              <option value="">Todas</option>
              <option value="maquillaje">Maquillaje</option>
              <option value="skincare">Skincare</option>
              <option value="cabello">Cabello</option>
              <option value="accesorios">Accesorios</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-text-medium mb-1">Marca</label>
            <select v-model="filters.brand" class="w-full px-3 py-2 border border-gray-200 rounded-lg">
              <option value="">Todas</option>
              <option value="mac">MAC</option>
              <option value="nars">NARS</option>
              <option value="charlotte">Charlotte Tilbury</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-text-medium mb-1">Precio</label>
            <select v-model="filters.priceRange" class="w-full px-3 py-2 border border-gray-200 rounded-lg">
              <option value="">Cualquiera</option>
              <option value="0-50000">Hasta $50.000</option>
              <option value="50000-100000">$50.000 - $100.000</option>
              <option value="100000+">Más de $100.000</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-text-medium mb-1">Stock</label>
            <select v-model="filters.stock" class="w-full px-3 py-2 border border-gray-200 rounded-lg">
              <option value="">Todos</option>
              <option value="in-stock">En Stock</option>
              <option value="low-stock">Stock Bajo</option>
            </select>
          </div>
        </div>
      </div>
    </transition>

    <!-- Products Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
      <div 
        v-for="product in products" 
        :key="product.id"
        class="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow group"
      >
        <!-- Image -->
        <div class="aspect-square bg-gray-100 relative overflow-hidden">
          <img 
            :src="product.image" 
            :alt="product.name"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <!-- Discount Badge -->
          <span 
            v-if="product.discount > 0"
            class="absolute top-2 left-2 bg-[#C9A962] text-white text-xs font-medium px-2 py-1 rounded"
          >
            -{{ product.discount }}%
          </span>
        </div>
        
        <!-- Info -->
        <div class="p-4">
          <p class="text-xs text-text-light mb-1">{{ product.brand }}</p>
          <h3 class="font-medium text-text-dark text-sm mb-2 line-clamp-2">{{ product.name }}</h3>
          
          <!-- Pricing -->
          <div class="mb-3">
            <div class="flex items-baseline gap-2">
              <span class="text-lg font-bold text-[#C9A962]">${{ product.wholesalePrice.toLocaleString() }}</span>
              <span class="text-xs text-text-light line-through">${{ product.retailPrice.toLocaleString() }}</span>
            </div>
            <p class="text-xs text-green-600 mt-1">
              Ahorro: ${{ (product.retailPrice - product.wholesalePrice).toLocaleString() }}
            </p>
          </div>

          <!-- Stock & Min Order -->
          <div class="flex items-center justify-between text-xs text-text-light mb-3">
            <span>Stock: {{ product.stock }}</span>
            <span>Mín: {{ product.minOrder }} uds</span>
          </div>

          <!-- Add to Cart -->
          <div class="flex items-center gap-2">
            <input 
              v-model.number="product.quantity"
              type="number"
              :min="product.minOrder"
              :max="product.stock"
              class="w-16 px-2 py-2 border border-gray-200 rounded text-center text-sm"
            />
            <button 
              @click="addToCart(product)"
              class="flex-1 py-2 bg-[#1A1A1A] hover:bg-black text-white text-sm font-medium rounded transition-colors"
            >
              Agregar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="products.length === 0" class="text-center py-12 bg-white rounded-lg">
      <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
      </svg>
      <h3 class="text-lg font-medium text-text-dark mb-2">No se encontraron productos</h3>
      <p class="text-text-light">Intenta con otros filtros de búsqueda</p>
    </div>

    <!-- Load More -->
    <div v-if="hasMore" class="text-center">
      <button 
        @click="loadMore"
        class="px-6 py-3 border border-[#C9A962] text-[#C9A962] font-medium rounded-lg hover:bg-[#C9A962]/10 transition-colors"
      >
        Cargar más productos
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'B2BCatalogo',
  setup() {
    const searchQuery = ref('')
    const showFilters = ref(false)
    const filters = ref({
      category: '',
      brand: '',
      priceRange: '',
      stock: ''
    })
    const hasMore = ref(true)

    // Mock products - TODO: Conectar con API
    const products = ref([
      {
        id: 1,
        name: 'Labial MAC Ruby Woo Matte',
        brand: 'MAC',
        image: '/placeholder-product.jpg',
        retailPrice: 95000,
        wholesalePrice: 72000,
        discount: 24,
        stock: 150,
        minOrder: 6,
        quantity: 6
      },
      {
        id: 2,
        name: 'NARS Orgasm Blush',
        brand: 'NARS',
        image: '/placeholder-product.jpg',
        retailPrice: 125000,
        wholesalePrice: 94000,
        discount: 25,
        stock: 80,
        minOrder: 3,
        quantity: 3
      },
      {
        id: 3,
        name: 'Charlotte Tilbury Pillow Talk Set',
        brand: 'Charlotte Tilbury',
        image: '/placeholder-product.jpg',
        retailPrice: 185000,
        wholesalePrice: 145000,
        discount: 22,
        stock: 45,
        minOrder: 2,
        quantity: 2
      },
      {
        id: 4,
        name: 'Fenty Beauty Pro Filt\'r Foundation',
        brand: 'Fenty Beauty',
        image: '/placeholder-product.jpg',
        retailPrice: 135000,
        wholesalePrice: 102000,
        discount: 24,
        stock: 200,
        minOrder: 4,
        quantity: 4
      },
    ])

    function addToCart(product) {
      console.log('Agregando al carrito:', product.name, 'x', product.quantity)
      // TODO: Implementar lógica de carrito B2B
      alert(`${product.quantity} unidades de "${product.name}" agregadas al carrito`)
    }

    function loadMore() {
      // TODO: Cargar más productos desde API
      hasMore.value = false
    }

    return {
      searchQuery,
      showFilters,
      filters,
      products,
      hasMore,
      addToCart,
      loadMore
    }
  }
}
</script>

<style scoped>
.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from, .slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
