<template>
  <div class="min-h-screen bg-[#FAFAFA]">

    <!-- ========================================
         TOP BAR - Carrusel de Anuncios (Solo Móvil)
         ======================================== -->
    <div class="sm:hidden bg-white h-7 flex items-center justify-center overflow-hidden">
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
         NAVBAR - Ultra-Minimal Luxury Glassmorphism
         ======================================== -->
    <header 
      :class="[
        'sticky sm:fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        isScrolled ? 'header-luxury-scrolled py-2' : 'header-luxury py-4'
      ]"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-8 lg:px-12">
        <!-- Mobile Header: Hamburger | Logo (center) | Search + Cart -->
        <div class="flex lg:hidden items-center justify-between">
          <!-- Left: Hamburger -->
          <button 
            @click="openMobileMenu"
            class="w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target hover:bg-black/5"
          >
            <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
            </svg>
          </button>

          <!-- Center: Logo Wordmark -->
          <a href="#" class="absolute left-1/2 -translate-x-1/2 flex items-center">
            <span class="text-[22px] font-semibold tracking-[0.18em] text-[#111] uppercase" style="font-family: 'Cormorant Garamond', 'Playfair Display', serif;">KHARIS</span>
          </a>

          <!-- Right: Search + Cart -->
          <div class="flex items-center gap-1">
            <button 
              @click="openMobileSearch"
              class="w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target hover:bg-black/5"
            >
              <svg class="w-[18px] h-[18px] text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </button>
            <button 
              class="relative w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target hover:bg-black/5"
              @click="openCartDrawer"
            >
              <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
              <span 
                v-if="cartCount > 0"
                class="absolute -top-0.5 -right-0.5 w-4 h-4 text-[9px] font-medium rounded-full flex items-center justify-center bg-text-dark text-white"
              >
                {{ cartCount }}
              </span>
            </button>
          </div>
        </div>

        <!-- Desktop Header: Logo | Search | Nav | Icons -->
        <div class="hidden lg:flex items-center justify-between">
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
          <div class="flex flex-1 max-w-xs mx-8">
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

          <!-- Navegación Desktop -->
          <nav class="flex items-center gap-7">
            <router-link to="/catalogo" class="nav-link-luxury">CATÁLOGO</router-link>
            <a href="#categorias" class="nav-link-luxury">CATEGORÍAS</a>
            <a href="#productos" class="nav-link-luxury">PRODUCTOS</a>
            <a href="#mayoreo" class="nav-link-luxury">MAYOREO</a>
            <a href="#testimonios" class="nav-link-luxury">RESEÑAS</a>
            <a href="#contacto" class="nav-link-luxury">CONTACTO</a>
          </nav>

          <!-- Acciones Desktop - Iconos -->
          <div class="flex items-center gap-1">
            
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
                <span v-if="isLoggedIn" class="text-xs font-medium" :class="isScrolled ? 'text-text-dark' : 'text-white drop-shadow-[0_1px_2px_rgba(0,0,0,0.5)]'">
                  {{ userInitial }}
                </span>
                <!-- Si no está logueado, mostrar icono -->
                <svg v-else class="w-4 h-4" :class="isScrolled ? 'text-text-dark' : 'text-white drop-shadow-[0_1px_2px_rgba(0,0,0,0.5)]'" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
              </button>
              
              <!-- Dropdown Menu - Bottom Sheet en móvil, Dropdown en desktop -->
              <Teleport to="body">
                <!-- Backdrop oscuro (solo móvil, visible cuando abre) -->
                <transition
                  enter-active-class="transition duration-200 ease-out"
                  enter-from-class="opacity-0"
                  enter-to-class="opacity-100"
                  leave-active-class="transition duration-150 ease-in"
                  leave-from-class="opacity-100"
                  leave-to-class="opacity-0"
                >
                  <div 
                    v-if="showUserMenu"
                    class="sm:hidden fixed inset-0 bg-black/50"
                    style="z-index: 99998;"
                    @click="showUserMenu = false"
                  ></div>
                </transition>

                <!-- Desktop dropdown (sm+) -->
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
                    class="hidden sm:block fixed w-52 bg-white rounded-lg shadow-[0_16px_48px_rgb(0,0,0,0.25)] py-2 border border-black/10"
                    :style="{
                      top: (userMenuRef?.getBoundingClientRect().bottom || 0) + 12 + 'px',
                      left: ((userMenuRef?.getBoundingClientRect().right || 0) - 208) + 'px',
                      zIndex: 99999
                    }"
                  >
                    <template v-if="isLoggedIn">
                      <div class="px-4 py-3 border-b border-black/10 bg-nude-50/30">
                        <p class="text-xs text-text-medium mb-0.5">Hola,</p>
                        <p class="text-sm text-text-dark font-semibold truncate">{{ currentUser?.nombre || currentUser?.email }}</p>
                      </div>
                      <router-link to="/mi-cuenta" class="flex items-center gap-3 px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors" @click="showUserMenu = false">
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>
                        Mi Cuenta
                      </router-link>
                      <button @click="handleMenuAction('pedidos')" class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors">
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
                        Mis Pedidos
                      </button>
                      <button @click="handleMenuAction('favoritos')" class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors border-b border-black/10">
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" /></svg>
                        Ver Favoritos
                      </button>
                      <button @click="cerrarSesion" class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors mt-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" /></svg>
                        Cerrar Sesión
                      </button>
                    </template>
                    <template v-else>
                      <button @click="handleMenuAction('login')" class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors">
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" /></svg>
                        Inicia sesión
                      </button>
                      <button @click="handleMenuAction('pedidos')" class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors">
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
                        Mi pedido
                      </button>
                      <button @click="handleMenuAction('favoritos')" class="flex items-center gap-3 w-full text-left px-4 py-2.5 text-sm text-text-dark font-medium hover:bg-nude-100 transition-colors">
                        <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" /></svg>
                        Ver Favoritos
                      </button>
                    </template>
                  </div>
                </transition>

                <!-- Mobile Bottom Sheet (< sm) -->
                <transition
                  enter-active-class="transition duration-300 ease-out"
                  enter-from-class="translate-y-full"
                  enter-to-class="translate-y-0"
                  leave-active-class="transition duration-200 ease-in"
                  leave-from-class="translate-y-0"
                  leave-to-class="translate-y-full"
                >
                  <div 
                    v-if="showUserMenu"
                    class="sm:hidden fixed bottom-0 left-0 right-0 bg-white rounded-t-[20px] shadow-[0_-8px_30px_rgba(0,0,0,0.12)] pb-safe"
                    style="z-index: 99999;"
                  >
                    <!-- Drag Handle -->
                    <div class="flex justify-center pt-3 pb-2" @click="showUserMenu = false">
                      <div class="w-10 h-1 bg-text-dark/15 rounded-full"></div>
                    </div>

                    <!-- Header si está logueado -->
                    <div v-if="isLoggedIn" class="px-5 pb-3 border-b border-black/5">
                      <p class="text-xs text-text-light">Hola,</p>
                      <p class="text-base text-text-dark font-semibold truncate">{{ currentUser?.nombre || currentUser?.email }}</p>
                    </div>

                    <!-- Items -->
                    <div class="py-1">
                      <template v-if="isLoggedIn">
                        <router-link to="/mi-cuenta" class="flex items-center gap-4 w-full px-5 py-4 text-[15px] text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/5" @click="showUserMenu = false">
                          <div class="w-9 h-9 bg-nude-100 rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-[18px] h-[18px] text-text-dark/70" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>
                          </div>
                          Mi Cuenta
                        </router-link>
                        <button @click="handleMenuAction('pedidos')" class="flex items-center gap-4 w-full text-left px-5 py-4 text-[15px] text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/5">
                          <div class="w-9 h-9 bg-nude-100 rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-[18px] h-[18px] text-text-dark/70" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
                          </div>
                          Mis Pedidos
                        </button>
                        <button @click="handleMenuAction('favoritos')" class="flex items-center gap-4 w-full text-left px-5 py-4 text-[15px] text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/5">
                          <div class="w-9 h-9 bg-brand-50 rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-[18px] h-[18px] text-brand-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" /></svg>
                          </div>
                          Ver Favoritos
                        </button>
                        <button @click="cerrarSesion" class="flex items-center gap-4 w-full text-left px-5 py-4 text-[15px] text-red-500 font-medium active:bg-red-50 transition-colors">
                          <div class="w-9 h-9 bg-red-50 rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-[18px] h-[18px] text-red-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" /></svg>
                          </div>
                          Cerrar Sesión
                        </button>
                      </template>
                      <template v-else>
                        <button @click="handleMenuAction('login')" class="flex items-center gap-4 w-full text-left px-5 py-4 text-[15px] text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/5">
                          <div class="w-9 h-9 bg-brand-50 rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-[18px] h-[18px] text-brand-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" /></svg>
                          </div>
                          Inicia sesión
                        </button>
                        <button @click="handleMenuAction('pedidos')" class="flex items-center gap-4 w-full text-left px-5 py-4 text-[15px] text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/5">
                          <div class="w-9 h-9 bg-nude-100 rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-[18px] h-[18px] text-text-dark/70" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
                          </div>
                          Mi pedido
                        </button>
                        <button @click="handleMenuAction('favoritos')" class="flex items-center gap-4 w-full text-left px-5 py-4 text-[15px] text-text-dark font-medium active:bg-nude-50 transition-colors">
                          <div class="w-9 h-9 bg-brand-50 rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-[18px] h-[18px] text-brand-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" /></svg>
                          </div>
                          Ver Favoritos
                        </button>
                      </template>
                    </div>

                    <!-- Safe area bottom padding -->
                    <div class="h-6"></div>
                  </div>
                </transition>
              </Teleport>
            </div>
            
            <!-- Carrito Desktop -->
            <button 
              :class="[
                'relative w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target',
                isScrolled ? 'hover:bg-black/5' : 'hover:bg-white/10'
              ]"
              @click="openCartDrawer"
            >
              <svg :class="['w-4 h-4', isScrolled ? 'text-text-dark' : 'text-white drop-shadow-[0_1px_2px_rgba(0,0,0,0.5)]']" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
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
          </div>
        </div>

        <!-- Mobile Search Overlay (Full-Screen) - via Teleport -->
        <Teleport to="body">
          <transition
            enter-active-class="search-overlay-enter-active"
            enter-from-class="search-overlay-enter-from"
            enter-to-class="search-overlay-enter-to"
            leave-active-class="search-overlay-leave-active"
            leave-from-class="search-overlay-leave-from"
            leave-to-class="search-overlay-leave-to"
          >
            <div v-if="mobileSearchOpen" class="fixed inset-0 z-[9998] bg-white lg:hidden search-overlay-mobile">
              
              <!-- Header del Search overlay -->
              <div class="flex items-center gap-3 px-4 py-3 border-b border-black/5">
                <!-- Botón Cerrar (flecha atrás) -->
                <button 
                  @click="closeMobileSearch"
                  class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-nude-100 active:bg-nude-200 transition-colors flex-shrink-0"
                  aria-label="Cerrar búsqueda"
                >
                  <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
                  </svg>
                </button>

                <!-- Input de búsqueda -->
                <div class="flex-1 relative">
                  <input 
                    ref="mobileSearchInputRef"
                    type="text"
                    v-model="searchQuery"
                    @input="getSuggestions"
                    @keyup.enter="handleSearch()"
                    @focus="getSuggestions"
                    placeholder="Buscar..."
                    class="w-full py-2.5 px-4 bg-[#F5F5F5] rounded-full text-sm text-text-dark placeholder-text-light/50 focus:outline-none focus:bg-[#EFEFEF] transition-colors"
                  />
                </div>

                <!-- Botón limpiar -->
                <button 
                  v-if="searchQuery.length > 0"
                  @click="searchQuery = ''; searchSuggestions = []; showSuggestions = false"
                  class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-nude-100 transition-colors flex-shrink-0"
                >
                  <svg class="w-4 h-4 text-text-light" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Resultados / Sugerencias -->
              <div class="flex-1 overflow-y-auto">
                
                <!-- Estado vacío: cuando no hay query -->
                <div v-if="!searchQuery.trim()" class="flex flex-col items-center justify-center pt-20 px-6">
                  <svg class="w-12 h-12 text-text-light/30 mb-4" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                  </svg>
                  <p class="text-sm text-text-light/60 text-center">Busca extensiones, accesorios y más</p>
                </div>

                <!-- Lista de sugerencias -->
                <div v-else-if="showSuggestions && searchSuggestions.length > 0" class="divide-y divide-black/5">
                  <button
                    v-for="producto in searchSuggestions"
                    :key="producto.id"
                    @click="handleSearch(producto)"
                    class="w-full px-5 py-3.5 flex items-center gap-4 text-left active:bg-nude-50 transition-colors"
                  >
                    <div class="w-12 h-12 rounded-xl overflow-hidden flex-shrink-0 bg-nude-50 ring-1 ring-nude-200/30">
                      <img 
                        v-if="producto.imagen_principal || producto.imagen_url || producto.imagen"
                        :src="getImageUrl(producto.imagen_principal || producto.imagen_url || producto.imagen)"
                        :alt="producto.nombre"
                        class="w-full h-full object-cover"
                      />
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-text-dark truncate">
                        {{ producto.nombre }}
                      </p>
                      <p class="text-xs font-semibold text-brand-600 mt-0.5">
                        {{ formatPrice(getItemPrice(producto)) }}
                      </p>
                    </div>
                    <svg class="w-4 h-4 text-text-light/30 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                  </button>
                  
                  <!-- Ver todos -->
                  <button
                    @click="handleSearch()"
                    class="w-full px-5 py-4 flex items-center justify-center gap-2 text-sm font-medium text-brand-600 active:bg-nude-50 transition-colors"
                  >
                    Ver todos los resultados
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                  </button>
                </div>

                <!-- Sin resultados -->
                <div v-else-if="searchQuery.trim().length >= 2 && !showSuggestions" class="flex flex-col items-center justify-center pt-20 px-6">
                  <p class="text-sm text-text-light/60 text-center">No encontramos resultados para "{{ searchQuery }}"</p>
                  <p class="text-xs text-text-light/40 mt-1">Intenta con otra palabra</p>
                </div>
              </div>

            </div>
          </transition>
        </Teleport>

        <!-- Mobile Menu Off-Canvas Sidebar - via Teleport -->
        <Teleport to="body">
          <!-- Backdrop -->
          <transition
            enter-active-class="transition-opacity duration-300 ease-out"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition-opacity duration-200 ease-in"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div 
              v-if="mobileMenuOpen" 
              class="fixed inset-0 z-[9996] bg-black/50 lg:hidden"
              @click="closeMobileMenu"
            ></div>
          </transition>

          <!-- Sidebar Panel -->
          <transition
            enter-active-class="sidebar-enter-active"
            enter-from-class="sidebar-enter-from"
            enter-to-class="sidebar-enter-to"
            leave-active-class="sidebar-leave-active"
            leave-from-class="sidebar-leave-from"
            leave-to-class="sidebar-leave-to"
          >
            <nav v-if="mobileMenuOpen" class="fixed top-0 left-0 z-[9997] w-[52%] max-w-[220px] h-full bg-white lg:hidden flex flex-col sidebar-mobile">
              
              <!-- Header del Sidebar -->
              <div class="flex items-center justify-between px-4 py-3.5 border-b border-black/5">
                <img 
                  src="/logo-kharis.png" 
                  alt="Kharis" 
                  class="h-8 w-auto object-contain"
                />
                <button 
                  @click="closeMobileMenu"
                  class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-nude-100 active:bg-nude-200 transition-colors"
                  aria-label="Cerrar menú"
                >
                  <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Lista de enlaces -->
              <div class="flex-1 overflow-y-auto py-2">
                <!-- Mi Cuenta / Iniciar Sesión -->
                <button 
                  v-if="isLoggedIn"
                  @click="closeMobileMenu(); $router.push('/mi-cuenta')"
                  class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04] w-full text-left"
                >
                  <div class="w-6 h-6 rounded-full bg-brand-50 flex items-center justify-center flex-shrink-0">
                    <span class="text-[10px] font-semibold text-brand-600">{{ userInitial }}</span>
                  </div>
                  Mi Cuenta
                </button>
                <button 
                  v-else
                  @click="closeMobileMenu(); handleMenuAction('login')"
                  class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04] w-full text-left"
                >
                  <svg class="w-4 h-4 text-brand-600 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                  </svg>
                  Iniciar Sesión
                </button>
                <router-link 
                  to="/catalogo" 
                  @click="closeMobileMenu" 
                  class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
                >
                  <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
                  </svg>
                  Catálogo
                </router-link>
                <a 
                  href="#categorias" 
                  @click="closeMobileMenu" 
                  class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
                >
                  <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6z" />
                  </svg>
                  Categorías
                </a>
                <a 
                  href="#productos" 
                  @click="closeMobileMenu" 
                  class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
                >
                  <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                  </svg>
                  Productos
                </a>
                <a 
                  href="#mayoreo" 
                  @click="closeMobileMenu" 
                  class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
                >
                  <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 003.75-.615A2.993 2.993 0 009.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 002.25 1.016c.896 0 1.7-.393 2.25-1.016A3.001 3.001 0 0021 9.349m-18 0a2.998 2.998 0 00.832-2.078c.1-.695.564-1.267 1.168-1.521L7.5 4.5h9l2.5 1.25c.604.254 1.067.826 1.168 1.521A2.998 2.998 0 0021 9.35" />
                  </svg>
                  Mayoreo
                </a>
                <a 
                  href="#testimonios" 
                  @click="closeMobileMenu" 
                  class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
                >
                  <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
                  </svg>
                  Reseñas
                </a>
                <a 
                  href="#contacto" 
                  @click="closeMobileMenu" 
                  class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors"
                >
                  <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                  </svg>
                  Contacto
                </a>
              </div>

              <!-- Footer del Sidebar -->
              <div class="px-4 py-4 border-t border-black/5">
                <p class="text-[9px] tracking-[0.12em] uppercase text-text-light/40 mb-2 font-medium">Síguenos</p>
                <div class="flex items-center gap-2">
                  <a href="https://www.instagram.com/kharisdistribuidora" target="_blank" class="w-7 h-7 rounded-full bg-nude-50 flex items-center justify-center active:bg-nude-200 transition-colors">
                    <svg class="w-3.5 h-3.5 text-text-dark/50" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
                    </svg>
                  </a>
                  <a href="https://wa.me/18298776031" target="_blank" class="w-7 h-7 rounded-full bg-nude-50 flex items-center justify-center active:bg-nude-200 transition-colors">
                    <svg class="w-3.5 h-3.5 text-text-dark/50" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                    </svg>
                  </a>
                  <a href="https://www.tiktok.com/@kharisdistribuidora" target="_blank" class="w-7 h-7 rounded-full bg-nude-50 flex items-center justify-center active:bg-nude-200 transition-colors">
                    <svg class="w-3.5 h-3.5 text-text-dark/50" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13.2a8.16 8.16 0 005.58 2.17V12a4.85 4.85 0 01-5.58-2.17V2h3.45a4.83 4.83 0 003.77 4.25v3.44h-1.64z"/>
                    </svg>
                  </a>
                </div>
                <p class="text-[9px] text-text-light/35 mt-3">&copy; 2026 Kharis Distribuidora</p>
              </div>

            </nav>
          </transition>
        </Teleport>
      </div>
    </header>

    <!-- ========================================
         HERO SECTION - Full Screen High Impact
         ======================================== -->
    <section class="relative sm:mt-0 h-[75svh] min-h-[500px] sm:h-auto sm:min-h-screen flex items-center overflow-hidden">
      
      <!-- ===== BACKGROUND CAROUSEL ===== -->
      <div class="absolute inset-0 z-0">
        <!-- Carousel Images/Videos -->
        <transition-group name="hero-slide" tag="div" class="absolute inset-0">
          <template v-for="(slide, index) in activeHeroSlides" :key="index">
            <!-- Video Slide con overlay sutil -->
            <div
              v-if="slide.video && currentSlide === index"
              v-show="currentSlide === index"
              class="absolute inset-0"
            >
              <video
                :src="slide.video"
                :alt="slide.alt"
                class="absolute inset-0 w-full h-full object-cover object-center"
                autoplay
                muted
                loop
                playsinline
                preload="auto"
              ></video>
              <!-- Overlay sutil para suavizar calidad + gradiente inferior -->
              <div class="absolute inset-0 bg-black/20"></div>
              <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent"></div>
            </div>
            <!-- Image Slide -->
            <img 
              v-else-if="slide.image"
              v-show="currentSlide === index"
              :src="slide.image" 
              :alt="slide.alt" 
              class="absolute inset-0 w-full h-full object-cover object-top sm:object-top hero-image-mobile"
            />
          </template>
        </transition-group>
        <!-- Gradients for readability - Desktop -->
        <div class="hidden sm:block absolute inset-0 bg-gradient-to-r from-black/80 via-black/40 to-transparent z-10"></div>
        <div class="hidden sm:block absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/20 z-10"></div>
        
        <!-- Overlay Retail Móvil - Solo gradiente inferior, imagen limpia arriba -->
        <div class="sm:hidden absolute inset-0 hero-overlay-mobile z-10"></div>
        
        <!-- Carousel Indicators - Desktop only (mobile dots are in content block) -->
        <div class="hidden sm:flex absolute bottom-8 left-1/2 -translate-x-1/2 z-20 items-center gap-2">
          <button 
            v-for="(slide, index) in activeHeroSlides" 
            :key="index"
            @click="goToSlide(index)"
            :class="[
              'rounded-full transition-all duration-300',
              currentSlide === index 
                ? 'bg-white w-6 h-2' 
                : 'bg-white/40 hover:bg-white/60 w-2 h-2'
            ]"
          ></button>
        </div>
      </div>

      <!-- ===== CONTENT ===== -->
      <div class="relative z-10 w-full h-full sm:min-h-screen flex flex-col justify-end sm:justify-center max-w-7xl mx-auto px-5 sm:px-8 lg:px-12 pb-4 sm:pb-0 sm:pt-20">
        
        <!-- Desktop content block (hidden on mobile) -->
        <div class="hidden sm:block max-w-3xl text-left">
          
          <!-- Badge -->
          <div class="inline-flex items-center gap-2.5 bg-white/10 backdrop-blur-md border border-white/20 rounded-full px-5 py-2.5 mb-8 animate-fade-in-up">
            <span class="w-2 h-2 bg-gold-400 rounded-full animate-pulse"></span>
            <span class="text-sm font-medium text-white tracking-wide uppercase">Distribuidora Mayorista desde 2023</span>
          </div>

          <!-- Title Desktop -->
          <h1 class="font-luxury text-white leading-[1.05] mb-8 drop-shadow-2xl animate-fade-in-up delay-100">
            <span class="block text-3xl lg:text-4xl font-light tracking-wide mb-2">Tu Socio Experto en</span>
            <span class="block text-6xl lg:text-7xl xl:text-8xl text-transparent bg-clip-text bg-gradient-to-r from-white via-gold-200 to-gold-400 font-bold italic leading-[1.1]">
              Belleza Profesional
            </span>
          </h1>

          <!-- Subtitle Desktop -->
          <p class="text-lg lg:text-xl text-white/90 leading-relaxed max-w-xl font-light animate-fade-in-up delay-200 tracking-wide">
            Extensiones 100% naturales, pelucas premium y accesorios de clase mundial.
          </p>
          
          <!-- CTAs Desktop -->
          <div class="flex flex-row gap-5 mt-12 mb-16 animate-fade-in-up delay-300">
            <router-link 
              to="/catalogo" 
              class="inline-flex items-center justify-center px-8 py-4 bg-white text-gray-900 font-semibold text-base rounded-full shadow-lg hover:shadow-xl hover:bg-gray-100 transition-all duration-300 touch-target"
            >
              Ver Catálogo
              <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
              </svg>
            </router-link>
            
            <a 
              href="#mayoreo" 
              class="inline-flex items-center justify-center px-8 py-4 bg-transparent border border-white/50 text-white font-medium text-base rounded-full hover:bg-white hover:text-gray-900 transition-all duration-300 backdrop-blur-sm touch-target"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                 <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 003.75-.615A2.993 2.993 0 009.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 002.25 1.016c.896 0 1.7-.393 2.25-1.016a3.001 3.001 0 003.75.614m-16.5 0a3.004 3.004 0 01-.621-4.72L4.318 3.44A1.5 1.5 0 015.378 3h13.243a1.5 1.5 0 011.06.44l1.19 1.189a3 3 0 01-.621 4.72m-13.5 8.65h3.75a.75.75 0 00.75-.75V13.5a.75.75 0 00-.75-.75H6.75a.75.75 0 00-.75.75v3.75c0 .415.336.75.75.75z" />
              </svg>
              Portal Mayorista
            </a>
          </div>
        </div>

        <!-- Mobile content block - Bottom aligned, editorial clean -->
        <div class="sm:hidden text-left">
          <!-- Title Móvil - Editorial Serif Look -->
          <h1 class="text-white leading-[1.08] mb-3.5 hero-animate-title">
            <span class="block text-[1.85rem] font-bold tracking-tight" style="font-family: 'Inter', sans-serif;">Cabello 100%</span>
            <span class="block text-[2.1rem] font-bold tracking-tight" style="font-family: 'Inter', sans-serif;">Natural</span>
            <span class="block text-[2.4rem] italic tracking-wide text-white/95" style="font-family: 'Cormorant Garamond', 'Playfair Display', serif; font-weight: 500;">Premium</span>
          </h1>
          
          <!-- CTAs Móvil - Side by side, compactos -->
          <div class="flex flex-row gap-2.5 hero-animate-cta">
            <router-link 
              to="/catalogo" 
              class="btn-hero-mobile btn-hero-primary flex-1 inline-flex items-center justify-center px-4 py-3 text-gray-900 font-semibold text-[13px] rounded-[4px] tracking-wide touch-target"
            >
              VER CATÁLOGO
            </router-link>
            
            <a 
              href="#mayoreo" 
              class="btn-hero-mobile btn-hero-secondary flex-1 inline-flex items-center justify-center px-4 py-3 text-white font-medium text-[13px] rounded-[4px] tracking-wide touch-target"
            >
              MAYORISTA
            </a>
          </div>

          <!-- Mobile Carousel Dots -->
          <div class="flex justify-center items-center gap-1.5 mt-4">
            <button 
              v-for="(slide, index) in activeHeroSlides" 
              :key="'mob-dot-'+index"
              @click="goToSlide(index)"
              :class="[
                'rounded-full transition-all duration-300',
                currentSlide === index 
                  ? 'bg-white w-5 h-[5px]' 
                  : 'bg-white/40 w-[5px] h-[5px]'
              ]"
            ></button>
          </div>
        </div>
      </div>

    </section>

    <!-- ========================================
         TRUST BAR - Premium Editorial Ribbon (3 en móvil, 4 en desktop)
         ======================================== -->
    <section class="trust-ribbon-premium relative overflow-hidden py-0 sm:py-0">
      
      <!-- Mobile: Banda horizontal dark retail-style -->
      <div class="sm:hidden bg-[#1a1a1a] py-3.5">
        <div class="flex items-center justify-evenly px-3">
          <!-- Envío Gratis -->
          <div class="flex items-center gap-2">
            <svg class="w-[18px] h-[18px] text-white/70 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
            </svg>
            <span class="text-[11px] font-bold tracking-wider uppercase text-white leading-tight">Envío Gratis</span>
          </div>
          <!-- Divider -->
          <div class="w-px h-4 bg-white/20"></div>
          <!-- Pago Seguro -->
          <div class="flex items-center gap-2">
            <svg class="w-[18px] h-[18px] text-white/70 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
            </svg>
            <span class="text-[11px] font-bold tracking-wider uppercase text-white leading-tight">Pago Seguro</span>
          </div>
          <!-- Divider -->
          <div class="w-px h-4 bg-white/20"></div>
          <!-- Asesoría VIP -->
          <div class="flex items-center gap-2">
            <svg class="w-[18px] h-[18px] text-white/70 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
            </svg>
            <span class="text-[11px] font-bold tracking-wider uppercase text-white leading-tight">Asesoría VIP</span>
          </div>
        </div>
      </div>

      <!-- Desktop: Layout original con círculos -->
      <div class="hidden sm:block relative max-w-6xl mx-auto px-4">
        <div class="flex flex-wrap lg:flex-nowrap items-stretch justify-center gap-8">
          
          <!-- Item 1: Envíos VIP -->
          <div class="trust-item-premium group py-7 lg:py-9 px-3 lg:px-8 flex flex-col items-center text-center relative">
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-16 h-16 lg:w-20 lg:h-20 rounded-full bg-gradient-to-br from-white to-gray-50 shadow-lg flex items-center justify-center mb-4 group-hover:shadow-xl group-hover:scale-110 transition-all duration-300">
                <svg class="w-7 h-7 lg:w-8 lg:h-8 text-[#8B7355] group-hover:text-[#D81B60] transition-colors duration-300" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                </svg>
              </div>
              <h4 class="text-xs lg:text-sm font-semibold tracking-[0.15em] uppercase text-[#1a1a1a] mb-1">Envío Gratis</h4>
              <p class="text-xs lg:text-sm text-[#8B7355] font-light leading-tight">Desde $350.000</p>
            </div>
          </div>

          <!-- Item 2: Calidad Premium -->
          <div class="trust-item-premium group py-7 lg:py-9 px-3 lg:px-8 flex flex-col items-center text-center relative">
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-16 h-16 lg:w-20 lg:h-20 rounded-full bg-gradient-to-br from-white to-gray-50 shadow-lg flex items-center justify-center mb-4 group-hover:shadow-xl group-hover:scale-110 transition-all duration-300">
                <svg class="w-7 h-7 lg:w-8 lg:h-8 text-[#8B7355] group-hover:text-[#D81B60] transition-colors duration-300" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
                </svg>
              </div>
              <h4 class="text-xs lg:text-sm font-semibold tracking-[0.15em] uppercase text-[#1a1a1a] mb-1">Calidad Premium</h4>
              <p class="text-xs lg:text-sm text-[#8B7355] font-light leading-tight">Productos garantizados</p>
            </div>
          </div>

          <!-- Item 3: Pago Seguro -->
          <div class="trust-item-premium group py-7 lg:py-9 px-3 lg:px-8 flex flex-col items-center text-center relative">
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-16 h-16 lg:w-20 lg:h-20 rounded-full bg-gradient-to-br from-white to-gray-50 shadow-lg flex items-center justify-center mb-4 group-hover:shadow-xl group-hover:scale-110 transition-all duration-300">
                <svg class="w-7 h-7 lg:w-8 lg:h-8 text-[#8B7355] group-hover:text-[#D81B60] transition-colors duration-300" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                </svg>
              </div>
              <h4 class="text-xs lg:text-sm font-semibold tracking-[0.15em] uppercase text-[#1a1a1a] mb-1">Pago Seguro</h4>
              <p class="text-xs lg:text-sm text-[#8B7355] font-light leading-tight">SSL 256-bit</p>
            </div>
          </div>

          <!-- Item 4: Asesoría VIP -->
          <div class="trust-item-premium group py-7 lg:py-9 px-3 lg:px-8 flex flex-col items-center text-center relative">
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-16 h-16 lg:w-20 lg:h-20 rounded-full bg-gradient-to-br from-white to-gray-50 shadow-lg flex items-center justify-center mb-4 group-hover:shadow-xl group-hover:scale-110 transition-all duration-300">
                <svg class="w-7 h-7 lg:w-8 lg:h-8 text-[#8B7355] group-hover:text-[#D81B60] transition-colors duration-300" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                </svg>
              </div>
              <h4 class="text-xs lg:text-sm font-semibold tracking-[0.15em] uppercase text-[#1a1a1a] mb-1">Asesoría VIP</h4>
              <p class="text-xs lg:text-sm text-[#8B7355] font-light leading-tight">Personalizada</p>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ========================================
         CATEGORÍAS - Bento Box Grid (Smart Mobile Grid)
         ======================================== -->
    <section id="categorias" class="py-5 sm:py-12 lg:py-28 bg-[#FAFAFA]">
      <div class="max-w-7xl mx-auto px-3 sm:px-8 lg:px-12">
        <!-- Section Header - Left-aligned mobile, centered desktop -->
        <div class="text-left sm:text-center mb-3 sm:mb-10 lg:mb-14">
          <span class="hidden sm:inline-block text-brand-600 font-medium text-xs sm:text-sm tracking-widest uppercase mb-2 sm:mb-4">Nuestro Catálogo</span>
          <h2 class="text-[17px] font-bold uppercase tracking-wide sm:tracking-normal sm:normal-case sm:font-luxury sm:text-4xl lg:text-5xl text-text-dark mb-0 sm:mb-4">
            Categorías <em class="not-italic text-brand-600">Exclusivas</em>
          </h2>
          <p class="hidden sm:block text-text-medium max-w-xl mx-auto text-sm lg:text-base">
            Productos seleccionados para profesionales de la belleza que buscan calidad excepcional
          </p>
        </div>

        <!-- Categories: Horizontal Carousel (mobile) / Bento Grid (desktop) -->
        <div class="relative">
          <!-- Scroll arrow indicator (mobile only, Mercado Libre style) -->
          <button 
            v-if="categorias.length > 1"
            @click="scrollCategorias"
            class="cat-scroll-arrow md:hidden absolute right-0 top-1/2 -translate-y-1/2 z-20 w-9 h-9 bg-white shadow-lg flex items-center justify-center transition-opacity duration-500"
            :class="{ 'opacity-0 pointer-events-none': catScrolled }"
            aria-label="Deslizar categorías"
          >
            <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </button>

        <div ref="categoriasCarouselRef" class="categories-carousel md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-5 lg:gap-6" @scroll="onCatScroll">
          <div 
            v-for="(categoria, index) in categorias" 
            :key="categoria.id"
            :class="[
              'group cursor-pointer category-card-item',
              // Mobile: carousel card sizing (handled via CSS)
              // Desktop grid logic
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
                'relative cat-card-inner bento-item shadow-soft hover-lift overflow-hidden',
                // Mobile: zero radius via CSS override; Desktop: rounded
                'rounded-none md:rounded-2xl lg:rounded-3xl',
                // Mobile: tall uniform height for carousel impact
                'h-72 sm:h-80',
                // Desktop: adaptive heights
                categoria.prioridad === 1 && index === 0 ? 'md:h-80 lg:h-96' : 'md:h-64 lg:h-80',
                categorias.length === 1 ? 'md:h-96 lg:h-[500px]' :
                categorias.length === 2 ? 'md:h-80 lg:h-96' :
                categorias.length === 3 && categoria.prioridad === 1 ? 'md:h-80 lg:h-full lg:min-h-[400px]' :
                categorias.length === 3 && categoria.prioridad !== 1 ? 'md:h-64 lg:h-full lg:min-h-[200px]' : ''
              ]"
            >
              <img 
                :src="categoria.imagen || 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=1000&h=800&fit=crop&q=85'" 
                :alt="categoria.nombre" 
                class="absolute inset-0 w-full h-full object-cover img-zoom"
              >
              <!-- Overlay: hard gradient on mobile, soft on desktop -->
              <div class="absolute inset-0 cat-overlay-sharp sm:bento-overlay"></div>
              <div 
                :class="[
                  'absolute bottom-0 left-0 right-0',
                  'p-4 sm:p-6 lg:p-8'
                ]"
              >
                <!-- Badge "MÁS VENDIDO" - solid label style on mobile -->
                <span 
                  v-if="categoria.prioridad === 1 && categoria.orden === 1" 
                  class="cat-badge-sharp inline-block bg-black text-white text-[10px] sm:text-xs font-bold uppercase tracking-wider px-2.5 py-1 sm:px-3 sm:py-1 rounded-none sm:rounded-full mb-2 sm:mb-3"
                >
                  MÁS VENDIDO
                </span>
                
                <!-- Title: Bold sans-serif uppercase on mobile, luxury on desktop -->
                <h3 
                  class="cat-title-sharp text-white leading-tight text-lg sm:text-2xl lg:text-3xl font-black uppercase sm:normal-case sm:font-luxury mb-1 sm:mb-2"
                >
                  {{ categoria.nombre }}
                </h3>
                
                <!-- Descripción - OCULTA en móvil para todas las tarjetas -->
                <p 
                  v-if="categoria.prioridad === 1 && index === 0"
                  class="hidden sm:block text-white/80 mb-2 sm:mb-4 text-sm sm:text-base max-w-md"
                >
                  {{ categoria.descripcion }}
                </p>
                <p 
                  v-else
                  class="hidden sm:block text-white/80 mb-4 text-sm"
                >
                  {{ categoria.descripcion_corta || categoria.descripcion }}
                </p>
                
                <!-- CTA: sharp label style on mobile -->
                <span 
                  class="cat-cta-sharp inline-flex items-center gap-1.5 sm:gap-2 text-white font-bold text-xs sm:text-sm uppercase tracking-wider sm:tracking-normal sm:normal-case sm:font-medium transition-all group-hover:gap-4 mt-1 sm:mt-0"
                >
                  VER COLECCIÓN
                  <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>
        </div>
      </div>
    </section>

    <!-- ========================================
         PRODUCTOS DESTACADOS
         ======================================== -->
    <section id="productos" class="py-10 sm:py-20 lg:py-28 bg-gradient-to-b from-nude-100/50 to-[#FAFAFA]">
      <div class="max-w-screen-xl mx-auto px-3 sm:px-8 lg:px-10">
        <!-- Section Header - Compacto en móvil -->
        <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-3 sm:gap-6 mb-5 sm:mb-14">
          <div class="text-left sm:text-left">
            <span class="hidden sm:inline-block text-brand-600 font-medium text-sm tracking-widest uppercase mb-4">Selección Premium</span>
            <h2 class="text-[17px] font-bold uppercase tracking-wide sm:tracking-normal sm:normal-case sm:font-luxury sm:text-4xl lg:text-5xl text-text-dark">
              Productos <em class="not-italic text-brand-600">Destacados</em>
            </h2>
          </div>
          <router-link to="/catalogo" class="hidden sm:inline-flex items-center gap-2 text-[13px] text-text-dark font-medium uppercase tracking-[0.1em] border border-text-dark/20 px-6 py-3 rounded-sm hover:bg-text-dark hover:text-white transition-all group">
            VER TODO EL CATÁLOGO
            <svg class="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
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
        <!-- Products Grid - Retail Premium -->
        <div v-else-if="productos.length > 0" class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-8">
          <!-- Product Card - Minimalista, 100% clickeable -->
          <article
            v-for="producto in productos"
            :key="producto.id"
            :data-producto-id="producto.id"
            @click="irADetalle(producto.id)"
            class="group cursor-pointer"
          >
            <!-- Imagen Container -->
            <div class="relative aspect-[3/4] rounded-xl sm:rounded-2xl overflow-hidden bg-gray-50">
              <!-- Wishlist Button - Sobre la imagen -->
              <button 
                @click.stop="toggleFavorito(producto)"
                class="absolute top-2 right-2 sm:top-3 sm:right-3 z-10 w-8 h-8 sm:w-9 sm:h-9 bg-white rounded-full flex items-center justify-center shadow-sm transition-all hover:shadow-md active:scale-95"
              >
                <svg 
                  class="w-4 h-4 sm:w-[18px] sm:h-[18px] transition-colors" 
                  :class="isInWishlist(producto.id) ? 'text-[#D81B60]' : 'text-gray-400'"
                  :fill="isInWishlist(producto.id) ? 'currentColor' : 'none'" 
                  stroke="currentColor" 
                  stroke-width="1.5" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>
              </button>

              <!-- Image / Video -->
              <video
                v-if="isVideo(getProductoMediaUrl(producto))"
                :src="getProductoMediaUrl(producto)"
                class="w-full h-full object-cover"
                autoplay
                muted
                loop
                playsinline
                preload="metadata"
              ></video>
              <img
                v-else-if="getProductoMediaUrl(producto)"
                :src="getProductoMediaUrl(producto)"
                :alt="producto.nombre"
                class="w-full h-full object-cover sm:group-hover:scale-105 transition-transform duration-500"
                @error="handleImageError"
              >
              <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-50">
                <svg class="w-10 h-10 text-gray-200" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
              </div>
            </div>

            <!-- Product Info - Solo título y precio, alineado izquierda -->
            <div class="mt-2.5 sm:mt-3">
              <h3 class="font-medium text-[13px] sm:text-sm text-gray-900 leading-tight line-clamp-2 min-h-[2.6em] sm:group-hover:text-[#D81B60] transition-colors">{{ producto.nombre }}</h3>
              <p class="mt-1.5 text-[15px] sm:text-base font-bold text-gray-900 leading-none">
                ${{ formatPrice(producto.precio_monto || producto.precio) }}<span class="text-[9px] sm:text-[10px] text-gray-400 font-normal ml-0.5">{{ producto.precio_moneda || 'COP' }}</span>
              </p>
            </div>
          </article>
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

        <!-- CTA Ver catálogo - Visible solo en móvil debajo del grid -->
        <div v-if="productos.length > 0" class="flex sm:hidden justify-center mt-6">
          <router-link to="/catalogo" class="w-full inline-flex items-center justify-center gap-2 text-[13px] text-text-dark font-medium uppercase tracking-[0.1em] border border-text-dark/20 px-5 py-3 rounded-sm hover:bg-text-dark hover:text-white transition-all">
            VER TODO EL CATÁLOGO
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ========================================
         VIDEO KANEKALON - Sección Inmersiva Optimizada
         ======================================== -->
    <section class="relative bg-black overflow-hidden video-hero-section">
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
        
        <!-- Overlay - Gradiente cinemático: limpio arriba, oscuro abajo -->
        <div class="absolute inset-0 video-hero-overlay"></div>
        
        <!-- Contenido sobre el video - Bottom-aligned en móvil -->
        <div class="absolute inset-0 flex items-end sm:items-center lg:items-end justify-center video-hero-content">
          <div class="text-center sm:text-center px-5 sm:px-6 pb-14 sm:pb-12 lg:pb-20 w-full max-w-2xl mx-auto">
            <!-- Badge - Oculto en móvil -->
            <div class="video-hero-badge hidden sm:inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-5 py-2 mb-6">
              <span class="text-white/90 text-sm font-medium uppercase tracking-wider">Calidad Premium</span>
            </div>
            <h2 class="font-luxury text-[26px] leading-tight sm:text-3xl lg:text-5xl text-white mb-2 sm:mb-4 drop-shadow-2xl">
              Extensiones 100% <span class="text-brand-400">Naturales</span>
            </h2>
            <!-- Párrafo descriptivo - Oculto en móvil, visible en tablet+ -->
            <p class="hidden sm:block text-white/80 text-base lg:text-lg max-w-xl lg:max-w-2xl mx-auto mb-8 leading-relaxed">
              Tecnología de fibras de la más alta calidad. Transforma tu look con elegancia y sofisticación profesional.
            </p>
            <router-link 
              to="/catalogo"
              class="inline-flex items-center gap-2 bg-white hover:bg-nude-100 text-text-dark font-medium text-xs sm:text-base px-4 py-2 sm:px-7 sm:py-3.5 rounded-full transition-all shadow-lg hover:shadow-xl"
            >
              Ver Catálogo Completo
              <svg class="w-3.5 h-3.5 sm:w-5 sm:h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
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
    <section id="mayoreo" class="py-10 sm:py-20 lg:py-32 relative overflow-hidden bg-gradient-to-br from-[#F5EDE4] via-[#FBF7F3] to-[#F0E6DC]">
      <!-- Decorative Pattern -->
      <div class="absolute inset-0 opacity-[0.03]" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23000000\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12 relative z-10">
        <div class="grid lg:grid-cols-2 gap-8 sm:gap-12 lg:gap-16 items-center">
          
          <!-- Image - Oculta en móvil para mantener sección compacta -->
          <div class="relative order-2 lg:order-1 hidden sm:block">
            <div class="relative rounded-3xl overflow-hidden shadow-2xl">
              <img 
                src="https://images.unsplash.com/photo-1560066984-138dadb4c035?w=700&h=800&fit=crop&q=85" 
                alt="Salón de belleza profesional" 
                class="w-full h-auto"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>
              
              <!-- Stats Card -->
              <div class="absolute bottom-6 left-6 right-6 bg-white/95 rounded-2xl shadow-xl p-6">
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

            <p class="text-text-medium text-sm sm:text-lg mb-6 sm:mb-8 max-w-xl leading-relaxed">
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

            <!-- CTA -->
            <div class="flex flex-col sm:flex-row gap-3 sm:gap-4">
              <a 
                href="https://pro.demostracion.store/"
                class="inline-flex items-center justify-center gap-2 sm:gap-3 bg-white hover:bg-nude-50 border-2 border-nude-300 text-text-dark font-medium text-sm sm:text-base px-5 py-3 sm:px-7 sm:py-3.5 rounded-full transition-all hover:border-brand-400 touch-target"
              >
                <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 .75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349M3.75 21V9.349m0 0a3.001 3.001 0 0 0 3.75-.615A2.993 2.993 0 0 0 9.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 0 0 2.25 1.016c.896 0 1.7-.393 2.25-1.015a3.001 3.001 0 0 0 3.75.614m-16.5 0a3.004 3.004 0 0 1-.621-4.72l1.189-1.19A1.5 1.5 0 0 1 5.378 3h13.243a1.5 1.5 0 0 1 1.06.44l1.19 1.189a3 3 0 0 1-.621 4.72M6.75 18h3.75a.75.75 0 0 0 .75-.75V13.5a.75.75 0 0 0-.75-.75H6.75a.75.75 0 0 0-.75.75v3.75c0 .414.336.75.75.75Z" />
                </svg>
                Portal Mayoristas
              </a>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ========================================
         PLAN EMPRENDEDOR - Paquete de Productos
         ======================================== -->
    <section class="relative bg-gradient-to-br from-[#1A1A1A] via-[#2D2D2D] to-[#1A1A1A] overflow-hidden py-14 sm:py-20 lg:py-28">
      <!-- Decoración dorada sutil -->
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#C9A962]/40 to-transparent"></div>
      <div class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#C9A962]/40 to-transparent"></div>
      
      <!-- Patrón de fondo sutil -->
      <div class="absolute inset-0 opacity-5">
        <div class="absolute top-10 left-10 w-32 h-32 border border-[#C9A962] rounded-full"></div>
        <div class="absolute bottom-10 right-10 w-48 h-48 border border-[#C9A962] rounded-full"></div>
        <div class="absolute top-1/2 left-1/4 w-20 h-20 border border-[#C9A962] rounded-full"></div>
      </div>

      <div class="max-w-3xl mx-auto px-5 sm:px-8 lg:px-12 relative z-10 text-center">
        <div class="inline-flex items-center gap-2 border border-[#C9A962]/60 rounded-sm px-4 py-1.5 mb-6">
          <svg class="w-4 h-4 text-[#C9A962]" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          <span class="text-[10px] tracking-[0.25em] uppercase text-[#C9A962] font-medium">OPORTUNIDAD EXCLUSIVA</span>
        </div>

        <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl xl:text-6xl text-white leading-[1.1] mb-5">
          Plan <span class="text-[#C9A962]">Emprendedor</span>
        </h2>

        <p class="text-white/70 text-base sm:text-lg mb-6 leading-relaxed max-w-md mx-auto">
          Inicia tu negocio de extensiones y pelucas con un paquete completo a precio mayorista.
        </p>

        <!-- Precio destacado -->
        <div class="mb-8">
          <div class="inline-flex items-baseline gap-2">
            <span class="text-4xl sm:text-5xl lg:text-6xl font-bold text-[#C9A962]">$1.730.000</span>
            <span class="text-white/50 text-sm">COP</span>
          </div>
          <p class="text-white/60 text-sm mt-2">Paquete completo para iniciar</p>
        </div>

        <!-- CTA WhatsApp -->
        <a
          href="https://wa.me/4796657763?text=Hola%2C%20quiero%20información%20sobre%20el%20Plan%20Emprendedor%20de%20%241.730.000.%20%C2%BFQué%20incluye%3F"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center justify-center gap-3 bg-[#25D366] hover:bg-[#20BD5A] text-white font-semibold text-sm sm:text-base px-7 py-3.5 sm:py-4 rounded-full transition-all hover:scale-105 hover:shadow-xl shadow-lg touch-target"
        >
          <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
          ¿Qué incluye? Pregúntanos
        </a>
      </div>
    </section>

    <!-- ========================================
         TESTIMONIOS - Prueba Social (Oculto en móvil)
         ======================================== -->
    <section id="testimonios" class="hidden sm:block py-20 lg:py-28 bg-[#FAFAFA]">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 lg:px-12">
        <!-- Section Header -->
        <div class="text-center mb-14">
          <span class="inline-block text-brand-600 font-medium text-sm tracking-widest uppercase mb-4">Testimonios</span>
          <h2 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-text-dark mb-4">
            Lo que opinan quienes compran en <em class="not-italic text-brand-600">Kharis</em>
          </h2>
          <p class="text-text-medium max-w-xl mx-auto">
            Opiniones verificadas de compras reales
          </p>
        </div>

        <!-- Testimonials Grid -->
        <div v-if="resenasLoading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          <div v-for="i in 3" :key="i" class="bg-white rounded-3xl p-8 shadow-soft">
            <div class="h-4 w-28 bg-nude-100 rounded mb-4"></div>
            <div class="h-14 w-full bg-nude-50 rounded mb-6"></div>
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-full bg-nude-100"></div>
              <div class="space-y-2">
                <div class="h-3 w-28 bg-nude-100 rounded"></div>
                <div class="h-3 w-36 bg-nude-50 rounded"></div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="resenasDestacadas.length" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          <div v-for="resena in resenasDestacadas" :key="resena.id" class="bg-white rounded-3xl p-8 shadow-soft hover-lift">
            <div class="flex items-center gap-1 mb-4">
              <svg v-for="i in 5" :key="i" class="w-5 h-5" :class="i <= resena.rating ? 'text-gold-400' : 'text-gray-200'" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <p class="text-text-medium mb-6 leading-relaxed">
              Calificación verificada de una compra real.
            </p>
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-full bg-blush-100 text-brand-600 font-semibold flex items-center justify-center">
                {{ getInitials(resena.cliente) }}
              </div>
              <div>
                <p class="font-semibold text-text-dark">{{ resena.cliente }}</p>
                <p class="text-sm text-text-light">Producto: {{ resena.producto_nombre }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center text-text-medium">
          Aún no hay calificaciones aprobadas. Sé la primera persona en calificar.
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
              <span class="font-semibold text-brand-600">Especialistas</span> en extensiones, pelucas y frontales premium
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
                Tu socio experto en belleza profesional. Extensiones, pelucas y accesorios de la más alta calidad.
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
          <div class="flex flex-col items-center gap-3 text-center">
            <p class="text-white/50 text-sm">© 2026 Kharis Distribuidora. Todos los derechos reservados.</p>
            <p class="text-white/40 text-xs">
              Desarrollado por 
              <a href="https://105code.cloud" target="_blank" rel="noopener noreferrer" class="text-white/60 hover:text-white font-medium transition-colors">105 Code</a>
              &amp;
              <span class="text-white/60 font-medium">Websarrollab</span>
            </p>
          </div>
        </div>
      </div>
    </footer>

    <!-- ========================================
         FLOATING SOCIAL BUTTONS (Right Side) - Compactos en móvil
         ======================================== -->
    <!-- Instagram Button - Solo visible en tablet/desktop para enfoque en conversión móvil -->
    <a 
      href="https://www.instagram.com/kharisdistribuidora/"
      target="_blank"
      class="hidden sm:flex fixed bottom-28 right-6 w-14 h-14 lg:w-16 lg:h-16 bg-gradient-to-br from-purple-500 via-pink-500 to-orange-400 text-white rounded-full items-center justify-center shadow-xl hover:scale-110 transition-all duration-300 z-40 group touch-target"
    >
      <svg class="w-6 h-6 lg:w-8 lg:h-8" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
      </svg>
      <!-- Tooltip - Solo desktop -->
      <span class="hidden lg:block absolute right-full mr-3 bg-white text-text-dark text-sm font-medium px-4 py-2 rounded-xl shadow-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
        Síguenos en Instagram
      </span>
    </a>

    <!-- WhatsApp Button - Solo visible después del hero -->
    <a 
      v-show="showFloatingBtns || windowWidth >= 640"
      href="https://wa.me/4796657763?text=Hola,%20me%20interesa%20información%20sobre%20sus%20productos"
      target="_blank"
      class="fixed bottom-4 sm:bottom-6 right-4 sm:right-6 w-11 h-11 sm:w-14 sm:h-14 lg:w-16 lg:h-16 bg-green-500 text-white rounded-full flex items-center justify-center shadow-xl hover:bg-green-600 hover:scale-110 transition-all duration-300 z-40 group touch-target"
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
        class="fixed top-0 right-0 h-full w-full sm:w-[380px] bg-white z-[60] flex flex-col cart-drawer-panel"
        @click.stop
      >
        <!-- Header - Elegante con Serif -->
        <div class="flex items-center justify-between border-b border-nude-200/40 cart-drawer-header">
          <h2 class="font-luxury text-text-dark cart-drawer-title">Tu Selección</h2>
          <button 
            @click="closeCartDrawer"
            class="w-7 h-7 rounded-full flex items-center justify-center hover:bg-nude-100 transition-colors"
          >
            <svg class="w-3.5 h-3.5 text-text-medium" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Barra de Progreso Envío Gratis - Minimalista -->
        <div v-if="getCartSubtotal() < 300000" class="bg-gradient-to-r from-nude-50 to-white cart-shipping-bar">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[0.6875rem] text-text-medium">
              Te faltan ${{ formatPrice(300000 - getCartSubtotal()) }} para envío gratis
            </span>
            <span class="text-[0.6875rem] text-brand-600 font-medium">{{ Math.min(100, Math.round((getCartSubtotal() / 300000) * 100)) }}%</span>
          </div>
          <div class="h-0.5 bg-nude-200 rounded-full overflow-hidden">
            <div 
              class="h-full bg-gradient-to-r from-brand-500 to-brand-600 rounded-full transition-all duration-500"
              :style="{ width: Math.min(100, (getCartSubtotal() / 300000) * 100) + '%' }"
            ></div>
          </div>
        </div>
        <div v-else class="bg-gradient-to-r from-green-50 to-white cart-shipping-bar">
          <div class="flex items-center justify-center gap-1.5">
            <svg class="w-3.5 h-3.5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-xs text-green-700 font-medium">Envío gratis aplicado</span>
          </div>
        </div>
        
        <!-- Contenido del Carrito -->
        <div class="flex-1 overflow-y-auto px-3 sm:px-4">
          <!-- Loading -->
          <div v-if="cartLoading" class="flex items-center justify-center h-28">
            <div class="w-6 h-6 border-2 border-brand-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
          
          <!-- Carrito vacío - Femenino -->
          <div v-else-if="cartItems.length === 0" class="flex flex-col items-center justify-center text-center cart-empty">
            <div class="rounded-full bg-gradient-to-br from-nude-100 to-nude-200 flex items-center justify-center cart-empty-icon">
              <svg class="w-8 h-8 sm:w-9 sm:h-9 text-brand-400" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
            </div>
            <h3 class="font-luxury text-text-dark cart-empty-title">Tu selección está vacía</h3>
            <p class="cart-empty-text">Descubre productos increíbles para ti</p>
            <button 
              @click="closeCartDrawer"
              class="bg-brand-600 hover:bg-brand-700 text-white font-medium rounded-full transition-all hover:shadow-lg hover:shadow-brand-600/20 cart-empty-btn"
            >
              Explorar colección
            </button>
          </div>
          
          <!-- Items del carrito - Soft Beauty -->
          <div v-else class="py-3 space-y-2.5">
            <div 
              v-for="item in cartItems" 
              :key="item.variante_id || item.producto_id"
              class="flex bg-white transition-colors cart-item"
            >
              <!-- Imagen del producto -->
              <div class="bg-gradient-to-br from-nude-50 to-nude-100 flex-shrink-0 overflow-hidden flex items-center justify-center cart-item-image">
                <img 
                  v-if="getCartMediaUrl(item)" 
                  :src="getCartMediaUrl(item)" 
                  :alt="item.nombre"
                  class="w-full h-full object-cover"
                  @error="handleImageError"
                />
                <div v-if="getCartMediaUrl(item) && isVideo(getCartSourceUrl(item))" class="absolute inset-0 flex items-center justify-center bg-black/25">
                  <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                  </svg>
                </div>
                <svg v-else class="w-6 h-6 text-nude-300" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
                </svg>
              </div>
              
              <!-- Info del producto -->
              <div class="flex-1 min-w-0 flex flex-col justify-between py-0.5">
                <div>
                  <h3 class="line-clamp-2 cart-item-name">
                    {{ item.nombre || 'Producto' }}
                  </h3>
                  <p v-if="item.color || item.largo" class="cart-item-variant">
                    <span v-if="item.color">{{ formatColorLabel(item.color) }}</span>
                    <span v-if="item.color && item.largo"> · </span>
                    <span v-if="item.largo">{{ item.largo }}</span>
                  </p>
                  
                  <!-- Selector de Cantidad - Boutique Style -->
                  <div class="flex items-center mt-1.5">
                    <div class="cart-qty-selector">
                      <button 
                        @click="updateQuantity(item.variante_id || item.producto_id, (item.cantidad || 1) - 1)"
                        class="cart-qty-btn"
                        :disabled="(item.cantidad || 1) <= 1"
                      >
                        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" d="M5 12h14" />
                        </svg>
                      </button>
                      <span class="cart-qty-value">{{ item.cantidad || 1 }}</span>
                      <button 
                        @click="updateQuantity(item.variante_id || item.producto_id, (item.cantidad || 1) + 1)"
                        class="cart-qty-btn"
                      >
                        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" d="M12 5v14m-7-7h14" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
                
                <!-- Precio -->
                <p class="cart-item-price mt-1">
                  ${{ formatPrice(getItemPrice(item)) }}
                </p>
              </div>
              
              <!-- Eliminar - Rosado suave -->
              <button 
                @click.stop="removeFromCart(item.variante_id || item.producto_id)"
                class="self-start cart-remove-btn"
                title="Eliminar"
              >
                <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Footer - Fondo Nude, Botón Pill -->
        <div v-if="cartItems.length > 0" class="cart-footer">
          <!-- Resumen de precios -->
          <div class="cart-footer-summary space-y-1.5">
            <div class="cart-summary-row">
              <span>Subtotal</span>
              <span>${{ formatPrice(getCartSubtotal()) }}</span>
            </div>
            <div class="cart-summary-row">
              <span>Envío</span>
              <span class="italic">Por calcular</span>
            </div>
            <div class="cart-total-row">
              <span class="cart-total-label">Total</span>
              <span class="cart-total-value">${{ formatPrice(getCartSubtotal()) }}</span>
            </div>
          </div>
          
          <!-- Botones -->
          <div class="cart-actions">
            <button 
              @click="irACheckout"
              class="cart-checkout-btn"
            >
              Finalizar Compra
            </button>
            <button 
              @click="closeCartDrawer"
              class="cart-continue-btn"
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
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { productosService, carritoService, authService, favoritosService } from '../services/productos'
import { resenasService } from '../services/resenas'
import { categoriasService } from '../services/categorias'
import { getImageUrl } from '../services/api'
import { formatColorLabel } from '@/utils/colorLabels'

export default {
  name: 'Home',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const productos = ref([])
    const categorias = ref([])
    const resenasDestacadas = ref([])
    const resenasLoading = ref(true)
    const loading = ref(true)
    const error = ref(null)
    const cartCount = ref(0)
    const isScrolled = ref(false)
    const showFloatingBtns = ref(false)
    const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)

    // Top Bar Announcements
    const announcements = ref([
      'ENVÍO GRATIS EN COMPRAS SUPERIORES A $200.000',
      '5% OFF ADICIONAL PAGANDO CON TRANSFERENCIA',
      'NUEVA COLECCIÓN: EXTENSIONES REMY PREMIUM'
    ])
    const currentAnnouncement = ref(0)
    let announcementInterval = null

    const mobileMenuOpen = ref(false)
    const mobileSearchOpen = ref(false)
    const mobileSearchInputRef = ref(null)
    const searchQuery = ref('')
    const searchSuggestions = ref([])
    const showSuggestions = ref(false)
    const searchInputRef = ref(null)
    const suggestionsRef = ref(null)

    // ===== Carousel de categorías (móvil) =====
    const categoriasCarouselRef = ref(null)
    const catScrolled = ref(false)

    const scrollCategorias = () => {
      const el = categoriasCarouselRef.value
      if (el) {
        el.scrollBy({ left: el.offsetWidth * 0.85, behavior: 'smooth' })
      }
    }

    const onCatScroll = () => {
      const el = categoriasCarouselRef.value
      if (el && el.scrollLeft > 30) {
        catScrolled.value = true
      }
    }

    // ===== Funciones del menú móvil off-canvas =====
    const openMobileMenu = () => {
      mobileMenuOpen.value = true
      document.body.style.overflow = 'hidden'
    }
    const closeMobileMenu = () => {
      mobileMenuOpen.value = false
      document.body.style.overflow = ''
    }

    // ===== Funciones de búsqueda móvil full-screen =====
    const openMobileSearch = () => {
      mobileSearchOpen.value = true
      document.body.style.overflow = 'hidden'
      // Autofocus después del render
      setTimeout(() => {
        mobileSearchInputRef.value?.focus()
      }, 100)
    }
    const closeMobileSearch = () => {
      mobileSearchOpen.value = false
      document.body.style.overflow = ''
      searchQuery.value = ''
      searchSuggestions.value = []
      showSuggestions.value = false
    }
    
    // ===== WISHLIST LOCAL (sin login requerido) =====
    const wishlist = ref([])
    
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
    
    const isInWishlist = (productId) => {
      return wishlist.value.includes(productId)
    }
    
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

    const getInitials = (fullName) => {
      if (!fullName) return 'C'
      const parts = String(fullName).trim().split(' ').filter(Boolean)
      if (parts.length === 1) return parts[0][0]?.toUpperCase() || 'C'
      return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
    }

    const cargarResenasDestacadas = async () => {
      resenasLoading.value = true
      try {
        resenasDestacadas.value = await resenasService.getDestacadas(6)
      } catch (e) {
        resenasDestacadas.value = []
      } finally {
        resenasLoading.value = false
      }
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
    const videoPosters = ref({})
    
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
          const rawItems = Array.isArray(data)
            ? data
            : (data?.items || [])
          const items = rawItems.map((item) => {
            const productoId = item?.producto_id ?? item?.id
            const varianteId = item?.variante_id ?? null
            return {
              ...item,
              producto_id: productoId,
              variante_id: varianteId
            }
          })

          // Compatibilidad con formato antiguo (sin timestamp/total)
          const timestamp = typeof data?.timestamp === 'number' ? data.timestamp : Date.now()
          const total = typeof data?.total === 'number'
            ? data.total
            : items.reduce((acc, item) => {
              const unit = item?.precio_unitario ?? item?.precio_monto ?? item?.precio ?? 0
              const qty = item?.cantidad ?? 1
              const subtotal = item?.subtotal
              return acc + (typeof subtotal === 'number' ? subtotal : unit * qty)
            }, 0)

          // Solo usar cache si tiene menos de 30 minutos
          if (Date.now() - timestamp < 30 * 60 * 1000) {
            return { items, total, count: parseInt(count) || 0 }
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
    const updateQuantity = async (itemKey, nuevaCantidad) => {
      if (nuevaCantidad < 1) {
        // Si la cantidad es 0 o menos, eliminar el producto
        await removeFromCart(itemKey)
        return
      }
      
      try {
        // Actualizar localmente primero para feedback inmediato
        const itemIndex = cartItems.value.findIndex(i => (i.variante_id || i.producto_id) === itemKey)
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
          const item = cartItems.value.find(i => (i.variante_id || i.producto_id) === itemKey)
          if (item) {
            await carritoService.actualizarCantidad(
              item.producto_id,
              item.variante_id,
              nuevaCantidad,
              localStorage.getItem('kharis_cart_id')
            )
          }
        }
      } catch (err) {
        console.error('Error actualizando cantidad:', err)
        // Recargar del servidor en caso de error
        await loadCartItems()
      }
    }
    
    const loadCartItems = async () => {
      cartLoading.value = true
      
      // Cargar items del localStorage SIN restricción de tiempo
      // (consistente con Catalogo.vue y ProductoDetalle.vue)
      try {
        const cached = localStorage.getItem(CART_STORAGE_KEY)
        if (cached) {
          const data = JSON.parse(cached)
          const rawItems = Array.isArray(data) ? data : (data?.items || [])
          const items = rawItems.map((item) => {
            const productoId = item?.producto_id ?? item?.id
            const varianteId = item?.variante_id ?? null
            return {
              ...item,
              producto_id: productoId,
              variante_id: varianteId
            }
          })
          
          if (items.length > 0) {
            cartItems.value = items
            cartTotal.value = typeof data?.total === 'number'
              ? data.total
              : items.reduce((acc, item) => {
                  const unit = item?.precio_unitario ?? item?.precio_monto ?? item?.precio ?? 0
                  const qty = item?.cantidad ?? 1
                  const subtotal = item?.subtotal
                  return acc + (typeof subtotal === 'number' ? subtotal : unit * qty)
                }, 0)
            cartCount.value = items.reduce((sum, item) => sum + (item.cantidad || 1), 0)
          }
        }
      } catch (e) {
        console.warn('Error leyendo carrito de localStorage:', e)
      }
      
      // Si no está logueado, solo usar cache local
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
          if (data.id) {
            localStorage.setItem('kharis_cart_id', data.id)
          }
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
    
    const removeFromCart = async (itemKey) => {
      try {
        // Primero actualizar UI localmente para feedback inmediato
        const itemIndex = cartItems.value.findIndex(i => (i.variante_id || i.producto_id) === itemKey)
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
            const item = cartItems.value.find(i => (i.variante_id || i.producto_id) === itemKey)
            await carritoService.eliminarProducto(
              item?.producto_id,
              item?.variante_id,
              localStorage.getItem('kharis_cart_id')
            )
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
        video: '/images/hero%20b2c/VID-20260213-WA0003.mp4',
        alt: 'Video promocional - Belleza profesional'
      },
      {
        image: '/images/hero%20b2c/1.jpeg',
        alt: 'Belleza profesional - Extensiones premium'
      },
      {
        image: '/images/hero%20b2c/2.jpeg',
        alt: 'Cabello natural de alta calidad'
      },
      {
        image: '/images/hero%20b2c/3.jpeg',
        alt: 'Estilo y elegancia profesional'
      }
    ])

    // Slides desktop - imágenes horizontales originales
    const heroSlidesDesktop = ref([
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

    // Slides activos según viewport: móvil = verticales, desktop = horizontales
    const activeHeroSlides = computed(() => {
      return windowWidth.value < 640 ? heroSlides.value : heroSlidesDesktop.value
    })

    const goToSlide = (index) => {
      currentSlide.value = index
      resetSlideInterval()
    }

    const nextSlide = () => {
      currentSlide.value = (currentSlide.value + 1) % activeHeroSlides.value.length
    }

    const startSlideshow = () => {
      // Duración dinámica: 11s para videos, 6s para imágenes
      const getCurrentSlideDuration = () => {
        const currentSlideData = activeHeroSlides.value[currentSlide.value]
        return currentSlideData?.video ? 11000 : 6000
      }
      
      const scheduleNextSlide = () => {
        if (slideInterval) clearTimeout(slideInterval)
        slideInterval = setTimeout(() => {
          nextSlide()
          scheduleNextSlide()
        }, getCurrentSlideDuration())
      }
      
      scheduleNextSlide()
    }

    const resetSlideInterval = () => {
      if (slideInterval) clearTimeout(slideInterval)
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
        closeMobileSearch()
      } else if (searchQuery.value.trim()) {
        // Navegar al catálogo con el query de búsqueda
        const query = searchQuery.value.trim()
        router.push({ path: '/catalogo', query: { q: query } })
        showSuggestions.value = false
        closeMobileSearch()
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
      // En móvil el header siempre es blanco (sólido), no transparente
      if (windowWidth.value < 640) {
        isScrolled.value = true
      } else {
        const threshold = 30
        isScrolled.value = window.scrollY > threshold
      }
      // Botones flotantes: solo visibles después de pasar el hero (>500px)
      showFloatingBtns.value = window.scrollY > 500
    }

    const handleResize = () => {
      const prevWidth = windowWidth.value
      windowWidth.value = window.innerWidth
      // Re-evaluar header al cambiar tamaño (mobile siempre blanco)
      handleScroll()
      // Reset slide si cambiamos entre mobile/desktop (diferente cantidad de slides)
      const crossedBreakpoint = (prevWidth < 640 && windowWidth.value >= 640) || (prevWidth >= 640 && windowWidth.value < 640)
      if (crossedBreakpoint) {
        currentSlide.value = 0
        resetSlideInterval()
      }
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
        const categoriasData = data.categorias || data || []
        categorias.value = categoriasData.map((categoria) => {
          if (!categoria) return categoria
          const nombreOriginal = String(categoria.nombre || '')
          const nombreNormalizado = nombreOriginal.replace(/\s+/g, ' ').trim().toLowerCase()
          const descripcion = String(categoria.descripcion || '')
          const descripcionCorta = String(categoria.descripcion_corta || '')
          const descNormalizada = descripcion.replace(/\s+/g, ' ').trim().toLowerCase()
          const descCortaNormalizada = descripcionCorta.replace(/\s+/g, ' ').trim().toLowerCase()
          if (nombreNormalizado === 'extensiones') {
            const nuevoTexto = 'Largos y tonos para cada look, con calidad comprobada y caida natural.'
            return {
              ...categoria,
              descripcion: nuevoTexto,
              descripcion_corta: nuevoTexto
            }
          }
          if (nombreNormalizado.includes('pelucas lacefront') || nombreNormalizado.includes('full lace')) {
            return {
              ...categoria,
              nombre: 'Pelucas de encaje frontal y completo'
            }
          }
          if (nombreNormalizado.includes('accesorios') && (nombreNormalizado.includes('cuidado') || nombreNormalizado.includes('styling'))) {
            return {
              ...categoria,
              nombre: 'Accesorios de cuidado y peinado'
            }
          }
          if (descNormalizada.includes('lacefront') || descNormalizada.includes('full lace')) {
            return {
              ...categoria,
              descripcion: 'Encaje frontal y completo con acabado natural.',
              descripcion_corta: 'Encaje frontal y completo.'
            }
          }
          if (descCortaNormalizada.includes('lacefront') || descCortaNormalizada.includes('full lace')) {
            return {
              ...categoria,
              descripcion_corta: 'Encaje frontal y completo.'
            }
          }
          if (descNormalizada.includes('cuidado') && descNormalizada.includes('styling')) {
            return {
              ...categoria,
              descripcion: 'Cuidado y peinado para un acabado profesional.',
              descripcion_corta: 'Cuidado y peinado.'
            }
          }
          if (descCortaNormalizada.includes('cuidado') && descCortaNormalizada.includes('styling')) {
            return {
              ...categoria,
              descripcion_corta: 'Cuidado y peinado.'
            }
          }
          return categoria
        })
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
        const variantes = Array.isArray(producto?.variantes) ? producto.variantes : []
        const varianteSeleccionada = variantes.find(v => v.activo !== false && (v.stock_actual ?? 0) > 0) || variantes[0] || null
        const requiereVariante = variantes.length > 0
        if (requiereVariante && !varianteSeleccionada) {
          showToast('Selecciona una combinación disponible', 'info')
          return
        }

        const precioProducto = Number(
          varianteSeleccionada?.precio_monto ?? producto.precio_monto ?? producto.precio_final ?? producto.precio ?? 0
        )
        const itemKey = requiereVariante ? (varianteSeleccionada?.id || producto.id) : producto.id
        const varianteId = requiereVariante ? (varianteSeleccionada?.id || null) : null
        
        // Actualizar carrito local inmediatamente (para todos los usuarios)
        const currentItems = [...cartItems.value]
        const existingIndex = currentItems.findIndex(i => (i.variante_id || i.producto_id) === itemKey)
        if (existingIndex >= 0) {
          currentItems[existingIndex].cantidad++
          currentItems[existingIndex].subtotal = currentItems[existingIndex].cantidad * currentItems[existingIndex].precio_unitario
        } else {
          const imgUrl = producto.imagen_url || producto.imagen_principal || producto.imagen || producto.imagenes?.[0] || null
          currentItems.push({
            producto_id: producto.id,
            variante_id: varianteId,
            variante_sku: varianteSeleccionada?.sku || '',
            color: varianteSeleccionada?.color || '',
            largo: varianteSeleccionada?.largo || '',
            nombre: producto.nombre,
            imagen_url: getImageUrl(varianteSeleccionada?.imagen_url || imgUrl),
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
            await carritoService.agregarProducto(producto.id, varianteId, 1)
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
      const productId = producto.id
      const idx = wishlist.value.indexOf(productId)
      if (idx > -1) {
        wishlist.value.splice(idx, 1)
        showToast('Eliminado de favoritos', 'info')
      } else {
        wishlist.value.push(productId)
        showToast('Añadido a favoritos ❤️', 'success')
      }
      saveWishlist()
      
      // Si está logueado, sincronizar también con el servidor
      if (isLoggedIn.value) {
        try {
          await favoritosService.toggle(productId)
        } catch (err) {
          console.error('Error sincronizando favorito con servidor:', err)
        }
      }
    }
    
    // User menu functions
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
    }
    
    const handleMenuAction = (action) => {
      showUserMenu.value = false
      
      // Favoritos no requiere login
      if (action === 'favoritos') {
        router.push('/favoritos')
        return
      }
      
      if (!isLoggedIn.value) {
        router.push('/login')
        return
      }
      
      switch(action) {
        case 'pedidos':
          router.push('/mi-cuenta?tab=compras')
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
      // Ignorar si el click viene del botón mobile de usuario
      if (event.target.closest('[data-user-toggle]')) return
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

    const getProductoMediaUrl = (producto) => {
      return getImageUrl(producto?.imagen_principal || producto?.imagen_url || producto?.imagen)
    }

    const isVideo = (url) => {
      if (!url) return false
      const cleanUrl = url.split('?')[0].toLowerCase()
      return ['.mp4', '.webm', '.ogg', '.mov'].some(ext => cleanUrl.endsWith(ext))
    }

    const createVideoPoster = (url) => {
      return new Promise((resolve) => {
        try {
          const video = document.createElement('video')
          video.crossOrigin = 'anonymous'
          video.muted = true
          video.playsInline = true
          video.preload = 'metadata'
          video.src = url

          const onError = () => resolve(null)

          video.addEventListener('error', onError, { once: true })
          video.addEventListener('loadeddata', () => {
            const seekTo = Math.min(1, video.duration || 1)
            try {
              video.currentTime = seekTo
            } catch {
              resolve(null)
            }
          }, { once: true })

          video.addEventListener('seeked', () => {
            try {
              const canvas = document.createElement('canvas')
              canvas.width = video.videoWidth || 120
              canvas.height = video.videoHeight || 120
              const ctx = canvas.getContext('2d')
              if (!ctx) return resolve(null)
              ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
              resolve(canvas.toDataURL('image/jpeg', 0.82))
            } catch {
              resolve(null)
            }
          }, { once: true })
        } catch {
          resolve(null)
        }
      })
    }

    const ensureVideoPoster = async (url) => {
      if (videoPosters.value[url]) return
      const poster = await createVideoPoster(url)
      if (poster) {
        videoPosters.value = { ...videoPosters.value, [url]: poster }
      }
    }

    const getCartSourceUrl = (item) => {
      return getImageUrl(item?.imagen_url || item?.imagen_principal || item?.imagen)
    }

    const getCartMediaUrl = (item) => {
      const url = getCartSourceUrl(item)
      if (!url) return ''
      if (isVideo(url)) {
        ensureVideoPoster(url)
        return videoPosters.value[url] || ''
      }
      return url
    }

    const cargarResumenCarrito = async () => {
      // PRIMERO: Leer el count directamente del localStorage (sin restricción de tiempo)
      // Esto mantiene consistencia con Catalogo.vue y ProductoDetalle.vue
      try {
        const storedCount = localStorage.getItem(CART_COUNT_KEY)
        if (storedCount) {
          const parsedCount = parseInt(storedCount, 10)
          if (!isNaN(parsedCount) && parsedCount > 0) {
            cartCount.value = parsedCount
          }
        }
      } catch (e) {
        console.warn('Error leyendo cart count:', e)
      }
      
      // Si no está logueado, usar solo el valor de localStorage
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
      loadWishlist()
      const categoriasPromise = cargarCategorias()
      const productosPromise = cargarProductos()
      cargarResenasDestacadas()
      cargarResumenCarrito()
      window.addEventListener('scroll', handleScroll)
      window.addEventListener('resize', handleResize)
      window.addEventListener('user-logged-in', handleUserLoggedIn)
      document.addEventListener('click', handleClickOutside)
      document.addEventListener('click', handleClickOutsideSearch)
      handleScroll()
      handleResize()
      startSlideshow()
      
      // Iniciar carrusel de anuncios
      announcementInterval = setInterval(() => {
        currentAnnouncement.value = (currentAnnouncement.value + 1) % announcements.value.length
      }, 3500)
      
      // Manejar scroll al hash cuando venimos de otra página
      if (route.hash) {
        Promise.allSettled([categoriasPromise, productosPromise]).then(async () => {
          await nextTick()
          requestAnimationFrame(() => {
            const element = document.querySelector(route.hash)
            if (!element) return

            const headerOffset = 100
            const y = element.getBoundingClientRect().top + window.scrollY - headerOffset
            window.scrollTo({ top: y, behavior: 'smooth' })
          })
        })
      }
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
      window.removeEventListener('resize', handleResize)
      window.removeEventListener('user-logged-in', handleUserLoggedIn)
      document.removeEventListener('click', handleClickOutside)
      document.removeEventListener('click', handleClickOutsideSearch)
      if (slideInterval) clearTimeout(slideInterval)
      if (announcementInterval) clearInterval(announcementInterval)
    })

    return {
      productos,
      categorias,
      resenasDestacadas,
      resenasLoading,
      loading,
      error,
      cartCount,
      isScrolled,
      showFloatingBtns,
      windowWidth,
      mobileMenuOpen,
      openMobileMenu,
      closeMobileMenu,
      mobileSearchOpen,
      mobileSearchInputRef,
      openMobileSearch,
      closeMobileSearch,
      searchQuery,
      searchSuggestions,
      showSuggestions,
      searchInputRef,
      suggestionsRef,
      currentSlide,
      heroSlides,
      heroSlidesDesktop,
      activeHeroSlides,
      goToSlide,
      handleSearch,
      getSuggestions,
        getTotalSearchResults,
      scrollToProducto,
      handleSearch,
      scrollToTop,
      formatPrice,
      formatColorLabel,
      getItemPrice,
      getCartSubtotal,
      cargarProductos,
      irACategoria,
      irADetalle,
      agregarAlCarrito,
      toggleFavorito,
      isInWishlist,
      toggleUserMenu,
      handleMenuAction,
      cerrarSesion,
      showUserMenu,
      userMenuRef,
      // Announcements
      announcements,
      currentAnnouncement,
      isLoggedIn,
      currentUser,
      userInitial,
      // Toast
      toast,
      showToast,
      showCartToast,
      getInitials,
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
      getImageUrl,
      getProductoMediaUrl,
      getCartSourceUrl,
      getCartMediaUrl,
      isVideo,
      // Carousel categorías
      categoriasCarouselRef,
      catScrolled,
      scrollCategorias,
      onCatScroll
    }
  }
}
</script>

<style scoped>
/* Línea de truncado para nombres de productos */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ==========================================
   VIDEO HERO - CINEMÁTICO MÓVIL
   ========================================== */

/* (guia rapida movil usa utilidades Tailwind, no requiere CSS custom) */

/* Móvil: gradiente cinemático - limpio arriba, texto legible abajo */
@media (max-width: 767px) {
  .video-hero-overlay {
    background: linear-gradient(
      to top,
      rgba(0, 0, 0, 0.85) 0%,
      rgba(0, 0, 0, 0.4) 35%,
      rgba(0, 0, 0, 0.05) 55%,
      transparent 70%
    ) !important;
  }
}

/* Tablet/Desktop: overlay original más distribuido */
@media (min-width: 768px) {
  .video-hero-overlay {
    background: linear-gradient(
      to top,
      rgba(0, 0, 0, 0.75) 0%,
      rgba(0, 0, 0, 0.2) 40%,
      rgba(0, 0, 0, 0.35) 100%
    );
  }
}

/* Hero Slide Transition - Horizontal slide */
.hero-slide-enter-active,
.hero-slide-leave-active {
  transition: transform 0.6s ease-in-out;
  position: absolute;
  inset: 0;
  will-change: transform;
}
.hero-slide-enter-from {
  transform: translateX(100%);
}
.hero-slide-leave-to {
  transform: translateX(-100%);
}
.hero-slide-enter-to,
.hero-slide-leave-from {
  transform: translateX(0);
}

/* ==========================================
   SEARCH OVERLAY MÓVIL - Full-Screen
   ========================================== */
.search-overlay-mobile {
  display: flex;
  flex-direction: column;
}

/* Safe area para dispositivos con notch */
@supports (padding-top: env(safe-area-inset-top)) {
  .search-overlay-mobile {
    padding-top: env(safe-area-inset-top);
  }
}

/* Animación de entrada: fade + slide-up suave */
.search-overlay-enter-active {
  transition: opacity 0.25s ease-out, transform 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}
.search-overlay-leave-active {
  transition: opacity 0.2s ease-in, transform 0.2s ease-in;
}
.search-overlay-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.search-overlay-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.search-overlay-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.search-overlay-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

/* ==========================================
   OFF-CANVAS SIDEBAR MÓVIL
   ========================================== */
.sidebar-mobile {
  box-shadow: 8px 0 30px rgba(0, 0, 0, 0.1);
}

/* Safe area para dispositivos con notch */
@supports (padding-top: env(safe-area-inset-top)) {
  .sidebar-mobile {
    padding-top: env(safe-area-inset-top);
  }
}

/* Slide-in desde la izquierda */
.sidebar-enter-active {
  transition: transform 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}
.sidebar-leave-active {
  transition: transform 0.25s ease-in;
}
.sidebar-enter-from {
  transform: translateX(-100%);
}
.sidebar-enter-to {
  transform: translateX(0);
}
.sidebar-leave-from {
  transform: translateX(0);
}
.sidebar-leave-to {
  transform: translateX(-100%);
}

/* ==========================================
   CATEGORÍAS - CARRUSEL HORIZONTAL (MOBILE)
   Sharp & Bold Retail Style
   ========================================== */

/* Mobile only: horizontal carousel */
@media (max-width: 767px) {
  .categories-carousel {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 2px;

    /* Hide scrollbar - all browsers */
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  .categories-carousel::-webkit-scrollbar {
    display: none;
  }

  /* Each card: 85% width — photo is the protagonist */
  .categories-carousel .category-card-item {
    flex: 0 0 85%;
    min-width: 85%;
    scroll-snap-align: start;
  }

  .categories-carousel .category-card-item:first-child {
    margin-left: 0;
  }

  .categories-carousel .category-card-item:last-child {
    margin-right: 4px;
  }

  /* === SCROLL ARROW INDICATOR (Mercado Libre style) === */
  .cat-scroll-arrow {
    border-radius: 0;
    border: none;
    box-shadow: -4px 0 12px rgba(0, 0, 0, 0.12);
    animation: cat-arrow-pulse 1.8s ease-in-out infinite;
  }

  @keyframes cat-arrow-pulse {
    0%, 100% { transform: translateY(-50%) translateX(0); }
    50% { transform: translateY(-50%) translateX(4px); }
  }

  /* === ZERO RADIUS — Hard geometric edges === */
  .cat-card-inner {
    border-radius: 0 !important;
  }

  .cat-badge-sharp {
    border-radius: 0 !important;
  }

  /* === BOLD SANS-SERIF TYPOGRAPHY === */
  .cat-title-sharp {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  }

  .cat-cta-sharp {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  /* === HARD OVERLAY — dark bottom band for text legibility === */
  .cat-overlay-sharp {
    background: linear-gradient(
      to top,
      rgba(0, 0, 0, 0.82) 0%,
      rgba(0, 0, 0, 0.35) 40%,
      rgba(0, 0, 0, 0.05) 65%,
      transparent 80%
    );
  }

  /* === PRODUCT CARDS — Zero radius on mobile === */
  .product-card-mobile .rounded-xl,
  .product-card-mobile .rounded-3xl {
    border-radius: 0 !important;
  }

  .product-badge-mobile {
    border-radius: 0 !important;
  }

  /* Product grid: tighter gap on mobile */
  .product-grid-mobile {
    gap: 6px !important;
  }
}
</style>
