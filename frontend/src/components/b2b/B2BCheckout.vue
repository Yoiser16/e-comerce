<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    <div class="max-w-[900px] mx-auto px-4 sm:px-6 py-6 lg:py-8">
      
      <!-- Breadcrumb -->
      <nav class="flex items-center gap-2 text-sm text-gray-400 mb-6">
        <router-link to="/portal" class="hover:text-gray-600 transition-colors">Portal</router-link>
        <span>/</span>
        <router-link to="/portal/carrito" class="hover:text-gray-600 transition-colors">Carrito</router-link>
        <span>/</span>
        <span class="text-gray-700">Checkout</span>
      </nav>

      <!-- Step Indicator -->
      <div class="flex items-center justify-center gap-2 mb-8">
        <div 
          v-for="(stepInfo, index) in steps" 
          :key="index"
          class="flex items-center gap-2"
        >
          <div 
            class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors"
            :class="currentStep > index ? 'bg-gray-900 text-white' : currentStep === index ? 'bg-gray-900 text-white' : 'bg-gray-200 text-gray-500'"
          >
            <svg v-if="currentStep > index" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            <span v-else>{{ index + 1 }}</span>
          </div>
          <span 
            class="text-sm hidden sm:inline"
            :class="currentStep >= index ? 'text-gray-900' : 'text-gray-400'"
          >{{ stepInfo.title }}</span>
          <div v-if="index < steps.length - 1" class="w-8 h-px bg-gray-300 mx-2"></div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left Column: Steps -->
        <div class="lg:col-span-8">
          
          <!-- ====================================
               STEP 1: DIRECCIÓN DE ENTREGA
          ==================================== -->
          <div v-if="currentStep === 0" class="bg-white rounded-lg border border-gray-200 p-5">
            <h2 class="text-lg font-semibold text-gray-900 mb-1">Revisa la forma de entrega</h2>
            <p class="text-sm text-gray-500 mb-6">Confirma o actualiza tu dirección de envío</p>

            <!-- Si tiene dirección guardada -->
            <div v-if="hasSavedAddress && !editingAddress" class="space-y-4">
              <label class="flex items-start gap-3 p-4 border border-gray-900 rounded-lg bg-gray-50 cursor-pointer">
                <input type="radio" checked class="mt-1 w-4 h-4 text-gray-900" />
                <div class="flex-1">
                  <div class="flex justify-between items-start">
                    <p class="font-medium text-gray-900">Enviar a domicilio</p>
                    <span class="text-gray-900 font-medium">${{ formatPrice(shippingCost) }}</span>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">{{ savedAddress.direccion }} - {{ savedAddress.ciudad }}, {{ savedAddress.departamento }}</p>
                  <p class="text-xs text-gray-400 mt-0.5">{{ savedAddress.tipo || 'Residencial' }}</p>
                </div>
              </label>

              <button 
                @click="editingAddress = true"
                class="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                Modificar domicilio o elegir otro
              </button>

              <div class="pt-4">
                <button 
                  @click="goToStep(1)"
                  class="w-full sm:w-auto px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
                >
                  Continuar
                </button>
              </div>
            </div>

            <!-- Formulario de dirección (sin dirección guardada o editando) -->
            <div v-else class="space-y-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="sm:col-span-2">
                  <label class="block text-sm text-gray-600 mb-1">Dirección *</label>
                  <input 
                    v-model="form.direccion"
                    type="text"
                    placeholder="Calle, número, barrio..."
                    class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  />
                </div>
                <div>
                  <label class="block text-sm text-gray-600 mb-1">Ciudad *</label>
                  <input 
                    v-model="form.ciudad"
                    type="text"
                    class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  />
                </div>
                <div>
                  <label class="block text-sm text-gray-600 mb-1">Departamento *</label>
                  <input 
                    v-model="form.departamento"
                    type="text"
                    class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  />
                </div>
                <div>
                  <label class="block text-sm text-gray-600 mb-1">Teléfono *</label>
                  <input 
                    v-model="form.telefono"
                    type="tel"
                    class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  />
                </div>
                <div>
                  <label class="block text-sm text-gray-600 mb-1">Tipo de dirección</label>
                  <select 
                    v-model="form.tipo"
                    class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  >
                    <option value="Residencial">Residencial</option>
                    <option value="Comercial">Comercial</option>
                    <option value="Oficina">Oficina</option>
                  </select>
                </div>
                <div class="sm:col-span-2">
                  <label class="block text-sm text-gray-600 mb-1">Indicaciones adicionales</label>
                  <input 
                    v-model="form.indicaciones"
                    type="text"
                    placeholder="Apartamento, piso, punto de referencia..."
                    class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  />
                </div>
              </div>

              <div class="flex gap-3 pt-4">
                <button 
                  v-if="hasSavedAddress"
                  @click="editingAddress = false"
                  class="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancelar
                </button>
                <button 
                  @click="saveAddressAndContinue"
                  :disabled="!isAddressValid"
                  class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Continuar
                </button>
              </div>
            </div>
          </div>

          <!-- ====================================
               STEP 2: VALIDAR UBICACIÓN EN MAPA
          ==================================== -->
          <div v-if="currentStep === 1" class="bg-white rounded-lg border border-gray-200 p-5">
            <h2 class="text-lg font-semibold text-gray-900 mb-1">Revisa la dirección</h2>
            <p class="text-sm text-gray-500 mb-4">Confirma que el marcador esté en la ubicación correcta. Puedes moverlo si es necesario.</p>

            <!-- Address display -->
            <div class="bg-gray-50 rounded-lg p-3 mb-4 flex items-center gap-3">
              <svg class="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <p class="text-sm text-gray-700">{{ fullAddress }}</p>
            </div>

            <!-- Map Container -->
            <div class="relative rounded-lg overflow-hidden border border-gray-200 mb-4" style="height: 350px;">
              <div ref="mapContainer" class="w-full h-full"></div>
              
              <!-- Map loading placeholder -->
              <div v-if="!mapLoaded" class="absolute inset-0 bg-gray-100 flex items-center justify-center">
                <div class="text-center">
                  <svg class="w-8 h-8 text-gray-400 mx-auto mb-2 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <p class="text-sm text-gray-500">Cargando mapa...</p>
                </div>
              </div>
            </div>

            <!-- Instructions -->
            <p class="text-xs text-gray-500 mb-4 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Arrastra el marcador para ajustar la ubicación exacta
            </p>

            <!-- Buttons -->
            <div class="flex gap-3">
              <button 
                @click="goToStep(0)"
                class="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                ← Volver
              </button>
              <button 
                @click="confirmLocation"
                class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
              >
                Confirmar ubicación
              </button>
            </div>
          </div>

          <!-- ====================================
               STEP 3: MÉTODO DE PAGO
          ==================================== -->
          <div v-if="currentStep === 2" class="bg-white rounded-lg border border-gray-200 p-5">
            <h2 class="text-lg font-semibold text-gray-900 mb-1">Elige el método de pago</h2>
            <p class="text-sm text-gray-500 mb-6">Selecciona cómo deseas completar tu pedido</p>

            <div class="space-y-3">
              <!-- WhatsApp Option -->
              <label 
                class="flex items-start gap-4 p-4 border rounded-lg cursor-pointer transition-colors"
                :class="form.metodoPago === 'whatsapp' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
              >
                <input 
                  v-model="form.metodoPago"
                  type="radio"
                  value="whatsapp"
                  class="mt-1 w-4 h-4 text-gray-900 focus:ring-gray-500"
                />
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                    </svg>
                    <p class="font-medium text-gray-900">Finalizar por WhatsApp</p>
                  </div>
                  <p class="text-sm text-gray-500 mt-1">Enviaremos tu pedido a nuestro asesor para coordinar el pago (transferencia, Nequi, Daviplata)</p>
                </div>
              </label>

              <!-- Wompi Option -->
              <label 
                class="flex items-start gap-4 p-4 border rounded-lg cursor-pointer transition-colors"
                :class="form.metodoPago === 'wompi' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
              >
                <input 
                  v-model="form.metodoPago"
                  type="radio"
                  value="wompi"
                  class="mt-1 w-4 h-4 text-gray-900 focus:ring-gray-500"
                />
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                    </svg>
                    <p class="font-medium text-gray-900">Pagar con Wompi</p>
                  </div>
                  <p class="text-sm text-gray-500 mt-1">Tarjeta de crédito/débito, PSE, Bancolombia, Nequi, Efecty</p>
                  <div class="flex items-center gap-2 mt-2">
                    <span class="text-xs text-gray-400">Powered by</span>
                    <span class="text-xs font-medium text-gray-600">Wompi</span>
                  </div>
                </div>
              </label>
            </div>

            <!-- Notas del pedido -->
            <div class="mt-6">
              <label class="block text-sm text-gray-600 mb-1">Notas del pedido (opcional)</label>
              <textarea 
                v-model="form.notas"
                rows="2"
                placeholder="Instrucciones especiales..."
                class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:ring-1 focus:ring-gray-300 focus:border-gray-300 resize-none text-sm"
              ></textarea>
            </div>

            <!-- Buttons -->
            <div class="flex gap-3 mt-6">
              <button 
                @click="goToStep(1)"
                class="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                ← Volver
              </button>
              <button 
                @click="submitOrder"
                :disabled="isSubmitting || !form.metodoPago"
                class="flex-1 sm:flex-none px-8 py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <span v-if="isSubmitting">Procesando...</span>
                <template v-else>
                  <span v-if="form.metodoPago === 'whatsapp'">Enviar a WhatsApp</span>
                  <span v-else>Ir a pagar</span>
                </template>
              </button>
            </div>
          </div>
        </div>

        <!-- Right Column: Order Summary -->
        <div class="lg:col-span-4">
          <div class="bg-white rounded-lg border border-gray-200 p-5 lg:sticky lg:top-24">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Resumen de compra</h3>

            <!-- Products summary -->
            <div class="space-y-2 pb-4 border-b border-gray-100">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Productos ({{ cartItems.length }})</span>
                <span class="text-gray-900">${{ formatPrice(subtotal) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Envío</span>
                <span class="text-gray-900">${{ formatPrice(shippingCost) }}</span>
              </div>
            </div>

            <!-- Total -->
            <div class="py-4">
              <div class="flex justify-between items-baseline">
                <span class="text-gray-600">Total</span>
                <p class="text-xl font-bold text-gray-900">${{ formatPrice(total) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'B2BCheckout',
  setup() {
    const router = useRouter()
    const mapContainer = ref(null)
    const mapLoaded = ref(false)
    let map = null
    let marker = null

    // State
    const currentStep = ref(0)
    const cartItems = ref([])
    const isSubmitting = ref(false)
    const editingAddress = ref(false)
    const freeShippingThreshold = 500000

    const steps = [
      { title: 'Dirección' },
      { title: 'Ubicación' },
      { title: 'Pago' }
    ]

    const savedAddress = reactive({
      direccion: '',
      ciudad: '',
      departamento: '',
      telefono: '',
      tipo: 'Residencial',
      indicaciones: '',
      lat: null,
      lng: null
    })

    const form = reactive({
      direccion: '',
      ciudad: '',
      departamento: '',
      telefono: '',
      tipo: 'Residencial',
      indicaciones: '',
      metodoPago: 'whatsapp',
      notas: '',
      lat: null,
      lng: null
    })

    // Computed
    const hasSavedAddress = computed(() => {
      return savedAddress.direccion && savedAddress.ciudad && savedAddress.departamento
    })

    const isAddressValid = computed(() => {
      return form.direccion && form.ciudad && form.departamento && form.telefono
    })

    const fullAddress = computed(() => {
      const addr = hasSavedAddress.value && !editingAddress.value ? savedAddress : form
      return `${addr.direccion} - ${addr.ciudad}, ${addr.departamento}`
    })

    const subtotal = computed(() => {
      return cartItems.value.reduce((sum, item) => {
        const qty = item.cantidad || item.quantity || 1
        const price = item.precio || item.wholesalePrice || 0
        return sum + (price * qty)
      }, 0)
    })

    const shippingCost = computed(() => {
      if (subtotal.value >= freeShippingThreshold) return 0
      return 33182
    })

    const total = computed(() => subtotal.value + shippingCost.value)

    // Methods
    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

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

    function loadUserData() {
      const userData = localStorage.getItem('b2b_user')
      if (userData) {
        try {
          const user = JSON.parse(userData)
          if (user.direccion) {
            savedAddress.direccion = user.direccion || ''
            savedAddress.ciudad = user.ciudad || ''
            savedAddress.departamento = user.departamento || ''
            savedAddress.telefono = user.telefono || ''
            savedAddress.tipo = user.tipo_direccion || 'Residencial'
            savedAddress.indicaciones = user.indicaciones || ''
            savedAddress.lat = user.lat || null
            savedAddress.lng = user.lng || null
          }
          form.telefono = user.telefono || ''
        } catch {
          // Sin datos
        }
      }
    }

    function goToStep(step) {
      currentStep.value = step
      if (step === 1) {
        nextTick(() => initMap())
      }
    }

    function saveAddressAndContinue() {
      if (!isAddressValid.value) return
      Object.assign(savedAddress, {
        direccion: form.direccion,
        ciudad: form.ciudad,
        departamento: form.departamento,
        telefono: form.telefono,
        tipo: form.tipo,
        indicaciones: form.indicaciones
      })
      editingAddress.value = false
      goToStep(1)
    }

    async function initMap() {
      if (map) {
        updateMapLocation()
        return
      }

      if (typeof google === 'undefined' || !google.maps) {
        await loadGoogleMapsScript()
      }

      const address = hasSavedAddress.value && !editingAddress.value ? savedAddress : form
      const geocoder = new google.maps.Geocoder()
      const fullAddr = `${address.direccion}, ${address.ciudad}, ${address.departamento}, Colombia`
      
      geocoder.geocode({ address: fullAddr }, (results, status) => {
        let lat = 4.6097
        let lng = -74.0817
        
        if (status === 'OK' && results[0]) {
          lat = results[0].geometry.location.lat()
          lng = results[0].geometry.location.lng()
        } else if (address.lat && address.lng) {
          lat = address.lat
          lng = address.lng
        }

        map = new google.maps.Map(mapContainer.value, {
          center: { lat, lng },
          zoom: 16,
          disableDefaultUI: true,
          zoomControl: true,
          mapTypeControl: false,
          streetViewControl: false,
          fullscreenControl: false
        })

        marker = new google.maps.Marker({
          position: { lat, lng },
          map: map,
          draggable: true,
          animation: google.maps.Animation.DROP
        })

        marker.addListener('dragend', () => {
          const pos = marker.getPosition()
          form.lat = pos.lat()
          form.lng = pos.lng()
        })

        form.lat = lat
        form.lng = lng
        mapLoaded.value = true
      })
    }

    function loadGoogleMapsScript() {
      return new Promise((resolve, reject) => {
        if (typeof google !== 'undefined' && google.maps) {
          resolve()
          return
        }

        const script = document.createElement('script')
        script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''}&libraries=places`
        script.async = true
        script.defer = true
        script.onload = resolve
        script.onerror = reject
        document.head.appendChild(script)
      })
    }

    function updateMapLocation() {
      if (!map || !marker) return
      const address = hasSavedAddress.value && !editingAddress.value ? savedAddress : form
      
      const geocoder = new google.maps.Geocoder()
      const fullAddr = `${address.direccion}, ${address.ciudad}, ${address.departamento}, Colombia`
      
      geocoder.geocode({ address: fullAddr }, (results, status) => {
        if (status === 'OK' && results[0]) {
          const location = results[0].geometry.location
          map.setCenter(location)
          marker.setPosition(location)
          form.lat = location.lat()
          form.lng = location.lng()
        }
      })
    }

    function confirmLocation() {
      savedAddress.lat = form.lat
      savedAddress.lng = form.lng
      goToStep(2)
    }

    async function submitOrder() {
      if (isSubmitting.value) return
      isSubmitting.value = true

      try {
        const orderData = {
          direccion: savedAddress.direccion || form.direccion,
          ciudad: savedAddress.ciudad || form.ciudad,
          departamento: savedAddress.departamento || form.departamento,
          telefono: savedAddress.telefono || form.telefono,
          indicaciones: form.indicaciones,
          lat: form.lat,
          lng: form.lng,
          metodoPago: form.metodoPago,
          notas: form.notas,
          items: cartItems.value,
          subtotal: subtotal.value,
          envio: shippingCost.value,
          total: total.value
        }

        if (form.metodoPago === 'whatsapp') {
          const itemsText = cartItems.value.map(item => {
            const name = item.nombre || item.name
            const qty = item.cantidad || item.quantity
            const price = item.precio || item.wholesalePrice
            return `• ${name} x${qty} = $${formatPrice(price * qty)}`
          }).join('%0A')

          const message = `🛒 *PEDIDO MAYORISTA*%0A%0A` +
            `📦 *Productos:*%0A${itemsText}%0A%0A` +
            `💰 *Subtotal:* $${formatPrice(subtotal.value)}%0A` +
            `🚚 *Envío:* $${formatPrice(shippingCost.value)}%0A` +
            `*TOTAL: $${formatPrice(total.value)}*%0A%0A` +
            `📍 *Dirección:*%0A${orderData.direccion}%0A${orderData.ciudad}, ${orderData.departamento}%0A%0A` +
            `📱 *Teléfono:* ${orderData.telefono}%0A` +
            (orderData.notas ? `📝 *Notas:* ${orderData.notas}` : '')

          const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER || '573001234567'
          window.open(`https://wa.me/${whatsappNumber}?text=${message}`, '_blank')
          localStorage.removeItem('b2b_cart')
          router.push({ path: '/portal/pedidos', query: { success: 'whatsapp' } })
        } else {
          // TODO: Integrar Wompi widget
          alert('Redirigiendo a Wompi para completar el pago...')
          localStorage.removeItem('b2b_cart')
          router.push({ path: '/portal/pedidos', query: { success: 'wompi', pending: 'true' } })
        }
      } catch (error) {
        console.error('Error al procesar pedido:', error)
        alert('Error al procesar el pedido. Por favor intenta nuevamente.')
      } finally {
        isSubmitting.value = false
      }
    }

    onMounted(() => {
      loadCart()
      loadUserData()

      if (cartItems.value.length === 0) {
        router.replace('/portal/carrito')
      }
    })

    return {
      mapContainer,
      mapLoaded,
      currentStep,
      steps,
      cartItems,
      isSubmitting,
      editingAddress,
      savedAddress,
      form,
      hasSavedAddress,
      isAddressValid,
      fullAddress,
      subtotal,
      shippingCost,
      total,
      formatPrice,
      goToStep,
      saveAddressAndContinue,
      confirmLocation,
      submitOrder
    }
  }
}
</script>
