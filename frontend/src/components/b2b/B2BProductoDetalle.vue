<template>
  <div class="min-h-screen bg-[#EBEBEB]">
    <!-- Toast notifications -->
    <B2BToast />
    
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center min-h-[70vh]">
      <div class="text-center">
        <div class="relative w-16 h-16 mx-auto mb-4">
          <div class="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
          <div class="absolute inset-0 border-4 border-t-[#1A1A1A] border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin"></div>
        </div>
        <p class="text-gray-400 text-sm">Cargando producto...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="min-h-[60vh] flex items-center justify-center px-4">
      <div class="text-center max-w-md mx-auto bg-white rounded-lg p-8">
        <div class="w-16 h-16 mx-auto bg-red-50 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">Producto no encontrado</h3>
        <p class="text-gray-500 mb-6">{{ error }}</p>
        <router-link to="/portal/catalogo" class="inline-flex items-center gap-2 text-[#007185] font-medium hover:underline">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          Volver al catálogo
        </router-link>
      </div>
    </div>

    <!-- ========================================
         PRODUCT CONTENT - 3 COLUMN LAYOUT
         Galería | Info que vende | Compra sticky
    ======================================== -->
    <div v-else>
      
      <!-- Breadcrumb -->
      <div class="border-b border-gray-200">
        <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <nav class="flex items-center gap-2 text-sm text-gray-400">
            <router-link to="/portal" class="text-[#007185] hover:text-[#C7511F] hover:underline transition-colors">Portal</router-link>
            <span class="text-gray-300">›</span>
            <router-link to="/portal/catalogo" class="text-[#007185] hover:text-[#C7511F] hover:underline transition-colors">Catálogo</router-link>
            <template v-if="producto.categoria">
              <span class="text-gray-300">›</span>
              <router-link :to="`/portal/catalogo?categoria=${producto.categoria.nombre}`" class="text-[#007185] hover:text-[#C7511F] hover:underline transition-colors">{{ producto.categoria.nombre }}</router-link>
            </template>
            <span class="text-gray-300">›</span>
            <span class="text-gray-600 truncate max-w-[300px]">{{ producto.nombre }}</span>
          </nav>
        </div>
      </div>

      <!-- ============================================
           MOBILE VIEW - Mercado Libre Style (lg:hidden)
      ============================================ -->
      <div class="lg:hidden">
        <!-- Mobile Gallery with Swipe -->
        <div class="relative bg-white">
          <!-- Main Swipeable Gallery -->
          <div 
            class="relative aspect-square overflow-hidden"
            @touchstart="handleTouchStart"
            @touchmove="handleTouchMove"
            @touchend="handleTouchEnd"
          >
            <!-- Image Counter Badge -->
            <div class="absolute top-3 left-3 z-20 px-2.5 py-1 bg-black/60 rounded-full">
              <span class="text-white text-xs font-medium">{{ imagenActualIndex + 1 }}/{{ imagenes.length }}</span>
            </div>
            
            <!-- Favorite Button -->
            <button 
              @click="toggleFavorito"
              class="absolute top-3 right-3 z-20 w-10 h-10 bg-white rounded-full shadow-md flex items-center justify-center"
              :class="esFavorito ? 'text-rose-500' : 'text-gray-400'"
            >
              <svg class="w-5 h-5" :fill="esFavorito ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              </svg>
            </button>
            
            <!-- Share Button -->
            <button 
              @click="compartirProducto"
              class="absolute top-3 right-16 z-20 w-10 h-10 bg-white rounded-full shadow-md flex items-center justify-center text-gray-500"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
              </svg>
            </button>
            
            <!-- Main Image -->
            <video
              v-if="isVideoUrl(imagenActual) && !hasMediaError(imagenActual)"
              :src="imagenActual"
              class="w-full h-full object-contain bg-white"
              playsinline
              controls
              @error="handleVideoError(imagenActual)"
            ></video>
            <img 
              v-else
              :src="getDisplayMedia(imagenActual)" 
              :alt="producto.nombre"
              class="w-full h-full object-contain bg-white"
              @error="handleImageError(imagenActual, $event)"
            />
          </div>
          
          <!-- Dot Indicators -->
          <div v-if="imagenes.length > 1" class="flex justify-center gap-1.5 py-3 bg-white">
            <button 
              v-for="(img, idx) in imagenes" 
              :key="idx"
              @click="imagenActualIndex = idx"
              class="w-2 h-2 rounded-full transition-all"
              :class="imagenActualIndex === idx ? 'bg-[#1A1A1A] w-5' : 'bg-gray-300'"
            ></button>
          </div>
        </div>
        
        <!-- Mobile Product Info -->
        <div class="bg-white px-4 pb-4">
          <!-- Condition & Sold Count -->
          <div class="flex items-center gap-2 text-xs text-gray-500 mb-2">
            <span>Nuevo</span>
            <span>|</span>
            <span>Mayorista</span>
            <span v-if="stockDisponible <= 20" class="text-orange-600 font-medium">• Últimas {{ stockDisponible }} uds</span>
          </div>
          
          <!-- Title -->
          <h1 class="text-base font-normal text-gray-900 leading-snug mb-3">
            {{ producto.nombre }}
          </h1>
          
          <!-- Price Section -->
          <div class="mb-3">
            <!-- Original Price (tachado) -->
            <p v-if="descuento > 0" class="text-sm text-gray-400 line-through">
              ${{ formatPrice(precioRetail) }}
            </p>
            
            <!-- Current Price + Discount -->
            <div class="flex items-baseline gap-2">
              <span class="text-[32px] font-light text-gray-900">${{ formatPrice(precioUnitarioActual) }}</span>
              <span v-if="descuentoTotal > 0" class="text-base font-medium text-green-600">{{ descuentoTotal }}% OFF</span>
            </div>
            
            <!-- Cuotas info -->
            <p class="text-sm text-gray-600 mt-1">
              en <span class="text-green-600 font-medium">12x ${{ formatPrice(Math.ceil(precioUnitarioActual / 12)) }}</span> sin interés
            </p>
          </div>
          
          <!-- Envío Gratis -->
          <div class="flex items-center gap-2 mb-4">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/>
            </svg>
            <span class="text-green-600 text-sm font-medium">Envío gratis a todo el país</span>
          </div>
          
          <!-- Quick Specs -->
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="px-2.5 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
              Lote mín: {{ loteMinimo }} uds
            </span>
            <span v-if="producto.tipo" class="px-2.5 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
              {{ producto.tipo }}
            </span>
            <span v-if="producto.origen" class="px-2.5 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
              {{ producto.origen }}
            </span>
          </div>

          <!-- Variantes (Mobile) -->
          <div v-if="tieneVariantes" class="border border-gray-200 rounded-lg p-3 bg-white/80 mb-4">
            <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-2">Variantes</p>
            <div v-if="coloresDisponibles.length" class="mb-3">
              <div class="flex items-center justify-between mb-2">
                <p class="text-xs text-gray-500">Color</p>
                <span class="text-[11px] text-gray-600">{{ colorSeleccionadoLabel }}</span>
              </div>
              <div class="flex flex-wrap gap-2">
                <button
                  v-if="varianteBase"
                  type="button"
                  class="w-9 h-9 rounded-full border transition-all flex items-center justify-center"
                  :class="colorSeleccionado === BASE_VARIANTE_VALUE ? 'border-[#007185] ring-2 ring-[#007185]/30' : 'border-gray-200 hover:border-[#007185]/40'"
                  @click="colorSeleccionado = BASE_VARIANTE_VALUE; largoSeleccionado = ''"
                  :style="{ backgroundColor: COLOR_BASE_HEX }"
                >
                  <svg
                    v-if="colorSeleccionado === BASE_VARIANTE_VALUE"
                    class="w-4 h-4"
                    :class="isLightColor(COLOR_BASE_HEX) ? 'text-gray-900' : 'text-white'"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
                <button
                  v-for="color in coloresDisponibles"
                  :key="color"
                  type="button"
                  class="w-9 h-9 rounded-full border transition-all flex items-center justify-center"
                  :class="colorSeleccionado === color ? 'border-[#007185] ring-2 ring-[#007185]/30' : 'border-gray-200 hover:border-[#007185]/40'"
                  @click="colorSeleccionado = color"
                  :style="{ backgroundColor: getColorHex(color) }"
                >
                  <svg
                    v-if="colorSeleccionado === color"
                    class="w-4 h-4"
                    :class="isLightColor(getColorHex(color)) ? 'text-gray-900' : 'text-white'"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
            </div>
            <div v-if="largosDisponibles.length">
              <p class="text-xs text-gray-500 mb-2">Largo</p>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="largo in largosDisponibles"
                  :key="largo"
                  type="button"
                  class="px-2.5 py-1.5 text-xs rounded-md border transition-colors"
                  :class="String(largoSeleccionado) === String(largo) ? 'border-[#007185] text-[#007185] bg-[#F7FAFA]' : 'border-gray-200 text-gray-700 hover:border-[#007185]/40'"
                  @click="largoSeleccionado = largo"
                >
                  {{ largo }}"
                </button>
              </div>
            </div>
            <p v-if="selectionIncomplete" class="text-[11px] text-orange-600 mt-2">Selecciona una variante para continuar.</p>
          </div>
          
          <!-- Quantity Selector Mobile - Card compacta -->
          <div class="border border-gray-200 rounded-xl p-4 mt-4 bg-white">
            <!-- Header -->
            <p class="text-xs text-gray-500 uppercase tracking-wider font-medium mb-3">Selecciona cantidad</p>
            
            <!-- Quick Quantity Buttons -->
            <div class="grid grid-cols-4 gap-2 mb-4">
              <button 
                v-for="lote in lotesRapidos" 
                :key="lote"
                @click="seleccionarLote(lote)"
                :disabled="lote > stockDisponible"
                class="py-2.5 text-sm font-medium rounded-lg border-2 transition-all"
                :class="cantidad === lote 
                  ? 'bg-[#1A1A1A] text-white border-[#1A1A1A]' 
                  : lote > stockDisponible 
                    ? 'bg-gray-50 text-gray-300 border-gray-100 cursor-not-allowed' 
                    : 'bg-white text-gray-700 border-gray-200 hover:border-[#1A1A1A]'"
              >
                {{ lote }}
              </button>
            </div>
            
            <!-- Custom Quantity Row -->
            <div class="flex items-center gap-3 mb-4">
              <span class="text-sm text-gray-500">Otra cantidad:</span>
              <div class="flex items-center border-2 border-gray-200 rounded-lg overflow-hidden">
                <button 
                  @click="decrementarLote"
                  :disabled="cantidad <= loteMinimo"
                  class="w-10 h-10 flex items-center justify-center text-gray-600 hover:bg-gray-50 disabled:opacity-30"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                  </svg>
                </button>
                <span class="w-12 text-center font-bold text-gray-900">{{ cantidad }}</span>
                <button 
                  @click="incrementarLote"
                  :disabled="cantidad + loteMinimo > stockDisponible"
                  class="w-10 h-10 flex items-center justify-center text-gray-600 hover:bg-gray-50 disabled:opacity-30"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Divider -->
            <div class="border-t border-gray-100 my-4"></div>
            
            <!-- Total Row -->
            <div class="flex justify-between items-center mb-4">
              <div>
                <p class="text-sm text-gray-500">Total</p>
                <p class="text-xs text-gray-400">{{ cantidad }} unidades</p>
              </div>
              <div class="text-right">
                <p class="text-2xl font-bold text-gray-900">${{ formatPrice(subtotal) }}</p>
                <p v-if="ahorroTotal > 0" class="text-sm text-green-600 font-medium">
                  Ahorras ${{ formatPrice(ahorroTotal) }}
                </p>
              </div>
            </div>
            
            <!-- Add to Cart Button -->
            <button 
              @click="agregarAlCarrito"
              :disabled="stockDisponible < loteMinimo || agregando || selectionIncomplete"
              class="w-full py-4 bg-[#1A1A1A] hover:bg-black text-white font-bold text-base rounded-lg flex items-center justify-center gap-2 disabled:opacity-50 transition-colors"
            >
              <svg v-if="!agregando" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
              </svg>
              <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              {{ agregando ? 'Agregando...' : 'Agregar al pedido' }}
            </button>
          </div>
          
          <!-- Descripción expandible -->
          <details v-if="producto.descripcion || tieneCaracteristicas" class="border-t border-gray-100 pt-4">
            <summary class="flex items-center justify-between py-2 cursor-pointer">
              <span class="text-sm font-medium text-gray-900">Ver descripción y características</span>
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </summary>
            <div class="pt-3 pb-2">
              <div v-if="producto.descripcion" class="text-sm text-gray-600 mb-4" v-html="producto.descripcion"></div>
              <div v-if="tieneCaracteristicas" class="space-y-2">
                <div v-if="producto.tipo" class="flex text-sm">
                  <span class="text-gray-500 w-24">Tipo:</span>
                  <span class="text-gray-900">{{ producto.tipo }}</span>
                </div>
                <div v-if="producto.color" class="flex text-sm">
                  <span class="text-gray-500 w-24">Color:</span>
                  <span class="text-gray-900">{{ producto.color }}</span>
                </div>
                <div v-if="producto.largo" class="flex text-sm">
                  <span class="text-gray-500 w-24">Largo:</span>
                  <span class="text-gray-900">{{ producto.largo }}</span>
                </div>
                <div v-if="producto.origen" class="flex text-sm">
                  <span class="text-gray-500 w-24">Origen:</span>
                  <span class="text-gray-900">{{ producto.origen }}</span>
                </div>
                <div v-if="producto.calidad" class="flex text-sm">
                  <span class="text-gray-500 w-24">Calidad:</span>
                  <span class="text-gray-900">{{ producto.calidad }}</span>
                </div>
                <div v-if="producto.peso_gramos" class="flex text-sm">
                  <span class="text-gray-500 w-24">Peso:</span>
                  <span class="text-gray-900">{{ producto.peso_gramos }}g</span>
                </div>
              </div>
            </div>
          </details>
          
          <!-- Precios por volumen expandible -->
          <details class="border-t border-gray-100 pt-2">
            <summary class="flex items-center justify-between py-2 cursor-pointer">
              <span class="text-sm font-medium text-gray-900">Precios por volumen</span>
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </summary>
            <div class="pt-2 pb-2 space-y-2">
              <div 
                v-for="tier in preciosPorVolumen" 
                :key="tier.cantidad"
                @click="seleccionarLote(tier.cantidad)"
                class="flex items-center justify-between p-2 rounded-lg cursor-pointer transition-colors"
                :class="cantidad >= tier.cantidad ? 'bg-[#FAF5F2]' : 'hover:bg-gray-50'"
              >
                <div>
                  <span class="font-medium text-gray-900">{{ tier.cantidad }} uds</span>
                  <span class="text-xs text-gray-500 ml-2">{{ tier.descripcion }}</span>
                </div>
                <span class="font-bold text-gray-900">${{ formatPrice(tier.precioUnitario) }}/ud</span>
              </div>
            </div>
          </details>
          
          <!-- WhatsApp consulta -->
          <a 
            :href="whatsappUrl"
            target="_blank"
            class="flex items-center justify-center gap-2 w-full py-3 mt-4 border border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50"
          >
            <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 24 24">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
            </svg>
            <span class="font-medium text-sm">Consultar por WhatsApp</span>
          </a>
        </div>
        
        <!-- Mobile Related Products -->
        <div v-if="productosRelacionados.length > 0" class="mt-3 px-4 pb-6">
          <div class="flex items-center justify-between mb-3">
            <h2 class="font-bold text-base text-gray-900">Productos relacionados</h2>
            <router-link to="/portal/catalogo" class="text-sm text-[#8B7355] font-medium">
              Ver más
            </router-link>
          </div>
          <div class="flex gap-3 overflow-x-auto pb-2 -mx-4 px-4 scrollbar-hide">
            <router-link 
              v-for="prod in productosRelacionados" 
              :key="prod.id"
              :to="`/portal/producto/${prod.id}`"
              class="flex-shrink-0 w-36 border border-gray-100 rounded-lg overflow-hidden bg-white"
            >
              <div class="aspect-square bg-gray-50 overflow-hidden">
                <img 
                  :src="getDisplayMedia(prod.imagen_principal)" 
                  :alt="prod.nombre"
                  class="w-full h-full object-cover"
                  @error="handleImageError(prod.imagen_principal, $event)"
                />
              </div>
              <div class="p-2.5">
                <p class="text-gray-800 text-xs line-clamp-2 leading-snug mb-1.5 min-h-[2rem]">{{ prod.nombre }}</p>
                <p class="text-gray-900 font-bold text-sm">${{ formatPrice(prod.precio_mayorista || prod.monto_precio) }}</p>
                <p class="text-green-600 text-[10px] font-medium mt-0.5">Envío gratis</p>
              </div>
            </router-link>
          </div>
        </div>
      </div>

      <!-- ============================================
           DESKTOP VIEW - Original Layout (hidden on mobile)
      ============================================ -->
      <div class="hidden lg:block max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-5 lg:py-6">
        
        <!-- Main white card wrapping all product content -->
        <div class="bg-white rounded-lg overflow-hidden">
          <div class="p-4 sm:p-6 lg:p-8">
            <div class="grid grid-cols-12 gap-6 lg:gap-8">
          
          <!-- ====================================
               COLUMN 1: GALERÍA - Thumbnails verticales estilo Amazon
          ==================================== -->
          <div class="col-span-5">
            <div class="sticky top-24">
              
              <div class="flex gap-3">
                <!-- Thumbnails Verticales (izquierda) - estilo Amazon -->
                <div v-if="imagenes.length > 1" class="flex flex-col gap-1.5 flex-shrink-0">
                  <button 
                    v-for="(img, idx) in imagenes" 
                    :key="idx"
                    @click="imagenActualIndex = idx"
                    @mouseenter="imagenActualIndex = idx"
                    class="w-[52px] h-[52px] rounded overflow-hidden border transition-all flex-shrink-0"
                    :class="imagenActualIndex === idx ? 'border-[#007185] shadow-sm ring-1 ring-[#007185]' : 'border-gray-200 hover:border-[#007185]'"
                  >
                    <video
                      v-if="isVideoUrl(img) && !hasMediaError(img)"
                      :src="img"
                      class="w-full h-full object-cover"
                      muted playsinline preload="metadata"
                      @error="handleVideoError(img)"
                    ></video>
                    <img
                      v-else
                      :src="getDisplayMedia(img)"
                      :alt="`Vista ${idx + 1}`"
                      class="w-full h-full object-cover"
                      @error="handleImageError(img, $event)"
                    />
                  </button>
                </div>
                
                <!-- Main Image -->
                <div class="flex-1 relative">
                  <!-- Badges -->
                  <div class="absolute top-3 left-3 z-10 flex flex-col gap-2">
                    <span class="px-2.5 py-1 bg-[#1A1A1A] text-white text-[10px] font-bold uppercase tracking-wider rounded">
                      Mayorista
                    </span>
                    <span 
                      v-if="stockDisponible <= 10 && stockDisponible > 0"
                      class="px-2.5 py-1 bg-orange-500 text-white text-[10px] font-bold rounded animate-pulse"
                    >
                      Últimas {{ stockDisponible }} uds
                    </span>
                  </div>
                  
                  <!-- Favorite -->
                  <button 
                    @click="toggleFavorito"
                    class="absolute top-3 right-3 z-10 w-9 h-9 bg-white rounded-full shadow flex items-center justify-center hover:scale-110 transition-transform"
                    :class="esFavorito ? 'text-rose-500' : 'text-gray-400'"
                  >
                    <svg class="w-5 h-5" :fill="esFavorito ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                    </svg>
                  </button>
                  
                  <!-- Imagen Principal -->
                  <div class="aspect-square max-h-[480px] rounded-lg overflow-hidden">
                    <video
                      v-if="isVideoUrl(imagenActual) && !hasMediaError(imagenActual)"
                      :src="imagenActual"
                      class="w-full h-full object-cover"
                      playsinline
                      controls
                      @error="handleVideoError(imagenActual)"
                    ></video>
                    <img 
                      v-else
                      :src="getDisplayMedia(imagenActual)" 
                      :alt="producto.nombre"
                      class="w-full h-full object-cover cursor-zoom-in"
                      @error="handleImageError(imagenActual, $event)"
                      @click="abrirZoom"
                    />
                  </div>
                </div>
              </div>
              
              <!-- Thumbnails Horizontal Mobile -->
              <div v-if="imagenes.length > 1" class="flex sm:hidden gap-1.5 mt-3 overflow-x-auto pb-2 scrollbar-hide">
                <button 
                  v-for="(img, idx) in imagenes" 
                  :key="idx"
                  @click="imagenActualIndex = idx"
                  class="flex-shrink-0 w-12 h-12 rounded overflow-hidden border transition-all"
                  :class="imagenActualIndex === idx ? 'border-[#007185] ring-1 ring-[#007185]' : 'border-gray-200'"
                >
                  <video
                    v-if="isVideoUrl(img) && !hasMediaError(img)"
                    :src="img"
                    class="w-full h-full object-cover"
                    muted
                    playsinline
                    preload="metadata"
                    @error="handleVideoError(img)"
                  ></video>
                  <img
                    v-else
                    :src="getDisplayMedia(img)"
                    :alt="`Vista ${idx + 1}`"
                    class="w-full h-full object-cover"
                    @error="handleImageError(img, $event)"
                  />
                </button>
              </div>
              
              <!-- Compartir / Reportar -->
              <div class="flex items-center gap-4 mt-3 text-xs text-[#007185]">
                <button @click="compartirProducto" class="hover:underline flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"/>
                  </svg>
                  Compartir
                </button>
              </div>
            </div>
          </div>

          <!-- ====================================
               COLUMN 2: INFO DEL PRODUCTO
          ==================================== -->
          <div class="lg:col-span-4 space-y-4">
            
            <!-- Categoría + SKU -->
            <div>
              <div class="flex items-center gap-2 mb-1.5 text-xs">
                <router-link 
                  v-if="producto.categoria"
                  :to="`/portal/catalogo?categoria=${producto.categoria.nombre}`"
                  class="text-[#007185] hover:text-[#C7511F] hover:underline uppercase tracking-wide font-medium"
                >
                  {{ producto.categoria.nombre }}
                </router-link>
                <span v-if="producto.sku" class="text-gray-300">|</span>
                <span v-if="producto.sku" class="text-gray-400 font-mono">
                  REF: {{ producto.sku }}
                </span>
              </div>
              <h1 class="text-xl sm:text-2xl lg:text-[26px] font-normal text-[#0F1111] leading-tight">
                {{ producto.nombre }}
              </h1>
            </div>

            <div class="flex flex-wrap items-center gap-2 text-[10px] sm:text-[11px] uppercase tracking-[0.18em] text-[#7A7A7A]">
              <span class="px-3 py-1 rounded-full bg-[#FAF5F2] border border-[#C9A962]/30 text-[#8B7355]">
                Stock {{ stockDisponible }} uds
              </span>
              <span class="px-3 py-1 rounded-full bg-white border border-gray-200 text-[#5A5A5A]">
                Lote minimo {{ loteMinimo }}
              </span>
              <span v-if="producto.metodo" class="px-3 py-1 rounded-full bg-white border border-gray-200 text-[#5A5A5A]">
                {{ producto.metodo }}
              </span>
            </div>

            <!-- Variantes (Desktop) -->
            <div v-if="tieneVariantes" class="border border-gray-200 rounded-lg p-3 bg-white/80">
              <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-2">Variantes</p>
              <div v-if="coloresDisponibles.length" class="mb-3">
                <div class="flex items-center justify-between mb-2">
                  <p class="text-xs text-gray-500">Color</p>
                  <span class="text-[11px] text-gray-600">{{ colorSeleccionadoLabel }}</span>
                </div>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-if="varianteBase"
                    type="button"
                    class="w-9 h-9 rounded-full border transition-all flex items-center justify-center"
                    :class="colorSeleccionado === BASE_VARIANTE_VALUE ? 'border-[#007185] ring-2 ring-[#007185]/30' : 'border-gray-200 hover:border-[#007185]/40'"
                    @click="colorSeleccionado = BASE_VARIANTE_VALUE; largoSeleccionado = ''"
                    :style="{ backgroundColor: COLOR_BASE_HEX }"
                  >
                    <svg
                      v-if="colorSeleccionado === BASE_VARIANTE_VALUE"
                      class="w-4 h-4"
                      :class="isLightColor(COLOR_BASE_HEX) ? 'text-gray-900' : 'text-white'"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  </button>
                  <button
                    v-for="color in coloresDisponibles"
                    :key="color"
                    type="button"
                    class="w-9 h-9 rounded-full border transition-all flex items-center justify-center"
                    :class="colorSeleccionado === color ? 'border-[#007185] ring-2 ring-[#007185]/30' : 'border-gray-200 hover:border-[#007185]/40'"
                    @click="colorSeleccionado = color"
                    :style="{ backgroundColor: getColorHex(color) }"
                  >
                    <svg
                      v-if="colorSeleccionado === color"
                      class="w-4 h-4"
                      :class="isLightColor(getColorHex(color)) ? 'text-gray-900' : 'text-white'"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  </button>
                </div>
              </div>
              <div v-if="largosDisponibles.length">
                <p class="text-xs text-gray-500 mb-2">Largo</p>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="largo in largosDisponibles"
                    :key="largo"
                    type="button"
                    class="px-2.5 py-1.5 text-xs rounded-md border transition-colors"
                    :class="String(largoSeleccionado) === String(largo) ? 'border-[#007185] text-[#007185] bg-[#F7FAFA]' : 'border-gray-200 text-gray-700 hover:border-[#007185]/40'"
                    @click="largoSeleccionado = largo"
                  >
                    {{ largo }}"
                  </button>
                </div>
              </div>
              <p v-if="selectionIncomplete" class="text-[11px] text-orange-600 mt-2">Selecciona una variante para continuar.</p>
            </div>
            
            <!-- Separador -->
            <hr class="border-gray-200">
            
            <!-- Características Rápidas (datos reales del producto) -->
            <div v-if="tieneCaracteristicas">
              <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Características</h3>
              <ul class="space-y-2">
                <li v-if="producto.tipo" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Tipo: {{ producto.tipo }}
                </li>
                <li v-if="producto.color" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Color: {{ formatColorLabel(producto.color) }}
                </li>
                <li v-if="producto.largo" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Largo: {{ producto.largo }}
                </li>
                <li v-if="producto.origen" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Origen: {{ producto.origen }}
                </li>
                <li v-if="producto.calidad" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Calidad: {{ producto.calidad }}
                </li>
                <li v-if="producto.peso_gramos" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Peso: {{ producto.peso_gramos }}g
                </li>
                <li v-if="producto.metodo" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Método: {{ producto.metodo }}
                </li>
              </ul>
            </div>
            
            <!-- Descripción Corta -->
            <div v-if="producto.descripcion" class="text-gray-600 text-sm leading-relaxed" v-html="producto.descripcion"></div>
            
            <!-- Separador -->
            <hr class="border-gray-200">
            
            <!-- Precios por Volumen - Tabla limpia estilo ML -->
            <div class="border border-gray-200 rounded-lg overflow-hidden">
              <div class="bg-gray-50 px-4 py-2.5 border-b border-gray-200">
                <h3 class="text-xs font-bold text-gray-600 uppercase tracking-wider flex items-center gap-2">
                  <svg class="w-4 h-4 text-[#007185]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                  </svg>
                  Precios por volumen
                </h3>
              </div>
              <table class="w-full text-sm">
                <tbody>
                  <tr 
                    v-for="(tier, idx) in preciosPorVolumen" 
                    :key="tier.cantidad"
                    class="border-b border-gray-100 last:border-0 cursor-pointer transition-colors"
                    :class="cantidad >= tier.cantidad ? 'bg-[#F7FAFA]' : idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'"
                    @click="seleccionarLote(tier.cantidad)"
                  >
                    <td class="px-4 py-2.5 font-bold text-gray-900 w-20">{{ tier.cantidad }} uds</td>
                    <td class="px-4 py-2.5 text-gray-500">{{ tier.descripcion }}</td>
                    <td class="px-4 py-2.5 font-bold text-gray-900 text-right">${{ formatPrice(tier.precioUnitario) }}/ud</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Calificaciones de clientes -->
            <div class="border border-gray-200 rounded-lg p-4">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-xs font-bold text-gray-600 uppercase tracking-wider">Calificaciones</h3>
                <span class="text-xs text-gray-400">{{ promedioFormateado }} / 5</span>
              </div>
              <div class="flex items-center gap-2 mb-3">
                <div class="flex items-center gap-1">
                  <svg v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= promedioRedondeado ? 'text-[#C9A962]' : 'text-gray-200'" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
                <span class="text-xs text-gray-500">{{ resumenResenas.total }} calificaciones</span>
              </div>

              <div v-if="isLoggedIn" class="border border-gray-200 rounded-md p-3 bg-white">
                <p class="text-[11px] text-gray-500 mb-2">Tu calificación</p>
                <div class="flex items-center gap-2 flex-wrap">
                  <button
                    v-for="i in 5"
                    :key="i"
                    type="button"
                    class="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center transition-colors"
                    :class="i <= miRating ? 'bg-[#1A1A1A] text-white' : 'bg-white text-gray-700 hover:bg-gray-50'"
                    @click="miRating = i"
                  >
                    <span class="text-xs font-semibold">{{ i }}</span>
                  </button>
                  <button
                    type="button"
                    class="ml-auto px-3 py-2 text-[11px] uppercase tracking-wider bg-[#1A1A1A] text-white hover:bg-black transition-colors disabled:opacity-50"
                    :disabled="!miRating || enviandoResena"
                    @click="enviarResena"
                  >
                    {{ enviandoResena ? 'Enviando...' : 'Enviar' }}
                  </button>
                </div>
                <p v-if="resenaMensaje" class="text-[11px] text-emerald-600 mt-2">{{ resenaMensaje }}</p>
                <p v-if="resenaError" class="text-[11px] text-red-600 mt-2">{{ resenaError }}</p>
                <p class="text-[10px] text-gray-400 mt-2">Solo clientes con compra pueden calificar. Requiere aprobación.</p>
              </div>
              <div v-else class="text-[11px] text-gray-400">
                Inicia sesión para calificar este producto.
              </div>

              <div class="mt-3">
                <div v-if="resenasLoading" class="space-y-2">
                  <div v-for="i in 3" :key="i" class="h-8 bg-gray-50 rounded"></div>
                </div>
                <div v-else-if="resenasProducto.length" class="space-y-2">
                  <div v-for="resena in resenasProducto" :key="resena.id" class="flex items-center justify-between text-sm text-gray-600">
                    <span class="font-medium text-gray-800">{{ resena.cliente }}</span>
                    <div class="flex items-center gap-1">
                      <svg v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= resena.rating ? 'text-[#C9A962]' : 'text-gray-200'" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    </div>
                  </div>
                </div>
                <div v-else class="text-[11px] text-gray-400">
                  Aún no hay calificaciones aprobadas.
                </div>
              </div>
            </div>
            
            <!-- Ficha Técnica Expandible -->
            <details class="border border-gray-200 rounded-lg group">
              <summary class="px-4 py-3 cursor-pointer flex items-center justify-between hover:bg-gray-50 transition-colors">
                <span class="text-sm font-bold text-gray-700 flex items-center gap-2">
                  <svg class="w-4 h-4 text-[#007185]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                  </svg>
                  Ver ficha técnica completa
                </span>
                <svg class="w-4 h-4 text-gray-400 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </summary>
              <div class="px-4 pb-4 border-t border-gray-200">
                <table class="w-full text-sm mt-2">
                  <tbody>
                    <tr v-if="producto.sku" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500 w-32">Referencia</td>
                      <td class="py-2 font-mono text-gray-900">{{ producto.sku }}</td>
                    </tr>
                    <tr v-if="producto.categoria" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Categoría</td>
                      <td class="py-2 text-gray-900">{{ producto.categoria.nombre }}</td>
                    </tr>
                    <tr v-if="producto.tipo" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Tipo</td>
                      <td class="py-2 text-gray-900">{{ producto.tipo }}</td>
                    </tr>
                    <tr v-if="producto.color" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Color</td>
                      <td class="py-2 text-gray-900">{{ producto.color }}</td>
                    </tr>
                    <tr v-if="producto.largo" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Largo</td>
                      <td class="py-2 text-gray-900">{{ producto.largo }}</td>
                    </tr>
                    <tr v-if="producto.origen" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Origen</td>
                      <td class="py-2 text-gray-900">{{ producto.origen }}</td>
                    </tr>
                    <tr v-if="producto.calidad" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Calidad</td>
                      <td class="py-2 text-gray-900">{{ producto.calidad }}</td>
                    </tr>
                    <tr v-if="producto.metodo" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Método</td>
                      <td class="py-2 text-gray-900">{{ producto.metodo }}</td>
                    </tr>
                    <tr v-if="producto.peso_gramos" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Peso</td>
                      <td class="py-2 text-gray-900">{{ producto.peso_gramos }}g</td>
                    </tr>
                    <tr class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Stock</td>
                      <td class="py-2 font-semibold text-gray-900">{{ stockDisponible }} uds</td>
                    </tr>
                    <tr>
                      <td class="py-2 text-gray-500">Lote mínimo</td>
                      <td class="py-2 font-semibold text-gray-900">{{ loteMinimo }} uds</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </details>
          </div>

          <!-- ====================================
               COLUMN 3: COMPRA STICKY
          ==================================== -->
          <div class="lg:col-span-3">
            <div class="lg:sticky lg:top-24 space-y-3">
              
              <!-- Card de Compra Principal -->
              <div class="border border-gray-200 rounded-lg overflow-hidden shadow-sm">
                
                <!-- Header con precio -->
                <div class="bg-[#1A1A1A] text-white p-4 sm:p-5">
                  <p class="text-[11px] text-gray-400 uppercase tracking-wider font-bold mb-1">Precio Mayorista</p>
                  <div class="flex items-baseline gap-1.5">
                    <span class="text-[32px] font-bold leading-none transition-all duration-300">${{ formatPrice(precioUnitarioActual) }}</span>
                    <span class="text-gray-400 text-sm">/unidad</span>
                  </div>
                  <p v-if="descuentoTotal > 0" class="text-emerald-400 text-sm mt-1.5 font-medium">
                    {{ descuentoTotal }}% menos que precio al público
                  </p>
                </div>
                
                <!-- Selector de Cantidad -->
                <div class="p-4 sm:p-5 border-b border-gray-100 bg-white">
                  <label class="text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-2.5 block">
                    Cantidad (mín. {{ loteMinimo }})
                  </label>
                  
                  <!-- Botones Rápidos -->
                  <div class="flex flex-wrap gap-1.5 mb-3">
                    <button 
                      v-for="lote in lotesRapidos" 
                      :key="lote"
                      @click="seleccionarLote(lote)"
                      :disabled="lote > stockDisponible"
                      class="px-3 py-1.5 text-sm font-medium rounded-md border transition-all"
                      :class="cantidad === lote 
                        ? 'bg-[#1A1A1A] text-white border-[#1A1A1A]' 
                        : lote > stockDisponible 
                          ? 'bg-gray-50 text-gray-300 border-gray-200 cursor-not-allowed' 
                          : 'bg-white text-gray-700 border-gray-300 hover:border-[#007185] hover:text-[#007185]'"
                    >
                      {{ lote }}
                    </button>
                  </div>
                  
                  <!-- Input Cantidad -->
                  <div class="flex items-center border border-gray-300 rounded-md overflow-hidden">
                    <button 
                      @click="decrementarLote"
                      :disabled="cantidad <= loteMinimo"
                      class="w-11 h-11 flex items-center justify-center hover:bg-gray-100 transition-colors disabled:opacity-30 border-r border-gray-200"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                      </svg>
                    </button>
                    <input 
                      type="number" 
                      v-model.number="cantidad" 
                      :min="loteMinimo" 
                      :max="stockDisponible"
                      :step="loteMinimo"
                      class="flex-1 text-center font-bold text-lg py-2 focus:outline-none bg-gray-50"
                    />
                    <button 
                      @click="incrementarLote"
                      :disabled="cantidad + loteMinimo > stockDisponible"
                      class="w-11 h-11 flex items-center justify-center hover:bg-gray-100 transition-colors disabled:opacity-30 border-l border-gray-200"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                      </svg>
                    </button>
                  </div>
                  <p class="text-[11px] text-gray-400 mt-2 text-center">
                    Stock: {{ stockDisponible }} uds
                  </p>
                </div>
                
                <!-- Total -->
                <div class="p-4 sm:p-5 bg-white border-b border-gray-100">
                  <div class="flex justify-between text-sm text-gray-500 mb-1.5">
                    <span>{{ cantidad }} uds × ${{ formatPrice(precioUnitarioActual) }}</span>
                  </div>
                  <div class="flex justify-between items-baseline">
                    <span class="text-sm font-medium text-gray-600">Total:</span>
                    <span class="text-[26px] font-bold text-[#0F1111]">${{ formatPrice(subtotal) }}</span>
                  </div>
                  <p v-if="ahorroTotal > 0" class="text-emerald-600 text-sm font-medium mt-1 text-right">
                    Ahorras ${{ formatPrice(ahorroTotal) }}
                  </p>
                </div>
                
                <!-- CTA -->
                <div class="p-4 sm:p-5 bg-white">
                  <button 
                    @click="agregarAlCarrito"
                    :disabled="stockDisponible < loteMinimo || agregando || selectionIncomplete"
                    class="w-full py-3.5 bg-[#1A1A1A] hover:bg-black text-white font-bold text-base rounded-md flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <svg v-if="!agregando" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
                    </svg>
                    <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                    </svg>
                    {{ agregando ? 'Agregando...' : 'Agregar al pedido' }}
                  </button>
                </div>
              </div>
              
              <!-- Secundarios -->
              <div class="flex gap-2">
                <a 
                  :href="whatsappUrl"
                  target="_blank"
                  class="flex-1 py-3 px-4 border border-gray-300 text-gray-700 font-medium rounded-md flex items-center justify-center gap-2 transition-colors hover:bg-gray-50 hover:border-gray-400 text-sm"
                >
                  <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                  </svg>
                  Consultar
                </a>
                <button 
                  @click="toggleFavorito"
                  class="w-11 h-11 rounded-md flex items-center justify-center border transition-all"
                  :class="esFavorito ? 'border-rose-300 bg-rose-50 text-rose-500' : 'border-gray-300 text-gray-400 hover:border-gray-400 hover:text-gray-500'"
                >
                  <svg class="w-5 h-5" :fill="esFavorito ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                  </svg>
                </button>
              </div>
              
              <!-- Medios de Pago -->
              <div class="border border-gray-200 rounded-lg p-4 bg-white">
                <h4 class="text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-3">Medios de pago</h4>
                
                <!-- Transferencias digitales -->
                <div class="mb-4">
                  <p class="text-xs text-gray-500 mb-2">Transferencias</p>
                  <div class="flex flex-wrap items-center gap-2">
                    <!-- Nequi -->
                    <div class="h-7 px-2 bg-[#DF0073] rounded flex items-center justify-center">
                      <span class="text-white text-[11px] font-bold">Nequi</span>
                    </div>
                    <!-- Daviplata -->
                    <div class="h-7 px-2 bg-[#ED1C24] rounded flex items-center justify-center">
                      <span class="text-white text-[11px] font-bold">Daviplata</span>
                    </div>
                    <!-- Bancolombia -->
                    <div class="h-7 px-2 bg-[#FFCD00] rounded flex items-center justify-center">
                      <span class="text-[#0033A0] text-[11px] font-bold">Bancolombia</span>
                    </div>
                  </div>
                </div>
                
                <!-- Efectivo -->
                <div class="mb-4">
                  <p class="text-xs text-gray-500 mb-2">Efectivo</p>
                  <div class="flex flex-wrap items-center gap-2">
                    <!-- Efecty -->
                    <div class="h-7 px-2 bg-[#FFCC00] rounded flex items-center justify-center">
                      <span class="text-[#000] text-[11px] font-bold">efecty</span>
                    </div>
                    <!-- Contra entrega -->
                    <div class="h-7 px-2 bg-gray-700 rounded flex items-center justify-center">
                      <span class="text-white text-[10px] font-medium">Contra entrega</span>
                    </div>
                  </div>
                </div>
                
                <!-- Tarjetas de crédito -->
                <div>
                  <p class="text-xs text-gray-500 mb-2">Tarjetas de crédito</p>
                  <div class="flex flex-wrap items-center gap-2">
                    <!-- Visa -->
                    <div class="h-7 w-11 bg-white border border-gray-200 rounded flex items-center justify-center">
                      <span class="text-[#1A1F71] text-[11px] font-bold italic">VISA</span>
                    </div>
                    <!-- Mastercard -->
                    <div class="h-7 w-11 bg-[#F7F7F7] border border-gray-200 rounded flex items-center justify-center overflow-hidden">
                      <div class="flex -space-x-1.5">
                        <div class="w-4 h-4 bg-[#EB001B] rounded-full"></div>
                        <div class="w-4 h-4 bg-[#F79E1B] rounded-full"></div>
                      </div>
                    </div>
                    <!-- PSE -->
                    <div class="h-7 px-2 bg-white border border-gray-200 rounded flex items-center justify-center">
                      <span class="text-[#0033A0] text-[10px] font-bold">PSE</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
          </div>
        </div>
        
        <!-- ========================================
             PRODUCTOS RELACIONADOS - Separate white card
        ======================================== -->
        <div v-if="productosRelacionados.length > 0" class="mt-4 bg-white rounded-lg p-4 sm:p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-bold text-lg sm:text-xl text-gray-900">Productos relacionados</h2>
            <router-link to="/portal/catalogo" class="text-sm text-[#007185] hover:text-[#C7511F] hover:underline font-medium transition-colors">
              Ver todos
            </router-link>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 sm:gap-4">
            <router-link 
              v-for="prod in productosRelacionados" 
              :key="prod.id"
              :to="`/portal/producto/${prod.id}`"
              class="border border-gray-100 rounded-lg overflow-hidden hover:shadow-md transition-shadow duration-200"
            >
              <div class="aspect-square bg-gray-50 overflow-hidden">
                <img 
                  :src="getDisplayMedia(prod.imagen_principal)" 
                  :alt="prod.nombre"
                  class="w-full h-full object-cover"
                  @error="handleImageError(prod.imagen_principal, $event)"
                />
              </div>
              <div class="p-3">
                <p class="text-gray-800 text-[13px] sm:text-sm line-clamp-2 leading-snug mb-2 min-h-[2.25rem]">{{ prod.nombre }}</p>
                <p class="text-[#0F1111] font-bold text-base">${{ formatPrice(prod.precio_mayorista || prod.monto_precio) }}</p>
                <p v-if="prod.precio && prod.precio > (prod.precio_mayorista || prod.monto_precio)" class="text-xs text-gray-400 line-through">
                  ${{ formatPrice(prod.precio) }}
                </p>
                <p class="text-emerald-600 text-xs font-medium mt-1">Envío gratis</p>
              </div>
            </router-link>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productosService, vistosService } from '@/services/productos'
import { obtenerProducto as obtenerProductoB2B, obtenerProductos as obtenerProductosB2B } from '@/services/mayoristas'
import { resenasService } from '@/services/resenas'
import { B2BToast, useToast } from './ui'
import { getImageUrl } from '@/services/api'
import { formatColorLabel } from '@/utils/colorLabels'
import { getUnitPriceForQty, normalizeB2BTiers } from '@/utils/b2bPricing'

export default {
  name: 'B2BProductoDetalle',
  components: {
    B2BToast
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const toast = useToast()
    
    // ===== LOTES B2B =====
    
    // State
    const producto = ref({})
    const loading = ref(true)
    const error = ref(null)
    const cantidad = ref(1)
    const imagenActualIndex = ref(0)
    const esFavorito = ref(false)
    const agregando = ref(false)
    const productosRelacionados = ref([])
    const mediaErrors = reactive({})
    const colorSeleccionado = ref('')
    const largoSeleccionado = ref('')
    const BASE_VARIANTE_VALUE = '__base__'
    const baseSeleccionada = computed(() => colorSeleccionado.value === BASE_VARIANTE_VALUE)
    const COLOR_BASE_HEX = '#F5EFE7'
    const COLOR_HEX = {
      negro_natural: '#1A1A1A',
      negro_azabache: '#0f0f10',
      castano_oscuro: '#3d2314',
      castano_medio: '#6b4423',
      castano_claro: '#8b6b47',
      castano_chocolate: '#4d2a1f',
      rubio_oscuro: '#a67b5b',
      rubio_medio: '#c19a6b',
      rubio_claro: '#e0c3a0',
      rubio_platino: '#e5e4e2',
      rubio_cenizo: '#b8a898',
      rubio_miel: '#d6a66a',
      pelirrojo: '#8b0000',
      cobrizo: '#b87333',
      borgona: '#722f37',
      rosa: '#f3a8c2',
      azul: '#3f6ea6',
      morado: '#6b4ea1',
      verde: '#3b7a57',
      gris: '#9ca3af',
      ombre: '#8c6f5a',
      balayage: '#c6a36b',
      highlights: '#e6cfa8'
    }

    // Reseñas
    const resenasProducto = ref([])
    const resenasLoading = ref(false)
    const resumenResenas = ref({ promedio: 0, total: 0 })
    const miRating = ref(0)
    const enviandoResena = ref(false)
    const resenaMensaje = ref('')
    const resenaError = ref('')
    
    // User
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{}')
    })

    const isLoggedIn = computed(() => !!user.value?.email)
    
    // Computed
    function normalizeMediaUrl(raw) {
      if (typeof raw !== 'string') return null
      const cleaned = raw.trim()
      if (!cleaned) return null
      const isFilenameOnly = !cleaned.includes('/') && !cleaned.includes('\\')
      const isStaticRelative = cleaned.startsWith('static/') || cleaned.startsWith('uploads/')
      let resolved = cleaned
      if (isFilenameOnly) {
        resolved = `/static/uploads/productos/${cleaned}`
      } else if (isStaticRelative) {
        resolved = `/${cleaned}`
      }
      return getImageUrl(resolved)
    }

    const imagenes = computed(() => {
      const media = []
      const principal = normalizeMediaUrl(
        producto.value.imagen_principal || producto.value.imagen_url || producto.value.imagen
      )
      if (principal) media.push(principal)
      if (producto.value.imagenes && Array.isArray(producto.value.imagenes)) {
        const adicionales = producto.value.imagenes
          .map(img => normalizeMediaUrl(img))
          .filter(img => !!img && img !== principal)
        media.push(...adicionales)
      }
      return media.length > 0 ? [...new Set(media)] : ['/placeholder.png']
    })
    
    const imagenActual = computed(() => {
      const current = imagenes.value[imagenActualIndex.value] || null
      if (!current || current === '/placeholder.png') {
        return '/placeholder.png'
      }
      return current
    })
    
    const tieneCaracteristicas = computed(() => {
      const p = producto.value
      return p.tipo || p.color || p.largo || p.origen || p.calidad || p.peso_gramos || p.metodo
    })

    const variantesDisponibles = computed(() => {
      const variantes = Array.isArray(producto.value?.variantes) ? producto.value.variantes : []
      return variantes.filter(v => v && v.activo !== false)
    })

    const tieneVariantes = computed(() => variantesDisponibles.value.length > 0)

    const varianteBase = computed(() => {
      return variantesDisponibles.value.find(v => !v.color && !v.largo) || null
    })

    const coloresDisponibles = computed(() => {
      const colores = new Set()
      variantesDisponibles.value.forEach((v) => {
        if (v.color) colores.add(v.color)
      })
      return Array.from(colores)
    })

    const largosDisponibles = computed(() => {
      if (colorSeleccionado.value === BASE_VARIANTE_VALUE) return []
      const largos = new Set()
      const source = colorSeleccionado.value
        ? variantesDisponibles.value.filter(v => v.color === colorSeleccionado.value)
        : variantesDisponibles.value
      source.forEach((v) => {
        if (v.largo) largos.add(v.largo)
      })
      return Array.from(largos)
    })

    const variantesFiltradas = computed(() => {
      if (!tieneVariantes.value) return []
      if (colorSeleccionado.value === BASE_VARIANTE_VALUE) {
        return varianteBase.value ? [varianteBase.value] : []
      }
      return variantesDisponibles.value.filter((v) => {
        if (colorSeleccionado.value && v.color !== colorSeleccionado.value) return false
        if (largoSeleccionado.value && String(v.largo) !== String(largoSeleccionado.value)) return false
        return true
      })
    })

    const varianteSeleccionada = computed(() => {
      if (!tieneVariantes.value) return null
      if (colorSeleccionado.value === BASE_VARIANTE_VALUE) {
        return varianteBase.value || {
          id: null,
          sku: producto.value.sku || producto.value.codigo || '',
          color: null,
          largo: null,
          precio_monto: producto.value.precio_mayorista || producto.value.monto_precio || 0,
          precio_moneda: 'COP',
          stock_actual: producto.value.stock_actual ?? 0,
          stock_minimo: producto.value.stock_minimo ?? 0,
          cantidad_minima_mayorista: producto.value.cantidad_minima_mayorista ?? producto.value.cantidad_minima ?? 1,
          descuentos_volumen: producto.value.descuentos_volumen || [],
          imagen_url: producto.value.imagen_principal || null,
          activo: true,
          orden: 0
        }
      }
      if (!colorSeleccionado.value && !largoSeleccionado.value) return null
      return variantesFiltradas.value.find(v => (v.stock_actual ?? 0) > 0) || variantesFiltradas.value[0] || null
    })

    const loteMinimo = computed(() => {
      const raw = varianteSeleccionada.value?.cantidad_minima_mayorista
        ?? producto.value?.cantidad_minima_mayorista
        ?? producto.value?.cantidad_minima
      const value = Number(raw || 1)
      return value > 0 ? value : 1
    })

    const descuentosVolumen = computed(() => {
      const source = varianteSeleccionada.value?.descuentos_volumen?.length
        ? varianteSeleccionada.value.descuentos_volumen
        : producto.value?.descuentos_volumen
      return normalizeB2BTiers(source)
    })

    const lotesRapidos = computed(() => {
      const set = new Set()
      if (loteMinimo.value > 0) set.add(loteMinimo.value)
      descuentosVolumen.value.forEach((tier) => set.add(tier.cantidad_minima))
      return Array.from(set).sort((a, b) => a - b).slice(0, 4)
    })

    const stockDisponible = computed(() => {
      if (tieneVariantes.value) return varianteSeleccionada.value?.stock_actual ?? 0
      return producto.value.stock_actual ?? 0
    })
    
    const precioMayorista = computed(() => {
      if (tieneVariantes.value) return varianteSeleccionada.value?.precio_monto || 0
      return producto.value.precio_mayorista || producto.value.monto_precio || 0
    })
    
    const precioRetail = computed(() => {
      return producto.value.precio || producto.value.monto_precio || precioMayorista.value
    })
    
    const descuento = computed(() => {
      if (precioRetail.value <= precioMayorista.value) return 0
      return Math.round((1 - precioMayorista.value / precioRetail.value) * 100)
    })

    // Descuento total (mayorista + volumen) vs retail
    const descuentoTotal = computed(() => {
      if (precioRetail.value <= 0) return 0
      return Math.round((1 - precioUnitarioActual.value / precioRetail.value) * 100)
    })

    const promedioRedondeado = computed(() => {
      return Math.round(Number(resumenResenas.value.promedio || 0))
    })

    const promedioFormateado = computed(() => {
      const total = Number(resumenResenas.value.total || 0)
      const promedio = Number(resumenResenas.value.promedio || 0)
      return total > 0 ? promedio.toFixed(1) : '0.0'
    })
    
    // Precio unitario con descuento por volumen
    const precioUnitarioActual = computed(() => {
      return getUnitPriceForQty(precioMayorista.value, cantidad.value, descuentosVolumen.value)
    })
    
    const subtotal = computed(() => precioUnitarioActual.value * cantidad.value)
    
    const ahorroTotal = computed(() => {
      return (precioMayorista.value * cantidad.value) - subtotal.value
    })

    const colorSeleccionadoLabel = computed(() => {
      if (colorSeleccionado.value === BASE_VARIANTE_VALUE) return 'Estándar'
      if (!colorSeleccionado.value) return ''
      return formatColorLabel(colorSeleccionado.value)
    })
    
    // Tabla de precios por volumen
    const preciosPorVolumen = computed(() => {
      const base = precioMayorista.value
      const tiers = descuentosVolumen.value.length
        ? descuentosVolumen.value
        : [{ cantidad_minima: loteMinimo.value, descuento_porcentaje: 0 }]

      return tiers.map((tier) => {
        const pct = Number(tier.descuento_porcentaje || 0)
        const cantidad = Number(tier.cantidad_minima)
        const precioUnitario = base * (1 - pct / 100)
        const descripcion = pct > 0
          ? `${pct}% OFF`
          : (cantidad === loteMinimo.value ? 'Lote mínimo' : 'Precio base')

        return {
          cantidad,
          precioUnitario,
          precioTotal: precioUnitario * cantidad,
          descripcion
        }
      })
    })

    const selectionIncomplete = computed(() => {
      return tieneVariantes.value && !varianteSeleccionada.value
    })
    
    const tieneEspecificaciones = computed(() => {
      return producto.value.longitud || producto.value.color || producto.value.textura || producto.value.peso
    })
    
    const whatsappUrl = computed(() => {
      const mensaje = encodeURIComponent(
        `Hola! Me interesa pedir por mayor:\n\n` +
        `📦 Producto: ${producto.value.nombre}\n` +
        `📋 SKU: ${producto.value.sku || 'N/A'}\n` +
        `🔢 Cantidad: ${cantidad.value} unidades\n` +
        `💰 Total: $${formatPrice(subtotal.value)}\n\n` +
        `Link: ${window.location.href}`
      )
      return `https://wa.me/4796657763?text=${mensaje}` // Cambiar número
    })
    
    // Methods
    function formatPrice(value) {
      return Number(value || 0).toLocaleString('es-CO')
    }

    function getColorHex(color) {
      return COLOR_HEX[color] || '#9ca3af'
    }

    function isLightColor(hex) {
      const c = hex.substring(1)
      const rgb = parseInt(c, 16)
      const r = (rgb >> 16) & 0xff
      const g = (rgb >> 8) & 0xff
      const b = (rgb >> 0) & 0xff
      const luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
      return luma > 160
    }
    
    function getPlaceholderImage() {
      return '/placeholder.png'
    }

    function isVideoUrl(url) {
      const value = (url || '').toLowerCase()
      return value.includes('.mp4') || value.includes('.webm') || value.includes('.ogg')
    }

    function hasMediaError(url) {
      return !!mediaErrors[url]
    }

    function getDisplayMedia(url) {
      if (!url || hasMediaError(url)) return getPlaceholderImage()
      return url
    }

    function handleImageError(url, event) {
      if (url) {
        mediaErrors[url] = true
      }
      event.target.src = getPlaceholderImage()
    }

    function handleVideoError(url) {
      if (url) {
        mediaErrors[url] = true
      }
    }
    
    function abrirZoom() {
      // Abrir imagen en nueva pestaña para zoom
      window.open(imagenActual.value, '_blank')
    }

    // ===== MÉTODOS DE LOTES =====
    function seleccionarLote(lote) {
      if (lote <= stockDisponible.value) {
        cantidad.value = lote
      }
    }
    
    function incrementarLote() {
      const nuevo = cantidad.value + loteMinimo.value
      if (nuevo <= stockDisponible.value) {
        cantidad.value = nuevo
      }
    }
    
    function decrementarLote() {
      const nuevo = cantidad.value - loteMinimo.value
      if (nuevo >= loteMinimo.value) {
        cantidad.value = nuevo
      }
    }
    
    // Mantener antiguos para compatibilidad
    function incrementarCantidad() {
      incrementarLote()
    }
    
    function decrementarCantidad() {
      decrementarLote()
    }
    
    function getFavoritosKey() {
      const keyPart = user.value?.email || user.value?.id || user.value?.usuario_id || 'anon'
      return `b2b_favoritos_${keyPart}`
    }

    // Helper para actualizar localStorage de favoritos
    function updateLocalFavoritos(productoId, agregar) {
      let favoritos = []
      try {
        const stored = localStorage.getItem(getFavoritosKey())
        if (stored) favoritos = JSON.parse(stored)
      } catch {}
      
      if (agregar) {
        if (!favoritos.includes(productoId)) {
          favoritos.push(productoId)
        }
      } else {
        favoritos = favoritos.filter(id => id !== productoId)
      }
      localStorage.setItem(getFavoritosKey(), JSON.stringify(favoritos))
      // Dispatch event para que el header se actualice
      window.dispatchEvent(new CustomEvent('favoritos-updated'))
    }
    
    function toggleFavorito() {
      esFavorito.value = !esFavorito.value
      updateLocalFavoritos(producto.value.id, esFavorito.value)
    }

    async function compartirProducto() {
      const url = window.location.href
      const titulo = producto.value?.nombre || 'Producto Kharis'
      if (navigator.share) {
        try {
          await navigator.share({ title: titulo, url })
        } catch (e) { /* user cancelled */ }
      } else {
        try {
          await navigator.clipboard.writeText(url)
          alert('Enlace copiado al portapapeles')
        } catch {
          prompt('Copia este enlace:', url)
        }
      }
    }
    
    // ===== TOUCH SWIPE HANDLERS =====
    const touchStartX = ref(0)
    const touchEndX = ref(0)
    
    function handleTouchStart(e) {
      touchStartX.value = e.touches[0].clientX
    }
    
    function handleTouchMove(e) {
      touchEndX.value = e.touches[0].clientX
    }
    
    function handleTouchEnd() {
      const diff = touchStartX.value - touchEndX.value
      const threshold = 50
      
      if (diff > threshold && imagenActualIndex.value < imagenes.value.length - 1) {
        // Swipe left - next image
        imagenActualIndex.value++
      } else if (diff < -threshold && imagenActualIndex.value > 0) {
        // Swipe right - previous image
        imagenActualIndex.value--
      }
    }
    
    async function agregarAlCarrito() {
      if (agregando.value) return
      
      try {
        agregando.value = true

        const requiereVariante = tieneVariantes.value && !baseSeleccionada.value
        if (requiereVariante && !varianteSeleccionada.value) {
          toast.error('Selecciona una variante disponible antes de continuar', 3000)
          return
        }

        const itemKey = baseSeleccionada.value
          ? producto.value.id
          : (varianteSeleccionada.value?.id || producto.value.id)
        const varianteId = baseSeleccionada.value ? null : (varianteSeleccionada.value?.id || null)
        
        // Agregar al carrito del storage
        const cart = JSON.parse(localStorage.getItem('b2b_cart') || '{"items":[]}')
        const existingIndex = cart.items.findIndex(i => (i.variante_id || i.id || i.producto_id) === itemKey)
        
        if (existingIndex >= 0) {
          cart.items[existingIndex].cantidad += cantidad.value
          cart.items[existingIndex].cantidad_minima_mayorista = loteMinimo.value
          cart.items[existingIndex].descuentos_volumen = descuentosVolumen.value
        } else {
          cart.items.push({
            id: producto.value.id,
            variante_id: varianteId,
            variante_sku: baseSeleccionada.value
              ? (producto.value.sku || producto.value.codigo || '')
              : (varianteSeleccionada.value?.sku || producto.value.sku || producto.value.codigo || ''),
            color: baseSeleccionada.value ? '' : (varianteSeleccionada.value?.color || ''),
            largo: baseSeleccionada.value ? '' : (varianteSeleccionada.value?.largo || ''),
            nombre: producto.value.nombre,
            imagen: varianteSeleccionada.value?.imagen_url || producto.value.imagen_principal,
            precio: precioMayorista.value,
            cantidad_minima_mayorista: loteMinimo.value,
            descuentos_volumen: descuentosVolumen.value,
            cantidad: cantidad.value
          })
        }
        
        localStorage.setItem('b2b_cart', JSON.stringify(cart))
        window.dispatchEvent(new CustomEvent('cart-updated'))
        
        // Feedback visual con toast
        toast.success(`${producto.value.nombre} agregado al carrito (${cantidad.value} unidades)`, 3000)
        
      } catch (err) {
        console.error('Error al agregar al carrito:', err)
      } finally {
        agregando.value = false
      }
    }
    
    async function cargarProducto(id) {
      try {
        loading.value = true
        error.value = null
        
        // Cargar producto con precios mayoristas desde endpoint B2B
        const data = await obtenerProductoB2B(id)
        producto.value = data

        await cargarResumenResenas()
        await cargarResenasProducto()
        
        // Registrar vista
        if (user.value?.email) {
          try {
            await vistosService.registrar(id, user.value.email)
          } catch (err) {
            console.warn('Error registrando vista:', err)
          }
        }
        
        // Verificar si es favorito desde localStorage
        try {
          const stored = localStorage.getItem(getFavoritosKey())
          if (stored) {
            const favs = JSON.parse(stored)
            esFavorito.value = favs.includes(id)
          } else {
            esFavorito.value = false
          }
        } catch {
          esFavorito.value = false
        }
        
        // Cargar productos relacionados (misma categoría) con precios B2B
        if (producto.value.categoria?.nombre || producto.value.categoria_nombre) {
          try {
            const catNombre = producto.value.categoria?.nombre || producto.value.categoria_nombre
            const relacionados = await obtenerProductosB2B({
              categoria: catNombre,
              limit: 6
            })
            productosRelacionados.value = relacionados.filter(p => p.id !== id).slice(0, 5).map(p => ({
              ...p,
              imagen_principal: normalizeMediaUrl(p.imagen_principal || p.imagen_url || p.imagen) || '/placeholder.png'
            }))
          } catch (err) {
            console.warn('Error cargando relacionados:', err)
          }
        }
        
      } catch (err) {
        console.error('Error cargando producto:', err)
        error.value = 'No se pudo cargar el producto'
      } finally {
        loading.value = false
      }
    }

    async function cargarResumenResenas() {
      if (!producto.value?.id) return
      try {
        resumenResenas.value = await resenasService.getResumenProducto(producto.value.id)
      } catch (err) {
        resumenResenas.value = { promedio: 0, total: 0 }
      }
    }

    async function cargarResenasProducto() {
      if (!producto.value?.id) return
      resenasLoading.value = true
      try {
        resenasProducto.value = await resenasService.getResenasProducto(producto.value.id, { limit: 6 })
      } catch (err) {
        resenasProducto.value = []
      } finally {
        resenasLoading.value = false
      }
    }

    async function enviarResena() {
      if (!producto.value?.id || !miRating.value) return
      resenaMensaje.value = ''
      resenaError.value = ''
      enviandoResena.value = true
      try {
        await resenasService.crearResena(producto.value.id, miRating.value)
        resenaMensaje.value = 'Tu calificación quedó pendiente de aprobación.'
        miRating.value = 0
        await cargarResumenResenas()
        await cargarResenasProducto()
      } catch (err) {
        resenaError.value = err?.response?.data?.detail || 'No se pudo enviar la calificación'
      } finally {
        enviandoResena.value = false
      }
    }
    
    // Watch for route changes
    watch(() => route.params.id, (newId) => {
      if (newId) {
        cargarProducto(newId)
        window.scrollTo(0, 0)
      }
    })

    watch(coloresDisponibles, (colores) => {
      if (!tieneVariantes.value) return
      if (!colorSeleccionado.value && varianteBase.value) {
        colorSeleccionado.value = BASE_VARIANTE_VALUE
        return
      }
      if (colores.length === 1) {
        colorSeleccionado.value = colores[0]
      }
      if (
        colorSeleccionado.value &&
        colorSeleccionado.value !== BASE_VARIANTE_VALUE &&
        !colores.includes(colorSeleccionado.value)
      ) {
        colorSeleccionado.value = ''
      }
    })

    watch([colorSeleccionado, largosDisponibles], () => {
      if (largosDisponibles.value.length === 1 && !largoSeleccionado.value) {
        largoSeleccionado.value = largosDisponibles.value[0]
        return
      }
      if (!largoSeleccionado.value) return
      if (!largosDisponibles.value.includes(largoSeleccionado.value)) {
        largoSeleccionado.value = ''
      }
    })

    watch(loteMinimo, (minimo) => {
      if (!minimo) return
      if (cantidad.value < minimo) {
        cantidad.value = minimo
      }
    })
    
    // Lifecycle
    onMounted(() => {
      if (route.params.id) {
        cargarProducto(route.params.id)
      }
    })
    
    return {
      // Constantes
      loteMinimo,
      lotesRapidos,
      // State
      producto,
      loading,
      error,
      cantidad,
      imagenActualIndex,
      imagenActual,
      imagenes,
      esFavorito,
      agregando,
      productosRelacionados,
      tieneCaracteristicas,
      tieneVariantes,
      varianteBase,
      coloresDisponibles,
      largosDisponibles,
      colorSeleccionado,
      largoSeleccionado,
      BASE_VARIANTE_VALUE,
      COLOR_BASE_HEX,
      stockDisponible,
      resenasProducto,
      resenasLoading,
      resumenResenas,
      miRating,
      enviandoResena,
      resenaMensaje,
      resenaError,
      promedioRedondeado,
      promedioFormateado,
      isLoggedIn,
      // Computed precios
      precioMayorista,
      precioRetail,
      descuento,
      descuentoTotal,
      subtotal,
      precioUnitarioActual,
      ahorroTotal,
      preciosPorVolumen,
      selectionIncomplete,
      tieneEspecificaciones,
      whatsappUrl,
      formatColorLabel,
      colorSeleccionadoLabel,
      // Methods
      formatPrice,
      getColorHex,
      isLightColor,
      handleImageError,
      handleVideoError,
      getDisplayMedia,
      isVideoUrl,
      hasMediaError,
      abrirZoom,
      seleccionarLote,
      incrementarLote,
      decrementarLote,
      incrementarCantidad,
      decrementarCantidad,
      toggleFavorito,
      compartirProducto,
      agregarAlCarrito,
      enviarResena,
      // Touch handlers
      handleTouchStart,
      handleTouchMove,
      handleTouchEnd
    }
  }
}
</script>
