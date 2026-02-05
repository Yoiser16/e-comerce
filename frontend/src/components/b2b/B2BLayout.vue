<template>
  <div class="min-h-screen bg-[#F8F6F3]">
    <!-- B2B Header -->
    <header class="bg-[#1A1A1A] text-white sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <router-link to="/portal" class="flex items-center gap-3">
            <img src="/logo-kharis.png" alt="Kharis Pro" class="w-10 h-10 rounded-full bg-white/10 p-1" />
            <div>
              <span class="text-[#C9A962] font-luxury text-lg tracking-wider">KHARIS PRO</span>
              <span class="hidden sm:block text-white/50 text-xs">Portal Mayoristas</span>
            </div>
          </router-link>

          <!-- Navigation Desktop -->
          <nav class="hidden md:flex items-center gap-6">
            <router-link 
              v-for="item in navItems" 
              :key="item.to"
              :to="item.to"
              class="text-white/70 hover:text-white text-sm tracking-wide transition-colors"
              active-class="text-[#C9A962]"
            >
              {{ item.label }}
            </router-link>
          </nav>

          <!-- Actions -->
          <div class="flex items-center gap-4">
            <!-- Cart -->
            <router-link 
              to="/portal/carrito" 
              class="relative p-2 text-white/70 hover:text-white transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              <span 
                v-if="cartCount > 0"
                class="absolute -top-1 -right-1 w-5 h-5 bg-[#C9A962] text-[#1A1A1A] text-xs font-bold rounded-full flex items-center justify-center"
              >
                {{ cartCount }}
              </span>
            </router-link>

            <!-- User Menu -->
            <div class="relative" ref="userMenuRef">
              <button 
                @click="showUserMenu = !showUserMenu"
                class="flex items-center gap-2 p-2 text-white/70 hover:text-white transition-colors"
              >
                <div class="w-8 h-8 rounded-full bg-[#C9A962]/20 flex items-center justify-center">
                  <span class="text-[#C9A962] text-sm font-medium">{{ userInitials }}</span>
                </div>
                <svg class="w-4 h-4 hidden sm:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Dropdown -->
              <transition name="dropdown">
                <div 
                  v-if="showUserMenu"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 z-50"
                >
                  <div class="px-4 py-2 border-b border-gray-100">
                    <p class="text-sm font-medium text-text-dark truncate">{{ user.nombre }}</p>
                    <p class="text-xs text-text-light truncate">{{ user.email }}</p>
                  </div>
                  <router-link 
                    to="/portal/cuenta" 
                    class="block px-4 py-2 text-sm text-text-medium hover:bg-gray-50"
                    @click="showUserMenu = false"
                  >
                    Mi Cuenta
                  </router-link>
                  <router-link 
                    to="/portal/pedidos" 
                    class="block px-4 py-2 text-sm text-text-medium hover:bg-gray-50"
                    @click="showUserMenu = false"
                  >
                    Mis Pedidos
                  </router-link>
                  <button 
                    @click="handleLogout"
                    class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                  >
                    Cerrar sesión
                  </button>
                </div>
              </transition>
            </div>

            <!-- Mobile Menu Toggle -->
            <button 
              @click="showMobileMenu = !showMobileMenu"
              class="md:hidden p-2 text-white/70 hover:text-white"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <transition name="slide">
        <nav v-if="showMobileMenu" class="md:hidden border-t border-white/10 py-4 px-4">
          <router-link 
            v-for="item in navItems" 
            :key="item.to"
            :to="item.to"
            class="block py-3 text-white/70 hover:text-white text-sm tracking-wide border-b border-white/5"
            active-class="text-[#C9A962]"
            @click="showMobileMenu = false"
          >
            {{ item.label }}
          </router-link>
        </nav>
      </transition>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <router-view />
    </main>

    <!-- B2B Footer -->
    <footer class="bg-[#1A1A1A] text-white/50 py-6 mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm">
        <p>&copy; {{ new Date().getFullYear() }} Kharis Distribuidora. Portal Mayoristas.</p>
        <p class="mt-1">
          <a href="#" class="hover:text-[#C9A962]">Términos</a> · 
          <a href="#" class="hover:text-[#C9A962]">Privacidad</a> · 
          <a :href="retailUrl" class="hover:text-[#C9A962]">Tienda Retail</a>
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCrossContextUrl, APP_CONTEXT } from '../../utils/subdomain'

export default {
  name: 'B2BLayout',
  setup() {
    const router = useRouter()
    const showUserMenu = ref(false)
    const showMobileMenu = ref(false)
    const userMenuRef = ref(null)

    const navItems = [
      { to: '/portal', label: 'Dashboard' },
      { to: '/portal/catalogo', label: 'Catálogo' },
      { to: '/portal/pedidos', label: 'Mis Pedidos' },
    ]

    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{"nombre": "Usuario", "email": ""}')
    })

    const userInitials = computed(() => {
      const nombre = user.value.nombre || 'U'
      return nombre.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    })

    const cartCount = computed(() => {
      // TODO: Conectar con store de carrito B2B
      return 0
    })

    const retailUrl = computed(() => getCrossContextUrl(APP_CONTEXT.B2C))

    function handleLogout() {
      localStorage.removeItem('b2b_access_token')
      localStorage.removeItem('b2b_refresh_token')
      localStorage.removeItem('b2b_user')
      router.push('/login')
    }

    // Cerrar menú al hacer click fuera
    function handleClickOutside(event) {
      if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
        showUserMenu.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      navItems,
      user,
      userInitials,
      cartCount,
      retailUrl,
      showUserMenu,
      showMobileMenu,
      userMenuRef,
      handleLogout
    }
  }
}
</script>

<style scoped>
.dropdown-enter-active, .dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from, .slide-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
