<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FBF9F7] to-[#F5F0EC]">
    
    <!-- Header Premium -->
    <header class="bg-white/80 border-b border-nude-100/50 py-5 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <router-link to="/" class="group flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-brand-500 to-brand-600 flex items-center justify-center shadow-lg shadow-brand-500/20">
              <span class="text-white font-luxury text-lg">K</span>
            </div>
            <span class="font-luxury text-2xl text-text-dark tracking-wide group-hover:text-brand-600 transition-colors">Kharis</span>
          </router-link>
          
          <!-- Badges de seguridad -->
          <div class="hidden sm:flex items-center gap-6">
            <div class="flex items-center gap-2 text-sm text-text-medium">
              <div class="w-8 h-8 rounded-full bg-green-50 flex items-center justify-center">
                <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                </svg>
              </div>
              <span>Compra Segura</span>
            </div>
            <div class="flex items-center gap-2 text-sm text-text-medium">
              <div class="w-8 h-8 rounded-full bg-brand-50 flex items-center justify-center">
                <svg class="w-4 h-4 text-brand-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>
              </div>
              <span>Satisfacción Garantizada</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
      
      <!-- Título Premium -->
      <div class="text-center mb-10">
        <h1 class="font-luxury text-3xl lg:text-4xl text-text-dark mb-3">Finalizar Pedido</h1>
        <p class="text-text-medium">Estás a un paso de lucir increíble ✨</p>
      </div>
      
      <!-- Barra de Progreso Premium -->
      <div class="max-w-xl mx-auto mb-12">
        <div class="flex items-center justify-between relative">
          <!-- Línea de fondo -->
          <div class="absolute top-5 left-0 right-0 h-0.5 bg-nude-200"></div>
          <!-- Línea de progreso -->
          <div class="absolute top-5 left-0 h-0.5 bg-gradient-to-r from-brand-500 to-brand-600 transition-all duration-500" :style="{ width: progressWidth }"></div>
          
          <!-- Paso 1 -->
          <div class="relative z-10 flex flex-col items-center">
            <div :class="['w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300 shadow-lg', currentStep >= 1 ? 'bg-gradient-to-br from-brand-500 to-brand-600 text-white shadow-brand-500/30' : 'bg-white text-text-medium border-2 border-nude-200']">
              <svg v-if="currentStep > 1" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
              <span v-else>1</span>
            </div>
            <span class="mt-2 text-xs font-medium" :class="currentStep >= 1 ? 'text-brand-600' : 'text-text-medium'">Datos</span>
          </div>
          
          <!-- Paso 2 -->
          <div class="relative z-10 flex flex-col items-center">
            <div :class="['w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300 shadow-lg', currentStep >= 2 ? 'bg-gradient-to-br from-brand-500 to-brand-600 text-white shadow-brand-500/30' : 'bg-white text-text-medium border-2 border-nude-200']">
              <svg v-if="currentStep > 2" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
              <span v-else>2</span>
            </div>
            <span class="mt-2 text-xs font-medium" :class="currentStep >= 2 ? 'text-brand-600' : 'text-text-medium'">Envío</span>
          </div>
          
          <!-- Paso 3 -->
          <div class="relative z-10 flex flex-col items-center">
            <div :class="['w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300 shadow-lg', currentStep >= 3 ? 'bg-gradient-to-br from-brand-500 to-brand-600 text-white shadow-brand-500/30' : 'bg-white text-text-medium border-2 border-nude-200']">
              <span>3</span>
            </div>
            <span class="mt-2 text-xs font-medium" :class="currentStep >= 3 ? 'text-brand-600' : 'text-text-medium'">Pago</span>
          </div>
        </div>
      </div>

      <!-- Contenido Principal - 2 Columnas -->
      <div class="grid lg:grid-cols-5 gap-8 lg:gap-12">
        
        <!-- Columna Izquierda: Formularios (60%) -->
        <div class="lg:col-span-3 space-y-6">
          
          <!-- Sección: Información Personal -->
          <div class="bg-white rounded-3xl p-6 lg:p-8 shadow-xl shadow-black/[0.03] border border-nude-100/50">
            <div class="flex items-center gap-4 mb-8">
              <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center">
                <svg class="w-6 h-6 text-brand-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
              </div>
              <div>
                <h2 class="font-luxury text-xl text-text-dark">Información Personal</h2>
                <p class="text-sm text-text-medium">¿A quién enviamos tu pedido?</p>
              </div>
            </div>
            
            <div class="grid sm:grid-cols-2 gap-5">
              <div class="group">
                <label class="block text-sm font-medium text-text-dark mb-2">Nombre completo</label>
                <input 
                  type="text" 
                  v-model="form.nombre"
                  class="w-full px-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all placeholder:text-text-light"
                  placeholder="Tu nombre"
                />
              </div>
              
              <div class="group">
                <label class="block text-sm font-medium text-text-dark mb-2">Correo electrónico</label>
                <input 
                  type="email" 
                  v-model="form.email"
                  class="w-full px-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all placeholder:text-text-light"
                  placeholder="tu@email.com"
                />
              </div>
              
              <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-text-dark mb-2">
                  Teléfono / WhatsApp
                  <span class="text-brand-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <span class="absolute left-4 top-1/2 -translate-y-1/2 text-text-medium">+47</span>
                  <input 
                    type="tel" 
                    v-model="form.telefono"
                    class="w-full pl-14 pr-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all placeholder:text-text-light"
                    placeholder="47 966 57 763"
                  />
                </div>
                <p class="text-xs text-text-medium mt-2 flex items-center gap-1">
                  <svg class="w-3.5 h-3.5 text-green-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                  </svg>
                  Te enviaremos actualizaciones de tu pedido
                </p>
              </div>
            </div>
          </div>

          <!-- Sección: Dirección de Entrega -->
          <div class="bg-white rounded-3xl p-6 lg:p-8 shadow-xl shadow-black/[0.03] border border-nude-100/50">
            <div class="flex items-center gap-4 mb-8">
              <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-100 to-amber-50 flex items-center justify-center">
                <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                </svg>
              </div>
              <div>
                <h2 class="font-luxury text-xl text-text-dark">Dirección de Entrega</h2>
                <p class="text-sm text-text-medium">¿Dónde recibes tu pedido?</p>
              </div>
            </div>
            
            <div class="grid sm:grid-cols-2 gap-5">
              <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-text-dark mb-2">Dirección completa</label>
                <input 
                  type="text" 
                  v-model="form.direccion"
                  class="w-full px-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all placeholder:text-text-light"
                  placeholder="Calle, número, colonia..."
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-text-dark mb-2">Ciudad</label>
                <input 
                  type="text" 
                  v-model="form.ciudad"
                  class="w-full px-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all placeholder:text-text-light"
                  placeholder="Tu ciudad"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-text-dark mb-2">Código Postal</label>
                <input 
                  type="text" 
                  v-model="form.codigoPostal"
                  class="w-full px-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all placeholder:text-text-light"
                  placeholder="00000"
                />
              </div>
              
              <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-text-dark mb-2">Referencias <span class="text-text-light">(opcional)</span></label>
                <textarea 
                  v-model="form.referencias"
                  rows="2"
                  class="w-full px-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all resize-none placeholder:text-text-light"
                  placeholder="Entre calles, color de casa, indicaciones para el repartidor..."
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Sección: Método de Pago -->
          <div class="bg-white rounded-3xl p-6 lg:p-8 shadow-xl shadow-black/[0.03] border border-nude-100/50">
            <div class="flex items-center gap-4 mb-8">
              <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-green-100 to-green-50 flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
                </svg>
              </div>
              <div>
                <h2 class="font-luxury text-xl text-text-dark">Método de Pago</h2>
                <p class="text-sm text-text-medium">Elige cómo quieres pagar</p>
              </div>
            </div>
            
            <!-- Opciones de Pago -->
            <div class="space-y-4">
              
              <!-- Opción A: Pago Online -->
              <div 
                @click="paymentMethod = 'online'"
                :class="[
                  'relative border-2 rounded-2xl p-5 cursor-pointer transition-all duration-300',
                  paymentMethod === 'online' 
                    ? 'border-brand-500 bg-gradient-to-br from-brand-50/50 to-white shadow-lg shadow-brand-500/10' 
                    : 'border-nude-200 hover:border-brand-200 hover:shadow-md'
                ]"
              >
                <!-- Badge recomendado -->
                <div v-if="paymentMethod !== 'online'" class="absolute -top-3 left-4 px-3 py-0.5 bg-brand-500 text-white text-xs font-medium rounded-full">
                  Recomendado
                </div>
                
                <div class="flex items-start gap-4">
                  <div :class="['w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 mt-0.5 transition-all', paymentMethod === 'online' ? 'border-brand-600 bg-brand-600' : 'border-nude-300']">
                    <svg v-if="paymentMethod === 'online'" class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center justify-between flex-wrap gap-2">
                      <h3 class="font-semibold text-text-dark text-lg">Pago Seguro Online</h3>
                      <div class="flex items-center gap-2">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" alt="Visa" class="h-5" />
                        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg" alt="Mastercard" class="h-6" />
                        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg" alt="PayPal" class="h-5" />
                      </div>
                    </div>
                    <p class="text-sm text-text-medium mt-1">Paga de forma rápida y segura con tu tarjeta</p>
                    
                    <!-- Formulario de tarjeta (cuando está seleccionado) -->
                    <div v-if="paymentMethod === 'online'" class="mt-6 space-y-4 animate-fadeIn">
                      <div>
                        <label class="block text-sm font-medium text-text-dark mb-2">Número de tarjeta</label>
                        <div class="relative">
                          <input 
                            type="text" 
                            v-model="card.number"
                            class="w-full pl-12 pr-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all"
                            placeholder="0000 0000 0000 0000"
                          />
                          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-light" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
                          </svg>
                        </div>
                      </div>
                      <div class="grid grid-cols-2 gap-4">
                        <div>
                          <label class="block text-sm font-medium text-text-dark mb-2">Vencimiento</label>
                          <input 
                            type="text" 
                            v-model="card.expiry"
                            class="w-full px-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all"
                            placeholder="MM/AA"
                          />
                        </div>
                        <div>
                          <label class="block text-sm font-medium text-text-dark mb-2">CVV</label>
                          <input 
                            type="text" 
                            v-model="card.cvv"
                            class="w-full px-4 py-3.5 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 focus:ring-4 focus:ring-brand-100/50 focus:bg-white transition-all"
                            placeholder="123"
                          />
                        </div>
                      </div>
                      <div class="flex items-center gap-2 text-xs text-text-medium bg-green-50 p-3 rounded-lg">
                        <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                        </svg>
                        <span>Tus datos están protegidos con encriptación SSL de 256 bits</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Opción B: Atención Personalizada / WhatsApp (VIP) -->
              <div 
                @click="selectWhatsAppPayment"
                :class="[
                  'relative border-2 rounded-2xl p-5 cursor-pointer transition-all duration-300 overflow-hidden',
                  paymentMethod === 'whatsapp' 
                    ? 'border-green-500 bg-gradient-to-br from-green-50 via-emerald-50/50 to-white shadow-lg shadow-green-500/10' 
                    : 'border-nude-200 hover:border-green-200 hover:shadow-md'
                ]"
              >
                <!-- Decoración VIP -->
                <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-amber-400/20 to-transparent rounded-bl-full"></div>
                
                <div class="flex items-start gap-4 relative">
                  <div :class="['w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 mt-0.5 transition-all', paymentMethod === 'whatsapp' ? 'border-green-600 bg-green-600' : 'border-nude-300']">
                    <svg v-if="paymentMethod === 'whatsapp'" class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-3 flex-wrap">
                      <h3 class="font-semibold text-text-dark text-lg">Atención Personalizada</h3>
                      <span class="text-xs bg-gradient-to-r from-amber-400 to-orange-400 text-white px-3 py-1 rounded-full font-bold shadow-sm">✨ VIP</span>
                    </div>
                    <p class="text-sm text-text-medium mt-1">Finaliza tu compra con una asesora experta por WhatsApp</p>
                    
                    <!-- Código de Pre-Orden (cuando está seleccionado) -->
                    <div v-if="paymentMethod === 'whatsapp'" class="mt-6 space-y-4 animate-fadeIn">
                      <div class="bg-gradient-to-r from-amber-50 via-orange-50 to-amber-50 rounded-2xl p-5 border border-amber-200/50">
                        <div class="flex items-center gap-2 mb-3">
                          <div class="w-8 h-8 rounded-full bg-amber-400 flex items-center justify-center">
                            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                          </div>
                          <span class="text-sm font-medium text-amber-800">Tu código de Pre-Orden está listo</span>
                        </div>
                        <div class="flex items-center justify-between bg-white rounded-xl p-4 border border-amber-200/50">
                          <span class="font-mono text-3xl font-bold text-amber-900 tracking-widest">{{ preOrderCode }}</span>
                          <button 
                            @click.stop="copyCode"
                            class="flex items-center gap-1.5 text-sm text-amber-600 hover:text-amber-800 font-medium transition-colors"
                          >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
                            </svg>
                            Copiar
                          </button>
                        </div>
                        <p class="text-xs text-amber-700 mt-3 text-center">Comparte este código con tu asesora para confirmar tu pedido</p>
                      </div>
                      
                      <!-- Botón WhatsApp Premium -->
                      <a 
                        :href="whatsappLink"
                        target="_blank"
                        class="group w-full flex items-center justify-center gap-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-4 px-6 rounded-2xl transition-all duration-300 shadow-xl shadow-green-500/30 hover:shadow-green-500/40 hover:scale-[1.02]"
                      >
                        <svg class="w-7 h-7" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                        </svg>
                        <span class="text-lg">Continuar por WhatsApp</span>
                        <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                        </svg>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Botón Finalizar (solo para pago online) -->
            <button 
              v-if="paymentMethod === 'online'"
              @click="procesarPago"
              :disabled="processing"
              class="mt-8 w-full bg-gradient-to-r from-brand-600 to-brand-700 hover:from-brand-700 hover:to-brand-800 disabled:from-brand-300 disabled:to-brand-400 text-white font-semibold text-lg py-4 rounded-2xl transition-all duration-300 shadow-xl shadow-brand-600/30 hover:shadow-brand-600/40 hover:scale-[1.01] uppercase tracking-wider"
            >
              <span v-if="processing" class="flex items-center justify-center gap-3">
                <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Procesando tu pago...
              </span>
              <span v-else class="flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                </svg>
                Pagar ${{ formatPrice(getTotal()) }} MXN
              </span>
            </button>
          </div>
        </div>

        <!-- Columna Derecha: Resumen del Pedido (40%) -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-3xl p-6 lg:p-8 shadow-xl shadow-black/[0.03] border border-nude-100/50 lg:sticky lg:top-28">
            <h2 class="font-luxury text-xl text-text-dark mb-6 flex items-center gap-3">
              <span class="text-2xl">🛍️</span>
              Tu Pedido
            </h2>
            
            <!-- Lista de productos -->
            <div class="space-y-4 mb-6 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
              <div 
                v-for="item in cartItems" 
                :key="item.producto_id"
                class="flex gap-4 p-3 bg-nude-50/50 rounded-2xl"
              >
                <div class="w-20 h-20 bg-white rounded-xl flex-shrink-0 overflow-hidden flex items-center justify-center border border-nude-100 shadow-sm">
                  <img 
                    v-if="item.imagen_url" 
                    :src="item.imagen_url" 
                    :alt="item.nombre"
                    class="w-full h-full object-cover"
                  />
                  <div v-else class="w-full h-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center">
                    <svg class="w-8 h-8 text-brand-300" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                    </svg>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="font-medium text-text-dark line-clamp-2">{{ item.nombre || 'Producto' }}</h4>
                  <p class="text-sm text-text-medium mt-1">Cantidad: {{ item.cantidad || 1 }}</p>
                  <p class="font-semibold text-brand-600 mt-1">${{ formatPrice(getItemPrice(item)) }}</p>
                </div>
              </div>
            </div>
            
            <!-- Cupón de descuento -->
            <div class="mb-6">
              <div class="flex gap-2">
                <input 
                  type="text" 
                  v-model="cupon"
                  class="flex-1 px-4 py-3 bg-nude-50/50 border border-nude-200 rounded-xl focus:outline-none focus:border-brand-400 text-sm placeholder:text-text-light"
                  placeholder="¿Tienes un cupón?"
                />
                <button class="px-4 py-3 bg-text-dark text-white text-sm font-medium rounded-xl hover:bg-black transition-colors">
                  Aplicar
                </button>
              </div>
            </div>
            
            <!-- Desglose de precios -->
            <div class="border-t border-nude-200 pt-5 space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-text-medium">Subtotal</span>
                <span class="text-text-dark font-medium">${{ formatPrice(getSubtotal()) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-text-medium">Envío</span>
                <span :class="envioGratis ? 'text-green-600 font-semibold' : 'text-text-dark'">
                  {{ envioGratis ? '¡GRATIS! 🎉' : '$' + formatPrice(costoEnvio) }}
                </span>
              </div>
              
              <!-- Barra de progreso envío gratis -->
              <div v-if="!envioGratis" class="bg-brand-50 rounded-xl p-4">
                <div class="flex items-center justify-between text-xs mb-2">
                  <span class="text-brand-600 font-medium">¡Te faltan ${{ formatPrice(500 - getSubtotal()) }} para envío gratis!</span>
                  <span class="text-brand-400">🚚</span>
                </div>
                <div class="w-full h-2 bg-brand-100 rounded-full overflow-hidden">
                  <div 
                    class="h-full bg-gradient-to-r from-brand-400 to-brand-600 rounded-full transition-all duration-500"
                    :style="{ width: Math.min((getSubtotal() / 500) * 100, 100) + '%' }"
                  ></div>
                </div>
              </div>
              
              <div class="flex justify-between items-center pt-4 border-t border-nude-200">
                <span class="text-text-dark font-semibold text-lg">Total</span>
                <div class="text-right">
                  <span class="font-luxury text-3xl font-bold text-text-dark">${{ formatPrice(getTotal()) }}</span>
                  <span class="text-sm text-text-medium ml-1">MXN</span>
                </div>
              </div>
            </div>
            
            <!-- Sellos de Confianza -->
            <div class="mt-6 pt-5 border-t border-nude-200">
              <div class="grid grid-cols-2 gap-3">
                <div class="flex items-center gap-2 text-xs text-text-medium bg-nude-50/50 p-3 rounded-xl">
                  <svg class="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                  </svg>
                  <span>Compra Segura</span>
                </div>
                <div class="flex items-center gap-2 text-xs text-text-medium bg-nude-50/50 p-3 rounded-xl">
                  <svg class="w-5 h-5 text-brand-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                  </svg>
                  <span>Envío Asegurado</span>
                </div>
                <div class="flex items-center gap-2 text-xs text-text-medium bg-nude-50/50 p-3 rounded-xl">
                  <svg class="w-5 h-5 text-amber-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                  </svg>
                  <span>Devolución Fácil</span>
                </div>
                <div class="flex items-center gap-2 text-xs text-text-medium bg-nude-50/50 p-3 rounded-xl">
                  <svg class="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                  </svg>
                  <span>Soporte WhatsApp</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Footer mini -->
    <footer class="mt-12 py-6 border-t border-nude-100 bg-white/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm text-text-medium">© 2026 Kharis Distribuidora. Todos los derechos reservados.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Checkout',
  setup() {
    const router = useRouter()
    const currentStep = ref(3)
    const paymentMethod = ref(null)
    const processing = ref(false)
    const preOrderCode = ref('')
    const cupon = ref('')
    const codeCopied = ref(false)
    
    // Calcular progreso de la barra
    const progressWidth = computed(() => {
      if (currentStep.value >= 3) return '100%'
      if (currentStep.value >= 2) return '50%'
      return '0%'
    })
    
    // Datos del formulario
    const form = ref({
      nombre: '',
      email: '',
      telefono: '',
      direccion: '',
      ciudad: '',
      codigoPostal: '',
      referencias: ''
    })
    
    // Datos de tarjeta
    const card = ref({
      number: '',
      expiry: '',
      cvv: ''
    })
    
    // Carrito desde localStorage
    const cartItems = ref([])
    const costoEnvio = ref(50)
    
    const envioGratis = computed(() => getSubtotal() >= 500)
    
    // Número de WhatsApp de la tienda
    const whatsappNumber = '4796657763' // Cambiar por el número real
    
    const whatsappLink = computed(() => {
      const productos = cartItems.value.map(i => `• ${i.nombre || 'Producto'} x${i.cantidad || 1}`).join('%0A')
      const mensaje = `Hola, quiero finalizar mi pedido con código *${preOrderCode.value}*%0A%0A📦 *Productos:*%0A${productos}%0A%0A💰 *Total:* $${formatPrice(getTotal())} MXN%0A%0A📍 *Envío a:* ${form.value.direccion || 'Por definir'}, ${form.value.ciudad || ''}`
      return `https://wa.me/${whatsappNumber}?text=${mensaje}`
    })
    
    const generatePreOrderCode = () => {
      const random = Math.floor(1000 + Math.random() * 9000)
      preOrderCode.value = `K-${random}`
    }
    
    const selectWhatsAppPayment = () => {
      paymentMethod.value = 'whatsapp'
      if (!preOrderCode.value) {
        generatePreOrderCode()
      }
    }
    
    const copyCode = async () => {
      try {
        await navigator.clipboard.writeText(preOrderCode.value)
        codeCopied.value = true
        setTimeout(() => codeCopied.value = false, 2000)
      } catch (e) {
        console.error('Error copiando código:', e)
      }
    }
    
    const formatPrice = (price) => {
      const numPrice = Number(price)
      if (isNaN(numPrice)) return '0'
      return new Intl.NumberFormat('es-MX').format(numPrice)
    }
    
    const getItemPrice = (item) => {
      const price = item.subtotal || item.precio_unitario || item.precio || 0
      const cantidad = item.cantidad || 1
      if (item.subtotal) return item.subtotal
      return price * cantidad
    }
    
    const getSubtotal = () => {
      return cartItems.value.reduce((total, item) => total + getItemPrice(item), 0)
    }
    
    const getTotal = () => {
      const subtotal = getSubtotal()
      return subtotal + (envioGratis.value ? 0 : costoEnvio.value)
    }
    
    const procesarPago = async () => {
      processing.value = true
      // Aquí iría la integración con la pasarela de pago
      setTimeout(() => {
        processing.value = false
        alert('¡Pago procesado exitosamente! Te enviamos un correo de confirmación.')
        localStorage.removeItem('kharis_cart_cache')
        localStorage.removeItem('kharis_cart_count')
        router.push('/')
      }, 2500)
    }
    
    const loadCart = () => {
      try {
        const cached = localStorage.getItem('kharis_cart_cache')
        if (cached) {
          const data = JSON.parse(cached)
          cartItems.value = data.items || []
        }
        
        // También cargar datos del usuario si está logueado
        const user = JSON.parse(localStorage.getItem('user') || 'null')
        if (user) {
          form.value.nombre = user.nombre || ''
          form.value.email = user.email || ''
        }
      } catch (e) {
        console.error('Error cargando carrito:', e)
      }
    }
    
    const unlockScroll = () => {
      document.body.style.overflow = ''
      document.body.style.paddingRight = ''
    }
    
    onMounted(() => {
      // IMPORTANTE: Desbloquear scroll al entrar al checkout
      unlockScroll()
      
      loadCart()
      // Si no hay productos, redirigir
      if (cartItems.value.length === 0) {
        router.push('/')
      }
    })
    
    onUnmounted(() => {
      // Asegurar que el scroll está desbloqueado al salir
      unlockScroll()
    })
    
    return {
      currentStep,
      progressWidth,
      paymentMethod,
      processing,
      preOrderCode,
      cupon,
      codeCopied,
      form,
      card,
      cartItems,
      costoEnvio,
      envioGratis,
      whatsappLink,
      selectWhatsAppPayment,
      copyCode,
      formatPrice,
      getItemPrice,
      getSubtotal,
      getTotal,
      procesarPago
    }
  }
}
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #E5DDD5;
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #D4C8BC;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
