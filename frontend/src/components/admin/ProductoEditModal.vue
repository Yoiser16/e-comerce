<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div 
        v-if="visible" 
        class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
        @click.self="closeModal"
      >
        <div class="bg-[#FAFAFA] rounded-3xl shadow-2xl w-full max-w-6xl max-h-[90vh] overflow-hidden flex flex-col border border-black/5">
          <!-- Header -->
          <div class="flex items-center justify-between p-6 border-b border-black/5 bg-white">
            <div>
              <h2 class="text-2xl font-semibold text-text-dark">{{ isEditing ? 'Editar Producto' : 'Nuevo Producto' }}</h2>
              <p class="text-text-medium text-sm">{{ isEditing ? 'Modifica los datos del producto' : 'Agrega un nuevo producto al catálogo' }}</p>
            </div>
            <button 
              @click="closeModal"
              class="p-2 hover:bg-black/5 rounded-lg transition-colors"
            >
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Body - Scrollable -->
          <div class="flex-1 overflow-y-auto p-6">
            <!-- Error Alert -->
            <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-3 flex items-center gap-3 mb-4">
              <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <p class="text-red-800 text-sm">{{ error }}</p>
            </div>

            <!-- Loading State -->
            <div v-if="loadingProduct" class="animate-pulse grid grid-cols-3 gap-4">
              <div class="col-span-2 space-y-4">
                <div class="h-10 bg-gray-200 rounded"></div>
                <div class="h-20 bg-gray-200 rounded"></div>
              </div>
              <div class="h-32 bg-gray-200 rounded"></div>
            </div>

            <!-- Form - Layout Asimétrico 2 Columnas (65% / 35%) -->
            <form v-else @submit.prevent="submitForm" id="product-form">
              <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                
                <!-- ════════════════════════════════════════════════════════ -->
                <!-- COLUMNA IZQUIERDA (Principal - 65%) -->
                <!-- ════════════════════════════════════════════════════════ -->
                <div class="lg:col-span-8 space-y-6">
                  
                  <!-- ═══ BLOQUE: INFORMACIÓN GENERAL ═══ -->
                  <div class="space-y-4 bg-white border border-black/5 rounded-2xl p-5 shadow-[0_10px_30px_rgba(0,0,0,0.05)]">
                    <h3 class="text-[11px] font-semibold text-text-medium uppercase tracking-[0.2em]">DETALLES</h3>
                    
                    <!-- Nombre (Ancho completo) -->
                    <div>
                      <label class="block text-sm font-medium text-text-dark mb-2">Nombre del Producto <span class="text-red-500">*</span></label>
                      <input 
                        v-model="form.nombre"
                        type="text"
                        required
                        class="w-full px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all text-sm"
                        placeholder="Ej: Extensiones Premium 20 pulgadas"
                      >
                    </div>

                    <!-- Descripción (Mayor altura) -->
                    <div>
                      <label class="block text-sm font-medium text-text-dark mb-2">Descripción</label>
                      <textarea 
                        v-model="form.descripcion"
                        rows="4"
                        class="w-full px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all resize-none text-sm"
                        placeholder="Describe las características principales del producto..."
                      ></textarea>
                    </div>
                  </div>

                  <!-- ═══ BLOQUE: PRECIOS E INVENTARIO ═══ -->
                  <div class="space-y-4 bg-white border border-black/5 rounded-2xl p-5 shadow-[0_10px_30px_rgba(0,0,0,0.05)]">
                    <h3 class="text-[11px] font-semibold text-text-medium uppercase tracking-[0.2em]">PRECIOS E INVENTARIO</h3>
                    
                    <!-- Fila 1: Precio, Costo, SKU -->
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      <div>
                        <label class="block text-sm font-medium text-text-dark mb-2">Precio <span class="text-red-500">*</span></label>
                        <div class="relative">
                          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-text-medium text-sm">$</span>
                          <input 
                            v-model.number="form.precio_monto"
                            type="number"
                            step="0.01"
                            required
                            class="w-full pl-8 pr-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all text-sm"
                            placeholder="45000"
                          >
                        </div>
                      </div>
                      
                      <div>
                        <label class="block text-sm font-medium text-text-light mb-2">Costo <span class="text-xs text-text-light">(opcional)</span></label>
                        <div class="relative">
                          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-text-medium text-sm">$</span>
                          <input 
                            type="number"
                            step="0.01"
                            class="w-full pl-8 pr-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all text-sm"
                            placeholder="30000"
                          >
                        </div>
                      </div>
                      
                      <div>
                        <label class="block text-sm font-medium text-text-light mb-2">SKU</label>
                        <input 
                          v-model="form.codigo"
                          type="text"
                          :disabled="isEditing"
                          :class="isEditing ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : 'bg-[#FAFAFA]'"
                          class="w-full px-4 py-3 border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 transition-all text-sm"
                          placeholder="Auto"
                        >
                      </div>
                    </div>

                    <!-- Fila 2: Stock y Stock Mínimo -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label class="block text-sm font-medium text-text-dark mb-2">Stock Actual <span class="text-red-500">*</span></label>
                        <input 
                          v-model.number="form.stock_actual"
                          type="number"
                          required
                          class="w-full px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all text-sm"
                          placeholder="50"
                        >
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-text-dark mb-2">Stock Mínimo</label>
                        <input 
                          v-model.number="form.stock_minimo"
                          type="number"
                          class="w-full px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all text-sm"
                          placeholder="5"
                        >
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-text-dark mb-2">Cantidad mínima mayorista <span class="text-red-500">*</span></label>
                        <input 
                          v-model.number="form.cantidad_minima_mayorista"
                          type="number"
                          min="1"
                          required
                          class="w-full px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all text-sm"
                          placeholder="1"
                        >
                      </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label class="block text-sm font-medium text-text-dark mb-2">Disponible en mayoristas</label>
                        <label class="flex items-center justify-between px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg cursor-pointer hover:bg-white transition-all">
                          <span class="text-sm text-text-dark">{{ form.disponible_b2b ? 'Activo' : 'Oculto' }}</span>
                          <input v-model="form.disponible_b2b" type="checkbox" class="sr-only peer">
                          <div class="relative w-11 h-6 bg-gray-200 peer-focus:ring-2 peer-focus:ring-[#D81B60]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#D81B60]"></div>
                        </label>
                      </div>
                      <div>
                        <label class="block text-sm font-medium text-text-dark mb-2">Descuento mayorista (%)</label>
                        <input
                          v-model.number="form.porcentaje_descuento_b2b"
                          type="number"
                          min="0"
                          max="90"
                          class="w-full px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 focus:bg-white transition-all text-sm"
                          placeholder="Ej: 15"
                        >
                        <p class="text-xs text-text-light mt-1">Se aplica sobre el precio base cuando el producto está en canal mayorista.</p>
                      </div>
                    </div>
                  </div>

                    <!-- ═══ BLOQUE: TIPO DE PRODUCTO ═══ -->
                    <div class="space-y-4 bg-white border border-black/5 rounded-2xl p-5 shadow-[0_10px_30px_rgba(0,0,0,0.05)]">
                      <div>
                        <h3 class="text-[11px] font-semibold text-text-medium uppercase tracking-[0.2em]">TIPO DE PRODUCTO</h3>
                        <p class="text-xs text-text-light mt-1">Elige si vendes un producto simple o con variantes.</p>
                      </div>
                      <div class="flex flex-wrap gap-2">
                        <button
                          type="button"
                          @click="modoProducto = 'simple'"
                          :class="[
                            'px-3 py-2 text-xs font-semibold rounded-lg border transition-colors',
                            modoProducto === 'simple'
                              ? 'bg-text-dark text-white border-text-dark'
                              : 'bg-white text-text-dark border-text-dark/20 hover:border-text-dark/40'
                          ]"
                        >
                          Producto simple
                        </button>
                        <button
                          type="button"
                          @click="modoProducto = 'variantes'"
                          :class="[
                            'px-3 py-2 text-xs font-semibold rounded-lg border transition-colors',
                            modoProducto === 'variantes'
                              ? 'bg-[#D81B60] text-white border-[#D81B60]'
                              : 'bg-white text-text-dark border-text-dark/20 hover:border-text-dark/40'
                          ]"
                        >
                          Con variantes
                        </button>
                      </div>
                      <p v-if="modoProducto === 'simple'" class="text-xs text-text-light">Guardarás un solo precio y stock. Las variantes no se enviarán.</p>
                      <p v-else class="text-xs text-text-light">Agrega variantes por color/largo si seleccionas esta opción.</p>
                    </div>

                    <!-- ═══ BLOQUE: VARIANTES ═══ -->
                    <div v-if="modoProducto === 'variantes'" class="space-y-4 bg-white border border-black/5 rounded-2xl p-5 shadow-[0_10px_30px_rgba(0,0,0,0.05)]">
                      <div class="flex items-center justify-between">
                        <div>
                          <h3 class="text-[11px] font-semibold text-text-medium uppercase tracking-[0.2em]">VARIANTES</h3>
                          <p class="text-xs text-text-light mt-1">Configura color, largo, precio y stock por variante.</p>
                        </div>
                        <button
                          type="button"
                          @click="addVariante"
                          class="px-3 py-2 text-xs bg-text-dark text-white rounded-lg hover:bg-black transition-colors"
                        >
                          + Agregar Variante
                        </button>
                      </div>

                      <div v-if="form.variantes.length" class="space-y-3">
                        <div class="hidden md:grid md:grid-cols-12 text-[11px] uppercase tracking-[0.12em] text-text-light">
                          <span class="md:col-span-2">Color</span>
                          <span class="md:col-span-2">Largo</span>
                          <span class="md:col-span-2">Precio</span>
                          <span class="md:col-span-3">Stock / Min / May</span>
                          <span class="md:col-span-2">SKU</span>
                          <span class="md:col-span-1 text-right">Activo</span>
                        </div>

                        <div
                          v-for="(variante, index) in form.variantes"
                          :key="index"
                          class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center border border-black/5 rounded-xl p-3"
                        >
                          <div class="md:col-span-2">
                            <label class="md:hidden text-xs text-text-light">Color</label>
                            <select
                              v-model="variante.color"
                              class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-xs"
                            >
                              <option value="">Sin color</option>
                              <option v-for="option in COLOR_OPTIONS" :key="option.value" :value="option.value">
                                {{ option.label }}
                              </option>
                            </select>
                          </div>

                          <div class="md:col-span-2">
                            <label class="md:hidden text-xs text-text-light">Largo</label>
                            <select
                              v-model="variante.largo"
                              class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-xs"
                            >
                              <option value="">Sin largo</option>
                              <option v-for="option in LARGO_OPTIONS" :key="option" :value="option">
                                {{ option }}"
                              </option>
                            </select>
                          </div>

                          <div class="md:col-span-2">
                            <label class="md:hidden text-xs text-text-light">Precio</label>
                            <input
                              v-model.number="variante.precio_monto"
                              type="number"
                              step="0.01"
                              class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-xs"
                            >
                          </div>

                          <div class="md:col-span-3 grid grid-cols-3 gap-2">
                            <div>
                              <label class="md:hidden text-xs text-text-light">Stock</label>
                              <input
                                v-model.number="variante.stock_actual"
                                type="number"
                                class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-xs"
                              >
                            </div>
                            <div>
                              <label class="md:hidden text-xs text-text-light">Min</label>
                              <input
                                v-model.number="variante.stock_minimo"
                                type="number"
                                class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-xs"
                              >
                            </div>
                            <div>
                              <label class="md:hidden text-xs text-text-light">Min May</label>
                              <input
                                v-model.number="variante.cantidad_minima_mayorista"
                                type="number"
                                min="1"
                                class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-xs"
                              >
                            </div>
                          </div>

                          <div class="md:col-span-2">
                            <label class="md:hidden text-xs text-text-light">SKU</label>
                            <input
                              v-model="variante.sku"
                              type="text"
                              class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-xs"
                            >
                          </div>

                          <div class="md:col-span-1 flex items-center justify-between md:justify-end gap-3">
                            <label class="flex items-center gap-2 text-xs text-text-dark">
                              <input v-model="variante.activo" type="checkbox" class="w-4 h-4 text-[#D81B60] border-gray-300 rounded">
                              Activo
                            </label>
                            <button
                              type="button"
                              @click="removeVariante(index)"
                              class="text-xs text-red-600 hover:text-red-700"
                            >
                              Quitar
                            </button>
                          </div>
                        </div>
                      </div>

                      <div v-else class="text-xs text-text-light">Agrega al menos una variante si manejas precios o stock por color/largo.</div>
                    </div>

                  <!-- ═══ BLOQUE: ATRIBUTOS (Opcional) ═══ -->
                  <div class="space-y-4 bg-white border border-black/5 rounded-2xl p-5 shadow-[0_10px_30px_rgba(0,0,0,0.05)]">
                    <div class="flex items-center justify-between">
                      <h3 class="text-[11px] font-semibold text-text-medium uppercase tracking-[0.2em]">ATRIBUTOS</h3>
                      <span class="text-xs text-text-light">Opcional</span>
                    </div>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      <!-- Método -->
                      <div class="space-y-2">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.metodo" type="checkbox" class="w-4 h-4 text-[#D81B60] border-gray-300 rounded focus:ring-[#D81B60]">
                          <span class="text-sm text-text-dark">Método</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.metodo"
                          v-model="form.metodo"
                          type="text"
                          placeholder="Tape, cosido, halo..."
                          class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-sm focus:outline-none focus:border-text-dark/30"
                        >
                      </div>
                      
                      <!-- Color -->
                      <div class="space-y-2">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.color" type="checkbox" class="w-4 h-4 text-[#D81B60] border-gray-300 rounded focus:ring-[#D81B60]">
                          <span class="text-sm text-text-dark">Color</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.color"
                          v-model="form.color"
                          type="text"
                          placeholder="Negro, Castaño..."
                          class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-sm focus:outline-none focus:border-text-dark/30"
                        >
                      </div>
                      
                      <!-- Largo -->
                      <div class="space-y-2">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.largo" type="checkbox" class="w-4 h-4 text-[#D81B60] border-gray-300 rounded focus:ring-[#D81B60]">
                          <span class="text-sm text-text-dark">Largo</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.largo"
                          v-model="form.largo"
                          type="text"
                          placeholder="20 pulgadas"
                          class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-sm focus:outline-none focus:border-text-dark/30"
                        >
                      </div>
                      
                      <!-- Tipo -->
                      <div class="space-y-2">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.tipo" type="checkbox" class="w-4 h-4 text-[#D81B60] border-gray-300 rounded focus:ring-[#D81B60]">
                          <span class="text-sm text-text-dark">Tipo</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.tipo"
                          v-model="form.tipo"
                          type="text"
                          placeholder="Liso, Ondulado..."
                          class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-sm focus:outline-none focus:border-text-dark/30"
                        >
                      </div>
                      
                      <!-- Origen -->
                      <div class="space-y-2">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.origen" type="checkbox" class="w-4 h-4 text-[#D81B60] border-gray-300 rounded focus:ring-[#D81B60]">
                          <span class="text-sm text-text-dark">Origen</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.origen"
                          v-model="form.origen"
                          type="text"
                          placeholder="Brasil, India..."
                          class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-sm focus:outline-none focus:border-text-dark/30"
                        >
                      </div>
                      
                      <!-- Calidad -->
                      <div class="space-y-2">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.calidad" type="checkbox" class="w-4 h-4 text-[#D81B60] border-gray-300 rounded focus:ring-[#D81B60]">
                          <span class="text-sm text-text-dark">Calidad</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.calidad"
                          v-model="form.calidad"
                          type="text"
                          placeholder="Premium, Remy..."
                          class="w-full px-3 py-2 bg-[#FAFAFA] border border-text-dark/10 rounded-lg text-sm focus:outline-none focus:border-text-dark/30"
                        >
                      </div>
                    </div>
                  </div>
                </div>

                <!-- ════════════════════════════════════════════════════════ -->
                <!-- COLUMNA DERECHA (Media & Organización - 35%) -->
                <!-- ════════════════════════════════════════════════════════ -->
                <div class="lg:col-span-4 space-y-6">
                  
<!-- ═══ BLOQUE: IMÁGENES DEL PRODUCTO ═══ -->
                <div class="space-y-4 bg-white border border-black/5 rounded-2xl p-5 shadow-[0_10px_30px_rgba(0,0,0,0.05)]">
                  <h3 class="text-[11px] font-semibold text-text-medium uppercase tracking-[0.2em]">IMÁGENES DEL PRODUCTO</h3>
                  
                  <!-- Input para agregar URL -->
                  <div class="flex items-center gap-2">
                    <input
                      v-model="newGalleryUrl"
                      type="text"
                      placeholder="Pega una URL de imagen y agrégala"
                      class="flex-1 px-3 py-2.5 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 text-xs"
                    >
                    <button
                      type="button"
                      @click="addGalleryUrl"
                      class="px-4 py-2.5 bg-text-dark text-white text-xs rounded-lg hover:bg-black transition-colors"
                    >
                      Agregar
                    </button>
                  </div>

                  <!-- Botón único para subir imágenes y videos (múltiples) -->
                  <div class="flex items-center gap-2">
                    <input
                      ref="galleryFileInput"
                      type="file"
                      accept="image/*,video/*"
                      multiple
                      class="hidden"
                      @change="handleGalleryFilesSelect"
                    >
                    <button
                      type="button"
                      @click="$refs.galleryFileInput.click()"
                      class="w-full px-4 py-3 bg-text-dark hover:bg-black text-white rounded-lg font-medium transition-all text-sm flex items-center justify-center gap-2"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      Subir Imágenes o Videos
                    </button>
                  </div>
                  <p class="text-xs text-text-light text-center">Imágenes: JPG, PNG, WEBP (máx. 5MB) • Videos: MP4, WEBM (máx. 20MB)</p>
                  <p v-if="galleryUploading" class="text-xs text-primary text-center font-medium">⏳ Subiendo imágenes...</p>

                  <!-- Galería con distintivo de estrella para la principal -->
                  <div v-if="galleryUrls.length" class="grid grid-cols-2 gap-2">
                    <div 
                      v-for="url in galleryUrls" 
                      :key="url" 
                      class="relative aspect-square bg-white border rounded-lg overflow-hidden"
                      :class="form.imagen_principal === url ? 'border-[#D4A85A] border-2' : 'border-text-dark/10'"
                    >
                      <!-- Estrella dorada para imagen principal -->
                      <div 
                        v-if="form.imagen_principal === url" 
                        class="absolute top-1 left-1 z-10 bg-[#D4A85A] rounded-full p-1"
                      >
                        <svg class="w-3 h-3 text-white fill-current" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      </div>
                      
                      <!-- Mostrar video o imagen -->
                      <video v-if="isVideo(url)" :src="getImageUrl(url)" class="w-full h-full object-cover" muted></video>
                      <img v-else :src="getImageUrl(url)" class="w-full h-full object-cover" @error="handleImageError" />
                      
                      <!-- Icono de play para videos -->
                      <div v-if="isVideo(url)" class="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <div class="bg-black/50 rounded-full p-2">
                          <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                          </svg>
                        </div>
                      </div>
                      
                      <div class="absolute inset-0 bg-black/0 hover:bg-black/20 transition-colors flex items-end justify-between p-1">
                        <button
                          v-if="form.imagen_principal !== url"
                          type="button"
                          @click="setAsPrincipal(url)"
                          class="text-[10px] px-2 py-1 bg-white/90 text-text-dark rounded hover:bg-white transition-colors"
                        >
                          ⭐ Principal
                        </button>
                        <span v-else class="text-[10px] px-2 py-1 bg-[#D4A85A]/90 text-white rounded font-medium">
                          Principal
                        </span>
                        <button
                          type="button"
                          @click="removeGalleryUrl(url)"
                          class="text-[10px] px-2 py-1 bg-white/90 text-red-600 rounded hover:bg-white transition-colors"
                        >
                          Quitar
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Mensaje cuando no hay imágenes -->
                  <div v-else class="text-center py-8 border-2 border-dashed border-text-dark/10 rounded-lg">
                    <svg class="w-12 h-12 mx-auto mb-3 text-text-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <p class="text-sm text-text-medium">Sin imágenes</p>
                    <p class="text-xs text-text-light">Sube imágenes o agrega una URL</p>
                  </div>
                  
                  <p v-if="galleryUrls.length > 0" class="text-xs text-text-light">
                    💡 Haz clic en "⭐ Principal" para seleccionar la imagen/video destacado del producto
                  </p>
                  </div>

                  <!-- ═══ BLOQUE: ORGANIZACIÓN ═══ -->
                  <div class="space-y-4 bg-white border border-black/5 rounded-2xl p-5 shadow-[0_10px_30px_rgba(0,0,0,0.05)]">
                    <h3 class="text-[11px] font-semibold text-text-medium uppercase tracking-[0.2em]">ORGANIZACIÓN</h3>
                    
                    <!-- Categoría -->
                    <div>
                      <label class="block text-sm font-medium text-text-dark mb-2">Categoría</label>
                      <select 
                        v-model="form.categoria"
                        class="w-full px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 text-sm"
                      >
                        <option :value="null">Sin categoría</option>
                        <option v-for="cat in categorias" :key="cat.id" :value="cat.id">
                          {{ cat.nombre }}
                        </option>
                      </select>
                    </div>

                    <!-- Marca (placeholder) -->
                    <div>
                      <label class="block text-sm font-medium text-text-dark mb-2">Marca</label>
                      <input 
                        type="text"
                        placeholder="Kharis Distribuidora"
                        class="w-full px-4 py-3 bg-[#FAFAFA] border border-text-dark/10 rounded-lg focus:outline-none focus:border-text-dark/30 text-sm"
                      >
                    </div>

                    <!-- Estado -->
                    <div>
                      <label class="block text-sm font-medium text-text-dark mb-2">Estado</label>
                      <label class="flex items-center justify-between p-4 bg-[#FAFAFA] border border-text-dark/10 rounded-lg cursor-pointer hover:bg-white transition-all">
                        <span class="text-sm text-text-dark">{{ form.activo ? 'Activo' : 'Borrador' }}</span>
                        <div class="flex items-center gap-3">
                          <input v-model="form.activo" type="checkbox" class="sr-only peer">
                          <div class="relative w-11 h-6 bg-gray-200 peer-focus:ring-2 peer-focus:ring-[#D81B60]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                        </div>
                      </label>
                    </div>

                    <!-- Producto Destacado -->
                    <div>
                      <label class="flex items-center justify-between p-4 bg-[#FAF5F2] border border-[#C9A962]/20 rounded-lg cursor-pointer hover:bg-[#F5EBE5] transition-all">
                        <div class="flex items-center gap-2">
                          <svg class="w-5 h-5 text-[#C9A962]" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                          <div>
                            <span class="text-sm font-medium text-text-dark">Destacado</span>
                            <p class="text-xs text-text-light">Aparece en portada</p>
                          </div>
                        </div>
                        <div>
                          <input v-model="form.destacado" type="checkbox" class="sr-only peer">
                          <div class="relative w-11 h-6 bg-gray-200 peer-focus:ring-2 peer-focus:ring-[#C9A962]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C9A962]"></div>
                        </div>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>

          <!-- Footer - Actions -->
          <div class="flex items-center justify-between gap-3 p-4 border-t border-black/5 bg-white">
            <p class="text-xs text-text-light hidden sm:block">Los cambios se aplican de inmediato en el catálogo</p>
            <button 
              type="button"
              @click="closeModal"
              class="px-5 py-2.5 text-gray-700 bg-white hover:bg-gray-100 rounded-lg font-medium transition-colors border border-gray-200 text-sm"
            >
              Cancelar
            </button>
            <button 
              type="submit"
              form="product-form"
              :disabled="saving"
              class="px-6 py-2.5 text-white bg-text-dark hover:bg-black rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2 text-sm"
            >
              <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ saving ? 'Guardando...' : (isEditing ? 'Guardar Cambios' : 'Crear Producto') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { productosService } from '../../services/productos'
import { categoriasService } from '../../services/categorias'
import { getImageUrl, API_BASE_URL } from '../../services/api'

const props = defineProps({
  visible: Boolean,
  productId: String // null = crear nuevo, string = editar existente
})

const emit = defineEmits(['close', 'updated', 'created'])

const isEditing = computed(() => !!props.productId)

const loadingProduct = ref(false)
const saving = ref(false)
const error = ref(null)

const categorias = ref([])

// Image upload
const imageUploadMode = ref('url') // 'url' o 'file'
const imagePreview = ref(null)
const selectedFileName = ref('')
const selectedFile = ref(null)
const fileInput = ref(null)

// Gallery images
const galleryUrls = ref([])
const newGalleryUrl = ref('')
const galleryUploading = ref(false)
const galleryFileInput = ref(null)

const COLOR_OPTIONS = [
  { value: 'negro_natural', label: 'Negro Natural' },
  { value: 'negro_azabache', label: 'Negro Azabache' },
  { value: 'castano_oscuro', label: 'Castaño Oscuro' },
  { value: 'castano_medio', label: 'Castaño Medio' },
  { value: 'castano_claro', label: 'Castaño Claro' },
  { value: 'castano_chocolate', label: 'Castaño Chocolate' },
  { value: 'rubio_oscuro', label: 'Rubio Oscuro' },
  { value: 'rubio_medio', label: 'Rubio Medio' },
  { value: 'rubio_claro', label: 'Rubio Claro' },
  { value: 'rubio_platino', label: 'Rubio Platino' },
  { value: 'rubio_cenizo', label: 'Rubio Cenizo' },
  { value: 'rubio_miel', label: 'Rubio Miel' },
  { value: 'pelirrojo', label: 'Pelirrojo' },
  { value: 'cobrizo', label: 'Cobrizo' },
  { value: 'borgona', label: 'Borgoña' },
  { value: 'rosa', label: 'Rosa' },
  { value: 'azul', label: 'Azul' },
  { value: 'morado', label: 'Morado' },
  { value: 'verde', label: 'Verde' },
  { value: 'gris', label: 'Gris' },
  { value: 'ombre', label: 'Ombré' },
  { value: 'balayage', label: 'Balayage' },
  { value: 'highlights', label: 'Highlights' }
]

const LARGO_OPTIONS = ['8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32']

const form = ref({
    cantidad_minima_mayorista: 1,
  codigo: '',
  nombre: '',
  descripcion: '',
  categoria: null,
  precio_monto: 0,
  precio_moneda: 'COP',
  stock_actual: 0,
  stock_minimo: 0,
  metodo: '',
  color: '',
  largo: '',
  tipo: '',
  origen: '',
  calidad: '',
  imagen_principal: '',
  imagenes: [],
  variantes: [],
  activo: true,
  destacado: false,
  disponible_b2b: true,
  porcentaje_descuento_b2b: null
})

const modoProducto = ref('simple')

// Checkboxes para habilitar atributos
const enabledAttrs = ref({
  metodo: false,
  color: false,
  largo: false,
  tipo: false,
  origen: false,
  calidad: false
})

const resetForm = () => {
  form.value = {
    codigo: '',
    nombre: '',
    descripcion: '',
    categoria: null,
    precio_monto: 0,
    precio_moneda: 'COP',
    stock_actual: 0,
    stock_minimo: 0,
    cantidad_minima_mayorista: 1,
    metodo: '',
    color: '',
    largo: '',
    tipo: '',
    origen: '',
    calidad: '',
    imagen_principal: '',
    imagenes: [],
    variantes: [],
    activo: true,
    destacado: false,
    disponible_b2b: true,
    porcentaje_descuento_b2b: null
  }
  modoProducto.value = 'simple'
  enabledAttrs.value = {
    metodo: false,
    color: false,
    largo: false,
    tipo: false,
    origen: false,
    calidad: false
  }
  // Reset image upload
  imageUploadMode.value = 'url'
  imagePreview.value = null
  selectedFileName.value = ''
  selectedFile.value = null
  galleryUrls.value = []
  newGalleryUrl.value = ''
  galleryUploading.value = false
  error.value = null
}

const addGalleryUrl = () => {
  const url = newGalleryUrl.value.trim()
  if (!url) return
  if (!galleryUrls.value.includes(url)) {
    galleryUrls.value.push(url)
  }
  newGalleryUrl.value = ''
}

const removeGalleryUrl = (url) => {
  galleryUrls.value = galleryUrls.value.filter((u) => u !== url)
}

const addVariante = () => {
  form.value.variantes.push({
    id: null,
    sku: '',
    color: '',
    largo: '',
    precio_monto: form.value.precio_monto || 0,
    precio_moneda: form.value.precio_moneda || 'COP',
    stock_actual: 0,
    stock_minimo: 0,
    cantidad_minima_mayorista: form.value.cantidad_minima_mayorista || 1,
    imagen_url: '',
    activo: true,
    orden: form.value.variantes.length
  })
}

const removeVariante = (index) => {
  form.value.variantes.splice(index, 1)
}

const normalizeVariantes = () => {
  return (form.value.variantes || [])
    .filter((v) => v && (v.color || v.largo || v.precio_monto || v.stock_actual))
    .map((v, idx) => ({
      id: v.id || null,
      sku: v.sku || '',
      color: v.color || null,
      largo: v.largo || null,
      precio_monto: Number(v.precio_monto || 0),
      precio_moneda: v.precio_moneda || form.value.precio_moneda || 'COP',
      stock_actual: Number(v.stock_actual || 0),
      stock_minimo: Number(v.stock_minimo || 0),
      cantidad_minima_mayorista: Number(v.cantidad_minima_mayorista || form.value.cantidad_minima_mayorista || 1),
      imagen_url: v.imagen_url || null,
      activo: v.activo !== false,
      orden: v.orden ?? idx
    }))
}

const validarFormulario = () => {
  if (!form.value.nombre || !form.value.nombre.trim()) {
    return 'El nombre del producto es obligatorio'
  }
  if (!form.value.descripcion || !form.value.descripcion.trim()) {
    return 'La descripción del producto es obligatoria'
  }
  if (Number(form.value.precio_monto || 0) <= 0) {
    return 'El precio debe ser mayor a 0'
  }
  if (form.value.stock_actual === null || form.value.stock_actual === undefined || Number(form.value.stock_actual) < 0) {
    return 'El stock actual es obligatorio'
  }
  if (!form.value.cantidad_minima_mayorista || Number(form.value.cantidad_minima_mayorista) < 1) {
    return 'La cantidad mínima mayorista debe ser mayor a 0'
  }

  if (modoProducto.value === 'variantes') {
    const variantesNormalizadas = normalizeVariantes()
    if (variantesNormalizadas.length === 0) {
      return 'Agrega al menos una variante'
    }
    for (let i = 0; i < variantesNormalizadas.length; i += 1) {
      const variante = variantesNormalizadas[i]
      if (!variante.color && !variante.largo) {
        return `La variante ${i + 1} debe tener color o largo`
      }
      if (Number(variante.precio_monto || 0) <= 0) {
        return `El precio de la variante ${i + 1} debe ser mayor a 0`
      }
      if (variante.stock_actual === null || variante.stock_actual === undefined || Number(variante.stock_actual) < 0) {
        return `El stock de la variante ${i + 1} es obligatorio`
      }
      if (!variante.cantidad_minima_mayorista || Number(variante.cantidad_minima_mayorista) < 1) {
        return `La cantidad mínima mayorista de la variante ${i + 1} debe ser mayor a 0`
      }
    }
  }

  return null
}

const setAsPrincipal = (url) => {
  form.value.imagen_principal = url
  imagePreview.value = null
}

const handleGalleryFilesSelect = async (event) => {
  const files = Array.from(event.target.files || [])
  if (!files.length) return

  galleryUploading.value = true
  error.value = null

  try {
    for (const file of files) {
      const isImage = file.type.startsWith('image/')
      const isVideo = file.type.startsWith('video/')
      
      if (!isImage && !isVideo) {
        throw new Error('Solo se permiten archivos de imagen o video')
      }
      
      // Validar tamaño según tipo
      if (isImage && file.size > 5 * 1024 * 1024) {
        throw new Error('Cada imagen debe ser menor a 5MB')
      }
      if (isVideo && file.size > 20 * 1024 * 1024) {
        throw new Error('Cada video debe ser menor a 20MB')
      }

      const formData = new FormData()
      formData.append('file', file)

      const uploadResponse = await fetch(`${API_BASE_URL}/api/v1/upload/imagen`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData
      })

      if (!uploadResponse.ok) {
        const errorData = await uploadResponse.json()
        throw new Error(errorData.detail || 'Error al subir la imagen')
      }

      const result = await uploadResponse.json()
      const url = result.url || result.imagen_url
      if (url && !galleryUrls.value.includes(url)) {
        galleryUrls.value.push(url)
      }
    }
  } catch (uploadErr) {
    console.error('Error uploading gallery images:', uploadErr)
    error.value = uploadErr.message || 'Error al subir las imágenes'
  } finally {
    galleryUploading.value = false
    if (galleryFileInput.value) {
      galleryFileInput.value.value = ''
    }
  }
}

// Handle file selection
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validate file size (5MB max)
  if (file.size > 5 * 1024 * 1024) {
    error.value = 'La imagen no debe superar 5MB'
    return
  }
  
  if (!file.type.startsWith('image/')) {
    error.value = 'Solo se permiten archivos de imagen'
    return
  }
  
  selectedFile.value = file
  selectedFileName.value = file.name
  error.value = null
  
  // Cambiar a modo file (no URL)
  imageUploadMode.value = 'file'
  
  // Limpiar la URL anterior para no confundir
  form.value.imagen_principal = null
  
  // Create preview (solo para mostrar, NO guardar en el formulario)
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const handleImageError = (e) => {
  e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f3f4f6" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em" fill="%239ca3af" font-size="12"%3ESin Imagen%3C/text%3E%3C/svg%3E'
}

const isVideo = (url) => {
  if (!url) return false
  const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov']
  const lowerUrl = url.toLowerCase()
  return videoExtensions.some(ext => lowerUrl.endsWith(ext))
}

const loadProduct = async () => {
  if (!props.productId) return
  
  loadingProduct.value = true
  error.value = null
  
  try {
    const producto = await productosService.getProducto(props.productId)
    
    const atributos = producto.atributos || {}
    
    const variantesPayload = Array.isArray(producto.variantes) ? producto.variantes : []
    const variantesVisuales = variantesPayload.filter((v) => v?.color || v?.largo)

    form.value = {
      codigo: producto.codigo,
      nombre: producto.nombre,
      descripcion: producto.descripcion || '',
      precio_monto: producto.precio?.monto || producto.precio_monto || 0,
      precio_moneda: producto.precio?.moneda || producto.precio_moneda || 'COP',
      stock_actual: producto.stock?.actual || producto.stock_actual || 0,
      stock_minimo: producto.stock?.minimo || producto.stock_minimo || 0,
      cantidad_minima_mayorista: producto.cantidad_minima_mayorista || 1,
      metodo: atributos.metodo || '',
      color: atributos.color || '',
      largo: atributos.largo || '',
      tipo: atributos.tipo || '',
      origen: atributos.origen || '',
      calidad: atributos.calidad || '',
      imagen_principal: producto.imagen_principal || '',
      imagenes: Array.isArray(producto.imagenes) ? producto.imagenes : [],
      variantes: variantesVisuales.map((v) => ({
        id: v.id || null,
        sku: v.sku || '',
        color: v.color || '',
        largo: v.largo || '',
        precio_monto: v.precio_monto ?? producto.precio?.monto ?? producto.precio_monto ?? 0,
        precio_moneda: v.precio_moneda || producto.precio?.moneda || producto.precio_moneda || 'COP',
        stock_actual: v.stock_actual ?? 0,
        stock_minimo: v.stock_minimo ?? 0,
        cantidad_minima_mayorista: v.cantidad_minima_mayorista ?? producto.cantidad_minima_mayorista ?? 1,
        imagen_url: v.imagen_url || '',
        activo: v.activo !== false,
        orden: v.orden ?? 0
      })),
      activo: producto.activo !== false,
      destacado: producto.destacado || false,
      disponible_b2b: producto.disponible_b2b !== false,
      porcentaje_descuento_b2b: producto.porcentaje_descuento_b2b ?? null
    }

    modoProducto.value = variantesVisuales.length > 0
      ? 'variantes'
      : 'simple'

    // Construir galleryUrls incluyendo la imagen principal
    const imagenes = Array.isArray(producto.imagenes) ? [...producto.imagenes] : []
    
    // Asegurar que la imagen principal esté en la galería
    if (producto.imagen_principal && !imagenes.includes(producto.imagen_principal)) {
      galleryUrls.value = [producto.imagen_principal, ...imagenes]
    } else {
      galleryUrls.value = imagenes
    }
    
    // Habilitar checkboxes si tienen valor
    enabledAttrs.value = {
      metodo: !!atributos.metodo,
      color: !!atributos.color,
      largo: !!atributos.largo,
      tipo: !!atributos.tipo,
      origen: !!atributos.origen,
      calidad: !!atributos.calidad
    }
  } catch (err) {
    console.error('Error loading product:', err)
    error.value = 'Error al cargar el producto'
  } finally {
    loadingProduct.value = false
  }
}

const submitForm = async () => {
  saving.value = true
  error.value = null
  
  try {
    const validationError = validarFormulario()
    if (validationError) {
      error.value = validationError
      saving.value = false
      return
    }

    // Auto-generar código SKU si está vacío
    if (!form.value.codigo || form.value.codigo.trim() === '') {
      form.value.codigo = `SKU-${Date.now()}-${Math.floor(Math.random() * 1000)}`
    }
    
    let imagenUrl = null
    
    // Si hay un archivo seleccionado, DEBE subirlo primero
    if (selectedFile.value && imageUploadMode.value === 'file') {
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      
      try {
        // Subir imagen al servidor
        const uploadResponse = await fetch(`${API_BASE_URL}/api/v1/upload/imagen`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: formData
        })
        
        if (uploadResponse.ok) {
          const result = await uploadResponse.json()
          imagenUrl = result.url || result.imagen_url
        } else {
          const errorData = await uploadResponse.json()
          throw new Error(errorData.detail || 'Error al subir la imagen')
        }
      } catch (uploadErr) {
        console.error('Error uploading image:', uploadErr)
        error.value = uploadErr.message || 'Error al subir la imagen'
        saving.value = false
        return
      }
    } else if (imageUploadMode.value === 'url') {
      // Si se eligió URL externa, usar esa
      imagenUrl = form.value.imagen_principal
    }
    
    const data = {
      ...form.value,
      // Solo enviar atributos habilitados
      metodo: enabledAttrs.value.metodo ? form.value.metodo : null,
      color: enabledAttrs.value.color ? form.value.color : null,
      largo: enabledAttrs.value.largo ? form.value.largo : null,
      tipo: enabledAttrs.value.tipo ? form.value.tipo : null,
      origen: enabledAttrs.value.origen ? form.value.origen : null,
      calidad: enabledAttrs.value.calidad ? form.value.calidad : null,
      imagen_principal: imagenUrl || null,
      imagenes: galleryUrls.value,
      destacado: form.value.destacado,
      cantidad_minima_mayorista: form.value.cantidad_minima_mayorista ?? 1,
      disponible_b2b: !!form.value.disponible_b2b,
      porcentaje_descuento_b2b: form.value.porcentaje_descuento_b2b ?? null,
      variantes: modoProducto.value === 'variantes' ? normalizeVariantes() : []
    }
    
    if (isEditing.value) {
      await productosService.actualizar(props.productId, data)
      emit('updated')
    } else {
      await productosService.crear(data)
      emit('created')
    }
    closeModal()
  } catch (err) {
    console.error('Error saving product:', err)
    
    // Manejo especial para error 409 (Conflict)
    if (err.response?.status === 409) {
      const detail = err.response?.data?.detail || ''
      if (detail.toLowerCase().includes('codigo') || detail.toLowerCase().includes('sku')) {
        error.value = 'Ya existe un producto con ese código/SKU. Usa uno diferente.'
      } else if (detail.toLowerCase().includes('nombre')) {
        error.value = 'Ya existe un producto con ese nombre. Usa uno diferente.'
      } else {
        error.value = 'Este producto ya existe. Verifica el código o nombre.'
      }
    } else {
      error.value = 'Error al guardar: ' + (err.response?.data?.detail || err.message)
    }
  } finally {
    saving.value = false
  }
}

const closeModal = () => {
  resetForm()
  emit('close')
}

// Cargar categorías al montar el componente
onMounted(async () => {
  try {
    const data = await categoriasService.listar({ soloActivas: true })
    categorias.value = data.categorias || data || []
  } catch (err) {
    console.error('Error cargando categorías:', err)
  }
})

// Watch for modal visibility changes
watch(() => props.visible, (newVal) => {
  if (newVal) {
    if (props.productId) {
      loadProduct()
    } else {
      resetForm()
    }
  }
})
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .bg-white,
.modal-fade-leave-active .bg-white {
  transition: transform 0.3s ease;
}

.modal-fade-enter-from .bg-white {
  transform: scale(0.9);
}

.modal-fade-leave-to .bg-white {
  transform: scale(0.9);
}
</style>
