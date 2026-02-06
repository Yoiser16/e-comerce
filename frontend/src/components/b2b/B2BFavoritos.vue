<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="font-luxury text-3xl sm:text-4xl text-gray-900">Mis Favoritos</h1>
          <p class="text-gray-500 mt-1">{{ favoritos.length }} producto{{ favoritos.length !== 1 ? 's' : '' }} guardado{{ favoritos.length !== 1 ? 's' : '' }}</p>
        </div>
        
        <router-link 
          to="/portal/catalogo"
          class="inline-flex items-center gap-2 text-[#C9A962] hover:text-[#B8943E] font-medium transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          Seguir comprando
        </router-link>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center min-h-[40vh]">
        <div class="relative w-16 h-16">
          <div class="absolute inset-0 border-4 border-gray-100 rounded-full"></div>
          <div class="absolute inset-0 border-4 border-[#C9A962] rounded-full border-t-transparent animate-spin"></div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="favoritos.length === 0" class="text-center py-20">
        <div class="w-24 h-24 mx-auto bg-pink-50 rounded-full flex items-center justify-center mb-6">
          <svg class="w-12 h-12 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
        </div>
        <h2 class="font-luxury text-2xl text-gray-800 mb-3">Aún no tienes favoritos</h2>
        <p class="text-gray-500 max-w-md mx-auto mb-8">
          Explora nuestro catálogo y guarda los productos que te gusten haciendo clic en el corazón
        </p>
        <router-link 
          to="/portal/catalogo"
          class="inline-flex items-center gap-2 bg-[#1A1A1A] hover:bg-black text-white font-medium px-8 py-4 rounded-xl transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          Explorar catálogo
        </router-link>
      </div>
      
      <!-- Favorites Grid -->
      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="item in favoritos" 
            :key="item.id"
            class="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 group relative"
          >
            <!-- Product Image -->
            <router-link 
              :to="`/portal/producto/${item.producto?.id || item.producto_id}`"
              class="block relative aspect-square bg-gray-50 overflow-hidden"
            >
              <img 
                :src="item.producto?.imagen_principal || '/placeholder.png'" 
                :alt="item.producto?.nombre || 'Producto'"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                @error="handleImageError"
              />
              
              <!-- Stock Badge -->
              <div 
                v-if="item.producto?.stock_actual <= 5 && item.producto?.stock_actual > 0"
                class="absolute top-3 left-3 bg-orange-500 text-white text-xs font-bold px-2.5 py-1 rounded-full"
              >
                ¡Últimas {{ item.producto.stock_actual }}!
              </div>
              <div 
                v-else-if="item.producto?.stock_actual === 0"
                class="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold px-2.5 py-1 rounded-full"
              >
                Agotado
              </div>
            </router-link>
            
            <!-- Remove Button -->
            <button 
              @click="eliminarFavorito(item)"
              class="absolute top-3 right-3 w-10 h-10 bg-white/90 rounded-full shadow-md flex items-center justify-center hover:bg-white hover:scale-110 transition-all duration-200 text-pink-500"
            >
              <svg class="w-5 h-5" fill="currentColor" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              </svg>
            </button>
            
            <!-- Product Info -->
            <div class="p-4">
              <router-link 
                :to="`/portal/producto/${item.producto?.id || item.producto_id}`"
                class="block"
              >
                <p class="text-xs text-[#C9A962] font-medium mb-1">
                  {{ item.producto?.categoria?.nombre || 'Productos' }}
                </p>
                <h3 class="font-medium text-gray-800 line-clamp-2 mb-2 group-hover:text-[#C9A962] transition-colors">
                  {{ item.producto?.nombre || 'Producto' }}
                </h3>
              </router-link>
              
              <!-- Pricing -->
              <div class="flex items-end gap-2 mb-4">
                <span class="text-xl font-bold text-gray-900">
                  ${{ formatPrice(item.producto?.precio_mayorista || item.producto?.monto_precio) }}
                </span>
                <span 
                  v-if="item.producto?.precio && item.producto?.precio > (item.producto?.precio_mayorista || item.producto?.monto_precio)"
                  class="text-sm text-gray-400 line-through"
                >
                  ${{ formatPrice(item.producto?.precio) }}
                </span>
              </div>
              
              <!-- Add to Cart Button -->
              <button 
                @click="agregarAlCarrito(item)"
                :disabled="item.producto?.stock_actual === 0"
                class="w-full py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-xl flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                {{ item.producto?.stock_actual === 0 ? 'Sin stock' : 'Agregar al carrito' }}
              </button>
              
              <!-- Date Added -->
              <p class="text-xs text-gray-400 text-center mt-3">
                Agregado {{ formatFecha(item.fecha_agregado) }}
              </p>
            </div>
          </div>
        </div>
        
        <!-- Clear All Button -->
        <div v-if="favoritos.length > 0" class="mt-12 text-center">
          <button 
            @click="limpiarFavoritos"
            class="text-gray-500 hover:text-red-500 text-sm font-medium underline transition-colors"
          >
            Eliminar todos los favoritos
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { favoritosService, productosService } from '@/services/productos'

export default {
  name: 'B2BFavoritos',
  setup() {
    const favoritos = ref([])
    const loading = ref(true)
    
    // User
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{}')
    })
    
    // Helper para sincronizar localStorage
    function syncLocalFavoritos() {
      const ids = favoritos.value.map(f => f.producto?.id || f.producto_id).filter(Boolean)
      localStorage.setItem('b2b_favoritos', JSON.stringify(ids))
      window.dispatchEvent(new CustomEvent('favoritos-updated'))
    }
    
    // Methods
    function formatPrice(value) {
      return Number(value || 0).toLocaleString('es-CO')
    }
    
    function formatFecha(fecha) {
      if (!fecha) return ''
      const d = new Date(fecha)
      const now = new Date()
      const diff = now - d
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      
      if (days === 0) return 'hoy'
      if (days === 1) return 'ayer'
      if (days < 7) return `hace ${days} días`
      if (days < 30) return `hace ${Math.floor(days / 7)} semanas`
      return d.toLocaleDateString('es-CO', { day: 'numeric', month: 'short' })
    }
    
    function handleImageError(e) {
      e.target.src = '/placeholder.png'
    }
    
    async function cargarFavoritos() {
      try {
        loading.value = true
        const apiData = await favoritosService.listar()
        favoritos.value = apiData
        // Sincronizar localStorage con la API
        syncLocalFavoritos()
      } catch (err) {
        console.error('Error cargando favoritos de API:', err)
        // Fallback: cargar desde localStorage
        try {
          const storedIds = JSON.parse(localStorage.getItem('b2b_favoritos') || '[]')
          if (storedIds.length > 0) {
            // Cargar info de productos desde la API
            const productos = await Promise.all(
              storedIds.map(async (id) => {
                try {
                  const producto = await productosService.getProducto(id)
                  return { producto_id: id, producto, fecha_agregado: new Date().toISOString() }
                } catch {
                  return null
                }
              })
            )
            favoritos.value = productos.filter(Boolean)
          } else {
            favoritos.value = []
          }
        } catch {
          favoritos.value = []
        }
      } finally {
        loading.value = false
      }
    }
    
    async function eliminarFavorito(item) {
      try {
        const id = item.producto?.id || item.producto_id
        await favoritosService.eliminar(id)
        favoritos.value = favoritos.value.filter(f => 
          (f.producto?.id || f.producto_id) !== id
        )
        syncLocalFavoritos()
      } catch (err) {
        console.error('Error eliminando favorito:', err)
        // Aún así eliminar localmente para UX
        const id = item.producto?.id || item.producto_id
        favoritos.value = favoritos.value.filter(f => 
          (f.producto?.id || f.producto_id) !== id
        )
        syncLocalFavoritos()
      }
    }
    
    async function limpiarFavoritos() {
      if (!confirm('¿Estás seguro de eliminar todos tus favoritos?')) return
      
      try {
        // Eliminar uno por uno
        for (const item of favoritos.value) {
          await favoritosService.eliminar(item.producto?.id || item.producto_id)
        }
        favoritos.value = []
        syncLocalFavoritos()
      } catch (err) {
        console.error('Error limpiando favoritos:', err)
        // Limpiar localmente de todas formas
        favoritos.value = []
        syncLocalFavoritos()
      }
    }
    
    function agregarAlCarrito(item) {
      const producto = item.producto
      if (!producto || producto.stock_actual === 0) return
      
      // Agregar al carrito del storage
      const cart = JSON.parse(localStorage.getItem('b2b_cart') || '{"items":[]}')
      const existingIndex = cart.items.findIndex(i => i.id === producto.id)
      
      if (existingIndex >= 0) {
        cart.items[existingIndex].cantidad += 1
      } else {
        cart.items.push({
          id: producto.id,
          nombre: producto.nombre,
          imagen: producto.imagen_principal,
          precio: producto.precio_mayorista || producto.monto_precio,
          cantidad: 1
        })
      }
      
      localStorage.setItem('b2b_cart', JSON.stringify(cart))
      alert(`${producto.nombre} agregado al carrito`)
    }
    
    // Lifecycle
    onMounted(() => {
      cargarFavoritos()
    })
    
    return {
      favoritos,
      loading,
      formatPrice,
      formatFecha,
      handleImageError,
      eliminarFavorito,
      limpiarFavoritos,
      agregarAlCarrito
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
