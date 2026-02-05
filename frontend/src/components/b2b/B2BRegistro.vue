<template>
  <div class="min-h-screen bg-[#1A1A1A] flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-lg">
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
        <p class="text-white/50 text-sm tracking-wide">Solicitud de Cuenta Mayorista</p>
      </div>

      <!-- Registration Card -->
      <div class="bg-white rounded-lg shadow-xl p-6 sm:p-8">
        <h2 class="text-text-dark text-xl font-medium mb-2 text-center">
          Únete a nuestra red de distribuidores
        </h2>
        <p class="text-text-light text-sm text-center mb-6">
          Completa el formulario y nuestro equipo revisará tu solicitud en 24-48 horas.
        </p>

        <!-- Success Message -->
        <div 
          v-if="submitted" 
          class="text-center py-8"
        >
          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-green-100 flex items-center justify-center">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-text-dark mb-2">¡Solicitud Enviada!</h3>
          <p class="text-text-light text-sm mb-4">
            Revisaremos tu información y te contactaremos pronto.
          </p>
          <router-link 
            to="/login"
            class="inline-block px-6 py-3 bg-[#1A1A1A] text-white rounded-lg hover:bg-black transition-colors"
          >
            Volver al Login
          </router-link>
        </div>

        <!-- Registration Form -->
        <form v-else @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-text-medium mb-1">Nombre Completo *</label>
              <input
                v-model="form.nombre"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-text-medium mb-1">Correo Electrónico *</label>
              <input
                v-model="form.email"
                type="email"
                required
                class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none"
              />
            </div>
          </div>

          <div class="grid sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-text-medium mb-1">Nombre de Empresa *</label>
              <input
                v-model="form.empresa"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-text-medium mb-1">NIT / RUT *</label>
              <input
                v-model="form.nit"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none"
              />
            </div>
          </div>

          <div class="grid sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-text-medium mb-1">Teléfono *</label>
              <input
                v-model="form.telefono"
                type="tel"
                required
                class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-text-medium mb-1">Ciudad *</label>
              <input
                v-model="form.ciudad"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-text-medium mb-1">Tipo de Negocio *</label>
            <select
              v-model="form.tipoNegocio"
              required
              class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none"
            >
              <option value="">Selecciona una opción</option>
              <option value="tienda">Tienda Física</option>
              <option value="salon">Salón de Belleza</option>
              <option value="ecommerce">E-commerce</option>
              <option value="distribuidor">Distribuidor</option>
              <option value="otro">Otro</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-text-medium mb-1">Mensaje (opcional)</label>
            <textarea
              v-model="form.mensaje"
              rows="3"
              placeholder="Cuéntanos sobre tu negocio..."
              class="w-full px-4 py-3 border border-gray-200 rounded-md focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none resize-none"
            ></textarea>
          </div>

          <div class="flex items-start gap-2">
            <input 
              v-model="form.acepta"
              type="checkbox" 
              required
              class="mt-1 w-4 h-4 text-[#C9A962] border-gray-300 rounded focus:ring-[#C9A962]"
            />
            <label class="text-sm text-text-medium">
              Acepto los <a href="#" class="text-[#C9A962] hover:underline">Términos y Condiciones</a> 
              y la <a href="#" class="text-[#C9A962] hover:underline">Política de Privacidad</a>
            </label>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-md transition-all disabled:opacity-50"
          >
            {{ loading ? 'Enviando...' : 'Enviar Solicitud' }}
          </button>
        </form>

        <!-- Login Link -->
        <div v-if="!submitted" class="mt-6 text-center">
          <p class="text-text-medium text-sm">
            ¿Ya tienes cuenta? 
            <router-link to="/login" class="text-[#C9A962] hover:underline">Inicia sesión</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'B2BRegistro',
  setup() {
    const loading = ref(false)
    const submitted = ref(false)
    const form = ref({
      nombre: '',
      email: '',
      empresa: '',
      nit: '',
      telefono: '',
      ciudad: '',
      tipoNegocio: '',
      mensaje: '',
      acepta: false
    })

    async function handleSubmit() {
      loading.value = true
      
      try {
        // TODO: Implementar llamada real a API
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        console.log('Solicitud B2B enviada:', form.value)
        submitted.value = true
        
      } catch (err) {
        console.error('Error al enviar solicitud:', err)
        alert('Error al enviar la solicitud. Intenta nuevamente.')
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      submitted,
      handleSubmit
    }
  }
}
</script>
