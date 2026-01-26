<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10 sm:py-14 lg:py-16">
      <button @click="router.back()" class="inline-flex items-center gap-2 text-text-medium hover:text-text-dark text-sm mb-6 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
        Volver
      </button>

      <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-14">
        <div class="aspect-square bg-gray-200 animate-pulse rounded-xl"></div>
        <div class="space-y-4">
          <div class="h-8 w-2/3 bg-gray-200 animate-pulse rounded"></div>
          <div class="h-4 w-1/3 bg-gray-200 animate-pulse rounded"></div>
          <div class="h-20 w-full bg-gray-200 animate-pulse rounded"></div>
          <div class="h-10 w-40 bg-gray-200 animate-pulse rounded"></div>
        </div>
      </div>

      <div v-else-if="error" class="text-center py-16 text-text-medium">
        {{ error }}
      </div>

      <div v-else-if="producto" class="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-14">
        <!-- Galería -->
        <div>
          <div class="aspect-square bg-white rounded-xl overflow-hidden border border-text-dark/5 shadow-sm">
            <img
              :src="getImageUrl(producto.imagen_principal)"
              :alt="producto.nombre"
              class="w-full h-full object-cover"
              @error="handleImageError"
            />
          </div>
          <div class="mt-4 grid grid-cols-4 gap-3">
            <div
              v-for="(thumb, idx) in miniaturas"
              :key="idx"
              class="aspect-square rounded-lg overflow-hidden border border-text-dark/10 bg-white"
            >
              <img :src="getImageUrl(thumb)" :alt="'Miniatura ' + (idx + 1)" class="w-full h-full object-cover" @error="handleImageError" />
            </div>
          </div>
        </div>

        <!-- Info -->
        <div class="space-y-5 lg:space-y-6">
          <div class="space-y-2">
            <p class="text-sm uppercase tracking-[0.14em] text-text-light">{{ producto.categoria || 'Colección' }}</p>
            <h1 class="font-luxury text-3xl sm:text-4xl text-text-dark leading-tight">{{ producto.nombre }}</h1>
          </div>

          <div class="flex flex-wrap items-center gap-3">
            <p class="text-2xl sm:text-3xl font-semibold text-text-dark">{{ formatearPrecio(producto.precio_monto) }}</p>
            <span class="text-sm text-text-medium">IVA incluido</span>
          </div>

          <!-- Stock disponible con resalte cuando hay poco -->
          <div 
            v-if="stockDisponible >= 0"
            :class="[
              'inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium tracking-wider border',
              stockDisponible === 0 
                ? 'bg-red-50 text-red-700 border-red-200' 
                : stockDisponible <= 5 
                  ? 'bg-amber-50 text-amber-700 border-amber-200 animate-pulse' 
                  : 'bg-emerald-50 text-emerald-700 border-emerald-200'
            ]"
          >
            <svg 
              v-if="stockDisponible === 0" 
              class="w-4 h-4" 
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd" />
            </svg>
            <svg 
              v-else-if="stockDisponible <= 5" 
              class="w-4 h-4" 
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
            </svg>
            <svg 
              v-else 
              class="w-4 h-4" 
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
            </svg>
            <span class="uppercase">
              {{ stockDisponible === 0 ? 'Agotado' : stockDisponible <= 5 ? `¡Solo quedan ${stockDisponible}!` : `${stockDisponible} disponibles` }}
            </span>
          </div>

          <div class="flex items-center gap-3 text-sm text-text-medium">
            <button
              type="button"
              @click="openCartDrawer"
              class="inline-flex items-center gap-2 px-3 py-2 border border-text-dark/10 rounded-full hover:border-text-dark/30 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l1 7h12l1.5-5H6" />
                <circle cx="9" cy="20" r="1" />
                <circle cx="17" cy="20" r="1" />
              </svg>
              Ver carrito ({{ cartCount }})
            </button>
          </div>

          <div class="text-text-medium leading-relaxed whitespace-pre-line">{{ producto.descripcion }}</div>

          <div class="grid grid-cols-2 gap-3 sm:gap-4 text-sm text-text-dark">
            <div v-if="producto.color" class="p-3 bg-white rounded-lg border border-text-dark/5">
              <p class="text-text-light text-xs uppercase tracking-[0.12em]">Color</p>
              <p class="font-medium">{{ producto.color }}</p>
            </div>
            <div v-if="producto.largo" class="p-3 bg-white rounded-lg border border-text-dark/5">
              <p class="text-text-light text-xs uppercase tracking-[0.12em]">Largo</p>
              <p class="font-medium">{{ producto.largo }}</p>
            </div>
            <div v-if="producto.tipo" class="p-3 bg-white rounded-lg border border-text-dark/5">
              <p class="text-text-light text-xs uppercase tracking-[0.12em]">Tipo</p>
              <p class="font-medium">{{ producto.tipo }}</p>
            </div>
            <div v-if="producto.origen" class="p-3 bg-white rounded-lg border border-text-dark/5">
              <p class="text-text-light text-xs uppercase tracking-[0.12em]">Origen</p>
              <p class="font-medium">{{ producto.origen }}</p>
            </div>
            <div v-if="producto.metodo" class="p-3 bg-white rounded-lg border border-text-dark/5">
              <p class="text-text-light text-xs uppercase tracking-[0.12em]">Método</p>
              <p class="font-medium">{{ producto.metodo }}</p>
            </div>
            <div v-if="producto.calidad" class="p-3 bg-white rounded-lg border border-text-dark/5">
              <p class="text-text-light text-xs uppercase tracking-[0.12em]">Calidad</p>
              <p class="font-medium">{{ producto.calidad }}</p>
            </div>
          </div>

          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <label class="text-sm text-text-medium">Cantidad</label>
              <input
                type="number"
                min="1"
                :max="stockDisponible"
                v-model.number="cantidad"
                class="w-24 px-3 py-2 border border-text-dark/10 rounded text-sm focus:outline-none focus:border-text-dark/30"
              />
            </div>
            <button
              @click="agregarAlCarrito"
              :disabled="stockDisponible === 0"
              class="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 bg-text-dark text-white rounded-sm text-sm font-semibold hover:bg-black transition-all disabled:opacity-60 disabled:cursor-not-allowed shadow-md"
            >
              Agregar al carrito
            </button>
            <p class="text-xs text-text-light">Entrega rápida y soporte personalizado.</p>
            <p v-if="mensaje" class="text-sm text-emerald-600">{{ mensaje }}</p>
            <p v-if="mensajeError" class="text-sm text-red-600">{{ mensajeError }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Mini drawer del carrito -->
    <transition name="fade">
      <div v-if="showCartDrawer" class="fixed inset-0 bg-black/40 z-40 flex justify-end" @click.self="closeCartDrawer">
        <div class="w-full max-w-sm h-full bg-white shadow-2xl flex flex-col">
          <!-- Header -->
          <div class="border-b border-text-dark/5 p-6 flex items-center justify-between">
            <h3 class="text-lg font-semibold text-text-dark">Mi Carrito</h3>
            <button @click="closeCartDrawer" class="text-text-medium hover:text-text-dark">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Items -->
          <div class="flex-1 overflow-y-auto p-6">
            <div v-if="carritoItems.length === 0" class="text-center py-12">
              <p class="text-text-medium text-sm">Tu carrito está vacío</p>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="item in carritoItems" 
                :key="item.producto_id"
                class="flex gap-3 pb-4 border-b border-text-dark/5"
              >
                <img 
                  :src="item.imagen_url"
                  :alt="item.nombre"
                  @error="handleImageError"
                  class="w-16 h-16 object-cover rounded bg-[#FAFAFA]"
                >
                <div class="flex-1">
                  <h4 class="text-sm font-medium text-text-dark line-clamp-2">{{ item.nombre }}</h4>
                  <p class="text-xs text-text-medium mt-1">Cant: {{ item.cantidad }}</p>
                  <p class="text-sm font-semibold text-text-dark mt-2">{{ formatearPrecio((item.precio_unitario || item.precio_monto || 0) * item.cantidad) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div v-if="carritoItems.length > 0" class="border-t border-text-dark/5 p-6 space-y-4">
            <div class="space-y-2">
              <div class="flex justify-between text-sm text-text-medium">
                <span>Subtotal:</span>
                <span>{{ formatearPrecio(cartSubtotal) }}</span>
              </div>
              <div class="flex justify-between text-lg font-semibold text-text-dark pt-2 border-t border-text-dark/5">
                <span>Total:</span>
                <span>{{ formatearPrecio(cartSubtotal) }}</span>
              </div>
            </div>
            <button @click="goToCheckout" class="w-full bg-text-dark hover:bg-black text-white py-3 rounded-sm text-sm font-semibold transition-all">Ir a pagar</button>
            <button @click="closeCartDrawer" class="w-full border border-text-dark/15 text-text-dark py-3 rounded-sm text-sm font-semibold hover:border-text-dark/40 transition-all">Seguir comprando</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productosService, carritoService, authService } from '@/services/productos'
import { getImageUrl } from '@/services/api'

const route = useRoute()
const router = useRouter()

const producto = ref(null)
const loading = ref(true)
const error = ref(null)
const miniaturas = ref([])
const mensaje = ref('')
const mensajeError = ref('')
const isLoggedIn = ref(authService.isAuthenticated())
const cantidad = ref(1)
const showCartDrawer = ref(false)
const carritoResumen = ref({ nombre: '', imagen: '', cantidad: 0, subtotal: 0 })
const cartCount = ref(0)
const carritoItems = ref([])

const CART_STORAGE_KEY = 'kharis_cart_cache'
const CART_COUNT_KEY = 'kharis_cart_count'

const saveCartToLocal = (items, count) => {
  try {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify({ items, timestamp: Date.now() }))
    localStorage.setItem(CART_COUNT_KEY, String(count))
    cartCount.value = count
  } catch (e) {
    console.warn('No se pudo guardar el carrito local:', e)
  }
}

const loadCartFromLocal = () => {
  try {
    const cached = localStorage.getItem(CART_STORAGE_KEY)
    if (cached) {
      const data = JSON.parse(cached)
      return data.items || []
    }
  } catch (e) {
    console.warn('No se pudo leer el carrito local:', e)
  }
  return []
}

const loadCartCount = () => {
  const stored = localStorage.getItem(CART_COUNT_KEY)
  if (stored) {
    const n = parseInt(stored, 10)
    cartCount.value = isNaN(n) ? 0 : n
  }
}

const formatearPrecio = (precio) => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0
  }).format(precio || 0)
}

const handleImageError = (e) => {
  e.target.src = 'https://dummyimage.com/600x600/f3f4f6/9ca3af&text=Sin+imagen'
}

const stockDisponible = computed(() => {
  const p = producto.value
  if (!p) return 0
  return Number(p.stock_actual ?? p.stock ?? p.stock_minimo ?? 0)
})

const cartSubtotal = computed(() => {
  return carritoItems.value.reduce((total, item) => {
    const precio = item.precio_unitario || item.precio_monto || 0
    return total + (precio * item.cantidad)
  }, 0)
})

const cargarProducto = async () => {
  loading.value = true
  error.value = null
  try {
    const id = route.params.id
    const data = await productosService.getProducto(id)
    producto.value = data
    const galeria = []
    if (data.imagen_principal) galeria.push(data.imagen_principal)
    if (data.imagenes && Array.isArray(data.imagenes)) galeria.push(...data.imagenes)
    miniaturas.value = galeria.slice(0, 4)
  } catch (err) {
    console.error(err)
    error.value = 'No pudimos cargar este producto'
  } finally {
    loading.value = false
  }
}

const agregarAlCarrito = async () => {
  if (!producto.value) return
  if (cantidad.value < 1) {
    cantidad.value = 1
  }
  if (stockDisponible.value <= 0) {
    mensajeError.value = 'Este producto no tiene stock disponible'
    mensaje.value = ''
    return
  }
  // Sumar la cantidad ya agregada en el carrito local
  const items = loadCartFromLocal()
  const idx = items.findIndex((i) => i.producto_id === producto.value.id)
  const cantidadEnCarrito = idx >= 0 ? items[idx].cantidad : 0
  const cantidadTotal = cantidadEnCarrito + cantidad.value
  if (cantidadTotal > stockDisponible.value) {
    mensajeError.value = `Solo hay ${stockDisponible.value - cantidadEnCarrito} disponibles para agregar (ya tienes ${cantidadEnCarrito} en el carrito)`
    mensaje.value = ''
    return
  }
  try {
    const precioUnitario = Number(producto.value.precio_monto || producto.value.precio || 0)
    if (idx >= 0) {
      items[idx].cantidad += cantidad.value
      items[idx].subtotal = items[idx].cantidad * (items[idx].precio_unitario || precioUnitario)
    } else {
      items.push({
        producto_id: producto.value.id,
        nombre: producto.value.nombre,
        imagen_url: getImageUrl(producto.value.imagen_principal),
        precio_unitario: precioUnitario,
        cantidad: cantidad.value,
        subtotal: precioUnitario * cantidad.value,
      })
    }
    const count = items.reduce((sum, i) => sum + (i.cantidad || 1), 0)
    saveCartToLocal(items, count)

    // Intentar sincronizar con backend si hay sesión
    if (isLoggedIn.value) {
      try {
        await carritoService.agregarProducto(producto.value.id, cantidad.value)
      } catch (backendErr) {
        console.warn('No se pudo sincronizar carrito con backend, queda en local:', backendErr)
      }
    }

    mensaje.value = 'Producto agregado al carrito'
    mensajeError.value = ''
    carritoResumen.value = {
      nombre: producto.value?.nombre || 'Producto',
      imagen: getImageUrl(producto.value?.imagen_principal || ''),
      cantidad: cantidad.value,
      subtotal: precioUnitario * cantidad.value
    }
    // Recargar todos los items del carrito
    carritoItems.value = loadCartFromLocal()
    showCartDrawer.value = true
  } catch (err) {
    console.error(err)
    mensajeError.value = 'No se pudo agregar al carrito'
    mensaje.value = ''
  }
}

const closeCartDrawer = () => {
  showCartDrawer.value = false
}

const goToCheckout = () => {
  showCartDrawer.value = false
  router.push('/checkout')
}

const openCartDrawer = () => {
  loadCartCount()
  carritoItems.value = loadCartFromLocal()
  showCartDrawer.value = true
}

onMounted(() => {
  cargarProducto()
  loadCartCount()
  carritoItems.value = loadCartFromLocal()
})
</script>
