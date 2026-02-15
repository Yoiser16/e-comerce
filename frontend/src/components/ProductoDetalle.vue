<template>
  <div class="min-h-screen bg-[#F9F8F6]">
    
    <!-- ========================================
         TOP BAR - Anuncio Fijo
         ======================================== -->
    <div class="fixed top-0 left-0 right-0 z-[60] bg-white h-7 flex items-center justify-center">
      <p class="text-[#333] text-[10px] font-normal uppercase tracking-[2px] text-center px-4">
        Envío gratis en compras mayores a $200.000
      </p>
    </div>

    <!-- ========================================
         HEADER - Mobile App Style / Desktop Luxury
         ======================================== -->
    <header 
      :class="[
        'fixed left-0 right-0 z-50 transition-all duration-300',
        'bg-white border-b border-text-dark/5',
        isScrolled ? 'shadow-sm' : ''
      ]"
      style="top: 28px;"
    >
      <!-- Mobile Header -->
      <div class="lg:hidden">
        <div class="flex items-center justify-between h-12 px-3">
          <!-- Left: Back -->
          <button 
            @click="router.back()"
            class="w-10 h-10 flex items-center justify-center -ml-2"
          >
            <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
          </button>
          
          <!-- Center: Logo -->
          <router-link to="/" class="absolute left-1/2 -translate-x-1/2">
            <img 
              src="/logo-kharis.png" 
              alt="Kharis" 
              class="h-8 w-auto object-contain"
            />
          </router-link>
          
          <!-- Right: User + Cart -->
          <div class="flex items-center gap-0.5">
            <router-link 
              to="/login"
              class="w-10 h-10 flex items-center justify-center"
            >
              <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
            </router-link>
            <button 
              class="relative w-10 h-10 flex items-center justify-center -mr-2"
              @click="showCartDrawer = true"
            >
              <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
              <span 
                v-if="cartCount > 0"
                class="absolute top-1 right-1 w-4 h-4 text-[9px] font-bold rounded-full flex items-center justify-center bg-text-dark text-white"
              >
                {{ cartCount > 9 ? '9+' : cartCount }}
              </span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Desktop Header -->
      <div class="hidden lg:block">
        <div class="max-w-[1400px] mx-auto px-6 xl:px-12">
          <div class="flex items-center justify-between h-16">
            <!-- Logo -->
            <router-link to="/" class="flex-shrink-0">
              <img 
                src="/logo-kharis.png" 
                alt="Kharis Distribuidora" 
                class="h-12 w-auto object-contain hover:opacity-80 transition-opacity"
              />
            </router-link>

            <!-- Navegación Desktop -->
            <nav class="flex items-center gap-8">
              <router-link to="/" class="text-[11px] font-medium tracking-[1.5px] text-text-dark hover:text-brand-600 transition-colors">INICIO</router-link>
              <router-link to="/catalogo" class="text-[11px] font-medium tracking-[1.5px] text-text-dark hover:text-brand-600 transition-colors">COLECCIÓN</router-link>
              <router-link to="/#mayoreo" class="text-[11px] font-medium tracking-[1.5px] text-text-dark hover:text-brand-600 transition-colors">MAYOREO</router-link>
              <router-link to="/#contacto" class="text-[11px] font-medium tracking-[1.5px] text-text-dark hover:text-brand-600 transition-colors">CONTACTO</router-link>
            </nav>

            <!-- Acciones Desktop -->
            <div class="flex items-center gap-1">
              <router-link 
                to="/login"
                class="w-10 h-10 rounded-full flex items-center justify-center hover:bg-[#f5f5f5] transition-colors"
              >
                <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
              </router-link>
              <button 
                class="relative w-10 h-10 rounded-full flex items-center justify-center hover:bg-[#f5f5f5] transition-colors"
                @click="showCartDrawer = true"
              >
                <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
                <span 
                  v-if="cartCount > 0"
                  class="absolute top-1 right-1 w-4 h-4 text-[9px] font-bold rounded-full flex items-center justify-center bg-text-dark text-white"
                >
                  {{ cartCount > 9 ? '9+' : cartCount }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Spacer para el header fijo + top bar -->
    <div class="h-[76px] lg:h-[92px]"></div>

    <!-- Back Navigation (solo desktop, en móvil está en el header) -->
    <div class="hidden lg:block max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-12 pt-4">
      <button @click="router.back()" class="inline-flex items-center gap-2 text-text-medium hover:text-text-dark text-sm transition-colors group">
        <svg class="w-4 h-4 transition-transform group-hover:-translate-x-1" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
        <span class="tracking-wide">Volver a la colección</span>
      </button>
    </div>

    <!-- Main Content -->
    <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-12 py-6 lg:py-8">
      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16">
        <div class="space-y-4">
          <div class="aspect-[4/5] bg-white animate-pulse rounded-sm"></div>
          <div class="grid grid-cols-4 gap-3">
            <div v-for="i in 4" :key="i" class="aspect-square bg-white animate-pulse rounded-sm"></div>
          </div>
        </div>
        <div class="space-y-6 pt-4">
          <div class="h-4 w-24 bg-white/80 animate-pulse rounded"></div>
          <div class="h-10 w-3/4 bg-white/80 animate-pulse rounded"></div>
          <div class="h-8 w-32 bg-white/80 animate-pulse rounded"></div>
          <div class="h-24 w-full bg-white/80 animate-pulse rounded"></div>
          <div class="h-14 w-full bg-white/80 animate-pulse rounded"></div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-20">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-50 mb-4">
          <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
        </div>
        <p class="text-text-medium">{{ error }}</p>
        <button @click="cargarProducto" class="mt-4 text-sm text-text-dark underline underline-offset-4 hover:no-underline">Reintentar</button>
      </div>

      <!-- Product Content -->
      <div v-else-if="producto" class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 xl:gap-20">
        
        <!-- LEFT: Gallery -->
        <div class="space-y-4">
          <!-- Main Image/Video -->
          <div 
            class="aspect-[4/5] bg-white overflow-hidden cursor-zoom-in relative group"
            @click="openLightbox"
          >
            <!-- Video principal -->
            <video 
              v-if="isVideo(imagenActiva)"
              :src="getImageUrl(imagenActiva)"
              class="w-full h-full object-cover"
              controls
              muted
            ></video>
            <!-- Imagen principal -->
            <img
              v-else
              :src="getImageUrl(imagenActiva)"
              :alt="producto.nombre"
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              @error="handleImageError"
            />
            <!-- Zoom hint -->
            <div class="absolute bottom-4 right-4 bg-white/90 px-3 py-1.5 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
              <span class="text-xs text-text-medium tracking-wide">Click para ampliar</span>
            </div>
          </div>
          
          <!-- Thumbnails -->
          <div class="grid grid-cols-4 gap-3">
            <button
              v-for="(thumb, idx) in miniaturas"
              :key="idx"
              @click="imagenActiva = thumb"
              :class="[
                'aspect-square overflow-hidden bg-white transition-all duration-200 relative',
                imagenActiva === thumb 
                  ? 'ring-2 ring-text-dark ring-offset-2' 
                  : 'opacity-70 hover:opacity-100'
              ]"
            >
              <!-- Video thumbnail -->
              <video 
                v-if="isVideo(thumb)"
                :src="getImageUrl(thumb)"
                class="w-full h-full object-cover"
                muted
              ></video>
              <!-- Image thumbnail -->
              <img 
                v-else
                :src="getImageUrl(thumb)" 
                :alt="'Vista ' + (idx + 1)" 
                class="w-full h-full object-cover"
                @error="handleImageError" 
              />
              <!-- Play icon for videos -->
              <div v-if="isVideo(thumb)" class="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div class="bg-black/40 rounded-full p-1.5">
                  <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                  </svg>
                </div>
              </div>
            </button>
          </div>
        </div>

        <!-- RIGHT: Product Info (Sticky) -->
        <div class="lg:sticky lg:top-8 lg:self-start space-y-6">
          <!-- Category & Title -->
          <div class="space-y-3">
            <p class="text-xs uppercase tracking-[0.2em] text-text-light">{{ producto.categoria || 'Colección Premium' }}</p>
            <h1 class="font-luxury text-3xl sm:text-4xl lg:text-[42px] text-text-dark leading-tight">{{ producto.nombre }}</h1>
          </div>

          <!-- Price -->
          <div class="flex items-baseline gap-3">
            <span class="text-2xl sm:text-3xl font-semibold text-text-dark">{{ formatearPrecio(precioUnitarioSeleccionado) }}</span>
            <span class="text-sm text-text-light">IVA incluido</span>
          </div>

          <!-- Stock Badge -->
          <div 
            v-if="stockDisponible >= 0"
            :class="[
              'inline-flex items-center gap-2 text-xs font-medium tracking-wider',
              stockDisponible === 0 
                ? 'text-red-600' 
                : stockDisponible <= 5 
                  ? 'text-amber-600' 
                  : 'text-emerald-600'
            ]"
          >
            <span 
              :class="[
                'w-2 h-2 rounded-full',
                stockDisponible === 0 ? 'bg-red-500' : stockDisponible <= 5 ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500'
              ]"
            ></span>
            <span class="uppercase">
              {{ stockDisponible === 0 ? 'Agotado' : stockDisponible <= 5 ? `¡Solo ${stockDisponible} en stock!` : 'En stock' }}
            </span>
          </div>

          <!-- Short Description -->
          <p v-if="producto.descripcion" class="text-text-medium leading-relaxed text-sm sm:text-base line-clamp-3">
            {{ producto.descripcion }}
          </p>

          <!-- Divider -->
          <div class="border-t border-text-dark/10"></div>

          <!-- VARIANTES: Color Swatches -->
          <div v-if="coloresDisponibles.length > 1" class="space-y-3">
            <p class="text-xs uppercase tracking-[0.15em] text-text-light">Color: <span class="text-text-dark font-medium normal-case">{{ colorSeleccionadoLabel }}</span></p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="color in coloresDisponibles"
                :key="color.value"
                @click="selectColor(color)"
                :class="[
                  'w-8 h-8 rounded-full transition-all duration-200 relative',
                  colorSeleccionado === color.value 
                    ? 'ring-2 ring-text-dark ring-offset-2' 
                    : 'hover:ring-2 hover:ring-text-dark/30 hover:ring-offset-1'
                ]"
                :style="{ backgroundColor: color.hex }"
                :title="color.label"
              >
                <!-- Checkmark for selected -->
                <svg 
                  v-if="colorSeleccionado === color.value && isLightColor(color.hex)"
                  class="w-4 h-4 absolute inset-0 m-auto text-text-dark"
                  fill="currentColor" viewBox="0 0 20 20"
                >
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <svg 
                  v-else-if="colorSeleccionado === color.value"
                  class="w-4 h-4 absolute inset-0 m-auto text-white"
                  fill="currentColor" viewBox="0 0 20 20"
                >
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>

          <!-- VARIANTES: Largo (Pills) -->
          <div v-if="largosDisponibles.length > 1" class="space-y-3">
            <p class="text-xs uppercase tracking-[0.15em] text-text-light">Largo</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="largo in largosDisponibles"
                :key="largo.value"
                @click="selectLargo(largo)"
                :class="[
                  'px-4 py-2.5 text-sm font-medium transition-all duration-200 border',
                  largoSeleccionado === largo.value 
                    ? 'bg-text-dark text-white border-text-dark' 
                    : 'bg-white text-text-dark border-text-dark/20 hover:border-text-dark/50'
                ]"
              >
                {{ largo.label }}
              </button>
            </div>
          </div>

          <!-- VARIANTES: Calidad/Densidad (Pills) -->
          <div v-if="calidadesDisponibles.length" class="space-y-3">
            <p class="text-xs uppercase tracking-[0.15em] text-text-light">Calidad</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="calidad in calidadesDisponibles"
                :key="calidad"
                @click="calidadSeleccionada = calidad"
                :class="[
                  'px-4 py-2.5 text-sm font-medium transition-all duration-200 border',
                  calidadSeleccionada === calidad 
                    ? 'bg-text-dark text-white border-text-dark' 
                    : 'bg-white text-text-dark border-text-dark/20 hover:border-text-dark/50'
                ]"
              >
                {{ calidad }}
              </button>
            </div>
          </div>

          <!-- Quantity Selector -->
          <div class="flex items-center gap-4">
            <p class="text-xs uppercase tracking-[0.15em] text-text-light">Cantidad</p>
            <div class="flex items-center border border-text-dark/20 bg-white">
              <button 
                @click="cantidad > 1 && cantidad--"
                class="w-10 h-10 flex items-center justify-center text-text-medium hover:text-text-dark hover:bg-gray-50 transition-colors"
                :disabled="cantidad <= 1"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
                </svg>
              </button>
              <span class="w-12 text-center font-medium text-text-dark">{{ cantidad }}</span>
              <button 
                @click="cantidad < stockDisponible && cantidad++"
                class="w-10 h-10 flex items-center justify-center text-text-medium hover:text-text-dark hover:bg-gray-50 transition-colors"
                :disabled="cantidad >= stockDisponible"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Add to Cart Button -->
          <button
            @click="agregarAlCarrito"
            :disabled="stockDisponible === 0"
            class="w-full py-4 bg-text-dark text-white text-sm font-semibold uppercase tracking-[0.15em] hover:bg-black transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
            </svg>
            {{ stockDisponible === 0 ? 'AGOTADO' : 'AGREGAR AL CARRITO' }}
          </button>

          <!-- Success/Error Messages -->
          <transition name="fade">
            <div v-if="mensaje" class="flex items-center gap-2 text-sm text-emerald-600 bg-emerald-50 px-4 py-3 rounded-sm">
              <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
              </svg>
              {{ mensaje }}
            </div>
          </transition>
          <transition name="fade">
            <div v-if="mensajeError" class="flex items-center gap-2 text-sm text-red-600 bg-red-50 px-4 py-3 rounded-sm">
              <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd" />
              </svg>
              {{ mensajeError }}
            </div>
          </transition>

          <!-- Trust Badges -->
          <div class="grid grid-cols-3 gap-3 pt-2">
            <div class="flex flex-col items-center text-center py-3 px-2">
              <svg class="w-6 h-6 text-text-medium mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
              </svg>
              <span class="text-[10px] sm:text-xs text-text-light uppercase tracking-wider leading-tight">Envío<br/>Seguro</span>
            </div>
            <div class="flex flex-col items-center text-center py-3 px-2">
              <svg class="w-6 h-6 text-text-medium mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
              </svg>
              <span class="text-[10px] sm:text-xs text-text-light uppercase tracking-wider leading-tight">Garantía<br/>Remy 100%</span>
            </div>
            <div class="flex flex-col items-center text-center py-3 px-2">
              <svg class="w-6 h-6 text-text-medium mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
              </svg>
              <span class="text-[10px] sm:text-xs text-text-light uppercase tracking-wider leading-tight">Pagos<br/>Protegidos</span>
            </div>
          </div>

          <!-- Divider -->
          <div class="border-t border-text-dark/10 pt-4"></div>

          <!-- Accordions -->
          <div class="space-y-0">
            <!-- Descripción -->
            <div class="border-b border-text-dark/10">
              <button 
                @click="toggleAccordion('descripcion')"
                class="w-full py-4 flex items-center justify-between text-left group"
              >
                <span class="text-sm font-medium text-text-dark uppercase tracking-[0.1em]">Descripción del Producto</span>
                <svg 
                  :class="['w-4 h-4 text-text-medium transition-transform duration-300', accordionOpen.descripcion ? 'rotate-180' : '']"
                  fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                </svg>
              </button>
              <transition name="accordion">
                <div v-show="accordionOpen.descripcion" class="pb-4 text-sm text-text-medium leading-relaxed space-y-3">
                  <p class="whitespace-pre-line">{{ producto.descripcion || 'Extensión de cabello 100% humano de la más alta calidad. Ideal para transformar tu look con un acabado natural y duradero.' }}</p>
                  <div v-if="producto.tipo || producto.origen || producto.metodo" class="grid grid-cols-2 gap-2 pt-2">
                    <div v-if="producto.tipo" class="text-xs">
                      <span class="text-text-light">Tipo:</span> {{ producto.tipo }}
                    </div>
                    <div v-if="producto.origen" class="text-xs">
                      <span class="text-text-light">Origen:</span> {{ producto.origen }}
                    </div>
                    <div v-if="producto.metodo" class="text-xs">
                      <span class="text-text-light">Método:</span> {{ producto.metodo }}
                    </div>
                    <div v-if="producto.calidad" class="text-xs">
                      <span class="text-text-light">Calidad:</span> {{ producto.calidad }}
                    </div>
                  </div>
                </div>
              </transition>
            </div>

            <!-- Guía de Cuidados -->
            <div class="border-b border-text-dark/10">
              <button 
                @click="toggleAccordion('cuidados')"
                class="w-full py-4 flex items-center justify-between text-left group"
              >
                <span class="text-sm font-medium text-text-dark uppercase tracking-[0.1em]">Guía de Cuidados</span>
                <svg 
                  :class="['w-4 h-4 text-text-medium transition-transform duration-300', accordionOpen.cuidados ? 'rotate-180' : '']"
                  fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                </svg>
              </button>
              <transition name="accordion">
                <div v-show="accordionOpen.cuidados" class="pb-4 text-sm text-text-medium leading-relaxed space-y-2">
                  <ul class="space-y-2 list-disc list-inside">
                    <li>Lava con shampoo sin sulfatos y agua tibia</li>
                    <li>Usa acondicionador hidratante después de cada lavado</li>
                    <li>Deja secar al aire o usa secador a temperatura baja</li>
                    <li>Peina suavemente con un peine de dientes anchos</li>
                    <li>Guarda en su bolsa de seda cuando no esté en uso</li>
                    <li>Evita dormir con el cabello mojado</li>
                  </ul>
                </div>
              </transition>
            </div>

            <!-- Envíos y Devoluciones -->
            <div class="border-b border-text-dark/10">
              <button 
                @click="toggleAccordion('envios')"
                class="w-full py-4 flex items-center justify-between text-left group"
              >
                <span class="text-sm font-medium text-text-dark uppercase tracking-[0.1em]">Envíos y Devoluciones</span>
                <svg 
                  :class="['w-4 h-4 text-text-medium transition-transform duration-300', accordionOpen.envios ? 'rotate-180' : '']"
                  fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                </svg>
              </button>
              <transition name="accordion">
                <div v-show="accordionOpen.envios" class="pb-4 text-sm text-text-medium leading-relaxed space-y-3">
                  <div>
                    <p class="font-medium text-text-dark mb-1">Envíos</p>
                    <ul class="space-y-1 text-xs">
                      <li>• Envío gratis en compras mayores a $200.000</li>
                      <li>• Entrega en 2-5 días hábiles a nivel nacional</li>
                      <li>• Entrega express disponible en ciudades principales</li>
                    </ul>
                  </div>
                  <div>
                    <p class="font-medium text-text-dark mb-1">Devoluciones</p>
                    <ul class="space-y-1 text-xs">
                      <li>• 15 días para cambios o devoluciones</li>
                      <li>• Producto debe estar sin usar y en empaque original</li>
                      <li>• Contáctanos vía WhatsApp para iniciar el proceso</li>
                    </ul>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- Calificaciones de clientes -->
          <div class="mt-8 border-t border-text-dark/10 pt-6">
            <h3 class="text-sm font-medium text-text-dark uppercase tracking-[0.1em] mb-4">Calificaciones</h3>
            <div class="flex items-center gap-3 mb-3">
              <div class="flex items-center gap-1">
                <svg v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= promedioRedondeado ? 'text-gold-400' : 'text-gray-200'" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
              <span class="text-sm text-text-medium">{{ promedioFormateado }} / 5 · {{ resumenResenas.total }} calificaciones</span>
            </div>

            <div v-if="isLoggedIn" class="border border-text-dark/10 bg-white p-4 rounded-sm">
              <p class="text-xs text-text-light mb-2">Tu calificación</p>
              <div class="flex items-center gap-2 flex-wrap">
                <button
                  v-for="i in 5"
                  :key="i"
                  type="button"
                  class="w-8 h-8 rounded-full border border-text-dark/10 flex items-center justify-center transition-colors"
                  :class="i <= miRating ? 'bg-text-dark text-white' : 'bg-white text-text-dark hover:bg-text-dark/5'"
                  @click="miRating = i"
                >
                  <span class="text-xs font-semibold">{{ i }}</span>
                </button>
                <button
                  type="button"
                  class="ml-auto px-4 py-2 text-xs uppercase tracking-wider bg-text-dark text-white hover:bg-black transition-colors disabled:opacity-50"
                  :disabled="!miRating || enviandoResena"
                  @click="enviarResena"
                >
                  {{ enviandoResena ? 'Enviando...' : 'Enviar' }}
                </button>
              </div>
              <p v-if="resenaMensaje" class="text-xs text-emerald-600 mt-2">{{ resenaMensaje }}</p>
              <p v-if="resenaError" class="text-xs text-red-600 mt-2">{{ resenaError }}</p>
              <p class="text-[11px] text-text-light mt-2">Solo clientes con compra pueden calificar. Requiere aprobación.</p>
            </div>
            <div v-else class="text-xs text-text-light">
              Inicia sesión para calificar este producto.
            </div>

            <div class="mt-4">
              <div v-if="resenasLoading" class="space-y-3">
                <div v-for="i in 3" :key="i" class="h-10 bg-nude-50 rounded"></div>
              </div>
              <div v-else-if="resenasProducto.length" class="space-y-3">
                <div v-for="resena in resenasProducto" :key="resena.id" class="flex items-center justify-between text-sm text-text-medium">
                  <span class="font-medium text-text-dark">{{ resena.cliente }}</span>
                  <div class="flex items-center gap-1">
                    <svg v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= resena.rating ? 'text-gold-400' : 'text-gray-200'" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  </div>
                </div>
              </div>
              <div v-else class="text-xs text-text-light">
                Aún no hay calificaciones aprobadas.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Related Products Section -->
    <section v-if="productosRelacionados.length > 0" class="border-t border-text-dark/10 bg-white py-12 lg:py-16">
      <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-12">
        <!-- Section Header -->
        <div class="text-center mb-8 lg:mb-12">
          <p class="text-xs uppercase tracking-[0.2em] text-text-light mb-2">También te puede gustar</p>
          <h2 class="font-luxury text-2xl sm:text-3xl text-text-dark">Completa tu Look</h2>
        </div>

        <!-- Products Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          <router-link
            v-for="prod in productosRelacionados"
            :key="prod.id"
            :to="`/producto/${prod.id}`"
            class="group bg-[#F9F8F6] overflow-hidden"
          >
            <!-- Image -->
            <div class="aspect-[3/4] overflow-hidden relative">
              <img
                :src="getImageUrl(prod.imagen_principal)"
                :alt="prod.nombre"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                @error="handleImageError"
              />
              <!-- Quick Add Overlay -->
              <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors flex items-end justify-center pb-4 opacity-0 group-hover:opacity-100">
                <span class="bg-white text-text-dark text-xs font-medium px-4 py-2 uppercase tracking-wider">Ver Producto</span>
              </div>
            </div>
            <!-- Info -->
            <div class="p-3 sm:p-4 text-center">
              <h3 class="text-xs sm:text-sm font-medium text-text-dark line-clamp-1 group-hover:text-brand-600 transition-colors">{{ prod.nombre }}</h3>
              <p class="text-sm font-semibold text-text-dark mt-1">{{ formatearPrecio(prod.precio_monto) }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Lightbox Modal -->
    <transition name="fade">
      <div 
        v-if="lightboxOpen" 
        class="fixed inset-0 bg-black/95 z-50 flex items-center justify-center p-4"
        @click.self="lightboxOpen = false"
      >
        <button 
          @click="lightboxOpen = false"
          class="absolute top-6 right-6 text-white/70 hover:text-white transition-colors"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        
        <!-- Video en lightbox -->
        <video 
          v-if="isVideo(imagenActiva)"
          :src="getImageUrl(imagenActiva)" 
          class="max-w-full max-h-[85vh] object-contain"
          controls
        ></video>
        <!-- Imagen en lightbox -->
        <img 
          v-else
          :src="getImageUrl(imagenActiva)" 
          :alt="producto?.nombre"
          class="max-w-full max-h-[85vh] object-contain"
        />
        
        <!-- Thumbnails in lightbox -->
        <div class="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2">
          <button
            v-for="(thumb, idx) in miniaturas"
            :key="idx"
            @click.stop="imagenActiva = thumb"
            :class="[
              'w-12 h-12 overflow-hidden transition-all relative',
              imagenActiva === thumb ? 'ring-2 ring-white' : 'opacity-50 hover:opacity-100'
            ]"
          >
            <!-- Video thumbnail -->
            <video 
              v-if="isVideo(thumb)"
              :src="getImageUrl(thumb)"
              class="w-full h-full object-cover"
              muted
            ></video>
            <!-- Image thumbnail -->
            <img 
              v-else
              :src="getImageUrl(thumb)" 
              :alt="'Vista ' + (idx + 1)" 
              class="w-full h-full object-cover"
            />
            <!-- Play icon for videos -->
            <div v-if="isVideo(thumb)" class="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div class="bg-white/30 rounded-full p-1">
                <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                </svg>
              </div>
            </div>
          </button>
        </div>
      </div>
    </transition>

    <!-- Cart Drawer -->
    <transition name="drawer-slide">
      <div v-if="showCartDrawer" class="fixed inset-0 z-50 flex justify-end">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40" @click="closeCartDrawer"></div>
        
        <!-- Drawer -->
        <div class="relative w-full max-w-md h-full bg-white shadow-2xl flex flex-col">
          <!-- Header -->
          <div class="border-b border-text-dark/10 p-6 flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-text-dark">Mi Carrito</h3>
              <p class="text-xs text-text-light mt-0.5">{{ cartCount }} {{ cartCount === 1 ? 'artículo' : 'artículos' }}</p>
            </div>
            <button @click="closeCartDrawer" class="text-text-medium hover:text-text-dark transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Items -->
          <div class="flex-1 overflow-y-auto p-6">
            <div v-if="carritoItems.length === 0" class="text-center py-16">
              <svg class="w-16 h-16 mx-auto text-text-light/50 mb-4" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
              <p class="text-text-medium text-sm">Tu carrito está vacío</p>
              <button @click="closeCartDrawer" class="mt-4 text-sm text-text-dark underline underline-offset-4 hover:no-underline">Continuar comprando</button>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="item in carritoItems" 
                :key="item.variante_id || item.producto_id"
                class="flex gap-4 pb-4 border-b border-text-dark/5"
              >
                <img 
                  :src="item.imagen_url"
                  :alt="item.nombre"
                  @error="handleImageError"
                  class="w-20 h-20 object-cover bg-[#F9F8F6]"
                >
                <div class="flex-1 min-w-0">
                  <h4 class="text-sm font-medium text-text-dark line-clamp-2">{{ item.nombre }}</h4>
                  <p v-if="item.color || item.largo" class="text-xs text-text-light mt-1">
                    <span v-if="item.color">Color: {{ formatColorLabel(item.color) }}</span>
                    <span v-if="item.color && item.largo"> · </span>
                    <span v-if="item.largo">Largo: {{ item.largo }}</span>
                  </p>
                  <p class="text-xs text-text-light mt-1">Cantidad: {{ item.cantidad }}</p>
                  <p class="text-sm font-semibold text-text-dark mt-2">{{ formatearPrecio((item.precio_unitario || item.precio_monto || 0) * item.cantidad) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div v-if="carritoItems.length > 0" class="border-t border-text-dark/10 p-6 space-y-4 bg-[#FAFAFA]">
            <div class="flex justify-between items-center">
              <span class="text-sm text-text-medium">Subtotal</span>
              <span class="text-lg font-semibold text-text-dark">{{ formatearPrecio(cartSubtotal) }}</span>
            </div>
            <p class="text-xs text-text-light">Envío calculado en el checkout</p>
            <button 
              @click="goToCheckout" 
              class="w-full py-4 bg-text-dark hover:bg-black text-white text-sm font-semibold uppercase tracking-wider transition-all"
            >
              Finalizar Compra
            </button>
            <button 
              @click="closeCartDrawer" 
              class="w-full py-3 border border-text-dark/20 text-text-dark text-sm font-medium hover:border-text-dark/40 transition-all"
            >
              Seguir Comprando
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productosService, carritoService, authService } from '@/services/productos'
import { resenasService } from '@/services/resenas'
import { getImageUrl } from '@/services/api'
import { formatColorLabel } from '@/utils/colorLabels'

const route = useRoute()
const router = useRouter()

// Header scroll state
const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

// Product State
const producto = ref(null)
const loading = ref(true)
const error = ref(null)
const miniaturas = ref([])
const imagenActiva = ref('')
const lightboxOpen = ref(false)

// Messages
const mensaje = ref('')
const mensajeError = ref('')

// Variants Selection
const colorSeleccionado = ref('')
const largoSeleccionado = ref('')
const calidadSeleccionada = ref('')

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

const formatLargoLabel = (largo) => (largo ? `${largo}"` : '')
const BASE_VARIANTE_VALUE = '__base__'

const variantesDisponibles = computed(() => {
  const variantes = Array.isArray(producto.value?.variantes) ? producto.value.variantes : []
  return variantes.filter(v => v && v.activo !== false)
})

const varianteBase = computed(() => {
  return variantesDisponibles.value.find(v => !v.color && !v.largo) || null
})

const coloresDisponibles = computed(() => {
  const map = new Map()
  variantesDisponibles.value.forEach((v) => {
    if (!v.color) return
    if (!map.has(v.color)) {
      map.set(v.color, {
        value: v.color,
        label: formatColorLabel(v.color),
        hex: COLOR_HEX[v.color] || '#9ca3af'
      })
    }
  })
  const colores = Array.from(map.values())
  if (varianteBase.value) {
    colores.unshift({
      value: BASE_VARIANTE_VALUE,
      label: 'Estándar',
      hex: '#F5EFE7'
    })
  }
  return colores
})

const largosDisponibles = computed(() => {
  const map = new Map()
  variantesDisponibles.value.forEach((v) => {
    if (!v.largo) return
    if (!map.has(v.largo)) {
      map.set(v.largo, {
        value: v.largo,
        label: formatLargoLabel(v.largo)
      })
    }
  })
  return Array.from(map.values())
})

const formatCalidadLabel = (value) => {
  if (!value) return ''
  return String(value)
    .replace(/_/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/\b\w/g, (char) => char.toUpperCase())
}

const parseCalidades = (raw) => {
  if (!raw) return []
  if (Array.isArray(raw)) {
    return raw.map(formatCalidadLabel).filter(Boolean)
  }
  if (typeof raw === 'string') {
    return raw
      .split(/[|,]/)
      .map((item) => formatCalidadLabel(item))
      .filter(Boolean)
  }
  return []
}

const calidadesDisponibles = computed(() => parseCalidades(producto.value?.calidad))

// Cart State
const cantidad = ref(1)
const showCartDrawer = ref(false)
const cartCount = ref(0)
const carritoItems = ref([])
const isLoggedIn = ref(authService.isAuthenticated())

// Reseñas
const resenasProducto = ref([])
const resenasLoading = ref(false)
const resumenResenas = ref({ promedio: 0, total: 0 })
const miRating = ref(0)
const enviandoResena = ref(false)
const resenaMensaje = ref('')
const resenaError = ref('')

// Accordions
const accordionOpen = ref({
  descripcion: false,
  cuidados: false,
  envios: false
})

// Related Products
const productosRelacionados = ref([])

const CART_STORAGE_KEY = 'kharis_cart_cache'
const CART_COUNT_KEY = 'kharis_cart_count'

// Helper Functions
const isLightColor = (hex) => {
  const c = hex.substring(1)
  const rgb = parseInt(c, 16)
  const r = (rgb >> 16) & 0xff
  const g = (rgb >>  8) & 0xff
  const b = (rgb >>  0) & 0xff
  const luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
  return luma > 160
}

const toggleAccordion = (key) => {
  accordionOpen.value[key] = !accordionOpen.value[key]
}

const isVideo = (url) => {
  if (!url) return false
  const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov']
  const lowerUrl = url.toLowerCase()
  return videoExtensions.some(ext => lowerUrl.endsWith(ext))
}

const openLightbox = () => {
  lightboxOpen.value = true
}

const formatearPrecio = (precio) => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0
  }).format(precio || 0)
}

const handleImageError = (e) => {
  e.target.src = 'https://dummyimage.com/600x600/f3f4f6/9ca3af&text=Sin+imagen'
}

const handleUserLoggedIn = async () => {
  // Simplemente recargar desde localStorage cuando el usuario inicia sesión
  isLoggedIn.value = true
  loadCartCount()
  carritoItems.value = loadCartFromLocal()
}

// Cart Functions
const saveCartToLocal = (items, count) => {
  try {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify({ items, timestamp: Date.now() }))
    localStorage.setItem(CART_COUNT_KEY, String(count))
    cartCount.value = count
  } catch (e) {
    console.warn('No se pudo guardar el carrito local:', e)
  }
}

const loadCartFromLocal = () => {
  try {
    const cached = localStorage.getItem(CART_STORAGE_KEY)
    if (cached) {
      const data = JSON.parse(cached)
      const rawItems = data.items || []
      return rawItems.map((item) => {
        const productoId = item?.producto_id ?? item?.id
        const varianteId = item?.variante_id ?? productoId
        return {
          ...item,
          producto_id: productoId,
          variante_id: varianteId
        }
      })
    }
  } catch (e) {
    console.warn('No se pudo leer el carrito local:', e)
  }
  return []
}

const loadCartCount = () => {
  const stored = localStorage.getItem(CART_COUNT_KEY)
  if (stored) {
    const n = parseInt(stored, 10)
    cartCount.value = isNaN(n) ? 0 : n
  }
}

// Computed
const colorSeleccionadoLabel = computed(() => {
  if (colorSeleccionado.value === BASE_VARIANTE_VALUE) return 'Estándar'
  const color = coloresDisponibles.value.find(c => c.value === colorSeleccionado.value)
  return color?.label || colorSeleccionado.value || ''
})

const selectColor = (color) => {
  if (color.value === BASE_VARIANTE_VALUE) {
    colorSeleccionado.value = BASE_VARIANTE_VALUE
    largoSeleccionado.value = ''
    return
  }
  colorSeleccionado.value = color.value
}

const selectLargo = (largo) => {
  if (colorSeleccionado.value === BASE_VARIANTE_VALUE) {
    colorSeleccionado.value = ''
  }
  largoSeleccionado.value = largo.value
}

const varianteSeleccionada = computed(() => {
  const variantes = variantesDisponibles.value
  if (!variantes.length) return null

  if (colorSeleccionado.value === BASE_VARIANTE_VALUE) {
    return varianteBase.value
  }

  const color = colorSeleccionado.value
  const largo = largoSeleccionado.value

  if (!color && !largo && varianteBase.value) {
    return varianteBase.value
  }

  let match = null
  if (color && largo) {
    match = variantes.find(v => v.color === color && v.largo === largo)
  }
  if (!match && color) {
    match = variantes.find(v => v.color === color)
  }
  if (!match && largo) {
    match = variantes.find(v => v.largo === largo)
  }
  return match || variantes[0]
})

const precioUnitarioSeleccionado = computed(() => {
  return Number(
    varianteSeleccionada.value?.precio_monto ?? producto.value?.precio_monto ?? producto.value?.precio ?? 0
  )
})

const stockDisponible = computed(() => {
  if (varianteSeleccionada.value) {
    return Number(varianteSeleccionada.value.stock_actual ?? 0)
  }
  const p = producto.value
  if (!p) return 0
  return Number(p.stock_actual ?? p.stock ?? p.stock_minimo ?? 0)
})

const cartSubtotal = computed(() => {
  return carritoItems.value.reduce((total, item) => {
    const precio = item.precio_unitario || item.precio_monto || 0
    return total + (precio * item.cantidad)
  }, 0)
})

const promedioRedondeado = computed(() => {
  return Math.round(Number(resumenResenas.value.promedio || 0))
})

const promedioFormateado = computed(() => {
  const total = Number(resumenResenas.value.total || 0)
  const promedio = Number(resumenResenas.value.promedio || 0)
  return total > 0 ? promedio.toFixed(1) : '0.0'
})

// API Functions
const cargarProducto = async () => {
  loading.value = true
  error.value = null
  try {
    const id = route.params.id
    const data = await productosService.getProducto(id)
    producto.value = data
    
    // Set initial active image
    imagenActiva.value = data.imagen_principal
    
    // Build gallery
    const galeria = []
    if (data.imagen_principal) galeria.push(data.imagen_principal)
    if (data.imagenes && Array.isArray(data.imagenes)) {
      const extras = data.imagenes.filter((url) => url && url !== data.imagen_principal)
      galeria.push(...extras)
    }
    if (!imagenActiva.value && galeria.length) {
      imagenActiva.value = galeria[0]
    }
    miniaturas.value = galeria.slice(0, 6)
    
    // Set initial variant selections from variants or product data
    const variantes = Array.isArray(data.variantes) ? data.variantes : []
    if (variantes.length > 0) {
      const base = variantes.find(v => !v.color && !v.largo && v.activo !== false)
      const primera = base || variantes.find(v => v.activo !== false) || variantes[0]
      if (base) {
        colorSeleccionado.value = BASE_VARIANTE_VALUE
        largoSeleccionado.value = ''
      } else {
        colorSeleccionado.value = primera?.color || ''
        largoSeleccionado.value = primera?.largo || ''
      }
    } else {
      if (data.color) colorSeleccionado.value = data.color
      if (data.largo) largoSeleccionado.value = data.largo
    }
    const calidades = parseCalidades(data.calidad)
    calidadSeleccionada.value = calidades[0] || ''

    await cargarResumenResenas()
    await cargarResenasProducto()
    
    // Load related products
    await cargarProductosRelacionados(data.categoria)
  } catch (err) {
    console.error(err)
    error.value = 'No pudimos cargar este producto'
  } finally {
    loading.value = false
  }
}

const cargarResumenResenas = async () => {
  if (!producto.value?.id) return
  try {
    resumenResenas.value = await resenasService.getResumenProducto(producto.value.id)
  } catch (err) {
    resumenResenas.value = { promedio: 0, total: 0 }
  }
}

const cargarResenasProducto = async () => {
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

const enviarResena = async () => {
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

const cargarProductosRelacionados = async (categoria) => {
  try {
    const response = await productosService.getProductos({ categoria, limit: 4 })
    const productos = response.items || response.results || response || []
    // Filter out current product and limit to 4
    productosRelacionados.value = productos
      .filter(p => p.id !== producto.value?.id)
      .slice(0, 4)
  } catch (err) {
    console.warn('No se pudieron cargar productos relacionados:', err)
    productosRelacionados.value = []
  }
}

const agregarAlCarrito = async () => {
  if (!producto.value) return
  if (cantidad.value < 1) cantidad.value = 1
  
  if (stockDisponible.value <= 0) {
    mensajeError.value = 'Este producto no tiene stock disponible'
    mensaje.value = ''
    return
  }

  if (!varianteSeleccionada.value) {
    mensajeError.value = 'Selecciona una combinación de color y largo'
    mensaje.value = ''
    return
  }

  try {
    const precioUnitario = Number(
      varianteSeleccionada.value.precio_monto ?? producto.value.precio_monto ?? producto.value.precio ?? 0
    )
    
    // Usar SIEMPRE localStorage - el carrito es local
    const items = loadCartFromLocal()
    const idx = items.findIndex((i) => (i.variante_id || i.producto_id) === varianteSeleccionada.value.id)
    const cantidadEnCarrito = idx >= 0 ? items[idx].cantidad : 0
    const cantidadTotal = cantidadEnCarrito + cantidad.value
    
    if (cantidadTotal > stockDisponible.value) {
      mensajeError.value = `Solo hay ${stockDisponible.value - cantidadEnCarrito} disponibles para agregar`
      mensaje.value = ''
      return
    }
    
    if (idx >= 0) {
      items[idx].cantidad += cantidad.value
      items[idx].subtotal = items[idx].cantidad * (items[idx].precio_unitario || precioUnitario)
    } else {
      items.push({
        producto_id: producto.value.id,
        variante_id: varianteSeleccionada.value.id,
        variante_sku: varianteSeleccionada.value.sku || '',
        color: varianteSeleccionada.value.color || '',
        largo: varianteSeleccionada.value.largo || '',
        nombre: producto.value.nombre,
        imagen_url: getImageUrl(varianteSeleccionada.value.imagen_url || producto.value.imagen_principal),
        precio_unitario: precioUnitario,
        cantidad: cantidad.value,
        subtotal: precioUnitario * cantidad.value,
      })
    }
    
    const count = items.reduce((sum, i) => sum + (i.cantidad || 1), 0)
    saveCartToLocal(items, count)
    carritoItems.value = loadCartFromLocal()

    mensaje.value = '¡Agregado al carrito!'
    mensajeError.value = ''
    showCartDrawer.value = true
    
    // Clear message after 3 seconds
    setTimeout(() => { mensaje.value = '' }, 3000)
  } catch (err) {
    console.error(err)
    mensajeError.value = 'No se pudo agregar al carrito'
    mensaje.value = ''
  }
}

const closeCartDrawer = () => {
  showCartDrawer.value = false
}

const goToCheckout = () => {
  showCartDrawer.value = false
  router.push('/checkout')
}

// Watch for route changes (when clicking related products)
watch(() => route.params.id, (newId) => {
  if (newId) {
    cargarProducto()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})

onMounted(async () => {
  cargarProducto()
  
  // Cargar carrito desde localStorage
  loadCartCount()
  carritoItems.value = loadCartFromLocal()
  
  window.addEventListener('scroll', handleScroll)
  window.addEventListener('user-logged-in', handleUserLoggedIn)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('user-logged-in', handleUserLoggedIn)
})
</script>

<style scoped>
/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Accordion transition */
.accordion-enter-active,
.accordion-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.accordion-enter-from,
.accordion-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}

.accordion-enter-to,
.accordion-leave-from {
  max-height: 500px;
}

/* Drawer slide transition */
.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: all 0.3s ease;
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  opacity: 0;
}

.drawer-slide-enter-from > div:last-child,
.drawer-slide-leave-to > div:last-child {
  transform: translateX(100%);
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.2);
}
</style>
