<template>
  <div class="flex min-h-[calc(100vh-106px)]">

    <!-- ==================== SIDEBAR FIXED LEFT (like MercadoLibre) ==================== -->
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

          <!-- Router Links (Pedidos, Cupones) -->
          <button 
            v-for="link in sidebarLinks"
            :key="link.route"
            @click="router.push(link.route)"
            class="w-full flex items-center gap-2.5 px-3 py-2 text-left transition-colors text-[14px] rounded-md text-[#555] hover:bg-[#f5f5f5] hover:text-[#333] font-normal"
          >
            <span v-html="link.icon" class="w-[18px] h-[18px] text-[#999]"></span>
            {{ link.label }}
          </button>
        </nav>
      </div>
    </aside>

    <!-- ==================== MAIN CONTENT AREA ==================== -->
    <div class="flex-1 min-w-0">
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

        <!-- Mobile Sidebar (below header on mobile) -->
        <div class="lg:hidden mb-5">
          <div class="bg-white rounded-lg border border-[#e0e0e0] p-4" style="box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);">
            <!-- Stats -->
            <div class="flex items-center gap-2 mb-3">
              <div class="w-1.5 h-1.5 rounded-full bg-emerald-500"></div>
              <span class="text-[12px] font-semibold text-emerald-700">Mayorista Verificado</span>
            </div>
            <div class="grid grid-cols-4 gap-3 text-center text-[12px] mb-3 pb-3 border-b border-[#e8e8e8]">
              <div><span class="block font-semibold text-[#333]">{{ user.tier || 'Gold' }}</span><span class="text-[#999]">Nivel</span></div>
              <div><span class="block font-semibold text-emerald-600">{{ user.descuento || '15' }}%</span><span class="text-[#999]">Dto.</span></div>
              <div><span class="block font-semibold text-[#333]">${{ formatPrice(user.credito || 0) }}</span><span class="text-[#999]">Crédito</span></div>
              <div><span class="block font-semibold text-[#333]">{{ user.totalOrders || 0 }}</span><span class="text-[#999]">Pedidos</span></div>
            </div>
            <!-- Mobile nav -->
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'px-3 py-1.5 rounded-full text-[12px] font-medium transition-colors',
                  (activeTab === tab.id || (tab.id === 'profile' && activeTab === 'mydata'))
                    ? 'bg-[#2563eb] text-white' 
                    : 'bg-[#f0f0f0] text-[#555] hover:bg-[#e5e5e5]'
                ]"
              >
                {{ tab.label }}
              </button>
              <button 
                v-for="link in sidebarLinks"
                :key="link.route"
                @click="router.push(link.route)"
                class="px-3 py-1.5 rounded-full text-[12px] font-medium transition-colors bg-[#f0f0f0] text-[#555] hover:bg-[#e5e5e5]"
              >
                {{ link.label }}
              </button>
            </div>
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
                    class="h-[36px] px-5 text-[13px] font-medium text-white bg-[#2563eb] hover:bg-[#1d4ed8] rounded-md transition-colors"
                  >
                    Actualizar Contraseña
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
    <!-- end modal -->

      </div><!-- end max-w-960 -->
    </div><!-- end flex-1 content -->
  </div><!-- end flex container -->
</template>

<script>
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

const COLOMBIA_API = {
  departamentos: 'https://api-colombia.com/api/v1/Department',
  ciudades: (id) => `https://api-colombia.com/api/v1/Department/${id}/cities`
}

export default {
  name: 'B2BCuenta',
  setup() {
    const activeTab = ref('profile')
    const router = useRouter()
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
      { label: 'Mis Pedidos', route: '/portal/pedidos', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>' },
      { label: 'Cupones', route: '/portal/cupones', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>' },
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
        alert('Hemos enviado un correo de verificación a ' + user.value.email + '. Revisa tu bandeja de entrada.')
      } catch (error) {
        alert('Se ha enviado un correo de verificación a tu email. Revisa tu bandeja de entrada y carpeta de spam.')
      }
    }

    function dismissVerification() {
      verificationDismissed.value = true
      localStorage.setItem('verification_dismissed', 'true')
    }

    onMounted(async () => {
      loadForm()
      checkVerificationStatus()
      await loadDepartamentos()
      await loadAddresses()
    })

    return {
      activeTab, tabs, sidebarLinks, router, user, userInitials,
      editForm, passwordForm, addresses, notificationPrefs,
      showAddressModal, editingAddress, loadingAddresses, savingAddress,
      isEmailVerified, verificationDismissed,
      departamentos, municipios, addressForm, isAddressFormValid,
      formatPrice, resetForm, saveProfile, changePassword,
      openAddressModal, closeAddressModal, saveAddress, deleteAddress, setDefaultAddress,
      onDepartamentoChange, onMunicipioChange,
      sendVerificationEmail, dismissVerification
    }
  }
}
</script>
