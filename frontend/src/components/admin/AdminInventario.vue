<template>
  <div class="inventory-container">
    <!-- Header -->
    <div class="inventory-header">
      <div>
        <h2 class="inventory-title">Inventario</h2>
        <p class="inventory-subtitle">Control de stock y alertas</p>
      </div>
      <button class="btn-primary">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Ajuste de Stock
      </button>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-nav">
      <button 
        @click="activeTab = 'stock'"
        :class="['tab-item', { 'tab-item--active': activeTab === 'stock' }]"
      >
        Stock Actual
      </button>
      <button 
        @click="activeTab = 'movimientos'"
        :class="['tab-item', { 'tab-item--active': activeTab === 'movimientos' }]"
      >
        Movimientos / Kardex
      </button>
      <button 
        @click="activeTab = 'alertas'"
        :class="['tab-item', { 'tab-item--active': activeTab === 'alertas' }]"
      >
        Alertas de Stock
        <span v-if="stats.agotados + stats.stockBajo > 0" class="tab-badge">
          {{ stats.agotados + stats.stockBajo }}
        </span>
      </button>
    </div>

    <!-- KPI Cards - Clean Design -->
    <div v-if="activeTab === 'stock'" class="kpi-grid">
      <!-- KPI 1: Valor del Inventario -->
      <div class="kpi-card">
        <div class="kpi-icon kpi-icon--purple">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">Valor del Inventario</p>
          <p class="kpi-value">${{ formatNumber(valorInventario) }}</p>
        </div>
      </div>

      <!-- KPI 2: Total Productos -->
      <div class="kpi-card">
        <div class="kpi-icon kpi-icon--blue">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">Total Productos</p>
          <p class="kpi-value">{{ productos.length }} <span class="kpi-unit">SKUs</span></p>
        </div>
      </div>

      <!-- KPI 3: Por Reabastecer -->
      <div class="kpi-card kpi-card--warning">
        <div class="kpi-icon kpi-icon--orange">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">Por Reabastecer</p>
          <p class="kpi-value kpi-value--warning">{{ stats.agotados + stats.stockBajo }}</p>
        </div>
      </div>

      <!-- KPI 4: Stock Saludable -->
      <div class="kpi-card">
        <div class="kpi-icon kpi-icon--green">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">Stock Saludable</p>
          <p class="kpi-value kpi-value--success">{{ porcentajeSaludable }}%</p>
        </div>
      </div>
    </div>

    <!-- Inventory Table (Stock Actual) -->
    <div v-if="activeTab === 'stock'" class="inventory-table-container">
      <table class="inventory-table">
        <thead>
          <tr>
            <th class="col-producto">Producto</th>
            <th class="col-sku">SKU</th>
            <th class="col-stock">Stock Actual</th>
            <th class="col-minimo">Stock Mínimo</th>
            <th class="col-estado">Estado</th>
            <th class="col-acciones">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in inventario" :key="item.id" class="table-row">
            <td class="col-producto">
              <div class="producto-cell">
                <div class="producto-thumb">
                  <img v-if="item.imagen" :src="item.imagen" :alt="item.nombre" />
                  <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
                <span class="producto-nombre">{{ item.nombre }}</span>
              </div>
            </td>
            <td class="col-sku">
              <span class="sku-code">{{ item.sku }}</span>
            </td>
            <td class="col-stock">
              <div class="stock-cell">
                <span :class="['stock-number', getStockTextClass(item)]">{{ item.stock }}</span>
                <div class="stock-bar">
                  <div 
                    :class="['stock-bar-fill', getStockBarClass(item)]"
                    :style="{ width: getStockPercentage(item) + '%' }"
                  ></div>
                </div>
              </div>
            </td>
            <td class="col-minimo">
              <span class="minimo-text">{{ item.stockMinimo }}</span>
            </td>
            <td class="col-estado">
              <span :class="['status-badge', getStockBadgeClass(item)]">
                {{ getStockLabel(item) }}
              </span>
            </td>
            <td class="col-acciones">
              <div class="action-buttons">
                <button class="action-icon" title="Editar stock">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button class="action-icon" title="Ver historial">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Movimientos / Kardex View -->
    <div v-if="activeTab === 'movimientos'" class="movimientos-view">
      <!-- Filtros Avanzados -->
      <div class="filtros-bar">
        <div class="filtro-group">
          <label class="filtro-label">Rango de Fechas</label>
          <div class="filtro-dates">
            <input 
              type="date" 
              v-model="filtros.fechaDesde" 
              class="filtro-input"
              placeholder="Desde"
            />
            <span class="filtro-separator">—</span>
            <input 
              type="date" 
              v-model="filtros.fechaHasta" 
              class="filtro-input"
              placeholder="Hasta"
            />
          </div>
        </div>

        <div class="filtro-group">
          <label class="filtro-label">Tipo de Movimiento</label>
          <select v-model="filtros.tipo" class="filtro-select">
            <option value="">Todos</option>
            <option value="ENTRADA">Entrada</option>
            <option value="SALIDA">Salida</option>
            <option value="AJUSTE">Ajuste</option>
          </select>
        </div>

        <div class="filtro-group">
          <label class="filtro-label">Usuario</label>
          <select v-model="filtros.usuario" class="filtro-select">
            <option value="">Todos</option>
            <option value="admin">Administrador</option>
            <option value="vendedor">Vendedor</option>
          </select>
        </div>

        <button class="filtro-btn-reset" @click="resetFiltros">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Limpiar
        </button>
      </div>

      <!-- Tabla de Movimientos (Estilo Extracto Bancario) -->
      <div class="kardex-table-container">
        <table class="kardex-table">
          <thead>
            <tr>
              <th class="col-fecha">Fecha y Hora</th>
              <th class="col-producto">Producto</th>
              <th class="col-tipo">Tipo</th>
              <th class="col-cantidad">Cantidad</th>
              <th class="col-responsable">Responsable / Motivo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mov in movimientosFiltrados" :key="mov.id" class="kardex-row">
              <!-- Fecha y Hora -->
              <td class="col-fecha">
                <div class="fecha-cell">
                  <span class="fecha-dia">{{ formatFecha(mov.fecha) }}</span>
                  <span class="fecha-hora">{{ formatHora(mov.fecha) }}</span>
                </div>
              </td>

              <!-- Producto -->
              <td class="col-producto">
                <div class="producto-mini">
                  <div class="producto-mini-thumb">
                    <img v-if="mov.producto_imagen" :src="mov.producto_imagen" :alt="mov.producto_nombre" />
                    <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                  </div>
                  <span class="producto-mini-nombre">{{ mov.producto_nombre }}</span>
                </div>
              </td>

              <!-- Tipo de Movimiento -->
              <td class="col-tipo">
                <div :class="['tipo-badge', getTipoBadgeClass(mov.tipo)]">
                  <svg v-if="mov.tipo === 'ENTRADA'" class="tipo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m0 0l-4-4m4 4l4-4" />
                  </svg>
                  <svg v-else-if="mov.tipo === 'SALIDA'" class="tipo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 20V4m0 0l4 4m-4-4l-4 4" />
                  </svg>
                  <svg v-else class="tipo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span class="tipo-label">{{ mov.tipo }}</span>
                </div>
              </td>

              <!-- Cantidad -->
              <td class="col-cantidad">
                <span :class="['cantidad-number', getCantidadClass(mov.tipo)]">
                  {{ formatCantidad(mov.cantidad, mov.tipo) }}
                </span>
              </td>

              <!-- Responsable / Motivo -->
              <td class="col-responsable">
                <div class="responsable-cell">
                  <div class="responsable-avatar">
                    {{ getInitials(mov.usuario) }}
                  </div>
                  <div class="responsable-info">
                    <span class="responsable-nombre">{{ mov.usuario }}</span>
                    <span class="responsable-motivo">{{ mov.motivo }}</span>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Empty State -->
        <div v-if="movimientosFiltrados.length === 0" class="kardex-empty">
          <svg class="kardex-empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="kardex-empty-text">No hay movimientos registrados</p>
        </div>
      </div>
    </div>

    <!-- Alertas de Stock View -->
    <div v-if="activeTab === 'alertas'" class="alertas-view">
      <div class="alertas-empty">
        <svg class="alertas-empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <p class="alertas-empty-text">Vista de Alertas - Próximamente</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { productosService } from '../../services/productos'
import { inventarioService } from '../../services/inventario'

export default {
  name: 'AdminInventario',
  setup() {
    const loading = ref(true)
    const loadingMovimientos = ref(false)
    const productos = ref([])
    const activeTab = ref('stock')

    // Filtros para Movimientos
    const filtros = ref({
      fechaDesde: '',
      fechaHasta: '',
      tipo: '',
      usuario: ''
    })

    // Movimientos reales desde el backend
    const movimientos = ref([])

    const cargarMovimientos = async () => {
      try {
        loadingMovimientos.value = true
        
        const params = {
          limite: 100
        }
        
        if (filtros.value.fechaDesde) params.fechaDesde = filtros.value.fechaDesde
        if (filtros.value.fechaHasta) params.fechaHasta = filtros.value.fechaHasta
        if (filtros.value.tipo) params.tipo = filtros.value.tipo
        
        const data = await inventarioService.obtenerMovimientos(params)
        
        movimientos.value = data.map(m => ({
          id: m.id,
          fecha: m.fecha,
          producto_nombre: m.producto_nombre,
          producto_imagen: m.producto_imagen,
          tipo: m.tipo,
          cantidad: m.cantidad,
          usuario: m.usuario,
          motivo: m.motivo
        }))
        
        console.log(`✅ Movimientos cargados: ${movimientos.value.length} registros`)
      } catch (error) {
        console.error('❌ Error al cargar movimientos:', error)
        movimientos.value = []
      } finally {
        loadingMovimientos.value = false
      }
    }

    const cargarInventario = async () => {
      try {
        loading.value = true
        const data = await productosService.obtenerTodos({ limite: 1000 })
        
        // Transformar productos a formato de inventario
        productos.value = data.map(p => ({
          id: p.id,
          nombre: p.nombre,
          sku: p.codigo || 'N/A',
          stock: p.stock_actual || 0,
          stockMinimo: p.stock_minimo || 5,
          precio: parseFloat(p.precio_monto) || 0,
          imagen: p.imagen_principal || ''
        }))
        
        console.log(`✅ Inventario cargado: ${productos.value.length} productos`)
      } catch (error) {
        console.error('❌ Error al cargar inventario:', error)
        productos.value = []
      } finally {
        loading.value = false
      }
    }

    const stats = computed(() => {
      const agotados = productos.value.filter(p => p.stock === 0).length
      const stockBajo = productos.value.filter(p => p.stock > 0 && p.stock <= p.stockMinimo).length
      const saludables = productos.value.filter(p => p.stock > p.stockMinimo).length

      return { agotados, stockBajo, saludables }
    })

    const valorInventario = computed(() => {
      return productos.value.reduce((total, p) => total + (p.stock * p.precio), 0)
    })

    const porcentajeSaludable = computed(() => {
      if (productos.value.length === 0) return 0
      return Math.round((stats.value.saludables / productos.value.length) * 100)
    })

    const inventario = computed(() => productos.value)

    const getStockTextClass = (item) => {
      if (item.stock === 0) return 'stock-number--critical'
      if (item.stock <= item.stockMinimo) return 'stock-number--warning'
      return 'stock-number--healthy'
    }

    const getStockBarClass = (item) => {
      if (item.stock === 0) return 'stock-bar-fill--critical'
      if (item.stock <= item.stockMinimo) return 'stock-bar-fill--warning'
      return 'stock-bar-fill--healthy'
    }

    const getStockPercentage = (item) => {
      // Calcular porcentaje basado en stock mínimo * 3 como máximo ideal
      const ideal = item.stockMinimo * 3
      const percentage = (item.stock / ideal) * 100
      return Math.min(percentage, 100)
    }

    const getStockBadgeClass = (item) => {
      if (item.stock === 0) return 'status-badge--critical'
      if (item.stock <= item.stockMinimo) return 'status-badge--warning'
      return 'status-badge--healthy'
    }

    const getStockLabel = (item) => {
      if (item.stock === 0) return 'Agotado'
      if (item.stock <= item.stockMinimo) return 'Stock Bajo'
      return 'Disponible'
    }

    const formatNumber = (num) => {
      return new Intl.NumberFormat('es-CO').format(num || 0)
    }

    // ===== Funciones para Tab de Movimientos =====
    const movimientosFiltrados = computed(() => {
      let resultado = movimientos.value

      // Filtro por fecha desde
      if (filtros.value.fechaDesde) {
        const fechaDesde = new Date(filtros.value.fechaDesde)
        resultado = resultado.filter(m => new Date(m.fecha) >= fechaDesde)
      }

      // Filtro por fecha hasta
      if (filtros.value.fechaHasta) {
        const fechaHasta = new Date(filtros.value.fechaHasta)
        fechaHasta.setHours(23, 59, 59)
        resultado = resultado.filter(m => new Date(m.fecha) <= fechaHasta)
      }

      // Filtro por tipo
      if (filtros.value.tipo) {
        resultado = resultado.filter(m => m.tipo === filtros.value.tipo)
      }

      // Filtro por usuario
      if (filtros.value.usuario) {
        resultado = resultado.filter(m => m.usuario.toLowerCase().includes(filtros.value.usuario.toLowerCase()))
      }

      return resultado
    })

    const resetFiltros = () => {
      filtros.value = {
        fechaDesde: '',
        fechaHasta: '',
        tipo: '',
        usuario: ''
      }
      cargarMovimientos()
    }

    const formatFecha = (fecha) => {
      const d = new Date(fecha)
      const dia = String(d.getDate()).padStart(2, '0')
      const mes = String(d.getMonth() + 1).padStart(2, '0')
      const año = d.getFullYear()
      return `${dia}/${mes}/${año}`
    }

    const formatHora = (fecha) => {
      const d = new Date(fecha)
      const hora = String(d.getHours()).padStart(2, '0')
      const min = String(d.getMinutes()).padStart(2, '0')
      return `${hora}:${min}`
    }

    const getTipoBadgeClass = (tipo) => {
      return `tipo-badge--${tipo.toLowerCase()}`
    }

    const getCantidadClass = (tipo) => {
      if (tipo === 'ENTRADA') return 'cantidad-number--entrada'
      if (tipo === 'SALIDA') return 'cantidad-number--salida'
      return 'cantidad-number--ajuste'
    }

    const formatCantidad = (cantidad, tipo) => {
      if (tipo === 'ENTRADA') return `+${cantidad}`
      if (tipo === 'SALIDA') return `-${cantidad}`
      return cantidad > 0 ? `+${cantidad}` : String(cantidad)
    }

    const getInitials = (nombre) => {
      if (!nombre) return 'NA'
      const palabras = nombre.split(' ')
      if (palabras.length >= 2) {
        return (palabras[0][0] + palabras[1][0]).toUpperCase()
      }
      return nombre.substring(0, 2).toUpperCase()
    }

    onMounted(() => {
      cargarInventario()
    })

    // Cargar movimientos cuando se cambia al tab de movimientos
    watch(activeTab, (newTab) => {
      if (newTab === 'movimientos' && movimientos.value.length === 0) {
        cargarMovimientos()
      }
    })

    // Recargar movimientos cuando cambian los filtros de fecha o tipo
    watch(() => filtros.value.fechaDesde, () => {
      if (activeTab.value === 'movimientos') {
        cargarMovimientos()
      }
    })

    watch(() => filtros.value.fechaHasta, () => {
      if (activeTab.value === 'movimientos') {
        cargarMovimientos()
      }
    })

    watch(() => filtros.value.tipo, () => {
      if (activeTab.value === 'movimientos') {
        cargarMovimientos()
      }
    })

    return { 
      stats, 
      inventario, 
      productos,
      loading,
      loadingMovimientos,
      activeTab,
      valorInventario,
      porcentajeSaludable,
      getStockTextClass, 
      getStockBarClass,
      getStockPercentage,
      getStockBadgeClass, 
      getStockLabel, 
      formatNumber,
      cargarInventario,
      // Movimientos
      filtros,
      movimientos,
      movimientosFiltrados,
      cargarMovimientos,
      resetFiltros,
      formatFecha,
      formatHora,
      getTipoBadgeClass,
      getCantidadClass,
      formatCantidad,
      getInitials
    }
  }
}
</script>

<style scoped>
/* ========== INVENTORY CONTAINER ========== */
.inventory-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========== HEADER ========== */
.inventory-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.inventory-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px;
  letter-spacing: -0.02em;
}

.inventory-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #D81B60;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #c2185b;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(216, 27, 96, 0.25);
}

/* ========== TABS NAVIGATION ========== */
.tabs-nav {
  display: flex;
  gap: 2px;
  border-bottom: 2px solid #f3f4f6;
  padding: 0;
}

.tab-item {
  position: relative;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.tab-item:hover {
  color: #111827;
  background: #f9fafb;
}

.tab-item--active {
  color: #D81B60;
  font-weight: 600;
}

.tab-item--active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #D81B60;
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #ef4444;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  border-radius: 10px;
}

/* ========== KPI CARDS ========== */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.kpi-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.2s ease;
}

.kpi-card:hover {
  border-color: #d1d5db;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.kpi-card--warning {
  background: #fffef8;
  border-color: #fde68a;
}

.kpi-icon {
  width: 48px;
  height: 48px;
  min-width: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.kpi-icon svg {
  width: 24px;
  height: 24px;
}

.kpi-icon--purple {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  color: #ffffff;
}

.kpi-icon--blue {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: #ffffff;
}

.kpi-icon--orange {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: #ffffff;
}

.kpi-icon--green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #ffffff;
}

.kpi-content {
  flex: 1;
  min-width: 0;
}

.kpi-label {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  margin: 0 0 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.kpi-value {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.03em;
}

.kpi-value--warning {
  color: #d97706;
}

.kpi-value--success {
  color: #059669;
}

.kpi-unit {
  font-size: 14px;
  font-weight: 500;
  color: #9ca3af;
  margin-left: 4px;
}

/* ========== INVENTORY TABLE ========== */
.inventory-table-container {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  overflow: hidden;
}

.inventory-table {
  width: 100%;
  border-collapse: collapse;
}

.inventory-table thead {
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.inventory-table th {
  padding: 14px 20px;
  font-size: 11px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  text-align: left;
}

.col-stock,
.col-minimo {
  text-align: center;
}

.col-acciones {
  text-align: right;
}

.table-row {
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.15s ease;
}

.table-row:hover {
  background: #fafafa;
}

.table-row:last-child {
  border-bottom: none;
}

.inventory-table td {
  padding: 16px 20px;
  vertical-align: middle;
}

/* ========== PRODUCT CELL ========== */
.producto-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.producto-thumb {
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

.producto-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.producto-thumb svg {
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.producto-nombre {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

/* ========== SKU CODE ========== */
.sku-code {
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  font-size: 12px;
  color: #6b7280;
  background: #f9fafb;
  padding: 4px 8px;
  border-radius: 6px;
  letter-spacing: 0.02em;
}

/* ========== STOCK CELL WITH PROGRESS BAR ========== */
.stock-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.stock-number {
  font-size: 20px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.stock-number--critical {
  color: #dc2626;
}

.stock-number--warning {
  color: #f59e0b;
}

.stock-number--healthy {
  color: #10b981;
}

.stock-bar {
  width: 60px;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.stock-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.stock-bar-fill--critical {
  background: #dc2626;
}

.stock-bar-fill--warning {
  background: #f59e0b;
}

.stock-bar-fill--healthy {
  background: #10b981;
}

/* ========== MINIMUM STOCK ========== */
.minimo-text {
  font-size: 14px;
  color: #9ca3af;
  font-weight: 500;
}

/* ========== STATUS BADGE ========== */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 8px;
  text-transform: capitalize;
}

.status-badge--critical {
  background: #fee2e2;
  color: #991b1b;
}

.status-badge--warning {
  background: #fef3c7;
  color: #92400e;
}

.status-badge--healthy {
  background: #d1fae5;
  color: #065f46;
}

/* ========== ACTION BUTTONS ========== */
.action-buttons {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}

.action-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #6b7280;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.action-icon:hover {
  background: #f3f4f6;
  color: #111827;
}

.action-icon svg {
  width: 18px;
  height: 18px;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .inventory-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .tabs-nav {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .tab-item {
    white-space: nowrap;
  }
}

/* ========================================== */
/* MOVIMIENTOS / KARDEX VIEW (Extracto Bancario) */
/* ========================================== */

.movimientos-view {
  animation: fadeIn 0.3s ease;
}

/* ========== FILTROS BAR ========== */
.filtros-bar {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.filtro-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
  min-width: 180px;
}

.filtro-label {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filtro-dates {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filtro-separator {
  color: #9ca3af;
  font-size: 14px;
}

.filtro-input,
.filtro-select {
  padding: 10px 14px;
  font-size: 14px;
  color: #1f2937;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
  transition: all 0.2s ease;
  font-family: system-ui, -apple-system, sans-serif;
}

.filtro-input:focus,
.filtro-select:focus {
  border-color: #D81B60;
  box-shadow: 0 0 0 3px rgba(216, 27, 96, 0.1);
}

.filtro-input::placeholder {
  color: #9ca3af;
}

.filtro-btn-reset {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filtro-btn-reset svg {
  width: 16px;
  height: 16px;
}

.filtro-btn-reset:hover {
  background: #f3f4f6;
  color: #111827;
  border-color: #d1d5db;
}

/* ========== KARDEX TABLE (Estilo Extracto Bancario) ========== */
.kardex-table-container {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.kardex-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.kardex-table thead {
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.kardex-table thead th {
  padding: 14px 20px;
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.kardex-table tbody {
  background: #ffffff;
}

.kardex-row {
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.12s ease;
}

.kardex-row:hover {
  background: #fafafa;
}

.kardex-row:last-child {
  border-bottom: none;
}

.kardex-table td {
  padding: 16px 20px;
  vertical-align: middle;
}

/* Columnas específicas */
.col-fecha {
  width: 140px;
}

.col-producto {
  width: auto;
}

.col-tipo {
  width: 150px;
}

.col-cantidad {
  width: 120px;
  text-align: right;
}

.col-responsable {
  width: 280px;
}

/* ========== FECHA CELL ========== */
.fecha-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.fecha-dia {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.fecha-hora {
  font-size: 12px;
  color: #9ca3af;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
}

/* ========== PRODUCTO MINI ========== */
.producto-mini {
  display: flex;
  align-items: center;
  gap: 12px;
}

.producto-mini-thumb {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  background: #f9fafb;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.producto-mini-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.producto-mini-thumb svg {
  width: 16px;
  height: 16px;
  color: #d1d5db;
}

.producto-mini-nombre {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

/* ========== TIPO BADGE ========== */
.tipo-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tipo-icon {
  width: 14px;
  height: 14px;
}

.tipo-badge--entrada {
  background: #d1fae5;
  color: #065f46;
}

.tipo-badge--entrada .tipo-icon {
  color: #10b981;
}

.tipo-badge--salida {
  background: #fee2e2;
  color: #991b1b;
}

.tipo-badge--salida .tipo-icon {
  color: #ef4444;
}

.tipo-badge--ajuste {
  background: #e0e7ff;
  color: #3730a3;
}

.tipo-badge--ajuste .tipo-icon {
  color: #6366f1;
}

/* ========== CANTIDAD NUMBER ========== */
.cantidad-number {
  font-size: 16px;
  font-weight: 700;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  display: inline-block;
}

.cantidad-number--entrada {
  color: #10b981;
}

.cantidad-number--salida {
  color: #ef4444;
}

.cantidad-number--ajuste {
  color: #6366f1;
}

/* ========== RESPONSABLE CELL ========== */
.responsable-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.responsable-avatar {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  background: linear-gradient(135deg, #D81B60, #e91e63);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  text-transform: uppercase;
}

.responsable-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.responsable-nombre {
  font-size: 13px;
  font-weight: 600;
  color: #111827;
}

.responsable-motivo {
  font-size: 12px;
  color: #6b7280;
}

/* ========== EMPTY STATE ========== */
.kardex-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.kardex-empty-icon {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.kardex-empty-text {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}

/* ========== ALERTAS VIEW ========== */
.alertas-view {
  animation: fadeIn 0.3s ease;
}

.alertas-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  background: #ffffff;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
}

.alertas-empty-icon {
  width: 72px;
  height: 72px;
  color: #d1d5db;
  margin-bottom: 20px;
}

.alertas-empty-text {
  font-size: 16px;
  color: #6b7280;
  font-weight: 500;
  margin: 0;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .filtros-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .filtro-group {
    min-width: 100%;
  }

  .filtro-dates {
    flex-direction: column;
  }

  .filtro-separator {
    display: none;
  }

  .kardex-table-container {
    overflow-x: auto;
  }

  .kardex-table {
    min-width: 800px;
  }

  .producto-mini-nombre {
    font-size: 13px;
  }

  .responsable-motivo {
    font-size: 11px;
  }
}
</style>
```