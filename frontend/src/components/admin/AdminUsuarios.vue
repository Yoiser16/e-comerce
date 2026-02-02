<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Usuarios del Sistema</h2>
        <p class="text-gray-500">Administra los usuarios con acceso al panel</p>
      </div>
      <button 
        @click="showModal = true"
        class="inline-flex w-full sm:w-auto justify-center items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold px-5 py-3 rounded-xl transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
        </svg>
        Nuevo Usuario
      </button>
    </div>

    <!-- Users Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[760px]">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Usuario</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Rol</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Último Acceso</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="user in usuarios" :key="user.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold" :class="getRoleColor(user.rol)">
                    {{ user.iniciales }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ user.nombre }}</p>
                    <p class="text-sm text-gray-500">{{ user.email }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span :class="getRoleBadge(user.rol)" class="px-3 py-1 text-xs font-medium rounded-full">
                  {{ user.rol }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span 
                  :class="user.activo ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
                  class="px-3 py-1 text-xs font-medium rounded-full"
                >
                  {{ user.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-6 py-4 text-gray-500 text-sm">{{ user.ultimoAcceso }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button class="p-2 text-gray-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button 
                    v-if="user.rol !== 'ADMIN'"
                    class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Roles Info -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Permisos por Rol</h3>
      <div class="grid md:grid-cols-3 gap-6">
        <div class="p-4 bg-red-50 rounded-xl">
          <h4 class="font-semibold text-red-700 mb-2">🔴 ADMIN</h4>
          <ul class="text-sm text-red-600 space-y-1">
            <li>✓ Acceso total al sistema</li>
            <li>✓ Gestión de usuarios</li>
            <li>✓ Eliminar recursos</li>
            <li>✓ Configuración del sistema</li>
          </ul>
        </div>
        <div class="p-4 bg-blue-50 rounded-xl">
          <h4 class="font-semibold text-blue-700 mb-2">🔵 OPERADOR</h4>
          <ul class="text-sm text-blue-600 space-y-1">
            <li>✓ Crear productos</li>
            <li>✓ Gestionar órdenes</li>
            <li>✓ Modificar inventario</li>
            <li>✗ Eliminar recursos</li>
          </ul>
        </div>
        <div class="p-4 bg-gray-50 rounded-xl">
          <h4 class="font-semibold text-gray-700 mb-2">⚪ LECTURA</h4>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>✓ Ver productos</li>
            <li>✓ Ver órdenes</li>
            <li>✓ Ver clientes</li>
            <li>✗ Modificar datos</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { usuariosService } from '../../services/usuarios'

export default {
  name: 'AdminUsuarios',
  setup() {
    const showModal = ref(false)
    const loading = ref(true)
    const usuarios = ref([])

    const cargarUsuarios = async () => {
      try {
        loading.value = true
        const data = await usuariosService.obtenerTodos()
        
        // Transformar datos al formato del componente
        usuarios.value = data.map(usuario => ({
          id: usuario.id,
          nombre: usuario.nombre || usuario.username || usuario.email.split('@')[0],
          email: usuario.email,
          rol: usuario.rol || usuario.role || 'LECTURA',
          activo: usuario.activo !== undefined ? usuario.activo : usuario.is_active !== undefined ? usuario.is_active : true,
          ultimoAcceso: formatearUltimoAcceso(usuario.last_login || usuario.ultimo_acceso),
          iniciales: obtenerIniciales(usuario.nombre || usuario.username || usuario.email)
        }))
      } catch (error) {
        console.error('Error al cargar usuarios:', error)
        // Si falla, mostrar usuarios básicos del sistema
        usuarios.value = [
          { id: '1', nombre: 'Administrador', email: 'admin@ecommerce.com', rol: 'ADMIN', activo: true, ultimoAcceso: 'Activo', iniciales: 'AD' },
          { id: '2', nombre: 'Operador Sistema', email: 'operador@ecommerce.com', rol: 'OPERADOR', activo: true, ultimoAcceso: 'Activo', iniciales: 'OP' },
          { id: '3', nombre: 'Lectura', email: 'lectura@ecommerce.com', rol: 'LECTURA', activo: true, ultimoAcceso: 'Activo', iniciales: 'LE' },
        ]
      } finally {
        loading.value = false
      }
    }

    const obtenerIniciales = (nombre) => {
      if (!nombre) return '??'
      const parts = nombre.trim().split(' ')
      if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase()
      }
      return nombre.substring(0, 2).toUpperCase()
    }

    const formatearUltimoAcceso = (fecha) => {
      if (!fecha) return 'Nunca'
      
      const now = new Date()
      const loginDate = new Date(fecha)
      const diffMs = now - loginDate
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMs / 3600000)
      const diffDays = Math.floor(diffMs / 86400000)

      if (diffMins < 1) return 'Ahora mismo'
      if (diffMins < 60) return `Hace ${diffMins} minutos`
      if (diffHours < 24) return `Hace ${diffHours} horas`
      if (diffDays === 1) return 'Ayer'
      if (diffDays < 7) return `Hace ${diffDays} días`
      if (diffDays < 30) return `Hace ${Math.floor(diffDays / 7)} semanas`
      return `Hace ${Math.floor(diffDays / 30)} meses`
    }

    const getRoleColor = (rol) => {
      const colors = {
        'ADMIN': 'bg-red-500',
        'OPERADOR': 'bg-blue-500',
        'LECTURA': 'bg-gray-400'
      }
      return colors[rol] || 'bg-gray-400'
    }

    const getRoleBadge = (rol) => {
      const badges = {
        'ADMIN': 'bg-red-100 text-red-700',
        'OPERADOR': 'bg-blue-100 text-blue-700',
        'LECTURA': 'bg-gray-100 text-gray-700'
      }
      return badges[rol] || 'bg-gray-100 text-gray-700'
    }

    onMounted(() => {
      cargarUsuarios()
    })

    return { showModal, loading, usuarios, getRoleColor, getRoleBadge, cargarUsuarios }
  }
}
</script>

