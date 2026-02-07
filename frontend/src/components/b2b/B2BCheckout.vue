<template>
  <div class="min-h-screen bg-[#FAFAFA]">
    <div class="max-w-[1100px] mx-auto px-4 sm:px-6 lg:px-8 py-6 lg:py-8">
      
      <!-- Breadcrumb -->
      <nav class="flex items-center gap-2 text-sm text-gray-400 mb-6">
        <router-link to="/portal" class="hover:text-gray-600 transition-colors">Portal</router-link>
        <span>/</span>
        <router-link to="/portal/carrito" class="hover:text-gray-600 transition-colors">Carrito</router-link>
        <span>/</span>
        <span class="text-gray-700">Checkout</span>
      </nav>

      <!-- Step Indicator -->
      <div class="flex items-center justify-center gap-2 mb-8">
        <div 
          v-for="(stepInfo, index) in visibleSteps" 
          :key="index"
          class="flex items-center gap-2"
        >
          <div 
            class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors"
            :class="getStepClass(index)"
          >
            <svg v-if="isStepComplete(index)" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            <span v-else>{{ index + 1 }}</span>
          </div>
          <span 
            class="text-sm hidden sm:inline"
            :class="currentStep >= index ? 'text-gray-900' : 'text-gray-400'"
          >{{ stepInfo.title }}</span>
          <div v-if="index < visibleSteps.length - 1" class="w-12 h-px bg-gray-300 mx-2"></div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
        
        <!-- Left Column: Steps -->
        <div class="lg:col-span-8">
          
          <!-- ====================================
               STEP 0: LOADING INICIAL
               (Mientras se verifican direcciones)
          ==================================== -->
          <div v-if="currentStep === 0 && loadingAddresses" class="bg-white rounded-lg border border-gray-200 p-5 sm:p-6">
            <div class="py-12 text-center">
              <svg class="w-10 h-10 text-gray-400 mx-auto mb-3 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <p class="text-gray-600 font-medium">Cargando información de entrega...</p>
              <p class="text-sm text-gray-400 mt-1">Un momento por favor</p>
            </div>
          </div>

          <!-- ====================================
               STEP 0: REVISAR FORMA DE ENTREGA
               (Solo si tiene direcciones guardadas)
          ==================================== -->
          <div v-else-if="currentStep === 0 && hasSavedAddress && !showAddressForm" class="bg-white rounded-lg border border-gray-200 p-5 sm:p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Selecciona tu dirección de entrega</h2>

            <!-- Lista de direcciones guardadas -->
            <div class="space-y-3">
              <div 
                v-for="address in savedAddresses" 
                :key="address.id"
                @click="selectedAddressId = address.id"
                :class="[
                  'border rounded-lg p-4 sm:p-5 cursor-pointer transition-colors',
                  selectedAddressId === address.id 
                    ? 'border-blue-500 bg-blue-50/50' 
                    : 'border-gray-200 hover:border-gray-300'
                ]"
              >
                <div class="flex items-start gap-3">
                  <input 
                    type="radio" 
                    :checked="selectedAddressId === address.id"
                    class="mt-1 w-4 h-4 text-blue-600"
                    @click.stop
                    @change="selectedAddressId = address.id"
                  />
                  <div class="flex-1">
                    <div class="flex items-center justify-between mb-1">
                      <div class="flex items-center gap-2">
                        <span class="font-medium text-gray-900">{{ address.etiqueta || 'Mi dirección' }}</span>
                        <span v-if="address.is_default" class="text-xs px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full">Principal</span>
                      </div>
                      <span class="text-gray-700 font-medium">${{ formatPrice(shippingCost) }}</span>
                    </div>
                    <p class="text-gray-600 text-sm mb-1">
                      {{ address.direccion }}
                      <span v-if="address.complemento"> - {{ address.complemento }}</span>
                    </p>
                    <p class="text-gray-500 text-sm">{{ address.municipio }}, {{ address.departamento }}</p>
                    <p v-if="address.telefono" class="text-gray-400 text-xs mt-1">Tel: {{ address.telefono }}</p>
                  </div>
                </div>
              </div>

              <!-- Botón agregar nueva dirección -->
              <button 
                @click="showAddressForm = true"
                class="w-full p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50/30 transition-all flex items-center justify-center gap-2 text-gray-600 hover:text-blue-600"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <span class="font-medium">Agregar nueva dirección</span>
              </button>
            </div>

            <!-- Botón continuar -->
            <div class="flex justify-center mt-6">
              <button 
                @click="continueWithSavedAddress"
                :disabled="!selectedAddressId"
                class="px-10 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Continuar
              </button>
            </div>
          </div>

          <!-- ====================================
               STEP 0/1: FORMULARIO DE DIRECCIÓN
               (Si no tiene dirección o quiere modificar)
          ==================================== -->
          <div v-else-if="(currentStep === 0 && !hasSavedAddress) || showAddressForm" class="bg-white rounded-lg border border-gray-200 p-5 sm:p-6">
            <div class="flex items-center justify-between mb-1">
              <h2 class="text-xl font-semibold text-gray-900">
                {{ hasSavedAddress ? 'Modificar domicilio' : 'Nuevo domicilio' }}
              </h2>
              <button 
                v-if="hasSavedAddress && showAddressForm"
                @click="showAddressForm = false"
                class="text-gray-500 hover:text-gray-700"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
            <p class="text-sm text-gray-500 mb-6">Ingresa tu dirección de entrega</p>

            <!-- Botón Completar con Ubicación -->
            <button 
              @click="getMyLocation"
              :disabled="loadingLocation"
              class="w-full mb-6 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50/30 transition-all flex items-center justify-center gap-3 group"
            >
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                <svg v-if="!loadingLocation" class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <svg v-else class="w-5 h-5 text-blue-600 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
              </div>
              <div class="text-left">
                <p class="font-medium text-gray-900">{{ loadingLocation ? 'Obteniendo ubicación...' : 'Completar con mi ubicación' }}</p>
                <p class="text-xs text-gray-500">Usaremos GPS para autocompletar tu dirección</p>
              </div>
            </button>

            <!-- Formulario de dirección -->
            <div class="space-y-4">
              <!-- Dirección -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Dirección o lugar de entrega <span class="text-red-500">*</span>
                </label>
                <input 
                  v-model="form.direccion"
                  type="text"
                  placeholder="Ej: Carrera 71d #1-14 Sur"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm transition-colors"
                />
              </div>

              <!-- Complemento -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Apartamento / Casa / Oficina <span class="text-gray-400 font-normal">(opcional)</span>
                </label>
                <input 
                  v-model="form.complemento"
                  type="text"
                  placeholder="Ej: Apto 201, Torre B"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm transition-colors"
                />
              </div>

              <!-- Departamento y Municipio -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Departamento -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Departamento <span class="text-red-500">*</span>
                  </label>
                  <div class="relative">
                    <select 
                      v-model="form.departamentoId"
                      @change="onDepartamentoChange"
                      :disabled="loadingDepartamentos"
                      class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm transition-colors appearance-none bg-white"
                    >
                      <option :value="null" disabled>Selecciona un departamento</option>
                      <option 
                        v-for="dep in departamentos" 
                        :key="dep.id" 
                        :value="dep.id"
                      >
                        {{ dep.name }}
                      </option>
                    </select>
                    <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                    <div v-if="loadingDepartamentos" class="absolute right-10 top-1/2 -translate-y-1/2">
                      <svg class="w-4 h-4 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- Municipio -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Municipio / Ciudad <span class="text-red-500">*</span>
                  </label>
                  <div class="relative">
                    <select 
                      v-model="form.municipioId"
                      @change="onMunicipioChange"
                      :disabled="!form.departamentoId || loadingMunicipios"
                      class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm transition-colors appearance-none bg-white disabled:bg-gray-100 disabled:cursor-not-allowed"
                    >
                      <option :value="null" disabled>{{ form.departamentoId ? 'Selecciona un municipio' : 'Primero selecciona departamento' }}</option>
                      <option 
                        v-for="mun in municipios" 
                        :key="mun.id" 
                        :value="mun.id"
                      >
                        {{ mun.name }}
                      </option>
                    </select>
                    <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                    <div v-if="loadingMunicipios" class="absolute right-10 top-1/2 -translate-y-1/2">
                      <svg class="w-4 h-4 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Barrio -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Barrio <span class="text-gray-400 font-normal">(opcional)</span>
                </label>
                <input 
                  v-model="form.barrio"
                  type="text"
                  placeholder="Ej: Kennedy, Chapinero, Centro"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm transition-colors"
                />
              </div>

              <!-- Indicaciones de entrega -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Indicaciones para la entrega <span class="text-gray-400 font-normal">(opcional)</span>
                </label>
                <textarea 
                  v-model="form.indicaciones"
                  placeholder="Ej: Entre calles, color del edificio, no tiene timbre..."
                  maxlength="128"
                  rows="2"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm transition-colors resize-none"
                ></textarea>
                <p class="text-xs text-gray-400 mt-1 text-right">{{ form.indicaciones?.length || 0 }} / 128 caracteres</p>
              </div>

              <!-- Tipo de domicilio -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de domicilio</label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input 
                      v-model="form.tipoDomicilio"
                      type="radio"
                      value="Residencial"
                      class="w-4 h-4 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm text-gray-700">Residencial</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input 
                      v-model="form.tipoDomicilio"
                      type="radio"
                      value="Laboral"
                      class="w-4 h-4 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm text-gray-700">Laboral</span>
                  </label>
                </div>
              </div>

              <!-- Separador -->
              <hr class="my-6 border-gray-200" />

              <!-- Datos de contacto -->
              <div>
                <h3 class="text-sm font-semibold text-gray-900 mb-1">Datos de contacto</h3>
                <p class="text-xs text-gray-500 mb-4">Te llamaremos si hay un problema con la entrega.</p>
                
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Nombre y apellido <span class="text-red-500">*</span>
                    </label>
                    <input 
                      v-model="form.nombreContacto"
                      type="text"
                      placeholder="Nombre completo"
                      class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm transition-colors"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Teléfono <span class="text-red-500">*</span>
                    </label>
                    <input 
                      v-model="form.telefono"
                      type="tel"
                      placeholder="Ej: 3217355070"
                      class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm transition-colors"
                    />
                  </div>
                </div>
              </div>

              <!-- Botones -->
              <div class="pt-4 flex gap-3">
                <button 
                  v-if="hasSavedAddress && showAddressForm"
                  @click="showAddressForm = false"
                  class="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancelar
                </button>
                <button 
                  @click="saveAddressAndContinue"
                  :disabled="!isAddressValid || savingAddress"
                  class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  <svg v-if="savingAddress" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  {{ savingAddress ? 'Guardando...' : 'Guardar y continuar' }}
                </button>
              </div>
            </div>
          </div>

          <!-- ====================================
               STEP 1: MÉTODO DE PAGO
          ==================================== -->
          <div v-if="currentStep === 1" class="bg-white rounded-lg border border-gray-200 p-5 sm:p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-1">Elige el método de pago</h2>
            <p class="text-sm text-gray-500 mb-6">Selecciona cómo deseas completar tu pedido</p>

            <!-- Mostrar dirección seleccionada -->
            <div class="bg-gray-50 rounded-lg p-4 mb-6 flex items-start gap-3">
              <svg class="w-5 h-5 text-gray-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <div class="flex-1">
                <p class="text-sm text-gray-700 font-medium">Envío a:</p>
                <p class="text-sm text-gray-600">{{ fullAddress }}</p>
                <button 
                  @click="goToStep(0)"
                  class="text-blue-600 hover:text-blue-700 text-sm mt-1"
                >
                  Cambiar dirección
                </button>
              </div>
            </div>

            <div class="space-y-3">
              <!-- WhatsApp Option -->
              <label 
                class="flex items-start gap-4 p-4 border rounded-lg cursor-pointer transition-colors"
                :class="form.metodoPago === 'whatsapp' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
              >
                <input 
                  v-model="form.metodoPago"
                  type="radio"
                  value="whatsapp"
                  class="mt-1 w-4 h-4 text-gray-900 focus:ring-gray-500"
                />
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                    </svg>
                    <p class="font-medium text-gray-900">Finalizar por WhatsApp</p>
                  </div>
                  <p class="text-sm text-gray-500 mt-1">Enviaremos tu pedido a nuestro asesor para coordinar el pago (transferencia, Nequi, Daviplata)</p>
                </div>
              </label>

              <!-- Wompi Option -->
              <label 
                class="flex items-start gap-4 p-4 border rounded-lg cursor-pointer transition-colors"
                :class="form.metodoPago === 'wompi' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
              >
                <input 
                  v-model="form.metodoPago"
                  type="radio"
                  value="wompi"
                  class="mt-1 w-4 h-4 text-gray-900 focus:ring-gray-500"
                />
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                    </svg>
                    <p class="font-medium text-gray-900">Pagar en línea (Wompi)</p>
                  </div>
                  <p class="text-sm text-gray-500 mt-1">Tarjeta de crédito/débito, PSE, Bancolombia, Nequi, Efecty</p>
                </div>
              </label>
            </div>

            <!-- Notas adicionales -->
            <div class="mt-6">
              <label class="block text-sm text-gray-600 mb-1">Notas adicionales (opcional)</label>
              <textarea 
                v-model="form.notas"
                placeholder="Instrucciones especiales, horarios de entrega preferidos..."
                rows="3"
                class="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:ring-1 focus:ring-gray-300 focus:border-gray-300 text-sm resize-none"
              ></textarea>
            </div>

            <!-- Buttons -->
            <div class="flex gap-3 mt-6">
              <button 
                @click="goToStep(0)"
                class="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                ← Volver
              </button>
              <button 
                @click="submitOrder"
                :disabled="isSubmitting"
                class="flex-1 sm:flex-none px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <svg v-if="isSubmitting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                {{ isSubmitting ? 'Procesando...' : form.metodoPago === 'whatsapp' ? 'Enviar por WhatsApp' : 'Pagar ahora' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Right Column: Order Summary -->
        <div class="lg:col-span-4">
          <div class="bg-white rounded-lg border border-gray-200 p-5 sticky top-24">
            <h3 class="font-semibold text-gray-900 mb-4">Resumen de compra</h3>
            
            <!-- Items count and subtotal -->
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">Producto</span>
                <span class="text-gray-900">${{ formatPrice(subtotal) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Envío</span>
                <span :class="shippingCost === 0 ? 'text-green-600' : 'text-gray-900'">
                  {{ shippingCost === 0 ? 'Gratis' : `$${formatPrice(shippingCost)}` }}
                </span>
              </div>
            </div>

            <hr class="my-4 border-gray-100" />

            <!-- Total -->
            <div class="flex justify-between items-baseline">
              <span class="text-gray-900 font-medium">Total</span>
              <span class="text-2xl font-bold text-gray-900">${{ formatPrice(total) }}</span>
            </div>

            <!-- Free shipping progress -->
            <div v-if="shippingCost > 0" class="mt-4 p-3 bg-blue-50 rounded-lg">
              <p class="text-xs text-blue-800">
                🚚 Agrega <strong>${{ formatPrice(freeShippingThreshold - subtotal) }}</strong> más para envío gratis
              </p>
              <div class="mt-2 h-1.5 bg-blue-100 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-blue-600 rounded-full transition-all"
                  :style="{ width: `${Math.min((subtotal / freeShippingThreshold) * 100, 100)}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

// API de Colombia - Datos oficiales de departamentos y municipios
const COLOMBIA_API = {
  departamentos: 'https://api-colombia.com/api/v1/Department',
  ciudades: (departmentId) => `https://api-colombia.com/api/v1/Department/${departmentId}/cities`
}

export default {
  name: 'B2BCheckout',
  setup() {
    const router = useRouter()

    // State
    const currentStep = ref(0)
    const cartItems = ref([])
    const isSubmitting = ref(false)
    const savingAddress = ref(false)
    const loadingLocation = ref(false)
    const loadingDepartamentos = ref(false)
    const loadingMunicipios = ref(false)
    const freeShippingThreshold = 500000

    // Direcciones guardadas
    const savedAddresses = ref([])
    const selectedAddressId = ref(null)
    const showAddressForm = ref(false)
    const loadingAddresses = ref(true) // Inicia en true para evitar flash
    
    // Computed: dirección seleccionada
    const selectedAddress = computed(() => {
      if (!selectedAddressId.value) return null
      return savedAddresses.value.find(a => a.id === selectedAddressId.value)
    })
    
    const hasSavedAddress = computed(() => savedAddresses.value.length > 0)

    // Ubicaciones
    const departamentos = ref([])
    const municipios = ref([])

    // Steps - simplificado: Entrega y Pago
    const visibleSteps = computed(() => [
      { title: 'Entrega' },
      { title: 'Pago' }
    ])

    const form = reactive({
      direccion: '',
      complemento: '',
      departamento: '',
      departamentoId: null,
      municipio: '',
      municipioId: null,
      barrio: '',
      indicaciones: '',
      tipoDomicilio: 'Residencial',
      nombreContacto: '',
      telefono: '',
      metodoPago: 'whatsapp',
      notas: '',
      lat: null,
      lng: null
    })

    // Computed
    const isAddressValid = computed(() => {
      return form.direccion && 
             form.departamentoId && 
             form.municipioId && 
             form.telefono && 
             form.nombreContacto
    })

    const fullAddress = computed(() => {
      const addr = selectedAddress.value && !showAddressForm.value ? selectedAddress.value : form
      const parts = [addr.direccion]
      if (addr.complemento) parts.push(addr.complemento)
      if (addr.barrio) parts.push(addr.barrio)
      if (addr.municipio) parts.push(addr.municipio)
      if (addr.departamento) parts.push(addr.departamento)
      return parts.filter(p => p).join(', ')
    })

    const subtotal = computed(() => {
      return cartItems.value.reduce((sum, item) => {
        const qty = item.cantidad || item.quantity || 1
        const price = item.precio || item.wholesalePrice || 0
        return sum + (price * qty)
      }, 0)
    })

    const shippingCost = computed(() => {
      if (subtotal.value >= freeShippingThreshold) return 0
      return 17100 // Costo estándar de envío
    })

    const total = computed(() => subtotal.value + shippingCost.value)

    // Methods
    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

    function getStepClass(index) {
      if (currentStep.value > index) return 'bg-gray-900 text-white'
      if (currentStep.value === index) return 'bg-gray-900 text-white'
      return 'bg-gray-200 text-gray-500'
    }

    function isStepComplete(index) {
      return currentStep.value > index
    }

    function loadCart() {
      const cart = localStorage.getItem('b2b_cart')
      if (cart) {
        try {
          const data = JSON.parse(cart)
          cartItems.value = data.items || []
        } catch {
          cartItems.value = []
        }
      }
    }

    async function loadUserData() {
      const userData = localStorage.getItem('b2b_user')
      if (userData) {
        try {
          const user = JSON.parse(userData)
          form.nombreContacto = `${user.nombre || ''} ${user.apellido || ''}`.trim()
          form.telefono = user.telefono || ''
        } catch {
          // Sin datos
        }
      }

      // Cargar TODAS las direcciones del usuario desde el backend
      loadingAddresses.value = true
      try {
        const response = await apiClient.get('/b2b/me/direcciones')
        if (response.data && Array.isArray(response.data)) {
          savedAddresses.value = response.data
          
          // Seleccionar la dirección principal por defecto
          const defaultAddr = response.data.find(a => a.is_default) || response.data[0]
          if (defaultAddr) {
            selectedAddressId.value = defaultAddr.id
            
            // Cargar municipios si tiene departamento
            if (defaultAddr.departamento_id) {
              await loadMunicipios(defaultAddr.departamento_id)
            }
          }
        }
      } catch (error) {
        console.log('No hay direcciones guardadas:', error.message)
        savedAddresses.value = []
      } finally {
        loadingAddresses.value = false
      }
    }

    async function loadDepartamentos() {
      loadingDepartamentos.value = true
      try {
        const response = await fetch(COLOMBIA_API.departamentos)
        const data = await response.json()
        departamentos.value = data.sort((a, b) => a.name.localeCompare(b.name))
      } catch (error) {
        console.error('Error cargando departamentos:', error)
      } finally {
        loadingDepartamentos.value = false
      }
    }

    async function loadMunicipios(departamentoId) {
      if (!departamentoId) return
      
      loadingMunicipios.value = true
      municipios.value = []
      
      try {
        const response = await fetch(COLOMBIA_API.ciudades(departamentoId))
        const data = await response.json()
        municipios.value = data.sort((a, b) => a.name.localeCompare(b.name))
      } catch (error) {
        console.error('Error cargando municipios:', error)
      } finally {
        loadingMunicipios.value = false
      }
    }

    function onDepartamentoChange() {
      const dep = departamentos.value.find(d => d.id === form.departamentoId)
      if (dep) {
        form.departamento = dep.name
        form.municipioId = null
        form.municipio = ''
        loadMunicipios(dep.id)
      }
    }

    function onMunicipioChange() {
      const mun = municipios.value.find(m => m.id === form.municipioId)
      if (mun) {
        form.municipio = mun.name
      }
    }

    async function getMyLocation() {
      if (!navigator.geolocation) {
        alert('Tu navegador no soporta geolocalización')
        return
      }

      loadingLocation.value = true

      try {
        const position = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
          })
        })

        const { latitude, longitude } = position.coords
        form.lat = latitude
        form.lng = longitude

        // Reverse geocoding para obtener la dirección
        await reverseGeocode(latitude, longitude)
        
      } catch (error) {
        console.error('Error obteniendo ubicación:', error)
        if (error.code === 1) {
          alert('Permiso de ubicación denegado. Por favor habilítalo en la configuración de tu navegador.')
        } else if (error.code === 2) {
          alert('No se pudo obtener la ubicación. Verifica tu conexión GPS.')
        } else {
          alert('Error al obtener ubicación. Por favor ingresa los datos manualmente.')
        }
      } finally {
        loadingLocation.value = false
      }
    }

    async function reverseGeocode(lat, lng) {
      try {
        // Usamos Nominatim (OpenStreetMap) para reverse geocoding gratuito
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1&accept-language=es`,
          { headers: { 'User-Agent': 'KharisB2B/1.0' } }
        )
        const data = await response.json()

        if (data.address) {
          const addr = data.address
          
          // Construir dirección
          const roadParts = [addr.road, addr.house_number].filter(Boolean)
          form.direccion = roadParts.join(' ') || addr.display_name?.split(',')[0] || ''
          form.barrio = addr.suburb || addr.neighbourhood || addr.quarter || ''
          
          // Buscar departamento en nuestra lista
          const depName = addr.state || ''
          const foundDep = departamentos.value.find(
            d => d.name.toLowerCase() === depName.toLowerCase() ||
                 d.name.toLowerCase().includes(depName.toLowerCase())
          )
          
          if (foundDep) {
            form.departamentoId = foundDep.id
            form.departamento = foundDep.name
            await loadMunicipios(foundDep.id)
            
            // Buscar municipio
            const cityName = addr.city || addr.town || addr.municipality || ''
            const foundMun = municipios.value.find(
              m => m.name.toLowerCase() === cityName.toLowerCase() ||
                   m.name.toLowerCase().includes(cityName.toLowerCase())
            )
            
            if (foundMun) {
              form.municipioId = foundMun.id
              form.municipio = foundMun.name
            }
          }
        }
      } catch (error) {
        console.error('Error en reverse geocoding:', error)
      }
    }

    function goToStep(step) {
      currentStep.value = step
      if (step === 0) {
        showAddressForm.value = false
      }
    }

    function continueWithSavedAddress() {
      // Usar la dirección seleccionada
      const addr = selectedAddress.value
      if (!addr) return
      
      form.direccion = addr.direccion
      form.complemento = addr.complemento || ''
      form.departamento = addr.departamento
      form.departamentoId = addr.departamento_id
      form.municipio = addr.municipio
      form.municipioId = addr.municipio_id
      form.barrio = addr.barrio || ''
      form.indicaciones = addr.indicaciones || ''
      form.tipoDomicilio = addr.tipo_domicilio || 'Residencial'
      form.lat = addr.latitud
      form.lng = addr.longitud
      form.telefono = addr.telefono || form.telefono
      
      currentStep.value = 1
    }

    async function saveAddressAndContinue() {
      if (!isAddressValid.value) return
      
      savingAddress.value = true
      
      try {
        // Guardar dirección en el backend (crear nueva)
        const response = await apiClient.post('/b2b/me/direcciones', {
          etiqueta: form.tipoDomicilio || 'Mi dirección',
          direccion: form.direccion,
          complemento: form.complemento,
          departamento: form.departamento,
          departamento_id: form.departamentoId,
          municipio: form.municipio,
          municipio_id: form.municipioId,
          barrio: form.barrio,
          indicaciones: form.indicaciones,
          telefono: form.telefono,
          latitud: form.lat,
          longitud: form.lng,
          is_default: savedAddresses.value.length === 0 // Primera dirección es default
        })
        
        console.log('✅ Dirección guardada en backend')
        
        // Recargar direcciones y seleccionar la nueva
        await loadUserData()
        if (response.data && response.data.id) {
          selectedAddressId.value = response.data.id
        }
        
        showAddressForm.value = false
        currentStep.value = 1
        
      } catch (error) {
        console.error('Error guardando dirección:', error)
        // Continuar de todas formas al paso de pago
        currentStep.value = 1
      } finally {
        savingAddress.value = false
      }
    }

    async function submitOrder() {
      if (isSubmitting.value) return
      isSubmitting.value = true

      try {
        if (form.metodoPago === 'whatsapp') {
          const itemsText = cartItems.value.map(item => {
            const name = item.nombre || item.name
            const qty = item.cantidad || item.quantity
            const price = item.precio || item.wholesalePrice
            return `• ${name} x${qty} = $${formatPrice(price * qty)}`
          }).join('%0A')

          const direccionCompleta = [
            form.direccion,
            form.complemento,
            form.barrio,
            form.municipio,
            form.departamento
          ].filter(Boolean).join(', ')

          const message = `🛒 *PEDIDO MAYORISTA*%0A%0A` +
            `📦 *Productos:*%0A${itemsText}%0A%0A` +
            `💰 *Subtotal:* $${formatPrice(subtotal.value)}%0A` +
            `🚚 *Envío:* $${formatPrice(shippingCost.value)}%0A` +
            `*TOTAL: $${formatPrice(total.value)}*%0A%0A` +
            `📍 *Dirección:*%0A${direccionCompleta}%0A%0A` +
            `👤 *Contacto:* ${form.nombreContacto}%0A` +
            `📱 *Teléfono:* ${form.telefono}%0A` +
            (form.indicaciones ? `📝 *Indicaciones:* ${form.indicaciones}%0A` : '') +
            (form.notas ? `📝 *Notas:* ${form.notas}` : '')

          const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER || '573001234567'
          window.open(`https://wa.me/${whatsappNumber}?text=${message}`, '_blank')
          localStorage.removeItem('b2b_cart')
          router.push({ path: '/portal/pedidos', query: { success: 'whatsapp' } })
        } else {
          // TODO: Integrar Wompi widget
          alert('Redirigiendo a Wompi para completar el pago...')
          localStorage.removeItem('b2b_cart')
          router.push({ path: '/portal/pedidos', query: { success: 'wompi', pending: 'true' } })
        }
      } catch (error) {
        console.error('Error al procesar pedido:', error)
        alert('Error al procesar el pedido. Por favor intenta nuevamente.')
      } finally {
        isSubmitting.value = false
      }
    }

    onMounted(async () => {
      loadCart()
      await loadDepartamentos()
      await loadUserData()

      if (cartItems.value.length === 0) {
        router.replace('/portal/carrito')
      }
    })

    return {
      currentStep,
      visibleSteps,
      cartItems,
      isSubmitting,
      savingAddress,
      loadingLocation,
      loadingDepartamentos,
      loadingMunicipios,
      departamentos,
      municipios,
      form,
      hasSavedAddress,
      showAddressForm,
      savedAddresses,
      selectedAddressId,
      selectedAddress,
      loadingAddresses,
      isAddressValid,
      fullAddress,
      subtotal,
      shippingCost,
      total,
      freeShippingThreshold,
      formatPrice,
      getStepClass,
      isStepComplete,
      goToStep,
      getMyLocation,
      onDepartamentoChange,
      onMunicipioChange,
      continueWithSavedAddress,
      saveAddressAndContinue,
      submitOrder
    }
  }
}
</script>
