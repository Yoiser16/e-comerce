<template>
  <Teleport to="body">
    <transition-group
      name="toast"
      tag="div"
      class="fixed top-4 right-4 z-[9999] flex flex-col gap-2 pointer-events-none"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="pointer-events-auto bg-white rounded-xl shadow-2xl border border-gray-100 overflow-hidden min-w-[320px] max-w-md"
        :class="getToastClass(toast.type)"
      >
        <div class="flex items-start gap-3 p-4">
          <!-- Icon -->
          <div class="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center" :class="getIconBg(toast.type)">
            <svg v-if="toast.type === 'success'" class="w-5 h-5" :class="getIconColor(toast.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else-if="toast.type === 'error'" class="w-5 h-5" :class="getIconColor(toast.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            <svg v-else-if="toast.type === 'warning'" class="w-5 h-5" :class="getIconColor(toast.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <svg v-else class="w-5 h-5" :class="getIconColor(toast.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <h3 v-if="toast.title" class="font-semibold text-gray-900 text-sm mb-0.5">
              {{ toast.title }}
            </h3>
            <p class="text-gray-600 text-sm" :class="{ 'mt-1': !toast.title }">
              {{ toast.message }}
            </p>
          </div>

          <!-- Close Button -->
          <button
            @click="removeToast(toast.id)"
            class="flex-shrink-0 p-1 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-100"
            aria-label="Cerrar notificación"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Progress Bar -->
        <div class="h-1 bg-gray-100 overflow-hidden">
          <div
            class="h-full transition-all ease-linear"
            :class="getProgressClass(toast.type)"
            :style="{ width: `${toast.progress}%`, transitionDuration: `${toast.duration}ms` }"
          ></div>
        </div>
      </div>
    </transition-group>
  </Teleport>
</template>

<script>
import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export function useToast() {
  function showToast(options) {
    const id = toastId++
    const toast = {
      id,
      type: options.type || 'info',
      title: options.title,
      message: options.message || '',
      duration: options.duration || 3000,
      progress: 0
    }

    toasts.value.push(toast)

    // Animate progress bar
    setTimeout(() => {
      const toastIndex = toasts.value.findIndex(t => t.id === id)
      if (toastIndex !== -1) {
        toasts.value[toastIndex].progress = 100
      }
    }, 10)

    // Auto remove
    setTimeout(() => {
      removeToast(id)
    }, toast.duration)

    return id
  }

  function removeToast(id) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }

  return {
    showToast,
    removeToast,
    success: (message, title) => showToast({ type: 'success', message, title }),
    error: (message, title) => showToast({ type: 'error', message, title }),
    warning: (message, title) => showToast({ type: 'warning', message, title }),
    info: (message, title) => showToast({ type: 'info', message, title })
  }
}

export default {
  name: 'B2BToast',
  setup() {
    function getToastClass(type) {
      const classes = {
        success: 'border-l-4 border-l-emerald-500',
        error: 'border-l-4 border-l-red-500',
        warning: 'border-l-4 border-l-amber-500',
        info: 'border-l-4 border-l-blue-500'
      }
      return classes[type] || classes.info
    }

    function getIconBg(type) {
      const classes = {
        success: 'bg-emerald-50',
        error: 'bg-red-50',
        warning: 'bg-amber-50',
        info: 'bg-blue-50'
      }
      return classes[type] || classes.info
    }

    function getIconColor(type) {
      const classes = {
        success: 'text-emerald-600',
        error: 'text-red-600',
        warning: 'text-amber-600',
        info: 'text-blue-600'
      }
      return classes[type] || classes.info
    }

    function getProgressClass(type) {
      const classes = {
        success: 'bg-emerald-500',
        error: 'bg-red-500',
        warning: 'bg-amber-500',
        info: 'bg-blue-500'
      }
      return classes[type] || classes.info
    }

    function removeToast(id) {
      const index = toasts.value.findIndex(t => t.id === id)
      if (index !== -1) {
        toasts.value.splice(index, 1)
      }
    }

    return {
      toasts,
      getToastClass,
      getIconBg,
      getIconColor,
      getProgressClass,
      removeToast
    }
  }
}
</script>

<style scoped>
/* Toast Animations */
.toast-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 1, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>
