<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    <!-- Header simple con botón atrás -->
    <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-sm border-b border-black/5">
      <div class="max-w-5xl mx-auto px-4 sm:px-8 py-3 sm:py-4 flex items-center gap-4">
        <button @click="$router.back()" class="w-9 h-9 rounded-full flex items-center justify-center hover:bg-nude-100 transition-colors">
          <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
        </button>
        <div>
          <h1 class="font-luxury text-lg sm:text-2xl text-text-dark">Mis <span class="text-brand-600">Favoritos</span></h1>
          <p v-if="favoritos.length > 0" class="text-xs text-text-light">{{ favoritos.length }} producto{{ favoritos.length !== 1 ? 's' : '' }}</p>
        </div>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="flex flex-col items-center gap-4">
        <div class="w-10 h-10 border-3 border-brand-200 border-t-brand-600 rounded-full animate-spin"></div>
        <p class="text-text-light text-sm">Cargando favoritos...</p>
      </div>
    </div>

    <!-- Favoritos Grid -->
    <div v-else-if="favoritos.length > 0" class="max-w-5xl mx-auto px-3 sm:px-8 py-6 sm:py-10">
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-[10px] sm:gap-5 lg:gap-6">
        <div
          v-for="producto in favoritos"
          :key="producto.id"
          @click="irADetalle(producto.id)"
          class="group cursor-pointer"
        >
          <div class="relative bg-white rounded-xl sm:rounded-2xl overflow-hidden shadow-sm mb-2 sm:mb-3">
            <!-- Quitar de favoritos -->
            <button
              @click.stop="quitarFavorito(producto.id)"
              class="absolute top-2 right-2 z-10 w-7 h-7 sm:w-8 sm:h-8 bg-white/90 rounded-full flex items-center justify-center shadow-sm hover:bg-red-50 transition-colors"
            >
              <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-brand-600" fill="currentColor" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
            </button>

            <!-- Imagen -->
            <div class="aspect-[3/4] overflow-hidden bg-nude-100">
              <img
                v-if="getProductImage(producto)"
                :src="getProductImage(producto)"
                :alt="producto.nombre"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                @error="handleImageError"
              >
              <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-nude-100 to-nude-200">
                <svg class="w-12 h-12 text-nude-300" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Info -->
          <div class="px-1">
            <p class="text-[9px] sm:text-xs text-text-light uppercase tracking-wider mb-0 leading-tight">{{ producto.categoria || 'Extensiones' }}</p>
            <h3 class="font-medium text-[13px] leading-[1.3] sm:text-sm text-text-dark mb-1 line-clamp-2">{{ producto.nombre }}</h3>
            <p class="text-[15px] sm:text-base font-bold text-text-dark">${{ formatPrice(producto.precio_monto || producto.precio) }} <span class="text-[9px] sm:text-xs text-text-light font-normal">{{ producto.precio_moneda || 'COP' }}</span></p>
          </div>
        </div>
      </div>
    </div>

    <!-- Estado vacío -->
    <div v-else class="flex flex-col items-center justify-center py-20 px-6 text-center">
      <div class="w-20 h-20 bg-nude-100 rounded-full flex items-center justify-center mb-6">
        <svg class="w-10 h-10 text-nude-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
        </svg>
      </div>
      <h2 class="font-luxury text-xl sm:text-2xl text-text-dark mb-2">Aún no tienes favoritos</h2>
      <p class="text-text-medium text-sm max-w-xs mb-6">Explora nuestro catálogo y toca el corazón en los productos que te gusten</p>
      <router-link 
        to="/catalogo" 
        class="inline-flex items-center gap-2 bg-text-dark hover:bg-black text-white font-medium text-sm px-6 py-3 rounded-full transition-all"
      >
        Explorar catálogo
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
        </svg>
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { productosService } from '../services/productos'
import { getImageUrl } from '../services/api'

export default {
  name: 'Favoritos',
  setup() {
    const router = useRouter()
    const favoritos = ref([])
    const loading = ref(true)

    const loadWishlistIds = () => {
      try {
        const saved = localStorage.getItem('kharis_wishlist')
        return saved ? JSON.parse(saved) : []
      } catch {
        return []
      }
    }

    const saveWishlistIds = (ids) => {
      localStorage.setItem('kharis_wishlist', JSON.stringify(ids))
    }

    const cargarFavoritos = async () => {
      loading.value = true
      const ids = loadWishlistIds()

      if (ids.length === 0) {
        favoritos.value = []
        loading.value = false
        return
      }

      try {
        // Cargar todos los productos y filtrar por los IDs guardados
        const response = await productosService.getProductos({ limit: 200 })
        const productos = response.results || response || []
        favoritos.value = productos.filter(p => ids.includes(p.id))
      } catch (err) {
        console.error('Error cargando favoritos:', err)
        favoritos.value = []
      } finally {
        loading.value = false
      }
    }

    const quitarFavorito = (productId) => {
      // Quitar del localStorage
      const ids = loadWishlistIds().filter(id => id !== productId)
      saveWishlistIds(ids)
      // Quitar de la lista visual
      favoritos.value = favoritos.value.filter(p => p.id !== productId)
    }

    const irADetalle = (productoId) => {
      router.push(`/producto/${productoId}`)
    }

    const getProductImage = (producto) => {
      const url = producto.imagen_principal || producto.imagen_url || producto.imagen || producto.media_principal
      return url ? getImageUrl(url) : null
    }

    const handleImageError = (e) => {
      e.target.style.display = 'none'
    }

    const formatPrice = (price) => {
      const numPrice = Number(price)
      if (isNaN(numPrice)) return '0'
      return new Intl.NumberFormat('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(numPrice)
    }

    onMounted(() => {
      cargarFavoritos()
    })

    return {
      favoritos,
      loading,
      quitarFavorito,
      irADetalle,
      getProductImage,
      handleImageError,
      formatPrice,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
