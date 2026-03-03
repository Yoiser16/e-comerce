<template>
  <div id="app">
    <transition name="fade">
      <div 
        v-if="showPreloader"
        class="fixed inset-0 z-[9999] flex items-center justify-center px-6"
        style="background: linear-gradient(145deg, #1A1A1A 0%, #0D0D0D 50%, #1A1A1A 100%);"
        aria-label="Cargando Kharis Distribuidora"
      >
        <!-- Destellos decorativos sutiles -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none">
          <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-brand-500/5 rounded-full blur-3xl animate-pulse"></div>
          <div class="absolute bottom-1/3 right-1/4 w-48 h-48 bg-[#C9A962]/5 rounded-full blur-3xl animate-pulse" style="animation-delay: 0.5s;"></div>
        </div>

        <div class="relative flex flex-col items-center gap-6 text-center">
          <!-- Logo con glow sutil -->
          <div class="relative">
            <div class="absolute inset-0 bg-brand-500/15 rounded-3xl blur-2xl scale-110 animate-pulse"></div>
            <div class="relative w-28 h-28 sm:w-36 sm:h-36 rounded-3xl overflow-hidden shadow-2xl ring-1 ring-white/10">
              <img 
                src="/logo-kharis.jpeg" 
                alt="Kharis Distribuidora" 
                class="w-full h-full object-cover"
              />
            </div>
          </div>

          <!-- Texto con tipografía luxury -->
          <div class="flex flex-col items-center gap-1.5">
            <span class="text-white/90 text-xl sm:text-2xl font-semibold tracking-[0.2em] uppercase" style="font-family: 'Cormorant Garamond', 'Playfair Display', serif;">KHARIS</span>
            <span class="text-[#C9A962] text-[10px] sm:text-xs tracking-[0.35em] uppercase font-medium">DISTRIBUIDORA</span>
          </div>

          <!-- Línea de carga animada -->
          <div class="w-24 h-[1.5px] bg-white/10 rounded-full overflow-hidden mt-2">
            <div class="h-full bg-gradient-to-r from-brand-500 to-[#C9A962] rounded-full animate-loading-bar"></div>
          </div>

          <p class="text-white/40 text-[11px] sm:text-xs tracking-widest uppercase mt-1">Preparando tu experiencia</p>
        </div>
      </div>
    </transition>

    <!-- Mostrar Home solo si estamos en la ruta raíz -->
    <template v-if="isHomeRoute">
      <Home />
    </template>
    
    <!-- Login como overlay modal cuando está en /login -->
    <template v-else-if="isLoginRoute">
      <Home />
      <Login />
    </template>
    
    <!-- Para todas las demás rutas, usar router-view -->
    <router-view v-else />
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Home from './components/Home.vue'
import Login from './components/Login.vue'

export default {
  name: 'App',
  components: {
    Home,
    Login
  },
  setup() {
    const route = useRoute()
    const showPreloader = ref(true)
    
    const isHomeRoute = computed(() => route.path === '/')
    const isLoginRoute = computed(() => route.path === '/login')

    onMounted(() => {
      // Ocultar el preloader rápido (1.2s) y nunca más de 2s
      const timeout = setTimeout(() => {
        showPreloader.value = false
      }, 1200)

      // Fallback de 2s por seguridad
      setTimeout(() => {
        showPreloader.value = false
        clearTimeout(timeout)
      }, 2000)
    })
    
    return {
      isHomeRoute,
      isLoginRoute,
      showPreloader
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@keyframes loading-bar {
  0% { width: 0; transform: translateX(0); }
  50% { width: 100%; transform: translateX(0); }
  100% { width: 0; transform: translateX(96px); }
}

.animate-loading-bar {
  animation: loading-bar 1.4s ease-in-out infinite;
}
</style>
