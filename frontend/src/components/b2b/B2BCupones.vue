<template>
  <div class="flex min-h-[calc(100vh-106px)]">

    <!-- ==================== SIDEBAR FIXED LEFT (like B2BCuenta) ==================== -->
    <aside class="hidden lg:block w-[240px] flex-shrink-0 border-r border-[#e0e0e0] bg-white">
      <div class="sticky top-[106px] py-6 px-5">
        <h2 class="text-[15px] font-bold text-[#333] mb-5">Mi cuenta</h2>
        <nav class="space-y-0.5">
          <button 
            v-for="tab in accountTabs" 
            :key="tab.id"
            @click="router.push(tab.route)"
            :class="[
              'w-full flex items-center gap-2.5 px-3 py-2 text-left transition-colors text-[14px] rounded-md',
              'text-[#555] hover:bg-[#f5f5f5] hover:text-[#333] font-normal'
            ]"
          >
            <span v-html="tab.icon" class="w-[18px] h-[18px] text-[#999]"></span>
            {{ tab.label }}
          </button>

          <!-- Separator -->
          <div class="!my-3 border-t border-[#e8e8e8]"></div>

          <!-- Links con Cupones activo -->
          <button 
            @click="router.push('/portal/pedidos')"
            class="w-full flex items-center gap-2.5 px-3 py-2 text-left transition-colors text-[14px] rounded-md text-[#555] hover:bg-[#f5f5f5] hover:text-[#333] font-normal"
          >
            <span class="w-[18px] h-[18px] text-[#999]">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>
            </span>
            Mis Pedidos
          </button>
          <!-- Cupones - ACTIVO -->
          <button 
            class="w-full flex items-center gap-2.5 px-3 py-2 text-left transition-colors text-[14px] rounded-md text-[#2563eb] font-semibold bg-[#eff4ff]"
          >
            <span class="w-[18px] h-[18px] text-[#2563eb]">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
            </span>
            Cupones
          </button>
        </nav>
      </div>
    </aside>

    <!-- ==================== MAIN CONTENT AREA ==================== -->
    <div class="flex-1 min-w-0">
      <div class="max-w-[960px] mx-auto px-5 sm:px-8 py-6 lg:py-8">

        <!-- Avatar + Name Header -->
        <div class="flex items-center gap-4 mb-6">
          <div class="w-14 h-14 rounded-full bg-[#e8e8e8] flex items-center justify-center flex-shrink-0 border-2 border-[#d0d0d0]">
            <span class="text-[#666] text-lg font-bold">{{ userInitials }}</span>
          </div>
          <div>
            <h1 class="text-xl font-bold text-[#333]">{{ user.nombre }}</h1>
            <p class="text-[14px] text-[#666]">{{ user.email }}</p>
          </div>
        </div>

        <!-- Mobile Navigation -->
        <div class="lg:hidden mb-5">
          <div class="bg-white rounded-lg border border-[#e0e0e0] p-4" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="flex flex-wrap gap-2">
              <button 
                @click="router.push('/portal/cuenta')"
                class="px-3 py-1.5 rounded-full text-[12px] font-medium transition-colors bg-[#f0f0f0] text-[#555] hover:bg-[#e5e5e5]"
              >
                Perfil
              </button>
              <button 
                @click="router.push('/portal/pedidos')"
                class="px-3 py-1.5 rounded-full text-[12px] font-medium transition-colors bg-[#f0f0f0] text-[#555] hover:bg-[#e5e5e5]"
              >
                Mis Pedidos
              </button>
              <button 
                class="px-3 py-1.5 rounded-full text-[12px] font-medium transition-colors bg-[#2563eb] text-white"
              >
                Cupones
              </button>
            </div>
          </div>
        </div>

        <!-- Page Title -->
        <div class="mb-6">
          <h2 class="text-[22px] font-bold text-[#333]">Cupones y Descuentos</h2>
          <p class="text-[14px] text-[#666] mt-1">Canjea tus cupones exclusivos y obtén beneficios especiales</p>
        </div>

        <!-- Canjear Cupón Card -->
        <div class="bg-white rounded-lg border border-[#e0e0e0] p-5 mb-6" style="box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);">
          <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <div class="w-10 h-10 rounded-full bg-[#eff4ff] flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-[#2563eb]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
              </div>
              <div>
                <h3 class="text-[15px] font-semibold text-[#333]">¿Tienes un código de cupón?</h3>
                <p class="text-[13px] text-[#666]">Ingresa tu código para aplicar el descuento</p>
              </div>
            </div>
            <div class="flex items-center gap-2 w-full sm:w-auto">
              <input 
                v-model="cuponCode" 
                type="text" 
                placeholder="CÓDIGO"
                class="flex-1 sm:w-36 h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white uppercase"
                @keydown.enter="aplicarCupon"
              />
              <button 
                @click="aplicarCupon"
                :disabled="!cuponCode || aplicandoCupon"
                class="h-[38px] px-4 text-[13px] font-semibold text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                {{ aplicandoCupon ? 'Validando...' : 'Aplicar' }}
              </button>
            </div>
          </div>
          <!-- Feedback -->
          <transition name="fade">
            <div v-if="cuponFeedback" :class="['mt-4 p-3 rounded-md text-[13px]', cuponFeedback.success ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200']">
              {{ cuponFeedback.message }}
            </div>
          </transition>
        </div>

        <!-- Mis Cupones Disponibles -->
        <div class="bg-white rounded-lg border border-[#e0e0e0] overflow-hidden mb-6" style="box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);">
          <div class="px-5 py-4 border-b border-[#e8e8e8] flex items-center justify-between">
            <h3 class="text-[15px] font-bold text-[#333]">Mis Cupones Disponibles</h3>
            <span class="text-[13px] text-[#666]">{{ cuponesActivos.length }} cupones activos</span>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="py-12 text-center">
            <svg class="w-6 h-6 text-[#2563eb] mx-auto mb-2 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <p class="text-[13px] text-[#666]">Cargando cupones...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="cuponesActivos.length === 0" class="py-12 text-center px-5">
            <div class="w-14 h-14 mx-auto mb-4 bg-[#f5f5f5] rounded-full flex items-center justify-center">
              <svg class="w-7 h-7 text-[#999]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </div>
            <h4 class="text-[15px] font-semibold text-[#333] mb-1">No tienes cupones activos</h4>
            <p class="text-[13px] text-[#666] mb-4">Los cupones se asignan según tu nivel de mayorista</p>
            <router-link 
              to="/portal/catalogo"
              class="inline-flex items-center gap-1.5 text-[13px] text-[#2563eb] hover:text-[#1d4ed8] font-medium transition-colors"
            >
              Explorar catálogo
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            </router-link>
          </div>

          <!-- Cupones Grid -->
          <div v-else class="p-5 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div 
              v-for="cupon in cuponesActivos" 
              :key="cupon.id" 
              class="relative bg-white rounded-lg border border-[#e0e0e0] overflow-hidden hover:border-[#2563eb]/40 hover:shadow-md transition-all"
            >
              <div class="flex">
                <!-- Left Side - Discount Badge -->
                <div class="w-24 flex-shrink-0 bg-gradient-to-br from-[#2563eb] to-[#1d4ed8] text-white p-4 flex flex-col items-center justify-center relative">
                  <span class="text-2xl font-bold">{{ cupon.descuento }}%</span>
                  <span class="text-[10px] uppercase tracking-wide opacity-80">Descuento</span>
                  <!-- Perforated edge -->
                  <div class="absolute right-0 top-0 bottom-0 flex flex-col justify-around">
                    <div class="w-2.5 h-2.5 bg-white rounded-full -mr-1.5"></div>
                    <div class="w-2.5 h-2.5 bg-white rounded-full -mr-1.5"></div>
                    <div class="w-2.5 h-2.5 bg-white rounded-full -mr-1.5"></div>
                  </div>
                </div>
                <!-- Right Side - Info -->
                <div class="flex-1 p-4">
                  <h4 class="text-[14px] font-semibold text-[#333] mb-0.5">{{ cupon.nombre }}</h4>
                  <p class="text-[12px] text-[#666] mb-2">{{ cupon.descripcion }}</p>
                  <div class="flex flex-wrap items-center gap-3 text-[11px] text-[#888] mb-3">
                    <span v-if="cupon.compra_minima" class="flex items-center gap-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      Mínimo ${{ formatPrice(cupon.compra_minima) }}
                    </span>
                    <span class="flex items-center gap-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                      Hasta {{ formatDate(cupon.fecha_expiracion) }}
                    </span>
                  </div>
                  <div class="flex items-center justify-between">
                    <code class="px-2 py-1 bg-[#f5f5f5] rounded text-[12px] font-mono text-[#333]">{{ cupon.codigo }}</code>
                    <button 
                      @click="copiarCodigo(cupon.codigo)"
                      class="text-[12px] text-[#2563eb] hover:text-[#1d4ed8] font-medium flex items-center gap-1 transition-colors"
                    >
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                      Copiar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Beneficios por Nivel -->
        <div class="bg-white rounded-lg border border-[#e0e0e0] overflow-hidden" style="box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);">
          <div class="px-5 py-4 border-b border-[#e8e8e8]">
            <h3 class="text-[15px] font-bold text-[#333]">Beneficios por Nivel</h3>
            <p class="text-[13px] text-[#666] mt-0.5">Mientras más compras, más beneficios obtienes</p>
          </div>
          <div>
            <div 
              v-for="(nivel, index) in niveles" 
              :key="nivel.nombre" 
              :class="['px-5 py-4 flex items-center gap-4', index > 0 ? 'border-t border-[#e8e8e8]' : '']"
            >
              <div :class="['w-11 h-11 rounded-full flex items-center justify-center', nivel.bgColor]">
                <svg class="w-5 h-5" :class="nivel.iconColor" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="text-[14px] font-semibold text-[#333]">{{ nivel.nombre }}</h4>
                <p class="text-[12px] text-[#666]">{{ nivel.requisito }}</p>
              </div>
              <div class="text-right flex-shrink-0">
                <span class="text-xl font-bold" :class="nivel.iconColor">{{ nivel.descuento }}%</span>
                <p class="text-[11px] text-[#888]">descuento base</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Toast Notification -->
    <transition name="toast">
      <div 
        v-if="toast" 
        class="fixed bottom-6 right-6 bg-[#333] text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 z-50"
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'B2BCupones',
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const cuponCode = ref('')
    const aplicandoCupon = ref(false)
    const cuponFeedback = ref(null)
    const toast = ref('')
    const cuponesActivos = ref([])

    // Account tabs (same as B2BCuenta for consistency)
    const accountTabs = [
      { id: 'profile', label: 'Perfil', route: '/portal/cuenta', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>' },
      { id: 'addresses', label: 'Direcciones', route: '/portal/cuenta', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /></svg>' },
      { id: 'security', label: 'Seguridad', route: '/portal/cuenta', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>' },
      { id: 'notifications', label: 'Notificaciones', route: '/portal/cuenta', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>' },
    ]

    const niveles = [
      { nombre: 'Bronce', requisito: 'Compras hasta $2.000.000', descuento: 10, bgColor: 'bg-amber-100', iconColor: 'text-amber-600' },
      { nombre: 'Plata', requisito: 'Compras de $2.000.000 a $5.000.000', descuento: 15, bgColor: 'bg-gray-200', iconColor: 'text-gray-500' },
      { nombre: 'Gold', requisito: 'Compras superiores a $5.000.000', descuento: 20, bgColor: 'bg-amber-50', iconColor: 'text-amber-500' },
    ]

    // User data
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{"nombre": "Usuario", "email": "usuario@example.com"}')
    })

    const userInitials = computed(() => {
      const nombre = user.value.nombre || 'U'
      return nombre.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    })

    // Cupones de ejemplo (en producción vendrían del backend)
    const cuponesMock = [
      { id: 1, codigo: 'BIENVENIDO20', nombre: 'Cupón de Bienvenida', descripcion: 'Para tu primera compra como mayorista', descuento: 20, compra_minima: 500000, fecha_expiracion: '2026-03-30' },
      { id: 2, codigo: 'FEBRERO10', nombre: 'Promo Febrero', descripcion: 'Descuento especial del mes', descuento: 10, compra_minima: 200000, fecha_expiracion: '2026-02-27' },
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
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const codigoUpper = cuponCode.value.toUpperCase()
        const cuponExistente = cuponesMock.find(c => c.codigo === codigoUpper)
        
        if (cuponExistente) {
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
      router,
      loading,
      cuponCode,
      aplicandoCupon,
      cuponFeedback,
      toast,
      cuponesActivos,
      accountTabs,
      niveles,
      user,
      userInitials,
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
