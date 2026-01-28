<template>
  <div class="min-h-screen bg-[#F9F8F6]">
    
    <!-- ========================================
         TOP BAR - Carrusel de Anuncios (Minimalista)
         ======================================== -->
    <div class="fixed top-0 left-0 right-0 z-[60] bg-white h-7 flex items-center justify-center overflow-hidden">
      <div class="relative h-full w-full flex items-center justify-center">
        <transition
          mode="out-in"
          enter-active-class="transition-all duration-500 ease-out"
          enter-from-class="opacity-0 translate-y-full"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-300 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-full"
        >
          <p 
            :key="currentAnnouncement"
            class="text-[#333] text-[10px] font-normal uppercase tracking-[2px] text-center px-4"
          >
            {{ announcements[currentAnnouncement] }}
          </p>
        </transition>
      </div>
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
      <!-- Mobile Header (lg:hidden) - App Style -->
      <div class="lg:hidden">
        <div class="flex items-center justify-between h-12 px-3">
          <!-- Left: Menu + Search -->
          <div class="flex items-center gap-0.5">
            <button 
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="w-10 h-10 flex items-center justify-center -ml-2"
            >
              <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
              </svg>
            </button>
            <button 
              @click="mobileSearchOpen = !mobileSearchOpen"
              class="w-10 h-10 flex items-center justify-center"
            >
              <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </button>
          </div>
          
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
              @click="mostrarCarrito = true"
            >
              <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
              <span 
                v-if="cartCount > 0"
                class="absolute top-1 right-1 w-4 h-4 text-[9px] font-bold rounded-full flex items-center justify-center bg-text-dark text-white"
              >
                {{ cartCount }}
              </span>
            </button>
          </div>
        </div>
        
        <!-- Mobile Search Bar (expandible) -->
        <transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <div v-if="mobileSearchOpen" class="px-3 pb-3">
            <div class="relative">
              <input 
                type="text"
                v-model="searchQuery"
                @input="getSuggestions"
                @keyup.enter="handleSearch()"
                placeholder="Buscar productos..."
                class="w-full pl-10 pr-4 py-2.5 bg-[#f5f5f5] border-0 rounded-lg text-sm text-text-dark placeholder-text-light focus:outline-none focus:ring-2 focus:ring-text-dark/10"
              />
              <svg 
                class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-light pointer-events-none"
                fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </div>
          </div>
        </transition>
      </div>
      
      <!-- Desktop Header (hidden en móvil) -->
      <div class="hidden lg:block">
        <div class="max-w-7xl mx-auto px-6 xl:px-12">
          <div class="flex items-center justify-between h-16">
            <!-- Logo -->
            <router-link to="/" class="flex-shrink-0">
              <img 
                src="/logo-kharis.png" 
                alt="Kharis Distribuidora" 
                class="h-12 w-auto object-contain hover:opacity-80 transition-opacity"
              />
            </router-link>

            <!-- Buscador Desktop -->
            <div class="flex-1 max-w-md mx-8">
              <div class="relative" ref="searchInputRef">
                <input 
                  type="text"
                  v-model="searchQuery"
                  @input="getSuggestions"
                  @keyup.enter="handleSearch()"
                  @focus="showSuggestions = true"
                  placeholder="Buscar extensiones, accesorios..."
                  class="w-full pl-10 pr-4 py-2.5 bg-[#f5f5f5] border-0 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-text-dark/10 placeholder-text-medium"
                />
                <svg 
                  class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-medium pointer-events-none"
                  fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                </svg>
                
                <!-- Dropdown de Sugerencias -->
                <transition
                  enter-active-class="transition duration-150 ease-out"
                  enter-from-class="opacity-0 -translate-y-2"
                  enter-to-class="opacity-100 translate-y-0"
                  leave-active-class="transition duration-100 ease-in"
                  leave-from-class="opacity-100 translate-y-0"
                  leave-to-class="opacity-0 -translate-y-2"
                >
                  <div 
                    v-if="showSuggestions && searchSuggestions.length > 0"
                    class="absolute top-full left-0 right-0 mt-2 bg-white border border-text-dark/8 rounded-xl overflow-hidden z-50 shadow-lg"
                  >
                    <div class="max-h-80 overflow-y-auto">
                      <button
                        v-for="producto in searchSuggestions"
                        :key="producto.id"
                        @click="verProducto(producto.id)"
                        class="w-full px-4 py-3 hover:bg-[#f9f9f9] transition-colors flex items-center gap-3 text-left border-b border-text-dark/5 last:border-b-0"
                      >
                        <div class="w-10 h-10 rounded-lg overflow-hidden flex-shrink-0 bg-[#f9f9f9]">
                          <img 
                            v-if="producto.imagen_principal"
                            :src="getImageUrl(producto.imagen_principal)"
                            :alt="producto.nombre"
                            class="w-full h-full object-cover"
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm text-text-dark truncate">{{ producto.nombre }}</p>
                        </div>
                        <p class="text-sm font-medium text-text-dark flex-shrink-0">
                          {{ formatearPrecio(producto.precio_monto) }}
                        </p>
                      </button>
                    </div>
                  </div>
                </transition>
              </div>
            </div>

            <!-- Navegación Desktop -->
            <nav class="flex items-center gap-8">
              <router-link to="/" class="text-[11px] font-medium tracking-[1.5px] text-text-dark hover:text-brand-600 transition-colors">INICIO</router-link>
              <router-link to="/catalogo" class="text-[11px] font-medium tracking-[1.5px] text-brand-600">COLECCIÓN</router-link>
              <router-link to="/#mayoreo" class="text-[11px] font-medium tracking-[1.5px] text-text-dark hover:text-brand-600 transition-colors">MAYOREO</router-link>
              <router-link to="/#contacto" class="text-[11px] font-medium tracking-[1.5px] text-text-dark hover:text-brand-600 transition-colors">CONTACTO</router-link>
            </nav>

            <!-- Acciones Desktop -->
            <div class="flex items-center gap-1 ml-6">
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
                @click="mostrarCarrito = true"
              >
                <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
                <span 
                  v-if="cartCount > 0"
                  class="absolute top-1 right-1 w-4 h-4 text-[9px] font-bold rounded-full flex items-center justify-center bg-text-dark text-white"
                >
                  {{ cartCount }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile Menu Drawer -->
    <Teleport to="body">
      <Transition name="drawer-fade">
        <div 
          v-if="mobileMenuOpen"
          class="fixed inset-0 bg-black/40 z-50 lg:hidden"
          @click.self="mobileMenuOpen = false"
        ></div>
      </Transition>
      <Transition name="drawer-slide-left">
        <div 
          v-if="mobileMenuOpen"
          class="fixed left-0 top-0 bottom-0 w-72 bg-white z-50 lg:hidden flex flex-col"
        >
          <!-- Menu Header -->
          <div class="flex items-center justify-between p-4 border-b border-text-dark/5">
            <img src="/logo-kharis.png" alt="Kharis" class="h-8" />
            <button @click="mobileMenuOpen = false" class="w-10 h-10 flex items-center justify-center">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <!-- Menu Links -->
          <nav class="flex-1 py-4">
            <router-link to="/" @click="mobileMenuOpen = false" class="block px-6 py-3 text-sm font-medium text-text-dark">Inicio</router-link>
            <router-link to="/catalogo" @click="mobileMenuOpen = false" class="block px-6 py-3 text-sm font-medium text-brand-600">Catálogo</router-link>
            <router-link to="/#categorias" @click="mobileMenuOpen = false" class="block px-6 py-3 text-sm font-medium text-text-dark">Categorías</router-link>
            <router-link to="/#mayoreo" @click="mobileMenuOpen = false" class="block px-6 py-3 text-sm font-medium text-text-dark">Mayoreo</router-link>
            <router-link to="/#contacto" @click="mobileMenuOpen = false" class="block px-6 py-3 text-sm font-medium text-text-dark">Contacto</router-link>
          </nav>
          
          <!-- Menu Footer -->
          <div class="p-4 border-t border-text-dark/5">
            <router-link 
              to="/login" 
              @click="mobileMenuOpen = false"
              class="block w-full py-3 text-center text-sm font-medium text-white bg-text-dark rounded-lg"
            >
              Iniciar Sesión
            </router-link>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Spacer para el header fijo + top bar (28px + 48px/64px) -->
    <div class="h-[76px] lg:h-[92px]"></div>

    <!-- ========================================
         ENCABEZADO DE COLECCIÓN - Editorial Style
         ======================================== -->
    <section class="pt-8 lg:pt-12 pb-6 lg:pb-8">
      <div class="max-w-[800px] mx-auto px-6 text-center">
        <!-- Breadcrumb sutil -->
        <nav class="flex items-center justify-center gap-2 text-[11px] text-text-medium mb-5 uppercase tracking-[1.5px]">
          <router-link to="/" class="hover:text-text-dark transition-colors">Inicio</router-link>
          <span class="text-text-light">/</span>
          <span class="text-text-dark">Catálogo</span>
        </nav>
        
        <!-- Título Principal -->
        <h1 class="text-2xl sm:text-3xl lg:text-4xl font-semibold text-text-dark uppercase tracking-[3px] mb-4">
          Extensiones y Pelucas Premium
        </h1>
        
        <!-- Descripción -->
        <p class="text-sm text-text-medium leading-relaxed max-w-[550px] mx-auto">
          Eleva tu estilo con nuestra selección exclusiva de cabello 100% humano. 
          Piezas únicas diseñadas para profesionales que buscan volumen, largo y naturalidad.
        </p>
      </div>
    </section>
    
    <!-- Mobile: Mini header con título (se oculta porque ya tenemos el encabezado) -->
    <!-- Eliminado para evitar duplicación -->

    <!-- ========================================
         BARRA DE FILTROS MÓVIL - Horizontal
         ======================================== -->
    <div class="lg:hidden sticky top-[76px] z-30 bg-white border-b border-text-dark/5">
      <div class="flex items-center justify-between px-4 py-2.5">
        <!-- Botón Filtrar -->
        <button 
          @click="mostrarFiltrosMobile = true"
          class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-text-dark"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-9.75 0h9.75" />
          </svg>
          Filtrar
          <span v-if="activeFiltersCount > 0" class="w-5 h-5 text-[10px] font-bold bg-text-dark text-white rounded-full flex items-center justify-center">
            {{ activeFiltersCount }}
          </span>
        </button>
        
        <!-- Botón Ordenar -->
        <button 
          @click="mostrarOrdenarMobile = true"
          class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-text-dark"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 7.5L7.5 3m0 0L12 7.5M7.5 3v13.5m13.5 0L16.5 21m0 0L12 16.5m4.5 4.5V7.5" />
          </svg>
          Ordenar
        </button>
      </div>
    </div>

    <!-- ========================================
         CONTENEDOR PRINCIPAL - Max Width Layout
         ======================================== -->
    <div class="max-w-[1400px] mx-auto px-4 lg:px-8 pb-8 lg:pb-12">
      <div class="lg:grid lg:grid-cols-12 lg:gap-8">
        
        <!-- ========================================
             SIDEBAR DE FILTROS - Desktop (Sticky)
             ======================================== -->
        <aside class="hidden lg:block lg:col-span-3">
          <div class="sticky top-28 space-y-5 max-h-[calc(100vh-140px)] overflow-y-auto pr-2 scrollbar-thin">
            
            <!-- Título Filtros + Limpiar alineados -->
            <div class="flex items-center justify-between">
              <h2 class="text-sm font-semibold text-text-dark uppercase tracking-wider">Filtros</h2>
              <button 
                v-if="activeFiltersCount > 0"
                @click="limpiarFiltros"
                class="text-[11px] text-text-medium hover:text-brand-600 transition-colors underline"
              >
                Limpiar
              </button>
            </div>

            <!-- Filtro: Categorías (Acordeón) -->
            <div class="filter-accordion">
              <button 
                @click="toggleAccordion('categorias')"
                class="w-full flex items-center justify-between py-3 text-left border-b border-text-dark/10"
              >
                <span class="text-sm font-semibold text-text-dark uppercase tracking-wider">Categorías</span>
                <svg 
                  :class="['w-4 h-4 text-text-medium transition-transform duration-300', accordionOpen.categorias ? 'rotate-180' : '']"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="max-h-0 opacity-0"
                enter-to-class="max-h-96 opacity-100"
                leave-active-class="transition-all duration-200 ease-in"
                leave-from-class="max-h-96 opacity-100"
                leave-to-class="max-h-0 opacity-0"
              >
                <div v-show="accordionOpen.categorias" class="py-3 space-y-1 overflow-hidden">
                  <button 
                    @click="filtroCategoria = null"
                    :class="[
                      'w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all duration-200',
                      filtroCategoria === null 
                        ? 'bg-brand-50 text-brand-700 font-medium' 
                        : 'text-text-medium hover:bg-nude-50 hover:text-text-dark'
                    ]"
                  >
                    Todas las categorías
                  </button>
                  <button 
                    v-for="cat in categorias" 
                    :key="cat.id"
                    @click="filtroCategoria = cat.nombre"
                    :class="[
                      'w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all duration-200',
                      filtroCategoria === cat.nombre 
                        ? 'bg-brand-50 text-brand-700 font-medium' 
                        : 'text-text-medium hover:bg-nude-50 hover:text-text-dark'
                    ]"
                  >
                    {{ cat.nombre }}
                  </button>
                </div>
              </transition>
            </div>

            <!-- Filtro: Precio (Dual Range Slider) -->
            <div class="filter-accordion">
              <button 
                @click="toggleAccordion('precio')"
                class="w-full flex items-center justify-between py-3 text-left border-b border-text-dark/10"
              >
                <span class="text-sm font-semibold text-text-dark uppercase tracking-wider">Precio</span>
                <svg 
                  :class="['w-4 h-4 text-text-medium transition-transform duration-300', accordionOpen.precio ? 'rotate-180' : '']"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="max-h-0 opacity-0"
                enter-to-class="max-h-96 opacity-100"
                leave-active-class="transition-all duration-200 ease-in"
                leave-from-class="max-h-96 opacity-100"
                leave-to-class="max-h-0 opacity-0"
              >
                <div v-show="accordionOpen.precio" class="py-3 overflow-hidden">
                  <!-- Display del valor máximo -->
                  <div class="flex items-center justify-between mb-3">
                    <span class="text-sm text-text-medium">Hasta</span>
                    <span class="text-sm font-semibold text-text-dark">{{ formatearPrecio(precioRangoMax) }}</span>
                  </div>
                  
                  <!-- Single Range Slider -->
                  <div class="relative h-1.5 mb-4">
                    <!-- Track Background -->
                    <div class="absolute inset-0 bg-text-dark/10 rounded-full"></div>
                    <!-- Active Track -->
                    <div 
                      class="absolute h-full bg-text-dark rounded-full"
                      :style="{
                        width: ((precioRangoMax - precioMinDisponible) / (precioMaxDisponible - precioMinDisponible)) * 100 + '%'
                      }"
                    ></div>
                    <!-- Max Slider -->
                    <input 
                      type="range"
                      :min="precioMinDisponible"
                      :max="precioMaxDisponible"
                      :step="10000"
                      v-model.number="precioRangoMax"
                      class="range-slider-simple absolute w-full h-full appearance-none bg-transparent pointer-events-auto cursor-pointer"
                    />
                  </div>
                  
                  <!-- Quick Price Filters -->
                  <div class="flex flex-wrap gap-2 mt-3">
                    <button 
                      @click="setQuickPrice(0, 200000)"
                      :class="[
                        'px-3 py-1.5 text-xs rounded-full border transition-colors',
                        precioRangoMax <= 200000 ? 'border-text-dark bg-text-dark text-white' : 'border-text-dark/15 hover:border-text-dark/40'
                      ]"
                    >
                      Hasta $200K
                    </button>
                    <button 
                      @click="setQuickPrice(0, 500000)"
                      :class="[
                        'px-3 py-1.5 text-xs rounded-full border transition-colors',
                        precioRangoMax > 200000 && precioRangoMax <= 500000 ? 'border-text-dark bg-text-dark text-white' : 'border-text-dark/15 hover:border-text-dark/40'
                      ]"
                    >
                      Hasta $500K
                    </button>
                    <button 
                      @click="setQuickPrice(0, precioMaxDisponible)"
                      :class="[
                        'px-3 py-1.5 text-xs rounded-full border transition-colors',
                        precioRangoMax > 500000 ? 'border-text-dark bg-text-dark text-white' : 'border-text-dark/15 hover:border-text-dark/40'
                      ]"
                    >
                      Todos
                    </button>
                  </div>
                </div>
              </transition>
            </div>

            <!-- Filtro: Color (Acordeón con Checkboxes estilizados) -->
            <div class="filter-accordion">
              <button 
                @click="toggleAccordion('color')"
                class="w-full flex items-center justify-between py-3 text-left border-b border-text-dark/10"
              >
                <span class="text-sm font-semibold text-text-dark uppercase tracking-wider">Color</span>
                <svg 
                  :class="['w-4 h-4 text-text-medium transition-transform duration-300', accordionOpen.color ? 'rotate-180' : '']"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="max-h-0 opacity-0"
                enter-to-class="max-h-96 opacity-100"
                leave-active-class="transition-all duration-200 ease-in"
                leave-from-class="max-h-96 opacity-100"
                leave-to-class="max-h-0 opacity-0"
              >
                <div v-show="accordionOpen.color" class="py-3 space-y-1 overflow-hidden">
                  <label 
                    v-for="color in coloresDisponibles" 
                    :key="color"
                    class="flex items-center gap-3 p-2 rounded-lg cursor-pointer hover:bg-nude-50 transition-colors group"
                  >
                    <div class="relative">
                      <input 
                        type="checkbox" 
                        :value="color" 
                        v-model="filtrosColor"
                        class="sr-only peer"
                      >
                      <div class="w-5 h-5 border-2 border-text-dark/20 rounded-md peer-checked:border-brand-600 peer-checked:bg-brand-600 transition-all duration-200 flex items-center justify-center">
                        <svg class="w-3 h-3 text-white opacity-0 peer-checked:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    </div>
                    <div class="flex items-center gap-2">
                      <span 
                        class="w-4 h-4 rounded-full border border-text-dark/10"
                        :style="{ backgroundColor: getColorHex(color) }"
                      ></span>
                      <span class="text-sm text-text-medium group-hover:text-text-dark transition-colors">{{ color }}</span>
                    </div>
                  </label>
                </div>
              </transition>
            </div>

            <!-- Filtro: Tipo (Acordeón) -->
            <div class="filter-accordion">
              <button 
                @click="toggleAccordion('tipo')"
                class="w-full flex items-center justify-between py-3 text-left border-b border-text-dark/10"
              >
                <span class="text-sm font-semibold text-text-dark uppercase tracking-wider">Tipo</span>
                <svg 
                  :class="['w-4 h-4 text-text-medium transition-transform duration-300', accordionOpen.tipo ? 'rotate-180' : '']"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="max-h-0 opacity-0"
                enter-to-class="max-h-96 opacity-100"
                leave-active-class="transition-all duration-200 ease-in"
                leave-from-class="max-h-96 opacity-100"
                leave-to-class="max-h-0 opacity-0"
              >
                <div v-show="accordionOpen.tipo" class="py-3 space-y-1 overflow-hidden">
                  <label 
                    v-for="tipo in tiposDisponibles" 
                    :key="tipo"
                    class="flex items-center gap-3 p-2 rounded-lg cursor-pointer hover:bg-nude-50 transition-colors group"
                  >
                    <div class="relative">
                      <input 
                        type="checkbox" 
                        :value="tipo" 
                        v-model="filtrosTipo"
                        class="sr-only peer"
                      >
                      <div class="w-5 h-5 border-2 border-text-dark/20 rounded-md peer-checked:border-brand-600 peer-checked:bg-brand-600 transition-all duration-200 flex items-center justify-center">
                        <svg class="w-3 h-3 text-white opacity-0 peer-checked:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    </div>
                    <span class="text-sm text-text-medium group-hover:text-text-dark transition-colors">{{ tipo }}</span>
                  </label>
                </div>
              </transition>
            </div>

            <!-- Filtro: Largo -->
            <div class="filter-accordion">
              <button 
                @click="toggleAccordion('largo')"
                class="w-full flex items-center justify-between py-3 text-left border-b border-text-dark/10"
              >
                <span class="text-sm font-semibold text-text-dark uppercase tracking-wider">Largo</span>
                <svg 
                  :class="['w-4 h-4 text-text-medium transition-transform duration-300', accordionOpen.largo ? 'rotate-180' : '']"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="max-h-0 opacity-0"
                enter-to-class="max-h-96 opacity-100"
                leave-active-class="transition-all duration-200 ease-in"
                leave-from-class="max-h-96 opacity-100"
                leave-to-class="max-h-0 opacity-0"
              >
                <div v-show="accordionOpen.largo" class="py-3 overflow-hidden">
                  <div class="flex flex-wrap gap-2">
                    <button 
                      v-for="largo in largosDisponibles" 
                      :key="largo"
                      @click="toggleLargo(largo)"
                      :class="[
                        'px-3 py-2 text-xs font-medium rounded-lg border transition-all duration-200',
                        filtrosLargo.includes(largo)
                          ? 'border-brand-500 bg-brand-50 text-brand-700'
                          : 'border-text-dark/10 text-text-medium hover:border-brand-300 hover:text-brand-600'
                      ]"
                    >
                      {{ largo }}
                    </button>
                  </div>
                </div>
              </transition>
            </div>

          </div>
        </aside>

        <!-- ========================================
             GRID DE PRODUCTOS - Main Content
             ======================================== -->
        <main class="lg:col-span-9">
          <!-- Barra Superior Desktop (alineada con Filtros) -->
          <div class="hidden lg:flex items-center justify-between mb-6">
            <!-- Izquierda: Contador + Filtros activos -->
            <div class="flex items-center gap-3">
              <span class="text-sm text-text-dark font-medium">{{ productosFiltrados.length }} productos</span>
              
              <!-- Filtros activos -->
              <div class="flex items-center gap-2 flex-wrap">
                <span 
                  v-if="filtroCategoria"
                  class="inline-flex items-center gap-1.5 px-3 py-1 bg-white text-text-dark text-xs font-medium rounded-full border border-text-dark/10"
                >
                  {{ filtroCategoria }}
                  <button @click="filtroCategoria = null" class="hover:text-brand-600">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </span>
                <span 
                  v-for="color in filtrosColor" 
                  :key="color"
                  class="inline-flex items-center gap-1.5 px-3 py-1 bg-white text-text-dark text-xs font-medium rounded-full border border-text-dark/10"
                >
                  {{ color }}
                  <button @click="removeColorFilter(color)" class="hover:text-brand-600">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </span>
              </div>
            </div>
            
            <!-- Derecha: Ordenar Desktop -->
            <div class="relative">
              <select 
                v-model="ordenar"
                class="appearance-none pl-4 pr-10 py-2 bg-white border border-text-dark/10 rounded text-sm focus:outline-none cursor-pointer"
              >
                <option value="recientes">Más recientes</option>
                <option value="precio-asc">Precio: Menor a Mayor</option>
                <option value="precio-desc">Precio: Mayor a Menor</option>
                <option value="nombre">Nombre A-Z</option>
              </select>
              <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-medium pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-6">
            <div v-for="n in 8" :key="n" class="animate-pulse">
              <div class="aspect-[3/4] bg-white rounded-lg mb-3 shadow-sm"></div>
              <div class="space-y-2 px-1">
                <div class="h-3 bg-[#f0e8e5] rounded w-3/4"></div>
                <div class="h-4 bg-[#f5ebe8] rounded w-1/3"></div>
              </div>
            </div>
          </div>

          <!-- ========================================
               GRID DE PRODUCTOS - Estilo Editorial Limpio
               ======================================== -->
          <div 
            v-else-if="productosFiltrados.length > 0" 
            class="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-6"
          >
            <!-- Loop limpio solo productos -->
            <div 
              v-for="producto in productosFiltrados" 
              :key="producto.id"
              class="group"
            >
              <!-- Contenedor de Imagen - Clean Style con fondo blanco -->
              <div 
                @click="verProducto(producto.id)"
                class="relative aspect-[3/4] bg-white rounded-lg overflow-hidden mb-3 cursor-pointer shadow-sm hover:shadow-md transition-shadow duration-300"
              >
                <!-- Badge minimalista (esquina superior izquierda) -->
                <div class="absolute top-2 left-2 z-10 flex flex-col gap-1">
                  <span 
                    v-if="isNew(producto)"
                    class="px-2 py-0.5 bg-black text-white text-[9px] font-medium uppercase tracking-wide"
                  >
                    New
                  </span>
                  <span 
                    v-if="producto.precio_anterior && producto.precio_anterior > producto.precio_monto"
                    class="px-2 py-0.5 bg-brand-600 text-white text-[9px] font-medium"
                  >
                    -{{ Math.round((1 - producto.precio_monto / producto.precio_anterior) * 100) }}%
                  </span>
                </div>

                <!-- Imagen Principal -->
                <img 
                  v-if="producto.imagen_principal"
                  :src="getImageUrl(producto.imagen_principal)" 
                  :alt="producto.nombre"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  @error="handleImageError"
                >
                <div v-else class="w-full h-full flex items-center justify-center">
                  <svg class="w-12 h-12 text-text-light/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>

                <!-- Botón carrito circular flotante (esquina inferior derecha) -->
                <button 
                  @click.stop="addToCart(producto)"
                  class="absolute bottom-2 right-2 z-10 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-md hover:bg-black hover:text-white transition-all duration-200 opacity-0 group-hover:opacity-100 lg:opacity-100"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                  </svg>
                </button>
              </div>

              <!-- Info del Producto - Minimalista -->
              <div @click="verProducto(producto.id)" class="cursor-pointer px-1">
                <!-- Nombre -->
                <h3 class="text-xs sm:text-sm text-text-dark line-clamp-2 mb-1.5 leading-snug">
                  {{ producto.nombre }}
                </h3>

                <!-- Precio + Wishlist inline -->
                <div class="flex items-center justify-between">
                  <div class="flex items-baseline gap-2">
                    <p class="text-sm font-semibold text-text-dark">{{ formatearPrecio(producto.precio_monto) }}</p>
                    <p 
                      v-if="producto.precio_anterior && producto.precio_anterior > producto.precio_monto"
                      class="text-xs text-text-light line-through"
                    >
                      {{ formatearPrecio(producto.precio_anterior) }}
                    </p>
                  </div>
                  <button 
                    @click.stop="toggleWishlist(producto.id)"
                    class="p-1 hover:scale-110 transition-transform"
                  >
                    <svg 
                      :class="['w-4 h-4', isInWishlist(producto.id) ? 'text-brand-600 fill-brand-600' : 'text-text-light']"
                      fill="none" 
                      stroke="currentColor" 
                      stroke-width="1.5" 
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                    </svg>
                  </button>
                </div>

                <!-- Variantes de Color (opcional, minimalista) -->
                <div v-if="producto.variantes_color && producto.variantes_color.length > 1" class="flex items-center gap-1 mt-2">
                  <span 
                    v-for="(variante, idx) in producto.variantes_color.slice(0, 4)" 
                    :key="idx"
                    class="w-3 h-3 rounded-full border border-white shadow-sm"
                    :style="{ backgroundColor: getColorHex(variante) }"
                    :title="variante"
                  ></span>
                  <span 
                    v-if="producto.variantes_color.length > 4"
                    class="text-[10px] text-text-light ml-0.5"
                  >
                    +{{ producto.variantes_color.length - 4 }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Sin Resultados -->
          <div v-else class="text-center py-16">
            <div class="w-20 h-20 mx-auto mb-5 bg-[#f5f5f5] rounded-full flex items-center justify-center">
              <svg class="w-10 h-10 text-text-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-text-dark mb-2">No encontramos productos</h3>
            <p class="text-sm text-text-medium mb-5 max-w-sm mx-auto">
              No hay productos que coincidan con los filtros seleccionados.
            </p>
            <button 
              @click="limpiarFiltros"
              class="px-6 py-2.5 bg-black text-white text-sm font-medium rounded-full hover:bg-brand-600 transition-colors"
            >
              Limpiar filtros
            </button>
          </div>
        </main>
      </div>
    </div>

    <!-- ========================================
         MODAL DE FILTROS MÓVIL
         ======================================== -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div 
          v-if="mostrarFiltrosMobile"
          class="fixed inset-0 bg-black/50 z-50 lg:hidden"
          @click.self="mostrarFiltrosMobile = false"
        >
          <div class="absolute right-0 top-0 bottom-0 w-full max-w-sm bg-white overflow-hidden flex flex-col">
            <!-- Header -->
            <div class="flex-shrink-0 border-b border-text-dark/5 px-5 py-4 flex items-center justify-between bg-white">
              <h2 class="text-base font-medium text-text-dark">Filtros</h2>
              <button @click="mostrarFiltrosMobile = false" class="w-10 h-10 rounded-full hover:bg-[#f5f5f5] flex items-center justify-center transition-colors">
                <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Filtros Scrollable -->
            <div class="flex-1 overflow-y-auto p-5 space-y-4">
              
              <!-- Categorías -->
              <div class="bg-nude-50/50 rounded-xl p-4">
                <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-3">Categorías</h3>
                <div class="space-y-1">
                  <button 
                    @click="filtroCategoria = null"
                    :class="[
                      'w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all',
                      filtroCategoria === null ? 'bg-brand-50 text-brand-700 font-medium' : 'text-text-medium hover:bg-white'
                    ]"
                  >
                    Todas las categorías
                  </button>
                  <button 
                    v-for="cat in categorias" 
                    :key="cat.id"
                    @click="filtroCategoria = cat.nombre"
                    :class="[
                      'w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all',
                      filtroCategoria === cat.nombre ? 'bg-brand-50 text-brand-700 font-medium' : 'text-text-medium hover:bg-white'
                    ]"
                  >
                    {{ cat.nombre }}
                  </button>
                </div>
              </div>

              <!-- Precio -->
              <div class="bg-nude-50/50 rounded-xl p-4">
                <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-4">Precio</h3>
                <div class="flex items-center justify-between mb-4">
                  <span class="text-sm font-medium text-text-dark">{{ formatearPrecio(precioRangoMin) }}</span>
                  <span class="text-xs text-text-light">—</span>
                  <span class="text-sm font-medium text-text-dark">{{ formatearPrecio(precioRangoMax) }}</span>
                </div>
                <div class="relative h-2 mt-4">
                  <div class="absolute inset-0 bg-nude-200 rounded-full"></div>
                  <div 
                    class="absolute h-full bg-brand-500 rounded-full"
                    :style="{
                      left: ((precioRangoMin - precioMinDisponible) / (precioMaxDisponible - precioMinDisponible)) * 100 + '%',
                      right: (100 - ((precioRangoMax - precioMinDisponible) / (precioMaxDisponible - precioMinDisponible)) * 100) + '%'
                    }"
                  ></div>
                  <input 
                    type="range"
                    :min="precioMinDisponible"
                    :max="precioMaxDisponible"
                    :step="10000"
                    v-model.number="precioRangoMin"
                    @input="handlePrecioMinChange"
                    class="range-slider absolute w-full h-full appearance-none bg-transparent pointer-events-auto"
                  />
                  <input 
                    type="range"
                    :min="precioMinDisponible"
                    :max="precioMaxDisponible"
                    :step="10000"
                    v-model.number="precioRangoMax"
                    @input="handlePrecioMaxChange"
                    class="range-slider absolute w-full h-full appearance-none bg-transparent pointer-events-auto"
                  />
                </div>
              </div>

              <!-- Color -->
              <div class="bg-nude-50/50 rounded-xl p-4">
                <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-3">Color</h3>
                <div class="space-y-2">
                  <label 
                    v-for="color in coloresDisponibles" 
                    :key="color"
                    class="flex items-center gap-3 p-2 rounded-lg cursor-pointer hover:bg-white transition-colors"
                  >
                    <input 
                      type="checkbox" 
                      :value="color" 
                      v-model="filtrosColor"
                      class="w-4 h-4 rounded border-text-dark/20 text-brand-600 focus:ring-brand-500"
                    >
                    <span 
                      class="w-4 h-4 rounded-full border border-text-dark/10"
                      :style="{ backgroundColor: getColorHex(color) }"
                    ></span>
                    <span class="text-sm text-text-medium">{{ color }}</span>
                  </label>
                </div>
              </div>

              <!-- Tipo -->
              <div class="bg-nude-50/50 rounded-xl p-4">
                <h3 class="text-sm font-semibold text-text-dark uppercase tracking-wider mb-3">Tipo</h3>
                <div class="space-y-2">
                  <label 
                    v-for="tipo in tiposDisponibles" 
                    :key="tipo"
                    class="flex items-center gap-3 p-2 rounded-lg cursor-pointer hover:bg-white transition-colors"
                  >
                    <input 
                      type="checkbox" 
                      :value="tipo" 
                      v-model="filtrosTipo"
                      class="w-4 h-4 rounded border-text-dark/20 text-brand-600 focus:ring-brand-500"
                    >
                    <span class="text-sm text-text-medium">{{ tipo }}</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Footer con botones -->
            <div class="flex-shrink-0 border-t border-text-dark/5 p-4 bg-white space-y-2">
              <button @click="limpiarFiltros" class="w-full px-4 py-3 border border-text-dark/10 rounded-full text-sm font-medium text-text-dark hover:border-text-dark/30 transition-colors">
                Limpiar filtros
              </button>
              <button @click="mostrarFiltrosMobile = false" class="w-full px-4 py-3 bg-text-dark text-white rounded-full text-sm font-medium hover:bg-brand-600 transition-colors">
                Ver {{ productosFiltrados.length }} productos
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ========================================
         MODAL DE ORDENAR MÓVIL
         ======================================== -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div 
          v-if="mostrarOrdenarMobile"
          class="fixed inset-0 bg-black/50 z-50 lg:hidden flex items-end"
          @click.self="mostrarOrdenarMobile = false"
        >
          <div class="w-full bg-white rounded-t-2xl overflow-hidden">
            <!-- Header -->
            <div class="flex items-center justify-between px-5 py-4 border-b border-text-dark/5">
              <h3 class="text-base font-medium text-text-dark">Ordenar por</h3>
              <button @click="mostrarOrdenarMobile = false" class="w-8 h-8 rounded-full hover:bg-[#f5f5f5] flex items-center justify-center">
                <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <!-- Opciones -->
            <div class="py-2">
              <button 
                v-for="opcion in [
                  { value: 'recientes', label: 'Más recientes' },
                  { value: 'precio-asc', label: 'Precio: Menor a Mayor' },
                  { value: 'precio-desc', label: 'Precio: Mayor a Menor' },
                  { value: 'nombre', label: 'Nombre A-Z' }
                ]"
                :key="opcion.value"
                @click="ordenar = opcion.value; mostrarOrdenarMobile = false"
                :class="[
                  'w-full px-5 py-3.5 text-left text-sm flex items-center justify-between transition-colors',
                  ordenar === opcion.value ? 'bg-[#f5f5f5] text-text-dark font-medium' : 'text-text-medium hover:bg-[#fafafa]'
                ]"
              >
                {{ opcion.label }}
                <svg v-if="ordenar === opcion.value" class="w-5 h-5 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
            
            <!-- Safe area bottom -->
            <div class="h-6 bg-white"></div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ========================================
         DRAWER DEL CARRITO
         ======================================== -->
    <Teleport to="body">
      <Transition name="drawer-fade">
        <div 
          v-if="mostrarCarrito"
          class="fixed inset-0 bg-black/40 z-40"
          @click.self="mostrarCarrito = false"
        ></div>
      </Transition>
      <Transition name="drawer-slide">
        <div 
          v-if="mostrarCarrito"
          class="fixed right-0 top-0 bottom-0 w-full max-w-md bg-white shadow-2xl z-50 flex flex-col"
        >
          <!-- Header -->
          <div class="flex-shrink-0 border-b border-text-dark/5 p-6 flex items-center justify-between">
            <div>
              <h2 class="font-luxury text-xl text-text-dark">Mi Carrito</h2>
              <p class="text-xs text-text-medium mt-1">{{ carritoItems.length }} productos</p>
            </div>
            <button 
              @click="mostrarCarrito = false"
              class="w-10 h-10 rounded-full hover:bg-nude-100 flex items-center justify-center transition-colors"
            >
              <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Items del carrito -->
          <div class="flex-1 overflow-y-auto p-6">
            <div v-if="carritoItems.length === 0" class="text-center py-16">
              <div class="w-20 h-20 mx-auto mb-4 bg-nude-100 rounded-full flex items-center justify-center">
                <svg class="w-10 h-10 text-text-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
              </div>
              <p class="text-text-medium text-sm">Tu carrito está vacío</p>
              <button 
                @click="mostrarCarrito = false"
                class="mt-4 text-sm text-brand-600 hover:text-brand-700 font-medium"
              >
                Continuar comprando
              </button>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="item in carritoItems" 
                :key="item.id"
                class="flex gap-4 p-4 bg-nude-50/50 rounded-xl"
              >
                <img 
                  :src="getImageUrl(item.imagen_url)"
                  :alt="item.nombre"
                  @error="handleImageError"
                  class="w-20 h-20 object-cover rounded-lg bg-white"
                >
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-text-dark line-clamp-2">{{ item.nombre }}</h3>
                  <p class="text-xs text-text-medium mt-1">Cantidad: {{ item.cantidad }}</p>
                  <p class="text-sm font-semibold text-text-dark mt-2">{{ formatearPrecio((item.precio_unitario || item.precio_monto || 0) * item.cantidad) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer con totales y botones -->
          <div v-if="carritoItems.length > 0" class="flex-shrink-0 border-t border-text-dark/5 p-6 bg-nude-50/30">
            <div class="space-y-3 mb-6">
              <div class="flex justify-between text-sm text-text-medium">
                <span>Subtotal:</span>
                <span>{{ formatearPrecio(precioSubtotal) }}</span>
              </div>
              <div class="flex justify-between text-sm text-text-medium">
                <span>Envío:</span>
                <span class="text-green-600 font-medium">Gratis</span>
              </div>
              <div class="flex justify-between text-lg font-semibold text-text-dark pt-3 border-t border-text-dark/10">
                <span>Total:</span>
                <span>{{ formatearPrecio(precioSubtotal) }}</span>
              </div>
            </div>
            <button 
              @click="irACheckout"
              class="w-full bg-text-dark hover:bg-brand-600 text-white font-medium py-4 rounded-full transition-colors flex items-center justify-center gap-2"
            >
              Completar pedido
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </button>
            <button 
              @click="mostrarCarrito = false"
              class="w-full mt-3 text-sm text-text-medium hover:text-text-dark transition-colors"
            >
              Seguir comprando
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ========================================
         TOAST DE NOTIFICACIÓN
         ======================================== -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0 translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-4"
      >
        <div 
          v-if="showToast"
          class="fixed bottom-6 right-6 z-50 bg-text-dark text-white px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3"
        >
          <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span class="text-sm font-medium">{{ toastMessage }}</span>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

// Estados principales
const productos = ref([])
const categorias = ref([])
const loading = ref(true)
const cartCount = ref(0)
const mostrarCarrito = ref(false)
const carritoItems = ref([])

// Header
const isScrolled = ref(false)
const mobileMenuOpen = ref(false)
const mobileSearchOpen = ref(false)

// Búsqueda
const searchQuery = ref('')
const searchSuggestions = ref([])
const showSuggestions = ref(false)
const searchInputRef = ref(null)

// Vista
const vistaGrid = ref(true)

// Filtros
const filtroCategoria = ref(null)
const precioMin = ref(null)
const precioMax = ref(null)
const filtrosColor = ref([])
const filtrosTipo = ref([])
const filtrosLargo = ref([])
const ordenar = ref('recientes')

// Precio Range Slider
const precioMinDisponible = ref(0)
const precioMaxDisponible = ref(2000000)
const precioRangoMin = ref(0)
const precioRangoMax = ref(2000000)

// Acordeones
const accordionOpen = ref({
  categorias: true,
  precio: true,
  color: true,
  tipo: false,
  largo: false
})

// Mobile
const mostrarFiltrosMobile = ref(false)
const mostrarOrdenarMobile = ref(false)

// Top Bar Announcements
const announcements = ref([
  'ENVÍO GRATIS EN COMPRAS SUPERIORES A $200.000',
  '5% OFF ADICIONAL PAGANDO CON TRANSFERENCIA',
  'NUEVA COLECCIÓN: EXTENSIONES REMY PREMIUM'
])
const currentAnnouncement = ref(0)
let announcementInterval = null

// Wishlist
const wishlist = ref([])

// Toast
const showToast = ref(false)
const toastMessage = ref('')

// Opciones de filtros disponibles
const coloresDisponibles = ref(['Negro', 'Castaño', 'Rubio', 'Rojo', 'Borgogña', 'Platino', 'Rubio Ceniza'])
const tiposDisponibles = ref(['Liso', 'Ondulado', 'Rizado', 'Afro'])
const largosDisponibles = ref(['30cm', '40cm', '45cm', '50cm', '55cm', '60cm', '65cm', '70cm'])

// Contador de filtros activos
const activeFiltersCount = computed(() => {
  let count = 0
  if (filtroCategoria.value) count++
  count += filtrosColor.value.length
  count += filtrosTipo.value.length
  count += filtrosLargo.value.length
  if (precioRangoMin.value > precioMinDisponible.value || precioRangoMax.value < precioMaxDisponible.value) count++
  return count
})

// Productos filtrados
const productosFiltrados = computed(() => {
  let resultado = [...productos.value]

  // Filtro por categoría
  if (filtroCategoria.value) {
    const target = filtroCategoria.value
    const targetId = typeof target === 'object' && target !== null ? target.id : null
    const targetNombre = typeof target === 'object' && target !== null ? target.nombre : target

    resultado = resultado.filter(p => {
      const categoriaProducto = p.categoria || p.categoria_nombre
      const categoriaId = p.categoria_id
      const matchesNombre = targetNombre
        ? String(categoriaProducto ?? '').toLowerCase() === String(targetNombre).toLowerCase()
        : false
      const matchesId = targetId
        ? String(categoriaId ?? '') === String(targetId)
        : false
      return matchesNombre || matchesId
    })
  }

  // Filtro por precio (Range Slider)
  resultado = resultado.filter(p => {
    const precio = p.precio_monto || 0
    return precio >= precioRangoMin.value && precio <= precioRangoMax.value
  })

  // Filtro por color
  if (filtrosColor.value.length > 0) {
    resultado = resultado.filter(p => filtrosColor.value.includes(p.color))
  }

  // Filtro por tipo
  if (filtrosTipo.value.length > 0) {
    resultado = resultado.filter(p => filtrosTipo.value.includes(p.tipo))
  }

  // Filtro por largo
  if (filtrosLargo.value.length > 0) {
    resultado = resultado.filter(p => filtrosLargo.value.includes(p.largo))
  }

  // Ordenar
  if (ordenar.value === 'precio-asc') {
    resultado.sort((a, b) => a.precio_monto - b.precio_monto)
  } else if (ordenar.value === 'precio-desc') {
    resultado.sort((a, b) => b.precio_monto - a.precio_monto)
  } else if (ordenar.value === 'nombre') {
    resultado.sort((a, b) => a.nombre.localeCompare(b.nombre))
  } else if (ordenar.value === 'rating') {
    resultado.sort((a, b) => (b.rating || 4.5) - (a.rating || 4.5))
  } else {
    resultado.sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion))
  }

  return resultado
})

// Cálculo del precio subtotal del carrito
const precioSubtotal = computed(() => {
  return carritoItems.value.reduce((total, item) => {
    const precio = item.precio_unitario || item.precio_monto || 0
    return total + (precio * item.cantidad)
  }, 0)
})

// Métodos
const cargarProductos = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/v1/productos/')
    productos.value = data
    
    // Calcular rango de precios disponibles
    if (data.length > 0) {
      const precios = data.map(p => p.precio_monto || 0).filter(p => p > 0)
      precioMinDisponible.value = Math.min(...precios)
      precioMaxDisponible.value = Math.max(...precios)
      precioRangoMin.value = precioMinDisponible.value
      precioRangoMax.value = precioMaxDisponible.value
    }
  } catch (error) {
    console.error('Error cargando productos:', error)
  } finally {
    loading.value = false
  }
}

const cargarCategorias = async () => {
  try {
    const { data } = await axios.get('http://localhost:8000/api/v1/categorias/?solo_activas=true')
    categorias.value = data
  } catch (error) {
    console.error('Error cargando categorías:', error)
  }
}

const limpiarFiltros = () => {
  filtroCategoria.value = null
  precioMin.value = null
  precioMax.value = null
  precioRangoMin.value = precioMinDisponible.value
  precioRangoMax.value = precioMaxDisponible.value
  filtrosColor.value = []
  filtrosTipo.value = []
  filtrosLargo.value = []
}

const verProducto = (id) => {
  router.push(`/producto/${id}`)
}

const formatearPrecio = (precio) => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0
  }).format(precio)
}

const loadCartFromLocal = () => {
  try {
    const cart = localStorage.getItem('kharis_cart_cache')
    if (cart) {
      const parsed = JSON.parse(cart)
      carritoItems.value = parsed.items ? parsed.items : parsed
    } else {
      carritoItems.value = []
    }
  } catch (err) {
    carritoItems.value = []
  }
}

const irACheckout = () => {
  mostrarCarrito.value = false
  router.push('/checkout')
}

const getImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}

const handleImageError = (e) => {
  e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f5f5f5" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em" fill="%239ca3af" font-size="10"%3ESin Imagen%3C/text%3E%3C/svg%3E'
}

const loadCartCount = () => {
  try {
    const count = localStorage.getItem('kharis_cart_count')
    cartCount.value = count ? parseInt(count) : 0
  } catch (err) {
    cartCount.value = 0
  }
}

// Scroll handler
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

// Acordeón
const toggleAccordion = (key) => {
  accordionOpen.value[key] = !accordionOpen.value[key]
}

// Price Range handlers
const handlePrecioMinChange = () => {
  if (precioRangoMin.value > precioRangoMax.value) {
    precioRangoMin.value = precioRangoMax.value
  }
}

const handlePrecioMaxChange = () => {
  if (precioRangoMax.value < precioRangoMin.value) {
    precioRangoMax.value = precioRangoMin.value
  }
}

const setQuickPrice = (min, max) => {
  precioRangoMin.value = Math.max(min, precioMinDisponible.value)
  precioRangoMax.value = Math.min(max, precioMaxDisponible.value)
}

// Largo toggle
const toggleLargo = (largo) => {
  const idx = filtrosLargo.value.indexOf(largo)
  if (idx > -1) {
    filtrosLargo.value.splice(idx, 1)
  } else {
    filtrosLargo.value.push(largo)
  }
}

// Remove filter helpers
const removeColorFilter = (color) => {
  const idx = filtrosColor.value.indexOf(color)
  if (idx > -1) filtrosColor.value.splice(idx, 1)
}

const removeTipoFilter = (tipo) => {
  const idx = filtrosTipo.value.indexOf(tipo)
  if (idx > -1) filtrosTipo.value.splice(idx, 1)
}

// Color hex mapping
const getColorHex = (colorName) => {
  const colorMap = {
    'Negro': '#1a1a1a',
    'Castaño': '#5D4037',
    'Rubio': '#D4A76A',
    'Rojo': '#8B0000',
    'Borgogña': '#722F37',
    'Borgoña': '#722F37',
    'Platino': '#E5E4E2',
    'Rubio Ceniza': '#B8A898',
    'Negro Natural': '#2d2d2d',
    'Castaño Oscuro': '#3b2417',
    'Castaño Claro': '#8b6b47'
  }
  return colorMap[colorName] || '#9ca3af'
}

// Product helpers
const isNew = (producto) => {
  if (!producto.fecha_creacion) return false
  const createdDate = new Date(producto.fecha_creacion)
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
  return createdDate > thirtyDaysAgo
}

const getProductRating = (producto) => {
  return producto.rating || Math.floor(Math.random() * 2) + 4 // 4 o 5 estrellas por defecto
}

const getProductReviews = (producto) => {
  return producto.reviews_count || Math.floor(Math.random() * 50) + 10
}

// Wishlist
const loadWishlist = () => {
  try {
    const saved = localStorage.getItem('kharis_wishlist')
    wishlist.value = saved ? JSON.parse(saved) : []
  } catch {
    wishlist.value = []
  }
}

const saveWishlist = () => {
  localStorage.setItem('kharis_wishlist', JSON.stringify(wishlist.value))
}

const toggleWishlist = (productId) => {
  const idx = wishlist.value.indexOf(productId)
  if (idx > -1) {
    wishlist.value.splice(idx, 1)
    showToastMessage('Eliminado de favoritos')
  } else {
    wishlist.value.push(productId)
    showToastMessage('Añadido a favoritos ❤️')
  }
  saveWishlist()
}

const isInWishlist = (productId) => {
  return wishlist.value.includes(productId)
}

// Add to Cart
const addToCart = (producto) => {
  // Cargar carrito actual
  loadCartFromLocal()
  
  const existingIdx = carritoItems.value.findIndex(item => item.id === producto.id)
  
  if (existingIdx > -1) {
    carritoItems.value[existingIdx].cantidad += 1
  } else {
    carritoItems.value.push({
      id: producto.id,
      nombre: producto.nombre,
      precio_monto: producto.precio_monto,
      precio_unitario: producto.precio_monto,
      cantidad: 1,
      imagen_url: producto.imagen_principal
    })
  }
  
  // Guardar en localStorage
  localStorage.setItem('kharis_cart_cache', JSON.stringify({ items: carritoItems.value }))
  cartCount.value = carritoItems.value.reduce((acc, item) => acc + item.cantidad, 0)
  localStorage.setItem('kharis_cart_count', cartCount.value.toString())
  
  showToastMessage(`${producto.nombre} añadido al carrito`)
}

// Toast
const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// Search
const getSuggestions = () => {
  if (searchQuery.value.length < 2) {
    searchSuggestions.value = []
    showSuggestions.value = false
    return
  }
  
  const query = searchQuery.value.toLowerCase()
  searchSuggestions.value = productos.value
    .filter(p => p.nombre.toLowerCase().includes(query))
    .slice(0, 5)
  showSuggestions.value = true
}

const handleSearch = () => {
  showSuggestions.value = false
  // Implementar búsqueda completa si es necesario
}

// Click outside handler for search
const handleClickOutside = (e) => {
  if (searchInputRef.value && !searchInputRef.value.contains(e.target)) {
    showSuggestions.value = false
  }
}

// Lifecycle
onMounted(() => {
  // Preseleccionar categoría si viene por query (?categoria=Nombre)
  if (route.query?.categoria) {
    filtroCategoria.value = route.query.categoria
  }

  cargarProductos()
  cargarCategorias()
  loadCartCount()
  loadCartFromLocal()
  loadWishlist()
  
  window.addEventListener('scroll', handleScroll)
  document.addEventListener('click', handleClickOutside)
  
  // Iniciar carrusel de anuncios
  announcementInterval = setInterval(() => {
    currentAnnouncement.value = (currentAnnouncement.value + 1) % announcements.value.length
  }, 3500)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('click', handleClickOutside)
  
  // Limpiar intervalo del carrusel
  if (announcementInterval) {
    clearInterval(announcementInterval)
  }
})

// Mantener filtro en sync si cambia la query
watch(
  () => route.query.categoria,
  (nuevaCategoria) => {
    filtroCategoria.value = nuevaCategoria || null
  }
)
</script>

<style scoped>
/* Header Catalog - Siempre visible con fondo */
.header-catalog {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 2px 20px -2px rgba(0, 0, 0, 0.06);
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

/* Transiciones del Modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active > div,
.modal-fade-leave-active > div {
  transition: transform 0.3s ease;
}

.modal-fade-enter-from > div {
  transform: translateX(100%);
}

.modal-fade-leave-to > div {
  transform: translateX(100%);
}

/* Drawer Transitions */
.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.3s ease;
}

.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}

.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.3s ease;
}

.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
}

/* Range Slider Custom Styles */
.range-slider {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  cursor: pointer;
}

.range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #D81B60 0%, #e84a7e 100%);
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(216, 27, 96, 0.3);
  cursor: pointer;
  margin-top: -8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.range-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 4px 12px rgba(216, 27, 96, 0.4);
}

.range-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #D81B60 0%, #e84a7e 100%);
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(216, 27, 96, 0.3);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.range-slider::-moz-range-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 4px 12px rgba(216, 27, 96, 0.4);
}

/* Range Slider Simple - Neutral/Elegant */
.range-slider-simple {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  cursor: pointer;
}

.range-slider-simple::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #1A1A1A;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  margin-top: -7px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.range-slider-simple::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

.range-slider-simple::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #1A1A1A;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.range-slider-simple::-moz-range-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

.range-slider-simple::-webkit-slider-runnable-track {
  height: 4px;
  background: #E5E5E5;
  border-radius: 2px;
}

.range-slider-simple::-moz-range-track {
  height: 4px;
  background: #E5E5E5;
  border-radius: 2px;
}

/* Scrollbar personalizado */
.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 2px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.2);
}

/* Touch target for mobile */
.touch-target {
  min-width: 44px;
  min-height: 44px;
}

/* Checkbox custom (fallback) */
input[type="checkbox"]:checked {
  background-color: #D81B60;
  border-color: #D81B60;
}

/* Line clamp utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
