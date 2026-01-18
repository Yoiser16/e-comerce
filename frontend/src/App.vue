<template>
  <div id="app">
    <!-- Home siempre visible como fondo -->
    <Home />
    
    <!-- Login como overlay modal cuando está en /login -->
    <Login v-if="isLoginRoute" />
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
    
    return {
      isLoginRoute
    }
  }
}
</script>
