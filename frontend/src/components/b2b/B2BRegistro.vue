<template>
  <div class="min-h-screen flex flex-col lg:flex-row">
    <!-- =========================================================================
         LADO IZQUIERDO - Branding (igual que login)
    ========================================================================== -->
    <div class="relative lg:w-5/12 h-48 sm:h-64 lg:h-screen overflow-hidden">
      <!-- Gradient de fondo -->
      <div class="absolute inset-0 bg-gradient-to-br from-[#1A1A1A] via-[#2D2D2D] to-[#1A1A1A]"></div>
      
      <!-- Patrón decorativo -->
      <div class="absolute inset-0 opacity-5">
        <div class="absolute inset-0" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23C9A962\' fill-opacity=\'0.4\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>
      
      <!-- Overlay -->
      <div class="absolute inset-0 bg-black/40"></div>
      
      <!-- Contenido -->
      <div class="relative z-10 h-full flex flex-col justify-between p-6 sm:p-8 lg:p-12">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 lg:w-12 lg:h-12 rounded-full bg-white/10 p-2 flex items-center justify-center">
            <img src="/logo-kharis.png" alt="Kharis" class="w-full h-full object-contain" />
          </div>
          <div>
            <span class="text-[#C9A962] font-luxury text-lg lg:text-xl tracking-wider">KHARIS</span>
            <span class="text-white/60 text-xs lg:text-sm block -mt-1">PRO</span>
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
    <div class="flex-1 lg:w-7/12 flex items-center justify-center bg-[#FAFAFA] p-6 sm:p-8 lg:p-12 overflow-y-auto">
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
          <div class="text-center lg:text-left mb-6">
            <h2 class="text-2xl lg:text-3xl font-luxury text-text-dark mb-2">
              Solicitud de Cuenta Mayorista
            </h2>
            <p class="text-text-light">
              Completa el formulario para unirte a nuestra red de distribuidores
            </p>
          </div>

          <!-- Progress Steps -->
          <div class="flex items-center justify-center gap-4 mb-8">
            <div class="flex items-center gap-2">
              <div 
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors',
                  currentStep >= 1 ? 'bg-[#C9A962] text-white' : 'bg-gray-200 text-gray-500'
                ]"
              >
                <svg v-if="currentStep > 1" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span v-else>1</span>
              </div>
              <span :class="currentStep >= 1 ? 'text-text-dark font-medium' : 'text-text-light'" class="text-sm hidden sm:block">
                Información Personal
              </span>
            </div>
            
            <div class="w-12 h-0.5 bg-gray-200">
              <div 
                class="h-full bg-[#C9A962] transition-all duration-300"
                :style="{ width: currentStep > 1 ? '100%' : '0%' }"
              ></div>
            </div>
            
            <div class="flex items-center gap-2">
              <div 
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors',
                  currentStep >= 2 ? 'bg-[#C9A962] text-white' : 'bg-gray-200 text-gray-500'
                ]"
              >
                2
              </div>
              <span :class="currentStep >= 2 ? 'text-text-dark font-medium' : 'text-text-light'" class="text-sm hidden sm:block">
                Verificación de Identidad
              </span>
            </div>
          </div>

          <!-- Form -->
          <form @submit.prevent="handleSubmit">
            
            <!-- ===== PASO 1: Información Personal ===== -->
            <div v-show="currentStep === 1" class="space-y-4">
              <div class="grid sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-text-dark mb-1.5">Nombre *</label>
                  <input
                    v-model="form.nombre"
                    type="text"
                    required
                    placeholder="Tu nombre"
                    class="w-full px-4 py-3 bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.nombre ? 'border-red-300' : 'border-gray-200'"
                  />
                  <p v-if="errors.nombre" class="mt-1 text-sm text-red-500">{{ errors.nombre }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-text-dark mb-1.5">Apellidos *</label>
                  <input
                    v-model="form.apellido"
                    type="text"
                    required
                    placeholder="Tus apellidos"
                    class="w-full px-4 py-3 bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.apellido ? 'border-red-300' : 'border-gray-200'"
                  />
                  <p v-if="errors.apellido" class="mt-1 text-sm text-red-500">{{ errors.apellido }}</p>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">Celular / WhatsApp *</label>
                <div class="relative">
                  <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">+57</span>
                  <input
                    v-model="form.telefono"
                    type="tel"
                    required
                    placeholder="300 123 4567"
                    class="w-full px-4 py-3 pl-14 bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.telefono ? 'border-red-300' : 'border-gray-200'"
                  />
                </div>
                <p v-if="errors.telefono" class="mt-1 text-sm text-red-500">{{ errors.telefono }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">Correo Electrónico *</label>
                <input
                  v-model="form.email"
                  type="email"
                  required
                  placeholder="tu@empresa.com"
                  class="w-full px-4 py-3 bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                  :class="errors.email ? 'border-red-300' : 'border-gray-200'"
                />
                <p v-if="errors.email" class="mt-1 text-sm text-red-500">{{ errors.email }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">Contraseña *</label>
                <div class="relative">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    placeholder="Mínimo 8 caracteres"
                    class="w-full px-4 py-3 pr-12 bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                    :class="errors.password ? 'border-red-300' : 'border-gray-200'"
                  />
                  <button 
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                </div>
                <p v-if="errors.password" class="mt-1 text-sm text-red-500">{{ errors.password }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">Confirmar Contraseña *</label>
                <input
                  v-model="form.passwordConfirm"
                  type="password"
                  required
                  placeholder="Repite tu contraseña"
                  class="w-full px-4 py-3 bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                  :class="errors.passwordConfirm ? 'border-red-300' : 'border-gray-200'"
                />
                <p v-if="errors.passwordConfirm" class="mt-1 text-sm text-red-500">{{ errors.passwordConfirm }}</p>
              </div>

              <!-- Botón Siguiente -->
              <button
                type="button"
                @click="nextStep"
                class="w-full py-4 bg-[#1A1A1A] hover:bg-black text-white font-medium rounded-lg
                       transition-all duration-200 flex items-center justify-center gap-2 group mt-6"
              >
                <span>Siguiente</span>
                <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>

            <!-- ===== PASO 2: Verificación de Identidad ===== -->
            <div v-show="currentStep === 2" class="space-y-5">
              <!-- Tipo de Documento -->
              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">Tipo de Documento *</label>
                <select
                  v-model="form.tipoDocumento"
                  class="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                >
                  <option value="CC">Cédula de Ciudadanía</option>
                  <option value="CE">Cédula de Extranjería</option>
                  <option value="NIT">NIT (Empresa)</option>
                  <option value="PASAPORTE">Pasaporte</option>
                </select>
              </div>

              <!-- Número de Documento -->
              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">
                  {{ form.tipoDocumento === 'NIT' ? 'NIT' : 'Número de Documento' }} *
                </label>
                <input
                  v-model="form.numeroDocumento"
                  type="text"
                  required
                  :placeholder="form.tipoDocumento === 'NIT' ? '900.123.456-7' : '1.234.567.890'"
                  class="w-full px-4 py-3 bg-white border rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                  :class="errors.numeroDocumento ? 'border-red-300' : 'border-gray-200'"
                />
                <p v-if="errors.numeroDocumento" class="mt-1 text-sm text-red-500">{{ errors.numeroDocumento }}</p>
              </div>

              <!-- Nombre de Empresa (Opcional) -->
              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">
                  Nombre de Empresa / Negocio
                  <span class="text-text-light font-normal">(opcional)</span>
                </label>
                <input
                  v-model="form.nombreEmpresa"
                  type="text"
                  placeholder="Mi Salón de Belleza S.A.S"
                  class="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#C9A962]/20 focus:border-[#C9A962]"
                />
              </div>

              <!-- Upload Cédula Frente -->
              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">
                  Foto de {{ form.tipoDocumento === 'NIT' ? 'RUT' : 'Cédula' }} (Frente) *
                </label>
                <div 
                  @click="triggerFileInput('frente')"
                  @dragover.prevent="dragOver = 'frente'"
                  @dragleave="dragOver = null"
                  @drop.prevent="handleDrop($event, 'frente')"
                  :class="[
                    'border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all',
                    dragOver === 'frente' ? 'border-[#C9A962] bg-[#C9A962]/5' : 
                    errors.cedulaFrente ? 'border-red-300 bg-red-50' : 'border-gray-200 hover:border-[#C9A962]/50 hover:bg-gray-50'
                  ]"
                >
                  <!-- Preview si hay imagen -->
                  <div v-if="previews.frente" class="relative inline-block">
                    <img :src="previews.frente" alt="Cédula Frente" class="max-h-32 rounded-lg mx-auto" />
                    <button 
                      type="button"
                      @click.stop="removeFile('frente')"
                      class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                    <p class="text-sm text-text-medium mt-2">{{ form.cedulaFrente?.name }}</p>
                  </div>
                  
                  <!-- Estado vacío -->
                  <div v-else>
                    <svg class="w-10 h-10 mx-auto text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <p class="text-sm text-text-medium">
                      <span class="text-[#C9A962] font-medium">Haz clic para subir</span> o arrastra aquí
                    </p>
                    <p class="text-xs text-text-light mt-1">PNG, JPG hasta 5MB</p>
                  </div>
                </div>
                <input 
                  ref="inputFrente"
                  type="file"
                  accept="image/*"
                  class="hidden"
                  @change="handleFileChange($event, 'frente')"
                />
                <p v-if="errors.cedulaFrente" class="mt-1 text-sm text-red-500">{{ errors.cedulaFrente }}</p>
              </div>

              <!-- Upload Cédula Dorso -->
              <div>
                <label class="block text-sm font-medium text-text-dark mb-1.5">
                  Foto de {{ form.tipoDocumento === 'NIT' ? 'RUT' : 'Cédula' }} (Dorso) *
                </label>
                <div 
                  @click="triggerFileInput('dorso')"
                  @dragover.prevent="dragOver = 'dorso'"
                  @dragleave="dragOver = null"
                  @drop.prevent="handleDrop($event, 'dorso')"
                  :class="[
                    'border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all',
                    dragOver === 'dorso' ? 'border-[#C9A962] bg-[#C9A962]/5' : 
                    errors.cedulaDorso ? 'border-red-300 bg-red-50' : 'border-gray-200 hover:border-[#C9A962]/50 hover:bg-gray-50'
                  ]"
                >
                  <!-- Preview si hay imagen -->
                  <div v-if="previews.dorso" class="relative inline-block">
                    <img :src="previews.dorso" alt="Cédula Dorso" class="max-h-32 rounded-lg mx-auto" />
                    <button 
                      type="button"
                      @click.stop="removeFile('dorso')"
                      class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                    <p class="text-sm text-text-medium mt-2">{{ form.cedulaDorso?.name }}</p>
                  </div>
                  
                  <!-- Estado vacío -->
                  <div v-else>
                    <svg class="w-10 h-10 mx-auto text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <p class="text-sm text-text-medium">
                      <span class="text-[#C9A962] font-medium">Haz clic para subir</span> o arrastra aquí
                    </p>
                    <p class="text-xs text-text-light mt-1">PNG, JPG hasta 5MB</p>
                  </div>
                </div>
                <input 
                  ref="inputDorso"
                  type="file"
                  accept="image/*"
                  class="hidden"
                  @change="handleFileChange($event, 'dorso')"
                />
                <p v-if="errors.cedulaDorso" class="mt-1 text-sm text-red-500">{{ errors.cedulaDorso }}</p>
              </div>

              <!-- Términos -->
              <div class="flex items-start gap-3 pt-2">
                <input 
                  id="terminos"
                  v-model="form.aceptaTerminos"
                  type="checkbox"
                  required
                  class="mt-1 w-4 h-4 text-[#C9A962] border-gray-300 rounded focus:ring-[#C9A962]"
                />
                <label for="terminos" class="text-sm text-text-medium">
                  Acepto los <a href="#" class="text-[#C9A962] hover:underline">Términos y Condiciones</a> 
                  y autorizo el tratamiento de mis datos personales según la 
                  <a href="#" class="text-[#C9A962] hover:underline">Política de Privacidad</a>
                </label>
              </div>
              <p v-if="errors.aceptaTerminos" class="text-sm text-red-500 -mt-3">{{ errors.aceptaTerminos }}</p>

              <!-- Botones -->
              <div class="flex gap-4 pt-4">
                <button
                  type="button"
                  @click="prevStep"
                  class="flex-1 py-4 border border-gray-300 text-text-dark font-medium rounded-lg
                         hover:bg-gray-50 transition-all duration-200 flex items-center justify-center gap-2"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  <span>Atrás</span>
                </button>
                
                <button
                  type="submit"
                  :disabled="loading"
                  class="flex-1 py-4 bg-[#C9A962] hover:bg-[#B8944F] text-white font-medium rounded-lg
                         transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
                         flex items-center justify-center gap-2"
                >
                  <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{{ loading ? 'Enviando...' : 'Enviar Solicitud' }}</span>
                </button>
              </div>
            </div>
          </form>

          <!-- Link Login -->
          <div class="mt-8 pt-6 border-t border-gray-100 text-center">
            <p class="text-text-medium text-sm">
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
      handleModalAction
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
</style>
