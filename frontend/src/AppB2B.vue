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

    <!-- Contenido principal B2B -->
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'AppB2B',
  setup() {
    const showPreloader = ref(true)

    onMounted(() => {
      // Preloader más rápido para B2B (usuarios recurrentes)
      setTimeout(() => {
        showPreloader.value = false
      }, 800)
    })

    return {
      showPreloader
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
</style>
