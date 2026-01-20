<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div 
        v-if="visible" 
        class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
        @click.self="closeModal"
      >
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col">
          <!-- Header -->
          <div class="flex items-center justify-between p-5 border-b border-gray-100">
            <div>
              <h2 class="text-xl font-bold text-gray-900">{{ isEditing ? 'Editar Producto' : 'Nuevo Producto' }}</h2>
              <p class="text-gray-500 text-sm">{{ isEditing ? 'Modifica los datos del producto' : 'Agrega un nuevo producto al catálogo' }}</p>
            </div>
            <button 
              @click="closeModal"
              class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Body - Scrollable -->
          <div class="flex-1 overflow-y-auto p-5">
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

            <!-- Form -->
            <form v-else @submit.prevent="submitForm" id="product-form" class="space-y-5">
              <!-- Main Grid: 3 columns -->
              <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
                
                <!-- Left Column: Basic Info -->
                <div class="lg:col-span-2 space-y-4">
                  <!-- Row 1: Código + Nombre + Categoría -->
                  <div class="grid grid-cols-4 gap-4">
                    <div>
                      <label class="block text-xs font-medium text-gray-600 mb-1">Código / SKU</label>
                      <input 
                        v-model="form.codigo"
                        type="text"
                        :disabled="isEditing"
                        :class="isEditing ? 'bg-gray-100 text-gray-500' : 'bg-gray-50'"
                        class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 text-sm"
                        placeholder="Auto-generado si vacío"
                      >
                      <p class="text-xs text-gray-400 mt-1">Opcional - se genera automáticamente</p>
                    </div>
                    <div class="col-span-2">
                      <label class="block text-xs font-medium text-gray-600 mb-1">Nombre <span class="text-red-500">*</span></label>
                      <input 
                        v-model="form.nombre"
                        type="text"
                        required
                        class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 text-sm"
                        placeholder="Extensiones Clip-in 20 pulgadas"
                      >
                    </div>
                    <div>
                      <label class="block text-xs font-medium text-gray-600 mb-1">Categoría</label>
                      <select 
                        v-model="form.categoria"
                        class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 text-sm"
                      >
                        <option :value="null">Sin categoría</option>
                        <option v-for="cat in categorias" :key="cat.id" :value="cat.id">
                          {{ cat.nombre }}
                        </option>
                      </select>
                    </div>
                  </div>

                  <!-- Row 2: Descripción -->
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Descripción</label>
                    <textarea 
                      v-model="form.descripcion"
                      rows="2"
                      class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 resize-none text-sm"
                      placeholder="Descripción breve del producto..."
                    ></textarea>
                  </div>

                  <!-- Row 3: Precio, Stock, Stock Min, Estado -->
                  <div class="grid grid-cols-4 gap-3">
                    <div>
                      <label class="block text-xs font-medium text-gray-600 mb-1">Precio</label>
                      <div class="relative">
                        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">$</span>
                        <input 
                          v-model.number="form.precio_monto"
                          type="number"
                          step="0.01"
                          class="w-full pl-7 pr-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 text-sm"
                        >
                      </div>
                    </div>
                    <div>
                      <label class="block text-xs font-medium text-gray-600 mb-1">Stock</label>
                      <input 
                        v-model.number="form.stock_actual"
                        type="number"
                        class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 text-sm"
                      >
                    </div>
                    <div>
                      <label class="block text-xs font-medium text-gray-600 mb-1">Stock Mín</label>
                      <input 
                        v-model.number="form.stock_minimo"
                        type="number"
                        class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 text-sm"
                      >
                    </div>
                    <div>
                      <label class="block text-xs font-medium text-gray-600 mb-1">Estado</label>
                      <label class="flex items-center gap-2 h-[42px] cursor-pointer">
                        <input v-model="form.activo" type="checkbox" class="sr-only peer">
                        <div class="relative w-10 h-5 bg-gray-200 peer-focus:ring-2 peer-focus:ring-brand-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-brand-600"></div>
                        <span class="text-xs text-gray-600">{{ form.activo ? 'Activo' : 'Inactivo' }}</span>
                      </label>
                    </div>
                  </div>

                  <!-- Row 4: Atributos con Checkboxes -->
                  <div class="border border-gray-200 rounded-lg p-3">
                    <div class="flex items-center justify-between mb-3">
                      <label class="text-xs font-medium text-gray-600">Atributos (opcional)</label>
                      <span class="text-xs text-gray-400">Selecciona los que aplican</span>
                    </div>
                    <div class="grid grid-cols-3 gap-3">
                      <!-- Método -->
                      <div class="space-y-1">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.metodo" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500">
                          <span class="text-xs text-gray-700">Método</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.metodo"
                          v-model="form.metodo"
                          type="text"
                          placeholder="Clip-in, Tape..."
                          class="w-full px-2 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs focus:outline-none focus:border-brand-500"
                        >
                      </div>
                      <!-- Color -->
                      <div class="space-y-1">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.color" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500">
                          <span class="text-xs text-gray-700">Color</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.color"
                          v-model="form.color"
                          type="text"
                          placeholder="Negro, Castaño..."
                          class="w-full px-2 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs focus:outline-none focus:border-brand-500"
                        >
                      </div>
                      <!-- Largo -->
                      <div class="space-y-1">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.largo" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500">
                          <span class="text-xs text-gray-700">Largo</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.largo"
                          v-model="form.largo"
                          type="text"
                          placeholder="20 pulgadas..."
                          class="w-full px-2 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs focus:outline-none focus:border-brand-500"
                        >
                      </div>
                      <!-- Tipo -->
                      <div class="space-y-1">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.tipo" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500">
                          <span class="text-xs text-gray-700">Tipo</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.tipo"
                          v-model="form.tipo"
                          type="text"
                          placeholder="Liso, Ondulado..."
                          class="w-full px-2 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs focus:outline-none focus:border-brand-500"
                        >
                      </div>
                      <!-- Origen -->
                      <div class="space-y-1">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.origen" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500">
                          <span class="text-xs text-gray-700">Origen</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.origen"
                          v-model="form.origen"
                          type="text"
                          placeholder="Brasil, India..."
                          class="w-full px-2 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs focus:outline-none focus:border-brand-500"
                        >
                      </div>
                      <!-- Calidad -->
                      <div class="space-y-1">
                        <label class="flex items-center gap-2 cursor-pointer">
                          <input v-model="enabledAttrs.calidad" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500">
                          <span class="text-xs text-gray-700">Calidad</span>
                        </label>
                        <input 
                          v-if="enabledAttrs.calidad"
                          v-model="form.calidad"
                          type="text"
                          placeholder="Premium, Remy..."
                          class="w-full px-2 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs focus:outline-none focus:border-brand-500"
                        >
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Right Column: Image -->
                <div class="space-y-3">
                  <label class="block text-xs font-medium text-gray-600">Imagen del Producto</label>
                  
                  <!-- Preview -->
                  <div class="aspect-square bg-gray-100 rounded-xl overflow-hidden border-2 border-dashed border-gray-200">
                    <img 
                      v-if="imagePreview || form.imagen_principal"
                      :src="imagePreview || getImageUrl(form.imagen_principal)" 
                      alt="Preview"
                      class="w-full h-full object-cover"
                      @error="handleImageError"
                    >
                    <div v-else class="w-full h-full flex flex-col items-center justify-center text-gray-400">
                      <svg class="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span class="text-xs">Sin imagen</span>
                    </div>
                  </div>

                  <!-- Tabs: URL o Subir Archivo -->
                  <div class="flex gap-2 mb-2">
                    <button
                      type="button"
                      @click="imageUploadMode = 'url'"
                      :class="[
                        'flex-1 px-3 py-2 text-xs font-medium rounded-lg transition-colors',
                        imageUploadMode === 'url' 
                          ? 'bg-brand-600 text-white' 
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      ]"
                    >
                      URL Externa
                    </button>
                    <button
                      type="button"
                      @click="imageUploadMode = 'file'"
                      :class="[
                        'flex-1 px-3 py-2 text-xs font-medium rounded-lg transition-colors',
                        imageUploadMode === 'file' 
                          ? 'bg-brand-600 text-white' 
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      ]"
                    >
                      Subir Archivo
                    </button>
                  </div>

                  <!-- URL Input -->
                  <div v-if="imageUploadMode === 'url'">
                    <input 
                      v-model="form.imagen_principal"
                      type="text"
                      placeholder="https://ejemplo.com/imagen.jpg"
                      class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 text-xs"
                      @input="imagePreview = null"
                    >
                    <p class="text-xs text-gray-500 mt-1">Pega cualquier URL o link de imagen</p>
                  </div>

                  <!-- File Upload -->
                  <div v-else>
                    <input 
                      ref="fileInput"
                      type="file"
                      accept="image/*"
                      @change="handleFileSelect"
                      class="hidden"
                    >
                    <button
                      type="button"
                      @click="$refs.fileInput.click()"
                      class="w-full px-3 py-2.5 bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg hover:border-brand-500 hover:bg-brand-50 transition-colors text-xs text-gray-600 font-medium"
                    >
                      <svg class="w-5 h-5 mx-auto mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      {{ selectedFileName || 'Seleccionar imagen' }}
                    </button>
                    <p class="text-xs text-gray-500 mt-1">JPG, PNG, WEBP (máx. 5MB)</p>
                  </div>
                </div>
              </div>
            </form>
          </div>

          <!-- Footer - Actions -->
          <div class="flex items-center justify-end gap-3 p-4 border-t border-gray-100 bg-gray-50">
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
              class="px-5 py-2.5 text-white bg-brand-600 hover:bg-brand-700 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2 text-sm"
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
import { getImageUrl } from '../../services/api'

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

const form = ref({
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
  activo: true
})

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
    metodo: '',
    color: '',
    largo: '',
    tipo: '',
    origen: '',
    calidad: '',
    imagen_principal: '',
    activo: true
  }
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
  error.value = null
}

// Handle file selection
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (!file) {
    console.log('❌ No se seleccionó archivo')
    return
  }
  
  console.log('📁 Archivo seleccionado:', {
    nombre: file.name,
    tamaño: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
    tipo: file.type
  })
  
  // Validate file size (5MB max)
  if (file.size > 5 * 1024 * 1024) {
    error.value = 'La imagen no debe superar 5MB'
    console.log('❌ Archivo muy grande:', file.size)
    return
  }
  
  // Validate file type
  if (!file.type.startsWith('image/')) {
    error.value = 'Solo se permiten archivos de imagen'
    console.log('❌ Tipo de archivo no válido:', file.type)
    return
  }
  
  selectedFile.value = file
  selectedFileName.value = file.name
  error.value = null
  console.log('✅ Archivo validado y listo para subir')
  
  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
    console.log('🖼️ Preview generado')
  }
  reader.readAsDataURL(file)
}

const handleImageError = (e) => {
  e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f3f4f6" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em" fill="%239ca3af" font-size="12"%3ESin Imagen%3C/text%3E%3C/svg%3E'
}

const loadProduct = async () => {
  if (!props.productId) return
  
  loadingProduct.value = true
  error.value = null
  
  try {
    const producto = await productosService.getProducto(props.productId)
    console.log('Producto cargado en modal:', producto)
    console.log('🖼️ Imagen del producto:', producto.imagen_principal)
    
    const atributos = producto.atributos || {}
    
    form.value = {
      codigo: producto.codigo,
      nombre: producto.nombre,
      descripcion: producto.descripcion || '',
      precio_monto: producto.precio?.monto || producto.precio_monto || 0,
      precio_moneda: producto.precio?.moneda || producto.precio_moneda || 'COP',
      stock_actual: producto.stock?.actual || producto.stock_actual || 0,
      stock_minimo: producto.stock?.minimo || producto.stock_minimo || 0,
      metodo: atributos.metodo || '',
      color: atributos.color || '',
      largo: atributos.largo || '',
      tipo: atributos.tipo || '',
      origen: atributos.origen || '',
      calidad: atributos.calidad || '',
      imagen_principal: producto.imagen_principal || '',
      activo: producto.activo !== false
    }
    
    console.log('📋 Formulario rellenado con imagen:', form.value.imagen_principal)
    
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
    // Auto-generar código SKU si está vacío
    if (!form.value.codigo || form.value.codigo.trim() === '') {
      form.value.codigo = `SKU-${Date.now()}-${Math.floor(Math.random() * 1000)}`
    }
    
    let imagenUrl = form.value.imagen_principal
    
    console.log('💾 Iniciando guardado de producto...')
    console.log('🔧 Modo de imagen:', imageUploadMode.value)
    console.log('📷 Archivo seleccionado:', selectedFile.value ? selectedFile.value.name : 'Ninguno')
    console.log('🔗 URL actual:', imagenUrl)
    
    // Si hay un archivo seleccionado, subirlo primero
    if (selectedFile.value && imageUploadMode.value === 'file') {
      console.log('📤 Preparando subida de archivo...')
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      
      try {
        console.log('🌐 Enviando archivo a servidor...')
        // Subir imagen al servidor (necesitas crear este endpoint)
        const uploadResponse = await fetch('http://localhost:8000/api/v1/upload/imagen', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: formData
        })
        
        console.log('📡 Respuesta del servidor:', uploadResponse.status)
        
        if (uploadResponse.ok) {
          const result = await uploadResponse.json()
          console.log('✅ Imagen subida exitosamente:', result)
          imagenUrl = result.url || result.imagen_url
          console.log('🔗 Nueva URL de imagen:', imagenUrl)
        } else {
          const errorText = await uploadResponse.text()
          console.error('❌ Error del servidor:', errorText)
          throw new Error('Error al subir la imagen')
        }
      } catch (uploadErr) {
        console.error('❌ Error uploading image:', uploadErr)
        error.value = 'Error al subir la imagen. Por ahora usa URL externa.'
        saving.value = false
        return
      }
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
      imagen_principal: imagenUrl || null
    }
    
    console.log('📦 Datos a enviar al backend:', {
      ...data,
      imagen_principal: data.imagen_principal ? data.imagen_principal.substring(0, 100) + '...' : 'null'
    })
    
    if (isEditing.value) {
      console.log('✏️ Actualizando producto ID:', props.productId)
      await productosService.actualizar(props.productId, data)
      console.log('✅ Producto actualizado')
      emit('updated')
    } else {
      console.log('➕ Creando nuevo producto')
      await productosService.crear(data)
      console.log('✅ Producto creado')
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
