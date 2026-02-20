<template>
  <div class="min-h-screen flex flex-col bg-white">
    
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- LOADING INICIAL - Mientras determina el paso correcto               -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <div v-if="initialLoading" class="min-h-screen flex items-center justify-center bg-white">
      <div class="text-center">
        <div class="w-12 h-12 border-2 border-[#D81B60] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-[#7A7A7A] text-sm">Preparando tu pedido...</p>
      </div>
    </div>
    
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- CHECKOUT PRINCIPAL (solo se muestra cuando termina la carga)        -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <template v-else>
    
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- HEADER - Optimizado para móvil                                       -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <header class="bg-white border-b border-[#E5E7EB]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 sm:py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="text-[#7A7A7A] hover:text-[#D81B60] transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
          </router-link>
          <router-link to="/" class="font-luxury text-xl sm:text-2xl tracking-wide text-[#1A1A1A]">
            Kharis
          </router-link>
          <div class="flex items-center gap-1.5 text-xs sm:text-sm text-[#6B7280]">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
            </svg>
            <span class="hidden sm:inline">Compra Segura</span>
          </div>
        </div>
      </div>
    </header>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- STEPPER VISUAL - Compacto para móvil                                 -->
    <!-- En móvil: solo visible cuando mobileShowForm es true                 -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <div class="bg-white border-b border-[#E5E7EB] py-4 sm:py-6" :class="{ 'hidden lg:block': !mobileShowForm }">
      <div class="max-w-md mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-center gap-2 sm:gap-3">
          <!-- Paso 1 -->
          <div class="flex items-center gap-1.5 sm:gap-2" @click="goToStep(1)">
            <div :class="[
              'w-8 h-8 sm:w-9 sm:h-9 rounded-full flex items-center justify-center text-xs sm:text-sm font-bold transition-all cursor-pointer shadow-sm',
              currentStep >= 1 ? 'bg-[#D81B60] text-white' : 'bg-white border-2 border-gray-200 text-gray-400'
            ]">
              <svg v-if="currentStep > 1" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <span v-else>1</span>
            </div>
          </div>
          
          <!-- Línea conectora 1-2 -->
          <div class="w-12 sm:w-20 h-0.5 bg-gray-200 rounded-full overflow-hidden">
            <div 
              class="h-full bg-[#D81B60] transition-all duration-300"
              :style="{ width: currentStep > 1 ? '100%' : '0%' }"
            ></div>
          </div>
          
          <!-- Paso 2 -->
          <div class="flex items-center gap-1.5 sm:gap-2" @click="goToStep(2)">
            <div :class="[
              'w-8 h-8 sm:w-9 sm:h-9 rounded-full flex items-center justify-center text-xs sm:text-sm font-bold transition-all cursor-pointer shadow-sm',
              currentStep >= 2 ? 'bg-[#D81B60] text-white' : 'bg-white border-2 border-gray-200 text-gray-400'
            ]">
              <svg v-if="currentStep > 2" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <span v-else>2</span>
            </div>
          </div>
          
          <!-- Línea conectora 2-3 -->
          <div class="w-12 sm:w-20 h-0.5 bg-gray-200 rounded-full overflow-hidden">
            <div 
              class="h-full bg-[#D81B60] transition-all duration-300"
              :style="{ width: currentStep > 2 ? '100%' : '0%' }"
            ></div>
          </div>
          
          <!-- Paso 3 -->
          <div class="flex items-center gap-1.5 sm:gap-2" @click="goToStep(3)">
            <div :class="[
              'w-8 h-8 sm:w-9 sm:h-9 rounded-full flex items-center justify-center text-xs sm:text-sm font-bold transition-all cursor-pointer shadow-sm',
              currentStep >= 3 ? 'bg-[#D81B60] text-white' : 'bg-white border-2 border-gray-200 text-gray-400'
            ]">
              <span>3</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- CONTENIDO PRINCIPAL - Layout móvil fluid                             -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <main class="flex-1 bg-white lg:bg-[#FAFAFA]">
      <div class="max-w-7xl mx-auto lg:px-6 lg:py-8">
        <div class="grid grid-cols-1 lg:grid-cols-12 lg:gap-10">
          
          <!-- COLUMNA IZQUIERDA: Formularios -->
          <!-- En móvil: solo visible si mobileShowForm es true -->
          <!-- En desktop (lg:): siempre visible -->
          <div id="checkout-form" class="lg:col-span-8 order-2 lg:order-1" :class="{ 'hidden lg:block': !mobileShowForm }">
            <!-- Barra superior móvil: volver al resumen -->
            <div class="lg:hidden px-5 py-3 border-b border-[#f0f0f0]">
              <div class="flex items-center justify-between">
                <button 
                  @click="showMobileSummary"
                  class="flex items-center gap-2 text-[#6B7280] hover:text-[#1A1A1A] transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                  </svg>
                  <span class="text-sm">Volver</span>
                </button>
                <button 
                  @click="showMobileSummary"
                  class="text-xs text-[#c11252] font-medium hover:underline"
                >
                  Ver resumen
                </button>
              </div>
            </div>
            
            <!-- Contenedor fluid en móvil, tarjeta en desktop -->
            <div class="lg:bg-white lg:rounded-lg lg:shadow-sm lg:border lg:border-[#E5E7EB] lg:overflow-hidden">
              
              <!-- ═══════════════════════════════════════════════════════════ -->
              <!-- PASO 1: Datos de Contacto - Diseño móvil optimizado          -->
              <!-- ═══════════════════════════════════════════════════════════ -->
              <div v-show="currentStep === 1">
                <!-- Header de sección premium -->
                <div class="px-5 lg:px-8 py-6 lg:border-b lg:border-[#f0f0f0]">
                  <h2 class="text-lg font-semibold text-[#1A1A1A] tracking-tight">Datos de Contacto</h2>
                  <p class="text-sm text-[#9CA3AF] mt-1">Te enviaremos actualizaciones de tu pedido</p>
                </div>
                
                <div class="px-5 lg:px-8 pb-8 pt-4 flex flex-col gap-4">
                  <div class="input-group">
                    <label>Correo electrónico</label>
                    <input type="email" v-model="form.email" placeholder="tu@email.com" @input="saveFormToStorage" />
                  </div>
                  
                  <div class="grid grid-cols-2 gap-4">
                    <div class="input-group">
                      <label>Nombre</label>
                      <input type="text" v-model="form.nombre" placeholder="Tu nombre" @input="saveFormToStorage" />
                    </div>
                    <div class="input-group">
                      <label>Apellido</label>
                      <input type="text" v-model="form.apellido" placeholder="Tu apellido" @input="saveFormToStorage" />
                    </div>
                  </div>
                  
                  <div class="input-group">
                    <label>Teléfono WhatsApp</label>
                    <div class="relative flex">
                      <!-- Prefijo de país - fondo blanco premium -->
                      <div class="flex items-center justify-center px-4 bg-white border border-r-0 border-[#e0e0e0] rounded-l-lg">
                        <span class="text-[#6B7280] text-sm">🇨🇴 +57</span>
                      </div>
                      <!-- Input de teléfono -->
                      <input 
                        type="tel" 
                        v-model="form.telefono" 
                        placeholder="300 123 4567" 
                        class="flex-1 !rounded-l-none !border-l-0" 
                        @input="formatPhoneNumber"
                        maxlength="12"
                      />
                    </div>
                    
                  </div>
                  
                  <div class="grid grid-cols-2 gap-4">
                    <div class="input-group">
                      <label>Tipo Doc.</label>
                      <select v-model="form.tipoDocumento" @change="saveFormToStorage">
                        <option value="">Selecciona</option>
                        <option value="CC">CC</option>
                        <option value="CE">CE</option>
                        <option value="TI">TI</option>
                        <option value="PASAPORTE">Pasaporte</option>
                        <option value="NIT">NIT</option>
                      </select>
                    </div>
                    <div class="input-group">
                      <label>Número Documento</label>
                      <input 
                        type="text" 
                        v-model="form.numeroDocumento" 
                        placeholder="1234567890" 
                        inputmode="numeric"
                        pattern="[0-9]*"
                        minlength="5"
                        maxlength="15"
                        @input="formatDocumentNumber"
                      />
                    </div>
                  </div>
                  <p class="text-xs text-[#9CA3AF] -mt-2">Requerido por la transportadora</p>
                  
                  <label class="flex items-center gap-3 cursor-pointer group">
                    <div class="relative">
                      <input type="checkbox" v-model="form.newsletter" class="sr-only peer" @change="saveFormToStorage" />
                      <div class="w-5 h-5 border border-[#e0e0e0] rounded peer-checked:bg-[#c11252] peer-checked:border-[#c11252] transition-all"></div>
                      <svg class="absolute inset-0 w-5 h-5 text-white opacity-0 peer-checked:opacity-100" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                    </div>
                    <span class="text-sm text-[#6B7280]">Recibir novedades y ofertas exclusivas</span>
                  </label>
                </div>
                
                <!-- Footer con CTA - fluid en móvil -->
                <div class="px-5 lg:px-8 py-4 lg:bg-[#FAFAFA] lg:border-t lg:border-[#f0f0f0]">
                  <button 
                    @click="nextStep"
                    :disabled="!isStep1Valid"
                    class="w-full bg-[#c11252] hover:bg-[#a00f45] disabled:bg-[#e5e7eb] disabled:text-[#9CA3AF] text-white py-4 text-sm font-semibold rounded-xl transition-all"
                  >
                    Continuar
                  </button>
                  
                  <!-- Badges de seguridad - solo en desktop -->
                  <div class="hidden lg:flex items-center justify-center gap-4 mt-5 text-xs text-[#9CA3AF]">
                    <div class="flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                      </svg>
                      <span>Pago Seguro</span>
                    </div>
                    <div class="flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                      </svg>
                      <span>Envío Nacional</span>
                    </div>
                    <div class="flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
                      </svg>
                      <span>Garantía</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Backdrop para dropdowns en móvil -->
              <div 
                v-if="dropdowns.departamento || dropdowns.municipio"
                @click="dropdowns.departamento = false; dropdowns.municipio = false"
                class="sm:hidden fixed inset-0 bg-black/40 z-[150]"
              ></div>

              <!-- ═══════════════════════════════════════════════════════════ -->
              <!-- PASO 2: Dirección de Envío - Optimizado móvil                -->
              <!-- ═══════════════════════════════════════════════════════════ -->
              <div v-show="currentStep === 2">
                <!-- Header de sección premium -->
                <div class="px-5 lg:px-8 py-6 lg:border-b lg:border-[#f0f0f0]">
                  <h2 class="text-lg font-semibold text-[#1A1A1A] tracking-tight">Dirección de Envío</h2>
                  <p class="text-sm text-[#9CA3AF] mt-1">¿Dónde entregamos tu pedido?</p>
                </div>
                
                <div class="px-5 lg:px-8 pb-8 pt-4 flex flex-col gap-4">
                  <!-- País + Departamento en una fila horizontal -->
                  <div class="input-group" v-if="form.pais === 'CO'">
                    <label>Departamento</label>
                    <div class="flex items-center gap-2">
                      <!-- País - Badge compacto -->
                      <div class="flex items-center justify-center w-[52px] h-[52px] bg-[#fafafa] border border-[#e0e0e0] rounded-lg flex-shrink-0">
                        <span class="text-lg">🇨🇴</span>
                      </div>
                      
                      <!-- Departamento - Ocupa el resto -->
                      <div class="flex-1">
                      <div class="custom-dropdown" @click.stop>
                      <button 
                        type="button"
                        @click="toggleDropdown('departamento')"
                        :disabled="loadingDepartamentos"
                        class="dropdown-trigger"
                      >
                        <span :class="{ 'text-[#9CA3AF]': !getDepName }">
                          {{ loadingDepartamentos ? 'Cargando...' : (getDepName || 'Selecciona tu departamento') }}
                        </span>
                        <svg v-if="!loadingDepartamentos" class="w-5 h-5 text-[#6B7280] transition-transform" :class="{ 'rotate-180': dropdowns.departamento }" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                        </svg>
                        <svg v-else class="w-5 h-5 text-[#6B7280] animate-spin" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                        </svg>
                      </button>
                      
                      <!-- Dropdown panel - Ahora fullscreen en móvil -->
                      <div v-show="dropdowns.departamento" class="dropdown-panel">
                        <!-- Header móvil -->
                        <div class="sm:hidden flex items-center justify-between px-4 py-3 border-b border-[#E5E7EB]">
                          <span class="font-medium text-[#1A1A1A]">Selecciona departamento</span>
                          <button @click="dropdowns.departamento = false" class="p-1">
                            <svg class="w-5 h-5 text-[#6B7280]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                          </button>
                        </div>
                        <div class="dropdown-search">
                          <svg class="w-4 h-4 text-[#9CA3AF]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                          <input 
                            type="text" 
                            v-model="searchDep" 
                            placeholder="Buscar departamento..."
                            class="!text-base"
                            @click.stop
                          />
                        </div>
                        <ul class="dropdown-list">
                          <li 
                            v-for="dep in departamentosFiltrados" 
                            :key="dep.id"
                            @click="selectDepartamento(dep)"
                            :class="{ 'selected': dep.nombre === form.departamento || dep.id === form.departamentoId }"
                            class="!py-3.5"
                          >
                            {{ dep.nombre }}
                            <svg v-if="dep.nombre === form.departamento || dep.id === form.departamentoId" class="w-5 h-5 text-[#D81B60]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                            </svg>
                          </li>
                          <li v-if="departamentosFiltrados.length === 0" class="empty">
                            No se encontraron resultados
                          </li>
                        </ul>
                      </div>
                    </div>
                    </div>
                    </div>
                  </div>
                  
                  <!-- Oculto: País -->
                  <input type="hidden" v-model="form.pais" />
                  
                  <!-- Municipio -->
                  <div class="input-group" v-if="form.departamento">
                    <label>Ciudad / Municipio</label>
                    <div class="custom-dropdown" @click.stop>
                      <button 
                        type="button"
                        @click="toggleDropdown('municipio')"
                        :disabled="loadingMunicipios"
                        class="dropdown-trigger"
                      >
                        <span :class="{ 'text-[#9CA3AF]': !getMunName }">
                          {{ loadingMunicipios ? 'Cargando...' : (getMunName || 'Selecciona tu ciudad') }}
                        </span>
                        <svg v-if="!loadingMunicipios" class="w-5 h-5 text-[#6B7280] transition-transform" :class="{ 'rotate-180': dropdowns.municipio }" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                        </svg>
                        <svg v-else class="w-5 h-5 text-[#6B7280] animate-spin" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                        </svg>
                      </button>
                      
                      <!-- Dropdown panel - Fullscreen en móvil -->
                      <div v-show="dropdowns.municipio" class="dropdown-panel">
                        <!-- Header móvil -->
                        <div class="sm:hidden flex items-center justify-between px-4 py-3 border-b border-[#E5E7EB]">
                          <span class="font-medium text-[#1A1A1A]">Selecciona tu ciudad</span>
                          <button @click="dropdowns.municipio = false" class="p-1">
                            <svg class="w-5 h-5 text-[#6B7280]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                          </button>
                        </div>
                        <div class="dropdown-search">
                          <svg class="w-4 h-4 text-[#9CA3AF]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                          <input 
                            type="text" 
                            v-model="searchMun" 
                            placeholder="Buscar municipio..."
                            class="!text-base"
                            @click.stop
                          />
                        </div>
                        <ul class="dropdown-list">
                          <li 
                            v-for="mun in municipiosFiltrados" 
                            :key="mun.id"
                            @click="selectMunicipio(mun)"
                            :class="{ 'selected': mun.nombre === form.municipio }"
                            class="!py-3.5"
                          >
                            {{ mun.nombre }}
                            <svg v-if="mun.nombre === form.municipio" class="w-5 h-5 text-[#D81B60]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                            </svg>
                          </li>
                          <li v-if="municipiosFiltrados.length === 0" class="empty">
                            No se encontraron resultados
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Tipo de Zona -->
                  <div class="input-group" v-if="form.municipio">
                    <label>Tipo de zona</label>
                    <div class="flex gap-3 h-[52px]">
                      <button 
                        type="button"
                        @click="form.tipoZona = 'urbano'; saveFormToStorage()"
                        :class="[
                          'flex-1 flex items-center justify-center gap-2 border transition-all text-sm font-medium rounded-lg',
                          form.tipoZona === 'urbano' 
                            ? 'border-[#c11252] bg-[#c112520a] text-[#c11252]' 
                            : 'border-[#e0e0e0] bg-white hover:border-[#d1d5db] text-[#4A4A4A]'
                        ]"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" />
                        </svg>
                        Urbano
                      </button>
                      <button 
                        type="button"
                        @click="form.tipoZona = 'rural'; saveFormToStorage()"
                        :class="[
                          'flex-1 flex items-center justify-center gap-2 border transition-all text-sm font-medium rounded-lg',
                          form.tipoZona === 'rural' 
                            ? 'border-[#c11252] bg-[#c112520a] text-[#c11252]' 
                            : 'border-[#e0e0e0] bg-white hover:border-[#d1d5db] text-[#4A4A4A]'
                        ]"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                        </svg>
                        Rural
                      </button>
                    </div>
                  </div>
                  
                  <!-- Dirección y Barrio en línea (urbano) -->
                  <div class="grid grid-cols-1 sm:grid-cols-3 gap-4" v-if="form.tipoZona === 'urbano'">
                    <div class="input-group sm:col-span-2">
                      <label>Dirección</label>
                      <input type="text" v-model="form.direccion" placeholder="Calle 123 # 45 - 67" @input="saveFormToStorage" />
                    </div>
                    <div class="input-group">
                      <label>Barrio</label>
                      <input type="text" v-model="form.barrio" placeholder="Nombre del barrio" @input="saveFormToStorage" />
                    </div>
                  </div>
                  
                  <!-- Indicaciones (rural) -->
                  <div class="input-group" v-if="form.tipoZona === 'rural'">
                    <label>Indicaciones de llegada</label>
                    <textarea 
                      v-model="form.indicacionesRural" 
                      placeholder="Describe cómo llegar a tu ubicación..."
                      class="!h-24 resize-none"
                      @input="saveFormToStorage"
                    ></textarea>
                  </div>
                  
                  <!-- Apartamento/Oficina -->
                  <div class="input-group" v-if="form.tipoZona">
                    <label>Apartamento / Oficina (opcional)</label>
                    <input type="text" v-model="form.apartamento" placeholder="Ej: Apto 201, Torre B" @input="saveFormToStorage" />
                  </div>
                </div>
                
                <!-- Footer con CTAs - estilo premium -->
                <div class="px-5 lg:px-8 py-6 lg:bg-[#fafafa] lg:border-t lg:border-[#f0f0f0]">
                  <div class="flex gap-3">
                    <button 
                      @click="prevStep"
                      class="px-6 py-4 border border-[#e0e0e0] text-[#4A4A4A] text-sm font-medium rounded-lg hover:border-[#c11252] hover:text-[#c11252] transition-all bg-white"
                    >
                      Volver
                    </button>
                    <button 
                      @click="nextStep"
                      :disabled="!isStep2Valid"
                      class="flex-1 bg-[#c11252] hover:bg-[#a00f45] disabled:bg-[#e5e7eb] disabled:text-[#9CA3AF] text-white py-4 text-sm font-semibold rounded-xl transition-all"
                    >
                      Continuar al Pago
                    </button>
                  </div>
                  
                  <div class="hidden lg:flex items-center justify-center gap-6 mt-5 text-xs text-[#9CA3AF]">
                    <div class="flex items-center gap-1.5">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                      </svg>
                      <span>Datos Protegidos</span>
                    </div>
                    <div class="flex items-center gap-1.5">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                      </svg>
                      <span>Envío Asegurado</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- ═══════════════════════════════════════════════════════════ -->
              <!-- PASO 3: Método de Pago                                       -->
              <!-- ═══════════════════════════════════════════════════════════ -->
              <!-- PASO 3: Método de Pago - Diseño fluid retail                  -->
              <!-- ═══════════════════════════════════════════════════════════ -->
              <div v-show="currentStep === 3">
                <!-- Header de sección -->
                <div class="px-5 lg:px-8 py-5 lg:py-6 lg:border-b lg:border-[#f0f0f0]">
                  <h2 class="text-lg font-semibold text-[#1A1A1A] tracking-tight">Método de Pago</h2>
                  <p class="text-sm text-[#9CA3AF] mt-1">Selecciona cómo deseas pagar</p>
                </div>
                
                <!-- Banner informativo para clientes recurrentes (sutil) -->
                <div v-if="clienteConDatosCompletos" class="mx-5 lg:mx-8 mb-4 flex items-center gap-2 text-sm text-[#c11252]">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>¡Hola de nuevo! Ya tenemos tu información guardada.</span>
                </div>
                
                <!-- Resumen de datos - SIN TARJETA, texto limpio con enlaces -->
                <div class="px-5 lg:px-8 space-y-3 mb-6">
                  <div class="flex items-center justify-between py-2 border-b border-[#f0f0f0]">
                    <div class="flex-1 min-w-0">
                      <span class="text-xs text-[#9CA3AF] uppercase tracking-wider">Contacto</span>
                      <p class="text-sm text-[#1A1A1A] mt-0.5 truncate">{{ form.email }}</p>
                    </div>
                    <button @click="goToStep(1)" class="text-xs text-[#c11252] hover:underline ml-4">Editar</button>
                  </div>
                  <div class="flex items-center justify-between py-2">
                    <div class="flex-1 min-w-0">
                      <span class="text-xs text-[#9CA3AF] uppercase tracking-wider">Envío a</span>
                      <p class="text-sm text-[#1A1A1A] mt-0.5 truncate">{{ getFullAddress() }}</p>
                    </div>
                    <button @click="goToStep(2)" class="text-xs text-[#c11252] hover:underline ml-4">Editar</button>
                  </div>
                </div>
                
                <!-- Separador -->
                <div class="border-t border-[#f0f0f0] mx-5 lg:mx-8 mb-5"></div>
                
                <!-- Opciones de Pago - Diseño limpio -->
                <div class="px-5 lg:px-8 pb-6 space-y-3">
                  <!-- Opción Wompi -->
                  <div 
                    @click="selectedPayment = 'wompi'"
                    :class="[
                      'cursor-pointer rounded-xl p-4 transition-all',
                      selectedPayment === 'wompi' 
                        ? 'border-2 border-[#c11252] bg-[#fef7f9]' 
                        : 'border border-[#e5e7eb] hover:border-[#c11252]/30'
                    ]"
                  >
                    <div class="flex items-center gap-3">
                      <div :class="[
                        'w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0',
                        selectedPayment === 'wompi' ? 'border-[#c11252]' : 'border-[#d1d5db]'
                      ]">
                        <div :class="['w-2.5 h-2.5 rounded-full transition-all', selectedPayment === 'wompi' ? 'bg-[#c11252]' : '']"></div>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-[#1A1A1A]">Pago Seguro Inmediato</p>
                        <p class="text-xs text-[#9CA3AF] mt-0.5">Tarjeta, PSE, Nequi, Daviplata</p>
                      </div>
                      <div class="flex items-center gap-1.5 flex-shrink-0">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" alt="Visa" class="h-3 opacity-60" />
                        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg" alt="MC" class="h-4 opacity-60" />
                      </div>
                    </div>
                  </div>
                  
                  <!-- Opción Asesora - Con badge elegante inline -->
                  <div 
                    @click="selectedPayment = 'asesor'"
                    :class="[
                      'cursor-pointer rounded-xl p-4 transition-all',
                      selectedPayment === 'asesor' 
                        ? 'border-2 border-[#c11252] bg-[#fef7f9]' 
                        : 'border border-[#e5e7eb] hover:border-[#c11252]/30'
                    ]"
                  >
                    <div class="flex items-center gap-3">
                      <div :class="[
                        'w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0',
                        selectedPayment === 'asesor' ? 'border-[#c11252]' : 'border-[#d1d5db]'
                      ]">
                        <div :class="['w-2.5 h-2.5 rounded-full transition-all', selectedPayment === 'asesor' ? 'bg-[#c11252]' : '']"></div>
                      </div>
                      <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-2">
                          <p class="text-sm font-medium text-[#1A1A1A]">Finalizar con Asesora</p>
                          <span class="text-[10px] text-[#c11252] font-medium">Recomendado</span>
                        </div>
                        <p class="text-xs text-[#9CA3AF] mt-0.5">Atención personalizada por WhatsApp</p>
                      </div>
                      <!-- Icono WhatsApp armonizado (monocromático) -->
                      <div class="w-8 h-8 rounded-full bg-[#f3f4f6] flex items-center justify-center flex-shrink-0">
                        <svg class="w-4 h-4 text-[#6B7280]" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Footer con CTA - fluid y touch-friendly -->
                <div class="px-5 lg:px-8 py-6 lg:bg-[#FAFAFA] lg:border-t lg:border-[#f0f0f0]">
                  <button 
                    @click="processPayment"
                    :disabled="!selectedPayment || processing"
                    class="w-full bg-[#c11252] hover:bg-[#a00f45] disabled:bg-[#e5e7eb] disabled:text-[#9CA3AF] text-white py-4 text-sm font-semibold rounded-xl transition-all flex items-center justify-center gap-2"
                  >
                    <svg v-if="processing" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                    </svg>
                    <span v-if="processing">Procesando...</span>
                    <span v-else>{{ selectedPayment === 'asesor' ? 'Continuar con Asesora' : 'Pagar Ahora' }}</span>
                  </button>
                  
                  <div class="flex items-center justify-center gap-2 mt-5 text-xs text-[#9CA3AF]">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                    </svg>
                    <span>Conexión segura SSL</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- COLUMNA DERECHA: Resumen del Pedido - fluid en móvil -->
          <!-- En móvil: solo visible si mobileShowForm es false -->
          <!-- En desktop (lg:): siempre visible -->
          <div class="lg:col-span-4 order-1 lg:order-2" :class="{ 'hidden lg:block': mobileShowForm }">
            <div class="bg-white lg:rounded-xl lg:border lg:border-[#e5e7eb] overflow-hidden lg:sticky lg:top-6">
              
              <!-- Header del resumen -->
              <div class="px-5 lg:px-6 py-5 lg:py-4 lg:border-b lg:border-[#f0f0f0]">
                <!-- Móvil: título grande -->
                <div class="lg:hidden">
                  <h2 class="text-xl font-semibold text-[#1A1A1A] tracking-tight">Tu carrito</h2>
                  <p class="text-sm text-[#9CA3AF] mt-1">{{ cartItems.length }} {{ cartItems.length === 1 ? 'producto' : 'productos' }}</p>
                </div>
                <!-- Desktop: título compacto -->
                <h3 class="hidden lg:block font-semibold text-base text-[#1A1A1A]">Resumen de compra</h3>
              </div>
              
              <!-- Productos -->
              <div class="divide-y divide-[#f0f0f0]">
                <div 
                  v-for="item in cartItems" 
                  :key="item.producto_id"
                  class="flex gap-3 px-5 lg:px-6 py-4"
                >
                  <div class="w-14 h-14 bg-[#f9f9f9] rounded-lg overflow-hidden flex-shrink-0">
                    <img 
                      v-if="getCartMediaUrl(item)" 
                      :src="getCartMediaUrl(item)" 
                      :alt="item.nombre"
                      class="w-full h-full object-cover"
                    />
                    <div v-else class="w-full h-full flex items-center justify-center bg-[#f3f4f6]">
                      <svg class="w-5 h-5 text-[#D1D5DB]" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                      </svg>
                    </div>
                  </div>
                  
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-[#1A1A1A] line-clamp-2">{{ item.nombre || 'Producto' }}</p>
                    <p v-if="item.color || item.largo" class="text-xs text-[#9CA3AF] mt-0.5">
                      <span v-if="item.color">{{ formatColorLabel(item.color) }}</span>
                      <span v-if="item.color && item.largo"> · </span>
                      <span v-if="item.largo">{{ item.largo }}</span>
                    </p>
                    <p class="text-xs text-[#9CA3AF] mt-0.5">Cantidad: {{ item.cantidad || 1 }}</p>
                  </div>
                  
                  <div class="text-sm font-semibold text-[#1A1A1A]">
                    ${{ formatPrice(getItemPrice(item)) }}
                  </div>
                </div>
              </div>
              
              <!-- Cupón -->
              <div class="px-5 lg:px-6 py-4 border-t border-[#f0f0f0]">
                <div class="flex gap-2">
                  <input 
                    type="text" 
                    v-model="cupon"
                    class="flex-1 px-3 py-2.5 bg-[#f3f4f6] border border-transparent rounded-lg text-sm focus:outline-none focus:bg-white focus:border-[#c11252] placeholder:text-[#9CA3AF] transition-all"
                    placeholder="Código de descuento"
                  />
                  <button class="px-4 py-2.5 bg-[#c11252] hover:bg-[#a00f45] text-white text-sm font-medium rounded-lg transition-all">
                    Aplicar
                  </button>
                </div>
              </div>
              
              <!-- Totales -->
              <div class="px-5 lg:px-6 py-4 border-t border-[#f0f0f0] space-y-3">
                <div class="flex justify-between text-sm">
                  <span class="text-[#9CA3AF]">Subtotal</span>
                  <span class="text-[#1A1A1A] font-medium">${{ formatPrice(getSubtotal()) }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-[#9CA3AF]">Envío</span>
                  <span :class="envioGratis ? 'text-green-600 font-semibold' : 'text-[#1A1A1A]'">
                    {{ envioGratis ? 'Gratis' : '$' + formatPrice(costoEnvio) }}
                  </span>
                </div>
                
                <div class="border-t border-[#f0f0f0] pt-3"></div>
                
                <div class="flex justify-between items-baseline">
                  <span class="text-base font-medium text-[#1A1A1A]">Total</span>
                  <div class="text-right">
                    <span class="text-2xl font-bold text-[#c11252]">${{ formatPrice(getTotal()) }}</span>
                    <span class="text-xs text-[#9CA3AF] ml-1">COP</span>
                  </div>
                </div>
                
                <p class="text-[10px] sm:text-xs text-[#9CA3AF] text-right">Incluye impuestos</p>
              </div>
              
              <!-- Banner envío gratis - Solo si no es gratis -->
              <!-- Envío gratis progress -->
              <div v-if="!envioGratis" class="px-5 lg:px-6 py-3 bg-[#fef7f9]">
                <p class="text-xs text-[#c11252] font-medium text-center">
                  ¡Agrega ${{ formatPrice(300000 - getSubtotal()) }} más para envío gratis!
                </p>
              </div>
              
              <!-- CTA Móvil - Ir al formulario -->
              <div class="lg:hidden px-5 py-5 border-t border-[#f0f0f0]">
                <button 
                  @click="showMobileForm"
                  class="w-full py-4 bg-[#c11252] hover:bg-[#a00f45] text-white text-sm font-semibold rounded-xl transition-all flex items-center justify-center gap-2"
                >
                  <span>Completar mis datos</span>
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-[#f0f0f0] py-5 mt-auto">
      <div class="max-w-7xl mx-auto px-5 lg:px-6 flex flex-wrap items-center justify-center gap-4 text-xs text-[#9CA3AF]">
        <a href="#" class="hover:text-[#1A1A1A] transition-colors">Privacidad</a>
        <span class="text-[#e5e7eb]">·</span>
        <a href="#" class="hover:text-[#1A1A1A] transition-colors">Términos</a>
        <span class="text-[#e5e7eb]">·</span>
        <a href="#" class="hover:text-[#1A1A1A] transition-colors">Devoluciones</a>
      </div>
    </footer>

    <!-- Overlay de carga Wompi - DESACTIVADO TEMPORALMENTE
    <div v-if="processing && selectedPayment === 'wompi'" class="fixed inset-0 bg-black/60 z-[999] flex items-center justify-center">
      <div class="bg-white rounded-lg p-8 max-w-sm mx-4 text-center">
        <div class="mb-4 flex justify-center">
          <svg class="w-16 h-16 text-[#00D4AA] animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <h3 class="font-luxury text-xl text-[#1A1A1A] mb-2">Conectando con Wompi...</h3>
        <p class="text-sm text-[#7A7A7A]">Preparando pasarela de pagos segura</p>
        <div class="mt-6 flex items-center justify-center gap-2 text-xs text-[#9CA3AF]">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
          </svg>
          <span>Conexión segura SSL</span>
        </div>
      </div>
    </div>
    FIN Overlay Wompi -->
    
    <!-- Modal de Error de Stock -->
    <div v-if="showStockModal" class="fixed inset-0 bg-black/60 z-[999] flex items-center justify-center p-4" @click.self="showStockModal = false">
      <div class="bg-white rounded-sm shadow-2xl max-w-md w-full overflow-hidden animate-fade-in">
        <!-- Header -->
        <div class="bg-gradient-to-r from-yellow-50 to-amber-50 px-6 py-5 border-b border-yellow-100">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5-.217 3.374 1.45 4.19.433.212.902.356 1.384.418M21.303 16.126c.865 1.5.217 3.374-1.45 4.19-.433.212-.902.356-1.384.418M4.697 7.874c-.866-1.5-.217-3.374 1.45-4.19.433-.212.902-.356 1.384-.418M19.303 7.874c.865-1.5.217-3.374-1.45-4.19-.433-.212-.902-.356-1.384-.418" />
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="font-luxury text-xl text-[#1A1A1A]">Stock Insuficiente</h3>
              <p class="text-sm text-[#7A7A7A] mt-1">{{ stockModalMessage }}</p>
            </div>
            <button @click="showStockModal = false" class="text-[#9CA3AF] hover:text-[#1A1A1A] transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Body -->
        <div class="p-6">
          <div v-if="stockModalProducts.length > 0" class="space-y-3 mb-6">
            <p class="text-sm font-medium text-[#4A4A4A] mb-3">Productos afectados:</p>
            <div 
              v-for="prod in stockModalProducts" 
              :key="prod.producto_id"
              class="flex items-start gap-3 p-3 bg-red-50 border border-red-100 rounded-sm"
            >
              <div class="relative flex-shrink-0">
                <img 
                  v-if="getCartMediaUrl(prod)" 
                  :src="getCartMediaUrl(prod)" 
                  :alt="prod.nombre"
                  class="w-16 h-16 object-cover rounded bg-white"
                  @error="e => e.target.src = '/placeholder.jpg'"
                />
                <div class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center shadow-sm">
                  <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                  </svg>
                </div>
              </div>
              <div class="flex-1 min-w-0 text-sm">
                <p class="font-medium text-[#1A1A1A]">{{ prod.nombre }}</p>
                <p class="text-[#7A7A7A] mt-1.5">
                  <span class="text-red-600 font-semibold">Disponible: {{ prod.stock_disponible }}</span>
                  <span class="mx-2">•</span>
                  <span>Solicitado: {{ prod.stock_solicitado }}</span>
                </p>
              </div>
            </div>
          </div>
          
          <p class="text-sm text-[#7A7A7A] mb-6">
            Por favor, ajusta las cantidades en tu carrito y vuelve a intentar.
          </p>
          
          <button 
            @click="showStockModal = false"
            class="w-full bg-[#D81B60] hover:bg-[#C2185B] text-white py-3 px-6 rounded-lg text-sm font-medium tracking-wide uppercase transition-all"
          >
            Entendido
          </button>
        </div>
      </div>
    </div>
    
    </template><!-- fin v-else -->
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient, { getImageUrl, API_BASE_URL } from '@/services/api'
import { formatColorLabel } from '@/utils/colorLabels'

// API de Colombia - Datos oficiales de departamentos y municipios
const COLOMBIA_API = {
  // Usamos api-colombia.com - API gratuita con datos del DANE
  departamentos: 'https://api-colombia.com/api/v1/Department',
  ciudades: (departmentId) => `https://api-colombia.com/api/v1/Department/${departmentId}/cities`
}

export default {
  name: 'Checkout',
  setup() {
    const router = useRouter()
    const currentStep = ref(1)
    const maxStep = ref(1)
    const selectedPayment = ref('asesor') // Por defecto WhatsApp (Wompi desactivado temporalmente)
    const processing = ref(false)
    const cupon = ref('')
    const wompiLoaded = ref(false)
    
    // Estado de carga inicial - mostrar loading mientras determina el paso correcto
    const initialLoading = ref(true)
    
    // Estado para clientes con datos completos (saltar al paso 3)
    const clienteConDatosCompletos = ref(false)
    
    // Estado de carga para ubicación
    const loadingDepartamentos = ref(false)
    const loadingMunicipios = ref(false)
    
    // Custom dropdowns state
    const dropdowns = ref({
      departamento: false,
      municipio: false
    })
    const searchDep = ref('')
    const searchMun = ref('')
    
    // Estado del modal de stock
    const showStockModal = ref(false)
    const stockModalMessage = ref('')
    const stockModalProducts = ref([])

    // Cache de posters para videos en carrito
    const videoPosters = ref({})
    
    // Configuración Wompi
    const WOMPI_CONFIG = {
      publicKey: import.meta.env.VITE_WOMPI_PUBLIC_KEY || 'pub_test_ZVH2hPZRCY7iVcPAyCCh53E5cS2SUFmW',
      currency: 'COP',
      amountInCents: true // Wompi requiere montos en centavos
    }
    const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER || '4796657763'
    
    // Form con nuevos campos
    const form = ref({
      email: '',
      nombre: '',
      apellido: '',
      telefono: '',
      tipoDocumento: 'CC',
      numeroDocumento: '',
      newsletter: false,
      pais: 'CO', // Colombia por defecto
      departamento: '',
      departamentoId: null, // ID numérico para la API de Colombia
      municipio: '',
      tipoZona: '',
      direccion: '',
      barrio: '',
      indicacionesRural: '',
      apartamento: ''
    })
    
    // Datos de ubicación - cargados desde API
    const departamentos = ref([])
    const municipios = ref([])
    
    // Cargar departamentos desde API
    const loadDepartamentos = async () => {
      loadingDepartamentos.value = true
      try {
        const response = await fetch(COLOMBIA_API.departamentos)
        const data = await response.json()
        // Ordenar alfabéticamente y mapear al formato esperado
        departamentos.value = data
          .map(d => ({ id: d.id, codigo: String(d.id), nombre: d.name }))
          .sort((a, b) => a.nombre.localeCompare(b.nombre))
      } catch (e) {
        console.error('Error cargando departamentos:', e)
        departamentos.value = []
      } finally {
        loadingDepartamentos.value = false
      }
    }
    
    // Cargar municipios cuando cambia el departamento
    // Acepta tanto ID numérico como nombre del departamento
    const loadMunicipios = async (departamentoIdOrName) => {
      if (!departamentoIdOrName) {
        municipios.value = []
        return
      }
      
      loadingMunicipios.value = true
      try {
        // Si es un string (nombre), buscar el ID
        let depId = departamentoIdOrName
        if (typeof departamentoIdOrName === 'string' && isNaN(parseInt(departamentoIdOrName))) {
          // Es un nombre, buscar en la lista de departamentos
          const dep = departamentos.value.find(d => 
            d.nombre.toLowerCase() === departamentoIdOrName.toLowerCase()
          )
          if (dep) {
            depId = dep.id
            form.value.departamentoId = dep.id
          } else {
            console.log('⚠️ Departamento no encontrado en la lista:', departamentoIdOrName)
            municipios.value = []
            loadingMunicipios.value = false
            return
          }
        }
        
        const response = await fetch(COLOMBIA_API.ciudades(depId))
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }
        const data = await response.json()
        // Ordenar alfabéticamente y mapear al formato esperado
        municipios.value = data
          .map(m => ({ id: m.id, codigo: String(m.id), nombre: m.name }))
          .sort((a, b) => a.nombre.localeCompare(b.nombre))
      } catch (e) {
        console.error('Error cargando municipios:', e)
        municipios.value = []
      } finally {
        loadingMunicipios.value = false
      }
    }
    
    // Computed con filtro de búsqueda para dropdowns
    const departamentosFiltrados = computed(() => {
      if (!searchDep.value) return departamentos.value
      const term = searchDep.value.toLowerCase()
      return departamentos.value.filter(d => d.nombre.toLowerCase().includes(term))
    })
    
    const municipiosFiltrados = computed(() => {
      if (!searchMun.value) return municipios.value
      const term = searchMun.value.toLowerCase()
      return municipios.value.filter(m => m.nombre.toLowerCase().includes(term))
    })
    
    // Dropdown helpers
    const toggleDropdown = (name) => {
      // Cerrar otros dropdowns
      Object.keys(dropdowns.value).forEach(key => {
        if (key !== name) dropdowns.value[key] = false
      })
      dropdowns.value[name] = !dropdowns.value[name]
      // Limpiar búsqueda al abrir
      if (dropdowns.value[name]) {
        if (name === 'departamento') searchDep.value = ''
        if (name === 'municipio') searchMun.value = ''
      }
    }
    
    const closeDropdowns = () => {
      Object.keys(dropdowns.value).forEach(key => {
        dropdowns.value[key] = false
      })
    }
    
    const selectDepartamento = async (dep) => {
      form.value.departamento = dep.nombre  // Guardar nombre, no ID
      form.value.departamentoId = dep.id    // Guardar ID para la API
      dropdowns.value.departamento = false
      searchDep.value = ''
      form.value.municipio = ''
      form.value.tipoZona = ''
      saveFormToStorage()
      await loadMunicipios(dep.id)
    }
    
    const selectMunicipio = (mun) => {
      form.value.municipio = mun.nombre  // Guardar nombre, no ID
      dropdowns.value.municipio = false
      searchMun.value = ''
      saveFormToStorage()
    }
    
    // Obtener nombre seleccionado
    const getDepName = computed(() => {
      // Convertir a string de forma segura
      const depValue = form.value.departamento
      const depStr = typeof depValue === 'string' ? depValue : String(depValue || '')
      
      // Buscar por ID o por nombre
      const dep = departamentos.value.find(d => 
        d.id === form.value.departamentoId ||
        d.id === Number(depValue) ||
        d.nombre === depStr ||
        (depStr && d.nombre?.toLowerCase() === depStr.toLowerCase())
      )
      return dep ? dep.nombre : depStr
    })
    
    const getMunName = computed(() => {
      // Convertir a string de forma segura
      const munValue = form.value.municipio
      const munStr = typeof munValue === 'string' ? munValue : String(munValue || '')
      
      const mun = municipios.value.find(m => 
        m.id === Number(munValue) ||
        m.nombre === munStr ||
        (munStr && m.nombre?.toLowerCase() === munStr.toLowerCase())
      )
      return mun ? mun.nombre : munStr
    })
    
    // Cart
    const cartItems = ref([])
    const costoEnvio = ref(30000)
    const envioGratis = computed(() => getSubtotal() >= 300000)
    
    // Mobile: controla si muestra resumen (false) o formulario (true)
    const mobileShowForm = ref(false)
    
    const stepperProgress = computed(() => {
      if (currentStep.value === 1) return '0%'
      if (currentStep.value === 2) return '40%'
      return '80%'
    })
    
    // Validations
    const isStep1Valid = computed(() => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      const documentoValido = form.value.numeroDocumento && form.value.numeroDocumento.length >= 5
      return form.value.email && emailRegex.test(form.value.email) &&
             form.value.nombre && form.value.telefono &&
             form.value.tipoDocumento && documentoValido
    })
    
    const isStep2Valid = computed(() => {
      const baseValid = form.value.pais && form.value.departamento && form.value.municipio && form.value.tipoZona
      if (form.value.tipoZona === 'urbano') {
        return baseValid && form.value.direccion
      }
      if (form.value.tipoZona === 'rural') {
        return baseValid && form.value.indicacionesRural
      }
      return false
    })
    
    // Storage functions
    const STORAGE_KEY = 'kharis_checkout_form'
    const DOC_STORAGE_KEY = 'kharis_checkout_doc'
    
    const saveDocToStorage = () => {
      try {
        localStorage.setItem(DOC_STORAGE_KEY, JSON.stringify({
          tipoDocumento: form.value.tipoDocumento || 'CC',
          numeroDocumento: form.value.numeroDocumento || ''
        }))
      } catch (e) {
        console.warn('Error saving document to storage', e)
      }
    }

    const saveFormToStorage = () => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(form.value))
        saveDocToStorage()
      } catch (e) {
        console.warn('Error saving form to storage', e)
      }
    }
    
    // Formatear número de teléfono mientras escribe
    const formatPhoneNumber = () => {
      // Solo dígitos
      let digits = form.value.telefono.replace(/\D/g, '')
      
      // Máximo 10 dígitos (número colombiano sin código de país)
      digits = digits.slice(0, 10)
      
      // Formatear como 300 123 4567
      if (digits.length > 3 && digits.length <= 6) {
        digits = digits.slice(0, 3) + ' ' + digits.slice(3)
      } else if (digits.length > 6) {
        digits = digits.slice(0, 3) + ' ' + digits.slice(3, 6) + ' ' + digits.slice(6)
      }
      
      form.value.telefono = digits
      saveFormToStorage()
    }
    
    // Formatear número de documento (solo números)
    const formatDocumentNumber = () => {
      // Eliminar todo excepto dígitos
      form.value.numeroDocumento = form.value.numeroDocumento.replace(/\D/g, '')
      saveFormToStorage()
    }
    
    const loadFormFromStorage = () => {
      try {
        const saved = localStorage.getItem(STORAGE_KEY)
        if (saved) {
          const data = JSON.parse(saved)
          
          // Limpiar datos corruptos (IDs numéricos en vez de nombres)
          if (data.departamento && typeof data.departamento === 'number') {
            // Dato corrupto, limpiar
            localStorage.removeItem(STORAGE_KEY)
            console.log('🧹 Limpiando datos de formulario corruptos')
            return
          }
          
          // Asegurar que departamento y municipio sean strings
          if (data.departamento && typeof data.departamento !== 'string') {
            data.departamento = String(data.departamento)
          }
          if (data.municipio && typeof data.municipio !== 'string') {
            data.municipio = String(data.municipio)
          }
          Object.assign(form.value, data)
        }

        const savedDoc = localStorage.getItem(DOC_STORAGE_KEY)
        if (savedDoc) {
          try {
            const docData = JSON.parse(savedDoc)
            if (docData.tipoDocumento && !form.value.tipoDocumento) {
              form.value.tipoDocumento = docData.tipoDocumento
            }
            if (docData.numeroDocumento && !form.value.numeroDocumento) {
              form.value.numeroDocumento = docData.numeroDocumento
            }
          } catch {
            localStorage.removeItem(DOC_STORAGE_KEY)
          }
        }
      } catch (e) {
        console.warn('Error loading form from storage', e)
        localStorage.removeItem(STORAGE_KEY)
      }
    }
    
    // Cargar datos del cliente logueado y su última orden
    const loadClienteData = async () => {
      try {
        const token = localStorage.getItem('access_token')
        const userStr = localStorage.getItem('user')
        
        if (!token || !userStr) return // No hay usuario logueado
        
        const user = JSON.parse(userStr)
        const userEmail = user.email
        
        if (!userEmail) return
        
        console.log('🔍 Buscando cliente con email:', userEmail)
        
        // Obtener todos los clientes y buscar el actual por email
        const clientesResponse = await fetch(`${API_BASE_URL}/api/v1/clientes/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        
        if (!clientesResponse.ok) {
          console.log('❌ Error al cargar clientes:', clientesResponse.status)
          return
        }
        
        const clientes = await clientesResponse.json()
        const clienteActual = clientes.find(c => c.email === userEmail)
        
        if (!clienteActual) {
          console.log('❌ Cliente no encontrado en la base de datos')
          return
        }
        
        console.log('✅ Cliente encontrado:', clienteActual)
        
        // Precargar datos del cliente
        if (clienteActual.email && !form.value.email) {
          form.value.email = clienteActual.email
        }
        if (clienteActual.nombre && !form.value.nombre) {
          form.value.nombre = clienteActual.nombre
        }
        if (clienteActual.apellido && !form.value.apellido) {
          form.value.apellido = clienteActual.apellido || ''
        }
        if (clienteActual.telefono && !form.value.telefono) {
          form.value.telefono = clienteActual.telefono
        }
        
        console.log('📋 Datos básicos precargados')
        
        // PRIMERO: Intentar cargar dirección guardada en el perfil del cliente
        let direccionCargadaDesdeCliente = false
        let telefonoCargado = !!form.value.telefono
        
        if (clienteActual.direccion || clienteActual.departamento) {
          console.log('📍 Cliente tiene dirección guardada, precargando...')
          
          if (clienteActual.direccion && !form.value.direccion) {
            form.value.direccion = clienteActual.direccion
            console.log('📍 Dirección precargada desde cliente:', clienteActual.direccion)
          }
          if (clienteActual.departamento && !form.value.departamento) {
            form.value.departamento = clienteActual.departamento
            console.log('🏛️ Departamento precargado desde cliente:', clienteActual.departamento)
            await loadMunicipios(clienteActual.departamento)
          }
          if (clienteActual.municipio && !form.value.municipio) {
            form.value.municipio = clienteActual.municipio
            console.log('🏘️ Municipio precargado desde cliente:', clienteActual.municipio)
          }
          if (clienteActual.barrio && !form.value.barrio) {
            form.value.barrio = clienteActual.barrio
            console.log('🏡 Barrio precargado desde cliente:', clienteActual.barrio)
          }
          direccionCargadaDesdeCliente = true
          console.log('✅ Dirección precargada desde perfil del cliente')
        }
        
        // SEGUNDO: Si no tiene dirección o teléfono, buscar en órdenes anteriores
        if (!direccionCargadaDesdeCliente || !telefonoCargado) {
          console.log('ℹ️ Buscando datos faltantes en órdenes anteriores...')
          
          // Intentar obtener todas las órdenes y filtrar por este cliente
          try {
            const ordenesResponse = await fetch(`${API_BASE_URL}/api/v1/ordenes`, {
              headers: { 'Authorization': `Bearer ${token}` }
            })
          
            if (ordenesResponse.ok) {
              const ordenes = await ordenesResponse.json()
              
              console.log('📦 Órdenes totales:', ordenes.length)
              
              // Filtrar órdenes del cliente actual por EMAIL (no por ID)
              const ordenesCliente = ordenes
                .filter(o => o.cliente_email === clienteActual.email)
                .sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion))
              
              console.log('📦 Órdenes del cliente:', ordenesCliente.length)
              
              if (ordenesCliente.length > 0) {
                // Obtener el detalle de la última orden (tiene los datos de envío)
                const ultimaOrdenId = ordenesCliente[0].id
                console.log('🔍 Obteniendo detalle de orden:', ultimaOrdenId)
                
                const detalleResponse = await fetch(`${API_BASE_URL}/api/v1/ordenes/${ultimaOrdenId}`, {
                  headers: { 'Authorization': `Bearer ${token}` }
                })
                
                if (detalleResponse.ok) {
                  const ultimaOrden = await detalleResponse.json()
                  console.log('✅ Detalle última orden:', ultimaOrden)
                  
                  // Precargar teléfono si está en la orden pero no en el cliente
                  if (ultimaOrden.cliente_telefono && !form.value.telefono) {
                    form.value.telefono = ultimaOrden.cliente_telefono
                    console.log('📞 Teléfono precargado:', ultimaOrden.cliente_telefono)
                  }
                  
                  // Precargar dirección de la última orden
                  if (ultimaOrden.direccion_envio && !form.value.direccion) {
                    form.value.direccion = ultimaOrden.direccion_envio
                    console.log('📍 Dirección precargada:', ultimaOrden.direccion_envio)
                  }
                  if (ultimaOrden.departamento && !form.value.departamento) {
                    form.value.departamento = ultimaOrden.departamento
                    console.log('🏛️ Departamento precargado:', ultimaOrden.departamento)
                    await loadMunicipios(ultimaOrden.departamento)
                  }
                  if (ultimaOrden.municipio && !form.value.municipio) {
                    form.value.municipio = ultimaOrden.municipio
                    console.log('🏘️ Municipio precargado:', ultimaOrden.municipio)
                  }
                  if (ultimaOrden.barrio && !form.value.barrio) {
                    form.value.barrio = ultimaOrden.barrio
                    console.log('🏡 Barrio precargado:', ultimaOrden.barrio)
                  }
                  
                  console.log('✅ Todos los datos del cliente precargados desde última orden')
                  direccionCargadaDesdeCliente = true
                }
              } else {
                console.log('ℹ️ Cliente no tiene órdenes anteriores')
              }
            }
          } catch (e) {
            console.log('⚠️ No se pudieron cargar órdenes anteriores:', e.message)
          }
        } // fin if (!direccionCargadaDesdeCliente)
        
        // TERCERO: Si tiene todos los datos completos, saltar al paso 3
        const datosContactoCompletos = form.value.email && form.value.nombre && form.value.telefono
        const datosEnvioCompletos = form.value.direccion && form.value.departamento && form.value.municipio
        
        if (datosContactoCompletos && datosEnvioCompletos) {
          console.log('🚀 Cliente tiene datos completos, saltando al paso 3 (Pago)')
          clienteConDatosCompletos.value = true
          currentStep.value = 3
          maxStep.value = 3
        } else {
          console.log('📝 Cliente necesita completar datos:', {
            contacto: datosContactoCompletos,
            envio: datosEnvioCompletos
          })
        }
        
      } catch (error) {
        console.log('❌ Error al cargar datos del cliente:', error.message)
      }
    }
    
    const clearFormStorage = () => {
      localStorage.removeItem(STORAGE_KEY)
    }
    
    // Location handlers
    const onPaisChange = () => {
      form.value.departamento = ''
      form.value.municipio = ''
      form.value.tipoZona = ''
      municipios.value = []
      saveFormToStorage()
    }
    
    const onDepartamentoChange = async () => {
      form.value.municipio = ''
      form.value.tipoZona = ''
      saveFormToStorage()
      // Cargar municipios del departamento seleccionado
      await loadMunicipios(form.value.departamento)
    }
    
    // Get full address for display
    const getFullAddress = () => {
      // Asegurar que tenemos strings
      const depValue = typeof form.value.departamento === 'string' ? form.value.departamento : ''
      const munValue = typeof form.value.municipio === 'string' ? form.value.municipio : ''
      
      // Buscar departamento por código, id o nombre
      const dep = departamentos.value.find(d => 
        d.codigo === depValue || 
        d.id === Number(depValue) ||
        d.nombre === depValue ||
        (depValue && d.nombre?.toLowerCase() === depValue.toLowerCase())
      )
      
      // Buscar municipio por código, id o nombre
      const mun = municipios.value.find(m => 
        m.codigo === munValue || 
        m.id === Number(munValue) ||
        m.nombre === munValue ||
        (munValue && m.nombre?.toLowerCase() === munValue.toLowerCase())
      )
      
      // Construir dirección
      let addr = form.value.direccion || ''
      if (form.value.barrio) addr += `, Barrio ${form.value.barrio}`
      
      // Usar el nombre del departamento/municipio, o el valor guardado si no se encontró
      const depName = dep?.nombre || depValue || ''
      const munName = mun?.nombre || munValue || ''
      
      // Si no hay datos, mostrar mensaje amigable
      if (!addr && !munName && !depName) {
        return 'Sin dirección registrada'
      }
      
      return `${addr}${munName ? ', ' + munName : ''}${depName ? ', ' + depName : ''}`
    }

    // Función para construir el mensaje de WhatsApp de forma segura
    const buildWhatsAppMessage = () => {
      const productos = cartItems.value.map((i) => {
        const detalles = [
          i.color ? `Color: ${humanizeVariant(i.color)}` : '',
          i.largo ? `Largo: ${humanizeVariant(i.largo)}` : ''
        ].filter(Boolean).join(' · ')
        const sufijo = detalles ? ` (${detalles})` : ''
        return `• ${i.nombre || 'Producto'}${sufijo} x${i.cantidad || 1}`
      }).join('\n')
      const direccion = getWhatsAppAddress().replaceAll('%0A', '\n')
      
      const msg = `Hola, quiero finalizar mi pedido\n\n*CÓDIGO:* ${sessionStorage.getItem('temp_order_code') || 'KH-0000'}\n\n*PRODUCTOS:*\n${productos}\n\n*TOTAL:* $${formatPrice(getTotal())} COP\n\n${form.value.nombre} ${form.value.apellido}\n${form.value.telefono}\n\n*DIRECCIÓN:*\n${direccion}`
      
      return encodeURIComponent(msg)
    }
    const getWhatsAppAddress = () => {
      const depValue = typeof form.value.departamento === 'string' ? form.value.departamento : ''
      const munValue = typeof form.value.municipio === 'string' ? form.value.municipio : ''
      
      const dep = departamentos.value.find(d => 
        d.codigo === depValue || 
        d.id === Number(depValue) ||
        d.nombre === depValue ||
        (depValue && d.nombre?.toLowerCase() === depValue.toLowerCase())
      )
      
      const mun = municipios.value.find(m => 
        m.codigo === munValue || 
        m.id === Number(munValue) ||
        m.nombre === munValue ||
        (munValue && m.nombre?.toLowerCase() === munValue.toLowerCase())
      )
      
      const depName = dep?.nombre || depValue || ''
      const munName = mun?.nombre || munValue || ''
      const direccion = form.value.direccion || ''
      const apartamento = form.value.apartamento || ''
      const barrio = form.value.barrio || ''
      const indicacionesRural = form.value.indicacionesRural || ''
      
      // Formato para WhatsApp: cada elemento en su línea
      let parts = []
      if (depName) parts.push(depName)
      if (munName) parts.push(munName)
      if (direccion) parts.push(direccion)
      if (apartamento) parts.push(`Apartamento: ${apartamento}`)
      if (barrio) parts.push(`Barrio: ${barrio}`)
      if (indicacionesRural) parts.push(`Indicaciones: ${indicacionesRural}`)
      
      return parts.length > 0 ? parts.join('%0A') : 'Sin dirección registrada'
    }
    
    // Móvil: mostrar formulario (oculta resumen)
    const showMobileForm = () => {
      mobileShowForm.value = true
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
    
    // Móvil: volver al resumen
    const showMobileSummary = () => {
      mobileShowForm.value = false
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
    
    // Navigation
    const nextStep = async () => {
      if (currentStep.value === 1 && isStep1Valid.value) {
        // Auto-registrar usuario si no está logueado
        await autoRegisterUser()
      }
      
      if (currentStep.value < 3) {
        currentStep.value++
        maxStep.value = Math.max(maxStep.value, currentStep.value)
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }
    
    const prevStep = () => {
      if (currentStep.value > 1) {
        currentStep.value--
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }
    
    const goToStep = (step) => {
      if (step <= maxStep.value) {
        currentStep.value = step
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }
    
    // Auto-register user
    const autoRegisterUser = async () => {
      const token = localStorage.getItem('access_token')
      if (token) return // Ya está logueado
      
      try {
        // Intentar registrar con los datos del formulario
        const response = await apiClient.post('/clientes/auto-register', {
          email: form.value.email,
          nombre: form.value.nombre,
          apellido: form.value.apellido || '',
          telefono: form.value.telefono
        })
        
        if (response.data.access_token) {
          localStorage.setItem('access_token', response.data.access_token)
          localStorage.setItem('refresh_token', response.data.refresh_token || '')
          localStorage.setItem('user', JSON.stringify({
            email: form.value.email,
            nombre: form.value.nombre,
            apellido: form.value.apellido
          }))
        }
      } catch (e) {
        // Si falla (usuario ya existe), no pasa nada
        console.log('Auto-register skipped:', e.response?.data?.detail || e.message)
      }
    }
    
    // Wompi Widget - Carga del SDK
    const loadWompiSDK = () => {
      return new Promise((resolve, reject) => {
        if (window.WidgetCheckout) { 
          wompiLoaded.value = true
          resolve(window.WidgetCheckout)
          return 
        }
        const script = document.createElement('script')
        script.src = 'https://checkout.wompi.co/widget.js'
        script.async = true
        script.onload = () => { 
          wompiLoaded.value = true
          resolve(window.WidgetCheckout) 
        }
        script.onerror = () => reject(new Error('Error cargando Wompi'))
        document.head.appendChild(script)
      })
    }
    
    // Generar referencia única para Wompi
    const generateWompiReference = () => {
      const timestamp = Date.now()
      const random = Math.floor(Math.random() * 10000)
      return `KH-${timestamp}-${random}`
    }
    
    // Prices
    const formatPrice = (price) => {
      const num = Number(price)
      return isNaN(num) ? '0' : new Intl.NumberFormat('es-CO').format(num)
    }

    const humanizeVariant = (text) => {
      // Reemplazar guiones bajos con espacios y capitalizar cada palabra
      return text
        ?.split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ') || ''
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

    const getCartMediaUrl = (item) => {
      const url = getImageUrl(item?.imagen_url || item?.imagen_principal || item?.imagen)
      if (!url) return ''
      if (isVideo(url)) {
        ensureVideoPoster(url)
        return videoPosters.value[url] || ''
      }
      return url
    }
    
    const getItemPrice = (item) => {
      const price = item.subtotal || item.precio_unitario || item.precio || 0
      return item.subtotal ? item.subtotal : price * (item.cantidad || 1)
    }
    
    const getSubtotal = () => cartItems.value.reduce((t, i) => t + getItemPrice(i), 0)
    const getTotal = () => getSubtotal() + (envioGratis.value ? 0 : costoEnvio.value)
    
    // Payment
    const processPayment = async () => {
      if (selectedPayment.value === 'asesor') {
        processing.value = true
        
        try {
          if (!cartItems.value.length) {
            alert('Tu carrito está vacío. Agrega productos antes de continuar.')
            processing.value = false
            return
          }

          const invalidItems = cartItems.value.filter(item => !item.variante_id && !item.producto_id && !item.id)
          if (invalidItems.length > 0) {
            alert('Hay productos sin identificador válido. Actualiza el carrito e intenta nuevamente.')
            processing.value = false
            return
          }

          // 0. VALIDAR STOCK ANTES DE CREAR ORDEN
          console.log('🔍 Validando disponibilidad de stock...')
          const stockValidationUrl = `${API_BASE_URL}/api/v1/ordenes/validar-stock`
          
          const stockCheckResponse = await fetch(stockValidationUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              items: cartItems.value.map(item => ({
                producto_id: item.id || item.producto_id || '00000000-0000-0000-0000-000000000000',
                variante_id: item.variante_id || null,
                variante_sku: item.variante_sku || '',
                color: item.color || '',
                largo: item.largo || '',
                cantidad: item.cantidad || 1,
                precio_unitario: item.precio_unitario || item.precio || 0,
                nombre: item.nombre || 'Producto'
              }))
            })
          })
          
          const stockValidation = await stockCheckResponse.json()
          
          if (!stockValidation.disponible) {
            console.warn('⚠️ Stock insuficiente:', stockValidation)
            processing.value = false
            
            // Mostrar modal con productos con problemas + imagen del carrito
            const productosProblema = stockValidation.productos.filter(p => !p.disponible).map(p => {
              const itemCarrito = cartItems.value.find(item =>
                (item.variante_id && item.variante_id === p.variante_id) ||
                (item.id || item.producto_id) === p.producto_id
              )
              return {
                ...p,
                imagen_url: itemCarrito?.imagen_url || itemCarrito?.imagen_principal || '/placeholder.jpg'
              }
            })
            stockModalMessage.value = 'Algunos productos no están disponibles en la cantidad solicitada.'
            stockModalProducts.value = productosProblema
            showStockModal.value = true
            return
          }
          
          console.log('✅ Stock validado correctamente')
          
          // 1. Crear orden en el backend con estado PENDIENTE
          // Obtener nombres de departamento y municipio (no IDs)
          const depNombre = getDepName.value || form.value.departamento || ''
          const munNombre = getMunName.value || form.value.municipio || ''
          
          const ordenData = {
            email: form.value.email,
            nombre: form.value.nombre,
            apellido: form.value.apellido || '',
            telefono: form.value.telefono,
            tipo_documento: form.value.tipoDocumento || 'CC',
            numero_documento: form.value.numeroDocumento || '',
            direccion: form.value.direccion,
            departamento: depNombre,
            municipio: munNombre,
            barrio: form.value.barrio || '',
            notas: form.value.apartamento || '',
            items: cartItems.value.map(item => ({
              producto_id: item.id || item.producto_id || '00000000-0000-0000-0000-000000000000',
              variante_id: item.variante_id || null,
              variante_sku: item.variante_sku || '',
              color: item.color || '',
              largo: item.largo || '',
              cantidad: item.cantidad || 1,
              precio_unitario: item.precio_unitario || item.precio || 0,
              nombre: item.nombre || 'Producto'
            })),
            subtotal: getSubtotal(),
            envio: envioGratis.value ? 0 : costoEnvio.value,
            total: getTotal(),
            metodo_pago: 'whatsapp'
          }
          
          console.log('📄 Datos de documento a enviar:', {
            tipo_documento: ordenData.tipo_documento,
            numero_documento: ordenData.numero_documento
          })
          
          // Usar URL completa para evitar problemas de proxy
          const apiUrl = `${API_BASE_URL}/api/v1/ordenes`
          
          const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(ordenData)
          })
          
          if (!response.ok) {
            const errorData = await response.text()
            console.error('Error API:', response.status, errorData)
            throw new Error(`Error al crear la orden: ${response.status}`)
          }
          
          const orden = await response.json()
          const code = orden.codigo || `KH-${Math.floor(1000 + Math.random() * 9000)}`
          
          // 1.5 Actualizar dirección del cliente para futuras compras
          try {
            const token = localStorage.getItem('access_token') // Corregido: access_token
            const userStr = localStorage.getItem('user')
            if (token && userStr) {
              const user = JSON.parse(userStr)
              // Obtener el cliente por email
              const clientesResponse = await fetch(`${API_BASE_URL}/api/v1/clientes/`, {
                headers: { 'Authorization': `Bearer ${token}` }
              })
              if (clientesResponse.ok) {
                const clientes = await clientesResponse.json()
                const clienteActual = clientes.find(c => c.email === user.email)
                if (clienteActual) {
                  // Actualizar cliente con la dirección usada en esta orden
                  const updateData = {
                    id: clienteActual.id,
                    telefono: form.value.telefono,
                    direccion: form.value.direccion,
                    departamento: depNombre, // Usar el nombre que ya calculamos
                    municipio: munNombre, // Usar el nombre que ya calculamos
                    barrio: form.value.barrio || ''
                  }
                  console.log('📤 Actualizando dirección del cliente:', updateData)
                  
                  // PUT sin ID en la ruta - el ID va en el body
                  const updateResponse = await fetch(`${API_BASE_URL}/api/v1/clientes/`, {
                    method: 'PUT',
                    headers: { 
                      'Content-Type': 'application/json',
                      'Authorization': `Bearer ${token}` 
                    },
                    body: JSON.stringify(updateData)
                  })
                  if (updateResponse.ok) {
                    console.log('✅ Dirección del cliente actualizada para futuras compras')
                  } else {
                    const errText = await updateResponse.text()
                    console.log('⚠️ Error al actualizar dirección:', updateResponse.status, errText)
                  }
                }
              }
            }
          } catch (updateError) {
            console.log('⚠️ No se pudo actualizar la dirección del cliente:', updateError.message)
            // No fallar la orden por esto
          }
          
          // 2. Guardar código temporal para usarlo en buildWhatsAppMessage
          sessionStorage.setItem('temp_order_code', code)
          
          // 3. Construir mensaje de WhatsApp de forma segura
          const msg = buildWhatsAppMessage()
          const whatsappFinal = '4796657763'
          sessionStorage.setItem('orden_whatsapp', JSON.stringify({
            codigo: code,
            total: getTotal(),
            productos: cartItems.value,
            cliente: {
              nombre: form.value.nombre,
              apellido: form.value.apellido,
              telefono: form.value.telefono,
              email: form.value.email,
              departamento: form.value.departamento,
              municipio: form.value.municipio,
              direccion: form.value.direccion,
              apartamento: form.value.apartamento,
              barrio: form.value.barrio,
              indicacionesRural: form.value.indicacionesRural
            },
            whatsappUrl: `https://wa.me/${whatsappFinal}?text=${msg}`
          }))
          
          // 4. Limpiar carrito y formulario
          localStorage.removeItem('kharis_cart_cache')
          localStorage.removeItem('kharis_cart_count')
          cartItems.value = []
          clearFormStorage()
          
          // 5. Limpiar sessionStorage después de un pequeño delay para asegurar que PedidoConfirmado puede leer los datos
          setTimeout(() => {
            sessionStorage.removeItem('temp_order_code')
          }, 2000)
          
          // 7. Redirigir a página de confirmación
          window.location.href = '/pedido-confirmado'
          
        } catch (e) {
          processing.value = false
          console.error('❌ Error al procesar la orden:', e)
          
          // Diferenciar entre errores de stock y otros errores
          const errorMsg = e.message || String(e)
          if (errorMsg.includes('409') || errorMsg.includes('Stock insuficiente')) {
            // Error de stock - mostrar modal amigable
            stockModalMessage.value = 'Alguien más compró los últimos productos mientras completabas tu compra.'
            stockModalProducts.value = []
            showStockModal.value = true
            return
          }
          
          alert('No se pudo registrar la orden. Verifica tu carrito y vuelve a intentarlo.')
          return
        } finally {
          processing.value = false
        }
      } else {
        // Pago con Wompi - Usar Link de Checkout (redirect) en lugar de widget embebido
        processing.value = true
        try {
          const reference = generateWompiReference()
          const amountInCents = Math.round(getTotal() * 100) // Wompi requiere centavos
          
          // Limpiar teléfono (solo dígitos, sin +57)
          const rawPhone = form.value.telefono || ''
          const cleanPhone = rawPhone.replace(/\D/g, '').slice(-10)
          
          console.log('📱 Teléfono raw:', rawPhone)
          console.log('📱 Teléfono limpio:', cleanPhone)
          
          // Validar teléfono
          if (!cleanPhone || cleanPhone.length < 10) {
            alert('Por favor ingresa un número de teléfono válido de 10 dígitos')
            processing.value = false
            return
          }
          
          // Guardar datos de la orden en localStorage para recuperar después del pago
          const orderData = {
            reference,
            items: cartItems.value,
            total: getTotal(),
            customer: {
              email: form.value.email,
              nombre: form.value.nombre,
              apellido: form.value.apellido,
              telefono: cleanPhone,
              direccion: getFullAddress()
            },
            createdAt: new Date().toISOString()
          }
          localStorage.setItem('kharis_pending_order', JSON.stringify(orderData))
          
          console.log('🔧 Redirigiendo a Wompi con:', {
            reference,
            amountInCents,
            email: form.value.email
          })
          
          // Construir URL de checkout de Wompi (método redirect)
          const redirectUrl = encodeURIComponent(`${window.location.origin}/pago-exitoso`)
          const wompiCheckoutUrl = `https://checkout.wompi.co/l/${WOMPI_CONFIG.publicKey}?` + new URLSearchParams({
            'currency': 'COP',
            'amount-in-cents': amountInCents.toString(),
            'reference': reference,
            'redirect-url': `${window.location.origin}/pago-exitoso`,
            'customer-data:email': form.value.email,
            'customer-data:full-name': `${form.value.nombre} ${form.value.apellido}`.trim(),
            'customer-data:phone-number': cleanPhone,
            'customer-data:phone-number-prefix': '57'
          }).toString()
          
          console.log('🔗 URL Wompi:', wompiCheckoutUrl)
          
          // Redirigir a Wompi
          window.location.href = wompiCheckoutUrl
          
        } catch (e) {
          console.error('Error con Wompi:', e)
          alert('Error al conectar con la pasarela de pagos. Intenta de nuevo o usa pago por WhatsApp.')
          processing.value = false
        }
      }
    }
    
    // Load cart
    const loadCart = () => {
      try {
        const cached = localStorage.getItem('kharis_cart_cache')
        if (cached) {
          const data = JSON.parse(cached)
          const rawItems = data.items || []
          cartItems.value = rawItems.map((item) => {
            const productoId = item?.producto_id ?? item?.id
            const varianteId = item?.variante_id ?? null
            return {
              ...item,
              producto_id: productoId,
              variante_id: varianteId
            }
          })
        }
        
        // Cargar datos del usuario si está logueado
        const user = JSON.parse(localStorage.getItem('user') || 'null')
        if (user && !form.value.email) {
          form.value.nombre = user.nombre || form.value.nombre
          form.value.email = user.email || form.value.email
          form.value.apellido = user.apellido || form.value.apellido
        }
      } catch (e) { console.error(e) }
    }
    
    const unlockScroll = () => {
      document.body.style.overflow = ''
      document.body.style.paddingRight = ''
    }
    
    onMounted(async () => {
      const router = useRouter()
      
      // Validar que hay carrito - si no, redirigir al inicio
      await loadCart()
      if (!cartItems.value || cartItems.value.length === 0) {
        console.warn('⚠️ No hay carrito, redirigiendo al inicio')
        // Limpiar sessionStorage si existe
        sessionStorage.removeItem('orden_whatsapp')
        sessionStorage.removeItem('temp_order_code')
        router.push('/')
        return
      }
      
      unlockScroll()
      loadFormFromStorage() // Cargar formulario guardado primero
      loadWompiSDK().catch(() => {}) // Pre-cargar SDK de Wompi
      
      // Cargar departamentos de Colombia
      await loadDepartamentos()
      
      // Cargar datos del cliente logueado (precarga automática)
      // Esto también carga municipios si el cliente tiene departamento guardado
      await loadClienteData()
      
      // Cerrar dropdowns al hacer click fuera
      document.addEventListener('click', (e) => {
        if (!e.target.closest('.custom-dropdown')) {
          closeDropdowns()
        }
      })
      
      // Carga completa - mostrar checkout
      initialLoading.value = false
    })
    
    onUnmounted(() => { unlockScroll() })
    
    return {
      currentStep, maxStep, selectedPayment, processing, cupon, form,
      cartItems, costoEnvio, envioGratis, stepperProgress,
      mobileShowForm, showMobileForm, showMobileSummary,
      departamentos, departamentosFiltrados, municipiosFiltrados,
      loadingDepartamentos, loadingMunicipios,
      dropdowns, searchDep, searchMun,
      toggleDropdown, selectDepartamento, selectMunicipio,
      getDepName, getMunName,
      isStep1Valid, isStep2Valid,
      nextStep, prevStep, goToStep,
      onPaisChange, onDepartamentoChange,
      getFullAddress, getWhatsAppAddress, saveFormToStorage, formatPhoneNumber, formatDocumentNumber,
      buildWhatsAppMessage, formatPrice, formatColorLabel, getItemPrice, getSubtotal, getTotal, processPayment,
      getCartMediaUrl,
      clienteConDatosCompletos,
      initialLoading,
      showStockModal, stockModalMessage, stockModalProducts
    }
  }
}
</script>

<style scoped>
/* =================================================================
   ESTILOS PREMIUM CHECKOUT - Diseño Luxury Minimalista
   ================================================================= */

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem; /* 6px entre label e input */
}

/* Labels premium: pequeños, elegantes */
.input-group label {
  font-size: 0.75rem; /* 12px */
  font-weight: 500;
  color: #6b7280;
  letter-spacing: 0.01em;
}

/* Inputs premium: fondo blanco, bordes finos elegantes */
.input-group input,
.input-group select,
.input-group textarea {
  width: 100%;
  padding: 0.9375rem 1rem; /* 15px vertical */
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem; /* 8px */
  font-size: 0.9375rem;
  color: #1A1A1A;
  transition: all 0.2s ease;
  height: 52px;
}

.input-group textarea {
  height: auto;
  min-height: 100px;
  border-radius: 0.5rem;
  resize: vertical;
}

/* Focus: borde magenta con glow sutil */
.input-group input:focus,
.input-group select:focus,
.input-group textarea:focus {
  outline: none;
  border-color: #c11252;
  box-shadow: 0 0 0 3px rgba(193, 18, 82, 0.06);
}

/* Hover sutil */
.input-group input:hover:not(:focus),
.input-group select:hover:not(:focus),
.input-group textarea:hover:not(:focus) {
  border-color: #d1d5db;
}

.input-group input::placeholder,
.input-group textarea::placeholder {
  color: #9CA3AF;
}

/* Select wrapper personalizado */
.select-wrapper {
  position: relative;
  width: 100%;
}

.select-wrapper select {
  width: 100%;
  padding: 0.875rem 2.5rem 0.875rem 1rem;
  background-color: white;
  border: 1px solid #E5E7EB;
  font-size: 0.875rem;
  color: #1A1A1A;
  transition: all 0.2s ease;
  height: 50px;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.select-wrapper select:focus {
  outline: none;
  border-color: #D81B60;
  box-shadow: 0 0 0 3px rgba(216, 27, 96, 0.08);
}

.select-wrapper select:disabled {
  background-color: #F9FAFB;
  color: #9CA3AF;
  cursor: not-allowed;
}

.select-arrow {
  position: absolute;
  right: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1rem;
  height: 1rem;
  color: #6B7280;
  pointer-events: none;
}

/* Custom Dropdown - Diseño Premium */
.custom-dropdown {
  position: relative;
  width: 100%;
}

.dropdown-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9375rem 1rem;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  color: #1A1A1A;
  height: 52px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.dropdown-trigger:hover {
  border-color: #d1d5db;
}

.dropdown-trigger:focus {
  outline: none;
  border-color: #c11252;
  box-shadow: 0 0 0 3px rgba(193, 18, 82, 0.06);
}

.dropdown-trigger:disabled {
  background-color: #fafafa;
  color: #9CA3AF;
  cursor: not-allowed;
  border-color: #e5e7eb;
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.15);
  z-index: 100;
  max-height: 360px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

@media (max-width: 640px) {
  .dropdown-panel {
    position: fixed;
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
    max-height: 70vh;
    border-radius: 1rem 1rem 0 0;
    border: none;
    box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.2);
    z-index: 200;
  }
}

.dropdown-search {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
}

.dropdown-search input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.9375rem;
  color: #1A1A1A;
  outline: none;
  height: auto;
  padding: 0;
}

.dropdown-search input::placeholder {
  color: #9CA3AF;
}

.dropdown-list {
  flex: 1;
  overflow-y: auto;
  list-style: none;
  padding: 0.5rem 0;
  margin: 0;
}

.dropdown-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1rem;
  font-size: 0.9375rem;
  color: #4A4A4A;
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-list li:hover {
  background: #fef7f9;
}

.dropdown-list li.selected {
  background: #fef7f9;
  color: #c11252;
  font-weight: 500;
}

.dropdown-list li.empty {
  color: #9CA3AF;
  cursor: default;
  justify-content: center;
}

.dropdown-list li.empty:hover {
  background: transparent;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animación para el modal */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}
</style>
