<template>
  <div class="min-h-[70vh]">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="font-luxury text-3xl text-gray-900 mb-2">Centro de Ayuda</h1>
      <p class="text-gray-500">¿Cómo podemos ayudarte hoy?</p>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
      <a 
        href="https://wa.me/4796657763?text=Hola,%20necesito%20ayuda%20con%20mi%20pedido" 
        target="_blank"
        class="flex items-center gap-4 p-5 bg-white rounded-xl border border-gray-100 hover:border-emerald-200 hover:shadow-lg transition-all group"
      >
        <div class="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center group-hover:bg-emerald-100 transition-colors">
          <svg class="w-6 h-6 text-emerald-500" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/></svg>
        </div>
        <div>
          <h3 class="font-semibold text-gray-900">WhatsApp Directo</h3>
          <p class="text-sm text-gray-500">Respuesta inmediata</p>
        </div>
      </a>

      <a 
        href="mailto:soporte@kharisdistribuidora.com"
        class="flex items-center gap-4 p-5 bg-white rounded-xl border border-gray-100 hover:border-[#C9A962]/30 hover:shadow-lg transition-all group"
      >
        <div class="w-12 h-12 rounded-xl bg-[#C9A962]/10 flex items-center justify-center group-hover:bg-[#C9A962]/20 transition-colors">
          <svg class="w-6 h-6 text-[#C9A962]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
        </div>
        <div>
          <h3 class="font-semibold text-gray-900">Correo Electrónico</h3>
          <p class="text-sm text-gray-500">soporte@kharisdistribuidora.com</p>
        </div>
      </a>

      <a 
        href="tel:+4796657763"
        class="flex items-center gap-4 p-5 bg-white rounded-xl border border-gray-100 hover:border-blue-200 hover:shadow-lg transition-all group"
      >
        <div class="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center group-hover:bg-blue-100 transition-colors">
          <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
        </div>
        <div>
          <h3 class="font-semibold text-gray-900">Línea Directa</h3>
          <p class="text-sm text-gray-500">+57 300 123 4567</p>
        </div>
      </a>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- FAQs -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-2xl border border-gray-100 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100">
            <h2 class="text-lg font-bold text-gray-900">Preguntas Frecuentes</h2>
          </div>
          <div class="divide-y divide-gray-100">
            <div v-for="(faq, index) in faqs" :key="index" class="px-6">
              <button 
                @click="toggleFaq(index)"
                class="w-full flex items-center justify-between py-4 text-left"
              >
                <span class="font-medium text-gray-900 pr-4">{{ faq.question }}</span>
                <svg 
                  class="w-5 h-5 text-gray-400 flex-shrink-0 transition-transform" 
                  :class="{ 'rotate-180': openFaq === index }"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div 
                v-show="openFaq === index" 
                class="pb-4 text-gray-600 text-sm leading-relaxed"
              >
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- PQR Form -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-2xl border border-gray-100 overflow-hidden sticky top-24">
          <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-[#C9A962]/5 to-transparent">
            <h2 class="text-lg font-bold text-gray-900">Radicar PQR</h2>
            <p class="text-sm text-gray-500 mt-1">Peticiones, Quejas y Reclamos</p>
          </div>
          <form @submit.prevent="submitPqr" class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Tipo de solicitud</label>
              <select 
                v-model="pqrForm.tipo"
                class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962] outline-none transition-all"
              >
                <option value="">Seleccionar...</option>
                <option value="peticion">Petición</option>
                <option value="queja">Queja</option>
                <option value="reclamo">Reclamo</option>
                <option value="sugerencia">Sugerencia</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Asunto</label>
              <input 
                v-model="pqrForm.asunto"
                type="text"
                placeholder="Describe brevemente tu solicitud"
                class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962] outline-none transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Descripción</label>
              <textarea 
                v-model="pqrForm.descripcion"
                rows="4"
                placeholder="Cuéntanos los detalles de tu solicitud..."
                class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962] outline-none transition-all resize-none"
              ></textarea>
            </div>
            <button 
              type="submit"
              :disabled="!isFormValid || submitting"
              class="w-full py-3 bg-[#0F0F0F] text-white font-medium rounded-lg hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <span v-if="submitting">Enviando...</span>
              <span v-else>Enviar Solicitud</span>
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <Teleport to="body">
      <transition name="modal">
        <div v-if="showSuccessModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/50" @click="showSuccessModal = false"></div>
          <div class="relative bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6 text-center">
            <div class="w-16 h-16 mx-auto mb-4 bg-emerald-100 rounded-full flex items-center justify-center">
              <svg class="w-8 h-8 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Solicitud Enviada</h3>
            <p class="text-gray-500 mb-6">Te contactaremos pronto. Tu número de radicado es: <strong class="text-[#C9A962]">{{ ticketNumber }}</strong></p>
            <button 
              @click="showSuccessModal = false"
              class="px-6 py-2.5 bg-[#0F0F0F] text-white font-medium rounded-lg hover:bg-black transition-colors"
            >
              Entendido
            </button>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'B2BAyuda',
  setup() {
    const openFaq = ref(null)
    const showSuccessModal = ref(false)
    const submitting = ref(false)
    const ticketNumber = ref('')

    const pqrForm = ref({
      tipo: '',
      asunto: '',
      descripcion: ''
    })

    const faqs = [
      {
        question: '¿Cuáles son los requisitos para ser mayorista?',
        answer: 'Para acceder a precios de mayorista necesitas: RUT activo, cámara de comercio o documento equivalente, y un mínimo de compra inicial. Nuestro equipo evaluará tu solicitud en 24-48 horas hábiles.'
      },
      {
        question: '¿Cuánto demora el envío de mi pedido?',
        answer: 'Los envíos dentro de Bogotá se realizan en 24-48 horas hábiles. Para ciudades principales 2-3 días hábiles, y resto del país 3-5 días hábiles. Recibirás un número de guía para rastrear tu pedido.'
      },
      {
        question: '¿Puedo devolver un producto?',
        answer: 'Sí, aceptamos devoluciones dentro de los primeros 7 días después de recibir el producto, siempre que esté en su empaque original sin abrir. Los productos abiertos no tienen devolución por motivos de higiene.'
      },
      {
        question: '¿Cómo funcionan los niveles de mayorista?',
        answer: 'Tenemos 3 niveles: Bronce (compras hasta $2M), Plata ($2M-$5M) y Gold (más de $5M). Cada nivel tiene descuentos progresivos y beneficios exclusivos como envío gratis y atención prioritaria.'
      },
      {
        question: '¿Puedo pagar contra entrega?',
        answer: 'Actualmente trabajamos con pago anticipado (transferencia o tarjeta) para pedidos nuevos. Después de 3 pedidos exitosos, puedes acceder a línea de crédito según tu historial.'
      },
      {
        question: '¿Tienen catálogo físico?',
        answer: 'Nuestro catálogo es 100% digital y se actualiza en tiempo real. Puedes descargar PDFs desde la sección de catálogo o solicitar material de apoyo para tu tienda contactando a tu asesor.'
      }
    ]

    const isFormValid = computed(() => {
      return pqrForm.value.tipo && pqrForm.value.asunto && pqrForm.value.descripcion
    })

    function toggleFaq(index) {
      openFaq.value = openFaq.value === index ? null : index
    }

    async function submitPqr() {
      if (!isFormValid.value) return
      
      submitting.value = true
      
      // Simular envío
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Generar número de ticket
      ticketNumber.value = 'PQR-' + Date.now().toString().slice(-8)
      
      // Reset form
      pqrForm.value = { tipo: '', asunto: '', descripcion: '' }
      submitting.value = false
      showSuccessModal.value = true
    }

    return {
      openFaq,
      faqs,
      pqrForm,
      isFormValid,
      submitting,
      showSuccessModal,
      ticketNumber,
      toggleFaq,
      submitPqr
    }
  }
}
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
