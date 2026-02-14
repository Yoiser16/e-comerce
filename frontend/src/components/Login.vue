<template>
  <!-- ===== LOGIN OVERLAY ===== -->
  <!-- Móvil: Full-Screen | Desktop: Modal centrado -->
  <div class="login-overlay fixed inset-0 z-[9999]">
    
    <!-- Backdrop: Solo visible en desktop -->
    <div 
      class="absolute inset-0 bg-black/60 hidden md:block"
      @click="closeModal"
    ></div>

    <!-- Contenedor principal -->
    <div class="absolute inset-0 flex items-start md:items-center md:justify-center md:p-4">
      
      <!-- Login Box: Full-screen en móvil, modal en desktop -->
      <div 
        class="login-box relative bg-white w-full h-full md:h-auto md:max-h-[90vh] md:w-full md:max-w-md md:rounded-2xl md:shadow-2xl overflow-y-auto"
        @click.stop
      >
        
        <!-- Header: Botón cerrar -->
        <div class="sticky top-0 z-10 bg-white/95 flex items-center justify-between px-5 py-4 md:absolute md:top-0 md:right-0 md:left-auto md:bg-transparent md:p-5">
          <button 
            @click="closeModal"
            class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-nude-100 active:bg-nude-200 transition-colors"
            aria-label="Cerrar"
          >
            <!-- Flecha atrás en móvil -->
            <svg class="w-5 h-5 text-text-dark md:hidden" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
            <!-- X en desktop -->
            <svg class="w-5 h-5 text-text-light hidden md:block" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <!-- Spacer para mantener el botón a la izquierda en móvil -->
          <div class="md:hidden"></div>
        </div>

        <!-- Contenido del Login -->
        <div class="px-6 pb-10 pt-4 md:p-8 md:pt-10 lg:p-10">
          
          <!-- Logo -->
          <div class="flex justify-center mb-10 md:mb-8">
            <router-link to="/" class="flex items-center gap-3">
              <img 
                src="/logo-kharis.png" 
                alt="Kharis Distribuidora" 
                class="h-24 md:h-20 w-auto object-contain"
              />
            </router-link>
          </div>

          <!-- Título elegante y minimalista -->
          <h2 class="text-center font-luxury text-[26px] md:text-3xl text-text-dark mb-3 leading-tight">
            ¿Cómo quieres <em class="not-italic text-brand-600">iniciar sesión</em>?
          </h2>
          <p class="text-center text-sm text-text-light mb-10 md:mb-8">
            Elige tu método preferido para continuar
          </p>

          <!-- Opciones de Login -->
          <div class="space-y-3">
            
            <!-- Google Sign-In -->
            <div 
              id="google-signin-button" 
              class="flex justify-center w-full"
            ></div>

            <!-- Código de Acceso (Email) -->
            <button 
              type="button"
              @click="showEmailForm = !showEmailForm"
              class="w-full flex items-center justify-center gap-3 py-4 px-6 bg-white border-2 border-text-dark/10 rounded-xl hover:border-brand-500 hover:bg-nude-50/30 active:scale-[0.98] transition-all duration-200 group"
            >
              <svg class="w-5 h-5 text-text-medium group-hover:text-brand-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
              </svg>
              <span class="text-sm font-medium text-text-dark uppercase tracking-[0.08em]">Ingresar con código de acceso</span>
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
              <div class="relative">
                <input 
                  :type="showPassword ? 'text' : 'password'" 
                  v-model="form.password"
                  required
                  :placeholder="isRegistering ? 'Contraseña (mínimo 6 caracteres)' : 'Contraseña'"
                  class="w-full px-4 py-4 pr-12 bg-nude-50 border border-nude-200 rounded-xl text-text-dark placeholder-text-light focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all"
                >
                <button 
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-text-light hover:text-text-dark transition-colors"
                  tabindex="-1"
                >
                  <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                </button>
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
                <button type="button" @click="showForgotPassword" class="text-sm text-text-light hover:text-brand-600 transition-colors">
                  ¿Olvidaste tu contraseña?
                </button>
              </p>

            </form>
          </transition>

          <!-- ===== Flujo Recuperar Contraseña ===== -->
          <transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="opacity-0 -translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-2"
          >
            <div v-if="forgotStep > 0" class="mt-6 space-y-4">
              
              <!-- Paso 1: Ingresar email -->
              <form v-if="forgotStep === 1" @submit.prevent="handleForgotPassword" class="space-y-4">
                <p class="text-sm text-text-medium text-center">
                  Ingresa tu email y te enviaremos un código de recuperación.
                </p>
                <input 
                  type="email" 
                  v-model="forgotForm.email"
                  required
                  placeholder="Tu correo electrónico"
                  class="w-full px-4 py-4 bg-nude-50 border border-nude-200 rounded-xl text-text-dark placeholder-text-light focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all"
                >
                <div v-if="forgotError" class="text-red-500 text-sm text-center">{{ forgotError }}</div>
                <div v-if="forgotSuccess" class="text-green-600 text-sm text-center">{{ forgotSuccess }}</div>
                <button 
                  type="submit"
                  :disabled="forgotLoading"
                  class="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-4 px-6 rounded-xl transition-all disabled:opacity-70"
                >
                  <span v-if="!forgotLoading">Enviar código</span>
                  <span v-else class="flex items-center justify-center gap-2">
                    <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Enviando...
                  </span>
                </button>
                <p class="text-center">
                  <button type="button" @click="cancelForgotPassword" class="text-sm text-text-light hover:text-brand-600 transition-colors">
                    ← Volver al inicio de sesión
                  </button>
                </p>
              </form>

              <!-- Paso 2: Ingresar código + nueva contraseña -->
              <form v-if="forgotStep === 2" @submit.prevent="handleResetPassword" class="space-y-4">
                <p class="text-sm text-text-medium text-center">
                  Ingresa el código que enviamos a <strong>{{ forgotForm.email }}</strong>
                </p>
                <input 
                  type="text" 
                  v-model="forgotForm.codigo"
                  required
                  maxlength="6"
                  placeholder="Código de 6 dígitos"
                  class="w-full px-4 py-4 bg-nude-50 border border-nude-200 rounded-xl text-text-dark placeholder-text-light focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all text-center text-2xl tracking-[0.5em] font-mono"
                >
                <div class="relative">
                  <input 
                    :type="showNewPassword ? 'text' : 'password'" 
                    v-model="forgotForm.newPassword"
                    required
                    placeholder="Nueva contraseña (mínimo 6 caracteres)"
                    class="w-full px-4 py-4 pr-12 bg-nude-50 border border-nude-200 rounded-xl text-text-dark placeholder-text-light focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all"
                  >
                  <button 
                    type="button"
                    @click="showNewPassword = !showNewPassword"
                    class="absolute right-4 top-1/2 -translate-y-1/2 text-text-light hover:text-text-dark transition-colors"
                    tabindex="-1"
                  >
                    <svg v-if="!showNewPassword" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                  </button>
                </div>
                <div v-if="forgotError" class="text-red-500 text-sm text-center">{{ forgotError }}</div>
                <div v-if="forgotSuccess" class="text-green-600 text-sm text-center">{{ forgotSuccess }}</div>
                <button 
                  type="submit"
                  :disabled="forgotLoading"
                  class="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-4 px-6 rounded-xl transition-all disabled:opacity-70"
                >
                  <span v-if="!forgotLoading">Restablecer contraseña</span>
                  <span v-else class="flex items-center justify-center gap-2">
                    <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Restableciendo...
                  </span>
                </button>
                <p class="text-center">
                  <button type="button" @click="forgotStep = 1" class="text-sm text-text-light hover:text-brand-600 transition-colors">
                    ← Reenviar código
                  </button>
                </p>
              </form>

            </div>
          </transition>

          <!-- Divider -->
          <div class="my-10 md:my-8 border-t border-nude-200"></div>

          <!-- Toggle Login/Register -->
          <p v-if="forgotStep === 0" class="text-center text-sm text-text-medium">
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
import { ref, reactive, onMounted, onUnmounted } from 'vue'
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
    const showPassword = ref(false)
    const loading = ref(false)
    const error = ref(null)

    // Forgot password state
    const forgotStep = ref(0) // 0=oculto, 1=email, 2=código+nueva contraseña
    const forgotLoading = ref(false)
    const forgotError = ref('')
    const forgotSuccess = ref('')
    const showNewPassword = ref(false)
    const forgotForm = reactive({
      email: '',
      codigo: '',
      newPassword: ''
    })

    // ===== Bloquear scroll del body cuando el login está abierto =====
    const lockBodyScroll = () => {
      document.body.style.overflow = 'hidden'
      document.body.style.position = 'fixed'
      document.body.style.width = '100%'
      document.body.style.top = `-${window.scrollY}px`
    }
    const unlockBodyScroll = () => {
      const scrollY = document.body.style.top
      document.body.style.overflow = ''
      document.body.style.position = ''
      document.body.style.width = ''
      document.body.style.top = ''
      window.scrollTo(0, parseInt(scrollY || '0') * -1)
    }

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
      // Bloquear scroll del body
      lockBodyScroll()
      
      handleGoogleLogin().catch(() => {
        console.log('Google Sign-In no disponible')
      })
    })

    // Desbloquear scroll al desmontar
    onUnmounted(() => {
      unlockBodyScroll()
    })

    const closeModal = () => {
      // Desbloquear scroll antes de navegar
      unlockBodyScroll()
      // Usar replace para evitar agregar a historial y reducir delay
      const currentPath = router.currentRoute.value.path
      if (currentPath === '/login') {
        router.replace('/')
      }
      // Si ya estamos en otra ruta, no hacer nada
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
          error.value = 'Email o contraseña incorrectos. Intenta de nuevo.'
        } else if (err.response?.status === 429) {
          error.value = 'Demasiados intentos. Por favor espera un momento.'
        } else if (err.response?.status === 400) {
          error.value = err.response.data?.detail || 'Verifica los datos que ingresaste.'
        } else if (err.response?.status === 500) {
          error.value = 'Error del servidor. Por favor intenta más tarde.'
        } else if (err.response?.data?.detail) {
          error.value = err.response.data.detail
        } else {
          error.value = 'No pudimos conectar. Verifica tu conexión de internet.'
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
          error.value = err.response.data?.detail || err.response.data?.error || 'Verifica los datos que ingresaste.'
        } else if (err.response?.status === 409) {
          error.value = 'Este email ya está registrado. Intenta con otro.'
        } else if (err.response?.status === 500) {
          error.value = 'Error del servidor. Por favor intenta más tarde.'
        } else if (err.response?.data?.error) {
          error.value = err.response.data.error
        } else {
          error.value = 'No pudimos crear tu cuenta. Intenta de nuevo.'
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
      forgotStep.value = 0
      if (!showEmailForm.value) {
        showEmailForm.value = true
      }
    }

    const showForgotPassword = () => {
      forgotStep.value = 1
      forgotError.value = ''
      forgotSuccess.value = ''
      forgotForm.email = form.email || ''
      forgotForm.codigo = ''
      forgotForm.newPassword = ''
      showEmailForm.value = false
      error.value = ''
    }

    const cancelForgotPassword = () => {
      forgotStep.value = 0
      forgotError.value = ''
      forgotSuccess.value = ''
      showEmailForm.value = true
    }

    const handleForgotPassword = async () => {
      forgotError.value = ''
      forgotSuccess.value = ''
      forgotLoading.value = true

      try {
        const res = await apiClient.post('/auth/forgot-password', {
          email: forgotForm.email
        })
        if (res.data.sent) {
          forgotSuccess.value = 'Hemos enviado un código de recuperación a tu correo.'
          // Avanzar al paso 2 después de un breve delay
          setTimeout(() => {
            forgotStep.value = 2
            forgotSuccess.value = ''
          }, 1500)
        } else {
          forgotError.value = 'No encontramos una cuenta con ese correo. ¿Seguro que te registraste con este email?'
        }
      } catch (err) {
        console.error('Error en forgot-password:', err)
        if (err.response?.data?.detail) {
          forgotError.value = err.response.data.detail
        } else {
          forgotError.value = 'Error al enviar el código. Intenta de nuevo.'
        }
      } finally {
        forgotLoading.value = false
      }
    }

    const handleResetPassword = async () => {
      forgotError.value = ''
      forgotSuccess.value = ''

      if (forgotForm.newPassword.length < 6) {
        forgotError.value = 'La contraseña debe tener al menos 6 caracteres.'
        return
      }
      if (forgotForm.codigo.length !== 6) {
        forgotError.value = 'Ingresa el código de 6 dígitos.'
        return
      }

      forgotLoading.value = true

      try {
        await apiClient.post('/auth/reset-password', {
          email: forgotForm.email,
          codigo: forgotForm.codigo,
          new_password: forgotForm.newPassword
        })
        forgotSuccess.value = '¡Contraseña actualizada! Ahora puedes iniciar sesión.'
        // Volver al login después de un momento
        setTimeout(() => {
          forgotStep.value = 0
          forgotSuccess.value = ''
          showEmailForm.value = true
          form.email = forgotForm.email
          form.password = ''
        }, 2000)
      } catch (err) {
        console.error('Error en reset-password:', err)
        if (err.response?.data?.detail) {
          forgotError.value = err.response.data.detail
        } else {
          forgotError.value = 'Error al restablecer contraseña. Verifica el código.'
        }
      } finally {
        forgotLoading.value = false
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
      showPassword,
      loading,
      error,
      closeModal,
      handleLogin,
      handleRegister,
      toggleMode,
      // Forgot password
      forgotStep,
      forgotLoading,
      forgotError,
      forgotSuccess,
      forgotForm,
      showNewPassword,
      showForgotPassword,
      cancelForgotPassword,
      handleForgotPassword,
      handleResetPassword
    }
  }
}
</script>

<style scoped>
/* ===== Animaciones de entrada ===== */

/* Móvil: Slide-up desde abajo (app-like) */
.login-box {
  animation: loginSlideUp 0.35s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

@keyframes loginSlideUp {
  from {
    opacity: 0;
    transform: translateY(100%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Desktop: Scale + fade (modal clásico) */
@media (min-width: 768px) {
  .login-box {
    animation: loginModalEnter 0.3s ease-out forwards;
  }
  
  @keyframes loginModalEnter {
    from {
      opacity: 0;
      transform: scale(0.95) translateY(10px);
    }
    to {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }
}

/* ===== Scrollbar elegante para el contenido ===== */
.login-box::-webkit-scrollbar {
  width: 3px;
}
.login-box::-webkit-scrollbar-track {
  background: transparent;
}
.login-box::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

/* ===== Safe area para dispositivos con notch ===== */
@supports (padding-top: env(safe-area-inset-top)) {
  .login-box {
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
  }
}
</style>
