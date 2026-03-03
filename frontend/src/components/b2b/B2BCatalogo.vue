<template>
  <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-5 lg:py-6">
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
              <p v-if="!categories.length && !isLoadingFilters" class="text-xs text-gray-400 italic">Sin categorías</p>
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

        <!-- Disponibilidad -->
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
            </div>
          </transition>
        </div>

        <!-- Color -->
        <div v-if="colores.length" class="bg-white rounded-xl border border-gray-100 p-4">
          <button 
            @click="toggleSection('colors')"
            class="flex items-center justify-between w-full text-left"
          >
            <span class="font-medium text-gray-900">Color</span>
            <svg class="w-5 h-5 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.colors }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <transition name="collapse">
            <div v-if="openSections.colors" class="mt-3 space-y-2 max-h-48 overflow-y-auto">
              <label 
                v-for="color in colores" 
                :key="color.value"
                class="flex items-center gap-3 cursor-pointer group"
              >
                <input 
                  type="checkbox" 
                  :value="color.value"
                  v-model="filters.colors"
                  class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]"
                />
                <span class="text-sm text-gray-600 group-hover:text-gray-900">{{ color.label }}</span>
                <span class="ml-auto text-xs text-gray-400">({{ color.count }})</span>
              </label>
            </div>
          </transition>
        </div>

        <!-- Tipo -->
        <div v-if="tipos.length" class="bg-white rounded-xl border border-gray-100 p-4">
          <button 
            @click="toggleSection('types')"
            class="flex items-center justify-between w-full text-left"
          >
            <span class="font-medium text-gray-900">Tipo de Cabello</span>
            <svg class="w-5 h-5 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.types }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <transition name="collapse">
            <div v-if="openSections.types" class="mt-3 space-y-2">
              <label 
                v-for="tipo in tipos" 
                :key="tipo.value"
                class="flex items-center gap-3 cursor-pointer group"
              >
                <input 
                  type="checkbox" 
                  :value="tipo.value"
                  v-model="filters.types"
                  class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]"
                />
                <span class="text-sm text-gray-600 group-hover:text-gray-900">{{ tipo.label }}</span>
                <span class="ml-auto text-xs text-gray-400">({{ tipo.count }})</span>
              </label>
            </div>
          </transition>
        </div>
      </div>
    </aside>

    <!-- =========================================================================
         CONTENIDO PRINCIPAL
    ========================================================================== -->
    <div class="flex-1 min-w-0">
      <!-- Header limpio: resultados + controles -->
      <div class="mb-5">
        <!-- Título y conteo -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-1">
          <div>
            <h1 class="text-xl sm:text-2xl font-bold text-gray-900">Catálogo Mayorista</h1>
            <p class="text-sm text-gray-500 mt-0.5">
              {{ filteredProducts.length }} productos encontrados
            </p>
          </div>

          <!-- Controles en línea -->
          <div class="flex items-center gap-2 w-full sm:w-auto">

            <!-- Toggle Vista Grid/Lista (móvil) -->
            <div class="flex items-center border border-gray-200 rounded-lg overflow-hidden lg:hidden">
              <button 
                @click="viewMode = 'list'"
                class="p-2 transition-colors"
                :class="viewMode === 'list' ? 'bg-[#C9A962] text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16"/>
                </svg>
              </button>
              <button 
                @click="viewMode = 'grid'"
                class="p-2 transition-colors"
                :class="viewMode === 'grid' ? 'bg-[#C9A962] text-white' : 'bg-white text-gray-500 hover:bg-gray-50'"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zM14 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"/>
                </svg>
              </button>
            </div>

            <!-- Ordenar -->
            <div class="flex items-center gap-2 flex-1 sm:flex-none">
              <span class="text-sm text-gray-500 hidden sm:inline whitespace-nowrap">Ordenar por</span>
              <select 
                v-model="sortBy"
                class="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:ring-1 focus:ring-[#C9A962]/30 focus:border-[#C9A962] cursor-pointer"
              >
                <option value="relevance">Más relevantes</option>
                <option value="price-asc">Menor precio</option>
                <option value="price-desc">Mayor precio</option>
                <option value="name-asc">A-Z</option>
                <option value="newest">Más nuevos</option>
                <option value="bestseller">Más vendidos</option>
              </select>
            </div>

            <!-- Filtros móvil -->
            <button 
              @click="showMobileFilters = true"
              class="lg:hidden flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              <span v-if="activeFilterCount > 0" class="w-5 h-5 bg-[#C9A962] text-white text-xs font-bold rounded-full flex items-center justify-center">
                {{ activeFilterCount }}
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- Grid/List de Productos -->
      <div 
        v-if="filteredProducts.length > 0"
        :class="[
          viewMode === 'list' 
            ? 'flex flex-col gap-3 lg:grid lg:gap-4 lg:grid-cols-3 xl:grid-cols-4' 
            : 'grid gap-4 grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
        ]"
      >
        <B2BProductCard 
          v-for="product in filteredProducts" 
          :key="product.id"
          :product="product"
          :view-mode="viewMode"
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
            <div class="sticky top-0 bg-white border-b border-gray-100 px-4 py-4 flex items-center justify-between z-10">
              <h3 class="font-semibold text-gray-900">Filtros</h3>
              <button @click="showMobileFilters = false" class="p-2 hover:bg-gray-100 rounded-lg">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <!-- Filtros móvil -->
            <div class="p-4 space-y-4">
              <!-- Categorías -->
              <div class="border-b border-gray-100 pb-4">
                <button @click="toggleSection('m_categories')" class="flex items-center justify-between w-full text-left mb-2">
                  <span class="font-medium text-gray-900 text-sm">Categorías</span>
                  <svg class="w-4 h-4 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.m_categories }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div v-if="openSections.m_categories" class="space-y-2">
                  <label v-for="cat in categories" :key="cat.value" class="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" :value="cat.value" v-model="filters.categories" class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]" />
                    <span class="text-sm text-gray-600">{{ cat.label }}</span>
                    <span class="ml-auto text-xs text-gray-400">({{ cat.count }})</span>
                  </label>
                </div>
              </div>
              <!-- Precio -->
              <div class="border-b border-gray-100 pb-4">
                <p class="font-medium text-gray-900 text-sm mb-2">Precio</p>
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
              <!-- Disponibilidad -->
              <div class="border-b border-gray-100 pb-4">
                <p class="font-medium text-gray-900 text-sm mb-2">Disponibilidad</p>
                <label class="flex items-center gap-3 cursor-pointer">
                  <input type="checkbox" v-model="filters.inStock" class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]" />
                  <span class="text-sm text-gray-600 flex items-center gap-2">
                    <span class="w-2 h-2 bg-emerald-500 rounded-full"></span>
                    Solo en stock
                  </span>
                </label>
              </div>
              <!-- Color -->
              <div v-if="colores.length" class="border-b border-gray-100 pb-4">
                <button @click="toggleSection('m_colors')" class="flex items-center justify-between w-full text-left mb-2">
                  <span class="font-medium text-gray-900 text-sm">Color</span>
                  <svg class="w-4 h-4 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.m_colors }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div v-if="openSections.m_colors" class="space-y-2 max-h-40 overflow-y-auto">
                  <label v-for="color in colores" :key="color.value" class="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" :value="color.value" v-model="filters.colors" class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]" />
                    <span class="text-sm text-gray-600">{{ color.label }}</span>
                    <span class="ml-auto text-xs text-gray-400">({{ color.count }})</span>
                  </label>
                </div>
              </div>
              <!-- Tipo -->
              <div v-if="tipos.length">
                <button @click="toggleSection('m_types')" class="flex items-center justify-between w-full text-left mb-2">
                  <span class="font-medium text-gray-900 text-sm">Tipo de Cabello</span>
                  <svg class="w-4 h-4 text-gray-400 transition-transform" :class="{ 'rotate-180': openSections.m_types }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div v-if="openSections.m_types" class="space-y-2">
                  <label v-for="tipo in tipos" :key="tipo.value" class="flex items-center gap-3 cursor-pointer">
                    <input type="checkbox" :value="tipo.value" v-model="filters.types" class="w-4 h-4 rounded border-gray-300 text-[#C9A962] focus:ring-[#C9A962]" />
                    <span class="text-sm text-gray-600">{{ tipo.label }}</span>
                    <span class="ml-auto text-xs text-gray-400">({{ tipo.count }})</span>
                  </label>
                </div>
              </div>
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
                Ver {{ filteredProducts.length }} productos
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { B2BProductCard, B2BEmptyState, useToast } from './ui'
import { obtenerProductos, obtenerFiltrosB2B } from '@/services/mayoristas'
import { getImageUrl } from '@/services/api'
import { formatColorLabel } from '@/utils/colorLabels'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'B2BCatalogo',
  components: { B2BProductCard, B2BEmptyState },
  setup() {
    const toast = useToast()
    const route = useRoute()
    const router = useRouter()
    
    // State
    const searchQuery = ref('')
    const sortBy = ref('relevance')
    const viewMode = ref(window.innerWidth < 1024 ? 'list' : 'grid')
    const currentPage = ref(1)
    const itemsPerPage = 20
    const showMobileFilters = ref(false)
    const isLoadingProducts = ref(true)
    const isLoadingFilters = ref(true)

    // Filtros
    const filters = reactive({
      categories: [],
      colors: [],
      types: [],
      priceMin: null,
      priceMax: null,
      inStock: false,
      isNew: false,
      isOnSale: false
    })

    const openSections = reactive({
      categories: true,
      price: true,
      stock: true,
      colors: true,
      types: true,
      // Secciones móvil
      m_categories: true,
      m_colors: true,
      m_types: true
    })

    // Datos reales (cargados desde API)
    const categories = ref([])
    const colores = ref([])
    const tipos = ref([])

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
      const retail = parseFloat(producto.precio_retail || producto.retailPrice || 0)
      const wholesale = parseFloat(producto.precio_mayorista || producto.wholesalePrice || 0)

      // Normalización de imagen
      let image = producto.imagen_principal || producto.imagen || producto.imagen_url || producto.image
      if (typeof image === 'string') {
        const cleaned = image.trim()
        if (cleaned) {
          const isFilenameOnly = !cleaned.includes('/') && !cleaned.includes('\\')
          const isStaticRelative = cleaned.startsWith('static/') || cleaned.startsWith('uploads/')
          if (isFilenameOnly) {
            image = `/static/uploads/productos/${cleaned}`
          } else if (isStaticRelative) {
            image = `/${cleaned}`
          } else {
            image = cleaned
          }
          image = getImageUrl(image)
        } else {
          image = null
        }
      } else {
        image = null
      }
      // Normalizar color base (puede ser key o display name)
      const baseColor = producto.color ? formatColorLabel(producto.color) : null

      // Colores de variantes (ya vienen formateados del backend)
      const variantesColores = producto.variantes_colores || []

      return {
        id: producto.id || producto.producto_id,
        name: producto.nombre || producto.name,
        category: producto.categoria || producto.category,
        color: baseColor,
        tipo: producto.tipo || null,
        variantes_colores: variantesColores,
        sku: producto.sku || '',
        image,
        retailPrice: retail,
        wholesalePrice: wholesale,
        stock: producto.stock || 0,
        minOrder: producto.cantidad_minima || producto.minOrder || 1,
        inStock: (producto.stock || 0) > 0,
        isNew: producto.is_new || producto.isNew || false,
        isBestSeller: producto.is_bestseller || producto.isBestSeller || false,
        isOnSale: wholesale < retail && wholesale > 0
      }
    }

    // =========================================================================
    // CARGAR FILTROS DESDE API
    // =========================================================================
    async function cargarFiltros() {
      try {
        isLoadingFilters.value = true
        const data = await obtenerFiltrosB2B()
        if (data) {
          categories.value = (data.categorias || []).map(c => ({
            value: c.value,
            label: c.label,
            count: c.count
          }))
          colores.value = (data.colores || []).map(c => ({
            value: c.value,
            label: c.label,
            count: c.count
          }))
          tipos.value = (data.tipos || []).map(t => ({
            value: t.value,
            label: t.label,
            count: t.count
          }))
        }
      } catch (error) {
        console.error('Error al cargar filtros:', error)
      } finally {
        isLoadingFilters.value = false
      }
    }

    // =========================================================================
    // CARGAR PRODUCTOS DESDE API
    // =========================================================================
    async function cargarProductos() {
      try {
        isLoadingProducts.value = true
        const data = await obtenerProductos({ limite: 1000 })
        products.value = (Array.isArray(data) ? data : []).map(normalizarProducto)
      } catch (error) {
        console.error('Error al cargar productos:', error)
        toast.error('Error al cargar el catálogo. Intenta recargar la página.', 5000)
      } finally {
        isLoadingProducts.value = false
      }
    }

    // Computed
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
        result = result.filter(p => {
          const cat = (p.category || '').toLowerCase()
          return filters.categories.some(fc => fc.toLowerCase() === cat)
        })
      }

      // Filtro colores - busca en producto base Y variantes (como B2C)
      if (filters.colors.length > 0) {
        result = result.filter(p => {
          // Buscar en color base
          if (p.color && filters.colors.includes(p.color)) return true
          // Buscar en colores de variantes
          if (p.variantes_colores && p.variantes_colores.length > 0) {
            return p.variantes_colores.some(vc => filters.colors.includes(vc))
          }
          return false
        })
      }

      // Filtro tipos
      if (filters.types.length > 0) {
        result = result.filter(p => p.tipo && filters.types.includes(p.tipo))
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

      // Filtro Nuevos
      if (filters.isNew) {
        result = result.filter(p => p.isNew)
      }

      // Filtro Ofertas
      if (filters.isOnSale) {
        result = result.filter(p => p.isOnSale)
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
             filters.colors.length > 0 || 
             filters.types.length > 0 || 
             filters.priceMin || 
             filters.priceMax ||
             filters.inStock
    })

    const activeFilterCount = computed(() => {
      let count = filters.categories.length + filters.colors.length + filters.types.length
      if (filters.priceMin || filters.priceMax) count++
      if (filters.inStock) count++
      return count
    })

    const activeFilterTags = computed(() => {
      const tags = []
      filters.categories.forEach(c => {
        const cat = categories.value.find(cat => cat.value === c)
        tags.push({ key: `cat-${c}`, label: cat?.label || c })
      })
      filters.colors.forEach(c => {
        const color = colores.value.find(col => col.value === c)
        tags.push({ key: `color-${c}`, label: color?.label || c })
      })
      filters.types.forEach(t => {
        const tipo = tipos.value.find(tp => tp.value === t)
        tags.push({ key: `type-${t}`, label: tipo?.label || t })
      })
      if (filters.priceMin || filters.priceMax) {
        tags.push({ key: 'price', label: `$${(filters.priceMin || 0).toLocaleString()} - $${(filters.priceMax || '∞').toLocaleString()}` })
      }
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
      } else if (key.startsWith('color-')) {
        const color = key.replace('color-', '')
        filters.colors = filters.colors.filter(c => c !== color)
      } else if (key.startsWith('type-')) {
        const tipo = key.replace('type-', '')
        filters.types = filters.types.filter(t => t !== tipo)
      } else if (key === 'price') {
        filters.priceMin = null
        filters.priceMax = null
      } else if (key === 'inStock') {
        filters.inStock = false
      }
    }

    function clearAllFilters() {
      filters.categories = []
      filters.colors = []
      filters.types = []
      filters.priceMin = null
      filters.priceMax = null
      filters.inStock = false
      filters.isNew = false
      filters.isOnSale = false
      searchQuery.value = ''
    }

    function handleAddToCart({ product, quantity }) {
      const CANTIDAD_MINIMA = 10
      
      if (quantity < CANTIDAD_MINIMA) {
        alert(`La compra mínima para mayoristas es de ${CANTIDAD_MINIMA} unidades por producto.`)
        return
      }
      
      const cart = JSON.parse(localStorage.getItem('b2b_cart') || '{"items":[]}')
      const existing = cart.items.find(i => i.id === product.id)
      if (existing) {
        existing.quantity += quantity
      } else {
        cart.items.push({
          id: product.id,
          producto_id: product.id,
          variante_id: null,
          variante_sku: product.sku || '',
          color: '',
          largo: '',
          nombre: product.name,
          imagen: product.image,
          precio: product.wholesalePrice,
          cantidad_minima_mayorista: product.minOrder || 1,
          descuentos_volumen: [],
          cantidad: quantity
        })
      }
      localStorage.setItem('b2b_cart', JSON.stringify(cart))
      window.dispatchEvent(new CustomEvent('cart-updated'))
      alert(`✓ ${quantity} unidades de "${product.name}" agregadas al carrito`)
    }

    // =========================================================================
    // URL SYNC
    // =========================================================================
    function syncFiltersFromUrl() {
      const q = route.query
      clearAllFilters()
      
      if (q.categoria) {
        filters.categories = [q.categoria]
      }
      if (q.color) {
        filters.colors = [q.color]
      }
      if (q.tipo) {
        filters.types = [q.tipo]
      }
      if (q.nuevo === 'true') {
        filters.isNew = true
      }
      if (q.oferta === 'true') {
        filters.isOnSale = true
      }
      if (q.q) {
        searchQuery.value = q.q
      }
    }

    // Watchers
    watch(() => route.query, () => {
      syncFiltersFromUrl()
    })

    onMounted(() => {
      cargarFiltros()
      cargarProductos()
      syncFiltersFromUrl()
    })

    return {
      searchQuery, sortBy, viewMode, currentPage, itemsPerPage, showMobileFilters,
      filters, openSections, categories, colores, tipos, priceRanges, products,
      isLoadingProducts, isLoadingFilters,
      filteredProducts, totalProducts, totalPages,
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
