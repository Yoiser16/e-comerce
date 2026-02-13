<template>
  <div class="min-h-screen relative">
    
    <!-- Toast notifications -->
    <B2BToast />
    
    <!-- =========================================================================
         HERO SECTION - Carrusel con Efecto Overlay
    ========================================================================== -->
    <section class="relative overflow-hidden">
      
      <!-- ===== SLIDER CONTAINER ===== -->
      <div class="relative w-full overflow-hidden">
        
        <!-- Slides (transición horizontal) -->
        <div 
          class="flex transition-transform duration-700 ease-out"
          :style="{ transform: `translateX(-${currentScene * 100}%)` }"
        >
          
          <!-- ==================== SLIDE 1: Esmeralda ==================== -->
          <div class="w-full flex-shrink-0 bg-[#0b2820] relative">
            <!-- Elementos decorativos (ocultos en móvil) -->
            <div class="absolute inset-0 overflow-hidden hidden lg:block">
              <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-[#0d3d30]/50 rounded-full translate-x-1/3 -translate-y-1/3"></div>
              <div class="absolute bottom-0 left-0 w-80 h-80 bg-[#C9A962]/5 rounded-full -translate-x-1/2 translate-y-1/2"></div>
            </div>
            
            <div class="max-w-7xl mx-auto px-4 sm:px-8 lg:px-12">
              <!-- Móvil: Layout horizontal compacto -->
              <div class="flex lg:hidden items-center min-h-[180px] py-4 gap-3">
                <!-- Texto compacto móvil -->
                <div class="flex-1 pr-2">
                  <span class="text-[#C9A962] text-[9px] font-semibold tracking-[0.15em] uppercase">Mayorista</span>
                  <h1 class="font-luxury leading-[1.15] mt-1">
                    <span class="block text-white text-xl font-bold">Cabello <span class="text-[#C9A962]">Premium</span></span>
                  </h1>
                  <p class="text-white/60 text-xs leading-relaxed mt-2 line-clamp-2">
                    Extensiones 100% Remy y pelucas de lujo
                  </p>
                  <router-link 
                    to="/portal/catalogo"
                    class="inline-flex items-center gap-1.5 mt-3 px-4 py-2 bg-[#C9A962] text-[#0b2820] text-xs font-bold rounded-full"
                  >
                    Ver Catálogo
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                  </router-link>
                </div>
                <!-- Imagen compacta móvil -->
                <div class="relative w-28 h-28 flex-shrink-0">
                  <img 
                    src="/images/card%20panel/5.png" 
                    alt="Productos Premium" 
                    class="w-full h-full object-contain"
                  />
                  <div class="absolute -top-1 -right-1 bg-[#C9A962] rounded-lg px-2 py-1 rotate-3">
                    <p class="text-[#0b2820] text-[8px] font-bold">30% OFF</p>
                  </div>
                </div>
              </div>
              
              <!-- Desktop: Layout original -->
              <div class="hidden lg:grid lg:grid-cols-2 gap-4 min-h-[460px] items-start py-10">
                <!-- Texto -->
                <div class="relative z-10 pt-6">
                  <div class="inline-flex items-center gap-2 mb-4">
                    <span class="w-8 h-px bg-gradient-to-r from-[#C9A962] to-transparent"></span>
                    <span class="text-[#C9A962] text-[10px] font-semibold tracking-[0.2em] uppercase">Portal Mayorista</span>
                  </div>
                  
                  <h1 class="font-luxury leading-[1.1] mb-4">
                    <span class="block text-white/80 text-2xl font-light mb-1">Impulsa tu Negocio con</span>
                    <span class="block text-5xl xl:text-6xl font-bold">
                      <span class="text-white">Cabello </span>
                      <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#C9A962] via-[#E8D5A3] to-[#C9A962]">Premium</span>
                    </span>
                  </h1>
                  
                  <p class="text-white/60 text-base leading-relaxed mb-6 max-w-md">
                    Extensiones 100% Remy, pelucas de lujo y sistemas capilares con los mejores márgenes.
                  </p>
                  
                  <!-- CTAs -->
                  <div class="flex flex-wrap items-center gap-3 mb-6">
                    <router-link 
                      to="/portal/catalogo"
                      class="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-[#C9A962] to-[#D4B574] text-[#0b2820] text-sm font-bold rounded-full shadow-lg hover:scale-[1.02] transition-all"
                    >
                      Explorar Catálogo
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                      </svg>
                    </router-link>
                    
                    <router-link 
                      to="/portal/catalogo?nuevo=true"
                      class="inline-flex items-center gap-2 px-5 py-3 border border-white/25 text-white text-sm font-medium rounded-full hover:bg-white/10 transition-all"
                    >
                      Ver Novedades
                    </router-link>
                  </div>
                </div>
                
                <!-- Imagen con gradient mask -->
                <div class="relative flex items-center justify-end h-[360px]">
                  <div class="absolute inset-0 z-10 pointer-events-none" style="background: linear-gradient(90deg, #0b2820 0%, transparent 20%, transparent 80%, #0b2820 100%);"></div>
                  <div class="absolute inset-0 z-10 pointer-events-none" style="background: linear-gradient(180deg, #0b2820 0%, transparent 15%, transparent 85%, #0b2820 100%);"></div>
                  
                  <img 
                    src="/images/card%20panel/5.png" 
                    alt="Productos Premium" 
                    class="h-full w-auto object-contain relative z-0"
                    style="filter: drop-shadow(0 20px 40px rgba(0,0,0,0.4));"
                  />
                  
                  <div class="absolute top-4 right-8 z-20 bg-[#C9A962] rounded-xl px-4 py-2 shadow-xl rotate-3">
                    <p class="text-[#0b2820] text-[9px] font-bold uppercase">Hasta</p>
                    <p class="text-[#0b2820] text-xl font-black -mt-1">30% OFF</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Gradiente inferior para fundido suave -->
            <div class="absolute bottom-0 left-0 right-0 h-16 lg:h-48 z-10 pointer-events-none" style="background: linear-gradient(to bottom, transparent 0%, rgba(11,40,32,0.6) 40%, #FAFAFA 100%);"></div>
            <div class="h-6 lg:h-16"></div>
          </div>
          
          <!-- ==================== SLIDE 2: Champagne ==================== -->
          <div class="w-full flex-shrink-0 relative overflow-hidden" style="background: linear-gradient(135deg, #F5EBE0 0%, #E8D5C4 40%, #F2E6D9 70%, #DEC9B6 100%);">
            
            <!-- Elementos decorativos de fondo (ocultos en móvil) -->
            <div class="absolute inset-0 overflow-hidden hidden lg:block">
              <div class="absolute -top-20 -right-20 w-[400px] h-[400px] bg-[#C9A962]/10 rounded-full"></div>
              <div class="absolute bottom-0 left-0 w-80 h-80 bg-[#8B7355]/8 rounded-full -translate-x-1/3 translate-y-1/3"></div>
              <div class="absolute top-1/3 left-1/4 w-40 h-40 bg-[#D4A85A]/6 rounded-full"></div>
            </div>
            
            <div class="max-w-7xl mx-auto px-4 sm:px-8 lg:px-12 relative z-10">
              <!-- Móvil: Layout horizontal compacto -->
              <div class="flex lg:hidden items-center min-h-[180px] py-4 gap-3">
                <!-- Texto compacto móvil -->
                <div class="flex-1 pr-2">
                  <span class="text-[#8B7355] text-[9px] font-semibold tracking-[0.15em] uppercase">Certificado</span>
                  <h1 class="font-luxury leading-[1.15] mt-1">
                    <span class="block text-[#2C1810] text-xl font-bold">100% <span class="text-[#8B7355]">Remy</span></span>
                  </h1>
                  <p class="text-[#6B5B4E] text-xs leading-relaxed mt-2 line-clamp-2">
                    Cabello humano de la más alta calidad
                  </p>
                  <router-link 
                    to="/portal/catalogo"
                    class="inline-flex items-center gap-1.5 mt-3 px-4 py-2 bg-[#2C1810] text-white text-xs font-bold rounded-full"
                  >
                    Ver Colección
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                  </router-link>
                </div>
                <!-- Imagen compacta móvil -->
                <div class="relative w-28 h-28 flex-shrink-0">
                  <img 
                    src="/images/card%20panel/6.png" 
                    alt="Extensiones Remy" 
                    class="w-full h-full object-contain"
                  />
                  <div class="absolute -top-1 -right-1 bg-[#2C1810] rounded-lg px-2 py-1 rotate-3">
                    <p class="text-[#C9A962] text-[8px] font-bold">100%</p>
                  </div>
                </div>
              </div>
              
              <!-- Desktop: Layout original -->
              <div class="hidden lg:grid lg:grid-cols-2 gap-4 min-h-[460px] items-start py-10">
                <!-- Texto -->
                <div class="relative z-10 pt-6">
                  <div class="inline-flex items-center gap-2 mb-4">
                    <span class="w-8 h-px bg-gradient-to-r from-[#8B7355] to-transparent"></span>
                    <span class="text-[#8B7355] text-[10px] font-semibold tracking-[0.2em] uppercase">Calidad Certificada</span>
                  </div>
                  
                  <h1 class="font-luxury leading-[1.1] mb-4">
                    <span class="block text-[#5C4A3A] text-2xl font-light mb-1">Extensiones y Pelucas</span>
                    <span class="block text-5xl xl:text-6xl font-bold">
                      <span class="text-[#2C1810]">100% </span>
                      <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#8B7355] via-[#C9A962] to-[#8B7355]">Remy</span>
                    </span>
                  </h1>
                  
                  <p class="text-[#6B5B4E] text-base leading-relaxed mb-6 max-w-md">
                    Cabello humano de la más alta calidad. Precios exclusivos para distribuidores profesionales.
                  </p>
                  
                  <!-- CTAs -->
                  <div class="flex flex-wrap items-center gap-3 mb-6">
                    <router-link 
                      to="/portal/catalogo"
                      class="inline-flex items-center gap-2 px-6 py-3 bg-[#2C1810] text-white text-sm font-bold rounded-full shadow-lg hover:bg-[#1A0F09] hover:scale-[1.02] transition-all"
                    >
                      Ver Colección
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                      </svg>
                    </router-link>
                    
                    <a 
                      href="https://wa.me/4796657763"
                      target="_blank"
                      class="inline-flex items-center gap-2 px-5 py-3 border border-[#8B7355]/40 text-[#2C1810] text-sm font-medium rounded-full hover:bg-[#8B7355]/10 transition-all"
                    >
                      Contactar Asesor
                    </a>
                  </div>
                </div>
                
                <!-- Imagen -->
                <div class="relative flex items-center justify-end h-[360px]">
                  <img 
                    src="/images/card%20panel/6.png" 
                    alt="Extensiones Remy" 
                    class="h-full w-auto object-contain"
                    style="filter: drop-shadow(0 20px 40px rgba(44,24,16,0.25));"
                  />
                  
                  <div class="absolute top-4 right-8 bg-[#2C1810] rounded-xl px-4 py-2 shadow-xl rotate-3">
                    <p class="text-[#C9A962] text-[9px] font-bold uppercase">Certificado</p>
                    <p class="text-white text-xl font-black -mt-1">100%</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Gradiente inferior para fundido suave -->
            <div class="absolute bottom-0 left-0 right-0 h-12 lg:h-40 z-10 pointer-events-none" style="background: linear-gradient(to bottom, transparent 0%, #FAFAFA 100%);"></div>
            <div class="h-6 lg:h-16"></div>
          </div>
          
          <!-- ==================== SLIDE 3: Promoción Estilo ML ==================== -->
          <div class="w-full flex-shrink-0 relative overflow-hidden" style="background: linear-gradient(135deg, #FFE600 0%, #FFB800 50%, #FF9500 100%);">
            
            <!-- Elementos decorativos de fondo (ocultos en móvil) -->
            <div class="absolute inset-0 overflow-hidden hidden lg:block">
              <div class="absolute top-0 left-0 w-96 h-96 bg-white/10 rounded-full -translate-x-1/2 -translate-y-1/2"></div>
              <div class="absolute bottom-0 right-0 w-[500px] h-[500px] bg-orange-500/20 rounded-full translate-x-1/3 translate-y-1/3"></div>
              <div class="absolute top-1/2 left-1/4 w-32 h-32 bg-[#E91E63]/10 rounded-full"></div>
            </div>
            
            <div class="max-w-7xl mx-auto px-4 sm:px-8 lg:px-12 relative z-10">
              <!-- Móvil: Layout compacto horizontal -->
              <div class="flex lg:hidden items-center justify-between min-h-[180px] py-4">
                <!-- Texto izquierda -->
                <div class="flex-1">
                  <div class="inline-flex items-center gap-1.5 bg-[#E91E63] text-white px-2.5 py-1 rounded-full text-[9px] font-bold uppercase mb-2">
                    <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                    Oferta limitada
                  </div>
                  <h2 class="font-luxury text-[#1A1A1A] text-xl font-black leading-none mb-1">
                    LIQUIDACIÓN
                  </h2>
                  <p class="text-[#1A1A1A]/70 text-xs">
                    Descuentos <strong>exclusivos</strong> para mayoristas
                  </p>
                </div>
                <!-- Porcentaje derecha -->
                <div class="flex flex-col items-center justify-center pl-3">
                  <span class="text-[#1A1A1A]/60 text-[10px] font-bold">HASTA</span>
                  <div class="flex items-baseline">
                    <span class="text-[#1A1A1A] text-4xl font-black leading-none">50</span>
                    <span class="text-[#1A1A1A] text-lg font-black">%</span>
                  </div>
                  <span class="text-[#E91E63] text-xl font-black -mt-1">OFF</span>
                </div>
              </div>
              
              <!-- Desktop: Layout original centrado -->
              <div class="hidden lg:flex flex-col items-center justify-start min-h-[460px] py-10 text-center">
                <!-- Badge superior -->
                <div class="inline-flex items-center gap-2 bg-[#E91E63] text-white px-4 py-2 rounded-full text-sm font-bold uppercase tracking-wider mb-6 shadow-lg">
                  <span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
                  Oferta por tiempo limitado
                </div>
                
                <!-- Título principal -->
                <h2 class="font-luxury text-[#1A1A1A] text-7xl font-black leading-none mb-4 drop-shadow-sm">
                  LIQUIDACIÓN
                </h2>
                
                <!-- Porcentaje destacado -->
                <div class="flex items-center justify-center gap-4 mb-6">
                  <span class="text-[#1A1A1A]/70 text-3xl font-bold">HASTA</span>
                  <div class="relative">
                    <span class="text-[#1A1A1A] text-[120px] font-black leading-none">50</span>
                    <span class="absolute -top-2 -right-12 text-[#1A1A1A] text-5xl font-black">%</span>
                  </div>
                  <span class="text-[#E91E63] text-6xl font-black drop-shadow-lg">OFF</span>
                </div>
                
                <!-- Descripción -->
                <p class="text-[#1A1A1A]/80 text-lg max-w-lg">
                  Extensiones, pelucas y sistemas capilares con <strong>descuentos exclusivos</strong> para mayoristas
                </p>
                
                <!-- Footer info -->
                <p class="text-[#1A1A1A]/50 text-xs mt-3">*Aplican términos y condiciones. Válido hasta agotar existencias.</p>
              </div>
            </div>
            
            <!-- Gradiente inferior para fundido suave -->
            <div class="absolute bottom-0 left-0 right-0 h-12 lg:h-40 z-10 pointer-events-none" style="background: linear-gradient(to bottom, transparent 0%, #FAFAFA 100%);"></div>
            <div class="h-6 lg:h-16"></div>
          </div>
        </div>
        
        <!-- Flechas de navegación (solo desktop) -->
        <button 
          @click="prevScene"
          class="hidden lg:flex absolute left-0 top-1/2 -translate-y-1/2 z-20 w-12 h-20 bg-white/90 hover:bg-white shadow-[2px_0_10px_rgba(0,0,0,0.1)] items-center justify-center transition-all rounded-r-xl group"
        >
          <svg class="w-6 h-6 text-gray-500 group-hover:text-gray-800 transition-colors" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
        </button>
        <button 
          @click="nextScene"
          class="hidden lg:flex absolute right-0 top-1/2 -translate-y-1/2 z-20 w-12 h-20 bg-white/90 hover:bg-white shadow-[-2px_0_10px_rgba(0,0,0,0.1)] items-center justify-center transition-all rounded-l-xl group"
        >
          <svg class="w-6 h-6 text-gray-500 group-hover:text-gray-800 transition-colors" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
          </svg>
        </button>
        
        <!-- Indicadores de slide (más abajo en móvil) -->
        <div class="absolute bottom-8 lg:bottom-20 left-1/2 -translate-x-1/2 z-20 flex items-center gap-1.5 lg:gap-2">
          <button 
            v-for="(scene, index) in totalScenes" 
            :key="index"
            @click="goToScene(index)"
            class="rounded-full transition-all duration-300"
            :class="currentScene === index 
              ? 'bg-white w-5 lg:w-6 h-2 lg:h-2.5 shadow-lg' 
              : 'bg-white/40 w-2 lg:w-2.5 h-2 lg:h-2.5 hover:bg-white/60'"
          ></button>
        </div>
      </div>
      
    </section>

    <!-- =========================================================================
         TARJETAS DE CATEGORÍAS - Overlay sobre el carrusel
    ========================================================================== -->
    <section class="relative z-20 -mt-6 lg:-mt-24 pb-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-4 sm:gap-5">
          
          <!-- Card 1: Pelucas Naturales -->
          <router-link 
            to="/portal/catalogo?categoria=pelucas"
            class="bg-white rounded-xl overflow-hidden shadow-lg border border-gray-100"
          >
            <div class="aspect-square overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?q=80&w=600&auto=format&fit=crop" 
                alt="Pelucas naturales"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="p-4 sm:p-5">
              <h3 class="font-bold text-gray-900 text-base sm:text-lg mb-1">Pelucas Naturales</h3>
              <p class="text-gray-500 text-sm mb-3">100% cabello humano</p>
              <span class="text-[#2874A6] text-sm font-medium ">Ver más</span>
            </div>
          </router-link>
          
          <!-- Card 2: Extensiones Premium -->
          <router-link 
            to="/portal/catalogo?categoria=extensiones"
            class="bg-white rounded-xl overflow-hidden shadow-lg border border-gray-100"
          >
            <div class="aspect-square overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1519699047748-de8e457a634e?q=80&w=600&auto=format&fit=crop" 
                alt="Extensiones premium"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="p-4 sm:p-5">
              <h3 class="font-bold text-gray-900 text-base sm:text-lg mb-1">Extensiones Premium</h3>
              <p class="text-gray-500 text-sm mb-3">Técnicas profesionales y más</p>
              <span class="text-[#2874A6] text-sm font-medium ">Ver más</span>
            </div>
          </router-link>
          
          <!-- Card 3: Sistemas Capilares -->
          <router-link 
            to="/portal/catalogo?categoria=sistemas-capilares"
            class="bg-white rounded-xl overflow-hidden shadow-lg border border-gray-100"
          >
            <div class="aspect-square overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1621605815971-fbc98d665033?q=80&w=600&auto=format&fit=crop" 
                alt="Sistemas capilares"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="p-4 sm:p-5">
              <h3 class="font-bold text-gray-900 text-base sm:text-lg mb-1">Sistemas Capilares</h3>
              <p class="text-gray-500 text-sm mb-3">Soluciones profesionales</p>
              <span class="text-[#2874A6] text-sm font-medium ">Ver más</span>
            </div>
          </router-link>
          
          <!-- Card 4: Accesorios -->
          <router-link 
            to="/portal/catalogo?categoria=accesorios"
            class="bg-white rounded-xl overflow-hidden shadow-lg border border-gray-100"
          >
            <div class="aspect-square overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1522337660859-02fbefca4702?q=80&w=600&auto=format&fit=crop" 
                alt="Accesorios"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="p-4 sm:p-5">
              <h3 class="font-bold text-gray-900 text-base sm:text-lg mb-1">Accesorios</h3>
              <p class="text-gray-500 text-sm mb-3">Cuidado & estilizado</p>
              <span class="text-[#2874A6] text-sm font-medium ">Ver más</span>
            </div>
          </router-link>
          
          <!-- Card 5: Ofertas -->
          <router-link 
            to="/portal/catalogo?oferta=true"
            class="bg-white rounded-xl overflow-hidden shadow-lg border border-gray-100 col-span-2 lg:col-span-1"
          >
            <div class="aspect-square overflow-hidden relative">
              <img 
                :src="ofertaCardImage" 
                alt="Ofertas especiales"
                class="w-full h-full object-cover"
              />
              <div class="absolute top-3 right-3 bg-[#CC0C39] text-white text-[10px] sm:text-xs font-bold px-2.5 py-1 rounded-md shadow">
                Hasta 50% dto.
              </div>
            </div>
            <div class="p-4 sm:p-5">
              <h3 class="font-bold text-gray-900 text-base sm:text-lg mb-1">Ofertas Especiales</h3>
              <p class="text-gray-500 text-sm mb-3">Descuentos exclusivos</p>
              <span class="text-[#2874A6] text-sm font-medium ">Ver ofertas</span>
            </div>
          </router-link>
          
        </div>
      </div>
    </section>

    <!-- =========================================================================
         CONTENEDOR MAESTRO - Resto del contenido
    ========================================================================== -->
    <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12 py-6 sm:py-8 lg:py-10">

      <!-- =====================================================================
           SECCIÓN 2: COMIENZA A EXPLORAR (Catálogo B2B)
      ====================================================================== -->
      <section class="mb-12 sm:mb-16">
        <div class="bg-white rounded-lg p-4 sm:p-5">
        <!-- Header sección - Mismo estilo que Categorías -->
        <div class="flex items-center justify-between mb-5 sm:mb-6">
          <h2 class="font-bold text-xl sm:text-2xl text-gray-900">
            {{ hasOrderHistory ? 'Inspirado en tu actividad' : 'Comienza a explorar' }}
          </h2>
          <router-link 
            to="/portal/catalogo"
            class="text-[#007185] hover:text-[#C7511F] hover:underline text-sm font-medium transition-colors"
          >
            Ver todo
          </router-link>
        </div>
        
        <!-- Grid de productos -->
        <div v-if="isLoading" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3 sm:gap-4">
          <B2BSkeleton 
            v-for="n in 10" 
            :key="`skeleton-${n}`"
            variant="rounded" 
            class="aspect-[3/4] h-full" 
          />
        </div>
        
        <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3 sm:gap-4">
          <router-link 
            v-for="(product, index) in frequentProducts" 
            :key="product.id"
            :to="`/portal/producto/${product.id}`"
            :style="{ 
              animationDelay: getAnimationDelay(index),
              opacity: hasAnimated ? 1 : 0
            }"
            class="rounded-lg border border-gray-100 hover:shadow-md transition-shadow duration-200 overflow-hidden animate-fade-in-up"
          >
            <!-- Imagen -->
            <div class="relative">
              <div class="aspect-square overflow-hidden bg-gray-50">
                <video
                  v-if="isVideoUrl(product.image) && !hasMediaError(product)"
                  :src="product.image"
                  class="w-full h-full object-cover"
                  muted
                  playsinline
                  loop
                  autoplay
                  @error="handleVideoError(product)"
                ></video>
                <img
                  v-else
                  :src="getDisplayImage(product)"
                  :alt="product.name"
                  class="w-full h-full object-cover"
                  @error="handleProductImageError($event, product)"
                  loading="lazy"
                />
              </div>
              
              <!-- Botón de añadir rápido -->
              <button 
                @click.stop.prevent="quickAddToCart(product)"
                class="absolute bottom-2 right-2 w-8 h-8 bg-white hover:bg-[#E91E63] hover:text-white text-gray-700 rounded-full flex items-center justify-center shadow-md border border-gray-200 opacity-0 group-hover:opacity-100 transition-all duration-200"
                aria-label="Añadir rápido"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
              </button>
            </div>
            
            <!-- Info del producto -->
            <div class="p-3 sm:p-4">
              <!-- Nombre del producto -->
              <p class="text-gray-800 text-[13px] sm:text-sm line-clamp-2 leading-snug mb-2 min-h-[2.25rem]">
                {{ product.name }}
              </p>
              
              <!-- Precio -->
              <p v-if="product?.originalPrice && product.originalPrice > product.price" class="text-gray-400 text-xs line-through">
                ${{ (product?.originalPrice || 0).toLocaleString() }}
              </p>
              <div class="flex items-baseline gap-2">
                <p class="text-gray-900 font-bold text-base sm:text-lg">
                  ${{ (product?.price || 0).toLocaleString() }}
                </p>
                <span v-if="product?.discount" class="text-emerald-600 text-xs font-semibold">
                  {{ product.discount }}% OFF
                </span>
              </div>
              
              <!-- Envío / Stock -->
              <div class="flex items-center gap-1.5 mt-1.5">
                <span class="text-emerald-600 text-xs font-medium">Envío gratis</span>
              </div>
              
              <div class="flex items-center gap-1 mt-1">
                <span class="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>
                <span class="text-gray-400 text-[11px]">{{ product.stock || '150' }} Uds. disponibles</span>
              </div>
            </div>
          </router-link>
        </div>
        
        <!-- Botón ver catálogo móvil -->
        <div class="text-center mt-6 sm:hidden">
          <router-link 
            to="/portal/catalogo"
            class="inline-flex items-center gap-2 px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white text-sm font-medium rounded-lg transition-colors"
          >
            Ver catálogo completo
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </router-link>
        </div>
        </div>
      </section>

      <!-- =====================================================================
           BENEFITS BAR - Cards con imágenes premium
      ====================================================================== -->
      <section class="mb-12 sm:mb-16">
        <div class="bg-gradient-to-br from-[#FAF8F5] to-[#F5F0EA] rounded-2xl sm:rounded-3xl border border-[#E8E0D5] overflow-hidden">
          
          <!-- Header sutil y elegante -->
          <div class="px-5 sm:px-6 lg:px-8 py-5 sm:py-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-[#E8E0D5]">
            <div>
              <span class="text-[#C9A962] text-[10px] sm:text-xs font-semibold tracking-[0.15em] uppercase mb-1 block">Exclusivo para mayoristas</span>
              <h2 class="text-base sm:text-lg lg:text-xl font-bold text-[#2C1810]">Los mejores beneficios para tu negocio</h2>
            </div>
            <router-link 
              to="/portal/catalogo"
              class="flex-shrink-0 inline-flex items-center gap-2 px-5 py-2.5 sm:px-6 sm:py-3 bg-[#2C1810] hover:bg-[#1A0F0A] text-white text-xs sm:text-sm font-medium rounded-full transition-all duration-300"
            >
              Ver productos
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
              </svg>
            </router-link>
          </div>
          
          <div class="grid grid-cols-2 lg:grid-cols-4">
            
            <!-- Benefit 1: Envío gratis -->
            <div class="relative p-4 sm:p-6 lg:p-8 flex flex-col items-center text-center border-b lg:border-b-0 border-r border-[#E8E0D5] hover:bg-white/60 transition-colors duration-300">
              <div class="w-20 h-20 sm:w-24 sm:h-24 lg:w-28 lg:h-28 rounded-2xl overflow-hidden mb-3 sm:mb-4 bg-white shadow-md">
                <img 
                  src="/images/card%20panel/1.png" 
                  alt="Envío gratis" 
                  class="w-full h-full object-cover blur-[0.3px]"
                  style="image-rendering: auto;"
                  loading="lazy"
                />
              </div>
              <p class="font-medium text-[#2C1810] text-xs sm:text-sm leading-snug">Envíos gratis en productos desde $150.000</p>
            </div>
            
            <!-- Benefit 2: 100% Humano -->
            <div class="relative p-4 sm:p-6 lg:p-8 flex flex-col items-center text-center border-b lg:border-b-0 lg:border-r border-[#E8E0D5] hover:bg-white/60 transition-colors duration-300">
              <div class="w-20 h-20 sm:w-24 sm:h-24 lg:w-28 lg:h-28 rounded-2xl overflow-hidden mb-3 sm:mb-4 bg-white shadow-md">
                <img 
                  src="/images/card%20panel/2.png" 
                  alt="Calidad Premium" 
                  class="w-full h-full object-cover blur-[0.3px]"
                  style="image-rendering: auto;"
                  loading="lazy"
                />
              </div>
              <p class="font-medium text-[#2C1810] text-xs sm:text-sm leading-snug">Cabello 100% humano Remy certificado</p>
            </div>
            
            <!-- Benefit 3: Pago Seguro -->
            <div class="relative p-4 sm:p-6 lg:p-8 flex flex-col items-center text-center border-r border-[#E8E0D5] hover:bg-white/60 transition-colors duration-300">
              <div class="w-20 h-20 sm:w-24 sm:h-24 lg:w-28 lg:h-28 rounded-2xl overflow-hidden mb-3 sm:mb-4 bg-white shadow-md">
                <img 
                  src="/images/card%20panel/3.png" 
                  alt="Pago Seguro" 
                  class="w-full h-full object-cover blur-[0.3px]"
                  style="image-rendering: auto;"
                  loading="lazy"
                />
              </div>
              <p class="font-medium text-[#2C1810] text-xs sm:text-sm leading-snug">Pago seguro con encriptación SSL</p>
            </div>
            
            <!-- Benefit 4: Soporte VIP -->
            <div class="relative p-4 sm:p-6 lg:p-8 flex flex-col items-center text-center hover:bg-white/60 transition-colors duration-300">
              <div class="w-20 h-20 sm:w-24 sm:h-24 lg:w-28 lg:h-28 rounded-2xl overflow-hidden mb-3 sm:mb-4 bg-white shadow-md">
                <img 
                  src="/images/card%20panel/4.png" 
                  alt="Asesoría VIP" 
                  class="w-full h-full object-cover blur-[0.3px]"
                  style="image-rendering: auto;"
                  loading="lazy"
                />
              </div>
              <p class="font-medium text-[#2C1810] text-xs sm:text-sm leading-snug">Asesor personal disponible 24/7</p>
            </div>
            
          </div>
        </div>
      </section>

      <!-- =====================================================================
           SECCIÓN 3: OFERTAS - Layout Mercado Libre
           Izq: Oferta del día (card grande)
           Der: Carrusel horizontal de ofertas con flecha
      ====================================================================== -->
      <section class="mb-10 sm:mb-14">
        
        <!-- Skeleton loading -->
        <div v-if="isLoading" class="grid grid-cols-1 lg:grid-cols-[minmax(300px,1fr)_2fr] gap-4">
          <div class="bg-white rounded-md shadow-sm p-6">
            <B2BSkeleton variant="rounded" class="aspect-square" />
          </div>
          <div class="bg-white rounded-md shadow-sm p-6">
            <div class="flex gap-4 overflow-hidden">
              <B2BSkeleton v-for="n in 4" :key="`sk-of-${n}`" variant="rounded" class="min-w-[160px] aspect-[3/4]" />
            </div>
          </div>
        </div>
        
        <!-- Contenido real -->
        <div v-else-if="featuredProducts.length > 0" class="grid grid-cols-1 lg:grid-cols-[minmax(300px,1fr)_2fr] gap-4">
          
          <!-- ============ OFERTA DEL DÍA (Izquierda) ============ -->
          <router-link 
            :to="`/portal/producto/${featuredProducts[0].id}`"
            class="bg-white rounded-md shadow-sm p-5 sm:p-6 flex flex-col"
          >
            <h3 class="font-bold text-xl text-gray-900 mb-5">Oferta del día</h3>
            
            <!-- Imagen centrada -->
            <div class="flex-1 flex items-center justify-center px-4 mb-5">
              <video
                v-if="isVideoUrl(featuredProducts[0].image) && !hasMediaError(featuredProducts[0])"
                :src="featuredProducts[0].image"
                class="max-w-full max-h-[280px] object-contain"
                muted
                playsinline
                loop
                autoplay
                @error="handleVideoError(featuredProducts[0])"
              ></video>
              <img
                v-else
                :src="getDisplayImage(featuredProducts[0])"
                :alt="featuredProducts[0].name"
                class="max-w-full max-h-[280px] object-contain"
                @error="handleProductImageError($event, featuredProducts[0])"
                loading="lazy"
              />
            </div>
            
            <!-- Info -->
            <p class="text-gray-800 text-sm leading-snug mb-2 line-clamp-2">
              {{ featuredProducts[0].name }}
            </p>
            
            <p v-if="featuredProducts[0]?.originalPrice && featuredProducts[0].originalPrice > featuredProducts[0].price" class="text-gray-400 text-sm line-through">
              ${{ (featuredProducts[0]?.originalPrice || 0).toLocaleString() }}
            </p>
            
            <div class="flex items-baseline gap-2.5 mb-1">
              <span class="text-[28px] font-light text-gray-900">
                ${{ (featuredProducts[0]?.price || 0).toLocaleString() }}
              </span>
              <span v-if="featuredProducts[0]?.discount" class="text-emerald-600 text-sm font-semibold">
                {{ featuredProducts[0].discount }}% OFF
              </span>
            </div>
            
            <span class="text-emerald-600 text-[13px] font-medium">Envío gratis</span>
          </router-link>
          
          <!-- ============ OFERTAS CARRUSEL (Derecha) ============ -->
          <div class="bg-white rounded-md shadow-sm p-5 sm:p-6 flex flex-col">
            <!-- Header -->
            <div class="flex items-baseline gap-3 mb-5">
              <h3 class="font-bold text-xl text-gray-900">Ofertas</h3>
              <router-link 
                to="/portal/catalogo?orden=nuevo"
                class="text-[#007185] hover:text-[#C7511F] hover:underline text-sm font-medium"
              >
                Mostrar todas las ofertas
              </router-link>
            </div>
            
            <!-- Carrusel -->
            <div class="relative flex-1">
              <!-- Flecha izquierda -->
              <button 
                v-show="canScrollOffersLeft"
                @click="scrollOffers(-1)"
                class="absolute left-0 top-1/3 -translate-y-1/2 z-10 w-10 h-10 bg-white rounded-full shadow-lg border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition-colors"
              >
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              
              <!-- Contenedor scroll -->
              <div 
                ref="offersContainer"
                @scroll="onOffersScroll"
                class="flex gap-4 overflow-x-auto scrollbar-hide scroll-smooth"
                style="-ms-overflow-style: none; scrollbar-width: none;"
              >
                <router-link 
                  v-for="product in featuredProducts.slice(1)" 
                  :key="product.id"
                  :to="`/portal/producto/${product.id}`"
                  class="flex-shrink-0 w-[140px] sm:w-[170px]"
                >
                  <!-- Imagen -->
                  <div class="w-full aspect-[3/4] overflow-hidden rounded bg-gray-50 mb-2.5">
                    <video
                      v-if="isVideoUrl(product.image) && !hasMediaError(product)"
                      :src="product.image"
                      class="w-full h-full object-contain"
                      muted
                      playsinline
                      loop
                      autoplay
                      @error="handleVideoError(product)"
                    ></video>
                    <img
                      v-else
                      :src="getDisplayImage(product)"
                      :alt="product.name"
                      class="w-full h-full object-contain"
                      @error="handleProductImageError($event, product)"
                      loading="lazy"
                    />
                  </div>
                  
                  <!-- Nombre -->
                  <p class="text-gray-800 text-[13px] line-clamp-2 leading-snug mb-2">
                    {{ product.name }}
                  </p>
                  
                  <!-- Precio anterior -->
                  <p v-if="product?.originalPrice && product.originalPrice > product.price" class="text-gray-400 text-xs line-through">
                    ${{ (product?.originalPrice || 0).toLocaleString() }}
                  </p>
                  
                  <!-- Precio + descuento -->
                  <div class="flex items-baseline gap-1.5 flex-wrap">
                    <span class="text-[22px] font-light text-gray-900">
                      ${{ (product?.price || 0).toLocaleString() }}
                    </span>
                    <span v-if="product?.discount" class="text-emerald-600 text-xs font-semibold">
                      {{ product.discount }}% OFF
                    </span>
                  </div>
                  
                  <span class="text-emerald-600 text-[12px] font-medium mt-1 block">Envío gratis</span>
                </router-link>
              </div>
              
              <!-- Flecha derecha -->
              <button 
                v-show="canScrollOffersRight"
                @click="scrollOffers(1)"
                class="absolute right-0 top-1/3 -translate-y-1/2 z-10 w-10 h-10 bg-white rounded-full shadow-lg border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition-colors"
              >
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
          
        </div>
        
        <!-- Empty state -->
        <div v-else class="bg-white rounded-md shadow-sm p-8 text-center">
          <p class="text-gray-400 text-sm">No hay ofertas disponibles en este momento</p>
        </div>
        
        <!-- Botón explorar -->
        <div v-if="featuredProducts.length > 0" class="text-center mt-8">
          <router-link 
            to="/portal/catalogo"
            class="inline-flex items-center gap-2 px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white text-sm font-medium rounded-lg transition-colors"
          >
            Explorar catálogo completo
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </router-link>
        </div>
      </section>

      <!-- =====================================================================
           BANNER CTA - Asesoría (dentro del contenedor maestro)
      ====================================================================== -->
      <section class="mb-8">
        <div class="relative bg-gradient-to-r from-[#18181B] to-[#1F1F23] rounded-2xl p-6 sm:p-8 overflow-hidden">
          <!-- Decoración sutil -->
          <div class="absolute top-0 right-0 w-48 h-48 bg-gradient-to-bl from-[#C9A962]/10 to-transparent rounded-full blur-3xl"></div>
          
          <div class="relative flex flex-col sm:flex-row items-center gap-4 sm:gap-6">
            <!-- Icono -->
            <div class="shrink-0 w-14 h-14 bg-[#C9A962]/10 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-[#C9A962]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            
            <div class="flex-1 text-center sm:text-left">
              <h3 class="text-lg sm:text-xl font-semibold text-white mb-1">
                ¿Necesitas asesoría personalizada?
              </h3>
              <p class="text-white/50 text-sm">
                Nuestro equipo mayorista está disponible para ayudarte con tu pedido
              </p>
            </div>
            
            <a 
              href="https://wa.me/4796657763?text=Hola,%20soy%20mayorista%20y%20necesito%20asesoría"
              target="_blank"
              class="shrink-0 px-6 py-3 bg-white/10 hover:bg-white/20 text-white text-sm font-medium rounded-lg transition-all duration-300 flex items-center gap-2 border border-white/10"
            >
              <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
              </svg>
              Contactar ahora
            </a>
          </div>
        </div>
      </section>
      
    </div>
    <!-- FIN DEL CONTENEDOR MAESTRO -->
  </div>
</template>

<script>
import { ref, computed, reactive, onBeforeMount, onMounted, onUnmounted } from 'vue'
import { B2BToast, useToast } from './ui'
import B2BSkeleton from './ui/B2BSkeleton.vue'
import { obtenerProductos, obtenerProductosDestacados } from '@/services/mayoristas'
import { getImageUrl } from '@/services/api'
import { ordenesService } from '@/services/ordenes'
import { vistosService } from '@/services/productos'

export default {
  name: 'B2BDashboard',
  components: {
    B2BToast,
    B2BSkeleton
  },
  setup() {
    // =========================================================================
    // STATE
    // =========================================================================
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{"nombre": "Mayorista"}')
    })

    function getFavoritosKey() {
      const keyPart = user.value?.email || user.value?.id || user.value?.usuario_id || 'anon'
      return `b2b_favoritos_${keyPart}`
    }

    const cartCount = ref(0)
    const currentSlide = ref(0)
    const currentScene = ref(0)  // Sistema de escenarios: 0 = Esmeralda, 1 = Champagne, 2 = Promoción
    
    // Imagen aleatoria para card de ofertas (rota en cada refresh)
    const ofertaImages = ['/images/off.png', '/images/retail.png']
    const ofertaCardImage = ref(ofertaImages[Math.floor(Math.random() * ofertaImages.length)])
    const totalScenes = 3  // Total de slides del Hero
    const isLoading = ref(true)
    const hasAnimated = ref(false)
    let slideInterval = null
    let sceneInterval = null  // Intervalo para cambio de escenas
    
    // Toast notifications
    const toast = useToast()

    // Productos (se cargan desde API)
    const frequentProducts = ref([])
    const featuredProducts = ref([])
    
    // Carrusel de ofertas
    const offersScrollPos = ref(0)
    const offersContainer = ref(null)
    
    // Computed para verificar si tiene historial de compras
    const hasOrderHistory = computed(() => {
      return frequentProducts.value.length > 0 && frequentProducts.value[0]?.lastQty
    })

    // =========================================================================
    // CARRUSEL OFERTAS
    // =========================================================================
    function scrollOffers(direction) {
      const container = offersContainer.value
      if (!container) return
      const cardWidth = container.querySelector('a')?.offsetWidth || 200
      const scrollAmount = cardWidth + 16 // card width + gap
      container.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' })
    }
    
    function onOffersScroll() {
      const container = offersContainer.value
      if (!container) return
      offersScrollPos.value = container.scrollLeft
    }
    
    const canScrollOffersLeft = computed(() => offersScrollPos.value > 0)
    const canScrollOffersRight = computed(() => {
      const container = offersContainer.value
      if (!container) return true
      return offersScrollPos.value < container.scrollWidth - container.clientWidth - 2
    })

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

    const mediaErrors = reactive({})

    // =========================================================================
    // SISTEMA DE ESCENARIOS (Hero Section)
    // =========================================================================
    function startSceneShow() {
      sceneInterval = setInterval(() => {
        currentScene.value = (currentScene.value + 1) % totalScenes
      }, 6000) // Cambio cada 6 segundos
    }

    function goToScene(index) {
      currentScene.value = index
      // Reiniciar el intervalo para que no cambie inmediatamente
      if (sceneInterval) {
        clearInterval(sceneInterval)
        startSceneShow()
      }
    }

    function nextScene() {
      currentScene.value = (currentScene.value + 1) % totalScenes
      // Reiniciar el intervalo
      if (sceneInterval) {
        clearInterval(sceneInterval)
        startSceneShow()
      }
    }

    function prevScene() {
      currentScene.value = (currentScene.value - 1 + totalScenes) % totalScenes
      // Reiniciar el intervalo
      if (sceneInterval) {
        clearInterval(sceneInterval)
        startSceneShow()
      }
    }

    function stopSceneShow() {
      if (sceneInterval) {
        clearInterval(sceneInterval)
        sceneInterval = null
      }
    }

    // =========================================================================
    // HANDLERS
    // =========================================================================
    function getPlaceholderImage(product) {
      const initials = product?.name?.substring(0, 2).toUpperCase() || 'PR'
      return `https://placehold.co/400x500/f5f5f5/999999?text=${encodeURIComponent(initials)}`
    }

    function hasMediaError(product) {
      return !!mediaErrors[product?.id]
    }

    function getDisplayImage(product) {
      if (hasMediaError(product)) return getPlaceholderImage(product)
      return product?.image || getPlaceholderImage(product)
    }

    function isVideoUrl(url) {
      const value = (url || '').toLowerCase()
      return value.includes('.mp4') || value.includes('.webm') || value.includes('.ogg')
    }

    function handleProductImageError(event, product) {
      if (product?.id) {
        mediaErrors[product.id] = true
      }
      event.target.src = getPlaceholderImage(product)
    }

    function handleVideoError(product) {
      if (product?.id) {
        mediaErrors[product.id] = true
      }
    }

    function quickAddToCart(product) {
      // TODO: Integrar con servicio de carrito real
      cartCount.value++
      console.log('Agregado al carrito:', product.name)
      
      // Feedback visual elegante con toast
      toast.success(`${product.name} agregado al carrito`, 3000)
      
      // Animación del botón (manejado por CSS transition)
      const button = event.target.closest('button')
      if (button) {
        button.classList.add('scale-95')
        setTimeout(() => button.classList.remove('scale-95'), 150)
      }
    }
    
    // Staggered animation delay helper
    function getAnimationDelay(index) {
      return `${index * 100}ms`
    }

    // =========================================================================
    // NORMALIZAR DATOS DE PRODUCTOS
    // =========================================================================
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

    function getDiscountPercent(price, originalPrice) {
      const base = Number(originalPrice || 0)
      const current = Number(price || 0)
      if (!base || !current || current >= base) return null
      return Math.round(((base - current) / base) * 100)
    }

    function normalizarProducto(producto) {
      const image = normalizeMediaUrl(
        producto.imagen_principal || producto.imagen || producto.imagen_url || producto.image
      )
      const originalPrice = producto.precio_retail || producto.precio_original || producto.retailPrice || producto.originalPrice || producto.precio || producto.monto_precio || 0
      const price = producto.precio_mayorista || producto.wholesalePrice || producto.monto_precio || producto.price || 0
      return {
        id: producto.id || producto.producto_id,
        name: producto.nombre || producto.name,
        category: producto.categoria || producto.category || 'Sin categoría',
        price,
        originalPrice,
        stock: producto.stock || 0,
        image,
        badge: producto.stock < 5 ? 'low' : null,
        discount: getDiscountPercent(price, originalPrice)
      }
    }

    // =========================================================================
    // CARGAR DATOS DESDE API
    // =========================================================================
    async function cargarProductos() {
      try {
        isLoading.value = true
        
        // Cargar productos destacados (para Novedades)
        const destacados = await obtenerProductosDestacados()
        featuredProducts.value = (Array.isArray(destacados) ? destacados : [])
          .slice(0, 10)
          .map(normalizarProducto)
        
        // =====================================================================
        // ALGORITMO "TUS HABITUALES" - Inspirado en MercadoLibre
        // Prioridad: 1) Vistos recientemente  2) Favoritos  3) Productos destacados
        // =====================================================================
        const userEmail = user.value?.email
        let productosHabituales = []
        const productosUnicos = new Set() // Para evitar duplicados
        
        if (userEmail) {
          // 1. Cargar productos vistos recientemente
          try {
            const vistos = await vistosService.listar(userEmail, 10)
            if (vistos && vistos.length > 0) {
              vistos.forEach(v => {
                if (!productosUnicos.has(v.producto_id)) {
                  productosUnicos.add(v.producto_id)
                  const originalPrice = v.precio || 0
                  const price = v.precio_mayorista || originalPrice
                  productosHabituales.push({
                    id: v.producto_id,
                    name: v.nombre,
                    category: v.categoria || 'Sin categoría',
                    price,
                    originalPrice,
                    stock: v.stock || 0,
                    image: normalizeMediaUrl(v.imagen_principal || v.imagen || v.imagen_url),
                    badge: 'visto', // Badge para identificar origen
                    veces_visto: v.veces_visto,
                    discount: getDiscountPercent(price, originalPrice)
                  })
                }
              })
            }
          } catch (err) {
            // Silenciar errores de productos vistos
          }
          
          // 2. Agregar productos favoritos desde localStorage (sin duplicar)
          try {
            const storedFavoritos = localStorage.getItem(getFavoritosKey())
            if (storedFavoritos) {
              const favoritosIds = JSON.parse(storedFavoritos)
              
              // Cargar solo los primeros 3 favoritos para no saturar
              const limitedIds = favoritosIds.slice(0, 3)
              
              for (const productoId of limitedIds) {
                if (!productosUnicos.has(productoId)) {
                  try {
                    const producto = await obtenerProducto(productoId)
                    productosUnicos.add(productoId)
                    const originalPrice = producto.precio_retail || producto.precio_original || producto.precio || producto.monto_precio || 0
                    const price = producto.precio_mayorista || producto.monto_precio || originalPrice
                    productosHabituales.push({
                      id: producto.id,
                      name: producto.nombre,
                      category: producto.categoria_nombre || 'Favorito',
                      price,
                      originalPrice,
                      stock: producto.stock_actual || 0,
                      image: normalizeMediaUrl(producto.imagen_principal),
                      badge: 'favorito',
                      discount: getDiscountPercent(price, originalPrice)
                    })
                  } catch {
                    // Producto no disponible, continuar con el siguiente
                  }
                }
              }
            }
          } catch {
            // Silenciar errores de favoritos
          }
        }
        
        // Garantizar mínimo 5 productos siempre
        const MIN_PRODUCTOS = 5
        const MAX_PRODUCTOS = 10
        
        if (productosHabituales.length >= MIN_PRODUCTOS) {
          // Tiene suficientes productos vistos/favoritos
          frequentProducts.value = productosHabituales.slice(0, MAX_PRODUCTOS)
        } else {
          // Rellenar con productos destacados o generales hasta completar el mínimo
          try {
            const complemento = await obtenerProductos({ limit: MAX_PRODUCTOS })
            const productosExtra = (Array.isArray(complemento) ? complemento : [])
              .map(normalizarProducto)
              .filter(p => !productosUnicos.has(p.id)) // Sin duplicar
            
            const combinados = [...productosHabituales, ...productosExtra]
            frequentProducts.value = combinados.slice(0, MAX_PRODUCTOS)
          } catch (err) {
            // Si falla, al menos mostrar lo que tenemos
            if (productosHabituales.length > 0) {
              frequentProducts.value = productosHabituales
            } else {
              const productos = await obtenerProductos({ limit: MIN_PRODUCTOS })
              frequentProducts.value = (Array.isArray(productos) ? productos : [])
                .map(normalizarProducto)
            }
          }
        }
        
        // Activar animaciones después de cargar
        setTimeout(() => {
          hasAnimated.value = true
        }, 100)
        
      } catch (error) {
        console.error('âŒ [cargarProductos] Error:', error)
        toast.error('Error al cargar productos. Intenta recargar la página.', 5000)
      } finally {
        isLoading.value = false
      }
    }

    // =========================================================================
    // LIFECYCLE
    // =========================================================================
    onBeforeMount(() => {
      // Preparando componente
    })

    onMounted(() => {
      startSlideshow()
      startSceneShow()
      cargarProductos()
      
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
      stopSceneShow()  // Limpiar intervalo de escenarios
    })

    // =========================================================================
    // RETURN
    // =========================================================================
    return {
      user,
      cartCount,
      currentSlide,
      currentScene,
      totalScenes,
      isLoading,
      hasAnimated,
      hasOrderHistory,
      frequentProducts,
      featuredProducts,
      offersContainer,
      offersScrollPos,
      canScrollOffersLeft,
      canScrollOffersRight,
      scrollOffers,
      onOffersScroll,
      nextSlide,
      prevSlide,
      goToScene,
      nextScene,
      prevScene,
      handleProductImageError,
      handleVideoError,
      isVideoUrl,
      getDisplayImage,
      hasMediaError,
      quickAddToCart,
      getAnimationDelay,
      ofertaCardImage
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

/* ============================================
   ANIMACIONES STAGGERED Y TRANSICIONES FLUIDAS
   ============================================ */

/* Fade in up animation para productos */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

/* Hover transitions más suaves */
.group:hover .group-hover\:scale-105 {
  transform: scale(1.05);
}

.group:hover .group-hover\:rotate-90 {
  transform: rotate(90deg);
}

/* Focus states mejorados para accesibilidad WCAG AAA */
button:focus,
a:focus {
  outline: none;
}

button:focus-visible,
a:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}

/* Active state para feedback táctil */
.active\:scale-95:active {
  transform: scale(0.95);
}

/* Backdrop blur para badges */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* Transición del slider horizontal (estilo Mercado Libre) */
[style*="transform: translateX"] {
  transition: transform 700ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Full-width para el Hero (cubre todo el viewport) */
.hero-fullwidth {
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  /* Compensar padding del Layout y cubrir fondos arquitectónicos */
  margin-top: -2rem;
  padding-top: 2rem;
  z-index: 1;
}
@media (min-width: 640px) {
  .hero-fullwidth {
    margin-top: -2.5rem;
    padding-top: 2.5rem;
  }
}
</style>
