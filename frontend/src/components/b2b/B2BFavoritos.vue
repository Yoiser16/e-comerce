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
                :src="item.producto?.imagen_principal || item.producto?.imagen || '/placeholder.png'" 
                :alt="item.producto?.nombre || 'Producto'"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                @error="handleImageError"
                loading="lazy"
              />
              
              <!-- Stock Badge -->
              <div 
                v-if="(item.producto?.stock_actual || 0) <= 5 && (item.producto?.stock_actual || 0) > 0"
                class="absolute top-3 left-3 bg-orange-500 text-white text-xs font-bold px-2.5 py-1 rounded-full"
              >
                ¡Últimas {{ item.producto?.stock_actual || 0 }}!
              </div>
              <div 
                v-else-if="(item.producto?.stock_actual || 0) === 0"
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
                  ${{ formatPrice(item.producto?.precio_mayorista || item.producto?.monto_precio || item.producto?.precio || 0) }}
                </span>
                <span 
                  v-if="item.producto?.precio && item.producto?.precio > (item.producto?.precio_mayorista || item.producto?.monto_precio || 0)"
                  class="text-sm text-gray-400 line-through"
                >
                  ${{ formatPrice(item.producto.precio) }}
                </span>
              </div>
              
              <!-- Add to Cart Button -->
              <button 
                @click="agregarAlCarrito(item)"
                :disabled="(item.producto?.stock_actual || 0) === 0"
                class="w-full py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-xl flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                {{ (item.producto?.stock_actual || 0) === 0 ? 'Sin stock' : 'Agregar al carrito' }}
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

    <!-- Add to Cart Modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showCartModal" class="fixed inset-0 z-[60]">
          <div class="absolute inset-0 bg-black/40" @click="closeCartModal"></div>
          <div class="relative flex min-h-full items-center justify-center px-4 py-8">
            <div class="w-full max-w-md rounded-2xl bg-[#FAFAFA] shadow-2xl border border-[#C9A962]/20">
              <div class="px-6 pt-6 pb-4">
                <div class="flex items-start justify-between gap-3">
                  <div>
                    <p class="text-[11px] tracking-[0.2em] uppercase text-[#C9A962] font-semibold">Portal Mayorista</p>
                    <h3 class="font-luxury text-2xl text-[#1A1A1A] mt-2">Producto agregado</h3>
                  </div>
                  <button
                    class="w-9 h-9 rounded-full border border-[#C9A962]/30 text-[#1A1A1A] hover:bg-[#C9A962]/10 transition-colors"
                    @click="closeCartModal"
                  >
                    <svg class="w-4 h-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                <div class="mt-5 rounded-xl bg-white border border-[#C9A962]/15 px-4 py-3">
                  <p class="text-sm text-[#4A4A4A]">Agregaste</p>
                  <p class="text-base font-semibold text-[#1A1A1A] mt-1">
                    {{ modalQuantity }} unidades de {{ modalProductName }}
                  </p>
                </div>

                <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <router-link
                    to="/portal/carrito"
                    class="inline-flex items-center justify-center bg-[#1A1A1A] hover:bg-black text-white font-medium px-5 py-3 rounded-xl transition-colors"
                    @click="closeCartModal"
                  >
                    Ver carrito
                  </router-link>
                  <button
                    class="inline-flex items-center justify-center border border-[#1A1A1A]/30 text-[#1A1A1A] hover:border-[#1A1A1A] font-medium px-5 py-3 rounded-xl transition-colors"
                    @click="closeCartModal"
                  >
                    Seguir comprando
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { obtenerProducto as obtenerProductoB2B } from '@/services/mayoristas'

export default {
  name: 'B2BFavoritos',
  setup() {
    const favoritos = ref([])
    const loading = ref(true)
    const showCartModal = ref(false)
    const modalProductName = ref('')
    const modalQuantity = ref(0)
    let modalTimer = null
    
    // User
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{}')
    })

    function getFavoritosKey() {
      const keyPart = user.value?.email || user.value?.id || user.value?.usuario_id || 'anon'
      return `b2b_favoritos_${keyPart}`
    }
    
    // Helper para sincronizar localStorage
    function syncLocalFavoritos() {
      const ids = favoritos.value.map(f => f.producto?.id || f.producto_id).filter(Boolean)
      localStorage.setItem(getFavoritosKey(), JSON.stringify(ids))
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

    function openCartModal(productName, quantity) {
      modalProductName.value = productName || 'producto'
      modalQuantity.value = quantity || 0
      showCartModal.value = true

      if (modalTimer) clearTimeout(modalTimer)
      modalTimer = setTimeout(() => {
        showCartModal.value = false
      }, 3000)
    }

    function closeCartModal() {
      showCartModal.value = false
      if (modalTimer) {
        clearTimeout(modalTimer)
        modalTimer = null
      }
    }
    
    async function cargarFavoritos() {
      try {
        loading.value = true
        
        // Para B2B, cargar directamente desde localStorage con precios mayoristas
        // Esto evita problemas de autenticación y es más rápido
        const storedIds = JSON.parse(localStorage.getItem(getFavoritosKey()) || '[]')
        
        if (storedIds.length === 0) {
          favoritos.value = []
          return
        }
        
        // Cargar info de productos con precios mayoristas desde la API B2B
        const productos = await Promise.all(
          storedIds.map(async (id) => {
            try {
              const productoData = await obtenerProductoB2B(id)
              return {
                id: productoData.id || id,
                producto_id: productoData.id || id,
                fecha_agregado: new Date().toISOString(),
                producto: {
                  id: productoData.id,
                  nombre: productoData.nombre || 'Producto',
                  imagen_principal: productoData.imagen_principal || productoData.imagen,
                  precio_mayorista: productoData.precio_mayorista,
                  monto_precio: productoData.monto_precio,
                  precio: productoData.precio || productoData.monto_precio,
                  stock_actual: productoData.stock_actual || 0,
                  sku: productoData.sku,
                  categoria: productoData.categoria
                }
              }
            } catch (err) {
              return null
            }
          })
        )
        
        favoritos.value = productos.filter(Boolean)
        
      } catch (err) {
        favoritos.value = []
      } finally {
        loading.value = false
      }
    }
    
    async function eliminarFavorito(item) {
      const id = item.producto?.id || item.producto_id
      favoritos.value = favoritos.value.filter(f => 
        (f.producto?.id || f.producto_id) !== id
      )
      syncLocalFavoritos()
    }
    
    async function limpiarFavoritos() {
      if (!confirm('¿Estás seguro de eliminar todos tus favoritos?')) return
      
      favoritos.value = []
      syncLocalFavoritos()
    }
    
    function agregarAlCarrito(item) {
      const producto = item.producto
      if (!producto || (producto.stock_actual || 0) === 0) return
      
      const CANTIDAD_MINIMA = 10 // Compra mínima para mayoristas
      
      // Agregar al carrito del storage
      const cart = JSON.parse(localStorage.getItem('b2b_cart') || '{"items":[]}')
      const existingIndex = cart.items.findIndex(i => i.id === (producto.id || item.producto_id))
      
      if (existingIndex >= 0) {
        cart.items[existingIndex].cantidad += CANTIDAD_MINIMA
      } else {
        cart.items.push({
          id: producto.id || item.producto_id,
          nombre: producto.nombre || 'Producto',
          imagen: producto.imagen_principal || producto.imagen || '/placeholder.png',
          precio: producto.precio_mayorista || producto.monto_precio || producto.precio || 0,
          cantidad: CANTIDAD_MINIMA,
          sku: producto.sku || null,
          categoria: producto.categoria?.nombre || 'Productos'
        })
      }
      
      localStorage.setItem('b2b_cart', JSON.stringify(cart))
      openCartModal(producto.nombre || 'producto', CANTIDAD_MINIMA)
      
      // Actualizar contador del header
      window.dispatchEvent(new CustomEvent('cart-updated'))
    }
    
    // Lifecycle
    onMounted(() => {
      cargarFavoritos()
    })
    
    return {
      favoritos,
      loading,
      showCartModal,
      modalProductName,
      modalQuantity,
      formatPrice,
      formatFecha,
      handleImageError,
      eliminarFavorito,
      limpiarFavoritos,
      agregarAlCarrito,
      closeCartModal
    }
  }
}
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
