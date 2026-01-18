<template>
  <div id="app">
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
import { computed } from 'vue'
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
    
    const isHomeRoute = computed(() => route.path === '/')
    const isLoginRoute = computed(() => route.path === '/login')
    
    return {
      isHomeRoute,
      isLoginRoute
    }
  }
}
</script>
