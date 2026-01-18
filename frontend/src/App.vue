<template>
  <div id="app">
    <!-- Mostrar Home solo si NO estamos en rutas de admin -->
    <template v-if="!isAdminRoute">
      <Home />
      <!-- Login como overlay modal cuando está en /login -->
      <Login v-if="isLoginRoute" />
    </template>
    
    <!-- Para rutas de admin, usar router-view -->
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
    
    const isLoginRoute = computed(() => route.path === '/login')
    const isAdminRoute = computed(() => route.path.startsWith('/admin'))
    
    return {
      isLoginRoute,
      isAdminRoute
    }
  }
}
</script>
