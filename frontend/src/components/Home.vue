<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    
    <!-- ========================================
         NAVBAR - Glassmorphism Floating
         ======================================== -->
    <header 
      :class="[
        'fixed top-0 left-0 right-0 z-50 transition-all duration-500',
        isScrolled ? 'glass-navbar-scrolled py-3' : 'glass-navbar py-5'
      ]"
    >
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <a href="#" class="flex items-center gap-3 group">
            <div class="relative">
              <div class="w-11 h-11 bg-gradient-to-br from-brand-600 to-brand-700 rounded-2xl flex items-center justify-center shadow-soft transition-transform duration-300 group-hover:scale-105">
                <span class="text-white font-luxury font-bold text-xl">K</span>
              </div>
              <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-gold-400 rounded-full opacity-60"></div>
            </div>
            <div class="hidden sm:block">
              <h1 class="text-xl font-luxury font-semibold text-text-dark tracking-wide">Kharis</h1>
              <span class="text-[9px] text-brand-600 font-medium tracking-[0.25em] uppercase">Distribuidora</span>
            </div>
          </a>

          <!-- Navegación Desktop - Centrada -->
          <nav class="hidden lg:flex items-center gap-10">
            <a href="#categorias" class="text-text-medium hover:text-brand-600 font-medium text-sm tracking-wide transition-colors duration-300">Categorías</a>
            <a href="#productos" class="text-text-medium hover:text-brand-600 font-medium text-sm tracking-wide transition-colors duration-300">Productos</a>
            <a href="#mayoreo" class="text-text-medium hover:text-brand-600 font-medium text-sm tracking-wide transition-colors duration-300">Mayoreo</a>
            <a href="#testimonios" class="text-text-medium hover:text-brand-600 font-medium text-sm tracking-wide transition-colors duration-300">Reseñas</a>
            <a href="#contacto" class="text-text-medium hover:text-brand-600 font-medium text-sm tracking-wide transition-colors duration-300">Contacto</a>
          </nav>

          <!-- Acciones - Derecha -->
          <div class="flex items-center gap-3">
            <!-- Usuario -->
            <router-link to="/login" class="w-11 h-11 rounded-full flex items-center justify-center hover:bg-nude-200/60 transition-colors duration-300 touch-target">
              <svg class="w-5 h-5 text-text-medium" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
            </router-link>
            
            <!-- Carrito -->
            <button 
              class="relative w-11 h-11 rounded-full flex items-center justify-center hover:bg-nude-200/60 transition-colors duration-300 touch-target"
              @click="$emit('open-cart')"
            >
              <svg class="w-5 h-5 text-text-medium" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
              <span 
                v-if="cartCount > 0"
                class="absolute -top-0.5 -right-0.5 w-5 h-5 bg-brand-600 text-white text-[10px] font-bold rounded-full flex items-center justify-center shadow-sm"
              >
                {{ cartCount }}
              </span>
            </button>

            <!-- Menu Mobile -->
            <button 
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="lg:hidden w-11 h-11 rounded-full flex items-center justify-center hover:bg-nude-200/60 transition-colors duration-300 touch-target"
            >
              <svg class="w-5 h-5 text-text-medium" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Mobile Menu -->
        <transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="opacity-0 -translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-200 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-4"
        >
          <nav v-if="mobileMenuOpen" class="lg:hidden mt-6 pb-4">
            <div class="flex flex-col gap-1 bg-white/80 backdrop-blur-lg rounded-2xl p-4 shadow-soft">
              <a href="#categorias" @click="mobileMenuOpen = false" class="py-3 px-4 text-text-medium hover:text-brand-600 hover:bg-brand-50 rounded-xl font-medium transition-all">Categorías</a>
              <a href="#productos" @click="mobileMenuOpen = false" class="py-3 px-4 text-text-medium hover:text-brand-600 hover:bg-brand-50 rounded-xl font-medium transition-all">Productos</a>
              <a href="#mayoreo" @click="mobileMenuOpen = false" class="py-3 px-4 text-text-medium hover:text-brand-600 hover:bg-brand-50 rounded-xl font-medium transition-all">Mayoreo</a>
              <a href="#testimonios" @click="mobileMenuOpen = false" class="py-3 px-4 text-text-medium hover:text-brand-600 hover:bg-brand-50 rounded-xl font-medium transition-all">Reseñas</a>
              <a href="#contacto" @click="mobileMenuOpen = false" class="py-3 px-4 text-text-medium hover:text-brand-600 hover:bg-brand-50 rounded-xl font-medium transition-all">Contacto</a>
            </div>
          </nav>
        </transition>
      </div>
    </header>

    <!-- ========================================
         HERO SECTION - Slider de Fondo con Fade
         ======================================== -->
    <section class="relative min-h-screen flex items-center overflow-hidden">
      
      <!-- ===== SLIDER DE FONDOS (Solo cambian las imágenes) ===== -->
      <div class="absolute inset-0 lg:left-1/3">
        <!-- Slide 1: Hombre profesional -->
        <transition name="hero-fade">
          <img 
            v-if="currentSlide === 0"
            key="slide-0"
            src="https://images.unsplash.com/photo-1605980776566-0486c3ac7617?w=1400&h=1200&fit=crop&q=90" 
            alt="Profesional de la belleza" 
            class="absolute inset-0 w-full h-full object-cover object-center"
          >
        </transition>
        
        <!-- Slide 2: Mujer con cabello ondulado espectacular -->
        <transition name="hero-fade">
          <img 
            v-if="currentSlide === 1"
            key="slide-1"
            src="https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=1400&h=1200&fit=crop&q=90" 
            alt="Mujer con cabello ondulado hermoso" 
            class="absolute inset-0 w-full h-full object-cover object-center"
          >
        </transition>
        
        <!-- Slide 3: Close-up texturas de cabello y cosméticos -->
        <transition name="hero-fade">
          <img 
            v-if="currentSlide === 2"
            key="slide-2"
            src="https://images.unsplash.com/photo-1560869713-7d0a29430803?w=1400&h=1200&fit=crop&q=90" 
            alt="Texturas de cabello premium y cosméticos" 
            class="absolute inset-0 w-full h-full object-cover object-top"
          >
        </transition>

        <!-- Gradient Overlay (siempre visible) -->
        <div class="absolute inset-0 bg-gradient-to-r from-[#FAFAFA] via-[#FAFAFA]/90 lg:via-[#FAFAFA]/70 to-transparent z-10"></div>
        <div class="absolute inset-0 bg-gradient-to-t from-[#FAFAFA]/50 to-transparent lg:hidden z-10"></div>
      </div>

      <!-- Decorative Elements -->
      <div class="absolute top-32 right-20 w-64 h-64 bg-blush-200 rounded-full filter blur-3xl opacity-40 animate-pulse-soft hidden lg:block z-10"></div>
      <div class="absolute bottom-40 left-1/3 w-48 h-48 bg-nude-300 rounded-full filter blur-3xl opacity-50 animate-pulse-soft hidden lg:block z-10"></div>

      <!-- ===== CONTENIDO ESTÁTICO (NO se mueve) ===== -->
      <div class="relative z-20 max-w-7xl mx-auto px-5 sm:px-8 lg:px-12 pt-32 pb-20 lg:py-0">
        <div class="lg:max-w-lg xl:max-w-xl text-left">
          <!-- Badge -->
          <div class="inline-flex items-center gap-2.5 bg-white/80 backdrop-blur-sm border border-nude-300/50 rounded-full px-5 py-2.5 shadow-soft mb-6">
            <span class="w-2 h-2 bg-brand-600 rounded-full animate-pulse"></span>
            <span class="text-sm font-medium text-text-medium">Distribuidora Mayorista desde 2015</span>
          </div>

          <!-- Title -->
          <h1 class="font-luxury text-4xl sm:text-5xl lg:text-5xl xl:text-6xl text-text-dark leading-[1.15] mb-5">
            Tu Socio Experto en 
            <span class="block mt-1">
              <em class="text-brand-600 not-italic">Belleza</em> Profesional
            </span>
          </h1>

          <!-- Subtitle -->
          <p class="text-base lg:text-lg text-text-medium leading-relaxed mb-8 max-w-sm">
            Extensiones 100% naturales, pelucas premium y cosméticos de las mejores marcas internacionales para tu negocio.
          </p>

          <!-- CTAs -->
          <div class="flex flex-col sm:flex-row gap-3 mb-12">
            <a 
              href="#productos" 
              class="btn-primary inline-flex items-center justify-center gap-3 text-base touch-target"
            >
              Ver Catálogo
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </a>
            <a 
              href="#mayoreo" 
              class="btn-outline inline-flex items-center justify-center gap-3 text-base touch-target"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 003.75-.615A2.993 2.993 0 009.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 002.25 1.016c.896 0 1.7-.393 2.25-1.016a3.001 3.001 0 003.75.614m-16.5 0a3.004 3.004 0 01-.621-4.72L4.318 3.44A1.5 1.5 0 015.378 3h13.243a1.5 1.5 0 011.06.44l1.19 1.189a3 3 0 01-.621 4.72m-13.5 8.65h3.75a.75.75 0 00.75-.75V13.5a.75.75 0 00-.75-.75H6.75a.75.75 0 00-.75.75v3.75c0 .415.336.75.75.75z" />
              </svg>
              Portal Mayorista
            </a>
          </div>

          <!-- Floating Card -->
          <div class="hidden lg:flex items-center gap-4 bg-white rounded-2xl shadow-soft-lg p-5 max-w-xs animate-float-soft">
            <div class="w-14 h-14 bg-gradient-to-br from-gold-300 to-gold-400 rounded-xl flex items-center justify-center flex-shrink-0">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
              </svg>
            </div>
            <div>
              <p class="font-semibold text-text-dark">Calidad Certificada</p>
              <p class="text-sm text-text-light">100% Cabello Remy Natural</p>
            </div>
          </div>

          <!-- Slide Indicators -->
          <div class="flex items-center gap-3 mt-8 lg:mt-12">
            <button 
              v-for="(slide, index) in heroSlides" 
              :key="index"
              @click="goToSlide(index)"
              :class="[
                'h-1.5 rounded-full transition-all duration-500',
                currentSlide === index 
                  ? 'w-8 bg-brand-600' 
                  : 'w-4 bg-nude-400 hover:bg-nude-500'
              ]"
              :aria-label="'Ir a slide ' + (index + 1)"
            ></button>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         TRUST BAR - Banderas de Confianza
         ======================================== -->
    <section class="trust-bar py-8 lg:py-10">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 lg:gap-12">
          <div class="flex items-center gap-4 justify-center md:justify-start">
            <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-soft flex-shrink-0">
              <svg class="w-6 h-6 text-brand-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
              </svg>
            </div>
            <div>
              <p class="font-semibold text-text-dark text-sm">Envíos a todo el país</p>
              <p class="text-xs text-text-light">24-72 horas hábiles</p>
            </div>
          </div>

          <div class="flex items-center gap-4 justify-center md:justify-start">
            <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-soft flex-shrink-0">
              <svg class="w-6 h-6 text-gold-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
              </svg>
            </div>
            <div>
              <p class="font-semibold text-text-dark text-sm">Calidad Remy Certificada</p>
              <p class="text-xs text-text-light">100% cabello natural</p>
            </div>
          </div>

          <div class="flex items-center gap-4 justify-center md:justify-start">
            <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-soft flex-shrink-0">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
              </svg>
            </div>
            <div>
              <p class="font-semibold text-text-dark text-sm">Pagos Seguros</p>
              <p class="text-xs text-text-light">Tarjeta, transferencia, PayPal</p>
            </div>
          </div>

          <div class="flex items-center gap-4 justify-center md:justify-start">
            <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-soft flex-shrink-0">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
              </svg>
            </div>
            <div>
              <p class="font-semibold text-text-dark text-sm">Atención Experta</p>
              <p class="text-xs text-text-light">Asesoría personalizada</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         CATEGORÍAS - Bento Box Grid
         ======================================== -->
    <section id="categorias" class="py-20 lg:py-28 bg-[#FAFAFA]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <!-- Section Header -->
        <div class="text-center mb-14">
          <span class="inline-block text-brand-600 font-medium text-sm tracking-widest uppercase mb-4">Nuestro Catálogo</span>
          <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-text-dark mb-4">
            Categorías <em class="not-italic text-brand-600">Exclusivas</em>
          </h2>
          <p class="text-text-medium max-w-xl mx-auto">
            Productos seleccionados para profesionales de la belleza que buscan calidad excepcional
          </p>
        </div>

        <!-- Bento Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 lg:gap-6">
          <!-- Extensiones - Card Grande -->
          <div class="md:col-span-2 lg:col-span-2 lg:row-span-2 group cursor-pointer">
            <div class="relative h-80 lg:h-full min-h-[400px] bento-item shadow-soft hover-lift overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=1000&h=800&fit=crop&q=85" 
                alt="Extensiones de cabello premium" 
                class="absolute inset-0 w-full h-full object-cover img-zoom"
              >
              <div class="absolute inset-0 bento-overlay"></div>
              <div class="absolute bottom-0 left-0 right-0 p-6 lg:p-8">
                <span class="inline-block bg-gold-400 text-white text-xs font-bold px-3 py-1 rounded-full mb-3">MÁS VENDIDO</span>
                <h3 class="font-luxury text-2xl lg:text-3xl text-white mb-2">Extensiones</h3>
                <p class="text-white/80 mb-4 max-w-md">Cabello 100% Remy natural. Clip-in, tape, microring y más. Todos los largos y colores.</p>
                <span class="inline-flex items-center gap-2 text-white font-medium group-hover:gap-4 transition-all">
                  Explorar colección
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                  </svg>
                </span>
              </div>
            </div>
          </div>

          <!-- Pelucas -->
          <div class="group cursor-pointer">
            <div class="relative h-64 lg:h-full min-h-[200px] bento-item shadow-soft hover-lift overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?w=600&h=500&fit=crop&q=85" 
                alt="Pelucas lacefront premium" 
                class="absolute inset-0 w-full h-full object-cover img-zoom"
              >
              <div class="absolute inset-0 bento-overlay"></div>
              <div class="absolute bottom-0 left-0 right-0 p-5 lg:p-6">
                <h3 class="font-luxury text-xl lg:text-2xl text-white mb-1">Pelucas</h3>
                <p class="text-white/80 text-sm mb-3">Lacefront & Full Lace</p>
                <span class="inline-flex items-center gap-2 text-white text-sm font-medium group-hover:gap-3 transition-all">
                  Ver más
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                  </svg>
                </span>
              </div>
            </div>
          </div>

          <!-- Cosméticos -->
          <div class="group cursor-pointer">
            <div class="relative h-64 lg:h-full min-h-[200px] bento-item shadow-soft hover-lift overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&h=500&fit=crop&q=85" 
                alt="Cosméticos capilares profesionales" 
                class="absolute inset-0 w-full h-full object-cover img-zoom"
              >
              <div class="absolute inset-0 bento-overlay"></div>
              <div class="absolute bottom-0 left-0 right-0 p-5 lg:p-6">
                <h3 class="font-luxury text-xl lg:text-2xl text-white mb-1">Cosméticos</h3>
                <p class="text-white/80 text-sm mb-3">Cuidado & Styling</p>
                <span class="inline-flex items-center gap-2 text-white text-sm font-medium group-hover:gap-3 transition-all">
                  Ver más
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         PRODUCTOS DESTACADOS
         ======================================== -->
    <section id="productos" class="py-20 lg:py-28 bg-gradient-to-b from-nude-100/50 to-[#FAFAFA]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <!-- Section Header -->
        <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6 mb-14">
          <div>
            <span class="inline-block text-brand-600 font-medium text-sm tracking-widest uppercase mb-4">Selección Premium</span>
            <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-text-dark">
              Productos <em class="not-italic text-brand-600">Destacados</em>
            </h2>
          </div>
          <a href="#" class="inline-flex items-center gap-2 text-text-medium hover:text-brand-600 font-medium transition-colors group">
            Ver todo el catálogo
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
            </svg>
          </a>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8">
          <div v-for="i in 4" :key="i" class="animate-pulse">
            <div class="bg-nude-200 rounded-3xl aspect-[3/4] mb-5"></div>
            <div class="h-4 bg-nude-200 rounded-full w-1/3 mb-3"></div>
            <div class="h-5 bg-nude-200 rounded-full w-3/4 mb-3"></div>
            <div class="h-5 bg-nude-200 rounded-full w-1/4"></div>
          </div>
        </div>

        <!-- Products Grid -->
        <div v-else-if="productos.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8">
          <div
            v-for="producto in productos"
            :key="producto.id"
            class="group cursor-pointer"
          >
            <div class="relative bg-white rounded-3xl overflow-hidden shadow-soft hover-lift mb-5">
              <!-- Badge -->
              <div class="absolute top-4 left-4 z-10">
                <span class="bg-white/90 backdrop-blur-sm text-text-dark text-xs font-medium px-3 py-1.5 rounded-full shadow-sm">
                  {{ producto.categoria || 'Premium' }}
                </span>
              </div>
              
              <!-- Wishlist Button -->
              <button class="absolute top-4 right-4 z-10 w-10 h-10 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-sm hover:bg-brand-50 transition-colors touch-target">
                <svg class="w-5 h-5 text-text-light hover:text-brand-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>
              </button>

              <!-- Image -->
              <div class="aspect-[3/4] overflow-hidden bg-nude-100">
                <img
                  :src="producto.imagen || 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=500&fit=crop'"
                  :alt="producto.nombre"
                  class="w-full h-full object-cover img-zoom"
                >
              </div>

              <!-- Quick Add -->
              <button
                @click.stop="agregarAlCarrito(producto)"
                class="absolute bottom-4 left-4 right-4 bg-brand-600 text-white font-semibold py-3 px-6 rounded-2xl opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0 transition-all duration-300 shadow-lg hover:bg-brand-700 touch-target"
              >
                Agregar al carrito
              </button>
            </div>

            <!-- Product Info -->
            <div class="px-1">
              <p class="text-xs text-text-light uppercase tracking-wider mb-1">{{ producto.categoria || 'Extensiones' }}</p>
              <h3 class="font-medium text-text-dark mb-2 line-clamp-2 group-hover:text-brand-600 transition-colors">{{ producto.nombre }}</h3>
              <p class="text-lg font-semibold text-brand-600">${{ formatPrice(producto.precio) }} <span class="text-xs text-text-light font-normal">MXN</span></p>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-16">
          <div class="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-red-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
            </svg>
          </div>
          <p class="text-text-medium mb-6">{{ error }}</p>
          <button @click="cargarProductos" class="btn-primary">
            Reintentar
          </button>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-16">
          <div class="w-20 h-20 bg-nude-200 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-10 h-10 text-nude-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
            </svg>
          </div>
          <p class="text-text-medium">No hay productos disponibles en este momento</p>
        </div>
      </div>
    </section>

    <!-- ========================================
         SECCIÓN MAYORISTA - Fondo Oscuro
         ======================================== -->
    <section id="mayoreo" class="section-dark py-20 lg:py-28 relative overflow-hidden">
      <!-- Decorative Elements -->
      <div class="absolute top-0 right-0 w-96 h-96 bg-brand-600/10 rounded-full filter blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-80 h-80 bg-gold-400/10 rounded-full filter blur-3xl"></div>

      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12 relative z-10">
        <div class="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          <!-- Content -->
          <div>
            <span class="inline-flex items-center gap-2 bg-gold-400/20 border border-gold-400/30 text-gold-400 text-sm font-medium px-4 py-2 rounded-full mb-6">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              Programa Exclusivo Mayoristas
            </span>

            <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-white leading-tight mb-6">
              Impulsa tu <em class="not-italic text-gradient-gold">Negocio</em> de Belleza
            </h2>

            <p class="text-white/70 text-lg mb-8 max-w-lg">
              Únete a más de 2,000 profesionales que confían en Kharis para surtir sus salones, tiendas y negocios de belleza.
            </p>

            <!-- Benefits -->
            <ul class="space-y-4 mb-10">
              <li class="flex items-start gap-4">
                <div class="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p class="text-white font-medium">Descuentos desde 25% en adelante</p>
                  <p class="text-white/50 text-sm">Precios escalonados según volumen de compra</p>
                </div>
              </li>
              <li class="flex items-start gap-4">
                <div class="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p class="text-white font-medium">Asesor de cuenta dedicado</p>
                  <p class="text-white/50 text-sm">Atención personalizada vía WhatsApp</p>
                </div>
              </li>
              <li class="flex items-start gap-4">
                <div class="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p class="text-white font-medium">Envío gratis en pedidos +$5,000 MXN</p>
                  <p class="text-white/50 text-sm">Entregas prioritarias a todo México</p>
                </div>
              </li>
            </ul>

            <!-- CTAs -->
            <div class="flex flex-col sm:flex-row gap-4">
              <a 
                href="https://wa.me/525512345678?text=Hola,%20me%20interesa%20el%20programa%20de%20mayoristas"
                target="_blank"
                class="inline-flex items-center justify-center gap-3 bg-green-500 hover:bg-green-600 text-white font-semibold px-8 py-4 rounded-full transition-all shadow-lg hover:shadow-green-500/25 touch-target"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
                Contactar por WhatsApp
              </a>
              <button class="inline-flex items-center justify-center gap-3 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold px-8 py-4 rounded-full transition-all touch-target">
                Solicitar catálogo
              </button>
            </div>
          </div>

          <!-- Image -->
          <div class="relative hidden lg:block">
            <div class="relative rounded-3xl overflow-hidden shadow-2xl">
              <img 
                src="https://images.unsplash.com/photo-1560066984-138dadb4c035?w=700&h=800&fit=crop&q=85" 
                alt="Salón de belleza profesional" 
                class="w-full h-auto"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-carbon-900/60 to-transparent"></div>
            </div>

            <!-- Stats Card -->
            <div class="absolute -bottom-6 -left-6 bg-white rounded-2xl shadow-soft-xl p-6">
              <div class="flex items-center gap-6">
                <div class="text-center">
                  <p class="text-3xl font-bold text-brand-600">2k+</p>
                  <p class="text-xs text-text-light uppercase tracking-wider">Mayoristas</p>
                </div>
                <div class="w-px h-12 bg-nude-200"></div>
                <div class="text-center">
                  <p class="text-3xl font-bold text-brand-600">500+</p>
                  <p class="text-xs text-text-light uppercase tracking-wider">Productos</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         TESTIMONIOS - Prueba Social
         ======================================== -->
    <section id="testimonios" class="py-20 lg:py-28 bg-[#FAFAFA]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <!-- Section Header -->
        <div class="text-center mb-14">
          <span class="inline-block text-brand-600 font-medium text-sm tracking-widest uppercase mb-4">Testimonios</span>
          <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-text-dark mb-4">
            Lo que dicen nuestras <em class="not-italic text-brand-600">clientas</em>
          </h2>
          <p class="text-text-medium max-w-xl mx-auto">
            Miles de profesionales de la belleza confían en nosotros
          </p>
        </div>

        <!-- Testimonials Grid -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          <!-- Testimonial 1 -->
          <div class="bg-white rounded-3xl p-8 shadow-soft hover-lift">
            <div class="flex items-center gap-1 mb-4">
              <svg v-for="i in 5" :key="i" class="w-5 h-5 text-gold-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <p class="text-text-medium mb-6 leading-relaxed">
              "Las extensiones son de una calidad increíble. Mis clientas siempre quedan encantadas con el resultado. El cabello se siente natural y dura muchísimo."
            </p>
            <div class="flex items-center gap-4">
              <img 
                src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop&q=80" 
                alt="María García"
                class="w-12 h-12 rounded-full object-cover"
              >
              <div>
                <p class="font-semibold text-text-dark">María García</p>
                <p class="text-sm text-text-light">Estilista, CDMX</p>
              </div>
            </div>
          </div>

          <!-- Testimonial 2 -->
          <div class="bg-white rounded-3xl p-8 shadow-soft hover-lift">
            <div class="flex items-center gap-1 mb-4">
              <svg v-for="i in 5" :key="i" class="w-5 h-5 text-gold-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <p class="text-text-medium mb-6 leading-relaxed">
              "El programa de mayoristas me ha ayudado a crecer mi negocio. Los precios son excelentes y el servicio al cliente es de primera. ¡Los recomiendo 100%!"
            </p>
            <div class="flex items-center gap-4">
              <img 
                src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&q=80" 
                alt="Laura Mendoza"
                class="w-12 h-12 rounded-full object-cover"
              >
              <div>
                <p class="font-semibold text-text-dark">Laura Mendoza</p>
                <p class="text-sm text-text-light">Dueña de salón, Monterrey</p>
              </div>
            </div>
          </div>

          <!-- Testimonial 3 -->
          <div class="bg-white rounded-3xl p-8 shadow-soft hover-lift md:col-span-2 lg:col-span-1">
            <div class="flex items-center gap-1 mb-4">
              <svg v-for="i in 5" :key="i" class="w-5 h-5 text-gold-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <p class="text-text-medium mb-6 leading-relaxed">
              "Las pelucas lacefront son simplemente perfectas. El acabado es tan natural que nadie nota la diferencia. Mis clientas están felices con los resultados."
            </p>
            <div class="flex items-center gap-4">
              <img 
                src="https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=100&h=100&fit=crop&q=80" 
                alt="Carmen Rodríguez"
                class="w-12 h-12 rounded-full object-cover"
              >
              <div>
                <p class="font-semibold text-text-dark">Carmen Rodríguez</p>
                <p class="text-sm text-text-light">Especialista en pelucas, Guadalajara</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Before/After Gallery Hint -->
        <div class="mt-16 text-center">
          <div class="inline-flex items-center gap-4 bg-blush-100 rounded-full px-6 py-3">
            <div class="flex -space-x-2">
              <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=60&h=60&fit=crop" class="w-8 h-8 rounded-full border-2 border-white object-cover" alt="">
              <img src="https://images.unsplash.com/photo-1517841905240-472988babdf9?w=60&h=60&fit=crop" class="w-8 h-8 rounded-full border-2 border-white object-cover" alt="">
              <img src="https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=60&h=60&fit=crop" class="w-8 h-8 rounded-full border-2 border-white object-cover" alt="">
            </div>
            <p class="text-sm text-text-medium">
              <span class="font-semibold text-brand-600">+500 transformaciones</span> documentadas
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         FOOTER
         ======================================== -->
    <footer id="contacto" class="bg-text-dark text-white">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <!-- Main Footer -->
        <div class="py-16 lg:py-20">
          <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-12 lg:gap-8">
            <!-- Brand -->
            <div class="lg:col-span-1">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-12 h-12 bg-gradient-to-br from-brand-500 to-brand-600 rounded-2xl flex items-center justify-center">
                  <span class="text-white font-luxury font-bold text-xl">K</span>
                </div>
                <div>
                  <h2 class="text-xl font-luxury font-semibold">Kharis</h2>
                  <span class="text-xs text-white/50 tracking-widest uppercase">Distribuidora</span>
                </div>
              </div>
              <p class="text-white/60 text-sm mb-6 max-w-xs">
                Tu socio experto en belleza profesional. Extensiones, pelucas y cosméticos de la más alta calidad.
              </p>
              <div class="flex gap-3">
                <a href="#" class="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center hover:bg-brand-600 transition-colors">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a href="#" class="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center hover:bg-brand-600 transition-colors">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                </a>
                <a href="#" class="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center hover:bg-brand-600 transition-colors">
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1-.1z"/></svg>
                </a>
              </div>
            </div>

            <!-- Links -->
            <div>
              <h3 class="font-semibold mb-6 text-white/90">Productos</h3>
              <ul class="space-y-3">
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Extensiones Clip-in</a></li>
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Extensiones Tape</a></li>
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Pelucas Lacefront</a></li>
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Cosméticos Capilares</a></li>
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Novedades</a></li>
              </ul>
            </div>

            <div>
              <h3 class="font-semibold mb-6 text-white/90">Empresa</h3>
              <ul class="space-y-3">
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Sobre nosotros</a></li>
                <li><a href="#mayoreo" class="text-white/60 hover:text-white transition-colors text-sm">Programa Mayorista</a></li>
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Envíos y devoluciones</a></li>
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Preguntas frecuentes</a></li>
                <li><a href="#contacto" class="text-white/60 hover:text-white transition-colors text-sm">Contacto</a></li>
              </ul>
            </div>

            <div>
              <h3 class="font-semibold mb-6 text-white/90">Contacto</h3>
              <ul class="space-y-4">
                <li class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-brand-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
                  </svg>
                  <span class="text-white/60 text-sm">+52 55 1234 5678</span>
                </li>
                <li class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                  <a href="https://wa.me/525512345678" class="text-white/60 hover:text-white transition-colors text-sm">WhatsApp</a>
                </li>
                <li class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-brand-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                  </svg>
                  <a href="mailto:hola@kharis.mx" class="text-white/60 hover:text-white transition-colors text-sm">hola@kharis.mx</a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Bottom Bar -->
        <div class="border-t border-white/10 py-6">
          <div class="flex flex-col md:flex-row items-center justify-between gap-4">
            <p class="text-white/50 text-sm">© 2026 Kharis Distribuidora. Todos los derechos reservados.</p>
            <div class="flex items-center gap-6">
              <a href="#" class="text-white/50 hover:text-white text-sm transition-colors">Privacidad</a>
              <a href="#" class="text-white/50 hover:text-white text-sm transition-colors">Términos</a>
              <a href="#" class="text-white/50 hover:text-white text-sm transition-colors">Cookies</a>
            </div>
          </div>
        </div>
      </div>
    </footer>

    <!-- ========================================
         FLOATING WHATSAPP BUTTON
         ======================================== -->
    <a 
      href="https://wa.me/525512345678?text=Hola,%20me%20interesa%20información%20sobre%20sus%20productos"
      target="_blank"
      class="fixed bottom-6 right-6 w-16 h-16 bg-green-500 text-white rounded-full flex items-center justify-center shadow-xl hover:bg-green-600 hover:scale-110 transition-all duration-300 z-40 group touch-target"
    >
      <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
      </svg>
      <!-- Tooltip -->
      <span class="absolute right-full mr-3 bg-white text-text-dark text-sm font-medium px-4 py-2 rounded-xl shadow-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        ¿Necesitas ayuda?
      </span>
    </a>

  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { productosService, carritoService } from '../services/productos'

export default {
  name: 'Home',
  setup() {
    const productos = ref([])
    const loading = ref(true)
    const error = ref(null)
    const cartCount = ref(0)
    const isScrolled = ref(false)
    const mobileMenuOpen = ref(false)

    // ===== HERO SLIDER =====
    const currentSlide = ref(0)
    const heroSlides = ref([
      { id: 0, alt: 'Profesional de belleza' },
      { id: 1, alt: 'Mujer con cabello ondulado' },
      { id: 2, alt: 'Texturas de cabello premium' }
    ])
    let slideInterval = null

    const startSlideshow = () => {
      slideInterval = setInterval(() => {
        currentSlide.value = (currentSlide.value + 1) % heroSlides.value.length
      }, 6000) // Cambio cada 6 segundos
    }

    const goToSlide = (index) => {
      currentSlide.value = index
      // Reiniciar el intervalo para evitar saltos rápidos
      if (slideInterval) {
        clearInterval(slideInterval)
        startSlideshow()
      }
    }

    const formatPrice = (price) => {
      return new Intl.NumberFormat('es-MX').format(price)
    }

    const handleScroll = () => {
      isScrolled.value = window.scrollY > 50
    }

    const cargarProductos = async () => {
      loading.value = true
      error.value = null
      try {
        const data = await productosService.getDestacados()
        productos.value = data.productos || data.results || data || []
      } catch (err) {
        if (err.response?.status !== 401) {
          error.value = 'Error al cargar productos: ' + (err.response?.data?.detail || err.message)
        }
        console.error('Error cargando productos:', err)
        productos.value = []
      } finally {
        loading.value = false
      }
    }

    const agregarAlCarrito = async (producto) => {
      try {
        await carritoService.agregarProducto(producto.id, 1)
        cartCount.value++
        console.log('Producto agregado al carrito')
      } catch (err) {
        console.error('Error agregando al carrito:', err)
        if (err.response?.status !== 401) {
          alert('Error al agregar al carrito: ' + (err.response?.data?.detail || err.message))
        }
      }
    }

    const cargarResumenCarrito = async () => {
      try {
        const resumen = await carritoService.getResumen()
        cartCount.value = resumen.total_items || 0
      } catch (err) {
        if (err.response?.status !== 401) {
          console.error('Error cargando resumen del carrito:', err)
        }
        cartCount.value = 0
      }
    }

    onMounted(() => {
      cargarProductos()
      cargarResumenCarrito()
      window.addEventListener('scroll', handleScroll)
      handleScroll()
      startSlideshow()
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
      if (slideInterval) {
        clearInterval(slideInterval)
      }
    })

    return {
      productos,
      loading,
      error,
      cartCount,
      isScrolled,
      mobileMenuOpen,
      currentSlide,
      heroSlides,
      goToSlide,
      formatPrice,
      cargarProductos,
      agregarAlCarrito
    }
  }
}
</script>

<style scoped>
/* Línea de truncado para nombres de productos */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Hero Slider Fade Transition */
.hero-fade-enter-active {
  transition: opacity 1.5s ease-in-out;
}
.hero-fade-leave-active {
  transition: opacity 1.5s ease-in-out;
}
.hero-fade-enter-from,
.hero-fade-leave-to {
  opacity: 0;
}
.hero-fade-enter-to,
.hero-fade-leave-from {
  opacity: 1;
}
</style>
