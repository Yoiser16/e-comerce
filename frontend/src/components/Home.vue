<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    
    <!-- ========================================
         NAVBAR - Ultra-Minimal Luxury Glassmorphism
         ======================================== -->
    <header 
      :class="[
        'fixed top-0 left-0 right-0 z-50',
        isScrolled ? 'header-luxury-scrolled py-2' : 'header-luxury py-4'
      ]"
    >
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <a href="#" class="flex items-center gap-3 group flex-shrink-0">
            <div class="relative">
              <!-- Glow sutil detrás del logo para mayor presencia -->
              <div class="absolute inset-0 bg-gradient-to-r from-brand-500/5 via-brand-600/8 to-brand-500/5 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-full scale-150"></div>
              
              <!-- Logo dinámico según scroll -->
              <img 
                :src="isScrolled ? '/logo-kharis.png' : '/logo blanco.png'" 
                alt="Kharis Distribuidora" 
                class="relative h-12 sm:h-16 lg:h-20 w-auto object-contain group-hover:scale-105 drop-shadow-[0_2px_8px_rgba(216,27,96,0.15)] logo-transition"
                style="filter: contrast(1.1) saturate(1.15);"
              />
            </div>
          </a>

          <!-- Buscador Desktop -->
          <div class="hidden lg:flex flex-1 max-w-xs mx-8">
            <div class="relative w-full" ref="searchInputRef">
              <input 
                type="text"
                v-model="searchQuery"
                @input="getSuggestions"
                @keyup.enter="handleSearch()"
                @focus="getSuggestions"
                placeholder="Buscar extensiones, accesorios..."
                :class="[
                  'w-full pl-10 pr-4 py-2 border rounded-full text-xs focus:outline-none focus:ring-1 transition-all duration-300',
                  isScrolled 
                    ? 'bg-white/80 border-text-dark/15 text-text-dark placeholder-text-dark/70 focus:border-text-dark/30 focus:bg-white focus:ring-text-dark/15'
                    : 'bg-white/20 border-white/30 text-white placeholder-white/70 focus:border-white/50 focus:bg-white/30 focus:ring-white/20'
                ]"
              />
              <svg 
                :class="[
                  'absolute left-3.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none',
                  isScrolled ? 'text-text-medium' : 'text-white/80'
                ]"
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
                  ref="suggestionsRef"
                  class="dropdown-search-luxury absolute top-full left-0 right-0 mt-2 bg-white border border-text-dark/8 rounded-2xl overflow-hidden z-50"
                  style="box-shadow: 0 12px 40px -8px rgba(216, 27, 96, 0.12), 0 4px 16px -4px rgba(0, 0, 0, 0.08);"
                >
                  <div class="max-h-80 overflow-y-auto search-results-scroll">
                    <button
                      v-for="producto in searchSuggestions"
                      :key="producto.id"
                      @click="handleSearch(producto)"
                      class="w-full px-5 py-4 hover:bg-[#FFF0F5] transition-all duration-300 flex items-center gap-4 text-left group border-b border-nude-100/50 last:border-b-0"
                    >
                      <div class="w-12 h-12 rounded-lg overflow-hidden flex-shrink-0 bg-nude-50 ring-1 ring-nude-200/40 group-hover:ring-brand-300/40 transition-all duration-300">
                        <img 
                          v-if="producto.imagen_principal || producto.imagen_url || producto.imagen"
                          :src="getImageUrl(producto.imagen_principal || producto.imagen_url || producto.imagen)"
                          :alt="producto.nombre"
                          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-[#2A2A2A] truncate group-hover:text-brand-600 transition-colors duration-300">
                          {{ producto.nombre }}
                        </p>
                      </div>
                      <p class="text-sm font-semibold text-brand-600 flex-shrink-0">
                        {{ formatPrice(getItemPrice(producto)) }}
                      </p>
                    </button>
                  </div>
                  <div class="border-t border-text-dark/10 bg-nude-50/50">
                    <button
                      @click="handleSearch()"
                      class="w-full px-4 py-3 text-xs font-medium text-brand-600 hover:text-brand-700 transition-colors flex items-center justify-center gap-2"
                    >
                      Ver todos los {{ getTotalSearchResults() }} productos
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                      </svg>
                    </button>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- Navegación Desktop - Más legible -->
          <nav class="hidden lg:flex items-center gap-7">
            <a href="#categorias" class="nav-link-luxury">CATEGORÍAS</a>
            <a href="#productos" class="nav-link-luxury">PRODUCTOS</a>
            <a href="#mayoreo" class="nav-link-luxury">MAYOREO</a>
            <a href="#testimonios" class="nav-link-luxury">RESEÑAS</a>
            <a href="#contacto" class="nav-link-luxury">CONTACTO</a>
          </nav>

          <!-- Acciones - Iconos compactos -->
          <div class="flex items-center gap-0.5 sm:gap-1">
            <!-- Buscador Mobile -->
            <button 
              @click="mobileSearchOpen = !mobileSearchOpen"
              :class="[
                'lg:hidden w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target',
                isScrolled ? 'hover:bg-black/5' : 'hover:bg-white/10'
              ]"
            >
              <svg :class="['w-4 h-4', isScrolled ? 'text-text-dark' : 'text-white']" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </button>
            
            <!-- Usuario con dropdown -->
            <div class="relative" ref="userMenuRef">
              <button 
                @click="toggleUserMenu"
                class="w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target"
                :class="[
                  isLoggedIn 
                    ? (isScrolled ? 'border border-text-dark/20 hover:border-text-dark/40' : 'border border-white/30 hover:border-white/60')
                    : (isScrolled ? 'hover:bg-black/5' : 'hover:bg-white/10')
                ]"
              >
                <!-- Si está logueado, mostrar inicial con estilo sutil -->
                <span v-if="isLoggedIn" class="text-xs font-medium" :class="isScrolled ? 'text-text-dark' : 'text-white'">
                  {{ userInitial }}
                </span>
                <!-- Si no está logueado, mostrar icono -->
                <svg v-else class="w-4 h-4" :class="isScrolled ? 'text-text-dark' : 'text-white'" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
              </button>
              
              <!-- Dropdown Menu - Teleport al body para evitar overflow-hidden -->
              <Teleport to="body">
                <transition
                  enter-active-class="transition duration-150 ease-out"
                  enter-from-class="opacity-0 scale-95"
                  enter-to-class="opacity-100 scale-100"
                  leave-active-class="transition duration-100 ease-in"
                  leave-from-class="opacity-100 scale-100"
                  leave-to-class="opacity-0 scale-95"
                >
                  <div 
                    v-if="showUserMenu"
                    class="fixed w-52 bg-white rounded-lg shadow-[0_16px_48px_rgb(0,0,0,0.25)] py-2 border border-black/10"
                    :style="{
                      top: (userMenuRef?.getBoundingClientRect().bottom || 0) + 12 + 'px',
                      left: ((userMenuRef?.getBoundingClientRect().right || 0) - 208) + 'px',
                      zIndex: 99999
                    }"
                  >
                    <!-- Si está logueado -->
                    <template v-if="isLoggedIn">
                      <div class="px-4 py-3 border-b border-black/10 bg-nude-50/30">
                        <p class="text-xs text-text-medium mb-0.5">Hola,</p>
                        <p class="text-sm text-text-dark font-semibold truncate">{{ currentUser?.nombre || currentUser?.email }}</p>
                      </div>
                      <router-link 
                        to="/mi-cuenta"
                        class="flex items-center gap-3 px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors"
                        @click="showUserMenu = false"
                      >
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                        </svg>
                        Mi Cuenta
                      </router-link>
                      <button 
                        @click="handleMenuAction('pedidos')"
                        class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors"
                      >
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                        </svg>
                        Mis Pedidos
                      </button>
                      <button 
                        @click="handleMenuAction('favoritos')"
                        class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors border-b border-black/10"
                      >
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                        </svg>
                        Ver Favoritos
                      </button>
                      <button 
                        @click="cerrarSesion"
                        class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors mt-1"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
                        </svg>
                        Cerrar Sesión
                      </button>
                    </template>
                    
                    <!-- Si NO está logueado -->
                    <template v-else>
                      <button 
                        @click="handleMenuAction('login')"
                        class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors"
                      >
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                        </svg>
                        Inicia sesión
                      </button>
                      <button 
                        @click="handleMenuAction('pedidos')"
                        class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors"
                      >
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                        </svg>
                        Mi pedido
                      </button>
                      <button 
                        @click="handleMenuAction('favoritos')"
                        class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors"
                      >
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                        </svg>
                        Ver Favoritos
                      </button>
                    </template>
                  </div>
                </transition>
              </Teleport>
            </div>
            
            <!-- Carrito -->
            <button 
              :class="[
                'relative w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target',
                isScrolled ? 'hover:bg-black/5' : 'hover:bg-white/10'
              ]"
              @click="openCartDrawer"
            >
              <svg :class="['w-4 h-4', isScrolled ? 'text-text-dark' : 'text-white']" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
              <span 
                v-if="cartCount > 0"
                :class="[
                  'absolute -top-0.5 -right-0.5 w-4 h-4 text-[9px] font-medium rounded-full flex items-center justify-center',
                  isScrolled ? 'bg-text-dark text-white' : 'bg-brand-600 text-white'
                ]"
              >
                {{ cartCount }}
              </span>
            </button>

            <!-- Menu Mobile -->
            <button 
              @click="mobileMenuOpen = !mobileMenuOpen"
              :class="[
                'lg:hidden w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target',
                isScrolled ? 'hover:bg-black/5' : 'hover:bg-white/10'
              ]"
            >
              <svg :class="['w-4 h-4', isScrolled ? 'text-text-dark' : 'text-white']" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Mobile Search Bar - Estilo luxury -->
        <transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <div v-if="mobileSearchOpen" class="lg:hidden mt-4 pb-2">
            <div class="relative">
              <input 
                type="text"
                v-model="searchQuery"
                @input="getSuggestions"
                @keyup.enter="handleSearch()"
                @focus="getSuggestions"
                placeholder="Buscar productos..."
                class="w-full pl-11 pr-4 py-3 bg-white/80 backdrop-blur-sm border border-nude-200/50 rounded-full text-[11px] tracking-wider text-text-dark placeholder-text-light/60 focus:outline-none focus:border-text-dark/20 focus:ring-1 focus:ring-text-dark/5 transition-all"
              />
              <svg 
                class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-light/50 pointer-events-none"
                fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
              
              <!-- Sugerencias móvil -->
              <div 
                v-if="showSuggestions && searchSuggestions.length > 0"
                class="dropdown-search-luxury absolute top-full left-0 right-0 mt-2 bg-white border border-text-dark/8 rounded-2xl overflow-hidden z-50"
                style="box-shadow: 0 12px 40px -8px rgba(216, 27, 96, 0.12), 0 4px 16px -4px rgba(0, 0, 0, 0.08);"
              >
                <div class="max-h-64 overflow-y-auto search-results-scroll">
                  <button
                    v-for="producto in searchSuggestions"
                    :key="producto.id"
                    @click="handleSearch(producto)"
                    class="w-full px-4 py-3 hover:bg-[#FFF0F5] transition-all duration-300 flex items-center gap-3 text-left group border-b border-nude-100/50 last:border-b-0"
                  >
                    <div class="w-11 h-11 rounded-lg overflow-hidden flex-shrink-0 bg-nude-50 ring-1 ring-nude-200/40 group-hover:ring-brand-300/40 transition-all duration-300">
                      <img 
                        v-if="producto.imagen_principal || producto.imagen_url || producto.imagen"
                        :src="getImageUrl(producto.imagen_principal || producto.imagen_url || producto.imagen)"
                        :alt="producto.nombre"
                        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-xs font-medium text-[#2A2A2A] truncate group-hover:text-brand-600 transition-colors duration-300">
                        {{ producto.nombre }}
                      </p>
                      <p class="text-[10px] font-semibold text-brand-600 truncate mt-0.5">
                        {{ formatPrice(getItemPrice(producto)) }}
                      </p>
                    </div>
                  </button>
                </div>
                <div class="border-t border-text-dark/10 bg-nude-50/50">
                  <button
                    @click="handleSearch()"
                    class="w-full px-3 py-2.5 text-[11px] font-medium text-brand-600 hover:text-brand-700 transition-colors flex items-center justify-center gap-1.5"
                  >
                    Ver todos ({{ getTotalSearchResults() }})
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition>

        <!-- Mobile Menu - Estilo luxury minimalista -->
        <transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="opacity-0 -translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-200 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-4"
        >
          <nav v-if="mobileMenuOpen" class="lg:hidden mt-6 pb-4">
            <div class="flex flex-col gap-0.5 bg-white/90 backdrop-blur-xl rounded-2xl p-3 shadow-soft border border-nude-200/30">
              <a href="#categorias" @click="mobileMenuOpen = false" class="py-3.5 px-5 text-[11px] tracking-[0.2em] uppercase text-text-dark/80 hover:text-text-dark hover:bg-nude-100/50 rounded-xl font-medium transition-all">CATEGORÍAS</a>
              <a href="#productos" @click="mobileMenuOpen = false" class="py-3.5 px-5 text-[11px] tracking-[0.2em] uppercase text-text-dark/80 hover:text-text-dark hover:bg-nude-100/50 rounded-xl font-medium transition-all">PRODUCTOS</a>
              <a href="#mayoreo" @click="mobileMenuOpen = false" class="py-3.5 px-5 text-[11px] tracking-[0.2em] uppercase text-text-dark/80 hover:text-text-dark hover:bg-nude-100/50 rounded-xl font-medium transition-all">MAYOREO</a>
              <a href="#testimonios" @click="mobileMenuOpen = false" class="py-3.5 px-5 text-[11px] tracking-[0.2em] uppercase text-text-dark/80 hover:text-text-dark hover:bg-nude-100/50 rounded-xl font-medium transition-all">RESEÑAS</a>
              <a href="#contacto" @click="mobileMenuOpen = false" class="py-3.5 px-5 text-[11px] tracking-[0.2em] uppercase text-text-dark/80 hover:text-text-dark hover:bg-nude-100/50 rounded-xl font-medium transition-all">CONTACTO</a>
            </div>
          </nav>
        </transition>
      </div>
    </header>

    <!-- ========================================
         HERO SECTION - Full Screen High Impact
         ======================================== -->
    <section class="relative min-h-screen flex items-center overflow-hidden">
      
      <!-- ===== BACKGROUND CAROUSEL ===== -->
      <div class="absolute inset-0 z-0">
        <!-- Carousel Images -->
        <transition-group name="hero-crossfade" tag="div" class="absolute inset-0">
          <img 
            v-for="(slide, index) in heroSlides"
            :key="index"
            v-show="currentSlide === index"
            :src="slide.image" 
            :alt="slide.alt" 
            class="absolute inset-0 w-full h-full object-cover object-top"
          />
        </transition-group>
        <!-- Gradients for readability -->
        <div class="absolute inset-0 bg-gradient-to-r from-black/80 via-black/40 to-transparent z-10"></div>
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/20 z-10"></div>
        
        <!-- Carousel Indicators -->
        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2">
          <button 
            v-for="(slide, index) in heroSlides" 
            :key="index"
            @click="goToSlide(index)"
            :class="[
              'w-2 h-2 rounded-full transition-all duration-300',
              currentSlide === index 
                ? 'bg-white w-6' 
                : 'bg-white/40 hover:bg-white/60'
            ]"
          ></button>
        </div>
      </div>

      <!-- ===== CONTENT ===== -->
      <div class="relative z-10 w-full max-w-7xl mx-auto px-5 sm:px-8 lg:px-12 pt-20">
        <div class="max-w-3xl text-left">
          
          <!-- Badge -->
          <div class="inline-flex items-center gap-2.5 bg-white/10 backdrop-blur-md border border-white/20 rounded-full px-5 py-2.5 mb-8 animate-fade-in-up">
            <span class="w-2 h-2 bg-gold-400 rounded-full animate-pulse"></span>
            <span class="text-sm font-medium text-white tracking-wide uppercase">Distribuidora Mayorista desde 2023</span>
          </div>

          <!-- Title -->
          <h1 class="font-luxury text-white leading-[1.1] mb-8 drop-shadow-2xl animate-fade-in-up delay-100">
            <span class="block text-2xl sm:text-3xl lg:text-4xl font-normal mb-2">Tu Socio Experto en</span>
            <span class="block text-5xl sm:text-6xl lg:text-7xl xl:text-8xl text-transparent bg-clip-text bg-gradient-to-r from-white via-gold-200 to-gold-400 font-bold italic">
              Belleza Profesional
            </span>
          </h1>

          <!-- Subtitle -->
          <p class="text-base sm:text-lg lg:text-xl text-gray-100 leading-relaxed mb-8 sm:mb-12 max-w-xl font-light animate-fade-in-up delay-200 antialiased">
            Elevamos tu negocio con extensiones 100% naturales, pelucas premium y cosméticos de clase mundial.
          </p>

          <!-- CTAs - Más compactos en móvil -->
          <div class="flex flex-col sm:flex-row gap-3 sm:gap-5 mb-12 sm:mb-16 animate-fade-in-up delay-300">
            <router-link 
              to="/catalogo" 
              class="inline-flex items-center justify-center px-6 py-3 sm:px-8 sm:py-4 bg-white text-gray-900 font-semibold text-sm sm:text-base rounded-full shadow-lg hover:shadow-xl hover:bg-gray-100 transition-all duration-300 touch-target"
            >
              Ver Catálogo
              <svg class="w-4 h-4 sm:w-5 sm:h-5 ml-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
              </svg>
            </router-link>
            
            <a 
              href="#mayoreo" 
              class="inline-flex items-center justify-center px-6 py-3 sm:px-8 sm:py-4 bg-transparent border border-white/50 text-white font-medium text-sm sm:text-base rounded-full hover:bg-white hover:text-gray-900 transition-all duration-300 backdrop-blur-sm touch-target"
            >
              <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                 <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 003.75-.615A2.993 2.993 0 009.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 002.25 1.016c.896 0 1.7-.393 2.25-1.016a3.001 3.001 0 003.75.614m-16.5 0a3.004 3.004 0 01-.621-4.72L4.318 3.44A1.5 1.5 0 015.378 3h13.243a1.5 1.5 0 011.06.44l1.19 1.189a3 3 0 01-.621 4.72m-13.5 8.65h3.75a.75.75 0 00.75-.75V13.5a.75.75 0 00-.75-.75H6.75a.75.75 0 00-.75.75v3.75c0 .415.336.75.75.75z" />
              </svg>
              Portal Mayorista
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         TRUST BAR - Premium Editorial Ribbon
         ======================================== -->
    <section class="trust-ribbon-premium relative overflow-hidden">
      <!-- Fondo degradado suave -->
      <div class="absolute inset-0 bg-gradient-to-r from-[#FAF7F5] via-[#FDF9F7] to-[#FAF7F5]"></div>
      <!-- Línea decorativa superior -->
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#D4B9A9] to-transparent opacity-40"></div>
      <!-- Línea decorativa inferior -->
      <div class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#D4B9A9] to-transparent opacity-40"></div>
      
      <div class="relative max-w-6xl mx-auto px-4">
        <div class="flex flex-wrap lg:flex-nowrap items-stretch justify-center">
          
          <!-- Item 1: Envíos VIP -->
          <div class="trust-item-premium group w-1/2 lg:w-1/4 py-7 lg:py-9 px-3 lg:px-8 flex flex-col items-center text-center relative">
            <!-- Hover background effect -->
            <div class="absolute inset-0 bg-white/0 group-hover:bg-white/60 transition-all duration-500"></div>
            
            <div class="relative z-10 flex flex-col items-center">
              <!-- Icon container with subtle ring -->
              <div class="w-12 h-12 lg:w-14 lg:h-14 rounded-full border border-[#E8DED8] flex items-center justify-center mb-4 group-hover:border-[#D81B60]/30 group-hover:bg-[#D81B60]/5 transition-all duration-300">
                <svg class="w-5 h-5 lg:w-6 lg:h-6 text-[#8B7355] group-hover:text-[#D81B60] transition-colors duration-300" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                </svg>
              </div>
              <!-- Title -->
              <h4 class="text-[10px] sm:text-[11px] font-semibold tracking-[0.25em] uppercase text-[#1a1a1a] mb-1">
                Envíos VIP
              </h4>
              <!-- Subtitle -->
              <p class="text-[10px] sm:text-[11px] text-[#8B7355] font-light">
                Gratis en compras +$2,999
              </p>
            </div>
            
            <!-- Vertical Divider -->
            <div class="hidden lg:block absolute right-0 top-1/2 -translate-y-1/2 w-px h-16 bg-gradient-to-b from-transparent via-[#D4B9A9]/50 to-transparent"></div>
          </div>

          <!-- Item 2: Calidad Remy -->
          <div class="trust-item-premium group w-1/2 lg:w-1/4 py-7 lg:py-9 px-3 lg:px-8 flex flex-col items-center text-center relative">
            <div class="absolute inset-0 bg-white/0 group-hover:bg-white/60 transition-all duration-500"></div>
            
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-12 h-12 lg:w-14 lg:h-14 rounded-full border border-[#E8DED8] flex items-center justify-center mb-4 group-hover:border-[#D81B60]/30 group-hover:bg-[#D81B60]/5 transition-all duration-300">
                <svg class="w-5 h-5 lg:w-6 lg:h-6 text-[#8B7355] group-hover:text-[#D81B60] transition-colors duration-300" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
                </svg>
              </div>
              <h4 class="text-[10px] sm:text-[11px] font-semibold tracking-[0.25em] uppercase text-[#1a1a1a] mb-1">
                Calidad Remy
              </h4>
              <p class="text-[10px] sm:text-[11px] text-[#8B7355] font-light">
                100% Cabello Humano
              </p>
            </div>
            
            <div class="hidden lg:block absolute right-0 top-1/2 -translate-y-1/2 w-px h-16 bg-gradient-to-b from-transparent via-[#D4B9A9]/50 to-transparent"></div>
          </div>

          <!-- Item 3: Compra Segura -->
          <div class="trust-item-premium group w-1/2 lg:w-1/4 py-7 lg:py-9 px-3 lg:px-8 flex flex-col items-center text-center relative border-t lg:border-t-0 border-[#E8DED8]/50">
            <div class="absolute inset-0 bg-white/0 group-hover:bg-white/60 transition-all duration-500"></div>
            
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-12 h-12 lg:w-14 lg:h-14 rounded-full border border-[#E8DED8] flex items-center justify-center mb-4 group-hover:border-[#D81B60]/30 group-hover:bg-[#D81B60]/5 transition-all duration-300">
                <svg class="w-5 h-5 lg:w-6 lg:h-6 text-[#8B7355] group-hover:text-[#D81B60] transition-colors duration-300" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                </svg>
              </div>
              <h4 class="text-[10px] sm:text-[11px] font-semibold tracking-[0.25em] uppercase text-[#1a1a1a] mb-1">
                Pago Seguro
              </h4>
              <p class="text-[10px] sm:text-[11px] text-[#8B7355] font-light">
                Encriptación SSL 256-bit
              </p>
            </div>
            
            <div class="hidden lg:block absolute right-0 top-1/2 -translate-y-1/2 w-px h-16 bg-gradient-to-b from-transparent via-[#D4B9A9]/50 to-transparent"></div>
          </div>

          <!-- Item 4: Asesoría Experta -->
          <div class="trust-item-premium group w-1/2 lg:w-1/4 py-7 lg:py-9 px-3 lg:px-8 flex flex-col items-center text-center relative border-t lg:border-t-0 border-[#E8DED8]/50">
            <div class="absolute inset-0 bg-white/0 group-hover:bg-white/60 transition-all duration-500"></div>
            
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-12 h-12 lg:w-14 lg:h-14 rounded-full border border-[#E8DED8] flex items-center justify-center mb-4 group-hover:border-[#D81B60]/30 group-hover:bg-[#D81B60]/5 transition-all duration-300">
                <svg class="w-5 h-5 lg:w-6 lg:h-6 text-[#8B7355] group-hover:text-[#D81B60] transition-colors duration-300" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                </svg>
              </div>
              <h4 class="text-[10px] sm:text-[11px] font-semibold tracking-[0.25em] uppercase text-[#1a1a1a] mb-1">
                Asesoría VIP
              </h4>
              <p class="text-[10px] sm:text-[11px] text-[#8B7355] font-light">
                Atención Personalizada
              </p>
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

        <!-- Bento Grid - Adaptativo Inteligente -->
        <div class="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-5 lg:gap-6">
          <div 
            v-for="(categoria, index) in categorias" 
            :key="categoria.id"
            :class="[
              'group cursor-pointer',
              // En móvil, solo categoría destacada (P1) ocupa 2 columnas
              categoria.prioridad === 1 && index === 0 ? 'col-span-2' : '',
              // Lógica adaptativa para tablet y desktop
              categorias.length === 1 ? 'md:col-span-2 lg:col-span-3' : 
              categorias.length === 2 ? 'md:col-span-1 lg:col-span-1.5' : 
              categorias.length === 3 && categoria.prioridad === 1 ? 'md:col-span-2 lg:col-span-2 lg:row-span-2' : 
              categorias.length === 3 && categoria.prioridad !== 1 ? '' : 
              categorias.length >= 4 && index === 0 && categoria.prioridad === 1 ? 'md:col-span-2' : 
              ''
            ]"
            @click="irACategoria(categoria)"
            role="button"
            tabindex="0"
          >
            <div 
              :class="[
                'relative bento-item shadow-soft hover-lift overflow-hidden rounded-2xl sm:rounded-3xl',
                // Altura adaptativa móvil primero
                categoria.prioridad === 1 && index === 0 ? 'h-56 sm:h-80 lg:h-96' : 'h-40 sm:h-64 lg:h-80',
                // Lógica para otros tamaños
                categorias.length === 1 ? 'sm:h-96 lg:h-[500px]' :
                categorias.length === 2 ? 'sm:h-80 lg:h-96' :
                categorias.length === 3 && categoria.prioridad === 1 ? 'sm:h-80 lg:h-full lg:min-h-[400px]' :
                categorias.length === 3 && categoria.prioridad !== 1 ? 'sm:h-64 lg:h-full lg:min-h-[200px]' : ''
              ]"
            >
              <img 
                :src="categoria.imagen || 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=1000&h=800&fit=crop&q=85'" 
                :alt="categoria.nombre" 
                class="absolute inset-0 w-full h-full object-cover img-zoom"
              >
              <div class="absolute inset-0 bento-overlay"></div>
              <div 
                :class="[
                  'absolute bottom-0 left-0 right-0',
                  // Padding adaptativo - más compacto en móvil
                  categoria.prioridad === 1 && index === 0 ? 'p-4 sm:p-6 lg:p-8' : 'p-3 sm:p-5 lg:p-6'
                ]"
              >
                <!-- Badge "MÁS VENDIDO" solo para la primera P1 -->
                <span 
                  v-if="categoria.prioridad === 1 && categoria.orden === 1" 
                  class="inline-block bg-gold-400 text-white text-[10px] sm:text-xs font-bold px-2 sm:px-3 py-0.5 sm:py-1 rounded-full mb-2 sm:mb-3"
                >
                  MÁS VENDIDO
                </span>
                
                <!-- Título adaptativo -->
                <h3 
                  :class="[
                    'font-luxury text-white mb-1 sm:mb-2',
                    categoria.prioridad === 1 && index === 0 ? 'text-lg sm:text-2xl lg:text-3xl' : 'text-sm sm:text-xl lg:text-2xl'
                  ]"
                >
                  {{ categoria.nombre }}
                </h3>
                
                <!-- Descripción - oculta en tarjetas pequeñas en móvil -->
                <p 
                  v-if="categoria.prioridad === 1 && index === 0"
                  :class="[
                    'text-white/80 mb-2 sm:mb-4',
                    'text-xs sm:text-base max-w-md'
                  ]"
                >
                  {{ categoria.descripcion }}
                </p>
                <p 
                  v-else
                  class="hidden sm:block text-white/80 mb-4 text-sm"
                >
                  {{ categoria.descripcion_corta || categoria.descripcion }}
                </p>
                
                <!-- CTA -->
                <span 
                  :class="[
                    'inline-flex items-center gap-1.5 sm:gap-2 text-white font-medium transition-all',
                    categoria.prioridad === 1 && index === 0 ? 'text-xs sm:text-base group-hover:gap-4' : 'text-[11px] sm:text-sm group-hover:gap-3'
                  ]"
                >
                  {{ categoria.prioridad === 1 && index === 0 ? 'Explorar colección' : 'Ver más' }}
                  <svg 
                    :class="categoria.prioridad === 1 && index === 0 ? 'w-4 h-4 sm:w-5 sm:h-5' : 'w-3 h-3 sm:w-4 sm:h-4'" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2" 
                    viewBox="0 0 24 24"
                  >
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
      <div class="max-w-screen-xl mx-auto px-5 sm:px-8 lg:px-10">
        <!-- Section Header -->
        <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6 mb-14">
          <div>
            <span class="inline-block text-brand-600 font-medium text-sm tracking-widest uppercase mb-4">Selección Premium</span>
            <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-text-dark">
              Productos <em class="not-italic text-brand-600">Destacados</em>
            </h2>
          </div>
          <router-link to="/catalogo" class="inline-flex items-center gap-2 text-text-medium hover:text-brand-600 font-medium transition-colors group">
            Ver todo el catálogo
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
            </svg>
          </router-link>
        </div>

        <!-- Loading State - Skeleton dinámico -->
        <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8">
          <div class="animate-pulse col-span-full flex items-center justify-center py-12">
            <div class="flex flex-col items-center gap-4">
              <div class="w-12 h-12 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin"></div>
              <p class="text-text-light text-sm">Cargando productos...</p>
            </div>
          </div>
        </div>

        <!-- Products Grid -->
        <div v-else-if="productos.length > 0" class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6 lg:gap-8">
          <div
            v-for="producto in productos"
            :key="producto.id"
            :data-producto-id="producto.id"
            :data-producto-nombre="producto.nombre"
            @click="irADetalle(producto.id)"
            class="group cursor-pointer"
          >
            <div class="relative bg-white rounded-2xl sm:rounded-3xl overflow-hidden shadow-soft hover-lift mb-3 sm:mb-5">
              <!-- Badge -->
              <div class="absolute top-2 sm:top-4 left-2 sm:left-4 z-10">
                <span class="bg-white/90 backdrop-blur-sm text-text-dark text-[10px] sm:text-xs font-medium px-2 sm:px-3 py-1 sm:py-1.5 rounded-full shadow-sm">
                  {{ producto.categoria || 'Premium' }}
                </span>
              </div>
              
              <!-- Wishlist Button -->
              <button 
                @click.stop="toggleFavorito(producto)"
                class="absolute top-2 sm:top-4 right-2 sm:right-4 z-10 w-8 h-8 sm:w-10 sm:h-10 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-sm hover:bg-brand-50 transition-colors touch-target"
              >
                <svg class="w-4 h-4 sm:w-5 sm:h-5 text-text-light hover:text-brand-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>
              </button>

              <!-- Image -->
              <div class="aspect-[3/4] overflow-hidden bg-nude-100">
                <img
                  v-if="producto.imagen_principal || producto.imagen_url || producto.imagen"
                  :src="getImageUrl(producto.imagen_principal || producto.imagen_url || producto.imagen)"
                  :alt="producto.nombre"
                  class="w-full h-full object-cover img-zoom"
                  @error="handleImageError"
                >
                <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-nude-100 to-nude-200">
                  <svg class="w-24 h-24 text-nude-400" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
                  </svg>
                </div>
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
            <div class="px-2 sm:px-1">
              <p class="text-[10px] sm:text-xs text-text-light uppercase tracking-wider mb-0.5 sm:mb-1">{{ producto.categoria || producto.metodo || 'Extensiones' }}</p>
              <h3 class="font-medium text-xs sm:text-base text-text-dark mb-1 sm:mb-2 line-clamp-2 group-hover:text-brand-600 transition-colors">{{ producto.nombre }}</h3>
              <p class="text-sm sm:text-lg font-semibold text-brand-600">${{ formatPrice(producto.precio_monto || producto.precio) }} <span class="text-[10px] sm:text-xs text-text-light font-normal">{{ producto.precio_moneda || 'COP' }}</span></p>
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
         VIDEO KANEKALON - Sección Inmersiva Optimizada
         ======================================== -->
    <section class="relative bg-black overflow-hidden">
      <!-- Video Background con altura mínima para móvil -->
      <div class="relative w-full min-h-[50vh] sm:min-h-[60vh] lg:min-h-0">
        <video 
          ref="kanekalonVideo"
          class="w-full h-full min-h-[50vh] sm:min-h-[60vh] lg:min-h-0 lg:h-auto lg:max-h-[80vh] object-cover"
          autoplay 
          loop 
          muted 
          playsinline
          preload="auto"
        >
          <!-- Video local de alta calidad -->
          <source src="/kanekalon-video.mp4" type="video/mp4">
          Tu navegador no soporta videos HTML5.
        </video>
        
        <!-- Overlay con gradiente optimizado para legibilidad -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-black/40"></div>
        
        <!-- Contenido sobre el video - Mejor posicionado en móvil -->
        <div class="absolute inset-0 flex items-center lg:items-end justify-center pb-8 sm:pb-12 lg:pb-20">
          <div class="text-center px-5 sm:px-6">
            <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-1.5 sm:px-5 sm:py-2 mb-4 sm:mb-6">
              <span class="text-white/90 text-xs sm:text-sm font-medium uppercase tracking-wider">Calidad Premium</span>
            </div>
            <h2 class="font-luxury text-2xl sm:text-3xl lg:text-5xl text-white mb-3 sm:mb-4 drop-shadow-2xl">
              Extensiones 100% <span class="text-brand-400">Naturales</span>
            </h2>
            <p class="text-white/80 text-sm sm:text-base lg:text-lg max-w-md sm:max-w-xl lg:max-w-2xl mx-auto mb-6 sm:mb-8 leading-relaxed">
              Tecnología de fibras de la más alta calidad. Transforma tu look con elegancia y sofisticación profesional.
            </p>
            <router-link 
              to="/catalogo"
              class="inline-flex items-center gap-2 bg-white hover:bg-nude-100 text-text-dark font-medium text-sm sm:text-base px-5 py-2.5 sm:px-7 sm:py-3.5 rounded-full transition-all shadow-lg hover:shadow-xl"
            >
              Ver Catálogo Completo
              <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         SECCIÓN MAYORISTA - Diseño Premium
         ======================================== -->
    <section id="mayoreo" class="py-14 sm:py-20 lg:py-32 relative overflow-hidden bg-gradient-to-br from-[#F5EDE4] via-[#FBF7F3] to-[#F0E6DC]">
      <!-- Decorative Pattern -->
      <div class="absolute inset-0 opacity-[0.03]" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12 relative z-10">
        <div class="grid lg:grid-cols-2 gap-8 sm:gap-12 lg:gap-16 items-center">
          
          <!-- Image First -->
          <div class="relative order-2 lg:order-1">
            <div class="relative rounded-3xl overflow-hidden shadow-2xl">
              <img 
                src="https://images.unsplash.com/photo-1560066984-138dadb4c035?w=700&h=800&fit=crop&q=85" 
                alt="Salón de belleza profesional" 
                class="w-full h-auto"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>
              
              <!-- Stats Card -->
              <div class="absolute bottom-6 left-6 right-6 bg-white/95 backdrop-blur-sm rounded-2xl shadow-xl p-6">
                <div class="flex items-center justify-around gap-4">
                  <div class="text-center">
                    <p class="text-3xl sm:text-4xl font-bold text-brand-600 mb-1">2K+</p>
                    <p class="text-xs text-text-medium uppercase tracking-wider font-medium">Mayoristas</p>
                  </div>
                  <div class="w-px h-12 bg-nude-300"></div>
                  <div class="text-center">
                    <p class="text-3xl sm:text-4xl font-bold text-brand-600 mb-1">500+</p>
                    <p class="text-xs text-text-medium uppercase tracking-wider font-medium">Productos</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Content -->
          <div class="order-1 lg:order-2">
            <span class="inline-flex items-center gap-2.5 bg-brand-50 border border-brand-200 text-brand-700 text-xs font-semibold px-4 py-2 rounded-full mb-6">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              PROGRAMA EXCLUSIVO MAYORISTAS
            </span>

            <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-text-dark leading-tight mb-6">
              Impulsa tu <em class="not-italic text-brand-600">Negocio</em> de Belleza
            </h2>

            <p class="text-text-medium text-lg mb-8 max-w-xl leading-relaxed">
              Únete a más de 2,000 profesionales que confían en Kharis para surtir sus salones, tiendas y negocios de belleza.
            </p>

            <!-- Benefits - Más compactos en móvil -->
            <ul class="space-y-3 sm:space-y-5 mb-8 sm:mb-10">
              <li class="flex items-start gap-3 sm:gap-4">
                <div class="w-8 h-8 sm:w-10 sm:h-10 bg-green-50 rounded-lg sm:rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 sm:w-5 sm:h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p class="text-text-dark font-semibold text-sm sm:text-base mb-0.5">Descuentos desde 25% en adelante</p>
                  <p class="text-text-light text-xs sm:text-sm">Precios escalonados según volumen de compra</p>
                </div>
              </li>
              <li class="flex items-start gap-3 sm:gap-4">
                <div class="w-8 h-8 sm:w-10 sm:h-10 bg-green-50 rounded-lg sm:rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 sm:w-5 sm:h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p class="text-text-dark font-semibold text-sm sm:text-base mb-0.5">Asesor de cuenta dedicado</p>
                  <p class="text-text-light text-xs sm:text-sm">Atención personalizada vía WhatsApp</p>
                </div>
              </li>
              <li class="flex items-start gap-3 sm:gap-4">
                <div class="w-8 h-8 sm:w-10 sm:h-10 bg-green-50 rounded-lg sm:rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 sm:w-5 sm:h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <p class="text-text-dark font-semibold text-sm sm:text-base mb-0.5">Envío gratis en pedidos +$50,000 COP</p>
                  <p class="text-text-light text-xs sm:text-sm">Entregas prioritarias a todo Colombia</p>
                </div>
              </li>
            </ul>

            <!-- CTAs - Más compactos en móvil -->
            <div class="flex flex-col sm:flex-row gap-3 sm:gap-4">
              <a 
                href="https://wa.me/4796657763?text=Hola,%20me%20interesa%20el%20programa%20de%20mayoristas"
                target="_blank"
                class="inline-flex items-center justify-center gap-2 sm:gap-3 bg-green-500 hover:bg-green-600 text-white font-semibold text-sm sm:text-base px-5 py-3 sm:px-7 sm:py-3.5 rounded-full transition-all shadow-lg touch-target"
              >
                <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
                Contactar por WhatsApp
              </a>
              <button class="inline-flex items-center justify-center gap-2 sm:gap-3 bg-white hover:bg-nude-50 border-2 border-nude-300 text-text-dark font-medium text-sm sm:text-base px-5 py-3 sm:px-7 sm:py-3.5 rounded-full transition-all hover:border-brand-400 touch-target">
                Solicitar catálogo
              </button>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ========================================
         MARCAS CON LAS QUE TRABAJAMOS
         ======================================== -->
    <section class="py-20 lg:py-28 bg-gradient-to-b from-white to-nude-50">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <div class="text-center mb-16">
          <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-text-dark mb-4">
            Marcas <em class="not-italic text-brand-600">top</em> de nuestra tienda
          </h2>
          <p class="text-text-dark text-base sm:text-lg max-w-2xl mx-auto font-medium">
            Trabajamos con las mejores marcas de extensiones y productos de cabello natural
          </p>
        </div>

        <!-- Logos Grid -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 lg:gap-8 items-center">
          <!-- Placeholder para logos - El usuario agregará las imágenes a /public -->
          <div class="flex items-center justify-center p-8 bg-white rounded-2xl hover:shadow-luxury transition-all duration-300 border border-nude-200 hover:border-brand-300 hover:-translate-y-1">
            <div class="text-center">
              <p class="text-sm sm:text-base text-text-dark uppercase tracking-wide font-bold">kanekalon</p>
            </div>
          </div>
          <div class="flex items-center justify-center p-8 bg-white rounded-2xl hover:shadow-luxury transition-all duration-300 border border-nude-200 hover:border-brand-300 hover:-translate-y-1">
            <div class="text-center">
              <p class="text-sm sm:text-base text-text-dark uppercase tracking-wide font-bold">Cabello Humano</p>
            </div>
          </div>
          <div class="flex items-center justify-center p-8 bg-white rounded-2xl hover:shadow-luxury transition-all duration-300 border border-nude-200 hover:border-brand-300 hover:-translate-y-1">
            <div class="text-center">
              <p class="text-sm sm:text-base text-text-dark uppercase tracking-wide font-bold">Virgin Hair</p>
            </div>
          </div>
          <div class="flex items-center justify-center p-8 bg-white rounded-2xl hover:shadow-luxury transition-all duration-300 border border-nude-200 hover:border-brand-300 hover:-translate-y-1">
            <div class="text-center">
              <p class="text-sm sm:text-base text-text-dark uppercase tracking-wide font-bold">Remy Hair</p>
            </div>
          </div>
          <div class="flex items-center justify-center p-8 bg-white rounded-2xl hover:shadow-luxury transition-all duration-300 border border-nude-200 hover:border-brand-300 hover:-translate-y-1">
            <div class="text-center">
              <p class="text-sm sm:text-base text-text-dark uppercase tracking-wide font-bold">Brazilian Hair</p>
            </div>
          </div>
          <div class="flex items-center justify-center p-8 bg-white rounded-2xl hover:shadow-luxury transition-all duration-300 border border-nude-200 hover:border-brand-300 hover:-translate-y-1">
            <div class="text-center">
              <p class="text-sm sm:text-base text-text-dark uppercase tracking-wide font-bold">Premium Extensions</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         OFERTAS IRRESISTIBLES - Editorial Premium Design
         ======================================== -->
    <section class="relative bg-gradient-to-br from-[#FDFBFA] via-[#FAF7F5] to-[#FDFBFA] overflow-hidden py-20 lg:py-28">
      <!-- Líneas decorativas sutiles -->
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#D4B9A9]/30 to-transparent"></div>
      <div class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#D4B9A9]/30 to-transparent"></div>

      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <div class="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">
          
          <!-- Imagen Principal - Más cerca del texto -->
          <div class="relative order-2 lg:order-1">
            <div class="relative">
              <img 
                src="/promocion.webp" 
                alt="Promociones especiales" 
                class="w-full h-auto rounded-2xl shadow-xl"
              />
              <!-- Decorative frame -->
              <div class="absolute -inset-3 border border-[#D4B9A9]/20 rounded-3xl pointer-events-none"></div>
            </div>
          </div>

          <!-- Contenido - Diseño editorial integrado -->
          <div class="order-1 lg:order-2 lg:pl-4">
            
            <!-- Badge flotante minimalista con borde dorado -->
            <div class="inline-flex items-center gap-2 border border-[#C9A962]/50 rounded-sm px-4 py-1.5 mb-8">
              <span class="w-1.5 h-1.5 bg-[#C9A962] rounded-full"></span>
              <span class="text-[10px] tracking-[0.25em] uppercase text-[#8B7355] font-medium">EDICIÓN LIMITADA</span>
            </div>

            <!-- Título Principal - Cerca de la imagen -->
            <h2 class="font-luxury text-4xl sm:text-5xl lg:text-6xl text-text-dark leading-[1.1] mb-5">
              ¡<span class="text-brand-600">OFERTAS</span><br>
              <span class="font-luxury italic font-normal">irresistibles</span>!
            </h2>

            <!-- Descripción -->
            <p class="text-text-medium text-base sm:text-lg mb-8 leading-relaxed max-w-md">
              Disfruta de los mejores precios en cosméticos y productos de belleza por tiempo limitado, ¡aprovecha!
            </p>

            <!-- BENEFICIOS INTEGRADOS - Lista vertical con checkmarks elegantes -->
            <ul class="space-y-3 mb-10">
              <li class="flex items-center gap-3">
                <svg class="w-4 h-4 text-[#C9A962] flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
                <span class="text-sm text-text-dark/80">Hasta <span class="font-semibold text-text-dark">40% de descuento</span></span>
              </li>
              <li class="flex items-center gap-3">
                <svg class="w-4 h-4 text-[#C9A962] flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25m0 0V4.5m0 0H8.25m6 0V4.5m0 0H8.25" />
                </svg>
                <span class="text-sm text-text-dark/80">Envío <span class="font-semibold text-text-dark">gratis</span> en compras +$999</span>
              </li>
              <li class="flex items-center gap-3">
                <svg class="w-4 h-4 text-[#C9A962] flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                </svg>
                <span class="text-sm text-text-dark/80">Garantía de <span class="font-semibold text-text-dark">30 días</span></span>
              </li>
            </ul>

            <!-- CTA Button - Negro sólido elegante -->
            <a 
              href="#productos"
              class="inline-flex items-center justify-center gap-3 bg-text-dark hover:bg-black text-white font-medium text-sm tracking-wide px-8 py-4 rounded-sm transition-all hover:shadow-lg touch-target"
            >
              <span>VER COLECCIÓN</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
              </svg>
            </a>
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
                <li><a href="#" class="text-white/60 hover:text-white transition-colors text-sm">Accesorios</a></li>
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
                  <span class="text-white/60 text-sm">+47 966 57 763</span>
                </li>
                <li class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                  <a href="https://wa.me/4796657763" class="text-white/60 hover:text-white transition-colors text-sm">WhatsApp</a>
                </li>
                <li class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-brand-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                  </svg>
                  <a href="mailto:kharisdistribuidora1@gmail.com" class="text-white/60 hover:text-white transition-colors text-sm">karisdistribuidora1@gmail.com</a>
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
         FLOATING SOCIAL BUTTONS (Right Side) - Compactos en móvil
         ======================================== -->
    <!-- Instagram Button -->
    <a 
      href="https://www.instagram.com/kharis_hair21/"
      target="_blank"
      class="fixed bottom-24 sm:bottom-28 right-4 sm:right-6 w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 bg-gradient-to-br from-purple-500 via-pink-500 to-orange-400 text-white rounded-full flex items-center justify-center shadow-xl hover:scale-110 transition-all duration-300 z-40 group touch-target"
    >
      <svg class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
      </svg>
      <!-- Tooltip - Solo desktop -->
      <span class="hidden lg:block absolute right-full mr-3 bg-white text-text-dark text-sm font-medium px-4 py-2 rounded-xl shadow-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        Síguenos en Instagram
      </span>
    </a>

    <!-- WhatsApp Button -->
    <a 
      href="https://wa.me/4796657763?text=Hola,%20me%20interesa%20información%20sobre%20sus%20productos"
      target="_blank"
      class="fixed bottom-4 sm:bottom-6 right-4 sm:right-6 w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 bg-green-500 text-white rounded-full flex items-center justify-center shadow-xl hover:bg-green-600 hover:scale-110 transition-all duration-300 z-40 group touch-target"
    >
      <svg class="w-5 h-5 sm:w-6 sm:h-6 lg:w-8 lg:h-8" fill="currentColor" viewBox="0 0 24 24">
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
      </svg>
      <!-- Tooltip - Solo desktop -->
      <span class="hidden lg:block absolute right-full mr-3 bg-white text-text-dark text-sm font-medium px-4 py-2 rounded-xl shadow-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        ¿Necesitas ayuda?
      </span>
    </a>

    <!-- ========================================
         SCROLL TO TOP BUTTON (Left Side) - Compacto en móvil
         ======================================== -->
    <button 
      v-show="isScrolled"
      @click="scrollToTop"
      class="fixed bottom-4 sm:bottom-6 left-4 sm:left-6 w-10 h-10 sm:w-12 sm:h-12 lg:w-14 lg:h-14 bg-brand-600 hover:bg-brand-700 text-white rounded-full flex items-center justify-center shadow-xl hover:scale-110 transition-all duration-300 z-40 group touch-target"
    >
      <svg class="w-4 h-4 sm:w-5 sm:h-5 lg:w-6 lg:h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
      </svg>
      <!-- Tooltip - Solo desktop -->
      <span class="hidden lg:block absolute left-full ml-3 bg-white text-text-dark text-sm font-medium px-4 py-2 rounded-xl shadow-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        Subir
      </span>
    </button>

    <!-- ========================================
         TOAST NOTIFICATION - Estilo Premium Shopping (tipo Instagram)
         ======================================== -->
    <transition
      enter-active-class="transition-all duration-400 ease-out"
      leave-active-class="transition-all duration-300 ease-in"
      enter-from-class="opacity-0 translate-y-[-20px] scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-[-10px] scale-95"
    >
      <div 
        v-if="toast.show"
        class="fixed top-20 right-4 sm:right-6 z-[100] max-w-[360px] w-full sm:w-auto"
      >
        <!-- Toast para producto agregado (con imagen) -->
        <div 
          v-if="toast.type === 'cart' && toast.product"
          class="bg-white/95 rounded-2xl shadow-2xl overflow-hidden border border-nude-100"
          style="box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0,0,0,0.02);"
        >
          <!-- Contenido principal -->
          <div class="flex items-center gap-4 p-4">
            <!-- Thumbnail del producto -->
            <div class="w-16 h-16 rounded-xl bg-gradient-to-br from-nude-50 to-nude-100 flex-shrink-0 overflow-hidden flex items-center justify-center">
              <img 
                v-if="toast.product.imagen_url" 
                :src="toast.product.imagen_url" 
                :alt="toast.product.nombre"
                class="w-full h-full object-cover"
              />
              <svg v-else class="w-7 h-7 text-brand-300" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
            </div>
            
            <!-- Info -->
            <div class="flex-1 min-w-0">
              <h4 class="font-luxury text-sm text-text-dark">¡Excelente elección!</h4>
              <p class="text-xs text-text-medium mt-0.5 truncate">{{ toast.product.nombre }}</p>
            </div>
            
            <!-- CTA Ver Bolsa -->
            <button 
              @click="openCartDrawer(); toast.show = false"
              class="flex-shrink-0 text-xs font-semibold text-brand-600 hover:text-brand-700 uppercase tracking-wide transition-colors"
            >
              Ver bolsa
            </button>
          </div>
          
          <!-- Barra de progreso envío gratis -->
          <div v-if="getCartSubtotal() < 300000" class="px-4 pb-3">
            <div class="flex items-center gap-2">
              <div class="flex-1 h-1 bg-nude-100 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-brand-400 to-brand-600 rounded-full transition-all duration-500"
                  :style="{ width: Math.min(100, (getCartSubtotal() / 300000) * 100) + '%' }"
                ></div>
              </div>
              <span class="text-[10px] text-text-medium whitespace-nowrap">
                ${{ formatPrice(300000 - getCartSubtotal()) }} para envío gratis
              </span>
            </div>
          </div>
        </div>
        
        <!-- Toast genérico (info, error, success sin producto) -->
        <div 
          v-else
          class="bg-white/95 rounded-2xl shadow-2xl overflow-hidden"
          style="box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);"
        >
          <div class="flex items-center gap-3 px-5 py-4">
            <!-- Icono según tipo -->
            <div 
              :class="[
                'w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0',
                toast.type === 'success' ? 'bg-green-50' : toast.type === 'error' ? 'bg-red-50' : 'bg-brand-50'
              ]"
            >
              <svg v-if="toast.type === 'success'" class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="toast.type === 'error'" class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <svg v-else class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span class="text-sm font-medium text-text-dark">{{ toast.message }}</span>
          </div>
        </div>
      </div>
    </transition>

    <!-- ========================================
         CART DRAWER - Sidebar derecha (Estilo Soft Beauty)
         ======================================== -->
    <!-- Overlay oscuro sin blur para rendimiento -->
    <transition
      enter-active-class="transition-opacity duration-300 ease-out"
      leave-active-class="transition-opacity duration-200 ease-in"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="showCartDrawer"
        class="fixed inset-0 bg-black/40 z-50"
        @click="closeCartDrawer"
      ></div>
    </transition>
    
    <!-- Panel del Carrito - Soft Beauty Style -->
    <transition
      enter-active-class="transition-transform duration-300 ease-out"
      leave-active-class="transition-transform duration-200 ease-in"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <div 
        v-if="showCartDrawer"
        class="fixed top-0 right-0 h-full w-full sm:w-[400px] bg-white z-[60] flex flex-col"
        style="box-shadow: -20px 0 60px -15px rgba(0, 0, 0, 0.15);"
        @click.stop
      >
        <!-- Header - Elegante con Serif -->
        <div class="flex items-center justify-between px-6 py-5 border-b border-nude-200/50">
          <h2 class="font-luxury text-xl text-text-dark tracking-wide">Tu Selección</h2>
          <button 
            @click="closeCartDrawer"
            class="w-8 h-8 rounded-full flex items-center justify-center hover:bg-nude-100 transition-colors"
          >
            <svg class="w-4 h-4 text-text-medium" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Barra de Progreso Envío Gratis - Minimalista -->
        <div v-if="getCartSubtotal() < 300000" class="px-6 py-4 bg-gradient-to-r from-nude-50 to-white">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs text-text-medium">
              Te faltan ${{ formatPrice(300000 - getCartSubtotal()) }} para envío gratis
            </span>
            <span class="text-xs text-brand-600 font-medium">{{ Math.min(100, Math.round((getCartSubtotal() / 300000) * 100)) }}%</span>
          </div>
          <div class="h-1 bg-nude-200 rounded-full overflow-hidden">
            <div 
              class="h-full bg-gradient-to-r from-brand-500 to-brand-600 rounded-full transition-all duration-500"
              :style="{ width: Math.min(100, (getCartSubtotal() / 300000) * 100) + '%' }"
            ></div>
          </div>
        </div>
        <div v-else class="px-6 py-4 bg-gradient-to-r from-green-50 to-white">
          <div class="flex items-center justify-center gap-2">
            <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-sm text-green-700 font-medium">Envío gratis aplicado</span>
          </div>
        </div>
        
        <!-- Contenido del Carrito -->
        <div class="flex-1 overflow-y-auto px-4">
          <!-- Loading -->
          <div v-if="cartLoading" class="flex items-center justify-center h-32">
            <div class="w-8 h-8 border-2 border-brand-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
          
          <!-- Carrito vacío - Femenino -->
          <div v-else-if="cartItems.length === 0" class="flex flex-col items-center justify-center h-72 text-center px-4">
            <div class="w-24 h-24 rounded-full bg-gradient-to-br from-nude-100 to-nude-200 flex items-center justify-center mb-5">
              <svg class="w-10 h-10 text-brand-400" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
            </div>
            <h3 class="font-luxury text-lg text-text-dark mb-2">Tu selección está vacía</h3>
            <p class="text-text-medium text-sm mb-6">Descubre productos increíbles para ti</p>
            <button 
              @click="closeCartDrawer"
              class="bg-brand-600 hover:bg-brand-700 text-white font-medium text-sm px-8 py-3 rounded-full transition-all hover:shadow-lg hover:shadow-brand-600/25"
            >
              Explorar colección
            </button>
          </div>
          
          <!-- Items del carrito - Soft Beauty -->
          <div v-else class="py-4 space-y-4">
            <div 
              v-for="item in cartItems" 
              :key="item.producto_id"
              class="flex gap-4 p-3 bg-white rounded-xl border border-nude-100 hover:border-nude-200 transition-colors"
            >
              <!-- Imagen del producto - Más grande y redondeada -->
              <div class="w-[90px] h-[90px] bg-gradient-to-br from-nude-50 to-nude-100 rounded-xl flex-shrink-0 overflow-hidden flex items-center justify-center">
                <img 
                  v-if="item.imagen_url" 
                  :src="item.imagen_url" 
                  :alt="item.nombre"
                  class="w-full h-full object-cover"
                />
                <svg v-else class="w-8 h-8 text-nude-300" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
                </svg>
              </div>
              
              <!-- Info del producto -->
              <div class="flex-1 min-w-0 flex flex-col justify-between py-1">
                <div>
                  <h3 class="text-sm font-medium text-text-dark leading-snug line-clamp-2 mb-1">
                    {{ item.nombre || 'Producto' }}
                  </h3>
                  
                  <!-- Selector de Cantidad - Estilo Píldora -->
                  <div class="flex items-center gap-2 mt-2">
                    <div class="inline-flex items-center border border-nude-200 rounded-full">
                      <button 
                        @click="updateQuantity(item.producto_id, (item.cantidad || 1) - 1)"
                        class="w-7 h-7 flex items-center justify-center text-text-medium hover:text-text-dark transition-colors"
                        :disabled="(item.cantidad || 1) <= 1"
                      >
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" d="M5 12h14" />
                        </svg>
                      </button>
                      <span class="w-8 text-center text-sm font-medium text-text-dark">{{ item.cantidad || 1 }}</span>
                      <button 
                        @click="updateQuantity(item.producto_id, (item.cantidad || 1) + 1)"
                        class="w-7 h-7 flex items-center justify-center text-text-medium hover:text-text-dark transition-colors"
                      >
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" d="M12 5v14m-7-7h14" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
                
                <!-- Precio -->
                <p class="text-base font-semibold text-text-dark mt-1">
                  ${{ formatPrice(getItemPrice(item)) }}
                </p>
              </div>
              
              <!-- Eliminar - Más visible -->
              <button 
                @click.stop="removeFromCart(item.producto_id)"
                class="self-start mt-1 w-8 h-8 rounded-full flex items-center justify-center bg-red-50 hover:bg-red-100 transition-colors group"
                title="Eliminar producto"
              >
                <svg class="w-4 h-4 text-red-400 group-hover:text-red-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
              </button>
            </div>
            
            <!-- Espacio adicional al final de la lista -->
          </div>
        </div>
        
        <!-- Footer - Fondo Nude, Botón Pill con Glow -->
        <div v-if="cartItems.length > 0" class="border-t border-nude-200" style="background: #FDFBF7;">
          <!-- Resumen de precios -->
          <div class="px-6 py-4 space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-text-medium">Subtotal</span>
              <span class="text-text-dark">${{ formatPrice(getCartSubtotal()) }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-text-medium">Envío</span>
              <span class="text-text-medium italic">Por calcular</span>
            </div>
            <div class="flex items-center justify-between pt-3 border-t border-nude-200">
              <span class="text-text-dark font-medium">Total</span>
              <span class="font-luxury text-2xl font-bold text-text-dark">${{ formatPrice(getCartSubtotal()) }}</span>
            </div>
          </div>
          
          <!-- Botones -->
          <div class="px-6 pb-6 space-y-3">
            <button 
              @click="irACheckout"
              class="w-full bg-brand-600 hover:bg-brand-700 text-white font-medium text-sm py-4 rounded-full transition-all uppercase tracking-wider hover:shadow-xl hover:shadow-brand-600/30"
            >
              Finalizar Compra
            </button>
            <button 
              @click="closeCartDrawer"
              class="w-full text-sm text-text-medium hover:text-text-dark transition-colors py-2"
            >
              Seguir comprando
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { productosService, carritoService, authService, favoritosService } from '../services/productos'
import { categoriasService } from '../services/categorias'
import { getImageUrl } from '../services/api'

export default {
  name: 'Home',
  setup() {
    const router = useRouter()
    const productos = ref([])
    const categorias = ref([])
    const loading = ref(true)
    const error = ref(null)
    const cartCount = ref(0)
    const isScrolled = ref(false)
    const mobileMenuOpen = ref(false)
    const mobileSearchOpen = ref(false)
    const searchQuery = ref('')
    const searchSuggestions = ref([])
    const showSuggestions = ref(false)
    const searchInputRef = ref(null)
    const suggestionsRef = ref(null)
    
    // Ya no necesitamos computed separados, usamos categorias.value directamente
    
    // Estado de usuario - usando ref para reactividad inmediata
    const isLoggedIn = ref(authService.isAuthenticated())
    const currentUser = ref(JSON.parse(localStorage.getItem('user') || 'null'))
    const userInitial = computed(() => {
      if (!currentUser.value) return ''
      return (currentUser.value.nombre || currentUser.value.email || 'U')[0].toUpperCase()
    })
    
    // ===== TOAST NOTIFICATION SYSTEM =====
    const toast = ref({
      show: false,
      message: '',
      type: 'success', // 'success', 'error', 'info', 'cart'
      product: null // Para mostrar info del producto en el toast
    })
    let toastTimeout = null
    
    const showToast = (message, type = 'success', product = null) => {
      if (toastTimeout) clearTimeout(toastTimeout)
      toast.value = { show: true, message, type, product }
      toastTimeout = setTimeout(() => {
        toast.value.show = false
      }, 4000) // 4 segundos para el toast con producto
    }
    
    // Toast especial para carrito con producto
    const showCartToast = (product) => {
      if (toastTimeout) clearTimeout(toastTimeout)
      toast.value = { 
        show: true, 
        message: '¡Agregado a tu bolsa!', 
        type: 'cart', 
        product: {
          nombre: product.nombre || 'Producto',
          imagen_url: product.imagen_url || product.imagenes?.[0] || null,
          precio: product.precio_final || product.precio || 0
        }
      }
      toastTimeout = setTimeout(() => {
        toast.value.show = false
      }, 5000) // 5 segundos para ver bien el producto
    }
    
    // ===== CART DRAWER =====
    const showCartDrawer = ref(false)
    const cartItems = ref([])
    const cartTotal = ref(0)
    const cartLoading = ref(false)
    
    // ===== PERSISTENCIA LOCAL DEL CARRITO =====
    const CART_STORAGE_KEY = 'kharis_cart_cache'
    const CART_COUNT_KEY = 'kharis_cart_count'
    
    const saveCartToLocal = (items, total, count) => {
      try {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify({ items, total, timestamp: Date.now() }))
        localStorage.setItem(CART_COUNT_KEY, String(count))
      } catch (e) {
        console.warn('No se pudo guardar carrito en localStorage:', e)
      }
    }
    
    const loadCartFromLocal = () => {
      try {
        const cached = localStorage.getItem(CART_STORAGE_KEY)
        const count = localStorage.getItem(CART_COUNT_KEY)
        if (cached) {
          const data = JSON.parse(cached)
          // Solo usar cache si tiene menos de 30 minutos
          if (Date.now() - data.timestamp < 30 * 60 * 1000) {
            return { items: data.items || [], total: data.total || 0, count: parseInt(count) || 0 }
          }
        }
      } catch (e) {
        console.warn('Error leyendo carrito de localStorage:', e)
      }
      return null
    }
    
    const clearCartLocal = () => {
      localStorage.removeItem(CART_STORAGE_KEY)
      localStorage.removeItem(CART_COUNT_KEY)
    }
    
    const openCartDrawer = async () => {
      showCartDrawer.value = true
      // Cerrar toast si está abierto para evitar superposición
      if (toast.value.show) {
        toast.value.show = false
      }
      // Bloquear scroll del body
      document.body.style.overflow = 'hidden'
      await loadCartItems()
    }
    
    const closeCartDrawer = () => {
      showCartDrawer.value = false
      // Restaurar scroll del body
      document.body.style.overflow = ''
    }
    
    // Actualizar cantidad de un producto
    const updateQuantity = async (productoId, nuevaCantidad) => {
      if (nuevaCantidad < 1) {
        // Si la cantidad es 0 o menos, eliminar el producto
        await removeFromCart(productoId)
        return
      }
      
      try {
        // Actualizar localmente primero para feedback inmediato
        const itemIndex = cartItems.value.findIndex(i => i.producto_id === productoId)
        if (itemIndex >= 0) {
          cartItems.value[itemIndex].cantidad = nuevaCantidad
          // Recalcular subtotal local
          const item = cartItems.value[itemIndex]
          item.subtotal = (item.precio_unitario || item.precio || 0) * nuevaCantidad
          
          // Actualizar cache
          const newCount = cartItems.value.reduce((sum, i) => sum + i.cantidad, 0)
          const newTotal = getCartSubtotal()
          saveCartToLocal(cartItems.value, newTotal, newCount)
          cartCount.value = newCount
        }
        
        // Sincronizar con backend si está logueado
        if (isLoggedIn.value) {
          await carritoService.actualizarCantidad(productoId, nuevaCantidad)
        }
      } catch (err) {
        console.error('Error actualizando cantidad:', err)
        // Recargar del servidor en caso de error
        await loadCartItems()
      }
    }
    
    const loadCartItems = async () => {
      cartLoading.value = true
      
      // Primero cargar desde cache local para respuesta inmediata
      const cachedCart = loadCartFromLocal()
      if (cachedCart && cachedCart.items.length > 0) {
        cartItems.value = cachedCart.items
        cartTotal.value = cachedCart.total
        cartCount.value = cachedCart.count || cachedCart.items.reduce((sum, item) => sum + item.cantidad, 0)
      }
      
      // Si no está logueado, solo usar cache
      if (!isLoggedIn.value) {
        cartLoading.value = false
        return
      }
      
      try {
        const data = await carritoService.getCarrito()
        
        // El carrito puede ser null si no existe todavía
        if (data && data.items && data.items.length > 0) {
          cartItems.value = data.items
          cartTotal.value = data.total_final || 0
          cartCount.value = data.items.reduce((sum, item) => sum + item.cantidad, 0)
          // Guardar en cache local
          saveCartToLocal(data.items, data.total_final || 0, cartCount.value)
        } else if (data === null) {
          // Backend dice que no hay carrito - pero mantener cache si existe
        } else {
          // Solo limpiar si realmente está vacío
          if (!cachedCart || cachedCart.items.length === 0) {
            cartItems.value = []
            cartTotal.value = 0
            cartCount.value = 0
          }
        }
      } catch (err) {
        // 404 es normal si no hay carrito creado
        if (err.response?.status === 404) {
          // No existe carrito, usando cache
        } else if (err.response?.status !== 401) {
          console.error('Error cargando carrito:', err)
        }
      } finally {
        cartLoading.value = false
      }
    }
    
    const removeFromCart = async (itemId) => {
      try {
        // Primero actualizar UI localmente para feedback inmediato
        const itemIndex = cartItems.value.findIndex(i => i.producto_id === itemId)
        if (itemIndex >= 0) {
          const itemCantidad = cartItems.value[itemIndex].cantidad || 1
          cartItems.value.splice(itemIndex, 1)
          
          // Actualizar contador restando la cantidad del producto eliminado
          cartCount.value = Math.max(0, cartCount.value - itemCantidad)
          
          // Actualizar cache local
          if (cartItems.value.length === 0) {
            clearCartLocal()
            cartTotal.value = 0
            cartCount.value = 0
          } else {
            const newTotal = getCartSubtotal()
            // Recalcular el count total sumando todas las cantidades
            const newCount = cartItems.value.reduce((sum, item) => sum + (item.cantidad || 1), 0)
            cartCount.value = newCount
            saveCartToLocal(cartItems.value, newTotal, newCount)
            cartTotal.value = newTotal
          }
        }
        
        // Sincronizar con backend si está logueado
        if (isLoggedIn.value) {
          try {
            await carritoService.eliminarProducto(itemId)
          } catch (backendErr) {
            // Si falla el backend pero ya actualizamos localmente, no pasa nada grave
            console.warn('Error sync eliminar con backend:', backendErr)
          }
        }
        
        showToast('Producto eliminado', 'info')
      } catch (err) {
        console.error('Error eliminando del carrito:', err)
        showToast('Error al eliminar producto', 'error')
        // Recargar para sincronizar
        await loadCartItems()
      }
    }
    
    const irACheckout = () => {
      // Desbloquear scroll ANTES de navegar
      document.body.style.overflow = ''
      document.body.style.paddingRight = ''
      showCartDrawer.value = false
      router.push('/checkout')
    }
    
    // User menu dropdown
    const showUserMenu = ref(false)
    const userMenuRef = ref(null)

    // ===== HERO CAROUSEL =====
    const currentSlide = ref(0)
    let slideInterval = null
    
    const heroSlides = ref([
      {
        image: '/imghanekalom.jpg',
        alt: 'Kanekalon - Fibras de cabello premium'
      },
      {
        image: '/img2.jpg',
        alt: 'Extensiones de cabello profesionales'
      },
      {
        image: 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=1920&q=80',
        alt: 'Extensiones de cabello premium'
      },
      {
        image: 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=1920&q=80',
        alt: 'Cabello largo natural'
      },
      {
        image: 'https://images.unsplash.com/photo-1580618672591-eb180b1a973f?w=1920&q=80',
        alt: 'Estilista profesional'
      },
      {
        image: 'https://images.unsplash.com/photo-1562322140-8baeececf3df?w=1920&q=80',
        alt: 'Salón de belleza'
      }
    ])

    const goToSlide = (index) => {
      currentSlide.value = index
      resetSlideInterval()
    }

    const nextSlide = () => {
      currentSlide.value = (currentSlide.value + 1) % heroSlides.value.length
    }

    const startSlideshow = () => {
      slideInterval = setInterval(nextSlide, 4000) // Cambio cada 4 segundos
    }

    const resetSlideInterval = () => {
      if (slideInterval) clearInterval(slideInterval)
      startSlideshow()
    }

    // Función para obtener sugerencias mientras escribe
    const getSuggestions = async () => {
      const query = searchQuery.value.trim().toLowerCase()
      if (query.length < 2) {
        searchSuggestions.value = []
        showSuggestions.value = false
        return
      }
      try {
        // Usar autocompletar para sugerencias rápidas
        const resp = await productosService.autocompletar(query)
        // productos_rapidos es un array de productos sugeridos
        searchSuggestions.value = resp?.productos_rapidos || []
        showSuggestions.value = (resp?.productos_rapidos && resp.productos_rapidos.length > 0)
      } catch (err) {
        searchSuggestions.value = []
        showSuggestions.value = false
      }
    }
    
    // Función para obtener el total de resultados de búsqueda
    const getTotalSearchResults = () => {
      const query = searchQuery.value.trim().toLowerCase()
      
      if (!query) return 0
      
      return productos.value.filter(producto => 
        producto.nombre.toLowerCase().includes(query) ||
        producto.descripcion?.toLowerCase().includes(query) ||
        producto.categoria?.nombre?.toLowerCase().includes(query)
      ).length
    }
    
    // Función para ejecutar la búsqueda
    const handleSearch = (selectedProduct = null) => {
      if (selectedProduct) {
        // Navegar al detalle del producto
        router.push(`/producto/${selectedProduct.id}`)
        searchQuery.value = ''
        showSuggestions.value = false
        mobileSearchOpen.value = false
      } else if (searchQuery.value.trim()) {
        // Navegar al catálogo con el query de búsqueda
        const query = searchQuery.value.trim()
        router.push({ path: '/catalogo', query: { q: query } })
        showSuggestions.value = false
        mobileSearchOpen.value = false
      }
    }
    
    // Función para scrollear a un producto específico
    const scrollToProducto = (productoId) => {
      const element = document.getElementById('productos')
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        
        setTimeout(() => {
          const productoCard = document.querySelector(`[data-producto-id="${productoId}"]`)
          if (productoCard) {
            productoCard.scrollIntoView({ behavior: 'smooth', block: 'center' })
            productoCard.classList.add('ring-2', 'ring-brand-600', 'ring-offset-4')
            setTimeout(() => {
              productoCard.classList.remove('ring-2', 'ring-brand-600', 'ring-offset-4')
            }, 2500)
          }
        }, 500)
      }
    }
    
    // Cerrar sugerencias al hacer clic fuera
    const handleClickOutsideSearch = (event) => {
      if (searchInputRef.value && !searchInputRef.value.contains(event.target) &&
          suggestionsRef.value && !suggestionsRef.value.contains(event.target)) {
        showSuggestions.value = false
      }
    }

    const irACategoria = (categoria) => {
      const nombre = categoria?.nombre
      if (nombre) {
        router.push({ path: '/catalogo', query: { categoria: nombre } })
      } else {
        router.push('/catalogo')
      }
    }

    const irADetalle = (productoId) => {
      router.push(`/producto/${productoId}`)
    }

    const formatPrice = (price) => {
      // Manejar casos de NaN, null, undefined
      const numPrice = Number(price)
      if (isNaN(numPrice) || numPrice === null || numPrice === undefined) {
        return '0'
      }
      return new Intl.NumberFormat('es-CO').format(numPrice)
    }
    
    // Helper para obtener precio del item del carrito
    const getItemPrice = (item) => {
      // Intentar diferentes propiedades donde puede estar el precio
      const price = item.subtotal || item.precio_unitario || item.precio || item.precio_final || 0
      const cantidad = item.cantidad || 1
      // Si el subtotal ya incluye la cantidad, usarlo directo
      if (item.subtotal) return item.subtotal
      // Si no, calcular
      return price * cantidad
    }
    
    // Helper para calcular el subtotal del carrito
    const getCartSubtotal = () => {
      if (!cartItems.value || cartItems.value.length === 0) return 0
      return cartItems.value.reduce((total, item) => {
        return total + getItemPrice(item)
      }, 0)
    }

    const handleScroll = () => {
      isScrolled.value = window.scrollY > 30
    }

    const scrollToTop = () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }

    const cargarCategorias = async () => {
      try {
        const data = await categoriasService.listarHome()
        categorias.value = data.categorias || data || []
      } catch (err) {
        console.error('Error cargando categorías:', err)
        categorias.value = []
      }
    }
    
    const cargarProductos = async () => {
      loading.value = true
      error.value = null
      try {
        // Obtener SOLO productos destacados (no mostrar otros)
        const data = await productosService.getDestacados()
        const productosData = data.productos || data.results || data || []
        
        productos.value = productosData
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
        // Obtener el precio correcto del producto
        const precioProducto = Number(producto.precio_monto || producto.precio_final || producto.precio || 0)
        
        // Actualizar carrito local inmediatamente (para todos los usuarios)
        const currentItems = [...cartItems.value]
        const existingIndex = currentItems.findIndex(i => i.producto_id === producto.id)
        if (existingIndex >= 0) {
          currentItems[existingIndex].cantidad++
          currentItems[existingIndex].subtotal = currentItems[existingIndex].cantidad * currentItems[existingIndex].precio_unitario
        } else {
          currentItems.push({
            producto_id: producto.id,
            nombre: producto.nombre,
            imagen_url: producto.imagen_url || producto.imagen_principal || producto.imagen || producto.imagenes?.[0] || null,
            precio_unitario: precioProducto,
            cantidad: 1,
            subtotal: precioProducto
          })
        }
        
        // Incrementar contador
        cartCount.value++
        
        // Calcular nuevo total y guardar en localStorage
        const newTotal = currentItems.reduce((sum, item) => sum + (item.subtotal || item.precio_unitario * item.cantidad), 0)
        saveCartToLocal(currentItems, newTotal, cartCount.value)
        cartItems.value = currentItems
        cartTotal.value = newTotal
        
        // Mostrar toast premium con info del producto
        showCartToast(producto)
        
        // Si está logueado, también sincronizar con el backend
        if (isLoggedIn.value) {
          try {
            await carritoService.agregarProducto(producto.id, 1)
            // Sincronizar con backend en segundo plano
            cargarResumenCarrito().catch(e => console.warn('Error sync resumen:', e))
          } catch (backendErr) {
            console.warn('No se pudo sincronizar con backend, carrito guardado localmente:', backendErr)
          }
        }
      } catch (err) {
        console.error('Error agregando al carrito:', err)
        showToast('Error al agregar el producto', 'error')
      }
    }
    
    const toggleFavorito = async (producto) => {
      // Solo para usuarios logueados - mostrar mensaje amigable
      if (!isLoggedIn.value) {
        showToast('Inicia sesión para guardar favoritos ❤️', 'info')
        setTimeout(() => router.push('/login'), 1500)
        return
      }
      
      try {
        await favoritosService.toggle(producto.id)
        showToast('Favorito actualizado', 'success')
      } catch (err) {
        console.error('Error toggling favorito:', err)
        showToast('Error al actualizar favorito', 'error')
      }
    }
    
    // User menu functions
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
    }
    
    const handleMenuAction = (action) => {
      showUserMenu.value = false
      
      if (!isLoggedIn.value) {
        // Si no está logueado, abrir modal de login
        router.push('/login')
        return
      }
      
      // Si está logueado, redirigir según acción
      switch(action) {
        case 'pedidos':
          router.push('/mi-cuenta')
          break
        case 'favoritos':
          router.push('/catalogo?favoritos=true')
          break
        case 'login':
          router.push('/login')
          break
      }
    }
    
    const cerrarSesion = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      // Limpiar cache del carrito
      clearCartLocal()
      currentUser.value = null
      isLoggedIn.value = false // Actualizar estado de login inmediatamente
      showUserMenu.value = false
      cartCount.value = 0
      cartItems.value = []
      cartTotal.value = 0
      showToast('Sesión cerrada correctamente', 'info')
    }
    
    // Cerrar menú al hacer clic fuera
    const handleClickOutside = (event) => {
      if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
        showUserMenu.value = false
      }
    }
    
    const handleImageError = (e) => {
      e.target.style.display = 'none'
      const parent = e.target.parentElement
      if (parent) {
        parent.innerHTML = `
          <div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-nude-100 to-nude-200">
            <svg class="w-24 h-24 text-nude-400" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
            </svg>
          </div>
        `
      }
    }

    const cargarResumenCarrito = async () => {
      // Primero cargar desde cache local para respuesta inmediata
      const cachedCart = loadCartFromLocal()
      if (cachedCart && cachedCart.count > 0) {
        cartCount.value = cachedCart.count
      }
      
      // Si no está logueado, no intentar cargar del servidor
      if (!isLoggedIn.value) {
        return
      }
      
      try {
        const resumen = await carritoService.getResumen()
        
        // El resumen puede ser null si no hay carrito
        if (resumen !== null) {
          const count = resumen?.total_items || 0
          cartCount.value = count
          // Actualizar el count en localStorage
          localStorage.setItem(CART_COUNT_KEY, String(count))
        } else {
          // Resumen es null - mantener cache si existe
        }
      } catch (err) {
        // Solo mostrar error si no es 401 (no autenticado) o 404 (no hay carrito)
        if (err.response?.status !== 401 && err.response?.status !== 404) {
          console.error('Error cargando resumen del carrito:', err)
        }
        // Mantener el valor del cache
      }
    }

    // Listener para actualizar usuario cuando inicia sesión
    const handleUserLoggedIn = (event) => {
      currentUser.value = event.detail
      isLoggedIn.value = true // Actualizar estado de login inmediatamente
      cargarResumenCarrito()
      showToast('¡Bienvenido/a ' + (event.detail?.nombre || '') + '!', 'success')
    }

    onMounted(() => {
      cargarCategorias()
      cargarProductos()
      cargarResumenCarrito()
      window.addEventListener('scroll', handleScroll)
      window.addEventListener('user-logged-in', handleUserLoggedIn)
      document.addEventListener('click', handleClickOutside)
      document.addEventListener('click', handleClickOutsideSearch)
      handleScroll()
      startSlideshow()
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
      window.removeEventListener('user-logged-in', handleUserLoggedIn)
      document.removeEventListener('click', handleClickOutside)
      document.removeEventListener('click', handleClickOutsideSearch)
      if (slideInterval) clearInterval(slideInterval)
    })

    return {
      productos,
      categorias,
      loading,
      error,
      cartCount,
      isScrolled,
      mobileMenuOpen,
      mobileSearchOpen,
      searchQuery,
      searchSuggestions,
      showSuggestions,
      searchInputRef,
      suggestionsRef,
      currentSlide,
      heroSlides,
      goToSlide,
      handleSearch,
      getSuggestions,
        getTotalSearchResults,
      scrollToProducto,
      handleSearch,
      scrollToTop,
      formatPrice,
      getItemPrice,
      getCartSubtotal,
      cargarProductos,
      irACategoria,
      irADetalle,
      agregarAlCarrito,
      toggleFavorito,
      toggleUserMenu,
      handleMenuAction,
      cerrarSesion,
      showUserMenu,
      userMenuRef,
      isLoggedIn,
      currentUser,
      userInitial,
      // Toast
      toast,
      showToast,
      showCartToast,
      // Cart Drawer
      showCartDrawer,
      cartItems,
      cartTotal,
      cartLoading,
      openCartDrawer,
      closeCartDrawer,
      removeFromCart,
      updateQuantity,
      irACheckout,
      handleImageError,
      getImageUrl
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

/* Hero Crossfade Transition - Suave y elegante */
.hero-crossfade-enter-active {
  transition: opacity 1.2s ease-in-out;
}
.hero-crossfade-leave-active {
  transition: opacity 1.2s ease-in-out;
  position: absolute;
}
.hero-crossfade-enter-from {
  opacity: 0;
}
.hero-crossfade-leave-to {
  opacity: 0;
}
.hero-crossfade-enter-to,
.hero-crossfade-leave-from {
  opacity: 1;
}
</style>
