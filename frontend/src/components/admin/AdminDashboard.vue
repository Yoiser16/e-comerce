<template>
  <div class="space-y-4 sm:space-y-8 animate-fade-in font-sans pb-6 sm:pb-12">
    
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center min-h-[600px]">
      <div class="relative w-24 h-24">
        <div class="absolute inset-0 border-4 border-gray-100 rounded-full"></div>
        <div class="absolute inset-0 border-4 border-brand-500 rounded-full border-t-transparent animate-spin"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-brand-500 font-bold text-xs">CARGANDO</span>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="min-h-[400px] flex items-center justify-center">
      <div class="text-center max-w-md mx-auto p-8 rounded-3xl bg-white shadow-[0_20px_50px_rgba(0,0,0,0.05)] border border-gray-100">
        <div class="w-20 h-20 mx-auto bg-red-50 rounded-2xl flex items-center justify-center mb-6 rotate-3 hover:rotate-6 transition-transform">
          <svg class="w-10 h-10 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2 font-luxury">Sin conexión</h3>
        <p class="text-gray-500 mb-8 leading-relaxed">{{ error }}</p>
        <button @click="cargarDatos" class="w-full py-4 bg-gray-900 text-white font-medium rounded-xl hover:bg-black transition-all hover:shadow-lg hover:-translate-y-1">
          Reintentar ahora
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="space-y-6 sm:space-y-10">

      <!-- Header & Quick Actions -->
      <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-4 sm:gap-8 animate-card delay-0">
        <div>
          <span class="inline-flex items-center gap-2 px-2 sm:px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold tracking-wide border border-emerald-100 mb-2 sm:mb-4 shadow-sm">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            SISTEMA OPERATIVO
          </span>
          <h1 class="font-luxury text-3xl sm:text-4xl lg:text-5xl text-gray-900 mb-1 sm:mb-2 tracking-tight">Panel de Control</h1>
          <p class="text-gray-500 text-sm sm:text-base lg:text-lg">Resumen global de <span class="text-brand-600 font-medium">{{ fechaActual }}</span></p>
        </div>

        <div class="flex flex-wrap gap-2 sm:gap-4">
          <router-link to="/admin/productos" class="px-3 sm:px-4 py-2 sm:py-3 rounded-lg sm:rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-all flex items-center gap-2 group text-gray-600 hover:text-gray-900 hover:border-gray-200 text-sm">
            <div class="w-6 sm:w-8 h-6 sm:h-8 rounded-lg bg-gray-50 flex items-center justify-center group-hover:bg-gray-100 transition-colors">
              <svg class="w-3 sm:w-4 h-3 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
            </div>
            <span class="font-medium hidden sm:inline">Inventario</span>
          </router-link>
          
          <router-link to="/admin/ordenes" class="px-3 sm:px-4 py-2 sm:py-3 rounded-lg sm:rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-all flex items-center gap-2 group text-gray-600 hover:text-gray-900 hover:border-gray-200 text-sm">
            <div class="w-6 sm:w-8 h-6 sm:h-8 rounded-lg bg-gray-50 flex items-center justify-center group-hover:bg-gray-100 transition-colors">
              <svg class="w-3 sm:w-4 h-3 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
            </div>
            <span class="font-medium hidden sm:inline">Pedidos</span>
          </router-link>

          <button @click="() => cargarDatos(false)" class="p-2 sm:p-3 rounded-lg sm:rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-all text-gray-400 hover:text-brand-600 group">
            <svg class="w-4 sm:w-6 h-4 sm:h-6 transform group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
          </button>

          <button @click="exportReport" class="px-3 sm:px-5 py-2 sm:py-3 rounded-lg sm:rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-all flex items-center gap-2 text-gray-700 font-medium hover:text-brand-600 text-sm">
             <svg class="w-4 sm:w-5 h-4 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
             <span class="hidden sm:inline">Exportar</span>
          </button>

          <router-link to="/admin/productos/nuevo" class="px-4 sm:px-6 py-2 sm:py-3 rounded-lg sm:rounded-2xl bg-gray-900 text-white font-medium text-sm shadow-lg shadow-gray-900/20 hover:bg-black hover:scale-105 active:scale-95 transition-all flex items-center gap-2">
            <svg class="w-4 sm:w-5 h-4 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>
            <span class="hidden sm:inline">Nuevo Producto</span>
            <span class="sm:hidden">+</span>
          </router-link>
        </div>
      </div>

      <!-- Stats Masonry Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-6 animate-card delay-100">
        
        <!-- Revenue Card (Primary) -->
        <div class="col-span-1 md:col-span-2 bg-gradient-to-br from-gray-900 to-gray-800 rounded-[2.5rem] p-6 text-white relative overflow-hidden group shadow-2xl shadow-gray-900/20 hover-card-effect cursor-default">
          <div class="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
          <div class="absolute bottom-0 left-0 w-48 h-48 bg-brand-500/20 rounded-full blur-3xl -ml-10 -mb-10 pointer-events-none"></div>
          
          <div class="relative z-10 flex flex-col h-full justify-between">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-white/60 font-medium mb-1 text-xs">Ingresos Totales</p>
                <div class="flex items-baseline gap-2">
                  <span class="text-4xl font-luxury tracking-tight">${{ formatNumber(stats.totalVentas) }}</span>
                </div>
              </div>
              <div class="text-right">
                  <p class="text-white/40 text-[10px] uppercase tracking-wider mb-1">Ticket Promedio</p>
                  <span class="text-xl font-bold text-brand-300">${{ formatNumber(stats.ticketPromedio) }}</span>
              </div>
            </div>

            <div class="mt-4 flex items-end justify-between">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span class="px-2 py-0.5 rounded-md bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/20 flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
                    +12.5%
                  </span>
                  <span class="text-white/40 text-xs">vs mes anterior</span>
                </div>
              </div>
              <!-- Mini Sparkline visualization (aesthetic only) -->
              <div class="flex items-end gap-1 h-8">
                <div v-for="h in [40, 65, 50, 80, 55, 90, 70]" :key="h" class="w-2 bg-white/20 rounded-t-sm transition-all group-hover:bg-brand-400" :style="`height: ${h}%`"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Orders Card & Inventory Health -->
        <div class="bg-white rounded-[2rem] p-4 border border-gray-100 shadow-[0_10px_30px_rgba(0,0,0,0.02)] hover-card-effect flex flex-col justify-between group cursor-default">
          <div class="flex justify-between items-start mb-3">
             <div class="w-10 h-10 rounded-2xl bg-blue-50 flex items-center justify-center text-blue-600">
               <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
             </div>
             <span class="text-2xl font-bold text-gray-900">{{ stats.totalOrdenes }}</span>
          </div>
          <div>
            <p class="text-gray-400 font-medium text-xs mb-3">Salud Inventario</p>
            <div class="flex gap-1 h-2 rounded-full overflow-hidden bg-gray-100">
                <div class="bg-emerald-500 transition-all duration-1000" :style="`width: ${(saludInventario.saludable / (stats.totalProductos || 1)) * 100}%`"></div>
                <div class="bg-amber-400 transition-all duration-1000" :style="`width: ${(saludInventario.bajo / (stats.totalProductos || 1)) * 100}%`"></div>
                <div class="bg-red-500 transition-all duration-1000" :style="`width: ${(saludInventario.agotado / (stats.totalProductos || 1)) * 100}%`"></div>
            </div>
            <div class="flex justify-between mt-2 text-[10px] text-gray-400">
                <span>{{ saludInventario.saludable }} OK</span>
                <span v-if="saludInventario.bajo > 0" class="text-amber-600 font-bold">{{ saludInventario.bajo }} Bajo</span>
            </div>
          </div>
        </div>
        
        <!-- Customer Growth -->
        <div class="bg-white rounded-[2rem] p-4 border border-gray-100 shadow-[0_10px_30px_rgba(0,0,0,0.02)] hover-card-effect flex flex-col justify-between group cursor-default">
             <div class="flex justify-between items-center mb-2">
                 <p class="text-gray-400 text-xs font-bold uppercase">Nuevos Clientes</p>
                 <span class="text-emerald-500 font-bold text-sm">+{{ stats.clientesNuevos }}</span>
             </div>
             <div class="h-20 -mx-2">
                 <Bar :data="growthChartData" :options="growthChartOptions" />
             </div>
             <div class="flex items-center gap-2 mt-2">
                 <span class="text-2xl font-bold text-gray-900">{{ stats.totalClientes }}</span>
                 <span class="text-xs text-gray-400">total activos</span>
             </div>
        </div>

      </div>

      <!-- Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Main Chart Section: Revenue -->
        <div class="lg:col-span-2 bg-white rounded-[2.5rem] border border-gray-100 shadow-[0_20px_50px_rgba(0,0,0,0.04)] p-4 sm:p-8 relative flex flex-col animate-card delay-200 hover-card-effect">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
            <div>
              <h3 class="text-2xl font-luxury font-bold text-gray-900">Análisis de Ventas</h3>
              <p class="text-gray-400 text-sm mt-1">Tendencia de ventas en el tiempo</p>
            </div>
            
            <div class="bg-gray-50 p-1.5 rounded-2xl flex items-center shadow-inner">
               <button 
                v-for="period in ['24H', '7D', '30D']" 
                :key="period"
                @click="cambiarPeriodo(period)"
                class="px-5 py-2 rounded-xl text-xs font-bold transition-all duration-300 relative z-10"
                :class="selectedPeriod === period ? 'bg-white text-gray-900 shadow-md shadow-gray-200' : 'text-gray-400 hover:text-gray-600'"
              >
                {{ period }}
              </button>
            </div>
          </div>

          <div class="relative flex-1 w-full min-h-[300px]">
             <!-- Loading Overlay -->
            <transition name="fade">
              <div v-if="chartLoading" class="absolute inset-0 bg-white/60 backdrop-blur-[2px] z-20 flex items-center justify-center rounded-2xl">
                <div class="flex items-center gap-3 bg-white px-6 py-3 rounded-full shadow-lg border border-gray-100">
                   <div class="w-2 h-2 bg-brand-500 rounded-full animate-bounce"></div>
                   <div class="w-2 h-2 bg-brand-500 rounded-full animate-bounce delay-75"></div>
                   <div class="w-2 h-2 bg-brand-500 rounded-full animate-bounce delay-150"></div>
                </div>
              </div>
            </transition>
            
            <div class="h-[300px] w-full">
               <Line :data="salesChartData" :options="salesChartOptions" />
            </div>
          </div>
        </div>

        <!-- Sales by Category -->
        <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-[0_20px_50px_rgba(0,0,0,0.04)] p-4 sm:p-8 relative flex flex-col animate-card delay-300 hover-card-effect">
             <div class="mb-6">
               <h3 class="text-xl font-luxury font-bold text-gray-900">Por Categoría</h3>
               <p class="text-gray-400 text-sm mt-1">Ventas por segmento</p>
             </div>
             <div class="flex-1 relative min-h-[250px] flex items-center justify-center">
                 <Doughnut :data="categoryChartData" :options="donutChartOptions" />
                 <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none pr-20 md:pr-0 lg:pr-24 xl:pr-0">
                   <!-- Center text is tricky with legend on right, leaving empty for now -->
                 </div>
             </div>
        </div>

        <!-- Status Distribution -->
        <div class="bg-gray-50 rounded-[2.5rem] border border-gray-100 p-4 sm:p-8 animate-card delay-400 hover-card-effect">
             <div class="mb-6 flex justify-between items-end">
               <div>
                 <h3 class="text-xl font-luxury font-bold text-gray-900">Estado de Órdenes</h3>
                 <p class="text-gray-400 text-sm mt-1">Flujo actual de pedidos</p>
               </div>
               <span class="text-3xl font-bold text-gray-900">{{ stats.totalOrdenes }}</span>
             </div>
             <div class="space-y-4">
               <div v-for="item in pStatusData" :key="item.label" class="group hover:translate-x-2 transition-transform duration-300 cursor-default">
                 <div class="flex justify-between items-end mb-1">
                   <span class="text-sm font-semibold text-gray-700">{{ item.label }}</span>
                   <div class="text-right">
                     <span class="text-sm font-bold text-gray-900">{{ item.count }}</span>
                     <span class="text-xs text-gray-400 ml-1">({{ item.percent }}%)</span>
                   </div>
                 </div>
                 <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                   <div 
                     class="h-full rounded-full transition-all duration-1000 ease-out group-hover:opacity-90 relative overflow-hidden"
                     :class="item.color"
                     :style="`width: ${item.relativeWidth}%`"
                   >
                      <div class="absolute inset-0 bg-white/20 transform -skew-x-12 -translate-x-full group-hover:animate-shimmer"></div>
                   </div>
                 </div>
               </div>
             </div>
        </div>

        <!-- Top Products List -->
        <div class="lg:col-span-2 bg-gray-900 rounded-[2.5rem] p-8 text-white relative overflow-hidden shadow-2xl flex flex-col animate-card delay-500 hover-card-effect">
          <div class="absolute top-0 right-0 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none"></div>
          
          <div class="relative z-10 mb-8 flex items-center justify-between">
            <div>
              <h3 class="text-2xl font-luxury font-bold text-white">Top Productos</h3>
              <p class="text-white/40 text-sm mt-1">Los más vendidos del periodo</p>
            </div>
          </div>

          <div class="relative z-10 grid grid-cols-1 md:grid-cols-2 gap-4">
             <div v-for="(product, index) in topProducts" :key="product.id" class="flex items-center gap-4 p-4 rounded-3xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors group">
               <div class="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center text-lg font-bold">
                  {{ index + 1 }}
               </div>
               <div class="flex-1 min-w-0">
                 <h4 class="text-white font-medium truncate">{{ product.nombre }}</h4>
                 <p class="text-white/40 text-xs">{{ product.cantidad }} unidades vendidas</p>
               </div>
               <div class="text-right">
                 <span class="text-brand-400 font-bold block">${{ formatNumber(product.ventas) }}</span>
               </div>
             </div>
          </div>
        </div>

      </div>

      <!-- Recent Orders Table -->
      <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden p-8 animate-card delay-600 hover-card-effect">
        <div class="flex items-center justify-between mb-8">
          <div>
            <h3 class="text-2xl font-luxury font-bold text-gray-900">Transacciones Recientes</h3>
            <p class="text-gray-400 text-sm mt-1">Últimos movimientos registrados</p>
          </div>
          <router-link to="/admin/ordenes" class="px-5 py-2 rounded-xl bg-gray-50 text-gray-600 font-medium hover:bg-gray-100 transition-colors text-sm">
            Ver historial completo
          </router-link>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-100">
                <th class="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-wider">ID Orden</th>
                <th class="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Cliente</th>
                <th class="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Fecha</th>
                <th class="text-center py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Estado</th>
                <th class="text-right py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Monto</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="orden in recentOrders" :key="orden.id" class="group hover:bg-white hover:shadow-md hover:scale-[1.01] transition-all duration-200 cursor-pointer border-b border-transparent hover:border-gray-100 rounded-xl relative z-0 hover:z-10">
                 <td class="py-4 px-4">
                   <span class="font-mono text-xs font-bold bg-gray-100 text-gray-600 px-2 py-1 rounded-md group-hover:bg-gray-200 transition-colors">
                     #{{ orden.id.slice(0,6).toUpperCase() }}
                   </span>
                 </td>
                 <td class="py-4 px-4">
                   <div class="flex items-center gap-3">
                     <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-gray-200 to-gray-100 flex items-center justify-center text-xs font-bold text-gray-600">
                        {{ orden.cliente.charAt(0).toUpperCase() }}
                     </div>
                     <span class="text-sm font-medium text-gray-900">{{ orden.cliente }}</span>
                   </div>
                 </td>
                 <td class="py-4 px-4 text-sm text-gray-500">{{ orden.fecha }}</td>
                 <td class="py-4 px-4 text-center">
                   <span :class="getStatusClass(orden.estado)" class="inline-flex px-3 py-1 rounded-full text-xs font-bold border">
                     {{ getStatusLabel(orden.estado) }}
                   </span>
                 </td>
                 <td class="py-4 px-4 text-right">
                   <span class="text-sm font-bold text-gray-900">${{ formatNumber(orden.total) }}</span>
                 </td>
              </tr>
              <tr v-if="recentOrders.length === 0">
                <td colspan="5" class="py-12 text-center text-gray-400 bg-gray-50/30 rounded-2xl border border-dashed border-gray-200">
                  <div class="flex flex-col items-center gap-2">
                    <svg class="w-8 h-8 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg> 
                    <span>No hay datos recientes</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Line, Doughnut, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ArcElement
} from 'chart.js'
import apiClient from '../../services/api'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler, ArcElement)

export default {
  name: 'AdminDashboard',
  components: { Line, Doughnut, Bar },
  setup() {
    // Definimos una paleta de colores personalizada y moderna
    const brandColors = {
      primary: '#111827', // Dark/Black
      accent: '#D81B60', // Kharis Pink
      gold: '#C9A962',  // Luxury Gold
      success: '#10B981',
      warning: '#F59E0B',
      info: '#3B82F6'
    }

    const chartColors = [brandColors.accent, brandColors.gold, '#8B5CF6', brandColors.info, brandColors.success, '#EC4899', '#6366F1']
    
    const stats = ref({})
    // Valores por defecto para evitar errores al cargar parcialmente
    const defaultStats = { 
        totalVentas: 0, totalOrdenes: 0, ordenesPendientes: 0, 
        totalProductos: 0, productosActivos: 0, stockBajo: 0, 
        totalClientes: 0, clientesNuevos: 0, ticketPromedio: 0 
    }
    stats.value = { ...defaultStats }

    const loading = ref(true)
    const chartLoading = ref(false)
    const error = ref(null)
    const selectedPeriod = ref('7D')
    const pollingInterval = ref(null)

    const recentOrders = ref([])
    const lowStockProducts = ref([])
    const topProducts = ref([])
    const ventasPorPeriodo = ref({ labels: [], data: [] })
    const ventasPorCategoria = ref({ labels: [], data: [] })
    const distribucionEstados = ref({ labels: [], data: [] })
    const crecimientoClientes = ref({ labels: [], data: [] })
    const saludInventario = ref({ agotado: 0, bajo: 0, saludable: 0 })

    const fechaActual = computed(() => {
      const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }
      const date = new Date().toLocaleDateString('es-CO', options)
      return date.charAt(0).toUpperCase() + date.slice(1)
    })

    // Revenue Chart Config (Restored Pink Spline)
    const salesChartData = computed(() => ({
      labels: ventasPorPeriodo.value.labels || [],
      datasets: [{
        label: 'Ventas',
        data: ventasPorPeriodo.value.data || [],
        borderColor: '#EC4899', // Pink 500
        backgroundColor: (context) => {
          const ctx = context.chart.ctx
          const gradient = ctx.createLinearGradient(0, 0, 0, 300)
          gradient.addColorStop(0, 'rgba(236, 72, 153, 0.2)')
          gradient.addColorStop(1, 'rgba(236, 72, 153, 0)')
          return gradient
        },
        borderWidth: 3,
        tension: 0.4, // Smooth curve
        fill: true,
        pointBackgroundColor: '#EC4899',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    }))

    const salesChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#111827',
          padding: 12,
          callbacks: {
            label: (context) => ` ${new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(context.raw)}`
          }
        }
      },
      scales: {
        x: { 
          grid: { display: false },
          ticks: { font: { size: 12 }, color: '#9CA3AF' }
        },
        y: { 
          border: { display: false },
          grid: { color: '#F3F4F6' },
          ticks: { 
            font: { size: 11 }, 
            color: '#9CA3AF',
            callback: (val) => val >= 1000 ? `$${val/1000}k` : `$${val}` 
          } 
        }
      },
      interaction: {
        intersect: false,
        mode: 'index',
      },
    }

    // Donut Chart Configuration
    const topProductsChartData = computed(() => ({
      labels: topProducts.value.map(p => p.nombre),
      datasets: [{
        data: topProducts.value.map(p => p.ventas),
        backgroundColor: chartColors,
        borderWidth: 0,
        hoverOffset: 15, // Dynamic pop on hover
        borderRadius: 4
      }]
    }))



    // Category Chart Config
    const categoryChartData = computed(() => ({
      labels: ventasPorCategoria.value.labels || [],
      datasets: [{
        data: ventasPorCategoria.value.data || [],
        backgroundColor: chartColors,
        borderWidth: 0,
        hoverOffset: 20
      }]
    }))

    // Customer Growth Chart (Standard Bar for Readability)
    const growthChartData = computed(() => ({
      labels: crecimientoClientes.value.labels || [],
      datasets: [{
        label: 'Nuevos Clientes',
        data: crecimientoClientes.value.data || [],
        backgroundColor: '#10B981', // Solid Emerald
        hoverBackgroundColor: '#059669',
        borderRadius: 4,
        barPercentage: 0.6
      }]
    }))

     // Status Chart Config (Bar)
     // Processed Status Data for Custom HTML List
    const pStatusData = computed(() => {
       const labels = distribucionEstados.value.labels || []
       const data = distribucionEstados.value.data || []
       
       if (!labels.length) return []

       const total = data.reduce((a, b) => a + b, 0) || 1
       const max = Math.max(...data) || 1

       return labels.map((label, index) => {
          const l = label.toLowerCase()
          let color = 'bg-gray-500'
          
          // Paleta "Enterprise": Menos saturada, más elegante
          if(l.includes('completada') || l.includes('ok')) color = 'bg-teal-600' // Teal elegante
          else if(l.includes('pendiente')) color = 'bg-amber-500' // Amber cálido
          else if(l.includes('confirmada')) color = 'bg-indigo-600' // Indigo profundo
          else if(l.includes('proceso')) color = 'bg-blue-600' // Azul corporativo
          else if(l.includes('enviada')) color = 'bg-sky-500' // Sky
          else if(l.includes('cancelada')) color = 'bg-slate-400' // Gris neutro (menos alarmante que rojo)

          return {
             label,
             count: data[index],
             percent: Math.round((data[index] / total) * 100),
             relativeWidth: Math.round((data[index] / max) * 100),
             color
          }
       }).sort((a, b) => b.count - a.count) // Ordenar por cantidad
    })

    const basicChartOptions = {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            x: { grid: { display: false } },
            y: { grid: { borderDash: [5, 5] }, ticks: { stepSize: 1 } }
        }
    }

    const growthChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { 
                display: true, 
                grid: { display: false },
                ticks: { font: { size: 10 }, color: '#9CA3AF' }
            },
            y: { 
                display: true,
                min: 0,
                grid: { borderDash: [4, 4], color: '#F3F4F6' },
                ticks: { stepSize: 1, font: { size: 10 }, color: '#9CA3AF' } 
            }
        }
    }

    const statusChartOptions = {
      indexAxis: 'y', // Convertir a gráfico de barras horizontales
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#111827',
          padding: 12,
          displayColors: true,
          boxWidth: 8,
          boxHeight: 8,
          usePointStyle: true,
          callbacks: { 
            title: (items) => items[0].label.toUpperCase(),
            label: c => ` ${c.raw} órdenes` 
          }
        }
      },
      scales: {
        x: { 
            display: false, // Ocultar eje X
            grid: { display: false } 
        },
        y: { 
            display: true,
            grid: { display: false },
            ticks: { 
                font: { size: 12, weight: '600', family: 'Inter, sans-serif' },
                color: '#4B5563',
                mirror: false // Labels fuera de la barra
            } 
        }
      },
      layout: {
        padding: { left: 0, right: 20, top: 0, bottom: 0 }
      }
    }

    const donutChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '75%',
      plugins: {
        legend: { 
          display: true, 
          position: 'right',
          labels: { boxWidth: 10, font: { size: 11 }, color: '#9CA3AF', padding: 15 }
        },
        tooltip: {
          backgroundColor: '#fff',
          titleColor: '#111827',
          bodyColor: '#111827',
          borderColor: '#E5E7EB',
          borderWidth: 1,
          padding: 14,
          callbacks: {
            label: (context) => ` ${context.raw} unidades`
          }
        }
      }
    }

    // Data Loading Functions - OPTIMIZADO: Una sola llamada al backend
    const cargarDatos = async (silent = false) => {
      if(!silent) { loading.value = true; error.value = null }
      
      try {
        // Una sola llamada optimizada que trae todo el dashboard
        const res = await apiClient.get(`/dashboard/completo?periodo=${selectedPeriod.value}`)
        const data = res.data || {}
        
        // Estadísticas
        stats.value = {
          totalVentas: data.estadisticas?.total_ventas || 0,
          totalOrdenes: data.estadisticas?.total_ordenes || 0,
          ordenesPendientes: data.estadisticas?.ordenes_pendientes || 0,
          totalProductos: data.estadisticas?.total_productos || 0,
          productosActivos: data.estadisticas?.productos_activos || 0,
          stockBajo: data.estadisticas?.stock_bajo || 0,
          totalClientes: data.estadisticas?.total_clientes || 0,
          clientesNuevos: data.estadisticas?.clientes_nuevos || 0,
          ticketPromedio: data.estadisticas?.ticket_promedio || 0
        }
        
        // Órdenes recientes
        recentOrders.value = (data.ordenes_recientes || []).map(o => ({
          id: o.id || '---',
          cliente: o.cliente_nombre || 'Invitado',
          estado: o.estado || 'PENDIENTE',
          total: o.total || 0,
          fecha: o.tiempo_transcurrido || 'Reciente'
        }))
        
        // Ventas por período
        ventasPorPeriodo.value = {
          labels: data.ventas_por_periodo?.labels || [],
          data: data.ventas_por_periodo?.data || []
        }

        // Ventas por categoría
        ventasPorCategoria.value = {
          labels: data.ventas_por_categoria?.labels || [],
          data: data.ventas_por_categoria?.data || []
        }

        // Distribución de estados
        distribucionEstados.value = {
          labels: (data.distribucion_estados?.labels || []).map(l => getStatusLabel(l)), // Traducir labels
          data: data.distribucion_estados?.data || []
        }

        // Crecimiento clientes
        crecimientoClientes.value = {
            labels: data.crecimiento_clientes?.labels || [],
            data: data.crecimiento_clientes?.data || []
        }

        // Salud inventario
        saludInventario.value = data.salud_inventario || { agotado: 0, bajo: 0, saludable: 0}
        
        // Top productos
        topProducts.value = data.top_productos || []
        
        // Stock bajo
        lowStockProducts.value = data.productos_stock_bajo || []
        
        // Log de rendimiento
        if (data._meta) {
          console.log(`📊 Dashboard cargado en ${data._meta.tiempo_carga_ms}ms`)
        }
        
      } catch (e) {
        console.error('Error crítico dashboard:', e)
        if(!silent) error.value = 'Hubo un problema cargando la información.'
      } finally {
        if(!silent) loading.value = false
      }
    }

    const cambiarPeriodo = async (periodo) => {
      if (selectedPeriod.value === periodo) return
      selectedPeriod.value = periodo
      chartLoading.value = true
      
      try {
        // Recargar dashboard completo con nuevo período
        const res = await apiClient.get(`/dashboard/completo?periodo=${periodo}`)
        const data = res.data || {}
        
        ventasPorPeriodo.value = {
          labels: data.ventas_por_periodo?.labels || [],
          data: data.ventas_por_periodo?.data || []
        }
      } catch(e) { console.error(e) } 
      finally { setTimeout(() => chartLoading.value = false, 300) }
    }

    onMounted(() => {
      cargarDatos()
      // Polling cada 30 segundos (reducido de 15s para mejor rendimiento)
      pollingInterval.value = setInterval(() => cargarDatos(true), 30000)
    })

    onUnmounted(() => clearInterval(pollingInterval.value))

    // Utils
    const formatNumber = (n) => new Intl.NumberFormat('es-CO', { maximumFractionDigits: 0 }).format(n || 0)
    
    const getStatusClass = (status) => {
      const map = {
        'PENDIENTE': 'bg-amber-50 text-amber-700 border-amber-100',
        'CONFIRMADA': 'bg-blue-50 text-blue-700 border-blue-100',
        'EN_PROCESO': 'bg-violet-50 text-violet-700 border-violet-100',
        'ENVIADA': 'bg-indigo-50 text-indigo-700 border-indigo-100',
        'COMPLETADA': 'bg-emerald-50 text-emerald-700 border-emerald-100',
        'CANCELADA': 'bg-gray-50 text-gray-500 border-gray-100'
      }
      return map[status] || 'bg-gray-50 text-gray-500'
    }

    const getStatusLabel = (status) => {
      const map = {
        'PENDIENTE': 'Pendiente', 'CONFIRMADA': 'Confirmada', 'EN_PROCESO': 'En Proceso',
        'ENVIADA': 'Enviada', 'COMPLETADA': 'Completada', 'CANCELADA': 'Cancelada'
      }
      return map[status] || status
    }

    const exportReport = () => {
        // 1. Headers del CSV
        const headers = ['Order ID', 'Cliente', 'Items', 'Estado', 'Total', 'Fecha']
        
        // 2. Mapear datos de órdenes recientes
        const rows = recentOrders.value.map(o => [
            o.id,
            `"${o.cliente}"`, // Escapar comillas
            o.items,
            o.estado,
            o.total,
            `"${o.fecha}"`
        ])

        // 3. Unir todo en string CSV
        const csvContent = [
            headers.join(','),
            ...rows.map(r => r.join(','))
        ].join('\n')

        // 4. Crear Blob y descargar
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)
        
        link.setAttribute('href', url)
        link.setAttribute('download', `reporte_ventas_${new Date().toISOString().slice(0,10)}.csv`)
        link.style.visibility = 'hidden'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }

    return {
      stats, loading, chartLoading, error, selectedPeriod, recentOrders, topProducts, lowStockProducts,
      topProductsChartData, donutChartOptions, chartColors,
      categoryChartData, growthChartData, growthChartOptions, salesChartData, salesChartOptions,
      saludInventario, exportReport,
      fechaActual, cargarDatos, cambiarPeriodo, formatNumber, getStatusClass, getStatusLabel
    }
  }
}
</script>

<style scoped>
.font-luxury { font-family: 'Playfair Display', serif; }

.animate-fade-in {
  /* Removed simple fadeIn to use staggered animate-card instead */
}

/* Entrance Animations */
@keyframes slideUpFade {
  from { opacity: 0; transform: translateY(30px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.animate-card {
  opacity: 0; /* Star hidden */
  animation: slideUpFade 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

.delay-0 { animation-delay: 0ms; }
.delay-100 { animation-delay: 100ms; }
.delay-200 { animation-delay: 200ms; }
.delay-300 { animation-delay: 300ms; }
.delay-400 { animation-delay: 400ms; }
.delay-500 { animation-delay: 500ms; }
.delay-600 { animation-delay: 600ms; }

/* Shimmer Effect for graphs/loading */
@keyframes shimmer {
  100% { transform: skewX(-12deg) translateX(150%); }
}
.animate-shimmer { animation: shimmer 2s infinite; }
/* Global Hover Effect */
.hover-card-effect {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.hover-card-effect:hover {
  transform: translateY(-8px); /* Lift up notably */
  box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.15), 0 10px 20px -5px rgba(0, 0, 0, 0.1);
  animation: slideUpFade 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

/* Custom User-Requested Neon Theme */
.bg-neon-lime {
  background-color: #C6FF00;
  box-shadow: 0 0 15px rgba(198, 255, 0, 0.4);
}
.text-neon-glow {
  color: #C6FF00;
  text-shadow: 0 0 8px #C6FF00, 0 0 16px #C6FF00;
}
</style>
