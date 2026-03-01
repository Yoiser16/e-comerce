<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    
    <!-- Header Simple -->
    <header class="bg-white border-b border-gray-100 py-4">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <router-link to="/" class="flex items-center gap-3 w-fit">
          <img 
            src="/logo-kharis.png" 
            alt="Kharis" 
            class="h-10 w-auto object-contain"
          />
          <span class="font-luxury text-xl text-text-dark tracking-wide hidden sm:inline">KHARIS</span>
        </router-link>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="flex-1 flex items-center justify-center px-4 py-8 sm:py-12">
      <div class="max-w-md w-full">
        
        <!-- Estado de carga - Minimalista -->
        <div v-if="loading" class="text-center py-16">
          <div class="w-12 h-12 mx-auto mb-6 border-2 border-gray-200 border-t-[#D81B60] rounded-full animate-spin"></div>
          <p class="text-gray-500 text-sm">Procesando de forma segura...</p>
        </div>
        
        <!-- Contenido cuando ya cargó -->
        <template v-else>
          
          <!-- Pago Exitoso -->
          <template v-if="paymentStatus === 'approved'">
            
            <!-- Icono de éxito - Sutil y elegante -->
            <div class="text-center mb-8">
              <div class="w-16 h-16 mx-auto mb-5 rounded-full bg-emerald-100 flex items-center justify-center">
                <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
              </div>
              <h1 class="font-luxury text-2xl sm:text-3xl text-gray-900 mb-2">¡Pago Exitoso!</h1>
              <p class="text-gray-500 text-sm">Tu pedido ha sido confirmado y está en camino</p>
            </div>
            
            <!-- Tarjeta única con detalles -->
            <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden mb-6">
              
              <!-- Detalles del pedido -->
              <div class="px-5 py-4 border-b border-gray-100">
                <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Detalles del pedido</h3>
                <div class="space-y-3">
                  <div class="flex justify-between items-center" v-if="orderCode">
                    <span class="text-sm text-gray-500">Número de pedido</span>
                    <span class="text-sm font-semibold text-gray-900 font-mono">{{ orderCode }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-500">Referencia Wompi</span>
                    <span class="text-sm font-semibold text-gray-900 font-mono text-right max-w-[180px] truncate">{{ transactionRef }}</span>
                  </div>
                  <div class="flex justify-between items-center" v-if="transactionAmount">
                    <span class="text-sm text-gray-500">Monto</span>
                    <span class="text-sm font-semibold text-gray-900">${{ formatPrice(transactionAmount) }} COP</span>
                  </div>
                </div>
              </div>
              
              <!-- Próximo paso -->
              <div class="px-5 py-4 bg-gray-50">
                <div class="flex gap-3">
                  <div class="w-5 h-5 rounded-full bg-[#D81B60]/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <svg class="w-3 h-3 text-[#D81B60]" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <p class="text-sm text-gray-600">
                    <span class="font-medium text-gray-900">Próximo paso:</span> Recibirás un correo con los detalles de envío y seguimiento de tu pedido.
                  </p>
                </div>
              </div>
            </div>
            
            <!-- Error al crear orden (si existe) -->
            <div v-if="orderError" class="bg-amber-50 rounded-xl p-4 mb-6 border border-amber-200">
              <p class="text-sm text-amber-700">
                <span class="font-semibold">Aviso:</span> {{ orderError }}
              </p>
            </div>
            
          </template>
          
          <!-- Pago Pendiente -->
          <template v-else-if="paymentStatus === 'pending'">
            <div class="text-center mb-8">
              <div class="w-16 h-16 mx-auto mb-5 rounded-full bg-amber-100 flex items-center justify-center">
                <svg class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h1 class="font-luxury text-2xl sm:text-3xl text-gray-900 mb-2">Pago Pendiente</h1>
              <p class="text-gray-500 text-sm">Tu pago está siendo procesado</p>
            </div>
            
            <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 mb-6">
              <div class="flex gap-3">
                <svg class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <p class="text-sm text-gray-600 mb-1">
                    <span class="font-medium text-gray-900">Referencia:</span> {{ transactionRef }}
                  </p>
                  <p class="text-sm text-gray-500">El pago puede tardar hasta 24 horas en confirmarse. Te notificaremos por correo.</p>
                </div>
              </div>
            </div>
          </template>
          
          <!-- Pago Rechazado -->
          <template v-else-if="paymentStatus === 'rejected'">
            <div class="text-center mb-8">
              <div class="w-16 h-16 mx-auto mb-5 rounded-full bg-red-100 flex items-center justify-center">
                <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
              <h1 class="font-luxury text-2xl sm:text-3xl text-gray-900 mb-2">Pago Rechazado</h1>
              <p class="text-gray-500 text-sm">Hubo un problema con tu pago</p>
            </div>
            
            <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 mb-6">
              <div class="flex gap-3">
                <svg class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                </svg>
                <p class="text-sm text-gray-600">
                  <span class="font-medium text-gray-900">Motivo:</span> {{ transactionMessage || 'La transacción fue rechazada por el banco. Por favor intenta de nuevo.' }}
                </p>
              </div>
            </div>
          </template>
          
          <!-- Botones de acción - Jerarquía clara -->
          <div class="space-y-3">
            <!-- Primario: Seguir comprando o Ver mis compras -->
            <router-link 
              to="/" 
              class="w-full h-12 flex items-center justify-center bg-[#D81B60] hover:bg-[#C2185B] text-white font-semibold text-sm rounded-xl transition-colors"
            >
              Seguir Comprando
            </router-link>
            
            <!-- Secundario: Ver mis compras (solo si hay orden) -->
            <router-link 
              v-if="orderCode"
              to="/mi-cuenta?tab=compras" 
              class="w-full h-12 flex items-center justify-center bg-white border border-gray-300 text-gray-700 font-medium text-sm rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-colors"
            >
              Ver mis compras
            </router-link>
            
            <!-- Terciario: Contactar soporte (discreto) -->
            <a 
              :href="whatsappLink"
              target="_blank"
              class="w-full h-11 flex items-center justify-center gap-2 text-gray-500 text-sm hover:text-gray-700 transition-colors"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
              </svg>
              ¿Necesitas ayuda? Contáctanos
            </a>
          </div>
          
        </template>
      </div>
    </main>
    
    <!-- Footer minimalista -->
    <footer class="py-6 bg-white border-t border-gray-100">
      <div class="max-w-7xl mx-auto px-4 text-center">
        <p class="text-xs text-gray-400">© 2026 Kharis Distribuidora. Todos los derechos reservados.</p>
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
      formatPrice
    }
  }
}
</script>

<style scoped>
.font-luxury {
  font-family: 'Playfair Display', serif;
}
</style>
