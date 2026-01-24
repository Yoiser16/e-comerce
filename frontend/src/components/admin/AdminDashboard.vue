<template>
  <div class="space-y-8 animate-fade-in font-sans pb-12">
    
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
    <div v-else class="space-y-10">

      <!-- Header & Quick Actions -->
      <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-8">
        <div>
          <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold tracking-wide border border-emerald-100 mb-4 shadow-sm">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            SISTEMA OPERATIVO
          </span>
          <h1 class="font-luxury text-5xl text-gray-900 mb-2 tracking-tight">Panel de Control</h1>
          <p class="text-gray-500 text-lg">Resumen global de <span class="text-brand-600 font-medium">{{ fechaActual }}</span></p>
        </div>

        <div class="flex flex-wrap gap-4">
          <router-link to="/admin/productos" class="pl-4 pr-6 py-3 rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-all flex items-center gap-3 group text-gray-600 hover:text-gray-900 hover:border-gray-200">
            <div class="w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center group-hover:bg-gray-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
            </div>
            <span class="font-medium">Inventario</span>
          </router-link>
          
          <router-link to="/admin/ordenes" class="pl-4 pr-6 py-3 rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-all flex items-center gap-3 group text-gray-600 hover:text-gray-900 hover:border-gray-200">
            <div class="w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center group-hover:bg-gray-100 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
            </div>
            <span class="font-medium">Pedidos</span>
          </router-link>

          <button @click="cargarDatos" class="p-3 rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-all text-gray-400 hover:text-brand-600 group">
            <svg class="w-6 h-6 transform group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
          </button>

          <router-link to="/admin/productos/nuevo" class="px-6 py-3 rounded-2xl bg-gray-900 text-white font-medium shadow-lg shadow-gray-900/20 hover:bg-black hover:scale-105 active:scale-95 transition-all flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>
            Nueva Venta
          </router-link>
        </div>
      </div>

      <!-- Stats Masonry Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        
        <!-- Revenue Card (Primary) -->
        <div class="col-span-1 md:col-span-2 bg-gradient-to-br from-gray-900 to-gray-800 rounded-[2.5rem] p-8 text-white relative overflow-hidden group shadow-2xl shadow-gray-900/20">
          <div class="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
          <div class="absolute bottom-0 left-0 w-48 h-48 bg-brand-500/20 rounded-full blur-3xl -ml-10 -mb-10 pointer-events-none"></div>
          
          <div class="relative z-10 flex flex-col h-full justify-between">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-white/60 font-medium mb-1">Ingresos Totales</p>
                <div class="flex items-baseline gap-2">
                  <span class="text-5xl font-luxury tracking-tight">${{ formatNumber(stats.totalVentas) }}</span>
                </div>
              </div>
              <div class="p-3 bg-white/10 backdrop-blur-md rounded-2xl border border-white/10">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </div>
            </div>

            <div class="mt-8 flex items-end justify-between">
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
              <div class="flex items-end gap-1 h-12">
                <div v-for="h in [40, 65, 50, 80, 55, 90, 70]" :key="h" class="w-2 bg-white/20 rounded-t-sm transition-all group-hover:bg-brand-400" :style="`height: ${h}%`"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Orders Card -->
        <div class="bg-white rounded-[2rem] p-6 border border-gray-100 shadow-[0_10px_30px_rgba(0,0,0,0.02)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.06)] transition-all duration-300 flex flex-col justify-between group">
          <div class="flex justify-between items-start mb-4">
            <div class="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center text-blue-600 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
            </div>
            <span class="px-3 py-1 rounded-full bg-gray-50 text-gray-600 text-xs font-bold border border-gray-100">{{ stats.ordenesPendientes }} pendientes</span>
          </div>
          <div>
            <h3 class="text-3xl font-bold text-gray-900 mb-1">{{ stats.totalOrdenes }}</h3>
            <p class="text-gray-400 font-medium text-sm">Órdenes Totales</p>
          </div>
        </div>

        <!-- Products Card -->
        <div class="bg-white rounded-[2rem] p-6 border border-gray-100 shadow-[0_10px_30px_rgba(0,0,0,0.02)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.06)] transition-all duration-300 flex flex-col justify-between group">
          <div class="flex justify-between items-start mb-4">
            <div class="w-12 h-12 rounded-2xl bg-purple-50 flex items-center justify-center text-purple-600 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
            </div>
            <span :class="stats.stockBajo > 0 ? 'bg-amber-50 text-amber-600 border-amber-100' : 'bg-emerald-50 text-emerald-600 border-emerald-100'" class="px-3 py-1 rounded-full text-xs font-bold border">
              {{ stats.stockBajo }} Alertas
            </span>
          </div>
          <div>
            <h3 class="text-3xl font-bold text-gray-900 mb-1">{{ stats.totalProductos }}</h3>
            <p class="text-gray-400 font-medium text-sm">Productos Activos</p>
          </div>
        </div>

        <!-- Clients Card -->
        <div class="col-span-1 md:col-span-2 lg:col-span-3 xl:col-span-4 bg-white rounded-[2rem] p-6 border border-gray-100 shadow-[0_10px_30px_rgba(0,0,0,0.02)] flex items-center justify-between relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-pink-50/50 to-transparent pointer-events-none"></div>
          <div class="relative z-10 flex items-center gap-6">
            <div class="w-16 h-16 rounded-3xl bg-pink-50 flex items-center justify-center text-pink-600 shadow-sm border border-pink-100">
               <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
            </div>
             <div>
              <h3 class="text-2xl font-bold text-gray-900">{{ stats.totalClientes }} Clientes</h3>
              <p class="text-gray-500 text-sm">Registrados en la plataforma</p>
            </div>
          </div>
          <div class="relative z-10 flex items-center gap-4 pr-4">
             <div class="flex -space-x-3">
               <div v-for="i in 4" :key="i" class="w-10 h-10 rounded-full border-2 border-white bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-400">
                 <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/></svg>
               </div>
             </div>
             <span class="text-sm font-semibold text-pink-600 bg-pink-50 px-3 py-1 rounded-full">+{{ stats.clientesNuevos }} nuevos este mes</span>
          </div>
        </div>

      </div>

      <!-- Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Main Chart Section -->
        <div class="lg:col-span-2 bg-white rounded-[2.5rem] border border-gray-100 shadow-[0_20px_50px_rgba(0,0,0,0.04)] p-8 relative">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
            <div>
              <h3 class="text-2xl font-luxury font-bold text-gray-900">Análisis de Ingresos</h3>
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

          <div class="relative h-[400px] w-full">
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
            
            <Line :data="salesChartData" :options="salesChartOptions" />
          </div>
        </div>

        <!-- Right Column: Top Products -->
        <div class="bg-gray-900 rounded-[2.5rem] p-8 text-white relative overflow-hidden shadow-2xl flex flex-col">
          <div class="absolute top-0 right-0 w-64 h-64 bg-brand-500/20 rounded-full blur-3xl -mr-20 -mt-20"></div>
          
          <div class="relative z-10 mb-8">
            <h3 class="text-2xl font-luxury font-bold text-white">Top Ventas</h3>
            <p class="text-white/40 text-sm mt-1">Distribución mejores productos</p>
          </div>

          <div class="relative z-10 flex-1 flex flex-col justify-center items-center">
            <div class="w-64 h-64 relative">
              <Doughnut :data="topProductsChartData" :options="donutChartOptions" />
              <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                 <span class="text-4xl font-luxury">{{ topProducts.length }}</span>
                 <span class="text-[10px] uppercase tracking-[0.2em] text-white/40 mt-1">Items</span>
              </div>
            </div>
          </div>

          <div class="relative z-10 mt-8 space-y-4">
             <div v-for="(product, index) in topProducts.slice(0,3)" :key="product.id" class="flex items-center justify-between p-3 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
               <div class="flex items-center gap-3 overflow-hidden">
                 <span class="w-2 h-8 rounded-full flex-shrink-0" :style="{ backgroundColor: chartColors[index] }"></span>
                 <span class="text-sm font-medium text-white/90 truncate">{{ product.nombre }}</span>
               </div>
               <span class="text-white font-bold text-sm">{{ product.ventas }}</span>
             </div>
          </div>

        </div>

      </div>

      <!-- Recent Orders Table -->
      <div class="bg-white rounded-[2.5rem] border border-gray-100 shadow-sm overflow-hidden p-8">
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
              <tr v-for="orden in recentOrders" :key="orden.id" class="group hover:bg-gray-50/50 transition-colors">
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
import { Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ArcElement
} from 'chart.js'
import apiClient from '../../services/api'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler, ArcElement)

export default {
  name: 'AdminDashboard',
  components: { Line, Doughnut },
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

    const chartColors = [brandColors.accent, brandColors.gold, '#8B5CF6', brandColors.info, brandColors.success]
    
    const stats = ref({})
    // Valores por defecto para evitar errores al cargar parcialmente
    const defaultStats = { totalVentas: 0, totalOrdenes: 0, ordenesPendientes: 0, totalProductos: 0, productosActivos: 0, stockBajo: 0, totalClientes: 0, clientesNuevos: 0 }
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

    const fechaActual = computed(() => {
      const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }
      const date = new Date().toLocaleDateString('es-CO', options)
      return date.charAt(0).toUpperCase() + date.slice(1)
    })

    // Sales Chart Configuration
    const salesChartData = computed(() => {
      // Fallback labels
      let defaultLabels = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
      if (selectedPeriod.value === '24H') defaultLabels = ['00h', '04h', '08h', '12h', '16h', '20h']
      if (selectedPeriod.value === '30D') defaultLabels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']

      const labels = ventasPorPeriodo.value.labels?.length ? ventasPorPeriodo.value.labels : defaultLabels
      const data = ventasPorPeriodo.value.data?.length ? ventasPorPeriodo.value.data : labels.map(() => 0)

      return {
        labels,
        datasets: [{
          label: 'Ingresos',
          data,
          fill: true,
          borderColor: brandColors.accent,
          borderWidth: 4,
          tension: 0.45, // Super smooth
          pointRadius: 0,
          pointHoverRadius: 8,
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: brandColors.accent,
          pointHoverBorderWidth: 3,
          backgroundColor: (context) => {
            const ctx = context.chart.ctx
            const gradient = ctx.createLinearGradient(0, 0, 0, 350)
            gradient.addColorStop(0, 'rgba(216, 27, 96, 0.15)')
            gradient.addColorStop(1, 'rgba(216, 27, 96, 0)')
            return gradient
          },
        }]
      }
    })

    const salesChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false, mode: 'index' },
      plugins: {
        legend: { display: false },
        tooltip: {
          enabled: true,
          backgroundColor: '#111827',
          padding: 16,
          titleFont: { size: 14, family: "'Playfair Display', serif" },
          bodyFont: { size: 13, weight: 'bold' },
          cornerRadius: 10,
          displayColors: false,
          callbacks: {
            label: (context) => `$${new Intl.NumberFormat('es-CO').format(context.raw)}`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#9CA3AF', font: { size: 12 }, padding: 10 }
        },
        y: {
          border: { display: false },
          grid: { color: '#F3F4F6', drawTicks: false },
          ticks: { 
            color: '#9CA3AF', 
            font: { size: 11, weight: '500' },
            callback: val => `$${val >= 1000 ? val/1000 + 'k' : val}`,
            padding: 12
          }
        }
      }
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

    const donutChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '80%',
      plugins: {
        legend: { display: false },
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

    // Data Loading Functions
    const fetchData = async (endpoint, targetRef, defaultVal = []) => {
      try {
        const res = await apiClient.get(endpoint)
        targetRef.value = res.data || defaultVal
      } catch (e) {
        console.error(`Error fetching ${endpoint}:`, e)
        // Keep default/previous value
      }
    }

    const cargarDatos = async (silent = false) => {
      if(!silent) { loading.value = true; error.value = null }
      
      try {
        // Usamos una estrategia de "intento" individual para que si falla un endpoint
        // no se caiga todo el dashboard.
        await Promise.allSettled([
          // Estadísticas - Convertir snake_case a camelCase
          apiClient.get('/dashboard/estadisticas')
            .then(r => {
              const data = r.data || {}
              stats.value = {
                totalVentas: data.total_ventas || 0,
                totalOrdenes: data.total_ordenes || 0,
                ordenesPendientes: data.ordenes_pendientes || 0,
                totalProductos: data.total_productos || 0,
                productosActivos: data.productos_activos || 0,
                stockBajo: data.stock_bajo || 0,
                totalClientes: data.total_clientes || 0,
                clientesNuevos: data.clientes_nuevos || 0
              }
              console.log('📊 Stats cargadas:', stats.value)
            })
            .catch(e => {
              console.warn('Fallo estadísticas:', e)
              stats.value = defaultStats
            }),

          // Órdenes Recientes
          apiClient.get('/dashboard/ordenes/recientes?limite=5')
            .then(r => {
               recentOrders.value = (r.data || []).map(o => ({
                id: o.id || '---',
                cliente: o.cliente_nombre || 'Invitado',
                estado: o.estado || 'PENDIENTE',
                total: o.total || 0,
                fecha: o.tiempo_transcurrido || 'Reciente'
              }))
            })
            .catch(e => console.warn('Fallo ordenes:', e)),

          // Gráfico Ventas
          apiClient.get(`/dashboard/ventas/por-periodo?periodo=${selectedPeriod.value}`)
            .then(r => {
               ventasPorPeriodo.value = { labels: r.data.labels || [], data: r.data.data || [] }
            })
            .catch(e => console.warn('Fallo grafico ventas:', e)),

          // Top Productos (ya usa fetchData interno, pero lo aseguramos)
          fetchData('/dashboard/top-productos?limite=5', topProducts),
          
          // Stock Bajo
          fetchData('/dashboard/productos/stock-bajo?umbral=5&limite=10', lowStockProducts)
        ])

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
        // Fetch only sales data
        const res = await apiClient.get(`/dashboard/ventas/por-periodo?periodo=${periodo}`)
        ventasPorPeriodo.value = { labels: res.data.labels || [], data: res.data.data || [] }
      } catch(e) { console.error(e) } 
      finally { setTimeout(() => chartLoading.value = false, 300) }
    }

    onMounted(() => {
      cargarDatos()
      pollingInterval.value = setInterval(() => cargarDatos(true), 15000) // Poll faster for live feel
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

    return {
      stats, loading, chartLoading, error, selectedPeriod, recentOrders, topProducts, lowStockProducts,
      salesChartData, salesChartOptions, topProductsChartData, donutChartOptions, chartColors,
      fechaActual, cargarDatos, cambiarPeriodo, formatNumber, getStatusClass, getStatusLabel
    }
  }
}
</script>

<style scoped>
.font-luxury { font-family: 'Playfair Display', serif; }

.animate-fade-in {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); filter: blur(10px); }
  to { opacity: 1; transform: translateY(0); filter: blur(0); }
}

.delay-75 { animation-delay: 75ms; }
.delay-150 { animation-delay: 150ms; }
</style>
