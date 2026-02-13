<template>
  <div class="space-y-6 sm:space-y-10 animate-fade-in pb-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-text-light">Moderación</p>
        <h1 class="text-3xl sm:text-4xl font-luxury text-text-dark leading-tight">Calificaciones de clientes</h1>
        <p class="text-text-medium text-sm sm:text-base mt-1">Aprueba o rechaza las reseñas basadas en compras reales.</p>
      </div>
      <div class="flex items-center gap-2 bg-white border border-gray-200 rounded-xl p-1 shadow-sm">
        <button
          v-for="estado in estados"
          :key="estado.value"
          @click="cambiarFiltro(estado.value)"
          :class="[
            'px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition-all',
            estadoActivo === estado.value
              ? 'bg-gray-900 text-white shadow-md'
              : 'text-text-medium hover:text-text-dark hover:bg-gray-100'
          ]"
        >
          {{ estado.label }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <div v-for="i in 3" :key="i" class="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm animate-pulse space-y-4">
        <div class="h-4 bg-gray-100 rounded w-1/2"></div>
        <div class="h-3 bg-gray-100 rounded w-1/3"></div>
        <div class="h-12 bg-gray-100 rounded"></div>
        <div class="h-10 bg-gray-100 rounded"></div>
      </div>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-100 text-red-700 rounded-2xl p-4">{{ error }}</div>

    <div v-else-if="resenas.length === 0" class="bg-white border border-gray-100 rounded-2xl p-8 text-center shadow-sm">
      <p class="text-lg font-semibold text-text-dark">No hay reseñas {{ estadoActivo }}.</p>
      <p class="text-text-medium text-sm mt-1">Cuando lleguen nuevas calificaciones aparecerán aquí.</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <article
        v-for="resena in resenas"
        :key="resena.id"
        class="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all"
      >
        <div class="flex items-start justify-between gap-3 mb-3">
          <div>
            <p class="text-xs uppercase tracking-[0.18em] text-text-light mb-1">Producto</p>
            <p class="text-base font-semibold text-text-dark leading-snug">{{ resena.producto_nombre || 'Producto' }}</p>
          </div>
          <span :class="badgeClass(resena.estado)" class="px-2 py-1 text-[11px] rounded-full font-semibold border">
            {{ estadoLabel(resena.estado) }}
          </span>
        </div>

        <div class="flex items-center gap-2 mb-2">
          <div class="flex items-center gap-1 text-[#C9A962]">
            <svg
              v-for="i in 5"
              :key="i"
              class="w-4 h-4"
              :class="i <= resena.rating ? 'text-[#C9A962]' : 'text-gray-200'"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
          <span class="text-xs text-text-medium">{{ resena.rating }} / 5</span>
        </div>

        <div class="text-sm text-text-medium space-y-1 mb-3">
          <p class="font-semibold text-text-dark">{{ resena.cliente }}</p>
          <p class="text-xs text-text-light">{{ formatFecha(resena.fecha_creacion) }}</p>
        </div>

        <div class="flex items-center gap-2 mt-4" v-if="estadoActivo === 'pendiente'">
          <button
            class="flex-1 px-3 py-2 rounded-lg bg-emerald-500 text-white text-sm font-semibold hover:bg-emerald-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            :disabled="accionando === resena.id"
            @click="cambiarEstado(resena.id, 'aprobada')"
          >
            {{ accionando === resena.id ? 'Aprobando...' : 'Aprobar' }}
          </button>
          <button
            class="flex-1 px-3 py-2 rounded-lg border border-gray-200 text-sm font-semibold text-text-dark hover:border-red-300 hover:text-red-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            :disabled="accionando === resena.id"
            @click="cambiarEstado(resena.id, 'rechazada')"
          >
            {{ accionando === resena.id ? 'Rechazando...' : 'Rechazar' }}
          </button>
        </div>

        <p v-else class="text-xs text-text-light mt-2">Esta reseña ya fue {{ estadoLabel(resena.estado).toLowerCase() }}.</p>
      </article>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { resenasService } from '@/services/resenas'

const estados = [
  { value: 'pendiente', label: 'Pendientes' },
  { value: 'aprobada', label: 'Aprobadas' },
  { value: 'rechazada', label: 'Rechazadas' }
]

const estadoActivo = ref('pendiente')
const resenas = ref([])
const loading = ref(false)
const error = ref(null)
const accionando = ref(null)

const estadoLabel = (estado) => {
  const labels = {
    pendiente: 'Pendiente',
    aprobada: 'Aprobada',
    rechazada: 'Rechazada'
  }
  return labels[estado] || estado
}

const badgeClass = (estado) => {
  const base = 'border text-xs'
  if (estado === 'aprobada') return `${base} bg-emerald-50 text-emerald-700 border-emerald-100`
  if (estado === 'rechazada') return `${base} bg-red-50 text-red-700 border-red-100`
  return `${base} bg-amber-50 text-amber-700 border-amber-100`
}

const formatFecha = (fecha) => {
  try {
    return new Date(fecha).toLocaleString('es-ES', { dateStyle: 'medium', timeStyle: 'short' })
  } catch (e) {
    return fecha
  }
}

const cargarResenas = async () => {
  loading.value = true
  error.value = null
  try {
    resenas.value = await resenasService.listarAdmin(estadoActivo.value)
  } catch (e) {
    error.value = 'No se pudieron cargar las reseñas.'
  } finally {
    loading.value = false
  }
}

const cambiarEstado = async (id, estado) => {
  accionando.value = id
  try {
    await resenasService.cambiarEstado(id, estado)
    resenas.value = resenas.value.filter((r) => r.id !== id)
  } catch (e) {
    error.value = 'No se pudo actualizar el estado.'
  } finally {
    accionando.value = null
  }
}

const cambiarFiltro = (estado) => {
  if (estadoActivo.value === estado) return
  estadoActivo.value = estado
  cargarResenas()
}

onMounted(() => {
  cargarResenas()
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.25s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
