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
            
            <!-- Google Sign-In -->
            <div 
              id="google-signin-button" 
              class="flex justify-center w-full"
            ></div>

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

            <p v-if="error && !showEmailForm" class="text-center text-sm text-red-500">{{ error }}</p>

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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../services/api'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
    
    const form = reactive({
      nombre: '',
      email: '',
      password: ''
    })
    
    const showEmailForm = ref(false)
    const isRegistering = ref(false)
    const loading = ref(false)
    const error = ref(null)

    const loadGoogleScript = () => new Promise((resolve, reject) => {
      if (window.google?.accounts?.id) {
        resolve(true)
        return
      }
      const script = document.createElement('script')
      script.src = 'https://accounts.google.com/gsi/client'
      script.async = true
      script.defer = true
      script.onload = () => resolve(true)
      script.onerror = () => reject(new Error('No se pudo cargar Google Sign-In'))
      document.head.appendChild(script)
    })

    onMounted(() => {
      handleGoogleLogin().catch(() => {
        console.log('Google Sign-In no disponible')
      })
    })

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

    const handleGoogleLogin = async () => {
      error.value = null
      loading.value = true
      try {
        await loadGoogleScript()

        if (!googleClientId) {
          throw new Error('Configura VITE_GOOGLE_CLIENT_ID en el frontend')
        }

        const googleAccounts = window.google?.accounts?.id
        if (!googleAccounts) {
          throw new Error('No se pudo inicializar Google Sign-In')
        }

        await new Promise((resolve, reject) => {
          googleAccounts.initialize({
            client_id: googleClientId,
            callback: async (response) => {
              if (!response.credential) {
                reject(new Error('No se recibió credencial de Google'))
                return
              }
              try {
                const { data } = await apiClient.post('/auth/login/google', { id_token: response.credential })
                const { access, refresh, user } = data

                localStorage.setItem('access_token', access)
                localStorage.setItem('refresh_token', refresh)
                localStorage.setItem('user', JSON.stringify(user))

                window.dispatchEvent(new CustomEvent('user-logged-in', { detail: user }))
                closeModal()
                resolve(true)
              } catch (err) {
                reject(err)
              }
            },
          })

          // Renderizar botón de Google en lugar de prompt automático
          const buttonDiv = document.getElementById('google-signin-button')
          if (!buttonDiv) {
            reject(new Error('No se encontró el contenedor del botón de Google'))
            return
          }

          googleAccounts.renderButton(buttonDiv, {
            theme: 'outline',
            size: 'large',
            width: buttonDiv.offsetWidth || 300,
            text: 'signin_with',
            locale: 'es'
          })

          // Resolver inmediatamente después de renderizar el botón
          resolve(true)
        })
      } catch (err) {
        console.error('Error de login con Google:', err)
        if (err.response?.data?.error) {
          error.value = err.response.data.error
        } else {
          error.value = err.message || 'No se pudo iniciar sesión con Google'
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

    // Comentado temporalmente - Google Sign-In deshabilitado
    /*
    onMounted(() => {
      handleGoogleLogin()
    })
    */

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
