<template>
  <div class="min-h-screen flex flex-col lg:flex-row">
    <!-- =========================================================================
         LADO IZQUIERDO - Branding (igual que login)
    ========================================================================== -->
    <div class="relative lg:w-5/12 h-24 sm:h-40 lg:h-screen overflow-hidden">
      <!-- Gradient de fondo -->
      <div class="absolute inset-0 bg-gradient-to-br from-[#1A1A1A] via-[#2D2D2D] to-[#1A1A1A]"></div>
      
      <!-- Patrón decorativo -->
      <div class="absolute inset-0 opacity-5">
        <div class="absolute inset-0" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23C9A962\' fill-opacity=\'0.4\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>
      
      <!-- Overlay -->
      <div class="absolute inset-0 bg-black/40"></div>
      
      <!-- Contenido -->
      <div class="relative z-10 h-full flex flex-col justify-between p-4 sm:p-6 lg:p-12">
        <!-- Logo -->
        <div class="flex items-center gap-2 lg:gap-3">
          <div class="w-8 h-8 lg:w-12 lg:h-12 rounded-full bg-white/10 p-1.5 lg:p-2 flex items-center justify-center">
            <img src="/logo-kharis.png" alt="Kharis" class="w-full h-full object-contain" />
          </div>
          <div>
            <span class="text-[#C9A962] font-luxury text-base lg:text-xl tracking-wider">KHARIS</span>
            <span class="text-white/60 text-[10px] lg:text-sm block -mt-0.5 lg:-mt-1">PRO</span>
          </div>
        </div>
        
        <!-- Beneficios - Solo desktop -->
        <div class="hidden lg:block max-w-sm">
          <h1 class="text-white text-2xl xl:text-3xl font-luxury leading-tight mb-6">
            Únete a nuestra red exclusiva de distribuidores
          </h1>
          
          <ul class="space-y-4">
            <li class="flex items-start gap-3">
              <div class="w-6 h-6 rounded-full bg-[#C9A962]/20 flex items-center justify-center shrink-0 mt-0.5">
                <svg class="w-3.5 h-3.5 text-[#C9A962]" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <div>
                <p class="text-white font-medium">Precios Mayoristas</p>
                <p class="text-white/50 text-sm">Hasta 40% de descuento en productos</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <div class="w-6 h-6 rounded-full bg-[#C9A962]/20 flex items-center justify-center shrink-0 mt-0.5">
                <svg class="w-3.5 h-3.5 text-[#C9A962]" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <div>
                <p class="text-white font-medium">Crédito y Facilidades</p>
                <p class="text-white/50 text-sm">Opciones de pago flexibles</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <div class="w-6 h-6 rounded-full bg-[#C9A962]/20 flex items-center justify-center shrink-0 mt-0.5">
                <svg class="w-3.5 h-3.5 text-[#C9A962]" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <div>
                <p class="text-white font-medium">Soporte Prioritario</p>
                <p class="text-white/50 text-sm">Asesor dedicado para tu negocio</p>
              </div>
            </li>
          </ul>
        </div>

        <!-- Badge seguridad -->
        <div class="hidden lg:flex items-center gap-2 text-white/40 text-xs">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <span>Tus datos están protegidos</span>
        </div>
      </div>
    </div>

    <!-- =========================================================================
         LADO DERECHO - Formulario de Registro
    ========================================================================== -->
    <div class="flex-1 lg:w-7/12 flex items-start lg:items-center justify-center bg-[#FAFAFA] px-4 py-4 sm:p-6 lg:p-12 overflow-y-auto">
      <div class="w-full max-w-lg">
        
        <!-- ===== ESTADO: Solicitud Enviada ===== -->
        <div v-if="submitted" class="text-center py-8">
          <div class="w-20 h-20 mx-auto mb-6 rounded-full bg-green-100 flex items-center justify-center">
            <svg class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          
          <h2 class="text-2xl font-luxury text-text-dark mb-3">
            ¡Solicitud Recibida!
          </h2>
          
          <p class="text-text-medium mb-6 max-w-sm mx-auto">
            Nuestro equipo verificará tu identidad y documentos en menos de 
            <span class="font-semibold text-[#C9A962]">24 horas</span>.
          </p>
          
          <div class="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6 text-left">
            <div class="flex items-start gap-3">
              <svg class="w-5 h-5 text-amber-600 shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
              <div>
                <p class="text-sm font-medium text-amber-800">¿Qué sigue?</p>
                <ul class="text-sm text-amber-700 mt-1 space-y-1">
                  <li>• Recibirás un correo de confirmación</li>
                  <li>• Verificaremos tus documentos</li>
                  <li>• Te notificaremos cuando tu cuenta esté activa</li>
                </ul>
              </div>
            </div>
          </div>
          
          <router-link 
            to="/portal/login"
            class="inline-flex items-center gap-2 text-[#C9A962] hover:text-[#B8944F] transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>Volver al inicio de sesión</span>
          </router-link>
        </div>

        <!-- ===== FORMULARIO WIZARD ===== -->
        <div v-else>
          <!-- Header -->
          <div class="text-center lg:text-left mb-4 lg:mb-6">
            <h2 class="text-lg lg:text-3xl font-luxury text-text-dark mb-1 lg:mb-2">
              Solicitud de Cuenta Mayorista
            </h2>
            <p class="text-text-light text-xs lg:text-base">
              Completa el formulario para unirte a nuestra red de distribuidores
            </p>
          </div>

          <!-- Progress Steps -->
          <div class="flex items-center justify-center gap-3 lg:gap-4 mb-5 lg:mb-8">
            <div class="flex items-center gap-1.5 lg:gap-2">
              <div 
                :class="[
                  'w-6 h-6 lg:w-8 lg:h-8 rounded-full flex items-center justify-center text-xs lg:text-sm font-medium transition-colors',
                  currentStep >= 1 ? 'bg-[#C9A962] text-white' : 'bg-gray-200 text-gray-500'
                ]"
              >
                <svg v-if="currentStep > 1" class="w-3 h-3 lg:w-4 lg:h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span v-else>1</span>
              </div>
              <span :class="currentStep >= 1 ? 'text-text-dark font-medium' : 'text-text-light'" class="text-[10px] lg:text-sm hidden sm:block">
                Información Personal
              </span>
            </div>
            
            <div class="w-8 lg:w-12 h-0.5 bg-gray-200">
              <div 
                class="h-full bg-[#C9A962] transition-all duration-300"
                :style="{ width: currentStep > 1 ? '100%' : '0%' }"
              ></div>
            </div>
            
            <div class="flex items-center gap-1.5 lg:gap-2">
              <div 
                :class="[
                  'w-6 h-6 lg:w-8 lg:h-8 rounded-full flex items-center justify-center text-xs lg:text-sm font-medium transition-colors',
                  currentStep >= 2 ? 'bg-[#C9A962] text-white' : 'bg-gray-200 text-gray-500'
                ]"
              >
                2
              </div>
              <span :class="currentStep >= 2 ? 'text-text-dark font-medium' : 'text-text-light'" class="text-[10px] lg:text-sm hidden sm:block">
                Verificación de Identidad
              </span>
            </div>
          </div>

          <!-- Form -->
          <form @submit.prevent="handleSubmit">
            
            <!-- ===== PASO 1: Información Personal ===== -->
            <div v-show="currentStep === 1" class="space-y-3 lg:space-y-4">
              <div class="grid sm:grid-cols-2 gap-3 lg:gap-4">
                <div>
                  <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">Nombre *</label>
                  <input
                    v-model="form.nombre"
                    type="text"
                    required
                    placeholder="Tu nombre"
                    class="w-full px-3 py-2 lg:px-4 lg:py-3 text-sm lg:text-base bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.nombre ? 'border-red-300' : 'border-gray-200'"
                  />
                  <p v-if="errors.nombre" class="mt-1 text-xs text-red-500">{{ errors.nombre }}</p>
                </div>
                <div>
                  <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">Apellidos *</label>
                  <input
                    v-model="form.apellido"
                    type="text"
                    required
                    placeholder="Tus apellidos"
                    class="w-full px-3 py-2 lg:px-4 lg:py-3 text-sm lg:text-base bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.apellido ? 'border-red-300' : 'border-gray-200'"
                  />
                  <p v-if="errors.apellido" class="mt-1 text-xs text-red-500">{{ errors.apellido }}</p>
                </div>
              </div>

              <div>
                <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">Celular / WhatsApp *</label>
                <div class="relative">
                  <span class="absolute left-3 lg:left-4 top-1/2 -translate-y-1/2 text-gray-400 text-sm">+57</span>
                  <input
                    v-model="form.telefono"
                    type="tel"
                    required
                    placeholder="300 123 4567"
                    class="w-full px-3 py-2 lg:px-4 lg:py-3 pl-11 lg:pl-14 text-sm lg:text-base bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.telefono ? 'border-red-300' : 'border-gray-200'"
                  />
                </div>
                <p v-if="errors.telefono" class="mt-1 text-xs text-red-500">{{ errors.telefono }}</p>
              </div>

              <div>
                <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">Correo Electrónico *</label>
                <input
                  v-model="form.email"
                  type="email"
                  required
                  placeholder="tu@empresa.com"
                  class="w-full px-3 py-2 lg:px-4 lg:py-3 text-sm lg:text-base bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                  :class="errors.email ? 'border-red-300' : 'border-gray-200'"
                />
                <p v-if="errors.email" class="mt-1 text-xs text-red-500">{{ errors.email }}</p>
              </div>

              <div>
                <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">Contraseña *</label>
                <div class="relative">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    placeholder="Mínimo 8 caracteres"
                    class="w-full px-3 py-2 lg:px-4 lg:py-3 pr-10 lg:pr-12 text-sm lg:text-base bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.password ? 'border-red-300' : 'border-gray-200'"
                  />
                  <button 
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 lg:right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    <svg v-if="showPassword" class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                    <svg v-else class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                </div>
                <p v-if="errors.password" class="mt-1 text-xs text-red-500">{{ errors.password }}</p>
              </div>

              <div>
                <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">Confirmar Contraseña *</label>
                <input
                  v-model="form.passwordConfirm"
                  type="password"
                  required
                  placeholder="Repite tu contraseña"
                  class="w-full px-3 py-2 lg:px-4 lg:py-3 text-sm lg:text-base bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                  :class="errors.passwordConfirm ? 'border-red-300' : 'border-gray-200'"
                />
                <p v-if="errors.passwordConfirm" class="mt-1 text-xs text-red-500">{{ errors.passwordConfirm }}</p>
              </div>

              <!-- Botón Siguiente -->
              <button
                type="button"
                @click="nextStep"
                class="w-full py-2.5 lg:py-4 bg-[#1A1A1A] hover:bg-black text-white text-sm lg:text-base font-medium rounded-lg
                       transition-all duration-200 flex items-center justify-center gap-2 group mt-4 lg:mt-6"
              >
                <span>Siguiente</span>
                <svg class="w-4 h-4 lg:w-5 lg:h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>

            <!-- ===== PASO 2: Verificación de Identidad ===== -->
            <div v-show="currentStep === 2" class="space-y-3 lg:space-y-5">
              <!-- Tipo + Número de Documento en una fila -->
              <div>
                <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">Documento de Identidad *</label>
                <div class="flex gap-2">
                  <select
                    v-model="form.tipoDocumento"
                    class="w-20 lg:w-24 px-2 py-2 lg:px-3 lg:py-3 text-xs lg:text-sm bg-white border border-gray-200 rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                  >
                    <option value="CC">CC</option>
                    <option value="CE">CE</option>
                    <option value="NIT">NIT</option>
                    <option value="PASAPORTE">PAS</option>
                  </select>
                  <input
                    v-model="form.numeroDocumento"
                    type="text"
                    required
                    :placeholder="form.tipoDocumento === 'NIT' ? '900.123.456-7' : '123.456.789'"
                    class="flex-1 px-3 py-2 lg:px-4 lg:py-3 text-sm lg:text-base bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.numeroDocumento ? 'border-red-300' : 'border-gray-200'"
                  />
                </div>
                <p v-if="errors.numeroDocumento" class="mt-1 text-xs text-red-500">{{ errors.numeroDocumento }}</p>
              </div>

              <!-- Nombre de Empresa (Opcional) -->
              <div>
                <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">
                  Nombre de Empresa / Negocio
                  <span class="text-text-light font-normal">(opcional)</span>
                </label>
                <input
                  v-model="form.nombreEmpresa"
                  type="text"
                  placeholder="Mi Salón de Belleza S.A.S"
                  class="w-full px-3 py-2 lg:px-4 lg:py-3 text-sm lg:text-base bg-white border border-gray-200 rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                />
              </div>

              <!-- Upload Cédula Frente -->
              <div>
                <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">
                  Foto de {{ form.tipoDocumento === 'NIT' ? 'RUT' : 'Cédula' }} (Frente) *
                </label>
                
                <!-- Si ya hay preview -->
                <div v-if="previews.frente" class="border-2 border-[#C9A962] rounded-lg p-3 lg:p-4 bg-[#C9A962]/5">
                  <div class="relative inline-block w-full">
                    <img :src="previews.frente" alt="Cédula Frente" class="w-full max-h-28 lg:max-h-40 object-contain rounded-lg mx-auto" />
                    <button 
                      type="button"
                      @click.stop="removeFile('frente')"
                      class="absolute top-1 right-1 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 shadow-lg"
                    >
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  <p class="text-xs text-center text-[#C9A962] font-medium mt-2">✓ Foto capturada</p>
                </div>
                
                <!-- Si no hay preview - Botones de acción -->
                <div v-else class="flex gap-2">
                  <!-- Botón Cámara (SOLO MÓVIL) -->
                  <button
                    v-if="isMobile"
                    type="button"
                    @click="openCamera('frente')"
                    class="flex-1 border-2 border-dashed rounded-lg p-3 lg:p-4 text-center transition-all"
                    :class="errors.cedulaFrente ? 'border-red-300 bg-red-50' : 'border-gray-200 hover:border-[#C9A962] hover:bg-[#C9A962]/5'"
                  >
                    <svg class="w-6 h-6 lg:w-8 lg:h-8 mx-auto text-[#C9A962] mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <p class="text-xs lg:text-sm font-medium text-[#C9A962]">Tomar foto</p>
                  </button>
                  
                  <!-- Botón Archivo -->
                  <button
                    type="button"
                    @click="triggerFileInput('frente')"
                    class="border-2 border-dashed rounded-lg p-3 lg:p-4 text-center transition-all"
                    :class="[
                      isMobile ? 'flex-1' : 'w-full',
                      errors.cedulaFrente ? 'border-red-300 bg-red-50' : 'border-gray-200 hover:border-gray-400 hover:bg-gray-50'
                    ]"
                  >
                    <svg class="w-6 h-6 lg:w-8 lg:h-8 mx-auto text-gray-400 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <p class="text-xs lg:text-sm text-gray-500">Subir archivo</p>
                  </button>
                </div>
                
                <input 
                  ref="inputFrente"
                  type="file"
                  accept="image/*"
                  class="hidden"
                  @change="handleFileChange($event, 'frente')"
                />
                <p v-if="errors.cedulaFrente" class="mt-1 text-xs text-red-500">{{ errors.cedulaFrente }}</p>
              </div>

              <!-- Upload Cédula Dorso -->
              <div>
                <label class="block text-xs lg:text-sm font-medium text-text-dark mb-1">
                  Foto de {{ form.tipoDocumento === 'NIT' ? 'RUT' : 'Cédula' }} (Dorso) *
                </label>
                
                <!-- Si ya hay preview -->
                <div v-if="previews.dorso" class="border-2 border-[#C9A962] rounded-lg p-3 lg:p-4 bg-[#C9A962]/5">
                  <div class="relative inline-block w-full">
                    <img :src="previews.dorso" alt="Cédula Dorso" class="w-full max-h-28 lg:max-h-40 object-contain rounded-lg mx-auto" />
                    <button 
                      type="button"
                      @click.stop="removeFile('dorso')"
                      class="absolute top-1 right-1 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 shadow-lg"
                    >
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  <p class="text-xs text-center text-[#C9A962] font-medium mt-2">✓ Foto capturada</p>
                </div>
                
                <!-- Si no hay preview - Botones de acción -->
                <div v-else class="flex gap-2">
                  <!-- Botón Cámara (SOLO MÓVIL) -->
                  <button
                    v-if="isMobile"
                    type="button"
                    @click="openCamera('dorso')"
                    class="flex-1 border-2 border-dashed rounded-lg p-3 lg:p-4 text-center transition-all"
                    :class="errors.cedulaDorso ? 'border-red-300 bg-red-50' : 'border-gray-200 hover:border-[#C9A962] hover:bg-[#C9A962]/5'"
                  >
                    <svg class="w-6 h-6 lg:w-8 lg:h-8 mx-auto text-[#C9A962] mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <p class="text-xs lg:text-sm font-medium text-[#C9A962]">Tomar foto</p>
                  </button>
                  
                  <!-- Botón Archivo -->
                  <button
                    type="button"
                    @click="triggerFileInput('dorso')"
                    class="border-2 border-dashed rounded-lg p-3 lg:p-4 text-center transition-all"
                    :class="[
                      isMobile ? 'flex-1' : 'w-full',
                      errors.cedulaDorso ? 'border-red-300 bg-red-50' : 'border-gray-200 hover:border-gray-400 hover:bg-gray-50'
                    ]"
                  >
                    <svg class="w-6 h-6 lg:w-8 lg:h-8 mx-auto text-gray-400 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <p class="text-xs lg:text-sm text-gray-500">Subir archivo</p>
                  </button>
                </div>
                
                <input 
                  ref="inputDorso"
                  type="file"
                  accept="image/*"
                  class="hidden"
                  @change="handleFileChange($event, 'dorso')"
                />
                <p v-if="errors.cedulaDorso" class="mt-1 text-xs text-red-500">{{ errors.cedulaDorso }}</p>
              </div>

              <!-- Términos -->
              <div class="flex items-start gap-2 lg:gap-3 pt-1 lg:pt-2">
                <input 
                  id="terminos"
                  v-model="form.aceptaTerminos"
                  type="checkbox"
                  required
                  class="mt-0.5 w-3.5 h-3.5 lg:w-4 lg:h-4 text-[#C9A962] border-gray-300 rounded focus:ring-[#C9A962]"
                />
                <label for="terminos" class="text-[11px] lg:text-sm text-text-medium leading-tight">
                  Acepto los <a href="#" class="text-[#C9A962] hover:underline">Términos y Condiciones</a> 
                  y autorizo el tratamiento de mis datos personales según la 
                  <a href="#" class="text-[#C9A962] hover:underline">Política de Privacidad</a>
                </label>
              </div>
              <p v-if="errors.aceptaTerminos" class="text-xs text-red-500 -mt-2">{{ errors.aceptaTerminos }}</p>

              <!-- Botones -->
              <div class="flex gap-3 lg:gap-4 pt-2 lg:pt-4">
                <button
                  type="button"
                  @click="prevStep"
                  class="flex-1 py-2.5 lg:py-4 border border-gray-300 text-text-dark text-sm lg:text-base font-medium rounded-lg
                         hover:bg-gray-50 transition-all duration-200 flex items-center justify-center gap-1.5 lg:gap-2"
                >
                  <svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  <span>Atrás</span>
                </button>
                
                <button
                  type="submit"
                  :disabled="loading"
                  class="flex-1 py-2.5 lg:py-4 bg-[#C9A962] hover:bg-[#B8944F] text-white text-sm lg:text-base font-medium rounded-lg
                         transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                         flex items-center justify-center gap-1.5 lg:gap-2"
                >
                  <svg v-if="loading" class="w-4 h-4 lg:w-5 lg:h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{{ loading ? 'Enviando...' : 'Enviar Solicitud' }}</span>
                </button>
              </div>
            </div>
          </form>

          <!-- Link Login -->
          <div class="mt-5 lg:mt-8 pt-4 lg:pt-6 border-t border-gray-100 text-center">
            <p class="text-text-medium text-xs lg:text-sm">
              ¿Ya tienes cuenta? 
              <router-link to="/portal/login" class="text-[#C9A962] hover:underline font-medium">
                Inicia sesión
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- =========================================================================
         MODAL DE CÁMARA PROFESIONAL (estilo ML/Nequi)
    ========================================================================== -->
    <Teleport to="body">
      <Transition name="camera-modal">
        <div 
          v-if="camera.show" 
          class="fixed inset-0 z-[100] bg-black flex flex-col"
        >
          <!-- Header de la cámara -->
          <div class="relative z-20 flex items-center justify-between p-4 bg-gradient-to-b from-black/80 to-transparent">
            <button 
              @click="closeCamera"
              class="w-10 h-10 flex items-center justify-center text-white"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <span class="text-white font-medium text-sm">
              {{ camera.type === 'frente' ? 'Parte frontal del documento' : 'Parte trasera del documento' }}
            </span>
            <div class="w-10"></div>
          </div>

          <!-- Área del video con overlay -->
          <div class="flex-1 relative overflow-hidden flex items-center justify-center">
            <!-- Video de la cámara -->
            <video 
              ref="videoRef"
              autoplay 
              playsinline
              class="absolute inset-0 w-full h-full object-cover"
              :class="{ 'camera-filter': camera.enhanceMode }"
            ></video>
            
            <!-- Canvas oculto para captura -->
            <canvas ref="canvasRef" class="hidden"></canvas>
            
            <!-- Overlay con marco guía (solo cuando la cámara está activa) -->
            <div v-if="camera.isStreaming && !camera.captured" class="absolute inset-0 pointer-events-none">
              <!-- Oscurecer áreas fuera del marco -->
              <div class="absolute inset-0 bg-black/50"></div>
              
              <!-- Marco del documento (área clara) -->
              <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[85%] max-w-md aspect-[1.6/1]">
                <!-- Recorte transparente -->
                <div class="absolute inset-0 bg-black/50" style="box-shadow: 0 0 0 100vmax rgba(0,0,0,0.5);"></div>
                
                <!-- Marco con esquinas decorativas -->
                <div class="absolute inset-0 border-2 border-white/80 rounded-xl">
                  <!-- Esquinas animadas -->
                  <div class="absolute -top-0.5 -left-0.5 w-6 h-6 border-t-4 border-l-4 border-[#C9A962] rounded-tl-xl"></div>
                  <div class="absolute -top-0.5 -right-0.5 w-6 h-6 border-t-4 border-r-4 border-[#C9A962] rounded-tr-xl"></div>
                  <div class="absolute -bottom-0.5 -left-0.5 w-6 h-6 border-b-4 border-l-4 border-[#C9A962] rounded-bl-xl"></div>
                  <div class="absolute -bottom-0.5 -right-0.5 w-6 h-6 border-b-4 border-r-4 border-[#C9A962] rounded-br-xl"></div>
                </div>
                
                <!-- Texto guía -->
                <div class="absolute -bottom-12 left-0 right-0 text-center">
                  <p class="text-white text-sm font-medium">Coloca tu documento dentro del marco</p>
                  <p class="text-white/60 text-xs mt-1">Asegúrate de que esté bien iluminado</p>
                </div>
              </div>
            </div>
            
            <!-- Preview de captura -->
            <div v-if="camera.captured" class="absolute inset-0 flex items-center justify-center bg-black">
              <img 
                :src="camera.capturedImage" 
                alt="Foto capturada" 
                class="max-w-full max-h-full object-contain"
                :class="{ 'camera-filter': camera.enhanceMode }"
              />
            </div>
            
            <!-- Mensaje de cargando -->
            <div v-if="camera.loading" class="absolute inset-0 flex items-center justify-center bg-black/70 z-30">
              <div class="text-center">
                <svg class="w-12 h-12 mx-auto animate-spin text-[#C9A962]" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p class="text-white mt-3 text-sm">Procesando imagen...</p>
              </div>
            </div>
            
            <!-- Error de cámara -->
            <div v-if="camera.error" class="absolute inset-0 flex items-center justify-center bg-black z-30 p-6">
              <div class="text-center">
                <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <p class="text-white font-medium mb-2">No se pudo acceder a la cámara</p>
                <p class="text-white/60 text-sm mb-6">{{ camera.error }}</p>
                <button 
                  @click="closeCamera"
                  class="px-6 py-2.5 bg-white text-black rounded-lg font-medium"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>

          <!-- Controles de la cámara -->
          <div class="relative z-20 p-6 pb-8 bg-gradient-to-t from-black via-black/90 to-transparent">
            <!-- Toggle de filtro de mejora -->
            <div class="flex justify-center mb-4">
              <button 
                @click="camera.enhanceMode = !camera.enhanceMode"
                class="flex items-center gap-2 px-4 py-2 rounded-full transition-colors"
                :class="camera.enhanceMode ? 'bg-[#C9A962] text-white' : 'bg-white/20 text-white'"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <span class="text-xs font-medium">Mejorar nitidez</span>
              </button>
            </div>
            
            <!-- Botones de acción -->
            <div class="flex items-center justify-center gap-8">
              <!-- Si no hay captura -->
              <template v-if="!camera.captured">
                <!-- Botón capturar -->
                <button 
                  @click="capturePhoto"
                  :disabled="!camera.isStreaming || camera.loading"
                  class="w-16 h-16 rounded-full bg-white flex items-center justify-center disabled:opacity-50 transition-transform active:scale-95"
                >
                  <div class="w-14 h-14 rounded-full border-4 border-black/20"></div>
                </button>
              </template>
              
              <!-- Si ya hay captura - botones retomar/usar -->
              <template v-else>
                <button 
                  @click="retakePhoto"
                  class="flex-1 max-w-[140px] py-3 border-2 border-white text-white rounded-lg font-medium transition-colors hover:bg-white/10"
                >
                  Retomar
                </button>
                <button 
                  @click="usePhoto"
                  class="flex-1 max-w-[140px] py-3 bg-[#C9A962] text-white rounded-lg font-medium transition-colors hover:bg-[#B8944F]"
                >
                  Usar foto
                </button>
              </template>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- =========================================================================
         MODAL DE ESTADO (Cuenta en revisión, rechazada, etc.)
    ========================================================================== -->
    <Teleport to="body">
      <Transition name="modal">
        <div 
          v-if="statusModal.show" 
          class="fixed inset-0 z-50 flex items-center justify-center p-4"
        >
          <!-- Backdrop -->
          <div 
            class="absolute inset-0 bg-black/50"
            @click="closeStatusModal"
          ></div>
          
          <!-- Modal Content -->
          <div class="relative bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 text-center transform transition-all">
            <!-- Icono según estado -->
            <div 
              class="w-20 h-20 mx-auto mb-6 rounded-full flex items-center justify-center"
              :class="{
                'bg-amber-100': statusModal.status === 'pending' || statusModal.status === 'reviewing',
                'bg-green-100': statusModal.status === 'approved',
                'bg-red-100': statusModal.status === 'rejected' || statusModal.status === 'suspended',
                'bg-blue-100': statusModal.status === 'exists'
              }"
            >
              <!-- Clock (Pendiente) -->
              <svg v-if="statusModal.icon === 'clock'" class="w-10 h-10 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <!-- Search (En revisión) -->
              <svg v-else-if="statusModal.icon === 'search'" class="w-10 h-10 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <!-- Check (Aprobado) -->
              <svg v-else-if="statusModal.icon === 'check'" class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <!-- X (Rechazado) -->
              <svg v-else-if="statusModal.icon === 'x'" class="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <!-- Pause (Suspendido) -->
              <svg v-else-if="statusModal.icon === 'pause'" class="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <!-- User (Ya existe) -->
              <svg v-else class="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            
            <!-- Título -->
            <h3 class="text-xl font-luxury text-text-dark mb-3">
              {{ statusModal.title }}
            </h3>
            
            <!-- Mensaje -->
            <p class="text-text-medium mb-8 leading-relaxed">
              {{ statusModal.message }}
            </p>
            
            <!-- Botones -->
            <div class="flex flex-col sm:flex-row gap-3 justify-center">
              <!-- Botón de acción (si hay) -->
              <button 
                v-if="statusModal.action"
                @click="handleModalAction"
                class="px-6 py-3 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-lg transition-colors"
              >
                {{ statusModal.action === 'login' ? 'Iniciar sesión' : 'Contactar soporte' }}
              </button>
              
              <!-- Botón cerrar -->
              <button 
                @click="closeStatusModal"
                class="px-6 py-3 border border-gray-300 text-text-dark font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                {{ statusModal.action ? 'Cerrar' : 'Entendido' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'B2BRegistro',
  setup() {
    const router = useRouter()
    
    // =========================================================================
    // STATE
    // =========================================================================
    const currentStep = ref(1)
    const loading = ref(false)
    const submitted = ref(false)
    const showPassword = ref(false)
    const dragOver = ref(null)
    
    // Modal de estado (para mostrar mensajes elegantes)
    const statusModal = ref({
      show: false,
      status: '',
      title: '',
      message: '',
      icon: '',
      action: null
    })
    
    const inputFrente = ref(null)
    const inputDorso = ref(null)
    
    // Detección de dispositivo móvil
    const isMobile = ref(false)
    if (typeof window !== 'undefined') {
      isMobile.value = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) 
        || (navigator.maxTouchPoints && navigator.maxTouchPoints > 2)
    }
    
    // Refs para la cámara
    const videoRef = ref(null)
    const canvasRef = ref(null)
    
    // Estado de la cámara profesional
    const camera = ref({
      show: false,
      type: null, // 'frente' o 'dorso'
      isStreaming: false,
      loading: false,
      error: null,
      captured: false,
      capturedImage: null,
      enhanceMode: true, // Filtro de mejora activado por defecto
      stream: null
    })
    
    const form = reactive({
      // Paso 1
      nombre: '',
      apellido: '',
      telefono: '',
      email: '',
      password: '',
      passwordConfirm: '',
      // Paso 2
      tipoDocumento: 'CC',
      numeroDocumento: '',
      nombreEmpresa: '',
      cedulaFrente: null,
      cedulaDorso: null,
      aceptaTerminos: false
    })
    
    const previews = reactive({
      frente: null,
      dorso: null
    })
    
    const errors = reactive({})
    
    // =========================================================================
    // MODAL METHODS
    // =========================================================================
    function closeStatusModal() {
      statusModal.value.show = false
    }
    
    function handleModalAction() {
      const action = statusModal.value.action
      closeStatusModal()
      
      if (action === 'login') {
        router.push('/portal/login')
      } else if (action === 'support') {
        // Abrir WhatsApp de soporte
        window.open('https://wa.me/4796657763?text=Hola, necesito ayuda con mi cuenta mayorista', '_blank')
      }
    }

    // =========================================================================
    // METHODS
    // =========================================================================
    
    function clearErrors() {
      Object.keys(errors).forEach(key => delete errors[key])
    }
    
    function validateStep1() {
      clearErrors()
      let isValid = true
      
      if (!form.nombre.trim()) {
        errors.nombre = 'El nombre es requerido'
        isValid = false
      }
      
      if (!form.apellido.trim()) {
        errors.apellido = 'Los apellidos son requeridos'
        isValid = false
      }
      
      if (!form.telefono.trim()) {
        errors.telefono = 'El teléfono es requerido'
        isValid = false
      } else if (!/^\d{10}$/.test(form.telefono.replace(/\s/g, ''))) {
        errors.telefono = 'Ingresa un número de 10 dígitos'
        isValid = false
      }
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!form.email.trim()) {
        errors.email = 'El correo es requerido'
        isValid = false
      } else if (!emailRegex.test(form.email)) {
        errors.email = 'Ingresa un correo válido'
        isValid = false
      }
      
      if (!form.password) {
        errors.password = 'La contraseña es requerida'
        isValid = false
      } else if (form.password.length < 8) {
        errors.password = 'Mínimo 8 caracteres'
        isValid = false
      }
      
      if (form.password !== form.passwordConfirm) {
        errors.passwordConfirm = 'Las contraseñas no coinciden'
        isValid = false
      }
      
      return isValid
    }
    
    function validateStep2() {
      clearErrors()
      let isValid = true
      
      if (!form.numeroDocumento.trim()) {
        errors.numeroDocumento = 'El número de documento es requerido'
        isValid = false
      }
      
      if (!form.cedulaFrente) {
        errors.cedulaFrente = 'La foto del frente es requerida'
        isValid = false
      }
      
      if (!form.cedulaDorso) {
        errors.cedulaDorso = 'La foto del dorso es requerida'
        isValid = false
      }
      
      if (!form.aceptaTerminos) {
        errors.aceptaTerminos = 'Debes aceptar los términos'
        isValid = false
      }
      
      return isValid
    }
    
    async function nextStep() {
      if (!validateStep1()) return
      
      // Verificar si el email ya existe en el backend
      loading.value = true
      
      try {
        const API_BASE = import.meta.env.VITE_API_URL?.replace('/api/v1', '') || 'http://localhost:8000'
        
        const response = await fetch(`${API_BASE}/api/v1/mayoristas/verificar-email`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: form.email })
        })
        
        const data = await response.json()
        
        if (data.exists) {
          // Mostrar modal con el estado
          statusModal.value = {
            show: true,
            status: data.status,
            title: data.title,
            message: data.message,
            icon: data.icon,
            action: data.action || null
          }
          return
        }
        
        // Si no existe, continuar al paso 2
        currentStep.value = 2
        window.scrollTo({ top: 0, behavior: 'smooth' })
        
      } catch (err) {
        console.error('Error al verificar email:', err)
        // Si hay error de red, continuar de todos modos (el backend validará al enviar)
        currentStep.value = 2
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } finally {
        loading.value = false
      }
    }
    
    function prevStep() {
      currentStep.value = 1
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
    
    function triggerFileInput(type) {
      if (type === 'frente') {
        inputFrente.value?.click()
      } else {
        inputDorso.value?.click()
      }
    }
    
    function handleFileChange(event, type) {
      const file = event.target.files[0]
      if (file) {
        processFile(file, type)
      }
    }
    
    function handleDrop(event, type) {
      dragOver.value = null
      const file = event.dataTransfer.files[0]
      if (file && file.type.startsWith('image/')) {
        processFile(file, type)
      }
    }
    
    function processFile(file, type) {
      // Validar tamaño (5MB max)
      if (file.size > 5 * 1024 * 1024) {
        errors[type === 'frente' ? 'cedulaFrente' : 'cedulaDorso'] = 'El archivo no puede superar 5MB'
        return
      }
      
      // Guardar archivo
      if (type === 'frente') {
        form.cedulaFrente = file
        delete errors.cedulaFrente
      } else {
        form.cedulaDorso = file
        delete errors.cedulaDorso
      }
      
      // Crear preview
      const reader = new FileReader()
      reader.onload = (e) => {
        previews[type] = e.target.result
      }
      reader.readAsDataURL(file)
    }
    
    function removeFile(type) {
      if (type === 'frente') {
        form.cedulaFrente = null
        previews.frente = null
        if (inputFrente.value) inputFrente.value.value = ''
      } else {
        form.cedulaDorso = null
        previews.dorso = null
        if (inputDorso.value) inputDorso.value.value = ''
      }
    }
    
    // =========================================================================
    // CAMERA METHODS (Profesional estilo ML/Nequi)
    // =========================================================================
    
    async function openCamera(type) {
      camera.value = {
        show: true,
        type: type,
        isStreaming: false,
        loading: true,
        error: null,
        captured: false,
        capturedImage: null,
        enhanceMode: true,
        stream: null
      }
      
      // Esperar a que el video ref esté disponible
      await new Promise(resolve => setTimeout(resolve, 100))
      
      try {
        // Solicitar acceso a la cámara (preferir trasera en móviles)
        const stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: { ideal: 'environment' }, // Cámara trasera
            width: { ideal: 1920 },
            height: { ideal: 1080 }
          },
          audio: false
        })
        
        camera.value.stream = stream
        
        if (videoRef.value) {
          videoRef.value.srcObject = stream
          videoRef.value.onloadedmetadata = () => {
            camera.value.isStreaming = true
            camera.value.loading = false
          }
        }
      } catch (err) {
        console.error('Error al acceder a la cámara:', err)
        camera.value.loading = false
        
        if (err.name === 'NotAllowedError') {
          camera.value.error = 'Permiso de cámara denegado. Por favor, permite el acceso a la cámara en la configuración de tu navegador.'
        } else if (err.name === 'NotFoundError') {
          camera.value.error = 'No se encontró ninguna cámara en tu dispositivo.'
        } else {
          camera.value.error = 'Error al iniciar la cámara. Intenta subir la imagen manualmente.'
        }
      }
    }
    
    function closeCamera() {
      // Detener el stream de la cámara
      if (camera.value.stream) {
        camera.value.stream.getTracks().forEach(track => track.stop())
      }
      camera.value.show = false
    }
    
    function capturePhoto() {
      if (!videoRef.value || !canvasRef.value) return
      
      const video = videoRef.value
      const canvas = canvasRef.value
      const ctx = canvas.getContext('2d')
      
      // Configurar el canvas con las dimensiones del video
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      
      // Dibujar el frame actual del video
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      
      // Aplicar filtros de mejora si está activado
      if (camera.value.enhanceMode) {
        applyEnhanceFilter(ctx, canvas.width, canvas.height)
      }
      
      // Convertir a imagen
      const imageData = canvas.toDataURL('image/jpeg', 0.92)
      
      camera.value.captured = true
      camera.value.capturedImage = imageData
    }
    
    function applyEnhanceFilter(ctx, width, height) {
      // Obtener los datos de la imagen
      const imageData = ctx.getImageData(0, 0, width, height)
      const data = imageData.data
      
      // Aplicar mejoras para documentos:
      // - Aumentar contraste
      // - Aumentar brillo ligeramente
      // - Sharpening sutil
      
      const contrast = 1.15 // 15% más contraste
      const brightness = 10 // Un poco más de brillo
      
      for (let i = 0; i < data.length; i += 4) {
        // Aplicar contraste y brillo
        data[i] = Math.min(255, Math.max(0, ((data[i] - 128) * contrast) + 128 + brightness))     // R
        data[i+1] = Math.min(255, Math.max(0, ((data[i+1] - 128) * contrast) + 128 + brightness)) // G
        data[i+2] = Math.min(255, Math.max(0, ((data[i+2] - 128) * contrast) + 128 + brightness)) // B
      }
      
      ctx.putImageData(imageData, 0, 0)
    }
    
    function retakePhoto() {
      camera.value.captured = false
      camera.value.capturedImage = null
    }
    
    function usePhoto() {
      if (!camera.value.capturedImage) return
      
      // Convertir base64 a File
      const blob = dataURLtoBlob(camera.value.capturedImage)
      const timestamp = Date.now()
      const file = new File([blob], `documento_${camera.value.type}_${timestamp}.jpg`, { type: 'image/jpeg' })
      
      // Guardar en el formulario
      if (camera.value.type === 'frente') {
        form.cedulaFrente = file
        previews.frente = camera.value.capturedImage
        delete errors.cedulaFrente
      } else {
        form.cedulaDorso = file
        previews.dorso = camera.value.capturedImage
        delete errors.cedulaDorso
      }
      
      // Cerrar la cámara
      closeCamera()
    }
    
    function dataURLtoBlob(dataURL) {
      const parts = dataURL.split(',')
      const mime = parts[0].match(/:(.*?);/)[1]
      const bstr = atob(parts[1])
      let n = bstr.length
      const u8arr = new Uint8Array(n)
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n)
      }
      return new Blob([u8arr], { type: mime })
    }
    
    async function handleSubmit() {
      if (!validateStep2()) return
      
      loading.value = true
      
      try {
        const API_BASE = import.meta.env.VITE_API_URL?.replace('/api/v1', '') || 'http://localhost:8000'
        
        // Usar FormData para enviar archivos
        const formData = new FormData()
        formData.append('email', form.email)
        formData.append('password', form.password)
        formData.append('nombre', form.nombre)
        formData.append('apellido', form.apellido)
        formData.append('telefono', form.telefono)
        formData.append('tipo_documento', form.tipoDocumento)
        formData.append('numero_documento', form.numeroDocumento)
        formData.append('nombre_empresa', form.nombreEmpresa)
        formData.append('nit_empresa', form.nitEmpresa || '')
        
        // Agregar archivos de cédula si existen
        if (form.cedulaFrente) {
          formData.append('cedula_frente', form.cedulaFrente)
        }
        if (form.cedulaDorso) {
          formData.append('cedula_dorso', form.cedulaDorso)
        }
        
        // Enviar datos al backend (sin Content-Type, el browser lo pone automáticamente)
        const response = await fetch(`${API_BASE}/api/v1/mayoristas/registro`, {
          method: 'POST',
          body: formData
        })
        
        const data = await response.json()
        
        if (!response.ok) {
          throw new Error(data.detail || 'Error al registrar')
        }
        
        console.log('✅ Mayorista registrado:', data)
        
        // Mostrar estado de éxito
        submitted.value = true
        
      } catch (err) {
        console.error('Error al enviar solicitud:', err)
        alert(err.message || 'Error al enviar la solicitud. Intenta nuevamente.')
      } finally {
        loading.value = false
      }
    }

    // =========================================================================
    // RETURN
    // =========================================================================
    return {
      currentStep,
      loading,
      submitted,
      showPassword,
      dragOver,
      inputFrente,
      inputDorso,
      isMobile,
      videoRef,
      canvasRef,
      camera,
      form,
      previews,
      errors,
      statusModal,
      nextStep,
      prevStep,
      triggerFileInput,
      handleFileChange,
      handleDrop,
      removeFile,
      handleSubmit,
      closeStatusModal,
      handleModalAction,
      openCamera,
      closeCamera,
      capturePhoto,
      retakePhoto,
      usePhoto
    }
  }
}
</script>

<style scoped>
/* Checkbox personalizado */
input[type="checkbox"]:checked {
  background-color: #C9A962;
  border-color: #C9A962;
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95) translateY(10px);
}

/* Camera modal transitions */
.camera-modal-enter-active,
.camera-modal-leave-active {
  transition: all 0.3s ease;
}

.camera-modal-enter-from,
.camera-modal-leave-to {
  opacity: 0;
  transform: translateY(100%);
}

/* Filtro de mejora para documentos */
.camera-filter {
  filter: contrast(1.1) brightness(1.05) saturate(0.9);
}
</style>
