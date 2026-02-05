<template>
  <div class="max-w-6xl mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Mi Pedido Mayorista</h1>
        <p class="text-gray-500 mt-1">{{ cartItems.length }} productos en tu carrito</p>
      </div>
      <router-link 
        to="/portal/catalogo"
        class="flex items-center gap-2 text-[#C9A962] hover:text-[#B8984F] font-medium"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Agregar más productos
      </router-link>
    </div>

    <!-- Contenido Principal -->
    <div v-if="cartItems.length > 0" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Lista de Productos -->
      <div class="lg:col-span-2 space-y-4">
        <!-- Item del carrito -->
        <div 
          v-for="item in cartItems" 
          :key="item.id"
          class="bg-white rounded-xl border border-gray-100 p-4 sm:p-5 flex gap-4 group hover:shadow-md transition-shadow"
        >
          <!-- Imagen -->
          <div class="w-20 h-20 sm:w-24 sm:h-24 rounded-lg bg-gray-100 overflow-hidden flex-shrink-0">
            <img 
              :src="item.image || placeholderImage(item.name)"
              :alt="item.name"
              class="w-full h-full object-cover"
            />
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0">
                <p class="text-xs text-gray-400 uppercase tracking-wider mb-1">{{ item.category }}</p>
                <h3 class="font-semibold text-gray-900 truncate">{{ item.name }}</h3>
                <p class="text-xs text-gray-400 mt-0.5">SKU: {{ item.sku }}</p>
              </div>
              <button 
                @click="removeItem(item.id)"
                class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>

            <!-- Precio y cantidad -->
            <div class="flex flex-wrap items-end justify-between gap-4 mt-4">
              <div>
                <p class="text-xs text-gray-400 line-through">${{ formatPrice(item.retailPrice) }}</p>
                <p class="text-lg font-bold text-[#C9A962]">${{ formatPrice(item.wholesalePrice) }}</p>
                <p class="text-xs text-emerald-600">Ahorras ${{ formatPrice(item.retailPrice - item.wholesalePrice) }}/ud</p>
              </div>

              <!-- Cantidad -->
              <div class="flex items-center gap-3">
                <div class="flex items-center border border-gray-200 rounded-lg overflow-hidden">
                  <button 
                    @click="updateQuantity(item.id, item.quantity - 1)"
                    :disabled="item.quantity <= item.minOrder"
                    class="w-10 h-10 flex items-center justify-center hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                    </svg>
                  </button>
                  <input 
                    :value="item.quantity"
                    @change="updateQuantity(item.id, parseInt($event.target.value) || item.minOrder)"
                    type="number"
                    :min="item.minOrder"
                    :max="item.stock"
                    class="w-14 h-10 text-center border-x border-gray-200 focus:outline-none text-sm font-semibold"
                  />
                  <button 
                    @click="updateQuantity(item.id, item.quantity + 1)"
                    :disabled="item.quantity >= item.stock"
                    class="w-10 h-10 flex items-center justify-center hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                  </button>
                </div>

                <!-- Subtotal item -->
                <div class="text-right min-w-[100px]">
                  <p class="text-xs text-gray-400">Subtotal</p>
                  <p class="text-lg font-bold text-gray-900">${{ formatPrice(item.wholesalePrice * item.quantity) }}</p>
                </div>
              </div>
            </div>

            <!-- Mínimo de orden -->
            <p v-if="item.quantity < item.minOrder" class="text-xs text-amber-600 mt-2 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              Mínimo de compra: {{ item.minOrder }} unidades
            </p>
          </div>
        </div>

        <!-- Notas del pedido -->
        <div class="bg-white rounded-xl border border-gray-100 p-5">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Notas para el pedido (opcional)
          </label>
          <textarea 
            v-model="orderNotes"
            rows="3"
            placeholder="Instrucciones especiales, información de entrega, etc..."
            class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] resize-none text-sm"
          ></textarea>
        </div>
      </div>

      <!-- Resumen del Pedido -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-xl border border-gray-100 p-5 sticky top-24">
          <h2 class="text-lg font-bold text-gray-900 mb-4">Resumen del Pedido</h2>

          <!-- Detalles -->
          <div class="space-y-3 pb-4 border-b border-gray-100">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Subtotal ({{ totalItems }} productos)</span>
              <span class="font-medium text-gray-900">${{ formatPrice(subtotal) }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Descuento mayorista</span>
              <span class="font-medium text-emerald-600">-${{ formatPrice(totalDiscount) }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Envío</span>
              <span class="font-medium text-gray-900">
                {{ shippingCost === 0 ? 'Gratis' : `$${formatPrice(shippingCost)}` }}
              </span>
            </div>
          </div>

          <!-- Total -->
          <div class="py-4 border-b border-gray-100">
            <div class="flex justify-between items-baseline">
              <span class="text-gray-900 font-semibold">Total a Pagar</span>
              <div class="text-right">
                <p class="text-2xl font-bold text-gray-900">${{ formatPrice(total) }}</p>
                <p class="text-xs text-gray-400">IVA incluido</p>
              </div>
            </div>
          </div>

          <!-- Ahorro total -->
          <div class="py-4 bg-emerald-50 -mx-5 px-5 mb-4 flex items-center gap-3">
            <div class="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm font-semibold text-emerald-900">¡Estás ahorrando!</p>
              <p class="text-lg font-bold text-emerald-600">${{ formatPrice(totalDiscount) }}</p>
            </div>
          </div>

          <!-- Beneficios -->
          <div class="space-y-2 mb-6">
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Envío gratis en pedidos +$500.000
            </div>
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Entrega en 24-48 horas
            </div>
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Factura electrónica incluida
            </div>
          </div>

          <!-- Botón de checkout -->
          <button 
            @click="proceedToCheckout"
            :disabled="!canCheckout"
            class="w-full py-4 bg-[#1A1A1A] hover:bg-black text-white font-bold rounded-xl transition-colors 
                   disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 group"
          >
            Confirmar Pedido
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>

          <!-- Contacto -->
          <div class="mt-4 text-center">
            <p class="text-xs text-gray-400 mb-2">¿Necesitas ayuda?</p>
            <a 
              href="https://wa.me/573001234567?text=Hola,%20tengo%20una%20consulta%20sobre%20mi%20pedido%20mayorista"
              target="_blank"
              class="inline-flex items-center gap-2 text-sm text-green-600 hover:text-green-700 font-medium"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
              </svg>
              Contactar por WhatsApp
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-16 bg-white rounded-2xl border border-gray-100">
      <div class="w-24 h-24 mx-auto mb-6 bg-gray-100 rounded-2xl flex items-center justify-center">
        <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">Tu carrito está vacío</h2>
      <p class="text-gray-500 mb-8 max-w-md mx-auto">
        Explora nuestro catálogo mayorista y agrega productos para crear tu pedido
      </p>
      <router-link 
        to="/portal/catalogo" 
        class="inline-flex items-center gap-2 px-8 py-4 bg-[#1A1A1A] hover:bg-black text-white font-bold rounded-xl transition-colors group"
      >
        Explorar Catálogo
        <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'B2BCarrito',
  setup() {
    const router = useRouter()
    const cartItems = ref([])
    const orderNotes = ref('')
    const freeShippingThreshold = 500000

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
    }

    // Computed
    const totalItems = computed(() => cartItems.value.reduce((sum, item) => sum + item.quantity, 0))

    const subtotal = computed(() => cartItems.value.reduce((sum, item) => sum + (item.wholesalePrice * item.quantity), 0))

    const totalDiscount = computed(() => {
      return cartItems.value.reduce((sum, item) => {
        const discount = (item.retailPrice - item.wholesalePrice) * item.quantity
        return sum + discount
      }, 0)
    })

    const shippingCost = computed(() => {
      if (subtotal.value >= freeShippingThreshold) return 0
      return 25000 // Costo de envío si no cumple el mínimo
    })

    const total = computed(() => subtotal.value + shippingCost.value)

    const canCheckout = computed(() => {
      if (cartItems.value.length === 0) return false
      // Verificar que todos los items cumplan el mínimo de orden
      return cartItems.value.every(item => item.quantity >= item.minOrder)
    })

    // Methods
    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

    function placeholderImage(name) {
      const initials = name?.substring(0, 3).toUpperCase() || 'PRD'
      return `https://placehold.co/200x200/f5f5f5/1a1a1a?text=${encodeURIComponent(initials)}`
    }

    function updateQuantity(itemId, newQuantity) {
      const item = cartItems.value.find(i => i.id === itemId)
      if (item) {
        const qty = Math.max(1, Math.min(newQuantity, item.stock))
        item.quantity = qty
        saveCart()
      }
    }

    function removeItem(itemId) {
      cartItems.value = cartItems.value.filter(i => i.id !== itemId)
      saveCart()
    }

    function proceedToCheckout() {
      if (!canCheckout.value) return
      // TODO: Implementar flujo de checkout
      alert('Redirigiendo al checkout...')
      // router.push('/portal/checkout')
    }

    // Watch para persistir cambios
    watch(cartItems, saveCart, { deep: true })

    onMounted(() => {
      loadCart()
      
      // Si el carrito está vacío, agregar items de ejemplo para demo
      if (cartItems.value.length === 0) {
        cartItems.value = [
          { id: 1, name: 'Extensión Tape-in Premium 60cm Rubio #613', category: 'Extensiones', sku: 'EXT-001', image: 'https://placehold.co/200x200/f5f5f5/1a1a1a?text=EXT', retailPrice: 290000, wholesalePrice: 245000, stock: 28, minOrder: 2, quantity: 4 },
          { id: 2, name: 'Shampoo Profesional Sin Sulfatos 1L', category: 'Tratamientos', sku: 'SHP-002', image: 'https://placehold.co/200x200/f5f5f5/1a1a1a?text=SHP', retailPrice: 85000, wholesalePrice: 68000, stock: 45, minOrder: 6, quantity: 12 },
          { id: 4, name: 'Kit Balayage Profesional 6 Tonos', category: 'Coloración', sku: 'BAL-004', image: 'https://placehold.co/200x200/f5f5f5/1a1a1a?text=BAL', retailPrice: 245000, wholesalePrice: 189000, stock: 8, minOrder: 1, quantity: 2 }
        ]
        saveCart()
      }
    })

    return {
      cartItems, orderNotes,
      totalItems, subtotal, totalDiscount, shippingCost, total, canCheckout,
      formatPrice, placeholderImage, updateQuantity, removeItem, proceedToCheckout
    }
  }
}
</script>
