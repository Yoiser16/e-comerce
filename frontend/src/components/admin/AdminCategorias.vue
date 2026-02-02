<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Categorías</h2>
        <p class="text-gray-500">Gestiona las categorías de tu tienda</p>
      </div>
      <button 
        @click="openModal()"
        class="inline-flex w-full sm:w-auto justify-center items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold px-5 py-3 rounded-xl transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Nueva Categoría
      </button>
    </div>

    <!-- Info Card -->
    <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 flex items-start gap-3">
      <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
      </svg>
      <div class="text-sm text-blue-800">
        <p class="font-medium mb-1">Niveles de Prioridad:</p>
        <ul class="space-y-1">
          <li><span class="font-semibold">Prioridad 1:</span> Categoría grande/destacada en el home</li>
          <li><span class="font-semibold">Prioridad 2-3:</span> Categorías más pequeñas en el grid</li>
        </ul>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
      <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
      <p class="text-red-800 flex-1">{{ error }}</p>
      <button @click="loadCategorias" class="text-red-600 hover:text-red-800 font-medium text-sm">
        Reintentar
      </button>
    </div>

    <!-- Categories Grid -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <!-- Loading State -->
      <div v-if="loading" class="p-8">
        <div class="animate-pulse grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="i in 3" :key="i" class="h-48 bg-gray-200 rounded-xl"></div>
        </div>
      </div>

      <!-- Categories List -->
      <div v-else-if="categorias.length > 0" class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            v-for="categoria in categorias" 
            :key="categoria.id"
            class="relative bg-gray-50 rounded-xl overflow-hidden border border-gray-200 hover:border-brand-300 transition-colors group"
          >
            <!-- Image -->
            <div class="h-32 bg-gray-200 overflow-hidden">
              <img 
                v-if="categoria.imagen"
                :src="categoria.imagen" 
                :alt="categoria.nombre"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform"
                @error="handleImageError"
              >
              <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200">
                <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>

            <!-- Content -->
            <div class="p-4">
              <div class="flex items-start justify-between gap-2 mb-2">
                <h3 class="font-semibold text-gray-900">{{ categoria.nombre }}</h3>
                <span 
                  :class="getPrioridadClass(categoria.prioridad)"
                  class="px-2 py-0.5 text-xs font-medium rounded-full"
                >
                  P{{ categoria.prioridad }}
                </span>
              </div>
              <p class="text-sm text-gray-500 line-clamp-2 mb-3">
                {{ categoria.descripcion_corta || categoria.descripcion || 'Sin descripción' }}
              </p>
              
              <!-- Status badges -->
              <div class="flex items-center gap-2 mb-3">
                <span 
                  :class="categoria.activo ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                  class="px-2 py-0.5 text-xs font-medium rounded-full"
                >
                  {{ categoria.activo ? 'Activa' : 'Inactiva' }}
                </span>
                <span 
                  v-if="categoria.mostrar_en_home"
                  class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-700"
                >
                  En Home
                </span>
              </div>

              <!-- Actions -->
              <div class="flex items-center gap-2">
                <button 
                  @click="openModal(categoria)"
                  class="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Editar
                </button>
                <button 
                  @click="confirmDelete(categoria)"
                  class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="p-12 text-center">
        <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <p class="text-gray-500 mb-4">No hay categorías creadas</p>
        <button 
          @click="openModal()"
          class="text-brand-600 font-medium hover:underline"
        >
          Crear primera categoría
        </button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div 
          v-if="showModal" 
          class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          @click.self="closeModal"
        >
          <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
            <!-- Header -->
            <div class="flex items-center justify-between p-5 border-b border-gray-100">
              <h2 class="text-xl font-bold text-gray-900">
                {{ editingCategoria ? 'Editar Categoría' : 'Nueva Categoría' }}
              </h2>
              <button @click="closeModal" class="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Body -->
            <div class="flex-1 overflow-y-auto p-5">
              <!-- Error -->
              <div v-if="modalError" class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4 text-sm text-red-800">
                {{ modalError }}
              </div>

              <form @submit.prevent="submitForm" id="categoria-form" class="space-y-4">
                <!-- Nombre -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Nombre <span class="text-red-500">*</span>
                  </label>
                  <input 
                    v-model="form.nombre"
                    type="text"
                    required
                    class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500"
                    placeholder="Ej: Extensiones"
                  >
                </div>

                <!-- Descripción corta -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Descripción corta</label>
                  <input 
                    v-model="form.descripcion_corta"
                    type="text"
                    maxlength="150"
                    class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500"
                    placeholder="Texto corto para las tarjetas"
                  >
                </div>

                <!-- Descripción -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
                  <textarea 
                    v-model="form.descripcion"
                    rows="2"
                    class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500 resize-none"
                    placeholder="Descripción más detallada (opcional)"
                  ></textarea>
                </div>

                <!-- Image Upload / URL -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Imagen</label>
                  
                  <!-- Upload / URL Selector -->
                  <div class="flex gap-2 mb-3">
                    <button 
                      type="button"
                      @click="() => uploadMethod = 'file'"
                      :class="uploadMethod === 'file' ? 'bg-brand-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                      class="flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      Subir archivo
                    </button>
                    <button 
                      type="button"
                      @click="() => uploadMethod = 'url'"
                      :class="uploadMethod === 'url' ? 'bg-brand-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                      class="flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                      </svg>
                      Pegar URL
                    </button>
                  </div>

                  <!-- File Upload Input -->
                  <div v-if="uploadMethod === 'file'" class="space-y-2">
                    <div class="relative">
                      <input 
                        ref="fileInput"
                        type="file"
                        accept="image/*"
                        @change="handleImageFileSelect"
                        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      >
                      <div class="px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg hover:border-brand-300 hover:bg-brand-50 transition-colors cursor-pointer">
                        <div class="flex items-center gap-2">
                          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                          </svg>
                          <span v-if="!uploadingImage" class="text-gray-600">Haz click para seleccionar una imagen</span>
                          <span v-else class="text-brand-600 font-medium">{{ uploadingImage ? 'Subiendo...' : 'Subido ✓' }}</span>
                        </div>
                      </div>
                    </div>
                    <p class="text-xs text-gray-500">JPG, PNG, WEBP (máx. 5MB)</p>
                  </div>

                  <!-- URL Input -->
                  <div v-else class="space-y-2">
                    <input 
                      v-model="form.imagen"
                      type="url"
                      maxlength="2000"
                      class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500"
                      placeholder="https://ejemplo.com/imagen.jpg"
                    >
                    <p v-if="form.imagen && form.imagen.length > 1900" class="text-xs text-amber-600">
                      ⚠️ URL muy larga, considera usar un acortador
                    </p>
                  </div>
                </div>

                <!-- Image Preview -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Vista previa</label>
                  <div class="h-32 bg-gray-100 rounded-lg overflow-hidden border border-gray-200">
                    <img 
                      v-if="form.imagen"
                      :src="form.imagen" 
                      alt="Preview"
                      class="w-full h-full object-cover"
                      @error="e => e.target.src = 'https://via.placeholder.com/200x150?text=Error'"
                    >
                    <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                      <span class="text-sm">Sin imagen</span>
                    </div>
                  </div>
                </div>

                <!-- Prioridad + Orden -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Prioridad</label>
                    <select 
                      v-model.number="form.prioridad"
                      class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500"
                    >
                      <option :value="1">1 - Alta (Grande en Home)</option>
                      <option :value="2">2 - Media</option>
                      <option :value="3">3 - Baja</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Orden</label>
                    <input 
                      v-model.number="form.orden"
                      type="number"
                      min="0"
                      class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:border-brand-500"
                    >
                  </div>
                </div>

                <!-- Flags -->
                <div class="flex items-center gap-6">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input v-model="form.activo" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500">
                    <span class="text-sm text-gray-700">Activa</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input v-model="form.mostrar_en_home" type="checkbox" class="w-4 h-4 text-brand-600 border-gray-300 rounded focus:ring-brand-500">
                    <span class="text-sm text-gray-700">Mostrar en Home</span>
                  </label>
                </div>
              </form>
            </div>

            <!-- Footer -->
            <div class="flex items-center justify-end gap-3 p-4 border-t border-gray-100 bg-gray-50">
              <button 
                type="button"
                @click="closeModal"
                class="px-5 py-2.5 text-gray-700 bg-white hover:bg-gray-100 rounded-lg font-medium transition-colors border border-gray-200"
              >
                Cancelar
              </button>
              <button 
                type="submit"
                form="categoria-form"
                :disabled="saving"
                class="px-5 py-2.5 text-white bg-brand-600 hover:bg-brand-700 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
              >
                <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                {{ saving ? 'Guardando...' : (editingCategoria ? 'Guardar' : 'Crear') }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Eliminar Categoría</h3>
              <p class="text-gray-500 text-sm">Esta acción no se puede deshacer</p>
            </div>
          </div>
          
          <p class="text-gray-700">
            ¿Estás seguro de que deseas eliminar <span class="font-semibold">{{ categoriaToDelete?.nombre }}</span>?
          </p>
          
          <div class="flex gap-3 justify-end">
            <button 
              @click="showDeleteModal = false"
              class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="deleteCategoria"
              :disabled="deleting"
              class="px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg font-medium transition-colors disabled:opacity-50"
            >
              {{ deleting ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { categoriasService } from '../../services/categorias'
import { getImageUrl } from '../../services/api'

// Constants
const API_BASE_URL = 'http://localhost:8000'

// Get token from localStorage
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token')
  return {
    'Authorization': `Bearer ${token}`
  }
}

export default {
  name: 'AdminCategorias',
  setup() {
    const loading = ref(true)
    const categorias = ref([])
    const error = ref(null)
    
    const showModal = ref(false)
    const editingCategoria = ref(null)
    const modalError = ref(null)
    const saving = ref(false)
    
    const showDeleteModal = ref(false)
    const categoriaToDelete = ref(null)
    const deleting = ref(false)
    
    const fileInput = ref(null)
    const uploadMethod = ref('file')
    const uploadingImage = ref(false)
    
    const form = ref({
      nombre: '',
      descripcion: '',
      descripcion_corta: '',
      imagen: '',
      prioridad: 2,
      orden: 0,
      activo: true,
      mostrar_en_home: true
    })

    const resetForm = () => {
      form.value = {
        nombre: '',
        descripcion: '',
        descripcion_corta: '',
        imagen: '',
        prioridad: 2,
        orden: 0,
        activo: true,
        mostrar_en_home: true
      }
    }

    const loadCategorias = async () => {
      loading.value = true
      error.value = null
      try {
        categorias.value = await categoriasService.listar()
      } catch (err) {
        console.error('Error loading categorias:', err)
        error.value = err.response?.data?.detail || err.message
      } finally {
        loading.value = false
      }
    }

    const openModal = (categoria = null) => {
      editingCategoria.value = categoria
      modalError.value = null
      
      if (categoria) {
        form.value = {
          nombre: categoria.nombre,
          descripcion: categoria.descripcion || '',
          descripcion_corta: categoria.descripcion_corta || '',
          imagen: categoria.imagen || '',
          prioridad: categoria.prioridad,
          orden: categoria.orden,
          activo: categoria.activo,
          mostrar_en_home: categoria.mostrar_en_home
        }
      } else {
        resetForm()
      }
      
      showModal.value = true
    }

    const closeModal = () => {
      showModal.value = false
      editingCategoria.value = null
      modalError.value = null
    }

    const submitForm = async () => {
      saving.value = true
      modalError.value = null
      
      try {
        if (editingCategoria.value) {
          await categoriasService.actualizar(editingCategoria.value.id, form.value)
        } else {
          await categoriasService.crear(form.value)
        }
        
        closeModal()
        await loadCategorias()
      } catch (err) {
        console.error('Error saving categoria:', err)
        modalError.value = err.response?.data?.detail || err.message
      } finally {
        saving.value = false
      }
    }

    const confirmDelete = (categoria) => {
      categoriaToDelete.value = categoria
      showDeleteModal.value = true
    }

    const deleteCategoria = async () => {
      if (!categoriaToDelete.value) return
      
      deleting.value = true
      try {
        await categoriasService.eliminar(categoriaToDelete.value.id)
        showDeleteModal.value = false
        categoriaToDelete.value = null
        await loadCategorias()
      } catch (err) {
        console.error('Error deleting categoria:', err)
        error.value = 'Error al eliminar: ' + (err.response?.data?.detail || err.message)
      } finally {
        deleting.value = false
      }
    }

    const getPrioridadClass = (prioridad) => {
      switch (prioridad) {
        case 1: return 'bg-amber-100 text-amber-700'
        case 2: return 'bg-gray-100 text-gray-700'
        case 3: return 'bg-gray-100 text-gray-500'
        default: return 'bg-gray-100 text-gray-700'
      }
    }

    const handleImageError = (e) => {
      e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100"%3E%3Crect fill="%23f3f4f6" width="200" height="100"/%3E%3Ctext x="100" y="50" text-anchor="middle" dy=".3em" fill="%239ca3af" font-size="14"%3EError%3C/text%3E%3C/svg%3E'
    }

    const handleImageFileSelect = async (event) => {
      const file = event.target.files?.[0]
      if (!file) return

      // Validar tipo
      if (!file.type.startsWith('image/')) {
        modalError.value = 'Por favor selecciona una imagen válida'
        return
      }

      // Validar tamaño (5MB max)
      const MAX_SIZE = 5 * 1024 * 1024
      if (file.size > MAX_SIZE) {
        modalError.value = 'La imagen no debe superar 5MB'
        return
      }

      uploadingImage.value = true
      modalError.value = null

      try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch(
          `${API_BASE_URL}/api/v1/upload/imagen`,
          {
            method: 'POST',
            headers: getAuthHeaders(),
            body: formData
          }
        )

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Error al subir la imagen')
        }

        const data = await response.json()
        // Convertir URL relativa a absoluta usando getImageUrl()
        form.value.imagen = getImageUrl(data.url)
        
      } catch (err) {
        console.error('Error uploading image:', err)
        modalError.value = err.message || 'Error al subir la imagen. Intenta de nuevo.'
      } finally {
        uploadingImage.value = false
        // Reset file input
        if (fileInput.value) {
          fileInput.value.value = ''
        }
      }
    }

    onMounted(loadCategorias)

    return {
      loading,
      categorias,
      error,
      showModal,
      editingCategoria,
      modalError,
      saving,
      form,
      showDeleteModal,
      categoriaToDelete,
      deleting,
      fileInput,
      uploadMethod,
      uploadingImage,
      loadCategorias,
      openModal,
      closeModal,
      submitForm,
      confirmDelete,
      deleteCategoria,
      getPrioridadClass,
      handleImageError,
      handleImageFileSelect
    }
  }
}
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
