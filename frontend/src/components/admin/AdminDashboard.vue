<template>
  <div class="space-y-6 lg:space-y-8">
    
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
      <p class="text-red-600 mb-4">{{ error }}</p>
      <button @click="cargarDatos" class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
        Reintentar
      </button>
    </div>

    <!-- Content -->
    <div v-else>

      <!-- Header Section -->
      <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4 lg:gap-6">
        <div>
          <div class="flex items-center gap-2 text-sm text-text-light mb-1">
            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            Sistema Operativo • {{ fechaActual }}
          </div>
          <h1 class="font-luxury text-2xl lg:text-3xl text-text-dark">
            Panel de Control
          </h1>
        </div>
        <div class="flex items-center gap-3">
          <button 
            @click="cargarDatos"
            class="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-text-medium hover:text-text-dark border border-gray-200 rounded-xl hover:bg-gray-50 transition-all"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            Refrescar
          </button>
          <router-link 
            to="/admin/productos/nuevo"
            class="inline-flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-white font-medium px-5 py-2.5 rounded-xl transition-all shadow-lg shadow-emerald-500/20"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Nueva Venta
          </router-link>
        </div>
      </div>

      <!-- Stats Cards Row -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mt-6 lg:mt-8">
        
        <!-- Ventas del Mes -->
        <div class="bg-white rounded-2xl p-5 lg:p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-4">
            <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span class="text-emerald-600 text-xs font-semibold flex items-center gap-0.5 bg-emerald-50 px-2 py-1 rounded-full">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" />
              </svg>
              +12.5%
            </span>
          </div>
          <h3 class="text-2xl lg:text-3xl font-semibold text-text-dark tracking-tight">${{ formatNumber(stats.totalVentas) }}</h3>
          <p class="text-text-light text-sm mt-1">Ventas este mes</p>
        </div>

        <!-- Órdenes -->
        <div class="bg-white rounded-2xl p-5 lg:p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-4">
            <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
            </div>
            <span class="text-blue-600 text-xs font-semibold bg-blue-50 px-2 py-1 rounded-full">
              {{ stats.ordenesPendientes }} pendientes
            </span>
          </div>
          <h3 class="text-2xl lg:text-3xl font-semibold text-text-dark tracking-tight">{{ stats.totalOrdenes }}</h3>
          <p class="text-text-light text-sm mt-1">Órdenes totales</p>
        </div>

        <!-- Productos -->
        <div class="bg-white rounded-2xl p-5 lg:p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-4">
            <div class="w-10 h-10 bg-violet-50 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-violet-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
              </svg>
            </div>
            <span :class="stats.stockBajo > 0 ? 'text-amber-600 bg-amber-50' : 'text-emerald-600 bg-emerald-50'" class="text-xs font-semibold px-2 py-1 rounded-full">
              {{ stats.stockBajo }} stock bajo
            </span>
          </div>
          <h3 class="text-2xl lg:text-3xl font-semibold text-text-dark tracking-tight">{{ stats.totalProductos }}</h3>
          <p class="text-text-light text-sm mt-1">Productos activos</p>
        </div>

        <!-- Clientes -->
        <div class="bg-white rounded-2xl p-5 lg:p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-4">
            <div class="w-10 h-10 bg-rose-50 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-rose-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
              </svg>
            </div>
            <span class="text-rose-600 text-xs font-semibold bg-rose-50 px-2 py-1 rounded-full">
              +{{ stats.clientesNuevos }} nuevos
            </span>
          </div>
          <h3 class="text-2xl lg:text-3xl font-semibold text-text-dark tracking-tight">{{ stats.totalClientes }}</h3>
          <p class="text-text-light text-sm mt-1">Clientes registrados</p>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid lg:grid-cols-5 gap-6 mt-6 lg:mt-8">
        
        <!-- Sales Chart - Larger -->
        <div class="lg:col-span-3 bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-lg font-semibold text-text-dark">Análisis de Ventas</h3>
              <p class="text-sm text-text-light">Tendencia de ventas en el tiempo</p>
            </div>
            <div class="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
              <button 
                v-for="period in ['24H', '7D', '30D']" 
                :key="period"
                @click="selectedPeriod = period"
                :class="selectedPeriod === period ? 'bg-white shadow-sm text-text-dark' : 'text-text-light hover:text-text-medium'"
                class="px-3 py-1.5 text-xs font-medium rounded-md transition-all"
              >
                {{ period }}
              </button>
            </div>
          </div>
          
          <!-- Chart Container -->
          <div class="h-64 lg:h-72">
            <Line :data="salesChartData" :options="salesChartOptions" />
          </div>
        </div>

        <!-- Top Products Donut Chart -->
        <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <div class="mb-6">
            <h3 class="text-lg font-semibold text-text-dark">Top Productos</h3>
            <p class="text-sm text-text-light">Distribución de ventas</p>
          </div>
          
          <!-- Donut Chart -->
          <div class="flex flex-col items-center gap-6">
            <div class="relative w-36 h-36 lg:w-44 lg:h-44 flex-shrink-0">
              <Doughnut :data="topProductsChartData" :options="donutChartOptions" />
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-2xl font-bold text-text-dark">{{ topProducts.length }}</span>
                <span class="text-xs text-text-light">ITEMS</span>
              </div>
            </div>
            
            <!-- Legend -->
            <div class="w-full space-y-2">
              <div 
                v-for="(product, index) in topProducts.slice(0, 5)" 
                :key="product.nombre"
                class="flex items-center justify-between py-1"
              >
                <div class="flex items-center gap-2">
                  <span 
                    class="w-2.5 h-2.5 rounded-full flex-shrink-0" 
                    :style="{ backgroundColor: chartColors[index] }"
                  ></span>
                  <span class="text-sm text-text-medium truncate max-w-[120px]">{{ product.nombre }}</span>
                </div>
                <span class="text-sm font-semibold text-text-dark">${{ formatNumber(product.ventas) }}</span>
              </div>
              
              <div v-if="topProducts.length === 0" class="text-center py-4 text-text-light text-sm">
                Sin datos de ventas
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Section: Orders & Stock -->
      <div class="grid lg:grid-cols-3 gap-6 mt-6 lg:mt-8">
        
        <!-- Recent Orders Table -->
        <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="flex items-center justify-between p-5 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-text-dark">Últimas Transacciones</h3>
            <router-link to="/admin/ordenes" class="text-emerald-600 text-sm font-medium hover:text-emerald-700 transition-colors">
              Ver todas →
            </router-link>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="bg-gray-50/50">
                  <th class="px-5 py-3 text-left text-xs font-semibold text-text-light uppercase tracking-wider">Orden</th>
                  <th class="px-5 py-3 text-left text-xs font-semibold text-text-light uppercase tracking-wider">Cliente</th>
                  <th class="px-5 py-3 text-left text-xs font-semibold text-text-light uppercase tracking-wider">Estado</th>
                  <th class="px-5 py-3 text-right text-xs font-semibold text-text-light uppercase tracking-wider">Total</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="orden in recentOrders" :key="orden.id" class="hover:bg-gray-50/50 transition-colors">
                  <td class="px-5 py-4">
                    <span class="font-mono text-sm font-medium text-text-dark">#{{ orden.id.slice(0, 6).toUpperCase() }}</span>
                  </td>
                  <td class="px-5 py-4">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                        {{ orden.cliente.charAt(0).toUpperCase() }}
                      </div>
                      <span class="text-text-dark text-sm">{{ orden.cliente }}</span>
                    </div>
                  </td>
                  <td class="px-5 py-4">
                    <span :class="getStatusClass(orden.estado)" class="px-2.5 py-1 text-xs font-medium rounded-full">
                      {{ getStatusLabel(orden.estado) }}
                    </span>
                  </td>
                  <td class="px-5 py-4 text-right">
                    <span class="font-semibold text-text-dark">${{ formatNumber(orden.total) }}</span>
                  </td>
                </tr>
                <tr v-if="recentOrders.length === 0">
                  <td colspan="4" class="px-5 py-10 text-center text-text-light">
                    <svg class="w-12 h-12 mx-auto mb-3 text-gray-200" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                    </svg>
                    No hay transacciones recientes
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Alerts & Stock Section -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="flex items-center justify-between p-5 border-b border-gray-100">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
              </svg>
              <h3 class="text-lg font-semibold text-text-dark">Alertas Stock</h3>
            </div>
            <router-link to="/admin/inventario" class="text-amber-600 text-sm font-medium hover:text-amber-700">
              Ver Todo
            </router-link>
          </div>
          
          <div class="p-4 space-y-3 max-h-80 overflow-y-auto">
            <div 
              v-for="product in lowStockProducts" 
              :key="product.id"
              class="flex items-center gap-3 p-3 bg-amber-50/50 rounded-xl border border-amber-100"
            >
              <div class="w-12 h-12 bg-white rounded-lg overflow-hidden shadow-sm flex-shrink-0">
                <img 
                  :src="product.imagen" 
                  :alt="product.nombre" 
                  class="w-full h-full object-cover"
                  @error="$event.target.src = 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 fill=%22%23f3f4f6%22 viewBox=%220 0 24 24%22%3E%3Cpath d=%22M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z%22/%3E%3C/svg%3E'"
                >
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-sm text-text-dark truncate">{{ product.nombre }}</p>
                <p class="text-xs text-amber-600 font-semibold">{{ product.stock }} unidades restantes</p>
              </div>
              <button class="p-2 text-amber-600 hover:bg-amber-100 rounded-lg transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
              </button>
            </div>
            
            <div v-if="lowStockProducts.length === 0" class="text-center py-8">
              <div class="w-16 h-16 mx-auto mb-4 bg-emerald-50 rounded-full flex items-center justify-center">
                <svg class="w-8 h-8 text-emerald-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="text-text-medium font-medium">Todo el inventario OK</p>
              <p class="text-sm text-text-light">No hay productos críticos</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6 lg:mt-8">
        <router-link 
          to="/admin/productos/nuevo"
          class="flex flex-col items-center gap-3 p-5 bg-white border border-gray-100 rounded-2xl hover:shadow-md hover:border-emerald-200 transition-all group"
        >
          <div class="w-12 h-12 bg-gray-50 group-hover:bg-emerald-100 rounded-xl flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-400 group-hover:text-emerald-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
          </div>
          <span class="text-sm font-medium text-text-medium group-hover:text-emerald-600 transition-colors">Nuevo Producto</span>
        </router-link>

        <router-link 
          to="/admin/ordenes"
          class="flex flex-col items-center gap-3 p-5 bg-white border border-gray-100 rounded-2xl hover:shadow-md hover:border-blue-200 transition-all group"
        >
          <div class="w-12 h-12 bg-gray-50 group-hover:bg-blue-100 rounded-xl flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-400 group-hover:text-blue-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
            </svg>
          </div>
          <span class="text-sm font-medium text-text-medium group-hover:text-blue-600 transition-colors">Ver Órdenes</span>
        </router-link>

        <router-link 
          to="/admin/inventario"
          class="flex flex-col items-center gap-3 p-5 bg-white border border-gray-100 rounded-2xl hover:shadow-md hover:border-violet-200 transition-all group"
        >
          <div class="w-12 h-12 bg-gray-50 group-hover:bg-violet-100 rounded-xl flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-400 group-hover:text-violet-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
            </svg>
          </div>
          <span class="text-sm font-medium text-text-medium group-hover:text-violet-600 transition-colors">Inventario</span>
        </router-link>

        <router-link 
          to="/admin/clientes"
          class="flex flex-col items-center gap-3 p-5 bg-white border border-gray-100 rounded-2xl hover:shadow-md hover:border-rose-200 transition-all group"
        >
          <div class="w-12 h-12 bg-gray-50 group-hover:bg-rose-100 rounded-xl flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-gray-400 group-hover:text-rose-600 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
            </svg>
          </div>
          <span class="text-sm font-medium text-text-medium group-hover:text-rose-600 transition-colors">Clientes</span>
        </router-link>
      </div>

    </div><!-- End v-else content -->
  </div><!-- End main container -->
</template>

<script>
import { ref, computed, onMounted } from 'vue'
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

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ArcElement
)

export default {
  name: 'AdminDashboard',
  components: {
    Line,
    Doughnut
  },
  setup() {
    // Chart colors
    const chartColors = ['#10B981', '#3B82F6', '#F59E0B', '#8B5CF6', '#EC4899']
    
    // Stats
    const stats = ref({
      totalVentas: 0,
      totalOrdenes: 0,
      ordenesPendientes: 0,
      totalProductos: 0,
      productosActivos: 0,
      stockBajo: 0,
      totalClientes: 0,
      clientesNuevos: 0
    })

    const loading = ref(true)
    const error = ref(null)
    const selectedPeriod = ref('7D')

    // Recent orders
    const recentOrders = ref([])

    // Low stock products
    const lowStockProducts = ref([])
    
    // Top products - datos reales del backend
    const topProducts = ref([])

    // Fecha actual formateada
    const fechaActual = computed(() => {
      const options = { day: 'numeric', month: 'long', year: 'numeric' }
      return new Date().toLocaleDateString('es-CO', options)
    })

    // Sales chart data
    const salesChartData = computed(() => {
      const labels = selectedPeriod.value === '24H' 
        ? ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '23:00']
        : selectedPeriod.value === '7D'
        ? ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        : ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
      
      // Generate demo data based on period
      const generateData = () => {
        const baseValue = Math.max(stats.value.totalVentas / labels.length, 1000)
        return labels.map(() => Math.floor(baseValue * (0.5 + Math.random())))
      }

      return {
        labels,
        datasets: [{
          label: 'Ventas',
          data: generateData(),
          borderColor: '#10B981',
          backgroundColor: (context) => {
            const ctx = context.chart.ctx
            const gradient = ctx.createLinearGradient(0, 0, 0, 250)
            gradient.addColorStop(0, 'rgba(16, 185, 129, 0.3)')
            gradient.addColorStop(1, 'rgba(16, 185, 129, 0)')
            return gradient
          },
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: '#10B981',
          pointHoverBorderColor: '#fff',
          pointHoverBorderWidth: 2
        }]
      }
    })

    const salesChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1a1a1a',
          titleColor: '#fff',
          bodyColor: '#fff',
          padding: 12,
          cornerRadius: 8,
          displayColors: false,
          callbacks: {
            label: (context) => `$${context.raw.toLocaleString('es-CO')}`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { 
            color: '#9CA3AF',
            font: { size: 11 }
          }
        },
        y: {
          grid: { 
            color: '#F3F4F6',
            drawBorder: false
          },
          ticks: { 
            color: '#9CA3AF',
            font: { size: 11 },
            callback: (value) => `$${(value / 1000).toFixed(0)}k`
          }
        }
      }
    }

    // Donut chart data
    const topProductsChartData = computed(() => ({
      labels: topProducts.value.map(p => p.nombre),
      datasets: [{
        data: topProducts.value.map(p => p.ventas),
        backgroundColor: chartColors,
        borderWidth: 0,
        hoverOffset: 4
      }]
    }))

    const donutChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '75%',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1a1a1a',
          titleColor: '#fff',
          bodyColor: '#fff',
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: (context) => `$${context.raw.toLocaleString('es-CO')}`
          }
        }
      }
    }

    // Cargar estadísticas del backend
    const cargarEstadisticas = async () => {
      try {
        const response = await apiClient.get('/dashboard/estadisticas')
        stats.value = {
          totalVentas: response.data.total_ventas || 0,
          totalOrdenes: response.data.total_ordenes || 0,
          ordenesPendientes: response.data.ordenes_pendientes || 0,
          totalProductos: response.data.total_productos || 0,
          productosActivos: response.data.productos_activos || 0,
          stockBajo: response.data.stock_bajo || 0,
          totalClientes: response.data.total_clientes || 0,
          clientesNuevos: response.data.clientes_nuevos || 0
        }
      } catch (err) {
        console.error('Error al cargar estadísticas:', err)
        error.value = 'No se pudieron cargar las estadísticas'
      }
    }

    // Cargar órdenes recientes
    const cargarOrdenesRecientes = async () => {
      try {
        const response = await apiClient.get('/dashboard/ordenes/recientes?limite=5')
        recentOrders.value = response.data.map(orden => ({
          id: orden.id,
          cliente: orden.cliente_nombre || 'Cliente',
          estado: orden.estado,
          total: orden.total,
          fecha: orden.tiempo_transcurrido
        }))
      } catch (err) {
        console.error('Error al cargar órdenes recientes:', err)
      }
    }

    // Cargar productos con stock bajo
    const cargarProductosStockBajo = async () => {
      try {
        const response = await apiClient.get('/dashboard/productos/stock-bajo?umbral=5&limite=10')
        lowStockProducts.value = response.data.map(producto => ({
          id: producto.id,
          nombre: producto.nombre,
          stock: producto.stock_actual,
          imagen: producto.imagen_url || ''
        }))
      } catch (err) {
        console.error('Error al cargar productos con stock bajo:', err)
      }
    }

    // Cargar todos los datos
    const cargarDatos = async () => {
      loading.value = true
      error.value = null
      
      await Promise.all([
        cargarEstadisticas(),
        cargarOrdenesRecientes(),
        cargarProductosStockBajo()
      ])
      
      loading.value = false
    }

    // Cargar datos al montar
    onMounted(() => {
      cargarDatos()
    })

    const formatNumber = (num) => {
      return new Intl.NumberFormat('es-CO').format(num || 0)
    }

    // Status styles
    const getStatusClass = (status) => {
      const classes = {
        'PENDIENTE': 'bg-amber-100 text-amber-700',
        'CONFIRMADA': 'bg-blue-100 text-blue-700',
        'EN_PROCESO': 'bg-violet-100 text-violet-700',
        'ENVIADA': 'bg-indigo-100 text-indigo-700',
        'COMPLETADA': 'bg-emerald-100 text-emerald-700',
        'CANCELADA': 'bg-gray-100 text-gray-500'
      }
      return classes[status] || 'bg-gray-100 text-gray-600'
    }

    const getStatusLabel = (status) => {
      const labels = {
        'PENDIENTE': 'Pendiente',
        'CONFIRMADA': 'Confirmada',
        'EN_PROCESO': 'En proceso',
        'ENVIADA': 'Enviada',
        'COMPLETADA': 'Completada',
        'CANCELADA': 'Cancelada'
      }
      return labels[status] || status
    }

    return {
      stats,
      recentOrders,
      lowStockProducts,
      topProducts,
      loading,
      error,
      selectedPeriod,
      fechaActual,
      chartColors,
      salesChartData,
      salesChartOptions,
      topProductsChartData,
      donutChartOptions,
      formatNumber,
      getStatusClass,
      getStatusLabel,
      cargarDatos
    }
  }
}
</script>
