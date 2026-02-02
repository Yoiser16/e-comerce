<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Configuración</h2>
        <p class="text-gray-500">Ajustes del sistema y preferencias</p>
      </div>
    </div>

    <div class="grid lg:grid-cols-3 gap-6">
      <!-- Sidebar de secciones -->
      <div class="lg:col-span-1">
        <nav class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <button 
            v-for="section in sections" 
            :key="section.id"
            @click="activeSection = section.id"
            :class="[
              'w-full flex items-center gap-3 px-4 sm:px-5 py-3 sm:py-4 text-left transition-colors text-sm sm:text-base',
              activeSection === section.id ? 'bg-brand-50 text-brand-700 border-l-4 border-brand-600' : 'hover:bg-gray-50 text-gray-700'
            ]"
          >
            <span v-html="section.icon"></span>
            <span class="font-medium">{{ section.label }}</span>
          </button>
        </nav>
      </div>

      <!-- Contenido -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Información de la Tienda -->
        <div v-show="activeSection === 'tienda'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">Información de la Tienda</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre de la Tienda</label>
              <input type="text" v-model="config.nombreTienda" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email de Contacto</label>
              <input type="email" v-model="config.emailContacto" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Teléfono</label>
              <input type="tel" v-model="config.telefono" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Dirección</label>
              <textarea v-model="config.direccion" rows="2" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500"></textarea>
            </div>
          </div>
        </div>

        <!-- Moneda y Pagos -->
        <div v-show="activeSection === 'pagos'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">Moneda y Pagos</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Moneda</label>
              <select v-model="config.moneda" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500">
                <option value="USD">USD - Dólar Estadounidense</option>
                <option value="EUR">EUR - Euro</option>
                <option value="COP">COP - Peso Colombiano</option>
                <option value="COP">COP - Peso Colombiano</option>
              </select>
            </div>
            <div class="flex items-center justify-between py-3">
              <div>
                <p class="font-medium text-gray-900">Pagos con tarjeta</p>
                <p class="text-sm text-gray-500">Acepta pagos con tarjeta de crédito/débito</p>
              </div>
              <button 
                @click="config.pagosConTarjeta = !config.pagosConTarjeta"
                :class="[
                  'relative w-14 h-8 rounded-full transition-colors',
                  config.pagosConTarjeta ? 'bg-brand-600' : 'bg-gray-300'
                ]"
              >
                <span 
                  :class="[
                    'absolute top-1 w-6 h-6 bg-white rounded-full transition-transform shadow',
                    config.pagosConTarjeta ? 'left-7' : 'left-1'
                  ]"
                ></span>
              </button>
            </div>
            <div class="flex items-center justify-between py-3">
              <div>
                <p class="font-medium text-gray-900">Pago contra entrega</p>
                <p class="text-sm text-gray-500">Permite pago al recibir el producto</p>
              </div>
              <button 
                @click="config.pagoContraEntrega = !config.pagoContraEntrega"
                :class="[
                  'relative w-14 h-8 rounded-full transition-colors',
                  config.pagoContraEntrega ? 'bg-brand-600' : 'bg-gray-300'
                ]"
              >
                <span 
                  :class="[
                    'absolute top-1 w-6 h-6 bg-white rounded-full transition-transform shadow',
                    config.pagoContraEntrega ? 'left-7' : 'left-1'
                  ]"
                ></span>
              </button>
            </div>
          </div>
        </div>

        <!-- Envíos -->
        <div v-show="activeSection === 'envios'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">Configuración de Envíos</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Costo de envío base</label>
              <div class="flex">
                <span class="px-4 py-3 bg-gray-100 border border-r-0 border-gray-200 rounded-l-xl text-gray-500">$</span>
                <input type="number" v-model="config.costoEnvio" class="w-full px-4 py-3 border border-gray-200 rounded-r-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Envío gratis desde</label>
              <div class="flex">
                <span class="px-4 py-3 bg-gray-100 border border-r-0 border-gray-200 rounded-l-xl text-gray-500">$</span>
                <input type="number" v-model="config.envioGratisDesde" class="w-full px-4 py-3 border border-gray-200 rounded-r-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tiempo de entrega (días)</label>
              <input type="text" v-model="config.tiempoEntrega" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
          </div>
        </div>

        <!-- Notificaciones -->
        <div v-show="activeSection === 'notificaciones'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">Notificaciones</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between py-3">
              <div>
                <p class="font-medium text-gray-900">Nuevas órdenes</p>
                <p class="text-sm text-gray-500">Recibe notificación por cada nueva orden</p>
              </div>
              <button 
                @click="config.notifNuevaOrden = !config.notifNuevaOrden"
                :class="[
                  'relative w-14 h-8 rounded-full transition-colors',
                  config.notifNuevaOrden ? 'bg-brand-600' : 'bg-gray-300'
                ]"
              >
                <span 
                  :class="[
                    'absolute top-1 w-6 h-6 bg-white rounded-full transition-transform shadow',
                    config.notifNuevaOrden ? 'left-7' : 'left-1'
                  ]"
                ></span>
              </button>
            </div>
            <div class="flex items-center justify-between py-3">
              <div>
                <p class="font-medium text-gray-900">Stock bajo</p>
                <p class="text-sm text-gray-500">Alerta cuando un producto tiene poco stock</p>
              </div>
              <button 
                @click="config.notifStockBajo = !config.notifStockBajo"
                :class="[
                  'relative w-14 h-8 rounded-full transition-colors',
                  config.notifStockBajo ? 'bg-brand-600' : 'bg-gray-300'
                ]"
              >
                <span 
                  :class="[
                    'absolute top-1 w-6 h-6 bg-white rounded-full transition-transform shadow',
                    config.notifStockBajo ? 'left-7' : 'left-1'
                  ]"
                ></span>
              </button>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Umbral de stock bajo</label>
              <input type="number" v-model="config.umbralStockBajo" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
          </div>
        </div>

        <!-- Redes Sociales -->
        <div v-show="activeSection === 'redes'" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-6">Redes Sociales</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Instagram</label>
              <input type="url" v-model="config.instagram" placeholder="https://instagram.com/tu-tienda" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">WhatsApp</label>
              <input type="tel" v-model="config.whatsapp" placeholder="+57 300 123 4567" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Facebook</label>
              <input type="url" v-model="config.facebook" placeholder="https://facebook.com/tu-tienda" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">TikTok</label>
              <input type="url" v-model="config.tiktok" placeholder="https://tiktok.com/@tu-tienda" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500" />
            </div>
          </div>
        </div>

        <!-- Botón Guardar -->
        <div class="flex justify-end">
          <button class="inline-flex w-full sm:w-auto justify-center items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold px-8 py-3 rounded-xl transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Guardar Cambios
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'AdminConfig',
  setup() {
    const activeSection = ref('tienda')

    const sections = [
      { id: 'tienda', label: 'Tienda', icon: '🏪' },
      { id: 'pagos', label: 'Pagos', icon: '💳' },
      { id: 'envios', label: 'Envíos', icon: '📦' },
      { id: 'notificaciones', label: 'Notificaciones', icon: '🔔' },
      { id: 'redes', label: 'Redes Sociales', icon: '📱' },
    ]

    const config = reactive({
      nombreTienda: 'Kharis - Extensiones de Cabello',
      emailContacto: 'contacto@kharis.com',
      telefono: '+57 300 123 4567',
      direccion: 'Calle 123 #45-67, Bogotá, Colombia',
      moneda: 'COP',
      pagosConTarjeta: true,
      pagoContraEntrega: true,
      costoEnvio: 15000,
      envioGratisDesde: 200000,
      tiempoEntrega: '3-5 días hábiles',
      notifNuevaOrden: true,
      notifStockBajo: true,
      umbralStockBajo: 5,
      instagram: 'https://instagram.com/kharis_hair',
      whatsapp: '+573001234567',
      facebook: '',
      tiktok: ''
    })

    return { activeSection, sections, config }
  }
}
</script>
