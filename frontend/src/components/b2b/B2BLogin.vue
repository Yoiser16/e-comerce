<template>
  <div class="min-h-screen bg-[#1A1A1A] flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-md">
      <!-- Header / Branding -->
      <div class="text-center mb-8">
        <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-white/10 p-3">
          <img 
            src="/logo-kharis.png" 
            alt="Kharis Pro" 
            class="w-full h-full object-contain"
          />
        </div>
        <h1 class="text-[#C9A962] text-2xl font-luxury tracking-wider mb-1">KHARIS PRO</h1>
        <p class="text-white/50 text-sm tracking-wide">Portal Exclusivo Mayoristas</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white rounded-lg shadow-xl p-6 sm:p-8">
        <h2 class="text-text-dark text-xl font-medium mb-6 text-center">
          Accede a tu cuenta
        </h2>

        <!-- Error Message -->
        <div 
          v-if="error" 
          class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm"
        >
          {{ error }}
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-text-medium mb-1">
              Correo electrónico
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              placeholder="tu@empresa.com"
              class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] transition-all outline-none"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-text-medium mb-1">
              Contraseña
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] transition-all outline-none"
            />
          </div>

          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2 cursor-pointer">
              <input 
                v-model="form.remember" 
                type="checkbox" 
                class="w-4 h-4 text-[#C9A962] border-gray-300 rounded focus:ring-[#C9A962]"
              />
              <span class="text-text-medium">Recordarme</span>
            </label>
            <a href="#" class="text-[#C9A962] hover:underline">¿Olvidaste tu contraseña?</a>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-md transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            <span>{{ loading ? 'Ingresando...' : 'Ingresar' }}</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6 flex items-center gap-4">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-text-light text-sm">o</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Register CTA -->
        <div class="text-center">
          <p class="text-text-medium text-sm mb-3">¿No tienes cuenta de mayorista?</p>
          <router-link 
            to="/registro"
            class="inline-block w-full py-3 border border-[#C9A962] text-[#C9A962] font-medium rounded-md hover:bg-[#C9A962]/10 transition-all text-center"
          >
            Solicitar acceso
          </router-link>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-6 text-center">
        <p class="text-white/40 text-xs">
          ¿Eres cliente retail? 
          <a :href="retailUrl" class="text-[#C9A962] hover:underline">
            Visita nuestra tienda
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getCrossContextUrl, APP_CONTEXT } from '../../utils/subdomain'

export default {
  name: 'B2BLogin',
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    const form = ref({
      email: '',
      password: '',
      remember: false
    })
    const loading = ref(false)
    const error = ref('')

    const retailUrl = computed(() => getCrossContextUrl(APP_CONTEXT.B2C))

    async function handleLogin() {
      loading.value = true
      error.value = ''

      try {
        // TODO: Implementar llamada real a API B2B
        const response = await fetch('/api/v1/b2b/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: form.value.email,
            password: form.value.password
          })
        })

        if (!response.ok) {
          const data = await response.json()
          throw new Error(data.detail || 'Credenciales inválidas')
        }

        const data = await response.json()

        // Guardar tokens B2B (separados de B2C)
        localStorage.setItem('b2b_access_token', data.access_token)
        localStorage.setItem('b2b_refresh_token', data.refresh_token)
        localStorage.setItem('b2b_user', JSON.stringify(data.user))

        // Redirigir al dashboard o a la ruta original
        const redirect = route.query.redirect || '/portal'
        router.push(redirect)

      } catch (err) {
        console.error('Error de login B2B:', err)
        error.value = err.message || 'Error al iniciar sesión. Verifica tus credenciales.'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      error,
      retailUrl,
      handleLogin
    }
  }
}
</script>
