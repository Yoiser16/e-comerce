<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Órdenes</h2>
        <p class="text-gray-500">Gestiona los pedidos de tus clientes</p>
      </div>
      <div class="flex items-center gap-3">
        <button class="inline-flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-4 py-2.5 rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Exportar
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
      <div 
        v-for="stat in orderStats" 
        :key="stat.status"
        @click="filterStatus = stat.status"
        :class="[
          'p-4 rounded-2xl border-2 cursor-pointer transition-all',
          filterStatus === stat.status ? 'border-brand-500 bg-brand-50' : 'border-gray-100 bg-white hover:border-gray-200'
        ]"
      >
        <p class="text-2xl font-bold" :class="stat.color">{{ stat.count }}</p>
        <p class="text-sm text-gray-500">{{ stat.label }}</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4">
      <div class="flex flex-col lg:flex-row gap-4">
        <div class="flex-1 relative">
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por # orden o cliente..."
            class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
          >
        </div>
        <input 
          type="date" 
          v-model="filterDate"
          class="px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
        >
        <button 
          @click="clearFilters"
          class="px-4 py-3 text-gray-600 hover:text-gray-900 font-medium"
        >
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Orders Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="filteredOrders.length === 0" class="text-center py-20">
        <svg class="mx-auto h-16 w-16 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="mt-4 text-gray-500">No se encontraron órdenes</p>
      </div>

      <!-- Table Content -->
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Orden</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Cliente</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Productos</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Total</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase">Fecha</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="orden in filteredOrders" :key="orden.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <span class="font-mono font-medium text-gray-900">{{ orden.codigo || '#' + orden.id.slice(0, 8) }}</span>
              </td>
              <td class="px-6 py-4">
                <div>
                  <p class="font-medium text-gray-900">{{ orden.cliente_nombre }}</p>
                  <p class="text-sm text-gray-500">{{ orden.cliente_email }}</p>
                  <p v-if="orden.cliente_telefono" class="text-xs text-gray-400">{{ orden.cliente_telefono }}</p>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-gray-600">{{ orden.total_items }} productos</span>
              </td>
              <td class="px-6 py-4">
                <span class="font-semibold text-gray-900">${{ formatNumber(orden.total) }}</span>
              </td>
              <td class="px-6 py-4">
                <select 
                  v-model="orden.estado"
                  @change="updateOrderStatus(orden)"
                  :class="getStatusClass(orden.estado)"
                  class="px-3 py-1.5 text-xs font-medium rounded-full border-0 cursor-pointer"
                >
                  <option value="PENDIENTE">Pendiente</option>
                  <option value="CONFIRMADA">Confirmada</option>
                  <option value="EN_PROCESO">En Proceso</option>
                  <option value="ENVIADA">Enviada</option>
                  <option value="COMPLETADA">Completada</option>
                  <option value="CANCELADA">Cancelada</option>
                </select>
              </td>
              <td class="px-6 py-4 text-gray-500 text-sm">{{ orden.fecha }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button 
                    @click="viewOrder(orden)"
                    class="p-2 text-gray-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="Ver detalle"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button 
                    @click="printOrder(orden)"
                    class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Imprimir"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal de Detalles de Orden -->
    <div 
      v-if="showOrderDetail" 
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click.self="closeOrderDetail"
    >
      <div class="bg-white rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <!-- Header del Modal -->
        <div class="sticky top-0 bg-white border-b border-gray-100 px-6 py-5 flex items-center justify-between rounded-t-3xl">
          <div>
            <h3 class="text-xl font-bold text-gray-900">Detalle de Orden</h3>
            <p class="text-sm text-gray-500 font-mono mt-1">{{ selectedOrder?.codigo }}</p>
          </div>
          <button 
            @click="closeOrderDetail"
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Contenido del Modal -->
        <div v-if="loadingDetail" class="flex items-center justify-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
        </div>

        <div v-else-if="orderDetail" class="p-6 space-y-6">
          <!-- Información del Cliente -->
          <div class="bg-gradient-to-br from-[#F8F3EF] to-[#FAF5F2] rounded-2xl p-5 border border-nude-200/50">
            <h4 class="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-[#8B7355]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Información del Cliente
            </h4>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p class="text-gray-500 mb-1">Nombre</p>
                <p class="font-medium text-gray-900">{{ orderDetail.cliente_nombre }}</p>
              </div>
              <div>
                <p class="text-gray-500 mb-1">Documento</p>
                <p class="font-medium text-gray-900">{{ orderDetail.cliente_tipo_doc }} {{ orderDetail.cliente_num_doc }}</p>
              </div>
              <div>
                <p class="text-gray-500 mb-1">Email</p>
                <p class="font-medium text-gray-900">{{ orderDetail.cliente_email }}</p>
              </div>
              <div>
                <p class="text-gray-500 mb-1">Teléfono</p>
                <p class="font-medium text-gray-900">{{ orderDetail.cliente_telefono }}</p>
              </div>
            </div>
          </div>

          <!-- Dirección de Envío -->
          <div v-if="orderDetail.direccion_envio" class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-5 border border-blue-100">
            <h4 class="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Dirección de Envío
            </h4>
            <div class="space-y-2 text-sm">
              <p class="text-gray-900">{{ orderDetail.direccion_envio }}</p>
              <p class="text-gray-700">{{ orderDetail.barrio }}, {{ orderDetail.municipio }}, {{ orderDetail.departamento }}</p>
              <p v-if="orderDetail.notas_envio" class="text-gray-600 italic mt-2">{{ orderDetail.notas_envio }}</p>
            </div>
          </div>

          <!-- Productos -->
          <div class="border border-gray-200 rounded-2xl overflow-hidden">
            <div class="bg-gray-50 px-5 py-3 border-b border-gray-200">
              <h4 class="font-semibold text-gray-900 flex items-center gap-2">
                <svg class="w-5 h-5 text-[#8B7355]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                Productos ({{ orderDetail.items?.length || 0 }})
              </h4>
            </div>
            <div class="divide-y divide-gray-100">
              <div 
                v-for="item in orderDetail.items" 
                :key="item.id"
                class="flex items-center gap-4 p-4 hover:bg-gray-50"
              >
                <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center flex-shrink-0 border border-brand-200">
                  <span class="font-bold text-brand-700">{{ item.cantidad }}x</span>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="font-medium text-gray-900">{{ item.nombre }}</p>
                  <p class="text-sm text-gray-500">{{ item.sku }}</p>
                </div>
                <div class="text-right">
                  <p class="font-semibold text-gray-900">${{ formatNumber(item.precio_unitario * item.cantidad) }}</p>
                  <p class="text-sm text-gray-500">${{ formatNumber(item.precio_unitario) }} c/u</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Totales -->
          <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-5 border border-green-100">
            <div class="space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Subtotal</span>
                <span class="font-medium text-gray-900">${{ formatNumber(orderDetail.subtotal_monto || 0) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Envío</span>
                <span class="font-medium text-gray-900">${{ formatNumber(orderDetail.envio_monto || 0) }}</span>
              </div>
              <div class="flex justify-between text-lg font-bold pt-3 border-t border-green-200">
                <span class="text-gray-900">Total</span>
                <span class="text-green-700">${{ formatNumber(orderDetail.total) }}</span>
              </div>
            </div>
          </div>

          <!-- Estado y Método de Pago -->
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-gray-50 rounded-xl p-4">
              <p class="text-sm text-gray-500 mb-2">Estado</p>
              <span :class="getStatusClass(orderDetail.estado)" class="inline-block px-3 py-1.5 text-xs font-medium rounded-full">
                {{ getStatusLabel(orderDetail.estado) }}
              </span>
            </div>
            <div class="bg-gray-50 rounded-xl p-4">
              <p class="text-sm text-gray-500 mb-2">Método de Pago</p>
              <p class="font-medium text-gray-900 capitalize">{{ orderDetail.metodo_pago || 'WhatsApp' }}</p>
            </div>
          </div>

          <!-- Botones de Acción -->
          <div class="flex gap-3 pt-4">
            <button 
              @click="printOrder(orderDetail)"
              class="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-medium px-6 py-3 rounded-xl transition-all flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Imprimir
            </button>
            <button 
              @click="closeOrderDetail"
              class="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition-colors"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Área de impresión oculta -->
    <div id="printArea" class="hidden print:block">
      <div v-if="orderDetail" class="p-8 max-w-4xl mx-auto">
        <!-- Header de Impresión -->
        <div class="text-center mb-8 border-b-2 border-gray-300 pb-6">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Kharis Distribuidora</h1>
          <p class="text-gray-600">Orden de Pedido</p>
        </div>

        <!-- Información de la Orden -->
        <div class="grid grid-cols-2 gap-8 mb-8">
          <div>
            <h3 class="font-bold text-gray-900 mb-3">Información de Orden</h3>
            <p class="text-sm mb-1"><strong>Código:</strong> {{ orderDetail.codigo }}</p>
            <p class="text-sm mb-1"><strong>Fecha:</strong> {{ formatearFecha(orderDetail.fecha_creacion) }}</p>
            <p class="text-sm mb-1"><strong>Estado:</strong> {{ getStatusLabel(orderDetail.estado) }}</p>
            <p class="text-sm"><strong>Método de Pago:</strong> {{ orderDetail.metodo_pago || 'WhatsApp' }}</p>
          </div>
          <div>
            <h3 class="font-bold text-gray-900 mb-3">Información del Cliente</h3>
            <p class="text-sm mb-1"><strong>Nombre:</strong> {{ orderDetail.cliente_nombre }}</p>
            <p class="text-sm mb-1"><strong>Documento:</strong> {{ orderDetail.cliente_tipo_doc }} {{ orderDetail.cliente_num_doc }}</p>
            <p class="text-sm mb-1"><strong>Email:</strong> {{ orderDetail.cliente_email }}</p>
            <p class="text-sm"><strong>Teléfono:</strong> {{ orderDetail.cliente_telefono }}</p>
          </div>
        </div>

        <!-- Dirección de Envío -->
        <div v-if="orderDetail.direccion_envio" class="mb-8">
          <h3 class="font-bold text-gray-900 mb-3">Dirección de Envío</h3>
          <p class="text-sm">{{ orderDetail.direccion_envio }}</p>
          <p class="text-sm">{{ orderDetail.barrio }}, {{ orderDetail.municipio }}, {{ orderDetail.departamento }}</p>
          <p v-if="orderDetail.notas_envio" class="text-sm mt-2"><strong>Notas:</strong> {{ orderDetail.notas_envio }}</p>
        </div>

        <!-- Tabla de Productos -->
        <div class="mb-8">
          <h3 class="font-bold text-gray-900 mb-3">Productos</h3>
          <table class="w-full border-collapse border border-gray-300">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-4 py-2 text-left">SKU</th>
                <th class="border border-gray-300 px-4 py-2 text-left">Producto</th>
                <th class="border border-gray-300 px-4 py-2 text-center">Cantidad</th>
                <th class="border border-gray-300 px-4 py-2 text-right">Precio Unit.</th>
                <th class="border border-gray-300 px-4 py-2 text-right">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in orderDetail.items" :key="item.id">
                <td class="border border-gray-300 px-4 py-2 text-sm">{{ item.sku }}</td>
                <td class="border border-gray-300 px-4 py-2 text-sm">{{ item.nombre }}</td>
                <td class="border border-gray-300 px-4 py-2 text-center text-sm">{{ item.cantidad }}</td>
                <td class="border border-gray-300 px-4 py-2 text-right text-sm">${{ formatNumber(item.precio_unitario) }}</td>
                <td class="border border-gray-300 px-4 py-2 text-right text-sm">${{ formatNumber(item.precio_unitario * item.cantidad) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Totales -->
        <div class="flex justify-end">
          <div class="w-64">
            <div class="flex justify-between mb-2">
              <span class="text-sm">Subtotal:</span>
              <span class="text-sm font-medium">${{ formatNumber(orderDetail.subtotal_monto || 0) }}</span>
            </div>
            <div class="flex justify-between mb-2">
              <span class="text-sm">Envío:</span>
              <span class="text-sm font-medium">${{ formatNumber(orderDetail.envio_monto || 0) }}</span>
            </div>
            <div class="flex justify-between pt-2 border-t-2 border-gray-300">
              <span class="font-bold">TOTAL:</span>
              <span class="font-bold text-lg">${{ formatNumber(orderDetail.total) }}</span>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="mt-12 pt-6 border-t border-gray-300 text-center text-sm text-gray-600">
          <p>Gracias por su compra | Kharis Distribuidora</p>
          <p class="mt-1">WhatsApp: +57 321 735 5070</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ordenesService } from '../../services/ordenes'

export default {
  name: 'AdminOrdenes',
  setup() {
    const searchQuery = ref('')
    const filterStatus = ref('')
    const filterDate = ref('')
    const loading = ref(true)
    const ordenes = ref([])
    const showOrderDetail = ref(false)
    const loadingDetail = ref(false)
    const selectedOrder = ref(null)
    const orderDetail = ref(null)

    const orderStats = computed(() => {
      const all = ordenes.value.length
      const pendiente = ordenes.value.filter(o => o.estado === 'PENDIENTE').length
      const confirmada = ordenes.value.filter(o => o.estado === 'CONFIRMADA').length
      const enviada = ordenes.value.filter(o => o.estado === 'ENVIADA').length
      const completada = ordenes.value.filter(o => o.estado === 'COMPLETADA').length

      return [
        { status: '', label: 'Todas', count: all, color: 'text-gray-900' },
        { status: 'PENDIENTE', label: 'Pendientes', count: pendiente, color: 'text-yellow-600' },
        { status: 'CONFIRMADA', label: 'Confirmadas', count: confirmada, color: 'text-blue-600' },
        { status: 'ENVIADA', label: 'Enviadas', count: enviada, color: 'text-indigo-600' },
        { status: 'COMPLETADA', label: 'Completadas', count: completada, color: 'text-green-600' }
      ]
    })

    const cargarOrdenes = async () => {
      try {
        loading.value = true
        const data = await ordenesService.obtenerTodas()
        
        // Los datos ya vienen en el formato correcto desde la API
        ordenes.value = data.map(orden => ({
          id: orden.id,
          codigo: orden.codigo,
          cliente_nombre: orden.cliente_nombre || 'Sin cliente',
          cliente_email: orden.cliente_email || '',
          cliente_telefono: orden.cliente_telefono || '',
          total_items: orden.total_items || 0,
          total: orden.total || 0,
          estado: orden.estado,
          metodo_pago: orden.metodo_pago || 'whatsapp',
          fecha: formatearFecha(orden.fecha_creacion)
        }))
      } catch (error) {
        console.error('Error al cargar órdenes:', error)
        ordenes.value = []
      } finally {
        loading.value = false
      }
    }

    const formatearFecha = (fecha) => {
      if (!fecha) return ''
      const date = new Date(fecha)
      return new Intl.DateTimeFormat('es-ES', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }

    const filteredOrders = computed(() => {
      let result = ordenes.value

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(o => 
          o.id.toLowerCase().includes(query) ||
          (o.codigo && o.codigo.toLowerCase().includes(query)) ||
          o.cliente_nombre.toLowerCase().includes(query) ||
          o.cliente_email.toLowerCase().includes(query) ||
          (o.cliente_telefono && o.cliente_telefono.includes(query))
        )
      }

      if (filterStatus.value) {
        result = result.filter(o => o.estado === filterStatus.value)
      }

      return result
    })

    const formatNumber = (num) => new Intl.NumberFormat('es-CO').format(num)

    const getStatusClass = (status) => {
      const classes = {
        'PENDIENTE': 'bg-yellow-100 text-yellow-700',
        'CONFIRMADA': 'bg-blue-100 text-blue-700',
        'EN_PROCESO': 'bg-purple-100 text-purple-700',
        'ENVIADA': 'bg-indigo-100 text-indigo-700',
        'COMPLETADA': 'bg-green-100 text-green-700',
        'CANCELADA': 'bg-red-100 text-red-700'
      }
      return classes[status] || 'bg-gray-100 text-gray-700'
    }

    const clearFilters = () => {
      searchQuery.value = ''
      filterStatus.value = ''
      filterDate.value = ''
    }

    const updateOrderStatus = async (orden) => {
      try {
        await ordenesService.actualizarEstado(orden.id, orden.estado)
        console.log('Estado actualizado:', orden.id, orden.estado)
      } catch (error) {
        console.error('Error al actualizar estado:', error)
      }
    }

    const viewOrder = async (orden) => {
      selectedOrder.value = orden
      showOrderDetail.value = true
      loadingDetail.value = true
      
      try {
        const detalle = await ordenesService.obtenerPorId(orden.id)
        orderDetail.value = detalle
      } catch (error) {
        console.error('Error al cargar detalle de orden:', error)
        alert('Error al cargar los detalles de la orden')
        showOrderDetail.value = false
      } finally {
        loadingDetail.value = false
      }
    }

    const closeOrderDetail = () => {
      showOrderDetail.value = false
      selectedOrder.value = null
      orderDetail.value = null
    }

    const printOrder = (orden) => {
      // Si no tenemos el detalle cargado, lo cargamos primero
      if (!orderDetail.value || orderDetail.value.id !== orden.id) {
        viewOrder(orden).then(() => {
          setTimeout(() => {
            window.print()
          }, 500)
        })
      } else {
        window.print()
      }
    }

    const getStatusLabel = (status) => {
      const labels = {
        'PENDIENTE': 'Pendiente',
        'CONFIRMADA': 'Confirmada',
        'EN_PROCESO': 'En Proceso',
        'ENVIADA': 'Enviada',
        'COMPLETADA': 'Completada',
        'CANCELADA': 'Cancelada',
        'BORRADOR': 'Borrador'
      }
      return labels[status] || status
    }

    onMounted(() => {
      cargarOrdenes()
    })

    return {
      searchQuery,
      filterStatus,
      filterDate,
      loading,
      orderStats,
      ordenes,
      filteredOrders,
      showOrderDetail,
      loadingDetail,
      selectedOrder,
      orderDetail,
      formatNumber,
      getStatusClass,
      getStatusLabel,
      clearFilters,
      updateOrderStatus,
      viewOrder,
      closeOrderDetail,
      printOrder,
      cargarOrdenes,
      formatearFecha
    }
  }
}
</script>

<style scoped>
@media print {
  /* Ocultar todo */
  body * {
    visibility: hidden;
  }
  
  /* Mostrar solo el área de impresión */
  #printArea,
  #printArea * {
    visibility: visible;
  }
  
  #printArea {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
  }
  
  /* Asegurar que se muestre */
  .print\:block {
    display: block !important;
  }
  
  /* Ocultar elementos innecesarios */
  .no-print {
    display: none !important;
  }
  
  /* Ajustes de página */
  @page {
    size: A4;
    margin: 1cm;
  }
}

/* Animación del modal */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
