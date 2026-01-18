<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <button 
        @click="$router.back()"
        class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <div>
        <h2 class="text-2xl font-bold text-gray-900">
          {{ isEditing ? 'Editar Producto' : 'Nuevo Producto' }}
        </h2>
        <p class="text-gray-500">
          {{ isEditing ? 'Modifica los datos del producto' : 'Completa el formulario para agregar un producto' }}
        </p>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
      <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
      <p class="text-red-800">{{ error }}</p>
    </div>

    <!-- Success Alert -->
    <div v-if="success" class="bg-green-50 border border-green-200 rounded-xl p-4 flex items-center gap-3">
      <svg class="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      <p class="text-green-800">{{ success }}</p>
    </div>

    <!-- Loading State (edit mode) -->
    <div v-if="loadingProduct" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
      <div class="animate-pulse space-y-6">
        <div class="h-8 bg-gray-200 rounded w-1/3"></div>
        <div class="grid grid-cols-2 gap-6">
          <div class="h-12 bg-gray-200 rounded"></div>
          <div class="h-12 bg-gray-200 rounded"></div>
        </div>
        <div class="h-32 bg-gray-200 rounded"></div>
      </div>
    </div>

    <!-- Form -->
    <form v-else @submit.prevent="submitForm" class="space-y-6">
      <!-- Main Info Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-6">
        <h3 class="text-lg font-semibold text-gray-900 border-b border-gray-100 pb-3">
          Información General
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Código -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Código / SKU <span class="text-red-500">*</span>
            </label>
            <input 
              v-model="form.codigo"
              type="text"
              required
              :disabled="isEditing"
              placeholder="EXT-BR-24"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 disabled:bg-gray-100 disabled:text-gray-500"
            >
            <p class="text-xs text-gray-500 mt-1">El código no se puede modificar después de crear</p>
          </div>

          <!-- Nombre -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Nombre del Producto <span class="text-red-500">*</span>
            </label>
            <input 
              v-model="form.nombre"
              type="text"
              required
              placeholder="Extensiones Brasileñas 24 pulgadas"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
            >
          </div>
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Descripción <span class="text-red-500">*</span>
          </label>
          <textarea 
            v-model="form.descripcion"
            required
            rows="4"
            placeholder="Describe el producto con detalle..."
            class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 resize-none"
          ></textarea>
        </div>
      </div>

      <!-- Pricing & Stock Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-6">
        <h3 class="text-lg font-semibold text-gray-900 border-b border-gray-100 pb-3">
          Precio y Stock
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <!-- Precio -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Precio <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">$</span>
              <input 
                v-model.number="form.precio_monto"
                type="number"
                required
                min="0"
                step="0.01"
                placeholder="0.00"
                class="w-full pl-8 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
              >
            </div>
          </div>

          <!-- Moneda -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Moneda</label>
            <select 
              v-model="form.precio_moneda"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
            >
              <option value="MXN">MXN - Peso Mexicano</option>
              <option value="USD">USD - Dólar</option>
            </select>
          </div>

          <!-- Stock Actual -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Stock Actual <span class="text-red-500">*</span>
            </label>
            <input 
              v-model.number="form.stock_actual"
              type="number"
              required
              min="0"
              placeholder="0"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
            >
          </div>

          <!-- Stock Mínimo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Stock Mínimo</label>
            <input 
              v-model.number="form.stock_minimo"
              type="number"
              min="0"
              placeholder="5"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
            >
            <p class="text-xs text-gray-500 mt-1">Alerta cuando el stock baje de este nivel</p>
          </div>
        </div>
      </div>

      <!-- Attributes Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-6">
        <h3 class="text-lg font-semibold text-gray-900 border-b border-gray-100 pb-3">
          Atributos del Cabello
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Categoría/Método -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Producto</label>
            <select 
              v-model="form.metodo"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
            >
              <option value="">Seleccionar...</option>
              <option value="clip_in">Clip-In</option>
              <option value="tape_in">Tape-In</option>
              <option value="keratin_bond">Keratin Bond</option>
              <option value="micro_link">Micro Link</option>
              <option value="sew_in">Sew-In</option>
              <option value="halo">Halo</option>
              <option value="ponytail">Ponytail</option>
              <option value="bundle">Bundle</option>
              <option value="closure">Closure</option>
              <option value="frontal">Frontal</option>
              <option value="wig">Peluca</option>
            </select>
          </div>

          <!-- Color -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Color</label>
            <select 
              v-model="form.color"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
            >
              <option value="">Seleccionar...</option>
              <option value="negro_natural">Negro Natural</option>
              <option value="negro_azabache">Negro Azabache</option>
              <option value="castano_oscuro">Castaño Oscuro</option>
              <option value="castano_medio">Castaño Medio</option>
              <option value="castano_claro">Castaño Claro</option>
              <option value="rubio_oscuro">Rubio Oscuro</option>
              <option value="rubio_medio">Rubio Medio</option>
              <option value="rubio_claro">Rubio Claro</option>
              <option value="rubio_platino">Rubio Platino</option>
              <option value="pelirrojo">Pelirrojo</option>
              <option value="borgona">Borgoña</option>
              <option value="ombre">Ombré</option>
              <option value="balayage">Balayage</option>
            </select>
          </div>

          <!-- Largo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Largo (pulgadas)</label>
            <select 
              v-model="form.largo"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
            >
              <option value="">Seleccionar...</option>
              <option value="8">8"</option>
              <option value="10">10"</option>
              <option value="12">12"</option>
              <option value="14">14"</option>
              <option value="16">16"</option>
              <option value="18">18"</option>
              <option value="20">20"</option>
              <option value="22">22"</option>
              <option value="24">24"</option>
              <option value="26">26"</option>
              <option value="28">28"</option>
              <option value="30">30"</option>
            </select>
          </div>

          <!-- Tipo de cabello -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Textura</label>
            <select 
              v-model="form.tipo"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
            >
              <option value="">Seleccionar...</option>
              <option value="liso">Liso</option>
              <option value="ondulado">Ondulado</option>
              <option value="rizado">Rizado</option>
              <option value="afro">Afro</option>
              <option value="kinky">Kinky</option>
              <option value="body_wave">Body Wave</option>
              <option value="deep_wave">Deep Wave</option>
              <option value="water_wave">Water Wave</option>
            </select>
          </div>

          <!-- Origen -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Origen</label>
            <select 
              v-model="form.origen"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
            >
              <option value="">Seleccionar...</option>
              <option value="brasileno">Brasileño</option>
              <option value="peruano">Peruano</option>
              <option value="indio">Indio</option>
              <option value="malayo">Malayo</option>
              <option value="camboyano">Camboyano</option>
              <option value="mongol">Mongol</option>
              <option value="europeo">Europeo</option>
              <option value="ruso">Ruso</option>
            </select>
          </div>

          <!-- Calidad -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Calidad</label>
            <select 
              v-model="form.calidad"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500"
            >
              <option value="">Seleccionar...</option>
              <option value="remy">Remy</option>
              <option value="virgin">Virgin</option>
              <option value="double_drawn">Double Drawn</option>
              <option value="single_drawn">Single Drawn</option>
              <option value="raw">Raw</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Image Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-6">
        <h3 class="text-lg font-semibold text-gray-900 border-b border-gray-100 pb-3">
          Imagen del Producto
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Image URL -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">URL de Imagen</label>
            <input 
              v-model="form.imagen_principal"
              type="url"
              placeholder="https://ejemplo.com/imagen.jpg"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
            >
            <p class="text-xs text-gray-500 mt-1">Ingresa la URL de una imagen o sube una</p>
          </div>

          <!-- Image Preview -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Vista Previa</label>
            <div class="w-32 h-32 bg-gray-100 rounded-xl overflow-hidden border-2 border-dashed border-gray-300">
              <img 
                v-if="form.imagen_principal"
                :src="form.imagen_principal" 
                alt="Preview"
                class="w-full h-full object-cover"
                @error="handleImageError"
              >
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Status (edit only) -->
      <div v-if="isEditing" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Estado del Producto</h3>
            <p class="text-gray-500 text-sm">Controla si el producto está visible en la tienda</p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input 
              type="checkbox" 
              v-model="form.activo" 
              class="sr-only peer"
            >
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-brand-500/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-600"></div>
            <span class="ml-3 text-sm font-medium" :class="form.activo ? 'text-green-600' : 'text-gray-500'">
              {{ form.activo ? 'Activo' : 'Inactivo' }}
            </span>
          </label>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-end gap-4">
        <button 
          type="button"
          @click="$router.back()"
          class="px-6 py-3 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl font-medium transition-colors"
        >
          Cancelar
        </button>
        <button 
          type="submit"
          :disabled="saving"
          class="px-6 py-3 text-white bg-brand-600 hover:bg-brand-700 rounded-xl font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
        >
          <svg v-if="saving" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ saving ? 'Guardando...' : (isEditing ? 'Guardar Cambios' : 'Crear Producto') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productosService } from '../../services/productos'

export default {
  name: 'ProductoForm',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const loadingProduct = ref(false)
    const saving = ref(false)
    const error = ref(null)
    const success = ref(null)
    
    const form = ref({
      codigo: '',
      nombre: '',
      descripcion: '',
      precio_monto: null,
      precio_moneda: 'MXN',
      stock_actual: 0,
      stock_minimo: 5,
      metodo: '',
      color: '',
      largo: '',
      tipo: '',
      origen: '',
      calidad: '',
      imagen_principal: '',
      activo: true
    })

    const isEditing = computed(() => !!route.params.id)
    const productId = computed(() => route.params.id)

    const handleImageError = (e) => {
      e.target.src = 'https://via.placeholder.com/100?text=Error'
    }

    const loadProduct = async () => {
      if (!isEditing.value) return
      
      loadingProduct.value = true
      error.value = null
      
      try {
        const producto = await productosService.getProducto(productId.value)
        form.value = {
          codigo: producto.codigo,
          nombre: producto.nombre,
          descripcion: producto.descripcion,
          precio_monto: producto.precio_monto,
          precio_moneda: producto.precio_moneda || 'MXN',
          stock_actual: producto.stock_actual,
          stock_minimo: producto.stock_minimo,
          metodo: producto.metodo || '',
          color: producto.color || '',
          largo: producto.largo || '',
          tipo: producto.tipo || '',
          origen: producto.origen || '',
          calidad: producto.calidad || '',
          imagen_principal: producto.imagen_principal || '',
          activo: producto.activo
        }
      } catch (err) {
        console.error('Error loading product:', err)
        error.value = 'Error al cargar el producto: ' + (err.response?.data?.detail || err.message)
      } finally {
        loadingProduct.value = false
      }
    }

    const submitForm = async () => {
      saving.value = true
      error.value = null
      success.value = null
      
      try {
        const data = {
          ...form.value,
          // Limpiar valores vacíos
          metodo: form.value.metodo || null,
          color: form.value.color || null,
          largo: form.value.largo || null,
          tipo: form.value.tipo || null,
          origen: form.value.origen || null,
          calidad: form.value.calidad || null,
          imagen_principal: form.value.imagen_principal || null
        }

        if (isEditing.value) {
          // Actualizar
          await productosService.actualizar(productId.value, data)
          success.value = 'Producto actualizado correctamente'
        } else {
          // Crear
          await productosService.crear(data)
          success.value = 'Producto creado correctamente'
        }
        
        // Redirigir después de 1.5s
        setTimeout(() => {
          router.push('/admin/productos')
        }, 1500)
        
      } catch (err) {
        console.error('Error saving product:', err)
        error.value = 'Error al guardar: ' + (err.response?.data?.detail || err.message)
      } finally {
        saving.value = false
      }
    }

    onMounted(loadProduct)

    return {
      form,
      loadingProduct,
      saving,
      error,
      success,
      isEditing,
      handleImageError,
      submitForm
    }
  }
}
</script>
