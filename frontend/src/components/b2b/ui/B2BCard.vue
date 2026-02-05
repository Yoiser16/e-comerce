<template>
  <div :class="cardClasses">
    <!-- Header -->
    <div v-if="$slots.header || title" :class="headerClasses">
      <slot name="header">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="font-semibold text-gray-900" :class="titleSizeClass">{{ title }}</h3>
            <p v-if="subtitle" class="text-gray-500 text-sm mt-0.5">{{ subtitle }}</p>
          </div>
          <slot name="header-action"></slot>
        </div>
      </slot>
    </div>
    
    <!-- Body -->
    <div :class="bodyClasses">
      <slot></slot>
    </div>

    <!-- Footer -->
    <div v-if="$slots.footer" :class="footerClasses">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'B2BCard',
  props: {
    title: String,
    subtitle: String,
    variant: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'elevated', 'bordered', 'dark', 'gradient'].includes(v)
    },
    padding: {
      type: String,
      default: 'md',
      validator: (v) => ['none', 'sm', 'md', 'lg'].includes(v)
    },
    hover: Boolean,
    clickable: Boolean
  },
  setup(props) {
    const cardClasses = computed(() => {
      const base = ['rounded-xl overflow-hidden transition-all duration-300']
      
      const variants = {
        default: 'bg-white border border-gray-100',
        elevated: 'bg-white shadow-md hover:shadow-lg',
        bordered: 'bg-white border-2 border-gray-200',
        dark: 'bg-[#1A1A1A] text-white border border-gray-800',
        gradient: 'bg-gradient-to-br from-[#1A1A1A] via-[#252525] to-[#1A1A1A] text-white'
      }

      return [
        ...base,
        variants[props.variant],
        props.hover ? 'hover:shadow-lg hover:-translate-y-0.5' : '',
        props.clickable ? 'cursor-pointer' : ''
      ].join(' ')
    })

    const paddings = {
      none: '',
      sm: 'p-3',
      md: 'p-4 sm:p-5',
      lg: 'p-5 sm:p-6'
    }

    const headerClasses = computed(() => {
      return ['border-b', props.variant === 'dark' || props.variant === 'gradient' ? 'border-white/10' : 'border-gray-100', paddings[props.padding]].join(' ')
    })

    const bodyClasses = computed(() => paddings[props.padding])

    const footerClasses = computed(() => {
      return ['border-t', props.variant === 'dark' || props.variant === 'gradient' ? 'border-white/10' : 'border-gray-100', paddings[props.padding]].join(' ')
    })

    const titleSizeClass = computed(() => {
      return props.padding === 'lg' ? 'text-lg' : 'text-base'
    })

    return { cardClasses, headerClasses, bodyClasses, footerClasses, titleSizeClass }
  }
}
</script>
