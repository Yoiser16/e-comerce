<template>
  <div class="min-h-screen bg-[#F9F8F6]">

    <!-- ========================================
         HEADER - Mobile App Style / Desktop Luxury
         ======================================== -->
    <header 
      :class="[
        'fixed left-0 right-0 z-50 transition-all duration-300',
        'bg-white border-b border-text-dark/5',
        isScrolled ? 'shadow-sm' : ''
      ]"
      style="top: 0;"
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
            <button 
              @click="mobileSearchOpen = true"
              class="w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target hover:bg-black/5"
            >
              <svg class="w-[18px] h-[18px] text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </button>
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
                {{ cartCount > 9 ? '9+' : cartCount }}
              </span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Desktop Header -->
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
            <div class="flex-1 max-w-xs mx-8">
              <div class="relative" ref="searchInputRef">
                <input 
                  type="text"
                  v-model="searchQuery"
                  @input="getSuggestions"
                  @keyup.enter="goToSearch()"
                  @focus="getSuggestions"
                  placeholder="Buscar extensiones, accesorios..."
                  class="w-full pl-10 pr-4 py-2 border rounded-full text-xs focus:outline-none focus:ring-1 transition-all duration-300 bg-white/80 border-text-dark/15 text-text-dark placeholder-text-dark/70 focus:border-text-dark/30 focus:bg-white focus:ring-text-dark/15"
                />
                <svg 
                  class="absolute left-3.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none text-text-medium"
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
                        v-for="prod in searchSuggestions"
                        :key="prod.id"
                        @click="goToProduct(prod.id)"
                        class="w-full px-4 py-3 hover:bg-[#f9f9f9] transition-colors flex items-center gap-3 text-left border-b border-text-dark/5 last:border-b-0"
                      >
                        <div class="w-10 h-10 rounded-lg overflow-hidden flex-shrink-0 bg-[#f9f9f9]">
                          <img
                            v-if="prod.imagen_principal"
                            :src="getImageUrl(prod.imagen_principal)"
                            :alt="prod.nombre"
                            class="w-full h-full object-cover"
                            @error="handleImageError"
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm text-text-dark truncate">{{ prod.nombre }}</p>
                        </div>
                        <p class="text-sm font-medium text-text-dark flex-shrink-0">
                          {{ formatearPrecio(prod.precio_monto) }}
                        </p>
                      </button>
                    </div>
                  </div>
                </transition>
              </div>
            </div>

            <!-- Navegación Desktop -->
            <nav class="flex items-center gap-7">
              <router-link to="/catalogo" class="nav-link-luxury">CATÁLOGO</router-link>
              <router-link to="/#categorias" class="nav-link-luxury">CATEGORÍAS</router-link>
              <router-link to="/#productos" class="nav-link-luxury">PRODUCTOS</router-link>
              <router-link to="/#mayoreo" class="nav-link-luxury">MAYOREO</router-link>
              <router-link to="/#testimonios" class="nav-link-luxury">RESEÑAS</router-link>
              <router-link to="/#contacto" class="nav-link-luxury">CONTACTO</router-link>
            </nav>

            <!-- Acciones Desktop -->
            <div class="flex items-center gap-1 ml-6">
              <!-- Usuario con dropdown -->
              <div class="relative" ref="userMenuRef">
                <button 
                  @click="toggleUserMenu"
                  class="w-9 h-9 rounded-full flex items-center justify-center transition-colors duration-300 touch-target hover:bg-black/5"
                  :class="[isLoggedIn ? 'border border-text-dark/20 hover:border-text-dark/40' : '']"
                >
                  <span v-if="isLoggedIn" class="text-xs font-medium text-text-dark">{{ userInitial }}</span>
                  <svg v-else class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                  </svg>
                </button>
                
                <!-- Desktop dropdown + Mobile bottom sheet -->
                <Teleport to="body">
                  <!-- Backdrop móvil -->
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
                      <div class="flex justify-center pt-3 pb-2" @click="showUserMenu = false">
                        <div class="w-10 h-1 bg-text-dark/15 rounded-full"></div>
                      </div>
                      <div v-if="isLoggedIn" class="px-5 pb-3 border-b border-black/5">
                        <p class="text-xs text-text-light">Hola,</p>
                        <p class="text-base text-text-dark font-semibold truncate">{{ currentUser?.nombre || currentUser?.email }}</p>
                      </div>
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
                      <div class="h-6"></div>
                    </div>
                  </transition>
                </Teleport>
              </div>
              
              <!-- Cart Desktop -->
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
                  {{ cartCount > 9 ? '9+' : cartCount }}
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
          <div class="flex items-center gap-3 px-4 py-3 border-b border-black/5">
            <button 
              @click="mobileSearchOpen = false"
              class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-nude-100 active:bg-nude-200 transition-colors flex-shrink-0"
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
                @keyup.enter="goToSearch()"
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
          <div class="flex-1 overflow-y-auto">
            <div v-if="!searchQuery.trim()" class="flex flex-col items-center justify-center pt-20 px-6">
              <svg class="w-12 h-12 text-text-light/30 mb-4" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
              <p class="text-sm text-text-light/60 text-center">Busca extensiones, accesorios y más</p>
            </div>
            <div v-else-if="showSuggestions && searchSuggestions.length > 0" class="divide-y divide-black/5">
              <button
                v-for="prod in searchSuggestions"
                :key="prod.id"
                @click="goToProduct(prod.id); mobileSearchOpen = false"
                class="w-full px-5 py-3.5 flex items-center gap-4 text-left active:bg-nude-50 transition-colors"
              >
                <div class="w-12 h-12 rounded-xl overflow-hidden flex-shrink-0 bg-nude-50 ring-1 ring-nude-200/30">
                  <img 
                    v-if="prod.imagen_principal"
                    :src="getImageUrl(prod.imagen_principal)"
                    :alt="prod.nombre"
                    class="w-full h-full object-cover"
                    @error="handleImageError"
                  />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-text-dark truncate">{{ prod.nombre }}</p>
                  <p class="text-xs font-semibold text-brand-600 mt-0.5">{{ formatearPrecio(prod.precio_monto) }}</p>
                </div>
                <svg class="w-4 h-4 text-text-light/30 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                </svg>
              </button>
            </div>
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
      <transition
        enter-active-class="transition-transform duration-300 ease-out"
        enter-from-class="-translate-x-full"
        enter-to-class="translate-x-0"
        leave-active-class="transition-transform duration-200 ease-in"
        leave-from-class="translate-x-0"
        leave-to-class="-translate-x-full"
      >
        <nav v-if="mobileMenuOpen" class="fixed top-0 left-0 z-[9997] w-[52%] max-w-[220px] h-full bg-white lg:hidden flex flex-col">
          <div class="flex items-center justify-between px-4 py-3.5 border-b border-black/5">
            <img src="/logo-kharis.png" alt="Kharis" class="h-8 w-auto object-contain" />
            <button @click="mobileMenuOpen = false" class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-nude-100 active:bg-nude-200 transition-colors">
              <svg class="w-4 h-4 text-text-dark" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="flex-1 overflow-y-auto py-2">
            <button v-if="isLoggedIn" @click="mobileMenuOpen = false; $router.push('/mi-cuenta')" class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04] w-full text-left">
              <div class="w-6 h-6 rounded-full bg-brand-50 flex items-center justify-center flex-shrink-0">
                <span class="text-[10px] font-semibold text-brand-600">{{ userInitial }}</span>
              </div>
              Mi Cuenta
            </button>
            <button v-else @click="mobileMenuOpen = false; handleMenuAction('login')" class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04] w-full text-left">
              <svg class="w-4 h-4 text-brand-600 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>
              Iniciar Sesión
            </button>
            <router-link to="/catalogo" @click="mobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]">
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" /></svg>
              Catálogo
            </router-link>
            <router-link to="/#categorias" @click="mobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]">
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z" /><path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6z" /></svg>
              Categorías
            </router-link>
            <router-link to="/#productos" @click="mobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]">
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" /></svg>
              Productos
            </router-link>
            <router-link to="/#mayoreo" @click="mobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]">
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 003.75-.615A2.993 2.993 0 009.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 002.25 1.016c.896 0 1.7-.393 2.25-1.016A3.001 3.001 0 0021 9.349m-18 0a2.998 2.998 0 00.832-2.078c.1-.695.564-1.267 1.168-1.521L7.5 4.5h9l2.5 1.25c.604.254 1.067.826 1.168 1.521A2.998 2.998 0 0021 9.35" /></svg>
              Mayoreo
            </router-link>
            <router-link to="/#testimonios" @click="mobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors border-b border-black/[0.04]">
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" /></svg>
              Reseñas
            </router-link>
            <router-link to="/#contacto" @click="mobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 text-[12px] tracking-[0.08em] uppercase text-text-dark font-medium active:bg-nude-50 transition-colors">
              <svg class="w-4 h-4 text-text-light/50 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" /></svg>
              Contacto
            </router-link>
          </div>
          <div class="px-4 py-4 border-t border-black/5">
            <p class="text-[9px] tracking-[0.12em] uppercase text-text-light/40 mb-2 font-medium">Síguenos</p>
            <div class="flex items-center gap-2">
              <a href="https://www.instagram.com/kharisdistribuidora" target="_blank" class="w-7 h-7 rounded-full bg-nude-50 flex items-center justify-center active:bg-nude-200 transition-colors">
                <svg class="w-3.5 h-3.5 text-text-dark/50" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
              </a>
              <a href="https://wa.me/18298776031" target="_blank" class="w-7 h-7 rounded-full bg-nude-50 flex items-center justify-center active:bg-nude-200 transition-colors">
                <svg class="w-3.5 h-3.5 text-text-dark/50" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
              </a>
              <a href="https://www.tiktok.com/@kharisdistribuidora" target="_blank" class="w-7 h-7 rounded-full bg-nude-50 flex items-center justify-center active:bg-nude-200 transition-colors">
                <svg class="w-3.5 h-3.5 text-text-dark/50" fill="currentColor" viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13.2a8.16 8.16 0 005.58 2.17V12a4.85 4.85 0 01-5.58-2.17V2h3.45a4.83 4.83 0 003.77 4.25v3.44h-1.64z"/></svg>
              </a>
            </div>
            <p class="text-[9px] text-text-light/35 mt-3">&copy; 2026 Kharis Distribuidora</p>
          </div>
        </nav>
      </transition>
    </Teleport>

    <!-- Spacer para el header fijo -->
    <div class="h-[48px] lg:h-[64px]"></div>

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

    <!-- Cart Drawer - Soft Beauty Style (Normalized from Home) -->
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
                @click="goToCheckout"
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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
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

// Normalized header state
const mobileMenuOpen = ref(false)
const mobileSearchOpen = ref(false)
const mobileSearchInputRef = ref(null)
const searchQuery = ref('')
const searchSuggestions = ref([])
const showSuggestions = ref(false)
const searchInputRef = ref(null)
const showUserMenu = ref(false)
const userMenuRef = ref(null)
const currentUser = ref(null)



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
const cartLoading = ref(false)
const isLoggedIn = ref(authService.isAuthenticated())

const userInitial = computed(() => {
  if (!currentUser.value) return ''
  const name = currentUser.value.nombre || currentUser.value.email || ''
  return name.charAt(0).toUpperCase()
})

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

// === Normalized header methods ===
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const handleMenuAction = (action) => {
  showUserMenu.value = false
  mobileMenuOpen.value = false
  switch (action) {
    case 'login':
      router.push('/login')
      break
    case 'cuenta':
      router.push('/mi-cuenta')
      break
    case 'pedidos':
      router.push('/mi-cuenta?tab=pedidos')
      break
    case 'favoritos':
      router.push('/favoritos')
      break
  }
}

const cerrarSesion = () => {
  showUserMenu.value = false
  mobileMenuOpen.value = false
  authService.logout()
  isLoggedIn.value = false
  currentUser.value = null
  router.push('/')
}

let searchTimeout = null
const getSuggestions = () => {
  clearTimeout(searchTimeout)
  if (searchQuery.value.trim().length < 2) {
    searchSuggestions.value = []
    showSuggestions.value = false
    return
  }
  searchTimeout = setTimeout(async () => {
    try {
      const res = await productosService.autocompletar(searchQuery.value.trim())
      searchSuggestions.value = (res.results || res || []).slice(0, 6)
      showSuggestions.value = searchSuggestions.value.length > 0
    } catch {
      searchSuggestions.value = []
      showSuggestions.value = false
    }
  }, 250)
}

const goToSearch = () => {
  if (!searchQuery.value.trim()) return
  mobileSearchOpen.value = false
  showSuggestions.value = false
  router.push({ path: '/catalogo', query: { q: searchQuery.value.trim() } })
}

const goToProduct = (id) => {
  showSuggestions.value = false
  mobileSearchOpen.value = false
  router.push(`/producto/${id}`)
}

const handleClickOutside = (e) => {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    showUserMenu.value = false
  }
  if (searchInputRef.value && !searchInputRef.value.contains(e.target)) {
    showSuggestions.value = false
  }
}
// === End normalized header methods ===

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
        const varianteId = item?.variante_id ?? null
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

  const requiereVariante = variantesDisponibles.value.length > 0
  if (requiereVariante && !varianteSeleccionada.value) {
    mensajeError.value = 'Selecciona una combinación de color y largo'
    mensaje.value = ''
    return
  }

  try {
    const precioUnitario = Number(
      varianteSeleccionada.value?.precio_monto ?? producto.value.precio_monto ?? producto.value.precio ?? 0
    )
    const itemKey = requiereVariante ? (varianteSeleccionada.value?.id || producto.value.id) : producto.value.id
    const varianteId = requiereVariante ? (varianteSeleccionada.value?.id || null) : null
    
    // Usar SIEMPRE localStorage - el carrito es local
    const items = loadCartFromLocal()
    const idx = items.findIndex((i) => (i.variante_id || i.producto_id) === itemKey)
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
        variante_id: varianteId,
        variante_sku: varianteSeleccionada.value?.sku || '',
        color: varianteSeleccionada.value?.color || '',
        largo: varianteSeleccionada.value?.largo || '',
        nombre: producto.value.nombre,
        imagen_url: getImageUrl(varianteSeleccionada.value?.imagen_url || producto.value.imagen_principal),
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
    openCartDrawer()
    
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
  document.body.style.overflow = ''
}

const openCartDrawer = async () => {
  showCartDrawer.value = true
  document.body.style.overflow = 'hidden'
  await loadCartItems()
}

const goToCheckout = () => {
  document.body.style.overflow = ''
  showCartDrawer.value = false
  router.push('/checkout')
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

// Helper para obtener URL de imagen del carrito
const getCartMediaUrl = (item) => {
  const url = getImageUrl(item?.imagen_url || item?.imagen_principal || item?.imagen)
  if (!url) return ''
  if (isVideo(url)) return ''
  return url
}

// Cargar items del carrito (localStorage + API si logged in)
const loadCartItems = async () => {
  cartLoading.value = true
  
  // Primero cargar desde cache local
  const localItems = loadCartFromLocal()
  if (localItems.length > 0) {
    carritoItems.value = localItems
    cartCount.value = localItems.reduce((sum, i) => sum + (i.cantidad || 1), 0)
  }
  
  // Si está logueado, sincronizar con backend
  if (isLoggedIn.value) {
    try {
      const data = await carritoService.getCarrito()
      if (data && data.items && data.items.length > 0) {
        carritoItems.value = data.items
        cartCount.value = data.items.reduce((sum, item) => sum + item.cantidad, 0)
        const newTotal = carritoItems.value.reduce((acc, i) => acc + getItemPrice(i), 0)
        saveCartToLocal(carritoItems.value, cartCount.value)
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
    saveCartToLocal(carritoItems.value, newCount)
    cartCount.value = newCount
    
    // Sincronizar con backend si está logueado
    if (isLoggedIn.value) {
      try {
        await carritoService.actualizarCantidad(
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
    const itemCantidad = carritoItems.value[itemIndex].cantidad || 1
    carritoItems.value.splice(itemIndex, 1)
    
    if (carritoItems.value.length === 0) {
      localStorage.removeItem(CART_STORAGE_KEY)
      localStorage.removeItem(CART_COUNT_KEY)
      cartCount.value = 0
    } else {
      const newCount = carritoItems.value.reduce((sum, item) => sum + (item.cantidad || 1), 0)
      cartCount.value = newCount
      saveCartToLocal(carritoItems.value, newCount)
    }
    
    // Sincronizar con backend si está logueado
    if (isLoggedIn.value) {
      try {
        const item = carritoItems.value.find(i => (i.variante_id || i.producto_id) === itemKey)
        await carritoService.eliminarProducto(
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

// Watch for route changes (when clicking related products)
watch(() => route.params.id, (newId) => {
  if (newId) {
    cargarProducto()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})

// Auto-focus mobile search input
watch(mobileSearchOpen, (val) => {
  if (val) {
    nextTick(() => {
      mobileSearchInputRef.value?.focus()
    })
  }
})

onMounted(async () => {
  cargarProducto()
  
  // Cargar carrito desde localStorage
  loadCartCount()
  carritoItems.value = loadCartFromLocal()
  
  // User data
  try {
    const u = JSON.parse(localStorage.getItem('user') || 'null')
    if (u) currentUser.value = u
  } catch {}
  
  
  window.addEventListener('scroll', handleScroll)
  window.addEventListener('click', handleClickOutside)
  window.addEventListener('user-logged-in', handleUserLoggedIn)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('click', handleClickOutside)
  window.removeEventListener('user-logged-in', handleUserLoggedIn)
  if (searchTimeout) clearTimeout(searchTimeout)
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
