<template>
  <div class="min-h-screen flex items-center justify-center" style="background: linear-gradient(145deg, #1A1A1A 0%, #0D0D0D 50%, #1A1A1A 100%);">
    <!-- Destellos decorativos -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-[#E91E63]/5 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/3 right-1/4 w-48 h-48 bg-[#C9A962]/5 rounded-full blur-3xl animate-pulse" style="animation-delay: 0.5s;"></div>
    </div>

    <div class="relative flex flex-col items-center gap-6 text-center px-6">
      <!-- Logo con glow -->
      <div class="relative">
        <div class="absolute inset-0 bg-[#E91E63]/15 rounded-3xl blur-2xl scale-110 animate-pulse"></div>
        <div class="relative w-24 h-24 sm:w-28 sm:h-28 rounded-3xl overflow-hidden shadow-2xl ring-1 ring-white/10">
          <img src="/logo-kharis.jpeg" alt="Kharis" class="w-full h-full object-cover" />
        </div>
      </div>

      <!-- Texto -->
      <div class="flex flex-col items-center gap-1.5">
        <span class="text-white/90 text-lg sm:text-xl font-semibold tracking-[0.2em] uppercase" style="font-family: 'Cormorant Garamond', 'Playfair Display', serif;">KHARIS</span>
        <span class="text-[#C9A962] text-[9px] sm:text-[10px] tracking-[0.35em] uppercase font-medium">PORTAL MAYORISTA</span>
      </div>

      <!-- Barra de carga -->
      <div class="w-24 h-[1.5px] bg-white/10 rounded-full overflow-hidden mt-1">
        <div class="h-full bg-gradient-to-r from-[#E91E63] to-[#C9A962] rounded-full animate-progress"></div>
      </div>

      <p class="text-white/40 text-[11px] sm:text-xs tracking-widest uppercase">Preparando tu pedido</p>

      <p class="text-white/20 text-[10px] tracking-wide mt-2">No cierres esta ventana</p>
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
