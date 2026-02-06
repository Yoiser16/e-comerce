<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
      
      <!-- Breadcrumb discreto -->
      <nav class="flex items-center gap-2 text-sm text-gray-400 mb-6">
        <router-link to="/portal" class="hover:text-gray-600 transition-colors">Portal</router-link>
        <span>/</span>
        <router-link to="/portal/carrito" class="hover:text-gray-600 transition-colors">Carrito</router-link>
        <span>/</span>
        <span class="text-gray-700">Confirmar pedido</span>
      </nav>

      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-xl font-semibold text-gray-900">Confirmar Pedido Mayorista</h1>
        <p class="text-sm text-gray-500 mt-1">Revisa los datos antes de enviar tu solicitud</p>
      </div>

      <!-- Grid 2 columnas -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
        
        <!-- ====================================
             COLUMNA IZQUIERDA: Formulario (8 cols)
        ==================================== -->
        <div class="lg:col-span-8 space-y-5">
          
          <!-- Sección: Datos de entrega -->
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Datos de entrega</h2>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="sm:col-span-2">
                <label class="block text-sm text-gray-600 mb-1">Nombre o Razón Social *</label>
                <input 
                  v-model="form.nombre"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-200 rounded focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  :class="{'border-red-300': errors.nombre}"
                />
                <p v-if="errors.nombre" class="text-xs text-red-500 mt-1">{{ errors.nombre }}</p>
              </div>
              <div>
                <label class="block text-sm text-gray-600 mb-1">NIT / Cédula *</label>
                <input 
                  v-model="form.documento"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-200 rounded focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  :class="{'border-red-300': errors.documento}"
                />
              </div>
              <div>
                <label class="block text-sm text-gray-600 mb-1">Teléfono *</label>
                <input 
                  v-model="form.telefono"
                  type="tel"
                  class="w-full px-3 py-2 border border-gray-200 rounded focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  :class="{'border-red-300': errors.telefono}"
                />
              </div>
              <div class="sm:col-span-2">
                <label class="block text-sm text-gray-600 mb-1">Dirección de entrega *</label>
                <input 
                  v-model="form.direccion"
                  type="text"
                  placeholder="Calle, número, barrio..."
                  class="w-full px-3 py-2 border border-gray-200 rounded focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  :class="{'border-red-300': errors.direccion}"
                />
              </div>
              <div>
                <label class="block text-sm text-gray-600 mb-1">Ciudad *</label>
                <input 
                  v-model="form.ciudad"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-200 rounded focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  :class="{'border-red-300': errors.ciudad}"
                />
              </div>
              <div>
                <label class="block text-sm text-gray-600 mb-1">Departamento *</label>
                <input 
                  v-model="form.departamento"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-200 rounded focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm"
                  :class="{'border-red-300': errors.departamento}"
                />
              </div>
            </div>
          </div>

          <!-- Sección: Método de pago -->
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Método de pago</h2>
            
            <div class="space-y-3">
              <label 
                v-for="method in paymentMethods" 
                :key="method.id"
                class="flex items-center gap-3 p-3 border rounded cursor-pointer transition-colors"
                :class="form.metodoPago === method.id ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
              >
                <input 
                  v-model="form.metodoPago"
                  type="radio"
                  :value="method.id"
                  class="w-4 h-4 text-gray-900 focus:ring-gray-500"
                />
                <div class="flex-1">
                  <p class="text-sm font-medium text-gray-900">{{ method.name }}</p>
                  <p class="text-xs text-gray-500">{{ method.description }}</p>
                </div>
              </label>
            </div>
          </div>

          <!-- Sección: Notas adicionales -->
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Notas del pedido</h2>
            <textarea 
              v-model="form.notas"
              rows="2"
              placeholder="Instrucciones especiales de entrega o facturación..."
              class="w-full px-3 py-2 border border-gray-200 rounded focus:ring-1 focus:ring-gray-300 focus:border-gray-300 resize-none text-sm"
            ></textarea>
          </div>
        </div>

        <!-- ====================================
             COLUMNA DERECHA: Resumen (4 cols) - STICKY
        ==================================== -->
        <div class="lg:col-span-4">
          <div class="bg-white rounded-lg border border-gray-200 p-5 lg:sticky lg:top-24">
            
            <!-- Header -->
            <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Resumen</h2>

            <!-- Lista de productos resumida -->
            <div class="space-y-2 pb-4 border-b border-gray-100 max-h-48 overflow-y-auto">
              <div 
                v-for="item in cartItems" 
                :key="item.id"
                class="flex justify-between text-sm"
              >
                <span class="text-gray-600 truncate flex-1 pr-2">
                  {{ item.nombre || item.name }} × {{ item.cantidad || item.quantity }}
                </span>
                <span class="text-gray-900 flex-shrink-0">${{ formatPrice(getItemTotal(item)) }}</span>
              </div>
            </div>

            <!-- Totales -->
            <div class="space-y-3 py-4 border-b border-gray-100">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Subtotal</span>
                <span class="text-gray-900">${{ formatPrice(subtotal) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Envío</span>
                <span class="text-gray-900">{{ shippingCost === 0 ? 'Incluido' : `$${formatPrice(shippingCost)}` }}</span>
              </div>
            </div>

            <!-- Total destacado -->
            <div class="py-4 border-b border-gray-100">
              <div class="flex justify-between items-baseline">
                <span class="text-gray-500 text-sm">TOTAL</span>
                <p class="text-2xl font-bold text-gray-900">${{ formatPrice(total) }}</p>
              </div>
              <p class="text-xs text-gray-400 text-right mt-1">IVA incluido</p>
            </div>

            <!-- CTA -->
            <div class="pt-5 space-y-3">
              <button 
                @click="submitOrder"
                :disabled="isSubmitting || !isFormValid"
                class="w-full py-4 bg-[#1A1A1A] hover:bg-black text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <span v-if="isSubmitting">Procesando...</span>
                <span v-else>Enviar pedido</span>
              </button>

              <router-link 
                to="/portal/carrito"
                class="block text-center text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                ← Volver al carrito
              </router-link>
            </div>

            <!-- Info discreta -->
            <div class="mt-5 pt-4 border-t border-gray-100">
              <p class="text-xs text-gray-400 text-center">
                Recibirás confirmación por correo electrónico
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'B2BCheckout',
  setup() {
    const router = useRouter()
    const cartItems = ref([])
    const isSubmitting = ref(false)
    const freeShippingThreshold = 500000

    const form = reactive({
      nombre: '',
      documento: '',
      telefono: '',
      direccion: '',
      ciudad: '',
      departamento: '',
      metodoPago: 'transferencia',
      notas: ''
    })

    const errors = reactive({})

    const paymentMethods = [
      { id: 'transferencia', name: 'Transferencia bancaria', description: 'Bancolombia, Davivienda, Nequi' },
      { id: 'contraentrega', name: 'Pago contra entrega', description: 'Solo Bogotá y ciudades principales' },
      { id: 'credito', name: 'Crédito 30 días', description: 'Requiere aprobación previa' }
    ]

    // Helpers
    const getQuantity = (item) => item.cantidad || item.quantity || 1
    const getPrice = (item) => item.precio || item.wholesalePrice || 0
    const getItemTotal = (item) => getPrice(item) * getQuantity(item)

    // Computed
    const subtotal = computed(() => cartItems.value.reduce((sum, item) => sum + getItemTotal(item), 0))

    const shippingCost = computed(() => {
      if (subtotal.value >= freeShippingThreshold) return 0
      return 25000
    })

    const total = computed(() => subtotal.value + shippingCost.value)

    const isFormValid = computed(() => {
      return form.nombre && form.documento && form.telefono && 
             form.direccion && form.ciudad && form.departamento && 
             form.metodoPago && cartItems.value.length > 0
    })

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
          form.nombre = user.nombre || user.razon_social || ''
          form.documento = user.nit || user.documento || ''
          form.telefono = user.telefono || ''
          form.direccion = user.direccion || ''
          form.ciudad = user.ciudad || ''
          form.departamento = user.departamento || ''
        } catch {
          // No precargar datos
        }
      }
    }

    async function submitOrder() {
      if (!isFormValid.value || isSubmitting.value) return

      isSubmitting.value = true

      try {
        // TODO: Implementar llamada real a API
        // const response = await api.createOrder({ ...form, items: cartItems.value })
        
        // Simular delay de procesamiento
        await new Promise(resolve => setTimeout(resolve, 1500))

        // Limpiar carrito
        localStorage.removeItem('b2b_cart')
        
        // Redirigir a confirmación o pedidos
        router.push({ 
          path: '/portal/pedidos',
          query: { success: 'true' }
        })
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

      // Si no hay items, volver al carrito
      if (cartItems.value.length === 0) {
        router.replace('/portal/carrito')
      }
    })

    return {
      cartItems, form, errors, paymentMethods,
      isSubmitting, isFormValid,
      subtotal, shippingCost, total,
      formatPrice, getItemTotal, submitOrder
    }
  }
}
</script>
