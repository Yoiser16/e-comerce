<template>
  <div class="space-y-6 sm:space-y-8">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="font-luxury text-3xl sm:text-4xl text-text-dark mb-1">Base de Clientes</h2>
        <p class="text-text-medium text-sm sm:text-base">Gestión integral y análisis de tu cartera de clientes</p>
      </div>
      <button 
        @click="exportarCSV"
        class="hidden sm:flex py-2.5 px-5 text-sm font-medium text-white bg-text-dark hover:bg-black rounded-xl transition-colors duration-300 gap-2 items-center"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33A3.75 3.75 0 0113.5 19.5H6.75z" />
        </svg>
        Exportar
      </button>
    </div>

    <!-- Dashboard KPIs -->
    <div class="grid grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
      <!-- Total Ingresos -->
      <div class="bg-white rounded-2xl sm:rounded-3xl shadow-soft border border-text-dark/5 p-4 sm:p-6">
        <p class="text-text-light text-xs sm:text-sm mb-2">Ingreso Total</p>
        <p class="font-semibold text-xl sm:text-2xl text-text-dark">${{ formatNumber(totalIngresos) }}</p>
        <p class="text-text-light text-xs mt-2">de {{ clientes.length }} clientes</p>
      </div>

      <!-- Ticket Promedio -->
      <div class="bg-white rounded-2xl sm:rounded-3xl shadow-soft border border-text-dark/5 p-4 sm:p-6">
        <p class="text-text-light text-xs sm:text-sm mb-2">Ticket Promedio</p>
        <p class="font-semibold text-xl sm:text-2xl text-brand-600">${{ formatNumber(ticketPromedio) }}</p>
        <p class="text-text-light text-xs mt-2">por cliente</p>
      </div>

      <!-- Orden Promedio -->
      <div class="bg-white rounded-2xl sm:rounded-3xl shadow-soft border border-text-dark/5 p-4 sm:p-6">
        <p class="text-text-light text-xs sm:text-sm mb-2">Órdenes Promedio</p>
        <p class="font-semibold text-xl sm:text-2xl text-text-dark">{{ ordenesPromedio }}</p>
        <p class="text-text-light text-xs mt-2">por cliente</p>
      </div>
    </div>

    <!-- Filtros y búsqueda -->
    <div class="space-y-4 sm:space-y-0 sm:flex gap-4 items-end">
      <!-- Search -->
      <div class="flex-1 bg-white rounded-3xl shadow-soft border border-text-dark/5 p-4 sm:p-6">
        <div class="relative">
          <svg class="absolute left-4 sm:left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-text-light" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por nombre o email..."
            class="w-full pl-12 sm:pl-14 pr-4 sm:pr-6 py-3 sm:py-4 bg-[#FAFAFA] border border-text-dark/5 rounded-2xl text-sm sm:text-base text-text-dark placeholder-text-light/60 focus:outline-none focus:border-text-dark/20 focus:bg-white focus:ring-1 focus:ring-text-dark/5 transition-all duration-300"
          >
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="flex flex-col items-center gap-4">
        <div class="animate-spin rounded-full h-12 w-12 border-2 border-text-dark/10 border-t-text-dark"></div>
        <p class="text-text-medium text-sm">Cargando clientes...</p>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredClients.length === 0" class="bg-white rounded-3xl shadow-soft border border-text-dark/5 p-8 sm:p-12 text-center">
      <svg class="mx-auto h-16 w-16 sm:h-20 sm:w-20 text-text-light/40 mb-4" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <p class="text-text-medium text-sm sm:text-base">No se encontraron clientes</p>
    </div>

    <!-- Contenido (Tabla y Grid) -->
    <template v-else>
      <!-- Tabla de clientes (Desktop) -->
      <div class="hidden lg:block bg-white rounded-3xl shadow-soft border border-text-dark/5 overflow-hidden">
      <table class="w-full">
        <thead>
          <tr class="border-b border-text-dark/5 bg-[#FAFAFA]">
            <th class="px-6 py-4 text-left text-xs font-semibold text-text-dark">Cliente</th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-text-dark">Email</th>
            <th class="px-6 py-4 text-center text-xs font-semibold text-text-dark">Órdenes</th>
            <th class="px-6 py-4 text-right text-xs font-semibold text-text-dark">Gasto Total</th>
            <th class="px-6 py-4 text-center text-xs font-semibold text-text-dark">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-text-dark/5">
          <tr v-for="cliente in filteredClients" :key="cliente.id" class="hover:bg-[#FAFAFA] transition-colors">
            <td class="px-6 py-4 text-sm font-medium text-text-dark">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-gradient-to-br from-[#F5EBE5] to-[#FAF5F2] rounded-full flex items-center justify-center text-text-dark font-luxury font-semibold text-xs">
                  {{ cliente.iniciales }}
                </div>
                {{ cliente.nombre }}
              </div>
            </td>
            <td class="px-6 py-4 text-sm text-text-light">{{ cliente.email }}</td>
            <td class="px-6 py-4 text-sm text-center text-text-dark font-medium">{{ cliente.ordenes }}</td>
            <td class="px-6 py-4 text-sm text-right font-semibold text-brand-600">${{ formatNumber(cliente.totalCompras) }}</td>
            <td class="px-6 py-4 text-center space-x-3">
              <button @click="verDetalles(cliente)" class="text-brand-600 hover:text-brand-700 transition-colors" title="Ver órdenes">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
              <button @click="copiarEmail(cliente.email)" class="text-text-light hover:text-text-dark transition-colors" title="Copiar email">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Grid de clientes (Mobile) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 lg:hidden">
      <div 
        v-for="cliente in filteredClients" 
        :key="cliente.id"
        class="group bg-white rounded-2xl sm:rounded-3xl shadow-soft border border-text-dark/5 p-5 sm:p-6 hover:shadow-md hover:shadow-text-dark/10 transition-all duration-300"
      >
        <!-- Avatar y Información básica -->
        <div class="flex items-start gap-4 mb-5 sm:mb-6">
          <div class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-[#F5EBE5] to-[#FAF5F2] rounded-full flex items-center justify-center text-text-dark font-luxury font-semibold text-sm sm:text-base flex-shrink-0">
            {{ cliente.iniciales }}
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-text-dark text-sm sm:text-base truncate group-hover:text-brand-600 transition-colors">{{ cliente.nombre }}</h3>
            <p class="text-xs sm:text-sm text-text-light truncate mt-0.5">{{ cliente.email }}</p>

          </div>
        </div>
        
        <!-- Estadísticas -->
        <div class="grid grid-cols-2 gap-3 sm:gap-4 py-4 sm:py-5 border-t border-b border-text-dark/5">
          <div class="text-center">
            <p class="text-xl sm:text-2xl font-semibold text-text-dark">{{ cliente.ordenes }}</p>
            <p class="text-xs text-text-light mt-1">Órdenes</p>
          </div>
          <div class="text-center">
            <p class="text-xl sm:text-2xl font-semibold text-brand-600">${{ formatNumber(cliente.totalCompras) }}</p>
            <p class="text-xs text-text-light mt-1">Total gastado</p>
          </div>
        </div>

        <!-- Acciones -->
        <div class="mt-4 sm:mt-5 flex gap-2">
          <button 
            @click="verDetalles(cliente)"
            class="flex-1 py-2.5 sm:py-3 px-3 sm:px-4 text-xs sm:text-sm font-medium text-white bg-text-dark hover:bg-black rounded-xl sm:rounded-2xl transition-colors duration-300"
          >
            Ver detalle
          </button>
          <button 
            @click="copiarEmail(cliente.email)"
            class="p-2.5 sm:p-3 text-text-light hover:text-text-dark hover:bg-[#FAFAFA] rounded-xl sm:rounded-2xl transition-all duration-300" 
            title="Copiar email"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    </template>
  </div>

  <!-- Notificación flotante -->
  <transition name="fade">
    <div v-if="notificacion.visible" class="fixed bottom-6 right-6 sm:bottom-8 sm:right-8 z-50">
      <div :class="[
        'px-5 sm:px-6 py-3 sm:py-4 rounded-2xl shadow-lg text-sm font-medium flex items-center gap-3',
        notificacion.tipo === 'success' 
          ? 'bg-green-500 text-white' 
          : 'bg-red-500 text-white'
      ]">
        <svg v-if="notificacion.tipo === 'success'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        {{ notificacion.mensaje }}
      </div>
    </div>
  </transition>

  <!-- Modal de detalles del cliente -->
  <transition name="modal">
    <div v-if="mostrarModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      <!-- Overlay -->
      <div @click="cerrarModal" class="absolute inset-0 bg-black/30 backdrop-blur-md"></div>
      
      <!-- Modal -->
      <div class="relative bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <!-- Header con gradiente -->
        <div class="bg-gradient-to-r from-[#FAF5F2] to-[#F5EBE5] border-b border-text-dark/5 px-6 sm:px-8 py-8 sm:py-10 flex items-start justify-between">
          <div class="flex items-center gap-5">
            <div class="w-16 h-16 bg-gradient-to-br from-[#F5EBE5] to-[#FAF5F2] rounded-2xl flex items-center justify-center text-text-dark font-luxury font-semibold text-2xl border border-text-dark/10">
              {{ clienteSeleccionado?.iniciales }}
            </div>
            <div>
              <h3 class="font-luxury text-2xl text-text-dark">{{ clienteSeleccionado?.nombre }}</h3>
              <p class="text-xs text-text-light uppercase tracking-wide mt-2">Cliente registrado</p>
            </div>
          </div>
          <button @click="cerrarModal" class="text-text-light hover:text-text-dark hover:bg-white/50 p-2 rounded-xl transition-all">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Contenido -->
        <div v-if="clienteSeleccionado" class="p-6 sm:p-8 space-y-8">
          
          <!-- Sección 1: Información de contacto -->
          <div class="space-y-4">
            <h4 class="font-luxury text-lg text-text-dark">Información de Contacto</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <!-- Email -->
              <div class="bg-[#FAFAFA] rounded-2xl p-4 sm:p-5 border border-text-dark/5">
                <p class="text-xs text-text-light uppercase tracking-wide mb-2">Email</p>
                <div class="flex items-center justify-between gap-2">
                  <p class="text-sm font-medium text-text-dark break-all">{{ clienteSeleccionado.email }}</p>
                  <button 
                    @click="copiarEmail(clienteSeleccionado.email)"
                    class="text-brand-600 hover:text-brand-700 hover:bg-white p-2 rounded-lg transition-colors flex-shrink-0"
                    title="Copiar email"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </button>
                </div>
              </div>
              <!-- Teléfono -->
              <div class="bg-[#FAFAFA] rounded-2xl p-4 sm:p-5 border border-text-dark/5">
                <p class="text-xs text-text-light uppercase tracking-wide mb-2">Teléfono</p>
                <p class="text-sm font-medium text-text-dark">{{ clienteSeleccionado.telefono }}</p>
              </div>
            </div>
          </div>

          <div class="h-px bg-text-dark/5"></div>

          <!-- Sección 2: Métricas principales -->
          <div class="space-y-4">
            <h4 class="font-luxury text-lg text-text-dark">Resumen de Compras</h4>
            <div class="grid grid-cols-1 gap-4">
              <!-- Total gasto - Destacado -->
              <div class="bg-gradient-to-br from-brand-50 to-brand-100/30 border border-brand-200/50 rounded-3xl p-6 sm:p-8">
                <p class="text-xs text-text-light uppercase tracking-[0.15em] font-semibold mb-3">Monto Total Invertido</p>
                <p class="font-luxury text-4xl sm:text-5xl text-brand-600 mb-2">${{ formatNumber(clienteSeleccionado.totalCompras) }}</p>
                <div class="h-px bg-brand-200/30 my-4"></div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-xs text-text-light uppercase tracking-wide mb-1">Órdenes</p>
                    <p class="text-2xl font-semibold text-text-dark">{{ clienteSeleccionado.ordenes }}</p>
                  </div>
                  <div>
                    <p class="text-xs text-text-light uppercase tracking-wide mb-1">Última Compra</p>
                    <p class="text-sm font-medium text-text-dark">{{ formatFecha(clienteSeleccionado.ultimaCompra) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="h-px bg-text-dark/5"></div>

          <!-- Sección 3: Historial de órdenes -->
          <div v-if="ordenesCliente.length > 0" class="space-y-4">
            <h4 class="font-luxury text-lg text-text-dark">Historial de Órdenes</h4>
            <div class="space-y-2 max-h-64 overflow-y-auto pr-2">
              <div v-for="(orden, idx) in ordenesCliente" :key="orden.id" class="bg-gradient-to-r from-white to-[#FAFAFA] rounded-2xl border border-text-dark/5 p-4 hover:border-brand-200 hover:shadow-soft transition-all">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-brand-50 flex items-center justify-center text-brand-600 font-semibold text-sm">
                      #{{ idx + 1 }}
                    </div>
                    <div>
                      <p class="font-medium text-text-dark text-sm">Orden {{ orden.id }}</p>
                      <p class="text-xs text-text-light">{{ formatFecha(orden.fecha_creacion) }}</p>
                    </div>
                  </div>
                  <p class="font-semibold text-brand-600 text-sm">${{ formatNumber(orden.total_monto) }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="h-px bg-text-dark/5"></div>

          <!-- Acciones footer -->
          <div class="flex gap-3 pt-2">
            <button 
              @click="enviarEmail(clienteSeleccionado.email)"
              class="flex-1 py-3 px-5 text-sm font-semibold text-white bg-green-500 hover:bg-green-600 active:scale-95 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 shadow-soft"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Enviar Email
            </button>
            <button 
              @click="cerrarModal"
              class="flex-1 py-3 px-5 text-sm font-semibold text-text-dark bg-[#FAFAFA] hover:bg-gray-100 active:scale-95 rounded-xl transition-all duration-200 border border-text-dark/10"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-active > div:last-child,
.modal-leave-active > div:last-child {
  transition: transform 0.3s ease;
}

.modal-enter-from > div:last-child,
.modal-leave-to > div:last-child {
  transform: scale(0.95);
}
</style>

<script>
import { ref, computed, onMounted } from 'vue'
import { ordenesService } from '../../services/ordenes'

export default {
  name: 'AdminClientes',
  setup() {
    const searchQuery = ref('')
    const loading = ref(true)
    const clientes = ref([])
    const ordenesTodas = ref([])
    const clienteSeleccionado = ref(null)
    const mostrarModal = ref(false)
    const notificacion = ref({ visible: false, mensaje: '', tipo: 'success' })
    const filtroSegmento = ref('')
    const ordenesCliente = ref([])

    const cargarClientes = async () => {
      try {
        loading.value = true
        // Obtener todas las órdenes para extraer información de clientes
        const ordenes = await ordenesService.obtenerTodas()
        ordenesTodas.value = ordenes
        
        // Agrupar órdenes por cliente
        const clientesMap = {}
        ordenes.forEach(orden => {
          const clienteId = orden.cliente_id || orden.cliente_email
          if (!clienteId) return
          
          // Construir nombre del cliente de forma defensiva
          let nombreCliente = orden.cliente_nombre
          if (!nombreCliente || nombreCliente === 'undefined' || nombreCliente === 'null') {
            nombreCliente = orden.cliente_nombre_pila || orden.nombre_cliente || 'Cliente anónimo'
          }
          
          if (!clientesMap[clienteId]) {
            const ordenesCliente = ordenes.filter(o => o.cliente_id === clienteId || o.cliente_email === clienteId)
            const totalCompras = ordenesCliente.reduce((sum, o) => sum + (o.total_monto || o.total || 0), 0)
            const ultimaOrden = ordenesCliente.sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion))[0]
            
            clientesMap[clienteId] = {
              id: orden.cliente_id || orden.cliente_email,
              nombre: nombreCliente,
              email: orden.cliente_email || 'no@disponible.com',
              telefono: orden.cliente_telefono || 'No especificado',
              ordenes: 0,
              totalCompras: totalCompras,
              iniciales: obtenerIniciales(nombreCliente),
              ultimaCompra: ultimaOrden?.fecha_creacion || null
            }
          }
          
          clientesMap[clienteId].ordenes += 1
        })
        
        clientes.value = Object.values(clientesMap)
      } catch (error) {
        console.error('Error al cargar clientes desde órdenes:', error)
        clientes.value = []
      } finally {
        loading.value = false
      }
    }

    const obtenerIniciales = (nombre) => {
      if (!nombre || nombre === 'undefined' || nombre === 'null') return '??'
      const cleanNombre = nombre.trim()
      if (!cleanNombre) return '??'
      const parts = cleanNombre.split(' ')
      if (parts.length >= 2) {
        const firstInitial = parts[0][0]
        const secondInitial = parts[1][0]
        if (!firstInitial || !secondInitial) return '??'
        return (firstInitial + secondInitial).toUpperCase()
      }
      const twoChars = cleanNombre.substring(0, 2)
      return twoChars.length >= 2 ? twoChars.toUpperCase() : '??'
    }

    const obtenerOrdenesCliente = (clienteId) => {
      return ordenesTodas.value.filter(o => o.cliente_id === clienteId)
    }

    const formatFecha = (fecha) => {
      if (!fecha) return 'N/A'
      return new Date(fecha).toLocaleDateString('es-CO')
    }

    const filteredClients = computed(() => {
      let resultado = clientes.value

      // Filtrar por búsqueda
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        resultado = resultado.filter(c => 
          c.nombre.toLowerCase().includes(query) ||
          c.email.toLowerCase().includes(query)
        )
      }

      return resultado
    })

    const formatNumber = (num) => new Intl.NumberFormat('es-CO').format(num)

    const mostrarNotificacion = (mensaje, tipo = 'success') => {
      notificacion.value = { visible: true, mensaje, tipo }
      setTimeout(() => {
        notificacion.value.visible = false
      }, 3000)
    }

    const verDetalles = (cliente) => {
      clienteSeleccionado.value = cliente
      ordenesCliente.value = obtenerOrdenesCliente(cliente.id)
      mostrarModal.value = true
    }

    const cerrarModal = () => {
      mostrarModal.value = false
      clienteSeleccionado.value = null
    }

    const copiarEmail = async (email) => {
      try {
        await navigator.clipboard.writeText(email)
        mostrarNotificacion(`Email copiado: ${email}`, 'success')
      } catch (error) {
        console.error('Error al copiar email:', error)
        mostrarNotificacion('Error al copiar email', 'error')
      }
    }

    const enviarEmail = (email) => {
      window.location.href = `mailto:${email}`
    }

    const exportarCSV = () => {
      const headers = ['Cliente', 'Email', 'Teléfono', 'Órdenes', 'Total Compras', 'Segmento']
      const rows = filteredClients.value.map(c => [
        c.nombre,
        c.email,
        c.telefono,
        c.ordenes,
        c.totalCompras,
        c.segmento === 'vip' ? 'VIP' : c.segmento === 'regular' ? 'Regular' : 'Nuevo'
      ])

      let csv = headers.join(',') + '\n'
      rows.forEach(row => {
        csv += row.map(cell => `"${cell}"`).join(',') + '\n'
      })

      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `clientes_${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
      mostrarNotificacion('Datos exportados correctamente', 'success')
    }

    const totalIngresos = computed(() => {
      return clientes.value.reduce((sum, c) => sum + c.totalCompras, 0)
    })

    const ticketPromedio = computed(() => {
      if (clientes.value.length === 0) return 0
      return totalIngresos.value / clientes.value.length
    })

    const ordenesPromedio = computed(() => {
      if (clientes.value.length === 0) return 0
      const totalOrdenes = clientes.value.reduce((sum, c) => sum + c.ordenes, 0)
      return (totalOrdenes / clientes.value.length).toFixed(1)
    })

    onMounted(() => {
      cargarClientes()
    })

    return { 
      searchQuery, 
      loading, 
      clientes, 
      filteredClients, 
      formatNumber,
      formatFecha,
      cargarClientes,
      clienteSeleccionado,
      mostrarModal,
      notificacion,
      verDetalles,
      cerrarModal,
      copiarEmail,
      enviarEmail,
      mostrarNotificacion,
      ordenesCliente,
      exportarCSV,
      totalIngresos,
      ticketPromedio,
      ordenesPromedio
    }
  }
}
</script>

