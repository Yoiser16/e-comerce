<template>
  <div class="min-h-screen bg-[#FAFAFA] flex flex-col">

    <!-- Header minimal -->
    <header class="bg-white border-b border-gray-100 py-4">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <router-link to="/portal" class="flex items-center gap-2.5 w-fit">
          <div class="w-9 h-9 rounded-full bg-gradient-to-br from-gray-900 to-gray-700 flex items-center justify-center">
            <span class="text-white font-semibold text-sm">K</span>
          </div>
          <span class="font-semibold text-lg text-gray-900 tracking-wide">Kharis <span class="text-xs font-normal text-gray-400 ml-1">PRO</span></span>
        </router-link>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 flex items-center justify-center px-4 py-10">
      <div class="max-w-lg w-full">

        <!-- Card -->
        <div class="bg-white rounded-2xl p-7 sm:p-9 shadow-sm border border-gray-100 text-center">

          <!-- Loading State -->
          <div v-if="loading" class="py-8">
            <div class="w-14 h-14 mx-auto mb-5 relative">
              <div class="absolute inset-0 border-2 border-gray-200 rounded-full"></div>
              <div class="absolute inset-0 border-2 border-gray-900 rounded-full border-t-transparent animate-spin" style="animation-duration: 1.2s;"></div>
            </div>
            <p class="text-gray-600 font-medium">Verificando tu pago...</p>
            <p class="text-sm text-gray-400 mt-1">Consultando estado de la transacción</p>
          </div>

          <!-- APPROVED -->
          <template v-else-if="paymentStatus === 'approved'">
            <div class="w-18 h-18 mx-auto mb-5 rounded-full bg-green-100 flex items-center justify-center" style="width: 72px; height: 72px;">
              <svg class="w-9 h-9 text-green-600" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </div>

            <h1 class="text-2xl font-bold text-gray-900 mb-2">¡Pago Exitoso!</h1>
            <p class="text-gray-500 mb-6">Tu pedido ha sido confirmado y está siendo procesado</p>

            <!-- Transaction Details -->
            <div class="bg-green-50 rounded-xl p-5 mb-6 text-left border border-green-100">
              <div class="flex items-center gap-2 mb-3">
                <svg class="w-4.5 h-4.5 text-green-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25z" />
                </svg>
                <span class="font-semibold text-green-800 text-sm">Detalles del pago</span>
              </div>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-green-700">Referencia:</span>
                  <span class="font-mono font-semibold text-green-900">{{ transactionRef }}</span>
                </div>
                <div v-if="transactionId" class="flex justify-between">
                  <span class="text-green-700">ID Transacción:</span>
                  <span class="font-mono text-green-900 text-xs">{{ transactionId }}</span>
                </div>
                <div v-if="transactionAmount" class="flex justify-between">
                  <span class="text-green-700">Monto:</span>
                  <span class="font-semibold text-green-900">${{ formatPrice(transactionAmount) }} COP</span>
                </div>
                <div v-if="paymentMethod" class="flex justify-between">
                  <span class="text-green-700">Método:</span>
                  <span class="text-green-900">{{ paymentMethod }}</span>
                </div>
                <div v-if="ordenCodigo" class="flex justify-between">
                  <span class="text-green-700">Pedido:</span>
                  <span class="font-semibold text-green-900">{{ ordenCodigo }}</span>
                </div>
              </div>
            </div>

            <div class="bg-blue-50 rounded-lg p-3.5 mb-6 text-left">
              <p class="text-sm text-blue-700">
                <span class="font-semibold">📧 Próximo paso:</span> Recibirás un correo y notificación con el seguimiento de tu pedido mayorista.
              </p>
            </div>
          </template>

          <!-- PENDING -->
          <template v-else-if="paymentStatus === 'pending'">
            <div class="w-18 h-18 mx-auto mb-5 rounded-full bg-amber-100 flex items-center justify-center" style="width: 72px; height: 72px;">
              <svg class="w-9 h-9 text-amber-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <h1 class="text-2xl font-bold text-gray-900 mb-2">Pago Pendiente</h1>
            <p class="text-gray-500 mb-6">Tu pago está siendo procesado. Te notificaremos cuando se confirme.</p>

            <div class="bg-amber-50 rounded-xl p-4 mb-6 text-left border border-amber-200">
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-amber-700">Referencia:</span>
                  <span class="font-mono font-semibold text-amber-900">{{ transactionRef }}</span>
                </div>
                <div v-if="transactionAmount" class="flex justify-between">
                  <span class="text-amber-700">Monto:</span>
                  <span class="font-semibold text-amber-900">${{ formatPrice(transactionAmount) }} COP</span>
                </div>
              </div>
              <p class="text-xs text-amber-600 mt-3">
                ⏳ El pago puede tardar hasta 24 horas en confirmarse según el método seleccionado.
              </p>
            </div>
          </template>

          <!-- REJECTED -->
          <template v-else-if="paymentStatus === 'rejected'">
            <div class="w-18 h-18 mx-auto mb-5 rounded-full bg-red-100 flex items-center justify-center" style="width: 72px; height: 72px;">
              <svg class="w-9 h-9 text-red-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>

            <h1 class="text-2xl font-bold text-gray-900 mb-2">Pago Rechazado</h1>
            <p class="text-gray-500 mb-6">No se pudo procesar tu pago. No se realizó ningún cobro.</p>

            <div class="bg-red-50 rounded-xl p-4 mb-6 text-left border border-red-200">
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-red-700">Referencia:</span>
                  <span class="font-mono font-semibold text-red-900">{{ transactionRef }}</span>
                </div>
                <div v-if="statusMessage" class="mt-2">
                  <span class="text-red-700">Motivo:</span>
                  <span class="text-red-800 ml-1">{{ statusMessage }}</span>
                </div>
              </div>
            </div>

            <button 
              @click="retryPayment"
              class="w-full px-6 py-3 bg-gray-900 hover:bg-black text-white font-medium rounded-lg transition-colors mb-3"
            >
              Intentar nuevamente
            </button>
          </template>

          <!-- ERROR / UNKNOWN -->
          <template v-else>
            <div class="w-18 h-18 mx-auto mb-5 rounded-full bg-gray-100 flex items-center justify-center" style="width: 72px; height: 72px;">
              <svg class="w-9 h-9 text-gray-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
              </svg>
            </div>

            <h1 class="text-2xl font-bold text-gray-900 mb-2">Estado Desconocido</h1>
            <p class="text-gray-500 mb-6">No pudimos verificar el estado de tu pago. Contacta a soporte si el problema persiste.</p>
          </template>

          <!-- Actions -->
          <div class="flex flex-col sm:flex-row gap-3 mt-2" v-if="!loading">
            <router-link 
              to="/portal/cuenta?tab=pedidos" 
              class="flex-1 px-5 py-3 bg-gray-900 hover:bg-black text-white font-medium rounded-lg transition-colors text-center text-sm"
            >
              Ver mis pedidos
            </router-link>
            <router-link 
              to="/portal/catalogo" 
              class="flex-1 px-5 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors text-center text-sm"
            >
              Seguir comprando
            </router-link>
          </div>
        </div>

        <!-- Security badge -->
        <div class="flex items-center justify-center gap-2 mt-6 text-gray-400">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
          </svg>
          <span class="text-xs">Pago seguro procesado por Wompi</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTransactionStatus, mapTransactionStatus, fromCents } from '@/services/wompi'
import { crearOrden } from '@/services/mayoristas'

export default {
  name: 'B2BPagoResultado',
  setup() {
    const route = useRoute()
    const router = useRouter()

    const loading = ref(true)
    const paymentStatus = ref(null) // approved | pending | rejected | null
    const transactionRef = ref('')
    const transactionId = ref('')
    const transactionAmount = ref(null)
    const paymentMethod = ref('')
    const statusMessage = ref('')
    const ordenCodigo = ref('')

    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

    function retryPayment() {
      router.push('/portal/checkout/confirmar')
    }

    async function processTransaction(txId) {
      try {
        const tx = await getTransactionStatus(txId)
        
        if (!tx) {
          paymentStatus.value = null
          return
        }

        const mapped = mapTransactionStatus(tx.status)
        paymentStatus.value = mapped.status
        transactionRef.value = tx.reference || ''
        transactionId.value = tx.id || ''
        transactionAmount.value = tx.amount_in_cents ? fromCents(tx.amount_in_cents) : null
        paymentMethod.value = tx.payment_method_type || ''
        statusMessage.value = tx.status_message || ''

        // Si el pago fue aprobado, crear la orden en el backend
        if (mapped.status === 'approved') {
          await createOrderFromPayment(tx)
        }

      } catch (error) {
        console.error('Error verificando transacción:', error)
        paymentStatus.value = null
      }
    }

    async function createOrderFromPayment(tx) {
      try {
        // Recuperar datos del pedido guardados antes de redirigir a Wompi
        const pendingOrderStr = localStorage.getItem('b2b_pending_order')
        if (!pendingOrderStr) {
          console.warn('No se encontró orden pendiente en localStorage')
          return
        }

        const pendingOrder = JSON.parse(pendingOrderStr)

        const ordenData = {
          email: pendingOrder.customer.email,
          nombre: pendingOrder.customer.nombre,
          apellido: pendingOrder.customer.apellido || '',
          telefono: pendingOrder.customer.telefono,
          tipo_documento: pendingOrder.customer.tipo_documento || 'CC',
          numero_documento: pendingOrder.customer.numero_documento || '',
          direccion: pendingOrder.customer.direccion,
          departamento: pendingOrder.customer.departamento,
          municipio: pendingOrder.customer.municipio,
          barrio: pendingOrder.customer.barrio || '',
          notas: pendingOrder.customer.notas || `Pago Wompi - Ref: ${tx.reference} - ID: ${tx.id}`,
          items: pendingOrder.items.map(item => ({
            producto_id: item.id || item.producto_id,
            cantidad: item.cantidad || item.quantity,
            precio_unitario: item.precio || item.wholesalePrice || item.precio_unitario,
            nombre: item.nombre || item.name
          })),
          subtotal: pendingOrder.subtotal,
          envio: pendingOrder.envio,
          total: pendingOrder.total,
          metodo_pago: 'wompi'
        }

        const result = await crearOrden(ordenData)
        ordenCodigo.value = result.codigo || ''

        // Limpiar datos temporales
        localStorage.removeItem('b2b_pending_order')
        localStorage.removeItem('b2b_cart')

        console.log('✅ Orden B2B creada después de pago Wompi:', result.codigo)

      } catch (error) {
        console.error('Error creando orden después del pago:', error)
        // El pago se realizó pero hubo error creando la orden
        // El admin puede verificarlo por la referencia de Wompi
        statusMessage.value = 'Pago procesado. Si no ves tu pedido, contacta a soporte con la referencia.'
      }
    }

    onMounted(async () => {
      // Wompi redirige con el ID de la transacción como query param
      const txId = route.query.id
      const envState = route.query.env // sandbox or production

      if (txId) {
        await processTransaction(txId)
      } else {
        // Si no hay ID, intentar verificar con referencia guardada
        const pendingOrderStr = localStorage.getItem('b2b_pending_order')
        if (pendingOrderStr) {
          try {
            const pendingOrder = JSON.parse(pendingOrderStr)
            transactionRef.value = pendingOrder.reference || 'Sin referencia'
          } catch {
            // noop
          }
        }
        paymentStatus.value = null
      }

      loading.value = false
    })

    return {
      loading,
      paymentStatus,
      transactionRef,
      transactionId,
      transactionAmount,
      paymentMethod,
      statusMessage,
      ordenCodigo,
      formatPrice,
      retryPayment
    }
  }
}
</script>
