<template>
  <header 
    ref="headerRef"
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 ease-in-out"
    :class="[
      'shadow-lg shadow-black/10',
      isVisible ? 'translate-y-0' : '-translate-y-full'
    ]"
  >
    <!-- Gradient Accent Line (top) -->
    <div class="h-[3px] bg-gradient-to-r from-[#E91E63] via-[#FF6B9D] to-[#C9A962]"></div>

    <!-- Top Utility Bar (Desktop) -->
    <div class="hidden lg:block border-b border-white/[0.06] bg-[#1B1D21]">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-9 text-xs">
          <!-- Left: Address -->
          <router-link 
            to="/portal/cuenta?tab=addresses" 
            class="flex items-center gap-1.5 text-gray-400 hover:text-white transition-colors group"
          >
            <svg class="w-3.5 h-3.5 text-[#E91E63]/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
            </svg>
            <span v-if="defaultAddress">
              Enviar a <span class="text-white font-medium group-hover:text-[#E91E63]">{{ defaultAddress.ciudad }}</span>
            </span>
            <span v-else class="text-gray-500 hover:text-gray-300">Agregar dirección de envío</span>
          </router-link>
          
          <!-- Right: Help & WhatsApp -->
          <div class="flex items-center gap-4 text-gray-400">
            <router-link to="/portal/ayuda" class="hover:text-white transition-colors">
              Ayuda / PQR
            </router-link>
            <span class="text-gray-600">|</span>
            <a 
              href="https://wa.me/573001234567" 
              target="_blank" 
              class="flex items-center gap-1.5 text-emerald-400 hover:text-emerald-300 transition-colors font-medium"
            >
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
              </svg>
              WhatsApp B2B
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Header -->
    <div class="bg-[#232529]">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-14 lg:h-[68px] gap-3 lg:gap-5">
          
          <!-- Left: Logo & Nav -->
          <div class="flex items-center gap-3 lg:gap-7">
            <!-- Logo -->
            <router-link to="/portal" class="flex items-center gap-2.5 group shrink-0">
              <div class="w-9 h-9 lg:w-10 lg:h-10 rounded-xl bg-gradient-to-br from-[#E91E63] to-[#AD1457] p-[2px] shadow-lg shadow-[#E91E63]/20 group-hover:shadow-[#E91E63]/40 transition-shadow">
                <div class="w-full h-full rounded-[10px] bg-[#232529] flex items-center justify-center">
                  <img src="/logo-kharis.png" alt="Kharis Pro" class="w-6 h-6 lg:w-7 lg:h-7 object-contain" />
                </div>
              </div>
              <div class="hidden sm:block">
                <span class="text-white font-luxury text-base lg:text-lg tracking-wider">KHARIS PRO</span>
                <span class="block text-[#E91E63]/60 text-[9px] tracking-[0.2em] uppercase font-semibold">Portal Mayoristas</span>
              </div>
            </router-link>

            <!-- Desktop Navigation -->
            <nav class="hidden lg:flex items-center gap-0.5">
              <!-- Categories Dropdown -->
              <div 
                class="relative" 
                ref="categoriesMenuRef" 
                @mouseenter="showCategoriesMenu = true" 
                @mouseleave="showCategoriesMenu = false"
              >
                <button 
                  class="px-3 py-2 text-[13px] font-medium text-gray-300 hover:text-white transition-all flex items-center gap-1.5 rounded-lg hover:bg-white/[0.07]"
                >
                  Categorías
                  <svg 
                    class="w-4 h-4 transition-transform duration-200" 
                    :class="{ 'rotate-180': showCategoriesMenu }" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                <!-- Dropdown Menu -->
                <transition name="dropdown">
                  <div 
                    v-if="showCategoriesMenu" 
                    class="absolute left-0 top-full mt-1 w-64 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden"
                  >
                    <div class="py-2">
                      <router-link 
                        v-for="cat in categorias" 
                        :key="cat.id" 
                        :to="`/portal/catalogo?categoria=${cat.slug}`"
                        class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-[#FCE4EC] hover:text-[#E91E63] transition-colors"
                        @click="showCategoriesMenu = false"
                      >
                        <span class="w-1.5 h-1.5 rounded-full bg-[#E91E63]/60"></span>
                        {{ cat.nombre }}
                      </router-link>
                      <div class="border-t border-gray-100 mt-2 pt-2">
                        <router-link 
                          to="/portal/catalogo"
                          class="flex items-center justify-between px-4 py-2.5 text-sm text-[#E91E63] font-medium hover:bg-[#FCE4EC] transition-colors"
                          @click="showCategoriesMenu = false"
                        >
                          Ver todo el catálogo
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                          </svg>
                        </router-link>
                      </div>
                    </div>
                  </div>
                </transition>
              </div>

              <router-link 
                to="/portal/catalogo?oferta=true"
                class="px-3 py-2 text-[13px] font-bold text-[#FF6B9D] hover:text-white hover:bg-[#E91E63]/20 rounded-lg transition-all"
              >
                OFERTAS
              </router-link>

              <router-link 
                to="/portal/cupones"
                class="px-3 py-2 text-[13px] font-medium text-amber-400 hover:text-amber-300 hover:bg-white/[0.07] rounded-lg transition-all flex items-center gap-1.5"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 14.25l6-6m4.5-3.493V21.75l-3.75-1.5-3.75 1.5-3.75-1.5-3.75 1.5V4.757c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0c1.1.128 1.907 1.077 1.907 2.185zM9.75 9h.008v.008H9.75V9zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm4.125 4.5h.008v.008h-.008V13.5zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
                CUPONES
              </router-link>

              <router-link 
                to="/portal/catalogo?nuevo=true"
                class="px-3 py-2 text-[13px] font-medium text-emerald-400 hover:text-emerald-300 hover:bg-white/[0.07] rounded-lg transition-all flex items-center gap-1.5"
              >
                NUEVOS
                <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
              </router-link>
            </nav>
          </div>

          <!-- Center: Search Bar (Desktop) - Amazon/ML Style -->
          <div class="hidden md:flex flex-1 max-w-xl lg:max-w-2xl mx-4 lg:mx-6">
            <div class="relative w-full group">
              <div 
                class="flex items-center w-full rounded-xl overflow-hidden transition-all duration-200 ring-2 ring-transparent group-focus-within:ring-[#E91E63] group-focus-within:ring-offset-1 group-focus-within:ring-offset-[#232529]"
              >
                <div class="flex items-center justify-center w-10 h-[42px] bg-gray-100">
                  <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input 
                  v-model="searchQuery"
                  type="text" 
                  placeholder="Buscar productos, SKU, categorías..."
                  class="flex-1 h-[42px] px-3 bg-white text-sm text-gray-900 placeholder:text-gray-400 outline-none"
                  @keydown.enter="handleSearch"
                  @focus="showSearchSuggestions = true"
                />
                <button 
                  @click="handleSearch"
                  class="h-[42px] px-5 bg-gradient-to-r from-[#E91E63] to-[#C2185B] hover:from-[#FF1A6D] hover:to-[#E91E63] text-white transition-all flex items-center gap-2 font-bold text-sm"
                >
                  <span class="hidden lg:inline">Buscar</span>
                  <svg class="w-4 h-4 lg:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
              </div>
              
              <!-- Search Suggestions Dropdown -->
              <transition name="dropdown">
                <div 
                  v-if="showSearchSuggestions && searchQuery.length >= 2"
                  class="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden z-50"
                >
                  <div v-if="searchLoading" class="p-4 text-center">
                    <div class="w-5 h-5 border-2 border-[#E91E63] border-t-transparent rounded-full animate-spin mx-auto"></div>
                  </div>
                  <div v-else-if="searchResults.length > 0" class="divide-y divide-gray-50 max-h-[400px] overflow-y-auto">
                    <router-link 
                      v-for="product in searchResults.slice(0, 6)" 
                      :key="product.id" 
                      :to="`/portal/producto/${product.id}`"
                      class="flex items-center gap-3 p-3 hover:bg-gray-50 transition-colors"
                      @click="showSearchSuggestions = false"
                    >
                      <img 
                        :src="product.imagen_principal || '/placeholder.png'" 
                        :alt="product.nombre"
                        class="w-12 h-12 object-cover rounded-lg bg-gray-100"
                      />
                      <div class="flex-1 min-w-0">
                        <h4 class="font-medium text-gray-900 text-sm truncate">{{ product.nombre }}</h4>
                        <p class="text-xs text-gray-500">{{ product.categoria_nombre }}</p>
                        <span class="text-[#E91E63] font-bold text-sm">${{ formatPrice(product.precio_mayorista || product.precio) }}</span>
                      </div>
                    </router-link>
                    <button 
                      @click="handleSearch"
                      class="w-full p-3 text-center text-[#E91E63] font-medium text-sm hover:bg-[#FCE4EC] transition-colors"
                    >
                      Ver todos los resultados
                    </button>
                  </div>
                  <div v-else class="p-4 text-center text-gray-500 text-sm">
                    No se encontraron productos
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- Right: Actions -->
          <div class="flex items-center gap-1 sm:gap-2">
            <!-- Mobile Search Toggle -->
            <button 
              @click="showMobileSearch = true"
              class="md:hidden p-2 text-gray-400 hover:text-white hover:bg-white/[0.07] rounded-xl transition-all"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>

            <!-- B2B Balance Badge -->
            <div class="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-white/[0.06] border border-white/[0.08] rounded-xl hover:bg-white/[0.1] transition-colors cursor-default">
              <div class="w-6 h-6 rounded-lg bg-emerald-500/15 flex items-center justify-center">
                <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="flex flex-col">
                <span class="text-[9px] text-gray-500 uppercase tracking-wider leading-none">Saldo</span>
                <span class="text-sm font-bold text-emerald-400 leading-tight">${{ formatPrice(accountBalance) }}</span>
              </div>
            </div>

            <!-- Favorites -->
            <router-link 
              to="/portal/favoritos" 
              class="relative p-2 text-gray-400 hover:text-[#E91E63] hover:bg-white/[0.07] rounded-xl transition-all"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              </svg>
              <span 
                v-if="favoritosCount > 0" 
                class="absolute -top-1 -right-1 min-w-[18px] h-[18px] px-1 bg-[#E91E63] text-white text-[9px] font-bold rounded-full flex items-center justify-center ring-2 ring-[#232529]"
              >
                {{ favoritosCount > 99 ? '99+' : favoritosCount }}
              </span>
            </router-link>

            <!-- Cart with total -->
            <router-link 
              to="/portal/carrito" 
              class="relative flex items-center gap-1.5 px-2.5 py-2 text-gray-400 hover:text-[#E91E63] hover:bg-white/[0.07] rounded-xl transition-all"
            >
              <div class="relative">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                <span 
                  v-if="cartCount > 0" 
                  class="absolute -top-2 -right-2 min-w-[16px] h-[16px] px-0.5 bg-[#E91E63] text-white text-[9px] font-bold rounded-full flex items-center justify-center ring-2 ring-[#232529]"
                >
                  {{ cartCount > 99 ? '99+' : cartCount }}
                </span>
              </div>
              <!-- Cart Total (Desktop) -->
              <span class="hidden lg:inline text-sm font-bold text-white">${{ formatPrice(cartTotal) }}</span>
            </router-link>

            <!-- User Menu -->
            <div class="relative" ref="userMenuRef">
              <button 
                @click="showUserMenu = !showUserMenu" 
                class="flex items-center gap-2 p-1 hover:bg-white/[0.07] rounded-xl transition-all"
              >
                <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-[#E91E63] to-[#AD1457] flex items-center justify-center ring-2 ring-[#E91E63]/20">
                  <span class="text-white text-xs font-bold">{{ userInitials }}</span>
                </div>
                <div class="hidden lg:block text-left">
                  <p class="text-xs font-medium text-white truncate max-w-[100px] leading-tight">{{ user.nombre?.split(' ')[0] }}</p>
                  <div class="flex items-center gap-1">
                    <span class="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-amber-500/15 rounded text-[9px] text-amber-400 font-semibold">
                      <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                      </svg>
                      {{ user.nivel || 'Gold' }} · {{ user.descuento || '15' }}% OFF
                    </span>
                  </div>
                </div>
                <svg class="w-3.5 h-3.5 text-gray-500 hidden lg:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- User Dropdown -->
              <transition name="dropdown">
                <div 
                  v-if="showUserMenu" 
                  class="absolute right-0 mt-2 w-72 bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden z-50"
                >
                  <!-- User Info Header -->
                  <div class="px-4 py-4 bg-gradient-to-br from-[#FCE4EC] to-white border-b border-gray-100">
                    <div class="flex items-center gap-3">
                      <div class="w-12 h-12 rounded-full bg-gradient-to-br from-[#E91E63] to-[#AD1457] flex items-center justify-center">
                        <span class="text-white text-lg font-bold">{{ userInitials }}</span>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="font-semibold text-gray-900 truncate">{{ user.nombre }}</p>
                        <p class="text-sm text-gray-500 truncate">{{ user.email }}</p>
                      </div>
                    </div>
                    <div class="flex items-center gap-2 mt-3">
                      <span class="inline-flex items-center gap-1 px-2.5 py-1 bg-amber-100 text-amber-700 text-xs font-semibold rounded-full">
                        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                        {{ user.nivel || 'Gold' }}
                      </span>
                      <span class="text-xs text-emerald-600 font-medium">{{ user.descuento || '15' }}% OFF</span>
                    </div>
                  </div>
                  
                  <!-- Menu Items -->
                  <div class="py-2">
                    <router-link 
                      to="/portal/cuenta" 
                      class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors" 
                      @click="showUserMenu = false"
                    >
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Mi Cuenta
                    </router-link>
                    <router-link 
                      to="/portal/pedidos" 
                      class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors" 
                      @click="showUserMenu = false"
                    >
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                      Historial de Pedidos
                    </router-link>
                    <router-link 
                      to="/portal/favoritos" 
                      class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors" 
                      @click="showUserMenu = false"
                    >
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                      </svg>
                      Mis Favoritos
                    </router-link>
                  </div>
                  
                  <!-- Logout -->
                  <div class="border-t border-gray-100 py-2">
                    <button 
                      @click="handleLogout" 
                      class="flex items-center gap-3 w-full px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Cerrar Sesión
                    </button>
                  </div>
                </div>
              </transition>
            </div>

            <!-- Mobile Menu Toggle -->
            <button 
              @click="showMobileMenu = !showMobileMenu" 
              class="lg:hidden p-2 text-gray-400 hover:text-white hover:bg-white/[0.07] rounded-xl transition-all"
            >
              <svg v-if="!showMobileMenu" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide">
      <div v-if="showMobileMenu" class="lg:hidden bg-[#1B1D21] border-t border-white/[0.06]">
        <div class="max-w-[1600px] mx-auto px-4 py-4 space-y-1">
          <!-- Mobile Balance -->
          <div class="flex items-center justify-between px-4 py-3 bg-white/[0.04] border border-white/[0.06] rounded-xl mb-3">
            <span class="text-sm text-gray-400">Tu saldo disponible</span>
            <span class="text-lg font-bold text-emerald-400">${{ formatPrice(accountBalance) }}</span>
          </div>
          
          <!-- Categories -->
          <p class="px-4 py-2 text-[10px] text-slate-500 uppercase tracking-widest font-medium">Categorías</p>
          <router-link 
            v-for="cat in categorias" 
            :key="cat.id" 
            :to="`/portal/catalogo?categoria=${cat.slug}`"
            class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:text-[#E91E63] hover:bg-slate-700/50 rounded-xl transition-colors"
            @click="showMobileMenu = false"
          >
            <span class="w-2 h-2 rounded-full bg-[#E91E63]/60"></span>
            {{ cat.nombre }}
          </router-link>
          
          <div class="border-t border-slate-700 my-3"></div>
          
          <!-- Special Links -->
          <router-link 
            to="/portal/catalogo?nuevo=true" 
            class="flex items-center gap-3 px-4 py-3 text-[#E91E63] hover:bg-slate-700/50 rounded-xl transition-colors"
            @click="showMobileMenu = false"
          >
            <span class="w-2 h-2 bg-[#E91E63] rounded-full animate-pulse"></span>
            Nuevos Lanzamientos
          </router-link>
          <router-link 
            to="/portal/catalogo?oferta=true" 
            class="flex items-center gap-3 px-4 py-3 text-[#FF6B9D] hover:bg-slate-700/50 rounded-xl transition-colors"
            @click="showMobileMenu = false"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z" />
            </svg>
            Ofertas
          </router-link>
          <router-link 
            to="/portal/cupones" 
            class="flex items-center gap-3 px-4 py-3 text-amber-400 hover:bg-slate-700/50 rounded-xl transition-colors"
            @click="showMobileMenu = false"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 14.25l6-6m4.5-3.493V21.75l-3.75-1.5-3.75 1.5-3.75-1.5-3.75 1.5V4.757c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0c1.1.128 1.907 1.077 1.907 2.185z" />
            </svg>
            Cupones
          </router-link>
          
          <div class="border-t border-slate-700 my-3"></div>
          <p class="px-4 py-2 text-[10px] text-slate-500 uppercase tracking-widest font-medium">Mi cuenta</p>
          
          <router-link 
            to="/portal" 
            class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:bg-slate-700/50 rounded-xl transition-colors"
            @click="showMobileMenu = false"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/portal/catalogo" 
            class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:bg-slate-700/50 rounded-xl transition-colors"
            @click="showMobileMenu = false"
          >
            Catálogo Completo
          </router-link>
          <router-link 
            to="/portal/pedidos" 
            class="flex items-center gap-3 px-4 py-3 text-slate-300 hover:bg-slate-700/50 rounded-xl transition-colors"
            @click="showMobileMenu = false"
          >
            Mis Pedidos
          </router-link>
        </div>
      </div>
    </transition>

    <!-- Mobile Search Modal -->
    <Teleport to="body">
      <transition name="modal">
        <div 
          v-if="showMobileSearch" 
          class="fixed inset-0 z-[100] bg-[#1B1D21] flex flex-col"
        >
          <!-- Search Header -->
          <div class="flex items-center gap-3 p-4 border-b border-white/[0.06]">
            <button 
              @click="showMobileSearch = false"
              class="p-2 -ml-2 text-gray-400 hover:text-white"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div class="flex-1 relative">
              <input
                v-model="searchQuery"
                ref="mobileSearchInput"
                type="text"
                placeholder="Buscar productos..."
                class="w-full h-11 pl-4 pr-10 bg-white/[0.06] border border-white/[0.1] text-white placeholder:text-gray-500 rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#E91E63]/40 focus:border-[#E91E63]/40 transition-all"
                @keydown.enter="handleMobileSearch"
              />
              <button 
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Search Results -->
          <div class="flex-1 overflow-y-auto">
            <div v-if="searchLoading" class="p-8 text-center">
              <div class="w-8 h-8 border-2 border-[#E91E63] border-t-transparent rounded-full animate-spin mx-auto"></div>
              <p class="text-sm text-slate-400 mt-3">Buscando...</p>
            </div>
            <div v-else-if="searchResults.length > 0" class="divide-y divide-slate-700">
              <router-link 
                v-for="product in searchResults" 
                :key="product.id" 
                :to="`/portal/producto/${product.id}`"
                class="flex items-center gap-4 p-4 hover:bg-slate-800"
                @click="showMobileSearch = false"
              >
                <img 
                  :src="product.imagen_principal || '/placeholder.png'" 
                  :alt="product.nombre"
                  class="w-16 h-16 object-cover rounded-xl bg-slate-700"
                />
                <div class="flex-1 min-w-0">
                  <h4 class="font-medium text-white truncate">{{ product.nombre }}</h4>
                  <p class="text-sm text-slate-400">{{ product.categoria_nombre }}</p>
                  <span class="text-[#E91E63] font-bold">${{ formatPrice(product.precio_mayorista || product.precio) }}</span>
                </div>
              </router-link>
            </div>
            <div v-else-if="searchQuery.length >= 2" class="p-8 text-center">
              <svg class="w-16 h-16 text-slate-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p class="text-slate-400">No se encontraron productos</p>
            </div>
            <div v-else class="p-6">
              <p class="text-sm text-gray-500 text-center mb-4">Busca por nombre, SKU o categoría</p>
              <div class="flex flex-wrap gap-2 justify-center">
                <button 
                  v-for="term in ['Pelucas', 'Extensiones', 'Sistemas', 'Cabello natural']" 
                  :key="term"
                  @click="searchQuery = term"
                  class="px-4 py-2 text-sm bg-gray-100 hover:bg-[#FCE4EC] hover:text-[#E91E63] text-gray-700 rounded-full transition-colors"
                >
                  {{ term }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </header>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '../../services/api'
import { categoriasService } from '../../services/categorias'
import { obtenerProductos } from '../../services/mayoristas'

export default {
  name: 'B2BHeader',
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    // Refs
    const headerRef = ref(null)
    const userMenuRef = ref(null)
    const categoriesMenuRef = ref(null)
    const mobileSearchInput = ref(null)
    
    // UI State
    const showUserMenu = ref(false)
    const showMobileMenu = ref(false)
    const showCategoriesMenu = ref(false)
    const showSearchSuggestions = ref(false)
    const showMobileSearch = ref(false)
    
    // Search State
    const searchQuery = ref('')
    const searchResults = ref([])
    const searchLoading = ref(false)
    let searchTimeout = null
    
    // Smart Sticky State
    const isScrolled = ref(false)
    const isVisible = ref(true)
    let lastScrollY = 0
    let ticking = false
    
    // Data
    const accountBalance = ref(0)
    const cartTotal = ref(0)
    const defaultAddress = ref(null)
    const categorias = ref([])
    const favoritosCount = ref(0)

    // Computed
    const user = computed(() => {
      const stored = localStorage.getItem('b2b_user')
      if (stored) {
        try { return JSON.parse(stored) } catch { return { nombre: 'Usuario', email: '', nivel: 'Mayorista' } }
      }
      return { nombre: 'Usuario', email: '', nivel: 'Mayorista' }
    })

    const userInitials = computed(() => {
      const nombre = user.value.nombre || 'U'
      return nombre.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    })

    const cartCount = computed(() => {
      const cart = localStorage.getItem('b2b_cart')
      if (cart) { 
        try { return JSON.parse(cart).items?.length || 0 } 
        catch { return 0 } 
      }
      return 0
    })

    // Smart Sticky Logic
    function handleScroll() {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const currentScrollY = window.scrollY
          
          // Show shadow when scrolled
          isScrolled.value = currentScrollY > 10
          
          // Smart hide/show logic
          if (currentScrollY < 100) {
            // Always visible near top
            isVisible.value = true
          } else if (currentScrollY > lastScrollY && currentScrollY > 100) {
            // Scrolling down - hide
            isVisible.value = false
          } else if (currentScrollY < lastScrollY) {
            // Scrolling up - show
            isVisible.value = true
          }
          
          lastScrollY = currentScrollY
          ticking = false
        })
        ticking = true
      }
    }

    // Search Functions
    async function searchProducts(query) {
      if (!query || query.length < 2) {
        searchResults.value = []
        return
      }
      
      searchLoading.value = true
      try {
        const data = await obtenerProductos({ buscar: query, limit: 8 })
        searchResults.value = data || []
      } catch (error) {
        console.error('Error searching products:', error)
        searchResults.value = []
      } finally {
        searchLoading.value = false
      }
    }

    function handleSearch() {
      if (searchQuery.value.trim()) {
        showSearchSuggestions.value = false
        router.push({ path: '/portal/catalogo', query: { buscar: searchQuery.value.trim() } })
      }
    }

    function handleMobileSearch() {
      if (searchQuery.value.trim()) {
        showMobileSearch.value = false
        router.push({ path: '/portal/catalogo', query: { buscar: searchQuery.value.trim() } })
      }
    }

    // Utility Functions
    function formatPrice(value) { 
      return value?.toLocaleString('es-CO') || '0' 
    }

    function handleLogout() {
      localStorage.removeItem('b2b_access_token')
      localStorage.removeItem('b2b_refresh_token')
      localStorage.removeItem('b2b_user')
      localStorage.removeItem('b2b_cart')
      showUserMenu.value = false
      router.push('/portal/login')
    }

    function handleClickOutside(event) {
      if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
        showUserMenu.value = false
      }
      if (!event.target.closest('.search-container')) {
        showSearchSuggestions.value = false
      }
    }

    function updateFavoritosCount() {
      const fav = localStorage.getItem('b2b_favoritos')
      if (fav) { 
        try { favoritosCount.value = JSON.parse(fav).length || 0 } 
        catch { favoritosCount.value = 0 } 
      } else { 
        favoritosCount.value = 0 
      }
    }

    // Load Data
    async function loadDefaultAddress() {
      try {
        const response = await apiClient.get('/b2b/me/direcciones')
        if (response.data && response.data.length > 0) {
          defaultAddress.value = response.data.find(a => a.is_default) || response.data[0]
        }
      } catch (error) {
        console.error('Error loading address:', error)
      }
    }

    async function loadCategorias() {
      try {
        const data = await categoriasService.listar({ soloActivas: true })
        categorias.value = data || []
      } catch (error) {
        console.error('Error loading categories:', error)
      }
    }

    // Watchers
    watch(searchQuery, (newVal) => {
      if (searchTimeout) clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => searchProducts(newVal), 300)
    })

    watch(showMobileSearch, async (val) => {
      if (val) {
        await nextTick()
        mobileSearchInput.value?.focus()
      } else {
        searchQuery.value = ''
        searchResults.value = []
      }
    })

    // Lifecycle
    onMounted(() => {
      window.addEventListener('scroll', handleScroll, { passive: true })
      document.addEventListener('click', handleClickOutside)
      window.addEventListener('favoritos-updated', updateFavoritosCount)
      
      updateFavoritosCount()
      loadDefaultAddress()
      loadCategorias()
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
      document.removeEventListener('click', handleClickOutside)
      window.removeEventListener('favoritos-updated', updateFavoritosCount)
    })

    return {
      // Refs
      headerRef,
      userMenuRef,
      categoriesMenuRef,
      mobileSearchInput,
      
      // UI State
      showUserMenu,
      showMobileMenu,
      showCategoriesMenu,
      showSearchSuggestions,
      showMobileSearch,
      isScrolled,
      isVisible,
      
      // Search
      searchQuery,
      searchResults,
      searchLoading,
      
      // Data
      user,
      userInitials,
      cartCount,
      favoritosCount,
      accountBalance,
      cartTotal,
      defaultAddress,
      categorias,
      
      // Methods
      formatPrice,
      handleLogout,
      handleSearch,
      handleMobileSearch
    }
  }
}
</script>

<style scoped>
/* Dropdown Transitions */
.dropdown-enter-active, 
.dropdown-leave-active { 
  transition: all 0.2s ease; 
}
.dropdown-enter-from, 
.dropdown-leave-to { 
  opacity: 0; 
  transform: translateY(-8px); 
}

/* Slide Transition for Mobile Menu */
.slide-enter-active, 
.slide-leave-active { 
  transition: all 0.3s ease; 
}
.slide-enter-from, 
.slide-leave-to { 
  opacity: 0; 
  max-height: 0; 
  overflow: hidden;
}
.slide-enter-to,
.slide-leave-from {
  max-height: 800px;
}

/* Modal Transition */
.modal-enter-active, 
.modal-leave-active { 
  transition: all 0.3s ease; 
}
.modal-enter-from, 
.modal-leave-to { 
  opacity: 0; 
  transform: translateY(-10px);
}

/* Custom scrollbar for search dropdown */
.max-h-\[400px\]::-webkit-scrollbar {
  width: 4px;
}
.max-h-\[400px\]::-webkit-scrollbar-track {
  background: transparent;
}
.max-h-\[400px\]::-webkit-scrollbar-thumb {
  background: #E91E63;
  border-radius: 2px;
}
</style>
