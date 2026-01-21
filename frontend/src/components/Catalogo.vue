<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    <!-- Hero Minimalista -->
    <div class="bg-white border-b border-text-dark/5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-8 sm:py-12">
        <!-- Navegación -->
        <div class="flex items-center justify-between mb-6 sm:mb-8">
          <button 
            @click="$router.back()" 
            class="inline-flex items-center gap-2 text-text-medium hover:text-text-dark text-sm transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            Volver
          </button>
          <button 
            @click="mostrarCarrito = true"
            class="inline-flex items-center gap-2 px-3 py-2 border border-text-dark/10 rounded-full hover:border-text-dark/30 transition-colors text-sm text-text-medium hover:text-text-dark"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l1 7h12l1.5-5H6m0 0H3m13 7h3m-3 0a1 1 0 1 0 0 2h3a1 1 0 1 0 0-2m-12-1a1 1 0 1 0 0 2 1 1 0 0 0 0-2z" />
            </svg>
            Ver carrito (<span>{{ cartCount }}</span>)
          </button>
        </div>
        <!-- Título -->
        <h1 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-text-dark mb-3">Catálogo Completo</h1>
        <p class="text-text-medium text-sm sm:text-base max-w-2xl">Explora nuestra colección exclusiva de extensiones de cabello premium</p>
      </div>
    </div>

    <!-- Contenedor Principal -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-8 sm:py-12">
      <div class="lg:grid lg:grid-cols-12 lg:gap-8">
        
        <!-- Sidebar de Filtros (Desktop) -->
        <aside class="hidden lg:block lg:col-span-3 space-y-6">
          <!-- Categorías -->
          <div class="bg-white rounded-lg p-6 border border-text-dark/5">
            <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-4">Categorías</h3>
            <div class="space-y-2">
              <button 
                @click="filtroCategoria = null"
                :class="filtroCategoria === null ? 'text-text-dark font-medium' : 'text-text-medium hover:text-text-dark'"
                class="block text-sm transition-colors w-full text-left"
              >
                Todas las categorías
              </button>
              <button 
                v-for="cat in categorias" 
                :key="cat.id"
                @click="filtroCategoria = cat.nombre"
                :class="filtroCategoria === cat.nombre ? 'text-text-dark font-medium' : 'text-text-medium hover:text-text-dark'"
                class="block text-sm transition-colors w-full text-left"
              >
                {{ cat.nombre }}
              </button>
            </div>
          </div>

          <!-- Filtro de Precio -->
          <div class="bg-white rounded-lg p-6 border border-text-dark/5">
            <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-4">Precio</h3>
            <div class="space-y-3">
              <div class="flex items-center gap-3">
                <input 
                  v-model.number="precioMin" 
                  type="number" 
                  placeholder="Mín"
                  class="w-full px-3 py-2 border border-text-dark/10 rounded text-sm focus:outline-none focus:border-text-dark/30"
                >
                <span class="text-text-medium">-</span>
                <input 
                  v-model.number="precioMax" 
                  type="number" 
                  placeholder="Máx"
                  class="w-full px-3 py-2 border border-text-dark/10 rounded text-sm focus:outline-none focus:border-text-dark/30"
                >
              </div>
            </div>
          </div>

          <!-- Filtro por Color -->
          <div class="bg-white rounded-lg p-6 border border-text-dark/5">
            <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-4">Color</h3>
            <div class="space-y-2">
              <label v-for="color in coloresDisponibles" :key="color" class="flex items-center gap-2 text-sm text-text-medium hover:text-text-dark cursor-pointer">
                <input 
                  type="checkbox" 
                  :value="color" 
                  v-model="filtrosColor"
                  class="rounded border-text-dark/20"
                >
                {{ color }}
              </label>
            </div>
          </div>

          <!-- Filtro por Tipo -->
          <div class="bg-white rounded-lg p-6 border border-text-dark/5">
            <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-4">Tipo</h3>
            <div class="space-y-2">
              <label v-for="tipo in tiposDisponibles" :key="tipo" class="flex items-center gap-2 text-sm text-text-medium hover:text-text-dark cursor-pointer">
                <input 
                  type="checkbox" 
                  :value="tipo" 
                  v-model="filtrosTipo"
                  class="rounded border-text-dark/20"
                >
                {{ tipo }}
              </label>
            </div>
          </div>

          <!-- Limpiar Filtros -->
          <button 
            @click="limpiarFiltros"
            class="w-full px-4 py-2 text-sm text-text-medium hover:text-text-dark border border-text-dark/10 hover:border-text-dark/30 rounded transition-all"
          >
            Limpiar filtros
          </button>
        </aside>

        <!-- Grid de Productos -->
        <main class="lg:col-span-9">
          <!-- Barra Superior (Móvil: Botón Filtros + Ordenar) -->
          <div class="flex items-center justify-between mb-6">
            <!-- Botón Filtros Móvil -->
            <button 
              @click="mostrarFiltrosMobile = true"
              class="lg:hidden flex items-center gap-2 px-4 py-2 border border-text-dark/10 rounded text-sm text-text-dark"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Filtros
            </button>

            <!-- Contador de Resultados -->
            <p class="text-sm text-text-medium">
              {{ productosFiltrados.length }} {{ productosFiltrados.length === 1 ? 'producto' : 'productos' }}
            </p>

            <!-- Ordenar -->
            <select 
              v-model="ordenar"
              class="px-4 py-2 border border-text-dark/10 rounded text-sm focus:outline-none focus:border-text-dark/30"
            >
              <option value="recientes">Más recientes</option>
              <option value="precio-asc">Precio: Menor a Mayor</option>
              <option value="precio-desc">Precio: Mayor a Menor</option>
              <option value="nombre">Nombre A-Z</option>
            </select>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4 sm:gap-6">
            <div v-for="n in 9" :key="n" class="animate-pulse">
              <div class="aspect-square bg-gray-200 rounded-lg mb-3"></div>
              <div class="h-4 bg-gray-200 rounded mb-2"></div>
              <div class="h-4 bg-gray-200 rounded w-2/3"></div>
            </div>
          </div>

          <!-- Grid de Productos -->
          <div v-else-if="productosFiltrados.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4 sm:gap-6">
            <div 
              v-for="producto in productosFiltrados" 
              :key="producto.id"
              @click="verProducto(producto.id)"
              class="group cursor-pointer"
            >
              <!-- Imagen -->
              <div class="aspect-square bg-[#F5F5F5] rounded-lg overflow-hidden mb-3 border border-text-dark/5">
                <img 
                  v-if="producto.imagen_principal"
                  :src="getImageUrl(producto.imagen_principal)" 
                  :alt="producto.nombre"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  @error="handleImageError"
                >
                <div v-else class="w-full h-full flex items-center justify-center">
                  <svg class="w-12 h-12 text-text-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>

              <!-- Info -->
              <div class="space-y-1">
                <h3 class="text-sm font-medium text-text-dark line-clamp-2 group-hover:text-text-dark/70 transition-colors">
                  {{ producto.nombre }}
                </h3>
                <p class="text-sm text-text-dark font-semibold">{{ formatearPrecio(producto.precio_monto) }}</p>
                <div v-if="producto.color || producto.largo" class="flex items-center gap-2 text-xs text-text-light">
                  <span v-if="producto.color">{{ producto.color }}</span>
                  <span v-if="producto.color && producto.largo">•</span>
                  <span v-if="producto.largo">{{ producto.largo }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Sin Resultados -->
          <div v-else class="text-center py-16">
            <svg class="w-16 h-16 mx-auto text-text-light mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p class="text-text-medium">No se encontraron productos con estos filtros</p>
            <button 
              @click="limpiarFiltros"
              class="mt-4 text-sm text-text-dark hover:underline"
            >
              Limpiar filtros
            </button>
          </div>
        </main>
      </div>
    </div>

    <!-- Modal de Filtros Móvil -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div 
          v-if="mostrarFiltrosMobile"
          class="fixed inset-0 bg-black/50 z-50 lg:hidden"
          @click.self="mostrarFiltrosMobile = false"
        >
          <div class="absolute right-0 top-0 bottom-0 w-full max-w-sm bg-white overflow-y-auto">
            <!-- Header -->
            <div class="sticky top-0 bg-white border-b border-text-dark/5 px-4 py-4 flex items-center justify-between">
              <h2 class="text-lg font-semibold text-text-dark">Filtros</h2>
              <button @click="mostrarFiltrosMobile = false" class="p-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Filtros -->
            <div class="p-4 space-y-6">
              <!-- Categorías -->
              <div>
                <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-3">Categorías</h3>
                <div class="space-y-2">
                  <button 
                    @click="filtroCategoria = null"
                    :class="filtroCategoria === null ? 'text-text-dark font-medium' : 'text-text-medium'"
                    class="block text-sm w-full text-left"
                  >
                    Todas
                  </button>
                  <button 
                    v-for="cat in categorias" 
                    :key="cat.id"
                    @click="filtroCategoria = cat.nombre"
                    :class="filtroCategoria === cat.nombre ? 'text-text-dark font-medium' : 'text-text-medium'"
                    class="block text-sm w-full text-left"
                  >
                    {{ cat.nombre }}
                  </button>
                </div>
              </div>

              <!-- Resto de filtros (igual que desktop) -->
              <div>
                <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-3">Precio</h3>
                <div class="flex items-center gap-3">
                  <input v-model.number="precioMin" type="number" placeholder="Mín" class="w-full px-3 py-2 border border-text-dark/10 rounded text-sm">
                  <span>-</span>
                  <input v-model.number="precioMax" type="number" placeholder="Máx" class="w-full px-3 py-2 border border-text-dark/10 rounded text-sm">
                </div>
              </div>

              <div>
                <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-3">Color</h3>
                <div class="space-y-2">
                  <label v-for="color in coloresDisponibles" :key="color" class="flex items-center gap-2 text-sm">
                    <input type="checkbox" :value="color" v-model="filtrosColor" class="rounded border-text-dark/20">
                    {{ color }}
                  </label>
                </div>
              </div>

              <div>
                <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-3">Tipo</h3>
                <div class="space-y-2">
                  <label v-for="tipo in tiposDisponibles" :key="tipo" class="flex items-center gap-2 text-sm">
                    <input type="checkbox" :value="tipo" v-model="filtrosTipo" class="rounded border-text-dark/20">
                    {{ tipo }}
                  </label>
                </div>
              </div>
            </div>

            <!-- Footer con botones -->
            <div class="sticky bottom-0 bg-white border-t border-text-dark/5 p-4 space-y-2">
              <button @click="limpiarFiltros" class="w-full px-4 py-3 border border-text-dark/10 rounded text-sm">
                Limpiar filtros
              </button>
              <button @click="mostrarFiltrosMobile = false" class="w-full px-4 py-3 bg-text-dark text-white rounded text-sm">
                Ver resultados ({{ productosFiltrados.length }})
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Drawer del Carrito -->
    <Teleport to="body">
      <Transition name="drawer-fade">
        <div 
          v-if="mostrarCarrito"
          class="fixed inset-0 bg-black/30 z-40"
          @click.self="mostrarCarrito = false"
        ></div>
      </Transition>
      <Transition name="drawer-slide">
        <div 
          v-if="mostrarCarrito"
          class="fixed right-0 top-0 bottom-0 w-full max-w-sm bg-white shadow-xl z-50 flex flex-col"
        >
          <!-- Header -->
          <div class="border-b border-text-dark/5 p-6 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-text-dark">Mi Carrito</h2>
            <button 
              @click="mostrarCarrito = false"
              class="p-2 hover:bg-[#FAFAFA] rounded-full transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Items del carrito -->
          <div class="flex-1 overflow-y-auto p-6">
            <div v-if="carritoItems.length === 0" class="text-center py-12">
              <p class="text-text-medium text-sm">Tu carrito está vacío</p>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="item in carritoItems" 
                :key="item.id"
                class="flex gap-4 pb-4 border-b border-text-dark/5"
              >
                <img 
                  :src="getImageUrl(item.imagen_url)"
                  :alt="item.nombre"
                  @error="handleImageError"
                  class="w-20 h-20 object-cover rounded bg-[#FAFAFA]"
                >
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-text-dark">{{ item.nombre }}</h3>
                  <p class="text-xs text-text-medium mt-1">Cantidad: {{ item.cantidad }}</p>
                  <p class="text-sm font-semibold text-text-dark mt-2">{{ formatearPrecio((item.precio_unitario || item.precio_monto || 0) * item.cantidad) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer con totales y botones -->
          <div v-if="carritoItems.length > 0" class="border-t border-text-dark/5 p-6 space-y-4">
            <div class="space-y-2">
              <div class="flex justify-between text-sm text-text-medium">
                <span>Subtotal:</span>
                <span>{{ formatearPrecio(precioSubtotal) }}</span>
              </div>
              <div class="flex justify-between text-lg font-semibold text-text-dark pt-2 border-t border-text-dark/5">
                <span>Total:</span>
                <span>{{ formatearPrecio(precioSubtotal) }}</span>
              </div>
            </div>
            <button 
              @click="irACheckout"
              class="w-full bg-text-dark hover:bg-black text-white font-medium py-3 rounded-sm transition-colors"
            >
              Completar pedido
            </button>
            <button 
              @click="mostrarCarrito = false"
              class="w-full border border-text-dark/10 hover:border-text-dark/30 text-text-dark py-3 rounded-sm transition-colors text-sm"
            >
              Seguir comprando
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

// Estados
const productos = ref([])
const categorias = ref([])
const loading = ref(true)
const cartCount = ref(0)
const mostrarCarrito = ref(false)
const carritoItems = ref([])

// Filtros
const filtroCategoria = ref(null)
const precioMin = ref(null)
const precioMax = ref(null)
const filtrosColor = ref([])
const filtrosTipo = ref([])
const ordenar = ref('recientes')

// Mobile
const mostrarFiltrosMobile = ref(false)

// Opciones de filtros disponibles
const coloresDisponibles = ref(['Negro', 'Castaño', 'Rubio', 'Rojo', 'Borgogña'])
const tiposDisponibles = ref(['Liso', 'Ondulado', 'Rizado', 'Afro'])

// Productos filtrados
const productosFiltrados = computed(() => {
  let resultado = [...productos.value]

  // Filtro por categoría
  if (filtroCategoria.value) {
    const target = filtroCategoria.value
    const targetId = typeof target === 'object' && target !== null ? target.id : null
    const targetNombre = typeof target === 'object' && target !== null ? target.nombre : target

    resultado = resultado.filter(p => {
      const categoriaProducto = p.categoria || p.categoria_nombre
      const categoriaId = p.categoria_id
      const matchesNombre = targetNombre
        ? String(categoriaProducto ?? '').toLowerCase() === String(targetNombre).toLowerCase()
        : false
      const matchesId = targetId
        ? String(categoriaId ?? '') === String(targetId)
        : false
      return matchesNombre || matchesId
    })
  }

  // Filtro por precio
  if (precioMin.value) {
    resultado = resultado.filter(p => p.precio_monto >= precioMin.value)
  }
  if (precioMax.value) {
    resultado = resultado.filter(p => p.precio_monto <= precioMax.value)
  }

  // Filtro por color
  if (filtrosColor.value.length > 0) {
    resultado = resultado.filter(p => filtrosColor.value.includes(p.color))
  }

  // Filtro por tipo
  if (filtrosTipo.value.length > 0) {
    resultado = resultado.filter(p => filtrosTipo.value.includes(p.tipo))
  }

  // Ordenar
  if (ordenar.value === 'precio-asc') {
    resultado.sort((a, b) => a.precio_monto - b.precio_monto)
  } else if (ordenar.value === 'precio-desc') {
    resultado.sort((a, b) => b.precio_monto - a.precio_monto)
  } else if (ordenar.value === 'nombre') {
    resultado.sort((a, b) => a.nombre.localeCompare(b.nombre))
  } else {
    resultado.sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion))
  }

  return resultado
})

// Cálculo del precio subtotal del carrito
const precioSubtotal = computed(() => {
  return carritoItems.value.reduce((total, item) => {
    const precio = item.precio_unitario || item.precio_monto || 0
    return total + (precio * item.cantidad)
  }, 0)
})

// Métodos
const cargarProductos = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/v1/productos/')
    productos.value = data
  } catch (error) {
    console.error('Error cargando productos:', error)
  } finally {
    loading.value = false
  }
}

const cargarCategorias = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/v1/categorias/?solo_activas=true')
    categorias.value = data
  } catch (error) {
    console.error('Error cargando categorías:', error)
  }
}

const limpiarFiltros = () => {
  filtroCategoria.value = null
  precioMin.value = null
  precioMax.value = null
  filtrosColor.value = []
  filtrosTipo.value = []
}

const verProducto = (id) => {
  router.push(`/producto/${id}`)
}

const formatearPrecio = (precio) => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0
  }).format(precio)
}

const loadCartFromLocal = () => {
  try {
    const cart = localStorage.getItem('kharis_cart_cache')
    if (cart) {
      const parsed = JSON.parse(cart)
      // Si es un objeto con propiedad 'items' (formato nuevo), usa items
      carritoItems.value = parsed.items ? parsed.items : parsed
    } else {
      carritoItems.value = []
    }
  } catch (err) {
    carritoItems.value = []
  }
}

const irACheckout = () => {
  mostrarCarrito.value = false
  router.push('/checkout')
}

const getImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}

const handleImageError = (e) => {
  e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f3f4f6" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em" fill="%239ca3af" font-size="12"%3ESin Imagen%3C/text%3E%3C/svg%3E'
}

const loadCartCount = () => {
  try {
    const count = localStorage.getItem('kharis_cart_count')
    cartCount.value = count ? parseInt(count) : 0
  } catch (err) {
    cartCount.value = 0
  }
}

// Lifecycle
onMounted(() => {
  // Preseleccionar categoría si viene por query (?categoria=Nombre)
  if (route.query?.categoria) {
    filtroCategoria.value = route.query.categoria
  }

  cargarProductos()
  cargarCategorias()
  loadCartCount()
  loadCartFromLocal()
})

// Mantener filtro en sync si cambia la query
watch(
  () => route.query.categoria,
  (nuevaCategoria) => {
    filtroCategoria.value = nuevaCategoria || null
  }
)
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active > div,
.modal-fade-leave-active > div {
  transition: transform 0.3s ease;
}

.modal-fade-enter-from > div {
  transform: translateX(100%);
}

.modal-fade-leave-to > div {
  transform: translateX(100%);
}

.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.3s ease;
}

.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.3s ease;
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
}
</style>
