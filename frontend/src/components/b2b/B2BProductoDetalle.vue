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
        <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-3">
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
           MAIN PRODUCT AREA - White card on gray bg
      ============================================ -->
      <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-5 lg:py-6">
        
        <!-- Main white card wrapping all product content -->
        <div class="bg-white rounded-lg overflow-hidden">
          <div class="p-4 sm:p-6 lg:p-8">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
          
          <!-- ====================================
               COLUMN 1: GALERÍA - Thumbnails verticales estilo ML
          ==================================== -->
          <div class="lg:col-span-5 xl:col-span-5">
            <div class="lg:sticky lg:top-24">
              
              <div class="flex gap-3">
                <!-- Thumbnails Verticales (izquierda) - estilo ML -->
                <div v-if="imagenes.length > 1" class="hidden sm:flex flex-col gap-2 flex-shrink-0">
                  <button 
                    v-for="(img, idx) in imagenes" 
                    :key="idx"
                    @click="imagenActualIndex = idx"
                    class="w-14 h-14 rounded-md overflow-hidden border-2 transition-all flex-shrink-0"
                    :class="imagenActualIndex === idx ? 'border-[#007185] shadow-sm' : 'border-gray-200 hover:border-[#007185]'"
                  >
                    <img :src="img" :alt="`Vista ${idx + 1}`" class="w-full h-full object-cover"/>
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
                      v-if="producto.stock_actual <= 10 && producto.stock_actual > 0"
                      class="px-2.5 py-1 bg-orange-500 text-white text-[10px] font-bold rounded animate-pulse"
                    >
                      Últimas {{ producto.stock_actual }} uds
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
                  <div class="aspect-[4/5] bg-gray-50 rounded-lg overflow-hidden border border-gray-100">
                    <img 
                      :src="imagenActual" 
                      :alt="producto.nombre"
                      class="w-full h-full object-cover cursor-zoom-in"
                      @error="handleImageError"
                      @click="abrirZoom"
                    />
                  </div>
                </div>
              </div>
              
              <!-- Thumbnails Horizontal Mobile -->
              <div v-if="imagenes.length > 1" class="flex sm:hidden gap-2 mt-3 overflow-x-auto pb-2 scrollbar-hide">
                <button 
                  v-for="(img, idx) in imagenes" 
                  :key="idx"
                  @click="imagenActualIndex = idx"
                  class="flex-shrink-0 w-14 h-14 rounded-md overflow-hidden border-2 transition-all"
                  :class="imagenActualIndex === idx ? 'border-[#007185]' : 'border-gray-200'"
                >
                  <img :src="img" :alt="`Vista ${idx + 1}`" class="w-full h-full object-cover"/>
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
          <div class="lg:col-span-4 xl:col-span-4 space-y-5">
            
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
            
            <!-- Separador -->
            <hr class="border-gray-200">
            
            <!-- Características Rápidas -->
            <div>
              <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Características</h3>
              <ul class="space-y-2">
                <li v-if="producto.textura" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Textura {{ producto.textura }}
                </li>
                <li v-if="producto.longitud" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Largo: {{ producto.longitud }}"
                </li>
                <li v-if="producto.color" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Color: {{ producto.color }}
                </li>
                <li v-if="producto.densidad" class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Densidad: {{ producto.densidad }}
                </li>
                <li class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Calidad premium garantizada
                </li>
                <li class="flex items-center gap-2.5 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-[#007185] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Ideal para reventa
                </li>
              </ul>
            </div>
            
            <!-- Descripción Corta -->
            <div v-if="producto.descripcion" class="text-gray-600 text-sm leading-relaxed" v-html="producto.descripcion"></div>
            
            <!-- Separador -->
            <hr class="border-gray-200">
            
            <!-- Por qué este producto - Business Benefits -->
            <div class="bg-[#F7FAFA] rounded-lg p-4 border border-[#D5DBDB]">
              <h3 class="text-xs font-bold text-gray-600 uppercase tracking-wider mb-3 flex items-center gap-2">
                <svg class="w-4 h-4 text-[#007185]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
                Por qué vende bien
              </h3>
              <ul class="space-y-2 text-sm text-gray-700">
                <li class="flex items-start gap-2">
                  <span class="text-[#007185] font-bold">—</span>
                  Alta demanda en salones
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-[#007185] font-bold">—</span>
                  Margen sugerido: <strong class="text-gray-900">40% - 60%</strong>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-[#007185] font-bold">—</span>
                  Producto de rotación rápida
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-[#007185] font-bold">—</span>
                  Calidad constante por lote
                </li>
              </ul>
            </div>
            
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
                    <tr v-if="producto.marca" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Marca</td>
                      <td class="py-2 text-gray-900">{{ producto.marca }}</td>
                    </tr>
                    <tr v-if="producto.longitud" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Longitud</td>
                      <td class="py-2 text-gray-900">{{ producto.longitud }}"</td>
                    </tr>
                    <tr v-if="producto.color" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Color</td>
                      <td class="py-2 text-gray-900">{{ producto.color }}</td>
                    </tr>
                    <tr v-if="producto.textura" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Textura</td>
                      <td class="py-2 text-gray-900">{{ producto.textura }}</td>
                    </tr>
                    <tr v-if="producto.peso" class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Peso</td>
                      <td class="py-2 text-gray-900">{{ producto.peso }}g</td>
                    </tr>
                    <tr class="border-b border-gray-100">
                      <td class="py-2 text-gray-500">Stock</td>
                      <td class="py-2 font-semibold text-gray-900">{{ producto.stock_actual }} uds</td>
                    </tr>
                    <tr>
                      <td class="py-2 text-gray-500">Lote mínimo</td>
                      <td class="py-2 font-semibold text-gray-900">{{ LOTE_MINIMO }} uds</td>
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
                    {{ descuentoTotal }}% menos que retail
                  </p>
                </div>
                
                <!-- Selector de Cantidad -->
                <div class="p-4 sm:p-5 border-b border-gray-100 bg-white">
                  <label class="text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-2.5 block">
                    Cantidad (mín. {{ LOTE_MINIMO }})
                  </label>
                  
                  <!-- Botones Rápidos -->
                  <div class="flex flex-wrap gap-1.5 mb-3">
                    <button 
                      v-for="lote in [10, 20, 50, 100]" 
                      :key="lote"
                      @click="seleccionarLote(lote)"
                      :disabled="lote > producto.stock_actual"
                      class="px-3 py-1.5 text-sm font-medium rounded-md border transition-all"
                      :class="cantidad === lote 
                        ? 'bg-[#1A1A1A] text-white border-[#1A1A1A]' 
                        : lote > producto.stock_actual 
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
                      :disabled="cantidad <= LOTE_MINIMO"
                      class="w-11 h-11 flex items-center justify-center hover:bg-gray-100 transition-colors disabled:opacity-30 border-r border-gray-200"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                      </svg>
                    </button>
                    <input 
                      type="number" 
                      v-model.number="cantidad" 
                      :min="LOTE_MINIMO" 
                      :max="producto.stock_actual"
                      :step="LOTE_MINIMO"
                      class="flex-1 text-center font-bold text-lg py-2 focus:outline-none bg-gray-50"
                    />
                    <button 
                      @click="incrementarLote"
                      :disabled="cantidad + LOTE_MINIMO > producto.stock_actual"
                      class="w-11 h-11 flex items-center justify-center hover:bg-gray-100 transition-colors disabled:opacity-30 border-l border-gray-200"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                      </svg>
                    </button>
                  </div>
                  <p class="text-[11px] text-gray-400 mt-2 text-center">
                    Stock: {{ producto.stock_actual }} uds
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
                    :disabled="producto.stock_actual < LOTE_MINIMO || agregando"
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
                  :src="prod.imagen_principal || '/placeholder.png'" 
                  :alt="prod.nombre"
                  class="w-full h-full object-cover"
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

        <!-- ========================================
             VIDEOS DEL PRODUCTO - Amazon style
        ======================================== -->
        <div v-if="videosProducto.length > 0" class="mt-4 bg-white rounded-lg p-4 sm:p-6">
          <h2 class="font-bold text-lg sm:text-xl text-gray-900 mb-4">Videos del producto</h2>
          
          <div class="flex flex-col lg:flex-row gap-4">
            <!-- Video player principal -->
            <div class="flex-1">
              <div class="relative bg-black rounded-lg overflow-hidden aspect-video">
                <video 
                  :key="videoActual"
                  :src="videoActual" 
                  controls 
                  preload="metadata"
                  class="w-full h-full object-contain"
                  controlslist="nodownload"
                >
                  Tu navegador no soporta video.
                </video>
              </div>
              <!-- Info bajo el video -->
              <div class="mt-3 flex items-center justify-between">
                <p class="text-sm text-gray-500">{{ producto.nombre }}</p>
                <span class="text-xs text-gray-400">Video {{ videoActualIndex + 1 }} de {{ videosProducto.length }}</span>
              </div>
            </div>
            
            <!-- Lista de videos (sidebar derecho) -->
            <div v-if="videosProducto.length > 1" class="lg:w-72 xl:w-80 flex-shrink-0">
              <p class="text-sm font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <svg class="w-4 h-4 text-[#007185]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                Videos de este producto
              </p>
              <div class="flex lg:flex-col gap-3 overflow-x-auto lg:overflow-x-visible lg:max-h-[400px] lg:overflow-y-auto pb-2 lg:pb-0 scrollbar-hide">
                <button 
                  v-for="(vid, idx) in videosProducto" 
                  :key="idx"
                  @click="videoActualIndex = idx"
                  class="flex-shrink-0 flex items-start gap-3 rounded-lg p-2 transition-all duration-200 text-left"
                  :class="videoActualIndex === idx 
                    ? 'bg-gray-100 ring-2 ring-[#007185]' 
                    : 'hover:bg-gray-50'"
                >
                  <div class="relative w-28 sm:w-32 flex-shrink-0 aspect-video bg-gray-900 rounded-md overflow-hidden">
                    <video 
                      :src="vid" 
                      preload="metadata" 
                      muted 
                      class="w-full h-full object-cover"
                    ></video>
                    <div class="absolute inset-0 flex items-center justify-center">
                      <div class="w-8 h-8 rounded-full bg-black/60 flex items-center justify-center">
                        <svg class="w-4 h-4 text-white ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                      </div>
                    </div>
                    <span v-if="videoActualIndex === idx" class="absolute bottom-1 left-1 text-[10px] bg-[#007185] text-white px-1.5 py-0.5 rounded font-medium">Reproduciendo</span>
                  </div>
                  <div class="hidden sm:block min-w-0 pt-0.5">
                    <p class="text-[13px] font-medium text-gray-800 line-clamp-2">{{ producto.nombre }}</p>
                    <p class="text-xs text-gray-500 mt-1">Video {{ idx + 1 }}</p>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- ========================================
         MOBILE STICKY CTA
    ======================================== -->
    <div class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-3 shadow-[0_-4px_20px_rgba(0,0,0,0.08)] z-40">
      <div class="flex items-center gap-3">
        <div class="flex-1 min-w-0">
          <p class="text-[11px] text-gray-500 uppercase tracking-wider font-medium">Total ({{ cantidad }} uds)</p>
          <p class="text-xl font-bold text-[#0F1111]">${{ formatPrice(subtotal) }}</p>
        </div>
        <button 
          @click="agregarAlCarrito"
          :disabled="producto.stock_actual < LOTE_MINIMO || agregando"
          class="flex-shrink-0 py-3.5 px-6 bg-[#1A1A1A] hover:bg-black text-white font-bold text-sm rounded-md flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
          </svg>
          Agregar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productosService, favoritosService, vistosService } from '@/services/productos'
import { obtenerProducto as obtenerProductoB2B, obtenerProductos as obtenerProductosB2B } from '@/services/mayoristas'
import { B2BToast, useToast } from './ui'

export default {
  name: 'B2BProductoDetalle',
  components: {
    B2BToast
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const toast = useToast()
    
    // ===== CONSTANTES LOTES =====
    const LOTE_MINIMO = 10
    const lotesRapidos = [10, 20, 50, 100, 200]
    
    // State
    const producto = ref({})
    const loading = ref(true)
    const error = ref(null)
    const cantidad = ref(LOTE_MINIMO) // Empieza en mínimo del lote
    const imagenActualIndex = ref(0)
    const esFavorito = ref(false)
    const agregando = ref(false)
    const productosRelacionados = ref([])
    
    // User
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{}')
    })
    
    // Computed
    const imagenes = computed(() => {
      const imgs = []
      if (producto.value.imagen_principal && !isVideo(producto.value.imagen_principal)) {
        imgs.push(producto.value.imagen_principal)
      }
      if (producto.value.imagenes && Array.isArray(producto.value.imagenes)) {
        imgs.push(...producto.value.imagenes.filter(i => i !== producto.value.imagen_principal && !isVideo(i)))
      }
      return imgs.length > 0 ? imgs : ['/placeholder.png']
    })
    
    const imagenActual = computed(() => imagenes.value[imagenActualIndex.value] || '/placeholder.png')

    // Video helpers
    const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov']
    function isVideo(url) {
      if (!url) return false
      const lower = url.toLowerCase()
      return videoExtensions.some(ext => lower.includes(ext))
    }

    const videosProducto = computed(() => {
      const allMedia = []
      if (producto.value.imagen_principal) allMedia.push(producto.value.imagen_principal)
      if (producto.value.imagenes && Array.isArray(producto.value.imagenes)) {
        allMedia.push(...producto.value.imagenes)
      }
      return [...new Set(allMedia)].filter(url => isVideo(url))
    })

    const videoActualIndex = ref(0)
    const videoActual = computed(() => videosProducto.value[videoActualIndex.value] || null)
    
    const precioMayorista = computed(() => {
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
    
    // Precio unitario con descuento por volumen
    const precioUnitarioActual = computed(() => {
      const base = precioMayorista.value
      if (cantidad.value >= 200) return base * 0.90 // 10% extra
      if (cantidad.value >= 100) return base * 0.95 // 5% extra
      if (cantidad.value >= 50) return base * 0.97 // 3% extra
      return base
    })
    
    const subtotal = computed(() => precioUnitarioActual.value * cantidad.value)
    
    const ahorroTotal = computed(() => {
      return (precioMayorista.value * cantidad.value) - subtotal.value
    })
    
    // Tabla de precios por volumen
    const preciosPorVolumen = computed(() => {
      const base = precioMayorista.value
      return [
        { cantidad: 10, precioUnitario: base, precioTotal: base * 10, descripcion: 'Lote mínimo' },
        { cantidad: 20, precioUnitario: base, precioTotal: base * 20, descripcion: 'Ideal para probar' },
        { cantidad: 50, precioUnitario: base * 0.97, precioTotal: base * 0.97 * 50, descripcion: '3% OFF' },
        { cantidad: 100, precioUnitario: base * 0.95, precioTotal: base * 0.95 * 100, descripcion: '5% OFF' },
        { cantidad: 200, precioUnitario: base * 0.90, precioTotal: base * 0.90 * 200, descripcion: '10% OFF - Mejor precio' }
      ]
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
      return `https://wa.me/573001234567?text=${mensaje}` // Cambiar número
    })
    
    // Methods
    function formatPrice(value) {
      return Number(value || 0).toLocaleString('es-CO')
    }
    
    function handleImageError(e) {
      e.target.src = '/placeholder.png'
    }
    
    function abrirZoom() {
      // Abrir imagen en nueva pestaña para zoom
      window.open(imagenActual.value, '_blank')
    }

    // ===== MÉTODOS DE LOTES =====
    function seleccionarLote(lote) {
      if (lote <= producto.value.stock_actual) {
        cantidad.value = lote
      }
    }
    
    function incrementarLote() {
      const nuevo = cantidad.value + LOTE_MINIMO
      if (nuevo <= producto.value.stock_actual) {
        cantidad.value = nuevo
      }
    }
    
    function decrementarLote() {
      const nuevo = cantidad.value - LOTE_MINIMO
      if (nuevo >= LOTE_MINIMO) {
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
    
    // Helper para actualizar localStorage de favoritos
    function updateLocalFavoritos(productoId, agregar) {
      let favoritos = []
      try {
        const stored = localStorage.getItem('b2b_favoritos')
        if (stored) favoritos = JSON.parse(stored)
      } catch {}
      
      if (agregar) {
        if (!favoritos.includes(productoId)) {
          favoritos.push(productoId)
        }
      } else {
        favoritos = favoritos.filter(id => id !== productoId)
      }
      localStorage.setItem('b2b_favoritos', JSON.stringify(favoritos))
      // Dispatch event para que el header se actualice
      window.dispatchEvent(new CustomEvent('favoritos-updated'))
    }
    
    async function toggleFavorito() {
      try {
        if (esFavorito.value) {
          await favoritosService.eliminar(producto.value.id)
          esFavorito.value = false
          updateLocalFavoritos(producto.value.id, false)
        } else {
          await favoritosService.agregar(producto.value.id)
          esFavorito.value = true
          updateLocalFavoritos(producto.value.id, true)
        }
      } catch (err) {
        console.error('Error al toggle favorito:', err)
        esFavorito.value = !esFavorito.value
        updateLocalFavoritos(producto.value.id, esFavorito.value)
      }
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
    
    async function agregarAlCarrito() {
      if (agregando.value) return
      
      try {
        agregando.value = true
        
        // Agregar al carrito del storage
        const cart = JSON.parse(localStorage.getItem('b2b_cart') || '{"items":[]}')
        const existingIndex = cart.items.findIndex(i => i.id === producto.value.id)
        
        if (existingIndex >= 0) {
          cart.items[existingIndex].cantidad += cantidad.value
        } else {
          cart.items.push({
            id: producto.value.id,
            nombre: producto.value.nombre,
            imagen: producto.value.imagen_principal,
            precio: precioMayorista.value,
            cantidad: cantidad.value
          })
        }
        
        localStorage.setItem('b2b_cart', JSON.stringify(cart))
        
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
        
        // Registrar vista
        if (user.value?.email) {
          try {
            await vistosService.registrar(id, user.value.email)
          } catch (err) {
            console.warn('Error registrando vista:', err)
          }
        }
        
        // Verificar si es favorito (API + localStorage fallback)
        try {
          esFavorito.value = await favoritosService.verificar(id)
          // Sincronizar con localStorage
          updateLocalFavoritos(id, esFavorito.value)
        } catch (err) {
          // Fallback: revisar localStorage
          try {
            const stored = localStorage.getItem('b2b_favoritos')
            if (stored) {
              const favs = JSON.parse(stored)
              esFavorito.value = favs.includes(id)
            } else {
              esFavorito.value = false
            }
          } catch {
            esFavorito.value = false
          }
        }
        
        // Cargar productos relacionados (misma categoría) con precios B2B
        if (producto.value.categoria?.nombre || producto.value.categoria_nombre) {
          try {
            const catNombre = producto.value.categoria?.nombre || producto.value.categoria_nombre
            const relacionados = await obtenerProductosB2B({
              categoria: catNombre,
              limit: 6
            })
            productosRelacionados.value = relacionados.filter(p => p.id !== id).slice(0, 5)
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
    
    // Watch for route changes
    watch(() => route.params.id, (newId) => {
      if (newId) {
        cargarProducto(newId)
        window.scrollTo(0, 0)
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
      LOTE_MINIMO,
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
      videosProducto,
      videoActualIndex,
      videoActual,
      isVideo,
      // Computed precios
      precioMayorista,
      precioRetail,
      descuento,
      descuentoTotal,
      subtotal,
      precioUnitarioActual,
      ahorroTotal,
      preciosPorVolumen,
      tieneEspecificaciones,
      whatsappUrl,
      // Methods
      formatPrice,
      handleImageError,
      abrirZoom,
      seleccionarLote,
      incrementarLote,
      decrementarLote,
      incrementarCantidad,
      decrementarCantidad,
      toggleFavorito,
      compartirProducto,
      agregarAlCarrito
    }
  }
}
</script>
