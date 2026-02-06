<template>
  <div class="min-h-screen bg-[#FAFAFA] flex flex-col">
    <!-- =========================================================================
         TOP NAVIGATION BAR - Beauty Brand B2B Header
    ========================================================================== -->
    <header class="bg-[#0F0F0F] text-white sticky top-0 z-50">
      <div class="max-w-[1600px] mx-auto">
        <!-- Top utility bar -->
        <div class="hidden lg:flex items-center justify-between px-4 sm:px-6 lg:px-8 py-1.5 border-b border-white/5 text-[11px]">
          <div class="flex items-center gap-4 text-white/50">
            <a href="#" class="flex items-center gap-1.5 hover:text-white/80 transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
              </svg>
              <span>Ingresa tu ubicación para ver tiempos de entrega</span>
            </a>
          </div>
          <div class="flex items-center gap-4 text-white/50">
            <a href="#" class="hover:text-[#C9A962] transition-colors">Centro de ayuda</a>
            <span class="text-white/20">|</span>
            <a href="https://wa.me/573001234567" target="_blank" class="flex items-center gap-1.5 hover:text-emerald-400 transition-colors">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/></svg>
              WhatsApp B2B
            </a>
          </div>
        </div>

        <div class="flex items-center justify-between h-14 px-4 sm:px-6 lg:px-8">
          
          <!-- Left: Logo + Nav -->
          <div class="flex items-center gap-6 lg:gap-8">
            <!-- Logo -->
            <router-link to="/portal" class="flex items-center gap-3 group">
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#C9A962] to-[#A8893D] p-0.5">
                <div class="w-full h-full rounded-full bg-[#0F0F0F] flex items-center justify-center">
                  <img src="/logo-kharis.png" alt="Kharis Pro" class="w-7 h-7 object-contain" />
                </div>
              </div>
              <div class="hidden sm:block">
                <span class="text-[#C9A962] font-luxury text-lg tracking-wider">KHARIS PRO</span>
                <span class="block text-white/40 text-[10px] tracking-widest uppercase">Portal Mayoristas</span>
              </div>
            </router-link>

            <!-- Desktop Navigation - Beauty Categories -->
            <nav class="hidden lg:flex items-center">
              <!-- Main Categories with hover effect -->
              <router-link 
                to="/portal/catalogo?categoria=pelucas"
                class="relative px-3 py-2 text-[13px] font-medium text-white/70 hover:text-white transition-all duration-200 group"
              >
                PELUCAS
                <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-0.5 bg-[#C9A962] rounded-full group-hover:w-6 transition-all duration-300"></span>
              </router-link>
              <router-link 
                to="/portal/catalogo?categoria=extensiones"
                class="relative px-3 py-2 text-[13px] font-medium text-white/70 hover:text-white transition-all duration-200 group"
              >
                EXTENSIONES
                <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-0.5 bg-[#C9A962] rounded-full group-hover:w-6 transition-all duration-300"></span>
              </router-link>
              <router-link 
                to="/portal/catalogo?categoria=sistemas-capilares"
                class="relative px-3 py-2 text-[13px] font-medium text-white/70 hover:text-white transition-all duration-200 group"
              >
                SISTEMAS
                <span class="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-0.5 bg-[#C9A962] rounded-full group-hover:w-6 transition-all duration-300"></span>
              </router-link>
              
              <span class="w-px h-5 bg-white/10 mx-2"></span>
              
              <router-link 
                to="/portal/catalogo?nuevo=true"
                class="relative px-3 py-2 text-[13px] font-medium text-[#E8B4B8] hover:text-[#F0C4C8] transition-all duration-200 group flex items-center gap-1.5"
              >
                NUEVOS
                <span class="w-1.5 h-1.5 bg-[#E8B4B8] rounded-full animate-pulse"></span>
              </router-link>
              <router-link 
                to="/portal/catalogo?oferta=true"
                class="relative px-3 py-2 text-[13px] font-medium text-rose-400 hover:text-rose-300 transition-all duration-200"
              >
                OFERTAS
              </router-link>
            </nav>
          </div>

          <!-- Right: Actions -->
          <div class="flex items-center gap-2 sm:gap-4">
            <!-- Search Button -->
            <button 
              @click="showSearchModal = true"
              class="hidden sm:flex items-center gap-2 px-3 py-2 bg-white/5 hover:bg-white/10 rounded-lg transition-colors text-white/60 hover:text-white text-sm"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span class="hidden md:inline">Buscar...</span>
              <kbd class="hidden lg:inline ml-2 px-1.5 py-0.5 bg-white/10 rounded text-[10px] font-mono">⌘K</kbd>
            </button>

            <!-- Cart -->
            <router-link to="/portal/carrito" class="relative p-2 text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              <span v-if="cartCount > 0" class="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 bg-[#C9A962] text-[#0F0F0F] text-[10px] font-bold rounded-full flex items-center justify-center">
                {{ cartCount > 99 ? '99+' : cartCount }}
              </span>
            </router-link>

            <!-- User Menu -->
            <div class="relative" ref="userMenuRef">
              <button @click="showUserMenu = !showUserMenu" class="flex items-center gap-2 p-1.5 hover:bg-white/5 rounded-lg transition-colors">
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#C9A962] to-[#A8893D] flex items-center justify-center">
                  <span class="text-[#0F0F0F] text-sm font-bold">{{ userInitials }}</span>
                </div>
                <div class="hidden md:block text-left">
                  <p class="text-sm font-medium text-white truncate max-w-[120px]">{{ user.nombre }}</p>
                  <p class="text-[10px] text-white/40">{{ user.nivel || 'Mayorista' }}</p>
                </div>
                <svg class="w-4 h-4 text-white/40 hidden sm:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <transition name="dropdown">
                <div v-if="showUserMenu" class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-2xl border border-gray-100 overflow-hidden z-50">
                  <div class="px-4 py-4 bg-gradient-to-br from-gray-50 to-white border-b border-gray-100">
                    <p class="font-semibold text-gray-900 truncate">{{ user.nombre }}</p>
                    <p class="text-sm text-gray-500 truncate">{{ user.email }}</p>
                    <div class="flex items-center gap-2 mt-2">
                      <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-[#C9A962]/10 text-[#C9A962] text-xs font-semibold rounded-full border border-[#C9A962]/20">
                        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        {{ user.nivel || 'Mayorista' }}
                      </span>
                    </div>
                  </div>
                  <div class="py-2">
                    <router-link to="/portal/cuenta" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors" @click="showUserMenu = false">
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                      Mi Cuenta
                    </router-link>
                    <router-link to="/portal/pedidos" class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors" @click="showUserMenu = false">
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
                      Historial de Pedidos
                    </router-link>
                  </div>
                  <div class="border-t border-gray-100 py-2">
                    <button @click="handleLogout" class="flex items-center gap-3 w-full px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                      Cerrar Sesión
                    </button>
                  </div>
                </div>
              </transition>
            </div>

            <!-- Mobile Menu Toggle -->
            <button @click="showMobileMenu = !showMobileMenu" class="lg:hidden p-2 text-white/60 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
              <svg v-if="!showMobileMenu" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" /></svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </div>

        <!-- Mobile Navigation - Beauty Categories -->
        <transition name="slide">
          <nav v-if="showMobileMenu" class="lg:hidden border-t border-white/5 pb-4">
            <div class="px-4 pt-4 space-y-1">
              <!-- Beauty Categories -->
              <p class="px-4 py-2 text-[10px] text-white/30 uppercase tracking-widest font-medium">Categorías</p>
              <router-link to="/portal/catalogo?categoria=pelucas" class="flex items-center gap-3 px-4 py-3 text-white/70 hover:text-white hover:bg-white/5 rounded-lg transition-colors" @click="showMobileMenu = false">
                <svg class="w-5 h-5 text-[#C9A962]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>
                Pelucas
              </router-link>
              <router-link to="/portal/catalogo?categoria=extensiones" class="flex items-center gap-3 px-4 py-3 text-white/70 hover:text-white hover:bg-white/5 rounded-lg transition-colors" @click="showMobileMenu = false">
                <svg class="w-5 h-5 text-[#E8B4B8]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" /></svg>
                Extensiones
              </router-link>
              <router-link to="/portal/catalogo?categoria=sistemas-capilares" class="flex items-center gap-3 px-4 py-3 text-white/70 hover:text-white hover:bg-white/5 rounded-lg transition-colors" @click="showMobileMenu = false">
                <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" /></svg>
                Sistemas Capilares
              </router-link>
              
              <div class="border-t border-white/5 my-3"></div>
              
              <router-link to="/portal/catalogo?nuevo=true" class="flex items-center gap-3 px-4 py-3 text-[#E8B4B8] hover:text-[#F0C4C8] hover:bg-white/5 rounded-lg transition-colors" @click="showMobileMenu = false">
                <span class="w-2 h-2 bg-[#E8B4B8] rounded-full animate-pulse"></span>
                Nuevos Lanzamientos
              </router-link>
              <router-link to="/portal/catalogo?oferta=true" class="flex items-center gap-3 px-4 py-3 text-rose-400 hover:text-rose-300 hover:bg-white/5 rounded-lg transition-colors" @click="showMobileMenu = false">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 6h.008v.008H6V6z" /></svg>
                Ofertas
              </router-link>
              
              <div class="border-t border-white/5 my-3"></div>
              <p class="px-4 py-2 text-[10px] text-white/30 uppercase tracking-widest font-medium">Mi cuenta</p>
              
              <router-link v-for="item in navItems" :key="item.to" :to="item.to" class="flex items-center gap-3 px-4 py-3 text-white/70 hover:text-white hover:bg-white/5 rounded-lg transition-colors" :class="{ 'text-white bg-white/5': isActiveRoute(item.to) }" @click="showMobileMenu = false">
                {{ item.label }}
              </router-link>
            </div>
          </nav>
        </transition>
      </div>
    </header>

    <!-- Welcome Bar - Más compacta y elegante -->
    <div class="bg-[#18181B] border-b border-white/5">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-2">
        <div class="flex items-center justify-between gap-3 text-xs sm:text-sm">
          <div class="flex items-center gap-3 sm:gap-4">
            <span class="text-white/50">Hola, <span class="text-white/80 font-medium">{{ user.nombre?.split(' ')[0] || 'Mayorista' }}</span></span>
            <div class="hidden sm:flex items-center gap-1.5 text-[#C9A962]/80">
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              <span class="font-medium">{{ user.nivel || 'Gold' }}</span>
              <span class="text-white/30">·</span>
              <span class="text-emerald-400/80">{{ user.descuento || '15' }}% OFF</span>
            </div>
          </div>
          <div class="flex items-center gap-3 sm:gap-5 text-white/50">
            <div class="hidden sm:flex items-center gap-1.5">
              <span>Saldo:</span>
              <span class="text-emerald-400 font-medium">${{ formatPrice(accountBalance) }}</span>
            </div>
            <router-link to="/portal/carrito" class="flex items-center gap-1.5 text-white/70 hover:text-white transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
              <span class="font-medium">${{ formatPrice(cartTotal) }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="flex-1">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- Footer - Más sutil -->
    <footer class="bg-[#0F0F0F] text-white/40 py-6 mt-auto border-t border-white/5">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 rounded-full bg-gradient-to-br from-[#C9A962] to-[#A8893D] p-0.5">
              <div class="w-full h-full rounded-full bg-[#0F0F0F] flex items-center justify-center">
                <img src="/logo-kharis.png" alt="Kharis Pro" class="w-4 h-4 object-contain" />
              </div>
            </div>
            <span>&copy; {{ new Date().getFullYear() }} Kharis Distribuidora</span>
          </div>
          <div class="flex items-center gap-4">
            <a href="#" class="hover:text-[#C9A962] transition-colors">Términos</a>
            <a href="#" class="hover:text-[#C9A962] transition-colors">Privacidad</a>
            <a :href="retailUrl" class="hover:text-[#C9A962] transition-colors">Tienda Retail</a>
          </div>
        </div>
      </div>
    </footer>

    <!-- Search Modal -->
    <Teleport to="body">
      <transition name="modal">
        <div v-if="showSearchModal" class="fixed inset-0 z-[60] flex items-start justify-center pt-20 px-4">
          <div class="absolute inset-0 bg-black/60" @click="showSearchModal = false"></div>
          <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden">
            <div class="flex items-center gap-4 p-4 border-b border-gray-100">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              <input v-model="searchQuery" ref="searchInput" type="text" placeholder="Buscar productos, SKU..." class="flex-1 text-lg outline-none placeholder:text-gray-400" @keydown.esc="showSearchModal = false" />
              <button @click="showSearchModal = false" class="p-2 hover:bg-gray-100 rounded-lg"><svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg></button>
            </div>
            <div class="p-4 max-h-96 overflow-y-auto"><p class="text-sm text-gray-500 text-center py-8">Escribe para buscar productos...</p></div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getCrossContextUrl, APP_CONTEXT } from '../../utils/subdomain'

export default {
  name: 'B2BLayout',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userMenuRef = ref(null)
    const searchInput = ref(null)
    const showUserMenu = ref(false)
    const showMobileMenu = ref(false)
    const showSearchModal = ref(false)
    const searchQuery = ref('')
    const accountBalance = ref(0)
    const cartTotal = ref(0)

    const navItems = [
      { to: '/portal', label: 'Dashboard' },
      { to: '/portal/catalogo', label: 'Catálogo' },
      { to: '/portal/pedidos', label: 'Mis Pedidos' },
    ]

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
      if (cart) { try { return JSON.parse(cart).items?.length || 0 } catch { return 0 } }
      return 0
    })

    const retailUrl = computed(() => getCrossContextUrl(APP_CONTEXT.B2C))

    function isActiveRoute(path) {
      if (path === '/portal') return route.path === '/portal'
      return route.path.startsWith(path)
    }

    function formatPrice(value) { return value?.toLocaleString('es-CO') || '0' }

    function handleLogout() {
      localStorage.removeItem('b2b_access_token')
      localStorage.removeItem('b2b_refresh_token')
      localStorage.removeItem('b2b_user')
      localStorage.removeItem('b2b_cart')
      router.push('/portal/login')
    }

    function handleClickOutside(event) {
      if (userMenuRef.value && !userMenuRef.value.contains(event.target)) showUserMenu.value = false
    }

    function handleKeyboard(event) {
      if ((event.metaKey || event.ctrlKey) && event.key === 'k') { event.preventDefault(); showSearchModal.value = true }
    }

    watch(showSearchModal, async (val) => { if (val) { await nextTick(); searchInput.value?.focus() } })

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
      document.addEventListener('keydown', handleKeyboard)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
      document.removeEventListener('keydown', handleKeyboard)
    })

    return { userMenuRef, searchInput, showUserMenu, showMobileMenu, showSearchModal, searchQuery, navItems, user, userInitials, cartCount, cartTotal, accountBalance, retailUrl, isActiveRoute, formatPrice, handleLogout }
  }
}
</script>

<style scoped>
.dropdown-enter-active, .dropdown-leave-active { transition: all 0.2s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-10px); }
.slide-enter-active, .slide-leave-active { transition: all 0.3s ease; }
.slide-enter-from, .slide-leave-to { opacity: 0; max-height: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.modal-enter-active, .modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
