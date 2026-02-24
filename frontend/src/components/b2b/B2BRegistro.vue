<template>
  <div class="b2b-registro-screen min-h-screen flex flex-col lg:flex-row overflow-hidden">
    <!-- =========================================================================
         LADO IZQUIERDO - Branding (igual que login)
    ========================================================================== -->
    <div class="relative lg:w-5/12 lg:h-screen overflow-hidden">
      <!-- Gradient mobile: femenino y elegante / Desktop: oscuro profesional -->
      <div class="absolute inset-0 bg-gradient-to-b from-[#F5EBE5] via-[#FAF5F2] to-[#FDF8F6] lg:bg-gradient-to-br lg:from-[#1A1A1A] lg:via-[#2D2D2D] lg:to-[#1A1A1A]"></div>
      
      <!-- Patrón decorativo (solo desktop) -->
      <div class="absolute inset-0 opacity-5 hidden lg:block">
        <div class="absolute inset-0" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23C9A962\' fill-opacity=\'0.4\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
      </div>
      
      <!-- Overlay (solo desktop) -->
      <div class="absolute inset-0 bg-black/40 hidden lg:block"></div>
      
      <!-- Contenido -->
      <div class="relative z-10 h-full flex flex-col justify-between p-5 pb-6 lg:p-12">
        <!-- Logo móvil: centrado, estilo app femenino -->
        <div class="flex flex-col items-center gap-3 pt-3 lg:hidden">
          <div class="w-[72px] h-[72px] rounded-[22px] bg-white/90 shadow-md shadow-[#D4B29E]/15 p-3.5 flex items-center justify-center">
            <img src="/logo-kharis.png" alt="Kharis" class="w-full h-full object-contain" />
          </div>
          <div class="text-center">
            <span class="text-[#3D3229] font-luxury text-lg tracking-[0.15em] block">KHARIS</span>
            <span class="text-[#A69783] text-[11px] tracking-[0.3em] uppercase">Portal Mayoristas</span>
          </div>
        </div>

        <!-- Logo desktop: esquina superior izquierda -->
        <div class="hidden lg:flex items-center gap-2 lg:gap-3">
          <div class="w-12 h-12 rounded-full bg-white/10 p-2 flex items-center justify-center">
            <img src="/logo-kharis.png" alt="Kharis" class="w-full h-full object-contain" />
          </div>
          <div>
            <span class="text-[#C9A962] font-luxury text-xl tracking-wider">KHARIS</span>
            <span class="text-white/60 text-sm block -mt-1">PRO</span>
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
         En móvil: card flotante con bordes redondeados que sube sobre el header
         En desktop: lado derecho normal
    ========================================================================== -->
    <div class="flex-1 lg:w-7/12 flex items-start lg:items-center justify-center bg-white lg:bg-[#FAFAFA] -mt-5 lg:mt-0 rounded-t-[28px] lg:rounded-none relative z-20 px-5 pt-7 pb-8 sm:p-6 lg:p-12 overflow-y-auto hide-scrollbar">
      <div class="w-full max-w-lg">
        <!-- Pill indicator móvil (estilo app sheet) -->
        <div class="flex justify-center mb-5 lg:hidden">
          <div class="w-10 h-1 rounded-full bg-[#E2C9B8]/60"></div>
        </div>
        
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
          
          <p class="text-[#7A6B5D] lg:text-text-medium mb-6 max-w-sm mx-auto">
            Nuestro equipo verificará tu identidad en menos de 
            <span class="font-semibold text-[#3D3229]">24 horas</span>.
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
                  <li>• Verificaremos tu identidad</li>
                  <li>• Te notificaremos cuando tu cuenta esté activa</li>
                </ul>
              </div>
            </div>
          </div>
          
          <router-link 
            to="/portal/login"
            class="inline-flex items-center gap-2 text-[#3D3229] hover:text-[#2C2420] font-medium transition-colors"
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
            <h2 class="text-[22px] lg:text-3xl font-luxury text-[#3D3229] lg:text-text-dark mb-1.5 lg:mb-2">
              Solicitud de Cuenta
            </h2>
            <p class="text-[#A69783] lg:text-text-light text-[13px] lg:text-base">
              Completa el formulario para unirte a nuestra red
            </p>
          </div>

          <!-- Progress Steps -->
          <div class="flex items-center justify-center gap-3 lg:gap-4 mb-5 lg:mb-8">
            <div class="flex items-center gap-1.5 lg:gap-2">
              <div 
                :class="[
                  'w-7 h-7 lg:w-8 lg:h-8 rounded-full flex items-center justify-center text-xs lg:text-sm font-medium transition-colors',
                  currentStep >= 1 ? 'bg-[#2C2420] text-white' : 'bg-[#E8DDD3] text-[#A69783]'
                ]"
              >
                <svg v-if="currentStep > 1" class="w-3.5 h-3.5 lg:w-4 lg:h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span v-else>1</span>
              </div>
              <span :class="currentStep >= 1 ? 'text-[#3D3229] font-medium' : 'text-[#A69783]'" class="text-[11px] lg:text-sm hidden sm:block">
                Información Personal
              </span>
            </div>
            
            <div class="w-10 lg:w-12 h-0.5 bg-[#E8DDD3] rounded-full">
              <div 
                class="h-full bg-[#2C2420] rounded-full transition-all duration-300"
                :style="{ width: currentStep > 1 ? '100%' : '0%' }"
              ></div>
            </div>
            
            <div class="flex items-center gap-1.5 lg:gap-2">
              <div 
                :class="[
                  'w-7 h-7 lg:w-8 lg:h-8 rounded-full flex items-center justify-center text-xs lg:text-sm font-medium transition-colors',
                  currentStep >= 2 ? 'bg-[#2C2420] text-white' : 'bg-[#E8DDD3] text-[#A69783]'
                ]"
              >
                2
              </div>
              <span :class="currentStep >= 2 ? 'text-[#3D3229] font-medium' : 'text-[#A69783]'" class="text-[11px] lg:text-sm hidden sm:block">
                Verificación
              </span>
            </div>
          </div>

          <!-- Form -->
          <form @submit.prevent="handleSubmit">
            
            <!-- ===== PASO 1: Información Personal ===== -->
            <div v-show="currentStep === 1" class="space-y-4 lg:space-y-4">
              <div class="grid sm:grid-cols-2 gap-3 lg:gap-4">
                <div>
                  <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">Nombre *</label>
                  <input
                    v-model="form.nombre"
                    type="text"
                    required
                    placeholder="Tu nombre"
                    class="w-full px-4 py-3.5 lg:px-4 lg:py-3 text-[15px] lg:text-base text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border rounded-2xl lg:rounded-lg outline-none transition-all placeholder-[#C4B5A4] focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
                    :class="errors.nombre ? 'border-red-300' : 'border-[#E8DDD3] lg:border-gray-200'"
                  />
                  <p v-if="errors.nombre" class="mt-1 text-xs text-red-500">{{ errors.nombre }}</p>
                </div>
                <div>
                  <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">Apellidos *</label>
                  <input
                    v-model="form.apellido"
                    type="text"
                    required
                    placeholder="Tus apellidos"
                    class="w-full px-4 py-3.5 lg:px-4 lg:py-3 text-[15px] lg:text-base text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border rounded-2xl lg:rounded-lg outline-none transition-all placeholder-[#C4B5A4] focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
                    :class="errors.apellido ? 'border-red-300' : 'border-[#E8DDD3] lg:border-gray-200'"
                  />
                  <p v-if="errors.apellido" class="mt-1 text-xs text-red-500">{{ errors.apellido }}</p>
                </div>
              </div>

              <div>
                <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">Celular / WhatsApp *</label>
                <div class="relative">
                  <span class="absolute left-4 top-1/2 -translate-y-1/2 text-[#C4B5A4] text-[15px] lg:text-sm">+57</span>
                  <input
                    v-model="form.telefono"
                    type="tel"
                    required
                    placeholder=""
                    class="w-full px-4 py-3.5 lg:px-4 lg:py-3 pl-12 lg:pl-14 text-[15px] lg:text-base text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border rounded-2xl lg:rounded-lg outline-none transition-all placeholder-[#C4B5A4] focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
                    :class="errors.telefono ? 'border-red-300' : 'border-[#E8DDD3] lg:border-gray-200'"
                  />
                </div>
                <p v-if="errors.telefono" class="mt-1 text-xs text-red-500">{{ errors.telefono }}</p>
              </div>

              <div>
                <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">Correo Electrónico *</label>
                <input
                  v-model="form.email"
                  type="email"
                  required
                  placeholder=""
                  class="w-full px-4 py-3.5 lg:px-4 lg:py-3 text-[15px] lg:text-base text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border rounded-2xl lg:rounded-lg outline-none transition-all placeholder-[#C4B5A4] focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
                  :class="errors.email ? 'border-red-300' : 'border-[#E8DDD3] lg:border-gray-200'"
                />
                <p v-if="errors.email" class="mt-1 text-xs text-red-500">{{ errors.email }}</p>
              </div>

              <div>
                <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">Contraseña *</label>
                <div class="relative">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    placeholder="Crea una contraseña segura"
                    class="w-full px-4 py-3.5 lg:px-4 lg:py-3 pr-12 text-[15px] lg:text-base text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border rounded-2xl lg:rounded-lg outline-none transition-all placeholder-[#C4B5A4] focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
                    :class="errors.password ? 'border-red-300' : 'border-[#E8DDD3] lg:border-gray-200'"
                  />
                  <button 
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-4 top-1/2 -translate-y-1/2 text-[#C4B5A4] hover:text-[#7A6B5D] p-0.5 transition-colors"
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
                
                <!-- Validación de contraseña en tiempo real -->
                <div v-if="form.password" class="mt-2 space-y-1 bg-[#FDFCFA] p-3 rounded-2xl border border-[#E8DDD3]">
                  <p class="text-[11px] font-medium text-[#7A6B5D] mb-2">Requisitos de seguridad:</p>
                  
                  <div class="flex items-center gap-2 text-xs">
                    <svg v-if="passwordValidation.minimo8" class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span :class="passwordValidation.minimo8 ? 'text-green-600 font-medium' : 'text-[#A69783]'">Mínimo 8 caracteres</span>
                  </div>
                  
                  <div class="flex items-center gap-2 text-xs">
                    <svg v-if="passwordValidation.tieneMayuscula" class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span :class="passwordValidation.tieneMayuscula ? 'text-green-600 font-medium' : 'text-[#A69783]'">Al menos una MAYÚSCULA</span>
                  </div>
                  
                  <div class="flex items-center gap-2 text-xs">
                    <svg v-if="passwordValidation.tieneNumero" class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span :class="passwordValidation.tieneNumero ? 'text-green-600 font-medium' : 'text-[#A69783]'">Al menos un número (0-9)</span>
                  </div>
                  
                  <div class="flex items-center gap-2 text-xs">
                    <svg v-if="passwordValidation.tieneEspecial" class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span :class="passwordValidation.tieneEspecial ? 'text-green-600 font-medium' : 'text-[#A69783]'">Carácter especial (!@#$%^&*...)</span>
                  </div>
                </div>
                
                <p v-if="errors.password" class="mt-1 text-xs text-red-500">{{ errors.password }}</p>
              </div>

              <div>
                <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">Confirmar Contraseña *</label>
                <input
                  v-model="form.passwordConfirm"
                  type="password"
                  required
                  placeholder="Repite tu contraseña"
                  class="w-full px-4 py-3.5 lg:px-4 lg:py-3 text-[15px] lg:text-base text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border rounded-2xl lg:rounded-lg outline-none transition-all placeholder-[#C4B5A4] focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
                  :class="errors.passwordConfirm ? 'border-red-300' : 'border-[#E8DDD3] lg:border-gray-200'"
                />
                <p v-if="errors.passwordConfirm" class="mt-1 text-xs text-red-500">{{ errors.passwordConfirm }}</p>
              </div>

              <!-- Botón Siguiente -->
              <button
                type="button"
                @click="nextStep"
                class="w-full py-3.5 lg:py-4 bg-[#2C2420] hover:bg-[#1A1510] text-white text-[15px] lg:text-base font-medium rounded-2xl lg:rounded-lg
                       shadow-lg shadow-[#2C2420]/20 active:scale-[0.98]
                       transition-all duration-200 flex items-center justify-center gap-2 group mt-5 lg:mt-6"
              >
                <span>Siguiente</span>
                <svg class="w-4 h-4 lg:w-5 lg:h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>

            <!-- ===== PASO 2: Verificación de Identidad ===== -->
            <div v-show="currentStep === 2" class="space-y-4 lg:space-y-5">
              <!-- Tipo + Número de Documento en una fila -->
              <div>
                <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">Documento de Identidad *</label>
                <div class="flex gap-2">
                  <select
                    v-model="form.tipoDocumento"
                    class="w-22 lg:w-24 px-3 py-3.5 lg:px-3 lg:py-3 text-[13px] lg:text-sm text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border border-[#E8DDD3] lg:border-gray-200 rounded-xl lg:rounded-lg outline-none transition-all focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
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
                    inputmode="numeric"
                    :placeholder="form.tipoDocumento === 'NIT' ? '900123456' : (form.tipoDocumento === 'PASAPORTE' ? '1234567890' : '12345678')"
                    class="flex-1 px-4 py-3.5 lg:px-4 lg:py-3 text-[15px] lg:text-base text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border rounded-xl lg:rounded-lg outline-none transition-all placeholder-[#C4B5A4] focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
                    :class="form.numeroDocumento && !documentoValidation.longitudValida ? 'border-red-300' : 'border-[#E8DDD3] lg:border-gray-200'"
                  />
                </div>
                <!-- Validación de documento en tiempo real -->
                <div v-if="form.numeroDocumento" class="mt-2 space-y-1">
                  <div class="flex items-center gap-2 text-xs">
                    <svg v-if="documentoValidation.todoNumeros" class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span :class="documentoValidation.todoNumeros ? 'text-green-600' : 'text-red-600'">Solo números</span>
                  </div>
                  <div v-if="form.tipoDocumento === 'CC' || form.tipoDocumento === 'CE'" class="flex items-center gap-2 text-xs">
                    <svg v-if="documentoValidation.longitudValida" class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span :class="documentoValidation.longitudValida ? 'text-green-600' : 'text-red-600'">Mínimo 8 y máximo 10 dígitos</span>
                  </div>
                  <div v-else-if="form.tipoDocumento === 'NIT'" class="flex items-center gap-2 text-xs">
                    <svg v-if="documentoValidation.longitudValida" class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span :class="documentoValidation.longitudValida ? 'text-green-600' : 'text-red-600'">Exactamente 9 dígitos</span>
                  </div>
                  <div v-else-if="form.tipoDocumento === 'PASAPORTE'" class="flex items-center gap-2 text-xs">
                    <svg v-if="documentoValidation.longitudValida" class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span :class="documentoValidation.longitudValida ? 'text-green-600' : 'text-red-600'">10 a 13 dígitos</span>
                  </div>
                </div>
                <p v-if="errors.numeroDocumento" class="mt-1 text-xs text-red-500">{{ errors.numeroDocumento }}</p>
              </div>

              <!-- Foto Cédula -->
              <div>
                <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">
                  Foto del Documento <span class="text-red-400">*</span>
                  <span class="text-[#A69783] font-normal ml-1">(frente)</span>
                </label>
                <div
                  @click="$refs.cedulaInput.click()"
                  @dragover.prevent
                  @drop.prevent="e => { form.fotoCedula = e.dataTransfer.files[0] }"
                  class="relative cursor-pointer border-2 border-dashed rounded-2xl p-5 flex flex-col items-center gap-2 transition-all"
                  :class="errors.fotoCedula ? 'border-red-300 bg-red-50/30' : form.fotoCedula ? 'border-[#3D3229]/40 bg-[#FAF5F2]' : 'border-[#D4C5B5] bg-[#FDFCFA] hover:border-[#3D3229]/30 hover:bg-[#FAF5F2]'"
                >
                  <input
                    ref="cedulaInput"
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="e => { form.fotoCedula = e.target.files[0] }"
                  />
                  
                  <!-- Preview si ya hay archivo -->
                  <template v-if="form.fotoCedula">
                    <div class="flex items-center gap-3 w-full">
                      <div class="w-10 h-10 rounded-xl bg-[#3D3229]/10 flex items-center justify-center shrink-0">
                        <svg class="w-5 h-5 text-[#3D3229]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-[13px] font-medium text-[#3D3229] truncate">{{ form.fotoCedula.name }}</p>
                        <p class="text-[11px] text-[#A69783]">{{ (form.fotoCedula.size / 1024).toFixed(0) }} KB &middot; Toca para cambiar</p>
                      </div>
                      <svg class="w-4 h-4 text-green-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                    </div>
                  </template>
                  
                  <!-- Estado vacío -->
                  <template v-else>
                    <div class="w-10 h-10 rounded-full bg-[#E8DDD3] flex items-center justify-center">
                      <svg class="w-5 h-5 text-[#7A6B5D]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <p class="text-[13px] font-medium text-[#3D3229]">Subir foto de la cédula</p>
                    <p class="text-[11px] text-[#A69783]">JPG, PNG o PDF &middot; Máx. 5MB</p>
                  </template>
                </div>
                <p v-if="errors.fotoCedula" class="mt-1 text-xs text-red-500">{{ errors.fotoCedula }}</p>
              </div>

              <!-- Foto Cédula Trasera -->
              <div>
                <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">
                  Foto del Documento <span class="text-red-400">*</span>
                  <span class="text-[#A69783] font-normal ml-1">(trasera)</span>
                </label>
                <div
                  @click="$refs.cedulaTraseraInput.click()"
                  @dragover.prevent
                  @drop.prevent="e => { form.fotoCedulaTrasera = e.dataTransfer.files[0] }"
                  class="relative cursor-pointer border-2 border-dashed rounded-2xl p-5 flex flex-col items-center gap-2 transition-all"
                  :class="errors.fotoCedulaTrasera ? 'border-red-300 bg-red-50/30' : form.fotoCedulaTrasera ? 'border-[#3D3229]/40 bg-[#FAF5F2]' : 'border-[#D4C5B5] bg-[#FDFCFA] hover:border-[#3D3229]/30 hover:bg-[#FAF5F2]'"
                >
                  <input
                    ref="cedulaTraseraInput"
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="e => { form.fotoCedulaTrasera = e.target.files[0] }"
                  />
                  <template v-if="form.fotoCedulaTrasera">
                    <div class="flex items-center gap-3 w-full">
                      <div class="w-10 h-10 rounded-xl bg-[#3D3229]/10 flex items-center justify-center shrink-0">
                        <svg class="w-5 h-5 text-[#3D3229]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-[13px] font-medium text-[#3D3229] truncate">{{ form.fotoCedulaTrasera.name }}</p>
                        <p class="text-[11px] text-[#A69783]">{{ (form.fotoCedulaTrasera.size / 1024).toFixed(0) }} KB &middot; Toca para cambiar</p>
                      </div>
                      <svg class="w-4 h-4 text-green-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                    </div>
                  </template>
                  <template v-else>
                    <div class="w-10 h-10 rounded-full bg-[#E8DDD3] flex items-center justify-center">
                      <svg class="w-5 h-5 text-[#7A6B5D]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <p class="text-[13px] font-medium text-[#3D3229]">Subir foto trasera</p>
                    <p class="text-[11px] text-[#A69783]">JPG, PNG o PDF &middot; Máx. 5MB</p>
                  </template>
                </div>
                <p v-if="errors.fotoCedulaTrasera" class="mt-1 text-xs text-red-500">{{ errors.fotoCedulaTrasera }}</p>
              </div>

              <div>
                <label class="block text-[13px] lg:text-sm font-medium text-[#3D3229] lg:text-text-dark mb-1.5">
                  Nombre de Empresa / Negocio
                  <span class="text-[#A69783] font-normal">(opcional)</span>
                </label>
                <input
                  v-model="form.nombreEmpresa"
                  type="text"
                  placeholder="Mi Salón de Belleza S.A.S"
                  class="w-full px-4 py-3.5 lg:px-4 lg:py-3 text-[15px] lg:text-base text-[#3D3229] lg:text-text-dark bg-[#FDFCFA] lg:bg-white border border-[#E8DDD3] lg:border-gray-200 rounded-2xl lg:rounded-lg outline-none transition-all placeholder-[#C4B5A4] focus:ring-2 focus:ring-[#3D3229]/10 focus:border-[#3D3229]/30"
                />
              </div>


              <!-- Términos -->
              <div class="flex items-start gap-2.5 lg:gap-3 pt-1 lg:pt-2">
                <input 
                  id="terminos"
                  v-model="form.aceptaTerminos"
                  type="checkbox"
                  required
                  class="mt-0.5 w-4 h-4 lg:w-4 lg:h-4 text-[#3D3229] border-[#D4C5B5] rounded focus:ring-[#3D3229]/20"
                />
                <label for="terminos" class="text-[12px] lg:text-sm text-[#7A6B5D] leading-tight">
                  Acepto los <a href="#" class="text-[#3D3229] hover:underline font-medium">Términos y Condiciones</a> 
                  y autorizo el tratamiento de mis datos personales según la 
                  <a href="#" class="text-[#3D3229] hover:underline font-medium">Política de Privacidad</a>
                </label>
              </div>
              <p v-if="errors.aceptaTerminos" class="text-xs text-red-500 -mt-2">{{ errors.aceptaTerminos }}</p>

              <!-- Botones -->
              <div class="flex gap-3 lg:gap-4 pt-3 lg:pt-4">
                <button
                  type="button"
                  @click="prevStep"
                  class="flex-1 py-3.5 lg:py-4 border border-[#D4C5B5] text-[#3D3229] text-[15px] lg:text-base font-medium rounded-2xl lg:rounded-lg
                         hover:bg-[#FAF5F2] active:scale-[0.98] transition-all duration-200 flex items-center justify-center gap-1.5 lg:gap-2"
                >
                  <svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  <span>Atrás</span>
                </button>
                
                <button
                  type="submit"
                  :disabled="loading"
                  class="flex-1 py-3.5 lg:py-4 bg-[#2C2420] hover:bg-[#1A1510] text-white text-[15px] lg:text-base font-medium rounded-2xl lg:rounded-lg
                         shadow-lg shadow-[#2C2420]/20 active:scale-[0.98]
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
          <div class="mt-5 lg:mt-8 pt-4 lg:pt-6 border-t border-[#E8DDD3]/60 lg:border-gray-100 text-center">
            <p class="text-[#7A6B5D] lg:text-text-medium text-[13px] lg:text-sm">
              ¿Ya tienes cuenta? 
              <router-link to="/portal/login" class="text-[#3D3229] hover:underline font-medium">
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
                class="px-6 py-3 bg-[#2C2420] hover:bg-[#1A1510] text-white font-medium rounded-2xl transition-colors"
              >
                {{ statusModal.action === 'login' ? 'Iniciar sesión' : 'Contactar soporte' }}
              </button>
              
              <!-- Botón cerrar -->
              <button 
                @click="closeStatusModal"
                class="px-6 py-3 border border-[#D4C5B5] text-[#3D3229] font-medium rounded-2xl hover:bg-[#FAF5F2] transition-colors"
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
import { ref, reactive, watch } from 'vue'
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
    
    // Modal de estado (para mostrar mensajes elegantes)
    const statusModal = ref({
      show: false,
      status: '',
      title: '',
      message: '',
      icon: '',
      action: null
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
      fotoCedula: null,
      fotoCedulaTrasera: null,
      nombreEmpresa: '',
      aceptaTerminos: false
    })
    
    const errors = reactive({})
    
    // Validaciones en tiempo real para documento
    const documentoValidation = reactive({
      longitudValida: false,
      todoNumeros: false
    })
    
    // Validaciones en tiempo real para contraseña
    const passwordValidation = reactive({
      minimo8: false,
      tieneMayuscula: false,
      tieneNumero: false,
      tieneEspecial: false
    })
    
    // =========================================================================
    // WATCHERS - Validación en tiempo real
    // =========================================================================
    watch(() => form.numeroDocumento, (newVal) => {
      // Solo permitir números
      form.numeroDocumento = newVal.replace(/[^0-9]/g, '')
      
      // Validar según tipo de documento
      const longitud = form.numeroDocumento.length
      documentoValidation.todoNumeros = /^\d*$/.test(form.numeroDocumento)
      
      if (form.tipoDocumento === 'CC' || form.tipoDocumento === 'CE') {
        documentoValidation.longitudValida = longitud >= 8 && longitud <= 10
      } else if (form.tipoDocumento === 'NIT') {
        documentoValidation.longitudValida = longitud === 9
      } else if (form.tipoDocumento === 'PASAPORTE') {
        documentoValidation.longitudValida = longitud >= 10 && longitud <= 13
      }
    })
    
    watch(() => form.password, (newVal) => {
      passwordValidation.minimo8 = newVal.length >= 8
      passwordValidation.tieneMayuscula = /[A-Z]/.test(newVal)
      passwordValidation.tieneNumero = /\d/.test(newVal)
      passwordValidation.tieneEspecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(newVal)
    })
    
    watch(() => form.tipoDocumento, () => {
      // Re-validar el documento cuando cambia el tipo
      const newVal = form.numeroDocumento
      const longitud = newVal.length
      
      if (form.tipoDocumento === 'CC' || form.tipoDocumento === 'CE') {
        documentoValidation.longitudValida = longitud >= 8 && longitud <= 10
      } else if (form.tipoDocumento === 'NIT') {
        documentoValidation.longitudValida = longitud === 9
      } else if (form.tipoDocumento === 'PASAPORTE') {
        documentoValidation.longitudValida = longitud >= 10 && longitud <= 13
      }
    })
    
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
      } else if (!passwordValidation.minimo8 || !passwordValidation.tieneMayuscula || !passwordValidation.tieneNumero || !passwordValidation.tieneEspecial) {
        errors.password = 'La contraseña debe cumplir todos los requisitos'
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
      } else if (!documentoValidation.longitudValida || !documentoValidation.todoNumeros) {
        errors.numeroDocumento = 'El número de documento no es válido'
        isValid = false
      }
      
      if (!form.fotoCedula) {
        errors.fotoCedula = 'Debes subir una foto de tu documento de identidad'
        isValid = false
      }

      if (!form.fotoCedulaTrasera) {
        errors.fotoCedulaTrasera = 'Debes subir la foto trasera del documento'
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
        if (form.fotoCedula) {
          formData.append('foto_cedula', form.fotoCedula)
        }
        if (form.fotoCedulaTrasera) {
          formData.append('foto_cedula_trasera', form.fotoCedulaTrasera)
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
      form,
      errors,
      statusModal,
      documentoValidation,
      passwordValidation,
      nextStep,
      prevStep,
      handleSubmit,
      closeStatusModal,
      handleModalAction
    }
  }
}
</script>

<style scoped>
/* Hide scrollbar on mobile sheet */
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

/* Mobile app-like background */
.b2b-registro-screen {
  background: #FAF5F2;
}

@media (min-width: 1024px) {
  .b2b-registro-screen {
    background: #FAFAFA;
  }
}

/* Checkbox personalizado */
input[type="checkbox"]:checked {
  background-color: #3D3229;
  border-color: #3D3229;
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
