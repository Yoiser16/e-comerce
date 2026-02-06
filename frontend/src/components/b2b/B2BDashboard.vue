<template>
  <div class="min-h-screen bg-[#F8F8F8]">
    
    <!-- Toast notifications -->
    <B2BToast />
    
    <!-- =========================================================================
         HERO BANNER - Beauty Brand with Hair Focus
    ========================================================================== -->
    <div class="relative group mb-8 -mx-4 sm:-mx-6 overflow-hidden rounded-b-3xl">
      <!-- Slider Container -->
      <div 
        class="flex transition-transform duration-700 ease-[cubic-bezier(0.4,0,0.2,1)]"
        :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
      >
        <!-- Slide 1 - PELUCAS Y EXTENSIONES (Principal - Beauty Focus) -->
        <div class="w-full flex-shrink-0 relative">
          <div class="relative h-[280px] sm:h-[340px] lg:h-[400px] bg-gradient-to-br from-[#1A1318] via-[#1F1A1E] to-[#18181B] overflow-hidden">
            <!-- Decorative Hair Texture Background -->
            <div class="absolute inset-0">
              <!-- Soft flowing curves simulating hair -->
              <svg class="absolute right-0 top-0 h-full w-2/3 opacity-10" viewBox="0 0 400 500" fill="none">
                <path d="M200 0 Q350 100 300 250 T250 500" stroke="url(#hairGradient1)" stroke-width="1" fill="none"/>
                <path d="M250 0 Q400 150 320 300 T280 500" stroke="url(#hairGradient1)" stroke-width="0.5" fill="none"/>
                <path d="M300 0 Q450 120 350 280 T310 500" stroke="url(#hairGradient1)" stroke-width="0.5" fill="none"/>
                <path d="M150 0 Q300 80 280 200 T220 500" stroke="url(#hairGradient1)" stroke-width="1" fill="none"/>
                <defs>
                  <linearGradient id="hairGradient1" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#C9A962" stop-opacity="0.8"/>
                    <stop offset="50%" stop-color="#E8D5B0" stop-opacity="0.4"/>
                    <stop offset="100%" stop-color="#C9A962" stop-opacity="0.2"/>
                  </linearGradient>
                </defs>
              </svg>
              <!-- Silk/shine effect overlay -->
              <div class="absolute top-1/4 right-1/4 w-96 h-96 bg-gradient-to-br from-[#C9A962]/8 via-[#E8D5B0]/5 to-transparent rounded-full blur-3xl"></div>
              <div class="absolute bottom-0 right-0 w-80 h-80 bg-gradient-to-tl from-rose-500/5 via-transparent to-transparent rounded-full blur-3xl"></div>
            </div>
            
            <!-- Imagen de fondo - Pelo/Beauty -->
            <img 
              src="/img2.jpg" 
              alt="Pelucas y Extensiones Premium" 
              class="absolute inset-0 w-full h-full object-cover object-center opacity-40"
            />
            <!-- Overlay con gradiente elegante -->
            <div class="absolute inset-0 bg-gradient-to-r from-[#1A1318]/98 via-[#1A1318]/85 to-[#1A1318]/40"></div>
            <div class="absolute inset-0 bg-gradient-to-t from-[#1A1318]/60 via-transparent to-transparent"></div>
            
            <!-- Contenido Principal -->
            <div class="relative h-full flex flex-col justify-center px-6 sm:px-10 lg:px-16 max-w-2xl">
              <!-- Label elegante -->
              <span class="inline-flex items-center gap-3 text-[#E8B4B8] text-[10px] sm:text-[11px] font-medium tracking-[0.25em] uppercase mb-4 sm:mb-5">
                <span class="w-8 h-px bg-gradient-to-r from-[#E8B4B8] to-transparent"></span>
                Belleza profesional
              </span>
              
              <!-- Headline Principal -->
              <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold text-white leading-[1.1] mb-4 sm:mb-6 tracking-tight">
                Pelucas y extensiones<br class="hidden sm:block"/>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#C9A962] via-[#E8D5B0] to-[#C9A962]">
                  que elevan tu belleza
                </span>
              </h2>
              
              <!-- Subtítulo con beneficios -->
              <p class="text-white/60 text-sm sm:text-base mb-6 sm:mb-8 max-w-md leading-relaxed">
                Calidad premium · Venta mayorista · Envíos rápidos a todo el país
              </p>
              
              <!-- CTAs -->
              <div class="flex flex-wrap items-center gap-3">
                <router-link 
                  to="/portal/catalogo?categoria=pelucas"
                  class="inline-flex items-center gap-2 px-5 sm:px-6 py-2.5 sm:py-3 bg-[#C9A962] hover:bg-[#D4AF6A] text-[#18181B] text-sm font-semibold rounded-full transition-all duration-300 group hover:shadow-lg hover:shadow-[#C9A962]/25"
                >
                  Ver pelucas
                  <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </router-link>
                <router-link 
                  to="/portal/catalogo?categoria=extensiones"
                  class="inline-flex items-center gap-2 px-5 sm:px-6 py-2.5 sm:py-3 bg-white/10 hover:bg-white/15 text-white text-sm font-medium rounded-full border border-white/20 hover:border-white/30 transition-all duration-300 group"
                >
                  Explorar extensiones
                  <svg class="w-4 h-4 opacity-60 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </router-link>
              </div>
            </div>
            
            <!-- Decorative Element Right Side - Hair silhouette -->
            <div class="absolute right-0 bottom-0 w-1/3 h-full hidden lg:flex items-end justify-end opacity-20 pointer-events-none">
              <svg viewBox="0 0 200 400" class="h-full w-auto" fill="none">
                <path d="M100 400 Q120 300 90 200 Q60 100 100 0" stroke="#C9A962" stroke-width="0.5" fill="none"/>
                <path d="M120 400 Q140 280 110 180 Q80 80 120 0" stroke="#E8D5B0" stroke-width="0.5" fill="none"/>
                <path d="M80 400 Q100 320 70 220 Q40 120 80 0" stroke="#C9A962" stroke-width="0.3" fill="none"/>
              </svg>
            </div>
          </div>
        </div>
        
        <!-- Slide 2 - Ofertas -->
        <div class="w-full flex-shrink-0 relative">
            <!-- Slide 2 - Ofertas -->
            <div class="relative h-[280px] sm:h-[340px] lg:h-[400px] bg-[#1A1318] overflow-hidden group/slide">
            <!-- Imagen de fondo High-End -->
            <img 
              src="https://images.unsplash.com/photo-1562322140-8baeececf3df?q=80&w=1920&auto=format&fit=crop" 
              alt="Model hair extensions" 
              class="absolute inset-0 w-full h-full object-cover object-center opacity-60 group-hover/slide:scale-105 transition-transform duration-1000 ease-in-out"
            />
            
            <!-- Gradient Overlay Cinematic -->
            <div class="absolute inset-0 bg-gradient-to-r from-[#1A1318] via-[#1A1318]/70 to-transparent"></div>
            
            <div class="relative h-full flex flex-col justify-center px-6 sm:px-10 lg:px-16 max-w-xl">
              <!-- Badge Animado -->
              <div class="animate-fade-in-up" style="animation-delay: 100ms">
                <span class="inline-flex items-center gap-3 text-[#E8B4B8]/90 text-[11px] font-bold tracking-[0.2em] uppercase mb-4">
                  <span class="w-8 h-px bg-[#E8B4B8]"></span>
                  Limited Time Offer
                </span>
              </div>
              
              <!-- Título con Font Luxury -->
              <h2 class="animate-fade-in-up font-luxury text-3xl sm:text-5xl lg:text-6xl font-bold text-white leading-[1.05] mb-4 tracking-tight" style="animation-delay: 200ms">
                Hasta <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#D81B60] to-[#FF4081]">30% OFF</span><br />
                en Extensiones
              </h2>
              
              <!-- Descripción -->
              <p class="animate-fade-in-up text-white/70 text-sm sm:text-base mb-8 max-w-sm leading-relaxed font-light" style="animation-delay: 300ms">
                Eleva tu inventario con nuestra colección exclusiva de cabello 100% Remy.
              </p>
              
              <!-- Botón Premium -->
              <div class="animate-fade-in-up" style="animation-delay: 400ms">
                <router-link 
                  to="/portal/catalogo?oferta=true"
                  class="inline-flex items-center gap-3 px-8 py-3 bg-white text-[#1A1318] text-sm font-bold uppercase tracking-widest rounded-sm hover:bg-[#C9A962] hover:text-white transition-all duration-300 shadow-[0_0_20px_rgba(255,255,255,0.2)] hover:shadow-[0_0_30px_rgba(201,169,98,0.4)]"
                >
                  Comprar Ahora
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                  </svg>
                </router-link>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Slide 3 - Envío Gratis -->
        <div class="w-full flex-shrink-0 relative">
          <div class="relative h-[280px] sm:h-[340px] lg:h-[400px] bg-gradient-to-br from-[#141D1A] via-[#182420] to-[#18181B] overflow-hidden">
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
              <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl font-bold text-white/95 leading-tight mb-3 tracking-tight">
                Envío <span class="text-emerald-400">gratis</span><br class="hidden sm:block"/>
                a todo el país
              </h2>
              <p class="text-white/50 text-sm mb-6 max-w-sm leading-relaxed">
                En pedidos +$500.000. Entrega en 24-48 horas.
              </p>
              <router-link 
                to="/portal/catalogo"
                class="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-500/90 hover:bg-emerald-500 text-white text-sm font-semibold rounded-full transition-all duration-300 w-fit group hover:shadow-lg hover:shadow-emerald-500/20"
              >
                Explorar catálogo
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
         TRUST STRIP - Credibilidad y Confianza
    ========================================================================== -->
    <div class="mb-10 -mx-4 sm:-mx-6 px-4 sm:px-6">
      <div class="bg-gradient-to-r from-[#FDFBF9] via-white to-[#FDFBF9] border border-gray-100 rounded-2xl py-8 px-4 sm:px-8">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8">
          <!-- Envíos rápidos -->
          <div class="flex flex-col items-center text-center gap-3 group">
            <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-[#E8F5E9] to-[#C8E6C9] flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-all duration-300 shadow-md">
              <svg class="w-7 h-7 sm:w-9 sm:h-9 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <p class="text-sm sm:text-base font-semibold text-gray-800">Envíos rápidos</p>
              <p class="text-xs sm:text-sm text-gray-500 mt-0.5">24-48 horas</p>
            </div>
          </div>
          
          <!-- Calidad profesional -->
          <div class="flex flex-col items-center text-center gap-3 group">
            <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-[#FFF8E1] to-[#FFECB3] flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-all duration-300 shadow-md">
              <svg class="w-7 h-7 sm:w-9 sm:h-9 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
              </svg>
            </div>
            <div>
              <p class="text-sm sm:text-base font-semibold text-gray-800">Calidad profesional</p>
              <p class="text-xs sm:text-sm text-gray-500 mt-0.5">100% cabello humano</p>
            </div>
          </div>
          
          <!-- Compra segura -->
          <div class="flex flex-col items-center text-center gap-3 group">
            <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-[#E3F2FD] to-[#BBDEFB] flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-all duration-300 shadow-md">
              <svg class="w-7 h-7 sm:w-9 sm:h-9 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
              </svg>
            </div>
            <div>
              <p class="text-sm sm:text-base font-semibold text-gray-800">Compra segura</p>
              <p class="text-xs sm:text-sm text-gray-500 mt-0.5">Pago protegido</p>
            </div>
          </div>
          
          <!-- Atención personalizada -->
          <div class="flex flex-col items-center text-center gap-3 group">
            <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-br from-[#FCE4EC] to-[#F8BBD9] flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-all duration-300 shadow-md">
              <svg class="w-7 h-7 sm:w-9 sm:h-9 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
              </svg>
            </div>
            <div>
              <p class="text-sm sm:text-base font-semibold text-gray-800">Atención VIP</p>
              <p class="text-xs sm:text-sm text-gray-500 mt-0.5">Asesoría experta</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- =========================================================================
         CATEGORÍAS RÁPIDAS - Visual Beauty Categories
    ========================================================================== -->
    <div class="mb-12">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-lg sm:text-xl font-semibold text-gray-800 tracking-tight">Categorías</h2>
          <p class="text-gray-400 text-sm mt-0.5">Explora nuestro catálogo profesional</p>
        </div>
      </div>
      
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <!-- Pelucas Naturales -->
        <!-- Pelucas Naturales -->
        <router-link 
          to="/portal/catalogo?categoria=pelucas"
          class="group relative overflow-hidden rounded-2xl aspect-[4/3] sm:aspect-[3/2] shadow-sm hover:shadow-xl transition-all duration-500"
        >
          <!-- Imagen de fondo -->
          <img 
            src="https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?q=80&w=800&auto=format&fit=crop" 
            alt="Pelucas naturales"
            class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale-[30%] group-hover:grayscale-0"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#1A1318]/95 via-[#1A1318]/50 to-transparent opacity-90 group-hover:opacity-80 transition-opacity duration-300"></div>
          
          <div class="relative h-full flex flex-col justify-end p-4 sm:p-6">
            <div class="w-10 h-10 rounded-full bg-white/10 border border-white/20 backdrop-blur-md flex items-center justify-center mb-3 group-hover:scale-110 group-hover:bg-[#C9A962] group-hover:border-[#C9A962] transition-all duration-300 shadow-lg">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
            </div>
            
            <h3 class="text-white font-bold text-lg sm:text-xl mb-1 leading-tight tracking-tight">Pelucas naturales</h3>
            <p class="text-[#E8D5B0] text-xs sm:text-sm font-medium tracking-wide">CABELLO 100% HUMANO</p>
          </div>
          
           <!-- Arrow Icon -->
          <div class="absolute top-4 right-4 opacity-0 -translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-500 delay-100">
            <div class="w-8 h-8 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" />
              </svg>
            </div>
          </div>
        </router-link>
        
        <!-- Extensiones Premium -->
        <!-- Extensiones Premium -->
        <router-link 
          to="/portal/catalogo?categoria=extensiones"
          class="group relative overflow-hidden rounded-2xl aspect-[4/3] sm:aspect-[3/2] shadow-sm hover:shadow-xl transition-all duration-500"
        >
          <!-- Imagen de fondo -->
          <img 
            src="https://images.unsplash.com/photo-1519699047748-de8e457a634e?q=80&w=800&auto=format&fit=crop" 
            alt="Extensiones premium"
            class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale-[30%] group-hover:grayscale-0"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#1A1318]/95 via-[#1A1318]/50 to-transparent opacity-90 group-hover:opacity-80 transition-opacity duration-300"></div>
          
          <div class="relative h-full flex flex-col justify-end p-4 sm:p-6">
            <div class="w-10 h-10 rounded-full bg-white/10 border border-white/20 backdrop-blur-md flex items-center justify-center mb-3 group-hover:scale-110 group-hover:bg-[#E8B4B8] group-hover:border-[#E8B4B8] transition-all duration-300 shadow-lg">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
              </svg>
            </div>
            
            <h3 class="text-white font-bold text-lg sm:text-xl mb-1 leading-tight tracking-tight">Extensiones premium</h3>
            <p class="text-[#E8B4B8] text-xs sm:text-sm font-medium tracking-wide">CLIP-IN, TAPE & MÁS</p>
          </div>
          
           <!-- Arrow Icon -->
          <div class="absolute top-4 right-4 opacity-0 -translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-500 delay-100">
            <div class="w-8 h-8 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" />
              </svg>
            </div>
          </div>
        </router-link>
        
        <!-- Sistemas Capilares -->
        <!-- Sistemas Capilares -->
        <router-link 
          to="/portal/catalogo?categoria=sistemas-capilares"
          class="group relative overflow-hidden rounded-2xl aspect-[4/3] sm:aspect-[3/2] shadow-sm hover:shadow-xl transition-all duration-500"
        >
          <!-- Imagen de fondo -->
          <img 
            src="https://images.unsplash.com/photo-1621605815971-fbc98d665033?q=80&w=600&auto=format&fit=crop" 
            alt="Sistemas capilares"
            class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale-[30%] group-hover:grayscale-0"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#1A1318]/95 via-[#1A1318]/50 to-transparent opacity-90 group-hover:opacity-80 transition-opacity duration-300"></div>
          
          <div class="relative h-full flex flex-col justify-end p-4 sm:p-6">
            <div class="w-10 h-10 rounded-full bg-white/10 border border-white/20 backdrop-blur-md flex items-center justify-center mb-3 group-hover:scale-110 group-hover:bg-emerald-500 group-hover:border-emerald-500 transition-all duration-300 shadow-lg">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
              </svg>
            </div>
            
            <h3 class="text-white font-bold text-lg sm:text-xl mb-1 leading-tight tracking-tight">Sistemas capilares</h3>
            <p class="text-emerald-300 text-xs sm:text-sm font-medium tracking-wide">SOLUCIONES PROFESIONALES</p>
          </div>
          
           <!-- Arrow Icon -->
          <div class="absolute top-4 right-4 opacity-0 -translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-500 delay-100">
            <div class="w-8 h-8 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" />
              </svg>
            </div>
          </div>
        </router-link>
        
        <!-- Nuevos Lanzamientos -->
        <!-- Nuevos Lanzamientos -->
        <router-link 
          to="/portal/catalogo?nuevo=true"
          class="group relative overflow-hidden rounded-2xl aspect-[4/3] sm:aspect-[3/2] shadow-sm hover:shadow-xl transition-all duration-500"
        >
          <!-- Imagen de fondo -->
          <img 
            src="https://images.unsplash.com/photo-1522337660859-02fbefca4702?q=80&w=800&auto=format&fit=crop" 
            alt="Nuevos lanzamientos"
            class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale-[30%] group-hover:grayscale-0"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#1A1318]/95 via-[#1A1318]/50 to-transparent opacity-90 group-hover:opacity-80 transition-opacity duration-300"></div>
          
          <div class="relative h-full flex flex-col justify-end p-4 sm:p-6">
            <div class="w-10 h-10 rounded-full bg-white/10 border border-white/20 backdrop-blur-md flex items-center justify-center mb-3 group-hover:scale-110 group-hover:bg-purple-500 group-hover:border-purple-500 transition-all duration-300 shadow-lg">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
              </svg>
            </div>
            
            <div class="flex items-center gap-2 mb-1">
              <h3 class="text-white font-bold text-lg sm:text-xl leading-tight tracking-tight">Nuevos</h3>
              <span class="px-2 py-0.5 bg-purple-500 text-white text-[10px] font-bold rounded-full animate-pulse shadow-lg shadow-purple-500/40">NEW</span>
            </div>
            <p class="text-purple-300 text-xs sm:text-sm font-medium tracking-wide">ÚLTIMOS LANZAMIENTOS</p>
          </div>
          
           <!-- Arrow Icon -->
          <div class="absolute top-4 right-4 opacity-0 -translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-500 delay-100">
            <div class="w-8 h-8 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" />
              </svg>
            </div>
          </div>
        </router-link>
      </div>
    </div>
    <div class="mb-14">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="font-luxury text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight">
            {{ hasOrderHistory ? 'Inspirado en tu actividad' : 'Comienza a explorar' }}
          </h2>
          <p class="text-gray-500 text-sm mt-1 font-light tracking-wide">
            {{ hasOrderHistory ? 'Basado en lo que viste y tus favoritos' : 'Productos destacados para ti' }}
          </p>
        </div>
        <router-link 
          v-if="hasOrderHistory"
          to="/portal/favoritos"
          class="text-gray-500 hover:text-gray-700 text-sm font-medium flex items-center gap-1 transition-colors"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
          </svg>
          Mis favoritos
        </router-link>
      </div>
      
      <!-- Scroll horizontal de productos habituales -->
      <div v-if="isLoading" class="flex gap-3 overflow-x-auto pb-4 -mx-4 px-4 scrollbar-hide">
        <B2BSkeleton 
          v-for="n in 5" 
          :key="`skeleton-${n}`"
          variant="rounded" 
          class="flex-shrink-0 w-[150px] sm:w-[168px] h-[280px]" 
        />
      </div>
      
      <div v-else class="flex gap-3 overflow-x-auto pb-4 -mx-4 px-4 scrollbar-hide">
        <router-link 
          v-for="(product, index) in frequentProducts" 
          :key="product.id"
          :to="`/portal/producto/${product.id}`"
          :style="{ 
            animationDelay: getAnimationDelay(index),
            opacity: hasAnimated ? 1 : 0
          }"
          class="flex-shrink-0 w-[150px] sm:w-[170px] bg-white rounded-2xl overflow-hidden shadow-soft hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ease-out group animate-fade-in-up cursor-pointer"
        >
          <!-- Imagen del producto -->
          <div class="relative aspect-[4/5] bg-gray-50 overflow-hidden">
            <img 
              :src="product.image" 
              :alt="product.name"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
              @error="handleProductImageError($event, product)"
              loading="lazy"
            />
            <!-- Badge según tipo: visto, favorito, o cantidad comprada -->
            <div 
              v-if="product.badge === 'visto'" 
              class="absolute top-2 right-2 bg-blue-500/80 text-white text-[9px] px-1.5 py-0.5 rounded font-medium backdrop-blur-sm flex items-center gap-0.5"
            >
              <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
              </svg>
              {{ product.veces_visto || 1 }}
            </div>
            <div 
              v-else-if="product.badge === 'favorito'" 
              class="absolute top-2 right-2 bg-pink-500/80 text-white text-[9px] px-1.5 py-0.5 rounded font-medium backdrop-blur-sm"
            >
              <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
              </svg>
            </div>
            <div 
              v-else-if="product.lastQty" 
              class="absolute top-2 right-2 bg-gray-900/60 text-white text-[10px] px-1.5 py-0.5 rounded font-medium backdrop-blur-sm"
            >
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
            
            <!-- Botón agregar - con animación y accesibilidad -->
            <!-- Botón agregar minimalista -->
            <button 
              @click.prevent="quickAddToCart(product)"
              class="w-full py-2 bg-[#1A1A1A] hover:bg-[#C9A962] text-white text-xs font-semibold rounded-lg flex items-center justify-center gap-2 transition-all duration-300 shadow-md hover:shadow-lg"
              :aria-label="`Agregar ${product.name} al carrito`"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              AGREGAR
            </button>
          </div>
        </router-link>
        
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
          <h2 class="font-luxury text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight">Novedades</h2>
          <p class="text-gray-500 text-sm mt-1 font-light tracking-wide">Los productos más recientes del inventario</p>
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
      <div v-if="isLoading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
        <B2BSkeleton 
          v-for="n in 10" 
          :key="`skeleton-featured-${n}`"
          variant="rounded" 
          class="aspect-[4/5] h-[320px]" 
        />
      </div>
      
      <div v-else-if="featuredProducts.length > 0" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
        <div 
          v-for="(product, index) in featuredProducts" 
          :key="product.id"
          :style="{ 
            animationDelay: getAnimationDelay(index),
            opacity: hasAnimated ? 1 : 0
          }"
          class="group bg-white rounded-2xl overflow-hidden shadow-soft hover:shadow-xl hover:-translate-y-1 transition-all duration-500 ease-out animate-fade-in-up"
        >
          <!-- Imagen grande -->
          <div class="relative aspect-[4/5] bg-gray-50 overflow-hidden">
            <img 
              :src="product.image" 
              :alt="product.name"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
              @error="handleProductImageError($event, product)"
              loading="lazy"
            />
            
            <!-- Badges más sutiles -->
            <div class="absolute top-2 left-2 flex flex-col gap-1.5">
              <span 
                v-if="product.badge === 'new'"
                class="px-2 py-0.5 bg-emerald-500/90 text-white text-[10px] font-semibold rounded backdrop-blur-sm"
              >
                Nuevo
              </span>
              <span 
                v-if="product.badge === 'low'"
                class="px-2 py-0.5 bg-amber-500/90 text-white text-[10px] font-semibold rounded backdrop-blur-sm"
              >
                Últimas uds.
              </span>
              <span 
                v-if="product.badge === 'hot'"
                class="px-2 py-0.5 bg-rose-500/90 text-white text-[10px] font-semibold rounded backdrop-blur-sm"
              >
                Top ventas
              </span>
              <span 
                v-if="product.discount"
                class="px-2 py-0.5 bg-gray-900/80 text-white text-[10px] font-semibold rounded backdrop-blur-sm"
              >
                -{{ product.discount }}%
              </span>
            </div>
            
            <!-- Quick add overlay - con mejoras de accesibilidad -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-3">
              <button 
                @click="quickAddToCart(product)"
                class="px-4 py-2 bg-white/95 text-gray-900 text-xs font-semibold rounded-lg shadow-lg transform translate-y-2 group-hover:translate-y-0 transition-all duration-300 flex items-center gap-1.5 hover:bg-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-900 active:scale-95"
                :aria-label="`Agregar ${product.name} al carrito rápidamente`"
              >
                <svg class="w-3.5 h-3.5 group-hover:rotate-90 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
      
      <!-- Empty state si no hay productos -->
      <div v-else class="flex flex-col items-center justify-center py-16 px-4">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-800 mb-2">No hay productos disponibles</h3>
        <p class="text-gray-500 text-sm mb-6 text-center max-w-sm">
          Actualmente no hay productos en esta sección. Vuelve más tarde o explora el catálogo completo.
        </p>
        <router-link 
          to="/portal/catalogo"
          class="inline-flex items-center gap-2 px-5 py-2.5 bg-gray-900 hover:bg-gray-800 text-white text-sm font-medium rounded-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2"
        >
          Ver catálogo completo
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </router-link>
      </div>
      
      <!-- Botón ver más - con accesibilidad mejorada -->
      <div v-if="featuredProducts.length > 0" class="text-center mt-10">
        <router-link 
          to="/portal/catalogo"
          class="inline-flex items-center gap-2 px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white text-sm font-medium rounded-lg transition-all duration-300 group hover:shadow-lg hover:shadow-gray-900/20 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2"
          aria-label="Ver catálogo completo con todos los productos"
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
import { B2BToast, useToast } from './ui'
import B2BSkeleton from './ui/B2BSkeleton.vue'
import { obtenerProductos, obtenerProductosDestacados } from '@/services/mayoristas'
import { ordenesService } from '@/services/ordenes'
import { vistosService, favoritosService } from '@/services/productos'

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

    const cartCount = ref(0)
    const currentSlide = ref(0)
    const isLoading = ref(true)
    const hasAnimated = ref(false)
    let slideInterval = null
    
    // Toast notifications
    const toast = useToast()

    // Productos (se cargan desde API)
    const frequentProducts = ref([])
    const featuredProducts = ref([])
    
    // Computed para verificar si tiene historial de compras
    const hasOrderHistory = computed(() => {
      return frequentProducts.value.length > 0 && frequentProducts.value[0]?.lastQty
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
    function normalizarProducto(producto) {
      return {
        id: producto.id || producto.producto_id,
        name: producto.nombre || producto.name,
        category: producto.categoria || producto.category || 'Sin categoría',
        price: producto.precio_mayorista || producto.wholesalePrice || producto.price || 0,
        originalPrice: producto.precio_retail || producto.retailPrice || producto.originalPrice || 0,
        stock: producto.stock || 0,
        image: producto.imagen || producto.image || 'https://placehold.co/400x400',
        badge: producto.stock < 5 ? 'low' : null,
        discount: null
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
                  productosHabituales.push({
                    id: v.producto_id,
                    name: v.nombre,
                    category: v.categoria || 'Sin categoría',
                    price: v.precio_mayorista || v.precio || 0,
                    originalPrice: v.precio || 0,
                    stock: v.stock || 0,
                    image: v.imagen_principal || 'https://placehold.co/400x400',
                    badge: 'visto', // Badge para identificar origen
                    veces_visto: v.veces_visto
                  })
                }
              })
            }
          } catch (err) {
            console.warn('No se pudo obtener productos vistos:', err)
          }
          
          // 2. Agregar productos favoritos (sin duplicar)
          try {
            const favoritos = await favoritosService.listar()
            if (favoritos && favoritos.length > 0) {
              favoritos.forEach(f => {
                if (!productosUnicos.has(f.producto_id)) {
                  productosUnicos.add(f.producto_id)
                  productosHabituales.push({
                    id: f.producto_id,
                    name: f.nombre,
                    category: 'Favorito',
                    price: f.precio_monto || 0,
                    originalPrice: f.precio_monto || 0,
                    stock: 100, // Los favoritos no tienen stock en el DTO
                    image: f.imagen_principal || 'https://placehold.co/400x400',
                    badge: 'favorito' // Badge para identificar origen
                  })
                }
              })
            }
          } catch (err) {
            console.warn('No se pudo obtener favoritos:', err)
          }
        }
        
        // Si hay productos vistos/favoritos, usarlos
        if (productosHabituales.length > 0) {
          frequentProducts.value = productosHabituales.slice(0, 8)
        } else {
          // Si no hay historial, mostrar productos destacados como sugerencia
          const productos = await obtenerProductos({ limit: 5 })
          frequentProducts.value = (Array.isArray(productos) ? productos : [])
            .map(normalizarProducto)
        }
        
        // Activar animaciones después de cargar
        setTimeout(() => {
          hasAnimated.value = true
        }, 100)
        
      } catch (error) {
        console.error('Error al cargar productos:', error)
        toast.error('Error al cargar productos. Intenta recargar la página.', 5000)
      } finally {
        isLoading.value = false
      }
    }

    // =========================================================================
    // LIFECYCLE
    // =========================================================================
    onMounted(() => {
      startSlideshow()
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
    })

    // =========================================================================
    // RETURN
    // =========================================================================
    return {
      user,
      cartCount,
      currentSlide,
      isLoading,
      hasAnimated,
      hasOrderHistory,
      frequentProducts,
      featuredProducts,
      nextSlide,
      prevSlide,
      handleProductImageError,
      quickAddToCart,
      getAnimationDelay
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

/* Transición del slider más cinematográfica */
[style*="transform: translateX"] {
  transition: transform 700ms cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
