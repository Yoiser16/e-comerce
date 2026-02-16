<template>
  <div class="min-h-screen bg-[#F9F8F6]">
    
    <!-- ========================================
         TOP BAR - Carrusel de Anuncios (Minimalista)
         ======================================== -->
    <div class="bg-white h-7 flex items-center justify-center overflow-hidden">
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
        'sticky top-0 z-50 transition-all duration-300',
        'bg-white border-b border-text-dark/5',
        isScrolled ? 'shadow-sm' : ''
      ]"
    >
      <!-- Mobile Header (lg:hidden) - Normalized Luxury Style -->
      <div class="lg:hidden">
        <div class="flex items-center justify-between px-4 py-2">
          <!-- Left: Hamburger -->
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target hover:bg-black/5"
          >
            <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
            </svg>
          </button>

          <!-- Center: Logo Wordmark -->
          <router-link to="/" class="absolute left-1/2 -translate-x-1/2 flex items-center">
            <span class="text-[22px] font-semibold tracking-[0.18em] text-[#111] uppercase" style="font-family: 'Cormorant Garamond', 'Playfair Display', serif;">KHARIS</span>
          </router-link>

          <!-- Right: Search + Cart -->
          <div class="flex items-center gap-1">
            <!-- Search -->
            <button 
              @click="mobileSearchOpen = true"
              class="w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target hover:bg-black/5"
            >
              <svg class="w-[18px] h-[18px] text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </button>
            <!-- Usuario dropdown (hidden on mobile, Teleport preserved for desktop) -->
            <div class="relative hidden" ref="userMenuRefMobile">
              <button 
                @click="toggleUserMenu"
                class="w-10 h-10 flex items-center justify-center rounded-full transition-colors"
                :class="[
                  isLoggedIn 
                    ? 'border border-text-dark/20'
                    : 'hover:bg-black/5'
                ]"
              >
                <!-- Si está logueado, mostrar inicial -->
                <span v-if="isLoggedIn" class="text-xs font-medium text-text-dark">
                  {{ userInitial }}
                </span>
                <!-- Si no está logueado, mostrar icono -->
                <svg v-else class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
              </button>
              
              <!-- Dropdown Menu -->
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
                      top: ((userMenuRefMobile?.getBoundingClientRect().bottom || userMenuRefDesktop?.getBoundingClientRect().bottom || 0) + 12) + 'px',
                      left: ((userMenuRefMobile?.getBoundingClientRect().right || userMenuRefDesktop?.getBoundingClientRect().right || 0) - 208) + 'px',
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
            <button 
              class="relative w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target hover:bg-black/5"
              @click="openCartDrawer()"
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
                          <video
                            v-if="producto.imagen_principal && isVideo(getImageUrl(producto.imagen_principal))"
                            :src="getImageUrl(producto.imagen_principal)"
                            class="w-full h-full object-cover"
                            muted
                            playsinline
                            loop
                            autoplay
                            preload="metadata"
                          ></video>
                          <img
                            v-else-if="producto.imagen_principal"
                            :src="getImageUrl(producto.imagen_principal)"
                            :alt="producto.nombre"
                            class="w-full h-full object-cover"
                            @error="handleImageError"
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
            <nav class="flex items-center gap-7">
              <router-link to="/catalogo" class="nav-link-luxury !text-brand-600">CATÁLOGO</router-link>
              <router-link to="/#categorias" class="nav-link-luxury">CATEGORÍAS</router-link>
              <router-link to="/#productos" class="nav-link-luxury">PRODUCTOS</router-link>
              <router-link to="/#mayoreo" class="nav-link-luxury">MAYOREO</router-link>
              <router-link to="/#testimonios" class="nav-link-luxury">RESEÑAS</router-link>
              <router-link to="/#contacto" class="nav-link-luxury">CONTACTO</router-link>
            </nav>

            <!-- Acciones Desktop -->
            <div class="flex items-center gap-1 ml-6">
              <!-- Usuario con dropdown -->
              <div class="relative" ref="userMenuRefDesktop">
                <button 
                  @click="toggleUserMenu"
                  class="w-10 h-10 rounded-full flex items-center justify-center hover:bg-[#f5f5f5] transition-colors"
                  :class="[
                    isLoggedIn 
                      ? 'border border-text-dark/20'
                      : ''
                  ]"
                >
                  <!-- Si está logueado, mostrar inicial -->
                  <span v-if="isLoggedIn" class="text-xs font-medium text-text-dark">
                    {{ userInitial }}
                  </span>
                  <!-- Si no está logueado, mostrar icono -->
                  <svg v-else class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                  </svg>
                </button>
              </div>
              <button 
                class="relative w-10 h-10 rounded-full flex items-center justify-center hover:bg-[#f5f5f5] transition-colors"
                @click="openCartDrawer()"
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

    <!-- Mobile Search Overlay (Full-Screen) -->
    <Teleport to="body">
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="mobileSearchOpen" class="fixed inset-0 z-[9998] bg-white lg:hidden">
          <!-- Header del Search overlay -->
          <div class="flex items-center gap-3 px-4 py-3 border-b border-black/5">
            <button 
              @click="mobileSearchOpen = false"
              class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-nude-100 active:bg-nude-200 transition-colors flex-shrink-0"
              aria-label="Cerrar búsqueda"
            >
              <svg class="w-5 h-5 text-text-dark" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
              </svg>
            </button>
            <div class="flex-1 relative">
              <input 
                ref="mobileSearchInputRef"
                type="text"
                v-model="searchQuery"
                @input="getSuggestions"
                @keyup.enter="handleSearch()"
                placeholder="Buscar extensiones, accesorios..."
                class="w-full py-2.5 px-4 bg-[#F5F5F5] rounded-full text-sm text-text-dark placeholder-text-light/50 focus:outline-none focus:bg-[#EFEFEF] transition-colors"
              />
            </div>
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
            <!-- Estado vacío -->
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
                @click="verProducto(producto.id); mobileSearchOpen = false"
                class="w-full px-5 py-3.5 flex items-center gap-4 text-left active:bg-nude-50 transition-colors"
              >
                <div class="w-12 h-12 rounded-xl overflow-hidden flex-shrink-0 bg-nude-50 ring-1 ring-nude-200/30">
                  <video
                    v-if="producto.imagen_principal && isVideo(getImageUrl(producto.imagen_principal))"
                    :src="getImageUrl(producto.imagen_principal)"
                    class="w-full h-full object-cover"
                    muted playsinline loop autoplay preload="metadata"
                  ></video>
                  <img 
                    v-else-if="producto.imagen_principal"
                    :src="getImageUrl(producto.imagen_principal)"
                    :alt="producto.nombre"
                    class="w-full h-full object-cover"
                    @error="handleImageError"
                  />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-text-dark truncate">{{ producto.nombre }}</p>
                  <p class="text-xs font-semibold text-brand-600 mt-0.5">{{ formatearPrecio(producto.precio_monto) }}</p>
                </div>
                <svg class="w-4 h-4 text-text-light/30 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
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

    <!-- Mobile Menu Off-Canvas Sidebar -->
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
          @click="mobileMenuOpen = false"
        ></div>
      </transition>

      <!-- Sidebar Panel -->
      <transition
        enter-active-class="transition-transform duration-300 ease-out"
        enter-from-class="-translate-x-full"
        enter-to-class="translate-x-0"
        leave-active-class="transition-transform duration-200 ease-in"
        leave-from-class="translate-x-0"
        leave-to-class="-translate-x-full"
      >
        <nav v-if="mobileMenuOpen" class="fixed top-0 left-0 z-[9997] w-[52%] max-w-[220px] h-full bg-white lg:hidden flex flex-col">
          
          <!-- Header del Sidebar -->
          <div class="flex items-center justify-between px-4 py-3.5 border-b border-black/5">
            <img src="/logo-kharis.png" alt="Kharis" class="h-8 w-auto object-contain" />
            <button 
              @click="mobileMenuOpen = false"
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
              @click="mobileMenuOpen = false; $router.push('/mi-cuenta')"
              class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04] w-full text-left"
            >
              <div class="w-6 h-6 rounded-full bg-brand-50 flex items-center justify-center flex-shrink-0">
                <span class="text-[10px] font-semibold text-brand-600">{{ userInitial }}</span>
              </div>
              Mi Cuenta
            </button>
            <button 
              v-else
              @click="mobileMenuOpen = false; handleMenuAction('login')"
              class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04] w-full text-left"
            >
              <svg class="w-4 h-4 text-brand-600 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
              Iniciar Sesión
            </button>
            <router-link 
              to="/catalogo" 
              @click="mobileMenuOpen = false" 
              class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
            >
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
              </svg>
              Catálogo
            </router-link>
            <router-link 
              to="/#categorias" 
              @click="mobileMenuOpen = false" 
              class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
            >
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6z" />
              </svg>
              Categorías
            </router-link>
            <router-link 
              to="/#productos" 
              @click="mobileMenuOpen = false" 
              class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
            >
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
              </svg>
              Productos
            </router-link>
            <router-link 
              to="/#mayoreo" 
              @click="mobileMenuOpen = false" 
              class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
            >
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 003.75-.615A2.993 2.993 0 009.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 002.25 1.016c.896 0 1.7-.393 2.25-1.016A3.001 3.001 0 0021 9.349m-18 0a2.998 2.998 0 00.832-2.078c.1-.695.564-1.267 1.168-1.521L7.5 4.5h9l2.5 1.25c.604.254 1.067.826 1.168 1.521A2.998 2.998 0 0021 9.35" />
              </svg>
              Mayoreo
            </router-link>
            <router-link 
              to="/#testimonios" 
              @click="mobileMenuOpen = false" 
              class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]"
            >
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
              </svg>
              Reseñas
            </router-link>
            <router-link 
              to="/#contacto" 
              @click="mobileMenuOpen = false" 
              class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors"
            >
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
              </svg>
              Contacto
            </router-link>
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
    <div class="lg:hidden bg-white border-b border-text-dark/5">
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
          <div class="sticky top-16 space-y-5 max-h-[calc(100vh-80px)] overflow-y-auto pr-2 scrollbar-thin">
            
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
                    <div class="absolute inset-0 bg-[#F0E6DC] rounded-full"></div>
                    <!-- Active Track -->
                    <div 
                      class="absolute h-full bg-[#D4A85A] rounded-full"
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
                        precioRangoMax <= 200000 ? 'border-[#D4A85A] bg-[#FAF5F2] text-text-dark' : 'border-[#D4A85A]/30 hover:border-[#D4A85A]/60 text-text-medium'
                      ]"
                    >
                      Hasta $200K
                    </button>
                    <button 
                      @click="setQuickPrice(0, 500000)"
                      :class="[
                        'px-3 py-1.5 text-xs rounded-full border transition-colors',
                        precioRangoMax > 200000 && precioRangoMax <= 500000 ? 'border-[#D4A85A] bg-[#FAF5F2] text-text-dark' : 'border-[#D4A85A]/30 hover:border-[#D4A85A]/60 text-text-medium'
                      ]"
                    >
                      Hasta $500K
                    </button>
                    <button 
                      @click="setQuickPrice(0, precioMaxDisponible)"
                      :class="[
                        'px-3 py-1.5 text-xs rounded-full border transition-colors',
                        precioRangoMax > 500000 ? 'border-[#D4A85A] bg-[#FAF5F2] text-text-dark' : 'border-[#D4A85A]/30 hover:border-[#D4A85A]/60 text-text-medium'
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
                <video
                  v-if="producto.imagen_principal && isVideo(getImageUrl(producto.imagen_principal))"
                  :src="getImageUrl(producto.imagen_principal)"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  muted
                  playsinline
                  loop
                  autoplay
                  preload="metadata"
                ></video>
                <img
                  v-else-if="producto.imagen_principal"
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
                    class="absolute h-full bg-[#D4A85A] rounded-full"
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
         DRAWER DEL CARRITO - Soft Beauty Style (Normalized)
         ======================================== -->
    <Teleport to="body">
      <transition
        enter-active-class="transition-opacity duration-300 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="showCartDrawer"
          class="fixed inset-0 bg-black/40 z-50"
          @click="closeCartDrawer"
        ></div>
      </transition>
      
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

          <!-- Barra de Progreso Envío Gratis -->
          <div v-if="getCartSubtotal() < 300000 && carritoItems.length > 0" class="px-6 py-4 bg-gradient-to-r from-nude-50 to-white">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs text-text-medium">
                Te faltan {{ formatearPrecio(300000 - getCartSubtotal()) }} para envío gratis
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
          <div v-else-if="carritoItems.length > 0" class="px-6 py-4 bg-gradient-to-r from-green-50 to-white">
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
            <div v-else-if="carritoItems.length === 0" class="flex flex-col items-center justify-center h-72 text-center px-4">
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
                v-for="item in carritoItems" 
                :key="item.variante_id || item.producto_id"
                class="flex gap-4 p-3 bg-white rounded-xl border border-nude-100 hover:border-nude-200 transition-colors"
              >
                <!-- Imagen del producto -->
                <div class="w-[90px] h-[90px] bg-gradient-to-br from-nude-50 to-nude-100 rounded-xl flex-shrink-0 overflow-hidden flex items-center justify-center">
                  <img 
                    v-if="getCartMediaUrl(item)" 
                    :src="getCartMediaUrl(item)" 
                    :alt="item.nombre"
                    class="w-full h-full object-cover"
                    @error="handleImageError"
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
                    <p v-if="item.color || item.largo" class="text-xs text-text-light">
                      <span v-if="item.color">Color: {{ formatColorLabel(item.color) }}</span>
                      <span v-if="item.color && item.largo"> · </span>
                      <span v-if="item.largo">Largo: {{ item.largo }}</span>
                    </p>
                    
                    <!-- Selector de Cantidad - Estilo Píldora -->
                    <div class="flex items-center gap-2 mt-2">
                      <div class="inline-flex items-center border border-nude-200 rounded-full">
                        <button 
                          @click="updateQuantity(item.variante_id || item.producto_id, (item.cantidad || 1) - 1)"
                          class="w-7 h-7 flex items-center justify-center text-text-medium hover:text-text-dark transition-colors"
                          :disabled="(item.cantidad || 1) <= 1"
                        >
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" d="M5 12h14" />
                          </svg>
                        </button>
                        <span class="w-8 text-center text-sm font-medium text-text-dark">{{ item.cantidad || 1 }}</span>
                        <button 
                          @click="updateQuantity(item.variante_id || item.producto_id, (item.cantidad || 1) + 1)"
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
                    {{ formatearPrecio(getItemPrice(item)) }}
                  </p>
                </div>
                
                <!-- Eliminar -->
                <button 
                  @click.stop="removeFromCart(item.variante_id || item.producto_id)"
                  class="self-start mt-1 w-8 h-8 rounded-full flex items-center justify-center bg-red-50 hover:bg-red-100 transition-colors group"
                  title="Eliminar producto"
                >
                  <svg class="w-4 h-4 text-red-400 group-hover:text-red-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Footer - Fondo Nude, Botón Pill con Glow -->
          <div v-if="carritoItems.length > 0" class="border-t border-nude-200" style="background: #FDFBF7;">
            <div class="px-6 py-4 space-y-2">
              <div class="flex items-center justify-between text-sm">
                <span class="text-text-medium">Subtotal</span>
                <span class="text-text-dark">{{ formatearPrecio(getCartSubtotal()) }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-text-medium">Envío</span>
                <span class="text-text-medium italic">Por calcular</span>
              </div>
              <div class="flex items-center justify-between pt-3 border-t border-nude-200">
                <span class="text-text-dark font-medium">Total</span>
                <span class="font-luxury text-2xl font-bold text-text-dark">{{ formatearPrecio(getCartSubtotal()) }}</span>
              </div>
            </div>
            
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
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL, getImageUrl } from '../services/api'
import { authService, carritoService as carritoServiceImport } from '../services/productos'
import { formatColorLabel } from '@/utils/colorLabels'

const router = useRouter()
const route = useRoute()

// Estados principales
const productos = ref([])
const categorias = ref([])
const loading = ref(true)
const cartCount = ref(0)
const showCartDrawer = ref(false)
const carritoItems = ref([])
const cartLoading = ref(false)
const videoPosters = ref({})

// Usuario y menú
const isLoggedIn = ref(authService.isAuthenticated())
const currentUser = ref(JSON.parse(localStorage.getItem('user') || 'null'))
const showUserMenu = ref(false)
const userMenuRefMobile = ref(null)
const userMenuRefDesktop = ref(null)

// Header
const isScrolled = ref(false)
const mobileMenuOpen = ref(false)
const mobileSearchOpen = ref(false)
const mobileSearchInputRef = ref(null)

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

// Computed para usuario
const userInitial = computed(() => {
  if (!currentUser.value) return ''
  return (currentUser.value.nombre || currentUser.value.email || 'U')[0].toUpperCase()
})

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
// Métodos
const cargarProductos = async () => {
  try {
    const { data } = await axios.get(`${API_BASE_URL}/api/v1/productos/`)
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
    const { data } = await axios.get(`${API_BASE_URL}/api/v1/categorias/?solo_activas=true`)
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
      const rawItems = parsed?.items ? parsed.items : parsed
      const normalized = Array.isArray(rawItems) ? rawItems : []
      carritoItems.value = normalized.map((item) => {
        const productoId = item?.producto_id ?? item?.id
        const varianteId = item?.variante_id ?? null
        return {
          ...item,
          producto_id: productoId,
          variante_id: varianteId,
          id: productoId,
          precio_unitario: item?.precio_unitario ?? item?.precio_monto ?? item?.precio ?? 0
        }
      })
    } else {
      carritoItems.value = []
    }
  } catch (err) {
    carritoItems.value = []
  }
}

const irACheckout = () => {
  document.body.style.overflow = ''
  showCartDrawer.value = false
  router.push('/checkout')
}

const closeCartDrawer = () => {
  showCartDrawer.value = false
  document.body.style.overflow = ''
}

const openCartDrawer = async () => {
  showCartDrawer.value = true
  document.body.style.overflow = 'hidden'
  await loadCartItems()
}

// Helper para obtener precio del item del carrito
const getItemPrice = (item) => {
  const price = item.subtotal || item.precio_unitario || item.precio || item.precio_final || item.precio_monto || 0
  const cantidad = item.cantidad || 1
  if (item.subtotal) return item.subtotal
  return price * cantidad
}

// Helper para calcular el subtotal del carrito
const getCartSubtotal = () => {
  if (!carritoItems.value || carritoItems.value.length === 0) return 0
  return carritoItems.value.reduce((total, item) => {
    return total + getItemPrice(item)
  }, 0)
}

// Cargar items del carrito (localStorage + API si logged in)
const loadCartItems = async () => {
  cartLoading.value = true
  
  // Primero cargar desde cache local
  loadCartFromLocal()
  
  // Si está logueado, sincronizar con backend
  if (isLoggedIn.value) {
    try {
      const data = await carritoServiceImport.getCarrito()
      if (data && data.items && data.items.length > 0) {
        carritoItems.value = data.items
        cartCount.value = data.items.reduce((sum, item) => sum + item.cantidad, 0)
        localStorage.setItem('kharis_cart_cache', JSON.stringify({ items: data.items, timestamp: Date.now() }))
        localStorage.setItem('kharis_cart_count', String(cartCount.value))
        if (data.id) localStorage.setItem('kharis_cart_id', data.id)
      }
    } catch (err) {
      if (err.response?.status !== 401 && err.response?.status !== 404) {
        console.error('Error cargando carrito:', err)
      }
    }
  }
  
  cartLoading.value = false
}

// Actualizar cantidad de un producto en el carrito
const updateQuantity = async (itemKey, nuevaCantidad) => {
  if (nuevaCantidad < 1) {
    await removeFromCart(itemKey)
    return
  }
  
  const itemIndex = carritoItems.value.findIndex(i => (i.variante_id || i.producto_id) === itemKey)
  if (itemIndex >= 0) {
    carritoItems.value[itemIndex].cantidad = nuevaCantidad
    const item = carritoItems.value[itemIndex]
    item.subtotal = (item.precio_unitario || item.precio || item.precio_monto || 0) * nuevaCantidad
    
    const newCount = carritoItems.value.reduce((sum, i) => sum + i.cantidad, 0)
    localStorage.setItem('kharis_cart_cache', JSON.stringify({ items: carritoItems.value, timestamp: Date.now() }))
    localStorage.setItem('kharis_cart_count', String(newCount))
    cartCount.value = newCount
    
    if (isLoggedIn.value) {
      try {
        await carritoServiceImport.actualizarCantidad(
          item.producto_id,
          item.variante_id,
          nuevaCantidad,
          localStorage.getItem('kharis_cart_id')
        )
      } catch (err) {
        console.warn('Error sync cantidad con backend:', err)
      }
    }
  }
}

// Eliminar producto del carrito
const removeFromCart = async (itemKey) => {
  const itemIndex = carritoItems.value.findIndex(i => (i.variante_id || i.producto_id) === itemKey)
  if (itemIndex >= 0) {
    carritoItems.value.splice(itemIndex, 1)
    
    if (carritoItems.value.length === 0) {
      localStorage.removeItem('kharis_cart_cache')
      localStorage.removeItem('kharis_cart_count')
      cartCount.value = 0
    } else {
      const newCount = carritoItems.value.reduce((sum, item) => sum + (item.cantidad || 1), 0)
      cartCount.value = newCount
      localStorage.setItem('kharis_cart_cache', JSON.stringify({ items: carritoItems.value, timestamp: Date.now() }))
      localStorage.setItem('kharis_cart_count', String(newCount))
    }
    
    if (isLoggedIn.value) {
      try {
        const item = carritoItems.value.find(i => (i.variante_id || i.producto_id) === itemKey)
        await carritoServiceImport.eliminarProducto(
          item?.producto_id,
          item?.variante_id,
          localStorage.getItem('kharis_cart_id')
        )
      } catch (backendErr) {
        console.warn('Error sync eliminar con backend:', backendErr)
      }
    }
  }
}

// getImageUrl is imported from '../services/api'

const isVideo = (url) => {
  if (!url) return false
  const cleanUrl = url.split('?')[0].toLowerCase()
  return ['.mp4', '.webm', '.ogg', '.mov'].some(ext => cleanUrl.endsWith(ext))
}

const createVideoPoster = (url) => {
  return new Promise((resolve) => {
    try {
      const video = document.createElement('video')
      video.src = url
      video.muted = true
      video.playsInline = true
      video.crossOrigin = 'anonymous'

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

const getCartMediaUrl = (item) => {
  const url = getImageUrl(item?.imagen_url || item?.imagen_principal || item?.imagen)
  if (!url) return ''
  if (isVideo(url)) {
    ensureVideoPoster(url)
    return videoPosters.value[url] || ''
  }
  return url
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
const getDefaultVariante = (producto) => {
  const variantes = Array.isArray(producto?.variantes) ? producto.variantes : []
  return variantes.find(v => v.activo !== false && (v.stock_actual ?? 0) > 0) || variantes[0] || null
}

const addToCart = (producto) => {
  // Cargar carrito actual
  loadCartFromLocal()

  const varianteSeleccionada = getDefaultVariante(producto)
  const requiereVariante = Array.isArray(producto?.variantes) && producto.variantes.length > 0
  if (requiereVariante && !varianteSeleccionada) {
    showToastMessage('Selecciona una combinación disponible')
    return
  }
  const precioUnitario = Number(
    varianteSeleccionada?.precio_monto ?? producto.precio_monto ?? producto.precio ?? 0
  )
  const itemKey = requiereVariante ? (varianteSeleccionada?.id || producto.id) : producto.id
  const varianteId = requiereVariante ? (varianteSeleccionada?.id || null) : null
  
  const existingIdx = carritoItems.value.findIndex(item => (item.variante_id || item.producto_id || item.id) === itemKey)
  
  if (existingIdx > -1) {
    carritoItems.value[existingIdx].cantidad += 1
  } else {
    carritoItems.value.push({
      producto_id: producto.id,
      variante_id: varianteId,
      id: producto.id,
      nombre: producto.nombre,
      variante_sku: varianteSeleccionada?.sku || '',
      color: varianteSeleccionada?.color || '',
      largo: varianteSeleccionada?.largo || '',
      precio_monto: precioUnitario,
      precio_unitario: precioUnitario,
      cantidad: 1,
      imagen_url: varianteSeleccionada?.imagen_url || producto.imagen_principal
    })
  }
  
  // Guardar en localStorage (mismo formato que Home.vue espera)
  const total = carritoItems.value.reduce((acc, item) => {
    const unit = item.precio_unitario ?? item.precio_monto ?? item.precio ?? 0
    const qty = item.cantidad ?? 1
    return acc + unit * qty
  }, 0)
  localStorage.setItem('kharis_cart_cache', JSON.stringify({ items: carritoItems.value, total, timestamp: Date.now() }))
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

// Menú de usuario
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
  localStorage.removeItem('carrito')
  localStorage.removeItem('wishlist')
  currentUser.value = null
  isLoggedIn.value = false
  showUserMenu.value = false
  cartCount.value = 0
  carritoItems.value = []
  wishlist.value = []
  router.push('/')
}

const handleClickOutside = (event) => {
  if (searchInputRef.value && !searchInputRef.value.contains(event.target)) {
    showSuggestions.value = false
  }
  if ((userMenuRefMobile.value && !userMenuRefMobile.value.contains(event.target)) &&
      (userMenuRefDesktop.value && !userMenuRefDesktop.value.contains(event.target))) {
    showUserMenu.value = false
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
  if (announcementInterval) clearInterval(announcementInterval)
})

// Mantener filtro en sync si cambia la query
watch(
  () => route.query.categoria,
  (nuevaCategoria) => {
    filtroCategoria.value = nuevaCategoria || null
  }
)

// Auto-focus en el input de búsqueda cuando se abre el overlay
watch(mobileSearchOpen, (isOpen) => {
  if (isOpen) {
    nextTick(() => {
      mobileSearchInputRef.value?.focus()
    })
  } else {
    searchQuery.value = ''
    searchSuggestions.value = []
    showSuggestions.value = false
  }
})
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
  background: linear-gradient(135deg, #D4A85A 0%, #C9A962 100%);
  border: 3px solid white;
  box-shadow: 0 2px 10px rgba(201, 169, 98, 0.28);
  cursor: pointer;
  margin-top: -8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.range-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 4px 14px rgba(201, 169, 98, 0.36);
}

.range-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #D4A85A 0%, #C9A962 100%);
  border: 3px solid white;
  box-shadow: 0 2px 10px rgba(201, 169, 98, 0.28);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.range-slider::-moz-range-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 4px 14px rgba(201, 169, 98, 0.36);
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
  background: linear-gradient(135deg, #D4A85A 0%, #C9A962 100%);
  border: 2px solid white;
  box-shadow: 0 2px 10px rgba(201, 169, 98, 0.22);
  cursor: pointer;
  margin-top: -7px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.range-slider-simple::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(201, 169, 98, 0.32);
}

.range-slider-simple::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #D4A85A 0%, #C9A962 100%);
  border: 2px solid white;
  box-shadow: 0 2px 10px rgba(201, 169, 98, 0.22);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.range-slider-simple::-moz-range-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(201, 169, 98, 0.32);
}

.range-slider-simple::-webkit-slider-runnable-track {
  height: 4px;
  background: #F0E6DC;
  border-radius: 2px;
}

.range-slider-simple::-moz-range-track {
  height: 4px;
  background: #F0E6DC;
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
