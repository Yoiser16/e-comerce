<template>
  <div class="min-h-screen flex flex-col lg:flex-row">
    <!-- =========================================================================
         LADO IZQUIERDO - Hero Image con Branding
         En móvil: aparece arriba como banner compacto
         En desktop: mitad izquierda de la pantalla
    ========================================================================== -->
    <div class="relative lg:w-1/2 h-48 sm:h-64 lg:h-screen overflow-hidden">
      <!-- Gradient de fondo (siempre presente como fallback) -->
      <div class="absolute inset-0 bg-gradient-to-br from-[#1A1A1A] via-[#2D2D2D] to-[#1A1A1A]"></div>
      
      <!-- Patrón decorativo -->
      <div class="absolute inset-0 opacity-5">
        <div class="absolute inset-0" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23C9A962\' fill-opacity=\'0.4\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>
      
      <!-- Overlay oscuro -->
      <div class="absolute inset-0 bg-black/40"></div>
      
      <!-- Contenido sobre la imagen -->
      <div class="relative z-10 h-full flex flex-col justify-between p-6 sm:p-8 lg:p-12">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 lg:w-12 lg:h-12 rounded-full bg-white/10 p-2 flex items-center justify-center">
            <img 
              src="/logo-kharis.png" 
              alt="Kharis" 
              class="w-full h-full object-contain"
            />
          </div>
          <div>
            <span class="text-[#C9A962] font-luxury text-lg lg:text-xl tracking-wider">KHARIS</span>
            <span class="text-white/60 text-xs lg:text-sm block -mt-1">PRO</span>
          </div>
        </div>
        
        <!-- Texto inspirador - Solo visible en desktop -->
        <div class="hidden lg:block max-w-md">
          <h1 class="text-white text-3xl xl:text-4xl font-luxury leading-tight mb-4">
            Impulsa tu negocio con nosotros
          </h1>
          <p class="text-white/70 text-base xl:text-lg leading-relaxed">
            Accede a precios exclusivos, inventario en tiempo real y herramientas 
            diseñadas para hacer crecer tu distribución.
          </p>
          
          <!-- Stats -->
          <div class="flex gap-8 mt-8 pt-8 border-t border-white/10">
            <div>
              <p class="text-[#C9A962] text-2xl font-bold">+500</p>
              <p class="text-white/50 text-sm">Distribuidores activos</p>
            </div>
            <div>
              <p class="text-[#C9A962] text-2xl font-bold">24/7</p>
              <p class="text-white/50 text-sm">Soporte dedicado</p>
            </div>
            <div>
              <p class="text-[#C9A962] text-2xl font-bold">48h</p>
              <p class="text-white/50 text-sm">Envío garantizado</p>
            </div>
          </div>
        </div>

        <!-- Badge de seguridad -->
        <div class="hidden lg:flex items-center gap-2 text-white/40 text-xs">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <span>Conexión segura · Datos encriptados</span>
        </div>
      </div>
    </div>

    <!-- =========================================================================
         LADO DERECHO - Formulario de Login
    ========================================================================== -->
    <div class="flex-1 lg:w-1/2 flex items-center justify-center bg-[#FAFAFA] p-6 sm:p-8 lg:p-12">
      <div class="w-full max-w-md">
        <!-- Header del formulario -->
        <div class="text-center lg:text-left mb-8">
          <h2 class="text-2xl lg:text-3xl font-luxury text-text-dark mb-2">
            Bienvenido de nuevo
          </h2>
          <p class="text-text-light">
            Ingresa tus credenciales para acceder al portal
          </p>
        </div>

        <!-- ===== Mensajes de Estado ===== -->
        
        <!-- Error -->
        <transition name="fade">
          <div 
            v-if="error" 
            class="mb-6 p-4 rounded-lg flex items-start gap-3"
            :class="errorType === 'warning' 
              ? 'bg-amber-50 border border-amber-200' 
              : 'bg-red-50 border border-red-200'"
          >
            <div 
              class="shrink-0 w-5 h-5 rounded-full flex items-center justify-center mt-0.5"
              :class="errorType === 'warning' ? 'bg-amber-100' : 'bg-red-100'"
            >
              <svg 
                v-if="errorType === 'warning'"
                class="w-3 h-3 text-amber-600" fill="currentColor" viewBox="0 0 20 20"
              >
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg 
                v-else
                class="w-3 h-3 text-red-600" fill="currentColor" viewBox="0 0 20 20"
              >
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div>
              <p 
                class="text-sm font-medium"
                :class="errorType === 'warning' ? 'text-amber-800' : 'text-red-800'"
              >
                {{ errorTitle }}
              </p>
              <p 
                class="text-sm mt-0.5"
                :class="errorType === 'warning' ? 'text-amber-700' : 'text-red-600'"
              >
                {{ error }}
              </p>
            </div>
          </div>
        </transition>

        <!-- ===== Formulario ===== -->
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-text-dark mb-1.5">
              Correo electrónico
            </label>
            <div class="relative">
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                autocomplete="email"
                placeholder="tu@empresa.com"
                :disabled="loading"
                class="w-full px-4 py-3.5 pl-11 bg-white border border-gray-200 rounded-lg 
                       focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962] 
                       transition-all outline-none disabled:opacity-50 disabled:cursor-not-allowed"
                :class="{ 'border-red-300': fieldErrors.email }"
              />
              <svg 
                class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" 
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <p v-if="fieldErrors.email" class="mt-1 text-sm text-red-500">
              {{ fieldErrors.email }}
            </p>
          </div>

          <!-- Password -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label for="password" class="block text-sm font-medium text-text-dark">
                Contraseña
              </label>
              <button 
                type="button"
                @click="showForgotPassword = true"
                class="text-sm text-[#C9A962] hover:text-[#B8944F] transition-colors"
              >
                ¿Olvidaste tu contraseña?
              </button>
            </div>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                placeholder="••••••••"
                :disabled="loading"
                class="w-full px-4 py-3.5 pl-11 pr-12 bg-white border border-gray-200 rounded-lg 
                       focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962] 
                       transition-all outline-none disabled:opacity-50 disabled:cursor-not-allowed"
                :class="{ 'border-red-300': fieldErrors.password }"
              />
              <svg 
                class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" 
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <!-- Toggle password visibility -->
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="fieldErrors.password" class="mt-1 text-sm text-red-500">
              {{ fieldErrors.password }}
            </p>
          </div>

          <!-- Remember me -->
          <div class="flex items-center">
            <input 
              id="remember"
              v-model="form.remember" 
              type="checkbox" 
              class="w-4 h-4 text-[#C9A962] bg-white border-gray-300 rounded 
                     focus:ring-[#C9A962] focus:ring-2 cursor-pointer"
            />
            <label for="remember" class="ml-2 text-sm text-text-medium cursor-pointer">
              Mantener sesión iniciada
            </label>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="w-full py-4 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-lg
                   transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                   flex items-center justify-center gap-2 group"
          >
            <svg 
              v-if="loading" 
              class="w-5 h-5 animate-spin" 
              fill="none" viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ loading ? 'Verificando...' : 'Ingresar al Portal' }}</span>
            <svg 
              v-if="!loading"
              class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" 
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </form>

        <!-- ===== Divider ===== -->
        <div class="my-8 flex items-center gap-4">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-text-light text-sm">¿Nuevo distribuidor?</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- ===== CTA Registro ===== -->
        <div class="text-center">
          <p class="text-text-medium text-sm mb-4">
            Únete a nuestra red de distribuidores y accede a beneficios exclusivos
          </p>
          <router-link 
            to="/registro"
            class="inline-flex items-center justify-center w-full py-3.5 px-6
                   border-2 border-[#C9A962] text-[#C9A962] font-medium rounded-lg
                   hover:bg-[#C9A962] hover:text-white transition-all duration-200 group"
          >
            <span>Solicita tu cuenta aquí</span>
            <svg 
              class="w-4 h-4 ml-2 transform group-hover:translate-x-1 transition-transform" 
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </router-link>
        </div>

        <!-- ===== Footer Links ===== -->
        <div class="mt-8 pt-6 border-t border-gray-100 text-center">
          <p class="text-text-light text-xs">
            ¿Eres cliente retail? 
            <a :href="retailUrl" class="text-[#C9A962] hover:underline">
              Visita nuestra tienda
            </a>
          </p>
          <p class="text-text-light text-xs mt-2">
            <a href="#" class="hover:text-text-medium">Términos</a>
            <span class="mx-2">·</span>
            <a href="#" class="hover:text-text-medium">Privacidad</a>
            <span class="mx-2">·</span>
            <a href="#" class="hover:text-text-medium">Contacto</a>
          </p>
        </div>
      </div>
    </div>

    <!-- =========================================================================
         MODAL DE ESTADO (Cuenta pendiente, rechazada, suspendida, etc.)
    ========================================================================== -->
    <Teleport to="body">
      <Transition name="modal">
        <div 
          v-if="statusModal.show" 
          class="fixed inset-0 z-50 flex items-center justify-center p-4"
        >
          <!-- Backdrop -->
          <div 
            class="absolute inset-0 bg-black/50"
            @click="closeStatusModal"
          ></div>
          
          <!-- Modal Content -->
          <div class="relative bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 text-center transform transition-all">
            <!-- Icono según estado -->
            <div 
              class="w-20 h-20 mx-auto mb-6 rounded-full flex items-center justify-center"
              :class="{
                'bg-amber-100': statusModal.status === 'pending' || statusModal.status === 'reviewing',
                'bg-red-100': statusModal.status === 'rejected' || statusModal.status === 'suspended'
              }"
            >
              <!-- Clock (Pendiente) -->
              <svg v-if="statusModal.icon === 'clock'" class="w-10 h-10 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <!-- Search (En revisión) -->
              <svg v-else-if="statusModal.icon === 'search'" class="w-10 h-10 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <!-- X (Rechazado) -->
              <svg v-else-if="statusModal.icon === 'x'" class="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <!-- Pause (Suspendido) -->
              <svg v-else-if="statusModal.icon === 'pause'" class="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            
            <!-- Título -->
            <h3 class="text-xl font-luxury text-text-dark mb-3">
              {{ statusModal.title }}
            </h3>
            
            <!-- Mensaje -->
            <p class="text-text-medium mb-8 leading-relaxed">
              {{ statusModal.message }}
            </p>
            
            <!-- Botones -->
            <div class="flex flex-col sm:flex-row gap-3 justify-center">
              <!-- Botón de acción (contactar soporte) -->
              <a 
                v-if="statusModal.showSupport"
                href="https://wa.me/573001234567?text=Hola,%20necesito%20ayuda%20con%20mi%20cuenta%20mayorista"
                target="_blank"
                class="px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-medium rounded-lg transition-colors inline-flex items-center justify-center gap-2"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                </svg>
                Contactar soporte
              </a>
              
              <!-- Botón cerrar -->
              <button 
                @click="closeStatusModal"
                class="px-6 py-3 border border-gray-300 text-text-dark font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                Entendido
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
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
    
    // =========================================================================
    // STATE
    // =========================================================================
    const form = ref({
      email: '',
      password: '',
      remember: false
    })
    
    const loading = ref(false)
    const error = ref('')
    const errorType = ref('error') // 'error' | 'warning'
    const errorTitle = ref('Error de autenticación')
    const showPassword = ref(false)
    const showForgotPassword = ref(false)
    const imageError = ref(false)
    
    const fieldErrors = ref({
      email: '',
      password: ''
    })
    
    // Modal de estado de cuenta
    const statusModal = ref({
      show: false,
      status: '', // 'pending' | 'reviewing' | 'rejected' | 'suspended'
      title: '',
      message: '',
      icon: 'clock',
      showSupport: false
    })

    // =========================================================================
    // COMPUTED
    // =========================================================================
    const retailUrl = computed(() => getCrossContextUrl(APP_CONTEXT.B2C))
    
    const isFormValid = computed(() => {
      return form.value.email.trim() !== '' && form.value.password.trim() !== ''
    })

    // =========================================================================
    // METHODS
    // =========================================================================
    
    function handleImageError() {
      imageError.value = true
    }
    
    function clearErrors() {
      error.value = ''
      errorType.value = 'error'
      fieldErrors.value = { email: '', password: '' }
    }
    
    function closeStatusModal() {
      statusModal.value.show = false
    }
    
    function validateForm() {
      clearErrors()
      let isValid = true
      
      // Validar email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(form.value.email)) {
        fieldErrors.value.email = 'Ingresa un correo electrónico válido'
        isValid = false
      }
      
      // Validar password
      if (form.value.password.length < 6) {
        fieldErrors.value.password = 'La contraseña debe tener al menos 6 caracteres'
        isValid = false
      }
      
      return isValid
    }

    async function handleLogin() {
      if (!validateForm()) return
      
      loading.value = true
      clearErrors()

      try {
        const API_BASE = import.meta.env.VITE_API_URL?.replace('/api/v1', '') || 'http://localhost:8000'
        
        // =====================================================================
        // Llamada real a la API de login
        // =====================================================================
        const response = await fetch(`${API_BASE}/api/v1/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: form.value.email,
            password: form.value.password
          })
        })

        const data = await response.json()

        if (!response.ok) {
          // Manejar diferentes tipos de errores
          if (response.status === 401) {
            error.value = 'El correo o la contraseña son incorrectos. Verifica tus datos.'
            errorTitle.value = 'Credenciales inválidas'
            errorType.value = 'error'
          } else if (response.status === 403) {
            // Cuenta en revisión, rechazada o suspendida - mostrar modal elegante
            const detail = data.detail || ''
            
            // Determinar el estado según el mensaje del backend
            if (detail.includes('pendiente')) {
              statusModal.value = {
                show: true,
                status: 'pending',
                title: 'Solicitud en proceso',
                message: 'Tu solicitud de cuenta mayorista está pendiente de aprobación. Te notificaremos por correo electrónico cuando sea revisada.',
                icon: 'clock',
                showSupport: false
              }
            } else if (detail.includes('siendo revisada') || detail.includes('revisión')) {
              statusModal.value = {
                show: true,
                status: 'reviewing',
                title: 'En revisión',
                message: 'Tu solicitud está siendo revisada por nuestro equipo. Te contactaremos pronto con una respuesta.',
                icon: 'search',
                showSupport: false
              }
            } else if (detail.includes('rechazada') || detail.includes('rechazado')) {
              statusModal.value = {
                show: true,
                status: 'rejected',
                title: 'Solicitud rechazada',
                message: 'Lamentamos informarte que tu solicitud de cuenta mayorista no fue aprobada. Puedes contactar a soporte para más información.',
                icon: 'x',
                showSupport: true
              }
            } else if (detail.includes('suspendida') || detail.includes('suspendido')) {
              statusModal.value = {
                show: true,
                status: 'suspended',
                title: 'Cuenta suspendida',
                message: 'Tu cuenta de mayorista ha sido suspendida temporalmente. Contacta a soporte para resolver esta situación.',
                icon: 'pause',
                showSupport: true
              }
            } else {
              // Estado genérico
              statusModal.value = {
                show: true,
                status: 'pending',
                title: 'Cuenta no activa',
                message: detail || 'Tu cuenta no está activa actualmente. Contacta a soporte para más información.',
                icon: 'clock',
                showSupport: true
              }
            }
            return
          } else {
            error.value = data.detail || 'Error al iniciar sesión. Intenta nuevamente.'
            errorTitle.value = 'Error de autenticación'
            errorType.value = 'error'
          }
          return
        }

        // Guardar tokens B2B (separados de B2C)
        localStorage.setItem('b2b_access_token', data.access)
        localStorage.setItem('b2b_refresh_token', data.refresh)
        localStorage.setItem('b2b_user', JSON.stringify(data.user))
        
        // Si eligió "recordarme", guardar preferencia
        if (form.value.remember) {
          localStorage.setItem('b2b_remember', 'true')
        }

        console.log('✅ Login B2B exitoso')
        console.log('Usuario:', data.user)

        // Redirigir al dashboard o a la ruta original
        const redirect = route.query.redirect || '/portal'
        router.push(redirect)

      } catch (err) {
        console.error('Error de login B2B:', err)
        error.value = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.'
        errorTitle.value = 'Error de conexión'
        errorType.value = 'error'
      } finally {
        loading.value = false
      }
    }

    // =========================================================================
    // RETURN
    // =========================================================================
    return {
      form,
      loading,
      error,
      errorType,
      errorTitle,
      fieldErrors,
      showPassword,
      showForgotPassword,
      imageError,
      retailUrl,
      isFormValid,
      statusModal,
      handleLogin,
      handleImageError,
      closeStatusModal
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
}

/* Estilos para el checkbox personalizado */
input[type="checkbox"]:checked {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z'/%3e%3c/svg%3e");
  background-color: #C9A962;
  border-color: #C9A962;
}
</style>
