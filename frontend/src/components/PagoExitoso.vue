<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FBF9F7] to-[#F5F0EC] flex flex-col">
    
    <!-- Header Simple -->
    <header class="bg-white/80 border-b border-nude-100/50 py-5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <router-link to="/" class="flex items-center gap-3 w-fit">
          <div class="w-10 h-10 rounded-full bg-gradient-to-br from-brand-500 to-brand-600 flex items-center justify-center shadow-lg shadow-brand-500/20">
            <span class="text-white font-luxury text-lg">K</span>
          </div>
          <span class="font-luxury text-2xl text-text-dark tracking-wide">Kharis</span>
        </router-link>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="flex-1 flex items-center justify-center px-4 py-12">
      <div class="max-w-lg w-full">
        
        <!-- Card de Confirmación -->
        <div class="bg-white rounded-3xl p-8 lg:p-10 shadow-xl shadow-black/[0.03] border border-nude-100/50 text-center">
          
          <!-- Estado de carga -->
          <div v-if="loading" class="py-8">
            <div class="w-16 h-16 mx-auto mb-6 rounded-full bg-brand-100 flex items-center justify-center">
              <svg class="w-8 h-8 text-brand-500 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
            <p class="text-text-medium">Verificando tu pago...</p>
          </div>
          
          <!-- Pago Exitoso -->
          <template v-else-if="paymentStatus === 'approved'">
            <!-- Icono de éxito animado -->
            <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-green-400 to-green-500 flex items-center justify-center shadow-lg shadow-green-500/30 animate-bounce-once">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </div>
            
            <h1 class="font-luxury text-3xl text-text-dark mb-3">¡Pago Exitoso!</h1>
            <p class="text-text-medium mb-6">Tu pedido ha sido confirmado y está en camino ✨</p>
            
            <!-- Detalles del pedido -->
            <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-5 mb-6 text-left border border-green-100">
              <div class="flex items-center gap-2 mb-4">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                </svg>
                <span class="font-semibold text-green-800">Detalles de tu pedido</span>
              </div>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between" v-if="orderCode">
                  <span class="text-green-700">Número de pedido:</span>
                  <span class="font-mono font-semibold text-green-900">{{ orderCode }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-green-700">Referencia Wompi:</span>
                  <span class="font-mono font-semibold text-green-900">{{ transactionRef }}</span>
                </div>
                <div class="flex justify-between" v-if="transactionAmount">
                  <span class="text-green-700">Monto:</span>
                  <span class="font-semibold text-green-900">${{ formatPrice(transactionAmount) }} COP</span>
                </div>
              </div>
            </div>
            
            <!-- Siguiente paso -->
            <div class="bg-brand-50 rounded-xl p-4 mb-6 text-left">
              <p class="text-sm text-brand-700">
                <span class="font-semibold">📧 Próximo paso:</span> Recibirás un correo con los detalles de envío y seguimiento de tu pedido.
              </p>
            </div>
            
            <!-- Error al crear orden -->
            <div v-if="orderError" class="bg-amber-50 rounded-xl p-4 mb-6 text-left border border-amber-200">
              <p class="text-sm text-amber-700">
                <span class="font-semibold">⚠️ Aviso:</span> {{ orderError }}
              </p>
            </div>
          </template>
          
          <!-- Pago Pendiente -->
          <template v-else-if="paymentStatus === 'pending'">
            <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-amber-400 to-orange-400 flex items-center justify-center shadow-lg shadow-amber-500/30">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            
            <h1 class="font-luxury text-3xl text-text-dark mb-3">Pago Pendiente</h1>
            <p class="text-text-medium mb-6">Tu pago está siendo procesado. Te notificaremos cuando se confirme.</p>
            
            <div class="bg-amber-50 rounded-xl p-4 mb-6 text-left border border-amber-200">
              <p class="text-sm text-amber-700">
                <span class="font-semibold">⏳ Referencia:</span> {{ transactionRef }}<br>
                El pago puede tardar hasta 24 horas en confirmarse.
              </p>
            </div>
          </template>
          
          <!-- Pago Rechazado -->
          <template v-else-if="paymentStatus === 'rejected'">
            <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-red-400 to-red-500 flex items-center justify-center shadow-lg shadow-red-500/30">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            
            <h1 class="font-luxury text-3xl text-text-dark mb-3">Pago Rechazado</h1>
            <p class="text-text-medium mb-6">Hubo un problema con tu pago. Por favor intenta de nuevo.</p>
            
            <div class="bg-red-50 rounded-xl p-4 mb-6 text-left border border-red-200">
              <p class="text-sm text-red-700">
                <span class="font-semibold">❌ Motivo:</span> {{ transactionMessage || 'La transacción fue rechazada por el banco.' }}
              </p>
            </div>
          </template>
          
          <!-- Botones de acción -->
          <div class="flex flex-col sm:flex-row gap-3 mt-6">
            <router-link 
              to="/" 
              class="flex-1 bg-gradient-to-r from-brand-600 to-brand-700 hover:from-brand-700 hover:to-brand-800 text-white font-semibold py-3.5 px-6 rounded-xl transition-all duration-300 shadow-lg shadow-brand-600/20 hover:shadow-brand-600/30 text-center"
            >
              Seguir Comprando
            </router-link>
            
            <a 
              :href="whatsappLink"
              target="_blank"
              class="flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-3.5 px-6 rounded-xl transition-all duration-300 shadow-lg shadow-green-500/20 flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
              </svg>
              Contactar Soporte
            </a>
          </div>
        </div>
        
        <!-- Confetti animation for success -->
        <div v-if="paymentStatus === 'approved'" class="fixed inset-0 pointer-events-none z-50 overflow-hidden">
          <div class="confetti-container">
            <div v-for="i in 50" :key="i" class="confetti" :style="getConfettiStyle(i)"></div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Footer -->
    <footer class="py-6 border-t border-nude-100 bg-white/50">
      <div class="max-w-7xl mx-auto px-4 text-center">
        <p class="text-sm text-text-medium">© 2026 Kharis Distribuidora. Todos los derechos reservados.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

// Consistente con api.js - eliminar /api/v1 si viene en VITE_API_URL
const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace('/api/v1', '')

export default {
  name: 'PagoExitoso',
  setup() {
    const route = useRoute()
    const loading = ref(true)
    const paymentStatus = ref('approved') // approved, pending, rejected
    const transactionRef = ref('')
    const transactionAmount = ref(0)
    const transactionMessage = ref('')
    const orderCode = ref('') // Código de orden creada en nuestro sistema
    const orderCreated = ref(false)
    const orderError = ref('') // Para mostrar errores al usuario
    
    const whatsappNumber = '4796657763'
    
    const whatsappLink = computed(() => {
      const codigo = orderCode.value || transactionRef.value
      const mensaje = `Hola, tengo una consulta sobre mi pedido con referencia: ${codigo}`
      return `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(mensaje)}`
    })
    
    const formatPrice = (price) => {
      return new Intl.NumberFormat('es-CO').format(price)
    }
    
    const getConfettiStyle = (index) => {
      const colors = ['#D81B60', '#C9A962', '#4ade80', '#60a5fa', '#f472b6']
      return {
        left: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 3}s`,
        backgroundColor: colors[index % colors.length]
      }
    }
    
    // Crear la orden en el backend después del pago exitoso
    const createOrderFromPendingData = async (wompiTransactionId) => {
      try {
        // Leer datos guardados antes del pago
        const pendingOrderStr = localStorage.getItem('kharis_pending_order')
        if (!pendingOrderStr) {
          console.warn('⚠️ No hay datos de orden pendiente en localStorage')
          orderError.value = 'No se encontraron datos de la orden. Por favor contacta soporte con tu referencia de pago.'
          return false
        }
        
        const pendingOrder = JSON.parse(pendingOrderStr)
        console.log('📦 Creando orden desde datos pendientes:', pendingOrder)
        
        // Validar que tenemos los datos mínimos
        if (!pendingOrder.items || pendingOrder.items.length === 0) {
          orderError.value = 'No hay productos en la orden. Por favor contacta soporte.'
          return false
        }
        
        if (!pendingOrder.customer?.email) {
          orderError.value = 'Falta el email del cliente. Por favor contacta soporte.'
          return false
        }
        
        // Preparar datos para la API de órdenes
        const ordenData = {
          email: pendingOrder.customer?.email || '',
          nombre: pendingOrder.customer?.nombre || '',
          apellido: pendingOrder.customer?.apellido || '',
          telefono: pendingOrder.customer?.telefono || '',
          tipo_documento: pendingOrder.customer?.tipo_documento || 'CC',
          numero_documento: pendingOrder.customer?.numero_documento || '',
          direccion: pendingOrder.customer?.direccion || '',
          departamento: pendingOrder.customer?.departamento || '',
          municipio: pendingOrder.customer?.municipio || '',
          barrio: pendingOrder.customer?.barrio || '',
          notas: `Wompi TX: ${wompiTransactionId || transactionRef.value}`,
          items: (pendingOrder.items || []).map(item => ({
            producto_id: item.id || item.producto_id || '00000000-0000-0000-0000-000000000000',
            variante_id: item.variante_id || null,
            variante_sku: item.variante_sku || '',
            color: item.color || '',
            largo: item.largo || '',
            cantidad: item.cantidad || 1,
            precio_unitario: item.precio_unitario || item.precio || 0,
            nombre: item.nombre || 'Producto'
          })),
          subtotal: pendingOrder.subtotal || pendingOrder.total || 0,
          envio: pendingOrder.envio || 0,
          total: pendingOrder.total || 0,
          metodo_pago: 'wompi'
        }
        
        console.log('🚀 Enviando orden al backend:', ordenData)
        
        // API_BASE_URL es la raíz (ej: http://localhost:8000)
        const apiUrl = `${API_BASE_URL}/api/v1/ordenes`
        console.log('🔗 URL:', apiUrl)
        
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(ordenData)
        })
        
        if (!response.ok) {
          const errorText = await response.text()
          console.error('❌ Error creando orden:', response.status, errorText)
          orderError.value = `Error al registrar orden (${response.status}). Tu pago fue procesado. Contacta soporte con referencia: ${transactionRef.value}`
          return false
        }
        
        const orden = await response.json()
        console.log('✅ Orden creada exitosamente:', orden)
        
        orderCode.value = orden.codigo || ''
        orderCreated.value = true
        orderError.value = ''
        
        // Limpiar datos pendientes
        localStorage.removeItem('kharis_pending_order')
        localStorage.removeItem('kharis_cart_cache')
        localStorage.removeItem('kharis_cart_count')
        
        return true
      } catch (error) {
        console.error('❌ Error al crear orden:', error)
        orderError.value = `Error de conexión: ${error.message}. Tu pago fue procesado. Contacta soporte con referencia: ${transactionRef.value}`
        return false
      }
    }
    
    const parseEpaycoResponse = async () => {
      // Wompi y otros proveedores envían parámetros en la URL
      const params = route.query
      
      // Primero verificar si viene de Wompi
      if (params.ref || params.id) {
        await parseWompiResponse(params)
        return
      }
      
      // Si tiene status directo (desde nuestro callback)
      if (params.status) {
        transactionRef.value = params.ref || `KH-${Date.now()}`
        
        switch (params.status) {
          case 'approved':
            paymentStatus.value = 'approved'
            break
          case 'pending':
            paymentStatus.value = 'pending'
            break
          case 'declined':
          case 'rejected':
            paymentStatus.value = 'rejected'
            transactionMessage.value = 'Transacción rechazada'
            break
          default:
            paymentStatus.value = 'approved'
        }
        
        if (paymentStatus.value === 'approved' || paymentStatus.value === 'pending') {
          localStorage.removeItem('kharis_cart_cache')
          localStorage.removeItem('kharis_cart_count')
        }
        return
      }
      
      // Parámetros típicos de ePayco (legacy):
      // ref_payco, x_transaction_state, x_amount_ok, x_response, x_id_invoice
      
      if (params.ref_payco) {
        transactionRef.value = params.ref_payco
      } else if (params.x_id_invoice) {
        transactionRef.value = params.x_id_invoice
      } else {
        transactionRef.value = `KH-${Date.now()}`
      }
      
      if (params.x_amount) {
        transactionAmount.value = parseFloat(params.x_amount) || 0
      }
      
      // Mapear estado de transacción
      const state = params.x_transaction_state || params.x_cod_response
      
      switch (state) {
        case '1': // Aceptada
        case 'Aceptada':
          paymentStatus.value = 'approved'
          break
        case '2': // Rechazada
        case 'Rechazada':
          paymentStatus.value = 'rejected'
          transactionMessage.value = params.x_response || 'Transacción rechazada'
          break
        case '3': // Pendiente
        case 'Pendiente':
          paymentStatus.value = 'pending'
          break
        case '4': // Fallida
        case 'Fallida':
          paymentStatus.value = 'rejected'
          transactionMessage.value = params.x_response || 'Transacción fallida'
          break
        default:
          // Si no hay estado, asumir éxito (para pruebas)
          paymentStatus.value = 'approved'
      }
      
      // Limpiar carrito en caso de éxito
      if (paymentStatus.value === 'approved') {
        localStorage.removeItem('kharis_cart_cache')
        localStorage.removeItem('kharis_cart_count')
      }
    }
    
    // Parser específico para respuestas de Wompi
    const parseWompiResponse = async (params) => {
      transactionRef.value = params.ref || params.id || `KH-${Date.now()}`
      let wompiTransactionId = params.id || ''
      
      // Si Wompi redirecciona con ID de transacción, consultar estado
      if (params.id) {
        try {
          // Consultar estado de la transacción en Wompi
          const response = await fetch(`https://sandbox.wompi.co/v1/transactions/${params.id}`)
          const data = await response.json()
          
          if (data.data) {
            const transaction = data.data
            transactionRef.value = transaction.reference || params.ref || transactionRef.value
            transactionAmount.value = (transaction.amount_in_cents || 0) / 100
            wompiTransactionId = transaction.id || params.id
            
            switch (transaction.status) {
              case 'APPROVED':
                paymentStatus.value = 'approved'
                // Crear la orden en nuestro sistema
                console.log('✅ Pago aprobado, creando orden en el sistema...')
                await createOrderFromPendingData(wompiTransactionId)
                break
              case 'PENDING':
                paymentStatus.value = 'pending'
                break
              case 'DECLINED':
              case 'VOIDED':
              case 'ERROR':
                paymentStatus.value = 'rejected'
                transactionMessage.value = transaction.status_message || 'Transacción rechazada'
                break
              default:
                paymentStatus.value = 'pending'
            }
          }
        } catch (e) {
          console.warn('Error consultando transacción Wompi:', e)
          // En caso de error, usar los parámetros de la URL
          paymentStatus.value = params.status === 'approved' ? 'approved' : 'pending'
          if (paymentStatus.value === 'approved') {
            await createOrderFromPendingData(wompiTransactionId)
          }
        }
      } else {
        // Sin ID de transacción, usar status de la URL
        paymentStatus.value = 'approved'
        await createOrderFromPendingData(wompiTransactionId)
      }
      
      // Limpiar carrito solo si la orden se creó exitosamente
      // (ya se limpia en createOrderFromPendingData si es exitoso)
    }
    
    onMounted(() => {
      // Si viene con param "r" (return), es un rebote desde producción → localhost
      // Redirigir al origen local con todos los params de Wompi
      const returnParam = route.query.r
      if (returnParam) {
        try {
          const returnUrl = atob(returnParam)
          // Copiar todos los params excepto "r"
          const params = new URLSearchParams(route.query)
          params.delete('r')
          const separator = returnUrl.includes('?') ? '&' : '?'
          const fullUrl = params.toString() 
            ? `${returnUrl}${separator}${params.toString()}`
            : returnUrl
          console.log('🔄 Rebotando a origen local:', fullUrl)
          window.location.href = fullUrl
          return
        } catch (e) {
          console.warn('Error decodificando return URL:', e)
        }
      }
      
      // Parsear respuesta de ePayco/Wompi (async)
      const processPaymentResponse = async () => {
        // Pequeño delay para mejor UX
        await new Promise(resolve => setTimeout(resolve, 1000))
        await parseEpaycoResponse()
        loading.value = false
      }
      
      processPaymentResponse()
    })
    
    return {
      loading,
      paymentStatus,
      transactionRef,
      transactionAmount,
      transactionMessage,
      orderCode,
      orderError,
      whatsappLink,
      formatPrice,
      getConfettiStyle
    }
  }
}
</script>

<style scoped>
@keyframes bounce-once {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.animate-bounce-once {
  animation: bounce-once 0.5s ease-out;
}

.confetti-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.confetti {
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: fall 4s linear forwards;
}

@keyframes fall {
  0% {
    top: -10%;
    opacity: 1;
    transform: rotate(0deg) scale(1);
  }
  100% {
    top: 100%;
    opacity: 0;
    transform: rotate(720deg) scale(0.5);
  }
}
</style>
