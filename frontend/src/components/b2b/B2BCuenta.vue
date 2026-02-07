<template>
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Mi Cuenta</h1>
      <p class="text-gray-500 mt-1">Gestiona tu perfil y configuración empresarial</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Sidebar - Profile Card -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-xl border border-gray-100 p-6 sticky top-24">
          <!-- Avatar & Info -->
          <div class="text-center mb-6">
            <div class="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-[#C9A962] to-[#B8984F] flex items-center justify-center mb-4 shadow-lg">
              <span class="text-white text-2xl font-bold">{{ userInitials }}</span>
            </div>
            <h2 class="text-lg font-bold text-gray-900">{{ user.nombre }}</h2>
            <p class="text-sm text-gray-500">{{ user.email }}</p>
            <div class="mt-2 inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#C9A962]/10 rounded-full">
              <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
              <span class="text-xs font-medium text-[#C9A962]">Mayorista Verificado</span>
            </div>
          </div>

          <!-- Quick Stats -->
          <div class="space-y-3 pb-6 border-b border-gray-100">
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Nivel</span>
              <span class="text-sm font-bold text-[#C9A962]">{{ user.tier || 'Gold' }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Descuento</span>
              <span class="text-sm font-bold text-emerald-600">{{ user.descuento || '15' }}%</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Saldo Crédito</span>
              <span class="text-sm font-bold text-gray-900">${{ formatPrice(user.credito || 0) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Total Pedidos</span>
              <span class="text-sm font-bold text-gray-900">{{ user.totalOrders || 0 }}</span>
            </div>
          </div>

          <!-- Navigation -->
          <nav class="mt-6 space-y-1">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors text-sm font-medium',
                activeTab === tab.id 
                  ? 'bg-gray-100 text-gray-900' 
                  : 'text-gray-600 hover:bg-gray-50'
              ]"
            >
              <span v-html="tab.icon" class="w-5 h-5 text-current"></span>
              {{ tab.label }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Main Content -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Tab: Perfil -->
        <div v-if="activeTab === 'profile'" class="space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-bold text-gray-900 mb-6">Información Personal</h3>
            <div class="grid sm:grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre Completo</label>
                <input 
                  v-model="editForm.nombre"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input 
                  v-model="editForm.email"
                  type="email"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg bg-gray-50 cursor-not-allowed"
                  disabled
                />
                <p class="text-xs text-gray-400 mt-1">El email no puede modificarse</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Teléfono</label>
                <input 
                  v-model="editForm.telefono"
                  type="tel"
                  placeholder="+57 300 123 4567"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">WhatsApp</label>
                <input 
                  v-model="editForm.whatsapp"
                  type="tel"
                  placeholder="+57 300 123 4567"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-bold text-gray-900 mb-6">Información Empresarial</h3>
            <div class="grid sm:grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre de la Empresa</label>
                <input 
                  v-model="editForm.empresa"
                  type="text"
                  placeholder="Mi Salón de Belleza"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">NIT / RUT</label>
                <input 
                  v-model="editForm.nit"
                  type="text"
                  placeholder="900.123.456-7"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
              </div>
              <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Negocio</label>
                <select 
                  v-model="editForm.tipoNegocio"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                >
                  <option value="">Selecciona...</option>
                  <option value="salon">Salón de Belleza</option>
                  <option value="peluqueria">Peluquería</option>
                  <option value="spa">Spa / Centro Estético</option>
                  <option value="tienda">Tienda de Productos</option>
                  <option value="distribuidor">Distribuidor</option>
                  <option value="otro">Otro</option>
                </select>
              </div>
            </div>
          </div>

          <div class="flex justify-end gap-3">
            <button 
              @click="resetForm"
              class="px-6 py-3 border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 font-medium transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="saveProfile"
              class="px-6 py-3 bg-[#1A1A1A] hover:bg-black text-white rounded-lg font-medium transition-colors"
            >
              Guardar Cambios
            </button>
          </div>
        </div>

        <!-- Tab: Direcciones -->
        <div v-if="activeTab === 'addresses'" class="space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-bold text-gray-900">Direcciones de Envío</h3>
              <button 
                @click="openAddressModal()"
                class="px-4 py-2 bg-[#C9A962] hover:bg-[#B8984F] text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Agregar
              </button>
            </div>

            <!-- Loading state -->
            <div v-if="loadingAddresses" class="py-12 text-center">
              <svg class="w-8 h-8 text-gray-400 mx-auto mb-2 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <p class="text-sm text-gray-500">Cargando direcciones...</p>
            </div>

            <!-- Addresses list -->
            <div v-else-if="addresses.length > 0" class="space-y-4">
              <div 
                v-for="address in addresses" 
                :key="address.id"
                :class="[
                  'p-4 rounded-xl border-2 transition-colors',
                  address.is_default ? 'border-[#C9A962] bg-[#C9A962]/5' : 'border-gray-100 hover:border-gray-200'
                ]"
              >
                <div class="flex items-start justify-between gap-4">
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-1">
                      <h4 class="font-semibold text-gray-900">{{ address.etiqueta }}</h4>
                      <span v-if="address.is_default" class="text-xs px-2 py-0.5 bg-[#C9A962] text-white rounded-full">Principal</span>
                    </div>
                    <p class="text-gray-600 text-sm">
                      {{ address.direccion }}
                      <span v-if="address.complemento"> - {{ address.complemento }}</span>
                    </p>
                    <p class="text-gray-500 text-sm">{{ address.municipio }}, {{ address.departamento }}</p>
                    <p class="text-gray-400 text-xs mt-1">{{ address.telefono }}</p>
                  </div>
                  <div class="flex items-center gap-2">
                    <button 
                      v-if="!address.is_default"
                      @click="setDefaultAddress(address.id)"
                      class="p-2 text-gray-400 hover:text-[#C9A962] hover:bg-[#C9A962]/10 rounded-lg transition-colors"
                      title="Marcar como principal"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                      </svg>
                    </button>
                    <button 
                      @click="openAddressModal(address)"
                      class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                      title="Editar"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                    </button>
                    <button 
                      @click="deleteAddress(address.id)"
                      class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                      title="Eliminar"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty state -->
            <div v-else class="text-center py-12">
              <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-2xl flex items-center justify-center">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                </svg>
              </div>
              <h4 class="font-semibold text-gray-900 mb-1">No hay direcciones guardadas</h4>
              <p class="text-sm text-gray-500 mb-4">Agrega una dirección para agilizar tus pedidos</p>
              <button 
                @click="openAddressModal()"
                class="text-[#C9A962] hover:text-[#B8984F] font-medium text-sm"
              >
                + Agregar primera dirección
              </button>
            </div>
          </div>
        </div>

        <!-- Tab: Seguridad -->
        <div v-if="activeTab === 'security'" class="space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-bold text-gray-900 mb-6">Cambiar Contraseña</h3>
            <div class="max-w-md space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Contraseña Actual</label>
                <input 
                  v-model="passwordForm.current"
                  type="password"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nueva Contraseña</label>
                <input 
                  v-model="passwordForm.new"
                  type="password"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
                <p class="text-xs text-gray-400 mt-1">Mínimo 8 caracteres, incluye mayúsculas y números</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Confirmar Nueva Contraseña</label>
                <input 
                  v-model="passwordForm.confirm"
                  type="password"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962]"
                />
              </div>
              <button 
                @click="changePassword"
                class="px-6 py-3 bg-[#1A1A1A] hover:bg-black text-white rounded-lg font-medium transition-colors"
              >
                Actualizar Contraseña
              </button>
            </div>
          </div>
        </div>

        <!-- Tab: Notificaciones -->
        <div v-if="activeTab === 'notifications'" class="space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-bold text-gray-900 mb-6">Preferencias de Notificaciones</h3>
            <div class="space-y-4">
              <div 
                v-for="pref in notificationPrefs" 
                :key="pref.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-xl"
              >
                <div>
                  <h4 class="font-medium text-gray-900">{{ pref.label }}</h4>
                  <p class="text-sm text-gray-500">{{ pref.description }}</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="pref.enabled" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:ring-4 peer-focus:ring-[#C9A962]/30 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C9A962]"></div>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Agregar/Editar Dirección -->
    <div v-if="showAddressModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/50" @click="closeAddressModal"></div>
      
      <!-- Modal -->
      <div class="relative bg-white rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-gray-900">
              {{ editingAddress ? 'Editar Dirección' : 'Nueva Dirección' }}
            </h3>
            <button @click="closeAddressModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <!-- Etiqueta -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de la dirección</label>
              <input 
                v-model="addressForm.etiqueta"
                type="text"
                placeholder="Ej: Casa, Oficina, Bodega..."
                class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] text-sm"
              />
            </div>

            <!-- Dirección -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Dirección <span class="text-red-500">*</span>
              </label>
              <input 
                v-model="addressForm.direccion"
                type="text"
                placeholder="Ej: Carrera 71d #1-14 Sur"
                class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] text-sm"
              />
            </div>

            <!-- Complemento -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Complemento (opcional)</label>
              <input 
                v-model="addressForm.complemento"
                type="text"
                placeholder="Apto, oficina, local..."
                class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] text-sm"
              />
            </div>

            <!-- Departamento y Municipio -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Departamento <span class="text-red-500">*</span>
                </label>
                <select 
                  v-model="addressForm.departamento_id"
                  @change="onDepartamentoChange"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] text-sm"
                >
                  <option :value="null">Selecciona...</option>
                  <option v-for="dep in departamentos" :key="dep.id" :value="dep.id">
                    {{ dep.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Ciudad <span class="text-red-500">*</span>
                </label>
                <select 
                  v-model="addressForm.municipio_id"
                  @change="onMunicipioChange"
                  :disabled="!addressForm.departamento_id"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] text-sm disabled:bg-gray-100"
                >
                  <option :value="null">{{ addressForm.departamento_id ? 'Selecciona...' : 'Primero selecciona depto' }}</option>
                  <option v-for="mun in municipios" :key="mun.id" :value="mun.id">
                    {{ mun.name }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Barrio -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Barrio (opcional)</label>
              <input 
                v-model="addressForm.barrio"
                type="text"
                placeholder="Ej: Kennedy, Chapinero..."
                class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] text-sm"
              />
            </div>

            <!-- Teléfono -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Teléfono de contacto <span class="text-red-500">*</span>
              </label>
              <input 
                v-model="addressForm.telefono"
                type="tel"
                placeholder="Ej: 3001234567"
                class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] text-sm"
              />
            </div>

            <!-- Indicaciones -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Indicaciones (opcional)</label>
              <textarea 
                v-model="addressForm.indicaciones"
                rows="2"
                placeholder="Indicaciones para el repartidor..."
                class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] text-sm resize-none"
              ></textarea>
            </div>

            <!-- Marcar como principal -->
            <label class="flex items-center gap-3 cursor-pointer">
              <input 
                v-model="addressForm.is_default"
                type="checkbox"
                class="w-4 h-4 text-[#C9A962] focus:ring-[#C9A962] rounded"
              />
              <span class="text-sm text-gray-700">Marcar como dirección principal</span>
            </label>
          </div>

          <!-- Buttons -->
          <div class="flex gap-3 mt-6">
            <button 
              @click="closeAddressModal"
              class="flex-1 px-4 py-3 border border-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="saveAddress"
              :disabled="savingAddress || !isAddressFormValid"
              class="flex-1 px-4 py-3 bg-[#C9A962] hover:bg-[#B8984F] text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <svg v-if="savingAddress" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              {{ savingAddress ? 'Guardando...' : (editingAddress ? 'Actualizar' : 'Guardar') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted } from 'vue'
import apiClient from '@/services/api'

const COLOMBIA_API = {
  departamentos: 'https://api-colombia.com/api/v1/Department',
  ciudades: (id) => `https://api-colombia.com/api/v1/Department/${id}/cities`
}

export default {
  name: 'B2BCuenta',
  setup() {
    const activeTab = ref('profile')
    const showAddressModal = ref(false)
    const editingAddress = ref(null)
    const loadingAddresses = ref(false)
    const savingAddress = ref(false)

    const tabs = [
      { id: 'profile', label: 'Perfil', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>' },
      { id: 'addresses', label: 'Direcciones', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /></svg>' },
      { id: 'security', label: 'Seguridad', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>' },
      { id: 'notifications', label: 'Notificaciones', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>' },
    ]

    const user = computed(() => {
      return JSON.parse(localStorage.getItem('b2b_user') || '{"nombre": "Usuario", "email": "usuario@example.com"}')
    })

    const userInitials = computed(() => {
      const nombre = user.value.nombre || 'U'
      return nombre.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    })

    const editForm = reactive({
      nombre: '',
      email: '',
      telefono: '',
      whatsapp: '',
      empresa: '',
      nit: '',
      tipoNegocio: ''
    })

    const passwordForm = reactive({
      current: '',
      new: '',
      confirm: ''
    })

    // Direcciones
    const addresses = ref([])
    const departamentos = ref([])
    const municipios = ref([])

    const addressForm = reactive({
      etiqueta: 'Mi dirección',
      direccion: '',
      complemento: '',
      departamento: '',
      departamento_id: null,
      municipio: '',
      municipio_id: null,
      barrio: '',
      indicaciones: '',
      telefono: '',
      is_default: false
    })

    const isAddressFormValid = computed(() => {
      return addressForm.direccion && 
             addressForm.departamento_id && 
             addressForm.municipio_id && 
             addressForm.telefono
    })

    const notificationPrefs = ref([
      { id: 'orders', label: 'Actualizaciones de Pedidos', description: 'Recibe notificaciones sobre el estado de tus pedidos', enabled: true },
      { id: 'promotions', label: 'Promociones y Ofertas', description: 'Entérate de descuentos exclusivos para mayoristas', enabled: true },
      { id: 'stock', label: 'Alertas de Stock', description: 'Notificaciones cuando tus productos favoritos vuelvan a estar disponibles', enabled: false },
      { id: 'newsletter', label: 'Newsletter', description: 'Novedades, tendencias y tips para tu negocio', enabled: true },
    ])

    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

    function loadForm() {
      editForm.nombre = user.value.nombre || ''
      editForm.email = user.value.email || ''
      editForm.telefono = user.value.telefono || ''
      editForm.whatsapp = user.value.whatsapp || ''
      editForm.empresa = user.value.empresa || ''
      editForm.nit = user.value.nit || ''
      editForm.tipoNegocio = user.value.tipoNegocio || ''
    }

    function resetForm() {
      loadForm()
    }

    function saveProfile() {
      const userData = { ...user.value, ...editForm }
      localStorage.setItem('b2b_user', JSON.stringify(userData))
      alert('Perfil actualizado correctamente')
    }

    function changePassword() {
      if (passwordForm.new !== passwordForm.confirm) {
        alert('Las contraseñas no coinciden')
        return
      }
      if (passwordForm.new.length < 8) {
        alert('La contraseña debe tener al menos 8 caracteres')
        return
      }
      alert('Contraseña actualizada correctamente')
      passwordForm.current = ''
      passwordForm.new = ''
      passwordForm.confirm = ''
    }

    // API de Colombia
    async function loadDepartamentos() {
      try {
        const response = await fetch(COLOMBIA_API.departamentos)
        const data = await response.json()
        departamentos.value = data.sort((a, b) => a.name.localeCompare(b.name))
      } catch (error) {
        console.error('Error cargando departamentos:', error)
      }
    }

    async function loadMunicipios(departamentoId) {
      if (!departamentoId) return
      municipios.value = []
      try {
        const response = await fetch(COLOMBIA_API.ciudades(departamentoId))
        const data = await response.json()
        municipios.value = data.sort((a, b) => a.name.localeCompare(b.name))
      } catch (error) {
        console.error('Error cargando municipios:', error)
      }
    }

    function onDepartamentoChange() {
      const dep = departamentos.value.find(d => d.id === addressForm.departamento_id)
      if (dep) {
        addressForm.departamento = dep.name
        addressForm.municipio_id = null
        addressForm.municipio = ''
        loadMunicipios(dep.id)
      }
    }

    function onMunicipioChange() {
      const mun = municipios.value.find(m => m.id === addressForm.municipio_id)
      if (mun) {
        addressForm.municipio = mun.name
      }
    }

    // CRUD Direcciones
    async function loadAddresses() {
      loadingAddresses.value = true
      try {
        const response = await apiClient.get('/b2b/me/direcciones')
        addresses.value = response.data || []
      } catch (error) {
        console.error('Error cargando direcciones:', error)
        addresses.value = []
      } finally {
        loadingAddresses.value = false
      }
    }

    function openAddressModal(address = null) {
      editingAddress.value = address
      
      if (address) {
        // Editar existente
        addressForm.etiqueta = address.etiqueta
        addressForm.direccion = address.direccion
        addressForm.complemento = address.complemento || ''
        addressForm.departamento = address.departamento
        addressForm.departamento_id = address.departamento_id
        addressForm.municipio = address.municipio
        addressForm.municipio_id = address.municipio_id
        addressForm.barrio = address.barrio || ''
        addressForm.indicaciones = address.indicaciones || ''
        addressForm.telefono = address.telefono
        addressForm.is_default = address.is_default
        
        // Cargar municipios si tiene departamento
        if (address.departamento_id) {
          loadMunicipios(address.departamento_id)
        }
      } else {
        // Nueva dirección
        addressForm.etiqueta = 'Mi dirección'
        addressForm.direccion = ''
        addressForm.complemento = ''
        addressForm.departamento = ''
        addressForm.departamento_id = null
        addressForm.municipio = ''
        addressForm.municipio_id = null
        addressForm.barrio = ''
        addressForm.indicaciones = ''
        addressForm.telefono = user.value.telefono || ''
        addressForm.is_default = addresses.value.length === 0
      }
      
      showAddressModal.value = true
    }

    function closeAddressModal() {
      showAddressModal.value = false
      editingAddress.value = null
    }

    async function saveAddress() {
      if (!isAddressFormValid.value) return
      
      savingAddress.value = true
      
      try {
        const data = {
          etiqueta: addressForm.etiqueta,
          direccion: addressForm.direccion,
          complemento: addressForm.complemento,
          departamento: addressForm.departamento,
          departamento_id: addressForm.departamento_id,
          municipio: addressForm.municipio,
          municipio_id: addressForm.municipio_id,
          barrio: addressForm.barrio,
          indicaciones: addressForm.indicaciones,
          telefono: addressForm.telefono,
          is_default: addressForm.is_default
        }
        
        if (editingAddress.value) {
          // Actualizar
          await apiClient.put(`/b2b/me/direcciones/${editingAddress.value.id}`, data)
        } else {
          // Crear
          await apiClient.post('/b2b/me/direcciones', data)
        }
        
        await loadAddresses()
        closeAddressModal()
        
      } catch (error) {
        console.error('Error guardando dirección:', error)
        alert('Error al guardar la dirección. Por favor intenta nuevamente.')
      } finally {
        savingAddress.value = false
      }
    }

    async function deleteAddress(id) {
      if (!confirm('¿Estás seguro de eliminar esta dirección?')) return
      
      try {
        await apiClient.delete(`/b2b/me/direcciones/${id}`)
        await loadAddresses()
      } catch (error) {
        console.error('Error eliminando dirección:', error)
        alert('Error al eliminar la dirección')
      }
    }

    async function setDefaultAddress(id) {
      try {
        await apiClient.put(`/b2b/me/direcciones/${id}/default`)
        await loadAddresses()
      } catch (error) {
        console.error('Error al marcar dirección como principal:', error)
      }
    }

    onMounted(async () => {
      loadForm()
      await loadDepartamentos()
      await loadAddresses()
    })

    return {
      activeTab, tabs, user, userInitials,
      editForm, passwordForm, addresses, notificationPrefs,
      showAddressModal, editingAddress, loadingAddresses, savingAddress,
      departamentos, municipios, addressForm, isAddressFormValid,
      formatPrice, resetForm, saveProfile, changePassword,
      openAddressModal, closeAddressModal, saveAddress, deleteAddress, setDefaultAddress,
      onDepartamentoChange, onMunicipioChange
    }
  }
}
</script>
