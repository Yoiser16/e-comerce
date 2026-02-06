<template>
  <div id="app-b2b" class="min-h-screen bg-[#F8F6F3]">
    <!-- Preloader B2B -->
    <transition name="fade">
      <div 
        v-if="showPreloader"
        class="fixed inset-0 z-[9999] bg-[#1A1A1A] flex items-center justify-center px-6"
        aria-label="Cargando Kharis Pro"
      >
        <div class="flex flex-col items-center gap-4 text-center">
          <div class="w-24 h-24 sm:w-28 sm:h-28 rounded-full overflow-hidden bg-white/10 p-4">
            <img 
              src="/logo-kharis.png" 
              alt="Kharis Pro" 
              class="w-full h-full object-contain"
            />
          </div>
          <div class="flex flex-col items-center gap-2">
            <span class="text-[#C9A962] text-xl sm:text-2xl font-luxury tracking-wider">KHARIS PRO</span>
            <p class="text-white/60 text-sm tracking-wide">Portal Mayoristas</p>
          </div>
          <!-- Loading spinner -->
          <div class="mt-4">
            <div class="w-8 h-8 border-2 border-[#C9A962]/30 border-t-[#C9A962] rounded-full animate-spin"></div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Botón Flotante Instalar PWA -->
    <transition name="slide-up">
      <div 
        v-if="installPrompt"
        class="fixed bottom-6 left-6 z-[9000] flex flex-col items-start gap-2"
        role="alert"
      >
        <div class="bg-[#1A1A1A] border border-[#C9A962]/30 rounded-xl shadow-2xl p-4 max-w-sm backdrop-blur-md bg-opacity-95 text-left">
          <div class="flex items-start justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center p-1.5">
                <img src="/logo-kharis.png" alt="Icon" class="w-full h-full object-contain" />
              </div>
              <div>
                <h3 class="text-[#C9A962] font-semibold text-sm">Instalar App Mayorista</h3>
                <p class="text-white/60 text-xs mt-0.5">Acceso rápido desde tu inicio</p>
              </div>
            </div>
            <button 
              @click="installPrompt = null" 
              class="text-white/40 hover:text-white transition-colors"
              aria-label="Cerrar"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <button 
            @click="installApp"
            class="mt-3 w-full py-2 bg-[#C9A962] hover:bg-[#D4AF6A] text-[#1A1A1A] text-sm font-semibold rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Instalar
          </button>
        </div>
      </div>
    </transition>

    <!-- Contenido principal B2B -->
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'AppB2B',
  setup() {
    const showPreloader = ref(true)
    const installPrompt = ref(null)

    function handleInstallPrompt(e) {
      // Prevenir el banner nativo de Chrome
      e.preventDefault()
      // Guardar el evento
      installPrompt.value = e
      console.log('📱 PWA Install Prompt capturado')
    }

    async function installApp() {
      if (!installPrompt.value) return
      
      // Mostrar prompt nativo
      installPrompt.value.prompt()
      
      // Esperar elección del usuario
      const { outcome } = await installPrompt.value.userChoice
      console.log(`📱 Usuario eligió: ${outcome}`)
      
      // Limpiar prompt
      installPrompt.value = null
    }

    onMounted(() => {
      // Preloader
      setTimeout(() => {
        showPreloader.value = false
      }, 800)

      // Escuchar evento de instalación
      window.addEventListener('beforeinstallprompt', handleInstallPrompt)
    })

    onUnmounted(() => {
      window.removeEventListener('beforeinstallprompt', handleInstallPrompt)
    })

    return {
      showPreloader,
      installPrompt,
      installApp
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>
