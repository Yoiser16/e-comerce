<template>
  <header 
    ref="headerRef"
    class="fixed top-0 left-0 right-0 z-50 transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]"
    :class="[
      'shadow-lg shadow-black/20',
      isVisible ? 'translate-y-0' : '-translate-y-full'
    ]"
  >
    <!-- ============================== -->
    <!-- ROW 1: Main Header -->
    <!-- ============================== -->
    <div class="bg-[#131A2B]">
      <div class="w-full px-3 lg:px-8">
        <div class="flex items-center h-[48px] lg:h-[68px] gap-2 lg:gap-5">
          
          <!-- Logo -->
          <router-link to="/portal" class="flex items-center gap-2 lg:gap-3 group shrink-0">
            <div class="w-8 h-8 lg:w-11 lg:h-11 rounded-lg lg:rounded-xl overflow-hidden bg-white flex items-center justify-center shadow-md">
              <img src="/logo-kharis.png" alt="Kharis Pro" class="w-5 h-5 lg:w-8 lg:h-8 object-contain" />
            </div>
            <div class="hidden lg:block">
              <span class="text-white font-extrabold text-lg lg:text-xl tracking-wide leading-tight">KHARIS</span>
              <span class="block text-[#C9A962] text-[10px] tracking-[0.15em] uppercase font-bold">Portal Mayorista</span>
            </div>
          </router-link>

          <!-- Address (SOLO Desktop) - Amazon style -->
          <router-link 
            to="/portal/cuenta?tab=addresses" 
            class="hidden lg:flex items-center gap-1.5 shrink-0 hover:bg-white/[0.04] rounded px-2 py-1.5 transition-colors"
          >
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
            </svg>
            <div class="flex flex-col leading-none">
              <span class="text-[11px] text-white/50 leading-tight">Enviar a</span>
              <span v-if="defaultAddress && (defaultAddress.municipio || defaultAddress.ciudad)" class="text-[14px] font-bold text-white leading-tight">{{ defaultAddress.municipio || defaultAddress.ciudad }}</span>
              <span v-else class="text-[14px] font-bold text-white leading-tight">Colombia</span>
            </div>
          </router-link>

          <!-- Search Bar MÓVIL (inline en row 1) -->
          <div class="flex-1 lg:hidden">
            <div class="relative w-full">
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Buscar en Kharis..."
                class="w-full h-[36px] pl-3 pr-9 bg-white text-sm text-gray-900 placeholder:text-gray-400 rounded-md outline-none focus:ring-2 focus:ring-[#C9A962] transition-all"
                @keydown.enter="handleSearch"
                @focus="showMobileSearchResults = true"
              />
              <button 
                @click="handleSearch"
                class="absolute right-0 top-0 h-full w-9 flex items-center justify-center text-gray-400"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
              
              <!-- Resultados de búsqueda móvil -->
              <transition name="dropdown">
                <div 
                  v-if="showMobileSearchResults && searchQuery.length >= 2 && searchResults.length > 0"
                  class="absolute top-full left-0 right-0 mt-1 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden z-50 max-h-[60vh] overflow-y-auto"
                >
                  <router-link 
                    v-for="product in searchResults.slice(0, 5)" 
                    :key="product.id" 
                    :to="`/portal/producto/${product.id}`"
                    class="flex items-center gap-3 p-3 hover:bg-slate-50 transition-colors border-b border-gray-50 last:border-0"
                    @click="showMobileSearchResults = false; searchQuery = ''"
                  >
                    <img 
                      :src="product.imagen_principal || '/placeholder.png'" 
                      :alt="product.nombre"
                      class="w-10 h-10 object-cover rounded bg-gray-100"
                    />
                    <div class="flex-1 min-w-0">
                      <h4 class="font-medium text-gray-900 text-sm truncate">{{ product.nombre }}</h4>
                      <p class="text-xs text-gray-500">{{ product.categoria_nombre }}</p>
                    </div>
                    <span class="text-[#0F172A] font-semibold text-sm whitespace-nowrap">${{ formatPrice(product.precio_mayorista || product.precio) }}</span>
                  </router-link>
                  <button 
                    @click="handleSearch; showMobileSearchResults = false"
                    class="w-full p-2.5 text-center text-[#C9A962] font-medium text-sm hover:bg-slate-50 transition-colors"
                  >
                    Ver todos →
                  </button>
                </div>
              </transition>
            </div>
          </div>

          <!-- Search Bar DESKTOP -->
          <div class="hidden lg:flex flex-1 mx-3 lg:mx-6">
            <div class="relative w-full group">
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Buscar productos, marcas, SKU, categorías..."
                class="w-full h-[44px] lg:h-[48px] pl-5 pr-[54px] bg-white text-sm lg:text-[15px] text-gray-900 placeholder:text-gray-400 rounded-md outline-none ring-2 ring-[#C9A962] focus:ring-[#e0c172] transition-all"
                @keydown.enter="handleSearch"
                @focus="showSearchSuggestions = true"
              />
              <button 
                @click="handleSearch"
                class="absolute right-0 top-0 h-full w-[48px] lg:w-[52px] flex items-center justify-center rounded-r-md bg-gradient-to-b from-[#e0c172] via-[#D4A85A] to-[#C9A962] hover:from-[#C9A962] hover:to-[#b8953a] text-[#131A2B] transition-all"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
              
              <!-- Search Suggestions Dropdown -->
              <transition name="dropdown">
                <div 
                  v-if="showSearchSuggestions && searchQuery.length >= 2"
                  class="absolute top-full left-0 right-0 mt-1.5 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden z-50"
                >
                  <div v-if="searchLoading" class="p-4 text-center">
                    <div class="w-5 h-5 border-2 border-slate-300 border-t-transparent rounded-full animate-spin mx-auto"></div>
                  </div>
                  <div v-else-if="searchResults.length > 0" class="divide-y divide-gray-50 max-h-[400px] overflow-y-auto">
                    <router-link 
                      v-for="product in searchResults.slice(0, 6)" 
                      :key="product.id" 
                      :to="`/portal/producto/${product.id}`"
                      class="flex items-center gap-3 p-3 hover:bg-slate-50 transition-colors"
                      @click="showSearchSuggestions = false"
                    >
                      <img 
                        :src="product.imagen_principal || '/placeholder.png'" 
                        :alt="product.nombre"
                        class="w-10 h-10 object-cover rounded-md bg-gray-100"
                      />
                      <div class="flex-1 min-w-0">
                        <h4 class="font-medium text-gray-900 text-sm truncate">{{ product.nombre }}</h4>
                        <p class="text-xs text-gray-500">{{ product.categoria_nombre }}</p>
                      </div>
                      <span class="text-[#0F172A] font-semibold text-sm">${{ formatPrice(product.precio_mayorista || product.precio) }}</span>
                    </router-link>
                    <button 
                      @click="handleSearch"
                      class="w-full p-2.5 text-center text-[#0F172A] font-medium text-sm hover:bg-slate-50 transition-colors"
                    >
                      Ver todos los resultados →
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
          <div class="flex items-center gap-0 lg:gap-1 shrink-0">
            <!-- Notifications (SOLO DESKTOP) -->
            <div class="relative hidden lg:block" ref="notificationsRef">
              <button 
                class="relative p-2.5 text-white hover:text-[#C9A962] transition-colors"
                @click="toggleNotifications"
              >
                <svg class="w-[22px] h-[22px]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"/>
                </svg>
                <span 
                  v-if="notificationsCount > 0" 
                  class="absolute top-0 right-0 lg:top-0.5 lg:right-0.5 min-w-[16px] lg:min-w-[18px] h-[16px] lg:h-[18px] px-1 bg-red-500 text-white text-[9px] lg:text-[10px] font-bold rounded-full flex items-center justify-center"
                >
                  {{ notificationsCount > 9 ? '9+' : notificationsCount }}
                </span>
              </button>

              <transition name="dropdown">
                <div
                  v-if="showNotifications"
                  class="absolute right-0 mt-1.5 w-[320px] bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden z-50"
                >
                  <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
                    <div class="text-sm font-bold text-gray-900">Notificaciones</div>
                    <button
                      v-if="notificationsCount > 0"
                      class="text-[11px] text-[#8B6914] font-semibold hover:text-[#6f5310]"
                      @click="markAllNotificationsRead"
                    >
                      Marcar todas
                    </button>
                  </div>

                  <div v-if="notificationsLoading" class="p-4 text-center">
                    <div class="w-5 h-5 border-2 border-slate-300 border-t-transparent rounded-full animate-spin mx-auto"></div>
                  </div>

                  <div v-else-if="notifications.length" class="max-h-[360px] overflow-y-auto divide-y divide-gray-100">
                    <button
                      v-for="notif in notifications"
                      :key="notif.id"
                      class="w-full text-left px-4 py-3 hover:bg-slate-50 transition-colors"
                      @click="markNotificationRead(notif)"
                    >
                      <div class="flex items-start gap-2">
                        <span
                          class="mt-1.5 w-2 h-2 rounded-full"
                          :class="notif.leida ? 'bg-gray-300' : 'bg-[#C9A962]'"
                        ></span>
                        <div class="flex-1">
                          <p class="text-[13px] font-semibold text-gray-900 leading-snug">{{ notif.titulo }}</p>
                          <p class="text-[12px] text-gray-600 leading-snug mt-0.5">{{ notif.mensaje }}</p>
                          <p class="text-[11px] text-gray-400 mt-1">{{ formatNotificationDate(notif.fecha_creacion) }}</p>
                        </div>
                      </div>
                    </button>
                  </div>

                  <div v-else class="p-4 text-center text-gray-500 text-sm">
                    No tienes notificaciones por ahora.
                  </div>
                </div>
              </transition>
            </div>

            <!-- Cart -->
            <router-link 
              to="/portal/carrito" 
              class="relative flex items-center gap-1.5 p-2 lg:px-3 text-white hover:bg-white/[0.04] rounded transition-colors group"
            >
              <div class="relative">
                <svg class="w-5 h-5 lg:w-7 lg:h-7" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                </svg>
                <span 
                  v-if="cartCount > 0" 
                  class="absolute -top-1.5 -right-1.5 lg:-top-2 lg:-right-2 min-w-[16px] lg:min-w-[18px] h-[16px] lg:h-[18px] px-1 bg-[#C9A962] text-[#131A2B] text-[9px] lg:text-[10px] font-bold rounded-full flex items-center justify-center"
                >
                  {{ cartCount > 99 ? '99+' : cartCount }}
                </span>
              </div>
              <div class="hidden lg:flex flex-col leading-none">
                <span class="text-[11px] text-white/50 leading-tight">Carrito</span>
                <span class="text-[15px] font-bold text-white leading-tight">{{ cartCount }} {{ cartCount === 1 ? 'producto' : 'productos' }}</span>
              </div>
            </router-link>

            <!-- User Menu (hidden on mobile, shown on lg) -->
            <div class="relative hidden lg:block" ref="userMenuRef">
              <button 
                @click="showUserMenu = !showUserMenu" 
                class="flex items-center gap-1.5 p-2 lg:px-3 hover:bg-white/[0.04] rounded transition-colors"
              >
                <svg class="w-6 h-6 lg:w-7 lg:h-7 text-white" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
                <div class="flex flex-col leading-none">
                  <span class="text-[11px] text-white/50 leading-tight">Hola, {{ user.nombre?.split(' ')[0] }}</span>
                  <span class="text-[15px] font-bold text-white flex items-center gap-0.5 leading-tight">
                    Cuenta
                    <svg class="w-3 h-3 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
                    </svg>
                  </span>
                </div>
              </button>

              <!-- User Dropdown -->
              <transition name="dropdown">
                <div 
                  v-if="showUserMenu" 
                  class="absolute right-0 mt-1.5 w-64 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden z-50"
                >
                  <!-- User Info Header -->
                  <div class="px-4 py-3.5 bg-gradient-to-r from-slate-50 to-amber-50/20 border-b border-gray-100">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-full bg-[#131A2B] flex items-center justify-center ring-2 ring-[#C9A962]/30">
                        <span class="text-[#C9A962] text-sm font-bold">{{ userInitials }}</span>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="font-bold text-gray-900 text-sm truncate">{{ user.nombre }}</p>
                        <p class="text-xs text-gray-500 truncate">{{ user.email }}</p>
                      </div>
                    </div>
                    <div class="flex items-center gap-2 mt-2.5">
                      <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-[#C9A962]/15 text-[#8B6914] text-[10px] font-bold rounded border border-[#C9A962]/25">
                        {{ user.nivel || 'Gold' }}
                      </span>
                      <span class="text-[10px] text-gray-500">{{ user.descuento || '15' }}% descuento aplicado</span>
                    </div>
                  </div>
                  
                  <!-- Menu Items -->
                  <div class="py-1.5">
                    <router-link 
                      to="/portal/cuenta" 
                      class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-slate-50 transition-colors" 
                      @click="showUserMenu = false"
                    >
                      <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                      </svg>
                      Mi Cuenta
                    </router-link>
                    <router-link 
                      to="/portal/pedidos" 
                      class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-slate-50 transition-colors" 
                      @click="showUserMenu = false"
                    >
                      <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                      </svg>
                      Historial de Pedidos
                    </router-link>
                    <router-link 
                      to="/portal/favoritos" 
                      class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-slate-50 transition-colors" 
                      @click="showUserMenu = false"
                    >
                      <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"/>
                      </svg>
                      Mis Favoritos
                    </router-link>
                  </div>
                  
                  <!-- Logout -->
                  <div class="border-t border-gray-100 py-1.5">
                    <button 
                      @click="handleLogout" 
                      class="flex items-center gap-3 w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
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
              class="lg:hidden p-2 text-white hover:text-[#C9A962] transition-colors"
            >
              <svg v-if="!showMobileMenu" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================== -->
    <!-- ROW 2 MÓVIL: Barra de navegación estilo Amazon -->
    <!-- ============================== -->
    <div class="lg:hidden bg-[#1a2332] border-t border-white/[0.08]">
      <div class="flex items-center gap-1 px-3 py-1.5 overflow-x-auto scrollbar-hide">
        <router-link 
          to="/portal/catalogo?oferta=true"
          class="shrink-0 px-3 py-1.5 text-[12px] font-semibold text-[#C9A962] hover:bg-white/[0.08] rounded transition-colors whitespace-nowrap"
        >
          Ofertas
        </router-link>
        <router-link 
          to="/portal/cupones"
          class="shrink-0 px-3 py-1.5 text-[12px] font-medium text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors whitespace-nowrap"
        >
          Cupones
        </router-link>
        <router-link 
          to="/portal/catalogo?nuevo=true"
          class="shrink-0 px-3 py-1.5 text-[12px] font-medium text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors whitespace-nowrap flex items-center gap-1"
        >
          Nuevos
          <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span>
        </router-link>
        <router-link 
          to="/portal/catalogo"
          class="shrink-0 px-3 py-1.5 text-[12px] font-medium text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors whitespace-nowrap"
        >
          Catálogo
        </router-link>
        <router-link 
          to="/portal/pedidos"
          class="shrink-0 px-3 py-1.5 text-[12px] font-medium text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors whitespace-nowrap"
        >
          Mis Pedidos
        </router-link>
        <router-link 
          to="/portal/favoritos"
          class="shrink-0 px-3 py-1.5 text-[12px] font-medium text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors whitespace-nowrap flex items-center gap-1"
        >
          Favoritos
          <span 
            v-if="favoritosCount > 0" 
            class="text-[9px] px-1 py-0.5 bg-[#C9A962] text-[#131A2B] rounded-full font-bold"
          >
            {{ favoritosCount }}
          </span>
        </router-link>
      </div>
    </div>

    <!-- ============================== -->
    <!-- ROW 2: Navigation Bar (like Amazon's nav strip) -->
    <!-- ============================== -->
    <div class="hidden lg:block bg-[#1a2332] border-t border-white/[0.06]">
      <div class="w-full px-6 lg:px-8">
        <nav class="flex items-center gap-0.5 h-[38px] -ml-3">
          <!-- Categories Dropdown -->
          <div 
            class="relative" 
            ref="categoriesMenuRef" 
            @mouseenter="showCategoriesMenu = true" 
            @mouseleave="showCategoriesMenu = false"
          >
            <button 
              class="flex items-center gap-1.5 px-3 py-1.5 text-[13px] font-bold text-white hover:bg-white/[0.08] rounded transition-colors tracking-wide"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
              Todo
              <svg 
                class="w-3 h-3 text-white/60 transition-transform duration-200" 
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
                class="absolute left-0 top-full mt-0.5 w-60 bg-white rounded-lg shadow-2xl border border-gray-100 overflow-hidden"
              >
                <div class="py-1.5">
                  <router-link 
                    v-for="cat in categorias" 
                    :key="cat.id" 
                    :to="`/portal/catalogo?categoria=${cat.slug}`"
                    class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-slate-50 hover:text-[#131A2B] transition-colors font-medium"
                    @click="showCategoriesMenu = false"
                  >
                    {{ cat.nombre }}
                  </router-link>
                  <div class="border-t border-gray-100 mt-1.5 pt-1.5">
                    <router-link 
                      to="/portal/catalogo"
                      class="flex items-center justify-between px-4 py-2.5 text-sm text-[#131A2B] font-bold hover:bg-slate-50 transition-colors"
                      @click="showCategoriesMenu = false"
                    >
                      Ver todo el catálogo
                      <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </router-link>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <span class="w-px h-4 bg-white/15 mx-0.5"></span>

          <router-link 
            to="/portal/catalogo?oferta=true"
            class="px-3 py-1.5 text-[13px] font-bold text-[#C9A962] hover:bg-white/[0.08] rounded transition-colors"
          >
            Ofertas del Día
          </router-link>

          <router-link 
            to="/portal/cupones"
            class="px-3 py-1.5 text-[13px] font-semibold text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors"
          >
            Cupones
          </router-link>

          <router-link 
            to="/portal/catalogo?nuevo=true"
            class="px-3 py-1.5 text-[13px] font-semibold text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors flex items-center gap-1.5"
          >
            Nuevos Lanzamientos
            <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
          </router-link>

          <router-link 
            to="/portal/catalogo"
            class="px-3 py-1.5 text-[13px] font-semibold text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors"
          >
            Catálogo Completo
          </router-link>

          <router-link 
            to="/portal/pedidos"
            class="px-3 py-1.5 text-[13px] font-semibold text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors"
          >
            Mis Pedidos
          </router-link>

          <router-link 
            to="/portal/favoritos"
            class="px-3 py-1.5 text-[13px] font-semibold text-white/90 hover:text-white hover:bg-white/[0.08] rounded transition-colors flex items-center gap-1.5"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"/>
            </svg>
            Mis Favoritos
            <span 
              v-if="favoritosCount > 0" 
              class="text-[10px] px-1.5 py-0.5 bg-[#C9A962] text-[#131A2B] rounded-full font-bold"
            >
              {{ favoritosCount }}
            </span>
          </router-link>

          <!-- Spacer to push help links right -->
          <div class="flex-1"></div>

          <!-- Help & Contact (right side of nav bar) -->
          <div class="flex items-center gap-1">
            <router-link 
              to="/portal/ayuda" 
              class="px-2.5 py-1.5 text-[12px] text-white/50 hover:text-white/80 hover:bg-white/[0.05] rounded transition-colors"
            >
              Centro de ayuda
            </router-link>
            <a 
              href="https://wa.me/4796657763" 
              target="_blank" 
              class="flex items-center gap-1 px-2.5 py-1.5 text-[12px] text-white/50 hover:text-white/80 hover:bg-white/[0.05] rounded transition-colors"
            >
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
              </svg>
              Contacto
            </a>
          </div>
        </nav>
      </div>
    </div>

    <!-- Mobile Menu Fullscreen (estilo Mercado Libre) -->
    <Teleport to="body">
      <transition name="slide-fullscreen">
        <div 
          v-if="showMobileMenu" 
          class="lg:hidden fixed inset-0 z-[100] bg-white flex flex-col"
        >
          <!-- Header con búsqueda -->
          <div class="bg-[#131A2B] px-4 py-3">
            <div class="flex items-center gap-3">
              <!-- Logo -->
              <router-link to="/portal" @click="showMobileMenu = false" class="flex-shrink-0">
                <img src="/logo%20blanco.png" alt="Kharis" class="h-7 w-auto" />
              </router-link>
              
              <!-- Search -->
              <div class="flex-1 relative">
                <input
                  type="text"
                  placeholder="Buscar en Kharis..."
                  class="w-full h-9 pl-3 pr-8 bg-white rounded text-sm text-gray-800 placeholder:text-gray-400 outline-none"
                  @focus="showMobileMenu = false; showMobileSearch = true"
                />
                <svg class="absolute right-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/>
                </svg>
              </div>
              
              <!-- Cart & Close -->
              <router-link to="/portal/carrito" @click="showMobileMenu = false" class="relative p-1.5 text-white">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121 0 2.052-.868 2.178-1.977l.672-5.927A1.125 1.125 0 0014.732 5.25H4.51M7.5 14.25L5.106 5.272M8.25 18.75a.75.75 0 11-1.5 0 .75.75 0 011.5 0zM17.25 18.75a.75.75 0 11-1.5 0 .75.75 0 011.5 0z"/>
                </svg>
                <span v-if="cartItemsCount > 0" class="absolute -top-1 -right-1 w-4 h-4 bg-[#C9A962] text-[#131A2B] text-[10px] font-bold flex items-center justify-center rounded-full">
                  {{ cartItemsCount > 9 ? '9+' : cartItemsCount }}
                </span>
              </router-link>
              <button @click="showMobileMenu = false" class="p-1.5 text-white">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Contenido scrolleable -->
          <div class="flex-1 overflow-y-auto">
            <!-- Perfil de usuario -->
            <router-link 
              to="/portal/cuenta" 
              class="block px-4 py-4 border-b border-gray-100 hover:bg-gray-50 transition-colors"
              @click="showMobileMenu = false"
            >
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#C9A962] to-[#D4B574] flex items-center justify-center text-white font-bold text-sm">
                  {{ userInitials }}
                </div>
                <div class="flex-1 min-w-0">
                  <p class="font-semibold text-gray-800 text-sm truncate">{{ user?.nombre || 'Cliente' }}</p>
                  <p class="text-xs text-gray-500">Mi perfil ›</p>
                </div>
              </div>
            </router-link>
            
            <!-- Saldo disponible -->
            <div class="mx-4 my-3 px-4 py-3 bg-gradient-to-r from-[#C9A962] to-[#D4B574] rounded-lg flex items-center justify-between">
              <span class="text-sm text-[#2C1810] font-medium">Saldo disponible</span>
              <span class="text-lg font-bold text-[#2C1810]">${{ formatPrice(accountBalance) }}</span>
            </div>
            
            <!-- Navegación principal -->
            <nav class="py-2">
              <router-link 
                to="/portal" 
                class="flex items-center gap-4 px-4 py-3.5 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/>
                </svg>
                <span class="text-gray-800 text-[15px]">Inicio</span>
              </router-link>
              
              <router-link 
                to="/portal/cuenta?tab=notifications" 
                class="flex items-center gap-4 px-4 py-3.5 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <div class="relative">
                  <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"/>
                  </svg>
                  <span v-if="notificationsCount > 0" class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-[9px] font-bold flex items-center justify-center rounded-full">
                    {{ notificationsCount > 9 ? '9+' : notificationsCount }}
                  </span>
                </div>
                <span class="text-gray-800 text-[15px]">Notificaciones</span>
              </router-link>
              
              <router-link 
                to="/portal/pedidos" 
                class="flex items-center gap-4 px-4 py-3.5 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/>
                </svg>
                <span class="text-gray-800 text-[15px]">Mis Pedidos</span>
              </router-link>
              
              <router-link 
                to="/portal/favoritos" 
                class="flex items-center gap-4 px-4 py-3.5 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"/>
                </svg>
                <span class="text-gray-800 text-[15px]">Favoritos</span>
                <span v-if="favoritosCount > 0" class="ml-auto text-xs text-gray-400">{{ favoritosCount }}</span>
              </router-link>
              
              <router-link 
                to="/portal/catalogo?oferta=true" 
                class="flex items-center gap-4 px-4 py-3.5 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6z"/>
                </svg>
                <span class="text-gray-800 text-[15px]">Ofertas</span>
              </router-link>
              
              <router-link 
                to="/portal/cupones" 
                class="flex items-center gap-4 px-4 py-3.5 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 010 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 010-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375z"/>
                </svg>
                <span class="text-gray-800 text-[15px]">Cupones</span>
              </router-link>
            </nav>
            
            <div class="h-px bg-gray-100 mx-4"></div>
            
            <!-- Categorías -->
            <div class="py-2">
              <p class="px-4 py-2 text-xs text-gray-400 uppercase tracking-wider font-medium">Categorías</p>
              <router-link 
                v-for="cat in categorias" 
                :key="cat.id" 
                :to="`/portal/catalogo?categoria=${cat.slug}`"
                class="flex items-center gap-4 px-4 py-3 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <span class="text-gray-700 text-[15px]">{{ cat.nombre }}</span>
              </router-link>
              <router-link 
                to="/portal/catalogo"
                class="flex items-center gap-4 px-4 py-3 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <span class="text-[#C9A962] text-[15px] font-medium">Ver todo el catálogo</span>
                <svg class="w-4 h-4 text-[#C9A962] ml-auto" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
                </svg>
              </router-link>
            </div>
            
            <div class="h-px bg-gray-100 mx-4"></div>
            
            <!-- Mi cuenta -->
            <div class="py-2">
              <p class="px-4 py-2 text-xs text-gray-400 uppercase tracking-wider font-medium">Mi cuenta</p>
              
              <router-link 
                to="/portal/cuenta" 
                class="flex items-center gap-4 px-4 py-3 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/>
                </svg>
                <span class="text-gray-700 text-[15px]">Mi perfil</span>
              </router-link>
              
              <router-link 
                to="/portal/cuenta?tab=addresses" 
                class="flex items-center gap-4 px-4 py-3 hover:bg-gray-50 transition-colors"
                @click="showMobileMenu = false"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/>
                </svg>
                <span class="text-gray-700 text-[15px]">Mis direcciones</span>
              </router-link>
              
              <a 
                href="https://wa.me/4796657763" 
                target="_blank" 
                class="flex items-center gap-4 px-4 py-3 hover:bg-gray-50 transition-colors"
              >
                <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z"/>
                </svg>
                <span class="text-gray-700 text-[15px]">Ayuda / Contacto</span>
              </a>
            </div>
            
            <!-- Cerrar sesión -->
            <div class="p-4 mt-2">
              <button 
                @click="handleLogout"
                class="w-full flex items-center justify-center gap-2 py-3 border border-gray-200 rounded-lg text-gray-500 hover:bg-gray-50 transition-colors text-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9"/>
                </svg>
                Cerrar sesión
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- Mobile Search Modal -->
    <Teleport to="body">
      <transition name="modal">
        <div 
          v-if="showMobileSearch" 
          class="fixed inset-0 z-[100] bg-[#131A2B] flex flex-col"
        >
          <!-- Search Header -->
          <div class="flex items-center gap-3 p-4 border-b border-white/[0.06]">
            <button 
              @click="showMobileSearch = false"
              class="p-2 -ml-2 text-white/70 hover:text-white"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div class="flex-1 relative">
              <input
                v-model="searchQuery"
                ref="mobileSearchInput"
                type="text"
                placeholder="Buscar productos..."
                class="w-full h-10 pl-4 pr-10 bg-slate-800 border border-slate-700 text-white placeholder:text-slate-500 rounded-lg text-sm outline-none focus:ring-1 focus:ring-slate-500 focus:border-slate-500 transition-all"
                @keydown.enter="handleMobileSearch"
              />
              <button 
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Search Results -->
          <div class="flex-1 overflow-y-auto">
            <div v-if="searchLoading" class="p-8 text-center">
              <div class="w-6 h-6 border-2 border-slate-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
              <p class="text-sm text-slate-500 mt-3">Buscando...</p>
            </div>
            <div v-else-if="searchResults.length > 0" class="divide-y divide-slate-800">
              <router-link 
                v-for="product in searchResults" 
                :key="product.id" 
                :to="`/portal/producto/${product.id}`"
                class="flex items-center gap-4 p-4 hover:bg-slate-800/50"
                @click="showMobileSearch = false"
              >
                <img 
                  :src="product.imagen_principal || '/placeholder.png'" 
                  :alt="product.nombre"
                  class="w-14 h-14 object-cover rounded-lg bg-slate-800"
                />
                <div class="flex-1 min-w-0">
                  <h4 class="font-medium text-white text-sm truncate">{{ product.nombre }}</h4>
                  <p class="text-xs text-slate-500">{{ product.categoria_nombre }}</p>
                  <span class="text-amber-400 font-semibold text-sm">${{ formatPrice(product.precio_mayorista || product.precio) }}</span>
                </div>
              </router-link>
            </div>
            <div v-else-if="searchQuery.length >= 2" class="p-8 text-center">
              <svg class="w-12 h-12 text-slate-700 mx-auto mb-3" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
              <p class="text-slate-500 text-sm">No se encontraron productos</p>
            </div>
            <div v-else class="p-6">
              <p class="text-sm text-slate-600 text-center mb-4">Busca por nombre, SKU o categoría</p>
              <div class="flex flex-wrap gap-2 justify-center">
                <button 
                  v-for="term in ['Pelucas', 'Extensiones', 'Sistemas', 'Cabello natural']" 
                  :key="term"
                  @click="searchQuery = term"
                  class="px-3 py-1.5 text-sm bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-md transition-colors"
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
import { listarNotificaciones, marcarNotificacionLeida, marcarTodasLeidas } from '../../services/notificaciones'

export default {
  name: 'B2BHeader',
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    // Refs
    const headerRef = ref(null)
    const userMenuRef = ref(null)
    const categoriesMenuRef = ref(null)
    const notificationsRef = ref(null)
    const mobileSearchInput = ref(null)
    
    // UI State
    const showUserMenu = ref(false)
    const showMobileMenu = ref(false)
    const showCategoriesMenu = ref(false)
    const showSearchSuggestions = ref(false)
    const showMobileSearch = ref(false)
    const showMobileSearchResults = ref(false)
    
    // Search State
    const searchQuery = ref('')
    const searchResults = ref([])
    const searchLoading = ref(false)
    let searchTimeout = null
    
    // Smart Sticky State
    const isScrolled = ref(false)
    const isVisible = ref(true)
    let lastScrollY = 0
    let scrollDelta = 0
    const SCROLL_THRESHOLD = 60 // px of scroll needed to trigger hide
    let ticking = false
    
    // Data
    const accountBalance = ref(0)
    const cartTotal = ref(0)
    const cartCount = ref(0)
    const defaultAddress = ref(null)
    const categorias = ref([])
    const favoritosCount = ref(0)
    const notificationsCount = ref(0)
    const showNotifications = ref(false)
    const notifications = ref([])
    const notificationsLoading = ref(false)

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

    function updateCartCount() {
      const cart = localStorage.getItem('b2b_cart')
      if (cart) {
        try { cartCount.value = JSON.parse(cart).items?.length || 0 }
        catch { cartCount.value = 0 }
      } else {
        cartCount.value = 0
      }
    }

    function handleCartStorage(event) {
      if (event.key === 'b2b_cart') {
        updateCartCount()
      }
    }

    async function loadNotifications() {
      if (notificationsLoading.value) return
      notificationsLoading.value = true
      try {
        const data = await listarNotificaciones({ limit: 15, offset: 0, soloNoLeidas: false })
        notifications.value = data.items || []
        notificationsCount.value = data.unread_count || 0
      } catch (error) {
        console.error('Error loading notifications:', error)
      } finally {
        notificationsLoading.value = false
      }
    }

    async function markNotificationRead(notif) {
      if (!notif || notif.leida) return
      try {
        await marcarNotificacionLeida(notif.id)
        notif.leida = true
        notificationsCount.value = Math.max(0, notificationsCount.value - 1)
      } catch (error) {
        console.error('Error marking notification read:', error)
      }
    }

    async function markAllNotificationsRead() {
      if (notificationsCount.value === 0) return
      try {
        await marcarTodasLeidas()
        notifications.value = notifications.value.map(n => ({ ...n, leida: true }))
        notificationsCount.value = 0
      } catch (error) {
        console.error('Error marking all notifications read:', error)
      }
    }

    async function toggleNotifications() {
      showNotifications.value = !showNotifications.value
      if (showNotifications.value) {
        await loadNotifications()
      }
    }

    function formatNotificationDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleString('es-CO', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
    }

    // Smart Sticky Logic with scroll delta threshold
    function handleScroll() {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const currentScrollY = window.scrollY
          const diff = currentScrollY - lastScrollY
          
          // Show shadow when scrolled
          isScrolled.value = currentScrollY > 10
          
          // Always visible near top
          if (currentScrollY < 150) {
            isVisible.value = true
            scrollDelta = 0
          } else if (diff > 0) {
            // Scrolling DOWN — accumulate delta
            scrollDelta += diff
            if (scrollDelta > SCROLL_THRESHOLD) {
              isVisible.value = false
            }
          } else if (diff < 0) {
            // Scrolling UP — accumulate negative delta
            scrollDelta += diff
            if (scrollDelta < -30) {
              isVisible.value = true
              scrollDelta = 0
            }
          }
          
          // Reset delta when direction changes
          if ((diff > 0 && scrollDelta < 0) || (diff < 0 && scrollDelta > 0)) {
            scrollDelta = diff
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
      if (notificationsRef.value && !notificationsRef.value.contains(event.target)) {
        showNotifications.value = false
      }
      if (!event.target.closest('.search-container')) {
        showSearchSuggestions.value = false
      }
    }

    function getFavoritosKey() {
      const keyPart = user.value?.email || user.value?.id || user.value?.usuario_id || 'anon'
      return `b2b_favoritos_${keyPart}`
    }

    function updateFavoritosCount() {
      const fav = localStorage.getItem(getFavoritosKey())
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
      window.addEventListener('cart-updated', updateCartCount)
      window.addEventListener('storage', handleCartStorage)
      window.addEventListener('favoritos-updated', updateFavoritosCount)
      
      updateCartCount()
      updateFavoritosCount()
      loadNotifications()
      loadDefaultAddress()
      loadCategorias()
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
      document.removeEventListener('click', handleClickOutside)
      window.removeEventListener('cart-updated', updateCartCount)
      window.removeEventListener('storage', handleCartStorage)
      window.removeEventListener('favoritos-updated', updateFavoritosCount)
    })

    return {
      // Refs
      headerRef,
      userMenuRef,
      categoriesMenuRef,
      notificationsRef,
      mobileSearchInput,
      
      // UI State
      showUserMenu,
      showMobileMenu,
      showCategoriesMenu,
      showSearchSuggestions,
      showMobileSearch,
      showMobileSearchResults,
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
      defaultAddress,
      categorias,
      notificationsCount,
      showNotifications,
      notifications,
      notificationsLoading,
      
      // Methods
      formatPrice,
      formatNotificationDate,
      handleLogout,
      toggleNotifications,
      markNotificationRead,
      markAllNotificationsRead,
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

/* Slide Fullscreen Transition for Mobile Menu (ML style) */
.slide-fullscreen-enter-active, 
.slide-fullscreen-leave-active { 
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
}
.slide-fullscreen-enter-from { 
  opacity: 0;
  transform: translateX(100%);
}
.slide-fullscreen-leave-to { 
  opacity: 0;
  transform: translateX(100%);
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

/* Hide scrollbar for horizontal nav */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
