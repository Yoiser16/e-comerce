<template>
  <div class="max-w-2xl mx-auto space-y-6">
    <h1 class="text-2xl font-luxury text-text-dark">Mi Cuenta</h1>
    
    <!-- Profile Card -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="flex items-center gap-4 mb-6">
        <div class="w-16 h-16 rounded-full bg-[#C9A962]/20 flex items-center justify-center">
          <span class="text-[#C9A962] text-xl font-medium">{{ userInitials }}</span>
        </div>
        <div>
          <h2 class="text-lg font-medium text-text-dark">{{ user.nombre }}</h2>
          <p class="text-text-light">{{ user.email }}</p>
          <span class="inline-block mt-1 text-xs px-2 py-1 bg-[#C9A962]/10 text-[#C9A962] rounded-full">
            Mayorista Verificado
          </span>
        </div>
      </div>

      <div class="grid sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-text-medium mb-1">Empresa</label>
          <p class="text-text-dark">{{ user.empresa || 'No especificada' }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-text-medium mb-1">NIT/RUT</label>
          <p class="text-text-dark">{{ user.nit || 'No especificado' }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-text-medium mb-1">Teléfono</label>
          <p class="text-text-dark">{{ user.telefono || 'No especificado' }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-text-medium mb-1">Nivel de Descuento</label>
          <p class="text-[#C9A962] font-medium">{{ user.descuento || '15' }}%</p>
        </div>
      </div>

      <button class="mt-6 px-4 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">
        Editar Perfil
      </button>
    </div>

    <!-- Addresses -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <h3 class="text-lg font-medium text-text-dark mb-4">Direcciones de Envío</h3>
      <div class="p-4 border border-dashed border-gray-200 rounded-lg text-center">
        <p class="text-text-light mb-2">No hay direcciones guardadas</p>
        <button class="text-[#C9A962] text-sm hover:underline">+ Agregar dirección</button>
      </div>
    </div>

    <!-- Security -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <h3 class="text-lg font-medium text-text-dark mb-4">Seguridad</h3>
      <button class="px-4 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">
        Cambiar Contraseña
      </button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'B2BCuenta',
  setup() {
    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{"nombre": "Usuario", "email": "email@empresa.com"}')
    })

    const userInitials = computed(() => {
      const nombre = user.value.nombre || 'U'
      return nombre.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    })

    return {
      user,
      userInitials
    }
  }
}
</script>
