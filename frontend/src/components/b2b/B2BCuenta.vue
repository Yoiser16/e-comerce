<template>
  <div class="flex min-h-[calc(100vh-106px)] lg:min-h-[calc(100vh-106px)]">

    <!-- ==================== MOBILE VIEW (estilo Mercado Libre) ==================== -->
    <div class="lg:hidden w-full bg-[#FAFAFA]">
      
      <!-- Header con avatar centrado - SOLO en vista principal -->
      <div v-if="activeTab === 'profile'" class="bg-gradient-to-b from-[#C9A962] to-[#D4B574] pt-8 pb-12 px-4">
        <div class="flex flex-col items-center">
          <div class="w-20 h-20 rounded-full bg-white flex items-center justify-center shadow-lg mb-3">
            <span class="text-[#C9A962] text-2xl font-bold">{{ userInitials }}</span>
          </div>
          <h1 class="text-lg font-bold text-[#2C1810]">{{ user.nombre }}</h1>
          <p class="text-sm text-[#2C1810]/70">{{ user.email }}</p>
        </div>
      </div>
      
      <!-- Contenido -->
      <div :class="activeTab === 'profile' ? 'bg-white -mt-4 rounded-t-2xl min-h-[60vh]' : 'bg-white min-h-[80vh] pt-6'">
        
        <!-- Vista principal: Lista de opciones -->
        <div v-if="activeTab === 'profile'" class="py-2">
          <!-- Info personal -->
          <button 
            @click="activeTab = 'mydata'"
            class="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors border-b border-gray-100"
          >
            <svg class="w-5 h-5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/>
            </svg>
            <span class="flex-1 text-left text-[15px] text-gray-800">Tu información</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
            </svg>
          </button>
          
          <!-- Direcciones -->
          <button 
            @click="activeTab = 'addresses'"
            class="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors border-b border-gray-100"
          >
            <svg class="w-5 h-5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/>
            </svg>
            <span class="flex-1 text-left text-[15px] text-gray-800">Direcciones</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
            </svg>
          </button>
          
          <!-- Seguridad -->
          <button 
            @click="activeTab = 'security'"
            class="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors border-b border-gray-100"
          >
            <svg class="w-5 h-5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"/>
            </svg>
            <span class="flex-1 text-left text-[15px] text-gray-800">Seguridad</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
            </svg>
          </button>
          
          <!-- Mis Pedidos -->
          <button 
            @click="activeTab = 'pedidos'"
            class="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors border-b border-gray-100"
          >
            <svg class="w-5 h-5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/>
            </svg>
            <span class="flex-1 text-left text-[15px] text-gray-800">Mis Pedidos</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
            </svg>
          </button>
          
          <!-- Cupones -->
          <button 
            @click="activeTab = 'cupones'"
            class="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors border-b border-gray-100"
          >
            <svg class="w-5 h-5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 010 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 010-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375z"/>
            </svg>
            <span class="flex-1 text-left text-[15px] text-gray-800">Cupones</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
            </svg>
          </button>
          
          <!-- Comunicaciones -->
          <button 
            @click="activeTab = 'notifications'"
            class="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors border-b border-gray-100"
          >
            <svg class="w-5 h-5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"/>
            </svg>
            <span class="flex-1 text-left text-[15px] text-gray-800">Comunicaciones</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
            </svg>
          </button>
          
          <!-- Ayuda -->
          <a 
            href="https://wa.me/4796657763"
            target="_blank"
            class="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors border-b border-gray-100"
          >
            <svg class="w-5 h-5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z"/>
            </svg>
            <span class="flex-1 text-left text-[15px] text-gray-800">Ayuda</span>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"/>
            </svg>
          </a>
          
          <!-- Cerrar sesión -->
          <button 
            @click="logout"
            class="w-full flex items-center gap-4 px-5 py-4 hover:bg-gray-50 transition-colors mt-4"
          >
            <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9"/>
            </svg>
            <span class="flex-1 text-left text-[15px] text-red-500">Cerrar sesión</span>
          </button>
        </div>
        
        <!-- Vista de detalle móvil (cuando selecciona una opción) -->
        <div v-else class="px-4 py-3">
          <!-- Header con back button -->
          <button 
            @click="activeTab = 'profile'" 
            class="flex items-center gap-2 text-[14px] text-[#C9A962] font-medium mb-4"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
            </svg>
            Volver
          </button>
          
          <!-- MOBILE: Tu información -->
          <div v-if="activeTab === 'mydata'" class="space-y-4">
            <div class="flex items-center justify-between mb-2">
              <h2 class="text-lg font-bold text-gray-800">Tu información</h2>
              <button 
                v-if="!mobileEditMode"
                @click="mobileEditMode = true"
                class="text-[#C9A962] text-sm font-medium"
              >
                Editar
              </button>
              <button 
                v-else
                @click="mobileEditMode = false; saveProfile()"
                class="text-[#C9A962] text-sm font-medium"
              >
                Guardar
              </button>
            </div>
            
            <!-- MODO RESUMEN (solo lectura) -->
            <div v-if="!mobileEditMode" class="space-y-3">
              <!-- Datos Personales -->
              <div class="bg-white rounded-xl border border-gray-100 divide-y divide-gray-100">
                <div class="px-4 py-3">
                  <p class="text-xs text-gray-400 mb-0.5">Nombre completo</p>
                  <p class="text-[15px] text-gray-800">{{ user.nombre || 'Sin especificar' }}</p>
                </div>
                <div class="px-4 py-3">
                  <p class="text-xs text-gray-400 mb-0.5">Email</p>
                  <p class="text-[15px] text-gray-800">{{ user.email || 'Sin especificar' }}</p>
                </div>
                <div class="px-4 py-3">
                  <p class="text-xs text-gray-400 mb-0.5">Teléfono</p>
                  <p class="text-[15px] text-gray-800">{{ user.telefono || 'Sin especificar' }}</p>
                </div>
                <div class="px-4 py-3">
                  <p class="text-xs text-gray-400 mb-0.5">WhatsApp</p>
                  <p class="text-[15px] text-gray-800">{{ user.whatsapp || 'Sin especificar' }}</p>
                </div>
              </div>
              
              <!-- Datos Empresariales -->
              <div class="bg-white rounded-xl border border-gray-100">
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Información Empresarial</p>
                </div>
                <div class="divide-y divide-gray-100">
                  <div class="px-4 py-3">
                    <p class="text-xs text-gray-400 mb-0.5">Empresa</p>
                    <p class="text-[15px] text-gray-800">{{ user.empresa || 'Sin especificar' }}</p>
                  </div>
                  <div class="px-4 py-3">
                    <p class="text-xs text-gray-400 mb-0.5">NIT / Cédula</p>
                    <p class="text-[15px] text-gray-800">{{ user.nit || user.cedula || 'Sin especificar' }}</p>
                  </div>
                  <div class="px-4 py-3">
                    <p class="text-xs text-gray-400 mb-0.5">Tipo de negocio</p>
                    <p class="text-[15px] text-gray-800">{{ user.tipoNegocio || user.tipo_negocio || 'Sin especificar' }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- MODO EDICIÓN -->
            <div v-else class="space-y-3">
              <div class="bg-white rounded-xl border border-gray-100 p-4 space-y-4">
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Nombre Completo</label>
                  <input 
                    v-model="editForm.nombre"
                    type="text"
                    class="w-full h-11 px-3 text-sm text-gray-800 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C9A962] focus:border-transparent bg-gray-50"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Email</label>
                  <input 
                    :value="user.email"
                    type="email"
                    class="w-full h-11 px-3 text-sm text-gray-400 border border-gray-200 rounded-lg bg-gray-100"
                    disabled
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Teléfono</label>
                  <input 
                    v-model="editForm.telefono"
                    type="tel"
                    placeholder="+57 300 123 4567"
                    class="w-full h-11 px-3 text-sm text-gray-800 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C9A962] focus:border-transparent bg-gray-50"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">WhatsApp</label>
                  <input 
                    v-model="editForm.whatsapp"
                    type="tel"
                    placeholder="+57 300 123 4567"
                    class="w-full h-11 px-3 text-sm text-gray-800 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C9A962] focus:border-transparent bg-gray-50"
                  />
                </div>
              </div>
              
              <div class="bg-white rounded-xl border border-gray-100 p-4 space-y-4">
                <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Información Empresarial</p>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Nombre de la Empresa</label>
                  <input 
                    v-model="editForm.empresa"
                    type="text"
                    class="w-full h-11 px-3 text-sm text-gray-800 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C9A962] focus:border-transparent bg-gray-50"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">NIT / Cédula</label>
                  <input 
                    v-model="editForm.nit"
                    type="text"
                    class="w-full h-11 px-3 text-sm text-gray-800 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C9A962] focus:border-transparent bg-gray-50"
                  />
                </div>
              </div>
              
              <button 
                @click="cancelEdit"
                class="w-full py-3 text-gray-500 text-sm font-medium"
              >
                Cancelar
              </button>
            </div>
          </div>
          
          <!-- MOBILE: Direcciones -->
          <div v-if="activeTab === 'addresses'" class="space-y-4">
            <h2 class="text-lg font-bold text-gray-800 mb-3">Mis Direcciones</h2>
            
            <div v-if="addresses.length === 0" class="text-center py-8">
              <svg class="w-12 h-12 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/>
              </svg>
              <p class="text-gray-500 text-sm">No tienes direcciones guardadas</p>
            </div>
            
            <div v-for="addr in addresses" :key="addr.id" class="bg-white rounded-lg border border-gray-200 p-4">
              <div class="flex items-start justify-between">
                <div>
                  <p class="font-medium text-gray-800 text-sm">{{ addr.direccion }}</p>
                  <p class="text-gray-500 text-xs mt-1">{{ addr.ciudad }}, {{ addr.departamento }}</p>
                </div>
                <span v-if="addr.es_principal" class="text-xs px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded-full">Principal</span>
              </div>
            </div>
            
            <button 
              @click="showAddressModal = true"
              class="w-full py-3 border-2 border-dashed border-gray-300 text-gray-500 rounded-lg hover:border-[#C9A962] hover:text-[#C9A962] transition-colors text-sm font-medium"
            >
              + Agregar dirección
            </button>
          </div>
          
          <!-- MOBILE: Seguridad -->
          <div v-if="activeTab === 'security'" class="space-y-4">
            <h2 class="text-lg font-bold text-gray-800 mb-3">Seguridad</h2>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 space-y-4">
              <h3 class="font-semibold text-gray-700 text-sm">Cambiar contraseña</h3>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Contraseña actual</label>
                <input 
                  v-model="passwordForm.current"
                  type="password"
                  class="w-full h-10 px-3 text-sm text-gray-800 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C9A962] focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Nueva contraseña</label>
                <input 
                  v-model="passwordForm.new"
                  type="password"
                  class="w-full h-10 px-3 text-sm text-gray-800 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C9A962] focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Confirmar nueva contraseña</label>
                <input 
                  v-model="passwordForm.confirm"
                  type="password"
                  class="w-full h-10 px-3 text-sm text-gray-800 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C9A962] focus:border-transparent"
                />
              </div>
              <button 
                @click="changePassword"
                :disabled="changingPassword"
                class="w-full py-3 bg-[#C9A962] hover:bg-[#B8944D] text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
              >
                {{ changingPassword ? 'Actualizando...' : 'Actualizar contraseña' }}
              </button>
            </div>
          </div>
          
          <!-- MOBILE: Pedidos - Diseño mejorado con accordion -->
          <div v-if="activeTab === 'pedidos'" class="space-y-3">
            <!-- Header con contador -->
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-bold text-[#1A1A1A]">Mis Pedidos</h2>
              <span v-if="orders.length > 0" class="text-xs text-gray-400">{{ orders.length }} pedidos</span>
            </div>

            <!-- Loading -->
            <div v-if="isLoadingOrders" class="py-12 text-center">
              <svg class="w-6 h-6 text-[#C9A962] mx-auto mb-2 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <p class="text-sm text-gray-500">Cargando pedidos...</p>
            </div>
            
            <!-- Empty state -->
            <div v-else-if="orders.length === 0" class="text-center py-10 bg-white rounded-xl border border-gray-100">
              <div class="w-14 h-14 mx-auto mb-4 bg-[#FAF5F2] rounded-full flex items-center justify-center">
                <svg class="w-7 h-7 text-[#C9A962]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/>
                </svg>
              </div>
              <p class="text-[#1A1A1A] font-medium mb-1">No tienes pedidos aún</p>
              <p class="text-gray-400 text-sm mb-4">Explora nuestro catálogo y haz tu primer pedido</p>
              <router-link to="/portal/catalogo" class="inline-flex items-center gap-2 px-5 py-2.5 bg-[#1A1A1A] text-white text-sm font-medium rounded-xl">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/></svg>
                Explorar catálogo
              </router-link>
            </div>
            
            <!-- Orders list with accordion -->
            <div 
              v-for="order in orders" 
              :key="order.id" 
              class="bg-white rounded-xl border overflow-hidden transition-all duration-200"
              :class="expandedOrderId === order.id ? 'border-[#C9A962]/30 shadow-sm' : 'border-gray-100'"
            >
              <!-- Order Header (clickable) -->
              <div 
                @click="toggleOrderDetail(order)"
                class="p-4 cursor-pointer active:bg-gray-50"
              >
                <div class="flex gap-3">
                  <!-- Product Image -->
                  <div class="w-14 h-14 rounded-lg bg-gray-100 overflow-hidden flex-shrink-0">
                    <img
                      v-if="getOrderMediaUrl(order.products?.[0])"
                      :src="getOrderMediaUrl(order.products?.[0])"
                      :alt="order.products?.[0]?.name"
                      class="w-full h-full object-cover"
                      @error="$event.target.style.display='none'"
                    />
                    <div class="w-full h-full flex items-center justify-center">
                      <svg class="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
                    </div>
                  </div>

                  <!-- Order Info -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-start justify-between gap-2">
                      <div class="min-w-0">
                        <!-- Status badge -->
                        <span :class="[
                          'inline-flex items-center gap-1 text-xs font-medium mb-1',
                          order.status === 'Entregado' ? 'text-emerald-600' : 
                          order.status === 'En Camino' ? 'text-blue-600' : 
                          order.status === 'Pagada' ? 'text-green-600' : 
                          order.status === 'Pendiente' ? 'text-amber-600' : 'text-gray-500'
                        ]">
                          <span :class="[
                            'w-1.5 h-1.5 rounded-full',
                            order.status === 'Entregado' ? 'bg-emerald-500' : 
                            order.status === 'En Camino' ? 'bg-blue-500' : 
                            order.status === 'Pagada' ? 'bg-green-500' : 
                            order.status === 'Pendiente' ? 'bg-amber-500' : 'bg-gray-400'
                          ]"></span>
                          {{ order.status }}
                        </span>
                        <!-- Order number -->
                        <p class="text-sm font-semibold text-[#1A1A1A] truncate">{{ order.numero }}</p>
                        <!-- Date and items -->
                        <p class="text-xs text-gray-400 mt-0.5">{{ order.date }} · {{ order.items }} productos</p>
                      </div>
                      <!-- Total + Arrow -->
                      <div class="text-right flex-shrink-0">
                        <p class="text-base font-bold text-[#1A1A1A]">${{ formatPrice(order.total) }}</p>
                        <svg 
                          :class="[
                            'w-4 h-4 text-gray-300 mt-1 mx-auto transition-transform duration-200',
                            expandedOrderId === order.id ? 'rotate-180 text-[#C9A962]' : ''
                          ]" 
                          fill="none" stroke="currentColor" viewBox="0 0 24 24"
                        >
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Expanded Details (accordion) -->
              <div v-if="expandedOrderId === order.id" class="border-t border-gray-100 bg-[#FAFAFA]">
                <!-- Products -->
                <div class="p-4 space-y-2">
                  <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Productos</p>
                  <div v-for="(item, idx) in order.products" :key="idx" class="flex gap-3 p-3 bg-white rounded-lg">
                    <div class="w-11 h-11 rounded-md bg-gray-100 overflow-hidden flex-shrink-0">
                      <img
                        v-if="getOrderMediaUrl(item)"
                        :src="getOrderMediaUrl(item)"
                        :alt="item.name"
                        class="w-full h-full object-cover"
                        @error="$event.target.style.display='none'"
                      />
                    </div>
                    <div class="flex-1 min-w-0">
                      <h4 class="text-sm font-medium text-[#1A1A1A] line-clamp-1">{{ item.name }}</h4>
                      <p class="text-xs text-gray-400">{{ item.quantity }} × ${{ formatPrice(item.price) }}</p>
                    </div>
                    <div class="text-right">
                      <p class="text-sm font-semibold text-[#1A1A1A]">${{ formatPrice(item.price * item.quantity) }}</p>
                    </div>
                  </div>
                </div>

                <!-- Summary -->
                <div class="px-4 pb-3">
                  <div class="bg-white rounded-lg p-3 space-y-1.5">
                    <div class="flex justify-between text-xs text-gray-500">
                      <span>Subtotal</span>
                      <span>${{ formatPrice(order.subtotal || order.total) }}</span>
                    </div>
                    <div class="flex justify-between text-xs text-gray-500">
                      <span>Envío</span>
                      <span>{{ order.envio ? `$${formatPrice(order.envio)}` : 'Gratis' }}</span>
                    </div>
                    <div class="flex justify-between text-sm font-bold text-[#1A1A1A] pt-2 border-t border-gray-100">
                      <span>Total</span>
                      <span>${{ formatPrice(order.total) }}</span>
                    </div>
                  </div>
                </div>

                <!-- Info extras -->
                <div class="px-4 pb-3">
                  <div class="flex flex-wrap gap-3 text-[10px] text-gray-400">
                    <span class="flex items-center gap-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/></svg>
                      {{ order.metodoPago === 'wompi' ? 'Pago online' : 'WhatsApp' }}
                    </span>
                    <span class="flex items-center gap-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                      {{ order.date }}
                    </span>
                  </div>
                </div>

                <!-- Actions -->
                <div class="px-4 pb-4 flex gap-2">
                  <button 
                    v-if="order.status === 'Entregado'"
                    @click.stop="reorderItems(order)"
                    class="flex-1 py-2.5 text-xs font-medium text-[#C9A962] bg-[#FAF5F2] rounded-lg hover:bg-[#C9A962]/20 transition-colors"
                  >
                    Volver a comprar
                  </button>
                  <a 
                    href="https://wa.me/4796657763"
                    target="_blank"
                    class="flex-1 py-2.5 text-xs font-medium text-gray-600 bg-white border border-gray-200 rounded-lg text-center hover:bg-gray-50 transition-colors"
                  >
                    Consultar
                  </a>
                </div>
              </div>
            </div>
          </div>
          
          <!-- MOBILE: Cupones -->
          <div v-if="activeTab === 'cupones'" class="space-y-4">
            <h2 class="text-lg font-bold text-gray-800 mb-3">Mis Cupones</h2>
            
            <div v-if="!cuponesActivos || cuponesActivos.length === 0" class="text-center py-8">
              <svg class="w-12 h-12 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 010 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 010-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375z"/>
              </svg>
              <p class="text-gray-500 text-sm">No tienes cupones disponibles</p>
            </div>
            
            <div v-for="coupon in cuponesActivos" :key="coupon.id" class="bg-white rounded-lg border border-gray-200 p-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="font-bold text-[#C9A962] text-lg">{{ coupon.codigo }}</p>
                  <p class="text-gray-500 text-xs">{{ coupon.descripcion }}</p>
                </div>
                <span class="text-lg font-bold text-gray-800">{{ coupon.descuento }}%</span>
              </div>
            </div>
          </div>
          
          <!-- MOBILE: Comunicaciones -->
          <div v-if="activeTab === 'notifications'" class="space-y-4">
            <h2 class="text-lg font-bold text-gray-800 mb-3">Comunicaciones</h2>
            
            <div class="bg-white rounded-lg border border-gray-200 p-4 space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-800 text-sm">Ofertas por email</p>
                  <p class="text-gray-500 text-xs">Recibe promociones exclusivas</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="notificationSettings.offers" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C9A962]"></div>
                </label>
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-800 text-sm">Estado de pedidos</p>
                  <p class="text-gray-500 text-xs">Notificaciones de envío</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="notificationSettings.orders" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C9A962]"></div>
                </label>
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-800 text-sm">Nuevos productos</p>
                  <p class="text-gray-500 text-xs">Aviso de lanzamientos</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="notificationSettings.newProducts" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#C9A962]"></div>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== DESKTOP VIEW (original) ==================== -->
    <!-- SIDEBAR FIXED LEFT (like MercadoLibre) -->
    <aside class="hidden lg:block w-[240px] flex-shrink-0 border-r border-[#e0e0e0] bg-white">
      <div class="sticky top-[106px] py-6 px-5">
        <h2 class="text-[15px] font-bold text-[#333] mb-5">Mi cuenta</h2>
        <nav class="space-y-0.5">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'w-full flex items-center gap-2.5 px-3 py-2 text-left transition-colors text-[14px] rounded-md',
              (activeTab === tab.id || (tab.id === 'profile' && activeTab === 'mydata'))
                ? 'text-[#2563eb] font-semibold bg-[#eff4ff]' 
                : 'text-[#555] hover:bg-[#f5f5f5] hover:text-[#333] font-normal'
            ]"
          >
            <span v-html="tab.icon" :class="['w-[18px] h-[18px]', (activeTab === tab.id || (tab.id === 'profile' && activeTab === 'mydata')) ? 'text-[#2563eb]' : 'text-[#999]']"></span>
            {{ tab.label }}
          </button>

          <!-- Separator -->
          <div class="!my-3 border-t border-[#e8e8e8]"></div>

          <!-- Pedidos y Cupones como tabs internos -->
          <button 
            v-for="link in sidebarLinks"
            :key="link.id"
            @click="activeTab = link.id"
            :class="[
              'w-full flex items-center gap-2.5 px-3 py-2 text-left transition-colors text-[14px] rounded-md',
              activeTab === link.id
                ? 'text-[#2563eb] font-semibold bg-[#eff4ff]' 
                : 'text-[#555] hover:bg-[#f5f5f5] hover:text-[#333] font-normal'
            ]"
          >
            <span v-html="link.icon" :class="['w-[18px] h-[18px]', activeTab === link.id ? 'text-[#2563eb]' : 'text-[#999]']"></span>
            {{ link.label }}
          </button>
        </nav>
      </div>
    </aside>

    <!-- ==================== MAIN CONTENT AREA (DESKTOP ONLY) ==================== -->
    <div class="hidden lg:block flex-1 min-w-0">
      <div class="max-w-[960px] mx-auto px-5 sm:px-8 py-6 lg:py-8">

        <!-- Avatar + Name (like MercadoLibre - circular) -->
        <div class="flex items-center gap-4 mb-6">
          <div class="w-14 h-14 rounded-full bg-[#e8e8e8] flex items-center justify-center flex-shrink-0 border-2 border-[#d0d0d0]">
            <span class="text-[#666] text-lg font-bold">{{ userInitials }}</span>
          </div>
          <div>
            <h1 class="text-xl font-bold text-[#333]">{{ user.nombre }}</h1>
            <p class="text-[14px] text-[#666]">{{ user.email }}</p>
          </div>
        </div>

        <!-- Verification Banner -->
        <div v-if="!isEmailVerified && !verificationDismissed" class="mb-6 flex items-center gap-3 bg-white border border-[#e0e0e0] rounded-lg px-5 py-3.5" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
          <div class="w-1 h-8 bg-[#f97316] rounded-full flex-shrink-0"></div>
          <div class="flex items-center gap-3 flex-1 min-w-0">
            <svg class="w-5 h-5 text-[#666] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            <p class="text-[14px] text-[#333]">Valida tu e-mail y mantén tu cuenta segura</p>
          </div>
          <button 
            @click="sendVerificationEmail"
            class="flex-shrink-0 h-[34px] px-4 text-[13px] font-semibold text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md transition-colors"
          >
            Validar
          </button>
          <button @click="dismissVerification" class="flex-shrink-0 text-[#999] hover:text-[#555] p-1 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <!-- Default View: Summary Cards ONLY (like MercadoLibre) -->
        <div v-if="activeTab === 'profile'">
          <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <button 
              @click="activeTab = 'mydata'" 
              class="bg-white rounded-lg border border-[#e0e0e0] p-5 text-left hover:border-[#2563eb]/40 hover:shadow-md transition-all group cursor-pointer"
              style="box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);"
            >
              <svg class="w-7 h-7 text-[#666] group-hover:text-[#2563eb] transition-colors mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              <h3 class="text-[15px] font-semibold text-[#333] mb-1">Mis datos</h3>
              <p class="text-[13px] text-[#666] leading-relaxed">Nombre, teléfono y datos de contacto.</p>
            </button>
            <button 
              @click="activeTab = 'addresses'" 
              class="bg-white rounded-lg border border-[#e0e0e0] p-5 text-left hover:border-[#2563eb]/40 hover:shadow-md transition-all group cursor-pointer"
              style="box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);"
            >
              <svg class="w-7 h-7 text-[#666] group-hover:text-[#2563eb] transition-colors mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/></svg>
              <h3 class="text-[15px] font-semibold text-[#333] mb-1">Direcciones</h3>
              <p class="text-[13px] text-[#666] leading-relaxed">Direcciones de envío guardadas.</p>
            </button>
            <button 
              @click="activeTab = 'security'" 
              class="bg-white rounded-lg border border-[#e0e0e0] p-5 text-left hover:border-[#2563eb]/40 hover:shadow-md transition-all group cursor-pointer"
              style="box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);"
            >
              <svg class="w-7 h-7 text-[#666] group-hover:text-[#2563eb] transition-colors mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              <h3 class="text-[15px] font-semibold text-[#333] mb-1">Seguridad</h3>
              <p class="text-[13px] text-[#666] leading-relaxed">Contraseña y configuraciones de acceso.</p>
            </button>
            <button 
              @click="activeTab = 'notifications'" 
              class="bg-white rounded-lg border border-[#e0e0e0] p-5 text-left hover:border-[#2563eb]/40 hover:shadow-md transition-all group cursor-pointer"
              style="box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);"
            >
              <svg class="w-7 h-7 text-[#666] group-hover:text-[#2563eb] transition-colors mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
              <h3 class="text-[15px] font-semibold text-[#333] mb-1">Comunicaciones</h3>
              <p class="text-[13px] text-[#666] leading-relaxed">Elige qué notificaciones recibir.</p>
            </button>
            <button 
              @click="activeTab = 'mydata'"
              class="bg-white rounded-lg border border-[#e0e0e0] p-5 text-left hover:border-[#2563eb]/40 hover:shadow-md transition-all group cursor-pointer"
              style="box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);"
            >
              <svg class="w-7 h-7 text-[#666] group-hover:text-[#2563eb] transition-colors mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
              <h3 class="text-[15px] font-semibold text-[#333] mb-1">Datos Empresariales</h3>
              <p class="text-[13px] text-[#666] leading-relaxed">NIT, empresa y tipo de negocio.</p>
            </button>
          </div>
        </div>

        <!-- Tab: Mis Datos (form only when clicked) -->
        <div v-if="activeTab === 'mydata'" class="space-y-6">

          <!-- Back link -->
          <button @click="activeTab = 'profile'" class="flex items-center gap-1.5 text-[13px] text-[#2563eb] hover:text-[#1d4ed8] font-medium transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            Volver a Mi Cuenta
          </button>
          <div class="bg-white rounded-md border border-[#e0e0e0]" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="px-6 py-4 border-b border-[#e8e8e8]">
              <h3 class="text-[15px] font-bold text-[#333]">Información Personal</h3>
            </div>
            <div class="px-6 py-5">
              <div class="grid sm:grid-cols-2 gap-x-6 gap-y-5">
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">Nombre Completo</label>
                  <input 
                    v-model="editForm.nombre"
                    type="text"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white"
                  />
                </div>
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">Email</label>
                  <input 
                    v-model="editForm.email"
                    type="email"
                    class="w-full h-[38px] px-3 text-[14px] text-[#999] border border-[#e0e0e0] rounded-md bg-[#fafafa] cursor-not-allowed"
                    disabled
                  />
                  <p class="text-[11px] text-[#999] mt-1">El email no puede modificarse</p>
                </div>
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">Teléfono</label>
                  <input 
                    v-model="editForm.telefono"
                    type="tel"
                    placeholder="+57 300 123 4567"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
                  />
                </div>
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">WhatsApp</label>
                  <input 
                    v-model="editForm.whatsapp"
                    type="tel"
                    placeholder="+57 300 123 4567"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Business Info Form -->
          <div class="bg-white rounded-md border border-[#e0e0e0]" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="px-6 py-4 border-b border-[#e8e8e8]">
              <h3 class="text-[15px] font-bold text-[#333]">Información Empresarial</h3>
            </div>
            <div class="px-6 py-5">
              <div class="grid sm:grid-cols-2 gap-x-6 gap-y-5">
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">Nombre de la Empresa</label>
                  <input 
                    v-model="editForm.empresa"
                    type="text"
                    placeholder="Mi Salón de Belleza"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
                  />
                </div>
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">NIT / RUT</label>
                  <input 
                    v-model="editForm.nit"
                    type="text"
                    placeholder="900.123.456-7"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
                  />
                </div>
                <div class="sm:col-span-2">
                  <label class="block text-[12px] font-medium text-[#333] mb-1">Tipo de Negocio</label>
                  <select 
                    v-model="editForm.tipoNegocio"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white"
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
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end gap-4">
            <button 
              @click="activeTab = 'profile'"
              class="h-[36px] px-4 text-[13px] font-medium text-[#555] border border-[#ccc] rounded-md hover:bg-[#f5f5f5] transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="saveProfile"
              class="h-[36px] px-5 text-[13px] font-medium text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md transition-colors"
            >
              Guardar Cambios
            </button>
          </div>
        </div>

        <!-- Tab: Direcciones -->
        <div v-if="activeTab === 'addresses'">
          <div class="bg-white rounded-md border border-[#e0e0e0]" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="px-6 py-4 border-b border-[#e8e8e8] flex items-center justify-between">
              <h3 class="text-[15px] font-bold text-[#333]">Direcciones de Envío</h3>
              <button 
                @click="openAddressModal()"
                class="h-[34px] px-3.5 text-[13px] font-medium text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md transition-colors flex items-center gap-1.5"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
                </svg>
                Agregar
              </button>
            </div>

            <div class="px-6 py-5">
              <!-- Loading state -->
              <div v-if="loadingAddresses" class="py-8 text-center">
                <svg class="w-6 h-6 text-[#2563eb] mx-auto mb-2 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                <p class="text-[13px] text-[#999]">Cargando direcciones...</p>
              </div>

              <!-- Addresses list -->
              <div v-else-if="addresses.length > 0" class="divide-y divide-[#e8e8e8]">
                <div 
                  v-for="address in addresses" 
                  :key="address.id"
                  class="py-4 first:pt-0 last:pb-0 flex items-start justify-between gap-5"
                >
                  <div class="flex gap-3 flex-1 min-w-0">
                    <svg class="w-4.5 h-4.5 text-[#999] mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    <div class="min-w-0">
                      <div class="flex items-center gap-2 mb-0.5">
                        <h4 class="text-[14px] font-semibold text-[#333]">{{ address.etiqueta }}</h4>
                        <span v-if="address.is_default" class="text-[10px] px-1.5 py-px bg-[#2563eb] text-white rounded font-medium">Principal</span>
                      </div>
                      <p class="text-[13px] text-[#555]">
                        {{ address.direccion }}<span v-if="address.complemento"> · {{ address.complemento }}</span>
                      </p>
                      <p class="text-[12px] text-[#999]">{{ address.municipio }}, {{ address.departamento }} · {{ address.telefono }}</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-0.5 flex-shrink-0">
                    <button 
                      v-if="!address.is_default"
                      @click="setDefaultAddress(address.id)"
                      class="p-1.5 text-[#bbb] hover:text-[#2563eb] rounded transition-colors"
                      title="Marcar como principal"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                      </svg>
                    </button>
                    <button 
                      @click="openAddressModal(address)"
                      class="p-1.5 text-[#bbb] hover:text-[#555] rounded transition-colors"
                      title="Editar"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                    </button>
                    <button 
                      @click="deleteAddress(address.id)"
                      class="p-1.5 text-[#bbb] hover:text-red-500 rounded transition-colors"
                      title="Eliminar"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Empty state -->
              <div v-else class="text-center py-10">
                <svg class="w-8 h-8 text-[#ccc] mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                </svg>
                <h4 class="text-[14px] font-semibold text-[#333] mb-0.5">No hay direcciones guardadas</h4>
                <p class="text-[12px] text-[#999] mb-3">Agrega una dirección para agilizar tus pedidos</p>
                <button 
                  @click="openAddressModal()"
                  class="text-[13px] text-[#2563eb] hover:text-[#1d4ed8] font-medium"
                >
                  + Agregar primera dirección
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Seguridad -->
        <div v-if="activeTab === 'security'">
          <div class="bg-white rounded-md border border-[#e0e0e0]" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="px-6 py-4 border-b border-[#e8e8e8]">
              <h3 class="text-[15px] font-bold text-[#333]">Cambiar Contraseña</h3>
            </div>
            <div class="px-6 py-5">
              <div class="max-w-md space-y-5">
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">Contraseña Actual</label>
                  <input 
                    v-model="passwordForm.current"
                    type="password"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white"
                  />
                </div>
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">Nueva Contraseña</label>
                  <input 
                    v-model="passwordForm.new"
                    type="password"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white"
                  />
                  <p class="text-[11px] text-[#999] mt-1">Mínimo 8 caracteres, incluye mayúsculas y números</p>
                </div>
                <div>
                  <label class="block text-[12px] font-medium text-[#333] mb-1">Confirmar Nueva Contraseña</label>
                  <input 
                    v-model="passwordForm.confirm"
                    type="password"
                    class="w-full h-[38px] px-3 text-[14px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white"
                  />
                </div>
                <div>
                  <button 
                    @click="changePassword"
                    :disabled="changingPassword"
                    class="h-[36px] px-5 text-[13px] font-medium text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ changingPassword ? 'Actualizando...' : 'Actualizar Contraseña' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Notificaciones -->
        <div v-if="activeTab === 'notifications'">
          <div class="bg-white rounded-md border border-[#e0e0e0]" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="px-6 py-4 border-b border-[#e8e8e8]">
              <h3 class="text-[15px] font-bold text-[#333]">Preferencias de Notificaciones</h3>
            </div>
            <div class="divide-y divide-[#e8e8e8]">
              <div 
                v-for="pref in notificationPrefs" 
                :key="pref.id"
                class="flex items-center justify-between px-6 py-4"
              >
                <div class="pr-4">
                  <h4 class="text-[14px] font-medium text-[#333]">{{ pref.label }}</h4>
                  <p class="text-[12px] text-[#999] mt-0.5">{{ pref.description }}</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer flex-shrink-0">
                  <input type="checkbox" v-model="pref.enabled" class="sr-only peer">
                  <div class="w-9 h-5 bg-[#ccc] peer-focus:ring-2 peer-focus:ring-[#2563eb]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:shadow-sm after:transition-all peer-checked:bg-[#2563eb]"></div>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Mis Pedidos (Estilo Mercado Libre - Clean) -->
        <div v-if="activeTab === 'pedidos'">
          <!-- Header Simple -->
          <div class="mb-6">
            <h2 class="text-[22px] font-semibold text-[#333] mb-1">Compras</h2>
            <p class="text-[14px] text-[#666]">Revisa el estado de tus pedidos y haz seguimiento de tus envíos</p>
          </div>

          <!-- Filtros estilo tabs simples + búsqueda -->
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 pb-4 border-b border-[#e8e8e8]">
            <div class="flex items-center gap-1 overflow-x-auto pb-1 sm:pb-0">
              <button 
                v-for="status in ordersStatuses" 
                :key="status.value"
                @click="selectedStatus = status.value"
                :class="[
                  'px-4 py-2 text-[14px] font-medium transition-all whitespace-nowrap rounded-full',
                  selectedStatus === status.value 
                    ? 'bg-[#2563eb] text-white' 
                    : 'text-[#666] hover:bg-[#f5f5f5]'
                ]"
              >
                {{ status.label }}
              </button>
            </div>
            <div class="relative">
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#999]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              <input 
                v-model="searchQuery"
                type="text"
                placeholder="Buscar en compras"
                class="w-full sm:w-48 h-[40px] pl-10 pr-4 text-[14px] border border-[#ddd] rounded-full focus:outline-none focus:border-[#2563eb] bg-white"
              />
            </div>
          </div>

          <!-- Loading Orders -->
          <div v-if="isLoadingOrders" class="py-12 text-center">
            <svg class="w-6 h-6 text-[#2563eb] mx-auto mb-2 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <p class="text-[13px] text-[#666]">Cargando pedidos...</p>
          </div>

          <!-- Orders List - Accordion style -->
          <div v-else-if="filteredOrders.length > 0" class="space-y-3">
            <div 
              v-for="order in filteredOrders" 
              :key="order.id"
              class="bg-white rounded-lg border border-[#e5e5e5] overflow-hidden transition-all"
              :class="expandedOrderId === order.id ? 'shadow-md border-[#d0d0d0]' : 'hover:shadow-sm'"
            >
              <!-- Order Summary Row (clickable) -->
              <div 
                @click="toggleOrderDetail(order)"
                class="p-4 cursor-pointer group"
              >
                <div class="flex items-start gap-4">
                  <!-- Product Image -->
                  <div class="flex-shrink-0 relative">
                    <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-lg bg-[#f5f5f5] overflow-hidden">
                      <video
                        v-if="isVideo(getOrderMediaUrl(order.products?.[0]))"
                        :src="getOrderMediaUrl(order.products?.[0])"
                        class="w-full h-full object-cover"
                        muted
                        playsinline
                        preload="metadata"
                      />
                      <img
                        v-else-if="getOrderMediaUrl(order.products?.[0])"
                        :src="getOrderMediaUrl(order.products?.[0])"
                        :alt="order.products?.[0]?.name"
                        class="w-full h-full object-cover"
                        @error="$event.target.style.display='none'; $event.target.nextElementSibling && ($event.target.nextElementSibling.style.display='flex')"
                      />
                      <div v-else class="w-full h-full flex items-center justify-center">
                        <svg class="w-8 h-8 text-[#ccc]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
                      </div>
                      <div
                        v-if="getOrderMediaUrl(order.products?.[0]) && !isVideo(getOrderMediaUrl(order.products?.[0]))"
                        class="w-full h-full items-center justify-center"
                        style="display:none"
                      >
                        <svg class="w-8 h-8 text-[#ccc]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
                      </div>
                    </div>
                    <span v-if="order.items > 1" class="absolute -bottom-1 -right-1 bg-white border border-[#e0e0e0] text-[10px] text-[#666] font-medium px-1.5 py-0.5 rounded-full shadow-sm">
                      +{{ order.items - 1 }}
                    </span>
                  </div>

                  <!-- Order Info -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-start justify-between gap-3">
                      <div class="min-w-0">
                        <!-- Status Badge -->
                        <div class="flex items-center gap-2 mb-1.5">
                          <span :class="[
                            'inline-flex items-center gap-1 text-[13px] font-medium',
                            order.status === 'Entregado' ? 'text-emerald-600' : 
                            order.status === 'En Camino' ? 'text-blue-600' : 
                            order.status === 'Pagada' ? 'text-green-600' : 
                            order.status === 'Pendiente' ? 'text-amber-600' : 'text-[#666]'
                          ]">
                            <span v-if="order.status === 'Entregado'" class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                            <span v-else-if="order.status === 'En Camino'" class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
                            <span v-else-if="order.status === 'Pagada'" class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                            <span v-else-if="order.status === 'Pendiente'" class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                            <span v-else class="w-1.5 h-1.5 rounded-full bg-[#999]"></span>
                            {{ order.status }}
                            <span v-if="order.metodoPago === 'wompi'" class="text-[10px] text-[#999] font-normal ml-1">· Wompi</span>
                          </span>
                        </div>
                        
                        <!-- Product name or order summary -->
                        <p class="text-[15px] text-[#333] font-medium mb-0.5 truncate">
                          {{ order.products?.[0]?.name || `Pedido ${order.numero}` }}
                        </p>
                        
                        <!-- Order metadata -->
                        <p class="text-[13px] text-[#999]">
                          {{ order.numero }} · {{ order.date }} · {{ order.items }} {{ order.items === 1 ? 'producto' : 'productos' }}
                        </p>
                      </div>
                      
                      <!-- Price + Arrow -->
                      <div class="text-right flex-shrink-0 flex items-start gap-2">
                        <div>
                          <p class="text-[16px] font-semibold text-[#333]">${{ formatPrice(order.total) }}</p>
                        </div>
                        <svg 
                          :class="[
                            'w-5 h-5 text-[#ccc] flex-shrink-0 hidden sm:block transition-all duration-300',
                            expandedOrderId === order.id ? 'rotate-90 text-[#2563eb]' : 'group-hover:text-[#2563eb]'
                          ]" 
                          fill="none" stroke="currentColor" viewBox="0 0 24 24"
                        >
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </div>
                    
                    <!-- Ver detalle link -->
                    <div class="mt-2">
                      <span class="text-[13px] text-[#2563eb] font-medium">
                        {{ expandedOrderId === order.id ? 'Ocultar detalle' : 'Ver detalle' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Expanded Detail (accordion) -->
              <div 
                v-if="expandedOrderId === order.id" 
                class="border-t border-[#e8e8e8] animate-slideDown"
              >
                <!-- Products List -->
                <div class="p-4 space-y-2">
                  <p class="text-[12px] font-semibold text-[#888] uppercase tracking-wider mb-3">Productos del pedido</p>
                  <div v-for="(item, idx) in order.products" :key="idx" class="flex gap-3 p-3 bg-[#fafafa] rounded-lg">
                    <div class="w-14 h-14 rounded-md bg-[#f0f0f0] overflow-hidden flex-shrink-0">
                      <video
                        v-if="isVideo(getOrderMediaUrl(item))"
                        :src="getOrderMediaUrl(item)"
                        class="w-full h-full object-cover"
                        muted
                        playsinline
                        preload="metadata"
                      />
                      <img
                        v-else-if="getOrderMediaUrl(item)"
                        :src="getOrderMediaUrl(item)"
                        :alt="item.name"
                        class="w-full h-full object-cover"
                        @error="$event.target.style.display='none'"
                      />
                      <div v-else class="w-full h-full flex items-center justify-center">
                        <svg class="w-6 h-6 text-[#ccc]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <h4 class="text-[14px] font-medium text-[#333]">{{ item.name }}</h4>
                      <p class="text-[12px] text-[#888]">Cantidad: {{ item.quantity }} · ${{ formatPrice(item.price) }}/ud</p>
                    </div>
                    <div class="text-right flex-shrink-0">
                      <p class="text-[14px] font-semibold text-[#333]">${{ formatPrice(item.price * item.quantity) }}</p>
                    </div>
                  </div>
                </div>

                <!-- Order Summary -->
                <div class="px-4 pb-4">
                  <div class="bg-[#fafafa] rounded-lg p-4 space-y-2">
                    <div class="flex justify-between text-[13px] text-[#666]">
                      <span>Subtotal</span>
                      <span>${{ formatPrice(order.subtotal || order.total) }}</span>
                    </div>
                    <div class="flex justify-between text-[13px] text-[#666]">
                      <span>Envío</span>
                      <span>{{ order.envio ? `$${formatPrice(order.envio)}` : 'Gratis' }}</span>
                    </div>
                    <div class="flex justify-between text-[15px] font-bold text-[#333] pt-2 border-t border-[#e5e5e5]">
                      <span>Total</span>
                      <span>${{ formatPrice(order.total) }}</span>
                    </div>
                  </div>
                </div>

                <!-- Payment & Order Info -->
                <div class="px-4 pb-4">
                  <div class="flex flex-wrap gap-4 text-[12px] text-[#888]">
                    <div class="flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
                      <span>{{ order.metodoPago === 'wompi' ? 'Pago en línea (Wompi)' : 'Pago por WhatsApp' }}</span>
                    </div>
                    <div class="flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                      <span>{{ order.date }}</span>
                    </div>
                    <div class="flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" /></svg>
                      <span>{{ order.numero }}</span>
                    </div>
                  </div>
                </div>

                <!-- Actions -->
                <div class="px-4 pb-4 flex items-center gap-3">
                  <button v-if="order.status === 'Entregado'" @click.stop="reorderItems(order)" class="text-[13px] text-[#2563eb] hover:underline font-medium">
                    Volver a comprar
                  </button>
                  <button v-if="order.tracking" @click.stop="trackOrder(order)" class="text-[13px] text-[#2563eb] hover:underline font-medium">
                    Seguir envío
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State - Estilo Mercado Libre -->
          <div v-else class="py-16 sm:py-24">
            <div class="max-w-[400px] mx-auto text-center px-4">
              <!-- Ilustración grande estilo ML -->
              <div class="mb-8 relative">
                <svg class="w-40 h-40 mx-auto text-[#e0e0e0]" viewBox="0 0 200 200" fill="none">
                  <!-- Laptop base -->
                  <rect x="30" y="140" width="140" height="8" rx="2" fill="#d5d5d5"/>
                  <!-- Laptop screen -->
                  <rect x="40" y="70" width="120" height="75" rx="4" fill="#f5f5f5" stroke="#d5d5d5" stroke-width="2"/>
                  <!-- Screen content - search icon -->
                  <circle cx="100" cy="105" r="18" stroke="#c0c0c0" stroke-width="3" fill="none"/>
                  <text x="100" y="112" text-anchor="middle" fill="#c0c0c0" font-size="20">?</text>
                  <line x1="113" y1="118" x2="125" y2="130" stroke="#c0c0c0" stroke-width="3" stroke-linecap="round"/>
                  <!-- Cursor/pencil icon -->
                  <g transform="translate(130, 60)">
                    <rect x="0" y="0" width="30" height="30" rx="4" fill="#FFE082"/>
                    <path d="M8 18 L15 6 L22 18" stroke="#F9A825" stroke-width="2" fill="none" stroke-linecap="round"/>
                    <circle cx="15" cy="10" r="2" fill="#F9A825"/>
                  </g>
                </svg>
              </div>
              
              <h3 class="text-[20px] sm:text-[22px] font-semibold text-[#333] mb-3">
                {{ selectedStatus === 'all' ? '¡Haz tu primera compra!' : `No tienes compras "${getStatusLabel(selectedStatus)}"` }}
              </h3>
              <p class="text-[15px] text-[#666] leading-relaxed mb-6">
                {{ selectedStatus === 'all' 
                  ? 'Aquí podrás ver tus compras y hacer el seguimiento de tus envíos.' 
                  : 'Prueba seleccionando otro filtro o explora nuestros productos.' 
                }}
              </p>
              <router-link 
                to="/portal/catalogo" 
                class="inline-flex items-center gap-2 text-[15px] text-[#2563eb] hover:text-[#1d4ed8] font-medium transition-colors"
              >
                {{ selectedStatus === 'all' ? 'Ver ofertas del día' : 'Explorar catálogo' }}
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Tab: Cupones -->
        <div v-if="activeTab === 'cupones'">
          <!-- Canjear Cupón -->
          <div class="bg-white rounded-md border border-[#e0e0e0] p-5 mb-5" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
              <div class="flex items-center gap-3 flex-1 min-w-0">
                <div class="w-10 h-10 rounded-full bg-[#eff4ff] flex items-center justify-center flex-shrink-0">
                  <svg class="w-5 h-5 text-[#2563eb]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
                </div>
                <div>
                  <h3 class="text-[15px] font-semibold text-[#333]">¿Tienes un código de cupón?</h3>
                  <p class="text-[13px] text-[#666]">Ingresa tu código para aplicar el descuento</p>
                </div>
              </div>
              <div class="flex items-center gap-2 w-full sm:w-auto">
                <input v-model="cuponCode" type="text" placeholder="CÓDIGO" class="flex-1 sm:w-32 h-[36px] px-3 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white uppercase" @keydown.enter="aplicarCupon" />
                <button @click="aplicarCupon" :disabled="!cuponCode || aplicandoCupon" class="h-[36px] px-4 text-[13px] font-semibold text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap">
                  {{ aplicandoCupon ? 'Validando...' : 'Aplicar' }}
                </button>
              </div>
            </div>
            <transition name="fade">
              <div v-if="cuponFeedback" :class="['mt-4 p-3 rounded-md text-[13px]', cuponFeedback.success ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200']">
                {{ cuponFeedback.message }}
              </div>
            </transition>
          </div>

          <!-- Mis Cupones Disponibles -->
          <div class="bg-white rounded-md border border-[#e0e0e0] overflow-hidden mb-5" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="px-5 py-4 border-b border-[#e8e8e8] flex items-center justify-between">
              <h3 class="text-[15px] font-bold text-[#333]">Mis Cupones Disponibles</h3>
              <span class="text-[13px] text-[#666]">{{ cuponesActivos.length }} activos</span>
            </div>

            <div v-if="loadingCupones" class="py-10 text-center">
              <svg class="w-6 h-6 text-[#2563eb] mx-auto mb-2 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <p class="text-[13px] text-[#666]">Cargando cupones...</p>
            </div>

            <div v-else-if="cuponesActivos.length === 0" class="py-10 text-center px-5">
              <div class="w-12 h-12 mx-auto mb-3 bg-[#f5f5f5] rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-[#999]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
              </div>
              <h4 class="text-[14px] font-semibold text-[#333] mb-1">No tienes cupones activos</h4>
              <p class="text-[12px] text-[#666]">Los cupones se asignan según tu nivel de mayorista</p>
            </div>

            <div v-else class="p-4 grid grid-cols-1 md:grid-cols-2 gap-3">
              <div v-for="cupon in cuponesActivos" :key="cupon.id" class="relative bg-white rounded-md border border-[#e0e0e0] overflow-hidden hover:border-[#2563eb]/40 transition-all">
                <div class="flex">
                  <div class="w-20 flex-shrink-0 bg-gradient-to-br from-[#2563eb] to-[#1d4ed8] text-white p-3 flex flex-col items-center justify-center relative">
                    <span class="text-xl font-bold">{{ cupon.descuento }}%</span>
                    <span class="text-[9px] uppercase tracking-wide opacity-80">Dcto</span>
                    <div class="absolute right-0 top-0 bottom-0 flex flex-col justify-around">
                      <div class="w-2 h-2 bg-white rounded-full -mr-1"></div>
                      <div class="w-2 h-2 bg-white rounded-full -mr-1"></div>
                      <div class="w-2 h-2 bg-white rounded-full -mr-1"></div>
                    </div>
                  </div>
                  <div class="flex-1 p-3">
                    <h4 class="text-[13px] font-semibold text-[#333] mb-0.5">{{ cupon.nombre }}</h4>
                    <p class="text-[11px] text-[#666] mb-2">{{ cupon.descripcion }}</p>
                    <div class="flex items-center gap-2 text-[10px] text-[#888] mb-2">
                      <span v-if="cupon.compra_minima">Min ${{ formatPrice(cupon.compra_minima) }}</span>
                      <span>Hasta {{ formatDate(cupon.fecha_expiracion) }}</span>
                    </div>
                    <div class="flex items-center justify-between">
                      <code class="px-1.5 py-0.5 bg-[#f5f5f5] rounded text-[11px] font-mono text-[#333]">{{ cupon.codigo }}</code>
                      <button @click="copiarCodigo(cupon.codigo)" class="text-[11px] text-[#2563eb] hover:text-[#1d4ed8] font-medium flex items-center gap-1">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                        Copiar
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Beneficios por Nivel -->
          <div class="bg-white rounded-md border border-[#e0e0e0] overflow-hidden" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <div class="px-5 py-4 border-b border-[#e8e8e8]">
              <h3 class="text-[15px] font-bold text-[#333]">Beneficios por Nivel</h3>
              <p class="text-[12px] text-[#666] mt-0.5">Mientras más compras, más beneficios obtienes</p>
            </div>
            <div>
              <div v-for="(nivel, index) in niveles" :key="nivel.nombre" :class="['px-5 py-3.5 flex items-center gap-3', index > 0 ? 'border-t border-[#e8e8e8]' : '']">
                <div :class="['w-10 h-10 rounded-full flex items-center justify-center', nivel.bgColor]">
                  <svg class="w-5 h-5" :class="nivel.iconColor" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="text-[13px] font-semibold text-[#333]">{{ nivel.nombre }}</h4>
                  <p class="text-[11px] text-[#666]">{{ nivel.requisito }}</p>
                </div>
                <div class="text-right flex-shrink-0">
                  <span class="text-lg font-bold" :class="nivel.iconColor">{{ nivel.descuento }}%</span>
                  <p class="text-[10px] text-[#888]">descuento</p>
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
      <div class="relative bg-white rounded-lg w-full max-w-md max-h-[90vh] overflow-y-auto" style="box-shadow: 0 20px 60px rgba(0,0,0,0.15);">
        <!-- Modal Header -->
        <div class="sticky top-0 bg-white z-10 px-5 py-3.5 border-b border-[#e8e8e8] flex items-center justify-between">
          <h3 class="text-[15px] font-bold text-[#333]">
            {{ editingAddress ? 'Editar Dirección' : 'Nueva Dirección' }}
          </h3>
          <button @click="closeAddressModal" class="text-[#999] hover:text-[#333] p-1 rounded transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="px-5 py-4">
          <div class="space-y-3.5">
            <!-- Etiqueta -->
            <div>
              <label class="block text-[12px] font-medium text-[#333] mb-1">Nombre de la dirección</label>
              <input 
                v-model="addressForm.etiqueta"
                type="text"
                placeholder="Ej: Casa, Oficina, Bodega..."
                class="w-full h-[36px] px-3 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
              />
            </div>

            <!-- Dirección -->
            <div>
              <label class="block text-[12px] font-medium text-[#333] mb-1">
                Dirección <span class="text-red-500">*</span>
              </label>
              <input 
                v-model="addressForm.direccion"
                type="text"
                placeholder="Ej: Carrera 71d #1-14 Sur"
                class="w-full h-[36px] px-3 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
              />
            </div>

            <!-- Complemento -->
            <div>
              <label class="block text-[12px] font-medium text-[#333] mb-1">Complemento <span class="text-[#999] font-normal">(opcional)</span></label>
              <input 
                v-model="addressForm.complemento"
                type="text"
                placeholder="Apto, oficina, local..."
                class="w-full h-[36px] px-3 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
              />
            </div>

            <!-- Departamento y Municipio -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-[12px] font-medium text-[#333] mb-1">
                  Departamento <span class="text-red-500">*</span>
                </label>
                <select 
                  v-model="addressForm.departamento_id"
                  @change="onDepartamentoChange"
                  class="w-full h-[36px] px-2.5 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white"
                >
                  <option :value="null">Selecciona...</option>
                  <option v-for="dep in departamentos" :key="dep.id" :value="dep.id">
                    {{ dep.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-[12px] font-medium text-[#333] mb-1">
                  Ciudad <span class="text-red-500">*</span>
                </label>
                <select 
                  v-model="addressForm.municipio_id"
                  @change="onMunicipioChange"
                  :disabled="!addressForm.departamento_id"
                  class="w-full h-[36px] px-2.5 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white disabled:bg-[#f5f5f5] disabled:text-[#999] disabled:cursor-not-allowed"
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
              <label class="block text-[12px] font-medium text-[#333] mb-1">Barrio <span class="text-[#999] font-normal">(opcional)</span></label>
              <input 
                v-model="addressForm.barrio"
                type="text"
                placeholder="Ej: Kennedy, Chapinero..."
                class="w-full h-[36px] px-3 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
              />
            </div>

            <!-- Teléfono -->
            <div>
              <label class="block text-[12px] font-medium text-[#333] mb-1">
                Teléfono de contacto <span class="text-red-500">*</span>
              </label>
              <input 
                v-model="addressForm.telefono"
                type="tel"
                placeholder="Ej: 3001234567"
                class="w-full h-[36px] px-3 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white placeholder:text-[#bbb]"
              />
            </div>

            <!-- Indicaciones -->
            <div>
              <label class="block text-[12px] font-medium text-[#333] mb-1">Indicaciones <span class="text-[#999] font-normal">(opcional)</span></label>
              <textarea 
                v-model="addressForm.indicaciones"
                rows="2"
                placeholder="Indicaciones para el repartidor..."
                class="w-full px-3 py-2 text-[13px] text-[#333] border border-[#ccc] rounded-md focus:outline-none focus:ring-1 focus:ring-[#2563eb] focus:border-[#2563eb] bg-white resize-none placeholder:text-[#bbb]"
              ></textarea>
            </div>

            <!-- Marcar como principal -->
            <label class="flex items-center gap-2.5 cursor-pointer">
              <input 
                v-model="addressForm.is_default"
                type="checkbox"
                class="w-4 h-4 text-[#2563eb] focus:ring-[#2563eb] rounded border-[#ccc]"
              />
              <span class="text-[13px] text-[#555]">Marcar como dirección principal</span>
            </label>
          </div>

          <!-- Buttons -->
          <div class="flex gap-3 mt-5 pt-4 border-t border-[#e8e8e8]">
            <button 
              @click="closeAddressModal"
              class="flex-1 h-[36px] text-[13px] font-medium text-[#555] border border-[#ccc] rounded-md hover:bg-[#f5f5f5] transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="saveAddress"
              :disabled="savingAddress || !isAddressFormValid"
              class="flex-1 h-[36px] text-[13px] font-medium text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1.5"
            >
              <svg v-if="savingAddress" class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              {{ savingAddress ? 'Guardando...' : (editingAddress ? 'Actualizar' : 'Guardar') }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- end address modal -->

      </div><!-- end max-w-960 -->
    </div><!-- end flex-1 content -->
  </div><!-- end flex container -->
  
  <!-- Toast Notifications -->
  <B2BToast />
</template>

<script>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient, { getImageUrl } from '@/services/api'
import { obtenerMisPedidos } from '@/services/mayoristas'
import B2BToast, { useToast } from '@/components/b2b/ui/B2BToast.vue'

const COLOMBIA_API = {
  departamentos: 'https://api-colombia.com/api/v1/Department',
  ciudades: (id) => `https://api-colombia.com/api/v1/Department/${id}/cities`
}

export default {
  name: 'B2BCuenta',
  components: {
    B2BToast
  },
  setup() {
    const activeTab = ref('profile')
    const router = useRouter()
    const route = useRoute()
    const showAddressModal = ref(false)
    const editingAddress = ref(null)
    const loadingAddresses = ref(false)
    const savingAddress = ref(false)
    const isEmailVerified = ref(false)
    const verificationDismissed = ref(false)

    const tabs = [
      { id: 'profile', label: 'Perfil', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>' },
      { id: 'addresses', label: 'Direcciones', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /></svg>' },
      { id: 'security', label: 'Seguridad', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>' },
      { id: 'notifications', label: 'Notificaciones', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>' },
    ]

    const sidebarLinks = [
      { id: 'pedidos', label: 'Mis Pedidos', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>' },
      { id: 'cupones', label: 'Cupones', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>' },
    ]

    // =======================================================================
    // PEDIDOS STATE
    // =======================================================================
    const orders = ref([])
    const isLoadingOrders = ref(true)
    const selectedStatus = ref('all')
    const searchQuery = ref('')
    const expandedOrderId = ref(null)

    const ordersStats = computed(() => ({
      delivered: orders.value.filter(o => o.status === 'Entregado').length,
      shipping: orders.value.filter(o => o.status === 'En Camino').length,
      processing: orders.value.filter(o => o.status === 'Pagada' || o.status === 'Pendiente').length,
      totalSpent: orders.value.reduce((sum, o) => sum + o.total, 0)
    }))

    const ordersStatuses = computed(() => [
      { value: 'all', label: 'Todos', count: orders.value.length },
      { value: 'Pendiente', label: 'Pendientes', count: orders.value.filter(o => o.status === 'Pendiente').length },
      { value: 'Pagada', label: 'Pagadas', count: orders.value.filter(o => o.status === 'Pagada').length },
      { value: 'En Camino', label: 'En Camino', count: orders.value.filter(o => o.status === 'En Camino').length },
      { value: 'Entregado', label: 'Entregados', count: orders.value.filter(o => o.status === 'Entregado').length },
    ])

    const filteredOrders = computed(() => {
      let result = orders.value
      if (selectedStatus.value !== 'all') {
        result = result.filter(o => o.status === selectedStatus.value)
      }
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(o => 
          o.numero?.toLowerCase().includes(query) ||
          o.products?.some(p => p.name?.toLowerCase().includes(query))
        )
      }
      return result
    })

    function getStatusClass(status) {
      const classes = {
        'Entregado': 'bg-emerald-100 text-emerald-700',
        'En Camino': 'bg-blue-100 text-blue-700',
        'Pagada': 'bg-green-50 text-green-700',
        'Pendiente': 'bg-amber-50 text-amber-700',
        'Cancelado': 'bg-red-100 text-red-700',
      }
      return classes[status] || classes['Pendiente']
    }

    function getStatusLabel(value) {
      const labels = {
        'all': 'todas',
        'Pendiente': 'pendientes',
        'Pagada': 'pagadas',
        'En Camino': 'en camino',
        'Entregado': 'entregados'
      }
      return labels[value] || value
    }

    function mapEstado(estado, metodoPago) {
      const raw = (estado || 'pendiente').toLowerCase()
      const map = {
        'pendiente': metodoPago === 'wompi' ? 'Pagada' : 'Pendiente',
        'confirmada': 'Pagada',
        'pagada': 'Pagada',
        'en_proceso': 'En Camino',
        'enviada': 'En Camino',
        'completada': 'Entregado',
        'entregada': 'Entregado',
        'cancelada': 'Cancelado',
      }
      return map[raw] || 'Pendiente'
    }

    function formatFecha(fecha) {
      if (!fecha) return ''
      const d = new Date(fecha)
      if (isNaN(d)) return String(fecha)
      return d.toLocaleDateString('es-CO', { day: 'numeric', month: 'short', year: 'numeric' })
    }

    function isVideo(url) {
      if (!url) return false
      const cleanUrl = url.split('?')[0].toLowerCase()
      return ['.mp4', '.webm', '.ogg', '.mov'].some(ext => cleanUrl.endsWith(ext))
    }

    function getOrderMediaUrl(item) {
      const raw = item?.image || item?.imagen || item?.imagen_principal || ''
      return getImageUrl(raw) || ''
    }

    function normalizarOrden(orden) {
      const metodoPago = orden.metodo_pago || 'whatsapp'
      return {
        id: orden.id || orden.numero_orden,
        numero: orden.numero || orden.codigo || `ORD-${(orden.id || '').substring(0, 8)}`,
        date: formatFecha(orden.fecha || orden.date),
        total: orden.total || orden.monto_total || 0,
        subtotal: orden.subtotal || orden.total || 0,
        envio: orden.envio || 0,
        savings: orden.ahorro || orden.savings || 0,
        items: (orden.items?.length || orden.cantidad_items || 0),
        status: mapEstado(orden.estado || orden.status, metodoPago),
        metodoPago,
        tracking: orden.numero_seguimiento || orden.tracking || null,
        estimatedDelivery: orden.fecha_entrega_estimada || orden.estimatedDelivery,
        invoice: orden.numero_factura || orden.invoice,
        products: (orden.items || []).map(item => ({
          name: item.nombre || item.name || 'Producto',
          image: item.imagen || item.image || null,
          quantity: item.cantidad || item.quantity || 1,
          price: item.precio || item.price || item.precio_unitario || 0,
          id: item.id || item.producto_id || ''
        }))
      }
    }

    async function cargarPedidos() {
      try {
        isLoadingOrders.value = true
        const userStr = localStorage.getItem('b2b_user')
        if (!userStr) return
        const userData = JSON.parse(userStr)
        const pedidos = await obtenerMisPedidos(userData.email)
        orders.value = (Array.isArray(pedidos) ? pedidos : []).map(normalizarOrden)
      } catch (error) {
        console.error('Error al cargar pedidos:', error)
      } finally {
        isLoadingOrders.value = false
      }
    }

    function formatCompact(value) {
      if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
      if (value >= 1000) return (value / 1000).toFixed(0) + 'K'
      return value?.toString() || '0'
    }

    function toggleOrderDetail(order) {
      expandedOrderId.value = expandedOrderId.value === order.id ? null : order.id
    }

    function reorderItems(order) {
      showToast({
        type: 'info',
        title: 'Agregando al carrito',
        message: `Agregando ${order.items} productos al carrito...`
      })
    }

    function trackOrder(order) {
      showToast({
        type: 'info',
        title: 'Rastreo de envío',
        message: `Tracking: ${order.tracking}`
      })
    }

    // =======================================================================
    // CUPONES STATE  
    // =======================================================================
    const loadingCupones = ref(true)
    const cuponCode = ref('')
    const aplicandoCupon = ref(false)
    const cuponFeedback = ref(null)
    const cuponToast = ref('')
    const cuponesActivos = ref([])

    const niveles = [
      { nombre: 'Bronce', requisito: 'Compras hasta $2.000.000', descuento: 10, bgColor: 'bg-amber-100', iconColor: 'text-amber-600' },
      { nombre: 'Plata', requisito: 'Compras de $2.000.000 a $5.000.000', descuento: 15, bgColor: 'bg-gray-200', iconColor: 'text-gray-500' },
      { nombre: 'Gold', requisito: 'Compras superiores a $5.000.000', descuento: 20, bgColor: 'bg-amber-50', iconColor: 'text-amber-500' },
    ]

    const cuponesMock = [
      { id: 1, codigo: 'BIENVENIDO20', nombre: 'Cupón de Bienvenida', descripcion: 'Para tu primera compra como mayorista', descuento: 20, compra_minima: 500000, fecha_expiracion: '2026-03-30' },
      { id: 2, codigo: 'FEBRERO10', nombre: 'Promo Febrero', descripcion: 'Descuento especial del mes', descuento: 10, compra_minima: 200000, fecha_expiracion: '2026-02-27' },
    ]

    function formatDate(dateStr) {
      if (!dateStr) return 'Sin fecha'
      const date = new Date(dateStr)
      if (isNaN(date.getTime())) return 'Sin fecha'
      return date.toLocaleDateString('es-CO', { day: 'numeric', month: 'short', year: 'numeric' })
    }

    async function cargarCupones() {
      loadingCupones.value = true
      try {
        cuponesActivos.value = cuponesMock
      } catch (error) {
        console.error('Error cargando cupones:', error)
      } finally {
        loadingCupones.value = false
      }
    }

    async function aplicarCupon() {
      if (!cuponCode.value) return
      aplicandoCupon.value = true
      cuponFeedback.value = null
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        const codigoUpper = cuponCode.value.toUpperCase()
        const cuponExistente = cuponesMock.find(c => c.codigo === codigoUpper)
        if (cuponExistente) {
          if (cuponesActivos.value.find(c => c.codigo === codigoUpper)) {
            cuponFeedback.value = { success: false, message: 'Este cupón ya está en tu lista de cupones activos' }
          } else {
            cuponesActivos.value.push(cuponExistente)
            cuponFeedback.value = { success: true, message: `¡Cupón "${cuponExistente.nombre}" agregado exitosamente!` }
            cuponCode.value = ''
          }
        } else {
          cuponFeedback.value = { success: false, message: 'Código de cupón inválido o expirado' }
        }
      } catch (error) {
        cuponFeedback.value = { success: false, message: 'Error al validar el cupón. Intenta de nuevo.' }
      } finally {
        aplicandoCupon.value = false
      }
    }

    function copiarCodigo(codigo) {
      navigator.clipboard.writeText(codigo)
      cuponToast.value = 'Código copiado al portapapeles'
      setTimeout(() => { cuponToast.value = '' }, 2000)
    }

    // =======================================================================
    // ACCOUNT DATA
    // =======================================================================

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

    // Variables para vista móvil
    const changingPassword = ref(false)
    const mobileEditMode = ref(false)
    const notificationSettings = reactive({
      offers: true,
      orders: true,
      newProducts: false
    })
    
    function cancelEdit() {
      mobileEditMode.value = false
      loadForm() // Restaurar valores originales
    }

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

    const { showToast } = useToast()

    function saveProfile() {
      const userData = { ...user.value, ...editForm }
      localStorage.setItem('b2b_user', JSON.stringify(userData))
      showToast({
        type: 'success',
        title: 'Perfil actualizado',
        message: 'Tus datos han sido guardados correctamente'
      })
    }

    async function changePassword() {
      if (passwordForm.new !== passwordForm.confirm) {
        showToast({
          type: 'error',
          title: 'Error',
          message: 'Las contraseñas no coinciden'
        })
        return
      }
      if (passwordForm.new.length < 8) {
        showToast({
          type: 'error', 
          title: 'Error',
          message: 'La contraseña debe tener al menos 8 caracteres'
        })
        return
      }
      if (!passwordForm.current) {
        showToast({
          type: 'error',
          title: 'Error', 
          message: 'Debes ingresar tu contraseña actual'
        })
        return
      }
      
      changingPassword.value = true
      try {
        await apiClient.post('/b2b/me/cambiar-password', {
          current_password: passwordForm.current,
          new_password: passwordForm.new
        })
        
        showToast({
          type: 'success',
          title: 'Contraseña actualizada',
          message: 'Tu contraseña ha sido cambiada correctamente'
        })
        
        passwordForm.current = ''
        passwordForm.new = ''
        passwordForm.confirm = ''
      } catch (error) {
        console.error('Error al cambiar contraseña:', error)
        const message = error.response?.data?.detail || 'Error al cambiar la contraseña'
        showToast({
          type: 'error',
          title: 'Error',
          message
        })
      } finally {
        changingPassword.value = false
      }
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
        showToast({
          type: 'error',
          title: 'Error',
          message: 'Error al guardar la dirección. Por favor intenta nuevamente.'
        })
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
        showToast({
          type: 'error',
          title: 'Error',
          message: 'Error al eliminar la dirección'
        })
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

    // Email verification
    function checkVerificationStatus() {
      const userData = user.value
      isEmailVerified.value = userData.email_verified || false
      const dismissed = localStorage.getItem('verification_dismissed')
      if (dismissed) verificationDismissed.value = true
    }

    async function sendVerificationEmail() {
      try {
        await apiClient.post('/b2b/me/send-verification')
        showToast({
          type: 'success',
          title: 'Correo enviado',
          message: 'Revisa tu bandeja de entrada para verificar tu email.'
        })
      } catch (error) {
        showToast({
          type: 'info',
          title: 'Verificación',
          message: 'Revisa tu bandeja de entrada y carpeta de spam.'
        })
      }
    }

    function dismissVerification() {
      verificationDismissed.value = true
      localStorage.setItem('verification_dismissed', 'true')
    }

    onMounted(async () => {
      // Leer tab desde query params
      if (route.query.tab) {
        activeTab.value = route.query.tab
      }
      
      loadForm()
      checkVerificationStatus()
      await loadDepartamentos()
      await loadAddresses()
      
      // Cargar datos según el tab activo
      if (activeTab.value === 'pedidos') {
        await cargarPedidos()
      } else if (activeTab.value === 'cupones') {
        await cargarCupones()
      }
    })

    // Watch para cambios de tab y cargar datos
    watch(activeTab, async (newTab) => {
      // Actualizar URL sin recargar
      const query = newTab === 'profile' ? {} : { tab: newTab }
      router.replace({ query })
      
      if (newTab === 'pedidos' && orders.value.length === 0) {
        await cargarPedidos()
      } else if (newTab === 'cupones' && cuponesActivos.value.length === 0) {
        await cargarCupones()
      }
    })

    return {
      activeTab, tabs, sidebarLinks, router, user, userInitials,
      editForm, passwordForm, addresses, notificationPrefs,
      changingPassword, notificationSettings, mobileEditMode, cancelEdit,
      showAddressModal, editingAddress, loadingAddresses, savingAddress,
      isEmailVerified, verificationDismissed,
      departamentos, municipios, addressForm, isAddressFormValid,
      formatPrice, resetForm, saveProfile, changePassword,
      openAddressModal, closeAddressModal, saveAddress, deleteAddress, setDefaultAddress,
      onDepartamentoChange, onMunicipioChange,
      sendVerificationEmail, dismissVerification,
      // Pedidos
      orders, isLoadingOrders, selectedStatus, searchQuery, expandedOrderId,
      ordersStats, ordersStatuses, filteredOrders, getStatusClass, getStatusLabel, formatCompact,
      toggleOrderDetail, reorderItems, trackOrder,
      isVideo, getOrderMediaUrl,
      // Cupones
      loadingCupones, cuponCode, aplicandoCupon, cuponFeedback, cuponToast,
      cuponesActivos, niveles, formatDate, aplicarCupon, copiarCodigo
    }
  }
}
</script>

<style scoped>
@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    max-height: 800px;
    transform: translateY(0);
  }
}
.animate-slideDown {
  animation: slideDown 0.3s ease-out;
}
</style>