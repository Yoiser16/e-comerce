<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
      
      <!-- Breadcrumb discreto -->
      <nav class="flex items-center gap-2 text-sm text-gray-400 mb-6">
        <router-link to="/portal" class="hover:text-gray-600 transition-colors">Portal</router-link>
        <span>/</span>
        <router-link to="/portal/catalogo" class="hover:text-gray-600 transition-colors">Catálogo</router-link>
        <span>/</span>
        <span class="text-gray-700">Carrito</span>
        <span v-if="cartItems.length > 0" class="text-gray-500 ml-1">({{ cartItems.length }} productos, {{ totalUnits }} uds)</span>
      </nav>

      <!-- Contenido Principal: 2 columnas -->
      <div v-if="cartItems.length > 0" class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
        
        <!-- ====================================
             COLUMNA IZQUIERDA: Lista de productos (8 cols)
        ==================================== -->
        <div class="lg:col-span-8 space-y-3">
          
          <!-- Header de lista -->
          <div class="flex items-center justify-between pb-3 border-b border-gray-200">
            <h1 class="text-lg font-semibold text-gray-900">Productos en el pedido</h1>
            <button 
              @click="limpiarCarrito"
              class="text-sm text-gray-500 hover:text-gray-700 transition-colors"
            >
              Limpiar todo
            </button>
          </div>
          
          <!-- Items del carrito -->
          <div 
            v-for="item in cartItems" 
            :key="item.id"
            class="bg-white rounded-lg border border-gray-200 p-4 flex gap-4"
          >
            <!-- Imagen pequeña -->
            <div class="w-16 h-16 rounded bg-gray-100 overflow-hidden flex-shrink-0">
              <video
                v-if="isVideo(getCartMediaUrl(item))"
                :src="getCartMediaUrl(item)"
                class="w-full h-full object-cover"
                muted
                playsinline
              ></video>
              <img 
                v-else
                :src="getCartMediaUrl(item)"
                :alt="item.nombre || item.name"
                class="w-full h-full object-cover"
                @error="handleImageError"
              />
            </div>

            <!-- Info principal -->
            <div class="flex-1 min-w-0">
              <!-- Fila 1: Categoría + Nombre + SKU -->
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0 flex-1">
                  <p class="text-xs text-gray-400 uppercase tracking-wide">{{ item.categoria || item.category }}</p>
                  <h3 class="font-medium text-gray-900 truncate">{{ item.nombre || item.name }}</h3>
                  <p class="text-xs text-gray-400 font-mono mt-0.5">{{ item.sku || `SKU-${item.id}` }}</p>
                </div>
                
                <!-- Botón eliminar - texto -->
                <button 
                  @click="removeItem(item.id)"
                  class="text-sm text-gray-400 hover:text-red-500 transition-colors whitespace-nowrap"
                >
                  Eliminar
                </button>
              </div>

              <!-- Fila 2: Precio × Cantidad = Subtotal -->
              <div class="flex flex-wrap items-center justify-between gap-4 mt-3">
                
                <!-- Precio unitario -->
                <div class="text-sm text-gray-600">
                  ${{ formatPrice(item.precio || item.wholesalePrice) }} × {{ item.cantidad || item.quantity }} uds
                </div>

                <!-- Control de cantidad -->
                <div class="flex items-center gap-4">
                  <div class="flex items-center border border-gray-200 rounded">
                    <button 
                      @click="updateQuantity(item.id, (item.cantidad || item.quantity) - 1)"
                      :disabled="(item.cantidad || item.quantity) <= 10"
                      :title="(item.cantidad || item.quantity) <= 10 ? 'Compra mínima: 10 unidades' : ''"
                      class="w-8 h-8 flex items-center justify-center text-gray-500 hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                    >
                      <span class="text-lg">−</span>
                    </button>
                    <input 
                      :value="item.cantidad || item.quantity"
                      @change="updateQuantity(item.id, parseInt($event.target.value) || 10)"
                      type="number"
                      :min="10"
                      class="w-12 h-8 text-center border-x border-gray-200 focus:outline-none text-sm font-medium"
                    />
                    <button 
                      @click="updateQuantity(item.id, (item.cantidad || item.quantity) + 1)"
                      :disabled="(item.cantidad || item.quantity) >= (item.stock || 999)"
                      class="w-8 h-8 flex items-center justify-center text-gray-500 hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                    >
                      <span class="text-lg">+</span>
                    </button>
                  </div>

                  <!-- Subtotal línea -->
                  <div class="text-right min-w-[90px]">
                    <p class="font-semibold text-gray-900">${{ formatPrice((item.precio || item.wholesalePrice) * (item.cantidad || item.quantity)) }}</p>
                  </div>
                </div>
              </div>

              <!-- Aviso de mínimo -->
              <p 
                v-if="(item.cantidad || item.quantity) < 10" 
                class="text-xs text-red-500 mt-2 font-medium"
              >
                ⚠️ La compra mínima es de 10 unidades por producto
              </p>
            </div>
          </div>

          <!-- Notas del pedido -->
          <div class="bg-white rounded-lg border border-gray-200 p-4 mt-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Notas del pedido
            </label>
            <textarea 
              v-model="orderNotes"
              rows="2"
              placeholder="Instrucciones especiales de entrega o facturación..."
              class="w-full px-3 py-2 border border-gray-200 rounded focus:ring-1 focus:ring-gray-300 focus:border-gray-300 resize-none text-sm text-gray-700"
            ></textarea>
          </div>
        </div>

        <!-- ====================================
             COLUMNA DERECHA: Resumen (4 cols) - STICKY
        ==================================== -->
        <div class="lg:col-span-4">
          <div class="bg-white rounded-lg border border-gray-200 p-5 lg:sticky lg:top-24">
            
            <!-- Header -->
            <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Resumen del pedido</h2>

            <!-- Líneas de detalle -->
            <div class="space-y-3 pb-4 border-b border-gray-100">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Productos ({{ cartItems.length }})</span>
                <span class="text-gray-900">${{ formatPrice(subtotal) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">{{ totalUnits }} unidades</span>
                <span class="text-gray-400"></span>
              </div>
              <div v-if="totalDiscount > 0" class="flex justify-between text-sm">
                <span class="text-gray-600">Descuento por volumen</span>
                <span class="text-gray-700">−${{ formatPrice(totalDiscount) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Envío</span>
                <span class="text-gray-900">{{ shippingCost === 0 ? 'Incluido' : `$${formatPrice(shippingCost)}` }}</span>
              </div>
            </div>

            <!-- Total destacado -->
            <div class="py-5 border-b border-gray-100">
              <div class="flex justify-between items-baseline">
                <span class="text-gray-500 text-sm">TOTAL A PAGAR</span>
              </div>
              <p class="text-3xl font-bold text-gray-900 mt-1">${{ formatPrice(total) }}</p>
              <p class="text-xs text-gray-400 mt-1">IVA incluido</p>
            </div>

            <!-- CTA Principal -->
            <div class="pt-5 space-y-3">
              <button 
                @click="proceedToCheckout"
                :disabled="!canCheckout"
                class="w-full py-4 bg-[#1A1A1A] hover:bg-black text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Confirmar pedido
              </button>

              <!-- Link secundario -->
              <router-link 
                to="/portal/catalogo"
                class="block text-center text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                Seguir comprando →
              </router-link>
            </div>

            <!-- Contacto discreto -->
            <div class="mt-6 pt-4 border-t border-gray-100 text-center">
              <p class="text-xs text-gray-400 mb-1">¿Necesitas ajustar el pedido?</p>
              <a 
                href="https://wa.me/4796657763"
                target="_blank"
                class="text-xs text-gray-500 hover:text-gray-700 transition-colors"
              >
                Escríbenos por WhatsApp
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- ====================================
           Empty State - Carrito vacío
      ==================================== -->
      <div v-else class="text-center py-20 bg-white rounded-lg border border-gray-200">
        <div class="w-16 h-16 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
          </svg>
        </div>
        <h2 class="text-xl font-semibold text-gray-900 mb-2">Tu carrito está vacío</h2>
        <p class="text-gray-500 mb-8 max-w-sm mx-auto">
          Explora el catálogo para agregar productos a tu pedido
        </p>
        <router-link 
          to="/portal/catalogo" 
          class="inline-flex items-center gap-2 px-6 py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-lg transition-colors"
        >
          Ir al catálogo
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { getImageUrl } from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  name: 'B2BCarrito',
  setup() {
    const router = useRouter()
    const cartItems = ref([])
    const orderNotes = ref('')
    const freeShippingThreshold = 500000

    // Helpers para compatibilidad de campos
    const getQuantity = (item) => item.cantidad || item.quantity || 1
    const getPrice = (item) => item.precio || item.wholesalePrice || 0
    const getRetailPrice = (item) => item.precioPublico || item.retailPrice || getPrice(item)

    // Cargar carrito desde localStorage
    function loadCart() {
      const cart = localStorage.getItem('b2b_cart')
      if (cart) {
        try {
          const data = JSON.parse(cart)
          cartItems.value = data.items || []
        } catch {
          cartItems.value = []
        }
      }
    }

    // Guardar carrito en localStorage
    function saveCart() {
      localStorage.setItem('b2b_cart', JSON.stringify({ items: cartItems.value }))
      window.dispatchEvent(new CustomEvent('cart-updated'))
    }

    // Computed
    const totalUnits = computed(() => cartItems.value.reduce((sum, item) => sum + getQuantity(item), 0))

    const subtotal = computed(() => cartItems.value.reduce((sum, item) => sum + (getPrice(item) * getQuantity(item)), 0))

    const totalDiscount = computed(() => {
      return cartItems.value.reduce((sum, item) => {
        const discount = (getRetailPrice(item) - getPrice(item)) * getQuantity(item)
        return sum + Math.max(0, discount)
      }, 0)
    })

    const shippingCost = computed(() => {
      if (subtotal.value >= freeShippingThreshold) return 0
      return 25000
    })

    const total = computed(() => subtotal.value + shippingCost.value)

    const canCheckout = computed(() => {
      if (cartItems.value.length === 0) return false
      // Validar que todos los productos tengan al menos 10 unidades
      return cartItems.value.every(item => getQuantity(item) >= 10)
    })

    // Methods
    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

    function handleImageError(e) {
      e.target.src = '/placeholder.png'
    }

    function isVideo(url) {
      if (!url) return false
      const cleanUrl = url.split('?')[0].toLowerCase()
      return ['.mp4', '.webm', '.ogg', '.mov'].some(ext => cleanUrl.endsWith(ext))
    }

    function getCartMediaUrl(item) {
      const raw = item.imagen || item.image || item.imagen_principal || ''
      return getImageUrl(raw) || '/placeholder.png'
    }

    function updateQuantity(itemId, newQuantity) {
      const item = cartItems.value.find(i => i.id === itemId)
      if (item) {
        const ORDEN_MINIMA = 10 // Compra mínima para mayoristas
        const minQty = Math.max(item.minOrder || 1, ORDEN_MINIMA)
        const maxQty = item.stock || 999
        
        // Validar que la cantidad no sea menor a la orden mínima
        if (newQuantity < ORDEN_MINIMA) {
          alert(`La compra mínima para mayoristas es de ${ORDEN_MINIMA} unidades por producto.`)
          return
        }
        
        const qty = Math.max(minQty, Math.min(newQuantity, maxQty))
        // Compatibilidad: usar el campo que ya existe o crear quantity
        if ('cantidad' in item) {
          item.cantidad = qty
        } else {
          item.quantity = qty
        }
        saveCart()
      }
    }

    function removeItem(itemId) {
      cartItems.value = cartItems.value.filter(i => i.id !== itemId)
      saveCart()
    }

    function limpiarCarrito() {
      if (confirm('¿Estás seguro de eliminar todos los productos del carrito?')) {
        cartItems.value = []
        saveCart()
      }
    }

    function proceedToCheckout() {
      if (!canCheckout.value) return
      router.push('/portal/checkout/confirmar')
    }

    // Watch para persistir cambios
    watch(cartItems, saveCart, { deep: true })

    onMounted(() => {
      loadCart()
    })

    return {
      cartItems, orderNotes,
      totalUnits, subtotal, totalDiscount, shippingCost, total, canCheckout,
      formatPrice, handleImageError, updateQuantity, removeItem, limpiarCarrito, proceedToCheckout
      , isVideo, getCartMediaUrl
    }
  }
}
</script>
