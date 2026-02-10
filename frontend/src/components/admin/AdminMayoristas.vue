<template>
  <div class="p-6 lg:p-8">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
      <div>
        <h1 class="text-2xl font-semibold text-text-dark">Solicitudes Mayoristas</h1>
        <p class="text-text-light mt-1">Gestiona las solicitudes de cuentas mayoristas</p>
      </div>
      
      <!-- Stats rápidas -->
      <div class="flex items-center gap-4">
        <div class="px-4 py-2 bg-amber-50 border border-amber-200 rounded-lg">
          <span class="text-amber-700 font-semibold">{{ pendingCount }}</span>
          <span class="text-amber-600 text-sm ml-1">pendientes</span>
        </div>
        <div class="px-4 py-2 bg-green-50 border border-green-200 rounded-lg">
          <span class="text-green-700 font-semibold">{{ approvedCount }}</span>
          <span class="text-green-600 text-sm ml-1">aprobados</span>
        </div>
      </div>
    </div>

    <!-- Filtros -->
    <div class="bg-white rounded-xl border border-gray-200 p-4 mb-6">
      <div class="flex flex-wrap items-center gap-4">
        <!-- Tabs de estado -->
        <div class="flex bg-gray-100 rounded-lg p-1">
          <button
            v-for="tab in statusTabs"
            :key="tab.value"
            @click="activeTab = tab.value"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-md transition-all',
              activeTab === tab.value 
                ? 'bg-white text-text-dark shadow-sm' 
                : 'text-text-light hover:text-text-dark'
            ]"
          >
            {{ tab.label }}
            <span 
              v-if="tab.count > 0"
              :class="[
                'ml-1.5 px-1.5 py-0.5 text-xs rounded-full',
                activeTab === tab.value ? 'bg-brand-100 text-brand-600' : 'bg-gray-200 text-gray-600'
              ]"
            >
              {{ tab.count }}
            </span>
          </button>
        </div>

        <!-- Búsqueda -->
        <div class="flex-1 min-w-[200px]">
          <div class="relative">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar por nombre, email, empresa..."
              class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 outline-none"
            />
          </div>
        </div>

        <!-- Refresh -->
        <button 
          @click="fetchSolicitudes"
          :disabled="loading"
          class="p-2.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg :class="['w-5 h-5', loading && 'animate-spin']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && solicitudes.length === 0" class="flex justify-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredSolicitudes.length === 0" class="bg-white rounded-xl border border-gray-200 p-12 text-center">
      <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-text-dark mb-1">No hay solicitudes</h3>
      <p class="text-text-light">
        {{ activeTab === 'all' ? 'Aún no hay solicitudes de mayoristas' : `No hay solicitudes ${getStatusLabel(activeTab).toLowerCase()}` }}
      </p>
    </div>

    <!-- Tabla de Solicitudes -->
    <div v-else class="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left px-6 py-4 text-xs font-semibold text-text-light uppercase tracking-wider">Solicitante</th>
              <th class="text-left px-6 py-4 text-xs font-semibold text-text-light uppercase tracking-wider">Empresa</th>
              <th class="text-left px-6 py-4 text-xs font-semibold text-text-light uppercase tracking-wider">Documento</th>
              <th class="text-left px-6 py-4 text-xs font-semibold text-text-light uppercase tracking-wider">Fecha</th>
              <th class="text-left px-6 py-4 text-xs font-semibold text-text-light uppercase tracking-wider">Estado</th>
              <th class="text-right px-6 py-4 text-xs font-semibold text-text-light uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr 
              v-for="solicitud in filteredSolicitudes" 
              :key="solicitud.id"
              class="hover:bg-gray-50 transition-colors"
            >
              <!-- Solicitante -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center text-white font-medium">
                    {{ getInitials(solicitud.nombre, solicitud.apellido) }}
                  </div>
                  <div>
                    <p class="font-medium text-text-dark">{{ solicitud.nombre }} {{ solicitud.apellido }}</p>
                    <p class="text-sm text-text-light">{{ solicitud.email }}</p>
                  </div>
                </div>
              </td>

              <!-- Empresa -->
              <td class="px-6 py-4">
                <p class="text-text-dark">{{ solicitud.nombre_empresa || '—' }}</p>
                <p class="text-sm text-text-light">{{ solicitud.telefono }}</p>
              </td>

              <!-- Documento -->
              <td class="px-6 py-4">
                <p class="text-text-dark">{{ solicitud.tipo_documento }}</p>
                <p class="text-sm text-text-light font-mono">{{ solicitud.numero_documento }}</p>
              </td>

              <!-- Fecha -->
              <td class="px-6 py-4">
                <p class="text-text-dark">{{ formatDate(solicitud.date_joined) }}</p>
                <p class="text-sm text-text-light">{{ formatTime(solicitud.date_joined) }}</p>
              </td>

              <!-- Estado -->
              <td class="px-6 py-4">
                <span :class="getStatusBadgeClass(solicitud.estado_mayorista)">
                  {{ getStatusLabel(solicitud.estado_mayorista) }}
                </span>
              </td>

              <!-- Acciones -->
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <!-- Ver documentos -->
                  <button 
                    @click="openDocuments(solicitud)"
                    class="p-2 text-gray-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="Ver documentos"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>

                  <!-- Aprobar (solo si está pendiente) -->
                  <button 
                    v-if="solicitud.estado_mayorista === 'PENDIENTE' || solicitud.estado_mayorista === 'EN_REVISION'"
                    @click="aprobar(solicitud)"
                    :disabled="actionLoading === solicitud.id"
                    class="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors disabled:opacity-50"
                    title="Aprobar"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </button>

                  <!-- Rechazar (solo si está pendiente) -->
                  <button 
                    v-if="solicitud.estado_mayorista === 'PENDIENTE' || solicitud.estado_mayorista === 'EN_REVISION'"
                    @click="openRejectModal(solicitud)"
                    :disabled="actionLoading === solicitud.id"
                    class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                    title="Rechazar"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>

                  <!-- Suspender (solo si está aprobado) -->
                  <button 
                    v-if="solicitud.estado_mayorista === 'APROBADO'"
                    @click="suspender(solicitud)"
                    :disabled="actionLoading === solicitud.id"
                    class="p-2 text-amber-600 hover:bg-amber-50 rounded-lg transition-colors disabled:opacity-50"
                    title="Suspender"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                    </svg>
                  </button>

                  <!-- Reactivar (si está suspendido o rechazado) -->
                  <button 
                    v-if="solicitud.estado_mayorista === 'SUSPENDIDO' || solicitud.estado_mayorista === 'RECHAZADO'"
                    @click="aprobar(solicitud)"
                    :disabled="actionLoading === solicitud.id"
                    class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors disabled:opacity-50"
                    title="Reactivar"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </button>

                  <!-- Cambiar contraseña -->
                  <button 
                    @click="openPasswordModal(solicitud)"
                    :disabled="actionLoading === solicitud.id"
                    class="p-2 text-purple-600 hover:bg-purple-50 rounded-lg transition-colors disabled:opacity-50"
                    title="Cambiar contraseña"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Ver Documentos -->
    <div 
      v-if="showDocumentsModal" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
      @click.self="showDocumentsModal = false"
    >
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-3xl max-h-[90vh] overflow-hidden">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-lg font-semibold text-text-dark">Documentos de Verificación</h3>
            <p class="text-sm text-text-light">{{ selectedSolicitud?.nombre }} {{ selectedSolicitud?.apellido }}</p>
          </div>
          <button 
            @click="showDocumentsModal = false"
            class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Content -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
          <!-- Info del solicitante -->
          <div class="grid sm:grid-cols-2 gap-4 mb-6 p-4 bg-gray-50 rounded-xl">
            <div>
              <p class="text-xs text-text-light uppercase tracking-wider mb-1">Email</p>
              <p class="text-text-dark font-medium">{{ selectedSolicitud?.email }}</p>
            </div>
            <div>
              <p class="text-xs text-text-light uppercase tracking-wider mb-1">Teléfono</p>
              <p class="text-text-dark font-medium">{{ selectedSolicitud?.telefono || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-text-light uppercase tracking-wider mb-1">Empresa</p>
              <p class="text-text-dark font-medium">{{ selectedSolicitud?.nombre_empresa || 'No especificada' }}</p>
            </div>
            <div>
              <p class="text-xs text-text-light uppercase tracking-wider mb-1">Documento</p>
              <p class="text-text-dark font-medium">{{ selectedSolicitud?.tipo_documento }} {{ selectedSolicitud?.numero_documento }}</p>
            </div>
          </div>

          <!-- Imágenes de cédula -->
          <div class="grid sm:grid-cols-2 gap-6">
            <div>
              <p class="text-sm font-medium text-text-dark mb-3">Cédula / RUT (Frente)</p>
              <div class="aspect-[3/2] bg-gray-100 rounded-xl overflow-hidden border border-gray-200">
                <img 
                  v-if="selectedSolicitud?.cedula_frente && !imageErrors.frente"
                  :src="getImageUrl(selectedSolicitud.cedula_frente)"
                  alt="Cédula Frente"
                  class="w-full h-full object-contain cursor-pointer hover:opacity-90"
                  @click="openFullImage(selectedSolicitud.cedula_frente)"
                  @error="imageErrors.frente = true"
                />
                <div v-else class="w-full h-full flex flex-col items-center justify-center text-gray-400 gap-2">
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="text-sm">{{ imageErrors.frente ? 'Imagen no disponible' : 'No subida' }}</span>
                </div>
              </div>
            </div>
            <div>
              <p class="text-sm font-medium text-text-dark mb-3">Cédula / RUT (Dorso)</p>
              <div class="aspect-[3/2] bg-gray-100 rounded-xl overflow-hidden border border-gray-200">
                <img 
                  v-if="selectedSolicitud?.cedula_dorso && !imageErrors.dorso"
                  :src="getImageUrl(selectedSolicitud.cedula_dorso)"
                  alt="Cédula Dorso"
                  class="w-full h-full object-contain cursor-pointer hover:opacity-90"
                  @click="openFullImage(selectedSolicitud.cedula_dorso)"
                  @error="imageErrors.dorso = true"
                />
                <div v-else class="w-full h-full flex flex-col items-center justify-center text-gray-400 gap-2">
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="text-sm">{{ imageErrors.dorso ? 'Imagen no disponible' : 'No subida' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Notas de revisión (si existen) -->
          <div v-if="selectedSolicitud?.notas_revision" class="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-xl">
            <p class="text-sm font-medium text-amber-800 mb-1">Notas de Revisión</p>
            <p class="text-sm text-amber-700">{{ selectedSolicitud.notas_revision }}</p>
          </div>
        </div>

        <!-- Footer -->
        <div 
          v-if="selectedSolicitud?.estado_mayorista === 'PENDIENTE' || selectedSolicitud?.estado_mayorista === 'EN_REVISION'"
          class="flex items-center justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50"
        >
          <button
            @click="openRejectModal(selectedSolicitud); showDocumentsModal = false"
            class="px-5 py-2.5 border border-red-300 text-red-600 font-medium rounded-lg hover:bg-red-50 transition-colors"
          >
            Rechazar
          </button>
          <button
            @click="aprobar(selectedSolicitud); showDocumentsModal = false"
            class="px-5 py-2.5 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors"
          >
            Aprobar Solicitud
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Rechazar -->
    <div 
      v-if="showRejectModal" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
      @click.self="showRejectModal = false"
    >
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md">
        <div class="p-6">
          <div class="w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          
          <h3 class="text-lg font-semibold text-text-dark text-center mb-2">Rechazar Solicitud</h3>
          <p class="text-text-light text-center text-sm mb-6">
            ¿Estás seguro de rechazar la solicitud de <strong>{{ rejectingSolicitud?.nombre }}</strong>?
          </p>

          <div class="mb-6">
            <label class="block text-sm font-medium text-text-dark mb-2">Motivo del rechazo</label>
            <textarea
              v-model="rejectReason"
              rows="3"
              placeholder="Ej: Documentos ilegibles, información incompleta..."
              class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-red-500/20 focus:border-red-500 outline-none resize-none"
            ></textarea>
          </div>

          <div class="flex gap-3">
            <button
              @click="showRejectModal = false"
              class="flex-1 px-4 py-3 border border-gray-300 text-text-dark font-medium rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
            <button
              @click="rechazar"
              :disabled="actionLoading"
              class="flex-1 px-4 py-3 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
            >
              {{ actionLoading ? 'Rechazando...' : 'Confirmar Rechazo' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Cambiar Contraseña -->
    <div 
      v-if="showPasswordModal" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
      @click.self="showPasswordModal = false"
    >
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md">
        <div class="p-6">
          <div class="w-12 h-12 mx-auto mb-4 bg-purple-100 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
          </div>
          
          <h3 class="text-lg font-semibold text-text-dark text-center mb-1">Cambiar Contraseña</h3>
          <p class="text-text-light text-center text-sm mb-6">
            Establecer nueva contraseña para <strong>{{ passwordSolicitud?.nombre }} {{ passwordSolicitud?.apellido }}</strong>
            <br/>
            <span class="text-xs text-text-light">{{ passwordSolicitud?.email }}</span>
          </p>

          <form @submit.prevent="submitPasswordChange">
            <div class="mb-4">
              <label class="block text-sm font-medium text-text-dark mb-2">Nueva contraseña</label>
              <div class="relative">
                <input
                  v-model="newAdminPassword"
                  :type="showAdminNewPassword ? 'text' : 'password'"
                  required
                  minlength="8"
                  placeholder="Mínimo 8 caracteres"
                  class="w-full px-4 py-3 pr-12 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 outline-none"
                />
                <button
                  type="button"
                  @click="showAdminNewPassword = !showAdminNewPassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <svg v-if="showAdminNewPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="mb-6">
              <label class="block text-sm font-medium text-text-dark mb-2">Confirmar contraseña</label>
              <input
                v-model="confirmAdminPassword"
                :type="showAdminNewPassword ? 'text' : 'password'"
                required
                placeholder="Repite la contraseña"
                class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 outline-none"
                :class="confirmAdminPassword && confirmAdminPassword !== newAdminPassword 
                  ? 'border-red-300' 
                  : confirmAdminPassword && confirmAdminPassword === newAdminPassword 
                    ? 'border-green-400' 
                    : 'border-gray-200'"
              />
              <p v-if="confirmAdminPassword && confirmAdminPassword !== newAdminPassword" class="text-sm text-red-500 mt-1">
                Las contraseñas no coinciden
              </p>
            </div>

            <!-- Error -->
            <div v-if="passwordError" class="mb-4 p-3 rounded-lg bg-red-50 border border-red-200">
              <p class="text-sm text-red-700">{{ passwordError }}</p>
            </div>

            <div class="flex gap-3">
              <button
                type="button"
                @click="showPasswordModal = false"
                class="flex-1 px-4 py-3 border border-gray-300 text-text-dark font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="actionLoading || !newAdminPassword || newAdminPassword.length < 8 || newAdminPassword !== confirmAdminPassword"
                class="flex-1 px-4 py-3 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <svg v-if="actionLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ actionLoading ? 'Guardando...' : 'Cambiar Contraseña' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Toast de notificación -->
    <transition name="slide-up">
      <div 
        v-if="toast.show"
        :class="[
          'fixed bottom-6 right-6 z-50 px-6 py-4 rounded-xl shadow-lg flex items-center gap-3',
          toast.type === 'success' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
        ]"
      >
        <svg v-if="toast.type === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span>{{ toast.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'AdminMayoristas',
  setup() {
    // =========================================================================
    // STATE
    // =========================================================================
    const loading = ref(false)
    const actionLoading = ref(null)
    const solicitudes = ref([])
    const activeTab = ref('PENDIENTE')
    const searchQuery = ref('')
    
    const showDocumentsModal = ref(false)
    const selectedSolicitud = ref(null)
    const imageErrors = ref({ frente: false, dorso: false })
    
    const showRejectModal = ref(false)
    const rejectingSolicitud = ref(null)
    const rejectReason = ref('')

    const showPasswordModal = ref(false)
    const passwordSolicitud = ref(null)
    const newAdminPassword = ref('')
    const confirmAdminPassword = ref('')
    const showAdminNewPassword = ref(false)
    const passwordError = ref('')
    
    const toast = ref({ show: false, message: '', type: 'success' })

    // VITE_API_URL ya incluye /api/v1, así que usamos la base URL directamente
    const API_BASE = import.meta.env.VITE_API_URL?.replace('/api/v1', '') || 'http://localhost:8000'

    // =========================================================================
    // COMPUTED
    // =========================================================================
    const statusTabs = computed(() => [
      { label: 'Pendientes', value: 'PENDIENTE', count: solicitudes.value.filter(s => s.estado_mayorista === 'PENDIENTE').length },
      { label: 'En Revisión', value: 'EN_REVISION', count: solicitudes.value.filter(s => s.estado_mayorista === 'EN_REVISION').length },
      { label: 'Aprobados', value: 'APROBADO', count: solicitudes.value.filter(s => s.estado_mayorista === 'APROBADO').length },
      { label: 'Rechazados', value: 'RECHAZADO', count: solicitudes.value.filter(s => s.estado_mayorista === 'RECHAZADO').length },
      { label: 'Todos', value: 'all', count: solicitudes.value.length }
    ])

    const pendingCount = computed(() => 
      solicitudes.value.filter(s => s.estado_mayorista === 'PENDIENTE' || s.estado_mayorista === 'EN_REVISION').length
    )

    const approvedCount = computed(() => 
      solicitudes.value.filter(s => s.estado_mayorista === 'APROBADO').length
    )

    const filteredSolicitudes = computed(() => {
      let result = solicitudes.value

      // Filtrar por tab
      if (activeTab.value !== 'all') {
        result = result.filter(s => s.estado_mayorista === activeTab.value)
      }

      // Filtrar por búsqueda
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(s => 
          s.nombre?.toLowerCase().includes(query) ||
          s.apellido?.toLowerCase().includes(query) ||
          s.email?.toLowerCase().includes(query) ||
          s.nombre_empresa?.toLowerCase().includes(query) ||
          s.numero_documento?.includes(query)
        )
      }

      return result
    })

    // =========================================================================
    // METHODS
    // =========================================================================
    function getAuthHeaders() {
      const token = localStorage.getItem('access_token')
      return { Authorization: `Bearer ${token}` }
    }

    async function fetchSolicitudes() {
      loading.value = true
      console.log('🔍 Fetching solicitudes from:', `${API_BASE}/api/v1/mayoristas`)
      try {
        const response = await axios.get(`${API_BASE}/api/v1/mayoristas`, {
          headers: getAuthHeaders()
        })
        console.log('✅ Response:', response.data)
        // Asegurar que siempre sea un array
        const data = response.data
        if (Array.isArray(data)) {
          solicitudes.value = data
        } else if (data && Array.isArray(data.results)) {
          // Por si viene paginado
          solicitudes.value = data.results
        } else if (data && Array.isArray(data.data)) {
          solicitudes.value = data.data
        } else {
          console.warn('Respuesta inesperada de mayoristas:', data)
          solicitudes.value = []
        }
        console.log('📋 Solicitudes cargadas:', solicitudes.value.length)
      } catch (err) {
        console.error('❌ Error al cargar solicitudes:', err.response?.status, err.response?.data || err.message)
        solicitudes.value = [] // Resetear a array vacío en caso de error
        showToast('Error al cargar solicitudes', 'error')
      } finally {
        loading.value = false
      }
    }

    async function aprobar(solicitud) {
      actionLoading.value = solicitud.id
      try {
        await axios.post(`${API_BASE}/api/v1/mayoristas/${solicitud.id}/aprobar`, {}, {
          headers: getAuthHeaders()
        })
        showToast(`Solicitud de ${solicitud.nombre} aprobada`, 'success')
        await fetchSolicitudes()
      } catch (err) {
        console.error('Error al aprobar:', err)
        showToast('Error al aprobar solicitud', 'error')
      } finally {
        actionLoading.value = null
      }
    }

    async function rechazar() {
      if (!rejectingSolicitud.value) return
      
      actionLoading.value = rejectingSolicitud.value.id
      try {
        await axios.post(`${API_BASE}/api/v1/mayoristas/${rejectingSolicitud.value.id}/rechazar`, {
          notas: rejectReason.value
        }, {
          headers: getAuthHeaders()
        })
        showToast(`Solicitud de ${rejectingSolicitud.value.nombre} rechazada`, 'success')
        showRejectModal.value = false
        rejectReason.value = ''
        await fetchSolicitudes()
      } catch (err) {
        console.error('Error al rechazar:', err)
        showToast('Error al rechazar solicitud', 'error')
      } finally {
        actionLoading.value = null
      }
    }

    async function suspender(solicitud) {
      actionLoading.value = solicitud.id
      try {
        await axios.post(`${API_BASE}/api/v1/mayoristas/${solicitud.id}/suspender`, {}, {
          headers: getAuthHeaders()
        })
        showToast(`Cuenta de ${solicitud.nombre} suspendida`, 'success')
        await fetchSolicitudes()
      } catch (err) {
        console.error('Error al suspender:', err)
        showToast('Error al suspender cuenta', 'error')
      } finally {
        actionLoading.value = null
      }
    }

    function openDocuments(solicitud) {
      selectedSolicitud.value = solicitud
      imageErrors.value = { frente: false, dorso: false } // Reset errores de imagen
      showDocumentsModal.value = true
    }

    function openRejectModal(solicitud) {
      rejectingSolicitud.value = solicitud
      rejectReason.value = ''
      showRejectModal.value = true
    }

    function openPasswordModal(solicitud) {
      passwordSolicitud.value = solicitud
      newAdminPassword.value = ''
      confirmAdminPassword.value = ''
      showAdminNewPassword.value = false
      passwordError.value = ''
      showPasswordModal.value = true
    }

    async function submitPasswordChange() {
      if (!passwordSolicitud.value) return
      if (newAdminPassword.value !== confirmAdminPassword.value) {
        passwordError.value = 'Las contraseñas no coinciden'
        return
      }
      if (newAdminPassword.value.length < 8) {
        passwordError.value = 'La contraseña debe tener al menos 8 caracteres'
        return
      }

      actionLoading.value = passwordSolicitud.value.id
      passwordError.value = ''
      try {
        await axios.post(
          `${API_BASE}/api/v1/mayoristas/${passwordSolicitud.value.id}/cambiar-password`,
          { new_password: newAdminPassword.value },
          { headers: getAuthHeaders() }
        )
        showToast(`Contraseña cambiada para ${passwordSolicitud.value.nombre}`, 'success')
        showPasswordModal.value = false
      } catch (err) {
        console.error('Error al cambiar contraseña:', err)
        passwordError.value = err.response?.data?.detail || 'Error al cambiar la contraseña'
      } finally {
        actionLoading.value = null
      }
    }

    function openFullImage(url) {
      window.open(getImageUrl(url), '_blank')
    }

    function getImageUrl(path) {
      if (!path) return ''
      if (path.startsWith('http')) return path
      return `${API_BASE}${path}`
    }

    function getInitials(nombre, apellido) {
      const n = nombre?.charAt(0) || ''
      const a = apellido?.charAt(0) || ''
      return (n + a).toUpperCase() || '?'
    }

    function getStatusLabel(status) {
      const labels = {
        'PENDIENTE': 'Pendiente',
        'EN_REVISION': 'En Revisión',
        'APROBADO': 'Aprobado',
        'RECHAZADO': 'Rechazado',
        'SUSPENDIDO': 'Suspendido'
      }
      return labels[status] || status
    }

    function getStatusBadgeClass(status) {
      const classes = {
        'PENDIENTE': 'px-3 py-1 text-xs font-medium rounded-full bg-amber-100 text-amber-700',
        'EN_REVISION': 'px-3 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-700',
        'APROBADO': 'px-3 py-1 text-xs font-medium rounded-full bg-green-100 text-green-700',
        'RECHAZADO': 'px-3 py-1 text-xs font-medium rounded-full bg-red-100 text-red-700',
        'SUSPENDIDO': 'px-3 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700'
      }
      return classes[status] || 'px-3 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-600'
    }

    function formatDate(dateStr) {
      if (!dateStr) return '—'
      return new Date(dateStr).toLocaleDateString('es-CO', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      })
    }

    function formatTime(dateStr) {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleTimeString('es-CO', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    function showToast(message, type = 'success') {
      toast.value = { show: true, message, type }
      setTimeout(() => {
        toast.value.show = false
      }, 3000)
    }

    // =========================================================================
    // LIFECYCLE
    // =========================================================================
    onMounted(() => {
      fetchSolicitudes()
    })

    // =========================================================================
    // RETURN
    // =========================================================================
    return {
      loading,
      actionLoading,
      solicitudes,
      activeTab,
      searchQuery,
      statusTabs,
      pendingCount,
      approvedCount,
      filteredSolicitudes,
      showDocumentsModal,
      selectedSolicitud,
      imageErrors,
      showRejectModal,
      rejectingSolicitud,
      rejectReason,
      toast,
      fetchSolicitudes,
      aprobar,
      rechazar,
      suspender,
      openDocuments,
      openRejectModal,
      openPasswordModal,
      showPasswordModal,
      passwordSolicitud,
      newAdminPassword,
      confirmAdminPassword,
      showAdminNewPassword,
      passwordError,
      submitPasswordChange,
      openFullImage,
      getImageUrl,
      getInitials,
      getStatusLabel,
      getStatusBadgeClass,
      formatDate,
      formatTime
    }
  }
}
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
