<template>
  <div class="min-h-screen bg-[#F9FAFB]">
    <!-- Sidebar - Clean Canvas Style -->
    <aside 
      :class="[
        'fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-gray-100 transform transition-transform duration-300 ease-in-out lg:translate-x-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <!-- Logo - Minimal -->
      <div class="flex items-center h-20 px-8 border-b border-gray-50">
        <router-link to="/" class="flex items-center gap-3 group">
          <span class="font-luxury text-2xl text-text-dark tracking-wide">Kharis</span>
          <span class="text-[10px] uppercase tracking-widest text-text-light font-medium">Admin</span>
        </router-link>
      </div>

      <!-- Navigation - Minimal -->
      <nav class="mt-8 px-6">
        <div class="space-y-1">
          <router-link 
            v-for="item in menuItems" 
            :key="item.path"
            :to="item.path"
            :class="[
              'flex items-center gap-4 px-4 py-3.5 rounded-xl transition-all duration-200 group relative',
              isActive(item.path) 
                ? 'text-text-dark font-semibold' 
                : 'text-text-medium hover:text-text-dark hover:bg-gray-50'
            ]"
          >
            <!-- Active Indicator -->
            <div 
              v-if="isActive(item.path)"
              class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-brand-600 rounded-r-full"
            ></div>
            
            <span v-html="item.icon" class="w-5 h-5 opacity-70 group-hover:opacity-100"></span>
            <span class="flex-1">{{ item.name }}</span>
            <span 
              v-if="item.badge" 
              class="bg-brand-50 text-brand-600 text-xs font-semibold px-2.5 py-1 rounded-full"
            >
              {{ item.badge }}
            </span>
          </router-link>
        </div>

        <!-- Separator -->
        <div class="my-8 border-t border-gray-100"></div>

        <!-- Secondary Menu -->
        <div class="space-y-1">
          <router-link 
            to="/admin/config"
            :class="[
              'flex items-center gap-4 px-4 py-3.5 rounded-xl transition-all duration-200 group relative',
              isActive('/admin/config') 
                ? 'text-text-dark font-semibold' 
                : 'text-text-medium hover:text-text-dark hover:bg-gray-50'
            ]"
          >
            <div 
              v-if="isActive('/admin/config')"
              class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-brand-600 rounded-r-full"
            ></div>
            <svg class="w-5 h-5 opacity-70" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>Configuración</span>
          </router-link>
        </div>
      </nav>

      <!-- User Info (Bottom) - Minimal -->
      <div class="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-50">
        <div class="flex items-center gap-4">
          <div class="w-11 h-11 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl flex items-center justify-center text-text-dark font-semibold text-sm">
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-text-dark truncate">{{ userName }}</p>
            <p class="text-xs text-text-light uppercase tracking-wider">{{ userRole }}</p>
          </div>
          <button 
            @click="handleLogout"
            class="p-2.5 text-text-light hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
            title="Cerrar sesión"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
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
    <div class="lg:ml-72">
      <!-- Top Header - Minimal -->
      <header class="sticky top-0 z-30 bg-[#F9FAFB]/80 border-b border-gray-100/50">
        <div class="flex items-center justify-between h-20 px-6 lg:px-10">
          <!-- Mobile Menu Button -->
          <button 
            @click="sidebarOpen = !sidebarOpen"
            class="p-2.5 text-text-medium rounded-xl hover:bg-white hover:shadow-sm lg:hidden transition-all"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
          </button>

          <!-- Page Title -->
          <h1 class="hidden lg:block text-lg font-medium text-text-dark">{{ pageTitle }}</h1>

          <!-- Right Actions -->
          <div class="flex items-center gap-3">
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
                'relative flex items-center gap-2 px-3 py-2 rounded-xl transition-all',
                showRadio 
                  ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30' 
                  : 'text-text-medium hover:text-text-dark hover:bg-white hover:shadow-sm'
              ]"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 7.5l16.5-4.125M12 6.75c-2.708 0-5.363.224-7.948.655C2.999 7.58 2.25 8.507 2.25 9.574v9.176A2.25 2.25 0 004.5 21h15a2.25 2.25 0 002.25-2.25V9.574c0-1.067-.75-1.994-1.802-2.169A48.329 48.329 0 0012 6.75zm-1.683 6.443l-.311.311a1.125 1.125 0 01-1.59-1.59l.31-.312a1.125 1.125 0 011.591 1.591zm.22 3.17a.75.75 0 001.06 0l3.126-3.125a.75.75 0 00-1.06-1.061l-3.126 3.125a.75.75 0 000 1.061zm4.713-3.17l.311.311a1.125 1.125 0 01-1.59 1.59l-.312-.31a1.125 1.125 0 011.591-1.591z" />
              </svg>
              <span class="hidden sm:inline text-sm font-medium">Radio</span>
            </button>

            <!-- Notifications -->
            <button class="relative p-2.5 text-text-medium hover:text-text-dark hover:bg-white rounded-xl transition-all hover:shadow-sm">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
              </svg>
              <span class="absolute top-2 right-2 w-2 h-2 bg-brand-500 rounded-full ring-2 ring-[#F9FAFB]"></span>
            </button>

            <!-- Divider -->
            <div class="w-px h-6 bg-gray-200"></div>

            <!-- Back to Store -->
            <router-link 
              to="/"
              class="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-text-medium hover:text-text-dark hover:bg-white rounded-xl transition-all hover:shadow-sm"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
              </svg>
              <span class="hidden sm:inline">Ver tienda</span>
            </router-link>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="p-6 lg:p-10">
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
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import RadioPlayer from './RadioPlayer.vue'

export default {
  name: 'AdminLayout',
  components: {
    RadioPlayer
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const sidebarOpen = ref(false)
    const showRadio = ref(false)
    const isPlaying = ref(false)
    const currentStation = ref('')
    const radioPlayerRef = ref(null)

    const togglePlayback = () => {
      // Si hay una emisora actual, hacer toggle del play/pause
      if (radioPlayerRef.value) {
        // Abrir el modal para controlar
        showRadio.value = true
      }
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
        badge: '5'
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

    return {
      sidebarOpen,
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
      handleLogout
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
</style>
