<template>
  <div id="app">
    <transition name="fade">
      <div 
        v-if="showPreloader"
        class="fixed inset-0 z-[9999] bg-white flex items-center justify-center px-6"
        aria-label="Cargando Kharis Distribuidora"
      >
        <div class="flex flex-col items-center gap-4 text-center">
          <div class="w-28 h-28 sm:w-32 sm:h-32 rounded-full shadow-soft-lg overflow-hidden bg-white">
            <img 
              src="/logo-kharis.png" 
              alt="Kharis Distribuidora" 
              class="w-full h-full object-contain"
            />
          </div>
          <p class="text-text-dark text-sm sm:text-base tracking-wide">Preparando tu experiencia...</p>
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
  transition: opacity 0.35s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
