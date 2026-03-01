<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FAF5F2] via-[#FAFAFA] to-white text-text-dark">
    <!-- Header Simple -->
    <header class="bg-white/90 border-b border-black/5 shadow-[0_6px_30px_rgba(0,0,0,0.04)] sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
        <div class="flex items-center justify-between h-16">
          <!-- Logo + Texto -->
          <router-link to="/" class="flex items-center gap-3 group">
            <img 
              src="/logo-kharis.png" 
              alt="Kharis Distribuidora" 
              class="h-12 w-auto object-contain group-hover:scale-105 transition-transform duration-300"
            />
            <span class="font-luxury text-xl tracking-wider text-text-dark hidden sm:inline-block">KHARIS</span>
          </router-link>
          
          <!-- Navegación -->
          <nav class="flex items-center gap-6">
            <router-link to="/" class="text-xs tracking-widest text-text-dark/60 hover:text-text-dark transition-colors">
              TIENDA
            </router-link>
            <button 
              @click="cerrarSesion" 
              class="text-xs tracking-widest text-text-dark/60 hover:text-text-dark transition-colors"
            >
              CERRAR SESIÓN
            </button>
          </nav>
        </div>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-12">
      <!-- Saludo -->
      <div class="mb-12">
        <h1 class="font-luxury text-3xl sm:text-4xl text-text-dark mb-2">
          Hola, {{ userName }}
        </h1>
        <p class="text-text-dark/60 text-sm">
          Bienvenida a tu espacio personal
        </p>
      </div>

      <!-- Tabs de navegación -->
      <div class="border-b border-black/10 mb-8">
        <nav class="flex gap-8">
          <button 
            @click="activeTab = 'favoritos'"
              class="pb-4 text-sm tracking-[0.18em] uppercase transition-colors relative"
            :class="activeTab === 'favoritos' 
              ? 'text-text-dark font-medium' 
              : 'text-text-dark/50 hover:text-text-dark/70'"
          >
            MIS FAVORITOS
            <span 
              v-if="activeTab === 'favoritos'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-text-dark"
            ></span>
          </button>
          <button 
            @click="activeTab = 'compras'"
              class="pb-4 text-sm tracking-[0.18em] uppercase transition-colors relative"
            :class="activeTab === 'compras' 
              ? 'text-text-dark font-medium' 
              : 'text-text-dark/50 hover:text-text-dark/70'"
          >
            MIS COMPRAS
            <span 
              v-if="activeTab === 'compras'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-text-dark"
            ></span>
          </button>
          <button 
            @click="activeTab = 'datos'"
              class="pb-4 text-sm tracking-[0.18em] uppercase transition-colors relative"
            :class="activeTab === 'datos' 
              ? 'text-text-dark font-medium' 
              : 'text-text-dark/50 hover:text-text-dark/70'"
          >
            MIS DATOS
            <span 
              v-if="activeTab === 'datos'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-text-dark"
            ></span>
          </button>
        </nav>
      </div>

      <!-- Contenido de Favoritos -->
      <section v-if="activeTab === 'favoritos'">
        <div v-if="loadingFavoritos" class="flex justify-center py-16">
          <div class="w-8 h-8 border-2 border-text-dark/20 border-t-text-dark rounded-full animate-spin"></div>
        </div>
        
        <div v-else-if="favoritos.length === 0" class="text-center py-16">
          <svg class="w-16 h-16 mx-auto text-text-dark/20 mb-4" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
          </svg>
          <h3 class="font-luxury text-xl text-text-dark mb-2">Sin favoritos aún</h3>
          <p class="text-text-dark/50 text-sm mb-6">
            Explora nuestra colección y guarda tus productos favoritos
          </p>
          <router-link 
            to="/"
            class="inline-block px-8 py-3 bg-text-dark text-white text-sm tracking-wider hover:bg-black transition-colors"
          >
            EXPLORAR TIENDA
          </router-link>
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          <div
            v-for="producto in favoritos" 
            :key="producto.id"
            @click="irADetalle(producto.id)"
            class="group cursor-pointer bg-white/85 border border-black/5 shadow-[0_18px_50px_rgba(0,0,0,0.06)] rounded-sm p-3 transition-transform duration-300 hover:-translate-y-1"
          >
            <div class="relative aspect-[3/4] bg-nude-50 mb-3 overflow-hidden">
              <img 
                :src="getImageUrl(producto.imagen_principal) || '/placeholder.jpg'" 
                :alt="producto.nombre"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              />
              <button 
                @click.stop="quitarFavorito(producto.id)"
                class="absolute top-3 right-3 w-8 h-8 bg-white/90 rounded-full flex items-center justify-center hover:bg-white transition-colors"
              >
                <svg class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>
              </button>
            </div>
            <h3 class="text-sm text-text-dark font-medium mb-1 line-clamp-2">
              {{ producto.nombre }}
            </h3>
            <p class="text-sm text-text-dark/70">
              {{ formatPrice(producto.precio_monto, producto.precio_moneda) }}
            </p>
          </div>
        </div>
      </section>

      <!-- Contenido de Compras -->
      <section v-if="activeTab === 'compras'">
        <div v-if="loadingCompras" class="flex justify-center py-16">
          <div class="w-8 h-8 border-2 border-gray-200 border-t-gray-600 rounded-full animate-spin"></div>
        </div>
        
        <div v-else-if="compras.length === 0" class="text-center py-12 bg-white border border-gray-200 rounded-lg">
          <svg class="w-14 h-14 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
          </svg>
          <p class="text-gray-600 font-medium mb-1">Aún no tienes compras</p>
          <p class="text-gray-400 text-sm mb-5">Tu historial aparecerá aquí</p>
          <router-link 
            to="/catalogo"
            class="inline-flex items-center justify-center h-11 px-6 bg-[#1a1a1a] text-white text-sm font-medium rounded-lg hover:bg-black transition-colors"
          >
            Explorar productos
          </router-link>
        </div>

        <!-- Lista de pedidos - Master-Detail Pattern (tarjetas clickeables) -->
        <div v-else class="space-y-2">
          <button 
            v-for="orden in compras" 
            :key="orden.id"
            @click="verDetalleOrden(orden)"
            class="w-full text-left bg-white border border-gray-200 rounded-lg overflow-hidden hover:bg-gray-50/50 active:bg-gray-100/70 transition-colors cursor-pointer"
          >
            <!-- Header: Estado + Fecha + Chevron -->
            <div class="px-4 py-3 flex items-center gap-3">
              <div class="flex-1 min-w-0">
                <p 
                  class="text-[14px] font-medium leading-tight"
                  :class="getEstadoTextClass(orden)"
                >
                  {{ getEstadoDirecto(orden) }}
                </p>
                <p class="text-[12px] text-gray-400 mt-0.5">
                  {{ formatDateShort(orden.fecha) }} · {{ formatPriceCOP(orden.total) }}
                </p>
              </div>
              
              <!-- Chevron indicator -->
              <svg class="w-5 h-5 text-gray-300 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
              </svg>
            </div>

            <!-- Productos - Row layout con thumbnails agrupados -->
            <div class="px-4 pb-3 flex items-center gap-3">
              <!-- Thumbnails superpuestos -->
              <div class="flex -space-x-2 flex-shrink-0">
                <div 
                  v-for="(item, idx) in orden.items.slice(0, 3)" 
                  :key="item.id"
                  class="w-10 h-10 bg-gray-100 rounded-md overflow-hidden border-2 border-white"
                  :style="{ zIndex: 3 - idx }"
                >
                  <img
                    :src="getCompraMediaUrl(item) || '/placeholder.jpg'"
                    :alt="item.nombre"
                    class="w-full h-full object-cover"
                  />
                </div>
                <!-- Badge +N si hay más de 3 productos -->
                <div 
                  v-if="orden.items.length > 3"
                  class="w-10 h-10 bg-gray-200 rounded-md flex items-center justify-center border-2 border-white text-[11px] font-medium text-gray-500"
                >
                  +{{ orden.items.length - 3 }}
                </div>
              </div>
              
              <!-- Descripción resumida de productos -->
              <p class="text-[12px] text-gray-500 line-clamp-1 flex-1 min-w-0">
                {{ orden.items[0]?.nombre }}{{ orden.items.length > 1 ? ` y ${orden.items.length - 1} más` : '' }}
              </p>
            </div>

            <!-- Footer sutil: # Pedido + Estado de pago -->
            <div class="px-4 py-2 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-400">
              <span>#{{ orden.numero }}</span>
              <span v-if="orden.estado_pago === 'pagado'">✓ Pagado</span>
              <span v-else class="text-amber-500">Pendiente</span>
            </div>
          </button>
        </div>
      </section>

      <!-- Contenido de Datos -->
      <section v-if="activeTab === 'datos'">
        <div class="max-w-xl">
          <div class="bg-white p-6 sm:p-8 border border-black/5">
            <h3 class="font-luxury text-xl text-text-dark mb-6">Información Personal</h3>
            
            <!-- Loading state -->
            <div v-if="loadingDatos" class="flex justify-center py-8">
              <div class="w-8 h-8 border-2 border-text-dark/20 border-t-text-dark rounded-full animate-spin"></div>
            </div>
            
            <form v-else @submit.prevent="guardarDatos" class="space-y-5">
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">NOMBRE</label>
                <input 
                  v-model="datosUsuario.nombre"
                  type="text"
                  class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm"
                  placeholder="Tu nombre"
                />
              </div>
              
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">EMAIL</label>
                <input 
                  v-model="datosUsuario.email"
                  type="email"
                  disabled
                  class="w-full px-4 py-3 border border-black/10 bg-gray-50 text-text-dark/50 text-sm cursor-not-allowed"
                />
                <p class="text-xs text-text-dark/40 mt-1">El email no puede ser modificado</p>
              </div>
              
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">TELÉFONO</label>
                <input 
                  v-model="datosUsuario.telefono"
                  type="tel"
                  class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm"
                  placeholder="+57 300 123 4567"
                />
              </div>
              
              <!-- Ubicación -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs tracking-wider text-text-dark/60 mb-2">DEPARTAMENTO</label>
                  <input 
                    v-model="datosUsuario.departamento"
                    type="text"
                    class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm"
                    placeholder="Ej: Bogotá D.C."
                  />
                </div>
                <div>
                  <label class="block text-xs tracking-wider text-text-dark/60 mb-2">CIUDAD/MUNICIPIO</label>
                  <input 
                    v-model="datosUsuario.municipio"
                    type="text"
                    class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm"
                    placeholder="Ej: Bogotá"
                  />
                </div>
              </div>
              
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">BARRIO</label>
                <input 
                  v-model="datosUsuario.barrio"
                  type="text"
                  class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm"
                  placeholder="Ej: Chapinero"
                />
              </div>
              
              <div>
                <label class="block text-xs tracking-wider text-text-dark/60 mb-2">DIRECCIÓN</label>
                <textarea 
                  v-model="datosUsuario.direccion"
                  rows="3"
                  class="w-full px-4 py-3 border border-black/10 focus:border-text-dark/30 outline-none transition-colors text-sm resize-none"
                  placeholder="Tu dirección de envío completa"
                ></textarea>
              </div>
              
              <button 
                type="submit"
                :disabled="guardando"
                class="w-full px-6 py-3 bg-text-dark text-white text-sm tracking-wider hover:bg-black transition-colors disabled:opacity-50"
              >
                {{ guardando ? 'GUARDANDO...' : 'GUARDAR CAMBIOS' }}
              </button>
            </form>
          </div>
        </div>
      </section>
    </main>

    <!-- Bottom Sheet Modal - Detalle de Pedido -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div 
          v-if="selectedOrder" 
          class="fixed inset-0 z-[9998] bg-black/50"
          @click="closeOrderDetail"
        ></div>
      </Transition>
      
      <Transition
        enter-active-class="transition-transform duration-300 ease-out"
        enter-from-class="translate-y-full"
        enter-to-class="translate-y-0"
        leave-active-class="transition-transform duration-200 ease-in"
        leave-from-class="translate-y-0"
        leave-to-class="translate-y-full"
      >
        <div 
          v-if="selectedOrder" 
          class="fixed inset-x-0 bottom-0 z-[9999] bg-white rounded-t-2xl max-h-[90vh] flex flex-col shadow-2xl"
        >
          <!-- Header del Modal -->
          <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100">
            <h2 class="text-lg font-semibold text-gray-900">Detalle del Pedido</h2>
            <button 
              @click="closeOrderDetail"
              class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100 active:bg-gray-200 transition-colors"
            >
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <!-- Contenido scrolleable -->
          <div class="flex-1 overflow-y-auto px-5 py-4 space-y-5">
            
            <!-- Estado prominente -->
            <div class="text-center py-4 bg-gradient-to-r from-[#FAF5F2] to-[#FDF9F7] rounded-xl">
              <p 
                class="text-xl font-semibold"
                :class="getEstadoTextClass(selectedOrder)"
              >
                {{ getEstadoDirecto(selectedOrder) }}
              </p>
              <p class="text-sm text-gray-500 mt-1">Pedido #{{ selectedOrder.numero }}</p>
            </div>
            
            <!-- Guía de envío (si existe) -->
            <div v-if="selectedOrder.guia_envio" class="bg-blue-50 rounded-lg px-4 py-3 flex items-center gap-3">
              <svg class="w-5 h-5 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
              </svg>
              <div>
                <p class="text-sm font-medium text-blue-800">Guía de envío</p>
                <p class="text-sm text-blue-700 font-mono">{{ selectedOrder.guia_envio }}</p>
              </div>
            </div>
            
            <!-- Dirección de entrega -->
            <div class="border-b border-gray-100 pb-4">
              <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Dirección de entrega</h3>
              <p class="text-sm text-gray-700">{{ selectedOrder.direccion_envio || 'No especificada' }}</p>
              <p v-if="selectedOrder.municipio || selectedOrder.departamento" class="text-sm text-gray-500 mt-0.5">
                {{ [selectedOrder.municipio, selectedOrder.departamento].filter(Boolean).join(', ') }}
              </p>
            </div>
            
            <!-- Productos -->
            <div class="border-b border-gray-100 pb-4">
              <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Productos</h3>
              <div class="space-y-3">
                <div 
                  v-for="item in selectedOrder.items" 
                  :key="item.id"
                  class="flex gap-3"
                >
                  <div class="w-16 h-16 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                    <img
                      :src="getCompraMediaUrl(item) || '/placeholder.jpg'"
                      :alt="item.nombre"
                      class="w-full h-full object-cover"
                    />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-800 line-clamp-2">{{ item.nombre }}</p>
                    <p class="text-xs text-gray-400 mt-0.5">
                      Cant: {{ item.cantidad }}
                      <span v-if="item.color"> · {{ item.color }}</span>
                      <span v-if="item.largo"> · {{ item.largo }}"</span>
                    </p>
                    <p class="text-sm font-medium text-gray-700 mt-1">{{ formatPriceCOP(item.precio * item.cantidad) }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Método de pago -->
            <div class="border-b border-gray-100 pb-4">
              <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Método de pago</h3>
              <div class="flex items-center justify-between">
                <p class="text-sm text-gray-700">{{ getMetodoPagoLabel(selectedOrder.metodo_pago) }}</p>
                <span 
                  v-if="selectedOrder.estado_pago === 'pagado'"
                  class="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full"
                >
                  ✓ Pagado
                </span>
                <span v-else class="text-xs font-medium text-amber-600 bg-amber-50 px-2 py-1 rounded-full">
                  Pendiente
                </span>
              </div>
            </div>
            
            <!-- Resumen de pago -->
            <div>
              <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Resumen</h3>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between text-gray-600">
                  <span>Subtotal</span>
                  <span>{{ formatPriceCOP(selectedOrder.total) }}</span>
                </div>
                <div class="flex justify-between text-gray-600">
                  <span>Envío</span>
                  <span class="text-green-600">Gratis</span>
                </div>
                <div class="flex justify-between text-gray-900 font-semibold text-base pt-2 border-t border-gray-200">
                  <span>Total</span>
                  <span>{{ formatPriceCOP(selectedOrder.total) }}</span>
                </div>
              </div>
            </div>
            
          </div>
          
          <!-- Footer con botones de acción -->
          <div class="px-5 py-4 border-t border-gray-100 bg-white">
            <!-- Botón primario: Rastrear envío (SOLO si hay link_rastreo válido) -->
            <a 
              v-if="hasValidTrackingLink(selectedOrder)"
              :href="getTrackingUrl(selectedOrder)"
              target="_blank"
              rel="noopener noreferrer"
              class="w-full h-12 inline-flex items-center justify-center gap-2 bg-[#D81B60] text-white text-sm font-semibold rounded-xl hover:bg-[#C2185B] active:scale-[0.98] transition-all shadow-lg shadow-[#D81B60]/20 mb-3"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
              </svg>
              Rastrear envío
            </a>
            
            <!-- Botón secundario: Volver a comprar -->
            <button 
              @click="volverAComprar(selectedOrder); closeOrderDetail()"
              class="w-full h-11 inline-flex items-center justify-center gap-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-xl hover:bg-gray-50 hover:border-gray-400 active:scale-[0.98] transition-all"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
              </svg>
              Volver a comprar
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { productosService } from '../services/productos'
import { ordenesService } from '../services/ordenes'
import apiClient, { getImageUrl, hasValidToken } from '../services/api'

export default {
  name: 'MiCuenta',
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    // Handler para sesión expirada
    const handleSessionExpired = () => {
      console.log('Sesión expirada, redirigiendo a login...')
      router.push({ name: 'Login' })
    }
    
    // Estado
    const activeTab = ref('favoritos')
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
    
    // Favoritos
    const favoritos = ref([])
    const loadingFavoritos = ref(true)
    
    // Compras
    const compras = ref([])
    const loadingCompras = ref(true)
    
    // Datos de usuario (se cargarán del ClienteModel si existe)
    const datosUsuario = ref({
      nombre: user.value?.nombre || '',
      email: user.value?.email || '',
      telefono: user.value?.telefono || '',
      direccion: user.value?.direccion || '',
      departamento: '',
      municipio: '',
      barrio: ''
    })
    const guardando = ref(false)
    const loadingDatos = ref(false)
    
    // Order detail modal
    const selectedOrder = ref(null)
    
    // Computed
    const userName = computed(() => {
      if (!user.value) return 'Usuario'
      return user.value.nombre || user.value.email?.split('@')[0] || 'Usuario'
    })
    
    // Helper para leer IDs de localStorage (igual que Favoritos.vue)
    const loadWishlistIds = () => {
      try {
        const saved = localStorage.getItem('kharis_wishlist')
        return saved ? JSON.parse(saved) : []
      } catch {
        return []
      }
    }
    
    // Métodos
    const cargarFavoritos = async () => {
      loadingFavoritos.value = true
      
      // Leer IDs desde localStorage (fuente de verdad para favoritos)
      const ids = loadWishlistIds()
      
      if (ids.length === 0) {
        favoritos.value = []
        loadingFavoritos.value = false
        return
      }
      
      try {
        // Cargar productos y filtrar por los IDs guardados
        const response = await productosService.getProductos({ limit: 200 })
        const productos = response.results || response || []
        favoritos.value = productos.filter(p => ids.includes(p.id)).map(p => ({
          ...p,
          precio_monto: p.monto_precio || p.precio_monto || p.precio,
          precio_moneda: p.moneda_precio || p.precio_moneda || 'COP',
          categoria_nombre: p.categoria?.nombre || p.categoria_nombre || 'Extensiones'
        }))
      } catch (error) {
        console.error('Error cargando favoritos:', error)
        favoritos.value = []
      } finally {
        loadingFavoritos.value = false
      }
    }
    
    const cargarCompras = async () => {
      loadingCompras.value = true
      try {
        if (!user.value?.email) {
          compras.value = []
          return
        }

        const data = await ordenesService.obtenerPorEmail(user.value.email)
        const lista = Array.isArray(data) ? data : (data?.ordenes || data?.items || [])

        compras.value = lista.map((orden) => ({
          ...orden,
          estado: (orden.estado || '').toUpperCase(),
          items: (orden.items || []).map((item) => ({
            ...item,
            imagen: getImageUrl(item.imagen) || '/placeholder.jpg'
          }))
        }))
      } catch (error) {
        // 401 es esperado si el token expiró - no loguear como error
        if (error.response?.status !== 401) {
          console.error('Error cargando compras:', error)
        }
        compras.value = []
      } finally {
        loadingCompras.value = false
      }
    }
    
    const cargarDatosCliente = async () => {
      if (!user.value?.email) return
      
      loadingDatos.value = true
      try {
        // Intentar cargar datos del ClienteModel (datos de compras anteriores)
        const response = await apiClient.get(`/clientes/by-email/${encodeURIComponent(user.value.email)}`)
        const cliente = response.data
        
        if (cliente) {
          // Combinar nombre + apellido si ambos existen
          const nombreCompleto = [cliente.nombre, cliente.apellido].filter(Boolean).join(' ')
          
          datosUsuario.value = {
            nombre: nombreCompleto || user.value?.nombre || '',
            email: cliente.email || user.value?.email || '',
            telefono: cliente.telefono || '',
            direccion: cliente.direccion || '',
            departamento: cliente.departamento || '',
            municipio: cliente.municipio || '',
            barrio: cliente.barrio || ''
          }
        }
      } catch (error) {
        // 404 = cliente no existe, 401 = no autenticado - ambos son esperados
        if (error.response?.status !== 404 && error.response?.status !== 401) {
          console.error('Error cargando datos del cliente:', error)
        }
      } finally {
        loadingDatos.value = false
      }
    }

    const isVideo = (url) => {
      if (!url) return false
      const cleanUrl = url.split('?')[0].toLowerCase()
      return ['.mp4', '.webm', '.ogg', '.mov'].some(ext => cleanUrl.endsWith(ext))
    }

    const getCompraMediaUrl = (item) => {
      const raw = item?.imagen || item?.image || item?.imagen_principal || ''
      return getImageUrl(raw)
    }
    
    const quitarFavorito = (productoId) => {
      // Quitar del localStorage
      try {
        const ids = loadWishlistIds().filter(id => id !== productoId)
        localStorage.setItem('kharis_wishlist', JSON.stringify(ids))
      } catch (e) {
        console.error('Error actualizando localStorage:', e)
      }
      // Quitar de la lista visual
      favoritos.value = favoritos.value.filter(f => f.id !== productoId)
    }
    
    const irADetalle = (productoId) => {
      router.push(`/producto/${productoId}`)
    }
    
    const guardarDatos = async () => {
      guardando.value = true
      try {
        // TODO: Implementar endpoint
        // await apiClient.put('/auth/perfil', datosUsuario.value)
        alert('Datos guardados correctamente')
      } catch (error) {
        console.error('Error guardando datos:', error)
        alert('Error al guardar los datos')
      } finally {
        guardando.value = false
      }
    }
    
    const cerrarSesion = () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      router.push('/')
    }
    
    const formatPrice = (amount, currency = 'USD') => {
      if (!amount) return '$0'
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(amount)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    }
    
    const getEstadoClass = (estado) => {
      const clases = {
        'PENDIENTE': 'bg-yellow-50 text-yellow-700',
        'CONFIRMADO': 'bg-blue-50 text-blue-700',
        'ENVIADO': 'bg-purple-50 text-purple-700',
        'ENTREGADO': 'bg-green-50 text-green-700',
        'CANCELADO': 'bg-red-50 text-red-700'
      }
      return clases[estado] || 'bg-gray-50 text-gray-700'
    }
    
    // Formato precio COP
    const formatPriceCOP = (amount) => {
      if (!amount) return '$0'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(amount)
    }
    
    // Estado visual del pedido (para badges)
    const getEstadoVisualClass = (orden) => {
      if (orden.estado_envio === 'entregado') return 'bg-green-100 text-green-700'
      if (orden.estado_envio === 'enviado') return 'bg-blue-100 text-blue-700'
      if (orden.estado === 'cancelada') return 'bg-red-100 text-red-700'
      if (orden.estado_pago === 'pagado') return 'bg-emerald-50 text-emerald-700'
      return 'bg-amber-50 text-amber-700'
    }
    
    const getEstadoDotClass = (orden) => {
      if (orden.estado_envio === 'entregado') return 'bg-green-500'
      if (orden.estado_envio === 'enviado') return 'bg-blue-500 animate-pulse'
      if (orden.estado === 'cancelada') return 'bg-red-500'
      if (orden.estado_pago === 'pagado') return 'bg-emerald-500'
      return 'bg-amber-500'
    }
    
    const getEstadoLabel = (orden) => {
      if (orden.estado_envio === 'entregado') return 'Entregado'
      if (orden.estado_envio === 'enviado') return 'En camino'
      if (orden.estado === 'cancelada') return 'Cancelado'
      if (orden.estado_pago === 'pagado') return 'Confirmado'
      return 'Pendiente'
    }
    
    const getMetodoPagoLabel = (metodo) => {
      const metodos = {
        'wompi': 'Tarjeta/PSE',
        'transferencia': 'Transferencia',
        'whatsapp': 'Pago manual',
        'contraentrega': 'Contraentrega'
      }
      return metodos[metodo] || metodo || 'Pago manual'
    }
    
    // Estado directo tipo Mercado Libre (texto claro, sin badges)
    const getEstadoDirecto = (orden) => {
      if (orden.estado_envio === 'entregado') return '¡Entregado!'
      if (orden.estado_envio === 'enviado') return 'En tránsito'
      if (orden.estado === 'cancelada') return 'Pedido cancelado'
      if (orden.estado_pago === 'pagado') return 'Preparando tu pedido'
      return 'Pendiente de pago'
    }
    
    // Clase de color para estado directo
    const getEstadoTextClass = (orden) => {
      if (orden.estado_envio === 'entregado') return 'text-green-600'
      if (orden.estado_envio === 'enviado') return 'text-blue-600'
      if (orden.estado === 'cancelada') return 'text-red-600'
      if (orden.estado_pago === 'pagado') return 'text-gray-800'
      return 'text-amber-600'
    }
    
    // Fecha corta
    const formatDateShort = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleDateString('es-CO', {
        day: 'numeric',
        month: 'short'
      })
    }
    
    // Volver a comprar - agrega productos al carrito
    const volverAComprar = (orden) => {
      // Guardar items en localStorage para el carrito
      const cartItems = orden.items.map(item => ({
        producto_id: item.producto_id,
        nombre: item.nombre,
        cantidad: item.cantidad,
        precio: item.precio,
        imagen: item.imagen
      }))
      
      // Agregar al carrito existente o crear nuevo
      const existingCart = JSON.parse(localStorage.getItem('kharis_cart') || '[]')
      const newCart = [...existingCart, ...cartItems]
      localStorage.setItem('kharis_cart', JSON.stringify(newCart))
      
      // Notificar y redirigir
      alert(`${cartItems.length} producto(s) agregado(s) al carrito`)
      router.push('/catalogo')
    }
    
    // Ver detalle de orden - abre Bottom Sheet modal
    const verDetalleOrden = (orden) => {
      selectedOrder.value = orden
      // Bloquear scroll del body
      document.body.style.overflow = 'hidden'
    }
    
    // Cerrar modal de detalle
    const closeOrderDetail = () => {
      selectedOrder.value = null
      document.body.style.overflow = ''
    }
    
    // Verificar si hay tracking link válido
    const hasValidTrackingLink = (orden) => {
      return orden && orden.link_rastreo && orden.link_rastreo.trim() !== ''
    }
    
    // Obtener URL de tracking
    const getTrackingUrl = (orden) => {
      return orden?.link_rastreo || ''
    }
    
    // Verificar autenticación
    onMounted(() => {
      if (!user.value) {
        router.push('/')
        return
      }
      
      // Escuchar evento de sesión expirada
      window.addEventListener('session-expired', handleSessionExpired)
      
      // Establecer tab según parámetro de query
      const tabParam = route.query.tab
      if (tabParam && ['favoritos', 'compras', 'datos'].includes(tabParam)) {
        activeTab.value = tabParam
      }
      
      // Solo cargar datos si hay token válido
      if (hasValidToken()) {
        cargarFavoritos()
        cargarCompras()
        cargarDatosCliente()
      } else {
        // Token expirado o inválido - intentar cargar de todos modos
        // El interceptor de axios intentará refresh automáticamente
        cargarFavoritos()
        cargarCompras()
        cargarDatosCliente()
      }
    })
    
    onUnmounted(() => {
      window.removeEventListener('session-expired', handleSessionExpired)
    })
    
    return {
      activeTab,
      userName,
      favoritos,
      loadingFavoritos,
      compras,
      loadingCompras,
      datosUsuario,
      guardando,
      loadingDatos,
      quitarFavorito,
      irADetalle,
      guardarDatos,
      cerrarSesion,
      formatPrice,
      formatPriceCOP,
      formatDate,
      formatDateShort,
      getEstadoClass,
      getEstadoVisualClass,
      getEstadoDotClass,
      getEstadoLabel,
      getEstadoDirecto,
      getEstadoTextClass,
      getMetodoPagoLabel,
      getImageUrl,
      isVideo,
      getCompraMediaUrl,
      volverAComprar,
      verDetalleOrden,
      selectedOrder,
      closeOrderDetail,
      hasValidTrackingLink,
      getTrackingUrl
    }
  }
}
</script>

<style scoped>
.font-luxury {
  font-family: 'Playfair Display', serif;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
