<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FBF9F7] to-[#F5F0EC] flex flex-col">
    
    <!-- Header Simple -->
    <header class="bg-white/80 border-b border-nude-100/50 py-5">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <router-link to="/" class="flex items-center gap-3 w-fit">
          <img 
            src="/logo-kharis.png" 
            alt="Kharis" 
            class="h-16 sm:h-20 w-auto"
          />
        </router-link>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="flex-1 flex items-center justify-center px-4 py-8 lg:py-12">
      <div class="max-w-5xl w-full">
        
        <!-- Header de Éxito -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-[#A8E6CF] to-[#88D8B0] flex items-center justify-center shadow-lg shadow-emerald-200/50 animate-bounce-once">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
          </div>
          <h1 class="font-luxury text-3xl lg:text-4xl text-text-dark mb-2">¡Pedido Registrado!</h1>
          <p class="text-text-medium text-sm">Tu solicitud ha sido enviada exitosamente ✨</p>
        </div>
        
        <!-- Card de Confirmación -->
        <div class="bg-white rounded-3xl p-6 lg:p-8 shadow-xl shadow-black/[0.03] border border-nude-100/50">
          
          <!-- Grid Layout: 2 columnas en desktop, 1 en móvil -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
            
            <!-- Columna Izquierda: Detalles del Pedido -->
            <div>
              <div class="bg-gradient-to-br from-[#F8F3EF] to-[#FAF5F2] rounded-2xl p-5 border border-nude-200/50">
                <div class="flex items-center gap-2 mb-4">
                  <svg class="w-5 h-5 text-[#8B7355]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                  </svg>
                  <h3 class="font-semibold text-text-dark">Código de Pedido</h3>
                </div>
                
                <div class="space-y-3 text-sm">
                  <div class="flex justify-between items-center py-2.5 border-b border-nude-200/50">
                    <span class="text-text-medium">Código:</span>
                    <span class="font-mono font-bold text-[#8B7355] text-base">{{ codigo }}</span>
                  </div>
                  
                  <div class="flex justify-between items-center py-2.5 border-b border-nude-200/50">
                    <span class="text-text-medium">Cliente:</span>
                    <span class="font-medium text-text-dark">{{ nombreCliente }}</span>
                  </div>
                  
                  <div class="flex justify-between items-center py-2.5 border-b border-nude-200/50">
                    <span class="text-text-medium">Productos:</span>
                    <span class="font-medium text-text-dark">{{ totalProductos }} artículo{{ totalProductos !== 1 ? 's' : '' }}</span>
                  </div>
                  
                  <div class="flex justify-between items-center py-2.5">
                    <span class="text-text-medium">Total:</span>
                    <span class="font-bold text-[#C9A962] text-lg">${{ formatPrice(total) }} COP</span>
                  </div>
                </div>
              </div>
              
              <!-- Lista de productos -->
              <div v-if="productos.length > 0" class="mt-5">
                <h3 class="font-semibold text-text-dark mb-3 text-sm flex items-center gap-2">
                  <svg class="w-4 h-4 text-[#8B7355]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                  </svg>
                  Tu pedido incluye:
                </h3>
                <div class="space-y-2 max-h-[180px] overflow-y-auto custom-scrollbar">
                  <div 
                    v-for="(producto, index) in productos" 
                    :key="index"
                    class="flex items-center gap-3 p-3 bg-gradient-to-r from-[#FAF5F2] to-[#F8F3EF] rounded-xl border border-nude-100/50"
                  >
                    <div class="w-10 h-10 rounded-lg bg-white flex items-center justify-center text-[#8B7355] text-xs font-bold border border-nude-200/50 shadow-sm">
                      {{ producto.cantidad }}x
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-text-dark truncate">{{ producto.nombre }}</p>
                      <p class="text-xs text-text-medium">${{ formatPrice(producto.precio_unitario || producto.precio || 0) }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Columna Derecha: WhatsApp CTA -->
            <div class="flex flex-col justify-between">
              <div class="bg-gradient-to-br from-[#E8F5E9] to-[#F1F8E9] rounded-2xl p-6 border border-[#A8E6CF]/40">
                <div class="flex items-start gap-3 mb-5">
                  <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-[#A8E6CF] to-[#88D8B0] flex items-center justify-center flex-shrink-0 shadow-lg shadow-emerald-200/50">
                    <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                    </svg>
                  </div>
                  <div class="text-left flex-1">
                    <h3 class="font-semibold text-[#2E7D32] text-lg mb-1">Continúa por WhatsApp</h3>
                    <p class="text-xs text-text-medium leading-relaxed">Ahora finaliza tu compra por WhatsApp. Ya abrimos el chat con todos los detalles de tu pedido 💚</p>
                  </div>
                </div>
                
                <a 
                  :href="whatsappUrl" 
                  target="_blank"
                  class="w-full bg-gradient-to-r from-[#A8E6CF] to-[#88D8B0] text-white font-medium px-6 py-4 rounded-xl inline-flex items-center justify-center gap-2 hover:shadow-xl hover:shadow-emerald-200/40 transition-all hover:scale-[1.02] mb-3"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                  Abrir WhatsApp
                </a>
                
                <p class="text-xs text-center text-text-medium italic">Si el chat no se abrió, haz clic en el botón de arriba</p>
              </div>
              
              <!-- Botón volver al inicio -->
              <router-link 
                to="/" 
                class="mt-5 w-full bg-gradient-to-r from-text-dark to-black hover:from-black hover:to-text-dark text-white font-medium px-6 py-4 rounded-xl inline-flex items-center justify-center gap-2 transition-all hover:shadow-xl hover:shadow-black/20"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                </svg>
                Volver al Inicio
              </router-link>
            </div>
            
          </div>
          
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const codigo = ref('KH-0000')
const total = ref(0)
const productos = ref([])
const nombreCliente = ref('Cliente')
const telefono = ref('')
const whatsappNumber = '573217355070'

const totalProductos = computed(() => {
  return productos.value.reduce((sum, p) => sum + (p.cantidad || 1), 0)
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('es-CO').format(price)
}

const whatsappUrl = computed(() => {
  const productosTexto = productos.value.map(p => `• ${p.nombre || 'Producto'} x${p.cantidad || 1}`).join('%0A')
  const msg = `Hola, quiero finalizar mi pedido%0A%0A*CÓDIGO:* ${codigo.value}%0A%0A*PRODUCTOS:*%0A${productosTexto}%0A%0A*TOTAL:* $${formatPrice(total.value)} COP%0A%0A*${nombreCliente.value}*%0A${telefono.value}`
  return `https://wa.me/${whatsappNumber}?text=${msg}`
})

onMounted(() => {
  try {
    const ordenData = sessionStorage.getItem('orden_whatsapp')
    if (ordenData) {
      const orden = JSON.parse(ordenData)
      codigo.value = orden.codigo || 'KH-0000'
      total.value = orden.total || 0
      productos.value = orden.productos || []
      nombreCliente.value = `${orden.cliente?.nombre || ''} ${orden.cliente?.apellido || ''}`.trim() || 'Cliente'
      telefono.value = orden.cliente?.telefono || ''
      
      // Limpiar datos de sesión
      sessionStorage.removeItem('orden_whatsapp')
    } else {
      // Si no hay datos, redirigir al home después de 3 segundos
      setTimeout(() => {
        router.push('/')
      }, 3000)
    }
  } catch (e) {
    console.error('Error al cargar datos de la orden:', e)
  }
})
</script>

<style scoped>
@keyframes bounce-once {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.animate-bounce-once {
  animation: bounce-once 0.6s ease-in-out;
}

.font-luxury {
  font-family: 'Playfair Display', serif;
}

/* Scrollbar personalizado */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #FAF5F2;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #D4A85A;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #C9A962;
}
</style>
