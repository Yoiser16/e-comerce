<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FAF5F2] via-[#FAFAFA] to-white text-text-dark">
    <!-- Header Simple -->
    <header class="bg-white/90 border-b border-black/5 shadow-[0_6px_30px_rgba(0,0,0,0.04)] sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
        <div class="flex items-center justify-between h-16">
          <!-- Logo + Texto -->
          <router-link to="/" class="flex items-center gap-3 group">
            <img 
              src="/logo-kharis.png" 
              alt="Kharis Distribuidora" 
              class="h-12 w-auto object-contain group-hover:scale-105 transition-transform duration-300"
            />
            <span class="font-luxury text-xl tracking-wider text-text-dark hidden sm:inline-block">KHARIS</span>
          </router-link>
          
          <!-- Navegación -->
          <nav class="flex items-center gap-6">
            <router-link to="/" class="text-xs tracking-widest text-text-dark/60 hover:text-text-dark transition-colors">
              TIENDA
            </router-link>
            <button 
              @click="cerrarSesion" 
              class="text-xs tracking-widest text-text-dark/60 hover:text-text-dark transition-colors"
            >
              CERRAR SESIÓN
            </button>
          </nav>
        </div>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-12">
      <!-- Saludo -->
      <div class="mb-12">
        <h1 class="font-luxury text-3xl sm:text-4xl text-text-dark mb-2">
          Hola, {{ userName }}
        </h1>
        <p class="text-text-dark/60 text-sm">
          Bienvenida a tu espacio personal
        </p>
      </div>

      <!-- Tabs de navegación -->
      <div class="border-b border-black/10 mb-8">
        <nav class="flex gap-8">
          <button 
            @click="activeTab = 'favoritos'"
              class="pb-4 text-sm tracking-[0.18em] uppercase transition-colors relative"
            :class="activeTab === 'favoritos' 
              ? 'text-text-dark font-medium' 
              : 'text-text-dark/50 hover:text-text-dark/70'"
          >
            MIS FAVORITOS
            <span 
              v-if="activeTab === 'favoritos'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-text-dark"
            ></span>
          </button>
          <button 
            @click="activeTab = 'compras'"
              class="pb-4 text-sm tracking-[0.18em] uppercase transition-colors relative"
            :class="activeTab === 'compras' 
              ? 'text-text-dark font-medium' 
              : 'text-text-dark/50 hover:text-text-dark/70'"
          >
            MIS COMPRAS
            <span 
              v-if="activeTab === 'compras'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-text-dark"
            ></span>
          </button>
          <button 
            @click="activeTab = 'datos'"
              class="pb-4 text-sm tracking-[0.18em] uppercase transition-colors relative"
            :class="activeTab === 'datos' 
              ? 'text-text-dark font-medium' 
              : 'text-text-dark/50 hover:text-text-dark/70'"
          >
            MIS DATOS
            <span 
              v-if="activeTab === 'datos'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-text-dark"
            ></span>
          </button>
        </nav>
      </div>

      <!-- Contenido de Favoritos -->
      <section v-if="activeTab === 'favoritos'">
        <div v-if="loadingFavoritos" class="flex justify-center py-16">
          <div class="w-8 h-8 border-2 border-text-dark/20 border-t-text-dark rounded-full animate-spin"></div>
        </div>
        
        <div v-else-if="favoritos.length === 0" class="text-center py-16">
          <svg class="w-16 h-16 mx-auto text-text-dark/20 mb-4" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
          </svg>
          <h3 class="font-luxury text-xl text-text-dark mb-2">Sin favoritos aún</h3>
          <p class="text-text-dark/50 text-sm mb-6">
            Explora nuestra colección y guarda tus productos favoritos
          </p>
          <router-link 
            to="/"
            class="inline-block px-8 py-3 bg-text-dark text-white text-sm tracking-wider hover:bg-black transition-colors"
          >
            EXPLORAR TIENDA
          </router-link>
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          <div 
            v-for="producto in favoritos" 
            :key="producto.producto_id"
            @click="irADetalle(producto.producto_id)"
            class="group cursor-pointer bg-white/85 border border-black/5 shadow-[0_18px_50px_rgba(0,0,0,0.06)] rounded-sm p-3 transition-transform duration-300 hover:-translate-y-1"
          >
            <div class="relative aspect-[3/4] bg-nude-50 mb-3 overflow-hidden">
              <img 
                :src="getImageUrl(producto.imagen_principal) || '/placeholder.jpg'" 
                :alt="producto.nombre"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              />
              <button 
                @click.stop="quitarFavorito(producto.producto_id)"
                class="absolute top-3 right-3 w-8 h-8 bg-white/90 rounded-full flex items-center justify-center hover:bg-white transition-colors"
              >
                <svg class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>
              </button>
            </div>
            <h3 class="text-sm text-text-dark font-medium mb-1 line-clamp-2">
              {{ producto.nombre }}
            </h3>
            <p class="text-sm text-text-dark/70">
              {{ formatPrice(producto.precio_monto, producto.precio_moneda) }}
            </p>
          </div>
        </div>
      </section>

      <!-- Contenido de Compras -->
      <section v-if="activeTab === 'compras'">
        <div v-if="loadingCompras" class="flex justify-center py-16">
          <div class="w-8 h-8 border-2 border-text-dark/20 border-t-text-dark rounded-full animate-spin"></div>
        </div>
        
        <div v-else-if="compras.length === 0" class="text-center py-16 bg-white/85 border border-black/5 rounded-sm shadow-[0_18px_50px_rgba(0,0,0,0.06)]">
          <svg class="w-16 h-16 mx-auto text-text-dark/20 mb-4" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
          </svg>
          <h3 class="font-luxury text-xl text-text-dark mb-2">Sin compras aún</h3>
          <p class="text-text-dark/50 text-sm mb-6">
            Tu historial de compras aparecerá aquí
          </p>
          <router-link 
            to="/"
            class="inline-block px-8 py-3 bg-text-dark text-white text-sm tracking-wider hover:bg-black transition-colors"
          >
            COMENZAR A COMPRAR
          </router-link>
        </div>

        <div v-else class="space-y-6">
          <div 
            v-for="orden in compras" 
            :key="orden.id"
            class="bg-white/90 p-6 border border-black/5 shadow-[0_18px_50px_rgba(0,0,0,0.06)] rounded-sm"
          >
            <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-4 pb-4 border-b border-black/5">
              <div>
                <p class="text-xs text-text-dark/50 mb-1">Orden #{{ orden.numero }}</p>
                <p class="text-sm text-text-dark">{{ formatDate(orden.fecha) }}</p>
              </div>
              <div class="mt-2 sm:mt-0">
                <span 
                  class="inline-block px-3 py-1 text-xs tracking-wider rounded-full"
                  :class="getEstadoClass(orden.estado)"
                >
                  {{ orden.estado }}
                </span>
              </div>
            </div>
            
            <div class="space-y-3">
              <div 
                v-for="item in orden.items" 
                :key="item.id"
                class="flex gap-4"
              >
                <div class="w-16 h-20 bg-nude-50 flex-shrink-0">
                  <img 
                    :src="item.imagen || '/placeholder.jpg'" 
                    :alt="item.nombre"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div class="flex-1">
                  <p class="text-sm text-text-dark font-medium">{{ item.nombre }}</p>
                  <p class="text-xs text-text-dark/50">Cantidad: {{ item.cantidad }}</p>
                  <p class="text-sm text-text-dark/70 mt-1">{{ formatPrice(item.precio, 'USD') }}</p>
                </div>
              </div>
            </div>
            
            <div class="mt-4 pt-4 border-t border-black/5 flex justify-between items-center">
              <span class="text-sm text-text-dark/50">Total</span>
              <span class="text-lg font-medium text-text-dark">{{ formatPrice(orden.total, 'USD') }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Contenido de Datos -->
      <section v-if="activeTab === 'datos'">
        <div class="max-w-xl">
          <div class="bg-white p-6 sm:p-8 border border-black/5">
            <h3 class="font-luxury text-xl text-text-dark mb-6">Información Personal</h3>
            
            <form @submit.prevent="guardarDatos" class="space-y-5">
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">NOMBRE</label>
                <input 
                  v-model="datosUsuario.nombre"
                  type="text"
                  class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm"
                  placeholder="Tu nombre"
                />
              </div>
              
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">EMAIL</label>
                <input 
                  v-model="datosUsuario.email"
                  type="email"
                  disabled
                  class="w-full px-4 py-3 border border-black/10 bg-gray-50 text-text-dark/50 text-sm cursor-not-allowed"
                />
                <p class="text-xs text-text-dark/40 mt-1">El email no puede ser modificado</p>
              </div>
              
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">TELÉFONO</label>
                <input 
                  v-model="datosUsuario.telefono"
                  type="tel"
                  class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm"
                  placeholder="+1 (555) 000-0000"
                />
              </div>
              
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">DIRECCIÓN</label>
                <textarea 
                  v-model="datosUsuario.direccion"
                  rows="3"
                  class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm resize-none"
                  placeholder="Tu dirección de envío"
                ></textarea>
              </div>
              
              <button 
                type="submit"
                :disabled="guardando"
                class="w-full px-6 py-3 bg-text-dark text-white text-sm tracking-wider hover:bg-black transition-colors disabled:opacity-50"
              >
                {{ guardando ? 'GUARDANDO...' : 'GUARDAR CAMBIOS' }}
              </button>
            </form>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { favoritosService } from '../services/productos'
import { ordenesService } from '../services/ordenes'
import { getImageUrl } from '../services/api'

export default {
  name: 'MiCuenta',
  setup() {
    const router = useRouter()
    
    // Estado
    const activeTab = ref('favoritos')
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
    
    // Favoritos
    const favoritos = ref([])
    const loadingFavoritos = ref(true)
    
    // Compras
    const compras = ref([])
    const loadingCompras = ref(true)
    
    // Datos de usuario
    const datosUsuario = ref({
      nombre: user.value?.nombre || '',
      email: user.value?.email || '',
      telefono: user.value?.telefono || '',
      direccion: user.value?.direccion || ''
    })
    const guardando = ref(false)
    
    // Computed
    const userName = computed(() => {
      if (!user.value) return 'Usuario'
      return user.value.nombre || user.value.email?.split('@')[0] || 'Usuario'
    })
    
    // Métodos
    const cargarFavoritos = async () => {
      loadingFavoritos.value = true
      try {
        const data = await favoritosService.listar()
        // Backend devuelve una lista (List[FavoritoDTO]). Si viniera envuelto, manejar ambos casos.
        favoritos.value = Array.isArray(data) ? data : (data?.favoritos || data?.items || [])
      } catch (error) {
        console.error('Error cargando favoritos:', error)
        favoritos.value = []
      } finally {
        loadingFavoritos.value = false
      }
    }
    
    const cargarCompras = async () => {
      loadingCompras.value = true
      try {
        if (!user.value?.email) {
          compras.value = []
          return
        }

        const data = await ordenesService.obtenerPorEmail(user.value.email)
        const lista = Array.isArray(data) ? data : (data?.ordenes || data?.items || [])

        compras.value = lista.map((orden) => ({
          ...orden,
          estado: (orden.estado || '').toUpperCase(),
          items: (orden.items || []).map((item) => ({
            ...item,
            imagen: getImageUrl(item.imagen) || '/placeholder.jpg'
          }))
        }))
      } catch (error) {
        console.error('Error cargando compras:', error)
        compras.value = []
      } finally {
        loadingCompras.value = false
      }
    }
    
    const quitarFavorito = async (productoId) => {
      try {
        await favoritosService.eliminar(productoId)
        favoritos.value = favoritos.value.filter(f => f.producto_id !== productoId)
      } catch (error) {
        console.error('Error quitando favorito:', error)
      }
    }
    
    const irADetalle = (productoId) => {
      router.push(`/producto/${productoId}`)
    }
    
    const guardarDatos = async () => {
      guardando.value = true
      try {
        // TODO: Implementar endpoint
        // await apiClient.put('/auth/perfil', datosUsuario.value)
        alert('Datos guardados correctamente')
      } catch (error) {
        console.error('Error guardando datos:', error)
        alert('Error al guardar los datos')
      } finally {
        guardando.value = false
      }
    }
    
    const cerrarSesion = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      router.push('/')
    }
    
    const formatPrice = (amount, currency = 'USD') => {
      if (!amount) return '$0'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(amount)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    }
    
    const getEstadoClass = (estado) => {
      const clases = {
        'PENDIENTE': 'bg-yellow-50 text-yellow-700',
        'CONFIRMADO': 'bg-blue-50 text-blue-700',
        'ENVIADO': 'bg-purple-50 text-purple-700',
        'ENTREGADO': 'bg-green-50 text-green-700',
        'CANCELADO': 'bg-red-50 text-red-700'
      }
      return clases[estado] || 'bg-gray-50 text-gray-700'
    }
    
    // Verificar autenticación
    onMounted(() => {
      if (!user.value) {
        router.push('/')
        return
      }
      cargarFavoritos()
      cargarCompras()
    })
    
    return {
      activeTab,
      userName,
      favoritos,
      loadingFavoritos,
      compras,
      loadingCompras,
      datosUsuario,
      guardando,
      quitarFavorito,
      irADetalle,
      guardarDatos,
      cerrarSesion,
      formatPrice,
      formatDate,
      getEstadoClass,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.font-luxury {
  font-family: 'Playfair Display', serif;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
