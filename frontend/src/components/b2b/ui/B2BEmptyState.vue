<template>
  <div class="text-center py-12 sm:py-16 px-4">
    <!-- Icon -->
    <div 
      class="w-20 h-20 mx-auto mb-6 rounded-2xl flex items-center justify-center"
      :class="iconContainerClass"
    >
      <slot name="icon">
        <svg class="w-10 h-10" :class="iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="iconPath" />
        </svg>
      </slot>
    </div>

    <!-- Title -->
    <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-2">
      {{ title }}
    </h3>

    <!-- Description -->
    <p class="text-gray-500 text-sm sm:text-base max-w-md mx-auto mb-6 leading-relaxed">
      {{ description }}
    </p>

    <!-- Action -->
    <div v-if="$slots.action" class="flex flex-col sm:flex-row items-center justify-center gap-3">
      <slot name="action"></slot>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'B2BEmptyState',
  props: {
    title: {
      type: String,
      default: 'No hay datos'
    },
    description: {
      type: String,
      default: 'No se encontraron resultados'
    },
    type: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'cart', 'orders', 'products', 'search', 'error'].includes(v)
    }
  },
  setup(props) {
    const iconPaths = {
      default: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
      cart: 'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z',
      orders: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01',
      products: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z',
      search: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
      error: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
    }

    const iconPath = computed(() => iconPaths[props.type] || iconPaths.default)

    const iconContainerClass = computed(() => {
      if (props.type === 'error') return 'bg-red-100'
      return 'bg-gray-100'
    })

    const iconClass = computed(() => {
      if (props.type === 'error') return 'text-red-400'
      return 'text-gray-400'
    })

    return { iconPath, iconContainerClass, iconClass }
  }
}
</script>
