<template>
  <div class="min-h-screen bg-[#FAFAFA] flex items-center justify-center">
    <div class="text-center max-w-md mx-auto px-6">
      
      <!-- Loader minimal: línea animada -->
      <div class="w-16 h-16 mx-auto mb-8 relative">
        <div class="absolute inset-0 border-2 border-gray-200 rounded-full"></div>
        <div class="absolute inset-0 border-2 border-gray-900 rounded-full border-t-transparent animate-spin" style="animation-duration: 1.2s;"></div>
      </div>

      <!-- Título claro -->
      <h1 class="text-xl font-semibold text-gray-900 mb-2">
        Preparando tu pedido
      </h1>

      <!-- Subtexto -->
      <p class="text-gray-500 text-sm mb-6">
        Estamos validando precios y disponibilidad mayorista
      </p>

      <!-- Línea de progreso discreta -->
      <div class="w-48 mx-auto h-0.5 bg-gray-200 rounded-full overflow-hidden mb-8">
        <div class="h-full bg-gray-400 rounded-full animate-progress"></div>
      </div>

      <!-- Refuerzo de confianza -->
      <p class="text-xs text-gray-400">
        No cierres esta ventana
      </p>
    </div>
  </div>
</template>

<script>
import { onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'B2BCheckoutPending',
  setup() {
    const router = useRouter()
    const route = useRoute()
    let redirectTimeout = null

    onMounted(() => {
      // Validar que hay items en el carrito
      const cart = localStorage.getItem('b2b_cart')
      let hasItems = false
      
      if (cart) {
        try {
          const data = JSON.parse(cart)
          hasItems = data.items && data.items.length > 0
        } catch {
          hasItems = false
        }
      }

      // Si no hay items, volver al carrito
      if (!hasItems) {
        router.replace('/portal/carrito')
        return
      }

      // Duración ideal: 1.5-2 segundos
      // Suficiente para transmitir procesamiento
      // No tanto como para generar ansiedad
      redirectTimeout = setTimeout(() => {
        router.replace('/portal/checkout/confirmar')
      }, 1800)
    })

    onUnmounted(() => {
      if (redirectTimeout) {
        clearTimeout(redirectTimeout)
      }
    })

    return {}
  }
}
</script>

<style scoped>
@keyframes progress {
  0% {
    width: 0%;
    margin-left: 0;
  }
  50% {
    width: 60%;
    margin-left: 20%;
  }
  100% {
    width: 0%;
    margin-left: 100%;
  }
}

.animate-progress {
  animation: progress 1.5s ease-in-out infinite;
}
</style>
