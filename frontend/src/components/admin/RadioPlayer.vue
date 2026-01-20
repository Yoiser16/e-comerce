<template>
  <Teleport to="body">
    <Transition name="fade">
      <div 
        v-if="visible" 
        class="fixed inset-0 bg-black/40 z-[100] flex items-center justify-center p-4"
        @click="closeModal"
      >
        <!-- Contenedor Principal - Modo Claro Elegante -->
        <div 
          class="radio-modal-container w-full max-w-[1000px] h-[80vh] max-h-[680px] rounded-2xl shadow-2xl overflow-hidden flex flex-col relative font-sans bg-white border border-slate-200"
          @click.stop
        >
          
          <!-- Botón Cerrar -->
          <button 
            @click="closeModal"
            class="absolute top-4 right-4 z-50 rounded-full p-2 transition-all duration-200 text-slate-400 hover:text-slate-600 hover:bg-slate-100"
          >
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- LAYOUT PRINCIPAL - Sidebar + Content -->
          <div class="flex-1 flex overflow-hidden">
            
            <!-- SIDEBAR - Estilo Elegante -->
            <aside class="w-52 flex flex-col flex-shrink-0 border-r bg-slate-50/80 border-slate-200">
              <div class="p-5">
                <!-- Logo 105 Radio -->
                <div class="flex items-center gap-2.5 mb-8">
                  <div class="w-9 h-9 bg-gradient-to-br from-rose-400 to-pink-500 rounded-xl flex items-center justify-center shadow-sm">
                    <span class="text-white font-bold text-xs">105</span>
                  </div>
                  <span class="font-semibold text-base text-slate-800">105 Radio</span>
                </div>

                <!-- Navegación Principal -->
                <nav class="space-y-1">
                  <button 
                    @click="goHome"
                    class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-150 text-sm font-medium"
                    :class="currentView === 'home' && !currentCityFilter
                      ? 'bg-white text-slate-800 shadow-sm border border-slate-200'
                      : 'text-slate-500 hover:text-slate-700 hover:bg-white/60'"
                  >
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3 9.5L12 4l9 5.5M4 10v9a1 1 0 001 1h4v-5a1 1 0 011-1h4a1 1 0 011 1v5h4a1 1 0 001-1v-9" />
                    </svg>
                    Inicio
                  </button>
                  
                  <!-- Favoritos -->
                  <button 
                    @click="currentView = 'favorites'"
                    class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-150 text-sm font-medium"
                    :class="currentView === 'favorites' 
                      ? 'bg-white text-slate-800 shadow-sm border border-slate-200'
                      : 'text-slate-500 hover:text-slate-700 hover:bg-white/60'"
                  >
                    <svg class="h-4 w-4" :fill="currentView === 'favorites' ? 'currentColor' : 'none'" :class="currentView === 'favorites' ? 'text-rose-500' : ''" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
                    </svg>
                    Favoritos
                    <span 
                      v-if="favoriteRadios.length > 0"
                      class="ml-auto text-[10px] font-semibold px-1.5 py-0.5 rounded-full bg-rose-100 text-rose-600"
                    >
                      {{ favoriteRadios.length }}
                    </span>
                  </button>
                </nav>
                  
                <!-- Ciudades -->
                <div class="mt-8">
                  <h3 class="px-3 text-[11px] font-semibold uppercase tracking-wider mb-2 text-slate-400">Ciudades</h3>
                  <div class="space-y-0.5">
                    <button 
                      v-for="city in cities" 
                      :key="city.name"
                      @click="filterByCity(city.name)" 
                      class="w-full text-left px-3 py-2 text-sm rounded-xl transition-all duration-150 flex items-center gap-2.5"
                      :class="currentCityFilter === city.name 
                        ? 'bg-white text-slate-800 shadow-sm border border-slate-200'
                        : 'text-slate-500 hover:text-slate-700 hover:bg-white/60'"
                    >
                      <span class="w-2 h-2 rounded-full" :class="city.color"></span> {{ city.name }}
                    </button>
                  </div>
                </div>
              </div>
            </aside>

            <!-- ÁREA PRINCIPAL -->
            <main class="flex-1 relative overflow-y-auto custom-scrollbar pb-28 bg-white">
              
              <!-- Header con Search -->
              <header class="sticky top-0 z-30 px-6 py-4 border-b bg-white/95 border-slate-100">
                <div class="flex items-center gap-4">
                  <span class="text-sm font-medium text-slate-500">{{ greeting }}</span>
                  <div class="relative flex-1 max-w-xs">
                    <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </span>
                    <input 
                      type="text" 
                      v-model="searchQuery"
                      @input="handleSearch"
                      placeholder="Buscar emisoras..." 
                      class="w-full pl-9 pr-4 py-2 rounded-xl text-sm transition-all duration-150 focus:outline-none focus:ring-2 bg-slate-50 text-slate-700 placeholder-slate-400 focus:ring-rose-200 border border-slate-200 focus:border-rose-300"
                    />
                  </div>
                </div>
              </header>

              <div class="p-6 space-y-8">
                
                <!-- VIEW: SEARCH RESULTS -->
                <div v-if="currentView === 'search' && searchQuery">
                  <h2 class="text-base font-semibold mb-5 text-slate-800">Resultados</h2>
                  <div v-if="filteredRadios.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    <div 
                      v-for="station in filteredRadios" 
                      :key="station.id"
                      @click="playStation(station)"
                      class="group cursor-pointer"
                    >
                      <div class="relative aspect-square rounded-2xl overflow-hidden mb-3 border-2 transition-all duration-200 bg-slate-50 hover:shadow-lg"
                           :class="currentRadio?.id === station.id ? 'border-rose-400 shadow-lg shadow-rose-100' : 'border-slate-100 hover:border-slate-200'">
                        <img 
                          v-if="station.logo"
                          :src="station.logo" 
                          :alt="station.name"
                          class="w-full h-full object-contain p-5"
                          @error="handleImageError"
                        />
                        <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br" :class="getGradientColor(station.name)">
                          <span class="text-white font-bold text-2xl drop-shadow">{{ getInitials(station.name) }}</span>
                        </div>
                        
                        <!-- Hover overlay -->
                        <div class="absolute inset-0 flex items-center justify-center transition-opacity duration-200 opacity-0 group-hover:opacity-100 bg-black/20">
                          <button class="w-12 h-12 rounded-full flex items-center justify-center shadow-lg" :class="currentRadio?.id === station.id && isPlaying ? 'bg-rose-500 text-white' : 'bg-white text-slate-700'">
                            <svg v-if="currentRadio?.id === station.id && isPlaying" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                            </svg>
                            <svg v-else class="h-5 w-5 ml-0.5" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M8 5v14l11-7z" />
                            </svg>
                          </button>
                        </div>
                        
                        <!-- Favorite button -->
                        <button 
                          @click.stop="toggleFavorite(station)"
                          class="absolute top-2 right-2 z-10 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 shadow-sm"
                          :class="isFavorite(station.id) ? 'bg-rose-500 text-white' : 'opacity-0 group-hover:opacity-100 bg-white/90 text-slate-400 hover:text-rose-500'"
                        >
                          <svg class="h-4 w-4" :fill="isFavorite(station.id) ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
                          </svg>
                        </button>
                        
                        <!-- Live indicator -->
                        <div v-if="currentRadio?.id === station.id && isPlaying" class="absolute top-2 left-2 px-2 py-1 bg-rose-500 rounded-full text-[10px] font-semibold text-white uppercase tracking-wide flex items-center gap-1 shadow-sm">
                          <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                          EN VIVO
                        </div>
                      </div>
                      <h3 class="font-medium text-sm truncate px-1" :class="currentRadio?.id === station.id && isPlaying ? 'text-rose-600' : 'text-slate-700'">{{ station.name }}</h3>
                      <p v-if="station.city" class="text-xs text-slate-400 truncate px-1">{{ station.city }}</p>
                    </div>
                  </div>
                  <div v-else class="text-center py-16 text-slate-400">
                    <svg class="h-12 w-12 mx-auto mb-3 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <p class="text-sm">No encontramos emisoras</p>
                  </div>
                </div>

                <!-- VIEW: FAVORITES -->
                <div v-else-if="currentView === 'favorites'">
                  <div class="flex items-center gap-3 mb-5">
                    <h2 class="text-base font-semibold text-slate-800">Mis Favoritas</h2>
                    <span v-if="favoriteRadios.length > 0" class="text-xs px-2 py-0.5 rounded-full font-medium bg-rose-100 text-rose-600">
                      {{ favoriteRadios.length }}
                    </span>
                  </div>
                  
                  <div v-if="favoriteRadios.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    <div 
                      v-for="station in favoriteRadios" 
                      :key="station.id"
                      @click="playStation(station)"
                      class="group cursor-pointer"
                    >
                      <div class="relative aspect-square rounded-2xl overflow-hidden mb-3 border-2 transition-all duration-200 bg-slate-50 hover:shadow-lg"
                           :class="currentRadio?.id === station.id ? 'border-rose-400 shadow-lg shadow-rose-100' : 'border-slate-100 hover:border-slate-200'">
                        <img 
                          v-if="station.logo"
                          :src="station.logo" 
                          :alt="station.name"
                          class="w-full h-full object-contain p-5"
                          @error="handleImageError"
                        />
                        <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br" :class="getGradientColor(station.name)">
                          <span class="text-white font-bold text-2xl drop-shadow">{{ getInitials(station.name) }}</span>
                        </div>
                        
                        <!-- Favorite button (always visible) -->
                        <button 
                          @click.stop="toggleFavorite(station)"
                          class="absolute top-2 right-2 z-10 w-8 h-8 rounded-full flex items-center justify-center bg-rose-500 text-white shadow-sm"
                        >
                          <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
                          </svg>
                        </button>
                        
                        <!-- Live indicator -->
                        <div v-if="currentRadio?.id === station.id && isPlaying" class="absolute top-2 left-2 px-2 py-1 bg-rose-500 rounded-full text-[10px] font-semibold text-white uppercase tracking-wide flex items-center gap-1 shadow-sm">
                          <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                          EN VIVO
                        </div>
                      </div>
                      <h3 class="font-medium text-sm truncate px-1" :class="currentRadio?.id === station.id && isPlaying ? 'text-rose-600' : 'text-slate-700'">{{ station.name }}</h3>
                      <p v-if="station.city" class="text-xs text-slate-400 truncate px-1">{{ station.city }}</p>
                    </div>
                  </div>
                  
                  <div v-else class="text-center py-16">
                    <div class="w-16 h-16 rounded-2xl mx-auto mb-4 flex items-center justify-center bg-rose-50">
                      <svg class="h-7 w-7 text-rose-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
                      </svg>
                    </div>
                    <p class="text-sm font-medium mb-1 text-slate-600">Sin favoritas aún</p>
                    <p class="text-xs text-slate-400">Toca el corazón en cualquier emisora</p>
                  </div>
                </div>

                <!-- VIEW: HOME (default) -->
                <div v-else class="space-y-8">
                  
                  <!-- Loading State -->
                  <div v-if="loading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    <div v-for="i in 8" :key="i" class="animate-pulse">
                      <div class="aspect-square rounded-2xl bg-slate-200 mb-3"></div>
                      <div class="h-4 bg-slate-200 rounded w-3/4 mb-2"></div>
                      <div class="h-3 bg-slate-100 rounded w-1/2"></div>
                    </div>
                  </div>

                  <!-- Error State -->
                  <div v-else-if="error" class="text-center py-16">
                    <div class="w-16 h-16 rounded-2xl mx-auto mb-4 flex items-center justify-center bg-red-50">
                      <svg class="h-7 w-7 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                    </div>
                    <p class="text-sm font-medium mb-2 text-slate-600">Error al cargar emisoras</p>
                    <button @click="fetchRadios('/home')" class="text-xs text-rose-500 hover:text-rose-600 font-medium">Reintentar</button>
                  </div>
                  
                  <!-- Section: Lo más escuchado -->
                  <section v-else>
                    <h2 class="text-base font-semibold mb-4 text-slate-800">{{ currentCityFilter ? `Emisoras de ${currentCityFilter}` : 'Lo más escuchado' }}</h2>
                    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                      <div 
                        v-for="station in displayedRadios" 
                        :key="station.id"
                        @click="playStation(station)"
                        class="group cursor-pointer"
                      >
                        <div class="relative aspect-square rounded-2xl overflow-hidden mb-3 border-2 transition-all duration-200 bg-slate-50 hover:shadow-lg"
                             :class="currentRadio?.id === station.id ? 'border-rose-400 shadow-lg shadow-rose-100' : 'border-slate-100 hover:border-slate-200'">
                          <img 
                            v-if="station.logo"
                            :src="station.logo" 
                            :alt="station.name"
                            class="w-full h-full object-contain p-5"
                            @error="handleImageError"
                          />
                          <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br" :class="getGradientColor(station.name)">
                            <span class="text-white font-bold text-2xl drop-shadow">{{ getInitials(station.name) }}</span>
                          </div>
                          
                          <!-- Hover overlay -->
                          <div class="absolute inset-0 flex items-center justify-center transition-opacity duration-200 opacity-0 group-hover:opacity-100 bg-black/20">
                            <button class="w-12 h-12 rounded-full flex items-center justify-center shadow-lg" :class="currentRadio?.id === station.id && isPlaying ? 'bg-rose-500 text-white' : 'bg-white text-slate-700'">
                              <svg v-if="currentRadio?.id === station.id && isPlaying" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                              </svg>
                              <svg v-else class="h-5 w-5 ml-0.5" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M8 5v14l11-7z" />
                              </svg>
                            </button>
                          </div>
                          
                          <!-- Favorite button -->
                          <button 
                            @click.stop="toggleFavorite(station)"
                            class="absolute top-2 right-2 z-10 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 shadow-sm"
                            :class="isFavorite(station.id) ? 'bg-rose-500 text-white' : 'opacity-0 group-hover:opacity-100 bg-white/90 text-slate-400 hover:text-rose-500'"
                          >
                            <svg class="h-4 w-4" :fill="isFavorite(station.id) ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
                            </svg>
                          </button>
                          
                          <!-- Live indicator -->
                          <div v-if="currentRadio?.id === station.id && isPlaying" class="absolute top-2 left-2 px-2 py-1 bg-rose-500 rounded-full text-[10px] font-semibold text-white uppercase tracking-wide flex items-center gap-1 shadow-sm">
                            <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                            EN VIVO
                          </div>
                        </div>
                        <h3 class="font-medium text-sm truncate px-1" :class="currentRadio?.id === station.id && isPlaying ? 'text-rose-600' : 'text-slate-700'">{{ station.name }}</h3>
                        <p v-if="station.city" class="text-xs text-slate-400 truncate px-1">{{ station.city }}</p>
                      </div>
                    </div>
                  </section>

                </div>
              </div>
            </main>
          </div>

          <!-- PLAYER BAR - Sticky Bottom - Elegante -->
          <div class="absolute bottom-0 left-0 right-0 h-20 flex items-center justify-between px-5 z-50 border-t bg-white/95 border-slate-100">
            
            <!-- Info Emisora Actual -->
            <div class="w-[28%] flex items-center gap-3">
              <div v-if="currentRadio" class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-xl overflow-hidden relative flex-shrink-0 bg-slate-100 border border-slate-200">
                  <img 
                    v-if="currentRadio.logo"
                    :src="currentRadio.logo" 
                    :alt="currentRadio.name"
                    class="w-full h-full object-contain p-1" 
                    @error="handleImageError" 
                  />
                  <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br" :class="getGradientColor(currentRadio.name)">
                    <span class="text-white font-bold text-sm">{{ getInitials(currentRadio.name) }}</span>
                  </div>
                  <!-- Playing indicator -->
                  <div v-if="isPlaying" class="absolute inset-0 bg-black/30 flex items-center justify-center gap-0.5">
                    <div class="w-0.5 bg-white rounded-full animate-music-bar-1"></div>
                    <div class="w-0.5 bg-white rounded-full animate-music-bar-2"></div>
                    <div class="w-0.5 bg-white rounded-full animate-music-bar-3"></div>
                  </div>
                </div>
                <div class="min-w-0">
                  <div class="font-medium text-sm truncate max-w-[140px] text-slate-800">{{ currentRadio.name }}</div>
                  <div class="flex items-center gap-1.5 mt-0.5">
                    <span v-if="isPlaying" class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[9px] font-semibold uppercase tracking-wide bg-rose-100 text-rose-600">
                      <span class="w-1 h-1 bg-rose-500 rounded-full animate-pulse"></span>
                      En vivo
                    </span>
                    <span v-else class="text-xs text-slate-400">Pausado</span>
                  </div>
                </div>
                <!-- Favorite button -->
                <button 
                  class="p-1.5 rounded-full transition-colors duration-150"
                  :class="isFavorite(currentRadio?.id) ? 'text-rose-500' : 'text-slate-400 hover:text-rose-500'"
                  @click="toggleFavorite(currentRadio)"
                >
                  <svg class="h-4 w-4" :fill="isFavorite(currentRadio?.id) ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
                  </svg>
                </button>
              </div>
              <!-- Empty state -->
              <div v-else class="flex items-center gap-2.5 text-slate-400">
                <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-slate-100 border border-slate-200">
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                  </svg>
                </div>
                <span class="text-sm">Selecciona una emisora</span>
              </div>
            </div>

            <!-- Center Controls -->
            <div class="w-[44%] flex flex-col items-center justify-center gap-2">
              <div class="flex items-center gap-3">
                <!-- Random -->
                <button 
                  @click="playRandom"
                  class="p-2 rounded-full transition-colors duration-150 text-slate-400 hover:text-slate-600 hover:bg-slate-100"
                  title="Aleatorio"
                >
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                  </svg>
                </button>
                
                <!-- Previous -->
                <button 
                  @click="playPrevious"
                  class="p-2 rounded-full transition-colors duration-150 text-slate-500 hover:text-slate-700 hover:bg-slate-100"
                >
                  <svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
                  </svg>
                </button>

                <!-- Play/Pause -->
                <button 
                  @click="togglePlay"
                  class="w-11 h-11 rounded-full flex items-center justify-center transition-all duration-200 shadow-md"
                  :class="isPlaying ? 'bg-rose-500 hover:bg-rose-600 text-white' : 'bg-slate-800 hover:bg-slate-900 text-white'"
                >
                  <svg v-if="!isPlaying" class="h-5 w-5 ml-0.5" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                  <svg v-else class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                  </svg>
                </button>

                <!-- Next -->
                <button 
                  @click="playNext"
                  class="p-2 rounded-full transition-colors duration-150 text-slate-500 hover:text-slate-700 hover:bg-slate-100"
                >
                  <svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
                  </svg>
                </button>

                <!-- Repeat -->
                <button class="p-2 rounded-full transition-colors duration-150 text-slate-400 hover:text-slate-600 hover:bg-slate-100">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>
              </div>
              
              <!-- Progress indicator -->
              <div class="w-full max-w-sm flex items-center gap-2">
                <span 
                  class="text-[9px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded-full"
                  :class="isPlaying ? 'bg-rose-100 text-rose-600' : 'bg-slate-100 text-slate-400'"
                >
                  {{ isPlaying ? 'LIVE' : 'OFF' }}
                </span>
                <div class="flex-1 h-1 rounded-full overflow-hidden bg-slate-200">
                  <div v-if="isPlaying" class="h-full bg-gradient-to-r from-rose-400 to-pink-500 animate-progress-wave" style="width: 200%;"></div>
                </div>
              </div>
            </div>

            <!-- Volume -->
            <div class="w-[28%] flex items-center justify-end gap-2">
              <button 
                @click="toggleMute" 
                class="p-2 rounded-full transition-colors duration-150 text-slate-500 hover:text-slate-700 hover:bg-slate-100"
              >
                <svg v-if="!isMuted && volume > 0" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                </svg>
                <svg v-else class="h-4 w-4 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
                </svg>
              </button>
              <div class="w-24 h-1.5 rounded-full relative group cursor-pointer bg-slate-200">
                <input 
                  type="range" 
                  v-model="volume" 
                  @input="updateVolume"
                  min="0" 
                  max="100" 
                  class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div class="h-full rounded-full transition-all bg-slate-500" :style="{ width: volume + '%' }"></div>
              </div>
              <span class="text-[10px] w-7 text-right font-mono text-slate-400">{{ volume }}%</span>
            </div>

          </div>

        </div>
      </div>
    </Transition>
    
    <!-- Audio Element -->
    <audio ref="audioPlayer" @error="handleAudioError" preload="none"></audio>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  visible: Boolean
})

const emit = defineEmits(['close', 'playing', 'station-change'])

// State
const audioPlayer = ref(null)
const currentRadio = ref(null)
const isPlaying = ref(false)
const volume = ref(70)
const isMuted = ref(false)
const currentView = ref('home')
const searchQuery = ref('')
const favorites = ref(new Set())
const currentCityFilter = ref(null)
const loading = ref(false)
const error = ref(null)

// Cities
const cities = [
  { name: 'Medellín', color: 'bg-emerald-500', state: 'Antioquia' },
  { name: 'Bogotá', color: 'bg-blue-500', state: 'Bogota' },
  { name: 'Cali', color: 'bg-orange-500', state: 'Valle del Cauca' },
  { name: 'Costa', color: 'bg-amber-500', state: 'Atlantico' }
]

// API Base URL
const API_URL = 'https://105pos.pro/api/public/radio'

// No hay FALLBACK - Siempre usamos la API

// Emisoras - Se cargan desde la API
const radios = ref([])

// Mapeo de logos desde MyTuner CDN (URLs directas - igual que 105 POS)
const MYTUNER_LOGOS = {
  // MEDELLÍN (8 emisoras)
  'co-medellin-mega': 'https://static.mytuner.mobi/media/tvos_radios/660/la-mega-medellin.36fe2c68.png',
  'co-medellin-olimpica': 'https://static.mytuner.mobi/media/tvos_radios/919/olimpica-stereo-medellin-1049-fm.1f60f975.png',
  'co-medellin-elsol': 'https://static.mytuner.mobi/media/tvos_radios/045/el-sol-medellin.a4aa6e39.jpg',
  'co-medellin-mix': 'https://static.mytuner.mobi/media/tvos_radios/819/mix-899-fm-medellin.9117dedc.jpg',
  'co-medellin-tropicana': 'https://static.mytuner.mobi/media/tvos_radios/626/tropicana-medellin.28271e0c.png',
  'co-medellin-besame': 'https://static.mytuner.mobi/media/tvos_radios/302/besame-fm.bc8f3bdf.jpg',
  'co-medellin-radioacktiva': 'https://static.mytuner.mobi/media/tvos_radios/859/radioacktiva.c5cdb359.png',
  'co-medellin-estrella': 'https://static.mytuner.mobi/media/tvos_radios/825/estrella-estereo.d1ff4458.jpg',
  
  // BOGOTÁ (18 emisoras)
  'co-bogota-blu': 'https://static.mytuner.mobi/media/tvos_radios/666/blu-radio.2bf5a8c8.jpg',
  'co-bogota-caracol': 'https://static.mytuner.mobi/media/tvos_radios/303/caracol-radio.18b43470.jpg',
  'co-bogota-wradio': 'https://static.mytuner.mobi/media/tvos_radios/402/la-w-radio.61065ed8.jpg',
  'co-bogota-olimpica': 'https://static.mytuner.mobi/media/tvos_radios/919/olimpica-stereo-medellin-1049-fm.1f60f975.png',
  'co-bogota-los40': 'https://static.mytuner.mobi/media/tvos_radios/845/los-40-principales-colombia.b3eabffc.jpg',
  'co-bogota-tropicana': 'https://static.mytuner.mobi/media/tvos_radios/626/tropicana-medellin.28271e0c.png',
  'co-bogota-radioacktiva': 'https://static.mytuner.mobi/media/tvos_radios/859/radioacktiva.c5cdb359.png',
  'co-bogota-candela': 'https://static.mytuner.mobi/media/tvos_radios/833/candela-stereo.97aa41b3.png',
  'co-bogota-vibra': 'https://static.mytuner.mobi/media/tvos_radios/832/vibra-fm-1049.f9c0981a.png',
  'co-bogota-radionica': 'https://static.mytuner.mobi/media/tvos_radios/935/rtvc-radionica.03a04ab8.jpg',
  'co-bogota-lakalle': 'https://static.mytuner.mobi/media/tvos_radios/860/la-kalle-969-fm.c8a228d5.png',
  'co-bogota-lax': 'https://static.mytuner.mobi/media/tvos_radios/797/la-x-mas-musica.7ae2ec50.png',
  'co-bogota-maria': 'https://static.mytuner.mobi/media/tvos_radios/098/radio-maria-colombia.caed66ee.png',
  'co-bogota-superclasica': 'http://cdn-radiotime-logos.tunein.com/s161501q.png',
  
  // CALI (5 emisoras)
  'co-cali-olimpica': 'https://static.mytuner.mobi/media/tvos_radios/919/olimpica-stereo-medellin-1049-fm.1f60f975.png',
  'co-cali-tropicana': 'https://static.mytuner.mobi/media/tvos_radios/626/tropicana-medellin.28271e0c.png',
  'co-cali-mix': 'https://static.mytuner.mobi/media/tvos_radios/819/mix-899-fm-medellin.9117dedc.jpg',
  'co-cali-lax': 'https://static.mytuner.mobi/media/tvos_radios/797/la-x-mas-musica.7ae2ec50.png',
  'co-cali-energia': 'https://static.mytuner.mobi/media/tvos_radios/830/oxigeno.jpg',
  
  // BARRANQUILLA / COSTA ATLÁNTICA (3 emisoras - Radio Tiempo sin logo)
  'co-barranquilla-olimpica': 'https://static.mytuner.mobi/media/tvos_radios/919/olimpica-stereo-medellin-1049-fm.1f60f975.png',
  'co-barranquilla-mix': 'https://static.mytuner.mobi/media/tvos_radios/819/mix-899-fm-medellin.9117dedc.jpg',
  'co-barranquilla-vallenatisima': 'https://cdn-profiles.tunein.com/s293652/images/logog.png',
  
  // CARTAGENA (sin Radio Tiempo - widget)
}

// Función para obtener el logo de una emisora (prioriza MyTuner CDN)
const getStationLogo = (station) => {
  // Si tiene logo en MyTuner CDN, usarlo (como en 105 POS)
  if (MYTUNER_LOGOS[station.id]) {
    return MYTUNER_LOGOS[station.id]
  }
  // Para el resto, retornar null para que use gradientes con iniciales
  return null
}

// Mapear respuesta de la API al formato interno
const mapStation = (station) => ({
  id: station.id,
  name: station.name,
  city: station.city,
  logo: MYTUNER_LOGOS[station.id] || null, // Priorizar logos de MyTuner CDN
  url: station.stream_url,
  frequency: station.frequency,
  state: station.state,
  votes: station.votes || 0
})

// Cargar emisoras desde la API
const fetchRadios = async (params = {}) => {
  loading.value = true
  error.value = null
  
  try {
    const allRadios = []
    let offset = 0
    const limit = 20 // Pedir 20 por página
    let hasMore = true
    
    // Hacer requests paginados hasta obtener todas
    while (hasMore && allRadios.length < 100) {
      const queryParams = new URLSearchParams()
      if (params.state) queryParams.append('state', params.state)
      if (params.city) queryParams.append('city', params.city)
      queryParams.append('limit', limit)
      queryParams.append('offset', offset)
      
      const url = `${API_URL}/stations?${queryParams.toString()}`
      
      const response = await fetch(url)
      if (!response.ok) throw new Error('Error al cargar emisoras')
      
      const data = await response.json()
      
      if (data.success && Array.isArray(data.data)) {
        allRadios.push(...data.data)
        
        // Verificar si hay más datos
        hasMore = data.meta?.has_more || data.data.length === limit
        offset += limit
      } else {
        throw new Error('Formato de respuesta inválido')
      }
      
      // Seguridad: máximo 5 páginas
      if (offset >= 100) break
    }
    
    radios.value = allRadios.map(mapStation)
    
  } catch (e) {
    console.error('❌ Error cargando emisoras:', e)
    error.value = 'No se pudieron cargar las emisoras. Intenta más tarde.'
    radios.value = []
  } finally {
    loading.value = false
  }
}

// Filtrar por ciudad (filtrado local porque API no soporta este filtro)
const filterByCity = (cityName) => {
  currentCityFilter.value = cityName
  currentView.value = 'home'
  searchQuery.value = ''
}

// Buscar emisoras (búsqueda local en datos ya cargados)
const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (searchQuery.value && searchQuery.value.length >= 2) {
      currentView.value = 'search'
    } else if (!searchQuery.value) {
      currentView.value = 'home'
    }
  }, 300)
}

// Computed
const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour >= 5 && hour < 12) return 'Buenos días'
  if (hour >= 12 && hour < 19) return 'Buenas tardes'
  return 'Buenas noches'
})

const displayedRadios = computed(() => {
  if (currentCityFilter.value) {
    // Para "Costa", incluir Barranquilla y Cartagena
    if (currentCityFilter.value === 'Costa') {
      return radios.value.filter(r => 
        r.city === 'Barranquilla' || r.city === 'Cartagena'
      )
    }
    return radios.value.filter(r => r.city === currentCityFilter.value)
  }
  return radios.value
})

const filteredRadios = computed(() => {
  if (!searchQuery.value) return displayedRadios.value
  const query = searchQuery.value.toLowerCase()
  return radios.value.filter(r => r.name.toLowerCase().includes(query) || r.city?.toLowerCase().includes(query))
})

const favoriteRadios = computed(() => radios.value.filter(r => favorites.value.has(r.id)))

// Methods
const closeModal = () => emit('close')

const playStation = async (station) => {
  if (currentRadio.value?.id === station.id) {
    togglePlay()
    return
  }
  currentRadio.value = station
  emit('station-change', station.name)
  await playRadio()
}

const playRadio = async () => {
  if (!currentRadio.value || !audioPlayer.value) return
  try {
    audioPlayer.value.src = currentRadio.value.url
    audioPlayer.value.volume = volume.value / 100
    await audioPlayer.value.play()
    isPlaying.value = true
    emit('playing', true)
  } catch (error) {
    console.error('Error playing radio:', error)
    isPlaying.value = false
    emit('playing', false)
  }
}

const togglePlay = () => {
  if (!audioPlayer.value || !currentRadio.value) return
  if (isPlaying.value) {
    audioPlayer.value.pause()
    isPlaying.value = false
    emit('playing', false)
  } else {
    playRadio()
  }
}

const playNext = () => {
  if (!radios.value.length) return
  const currentIndex = radios.value.findIndex(r => r.id === currentRadio.value?.id)
  const nextIndex = (currentIndex + 1) % radios.value.length
  playStation(radios.value[nextIndex])
}

const playPrevious = () => {
  if (!radios.value.length) return
  const currentIndex = radios.value.findIndex(r => r.id === currentRadio.value?.id)
  const prevIndex = currentIndex <= 0 ? radios.value.length - 1 : currentIndex - 1
  playStation(radios.value[prevIndex])
}

const playRandom = () => {
  if (!radios.value.length) return
  const randomIndex = Math.floor(Math.random() * radios.value.length)
  playStation(radios.value[randomIndex])
}

const updateVolume = () => {
  if (audioPlayer.value) {
    audioPlayer.value.volume = volume.value / 100
    if (isMuted.value && volume.value > 0) isMuted.value = false
  }
}

const toggleMute = () => {
  if (audioPlayer.value) {
    isMuted.value = !isMuted.value
    audioPlayer.value.muted = isMuted.value
  }
}

const toggleFavorite = (station) => {
  if (!station) return
  if (favorites.value.has(station.id)) {
    favorites.value.delete(station.id)
  } else {
    favorites.value.add(station.id)
  }
  localStorage.setItem('ecommerce_radio_favorites', JSON.stringify([...favorites.value]))
}

const isFavorite = (id) => favorites.value.has(id)

let searchTimeout = null

// Ir al inicio
const goHome = () => {
  currentView.value = 'home'
  currentCityFilter.value = null
  searchQuery.value = ''
  // Recargar todas las emisoras
  fetchRadios({ limit: 100 })
}

const getInitials = (name) => {
  // Casos especiales para emisoras conocidas
  const specialCases = {
    'Blu Radio': 'BR',
    'Caracol Radio': 'CR',
    'W Radio': 'W',
    'Olímpica': 'OL',
    'LOS40': '40',
    'Tropicana': 'TR',
    'Radioacktiva': 'RA',
    'Candela': 'CA',
    'Vibra': 'VB',
    'Radiónica': 'RN',
    'La Kalle': 'LK',
    'La X': 'LX',
    'La Mega': 'LM',
    'La FM': 'FM',
    'Radio María': 'RM',
    'Super Clásica': 'SC',
    'Oxígeno': 'O2',
    'Bésame': 'BS',
    'Mix FM': 'MX',
    'Radio Tiempo': 'RT'
  }
  
  for (const [key, initials] of Object.entries(specialCases)) {
    if (name.includes(key)) return initials
  }
  
  // Fallback: primeras 2 letras de las primeras 2 palabras
  return name.split(' ').filter(w => w.length > 0 && !w.match(/^\d/)).slice(0, 2).map(w => w[0].toUpperCase()).join('')
}

const getGradientColor = (name) => {
  const colors = [
    'from-rose-400 to-pink-500', 
    'from-violet-400 to-purple-500', 
    'from-blue-400 to-indigo-500', 
    'from-emerald-400 to-teal-500', 
    'from-amber-400 to-orange-500', 
    'from-cyan-400 to-sky-500',
    'from-red-400 to-rose-500',
    'from-fuchsia-400 to-pink-500',
    'from-teal-400 to-cyan-500',
    'from-lime-400 to-green-500'
  ]
  const hash = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return colors[hash % colors.length]
}

const handleImageError = (e) => { if (e.target) e.target.style.display = 'none' }
const handleAudioError = () => { isPlaying.value = false; emit('playing', false) }

// Lifecycle - Cargar emisoras cuando se abre el modal
onMounted(() => {
  // Cargar favoritos
  const saved = localStorage.getItem('ecommerce_radio_favorites')
  if (saved) favorites.value = new Set(JSON.parse(saved))
  
  // Cargar TODAS las emisoras desde la API
  fetchRadios({ limit: 100 })
})

// Cargar emisoras cuando el modal se hace visible
watch(() => props.visible, (newVal) => {
  if (newVal && radios.value.length === 0) {
    fetchRadios({ limit: 100 })
  }
})

onUnmounted(() => {
  if (audioPlayer.value) {
    audioPlayer.value.pause()
    audioPlayer.value.src = ''
  }
})
</script>

<style scoped>
.fade-enter-active { transition: opacity 0.2s ease-out; }
.fade-leave-active { transition: opacity 0.15s ease-in; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #cbd5e1; }

@keyframes music-bar {
  0%, 100% { transform: scaleY(0.3); }
  50% { transform: scaleY(1); }
}
.animate-music-bar-1, .animate-music-bar-2, .animate-music-bar-3 {
  will-change: transform;
  transform-origin: center;
  height: 12px;
}
.animate-music-bar-1 { animation: music-bar 0.5s ease-in-out infinite; }
.animate-music-bar-2 { animation: music-bar 0.5s ease-in-out infinite 0.1s; }
.animate-music-bar-3 { animation: music-bar 0.5s ease-in-out infinite 0.2s; }

@keyframes progress-wave {
  0% { transform: translateX(-50%); }
  100% { transform: translateX(0%); }
}
.animate-progress-wave {
  animation: progress-wave 1.5s linear infinite;
  will-change: transform;
}

.radio-modal-container {
  transform: translateZ(0);
  backface-visibility: hidden;
}

.font-sans {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>
