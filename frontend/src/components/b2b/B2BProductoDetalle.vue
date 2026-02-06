<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    
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
      <div class="text-center max-w-md mx-auto">
        <div class="w-16 h-16 mx-auto bg-red-50 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <h3 class="text-xl font-luxury text-gray-900 mb-2">Producto no encontrado</h3>
        <p class="text-gray-500 mb-6">{{ error }}</p>
        <router-link to="/portal/catalogo" class="inline-flex items-center gap-2 text-[#1A1A1A] font-medium hover:underline">
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
      <div class="bg-white border-b border-gray-100">
        <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <nav class="flex items-center gap-2 text-sm text-gray-400">
            <router-link to="/portal" class="hover:text-gray-600 transition-colors">Portal</router-link>
            <span>/</span>
            <router-link to="/portal/catalogo" class="hover:text-gray-600 transition-colors">Catálogo</router-link>
            <span>/</span>
            <span class="text-gray-700 font-medium truncate max-w-[250px]">{{ producto.nombre }}</span>
          </nav>
        </div>
      </div>

      <!-- ============================================
           MAIN 3-COLUMN GRID (Desktop)
           Mobile: Stack vertically
      ============================================ -->
      <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
          
          <!-- ====================================
               COLUMN 1: GALERÍA (4 cols) - GRANDE, LIBRE
          ==================================== -->
          <div class="lg:col-span-5 xl:col-span-4">
            <div class="lg:sticky lg:top-24">
              
              <!-- Main Image - GRANDE Y LIBRE -->
              <div class="relative bg-white rounded-xl overflow-hidden mb-3">
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
                
                <!-- Imagen Principal - SIN PADDING, LIBRE -->
                <div class="aspect-[4/5] bg-gray-50">
                  <img 
                    :src="imagenActual" 
                    :alt="producto.nombre"
                    class="w-full h-full object-cover cursor-zoom-in"
                    @error="handleImageError"
                    @click="abrirZoom"
                  />
                </div>
              </div>
              
              <!-- Thumbnails Gallery - HORIZONTAL -->
              <div v-if="imagenes.length > 1" class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                <button 
                  v-for="(img, idx) in imagenes" 
                  :key="idx"
                  @click="imagenActualIndex = idx"
                  class="flex-shrink-0 w-16 h-20 rounded-lg overflow-hidden border-2 transition-all"
                  :class="imagenActualIndex === idx ? 'border-[#1A1A1A] shadow-md' : 'border-transparent hover:border-gray-300'"
                >
                  <img :src="img" :alt="`Vista ${idx + 1}`" class="w-full h-full object-cover"/>
                </button>
              </div>
              
              <!-- Indicador de imágenes -->
              <p v-if="imagenes.length > 1" class="text-xs text-gray-400 text-center mt-2">
                {{ imagenActualIndex + 1 }} / {{ imagenes.length }} fotos - Click en imagen para ampliar
              </p>
            </div>
          </div>

          <!-- ====================================
               COLUMN 2: INFO QUE VENDE (4 cols)
          ==================================== -->
          <div class="lg:col-span-4 xl:col-span-5 space-y-5">
            
            <!-- Título Principal -->
            <div>
              <div class="flex items-center gap-2 mb-2">
                <span v-if="producto.categoria" class="text-xs text-gray-500 uppercase tracking-wide">
                  {{ producto.categoria.nombre }}
                </span>
                <span v-if="producto.sku" class="text-xs text-gray-400 font-mono">
                  REF: {{ producto.sku }}
                </span>
              </div>
              <h1 class="font-luxury text-2xl sm:text-3xl lg:text-4xl text-[#1A1A1A] leading-tight">
                {{ producto.nombre }}
              </h1>
            </div>
            
            <!-- Características Rápidas - BULLETS QUE VENDEN -->
            <div class="bg-white rounded-xl p-4 border border-gray-200">
              <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Características</h3>
              <ul class="space-y-2">
                <li v-if="producto.textura" class="flex items-center gap-2 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Textura {{ producto.textura }}
                </li>
                <li v-if="producto.longitud" class="flex items-center gap-2 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Largo: {{ producto.longitud }}"
                </li>
                <li v-if="producto.color" class="flex items-center gap-2 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Color: {{ producto.color }}
                </li>
                <li v-if="producto.densidad" class="flex items-center gap-2 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Densidad: {{ producto.densidad }}
                </li>
                <li class="flex items-center gap-2 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Calidad premium garantizada
                </li>
                <li class="flex items-center gap-2 text-sm text-gray-700">
                  <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Ideal para reventa
                </li>
              </ul>
            </div>
            
            <!-- Descripción Corta -->
            <div v-if="producto.descripcion" class="text-gray-600 text-sm leading-relaxed line-clamp-3" v-html="producto.descripcion"></div>
            
            <!-- Por qué este producto - Business Benefits -->
            <div class="bg-white rounded-xl p-4 border border-gray-200">
              <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
                Por qué vende bien
              </h3>
              <ul class="space-y-2 text-sm text-gray-700">
                <li class="flex items-start gap-2">
                  <span class="text-gray-400">—</span>
                  Alta demanda en salones
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-gray-400">—</span>
                  Margen sugerido: <strong class="text-gray-900">40% - 60%</strong>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-gray-400">—</span>
                  Producto de rotación rápida
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-gray-400">—</span>
                  Calidad constante por lote
                </li>
              </ul>
            </div>
            
            <!-- Precios por Volumen - Compact Table -->
            <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
              <div class="bg-gray-50 px-4 py-2.5 border-b border-gray-100">
                <h3 class="text-xs font-semibold text-gray-600 uppercase tracking-wider flex items-center gap-2">
                  <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                  </svg>
                  Precios por volumen
                </h3>
              </div>
              <div class="divide-y divide-gray-50">
                <div 
                  v-for="tier in preciosPorVolumen" 
                  :key="tier.cantidad"
                  class="flex items-center justify-between px-4 py-2.5 text-sm hover:bg-gray-50 cursor-pointer transition-colors"
                  :class="cantidad >= tier.cantidad ? 'bg-gray-100' : ''"
                  @click="seleccionarLote(tier.cantidad)"
                >
                  <div class="flex items-center gap-3">
                    <span class="w-14 font-bold text-gray-900">{{ tier.cantidad }} uds</span>
                    <span class="text-gray-500">{{ tier.descripcion }}</span>
                  </div>
                  <span class="font-bold text-gray-900">
                    ${{ formatPrice(tier.precioUnitario) }}/ud
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Ficha Técnica Expandible -->
            <details class="bg-white rounded-xl border border-gray-100 group">
              <summary class="px-4 py-3 cursor-pointer flex items-center justify-between hover:bg-gray-50">
                <span class="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                  </svg>
                  Ver ficha técnica completa
                </span>
                <svg class="w-4 h-4 text-gray-400 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </summary>
              <div class="px-4 pb-4 border-t border-gray-100">
                <dl class="divide-y divide-gray-50 text-sm">
                  <div v-if="producto.sku" class="flex justify-between py-2">
                    <dt class="text-gray-500">Referencia</dt>
                    <dd class="font-mono text-gray-900">{{ producto.sku }}</dd>
                  </div>
                  <div v-if="producto.categoria" class="flex justify-between py-2">
                    <dt class="text-gray-500">Categoría</dt>
                    <dd class="text-gray-900">{{ producto.categoria.nombre }}</dd>
                  </div>
                  <div v-if="producto.marca" class="flex justify-between py-2">
                    <dt class="text-gray-500">Marca</dt>
                    <dd class="text-gray-900">{{ producto.marca }}</dd>
                  </div>
                  <div v-if="producto.longitud" class="flex justify-between py-2">
                    <dt class="text-gray-500">Longitud</dt>
                    <dd class="text-gray-900">{{ producto.longitud }}"</dd>
                  </div>
                  <div v-if="producto.color" class="flex justify-between py-2">
                    <dt class="text-gray-500">Color</dt>
                    <dd class="text-gray-900">{{ producto.color }}</dd>
                  </div>
                  <div v-if="producto.textura" class="flex justify-between py-2">
                    <dt class="text-gray-500">Textura</dt>
                    <dd class="text-gray-900">{{ producto.textura }}</dd>
                  </div>
                  <div v-if="producto.peso" class="flex justify-between py-2">
                    <dt class="text-gray-500">Peso</dt>
                    <dd class="text-gray-900">{{ producto.peso }}g</dd>
                  </div>
                  <div class="flex justify-between py-2">
                    <dt class="text-gray-500">Stock disponible</dt>
                    <dd class="font-semibold" :class="producto.stock_actual > 20 ? 'text-gray-900' : 'text-gray-600'">
                      {{ producto.stock_actual }} uds
                    </dd>
                  </div>
                  <div class="flex justify-between py-2">
                    <dt class="text-gray-500">Lote mínimo</dt>
                    <dd class="font-semibold text-gray-900">{{ LOTE_MINIMO }} uds</dd>
                  </div>
                </dl>
              </div>
            </details>
          </div>

          <!-- ====================================
               COLUMN 3: COMPRA STICKY (3 cols)
          ==================================== -->
          <div class="lg:col-span-3">
            <div class="lg:sticky lg:top-24 space-y-4">
              
              <!-- Card de Compra Principal - SIEMPRE VISIBLE -->
              <div class="bg-white rounded-xl border border-gray-200 shadow-lg overflow-hidden">
                
                <!-- Header con precio -->
                <div class="bg-[#1A1A1A] text-white p-4">
                  <p class="text-xs text-gray-400 uppercase tracking-wider mb-1">Precio Mayorista</p>
                  <div class="flex items-baseline gap-2">
                    <span class="text-3xl font-bold">${{ formatPrice(precioMayorista) }}</span>
                    <span class="text-gray-400 text-sm">/unidad</span>
                  </div>
                  <p v-if="descuento > 0" class="text-gray-400 text-sm mt-1">
                    {{ descuento }}% menos que retail
                  </p>
                </div>
                
                <!-- Selector de Cantidad -->
                <div class="p-4 border-b border-gray-100">
                  <label class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 block">
                    Cantidad (mín. {{ LOTE_MINIMO }})
                  </label>
                  
                  <!-- Botones Rápidos -->
                  <div class="flex flex-wrap gap-2 mb-3">
                    <button 
                      v-for="lote in [10, 20, 50, 100]" 
                      :key="lote"
                      @click="seleccionarLote(lote)"
                      :disabled="lote > producto.stock_actual"
                      class="px-3 py-1.5 text-sm font-medium rounded-lg transition-all"
                      :class="cantidad === lote 
                        ? 'bg-[#1A1A1A] text-white' 
                        : lote > producto.stock_actual 
                          ? 'bg-gray-100 text-gray-300 cursor-not-allowed' 
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                    >
                      {{ lote }}
                    </button>
                  </div>
                  
                  <!-- Input Cantidad -->
                  <div class="flex items-center border border-gray-200 rounded-lg overflow-hidden">
                    <button 
                      @click="decrementarLote"
                      :disabled="cantidad <= LOTE_MINIMO"
                      class="w-12 h-12 flex items-center justify-center hover:bg-gray-50 transition-colors disabled:opacity-30"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                      </svg>
                    </button>
                    <input 
                      type="number" 
                      v-model.number="cantidad" 
                      :min="LOTE_MINIMO" 
                      :max="producto.stock_actual"
                      :step="LOTE_MINIMO"
                      class="flex-1 text-center font-bold text-xl py-2 focus:outline-none"
                    />
                    <button 
                      @click="incrementarLote"
                      :disabled="cantidad + LOTE_MINIMO > producto.stock_actual"
                      class="w-12 h-12 flex items-center justify-center hover:bg-gray-50 transition-colors disabled:opacity-30"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                      </svg>
                    </button>
                  </div>
                  <p class="text-xs text-gray-400 mt-2 text-center">
                    Stock: {{ producto.stock_actual }} uds
                  </p>
                </div>
                
                <!-- Total -->
                <div class="p-4 bg-gray-50 border-b border-gray-100">
                  <div class="flex justify-between text-sm text-gray-500 mb-1">
                    <span>{{ cantidad }} uds × ${{ formatPrice(precioUnitarioActual) }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="font-semibold text-gray-700">Total:</span>
                    <span class="text-2xl font-bold text-[#1A1A1A]">${{ formatPrice(subtotal) }}</span>
                  </div>
                  <p v-if="ahorroTotal > 0" class="text-gray-600 text-sm font-medium mt-1 text-right">
                    Ahorras ${{ formatPrice(ahorroTotal) }}
                  </p>
                </div>
                
                <!-- CTA Principal - GRANDE -->
                <div class="p-4">
                  <button 
                    @click="agregarAlCarrito"
                    :disabled="producto.stock_actual < LOTE_MINIMO || agregando"
                    class="w-full py-4 bg-[#1A1A1A] hover:bg-black text-white font-bold text-lg rounded-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
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
                  class="flex-1 py-3 px-4 border border-gray-300 text-gray-700 font-medium rounded-lg flex items-center justify-center gap-2 transition-colors hover:bg-gray-50 hover:border-gray-400"
                >
                  <svg class="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                  </svg>
                  Consultar
                </a>
                <button 
                  @click="toggleFavorito"
                  class="w-12 h-12 rounded-lg flex items-center justify-center border transition-all"
                  :class="esFavorito ? 'border-gray-400 bg-gray-100 text-gray-700' : 'border-gray-300 text-gray-400 hover:border-gray-400'"
                >
                  <svg class="w-5 h-5" :fill="esFavorito ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                  </svg>
                </button>
              </div>
              
              <!-- Medios de Pago -->
              <div class="bg-white rounded-xl border border-gray-200 p-4">
                <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Medios de pago</h4>
                
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

        <!-- ========================================
             CARACTERÍSTICAS DEL PRODUCTO - Grid 2 columnas
        ======================================== -->
        <div class="mt-10 lg:mt-14">
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div class="px-5 py-4 border-b border-gray-100">
              <h2 class="text-lg font-semibold text-gray-900">Características del producto</h2>
            </div>
            <div class="p-5">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Especificación Item -->
                <div v-if="producto.categoria" class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Categoría</p>
                    <p class="text-sm font-medium text-gray-900">{{ producto.categoria.nombre }}</p>
                  </div>
                </div>
                
                <div v-if="producto.textura" class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6z"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Textura</p>
                    <p class="text-sm font-medium text-gray-900">{{ producto.textura }}</p>
                  </div>
                </div>
                
                <div v-if="producto.longitud" class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Longitud</p>
                    <p class="text-sm font-medium text-gray-900">{{ producto.longitud }}"</p>
                  </div>
                </div>
                
                <div v-if="producto.color" class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Color</p>
                    <p class="text-sm font-medium text-gray-900">{{ producto.color }}</p>
                  </div>
                </div>
                
                <div v-if="producto.densidad" class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Densidad</p>
                    <p class="text-sm font-medium text-gray-900">{{ producto.densidad }}</p>
                  </div>
                </div>
                
                <div v-if="producto.peso" class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Peso</p>
                    <p class="text-sm font-medium text-gray-900">{{ producto.peso }}g</p>
                  </div>
                </div>
                
                <div v-if="producto.marca" class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Marca</p>
                    <p class="text-sm font-medium text-gray-900">{{ producto.marca }}</p>
                  </div>
                </div>
                
                <div class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Stock disponible</p>
                    <p class="text-sm font-medium text-gray-900">{{ producto.stock_actual }} unidades</p>
                  </div>
                </div>
                
                <div class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Lote mínimo</p>
                    <p class="text-sm font-medium text-gray-900">{{ LOTE_MINIMO }} unidades</p>
                  </div>
                </div>
                
                <div v-if="producto.sku" class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"/>
                  </svg>
                  <div>
                    <p class="text-sm text-gray-500">Referencia / SKU</p>
                    <p class="text-sm font-medium text-gray-900 font-mono">{{ producto.sku }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- ========================================
             GALERÍA DE IMÁGENES DEL PRODUCTO
        ======================================== -->
        <div v-if="imagenes.length > 1" class="mt-10 lg:mt-14">
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div class="px-5 py-4 border-b border-gray-100">
              <h2 class="text-lg font-semibold text-gray-900">Imágenes del producto</h2>
            </div>
            <div class="p-5">
              <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
                <div 
                  v-for="(img, idx) in imagenes" 
                  :key="idx"
                  @click="imagenActualIndex = idx; abrirZoom()"
                  class="aspect-square bg-gray-50 rounded-lg overflow-hidden cursor-pointer hover:ring-2 hover:ring-gray-300 transition-all"
                >
                  <img :src="img" :alt="`${producto.nombre} - Vista ${idx + 1}`" class="w-full h-full object-cover"/>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ========================================
             PRODUCTOS RELACIONADOS
        ======================================== -->
        <div v-if="productosRelacionados.length > 0" class="mt-10 lg:mt-14">
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div class="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
              <h2 class="text-lg font-semibold text-gray-900">Productos relacionados</h2>
              <router-link to="/portal/catalogo" class="text-sm text-gray-500 hover:text-gray-700 transition-colors">
                Ver todos →
              </router-link>
            </div>
            <div class="p-5">
              <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
                <router-link 
                  v-for="prod in productosRelacionados" 
                  :key="prod.id"
                  :to="`/portal/producto/${prod.id}`"
                  class="group"
                >
                  <div class="aspect-[4/5] bg-gray-50 rounded-lg overflow-hidden mb-2">
                    <img 
                      :src="prod.imagen_principal || '/placeholder.png'" 
                      :alt="prod.nombre"
                      class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <h3 class="font-medium text-gray-800 text-sm line-clamp-2 mb-1 group-hover:text-gray-600">{{ prod.nombre }}</h3>
                  <div class="flex items-baseline gap-2">
                    <p class="text-[#1A1A1A] font-bold">${{ formatPrice(prod.precio_mayorista || prod.monto_precio) }}</p>
                    <p v-if="prod.precio && prod.precio > (prod.precio_mayorista || prod.monto_precio)" class="text-xs text-gray-400 line-through">
                      ${{ formatPrice(prod.precio) }}
                    </p>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">Mín. {{ LOTE_MINIMO }} uds</p>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- ========================================
         MOBILE STICKY CTA (solo visible en móvil)
    ======================================== -->
    <div class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-3 shadow-[0_-4px_20px_rgba(0,0,0,0.08)] z-40">
      <div class="flex items-center gap-3">
        <div class="flex-1">
          <p class="text-xs text-gray-500">Total ({{ cantidad }} uds)</p>
          <p class="text-xl font-bold text-[#1A1A1A]">${{ formatPrice(subtotal) }}</p>
        </div>
        <button 
          @click="agregarAlCarrito"
          :disabled="producto.stock_actual < LOTE_MINIMO || agregando"
          class="flex-1 py-3.5 bg-[#1A1A1A] hover:bg-black text-white font-bold rounded-lg flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

export default {
  name: 'B2BProductoDetalle',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
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
      if (producto.value.imagen_principal) imgs.push(producto.value.imagen_principal)
      if (producto.value.imagenes && Array.isArray(producto.value.imagenes)) {
        imgs.push(...producto.value.imagenes.filter(i => i !== producto.value.imagen_principal))
      }
      return imgs.length > 0 ? imgs : ['/placeholder.png']
    })
    
    const imagenActual = computed(() => imagenes.value[imagenActualIndex.value] || '/placeholder.png')
    
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
        // Si la API falla, igual actualizamos localmente para UX
        esFavorito.value = !esFavorito.value
        updateLocalFavoritos(producto.value.id, esFavorito.value)
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
        
        // Feedback visual
        alert(`${producto.value.nombre} agregado al carrito (${cantidad.value} unidades)`)
        
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
        
        // Cargar producto
        const data = await productosService.getProducto(id)
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
        
        // Cargar productos relacionados (misma categoría)
        if (producto.value.categoria?.id) {
          try {
            const relacionados = await productosService.getProductos({
              categoria: producto.value.categoria.id,
              limit: 5
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
      // Computed precios
      precioMayorista,
      precioRetail,
      descuento,
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
      agregarAlCarrito
    }
  }
}
</script>
