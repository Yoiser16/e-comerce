<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header - YouTube/Google Cloud Style -->
    <header class="fixed top-0 left-0 right-0 z-50 h-16 bg-white border-b border-gray-200">
      <div class="flex items-center justify-between h-full px-4">
        <!-- Left Zone: Toggle + Logo -->
        <div class="flex items-center gap-3">
          <!-- Hamburger Toggle (YouTube style) -->
          <button 
            @click="toggleSidebar" 
            class="w-10 h-10 flex items-center justify-center text-text-dark hover:bg-gray-100 rounded-full transition-all"
            title="Menú"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
          </button>

          <!-- Brand Logo -->
          <router-link to="/" class="flex items-center gap-2.5 group">
            <span class="font-luxury text-xl text-text-dark tracking-wide">Kharis</span>
            <span class="text-[11px] uppercase tracking-[0.15em] text-text-light font-bold">Admin</span>
          </router-link>
        </div>

        <!-- Right Zone: Actions -->
        <div class="flex items-center gap-2">
          <!-- Mini Radio Player - Cuando está reproduciendo -->
          <div 
            v-if="isPlaying && currentStation"
            class="flex items-center gap-2 px-3 py-2 bg-white rounded-xl border border-emerald-200 shadow-sm"
          >
            <!-- Barras animadas -->
            <div class="flex items-center gap-0.5 h-4">
              <div class="w-0.5 bg-emerald-500 rounded-full animate-music-bar" style="height: 30%; animation-delay: 0ms;"></div>
              <div class="w-0.5 bg-emerald-500 rounded-full animate-music-bar" style="height: 50%; animation-delay: 200ms;"></div>
              <div class="w-0.5 bg-emerald-500 rounded-full animate-music-bar" style="height: 70%; animation-delay: 400ms;"></div>
              <div class="w-0.5 bg-emerald-500 rounded-full animate-music-bar" style="height: 40%; animation-delay: 100ms;"></div>
            </div>

            <!-- Info de la emisora -->
            <button
              @click="showRadio = true"
              class="flex flex-col min-w-0 hover:opacity-80 transition-opacity"
              title="Abrir reproductor"
            >
              <span class="text-[10px] font-semibold text-emerald-600 uppercase tracking-wider leading-none">
                En vivo
              </span>
              <span class="text-xs font-medium text-text-dark truncate max-w-[100px] leading-tight mt-0.5">
                {{ currentStation }}
              </span>
            </button>

            <!-- Controles -->
            <div class="flex items-center gap-0.5 flex-shrink-0 pl-1 border-l border-gray-200">
              <!-- Play/Pause -->
              <button
                @click="togglePlayback"
                class="w-6 h-6 rounded-lg flex items-center justify-center hover:bg-emerald-50 transition-colors text-emerald-600"
                :title="isPlaying ? 'Pausar' : 'Reproducir'"
              >
                <svg v-if="isPlaying" class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
                </svg>
                <svg v-else class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Radio Button - Solo cuando NO está reproduciendo -->
          <button 
            v-else
            @click="showRadio = !showRadio"
            :class="[
              'relative w-10 h-10 flex items-center justify-center rounded-full transition-all',
              showRadio 
                ? 'bg-emerald-500 text-white' 
                : 'text-text-medium hover:text-text-dark hover:bg-gray-100'
            ]"
            title="Radio"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 7.5l16.5-4.125M12 6.75c-2.708 0-5.363.224-7.948.655C2.999 7.58 2.25 8.507 2.25 9.574v9.176A2.25 2.25 0 004.5 21h15a2.25 2.25 0 002.25-2.25V9.574c0-1.067-.75-1.994-1.802-2.169A48.329 48.329 0 0012 6.75zm-1.683 6.443l-.311.311a1.125 1.125 0 01-1.59-1.59l.31-.312a1.125 1.125 0 011.591 1.591zm.22 3.17a.75.75 0 001.06 0l3.126-3.125a.75.75 0 00-1.06-1.061l-3.126 3.125a.75.75 0 000 1.061zm4.713-3.17l.311.311a1.125 1.125 0 01-1.59 1.59l-.312-.31a1.125 1.125 0 011.591-1.591z" />
            </svg>
          </button>

          <!-- Notifications -->
          <div class="relative">
            <button 
              @click="toggleNotifications"
              :class="[
                'relative w-10 h-10 flex items-center justify-center rounded-full transition-all',
                showNotifications ? 'bg-brand-500 text-white' : 'text-text-medium hover:text-text-dark hover:bg-gray-100'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
              </svg>
              <!-- Badge contador -->
              <span 
                v-if="unseenOrdersCount > 0" 
                class="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] bg-brand-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center ring-2 ring-white animate-pulse"
              >
                {{ unseenOrdersCount > 9 ? '9+' : unseenOrdersCount }}
              </span>
            </button>
            
            <!-- Dropdown de notificaciones -->
            <transition name="fade">
              <div 
                v-if="showNotifications" 
                class="absolute right-0 top-12 w-80 bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden z-50"
              >
                <div class="p-4 border-b border-gray-100 flex items-center justify-between">
                  <h3 class="font-semibold text-text-dark">Notificaciones</h3>
                  <span v-if="recentNotifications.length > 0" class="text-xs text-brand-500 font-medium">
                    {{ recentNotifications.length }} nuevas
                  </span>
                </div>
                <div class="max-h-80 overflow-y-auto">
                  <div 
                    v-if="recentNotifications.length === 0" 
                    class="p-8 text-center text-text-light"
                  >
                    <svg class="w-12 h-12 mx-auto mb-3 text-gray-200" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
                    </svg>
                    <p class="text-sm">No hay notificaciones nuevas</p>
                  </div>
                  <router-link
                    v-for="notif in recentNotifications"
                    :key="notif.id"
                    :to="'/admin/ordenes'"
                    @click="showNotifications = false"
                    class="block p-4 hover:bg-gray-50 border-b border-gray-50 transition-colors"
                  >
                    <div class="flex items-start gap-3">
                      <div class="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                        </svg>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-text-dark">🎉 Nueva orden recibida</p>
                        <p class="text-xs text-text-light mt-0.5">{{ notif.codigo }} • ${{ formatNumber(notif.total) }}</p>
                        <p class="text-[10px] text-text-light/70 mt-1">{{ notif.tiempo }}</p>
                      </div>
                    </div>
                  </router-link>
                </div>
                <router-link 
                  to="/admin/ordenes" 
                  @click="showNotifications = false"
                  class="block p-3 text-center text-sm font-medium text-brand-600 hover:bg-brand-50 border-t border-gray-100 transition-colors"
                >
                  Ver todas las órdenes →
                </router-link>
              </div>
            </transition>
          </div>

          <!-- Divider -->
          <div class="w-px h-6 bg-gray-200 mx-1"></div>

          <!-- Back to Store -->
          <router-link 
            to="/"
            class="flex items-center gap-2 px-3 h-10 text-sm font-medium text-text-medium hover:text-text-dark hover:bg-gray-100 rounded-full transition-all"
            title="Ver tienda"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
            <span class="hidden sm:inline">Tienda</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Sidebar - YouTube/Google Cloud Style -->
    <aside 
      :class="[
        'fixed top-16 bottom-0 left-0 z-40 bg-white border-r border-gray-200 transform transition-all duration-300 ease-in-out overflow-y-auto',
        sidebarCollapsed ? 'w-[70px]' : 'w-60'
      ]"
    >
      <!-- Navigation Menu -->
      <nav class="py-3" :class="sidebarCollapsed ? 'px-2' : 'px-3'">
        <div class="space-y-0.5">
          <router-link 
            v-for="item in menuItems" 
            :key="item.path"
            :to="item.path"
            :class="[
              'flex items-center gap-3 rounded-lg transition-all duration-200 group relative',
              sidebarCollapsed ? 'justify-center px-2 py-3' : 'px-3 py-2.5',
              isActive(item.path) 
                ? 'bg-gray-100 text-text-dark font-medium' 
                : 'text-text-medium hover:text-text-dark hover:bg-gray-50'
            ]"
            :title="sidebarCollapsed ? item.name : ''"
          >
            <!-- Active Indicator (Left Border) -->
            <div 
              v-if="isActive(item.path)"
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-6 bg-text-dark rounded-r-full"
            ></div>
            
            <!-- Icon -->
            <span v-html="item.icon" class="w-5 h-5 flex-shrink-0"></span>
            
            <!-- Label -->
            <span v-if="!sidebarCollapsed" class="flex-1 text-sm">{{ item.name }}</span>
            
            <!-- Badge (expanded) -->
            <span 
              v-if="getItemBadge(item) && !sidebarCollapsed" 
              class="bg-brand-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[18px] text-center"
            >
              {{ getItemBadge(item) }}
            </span>
            
            <!-- Badge Dot (collapsed) -->
            <span 
              v-if="getItemBadge(item) && sidebarCollapsed" 
              class="absolute top-2 right-2 w-2 h-2 bg-brand-500 rounded-full ring-2 ring-white"
            ></span>
          </router-link>
        </div>

        <!-- Separator -->
        <div class="my-4 border-t border-gray-200" :class="sidebarCollapsed ? 'mx-2' : 'mx-3'"></div>

        <!-- Secondary Menu (Config) -->
        <div class="space-y-0.5">
          <router-link 
            to="/admin/config"
            :class="[
              'flex items-center gap-3 rounded-lg transition-all duration-200 group relative',
              sidebarCollapsed ? 'justify-center px-2 py-3' : 'px-3 py-2.5',
              isActive('/admin/config') 
                ? 'bg-gray-100 text-text-dark font-medium' 
                : 'text-text-medium hover:text-text-dark hover:bg-gray-50'
            ]"
            :title="sidebarCollapsed ? 'Configuración' : ''"
          >
            <div 
              v-if="isActive('/admin/config')"
              class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-6 bg-text-dark rounded-r-full"
            ></div>
            <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span v-if="!sidebarCollapsed" class="text-sm">Configuración</span>
          </router-link>
        </div>
      </nav>

      <!-- User Profile (Bottom) -->
      <div class="absolute bottom-0 left-0 right-0 border-t border-gray-200 bg-white">
        <!-- Expanded State -->
        <div v-if="!sidebarCollapsed" class="p-3">
          <div class="flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-50">
            <!-- Avatar -->
            <div class="w-9 h-9 bg-gradient-to-br from-gray-300 to-gray-400 rounded-full flex items-center justify-center text-white font-semibold text-xs">
              {{ userInitials }}
            </div>
            <!-- Info -->
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-text-dark truncate">{{ userName }}</p>
              <p class="text-[10px] text-text-light uppercase tracking-wider">{{ userRole }}</p>
            </div>
            <!-- Logout -->
            <button 
              @click="handleLogout"
              class="w-8 h-8 flex items-center justify-center text-text-light hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors flex-shrink-0"
              title="Cerrar sesión"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Collapsed State -->
        <div v-else class="flex flex-col items-center gap-3 py-4">
          <!-- Avatar -->
          <div class="w-9 h-9 bg-gradient-to-br from-gray-300 to-gray-400 rounded-full flex items-center justify-center text-white font-semibold text-xs">
            {{ userInitials }}
          </div>
          <!-- Logout -->
          <button 
            @click="handleLogout"
            class="w-9 h-9 flex items-center justify-center text-text-light hover:text-red-500 hover:bg-red-50 rounded-full transition-colors"
            title="Cerrar sesión"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Mobile Sidebar Overlay -->
    <div 
      v-if="sidebarOpen"
      @click="sidebarOpen = false"
      class="fixed inset-0 z-40 bg-black/20 lg:hidden"
    ></div>

    <!-- Main Content -->
    <div :class="sidebarCollapsed ? 'lg:ml-[70px]' : 'lg:ml-60'" class="pt-16 transition-all duration-300">
      <!-- Page Content -->
      <main class="p-6 lg:p-8">
        <router-view />
      </main>
    </div>

    <!-- Radio Player Component -->
    <RadioPlayer 
      :visible="showRadio" 
      @playing="isPlaying = $event"
      @station-change="currentStation = $event"
      @close="showRadio = false"
    />

    <!-- Modal de Permisos (Primera vez) - Rediseño Luxury Femenino -->
    <div 
      v-if="showPermissionModal" 
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-md permission-modal-overlay"
    >
      <div class="bg-white rounded-[28px] shadow-luxury max-w-md mx-4 overflow-hidden permission-modal-content">
        <!-- Header - Fondo Blanco con Icono Rosado -->
        <div class="bg-white pt-10 pb-6 px-8 text-center">
          <div class="w-20 h-20 bg-gradient-to-br from-brand-50 to-brand-100 rounded-full flex items-center justify-center mx-auto mb-5 ring-4 ring-brand-100/50">
            <svg class="w-9 h-9 text-brand-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
            </svg>
          </div>
          <h2 class="font-luxury text-3xl font-semibold text-brand-600 mb-2">¡Activa las Notificaciones!</h2>
          <p class="text-text-medium text-sm leading-relaxed px-2">
            Para no perderte ninguna orden nueva, necesitamos<br class="hidden sm:inline" /> tu permiso para enviarte notificaciones y reproducir sonidos.
          </p>
        </div>

        <!-- Body - Espaciado Generoso -->
        <div class="px-8 pb-8">
          <div class="space-y-4 mb-8">
            <!-- Feature 1: Push -->
            <div class="flex items-start gap-4 bg-gradient-to-br from-brand-50/30 to-transparent p-5 rounded-2xl border border-brand-100/30 hover:border-brand-200/50 transition-all duration-300">
              <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm ring-1 ring-brand-100/40">
                <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-sm font-semibold text-[#2A2A2A] mb-1">Notificaciones Push</p>
                <p class="text-xs text-text-light leading-relaxed">Recibe alertas incluso fuera del navegador</p>
              </div>
            </div>

            <!-- Feature 2: Sonido -->
            <div class="flex items-start gap-4 bg-gradient-to-br from-brand-50/30 to-transparent p-5 rounded-2xl border border-brand-100/30 hover:border-brand-200/50 transition-all duration-300">
              <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm ring-1 ring-brand-100/40">
                <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-sm font-semibold text-[#2A2A2A] mb-1">Sonido de Campanita</p>
                <p class="text-xs text-text-light leading-relaxed">Escucha cuando llega una orden nueva</p>
              </div>
            </div>

            <!-- Feature 3: Auto-refresh -->
            <div class="flex items-start gap-4 bg-gradient-to-br from-brand-50/30 to-transparent p-5 rounded-2xl border border-brand-100/30 hover:border-brand-200/50 transition-all duration-300">
              <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm ring-1 ring-brand-100/40">
                <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-sm font-semibold text-[#2A2A2A] mb-1">Actualización Automática</p>
                <p class="text-xs text-text-light leading-relaxed">Sin necesidad de refrescar la página</p>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="space-y-3">
            <button 
              @click="enableNotifications"
              class="w-full bg-gradient-to-r from-brand-500 to-brand-600 hover:from-brand-600 hover:to-brand-700 text-white font-semibold text-sm py-4 px-6 rounded-2xl transition-all duration-300 shadow-luxury-brand"
            >
              🔔 Activar Notificaciones
            </button>
            <button 
              @click="skipPermissions"
              class="w-full text-text-light hover:text-text-medium text-xs py-3 transition-colors font-medium"
            >
              Omitir (podré activarlo después)
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import RadioPlayer from './RadioPlayer.vue'
import { ordenesService } from '@/services/ordenes'

export default {
  name: 'AdminLayout',
  components: {
    RadioPlayer
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const sidebarOpen = ref(false)
    
    // Restaurar estado del sidebar desde localStorage
    const getSidebarState = () => {
      try {
        const saved = localStorage.getItem('sidebarCollapsed')
        return saved === 'true' // Convierte string a boolean
      } catch {
        return false // Por defecto abierto
      }
    }
    
    const sidebarCollapsed = ref(getSidebarState())

    const showRadio = ref(false)
    const isPlaying = ref(false)
    const currentStation = ref('')
    const radioPlayerRef = ref(null)

    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      // Guardar estado en localStorage
      localStorage.setItem('sidebarCollapsed', sidebarCollapsed.value.toString())
    }

    const togglePlayback = () => {
      // Si hay una emisora actual, hacer toggle del play/pause
      if (radioPlayerRef.value) {
        // Abrir el modal para controlar
        showRadio.value = true
      }
    }

    // Contador de órdenes sin ver
    const unseenOrdersCount = ref(0)
    const showNotifications = ref(false)
    const recentNotifications = ref([])
    const lastKnownOrderCount = ref(0)
    const pollingInterval = ref(null)
    const audioContext = ref(null)
    const audioUnlocked = ref(false)
    const showPermissionModal = ref(false)

    // Desbloquear audio después de interacción del usuario
    const unlockAudio = () => {
      if (audioUnlocked.value) return
      
      try {
        audioContext.value = new (window.AudioContext || window.webkitAudioContext)()
        
        // Reproducir sonido silencioso para desbloquear
        const buffer = audioContext.value.createBuffer(1, 1, 22050)
        const source = audioContext.value.createBufferSource()
        source.buffer = buffer
        source.connect(audioContext.value.destination)
        source.start(0)
        
        audioUnlocked.value = true
        console.log('🔊 Audio desbloqueado')
        
        // Remover listeners después de desbloquear
        document.removeEventListener('click', unlockAudio)
        document.removeEventListener('keydown', unlockAudio)
        document.removeEventListener('touchstart', unlockAudio)
      } catch (e) {
        console.warn('Error al desbloquear audio:', e)
      }
    }

    // Reproducir sonido de notificación (campanita real)
    const playNotificationSound = () => {
      try {
        // Asegurar que tenemos un AudioContext activo
        if (!audioContext.value || audioContext.value.state === 'closed') {
          audioContext.value = new (window.AudioContext || window.webkitAudioContext)()
        }
        
        // Resumir si está suspendido
        if (audioContext.value.state === 'suspended') {
          audioContext.value.resume()
        }
        
        const ctx = audioContext.value
        const now = ctx.currentTime
        
        // === SONIDO DE CAMPANITA REAL ===
        
        // Nota 1: Campanita alta
        const osc1 = ctx.createOscillator()
        const gain1 = ctx.createGain()
        osc1.type = 'sine'
        osc1.frequency.setValueAtTime(1568, now) // G6
        gain1.gain.setValueAtTime(0.4, now)
        gain1.gain.exponentialRampToValueAtTime(0.01, now + 0.3)
        osc1.connect(gain1)
        gain1.connect(ctx.destination)
        osc1.start(now)
        osc1.stop(now + 0.3)
        
        // Nota 2: Campanita más alta (delay 0.15s)
        const osc2 = ctx.createOscillator()
        const gain2 = ctx.createGain()
        osc2.type = 'sine'
        osc2.frequency.setValueAtTime(2093, now + 0.15) // C7
        gain2.gain.setValueAtTime(0, now)
        gain2.gain.setValueAtTime(0.35, now + 0.15)
        gain2.gain.exponentialRampToValueAtTime(0.01, now + 0.5)
        osc2.connect(gain2)
        gain2.connect(ctx.destination)
        osc2.start(now + 0.15)
        osc2.stop(now + 0.5)
        
        // Armónicos para hacer el sonido más "metálico" como campana real
        const osc3 = ctx.createOscillator()
        const gain3 = ctx.createGain()
        osc3.type = 'sine'
        osc3.frequency.setValueAtTime(3136, now) // G7 (armónico)
        gain3.gain.setValueAtTime(0.15, now)
        gain3.gain.exponentialRampToValueAtTime(0.01, now + 0.2)
        osc3.connect(gain3)
        gain3.connect(ctx.destination)
        osc3.start(now)
        osc3.stop(now + 0.2)
        
        console.log('🔔 Sonido de campanita reproducido')
        
      } catch (e) {
        console.warn('Error al reproducir sonido:', e)
        // Fallback: intentar con Audio HTML5
        try {
          const audio = new Audio('data:audio/wav;base64,UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YU')
          audio.volume = 0.5
          audio.play().catch(() => {})
        } catch (e2) {
          console.warn('Fallback de audio también falló:', e2)
        }
      }
    }

    // Solicitar permiso para notificaciones push
    const requestNotificationPermission = async () => {
      if (!('Notification' in window)) {
        console.warn('Este navegador no soporta notificaciones')
        return 'denied'
      }

      try {
        const permission = await Notification.requestPermission()
        console.log('🔔 Permiso de notificaciones:', permission)
        
        if (permission === 'granted') {
          console.log('✅ Notificaciones activadas correctamente')
          // NO reproducir sonido aquí - solo cuando llegue una orden real
        }
        
        return permission
      } catch (error) {
        console.error('Error al solicitar permiso:', error)
        return 'denied'
      }
    }

    // Activar notificaciones desde el modal
    const enableNotifications = async () => {
      const permission = await requestNotificationPermission()
      
      if (permission === 'granted') {
        // Guardar que ya se mostró el modal
        localStorage.setItem('notificationsPromptShown', 'true')
        showPermissionModal.value = false
        
        // Mostrar notificación de bienvenida (sin sonido)
        setTimeout(() => {
          new Notification('✅ Notificaciones Activadas', {
            body: 'Recibirás alertas de nuevas órdenes',
            icon: '/favicon.ico',
            silent: true // Sin sonido para la notificación de prueba
          })
        }, 500)
      } else {
        alert('⚠️ Para activar notificaciones, ve a la configuración de tu navegador y permite notificaciones para este sitio.')
      }
    }

    // Omitir permisos por ahora
    const skipPermissions = () => {
      localStorage.setItem('notificationsPromptShown', 'true')
      showPermissionModal.value = false
    }

    // Verificar si ya se mostró el modal
    const shouldShowPermissionModal = () => {
      const alreadyShown = localStorage.getItem('notificationsPromptShown')
      const notificationPermission = 'Notification' in window ? Notification.permission : 'denied'
      
      // Mostrar si no se ha mostrado antes Y las notificaciones no están permitidas
      return !alreadyShown && notificationPermission !== 'granted'
    }

    // Mostrar notificación push del navegador
    const showBrowserNotification = (orden) => {
      if ('Notification' in window && Notification.permission === 'granted') {
        const notification = new Notification('🎉 Nueva Orden Recibida!', {
          body: `Orden ${orden.codigo} - $${formatNumber(orden.total)}`,
          icon: '/favicon.ico',
          tag: 'nueva-orden-' + orden.id,
          requireInteraction: true,
          vibrate: [200, 100, 200]
        })
        
        // Click en la notificación abre la vista de órdenes
        notification.onclick = () => {
          window.focus()
          router.push('/admin/ordenes')
          notification.close()
        }
        
        // Auto cerrar después de 10 segundos
        setTimeout(() => notification.close(), 10000)
      }
    }

    // Formatear número
    const formatNumber = (num) => {
      return new Intl.NumberFormat('es-CO').format(num || 0)
    }

    const getSeenOrders = () => {
      try {
        return JSON.parse(localStorage.getItem('seenOrders') || '[]')
      } catch {
        return []
      }
    }

    // Polling para detectar nuevas órdenes
    const checkForNewOrders = async () => {
      try {
        const ordenes = await ordenesService.obtenerTodas()
        const seen = getSeenOrders()
        
        // Contar órdenes no vistas
        const unseen = ordenes.filter(o => !seen.includes(o.id))
        unseenOrdersCount.value = unseen.length
        
        // Detectar si hay NUEVAS órdenes (comparar con último conteo conocido)
        if (ordenes.length > lastKnownOrderCount.value && lastKnownOrderCount.value > 0) {
          const nuevasOrdenes = ordenes.length - lastKnownOrderCount.value
          console.log(`🔔 ${nuevasOrdenes} nueva(s) orden(es) detectada(s)!`)
          
          // Obtener las órdenes más recientes (las nuevas)
          const ordenesNuevas = ordenes.slice(0, nuevasOrdenes)
          
          // Reproducir sonido UNA SOLA VEZ (no por cada orden)
          playNotificationSound()
          
          // Agregar a notificaciones recientes
          ordenesNuevas.forEach((orden, index) => {
            recentNotifications.value.unshift({
              id: orden.id,
              codigo: orden.codigo || 'Nueva Orden',
              total: orden.total || 0,
              tiempo: 'Hace un momento'
            })
            
            // Mostrar notificación push solo para la primera (evitar spam)
            if (index === 0) {
              if (nuevasOrdenes > 1) {
                // Si hay múltiples, mostrar notificación agrupada
                showBrowserNotification({
                  ...orden,
                  codigo: `${nuevasOrdenes} nuevas órdenes`
                })
              } else {
                showBrowserNotification(orden)
              }
            }
          })
          
          // Limitar a 10 notificaciones recientes
          recentNotifications.value = recentNotifications.value.slice(0, 10)
        }
        
        lastKnownOrderCount.value = ordenes.length
      } catch (error) {
        console.error('Error al verificar nuevas órdenes:', error)
      }
    }

    // Iniciar polling
    const startOrderPolling = () => {
      // Verificar cada 5 segundos
      pollingInterval.value = setInterval(checkForNewOrders, 5000)
    }

    // Detener polling
    const stopOrderPolling = () => {
      if (pollingInterval.value) {
        clearInterval(pollingInterval.value)
        pollingInterval.value = null
      }
    }

    const toggleNotifications = () => {
      showNotifications.value = !showNotifications.value
    }

    // Cerrar dropdown al hacer clic fuera
    const closeNotificationsOnClickOutside = (event) => {
      if (showNotifications.value && !event.target.closest('.relative')) {
        showNotifications.value = false
      }
    }

    const updateUnseenCount = async () => {
      try {
        const ordenes = await ordenesService.obtenerTodas()
        const seen = getSeenOrders()
        unseenOrdersCount.value = ordenes.filter(o => !seen.includes(o.id)).length
        lastKnownOrderCount.value = ordenes.length
      } catch (error) {
        console.error('Error al obtener órdenes:', error)
      }
    }

    // Escuchar eventos de actualización
    const handleOrdenesUpdated = () => {
      updateUnseenCount()
    }

    // Menu items with thin stroke icons
    const menuItems = ref([
      {
        name: 'Dashboard',
        path: '/admin',
        icon: '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/></svg>',
        badge: null
      },
      {
        name: 'Productos',
        path: '/admin/productos',
        icon: '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z"/></svg>',
        badge: null
      },
      {
        name: 'Órdenes',
        path: '/admin/ordenes',
        icon: '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z"/></svg>',
        badgeKey: 'ordenes'
      },
      {
        name: 'Clientes',
        path: '/admin/clientes',
        icon: '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"/></svg>',
        badge: null
      },
      {
        name: 'Inventario',
        path: '/admin/inventario',
        icon: '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3"/></svg>',
        badge: '3'
      },
      {
        name: 'Categorías',
        path: '/admin/categorias',
        icon: '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z"/><path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6z"/></svg>',
        badge: null
      },
      {
        name: 'Usuarios',
        path: '/admin/usuarios',
        icon: '<svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/></svg>',
        badge: null
      }
    ])

    // Check if route is active
    const isActive = (path) => {
      if (path === '/admin') {
        return route.path === '/admin'
      }
      return route.path.startsWith(path)
    }

    // User info from localStorage
    const user = computed(() => {
      try {
        return JSON.parse(localStorage.getItem('user') || '{}')
      } catch {
        return {}
      }
    })

    const userName = computed(() => user.value.nombre || user.value.email || 'Admin')
    const userRole = computed(() => user.value.rol || 'ADMIN')
    const userInitials = computed(() => {
      const name = userName.value
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    })

    // Page title based on route
    const pageTitle = computed(() => {
      const titles = {
        '/admin': 'Dashboard',
        '/admin/productos': 'Productos',
        '/admin/ordenes': 'Órdenes',
        '/admin/clientes': 'Clientes',
        '/admin/inventario': 'Inventario',
        '/admin/categorias': 'Categorías',
        '/admin/usuarios': 'Usuarios',
        '/admin/config': 'Configuración'
      }
      return titles[route.path] || 'Admin'
    })

    const handleLogout = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      router.push('/')
    }

    // Función para obtener badge dinámico
    const getItemBadge = (item) => {
      if (item.badgeKey === 'ordenes') {
        return unseenOrdersCount.value > 0 ? unseenOrdersCount.value : null
      }
      return item.badge || null
    }

    onMounted(() => {
      // Mostrar modal de permisos si es necesario (con delay para mejor UX)
      setTimeout(() => {
        showPermissionModal.value = shouldShowPermissionModal()
      }, 1000)
      
      // Desbloquear audio con la primera interacción del usuario
      document.addEventListener('click', unlockAudio)
      document.addEventListener('keydown', unlockAudio)
      document.addEventListener('touchstart', unlockAudio)
      
      // Si ya tiene permisos, solo solicitarlos silenciosamente
      if (!shouldShowPermissionModal()) {
        requestNotificationPermission()
      }
      
      // Cargar conteo inicial
      updateUnseenCount()
      
      // Iniciar polling para detectar nuevas órdenes
      startOrderPolling()
      
      // Escuchar eventos de actualización
      window.addEventListener('ordenes-updated', handleOrdenesUpdated)
      
      // Cerrar dropdown al hacer clic fuera
      document.addEventListener('click', closeNotificationsOnClickOutside)
    })

    onUnmounted(() => {
      stopOrderPolling()
      window.removeEventListener('ordenes-updated', handleOrdenesUpdated)
      document.removeEventListener('click', closeNotificationsOnClickOutside)
      document.removeEventListener('click', unlockAudio)
      document.removeEventListener('keydown', unlockAudio)
      document.removeEventListener('touchstart', unlockAudio)
      
      // Cerrar AudioContext si existe
      if (audioContext.value) {
        audioContext.value.close().catch(() => {})
      }
    })

    return {
      sidebarOpen,
      sidebarCollapsed,
      toggleSidebar,
      showRadio,
      isPlaying,
      currentStation,
      radioPlayerRef,
      togglePlayback,
      menuItems,
      isActive,
      userName,
      userRole,
      userInitials,
      pageTitle,
      handleLogout,
      getItemBadge,
      unseenOrdersCount,
      showNotifications,
      toggleNotifications,
      recentNotifications,
      formatNumber,
      showPermissionModal,
      enableNotifications,
      skipPermissions
    }
  }
}
</script>

<style scoped>
@keyframes music-bar {
  0%, 100% { height: 30%; }
  50% { height: 100%; }
}

.animate-music-bar {
  animation: music-bar 0.6s ease-in-out infinite;
}

/* Transiciones para dropdown */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Animación para modal */
@keyframes scale-in {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scale-in 0.3s ease-out;
}
</style>
