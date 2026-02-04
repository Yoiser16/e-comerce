<template>
  <div class="ordenes-layout transition-colors duration-300">
    <!-- ========== MASTER LIST (Panel Izquierdo) ========== -->
    <aside class="master-list">
      <!-- Header del sidebar -->
      <div class="master-header">
        <h2 class="master-title">Órdenes</h2>
        <span class="master-count">{{ ordenes.length }}</span>
      </div>

      <!-- Búsqueda -->
      <div class="master-search">
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Buscar orden o cliente..."
          class="search-input"
        />
      </div>

      <!-- Filtros compactos -->
      <div class="master-filters">
        <button 
          v-for="filter in filters" 
          :key="filter.key"
          @click="activeFilter = filter.key"
          :class="['filter-chip', { active: activeFilter === filter.key }]"
        >
          {{ filter.label }}
          <span class="chip-count">{{ filter.count }}</span>
        </button>
      </div>

      <!-- Lista scrolleable de órdenes -->
      <div class="master-scroll">
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
        </div>
        
        <template v-else>
          <div 
            v-for="orden in filteredOrdenes" 
            :key="orden.id"
            @click="selectOrder(orden)"
            :class="['order-card', { 'order-card--active': selectedOrder?.id === orden.id, 'order-card--unseen': !isOrderSeen(orden.id) }]"
          >
            <!-- Indicador de no visto: Barra vertical magenta/verde -->
            <div v-if="!isOrderSeen(orden.id)" :class="['order-card__indicator', orden.estado_pago === 'PAGADO' ? 'order-card__indicator--paid' : 'order-card__indicator--new']"></div>
            <!-- Línea 1: ID + Hora -->
            <div class="order-card__row1">
              <span :class="['order-card__id', { 'order-card__id--bold': !isOrderSeen(orden.id) }]">{{ orden.codigo }}</span>
              <span class="order-card__time">{{ formatTimeAgo(orden.fecha_creacion) }}</span>
            </div>
            <!-- Línea 2: Cliente + Total -->
            <div class="order-card__row2">
              <span :class="['order-card__client', { 'order-card__client--bold': !isOrderSeen(orden.id) }]">{{ orden.cliente_nombre }}</span>
              <span class="order-card__total">${{ formatNumber(orden.total) }}</span>
            </div>
            <!-- Línea 3: Badge + Método pago -->
            <div class="order-card__row3">
              <span :class="['order-card__badge', getBadgeClass(orden.estado_pago)]">
                {{ formatStatus(orden.estado_pago) }}
              </span>
              <span class="order-card__method">
                <svg v-if="orden.metodo_pago === 'whatsapp'" class="method-icon" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                </svg>
                <svg v-else class="method-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                </svg>
              </span>
            </div>
          </div>
        </template>
        
        <div v-if="!loading && filteredOrdenes.length === 0" class="empty-list">
          <svg class="empty-list__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <span>Sin resultados</span>
        </div>
      </div>
    </aside>

    <!-- ========== DETAIL VIEW (Panel Derecho) ========== -->
    <main class="detail-view">
      <!-- Empty State -->
      <div v-if="!selectedOrder" class="detail-empty">
        <svg class="detail-empty__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        </svg>
        <p class="detail-empty__text">Selecciona una orden para ver los detalles</p>
      </div>

      <!-- Order Detail Content -->
      <div v-else class="detail-content">
        <!-- Sticky Header -->
        <header class="detail-header">
          <div class="detail-header__left">
            <h1 class="detail-header__title">{{ selectedOrder.codigo }}</h1>
            <span class="detail-header__date">{{ formatDate(selectedOrder.fecha_creacion) }}</span>
          </div>
          <div class="detail-header__actions">
            <button @click="printOrder" class="action-btn" title="Imprimir">
              <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
              </svg>
            </button>
            <button @click="openWhatsApp" class="action-btn action-btn--whatsapp" title="WhatsApp">
              <svg class="action-icon" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
              </svg>
            </button>
            <button class="action-btn" title="Editar">
              <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </button>
          </div>
        </header>

        <!-- Scrollable Detail Body -->
        <div class="detail-body">
          <!-- BENTO GRID: 3 Columnas -->
          <div class="bento-grid">
            <!-- Caja 1: Cliente -->
            <div class="bento-box">
              <div class="bento-box__header">
                <svg class="bento-box__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                <span class="bento-box__label">Cliente</span>
              </div>
              <div class="bento-box__content">
                <div class="client-info">
                  <div class="client-avatar">
                    {{ getInitials(orderDetail?.cliente_nombre || selectedOrder.cliente_nombre) }}
                  </div>
                  <div class="client-details">
                    <span class="client-name">{{ orderDetail?.cliente_nombre || selectedOrder.cliente_nombre }}</span>
                    <a :href="'tel:' + (orderDetail?.cliente_telefono || selectedOrder.cliente_telefono)" class="client-phone">
                      {{ orderDetail?.cliente_telefono || selectedOrder.cliente_telefono }}
                    </a>
                    <span class="client-email">{{ orderDetail?.cliente_email || selectedOrder.cliente_email }}</span>
                    <span v-if="(orderDetail?.cliente_num_doc || selectedOrder.cliente_num_doc)" class="client-doc">
                      <svg class="inline w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"/>
                      </svg>
                      {{ orderDetail?.cliente_tipo_doc || selectedOrder.cliente_tipo_doc || 'CC' }}: {{ orderDetail?.cliente_num_doc || selectedOrder.cliente_num_doc }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Caja 2: Envío -->
            <div class="bento-box !bg-white">
              <div class="bento-box__header">
                <svg class="bento-box__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <span class="bento-box__label">Envío</span>
              </div>
              <div class="bento-box__content">
                <div class="address-info">
                  <p class="address-line">{{ orderDetail?.direccion_envio || '-' }}</p>
                  <p class="address-city">{{ orderDetail?.barrio ? orderDetail.barrio + ', ' : '' }}{{ orderDetail?.municipio }}</p>
                  <p class="address-dept">{{ orderDetail?.departamento }}</p>
                </div>
                <div class="shipping-status">
                  <label class="compact-label">Estado</label>
                  <select 
                    v-model="selectedOrder.estado_envio" 
                    @change="updateEstadoEnvio"
                    :disabled="selectedOrder.estado_pago !== 'PAGADO'"
                    :class="['compact-select', getShippingClass(selectedOrder.estado_envio)]"
                  >
                    <option value="NO_ENVIADO">No Enviado</option>
                    <option value="ENVIADO">Enviado</option>
                    <option value="ENTREGADO">Entregado</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Caja 3: Pago -->
            <div class="bento-box !bg-white">
              <div class="bento-box__header">
                <svg class="bento-box__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                </svg>
                <span class="bento-box__label">Pago</span>
              </div>
              <div class="bento-box__content">
                <!-- Loading overlay para cambios de estado -->
                <div v-if="loadingEstadoChange" class="absolute inset-0 bg-white/80 backdrop-blur-sm z-20 flex items-center justify-center rounded-xl">
                  <div class="flex flex-col items-center gap-3">
                    <div class="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin"></div>
                    <p class="text-sm text-text-dark font-medium">Actualizando estado...</p>
                  </div>
                </div>
                
                <div class="payment-status">
                  <label class="compact-label">Estado</label>
                  <select 
                    v-model="selectedOrder.estado_pago" 
                    @change="updateEstadoPago"
                    :disabled="selectedOrder.estado_pago === 'PAGADO'"
                    :class="['compact-select', getStatusClass(selectedOrder.estado_pago)]"
                    :title="selectedOrder.estado_pago === 'PAGADO' ? 'No se puede cambiar el estado de una orden ya pagada' : ''"
                  >
                    <option value="PENDIENTE">Pendiente</option>
                    <option value="PAGADO">Pagado</option>
                    <option value="CANCELADO">Cancelado</option>
                  </select>
                  <p v-if="selectedOrder.estado_pago === 'PAGADO'" class="text-xs text-emerald-600 mt-1">
                    ✓ Orden confirmada - Stock descontado
                  </p>
                </div>
                <div class="payment-details">
                  <div class="payment-row">
                    <span class="payment-label">Método</span>
                    <span class="payment-value">{{ formatPaymentMethod(selectedOrder.metodo_pago) }}</span>
                  </div>
                  <div v-if="orderDetail?.referencia_pago" class="payment-row">
                    <span class="payment-label">Referencia</span>
                    <span class="payment-value payment-value--mono">{{ orderDetail.referencia_pago }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tabla de Productos (Estilo Factura) -->
          <div class="invoice-section">
            <div class="invoice-header">
              <span class="invoice-title">Productos</span>
              <span class="invoice-count">{{ orderDetail?.items?.length || 0 }} items</span>
            </div>
            <table class="invoice-table">
              <thead>
                <tr>
                  <th class="col-product">Producto</th>
                  <th class="col-qty">Cant.</th>
                  <th class="col-price">Precio</th>
                  <th class="col-subtotal">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in orderDetail?.items" :key="idx" class="invoice-row">
                  <td class="col-product">
                    <div class="product-cell">
                      <div class="product-thumb">
                        <img v-if="item.imagen" :src="item.imagen" :alt="item.nombre" />
                        <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                        </svg>
                      </div>
                      <span class="product-name">{{ item.nombre }}</span>
                    </div>
                  </td>
                  <td class="col-qty">{{ item.cantidad }}</td>
                  <td class="col-price">${{ formatNumber(item.precio_unitario) }}</td>
                  <td class="col-subtotal">${{ formatNumber(item.subtotal) }}</td>
                </tr>
                <tr v-if="!orderDetail?.items?.length">
                  <td colspan="4" class="empty-row">Sin productos</td>
                </tr>
              </tbody>
            </table>

            <!-- Totales alineados a la derecha -->
            <div class="invoice-totals">
              <div class="totals-row">
                <span class="totals-label">Subtotal</span>
                <span class="totals-value">${{ formatNumber(orderDetail?.subtotal_monto || 0) }}</span>
              </div>
              <div class="totals-row">
                <span class="totals-label">Envío</span>
                <span class="totals-value">${{ formatNumber(orderDetail?.envio_monto || 0) }}</span>
              </div>
              <div class="totals-row totals-row--final">
                <span class="totals-label">Total</span>
                <span class="totals-value">${{ formatNumber(orderDetail?.total || selectedOrder.total) }}</span>
              </div>
            </div>
          </div>

          <!-- Notas si existen -->
          <div v-if="orderDetail?.notas_envio" class="notes-box">
            <svg class="notes-icon" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
            <div class="notes-content">
              <span class="notes-label">NOTAS DEL CLIENTE</span>
              <p class="notes-text">{{ orderDetail.notas_envio }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de Mensajes -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
          <div class="modal-container" :class="modalType">
            <!-- Icono -->
            <div class="modal-icon">
              <svg v-if="modalType === 'success'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              <svg v-else-if="modalType === 'error'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
            </div>
            
            <!-- Contenido -->
            <h3 class="modal-title">{{ modalTitle }}</h3>
            <p class="modal-message">{{ modalMessage }}</p>
            
            <!-- Botón -->
            <button @click="handleModalAction" class="modal-btn" :class="modalType">
              {{ modalButtonText }}
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Modal de Confirmación (evita alert/confirm del navegador) -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="confirmState.open" class="modal-overlay" @click.self="cancelConfirm">
          <div class="modal-container warning">
            <div class="modal-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
            </div>
            <h3 class="modal-title">{{ confirmState.title }}</h3>
            <p class="modal-message whitespace-pre-line">{{ confirmState.message }}</p>
            <div class="confirm-actions">
              <button class="modal-btn ghost" @click="cancelConfirm">{{ confirmState.cancelText || 'Cancelar' }}</button>
              <button class="modal-btn warning" @click="acceptConfirm">{{ confirmState.confirmText || 'Aceptar' }}</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ordenesService } from '@/services/ordenes'

const router = useRouter()

// Estado
const ordenes = ref([])
const selectedOrder = ref(null)
const orderDetail = ref(null)
const loading = ref(true)
const loadingDetail = ref(false)
const loadingEstadoChange = ref(false) // Loading para cambios de estado
const searchQuery = ref('')
const activeFilter = ref('todas')
const pollingInterval = ref(null)
const lastOrderCount = ref(0)

// Modal de mensajes
const showModal = ref(false)
const modalType = ref('success') // success, error, warning
const modalTitle = ref('')
const modalMessage = ref('')
const modalButtonText = ref('Aceptar')
const modalAction = ref(null) // Acción al cerrar (ej: redirigir a login)

// Modal de confirmación
const confirmState = ref({
  open: false,
  title: '',
  message: '',
  confirmText: 'Aceptar',
  cancelText: 'Cancelar'
})
let confirmResolver = null

const openModal = (type, title, message, buttonText = 'Aceptar', action = null) => {
  modalType.value = type
  modalTitle.value = title
  modalMessage.value = message
  modalButtonText.value = buttonText
  modalAction.value = action
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const handleModalAction = () => {
  closeModal()
  if (modalAction.value) {
    modalAction.value()
  }
}

// Abrir modal de confirmación y esperar respuesta
const askConfirm = ({ title, message, confirmText = 'Aceptar', cancelText = 'Cancelar' }) => {
  return new Promise((resolve) => {
    confirmResolver = resolve
    confirmState.value = {
      open: true,
      title,
      message,
      confirmText,
      cancelText
    }
  })
}

const acceptConfirm = () => {
  confirmState.value.open = false
  if (confirmResolver) confirmResolver(true)
  confirmResolver = null
}

const cancelConfirm = () => {
  confirmState.value.open = false
  if (confirmResolver) confirmResolver(false)
  confirmResolver = null
}

// Función para reproducir sonido de caja registradora usando Web Audio API
const playNotificationSound = () => {
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    // Función helper para crear tonos
    const playTone = (frequency, startTime, duration, volume = 0.3) => {
      const oscillator = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      
      oscillator.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      oscillator.frequency.value = frequency
      oscillator.type = 'sine'
      
      gainNode.gain.setValueAtTime(volume, audioContext.currentTime + startTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + startTime + duration)
      
      oscillator.start(audioContext.currentTime + startTime)
      oscillator.stop(audioContext.currentTime + startTime + duration)
    }
    
    // Secuencia de notas: "CHA-CHING!" 🔔💰
    // Primera parte: "CHA" (campana alta)
    playTone(1200, 0, 0.08, 0.4)
    playTone(1600, 0.03, 0.08, 0.3)
    
    // Segunda parte: "CHING" (más agudo y resonante)
    playTone(2000, 0.15, 0.15, 0.35)
    playTone(2400, 0.18, 0.15, 0.25)
    playTone(2800, 0.21, 0.2, 0.2)
    
    // Nota grave de fondo (simula mecanismo de caja)
    playTone(200, 0, 0.1, 0.15)
    
  } catch (error) {
    console.log('No se pudo reproducir el sonido:', error)
  }
}

// Filtros
const filters = computed(() => [
  { key: 'todas', label: 'Todas', count: ordenes.value.length },
  { key: 'pendientes', label: 'Pendientes', count: ordenes.value.filter(o => o.estado_pago === 'PENDIENTE').length },
  { key: 'pagados', label: 'Pagados', count: ordenes.value.filter(o => o.estado_pago === 'PAGADO').length },
  { key: 'enviados', label: 'Enviados', count: ordenes.value.filter(o => o.estado_envio === 'ENVIADO' || o.estado_envio === 'ENTREGADO').length }
])

// Órdenes filtradas
const filteredOrdenes = computed(() => {
  let result = ordenes.value

  // Filtro por estado
  if (activeFilter.value === 'pendientes') {
    result = result.filter(o => o.estado_pago === 'PENDIENTE')
  } else if (activeFilter.value === 'pagados') {
    result = result.filter(o => o.estado_pago === 'PAGADO')
  } else if (activeFilter.value === 'enviados') {
    result = result.filter(o => o.estado_envio === 'ENVIADO' || o.estado_envio === 'ENTREGADO')
  }

  // Búsqueda
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(o => 
      o.codigo.toLowerCase().includes(q) ||
      o.cliente_nombre.toLowerCase().includes(q) ||
      o.cliente_email.toLowerCase().includes(q)
    )
  }

  return result
})

// Mapear estados
const mapEstadoPago = (estado) => {
  const e = estado?.toString().toUpperCase() || 'PENDIENTE'
  const map = {
    'PENDIENTE': 'PENDIENTE',
    'CONFIRMADA': 'PAGADO',
    'PAGADA': 'PAGADO',
    'PAGADO': 'PAGADO',
    'CANCELADA': 'CANCELADO',
    'CANCELADO': 'CANCELADO'
  }
  return map[e] || 'PENDIENTE'
}

const mapEstadoEnvio = (estado) => {
  const e = estado?.toString().toUpperCase() || 'NO_ENVIADO'
  const map = {
    'ENVIADA': 'ENVIADO',
    'ENVIADO': 'ENVIADO',
    'ENTREGADA': 'ENTREGADO',
    'ENTREGADO': 'ENTREGADO'
  }
  return map[e] || 'NO_ENVIADO'
}

// Cargar órdenes - Versión optimizada con items incluidos
const cargarOrdenes = async (silent = false) => {
  try {
    if (!silent) loading.value = true
    // Cargar con items incluidos para evitar segunda llamada
    const data = await ordenesService.obtenerTodas(true)
    
    const nuevasOrdenes = data.map(orden => ({
      id: orden.id,
      codigo: orden.codigo,
      cliente_nombre: orden.cliente_nombre || 'Sin cliente',
      cliente_email: orden.cliente_email || '',
      cliente_telefono: orden.cliente_telefono || '',
      cliente_tipo_doc: orden.cliente_tipo_doc || '',
      cliente_num_doc: orden.cliente_num_doc || '',
      total_items: orden.total_items || 0,
      total: orden.total || 0,
      subtotal_monto: orden.subtotal_monto || 0,
      envio_monto: orden.envio_monto || 0,
      direccion_envio: orden.direccion_envio || '',
      departamento: orden.departamento || '',
      municipio: orden.municipio || '',
      barrio: orden.barrio || '',
      notas_envio: orden.notas_envio || '',
      estado_pago: mapEstadoPago(orden.estado),
      estado_envio: mapEstadoEnvio(orden.estado),
      metodo_pago: orden.metodo_pago || 'whatsapp',
      fecha_creacion: orden.fecha_creacion,
      // Guardar items pre-cargados
      items: orden.items || null
    })).sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion))
    
    // Detectar nuevas órdenes y reproducir sonido
    if (silent && ordenes.value.length > 0 && nuevasOrdenes.length > ordenes.value.length) {
      const cantidadNuevas = nuevasOrdenes.length - ordenes.value.length
      console.log(`🔔 ${cantidadNuevas} nueva(s) orden(es) detectada(s)`)
      
      // Reproducir sonido de notificación
      playNotificationSound()
      
      // Mostrar notificación del navegador si está permitido
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Nueva Orden Recibida', {
          body: `${cantidadNuevas} nueva(s) orden(es) pendiente(s)`,
          icon: '/favicon.ico',
          tag: 'nueva-orden'
        })
      }
    }
    
    ordenes.value = nuevasOrdenes
  } catch (error) {
    console.error('Error al cargar órdenes:', error)
    if (!silent) ordenes.value = []
  } finally {
    if (!silent) loading.value = false
  }
}

// Iniciar polling automático
const startPolling = () => {
  // Actualizar cada 5 segundos
  pollingInterval.value = setInterval(() => {
    cargarOrdenes(true) // true = silent mode (sin mostrar loading)
  }, 5000)
}

// Detener polling
const stopPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
}

// Sistema de órdenes vistas
const getSeenOrders = () => {
  try {
    return JSON.parse(localStorage.getItem('seenOrders') || '[]')
  } catch {
    return []
  }
}

const markOrderAsSeen = (orderId) => {
  const seen = getSeenOrders()
  if (!seen.includes(orderId)) {
    seen.push(orderId)
    localStorage.setItem('seenOrders', JSON.stringify(seen))
    // Emitir evento para actualizar el sidebar
    window.dispatchEvent(new CustomEvent('ordenes-updated'))
  }
}

const isOrderSeen = (orderId) => {
  return getSeenOrders().includes(orderId)
}

const getUnseenCount = () => {
  const seen = getSeenOrders()
  return ordenes.value.filter(o => !seen.includes(o.id)).length
}

// Seleccionar orden - Versión optimizada usando datos pre-cargados
const selectOrder = async (orden) => {
  selectedOrder.value = { ...orden }
  // Guardar estados originales para detectar cambios
  selectedOrder.value._estadoOriginal = orden.estado_pago
  selectedOrder.value._estadoEnvioOriginal = orden.estado_envio
  
  // Marcar como vista
  markOrderAsSeen(orden.id)
  
  // Usar datos pre-cargados si están disponibles (optimización)
  if (orden.items && orden.items.length > 0) {
    // Los datos ya vienen del listado optimizado
    orderDetail.value = {
      id: orden.id,
      codigo: orden.codigo,
      estado: orden.estado_pago,
      cliente_nombre: orden.cliente_nombre,
      cliente_email: orden.cliente_email,
      cliente_telefono: orden.cliente_telefono,
      cliente_tipo_doc: orden.cliente_tipo_doc || '',
      cliente_num_doc: orden.cliente_num_doc || '',
      direccion_envio: orden.direccion_envio || '',
      departamento: orden.departamento || '',
      municipio: orden.municipio || '',
      barrio: orden.barrio || '',
      notas_envio: orden.notas_envio || '',
      subtotal_monto: orden.subtotal_monto || 0,
      envio_monto: orden.envio_monto || 0,
      total: orden.total || 0,
      metodo_pago: orden.metodo_pago || 'whatsapp',
      items: orden.items,
      fecha_creacion: orden.fecha_creacion
    }
    loadingDetail.value = false
  } else {
    // Fallback: cargar desde API si no hay items pre-cargados
    orderDetail.value = null
    try {
      loadingDetail.value = true
      const detail = await ordenesService.obtenerPorId(orden.id)
      orderDetail.value = detail
    } catch (error) {
      console.error('Error:', error)
    } finally {
      loadingDetail.value = false
    }
  }
}

// Actualizar estados
const updateEstadoPago = async () => {
  if (!selectedOrder.value) return
  
  const nuevoEstado = selectedOrder.value.estado_pago
  const estadoAnterior = selectedOrder.value._estadoOriginal || selectedOrder.value.estado_pago
  
  // Si no hay cambio real, no hacer nada
  if (nuevoEstado === estadoAnterior) return
  
  // Mensajes de confirmación según el cambio
  let mensaje = ''
  let titulo = 'Confirmar'
  if (nuevoEstado === 'PAGADO') {
    titulo = 'Confirmar pago'
    mensaje = '⚠️ ¿Confirmar que el pago fue recibido?\n\nEsto descontará el stock del inventario de forma permanente.'
  } else if (nuevoEstado === 'CANCELADO') {
    titulo = 'Cancelar orden'
    mensaje = '¿Está seguro de CANCELAR esta orden?\n\nEsta acción no se puede deshacer.'
  } else {
    mensaje = `¿Cambiar el estado de pago a "${nuevoEstado}"?`
  }
  
  const confirmado = await askConfirm({
    title: titulo,
    message: mensaje,
    confirmText: nuevoEstado === 'PAGADO' ? 'Confirmar pago' : 'Aceptar',
    cancelText: 'Cancelar'
  })
  
  if (!confirmado) {
    // Restaurar estado anterior si cancela
    selectedOrder.value.estado_pago = estadoAnterior
    return
  }
  
  // Activar loading
  loadingEstadoChange.value = true
  
  try {
    // CRÍTICO: Si cambiamos a PAGADO, debemos confirmar la orden para descontar stock
    if (nuevoEstado === 'PAGADO') {
      // Validar que la orden tenga productos antes de confirmar
      if (!orderDetail.value?.items || orderDetail.value.items.length === 0) {
        openModal('error', 'Sin productos', 'No se puede confirmar una orden sin productos. Agrega productos a la orden primero.')
        selectedOrder.value.estado_pago = estadoAnterior
        return
      }
      
      // Llamar al endpoint de confirmación que descuenta stock atómicamente
      await ordenesService.confirmar(selectedOrder.value.id)
      console.log('✅ Orden confirmada - Stock descontado')
    } else {
      // Para otros estados (PENDIENTE, CANCELADO), solo actualizar estado
      const estadoMap = { 'PENDIENTE': 'pendiente', 'CANCELADO': 'cancelada' }
      await ordenesService.actualizarEstado(selectedOrder.value.id, estadoMap[nuevoEstado])
    }
    
    // Si no está pagado, resetear estado de envío
    if (nuevoEstado !== 'PAGADO') {
      selectedOrder.value.estado_envio = 'NO_ENVIADO'
    }
    
    // Guardar el nuevo estado como original
    selectedOrder.value._estadoOriginal = nuevoEstado
    
    // Actualizar en la lista local
    const idx = ordenes.value.findIndex(o => o.id === selectedOrder.value.id)
    if (idx !== -1) {
      ordenes.value[idx].estado_pago = selectedOrder.value.estado_pago
      ordenes.value[idx].estado_envio = selectedOrder.value.estado_envio
      ordenes.value[idx]._estadoOriginal = nuevoEstado
    }
    
    openModal('success', '¡Listo!', 'Estado actualizado correctamente')
  } catch (error) {
    console.error('Error al actualizar estado de pago:', error)
    
    // Detectar si es error de sesión expirada
    if (error.response?.status === 401 || error.message?.includes('401') || error.message?.includes('lista negra') || error.message?.includes('token')) {
      openModal('error', 'Sesión expirada', 'Tu sesión ha expirado. Por favor inicia sesión nuevamente.', 'Ir al Login', () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
      })
      return
    }
    
    // Mensajes de error más específicos
    let errorMsg = error.response?.data?.detail || error.message
    
    if (errorMsg.includes('BORRADOR o PENDIENTE')) {
      errorMsg = 'Esta orden ya fue confirmada previamente. No se puede cambiar el estado de una orden pagada.'
    } else if (errorMsg.includes('sin líneas')) {
      errorMsg = 'No se puede confirmar una orden sin productos. Agrega productos primero.'
    } else if (errorMsg.includes('Stock insuficiente')) {
      errorMsg = 'Stock insuficiente para uno o más productos. ' + errorMsg
    }
    
    openModal('error', 'Error al confirmar', errorMsg)
    
    // Restaurar estado anterior
    selectedOrder.value.estado_pago = estadoAnterior
  } finally {
    // Desactivar loading
    loadingEstadoChange.value = false
  }
}

const updateEstadoEnvio = async () => {
  if (!selectedOrder.value || selectedOrder.value.estado_pago !== 'PAGADO') return
  
  const nuevoEstado = selectedOrder.value.estado_envio
  const estadoAnterior = selectedOrder.value._estadoEnvioOriginal || selectedOrder.value.estado_envio
  
  // Si no hay cambio real, no hacer nada
  if (nuevoEstado === estadoAnterior) return
  
  // Mensaje de confirmación
  const mensajes = {
    'NO_ENVIADO': '¿Marcar como NO ENVIADO?',
    'ENVIADO': '📦 ¿Confirmar que el pedido fue ENVIADO?',
    'ENTREGADO': '✅ ¿Confirmar que el pedido fue ENTREGADO?'
  }
  
  const confirmadoEnvio = await askConfirm({
    title: 'Actualizar envío',
    message: mensajes[nuevoEstado] || '¿Cambiar estado de envío?',
    confirmText: 'Confirmar',
    cancelText: 'Cancelar'
  })
  
  if (!confirmadoEnvio) {
    selectedOrder.value.estado_envio = estadoAnterior
    return
  }
  
  // Activar loading
  loadingEstadoChange.value = true
  
  try {
    const estadoMap = { 'NO_ENVIADO': 'confirmada', 'ENVIADO': 'enviada', 'ENTREGADO': 'entregada' }
    await ordenesService.actualizarEstado(selectedOrder.value.id, estadoMap[selectedOrder.value.estado_envio])
    
    selectedOrder.value._estadoEnvioOriginal = nuevoEstado
    
    const idx = ordenes.value.findIndex(o => o.id === selectedOrder.value.id)
    if (idx !== -1) {
      ordenes.value[idx].estado_envio = selectedOrder.value.estado_envio
      ordenes.value[idx]._estadoEnvioOriginal = nuevoEstado
    }
    
    openModal('success', '¡Listo!', 'Estado de envío actualizado')
  } catch (error) {
    console.error('Error:', error)
    
    // Detectar sesión expirada
    if (error.response?.status === 401) {
      openModal('error', 'Sesión expirada', 'Tu sesión ha expirado. Por favor inicia sesión nuevamente.', 'Ir al Login', () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
      })
      return
    }
    
    openModal('error', 'Error', 'No se pudo actualizar el estado de envío')
    selectedOrder.value.estado_envio = estadoAnterior
  } finally {
    // Desactivar loading
    loadingEstadoChange.value = false
  }
}

// Clases de estado
const getStatusClass = (status) => {
  const classes = {
    'PENDIENTE': 'status-pending',
    'PAGADO': 'status-paid',
    'CANCELADO': 'status-cancelled'
  }
  return classes[status] || 'status-pending'
}

const getBadgeClass = (status) => {
  const classes = {
    'PENDIENTE': 'badge--pending',
    'PAGADO': 'badge--paid',
    'CANCELADO': 'badge--cancelled'
  }
  return classes[status] || 'badge--pending'
}

const formatStatus = (status) => {
  const labels = {
    'PENDIENTE': 'Pendiente',
    'PAGADO': 'Pagado',
    'CANCELADO': 'Cancelado'
  }
  return labels[status] || status
}

// --- Comentarios de estilo para el modal de confirmación ---
// .confirm-actions usa layout horizontal con gap para botones

const getShippingClass = (status) => {
  const classes = {
    'NO_ENVIADO': 'shipping-pending',
    'ENVIADO': 'shipping-sent',
    'ENTREGADO': 'shipping-delivered'
  }
  return classes[status] || 'shipping-pending'
}

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

const formatPaymentMethod = (method) => {
  const methods = {
    'whatsapp': 'WhatsApp',
    'transferencia': 'Transferencia',
    'efectivo': 'Efectivo',
    'tarjeta': 'Tarjeta'
  }
  return methods[method?.toLowerCase()] || method || 'WhatsApp'
}

// Formateo
const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO').format(num || 0)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CO', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatTimeAgo = (date) => {
  const now = new Date()
  const d = new Date(date)
  const diff = Math.floor((now - d) / 1000)
  
  if (diff < 60) return 'ahora'
  if (diff < 3600) return `${Math.floor(diff / 60)}m`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`
  return `${Math.floor(diff / 86400)}d`
}

// Acciones
const printOrder = () => {
  window.print()
}

const openWhatsApp = () => {
  if (!selectedOrder.value) return
  const phone = selectedOrder.value.cliente_telefono?.replace(/\D/g, '') || '573217355070'
  const msg = `Hola, sobre tu pedido ${selectedOrder.value.codigo}`
  window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, '_blank')
}

onMounted(() => {
  cargarOrdenes()
  startPolling()
  
  // Solicitar permiso para notificaciones
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission()
  }
})

// Limpiar al desmontar
onUnmounted(() => {
  stopPolling()
})

// Exponer función para el sidebar
defineExpose({ getUnseenCount })
</script>

<style scoped>
/* ========================================
   LAYOUT MASTER-DETAIL PROFESIONAL
   Estilo: Productivity Dashboard
   ======================================== */

.ordenes-layout {
  display: flex;
  height: calc(100vh - 48px);
  margin: -24px -40px;
  /* background managed by utility classes */
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ========== MASTER LIST (Panel Izquierdo) ========== */
.master-list {
  width: 380px;
  min-width: 380px;
  /* background managed by utility classes */
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.master-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 20px 16px;
}

.master-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0;
  letter-spacing: -0.01em;
}

.master-count {
  background: #111827;
  color: #ffffff;
  font-size: 11px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 12px;
}

/* Search */
.master-search {
  position: relative;
  padding: 0 20px 12px;
}

.search-icon {
  position: absolute;
  left: 32px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #9ca3af;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 40px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  color: #111827;
  background: #f9fafb;
  outline: none;
  transition: all 0.15s ease;
}

.search-input:focus {
  border-color: #111827;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.05);
}

.search-input::placeholder {
  color: #9ca3af;
}

/* Filter Chips */
.master-filters {
  display: flex;
  gap: 6px;
  padding: 0 20px 16px;
  flex-wrap: wrap;
}

.filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f3f4f6;
  border: 1px solid transparent;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.filter-chip:hover {
  background: #e5e7eb;
  color: #374151;
}

.filter-chip.active {
  background: #111827;
  color: #ffffff;
  border-color: #111827;
}

.chip-count {
  font-size: 10px;
  opacity: 0.7;
}

/* Master Scroll */
.master-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 0 12px 12px;
}

/* Order Cards */
.order-card {
  position: relative;
  padding: 14px 16px;
  padding-left: 20px;
  margin-bottom: 2px;
  /* background managed by utility classes */
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: all 0.15s ease;
}

.order-card:hover {
  background: #fafafa;
}

.order-card--active {
  background: #F9FAFB;
  border-left: 3px solid #111827;
  padding-left: 17px;
}

/* Indicador de orden no leída: Barra vertical */
.order-card__indicator {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  border-radius: 0 2px 2px 0;
}

.order-card__indicator--new {
  background: #D81B60;
}

.order-card__indicator--paid {
  background: #10b981;
}

.order-card__row1 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.order-card__id {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  letter-spacing: -0.01em;
}

.order-card__id--bold {
  font-weight: 700;
}

.order-card__time {
  font-size: 11px;
  color: #9ca3af;
  font-weight: 500;
}

.order-card__row2 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.order-card__client {
  font-size: 14px;
  color: #6b7280;
  max-width: 180px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.order-card__client--bold {
  font-weight: 600;
  color: #111827;
}

.order-card__total {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.order-card__row3 {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-card__badge {
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.badge--pending {
  background: #fef3c7;
  color: #92400e;
}

.badge--paid {
  background: #dcfce7;
  color: #166534;
}

.badge--cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.order-card__method {
  display: flex;
  align-items: center;
}

.method-icon {
  width: 16px;
  height: 16px;
  color: #9ca3af;
}

/* Empty List */
.empty-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #9ca3af;
  text-align: center;
}

.empty-list__icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

/* Loading */
.loading-state {
  display: flex;
  justify-content: center;
  padding: 60px;
}

.spinner {
  width: 28px;
  height: 28px;
  border: 2px solid #e5e7eb;
  border-top-color: #111827;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========== DETAIL VIEW (Panel Derecho) ========== */
.detail-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  /* background managed by utility classes */
}

/* Empty State */
.detail-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

.detail-empty__icon {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
  opacity: 0.4;
}

.detail-empty__text {
  font-size: 14px;
  color: #6b7280;
}

/* Detail Content */
.detail-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Detail Header (Sticky) */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  /* background managed by utility classes */
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 10;
}

.detail-header__left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.detail-header__title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.03em;
}

.detail-header__date {
  font-size: 14px;
  color: #9ca3af;
  font-weight: 500;
}

.detail-header__actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
  background: transparent;
  border: none;
  color: #6b7280;
}

.action-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.action-btn--whatsapp {
  background: #25d366;
  color: #ffffff;
}

.action-btn--whatsapp:hover {
  background: #1fb855;
}

.action-icon {
  width: 18px;
  height: 18px;
}

/* Detail Body */
.detail-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ========== BENTO GRID ========== */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 12px;
}

@media (min-width: 640px) {
  .bento-grid {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 16px;
  }
}

@media (min-width: 1024px) {
  .bento-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
}

.bento-box {
  /* background managed by utility classes */
  border: none;
  border-radius: 16px;
  overflow: hidden;
}

.bento-box__header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 16px;
  background: transparent;
  border-bottom: none;
}

.bento-box__icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

.bento-box__label {
  font-size: 10px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.bento-box__content {
  padding: 16px;
}

/* Client Info */
.client-info {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.client-avatar {
  width: 44px;
  height: 44px;
  min-width: 44px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 0.02em;
}

.client-details {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.client-name {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.client-phone {
  font-size: 14px;
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.client-phone:hover {
  text-decoration: underline;
}

.client-email {
  font-size: 13px;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.client-doc {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  display: flex;
  align-items: center;
  margin-top: 2px;
  padding: 4px 8px;
  background: #f3f4f6;
  border-radius: 6px;
  width: fit-content;
}

/* Address Info */
.address-info {
  margin-bottom: 14px;
}

.address-line {
  font-size: 15px;
  font-weight: 500;
  color: #111827;
  margin: 0 0 4px;
}

.address-city {
  font-size: 14px;
  color: #4b5563;
  margin: 0 0 2px;
}

.address-dept {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
}

/* Shipping Status */
.shipping-status,
.payment-status {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}

.compact-label {
  font-size: 10px;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.compact-select {
  padding: 8px 32px 8px 12px;
  border: 1px solid transparent;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #111827;
  /* background managed by utility classes */
  outline: none;
  cursor: pointer;
  transition: all 0.15s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='10' height='6' viewBox='0 0 10 6' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1L5 5L9 1' stroke='%236b7280' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
}

.compact-select:hover {
  border-color: #e5e7eb;
}

.compact-select:disabled {
  background: #f9fafb;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Select States - Estilo Badge */
.compact-select.status-pending { 
  background: #fef3c7; 
  color: #92400e; 
  border-color: transparent;
}
.compact-select.status-paid { 
  background: #dcfce7; 
  color: #166534; 
  border-color: transparent;
}
.compact-select.status-cancelled { 
  background: #fee2e2; 
  color: #991b1b; 
  border-color: transparent;
}
.compact-select.shipping-pending { 
  background: #f3f4f6; 
  color: #4b5563;
}
.compact-select.shipping-sent { 
  background: #dbeafe; 
  color: #1e40af;
}
.compact-select.shipping-delivered { 
  background: #dcfce7; 
  color: #166534;
}

/* Payment Details */
.payment-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.payment-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.payment-label {
  font-size: 12px;
  color: #6b7280;
}

.payment-value {
  font-size: 13px;
  font-weight: 500;
  color: #111827;
}

.payment-value--mono {
  font-family: 'SF Mono', 'Monaco', monospace;
  font-size: 12px;
  color: #6b7280;
}

/* ========== INVOICE TABLE ========== */
.invoice-section {
  /* background managed by utility classes */
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.invoice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  background: #f9fafb;
  border-bottom: 1px solid #f3f4f6;
}

.invoice-title {
  font-size: 12px;
  font-weight: 600;
  color: #111827;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.invoice-count {
  font-size: 12px;
  color: #6b7280;
}

.invoice-table {
  width: 100%;
  border-collapse: collapse;
}

.invoice-table thead tr {
  background: #fafafa;
}

.invoice-table th {
  padding: 10px 20px;
  font-size: 10px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: left;
  border-bottom: 1px solid #f3f4f6;
}

.invoice-table .col-qty,
.invoice-table .col-price,
.invoice-table .col-subtotal {
  text-align: right;
  width: 100px;
}

.invoice-table .col-qty {
  width: 70px;
  text-align: center;
}

.invoice-row td {
  padding: 14px 20px;
  font-size: 14px;
  color: #111827;
  border-bottom: 1px solid #f3f4f6;
  vertical-align: middle;
}

.invoice-row:last-child td {
  border-bottom: none;
}

.invoice-row .col-qty {
  text-align: center;
  color: #6b7280;
}

.invoice-row .col-price,
.invoice-row .col-subtotal {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.invoice-row .col-subtotal {
  font-weight: 600;
}

/* Product Cell */
.product-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.product-thumb {
  width: 44px;
  height: 44px;
  min-width: 44px;
  background: #f3f4f6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.product-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-thumb svg {
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.product-name {
  font-weight: 500;
}

.empty-row {
  text-align: center;
  color: #d1d5db;
  font-style: normal;
  font-size: 13px;
  padding: 32px 20px !important;
}

/* Invoice Totals */
.invoice-totals {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding: 16px 20px;
  background: #fafafa;
  border-top: 1px solid #e5e7eb;
}

.totals-row {
  display: flex;
  justify-content: space-between;
  width: 220px;
  padding: 6px 0;
}

.totals-label {
  font-size: 14px;
  color: #6b7280;
}

.totals-value {
  font-size: 14px;
  color: #111827;
  font-variant-numeric: tabular-nums;
}

.totals-row--final {
  margin-top: 10px;
  padding-top: 14px;
  border-top: 2px solid #e5e7eb;
}

.totals-row--final .totals-label {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.totals-row--final .totals-value {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.02em;
}

/* Notes Box */
.notes-box {
  display: flex;
  gap: 14px;
  padding: 16px 18px;
  background: #fefce8;
  border: 1px solid #fde047;
  border-radius: 12px;
}

.notes-icon {
  width: 18px;
  height: 18px;
  min-width: 18px;
  color: #ca8a04;
  margin-top: 2px;
}

.notes-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.notes-label {
  font-size: 10px;
  font-weight: 700;
  color: #854d0e;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.notes-text {
  font-size: 13px;
  color: #713f12;
  margin: 0;
  line-height: 1.6;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1400px) {
  .bento-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .bento-box:last-child {
    grid-column: span 2;
  }
}

@media (max-width: 1100px) {
  .master-list {
    width: 320px;
    min-width: 320px;
  }
  
  .bento-grid {
    grid-template-columns: 1fr;
  }
  
  .bento-box:last-child {
    grid-column: span 1;
  }
}

@media (max-width: 900px) {
  .master-list {
    width: 280px;
    min-width: 280px;
  }
  
  .detail-body {
    padding: 16px;
  }
  
  .detail-header {
    padding: 14px 16px;
  }
}

@media (max-width: 768px) {
  .ordenes-layout {
    flex-direction: column;
    height: auto;
    margin: 0;
  }
  
  .master-list {
    width: 100%;
    min-width: 100%;
    height: auto;
    max-height: 45vh;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .detail-view {
    flex: 1;
    min-height: 0;
  }
  
  .bento-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .detail-header__title {
    font-size: 20px;
  }

  .detail-header__actions {
    width: 100%;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .detail-body {
    padding: 12px;
  }
}

/* ========== PRINT ========== */
@media print {
  .master-list {
    display: none;
  }
  
  .detail-header__actions {
    display: none;
  }
  
  .ordenes-layout {
    height: auto;
    margin: 0;
  }
  
  .detail-body {
    padding: 0;
  }
  
  .bento-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* ========== MODAL DE MENSAJES ========== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 16px;
  padding: 32px;
  max-width: 400px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.modal-icon svg {
  width: 32px;
  height: 32px;
}

.modal-container.success .modal-icon {
  background: #dcfce7;
}

.modal-container.success .modal-icon svg {
  color: #16a34a;
}

.modal-container.error .modal-icon {
  background: #fee2e2;
}

.modal-container.error .modal-icon svg {
  color: #dc2626;
}

.modal-container.warning .modal-icon {
  background: #fef3c7;
}

.modal-container.warning .modal-icon svg {
  color: #d97706;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px;
}

.modal-message {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 24px;
  line-height: 1.6;
}

.confirm-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.modal-btn.ghost {
  background: #f3f4f6;
  color: #1f2937;
}

.modal-btn.ghost:hover {
  background: #e5e7eb;
}

.modal-btn {
  width: 100%;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-btn.success {
  background: #16a34a;
  color: white;
}

.modal-btn.success:hover {
  background: #15803d;
}

.modal-btn.error {
  background: #dc2626;
  color: white;
}

.modal-btn.error:hover {
  background: #b91c1c;
}

.modal-btn.warning {
  background: #d97706;
  color: white;
}

.modal-btn.warning:hover {
  background: #b45309;
}

/* Animaciones del modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-container,
.modal-fade-leave-active .modal-container {
  transition: transform 0.2s ease;
}

.modal-fade-enter-from .modal-container,
.modal-fade-leave-to .modal-container {
  transform: scale(0.95);
}

/* ========================================
   DARK MODE OVERRIDES (Scoped)
   Using :global(.dark) to access the root class
   ======================================== */

:global(.dark) .ordenes-layout {
  background: #0f172a; /* Slate 900 */
}

/* Master List */
:global(.dark) .master-list {
  background: #1e293b; /* Slate 800 */
  border-right-color: #334155;
}

:global(.dark) .master-title {
  color: #f1f5f9;
}

:global(.dark) .search-input {
  background: #334155;
  border-color: #475569;
  color: #f1f5f9;
}

:global(.dark) .search-input:focus {
  background: #475569;
  border-color: #94a3b8;
}

:global(.dark) .filter-chip {
  background: #334155;
  color: #94a3b8;
}

:global(.dark) .filter-chip:hover {
  background: #475569;
  color: #f1f5f9;
}

:global(.dark) .filter-chip.active {
  background: #f1f5f9;
  color: #0f172a;
}

/* Order Cards */
:global(.dark) .order-card {
  background: #1e293b;
  border-bottom-color: #334155;
}

:global(.dark) .order-card:hover {
  background: #334155;
}

:global(.dark) .order-card--active {
  background: #334155;
  border-left-color: #f1f5f9;
}

:global(.dark) .order-card__id,
:global(.dark) .order-card__total,
:global(.dark) .order-card__client--bold {
  color: #f1f5f9;
}

:global(.dark) .order-card__client {
  color: #94a3b8;
}

/* Detail View */
:global(.dark) .detail-view {
  background: #0f172a;
}

:global(.dark) .detail-header {
  background: #1e293b;
  border-bottom-color: #334155;
}

:global(.dark) .detail-header__title {
  color: #f1f5f9;
}

:global(.dark) .action-btn:hover {
  background: #334155;
  color: #f1f5f9;
}

/* Bento Boxes */
:global(.dark) .bento-box {
  background: #1e293b;
}

:global(.dark) .client-name {
  color: #f1f5f9;
}

:global(.dark) .address-line {
  color: #f1f5f9;
}

:global(.dark) .compact-select {
  background-color: #334155;
  color: #f1f5f9;
}

:global(.dark) .payment-value {
  color: #f1f5f9;
}

/* Invoice Section */
:global(.dark) .invoice-section {
  background: #1e293b;
  border-color: #334155;
}

:global(.dark) .invoice-title {
  color: #f1f5f9;
}

:global(.dark) .invoice-table th {
  color: #94a3b8;
  border-bottom-color: #334155;
}

:global(.dark) .invoice-row td {
  border-bottom-color: #334155;
}

:global(.dark) .product-name {
  color: #f1f5f9;
}

:global(.dark) .col-price, 
:global(.dark) .col-subtotal {
  color: #f1f5f9;
}

:global(.dark) .totals-label {
  color: #94a3b8;
}

:global(.dark) .totals-value {
  color: #f1f5f9;
}

:global(.dark) .notes-box {
  background: #334155;
}

:global(.dark) .notes-text {
  color: #f1f5f9;
}
</style>
