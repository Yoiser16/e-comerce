<template>
  <span :class="badgeClasses">
    <span v-if="dot" class="w-1.5 h-1.5 rounded-full mr-1.5" :class="dotColorClass"></span>
    <span v-if="icon" class="mr-1">
      <slot name="icon"></slot>
    </span>
    <slot></slot>
  </span>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'B2BBadge',
  props: {
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'gold', 'success', 'warning', 'danger', 'info', 'dark', 'outline'].includes(v)
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['xs', 'sm', 'md', 'lg'].includes(v)
    },
    rounded: {
      type: String,
      default: 'full',
      validator: (v) => ['sm', 'md', 'lg', 'full'].includes(v)
    },
    dot: Boolean,
    icon: Boolean,
    pulse: Boolean
  },
  setup(props) {
    const badgeClasses = computed(() => {
      const base = ['inline-flex items-center font-semibold']

      const variants = {
        default: 'bg-gray-100 text-gray-700',
        gold: 'bg-gradient-to-r from-[#C9A962]/20 to-[#C9A962]/10 text-[#C9A962] border border-[#C9A962]/30',
        success: 'bg-emerald-100 text-emerald-700',
        warning: 'bg-amber-100 text-amber-700',
        danger: 'bg-red-100 text-red-700',
        info: 'bg-blue-100 text-blue-700',
        dark: 'bg-[#1A1A1A] text-white',
        outline: 'bg-transparent border border-gray-300 text-gray-600'
      }

      const sizes = {
        xs: 'text-[10px] px-1.5 py-0.5',
        sm: 'text-xs px-2 py-0.5',
        md: 'text-xs px-2.5 py-1',
        lg: 'text-sm px-3 py-1.5'
      }

      const roundedClasses = {
        sm: 'rounded',
        md: 'rounded-md',
        lg: 'rounded-lg',
        full: 'rounded-full'
      }

      return [
        ...base,
        variants[props.variant],
        sizes[props.size],
        roundedClasses[props.rounded],
        props.pulse ? 'animate-pulse' : ''
      ].join(' ')
    })

    const dotColorClass = computed(() => {
      const colors = {
        default: 'bg-gray-500',
        gold: 'bg-[#C9A962]',
        success: 'bg-emerald-500',
        warning: 'bg-amber-500',
        danger: 'bg-red-500',
        info: 'bg-blue-500',
        dark: 'bg-white',
        outline: 'bg-gray-500'
      }
      return colors[props.variant]
    })

    return { badgeClasses, dotColorClass }
  }
}
</script>
