<template>
  <div class="space-y-6">
    <!-- Header con Filtros Unificados -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      <!-- Título y Botón CTA -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h2 class="text-2xl font-bold text-text-dark">Gestión de Productos</h2>
          <p class="text-text-light text-sm mt-1">{{ productos.length }} productos en inventario</p>
        </div>
        <button 
          @click="openCreateModal"
          class="inline-flex w-full sm:w-auto justify-center items-center gap-2 bg-[#D81B60] hover:bg-[#C2185B] text-white font-medium text-sm px-6 py-3 rounded-lg transition-all duration-300 shadow-sm hover:shadow-md"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nuevo Producto
        </button>
      </div>

      <!-- Tabs -->
      <div class="flex gap-4 mb-6 border-b border-text-dark/10">
        <button
          @click="activeTab = 'activos'"
          :class="activeTab === 'activos' ? 'border-b-2 border-[#D81B60] text-[#D81B60]' : 'text-text-medium hover:text-text-dark'"
          class="pb-3 font-medium text-sm transition-colors"
        >
          Productos Activos ({{ productosActivos.length }})
        </button>
        <button
          @click="activeTab = 'inactivos'"
          :class="activeTab === 'inactivos' ? 'border-b-2 border-[#D81B60] text-[#D81B60]' : 'text-text-medium hover:text-text-dark'"
          class="pb-3 font-medium text-sm transition-colors"
        >
          Productos Inactivos ({{ productosInactivos.length }})
        </button>
      </div>

      <!-- Barra de Filtros Cohesiva -->
      <div class="flex flex-col lg:flex-row gap-3">
        <!-- Search -->
        <div class="flex-1 relative">
          <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por nombre, SKU o descripción..."
            class="w-full pl-10 pr-4 py-2.5 text-sm bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all"
          >
        </div>

        <!-- Category Filter -->
        <select 
          v-model="filterCategory"
          class="w-full lg:w-auto px-3 py-2.5 text-sm bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white min-w-[160px] transition-all"
        >
          <option value="">Todas las categorías</option>
          <option value="extensiones">Extensiones</option>
          <option value="pelucas">Pelucas</option>
          <option value="accesorios">Accesorios</option>
        </select>

        <!-- Stock Filter -->
        <select 
          v-model="filterStock"
          class="w-full lg:w-auto px-3 py-2.5 text-sm bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white min-w-[140px] transition-all"
        >
          <option value="">Todo el stock</option>
          <option value="available">Disponible</option>
          <option value="low">Stock bajo</option>
          <option value="out">Agotado</option>
        </select>

        <!-- Refresh button -->
        <button
          @click="loadProducts"
          class="w-full lg:w-auto px-3 py-2.5 bg-[#FAFAFA] hover:bg-gray-100 border border-text-dark/10 rounded-lg transition-all"
          :disabled="loading"
          title="Actualizar"
        >
          <svg class="w-4 h-4 text-text-medium" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      <!-- Bulk Actions -->
      <div v-if="selectedCount > 0" class="mt-4 flex flex-col lg:flex-row lg:items-center gap-3 rounded-xl border border-[#C9A962]/30 bg-[#FAF5F2] px-4 py-3">
        <div class="text-sm text-text-dark">
          <span class="font-semibold">{{ selectedCount }}</span> seleccionados
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            @click="openBulkConfirm('activar')"
            class="px-3 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors"
            :disabled="bulkLoading"
          >
            Activar
          </button>
          <button
            @click="openBulkConfirm('inactivar')"
            class="px-3 py-2 text-xs font-semibold rounded-lg bg-gray-800 text-white hover:bg-black transition-colors"
            :disabled="bulkLoading"
          >
            Inactivar
          </button>
          <button
            @click="openCategoryModal"
            class="px-3 py-2 text-xs font-semibold rounded-lg border border-text-dark/20 text-text-dark hover:border-text-dark transition-colors"
            :disabled="bulkLoading"
          >
            Editar categoria
          </button>
          <button
            @click="openStockModal"
            class="px-3 py-2 text-xs font-semibold rounded-lg border border-text-dark/20 text-text-dark hover:border-text-dark transition-colors"
            :disabled="bulkLoading"
          >
            Ajustar stock
          </button>
          <button
            @click="openBulkConfirm('eliminar')"
            class="px-3 py-2 text-xs font-semibold rounded-lg bg-red-600 text-white hover:bg-red-700 transition-colors"
            :disabled="bulkLoading"
          >
            Eliminar
          </button>
          <button
            @click="clearSelection"
            class="px-3 py-2 text-xs font-semibold rounded-lg text-text-medium hover:text-text-dark transition-colors"
            :disabled="bulkLoading"
          >
            Limpiar
          </button>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
      <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
      <div class="flex-1">
        <p class="text-red-800 font-medium">Error al cargar productos</p>
        <p class="text-red-600 text-sm">{{ error }}</p>
      </div>
      <button @click="loadProducts" class="text-red-600 hover:text-red-800 font-medium text-sm">
        Reintentar
      </button>
    </div>

    <!-- Products Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <!-- Loading State -->
      <div v-if="loading" class="p-8">
        <div class="animate-pulse space-y-4">
          <div v-for="i in 5" :key="i" class="flex items-center gap-4">
            <div class="w-16 h-16 bg-gray-200 rounded-xl"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-200 rounded w-1/3"></div>
              <div class="h-3 bg-gray-200 rounded w-1/4"></div>
            </div>
            <div class="h-8 bg-gray-200 rounded w-20"></div>
          </div>
        </div>
      </div>

      <!-- Table - Estilo Smart Inventory -->
      <div v-else class="overflow-x-auto">
        <table class="w-full min-w-[700px]">
          <thead class="bg-[#FAFAFA] border-b border-text-dark/5">
            <tr>
              <th class="px-4 py-3.5 text-left text-xs font-semibold text-text-medium uppercase tracking-wide w-10">
                <input
                  type="checkbox"
                  class="w-4 h-4 rounded border-text-dark/20 text-[#D81B60] focus:ring-[#D81B60]/30"
                  :checked="allDisplayedSelected"
                  :indeterminate.prop="someDisplayedSelected"
                  @change="toggleSelectAll"
                />
              </th>
              <th class="px-6 py-3.5 text-left text-xs font-semibold text-text-medium uppercase tracking-wide">Producto</th>
              <th class="px-6 py-3.5 text-right text-xs font-semibold text-text-medium uppercase tracking-wide">Precio</th>
              <th class="px-6 py-3.5 text-left text-xs font-semibold text-text-medium uppercase tracking-wide">Stock</th>
              <th class="px-6 py-3.5 text-left text-xs font-semibold text-text-medium uppercase tracking-wide">Estado</th>
              <th class="px-6 py-3.5 text-right text-xs font-semibold text-text-medium uppercase tracking-wide">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-text-dark/5">
            <tr v-for="producto in displayedProducts" :key="producto.id" class="hover:bg-[#FAFAFA] transition-colors">
              <td class="px-4 py-4">
                <input
                  type="checkbox"
                  class="w-4 h-4 rounded border-text-dark/20 text-[#D81B60] focus:ring-[#D81B60]/30"
                  :checked="isSelected(producto.id)"
                  @change="toggleSelection(producto.id)"
                />
              </td>
              <!-- Product - COLUMNA PRINCIPAL CON JERARQUÍA VISUAL -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-4">
                  <!-- Thumbnail Cuadrado (56x56px) -->
                  <div class="w-14 h-14 bg-[#F5F5F5] rounded-lg overflow-hidden flex-shrink-0 border border-text-dark/5 relative">
                    <img 
                      v-if="getProductMediaUrl(producto)"
                      :src="getProductMediaUrl(producto)" 
                      :alt="producto.nombre"
                      class="w-full h-full object-cover"
                      @error="handleImageError"
                    >
                    <!-- Play icon para videos -->
                    <div v-if="isVideo(getImageUrl(producto.imagen_principal))" class="absolute inset-0 flex items-center justify-center bg-black/30">
                      <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                      </svg>
                    </div>
                    <div v-else-if="!getProductMediaUrl(producto)" class="w-full h-full flex items-center justify-center">
                      <svg class="w-6 h-6 text-text-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>
                  
                  <!-- Jerarquía de Texto -->
                  <div class="min-w-0 flex-1">
                    <!-- Línea 1: Nombre (Negrita, Oscuro) -->
                    <p class="font-semibold text-[#111827] text-sm truncate mb-0.5">{{ producto.nombre }}</p>
                    
                    <!-- Línea 2: SKU + Categoría (Pequeño, Gris) -->
                    <div class="flex items-center gap-2 text-xs text-[#6B7280]">
                      <span class="font-mono">SKU: {{ producto.codigo }}</span>
                      <span class="text-text-light">•</span>
                      <span>{{ getCategoryLabel(producto) }}</span>
                    </div>
                  </div>
                </div>
              </td>
              
              <!-- Precio - ALINEADO A LA DERECHA, FUENTE TABULAR -->
              <td class="px-6 py-4 text-right">
                <span class="font-semibold text-text-dark text-sm tabular-nums">${{ formatNumber(producto.precio_monto) }}</span>
              </td>
              
              <!-- Stock - INDICADORES VISUALES DE SALUD -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <template v-if="getTotalStock(producto) > 20">
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span class="text-green-700 font-medium text-sm tabular-nums">{{ getTotalStock(producto) }}</span>
                  </template>
                  <template v-else-if="getTotalStock(producto) > 0 && getTotalStock(producto) <= 20">
                    <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                    <span class="text-orange-700 font-medium text-sm tabular-nums">{{ getTotalStock(producto) }}</span>
                  </template>
                  <template v-else>
                    <span class="px-2.5 py-1 bg-red-50 text-red-700 text-xs font-medium rounded-md">Sin Stock</span>
                  </template>
                </div>
              </td>
              
              <!-- Estado -->
              <td class="px-6 py-4">
                <span 
                  :class="producto.activo ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-600'"
                  class="px-2.5 py-1 text-xs font-medium rounded-md"
                >
                  {{ producto.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              
              <!-- Actions -->
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button 
                    @click="openEditModal(producto)"
                    class="p-2 text-gray-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="Editar"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    @click="openB2BModal(producto)"
                    class="p-2 text-gray-500 hover:text-[#8B7355] hover:bg-[#FAF5F2] rounded-lg transition-colors"
                    title="Descuentos Mayoristas"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 14l6-6m-7.5 2.5a2.5 2.5 0 115 0 2.5 2.5 0 01-5 0zm7 7a2.5 2.5 0 115 0 2.5 2.5 0 01-5 0z" />
                    </svg>
                  </button>
                  <button 
                    @click="confirmDelete(producto)"
                    :class="activeTab === 'inactivos' ? 'text-red-600 hover:bg-red-50' : 'text-text-medium hover:text-red-600 hover:bg-red-50'"
                    class="p-2 rounded-lg transition-all"
                    :title="activeTab === 'inactivos' ? 'Eliminar permanentemente' : 'Desactivar'"
                    :disabled="deleting === producto.id"
                  >
                    <svg v-if="deleting !== producto.id" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Empty State -->
            <tr v-if="displayedProducts.length === 0 && !loading">
              <td colspan="6" class="px-6 py-16 text-center">
                <div class="flex flex-col items-center">
                  <svg class="w-16 h-16 text-text-light mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                  <p class="text-text-medium font-medium mb-2">
                    {{ productos.length === 0 ? 'No hay productos en el inventario' : 'No se encontraron productos' }}
                  </p>
                  <p class="text-text-light text-sm mb-4">
                    {{ productos.length === 0 ? 'Comienza agregando tu primer producto' : 'Intenta ajustar los filtros de búsqueda' }}
                  </p>
                  <button 
                    v-if="productos.length === 0"
                    @click="openCreateModal"
                    class="text-[#D81B60] font-medium hover:underline text-sm"
                  >
                    Agregar primer producto
                  </button>
                  <button 
                    v-else
                    @click="clearFilters"
                    class="text-[#D81B60] font-medium hover:underline text-sm"
                  >
                    Limpiar filtros
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="productos.length > 0" class="flex items-center justify-between p-4 border-t border-text-dark/5 bg-[#FAFAFA]">
        <p class="text-sm text-text-medium">
          Mostrando <span class="font-medium text-text-dark">{{ displayedProducts.length }}</span> de <span class="font-medium text-text-dark">{{ productos.length }}</span> productos
        </p>
        <div class="flex items-center gap-2">
          <button 
            class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50"
            :disabled="currentPage === 1"
            @click="currentPage--"
          >
            Anterior
          </button>
          <button 
            class="px-4 py-2 text-sm font-medium text-white bg-brand-600 rounded-lg hover:bg-brand-700"
            @click="currentPage++"
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>

    <!-- Edit/Create Product Modal -->
    <ProductoEditModal 
      :visible="showEditModal"
      :product-id="editingProductId"
      @close="closeEditModal"
      @updated="handleProductUpdated"
      @created="handleProductUpdated"
    />

    <!-- Volume Discounts Modal -->
    <div v-if="showB2BModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div class="bg-[#FAFAFA] rounded-3xl max-w-2xl w-full p-6 sm:p-7 space-y-5 border border-black/5 shadow-[0_25px_70px_rgba(0,0,0,0.18)]">
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1">
            <h3 class="text-lg sm:text-xl font-luxury text-text-dark">Descuentos por volumen · Mayoristas</h3>
            <p class="text-sm text-text-medium mt-2">
              {{ b2bProduct?.nombre }}
            </p>
            
            <div v-if="b2bVariants.length" class="mt-5 pt-5 border-t border-text-dark/5">
              <p class="text-[10px] font-semibold uppercase tracking-[0.15em] text-text-light mb-2">Configurar descuentos para:</p>
              <select
                v-model="b2bTargetKey"
                @change="handleB2BTargetChange"
                class="w-full px-4 py-3 border border-text-dark/15 rounded-xl text-sm font-medium bg-white hover:border-text-dark/30 focus:outline-none focus:border-[#D81B60] focus:ring-2 focus:ring-[#D81B60]/10 transition-all duration-200"
              >
                <option value="producto" class="font-semibold">Producto base (todas las variantes)</option>
                <option v-for="variante in b2bVariants" :key="variante.id" :value="variante.id" class="font-medium">
                  {{ getVarianteLabel(variante) }}
                </option>
              </select>
              <p class="text-[10px] text-text-light mt-2">
                Mínimo requerido: <span class="font-semibold text-text-dark">{{ getB2BTargetMin() }} unidades</span>
              </p>
            </div>
            <div v-else class="mt-4 p-3 bg-blue-50 rounded-lg">
              <p class="text-[11px] text-blue-900 font-medium">Este producto no tiene variantes.</p>
            </div>
          </div>
          <button @click="closeB2BModal" class="flex-shrink-0 text-text-light hover:text-text-dark transition-colors mt-1">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div v-if="b2bLoading" class="py-8 text-center text-text-light">Cargando...</div>

        <div v-else class="space-y-3">
          <div class="grid grid-cols-12 gap-3 text-[11px] font-semibold text-text-medium uppercase tracking-[0.14em]">
            <div class="col-span-5">Cantidad mínima</div>
            <div class="col-span-5">Descuento (%)</div>
            <div class="col-span-2 text-right">Acción</div>
          </div>

          <div v-for="(tier, index) in b2bTiers" :key="index" class="grid grid-cols-12 gap-3 items-center">
            <div class="col-span-5">
              <input
                v-model.number="tier.cantidad_minima"
                type="number"
                min="1"
                class="w-full px-3 py-2.5 border border-text-dark/10 rounded-lg text-sm focus:outline-none focus:border-text-dark/30 bg-white"
              >
            </div>
            <div class="col-span-5">
              <input
                v-model.number="tier.descuento_porcentaje"
                type="number"
                min="0"
                max="90"
                class="w-full px-3 py-2.5 border border-text-dark/10 rounded-lg text-sm focus:outline-none focus:border-text-dark/30 bg-white"
              >
            </div>
            <div class="col-span-2 flex justify-end">
              <button
                @click="removeB2BTier(index)"
                class="px-2 py-1 text-[11px] text-text-light hover:text-text-dark"
                title="Eliminar tramo"
              >
                Quitar
              </button>
            </div>
          </div>

          <button
            type="button"
            @click="addB2BTier"
            class="text-sm text-text-dark font-medium hover:text-black"
          >
            + Agregar tramo
          </button>
        </div>

        <p v-if="b2bError" class="text-sm text-red-600">{{ b2bError }}</p>

        <div class="flex justify-end gap-3 pt-2">
          <button
            @click="closeB2BModal"
            class="px-4 py-2 text-sm text-text-dark border border-text-dark/20 rounded-lg hover:border-text-dark/40"
          >
            Cancelar
          </button>
          <button
            @click="saveB2BTiers"
            class="px-4 py-2 text-sm text-white bg-text-dark hover:bg-black rounded-lg"
            :disabled="b2bLoading"
          >
            Guardar
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Eliminar Producto</h3>
            <p class="text-gray-500 text-sm">Esta acción no se puede deshacer</p>
          </div>
        </div>
        
        <p class="text-gray-700">
          <template v-if="productToDelete?.activo">
            ¿Estás seguro de que deseas eliminar <span class="font-semibold">{{ productToDelete?.nombre }}</span>? Se marcará como inactivo.
          </template>
          <template v-else>
            ¿Estás seguro de que deseas <span class="text-red-600 font-semibold">ELIMINAR PERMANENTEMENTE</span> <span class="font-semibold">{{ productToDelete?.nombre }}</span> de la base de datos? Esta acción no se puede deshacer.
          </template>
        </p>
        
        <div class="flex gap-3 justify-end">
          <button 
            @click="showDeleteModal = false"
            class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
          >
            Cancelar
          </button>
          <button 
            @click="deleteProduct"
            :disabled="deleting"
            class="px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            {{ deleting ? 'Eliminando...' : 'Eliminar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Bulk Confirmation Modal -->
    <div v-if="bulkConfirm.open" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Confirmar accion</h3>
            <p class="text-gray-500 text-sm">{{ bulkConfirm.message }}</p>
          </div>
        </div>
        <div class="flex gap-3 justify-end">
          <button
            @click="closeBulkConfirm"
            class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="applyBulkAction"
            :disabled="bulkLoading"
            class="px-4 py-2 text-white bg-gray-900 hover:bg-black rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            {{ bulkLoading ? 'Aplicando...' : 'Confirmar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Bulk Category Modal -->
    <div v-if="bulkCategory.open" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Editar categoria</h3>
          <p class="text-gray-500 text-sm">Aplica una categoria a {{ selectedCount }} productos.</p>
        </div>
        <div class="space-y-3">
          <select
            v-model="bulkCategory.value"
            class="w-full px-3 py-2.5 text-sm bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white"
          >
            <option value="">Selecciona una categoria</option>
            <option v-for="cat in categoryOptions" :key="cat" :value="cat">{{ cat }}</option>
            <option value="__custom">Otra categoria...</option>
          </select>
          <input
            v-if="bulkCategory.value === '__custom'"
            v-model="bulkCategory.custom"
            type="text"
            placeholder="Nueva categoria"
            class="w-full px-3 py-2.5 text-sm bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white"
          />
        </div>
        <div class="flex gap-3 justify-end">
          <button
            @click="closeCategoryModal"
            class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="confirmCategoryBulk"
            :disabled="bulkLoading"
            class="px-4 py-2 text-white bg-gray-900 hover:bg-black rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            {{ bulkLoading ? 'Aplicando...' : 'Aplicar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Bulk Stock Modal -->
    <div v-if="bulkStock.open" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Ajustar stock</h3>
          <p class="text-gray-500 text-sm">Aplica un ajuste a {{ selectedCount }} productos.</p>
        </div>
        <div class="space-y-3">
          <div class="flex gap-2">
            <button
              @click="bulkStock.mode = 'add'"
              :class="bulkStock.mode === 'add' ? 'bg-[#D81B60] text-white' : 'bg-gray-100 text-gray-700'"
              class="px-3 py-2 text-xs font-semibold rounded-lg transition-colors"
            >
              Sumar
            </button>
            <button
              @click="bulkStock.mode = 'subtract'"
              :class="bulkStock.mode === 'subtract' ? 'bg-[#D81B60] text-white' : 'bg-gray-100 text-gray-700'"
              class="px-3 py-2 text-xs font-semibold rounded-lg transition-colors"
            >
              Restar
            </button>
            <button
              @click="bulkStock.mode = 'set'"
              :class="bulkStock.mode === 'set' ? 'bg-[#D81B60] text-white' : 'bg-gray-100 text-gray-700'"
              class="px-3 py-2 text-xs font-semibold rounded-lg transition-colors"
            >
              Fijar
            </button>
          </div>
          <input
            v-model.number="bulkStock.value"
            type="number"
            min="0"
            class="w-full px-3 py-2.5 text-sm bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white"
            placeholder="Cantidad"
          />
        </div>
        <div class="flex gap-3 justify-end">
          <button
            @click="closeStockModal"
            class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="confirmStockBulk"
            :disabled="bulkLoading"
            class="px-4 py-2 text-white bg-gray-900 hover:bg-black rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            {{ bulkLoading ? 'Aplicando...' : 'Aplicar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- History Warning Modal (Elegant) -->
    <div v-if="showHistoryWarningModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gradient-to-br from-white to-gray-50 rounded-3xl max-w-lg w-full shadow-2xl transform transition-all">
        <!-- Header con icono elegante -->
        <div class="relative overflow-hidden rounded-t-3xl bg-gradient-to-r from-amber-500 to-orange-500 p-8">
          <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
          <div class="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full -ml-12 -mb-12"></div>
          <div class="relative flex items-center gap-4">
            <div class="w-16 h-16 bg-white/20 backdrop-blur-xl rounded-2xl flex items-center justify-center shadow-lg">
              <svg class="w-9 h-9 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="text-2xl font-bold text-white drop-shadow-sm">Producto con Historial</h3>
              <p class="text-white/90 text-sm mt-1">Protección de datos activa</p>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="p-8 space-y-6">
          <!-- Producto Info -->
          <div class="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 bg-gradient-to-br from-pink-500 to-rose-500 rounded-xl flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-xs text-gray-500 font-medium uppercase tracking-wider">Producto</p>
                <p class="text-gray-900 font-semibold text-lg">{{ historyWarningData?.productoNombre }}</p>
              </div>
            </div>
          </div>

          <!-- Stats -->
          <div class="bg-gradient-to-br from-amber-50 to-orange-50 rounded-2xl p-5 border border-amber-200">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl flex items-center justify-center shadow-md">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-3xl font-bold text-gray-900">{{ historyWarningData?.numOrdenes }}</p>
                <p class="text-sm text-gray-600 font-medium">{{ historyWarningData?.numOrdenes === 1 ? 'Orden registrada' : 'Órdenes registradas' }}</p>
              </div>
            </div>
          </div>

          <!-- Mensaje explicativo -->
          <div class="space-y-3">
            <div class="flex items-start gap-3">
              <div class="w-6 h-6 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-gray-700 leading-relaxed">
                  Este producto tiene <strong class="text-gray-900">historial de ventas</strong> y no puede eliminarse permanentemente para preservar la <strong class="text-gray-900">integridad del sistema</strong>.
                </p>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <div class="w-6 h-6 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg class="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-gray-700 leading-relaxed">
                  <strong class="text-gray-900">Recomendación:</strong> Mantén el producto <span class="text-amber-600 font-semibold">desactivado</span> para que no aparezca en la tienda pero se conserve el historial.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer con botón -->
        <div class="px-8 pb-8">
          <button
            @click="showHistoryWarningModal = false; historyWarningData = null"
            class="w-full py-4 bg-gradient-to-r from-gray-800 to-gray-900 hover:from-gray-900 hover:to-black text-white font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            Entendido
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { productosService } from '../../services/productos'
import { getImageUrl } from '../../services/api'
import ProductoEditModal from './ProductoEditModal.vue'

export default {
  name: 'AdminProductos',
  components: {
    ProductoEditModal
  },
  setup() {
    const loading = ref(true)
    const productos = ref([])
    const error = ref(null)
    const searchQuery = ref('')
    const filterCategory = ref('')
    const filterStock = ref('')
    const currentPage = ref(1)
    const deleting = ref(null)
    const showDeleteModal = ref(false)
    const productToDelete = ref(null)
    const showEditModal = ref(false)
    const editingProductId = ref(null)
    const videoPosters = ref({})
    const activeTab = ref('activos')
    const showHistoryWarningModal = ref(false)
    const historyWarningData = ref(null)
    const showB2BModal = ref(false)
    const b2bProduct = ref(null)
    const b2bTiers = ref([])
    const b2bLoading = ref(false)
    const b2bError = ref('')
    const b2bVariants = ref([])
    const b2bTargetKey = ref('producto')
    const selectedIds = ref([])
    const bulkLoading = ref(false)
    const bulkConfirm = ref({ open: false, action: '', message: '' })
    const bulkCategory = ref({ open: false, value: '', custom: '' })
    const bulkStock = ref({ open: false, mode: 'add', value: 0 })

    const productosActivos = computed(() => {
      return productos.value.filter(p => p.activo)
    })

    const productosInactivos = computed(() => {
      return productos.value.filter(p => !p.activo)
    })

    const filteredProducts = computed(() => {
      let result = activeTab.value === 'activos' ? productosActivos.value : productosInactivos.value

      // Search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(p => 
          p.nombre.toLowerCase().includes(query) ||
          p.codigo.toLowerCase().includes(query) ||
          (p.descripcion && p.descripcion.toLowerCase().includes(query))
        )
      }

      // Category filter
      if (filterCategory.value) {
        result = result.filter(p => {
          const cat = getCategoryLabel(p).toLowerCase()
          return cat === filterCategory.value.toLowerCase()
        })
      }

      // Stock filter (base + variantes)
      if (filterStock.value === 'available') {
        result = result.filter(p => getTotalStock(p) > getTotalStockMin(p))
      } else if (filterStock.value === 'low') {
        result = result.filter(p => getTotalStock(p) > 0 && getTotalStock(p) <= getTotalStockMin(p))
      } else if (filterStock.value === 'out') {
        result = result.filter(p => getTotalStock(p) === 0)
      }

      return result
    })

    const displayedProducts = computed(() => {
      return filteredProducts.value
    })

    const selectedCount = computed(() => selectedIds.value.length)
    const displayedIds = computed(() => displayedProducts.value.map(p => p.id))
    const allDisplayedSelected = computed(() => {
      return displayedIds.value.length > 0 && displayedIds.value.every(id => selectedIds.value.includes(id))
    })
    const someDisplayedSelected = computed(() => {
      return displayedIds.value.some(id => selectedIds.value.includes(id)) && !allDisplayedSelected.value
    })
    const categoryOptions = computed(() => {
      const set = new Set()
      productos.value.forEach(p => {
        const label = getCategoryLabel(p)
        if (label) set.add(label)
      })
      return Array.from(set).sort((a, b) => a.localeCompare(b))
    })

    const formatNumber = (num) => {
      return new Intl.NumberFormat('es-CO').format(num)
    }

    const getTotalStock = (producto) => {
      const base = Number(producto?.stock_actual ?? 0)
      const variantes = Array.isArray(producto?.variantes)
        ? producto.variantes.filter((v) => v?.color || v?.largo)
        : []
      const variantesStock = variantes.reduce((sum, v) => sum + Number(v?.stock_actual ?? 0), 0)
      return base + variantesStock
    }

    const getTotalStockMin = (producto) => {
      const base = Number(producto?.stock_minimo ?? 0)
      const variantes = Array.isArray(producto?.variantes)
        ? producto.variantes.filter((v) => v?.color || v?.largo)
        : []
      const variantesMin = variantes.reduce((sum, v) => sum + Number(v?.stock_minimo ?? 0), 0)
      return base + variantesMin
    }

    const getStockClass = (stock, stockMinimo) => {
      if (stock === 0) return 'text-red-600'
      if (stock <= stockMinimo) return 'text-orange-600'
      return 'text-gray-900'
    }

    const formatAttributeValue = (value) => {
      if (!value) return ''
      return value
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ')
    }

    const getVarianteLabel = (variante) => {
      if (!variante) return 'Variante'
      const colorLabel = variante.color ? formatAttributeValue(variante.color) : 'Sin color'
      const largoLabel = variante.largo ? `${variante.largo}"` : ''
      const labelParts = [colorLabel]
      if (largoLabel) labelParts.push(largoLabel)
      return labelParts.join(' · ')
    }

    const getB2BTargetMin = () => {
      if (b2bTargetKey.value === 'producto') {
        return Number(b2bProduct.value?.cantidad_minima_mayorista || 1)
      }
      const variante = b2bVariants.value.find(v => String(v.id) === String(b2bTargetKey.value))
      return Number(variante?.cantidad_minima_mayorista || b2bProduct.value?.cantidad_minima_mayorista || 1)
    }

    const loadB2BTiers = async () => {
      if (!b2bProduct.value) return
      b2bLoading.value = true
      b2bError.value = ''

      try {
        const minimo = getB2BTargetMin()
        const data = b2bTargetKey.value === 'producto'
          ? await productosService.getB2BDescuentos(b2bProduct.value.id)
          : await productosService.getB2BDescuentosVariante(b2bTargetKey.value)

        const tiers = Array.isArray(data) ? data : []
        b2bTiers.value = tiers.length
          ? tiers.map((t) => ({
              cantidad_minima: Number(t.cantidad_minima || minimo),
              descuento_porcentaje: Number(t.descuento_porcentaje || 0)
            }))
          : []
      } catch (err) {
        b2bError.value = 'No se pudieron cargar los descuentos por volumen.'
        b2bTiers.value = []
      } finally {
        b2bLoading.value = false
      }
    }

    const getCategoryLabel = (producto) => {
      // Intentar obtener categoría de diferentes fuentes
      if (producto.categoria) return producto.categoria
      if (producto.metodo) {
        const metodoLabels = {
          'clip_in': 'Extensiones',
          'tape_in': 'Extensiones',
          'keratin_bond': 'Extensiones',
          'wig': 'Pelucas',
          'frontal': 'Pelucas',
          'closure': 'Pelucas',
        }
        return metodoLabels[producto.metodo] || 'Extensiones'
      }
      return 'Sin categoría'
    }

    const isVideo = (url) => {
      if (!url) return false
      const cleanUrl = url.split('?')[0].toLowerCase()
      return ['.mp4', '.webm', '.ogg', '.mov'].some(ext => cleanUrl.endsWith(ext))
    }

    const createVideoPoster = (url) => {
      return new Promise((resolve) => {
        try {
          const video = document.createElement('video')
          video.src = url
          video.muted = true
          video.playsInline = true
          video.crossOrigin = 'anonymous'

          const onError = () => resolve(null)

          video.addEventListener('error', onError, { once: true })
          video.addEventListener('loadeddata', () => {
            const seekTo = Math.min(1, video.duration || 1)
            try {
              video.currentTime = seekTo
            } catch {
              resolve(null)
            }
          }, { once: true })

          video.addEventListener('seeked', () => {
            try {
              const canvas = document.createElement('canvas')
              canvas.width = video.videoWidth || 120
              canvas.height = video.videoHeight || 120
              const ctx = canvas.getContext('2d')
              if (!ctx) return resolve(null)
              ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
              resolve(canvas.toDataURL('image/jpeg', 0.82))
            } catch {
              resolve(null)
            }
          }, { once: true })
        } catch {
          resolve(null)
        }
      })
    }

    const ensureVideoPoster = async (url) => {
      if (videoPosters.value[url]) return
      const poster = await createVideoPoster(url)
      if (poster) {
        videoPosters.value = { ...videoPosters.value, [url]: poster }
      }
    }

    const getProductMediaUrl = (producto) => {
      const url = getImageUrl(producto?.imagen_principal)
      if (!url) return ''
      if (isVideo(url)) {
        ensureVideoPoster(url)
        return videoPosters.value[url] || ''
      }
      return url
    }

    const handleImageError = (e) => {
      e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f3f4f6" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em" fill="%239ca3af" font-size="12"%3ESin Imagen%3C/text%3E%3C/svg%3E'
    }

    const openCreateModal = () => {
      editingProductId.value = null
      showEditModal.value = true
    }

    const openEditModal = (producto) => {
      editingProductId.value = producto.id
      showEditModal.value = true
    }

    const closeEditModal = () => {
      showEditModal.value = false
      editingProductId.value = null
    }

    const handleProductUpdated = async () => {
      // Recargar lista de productos después de editar/crear
      await loadProducts()
    }

    const openB2BModal = async (producto) => {
      b2bProduct.value = producto
      showB2BModal.value = true
      b2bError.value = ''
      b2bLoading.value = true
      b2bTargetKey.value = 'producto'
      b2bVariants.value = []
      try {
        const detalle = await productosService.getProducto(producto.id)
        const variantes = Array.isArray(detalle?.variantes) ? detalle.variantes : []
        // Excluir variantes sin atributos (la base se configura en "Producto base")
        b2bVariants.value = variantes.filter(v => v && v.activo !== false && (v.color || v.largo))
        await loadB2BTiers()
      } catch (err) {
        b2bError.value = 'No se pudieron cargar los descuentos por volumen.'
        b2bTiers.value = []
      } finally {
        b2bLoading.value = false
      }
    }

    const closeB2BModal = () => {
      showB2BModal.value = false
      b2bProduct.value = null
      b2bTiers.value = []
      b2bVariants.value = []
      b2bTargetKey.value = 'producto'
      b2bError.value = ''
    }

    const handleB2BTargetChange = async () => {
      await loadB2BTiers()
    }

    const addB2BTier = () => {
      b2bTiers.value = [
        ...b2bTiers.value,
        { cantidad_minima: 1, descuento_porcentaje: 0 }
      ]
    }

    const removeB2BTier = (index) => {
      b2bTiers.value = b2bTiers.value.filter((_, i) => i !== index)
    }

    const saveB2BTiers = async () => {
      if (!b2bProduct.value) return
      const payload = b2bTiers.value
        .map((t, idx) => ({
          cantidad_minima: Number(t.cantidad_minima || 0),
          descuento_porcentaje: Number(t.descuento_porcentaje || 0),
          activo: true,
          orden: idx
        }))
        .filter(t => t.cantidad_minima > 0)

      if (payload.length) {
        const cantidades = payload.map(t => t.cantidad_minima)
        const unique = new Set(cantidades)
        if (unique.size !== cantidades.length) {
          b2bError.value = 'No se permiten cantidades mínimas duplicadas.'
          return
        }
      }

      b2bLoading.value = true
      b2bError.value = ''
      try {
        if (b2bTargetKey.value === 'producto') {
          await productosService.updateB2BDescuentos(b2bProduct.value.id, payload)
        } else {
          await productosService.updateB2BDescuentosVariante(b2bTargetKey.value, payload)
        }
        await loadProducts()
        closeB2BModal()
      } catch (err) {
        b2bError.value = err?.response?.data?.detail || 'No se pudieron guardar los descuentos.'
      } finally {
        b2bLoading.value = false
      }
    }

    const confirmDelete = (producto) => {
      productToDelete.value = producto
      showDeleteModal.value = true
    }

    const deleteProduct = async () => {
      if (!productToDelete.value) return
      
      deleting.value = productToDelete.value.id
      const productoId = productToDelete.value.id
      const productoNombre = productToDelete.value.nombre
      const esActivo = productToDelete.value.activo
      
      try {
        if (esActivo) {
          // Si está activo, solo desactivar (soft delete)
          await productosService.eliminar(productoId)
          // Actualizar el estado en el array local sin remover
          const producto = productos.value.find(p => p.id === productoId)
          if (producto) {
            producto.activo = false
          }
          console.log(`✓ ${productoNombre} desactivado correctamente`)
        } else {
          // Si está inactivo, intentar eliminar permanentemente (hard delete)
          await productosService.eliminarPermanentemente(productoId)
          // Remover completamente de la lista
          productos.value = productos.value.filter(p => p.id !== productoId)
          console.log(`✓ ${productoNombre} eliminado permanentemente`)
        }
        
        // Cerrar modal
        showDeleteModal.value = false
        productToDelete.value = null
        
      } catch (err) {
        console.error('Error deleting product:', err)
        
        // Si el error es 400, es porque el producto tiene historial de órdenes
        if (err.response?.status === 400) {
          // Cerrar modal de confirmación
          showDeleteModal.value = false
          
          // Extraer el número de órdenes del mensaje de error
          const errorMsg = err.response.data.detail || ''
          const ordenesMatch = errorMsg.match(/(\d+)\s+órdenes?/i)
          const numOrdenes = ordenesMatch ? parseInt(ordenesMatch[1]) : 0
          
          // Mostrar modal elegante con información del historial
          historyWarningData.value = {
            productoNombre: productoNombre,
            numOrdenes: numOrdenes,
            mensaje: errorMsg
          }
          showHistoryWarningModal.value = true
        } else {
          error.value = 'Error al eliminar el producto: ' + (err.response?.data?.detail || err.message)
        }
      } finally {
        deleting.value = null
        productToDelete.value = null
      }
    }

    const clearFilters = () => {
      searchQuery.value = ''
      filterCategory.value = ''
      filterStock.value = ''
    }

    const isSelected = (id) => selectedIds.value.includes(id)

    const toggleSelection = (id) => {
      if (selectedIds.value.includes(id)) {
        selectedIds.value = selectedIds.value.filter(itemId => itemId !== id)
      } else {
        selectedIds.value = [...selectedIds.value, id]
      }
    }

    const toggleSelectAll = () => {
      if (allDisplayedSelected.value) {
        selectedIds.value = selectedIds.value.filter(id => !displayedIds.value.includes(id))
      } else {
        const merged = new Set([...selectedIds.value, ...displayedIds.value])
        selectedIds.value = Array.from(merged)
      }
    }

    const clearSelection = () => {
      selectedIds.value = []
    }

    const openBulkConfirm = (action) => {
      if (selectedCount.value === 0) return
      const actionLabel = {
        activar: 'activar',
        inactivar: 'inactivar',
        eliminar: 'eliminar'
      }[action]
      bulkConfirm.value = {
        open: true,
        action,
        message: `¿Deseas ${actionLabel} ${selectedCount.value} productos seleccionados?`
      }
    }

    const closeBulkConfirm = () => {
      bulkConfirm.value = { open: false, action: '', message: '' }
    }

    const openCategoryModal = () => {
      if (selectedCount.value === 0) return
      bulkCategory.value = { open: true, value: '', custom: '' }
    }

    const closeCategoryModal = () => {
      bulkCategory.value.open = false
    }

    const openStockModal = () => {
      if (selectedCount.value === 0) return
      bulkStock.value = { open: true, mode: 'add', value: 0 }
    }

    const closeStockModal = () => {
      bulkStock.value.open = false
    }

    const applyBulkAction = async () => {
      if (!bulkConfirm.value.action) return
      bulkLoading.value = true

      try {
        const productsMap = new Map(productos.value.map(p => [p.id, p]))
        for (const id of selectedIds.value) {
          const producto = productsMap.get(id)
          if (!producto) continue

          if (bulkConfirm.value.action === 'activar') {
            await productosService.actualizar(id, { activo: true })
          } else if (bulkConfirm.value.action === 'inactivar') {
            await productosService.actualizar(id, { activo: false })
          } else if (bulkConfirm.value.action === 'eliminar') {
            if (producto.activo) {
              await productosService.eliminar(id)
            } else {
              await productosService.eliminarPermanentemente(id)
            }
          }
        }

        await loadProducts()
        clearSelection()
        closeBulkConfirm()
      } catch (err) {
        console.error('Error en accion masiva:', err)
        error.value = err.response?.data?.detail || err.message || 'Error al aplicar la accion masiva'
      } finally {
        bulkLoading.value = false
      }
    }

    const confirmCategoryBulk = async () => {
      const value = bulkCategory.value.value === '__custom' ? bulkCategory.value.custom.trim() : bulkCategory.value.value
      if (!value) return

      bulkLoading.value = true
      try {
        for (const id of selectedIds.value) {
          await productosService.actualizar(id, { categoria: value })
        }
        await loadProducts()
        clearSelection()
        closeCategoryModal()
      } catch (err) {
        console.error('Error actualizando categoria:', err)
        error.value = err.response?.data?.detail || err.message || 'Error al actualizar categoria'
      } finally {
        bulkLoading.value = false
      }
    }

    const confirmStockBulk = async () => {
      const delta = Number(bulkStock.value.value)
      if (Number.isNaN(delta)) return

      bulkLoading.value = true
      try {
        const productsMap = new Map(productos.value.map(p => [p.id, p]))
        for (const id of selectedIds.value) {
          const producto = productsMap.get(id)
          if (!producto) continue

          let nuevoStock = producto.stock_actual
          if (bulkStock.value.mode === 'add') {
            nuevoStock = producto.stock_actual + delta
          } else if (bulkStock.value.mode === 'subtract') {
            nuevoStock = Math.max(0, producto.stock_actual - delta)
          } else if (bulkStock.value.mode === 'set') {
            nuevoStock = Math.max(0, delta)
          }

          await productosService.actualizar(id, { stock_actual: nuevoStock })
        }

        await loadProducts()
        clearSelection()
        closeStockModal()
      } catch (err) {
        console.error('Error ajustando stock:', err)
        error.value = err.response?.data?.detail || err.message || 'Error al ajustar stock'
      } finally {
        bulkLoading.value = false
      }
    }

    const loadProducts = async () => {
      loading.value = true
      error.value = null
      
      try {
        const data = await productosService.listarTodos()
        // La API puede devolver array directo o objeto con lista
        productos.value = Array.isArray(data) ? data : (data.productos || data.results || [])
        console.log('Productos cargados:', productos.value.length)
      } catch (err) {
        console.error('Error loading products:', err)
        error.value = err.response?.data?.detail || err.message || 'Error de conexión con el servidor'
        productos.value = []
      } finally {
        loading.value = false
      }
    }

    onMounted(loadProducts)

    watch(displayedProducts, (newList) => {
      const visibleIds = new Set(newList.map(p => p.id))
      selectedIds.value = selectedIds.value.filter(id => visibleIds.has(id))
    })

    return {
      loading,
      productos,
      error,
      searchQuery,
      filterCategory,
      filterStock,
      currentPage,
      filteredProducts,
      displayedProducts,
      deleting,
      showDeleteModal,
      productToDelete,
      showEditModal,
      editingProductId,
      activeTab,
      showHistoryWarningModal,
      historyWarningData,
      showB2BModal,
      b2bProduct,
      b2bVariants,
      b2bTargetKey,
      b2bTiers,
      b2bLoading,
      b2bError,
      selectedCount,
      allDisplayedSelected,
      someDisplayedSelected,
      bulkLoading,
      bulkConfirm,
      bulkCategory,
      bulkStock,
      categoryOptions,
      productosActivos,
      productosInactivos,
      formatNumber,
      getTotalStock,
      getTotalStockMin,
      getStockClass,
      getVarianteLabel,
      getB2BTargetMin,
      getCategoryLabel,
      handleImageError,
      openCreateModal,
      openEditModal,
      closeEditModal,
      handleProductUpdated,
      openB2BModal,
      closeB2BModal,
      handleB2BTargetChange,
      addB2BTier,
      removeB2BTier,
      saveB2BTiers,
      confirmDelete,
      deleteProduct,
      clearFilters,
      isSelected,
      toggleSelection,
      toggleSelectAll,
      clearSelection,
      openBulkConfirm,
      closeBulkConfirm,
      applyBulkAction,
      openCategoryModal,
      closeCategoryModal,
      confirmCategoryBulk,
      openStockModal,
      closeStockModal,
      confirmStockBulk,
      loadProducts,
      getImageUrl,
      isVideo,
      getProductMediaUrl
    }
  }
}
</script>

<style scoped>
/* Fuente tabular para n\u00fameros (precios y stock) */
.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
</style>
