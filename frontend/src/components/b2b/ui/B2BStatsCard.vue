<template>
  <div :class="cardClasses">
    <!-- Icon -->
    <div 
      class="flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center"
      :class="iconContainerClass"
    >
      <slot name="icon">
        <svg class="w-6 h-6" :class="iconClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      </slot>
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <p class="text-sm font-medium truncate" :class="labelClass">{{ label }}</p>
      <div class="flex items-baseline gap-2">
        <p class="text-2xl font-bold" :class="valueClass">
          <span v-if="prefix">{{ prefix }}</span>{{ formattedValue }}
        </p>
        <span 
          v-if="trend" 
          class="text-xs font-semibold flex items-center gap-0.5"
          :class="trendClass"
        >
          <svg v-if="trend > 0" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
          </svg>
          <svg v-else class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
          {{ Math.abs(trend) }}%
        </span>
      </div>
      <p v-if="subtitle" class="text-xs mt-1" :class="subtitleClass">{{ subtitle }}</p>
    </div>

    <!-- Action -->
    <div v-if="$slots.action" class="flex-shrink-0">
      <slot name="action"></slot>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'B2BStatsCard',
  props: {
    label: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    prefix: String,
    subtitle: String,
    trend: Number, // Positive or negative percentage
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'dark', 'success', 'warning', 'gold'].includes(v)
    },
    compact: Boolean
  },
  setup(props) {
    const formattedValue = computed(() => {
      if (typeof props.value === 'number') {
        return props.value.toLocaleString('es-CO')
      }
      return props.value
    })

    const cardClasses = computed(() => {
      const base = [
        'flex items-center gap-4 rounded-xl transition-all duration-200',
        props.compact ? 'p-3' : 'p-4 sm:p-5'
      ]

      const variants = {
        default: 'bg-white border border-gray-100',
        dark: 'bg-[#1A1A1A]',
        success: 'bg-emerald-50 border border-emerald-100',
        warning: 'bg-amber-50 border border-amber-100',
        gold: 'bg-gradient-to-br from-[#C9A962]/10 to-[#C9A962]/5 border border-[#C9A962]/20'
      }

      return [...base, variants[props.variant]].join(' ')
    })

    const iconContainerClass = computed(() => {
      const variants = {
        default: 'bg-gray-100',
        dark: 'bg-white/10',
        success: 'bg-emerald-100',
        warning: 'bg-amber-100',
        gold: 'bg-[#C9A962]/20'
      }
      return variants[props.variant]
    })

    const iconClass = computed(() => {
      const variants = {
        default: 'text-gray-600',
        dark: 'text-white',
        success: 'text-emerald-600',
        warning: 'text-amber-600',
        gold: 'text-[#C9A962]'
      }
      return variants[props.variant]
    })

    const labelClass = computed(() => {
      const variants = {
        default: 'text-gray-500',
        dark: 'text-white/60',
        success: 'text-emerald-700',
        warning: 'text-amber-700',
        gold: 'text-[#C9A962]'
      }
      return variants[props.variant]
    })

    const valueClass = computed(() => {
      const variants = {
        default: 'text-gray-900',
        dark: 'text-white',
        success: 'text-emerald-900',
        warning: 'text-amber-900',
        gold: 'text-[#1A1A1A]'
      }
      return variants[props.variant]
    })

    const subtitleClass = computed(() => {
      const variants = {
        default: 'text-gray-400',
        dark: 'text-white/40',
        success: 'text-emerald-600',
        warning: 'text-amber-600',
        gold: 'text-[#C9A962]/70'
      }
      return variants[props.variant]
    })

    const trendClass = computed(() => {
      if (!props.trend) return ''
      return props.trend > 0 ? 'text-emerald-600' : 'text-red-500'
    })

    return {
      formattedValue,
      cardClasses,
      iconContainerClass,
      iconClass,
      labelClass,
      valueClass,
      subtitleClass,
      trendClass
    }
  }
}
</script>
