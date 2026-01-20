<template>
  <div class="min-h-screen flex flex-col bg-white">
    
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- HEADER                                                               -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <header class="bg-white border-b border-[#E5E7EB]">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="w-32"></div>
          <router-link to="/" class="font-luxury text-2xl tracking-wide text-[#1A1A1A]">
            Kharis
          </router-link>
          <div class="w-32 flex justify-end">
            <div class="flex items-center gap-2 text-sm text-[#6B7280]">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
              </svg>
              <span class="hidden sm:inline">Compra Segura</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- STEPPER VISUAL                                                       -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <div class="bg-white border-b border-[#E5E7EB] py-8">
      <div class="max-w-2xl mx-auto px-6">
        <div class="flex items-center justify-between relative">
          <div class="absolute top-5 left-[10%] right-[10%] h-[2px] bg-[#E5E7EB]"></div>
          <div 
            class="absolute top-5 left-[10%] h-[2px] bg-[#1A1A1A] transition-all duration-500"
            :style="{ width: stepperProgress }"
          ></div>
          
          <div class="relative z-10 flex flex-col items-center" @click="goToStep(1)">
            <div :class="[
              'w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all cursor-pointer',
              currentStep >= 1 ? 'bg-[#1A1A1A] text-white' : 'bg-white border-2 border-[#E5E7EB] text-[#9CA3AF]'
            ]">
              <svg v-if="currentStep > 1" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
              <span v-else>1</span>
            </div>
            <span :class="['mt-3 text-xs font-medium tracking-wide uppercase', currentStep >= 1 ? 'text-[#1A1A1A]' : 'text-[#9CA3AF]']">
              Datos
            </span>
          </div>
          
          <div class="relative z-10 flex flex-col items-center" @click="goToStep(2)">
            <div :class="[
              'w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all cursor-pointer',
              currentStep >= 2 ? 'bg-[#1A1A1A] text-white' : 'bg-white border-2 border-[#E5E7EB] text-[#9CA3AF]'
            ]">
              <svg v-if="currentStep > 2" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
              <span v-else>2</span>
            </div>
            <span :class="['mt-3 text-xs font-medium tracking-wide uppercase', currentStep >= 2 ? 'text-[#1A1A1A]' : 'text-[#9CA3AF]']">
              Envío
            </span>
          </div>
          
          <div class="relative z-10 flex flex-col items-center" @click="goToStep(3)">
            <div :class="[
              'w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all cursor-pointer',
              currentStep >= 3 ? 'bg-[#1A1A1A] text-white' : 'bg-white border-2 border-[#E5E7EB] text-[#9CA3AF]'
            ]">
              <span>3</span>
            </div>
            <span :class="['mt-3 text-xs font-medium tracking-wide uppercase', currentStep >= 3 ? 'text-[#1A1A1A]' : 'text-[#9CA3AF]']">
              Pago
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!-- CONTENIDO PRINCIPAL                                                  -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <main class="flex-1 py-10">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex flex-col lg:flex-row gap-10">
          
          <!-- COLUMNA IZQUIERDA: Formularios -->
          <div class="flex-1">
            <div class="bg-white rounded-lg shadow-sm border border-[#E5E7EB] overflow-hidden">
              
              <!-- ═══════════════════════════════════════════════════════════ -->
              <!-- PASO 1: Datos de Contacto                                    -->
              <!-- ═══════════════════════════════════════════════════════════ -->
              <div v-show="currentStep === 1">
                <div class="px-8 py-6 border-b border-[#E5E7EB]">
                  <h2 class="font-luxury text-xl text-[#1A1A1A]">Datos de Contacto</h2>
                  <p class="text-sm text-[#7A7A7A] mt-1">Te enviaremos actualizaciones de tu pedido</p>
                </div>
                
                <div class="p-8 space-y-5">
                  <div class="input-group">
                    <label>Correo electrónico</label>
                    <input type="email" v-model="form.email" placeholder="tu@email.com" @input="saveFormToStorage" />
                  </div>
                  
                  <div class="grid sm:grid-cols-2 gap-5">
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
                    <label>Teléfono (WhatsApp)</label>
                    <div class="relative">
                      <span class="absolute left-4 top-1/2 -translate-y-1/2 text-[#7A7A7A] text-sm">+57</span>
                      <input type="tel" v-model="form.telefono" placeholder="300 123 4567" class="!pl-12" @input="saveFormToStorage" />
                    </div>
                  </div>
                  
                  <label class="flex items-center gap-3 cursor-pointer group mt-6">
                    <div class="relative">
                      <input type="checkbox" v-model="form.newsletter" class="sr-only peer" @change="saveFormToStorage" />
                      <div class="w-5 h-5 border-2 border-[#D1D5DB] rounded peer-checked:bg-[#1A1A1A] peer-checked:border-[#1A1A1A] transition-all"></div>
                      <svg class="absolute inset-0 w-5 h-5 text-white opacity-0 peer-checked:opacity-100" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                    </div>
                    <span class="text-sm text-[#7A7A7A]">Recibir novedades y ofertas exclusivas</span>
                  </label>
                </div>
                
                <div class="px-8 py-6 bg-[#FAFAFA] border-t border-[#E5E7EB]">
                  <button 
                    @click="nextStep"
                    :disabled="!isStep1Valid"
                    class="w-full bg-[#000000] hover:bg-[#D81B60] disabled:bg-[#F3F4F6] disabled:text-[#9CA3AF] text-white py-4 text-sm font-medium tracking-widest uppercase transition-all"
                  >
                    Continuar al Envío
                  </button>
                  
                  <div class="flex items-center justify-center gap-6 mt-6 text-xs text-[#6B7280]">
                    <div class="flex items-center gap-1.5">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                      </svg>
                      <span>Pago Seguro SSL</span>
                    </div>
                    <div class="flex items-center gap-1.5">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                      </svg>
                      <span>Envío Nacional</span>
                    </div>
                    <div class="flex items-center gap-1.5">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
                      </svg>
                      <span>Garantía de Calidad</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- ═══════════════════════════════════════════════════════════ -->
              <!-- PASO 2: Dirección de Envío                                   -->
              <!-- ═══════════════════════════════════════════════════════════ -->
              <div v-show="currentStep === 2">
                <div class="px-8 py-6 border-b border-[#E5E7EB]">
                  <h2 class="font-luxury text-xl text-[#1A1A1A]">Dirección de Envío</h2>
                  <p class="text-sm text-[#7A7A7A] mt-1">¿Dónde entregamos tu pedido?</p>
                </div>
                
                <div class="p-8 space-y-5">
                  <!-- País y Departamento en línea -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <!-- País -->
                    <div class="input-group">
                      <label>País</label>
                      <div class="select-wrapper">
                        <select v-model="form.pais" @change="onPaisChange">
                          <option value="">Selecciona país</option>
                          <option value="CO">Colombia</option>
                        </select>
                        <svg class="select-arrow" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                    </div>
                    
                    <!-- Departamento - Dropdown personalizado -->
                    <div class="input-group" v-if="form.pais === 'CO'">
                      <label>Departamento</label>
                      <div class="custom-dropdown" @click.stop>
                        <button 
                          type="button"
                          @click="toggleDropdown('departamento')"
                          :disabled="loadingDepartamentos"
                          class="dropdown-trigger"
                        >
                          <span :class="{ 'text-[#9CA3AF]': !getDepName }">
                            {{ loadingDepartamentos ? 'Cargando...' : (getDepName || 'Selecciona departamento') }}
                          </span>
                          <svg v-if="!loadingDepartamentos" class="w-4 h-4 text-[#6B7280] transition-transform" :class="{ 'rotate-180': dropdowns.departamento }" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                          </svg>
                          <svg v-else class="w-4 h-4 text-[#6B7280] animate-spin" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                          </svg>
                        </button>
                        
                        <!-- Dropdown panel -->
                        <div v-show="dropdowns.departamento" class="dropdown-panel">
                          <div class="dropdown-search">
                            <svg class="w-4 h-4 text-[#9CA3AF]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            <input 
                              type="text" 
                              v-model="searchDep" 
                              placeholder="Buscar departamento..."
                              @click.stop
                            />
                          </div>
                          <ul class="dropdown-list">
                            <li 
                              v-for="dep in departamentosFiltrados" 
                              :key="dep.id"
                              @click="selectDepartamento(dep)"
                              :class="{ 'selected': dep.id === form.departamento }"
                            >
                              {{ dep.nombre }}
                              <svg v-if="dep.id === form.departamento" class="w-4 h-4 text-[#1A1A1A]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
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
                  
                  <!-- Municipio y Tipo de Zona en línea -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" v-if="form.departamento">
                    <!-- Municipio - Dropdown personalizado -->
                    <div class="input-group">
                      <label>Municipio</label>
                      <div class="custom-dropdown" @click.stop>
                        <button 
                          type="button"
                          @click="toggleDropdown('municipio')"
                          :disabled="loadingMunicipios"
                          class="dropdown-trigger"
                        >
                          <span :class="{ 'text-[#9CA3AF]': !getMunName }">
                            {{ loadingMunicipios ? 'Cargando...' : (getMunName || 'Selecciona municipio') }}
                          </span>
                          <svg v-if="!loadingMunicipios" class="w-4 h-4 text-[#6B7280] transition-transform" :class="{ 'rotate-180': dropdowns.municipio }" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                          </svg>
                          <svg v-else class="w-4 h-4 text-[#6B7280] animate-spin" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                          </svg>
                        </button>
                        
                        <!-- Dropdown panel -->
                        <div v-show="dropdowns.municipio" class="dropdown-panel">
                          <div class="dropdown-search">
                            <svg class="w-4 h-4 text-[#9CA3AF]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            <input 
                              type="text" 
                              v-model="searchMun" 
                              placeholder="Buscar municipio..."
                              @click.stop
                            />
                          </div>
                          <ul class="dropdown-list">
                            <li 
                              v-for="mun in municipiosFiltrados" 
                              :key="mun.id"
                              @click="selectMunicipio(mun)"
                              :class="{ 'selected': mun.id === form.municipio }"
                            >
                              {{ mun.nombre }}
                              <svg v-if="mun.id === form.municipio" class="w-4 h-4 text-[#1A1A1A]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
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
                      <div class="flex gap-2 h-[50px]">
                        <button 
                          type="button"
                          @click="form.tipoZona = 'urbano'; saveFormToStorage()"
                          :class="[
                            'flex-1 flex items-center justify-center gap-2 border transition-all text-sm font-medium',
                            form.tipoZona === 'urbano' 
                              ? 'border-[#1A1A1A] bg-[#1A1A1A] text-white' 
                              : 'border-[#E5E7EB] hover:border-[#9CA3AF] text-[#4A4A4A]'
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
                            'flex-1 flex items-center justify-center gap-2 border transition-all text-sm font-medium',
                            form.tipoZona === 'rural' 
                              ? 'border-[#1A1A1A] bg-[#1A1A1A] text-white' 
                              : 'border-[#E5E7EB] hover:border-[#9CA3AF] text-[#4A4A4A]'
                          ]"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                          </svg>
                          Rural
                        </button>
                      </div>
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
                    <label>Vereda / Indicaciones de llegada</label>
                    <textarea 
                      v-model="form.indicacionesRural" 
                      placeholder="Describe cómo llegar a tu ubicación..."
                      class="!h-24 resize-none"
                      @input="saveFormToStorage"
                    ></textarea>
                  </div>
                  
                  <!-- Apartamento/Oficina -->
                  <div class="input-group" v-if="form.tipoZona">
                    <label>Apartamento, oficina, local (opcional)</label>
                    <input type="text" v-model="form.apartamento" placeholder="Ej: Apto 201, Torre B" @input="saveFormToStorage" />
                  </div>
                </div>
                
                <div class="px-8 py-6 bg-[#FAFAFA] border-t border-[#E5E7EB]">
                  <div class="flex gap-4">
                    <button 
                      @click="prevStep"
                      class="px-8 py-4 border border-[#E5E7EB] text-[#4A4A4A] text-sm font-medium tracking-widest uppercase hover:border-[#1A1A1A] transition-all"
                    >
                      Volver
                    </button>
                    <button 
                      @click="nextStep"
                      :disabled="!isStep2Valid"
                      class="flex-1 bg-[#000000] hover:bg-[#D81B60] disabled:bg-[#F3F4F6] disabled:text-[#9CA3AF] text-white py-4 text-sm font-medium tracking-widest uppercase transition-all"
                    >
                      Continuar al Pago
                    </button>
                  </div>
                  
                  <div class="flex items-center justify-center gap-6 mt-6 text-xs text-[#6B7280]">
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
              <div v-show="currentStep === 3">
                <div class="px-8 py-6 border-b border-[#E5E7EB]">
                  <h2 class="font-luxury text-xl text-[#1A1A1A]">Método de Pago</h2>
                  <p class="text-sm text-[#7A7A7A] mt-1">Selecciona cómo deseas pagar</p>
                </div>
                
                <!-- Resumen de datos -->
                <div class="mx-8 my-6 border border-[#E5E7EB] divide-y divide-[#E5E7EB]">
                  <div class="flex items-center justify-between px-5 py-4">
                    <div class="flex gap-4">
                      <span class="text-xs text-[#6B7280] uppercase tracking-wider w-14">Contacto</span>
                      <span class="text-sm text-[#4A4A4A]">{{ form.email }}</span>
                    </div>
                    <button @click="goToStep(1)" class="text-xs text-[#D81B60] hover:underline">Cambiar</button>
                  </div>
                  <div class="flex items-center justify-between px-5 py-4">
                    <div class="flex gap-4">
                      <span class="text-xs text-[#6B7280] uppercase tracking-wider w-14">Envío</span>
                      <span class="text-sm text-[#4A4A4A]">{{ getFullAddress() }}</span>
                    </div>
                    <button @click="goToStep(2)" class="text-xs text-[#D81B60] hover:underline">Cambiar</button>
                  </div>
                </div>
                
                <!-- Opciones de Pago -->
                <div class="px-8 pb-8 space-y-4">
                  <!-- Opción ePayco -->
                  <div 
                    @click="selectedPayment = 'epayco'"
                    :class="[
                      'cursor-pointer border-2 p-5 transition-all',
                      selectedPayment === 'epayco' 
                        ? 'border-[#D81B60] bg-[#FDF2F8]' 
                        : 'border-[#E5E7EB] hover:border-[#9CA3AF]'
                    ]"
                  >
                    <div class="flex items-center gap-4">
                      <div :class="[
                        'w-5 h-5 rounded-full border-2 flex items-center justify-center',
                        selectedPayment === 'epayco' ? 'border-[#D81B60]' : 'border-[#D1D5DB]'
                      ]">
                        <div :class="['w-2.5 h-2.5 rounded-full', selectedPayment === 'epayco' ? 'bg-[#D81B60]' : '']"></div>
                      </div>
                      <div class="flex-1">
                        <p class="font-medium text-[#1A1A1A]">Pago Seguro Inmediato</p>
                        <p class="text-xs text-[#7A7A7A] mt-0.5">Tarjeta, PSE, Nequi, Daviplata</p>
                      </div>
                      <div class="flex items-center gap-2">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" alt="Visa" class="h-4" />
                        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg" alt="MC" class="h-5" />
                        <!-- Icono ePayco SVG en lugar de imagen rota -->
                        <div class="h-5 px-2 bg-[#00B4DB] rounded text-white text-[10px] font-bold flex items-center">
                          ePayco
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Opción Asesora -->
                  <div 
                    @click="selectedPayment = 'asesor'"
                    :class="[
                      'cursor-pointer border-2 p-5 transition-all relative',
                      selectedPayment === 'asesor' 
                        ? 'border-[#D81B60] bg-[#FDF2F8]' 
                        : 'border-[#E5E7EB] hover:border-[#9CA3AF]'
                    ]"
                  >
                    <div class="absolute -top-2.5 left-4 px-2 py-0.5 bg-[#C9A962] text-white text-[10px] tracking-wider uppercase font-medium">
                      Recomendado
                    </div>
                    <div class="flex items-center gap-4">
                      <div :class="[
                        'w-5 h-5 rounded-full border-2 flex items-center justify-center',
                        selectedPayment === 'asesor' ? 'border-[#D81B60]' : 'border-[#D1D5DB]'
                      ]">
                        <div :class="['w-2.5 h-2.5 rounded-full', selectedPayment === 'asesor' ? 'bg-[#D81B60]' : '']"></div>
                      </div>
                      <div class="flex-1">
                        <p class="font-medium text-[#1A1A1A]">Finalizar con Asesora</p>
                        <p class="text-xs text-[#7A7A7A] mt-0.5">Atención personalizada por WhatsApp</p>
                      </div>
                      <div class="w-9 h-9 rounded-full bg-[#25D366]/10 flex items-center justify-center">
                        <svg class="w-5 h-5 text-[#25D366]" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="px-8 py-6 bg-[#FAFAFA] border-t border-[#E5E7EB]">
                  <div class="flex gap-4">
                    <button 
                      @click="prevStep"
                      class="px-8 py-4 border border-[#E5E7EB] text-[#4A4A4A] text-sm font-medium tracking-widest uppercase hover:border-[#1A1A1A] transition-all"
                    >
                      Volver
                    </button>
                    <button 
                      @click="processPayment"
                      :disabled="!selectedPayment || processing"
                      class="flex-1 bg-[#000000] hover:bg-[#D81B60] disabled:bg-[#F3F4F6] disabled:text-[#9CA3AF] text-white py-4 text-sm font-medium tracking-widest uppercase transition-all flex items-center justify-center gap-2"
                    >
                      <svg v-if="processing" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                      </svg>
                      <span v-if="processing">Conectando con pasarela...</span>
                      <span v-else>{{ selectedPayment === 'asesor' ? 'Continuar por WhatsApp' : 'Pagar Ahora' }}</span>
                    </button>
                  </div>
                  
                  <div class="flex items-center justify-center gap-2 mt-6 text-xs text-[#6B7280]">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                    </svg>
                    <span>Transacción protegida con encriptación SSL de 256 bits</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- COLUMNA DERECHA: Resumen del Pedido -->
          <div class="w-full lg:w-[400px] xl:w-[420px]">
            <div class="bg-white rounded-lg border border-[#E5E7EB] overflow-hidden lg:sticky lg:top-6">
              
              <div class="px-6 py-5 border-b border-[#E5E7EB]">
                <h3 class="font-medium text-[#1A1A1A]">Resumen de Compra</h3>
              </div>
              
              <div class="divide-y divide-[#E5E7EB]">
                <div 
                  v-for="item in cartItems" 
                  :key="item.producto_id"
                  class="flex gap-4 px-6 py-5"
                >
                  <div class="w-20 h-20 bg-white rounded border border-[#E5E7EB] overflow-hidden flex-shrink-0">
                    <img 
                      v-if="item.imagen_url" 
                      :src="item.imagen_url" 
                      :alt="item.nombre"
                      class="w-full h-full object-cover"
                    />
                    <div v-else class="w-full h-full flex items-center justify-center bg-[#FAF5F2]">
                      <svg class="w-8 h-8 text-[#D1D5DB]" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                      </svg>
                    </div>
                  </div>
                  
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-[#1A1A1A] line-clamp-2">{{ item.nombre || 'Producto' }}</p>
                    <p class="text-xs text-[#7A7A7A] mt-1">Cantidad: {{ item.cantidad || 1 }}</p>
                  </div>
                  
                  <div class="text-sm font-medium text-[#1A1A1A]">
                    ${{ formatPrice(getItemPrice(item)) }}
                  </div>
                </div>
              </div>
              
              <div class="px-6 py-5 border-t border-[#E5E7EB]">
                <div class="flex gap-3">
                  <input 
                    type="text" 
                    v-model="cupon"
                    class="flex-1 px-4 py-3 bg-white border border-[#E5E7EB] text-sm focus:outline-none focus:border-[#1A1A1A] placeholder:text-[#9CA3AF]"
                    placeholder="Código de descuento"
                  />
                  <button class="px-5 py-3 bg-[#1A1A1A] text-white text-sm font-medium hover:bg-black transition-colors">
                    Aplicar
                  </button>
                </div>
              </div>
              
              <div class="px-6 py-5 border-t border-[#E5E7EB] space-y-3">
                <div class="flex justify-between text-sm">
                  <span class="text-[#7A7A7A]">Subtotal</span>
                  <span class="text-[#4A4A4A]">${{ formatPrice(getSubtotal()) }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-[#7A7A7A]">Envío</span>
                  <span :class="envioGratis ? 'text-green-600' : 'text-[#4A4A4A]'">
                    {{ envioGratis ? 'Gratis' : '$' + formatPrice(costoEnvio) }}
                  </span>
                </div>
                
                <div class="border-t-2 border-[#1A1A1A] my-4"></div>
                
                <div class="flex justify-between items-baseline">
                  <span class="font-luxury text-lg text-[#1A1A1A]">Total</span>
                  <div class="text-right">
                    <span class="font-luxury text-2xl lg:text-3xl text-[#1A1A1A]">${{ formatPrice(getTotal()) }}</span>
                    <span class="text-xs text-[#7A7A7A] ml-1">COP</span>
                  </div>
                </div>
                
                <p class="text-xs text-[#6B7280] text-right">Incluye impuestos</p>
              </div>
              
              <div v-if="!envioGratis" class="px-6 py-4 bg-[#F9FAFB] border-t border-[#E5E7EB]">
                <div class="flex items-center gap-2 text-xs text-[#6B7280]">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                  </svg>
                  <span>Agrega ${{ formatPrice(300000 - getSubtotal()) }} más para envío gratis</span>
                </div>
                <div class="w-full h-1.5 bg-[#E5E7EB] rounded-full mt-2 overflow-hidden">
                  <div 
                    class="h-full bg-[#C9A962] transition-all"
                    :style="{ width: Math.min((getSubtotal() / 300000) * 100, 100) + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-[#E5E7EB] py-6 mt-auto">
      <div class="max-w-7xl mx-auto px-6 flex flex-wrap items-center justify-center gap-4 text-xs text-[#6B7280]">
        <a href="#" class="hover:text-[#1A1A1A] transition-colors">Política de Privacidad</a>
        <span class="text-[#D1D5DB]">·</span>
        <a href="#" class="hover:text-[#1A1A1A] transition-colors">Términos del Servicio</a>
        <span class="text-[#D1D5DB]">·</span>
        <a href="#" class="hover:text-[#1A1A1A] transition-colors">Política de Devoluciones</a>
      </div>
    </footer>

    <!-- Overlay de carga ePayco -->
    <div v-if="processing && selectedPayment === 'epayco'" class="fixed inset-0 bg-black/60 z-[999] flex items-center justify-center">
      <div class="bg-white rounded-lg p-8 max-w-sm mx-4 text-center">
        <div class="mb-4 flex justify-center">
          <svg class="w-16 h-16 text-[#D81B60] animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <h3 class="font-luxury text-xl text-[#1A1A1A] mb-2">Abriendo banco...</h3>
        <p class="text-sm text-[#7A7A7A]">Conectando con la pasarela de pagos segura</p>
        <div class="mt-6 flex items-center justify-center gap-2 text-xs text-[#9CA3AF]">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
          </svg>
          <span>Conexión segura SSL</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

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
    const selectedPayment = ref(null)
    const processing = ref(false)
    const cupon = ref('')
    const epaycoLoaded = ref(false)
    
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
    
    const EPAYCO_CONFIG = {
      publicKey: import.meta.env.VITE_EPAYCO_PUBLIC_KEY || '2943652c673afffaa5b7b67829f00a0c',
      test: import.meta.env.VITE_EPAYCO_TEST_MODE === 'true'
    }
    const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER || '4796657763'
    
    // Form con nuevos campos
    const form = ref({
      email: '',
      nombre: '',
      apellido: '',
      telefono: '',
      newsletter: false,
      pais: '',
      departamento: '',
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
    const loadMunicipios = async (departamentoId) => {
      if (!departamentoId) {
        municipios.value = []
        return
      }
      
      loadingMunicipios.value = true
      try {
        const response = await fetch(COLOMBIA_API.ciudades(departamentoId))
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
      form.value.departamento = dep.id
      dropdowns.value.departamento = false
      searchDep.value = ''
      form.value.municipio = ''
      form.value.tipoZona = ''
      saveFormToStorage()
      await loadMunicipios(dep.id)
    }
    
    const selectMunicipio = (mun) => {
      form.value.municipio = mun.id
      dropdowns.value.municipio = false
      searchMun.value = ''
      saveFormToStorage()
    }
    
    // Obtener nombre seleccionado
    const getDepName = computed(() => {
      const dep = departamentos.value.find(d => d.id === form.value.departamento)
      return dep ? dep.nombre : ''
    })
    
    const getMunName = computed(() => {
      const mun = municipios.value.find(m => m.id === form.value.municipio)
      return mun ? mun.nombre : ''
    })
    
    // Cart
    const cartItems = ref([])
    const costoEnvio = ref(30000)
    const envioGratis = computed(() => getSubtotal() >= 300000)
    
    const stepperProgress = computed(() => {
      if (currentStep.value === 1) return '0%'
      if (currentStep.value === 2) return '40%'
      return '80%'
    })
    
    // Validations
    const isStep1Valid = computed(() => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return form.value.email && emailRegex.test(form.value.email) &&
             form.value.nombre && form.value.telefono
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
    
    const saveFormToStorage = () => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(form.value))
      } catch (e) {
        console.warn('Error saving form to storage', e)
      }
    }
    
    const loadFormFromStorage = () => {
      try {
        const saved = localStorage.getItem(STORAGE_KEY)
        if (saved) {
          const data = JSON.parse(saved)
          Object.assign(form.value, data)
        }
      } catch (e) {
        console.warn('Error loading form from storage', e)
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
      const dep = departamentos.value.find(d => d.codigo === form.value.departamento || d.id === Number(form.value.departamento))
      const mun = municipiosFiltrados.value.find(m => m.codigo === form.value.municipio || m.id === Number(form.value.municipio))
      
      let addr = ''
      if (form.value.tipoZona === 'urbano') {
        addr = form.value.direccion
        if (form.value.barrio) addr += `, ${form.value.barrio}`
      } else {
        addr = form.value.indicacionesRural?.substring(0, 50) + '...'
      }
      
      return `${addr}, ${mun?.nombre || ''}, ${dep?.nombre || ''}`
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
    
    // ePayco
    const loadEpaycoSDK = () => {
      return new Promise((resolve, reject) => {
        if (window.ePayco) { epaycoLoaded.value = true; resolve(window.ePayco); return }
        const script = document.createElement('script')
        script.src = 'https://checkout.epayco.co/checkout.js'
        script.async = true
        script.onload = () => { epaycoLoaded.value = true; resolve(window.ePayco) }
        script.onerror = () => reject(new Error('Error cargando ePayco'))
        document.head.appendChild(script)
      })
    }
    
    // Prices
    const formatPrice = (price) => {
      const num = Number(price)
      return isNaN(num) ? '0' : new Intl.NumberFormat('es-CO').format(num)
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
        const code = `K-${Math.floor(1000 + Math.random() * 9000)}`
        const productos = cartItems.value.map(i => `• ${i.nombre || 'Producto'} x${i.cantidad || 1}`).join('%0A')
        const msg = `Hola, quiero finalizar mi pedido ✨%0A%0A🆔 *Código:* ${code}%0A%0A📦 *Productos:*%0A${productos}%0A%0A💰 *Total:* $${formatPrice(getTotal())} COP%0A%0A👤 *${form.value.nombre} ${form.value.apellido}*%0A📍 ${getFullAddress()}`
        window.open(`https://wa.me/${whatsappNumber}?text=${msg}`, '_blank')
        clearFormStorage()
      } else {
        processing.value = true
        try {
          await loadEpaycoSDK()
          const handler = window.ePayco.checkout.configure({ key: EPAYCO_CONFIG.publicKey, test: EPAYCO_CONFIG.test })
          const invoiceId = `KH-${Date.now()}-${Math.floor(Math.random() * 1000)}`
          
          // Pequeño delay para mostrar el loader antes de abrir ePayco
          await new Promise(resolve => setTimeout(resolve, 300))
          
          handler.open({
            name: 'Kharis Distribuidora',
            description: cartItems.value.map(i => `${i.nombre || 'Producto'} x${i.cantidad || 1}`).join(', ').substring(0, 250),
            invoice: invoiceId,
            currency: 'cop',
            amount: String(getTotal()),
            tax_base: '0',
            tax: '0',
            country: 'co',
            lang: 'es',
            external: 'true',
            response: `${window.location.origin}/pago-exitoso`,
            name_billing: `${form.value.nombre} ${form.value.apellido}`,
            address_billing: getFullAddress(),
            mobilephone_billing: form.value.telefono,
            email_billing: form.value.email
          })
          
          // Esperar un poco más para asegurar que la ventana de ePayco se abre
          await new Promise(resolve => setTimeout(resolve, 800))
          
          clearFormStorage()
        } catch (e) {
          alert('Error al conectar con la pasarela de pagos. Intenta de nuevo.')
        } finally {
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
          cartItems.value = data.items || []
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
      unlockScroll()
      loadFormFromStorage() // Cargar formulario guardado
      loadCart()
      loadEpaycoSDK().catch(() => {}) // Pre-cargar SDK
      
      // Cargar departamentos de Colombia
      await loadDepartamentos()
      
      // Si hay un departamento guardado, cargar sus municipios
      if (form.value.departamento) {
        await loadMunicipios(form.value.departamento)
      }
      
      // Cerrar dropdowns al hacer click fuera
      document.addEventListener('click', (e) => {
        if (!e.target.closest('.custom-dropdown')) {
          closeDropdowns()
        }
      })
    })
    
    onUnmounted(() => { unlockScroll() })
    
    return {
      currentStep, maxStep, selectedPayment, processing, cupon, form,
      cartItems, costoEnvio, envioGratis, stepperProgress,
      departamentos, departamentosFiltrados, municipiosFiltrados,
      loadingDepartamentos, loadingMunicipios,
      dropdowns, searchDep, searchMun,
      toggleDropdown, selectDepartamento, selectMunicipio,
      getDepName, getMunName,
      isStep1Valid, isStep2Valid,
      nextStep, prevStep, goToStep,
      onPaisChange, onDepartamentoChange,
      getFullAddress, saveFormToStorage,
      formatPrice, getItemPrice, getSubtotal, getTotal, processPayment
    }
  }
}
</script>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
  font-size: 0.75rem;
  font-weight: 500;
  color: #7A7A7A;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-group input,
.input-group select,
.input-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  background-color: white;
  border: 1px solid #E5E7EB;
  font-size: 0.875rem;
  color: #1A1A1A;
  transition: all 0.2s ease;
  height: 50px;
}

.input-group textarea {
  height: auto;
  min-height: 80px;
}

.input-group input:focus,
.input-group select:focus,
.input-group textarea:focus {
  outline: none;
  border-color: #1A1A1A;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
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
  border-color: #1A1A1A;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
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

/* Custom Dropdown */
.custom-dropdown {
  position: relative;
  width: 100%;
}

.dropdown-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1rem;
  background-color: white;
  border: 1px solid #E5E7EB;
  font-size: 0.875rem;
  color: #1A1A1A;
  height: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.dropdown-trigger:hover {
  border-color: #9CA3AF;
}

.dropdown-trigger:focus {
  outline: none;
  border-color: #1A1A1A;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.dropdown-trigger:disabled {
  background-color: #F9FAFB;
  color: #9CA3AF;
  cursor: not-allowed;
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #E5E7EB;
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.15);
  z-index: 100;
  max-height: 360px;
  display: flex;
  flex-direction: column;
}

@media (max-width: 640px) {
  .dropdown-panel {
    max-height: 320px;
  }
}

.dropdown-search {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #E5E7EB;
  background: #FAFAFA;
}

.dropdown-search input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.875rem;
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
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #4A4A4A;
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-list li:hover {
  background: #F9FAFB;
}

.dropdown-list li.selected {
  background: #F3F4F6;
  color: #1A1A1A;
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
</style>
