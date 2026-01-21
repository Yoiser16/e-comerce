<template>
  <div class="ordenes-layout">
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
            <!-- Indicador de no visto -->
            <div v-if="!isOrderSeen(orden.id)" class="order-card__unseen-dot"></div>
            <!-- Línea 1: ID + Hora -->
            <div class="order-card__row1">
              <span class="order-card__id">{{ orden.codigo }}</span>
              <span class="order-card__time">{{ formatTimeAgo(orden.fecha_creacion) }}</span>
            </div>
            <!-- Línea 2: Cliente + Total -->
            <div class="order-card__row2">
              <span class="order-card__client">{{ orden.cliente_nombre }}</span>
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
            <button @click="printOrder" class="action-btn action-btn--outline" title="Imprimir">
              <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
              </svg>
            </button>
            <button @click="openWhatsApp" class="action-btn action-btn--whatsapp" title="WhatsApp">
              <svg class="action-icon" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
              </svg>
            </button>
            <button class="action-btn action-btn--outline" title="Editar">
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
                    <span v-if="orderDetail?.cliente_num_doc" class="client-doc">
                      {{ orderDetail?.cliente_tipo_doc }} {{ orderDetail?.cliente_num_doc }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Caja 2: Envío -->
            <div class="bento-box">
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
            <div class="bento-box">
              <div class="bento-box__header">
                <svg class="bento-box__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                </svg>
                <span class="bento-box__label">Pago</span>
              </div>
              <div class="bento-box__content">
                <div class="payment-status">
                  <label class="compact-label">Estado</label>
                  <select 
                    v-model="selectedOrder.estado_pago" 
                    @change="updateEstadoPago"
                    :class="['compact-select', getStatusClass(selectedOrder.estado_pago)]"
                  >
                    <option value="PENDIENTE">Pendiente</option>
                    <option value="PAGADO">Pagado</option>
                    <option value="CANCELADO">Cancelado</option>
                  </select>
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
            <svg class="notes-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
            </svg>
            <div class="notes-content">
              <span class="notes-label">Notas del cliente</span>
              <p class="notes-text">{{ orderDetail.notas_envio }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ordenesService } from '@/services/ordenes'

// Estado
const ordenes = ref([])
const selectedOrder = ref(null)
const orderDetail = ref(null)
const loading = ref(true)
const loadingDetail = ref(false)
const searchQuery = ref('')
const activeFilter = ref('todas')
const pollingInterval = ref(null)
const lastOrderCount = ref(0)

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

// Cargar órdenes
const cargarOrdenes = async (silent = false) => {
  try {
    if (!silent) loading.value = true
    const data = await ordenesService.obtenerTodas()
    
    const nuevasOrdenes = data.map(orden => ({
      id: orden.id,
      codigo: orden.codigo,
      cliente_nombre: orden.cliente_nombre || 'Sin cliente',
      cliente_email: orden.cliente_email || '',
      cliente_telefono: orden.cliente_telefono || '',
      total_items: orden.total_items || 0,
      total: orden.total || 0,
      estado_pago: mapEstadoPago(orden.estado),
      estado_envio: mapEstadoEnvio(orden.estado),
      metodo_pago: orden.metodo_pago || 'whatsapp',
      fecha_creacion: orden.fecha_creacion
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

// Seleccionar orden
const selectOrder = async (orden) => {
  selectedOrder.value = orden
  orderDetail.value = null
  
  // Marcar como vista
  markOrderAsSeen(orden.id)
  
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

// Actualizar estados
const updateEstadoPago = async () => {
  if (!selectedOrder.value) return
  
  try {
    const estadoMap = { 'PENDIENTE': 'pendiente', 'PAGADO': 'confirmada', 'CANCELADO': 'cancelada' }
    await ordenesService.actualizarEstado(selectedOrder.value.id, estadoMap[selectedOrder.value.estado_pago])
    
    if (selectedOrder.value.estado_pago !== 'PAGADO') {
      selectedOrder.value.estado_envio = 'NO_ENVIADO'
    }
    
    const idx = ordenes.value.findIndex(o => o.id === selectedOrder.value.id)
    if (idx !== -1) {
      ordenes.value[idx].estado_pago = selectedOrder.value.estado_pago
      ordenes.value[idx].estado_envio = selectedOrder.value.estado_envio
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

const updateEstadoEnvio = async () => {
  if (!selectedOrder.value || selectedOrder.value.estado_pago !== 'PAGADO') return
  
  try {
    const estadoMap = { 'NO_ENVIADO': 'confirmada', 'ENVIADO': 'enviada', 'ENTREGADO': 'entregada' }
    await ordenesService.actualizarEstado(selectedOrder.value.id, estadoMap[selectedOrder.value.estado_envio])
    
    const idx = ordenes.value.findIndex(o => o.id === selectedOrder.value.id)
    if (idx !== -1) {
      ordenes.value[idx].estado_envio = selectedOrder.value.estado_envio
    }
  } catch (error) {
    console.error('Error:', error)
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
  background: #f8fafc;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ========== MASTER LIST (Panel Izquierdo) ========== */
.master-list {
  width: 380px;
  min-width: 380px;
  background: #ffffff;
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
  padding: 14px 16px;
  margin-bottom: 6px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.order-card:hover {
  border-color: #d1d5db;
  background: #fafafa;
}

.order-card--active {
  border-color: #3b82f6;
  background: #eff6ff;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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

/* Indicador de orden no vista */
.order-card {
  position: relative;
}

.order-card__unseen-dot {
  position: absolute;
  top: 14px;
  left: -4px;
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  box-shadow: 0 0 0 2px #ffffff;
}

.order-card--unseen {
  background: #f0f9ff;
  border-color: #bfdbfe;
}

.order-card--unseen:hover {
  background: #e0f2fe;
  border-color: #93c5fd;
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
  background: #f8fafc;
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
  background: #ffffff;
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
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.02em;
}

.detail-header__date {
  font-size: 13px;
  color: #6b7280;
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
}

.action-btn--outline {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  color: #6b7280;
}

.action-btn--outline:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #111827;
}

.action-btn--whatsapp {
  background: #25d366;
  border: none;
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
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.bento-box {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.bento-box__header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #f9fafb;
  border-bottom: 1px solid #f3f4f6;
}

.bento-box__icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

.bento-box__label {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
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
  color: #9ca3af;
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
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #111827;
  background: #ffffff;
  outline: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.compact-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.compact-select:disabled {
  background: #f9fafb;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Select States */
.compact-select.status-pending { border-color: #fbbf24; background: #fffbeb; }
.compact-select.status-paid { border-color: #22c55e; background: #f0fdf4; }
.compact-select.status-cancelled { border-color: #ef4444; background: #fef2f2; }
.compact-select.shipping-pending { border-color: #d1d5db; }
.compact-select.shipping-sent { border-color: #3b82f6; background: #eff6ff; }
.compact-select.shipping-delivered { border-color: #22c55e; background: #f0fdf4; }

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
  background: #ffffff;
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
  color: #9ca3af;
  font-style: italic;
  padding: 40px 20px !important;
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
  margin-top: 8px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
}

.totals-row--final .totals-label {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.totals-row--final .totals-value {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

/* Notes Box */
.notes-box {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 12px;
}

.notes-icon {
  width: 20px;
  height: 20px;
  min-width: 20px;
  color: #d97706;
}

.notes-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.notes-label {
  font-size: 11px;
  font-weight: 600;
  color: #92400e;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.notes-text {
  font-size: 13px;
  color: #78350f;
  margin: 0;
  line-height: 1.5;
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
  }
  
  .master-list {
    width: 100%;
    min-width: 100%;
    height: 280px;
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
</style>
