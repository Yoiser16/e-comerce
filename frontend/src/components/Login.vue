<template>
  <!-- ===== MODAL OVERLAY LOGIN ===== -->
  <div class="fixed inset-0 z-[100]">
    
    <!-- Backdrop: Simple overlay sin blur -->
    <div 
      class="absolute inset-0 bg-black/70"
      @click="closeModal"
    ></div>

    <!-- Modal Container -->
    <div class="absolute inset-0 flex items-center justify-center p-4">
      
      <!-- Modal Box -->
      <div 
        class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden animate-modal-enter"
        @click.stop
      >
        
        <!-- Botón Cerrar -->
        <button 
          @click="closeModal"
          class="absolute top-5 right-5 w-10 h-10 flex items-center justify-center rounded-full hover:bg-nude-100 transition-colors z-10"
        >
          <svg class="w-5 h-5 text-text-light" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Contenido del Modal -->
        <div class="p-8 sm:p-10">
          
          <!-- Logo -->
          <div class="flex justify-center mb-8">
            <router-link to="/" class="flex items-center gap-3">
              <img 
                src="/logo.jpeg" 
                alt="Kharis Distribuidora" 
                class="h-14 w-auto object-contain"
              />
            </router-link>
          </div>

          <!-- Título elegante -->
          <h2 class="text-center font-luxury text-2xl text-text-dark mb-2">
            <span v-if="!isRegistering">Bienvenido de <em class="not-italic text-brand-600">nuevo</em></span>
            <span v-else>Crea tu <em class="not-italic text-brand-600">cuenta</em></span>
          </h2>
          <p class="text-center text-sm text-text-light mb-8">
            <span v-if="!isRegistering">¿Cómo quieres iniciar sesión?</span>
            <span v-else>Regístrate para comenzar</span>
          </p>

          <!-- Opciones de Login -->
          <div class="space-y-3">
            
            <!-- Google -->
            <button 
              type="button"
              class="w-full flex items-center justify-center gap-3 py-4 px-6 bg-white border border-nude-300 rounded-xl hover:border-brand-500 hover:shadow-soft transition-all duration-300"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              <span class="text-sm font-medium text-text-dark uppercase tracking-wide">Ingresar con Google</span>
            </button>

            <!-- Email -->
            <button 
              type="button"
              @click="showEmailForm = !showEmailForm"
              class="w-full flex items-center justify-center gap-3 py-4 px-6 bg-white border border-nude-300 rounded-xl hover:border-brand-500 hover:shadow-soft transition-all duration-300"
            >
              <svg class="w-5 h-5 text-text-medium" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
              </svg>
              <span class="text-sm font-medium text-text-dark uppercase tracking-wide">Ingresar con correo</span>
            </button>

          </div>

          <!-- Formulario de Email (expandible) -->
          <transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="opacity-0 -translate-y-2 max-h-0"
            enter-to-class="opacity-100 translate-y-0 max-h-96"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100 translate-y-0 max-h-96"
            leave-to-class="opacity-0 -translate-y-2 max-h-0"
          >
            <form v-if="showEmailForm" @submit.prevent="isRegistering ? handleRegister() : handleLogin()" class="mt-6 space-y-4 overflow-hidden">
              
              <!-- Nombre (solo registro) -->
              <div v-if="isRegistering">
                <input 
                  type="text" 
                  v-model="form.nombre"
                  required
                  placeholder="Tu nombre completo"
                  class="w-full px-4 py-4 bg-nude-50 border border-nude-200 rounded-xl text-text-dark placeholder-text-light focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all"
                >
              </div>

              <!-- Email -->
              <div>
                <input 
                  type="email" 
                  v-model="form.email"
                  required
                  placeholder="Tu correo electrónico"
                  class="w-full px-4 py-4 bg-nude-50 border border-nude-200 rounded-xl text-text-dark placeholder-text-light focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all"
                >
              </div>

              <!-- Password -->
              <div>
                <input 
                  type="password" 
                  v-model="form.password"
                  required
                  :placeholder="isRegistering ? 'Contraseña (mínimo 6 caracteres)' : 'Contraseña'"
                  class="w-full px-4 py-4 bg-nude-50 border border-nude-200 rounded-xl text-text-dark placeholder-text-light focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all"
                >
              </div>

              <!-- Error -->
              <div v-if="error" class="text-red-500 text-sm text-center">
                {{ error }}
              </div>

              <!-- Submit -->
              <button 
                type="submit"
                :disabled="loading"
                class="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-4 px-6 rounded-xl transition-all disabled:opacity-70"
              >
                <span v-if="!loading">{{ isRegistering ? 'Crear Cuenta' : 'Ingresar' }}</span>
                <span v-else class="flex items-center justify-center gap-2">
                  <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isRegistering ? 'Creando cuenta...' : 'Ingresando...' }}
                </span>
              </button>

              <!-- Forgot Password (solo login) -->
              <p v-if="!isRegistering" class="text-center">
                <a href="#" class="text-sm text-text-light hover:text-brand-600 transition-colors">
                  ¿Olvidaste tu contraseña?
                </a>
              </p>

            </form>
          </transition>

          <!-- Divider -->
          <div class="my-8 border-t border-nude-200"></div>

          <!-- Toggle Login/Register -->
          <p class="text-center text-sm text-text-medium">
            <span v-if="!isRegistering">
              ¿No tienes cuenta? 
              <button @click="toggleMode" class="text-brand-600 hover:text-brand-700 font-semibold transition-colors">
                Regístrate
              </button>
            </span>
            <span v-else>
              ¿Ya tienes cuenta? 
              <button @click="toggleMode" class="text-brand-600 hover:text-brand-700 font-semibold transition-colors">
                Inicia sesión
              </button>
            </span>
          </p>

        </div>

      </div>
    </div>

  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../services/api'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    
    const form = reactive({
      nombre: '',
      email: '',
      password: ''
    })
    
    const showEmailForm = ref(false)
    const isRegistering = ref(false)
    const loading = ref(false)
    const error = ref(null)

    const closeModal = () => {
      router.push('/')
    }

    const handleLogin = async () => {
      loading.value = true
      error.value = null
      
      try {
        // Llamar al endpoint de login del backend
        const response = await apiClient.post('/auth/login', {
          email: form.email,
          password: form.password
        })
        
        const { access, refresh, user } = response.data
        
        console.log('Login exitoso:', user)
        
        // Redirigir según el rol del usuario
        if (user.rol === 'ADMIN' || user.rol === 'OPERADOR') {
          // ADMIN: NO guardar sesión en el ecommerce
          // Solo abrir ventana admin con los tokens en la URL (para que admin los capture)
          // El ecommerce queda como visitante anónimo
          const adminUrl = `/admin?token=${access}&refresh=${refresh}`
          window.open(adminUrl, '_blank')
          closeModal()
          // NO emitir evento - el admin no debe verse logueado en la tienda
        } else {
          // CLIENTE: Guardar tokens en localStorage
          localStorage.setItem('access_token', access)
          localStorage.setItem('refresh_token', refresh)
          localStorage.setItem('user', JSON.stringify(user))
          
          // Emitir evento ANTES de cerrar el modal
          window.dispatchEvent(new CustomEvent('user-logged-in', { detail: user }))
          
          // Pequeño delay para asegurar que el estado se actualice
          setTimeout(() => {
            closeModal()
          }, 100)
        }
        
      } catch (err) {
        console.error('Error de login:', err)
        
        if (err.response?.status === 401) {
          error.value = 'Credenciales incorrectas. Verifica tu email y contraseña.'
        } else if (err.response?.status === 429) {
          error.value = 'Demasiados intentos. Por favor espera un momento.'
        } else if (err.response?.data?.detail) {
          error.value = err.response.data.detail
        } else {
          error.value = 'Error de conexión. Intenta de nuevo.'
        }
      } finally {
        loading.value = false
      }
    }
    
    const handleRegister = async () => {
      error.value = ''
      loading.value = true

      try {
        const response = await apiClient.post('/auth/register', {
          nombre: form.nombre,
          email: form.email,
          password: form.password
        })
        
        const { access, refresh, user } = response.data
        
        console.log('Registro exitoso:', user)
        
        // Guardar tokens en localStorage
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user', JSON.stringify(user))
        
        // Emitir evento ANTES de cerrar el modal
        window.dispatchEvent(new CustomEvent('user-logged-in', { detail: user }))
        
        // Pequeño delay para asegurar que el estado se actualice
        setTimeout(() => {
          closeModal()
        }, 100)
        
      } catch (err) {
        console.error('Error de registro:', err)
        
        if (err.response?.status === 400) {
          error.value = err.response.data.error || 'Verifica los datos ingresados'
        } else if (err.response?.data?.error) {
          error.value = err.response.data.error
        } else {
          error.value = 'Error al crear la cuenta. Intenta de nuevo.'
        }
      } finally {
        loading.value = false
      }
    }
    
    const toggleMode = () => {
      isRegistering.value = !isRegistering.value
      error.value = ''
      form.nombre = ''
      form.email = ''
      form.password = ''
      if (!showEmailForm.value) {
        showEmailForm.value = true
      }
    }

    return {
      form,
      showEmailForm,
      isRegistering,
      loading,
      error,
      closeModal,
      handleLogin,
      handleRegister,
      toggleMode
    }
  }
}
</script>

<style scoped>
/* Modal entrance animation */
@keyframes modalEnter {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-modal-enter {
  animation: modalEnter 0.3s ease-out forwards;
}
</style>
