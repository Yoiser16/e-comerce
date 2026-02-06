<template>
  <div class="flex flex-col lg:flex-row gap-6">
    <!-- =========================================================================
         SIDEBAR DE FILTROS (Desktop)
    ========================================================================== -->
    <aside class="hidden lg:block w-72 flex-shrink-0">
      <div class="sticky top-24 space-y-6">
        <!-- Header Filtros -->
        <div class="flex items-center justify-between">
          <h2 class="font-semibold text-gray-900">Filtros</h2>
          <button 
            v-if="hasActiveFilters"
            @click="clearAllFilters"
            class="text-sm text-[#C9A962] hover:underline"
          >
            Limpiar todo
          </button>
        </div>

        <!-- Filtros Activos -->
        <div v-if="activeFilterTags.length > 0" class="flex flex-wrap gap-2">
          <span 
            v-for="tag in activeFilterTags" 
            :key="tag.key"
            class="inline-flex items-center gap-1 px-2 py-1 bg-[#C9A962]/10 text-[#C9A962] text-xs font-medium rounded-full"
          >
            {{ tag.label }}
            <button @click="removeFilter(tag.key)" class="hover:text-[#A8893D]">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </span>
        </div>

        <!-- Categorías -->
        <div class="bg-white rounded-xl border border-gray-100 p-4">
          <button 
            @click="toggleSection('categories')"
            class="flex items-center justify-between w-full text-left"
          >
            <span class="font-medium text-gray-900">Categorías</span>
            <svg class="w-5 h-5 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.categories }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <transition name="collapse">
            <div v-if="openSections.categories" class="mt-3 space-y-2">
              <label 
                v-for="cat in categories" 
                :key="cat.value"
                class="flex items-center gap-3 cursor-pointer group"
              >
                <input 
                  type="checkbox" 
                  :value="cat.value"
                  v-model="filters.categories"
                  class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]"
                />
                <span class="text-sm text-gray-600 group-hover:text-gray-900">{{ cat.label }}</span>
                <span class="ml-auto text-xs text-gray-400">({{ cat.count }})</span>
              </label>
            </div>
          </transition>
        </div>

        <!-- Precio -->
        <div class="bg-white rounded-xl border border-gray-100 p-4">
          <button 
            @click="toggleSection('price')"
            class="flex items-center justify-between w-full text-left"
          >
            <span class="font-medium text-gray-900">Precio Mayorista</span>
            <svg class="w-5 h-5 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.price }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <transition name="collapse">
            <div v-if="openSections.price" class="mt-3 space-y-3">
              <div class="flex items-center gap-2">
                <input 
                  v-model.number="filters.priceMin"
                  type="number"
                  placeholder="Mín"
                  class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
                <span class="text-gray-400">-</span>
                <input 
                  v-model.number="filters.priceMax"
                  type="number"
                  placeholder="Máx"
                  class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
              </div>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="range in priceRanges" 
                  :key="range.label"
                  @click="setPriceRange(range)"
                  class="px-3 py-1.5 text-xs font-medium rounded-full border transition-colors"
                  :class="isPriceRangeActive(range) ? 'bg-[#C9A962] text-white border-[#C9A962]' : 'border-gray-200 text-gray-600 hover:border-[#C9A962]'"
                >
                  {{ range.label }}
                </button>
              </div>
            </div>
          </transition>
        </div>

        <!-- Stock -->
        <div class="bg-white rounded-xl border border-gray-100 p-4">
          <button 
            @click="toggleSection('stock')"
            class="flex items-center justify-between w-full text-left"
          >
            <span class="font-medium text-gray-900">Disponibilidad</span>
            <svg class="w-5 h-5 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.stock }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <transition name="collapse">
            <div v-if="openSections.stock" class="mt-3 space-y-2">
              <label class="flex items-center gap-3 cursor-pointer group">
                <input type="checkbox" v-model="filters.inStock" class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]" />
                <span class="text-sm text-gray-600 group-hover:text-gray-900 flex items-center gap-2">
                  <span class="w-2 h-2 bg-emerald-500 rounded-full"></span>
                  Solo en stock
                </span>
              </label>
              <label class="flex items-center gap-3 cursor-pointer group">
                <input type="checkbox" v-model="filters.fastShipping" class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]" />
                <span class="text-sm text-gray-600 group-hover:text-gray-900 flex items-center gap-2">
                  <svg class="w-4 h-4 text-[#C9A962]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Envío inmediato
                </span>
              </label>
            </div>
          </transition>
        </div>

        <!-- Marcas -->
        <div class="bg-white rounded-xl border border-gray-100 p-4">
          <button 
            @click="toggleSection('brands')"
            class="flex items-center justify-between w-full text-left"
          >
            <span class="font-medium text-gray-900">Marcas</span>
            <svg class="w-5 h-5 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.brands }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <transition name="collapse">
            <div v-if="openSections.brands" class="mt-3">
              <input 
                v-model="brandSearch"
                type="text"
                placeholder="Buscar marca..."
                class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm mb-3 focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
              />
              <div class="space-y-2 max-h-48 overflow-y-auto">
                <label 
                  v-for="brand in filteredBrands" 
                  :key="brand.value"
                  class="flex items-center gap-3 cursor-pointer group"
                >
                  <input 
                    type="checkbox" 
                    :value="brand.value"
                    v-model="filters.brands"
                    class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]"
                  />
                  <span class="text-sm text-gray-600 group-hover:text-gray-900">{{ brand.label }}</span>
                </label>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </aside>

    <!-- =========================================================================
         CONTENIDO PRINCIPAL
    ========================================================================== -->
    <div class="flex-1 min-w-0">
      <!-- Header con búsqueda y controles -->
      <div class="bg-white rounded-xl border border-gray-100 p-4 mb-6">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <!-- Título y resultados -->
          <div>
            <h1 class="text-xl sm:text-2xl font-bold text-gray-900">Catálogo Mayorista</h1>
            <p class="text-sm text-gray-500 mt-1">
              {{ filteredProducts.length }} productos encontrados
            </p>
          </div>

          <!-- Controles -->
          <div class="flex items-center gap-3 w-full sm:w-auto">
            <!-- Búsqueda -->
            <div class="relative flex-1 sm:w-64">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar productos, SKU..."
                class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none text-sm"
              />
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>

            <!-- Ordenar -->
            <select 
              v-model="sortBy"
              class="px-4 py-2.5 border border-gray-200 rounded-xl text-sm bg-white focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] cursor-pointer"
            >
              <option value="relevance">Más relevantes</option>
              <option value="price-asc">Menor precio</option>
              <option value="price-desc">Mayor precio</option>
              <option value="name-asc">A-Z</option>
              <option value="newest">Más nuevos</option>
              <option value="bestseller">Más vendidos</option>
            </select>

            <!-- Filtros móvil -->
            <button 
              @click="showMobileFilters = true"
              class="lg:hidden flex items-center gap-2 px-4 py-2.5 border border-gray-200 rounded-xl hover:bg-gray-50"
            >
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              <span v-if="activeFilterCount > 0" class="w-5 h-5 bg-[#C9A962] text-white text-xs font-bold rounded-full flex items-center justify-center">
                {{ activeFilterCount }}
              </span>
            </button>

            <!-- Vista Grid/List -->
            <div class="hidden sm:flex items-center border border-gray-200 rounded-xl overflow-hidden">
              <button 
                @click="viewMode = 'grid'"
                class="p-2.5 transition-colors"
                :class="viewMode === 'grid' ? 'bg-[#C9A962] text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
              </button>
              <button 
                @click="viewMode = 'list'"
                class="p-2.5 transition-colors"
                :class="viewMode === 'list' ? 'bg-[#C9A962] text-white' : 'bg-white text-gray-600 hover:bg-gray-50'"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Grid de Productos -->
      <div 
        v-if="filteredProducts.length > 0"
        class="grid gap-4"
        :class="viewMode === 'grid' ? 'grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' : 'grid-cols-1'"
      >
        <B2BProductCard 
          v-for="product in filteredProducts" 
          :key="product.id"
          :product="product"
          @add-to-cart="handleAddToCart"
        />
      </div>

      <!-- Empty State -->
      <B2BEmptyState 
        v-else
        type="products"
        title="No se encontraron productos"
        description="Intenta ajustar los filtros o buscar con otros términos"
      >
        <template #action>
          <button 
            @click="clearAllFilters"
            class="px-6 py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-xl transition-colors"
          >
            Limpiar filtros
          </button>
        </template>
      </B2BEmptyState>

      <!-- Paginación -->
      <div v-if="filteredProducts.length > 0" class="mt-8 flex items-center justify-between">
        <p class="text-sm text-gray-500">
          Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, totalProducts) }} de {{ totalProducts }} productos
        </p>
        <div class="flex items-center gap-2">
          <button 
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <span class="px-4 py-2 text-sm font-medium">{{ currentPage }} / {{ totalPages }}</span>
          <button 
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- =========================================================================
         MODAL DE FILTROS MÓVIL
    ========================================================================== -->
    <Teleport to="body">
      <transition name="slide-up">
        <div 
          v-if="showMobileFilters"
          class="fixed inset-0 z-50 lg:hidden"
        >
          <div class="absolute inset-0 bg-black/50" @click="showMobileFilters = false"></div>
          <div class="absolute bottom-0 left-0 right-0 bg-white rounded-t-3xl max-h-[85vh] overflow-y-auto">
            <!-- Header -->
            <div class="sticky top-0 bg-white border-b border-gray-100 px-4 py-4 flex items-center justify-between">
              <h3 class="font-semibold text-gray-900">Filtros</h3>
              <button @click="showMobileFilters = false" class="p-2 hover:bg-gray-100 rounded-lg">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <!-- Filtros aquí (replicar sidebar) -->
            <div class="p-4 space-y-4">
              <p class="text-center text-gray-500 py-8">Filtros móvil próximamente...</p>
            </div>
            <!-- Footer -->
            <div class="sticky bottom-0 bg-white border-t border-gray-100 p-4 flex gap-3">
              <button 
                @click="clearAllFilters"
                class="flex-1 py-3 border border-gray-200 text-gray-700 font-medium rounded-xl hover:bg-gray-50"
              >
                Limpiar
              </button>
              <button 
                @click="showMobileFilters = false"
                class="flex-1 py-3 bg-[#1A1A1A] text-white font-medium rounded-xl hover:bg-black"
              >
                Aplicar filtros
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted } from 'vue'
import { B2BProductCard, B2BEmptyState } from './ui'
import { obtenerProductos } from '@/services/mayoristas'
import { useToast } from './ui'

export default {
  name: 'B2BCatalogo',
  components: { B2BProductCard, B2BEmptyState },
  setup() {
    const toast = useToast()
    
    // State
    const searchQuery = ref('')
    const sortBy = ref('relevance')
    const viewMode = ref('grid')
    const currentPage = ref(1)
    const itemsPerPage = 20
    const showMobileFilters = ref(false)
    const brandSearch = ref('')
    const isLoadingProducts = ref(true)

    // Filtros
    const filters = reactive({
      categories: [],
      brands: [],
      priceMin: null,
      priceMax: null,
      inStock: false,
      fastShipping: false
    })

    const openSections = reactive({
      categories: true,
      price: true,
      stock: true,
      brands: true
    })

    // Datos de ejemplo
    const categories = ref([
      { value: 'extensiones', label: 'Extensiones', count: 142 },
      { value: 'tratamientos', label: 'Tratamientos', count: 89 },
      { value: 'herramientas', label: 'Herramientas', count: 67 },
      { value: 'coloracion', label: 'Coloración', count: 54 },
      { value: 'maquillaje', label: 'Maquillaje', count: 128 },
      { value: 'skincare', label: 'Skincare', count: 76 }
    ])

    const brands = ref([
      { value: 'mac', label: 'MAC Cosmetics' },
      { value: 'nars', label: 'NARS' },
      { value: 'charlotte', label: 'Charlotte Tilbury' },
      { value: 'fenty', label: 'Fenty Beauty' },
      { value: 'kharis', label: 'Kharis Pro' },
      { value: 'olaplex', label: 'Olaplex' },
      { value: 'redken', label: 'Redken' }
    ])

    const priceRanges = [
      { label: 'Hasta $50K', min: 0, max: 50000 },
      { label: '$50K - $100K', min: 50000, max: 100000 },
      { label: '$100K - $200K', min: 100000, max: 200000 },
      { label: '+$200K', min: 200000, max: null }
    ]

    // Productos (cargados desde API)
    const products = ref([])

    // =========================================================================
    // NORMALIZAR DATOS DE PRODUCTOS
    // =========================================================================
    function normalizarProducto(producto) {
      return {
        id: producto.id || producto.producto_id,
        name: producto.nombre || producto.name,
        category: producto.categoria || producto.category,
        sku: producto.sku || '',
        image: producto.imagen || producto.image || 'https://placehold.co/400x400',
        retailPrice: producto.precio_retail || producto.retailPrice || 0,
        wholesalePrice: producto.precio_mayorista || producto.wholesalePrice || 0,
        stock: producto.stock || 0,
        minOrder: producto.cantidad_minima || producto.minOrder || 1,
        inStock: (producto.stock || 0) > 0,
        isNew: producto.is_new || producto.isNew || false,
        isBestSeller: producto.is_bestseller || producto.isBestSeller || false
      }
    }

    // =========================================================================
    // CARGAR PRODUCTOS DESDE API
    // =========================================================================
    async function cargarProductos() {
      try {
        isLoadingProducts.value = true
        const data = await obtenerProductos()
        products.value = (Array.isArray(data) ? data : []).map(normalizarProducto)
      } catch (error) {
        console.error('Error al cargar productos:', error)
        toast.error('Error al cargar el catálogo. Intenta recargar la página.', 5000)
      } finally {
        isLoadingProducts.value = false
      }
    }

    // Computed
    const filteredBrands = computed(() => {
      if (!brandSearch.value) return brands.value
      return brands.value.filter(b => b.label.toLowerCase().includes(brandSearch.value.toLowerCase()))
    })

    const filteredProducts = computed(() => {
      let result = [...products.value]

      // Búsqueda
      if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase()
        result = result.filter(p => 
          p.name.toLowerCase().includes(q) || 
          p.sku?.toLowerCase().includes(q) ||
          p.category?.toLowerCase().includes(q)
        )
      }

      // Filtro categorías
      if (filters.categories.length > 0) {
        result = result.filter(p => filters.categories.includes(p.category?.toLowerCase()))
      }

      // Filtro precio
      if (filters.priceMin) {
        result = result.filter(p => p.wholesalePrice >= filters.priceMin)
      }
      if (filters.priceMax) {
        result = result.filter(p => p.wholesalePrice <= filters.priceMax)
      }

      // Filtro stock
      if (filters.inStock) {
        result = result.filter(p => p.inStock && p.stock > 0)
      }

      // Ordenar
      switch(sortBy.value) {
        case 'price-asc': result.sort((a, b) => a.wholesalePrice - b.wholesalePrice); break
        case 'price-desc': result.sort((a, b) => b.wholesalePrice - a.wholesalePrice); break
        case 'name-asc': result.sort((a, b) => a.name.localeCompare(b.name)); break
        case 'newest': result.sort((a, b) => (b.isNew ? 1 : 0) - (a.isNew ? 1 : 0)); break
        case 'bestseller': result.sort((a, b) => (b.isBestSeller ? 1 : 0) - (a.isBestSeller ? 1 : 0)); break
      }

      return result
    })

    const totalProducts = computed(() => filteredProducts.value.length)
    const totalPages = computed(() => Math.ceil(totalProducts.value / itemsPerPage))

    const hasActiveFilters = computed(() => {
      return filters.categories.length > 0 || 
             filters.brands.length > 0 || 
             filters.priceMin || 
             filters.priceMax ||
             filters.inStock ||
             filters.fastShipping
    })

    const activeFilterCount = computed(() => {
      let count = filters.categories.length + filters.brands.length
      if (filters.priceMin || filters.priceMax) count++
      if (filters.inStock) count++
      if (filters.fastShipping) count++
      return count
    })

    const activeFilterTags = computed(() => {
      const tags = []
      filters.categories.forEach(c => tags.push({ key: `cat-${c}`, label: categories.value.find(cat => cat.value === c)?.label || c }))
      if (filters.priceMin || filters.priceMax) tags.push({ key: 'price', label: `$${(filters.priceMin || 0).toLocaleString()} - $${(filters.priceMax || '∞').toLocaleString()}` })
      if (filters.inStock) tags.push({ key: 'inStock', label: 'En stock' })
      return tags
    })

    // Methods
    function toggleSection(section) {
      openSections[section] = !openSections[section]
    }

    function setPriceRange(range) {
      filters.priceMin = range.min
      filters.priceMax = range.max
    }

    function isPriceRangeActive(range) {
      return filters.priceMin === range.min && filters.priceMax === range.max
    }

    function removeFilter(key) {
      if (key.startsWith('cat-')) {
        const cat = key.replace('cat-', '')
        filters.categories = filters.categories.filter(c => c !== cat)
      } else if (key === 'price') {
        filters.priceMin = null
        filters.priceMax = null
      } else if (key === 'inStock') {
        filters.inStock = false
      }
    }

    function clearAllFilters() {
      filters.categories = []
      filters.brands = []
      filters.priceMin = null
      filters.priceMax = null
      filters.inStock = false
      filters.fastShipping = false
      searchQuery.value = ''
    }

    function handleAddToCart({ product, quantity }) {
      console.log('Agregando al carrito:', product.name, 'x', quantity)
      // TODO: Integrar con servicio de carrito B2B
      const cart = JSON.parse(localStorage.getItem('b2b_cart') || '{"items":[]}')
      const existing = cart.items.find(i => i.id === product.id)
      if (existing) {
        existing.quantity += quantity
      } else {
        cart.items.push({ ...product, quantity })
      }
      localStorage.setItem('b2b_cart', JSON.stringify(cart))
      alert(`✓ ${quantity} unidades de "${product.name}" agregadas al carrito`)
    }

    // =========================================================================
    // LIFECYCLE
    // =========================================================================
    onMounted(() => {
      cargarProductos()
    })

    return {
      searchQuery, sortBy, viewMode, currentPage, itemsPerPage, showMobileFilters, brandSearch,
      filters, openSections, categories, brands, priceRanges, products, isLoadingProducts,
      filteredBrands, filteredProducts, totalProducts, totalPages,
      hasActiveFilters, activeFilterCount, activeFilterTags,
      toggleSection, setPriceRange, isPriceRangeActive, removeFilter, clearAllFilters, handleAddToCart
    }
  }
}
</script>

<style scoped>
.collapse-enter-active, .collapse-leave-active { transition: all 0.3s ease; }
.collapse-enter-from, .collapse-leave-to { opacity: 0; max-height: 0; overflow: hidden; }
.collapse-enter-to, .collapse-leave-from { max-height: 500px; }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); }
</style>
