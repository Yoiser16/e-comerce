<template>
  <div class="min-h-screen bg-[#F8F8F8]">
    
    <!-- =========================================================================
         HERO BANNER - Elegante y Minimalista
    ========================================================================== -->
    <div class="relative mb-12 -mx-4 sm:-mx-6 overflow-hidden rounded-b-3xl">
      <!-- Slider Container -->
      <div 
        class="flex transition-transform duration-700 ease-[cubic-bezier(0.4,0,0.2,1)]"
        :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
      >
        <!-- Slide 1 - Nueva Colección -->
        <div class="w-full flex-shrink-0 relative">
          <div class="relative h-[220px] sm:h-[280px] lg:h-[320px] bg-gradient-to-br from-[#18181B] via-[#1F1F23] to-[#18181B] overflow-hidden">
            <!-- Imagen de fondo -->
            <img 
              src="/img2.jpg" 
              alt="Extensiones" 
              class="absolute inset-0 w-full h-full object-cover object-center opacity-70"
            />
            <!-- Overlay oscuro -->
            <div class="absolute inset-0 bg-gradient-to-r from-[#18181B]/95 via-[#18181B]/80 to-transparent"></div>
            
            <!-- Contenido -->
            <div class="relative h-full flex flex-col justify-center px-6 sm:px-10 lg:px-16 max-w-xl">
              <span class="inline-flex items-center gap-3 text-[#C9A962]/80 text-[11px] font-medium tracking-[0.2em] uppercase mb-4">
                <span class="w-6 h-px bg-[#C9A962]/50"></span>
                Colección 2026
              </span>
              <h2 class="text-2xl sm:text-3xl lg:text-4xl font-semibold text-white/95 leading-tight mb-3 tracking-tight">
                Extensiones<br class="hidden sm:block"/>
                <span class="text-[#C9A962]">100% Humanas</span>
              </h2>
              <p class="text-white/50 text-sm mb-6 max-w-sm leading-relaxed">
                Calidad premium. Stock disponible para entrega inmediata.
              </p>
              <router-link 
                to="/portal/catalogo?categoria=extensiones"
                class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#C9A962] hover:bg-[#D4AF6A] text-[#18181B] text-sm font-semibold rounded-lg transition-all duration-300 w-fit group hover:shadow-lg hover:shadow-[#C9A962]/20"
              >
                Ver inventario
                <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Slide 2 - Ofertas -->
        <div class="w-full flex-shrink-0 relative">
          <div class="relative h-[220px] sm:h-[280px] lg:h-[320px] bg-gradient-to-br from-[#1C1820] via-[#211E26] to-[#18181B] overflow-hidden">
            <!-- Imagen de fondo -->
            <img 
              src="/promocion.webp" 
              alt="Promoción Maquillaje" 
              class="absolute inset-0 w-full h-full object-cover object-center opacity-65"
            />
            <!-- Overlay oscuro con tono rosado -->
            <div class="absolute inset-0 bg-gradient-to-r from-[#1C1820]/95 via-[#1C1820]/80 to-rose-900/30"></div>
            
            <div class="relative h-full flex flex-col justify-center px-6 sm:px-10 lg:px-16 max-w-xl">
              <span class="inline-flex items-center gap-3 text-rose-300/80 text-[11px] font-medium tracking-[0.2em] uppercase mb-4">
                <span class="w-6 h-px bg-rose-400/50"></span>
                Solo esta semana
              </span>
              <h2 class="text-2xl sm:text-3xl lg:text-4xl font-semibold text-white/95 leading-tight mb-3 tracking-tight">
                Hasta <span class="text-rose-400">30% OFF</span><br class="hidden sm:block"/>
                en Maquillaje
              </h2>
              <p class="text-white/50 text-sm mb-6 max-w-sm leading-relaxed">
                Descuentos exclusivos en las marcas más vendidas.
              </p>
              <router-link 
                to="/portal/catalogo?oferta=true"
                class="inline-flex items-center gap-2 px-5 py-2.5 bg-rose-500/90 hover:bg-rose-500 text-white text-sm font-semibold rounded-lg transition-all duration-300 w-fit group hover:shadow-lg hover:shadow-rose-500/20"
              >
                Ver ofertas
                <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Slide 3 - Envío Gratis -->
        <div class="w-full flex-shrink-0 relative">
          <div class="relative h-[220px] sm:h-[280px] lg:h-[320px] bg-gradient-to-br from-[#141D1A] via-[#182420] to-[#18181B] overflow-hidden">
            <!-- Decoración sutil -->
            <div class="absolute top-0 right-0 w-80 h-80 bg-gradient-to-bl from-emerald-500/15 to-transparent rounded-full blur-3xl"></div>
            <div class="absolute bottom-0 left-0 w-64 h-64 bg-gradient-to-tr from-emerald-500/10 to-transparent rounded-full blur-2xl"></div>
            <!-- Icono decorativo de envío -->
            <div class="absolute right-10 lg:right-20 top-1/2 -translate-y-1/2 hidden md:block">
              <svg class="w-32 lg:w-40 h-32 lg:h-40 text-emerald-500/10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="0.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
              </svg>
            </div>
            
            <div class="relative h-full flex flex-col justify-center px-6 sm:px-10 lg:px-16 max-w-xl">
              <span class="inline-flex items-center gap-3 text-emerald-400/80 text-[11px] font-medium tracking-[0.2em] uppercase mb-4">
                <span class="w-6 h-px bg-emerald-400/50"></span>
                Beneficio exclusivo
              </span>
              <h2 class="text-2xl sm:text-3xl lg:text-4xl font-semibold text-white/95 leading-tight mb-3 tracking-tight">
                Envío <span class="text-emerald-400">gratis</span><br class="hidden sm:block"/>
                a todo el país
              </h2>
              <p class="text-white/50 text-sm mb-6 max-w-sm leading-relaxed">
                En pedidos +$500.000. Entrega en 24-48 horas.
              </p>
              <router-link 
                to="/portal/catalogo"
                class="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-500/90 hover:bg-emerald-500 text-white text-sm font-semibold rounded-lg transition-all duration-300 w-fit group hover:shadow-lg hover:shadow-emerald-500/20"
              >
                Explorar
                <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Indicadores minimalistas (líneas) -->
      <div class="absolute bottom-5 left-1/2 -translate-x-1/2 flex items-center gap-1.5">
        <button 
          v-for="(slide, index) in 3" 
          :key="index"
          @click="currentSlide = index"
          class="h-0.5 rounded-full transition-all duration-500 ease-out"
          :class="currentSlide === index ? 'bg-white w-8' : 'bg-white/25 w-4 hover:bg-white/40'"
        ></button>
      </div>
      
      <!-- Flechas de navegación más sutiles -->
      <button 
        @click="prevSlide"
        class="absolute left-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-white/5 hover:bg-white/15 rounded-full flex items-center justify-center transition-all duration-300 opacity-0 group-hover:opacity-100 hover:scale-105"
      >
        <svg class="w-4 h-4 text-white/80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <button 
        @click="nextSlide"
        class="absolute right-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-white/5 hover:bg-white/15 rounded-full flex items-center justify-center transition-all duration-300 opacity-0 group-hover:opacity-100 hover:scale-105"
      >
        <svg class="w-4 h-4 text-white/80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <!-- =========================================================================
         SECCIÓN RECOMPRA - Tus Habituales
    ========================================================================== -->
    <div class="mb-14">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-lg sm:text-xl font-semibold text-gray-800 tracking-tight">Tus habituales</h2>
          <p class="text-gray-400 text-sm mt-0.5">Restock rápido de tus favoritos</p>
        </div>
        <router-link 
          to="/portal/pedidos"
          class="text-gray-500 hover:text-gray-700 text-sm font-medium flex items-center gap-1 transition-colors"
        >
          Ver historial
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
      
      <!-- Scroll horizontal de productos habituales -->
      <div class="flex gap-3 overflow-x-auto pb-4 -mx-4 px-4 scrollbar-hide">
        <div 
          v-for="product in frequentProducts" 
          :key="product.id"
          class="flex-shrink-0 w-[150px] sm:w-[168px] bg-white rounded-xl border border-gray-100/80 overflow-hidden hover:shadow-md hover:shadow-gray-200/50 hover:-translate-y-0.5 transition-all duration-300 ease-out group"
        >
          <!-- Imagen del producto -->
          <div class="relative aspect-[4/5] bg-gray-50 overflow-hidden">
            <img 
              :src="product.image" 
              :alt="product.name"
              class="w-full h-full object-cover group-hover:scale-103 transition-transform duration-500 ease-out"
              @error="handleProductImageError($event, product)"
            />
            <!-- Badge de cantidad - más pequeño y sutil -->
            <div class="absolute top-2 right-2 bg-gray-900/60 text-white text-[10px] px-1.5 py-0.5 rounded font-medium">
              ×{{ product.lastQty }}
            </div>
          </div>
          
          <!-- Info del producto -->
          <div class="p-3">
            <h3 class="font-medium text-gray-800 text-[13px] line-clamp-2 mb-1.5 leading-snug">
              {{ product.name }}
            </h3>
            <p class="text-gray-900 font-semibold text-sm mb-2.5">
              ${{ product.price.toLocaleString() }}
            </p>
            
            <!-- Botón agregar - más ligero -->
            <button 
              @click="quickAddToCart(product)"
              class="w-full py-2 bg-gray-100 hover:bg-gray-900 text-gray-700 hover:text-white text-xs font-medium rounded-lg flex items-center justify-center gap-1.5 transition-all duration-250"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Agregar
            </button>
          </div>
        </div>
        
        <!-- Card "Ver más" -->
        <router-link 
          to="/portal/catalogo"
          class="flex-shrink-0 w-[150px] sm:w-[168px] bg-gray-50/50 rounded-xl border border-dashed border-gray-200 flex flex-col items-center justify-center aspect-[4/5] hover:border-gray-300 hover:bg-gray-50 transition-all duration-300 group"
        >
          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center mb-2 shadow-sm group-hover:scale-105 transition-transform duration-300">
            <svg class="w-5 h-5 text-gray-400 group-hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </div>
          <span class="text-gray-500 font-medium text-xs">Ver catálogo</span>
          <span class="text-gray-400 text-[10px]">+500 productos</span>
        </router-link>
      </div>
    </div>

    <!-- =========================================================================
         SECCIÓN DESCUBRIMIENTO - Novedades
    ========================================================================== -->
    <div class="mb-14">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-lg sm:text-xl font-semibold text-gray-800 tracking-tight">Novedades</h2>
          <p class="text-gray-400 text-sm mt-0.5">Los productos más recientes del inventario</p>
        </div>
        <router-link 
          to="/portal/catalogo?orden=nuevo"
          class="text-gray-500 hover:text-gray-700 text-sm font-medium flex items-center gap-1 transition-colors"
        >
          Ver todas
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
      
      <!-- Grid de productos destacados -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
        <div 
          v-for="product in featuredProducts" 
          :key="product.id"
          class="group bg-white rounded-xl overflow-hidden border border-gray-100/80 hover:shadow-lg hover:shadow-gray-200/60 hover:-translate-y-0.5 transition-all duration-300 ease-out"
        >
          <!-- Imagen grande -->
          <div class="relative aspect-[4/5] bg-gray-50 overflow-hidden">
            <img 
              :src="product.image" 
              :alt="product.name"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
              @error="handleProductImageError($event, product)"
            />
            
            <!-- Badges más sutiles -->
            <div class="absolute top-2 left-2 flex flex-col gap-1.5">
              <span 
                v-if="product.badge === 'new'"
                class="px-2 py-0.5 bg-emerald-500/90 text-white text-[10px] font-semibold rounded"
              >
                Nuevo
              </span>
              <span 
                v-if="product.badge === 'low'"
                class="px-2 py-0.5 bg-amber-500/90 text-white text-[10px] font-semibold rounded"
              >
                Últimas uds.
              </span>
              <span 
                v-if="product.badge === 'hot'"
                class="px-2 py-0.5 bg-rose-500/90 text-white text-[10px] font-semibold rounded"
              >
                Top ventas
              </span>
              <span 
                v-if="product.discount"
                class="px-2 py-0.5 bg-gray-900/80 text-white text-[10px] font-semibold rounded"
              >
                -{{ product.discount }}%
              </span>
            </div>
            
            <!-- Quick add overlay -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-3">
              <button 
                @click="quickAddToCart(product)"
                class="px-4 py-2 bg-white/95 text-gray-900 text-xs font-semibold rounded-lg shadow-lg transform translate-y-2 group-hover:translate-y-0 transition-all duration-300 flex items-center gap-1.5 hover:bg-white"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Agregar
              </button>
            </div>
          </div>
          
          <!-- Info del producto -->
          <div class="p-3">
            <p class="text-gray-400 text-[10px] uppercase tracking-wider mb-0.5">{{ product.category }}</p>
            <h3 class="font-medium text-gray-800 text-[13px] line-clamp-2 mb-2 leading-snug min-h-[2.25rem]">
              {{ product.name }}
            </h3>
            
            <div class="flex items-end justify-between">
              <div>
                <p v-if="product.originalPrice" class="text-gray-400 text-[10px] line-through">
                  ${{ product.originalPrice.toLocaleString() }}
                </p>
                <p class="text-gray-900 font-semibold text-sm">
                  ${{ product.price.toLocaleString() }}
                </p>
              </div>
              <div class="flex items-center gap-0.5 text-gray-400 text-[10px]">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                </svg>
                {{ product.stock }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Botón ver más - más sutil -->
      <div class="text-center mt-10">
        <router-link 
          to="/portal/catalogo"
          class="inline-flex items-center gap-2 px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white text-sm font-medium rounded-lg transition-all duration-300 group hover:shadow-lg hover:shadow-gray-900/20"
        >
          Explorar catálogo completo
          <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </router-link>
      </div>
    </div>

    <!-- =========================================================================
         BANNER CTA - Asesoría (sutil y corporativo)
    ========================================================================== -->
    <div class="relative bg-gradient-to-r from-[#18181B] to-[#1F1F23] rounded-xl p-5 sm:p-6 overflow-hidden">
      <!-- Decoración sutil -->
      <div class="absolute top-0 right-0 w-48 h-48 bg-gradient-to-bl from-[#C9A962]/10 to-transparent rounded-full blur-3xl"></div>
      
      <div class="relative flex flex-col sm:flex-row items-center gap-4 sm:gap-6">
        <!-- Icono sin animación -->
        <div class="shrink-0 w-12 h-12 bg-[#C9A962]/10 rounded-xl flex items-center justify-center">
          <svg class="w-5 h-5 text-[#C9A962]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        
        <div class="flex-1 text-center sm:text-left">
          <h3 class="text-base sm:text-lg font-medium text-white/90 mb-0.5">
            ¿Necesitas asesoría personalizada?
          </h3>
          <p class="text-white/40 text-sm">
            Nuestro equipo B2B está disponible para ayudarte
          </p>
        </div>
        
        <a 
          href="https://wa.me/573001234567?text=Hola,%20soy%20mayorista%20y%20necesito%20asesoría"
          target="_blank"
          class="shrink-0 px-5 py-2.5 bg-white/10 hover:bg-white/15 text-white text-sm font-medium rounded-lg transition-all duration-300 flex items-center gap-2 hover:shadow-lg"
        >
          <svg class="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
          Contactar
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'B2BDashboard',
  setup() {
    // =========================================================================
    // STATE
    // =========================================================================
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{"nombre": "Mayorista"}')
    })

    const cartCount = ref(0)
    const currentSlide = ref(0)
    let slideInterval = null

    // Productos habituales (simulados - en producción vendrían de API)
    const frequentProducts = ref([
      { id: 1, name: 'Extensión Clip-in Rubio #613', price: 185000, image: 'https://placehold.co/300x300/1a1a1a/C9A962?text=EXT', lastQty: 5 },
      { id: 2, name: 'Shampoo Sin Sulfatos 500ml', price: 45000, image: 'https://placehold.co/300x300/1a1a1a/C9A962?text=SHP', lastQty: 12 },
      { id: 3, name: 'Tratamiento Keratina Pro', price: 125000, image: 'https://placehold.co/300x300/1a1a1a/C9A962?text=KRT', lastQty: 3 },
      { id: 4, name: 'Plancha Profesional Titanio', price: 320000, image: 'https://placehold.co/300x300/1a1a1a/C9A962?text=PLN', lastQty: 2 },
      { id: 5, name: 'Aceite de Argán 100ml', price: 38000, image: 'https://placehold.co/300x300/1a1a1a/C9A962?text=ARG', lastQty: 8 },
    ])

    // Productos destacados (simulados - en producción vendrían de API)
    const featuredProducts = ref([
      { id: 101, name: 'Extensión Tape-in Premium 60cm', price: 245000, originalPrice: 290000, discount: 15, category: 'Extensiones', badge: 'new', stock: 28, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=TAPE' },
      { id: 102, name: 'Kit Balayage Profesional', price: 189000, category: 'Coloración', badge: 'hot', stock: 12, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=BAL' },
      { id: 103, name: 'Secador Ionico 2400W', price: 285000, category: 'Herramientas', badge: 'low', stock: 4, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=SEC' },
      { id: 104, name: 'Mascarilla Hidratante 1L', price: 68000, originalPrice: 85000, discount: 20, category: 'Tratamientos', stock: 45, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=MSK' },
      { id: 105, name: 'Peluca Lace Front Natural', price: 520000, category: 'Pelucas', badge: 'new', stock: 8, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=PLC' },
      { id: 106, name: 'Tinte Orgánico Sin Amoniaco', price: 42000, category: 'Coloración', stock: 65, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=TNT' },
      { id: 107, name: 'Cepillo Térmico Cerámico', price: 95000, category: 'Herramientas', badge: 'hot', stock: 22, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=CEP' },
      { id: 108, name: 'Serum Reparador Puntas', price: 55000, category: 'Tratamientos', badge: 'low', stock: 6, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=SRM' },
      { id: 109, name: 'Extensión Microlink 50cm', price: 198000, category: 'Extensiones', badge: 'new', stock: 18, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=MCL' },
      { id: 110, name: 'Decolorante Premium 500g', price: 75000, originalPrice: 95000, discount: 21, category: 'Coloración', stock: 34, image: 'https://placehold.co/400x500/f5f5f5/1a1a1a?text=DEC' },
    ])

    // =========================================================================
    // SLIDER AUTO-PLAY
    // =========================================================================
    function startSlideshow() {
      slideInterval = setInterval(() => {
        currentSlide.value = (currentSlide.value + 1) % 3
      }, 5000)
    }

    function nextSlide() {
      currentSlide.value = (currentSlide.value + 1) % 3
    }

    function prevSlide() {
      currentSlide.value = (currentSlide.value - 1 + 3) % 3
    }

    // =========================================================================
    // HANDLERS
    // =========================================================================
    function handleProductImageError(event, product) {
      // Placeholder con iniciales del producto
      event.target.src = `https://placehold.co/400x500/f5f5f5/999999?text=${encodeURIComponent(product.name.substring(0, 2).toUpperCase())}`
    }

    function quickAddToCart(product) {
      // TODO: Integrar con servicio de carrito real
      cartCount.value++
      console.log('Agregado al carrito:', product.name)
      
      // Feedback visual temporal
      alert(`✓ ${product.name} agregado al carrito`)
    }

    // =========================================================================
    // LIFECYCLE
    // =========================================================================
    onMounted(() => {
      startSlideshow()
      
      // Cargar contador del carrito desde localStorage
      const savedCart = localStorage.getItem('b2b_cart')
      if (savedCart) {
        try {
          const cart = JSON.parse(savedCart)
          cartCount.value = cart.items?.length || 0
        } catch (e) {
          cartCount.value = 0
        }
      }
    })

    onUnmounted(() => {
      if (slideInterval) {
        clearInterval(slideInterval)
      }
    })

    // =========================================================================
    // RETURN
    // =========================================================================
    return {
      user,
      cartCount,
      currentSlide,
      frequentProducts,
      featuredProducts,
      nextSlide,
      prevSlide,
      handleProductImageError,
      quickAddToCart
    }
  }
}
</script>

<style scoped>
/* Ocultar scrollbar pero mantener funcionalidad */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

/* Line clamp para títulos */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
