<template>
  <div class="min-h-screen bg-[#FAFAFA] pb-24 lg:pb-0">
    <!-- Modal de confirmación para limpiar carrito -->
    <div v-if="showClearModal" class="fixed inset-0 bg-black/30 flex items-center justify-center z-[60] p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full animate-in fade-in zoom-in-95 duration-300">
        <div class="p-6 sm:p-8">
          <div class="flex justify-center mb-4">
            <div class="w-14 h-14 rounded-full bg-red-50 flex items-center justify-center">
              <svg class="w-7 h-7 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </div>
          </div>
          
          <h3 class="text-xl font-semibold text-gray-900 text-center mb-2">¿Limpiar carrito?</h3>
          <p class="text-gray-500 text-center text-sm mb-7">Se eliminarán todos los productos de tu pedido. Esta acción no se puede deshacer.</p>
          
          <div class="flex gap-3">
            <button
              @click="showClearModal = false"
              class="flex-1 px-4 py-3 border-2 border-gray-200 text-gray-900 font-medium rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
            <button
              @click="confirmClearCart"
              class="flex-1 px-4 py-3 bg-red-500 hover:bg-red-600 text-white font-medium rounded-lg transition-colors"
            >
              Eliminar todo
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-4 lg:py-8">
      
      <!-- Breadcrumb discreto - Oculto en móvil -->
      <nav class="hidden sm:flex items-center gap-2 text-sm text-gray-400 mb-6">
        <router-link to="/portal" class="hover:text-gray-600 transition-colors">Portal</router-link>
        <span>/</span>
        <router-link to="/portal/catalogo" class="hover:text-gray-600 transition-colors">Catálogo</router-link>
        <span>/</span>
        <span class="text-gray-700">Carrito</span>
        <span v-if="cartItems.length > 0" class="text-gray-500 ml-1">({{ cartItems.length }} productos, {{ totalUnits }} uds)</span>
      </nav>

      <!-- Mini header móvil -->
      <div class="sm:hidden flex items-center justify-between mb-4">
        <router-link to="/portal/catalogo" class="flex items-center gap-1 text-sm text-gray-500">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Catálogo
        </router-link>
        <span class="text-sm font-medium text-gray-900">Mi Carrito</span>
        <div class="w-16"></div>
      </div>

      <!-- Contenido Principal: 2 columnas -->
      <div v-if="cartItems.length > 0" class="grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-8">
        
        <!-- ====================================
             COLUMNA IZQUIERDA: Lista de productos (8 cols)
        ==================================== -->
        <div class="lg:col-span-8 space-y-3 order-2 lg:order-1">
          
          <!-- Header de lista -->
          <div class="flex items-center justify-between pb-2 sm:pb-3 border-b border-gray-200">
            <h1 class="text-base sm:text-lg font-semibold text-gray-900">
              Productos <span class="text-gray-400 font-normal">({{ cartItems.length }})</span>
            </h1>
            <button 
              @click="limpiarCarrito"
              class="text-xs sm:text-sm text-gray-400 hover:text-red-500 transition-colors"
            >
              Limpiar todo
            </button>
          </div>
          
          <!-- Items del carrito -->
          <div 
            v-for="item in cartItems" 
            :key="item.variante_id || item.id"
            class="bg-white rounded-xl border border-gray-200 p-3 sm:p-4"
          >
            <div class="flex gap-3 sm:gap-4">
              <!-- Imagen pequeña -->
              <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-lg bg-gray-100 overflow-hidden flex-shrink-0">
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
              <!-- Fila 1: Nombre + Eliminar -->
              <div class="flex items-start justify-between gap-2">
                <div class="min-w-0 flex-1">
                  <p class="text-[10px] sm:text-xs text-gray-400 uppercase tracking-wide">{{ item.categoria || item.category }}</p>
                  <h3 class="font-medium text-gray-900 text-sm sm:text-base line-clamp-2">{{ item.nombre || item.name }}</h3>
                  <p v-if="item.color || item.largo" class="text-[11px] text-gray-400 mt-1">
                    <span v-if="item.color">Color: {{ formatColorLabel(item.color) }}</span>
                    <span v-if="item.color && item.largo"> · </span>
                    <span v-if="item.largo">Largo: {{ item.largo }}</span>
                  </p>
                </div>
                
                <!-- Botón eliminar -->
                <button 
                  @click="removeItem(item.variante_id || item.id)"
                  class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>

              <!-- Precio unitario -->
              <p class="text-sm text-[#8B7355] font-medium mt-1">
                ${{ formatPrice(getUnitPrice(item)) }} <span class="text-gray-400 font-normal">c/u</span>
              </p>
            </div>
            </div>

            <!-- Fila inferior: Cantidad y Subtotal -->
            <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
              <!-- Control de cantidad compacto -->
              <div class="flex items-center border border-gray-200 rounded-lg overflow-hidden">
                <button 
                  @click="updateQuantity(item.variante_id || item.id, (item.cantidad || item.quantity) - 1)"
                  :disabled="(item.cantidad || item.quantity) <= 10"
                  class="w-9 h-9 flex items-center justify-center text-gray-500 hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                >
                  <span class="text-lg font-medium">−</span>
                </button>
                <input 
                  :value="item.cantidad || item.quantity"
                  @change="updateQuantity(item.variante_id || item.id, parseInt($event.target.value) || 10)"
                  type="number"
                  :min="10"
                  class="w-12 h-9 text-center border-x border-gray-200 focus:outline-none text-sm font-bold"
                />
                <button 
                  @click="updateQuantity(item.variante_id || item.id, (item.cantidad || item.quantity) + 1)"
                  :disabled="(item.cantidad || item.quantity) >= (item.stock || 999)"
                  class="w-9 h-9 flex items-center justify-center text-gray-500 hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                >
                  <span class="text-lg font-medium">+</span>
                </button>
              </div>

              <!-- Subtotal línea -->
              <div class="text-right">
                <p class="text-lg font-bold text-[#1A1A1A]">${{ formatPrice(getUnitPrice(item) * (item.cantidad || item.quantity)) }}</p>
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

          <!-- Notas del pedido - Solo desktop -->
          <div class="hidden lg:block bg-white rounded-xl border border-gray-200 p-4 mt-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Notas del pedido
            </label>
            <textarea 
              v-model="orderNotes"
              rows="2"
              placeholder="Instrucciones especiales de entrega o facturación..."
              class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-1 focus:ring-[#1A1A1A]/20 focus:border-[#1A1A1A] resize-none text-sm text-gray-700"
            ></textarea>
          </div>
        </div>

        <!-- ====================================
             COLUMNA DERECHA: Resumen (4 cols) - Primero en móvil
        ==================================== -->
        <div class="lg:col-span-4 order-1 lg:order-2">
          <div class="bg-white rounded-xl border border-gray-200 p-4 sm:p-5 lg:sticky lg:top-24">
            
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
            <div class="py-4 lg:py-5 border-b border-gray-100">
              <div class="flex justify-between items-baseline">
                <span class="text-gray-500 text-sm">TOTAL A PAGAR</span>
              </div>
              <p class="text-2xl lg:text-3xl font-bold text-[#1A1A1A] mt-1">${{ formatPrice(total) }}</p>
              <p class="text-xs text-gray-400 mt-1">IVA incluido</p>
            </div>

            <!-- CTA Principal - Solo visible en desktop -->
            <div class="hidden lg:block pt-5 space-y-3">
              <button 
                @click="proceedToCheckout"
                :disabled="!canCheckout"
                class="w-full py-4 bg-[#1A1A1A] hover:bg-black text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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

            <!-- Link seguir comprando - Solo en móvil -->
            <div class="lg:hidden pt-4">
              <router-link 
                to="/portal/catalogo"
                class="flex items-center justify-center gap-1 text-sm text-[#8B7355] font-medium"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                </svg>
                Seguir comprando
              </router-link>
            </div>

            <!-- Contacto discreto - Solo desktop -->
            <div class="hidden lg:block mt-6 pt-4 border-t border-gray-100 text-center">
              <p class="text-xs text-gray-400 mb-1">¿Necesitas ajustar el pedido?</p>
              <a 
                href="https://wa.me/4796657763"
                target="_blank"
                class="inline-flex items-center gap-1 text-xs text-[#8B7355] hover:text-[#6B5344] transition-colors"
              >
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                </svg>
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
          class="inline-flex items-center gap-2 px-6 py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-xl transition-colors"
        >
          Ir al catálogo
        </router-link>
      </div>
    </div>

    <!-- ====================================
         FOOTER STICKY MÓVIL - Solo visible en móvil
    ==================================== -->
    <div 
      v-if="cartItems.length > 0"
      class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 lg:hidden z-50 shadow-[0_-4px_20px_rgba(0,0,0,0.08)]"
    >
      <div class="flex items-center justify-between gap-4">
        <div>
          <p class="text-xs text-gray-500">Total a pagar</p>
          <p class="text-xl font-bold text-[#1A1A1A]">${{ formatPrice(total) }}</p>
        </div>
        <button 
          @click="proceedToCheckout"
          :disabled="!canCheckout"
          class="flex-1 max-w-[200px] py-3.5 bg-[#1A1A1A] hover:bg-black text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm"
        >
          Confirmar pedido
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { getImageUrl } from '@/services/api'
import { useRouter } from 'vue-router'
import { formatColorLabel } from '@/utils/colorLabels'
import { getUnitPriceForQty } from '@/utils/b2bPricing'

export default {
  name: 'B2BCarrito',
  setup() {
    const router = useRouter()
    const cartItems = ref([])
    const orderNotes = ref('')
    const showClearModal = ref(false)
    const freeShippingThreshold = 500000

    // Helpers para compatibilidad de campos
    const getQuantity = (item) => item.cantidad || item.quantity || 1
    const getPrice = (item) => item.precio || item.wholesalePrice || 0
    const getRetailPrice = (item) => item.precioPublico || item.retailPrice || getPrice(item)
    const getMinOrder = (item) => Number(item.cantidad_minima_mayorista || item.minOrder || 1)
    const getUnitPrice = (item) => getUnitPriceForQty(getPrice(item), getQuantity(item), item.descuentos_volumen)

    // Cargar carrito desde localStorage
    function loadCart() {
      const cart = localStorage.getItem('b2b_cart')
      if (cart) {
        try {
          const data = JSON.parse(cart)
          const items = Array.isArray(data.items) ? data.items : []
          // NO modificar variante_id - mantener valores originales
          // Si es null, debe quedarse null para que el backend busque por producto_id
          cartItems.value = items
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

    const subtotal = computed(() => cartItems.value.reduce((sum, item) => sum + (getUnitPrice(item) * getQuantity(item)), 0))

    const totalDiscount = computed(() => {
      return cartItems.value.reduce((sum, item) => {
        const discount = (getRetailPrice(item) - getUnitPrice(item)) * getQuantity(item)
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
      return cartItems.value.every(item => getQuantity(item) >= getMinOrder(item))
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

    function updateQuantity(itemKey, newQuantity) {
      const item = cartItems.value.find(i => (i.variante_id || i.id) === itemKey)
      if (item) {
        const minQty = getMinOrder(item)
        const maxQty = item.stock || 999
        
        // Validar que la cantidad no sea menor a la orden mínima
        if (newQuantity < minQty) {
          alert(`La compra mínima para mayoristas es de ${minQty} unidades por producto.`)
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

    function removeItem(itemKey) {
      cartItems.value = cartItems.value.filter(i => (i.variante_id || i.id) !== itemKey)
      saveCart()
    }

    function limpiarCarrito() {
      showClearModal.value = true
    }

    function confirmClearCart() {
      cartItems.value = []
      saveCart()
      showClearModal.value = false
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
      cartItems, orderNotes, showClearModal,
      totalUnits, subtotal, totalDiscount, shippingCost, total, canCheckout,
      formatPrice, formatColorLabel, handleImageError, updateQuantity, removeItem, limpiarCarrito, proceedToCheckout, confirmClearCart,
      getUnitPrice
      , isVideo, getCartMediaUrl
    }
  }
}
</script>
