<template>
  <div class="min-h-[70vh]">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="font-luxury text-3xl text-gray-900 mb-2">Cupones y Descuentos</h1>
      <p class="text-gray-500">Canjea tus cupones exclusivos y obtén beneficios especiales</p>
    </div>

    <!-- Canjear Cupón -->
    <div class="bg-gradient-to-br from-[#C9A962]/10 to-amber-50 rounded-2xl border border-[#C9A962]/20 p-6 mb-8">
      <div class="flex flex-col md:flex-row items-start md:items-center gap-4">
        <div class="flex-1">
          <h3 class="font-bold text-gray-900 mb-1">¿Tienes un código de cupón?</h3>
          <p class="text-sm text-gray-600">Ingresa tu código para aplicar el descuento en tu próxima compra</p>
        </div>
        <div class="flex items-center gap-2 w-full md:w-auto">
          <input 
            v-model="cuponCode" 
            type="text" 
            placeholder="Ingresa tu código"
            class="flex-1 md:w-48 px-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962] outline-none transition-all uppercase"
            @keydown.enter="aplicarCupon"
          />
          <button 
            @click="aplicarCupon"
            :disabled="!cuponCode || aplicandoCupon"
            class="px-5 py-2.5 bg-[#0F0F0F] text-white font-medium rounded-lg hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
          >
            <span v-if="aplicandoCupon">Validando...</span>
            <span v-else>Aplicar</span>
          </button>
        </div>
      </div>
      <!-- Feedback -->
      <transition name="fade">
        <div v-if="cuponFeedback" :class="['mt-4 p-3 rounded-lg text-sm', cuponFeedback.success ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700']">
          {{ cuponFeedback.message }}
        </div>
      </transition>
    </div>

    <!-- Mis Cupones Activos -->
    <div class="mb-10">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-900">Mis Cupones Disponibles</h2>
        <span class="text-sm text-gray-500">{{ cuponesActivos.length }} cupones activos</span>
      </div>

      <div v-if="loading" class="text-center py-12">
        <svg class="w-8 h-8 text-[#C9A962] animate-spin mx-auto" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-gray-500 mt-2">Cargando cupones...</p>
      </div>

      <div v-else-if="cuponesActivos.length === 0" class="bg-white rounded-2xl border border-gray-100 p-12 text-center">
        <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 14.25l6-6m4.5-3.493V21.75l-3.75-1.5-3.75 1.5-3.75-1.5-3.75 1.5V4.757c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0c1.1.128 1.907 1.077 1.907 2.185z" />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-2">No tienes cupones activos</h3>
        <p class="text-gray-500 mb-4">Los cupones se asignan según tu nivel de mayorista y actividad</p>
        <router-link 
          to="/portal/catalogo"
          class="inline-flex items-center gap-2 text-[#C9A962] hover:text-[#A8893D] font-medium transition-colors"
        >
          Explorar catálogo
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </router-link>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="cupon in cuponesActivos" 
          :key="cupon.id" 
          class="relative bg-white rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg transition-all"
        >
          <!-- Ticket Style -->
          <div class="flex">
            <!-- Left Side - Discount -->
            <div class="w-28 flex-shrink-0 bg-gradient-to-br from-[#C9A962] to-[#A8893D] text-white p-4 flex flex-col items-center justify-center relative">
              <span class="text-3xl font-bold">{{ cupon.descuento }}%</span>
              <span class="text-xs opacity-80">DESCUENTO</span>
              <!-- Perforated edge effect -->
              <div class="absolute right-0 top-0 bottom-0 flex flex-col justify-around">
                <div class="w-3 h-3 bg-white rounded-full -mr-1.5"></div>
                <div class="w-3 h-3 bg-white rounded-full -mr-1.5"></div>
                <div class="w-3 h-3 bg-white rounded-full -mr-1.5"></div>
              </div>
            </div>
            <!-- Right Side - Info -->
            <div class="flex-1 p-4">
              <div class="flex items-start justify-between mb-2">
                <div>
                  <h4 class="font-bold text-gray-900">{{ cupon.nombre }}</h4>
                  <p class="text-sm text-gray-500">{{ cupon.descripcion }}</p>
                </div>
              </div>
              <div class="flex items-center gap-4 text-xs text-gray-500 mb-3">
                <span v-if="cupon.compra_minima" class="flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  Mínimo ${{ formatPrice(cupon.compra_minima) }}
                </span>
                <span class="flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                  Válido hasta {{ formatDate(cupon.fecha_expiracion) }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <code class="px-2 py-1 bg-gray-100 rounded text-sm font-mono text-gray-700">{{ cupon.codigo }}</code>
                <button 
                  @click="copiarCodigo(cupon.codigo)"
                  class="text-sm text-[#C9A962] hover:text-[#A8893D] font-medium flex items-center gap-1 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                  Copiar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cupones por Nivel -->
    <div class="bg-white rounded-2xl border border-gray-100 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-100">
        <h2 class="text-lg font-bold text-gray-900">Beneficios por Nivel</h2>
        <p class="text-sm text-gray-500">Mientras más compras, más beneficios obtienes</p>
      </div>
      <div class="divide-y divide-gray-100">
        <div v-for="nivel in niveles" :key="nivel.nombre" class="px-6 py-4 flex items-center gap-4">
          <div :class="['w-12 h-12 rounded-full flex items-center justify-center', nivel.bgColor]">
            <svg class="w-6 h-6" :class="nivel.iconColor" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
          </div>
          <div class="flex-1">
            <h4 class="font-bold text-gray-900">{{ nivel.nombre }}</h4>
            <p class="text-sm text-gray-500">{{ nivel.requisito }}</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-bold" :class="nivel.iconColor">{{ nivel.descuento }}%</span>
            <p class="text-xs text-gray-500">descuento base</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <transition name="toast">
      <div 
        v-if="toast" 
        class="fixed bottom-6 right-6 bg-gray-900 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 z-50"
      >
        <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        {{ toast }}
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'B2BCupones',
  setup() {
    const loading = ref(true)
    const cuponCode = ref('')
    const aplicandoCupon = ref(false)
    const cuponFeedback = ref(null)
    const toast = ref('')
    const cuponesActivos = ref([])

    const niveles = [
      { nombre: 'Bronce', requisito: 'Compras hasta $2.000.000', descuento: 10, bgColor: 'bg-amber-100', iconColor: 'text-amber-600' },
      { nombre: 'Plata', requisito: 'Compras de $2.000.000 a $5.000.000', descuento: 15, bgColor: 'bg-gray-200', iconColor: 'text-gray-600' },
      { nombre: 'Gold', requisito: 'Compras superiores a $5.000.000', descuento: 20, bgColor: 'bg-[#C9A962]/20', iconColor: 'text-[#C9A962]' },
    ]

    // Cupones de ejemplo (en producción vendrían del backend)
    const cuponesMock = [
      { id: 1, codigo: 'BIENVENIDO20', nombre: 'Cupón de Bienvenida', descripcion: 'Para tu primera compra como mayorista', descuento: 20, compra_minima: 500000, fecha_expiracion: '2026-03-31' },
      { id: 2, codigo: 'FEBRERO10', nombre: 'Promo Febrero', descripcion: 'Descuento especial del mes', descuento: 10, compra_minima: 200000, fecha_expiracion: '2026-02-28' },
    ]

    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

    function formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString('es-CO', { day: 'numeric', month: 'short', year: 'numeric' })
    }

    async function cargarCupones() {
      loading.value = true
      try {
        // TODO: Cargar desde API real
        // const response = await apiClient.get('/b2b/me/cupones')
        // cuponesActivos.value = response.data
        cuponesActivos.value = cuponesMock
      } catch (error) {
        console.error('Error cargando cupones:', error)
      } finally {
        loading.value = false
      }
    }

    async function aplicarCupon() {
      if (!cuponCode.value) return
      
      aplicandoCupon.value = true
      cuponFeedback.value = null

      try {
        // Simular validación
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const codigoUpper = cuponCode.value.toUpperCase()
        const cuponExistente = cuponesMock.find(c => c.codigo === codigoUpper)
        
        if (cuponExistente) {
          // Verificar si ya está en activos
          if (cuponesActivos.value.find(c => c.codigo === codigoUpper)) {
            cuponFeedback.value = { success: false, message: 'Este cupón ya está en tu lista de cupones activos' }
          } else {
            cuponesActivos.value.push(cuponExistente)
            cuponFeedback.value = { success: true, message: `¡Cupón "${cuponExistente.nombre}" agregado exitosamente!` }
            cuponCode.value = ''
          }
        } else {
          cuponFeedback.value = { success: false, message: 'Código de cupón inválido o expirado' }
        }
      } catch (error) {
        cuponFeedback.value = { success: false, message: 'Error al validar el cupón. Intenta de nuevo.' }
      } finally {
        aplicandoCupon.value = false
      }
    }

    function copiarCodigo(codigo) {
      navigator.clipboard.writeText(codigo)
      toast.value = 'Código copiado al portapapeles'
      setTimeout(() => { toast.value = '' }, 2000)
    }

    onMounted(() => {
      cargarCupones()
    })

    return {
      loading,
      cuponCode,
      aplicandoCupon,
      cuponFeedback,
      toast,
      cuponesActivos,
      niveles,
      formatPrice,
      formatDate,
      aplicarCupon,
      copiarCodigo
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-10px); }
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(100px); }
</style>
