<template>
  <component
    :is="tag"
    :to="to"
    :href="href"
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="$emit('click', $event)"
  >
    <!-- Loading Spinner -->
    <svg 
      v-if="loading" 
      class="w-4 h-4 animate-spin"
      :class="{ 'mr-2': $slots.default }"
      fill="none" 
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>

    <!-- Icon Left -->
    <span v-if="iconLeft && !loading" class="flex-shrink-0" :class="{ 'mr-2': $slots.default }">
      <slot name="icon-left"></slot>
    </span>

    <!-- Content -->
    <slot></slot>

    <!-- Icon Right -->
    <span v-if="iconRight" class="flex-shrink-0 transition-transform group-hover:translate-x-0.5" :class="{ 'ml-2': $slots.default }">
      <slot name="icon-right">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </slot>
    </span>
  </component>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'B2BButton',
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (v) => ['primary', 'secondary', 'ghost', 'gold', 'danger', 'success', 'whatsapp'].includes(v)
    },
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(v)
    },
    to: String,
    href: String,
    type: {
      type: String,
      default: 'button'
    },
    disabled: Boolean,
    loading: Boolean,
    block: Boolean,
    rounded: {
      type: String,
      default: 'lg',
      validator: (v) => ['none', 'sm', 'md', 'lg', 'full'].includes(v)
    },
    iconLeft: Boolean,
    iconRight: Boolean
  },
  emits: ['click'],
  setup(props) {
    const tag = computed(() => {
      if (props.to) return 'router-link'
      if (props.href) return 'a'
      return 'button'
    })

    const buttonClasses = computed(() => {
      const base = [
        'inline-flex items-center justify-center font-semibold',
        'transition-all duration-200 ease-out',
        'focus:outline-none focus:ring-2 focus:ring-offset-2',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        'group'
      ]

      // Variants
      const variants = {
        primary: 'bg-[#1A1A1A] hover:bg-black text-white focus:ring-gray-500',
        secondary: 'bg-white hover:bg-gray-50 text-[#1A1A1A] border border-gray-200 hover:border-gray-300 focus:ring-gray-300',
        ghost: 'bg-transparent hover:bg-gray-100 text-[#1A1A1A] focus:ring-gray-300',
        gold: 'bg-[#C9A962] hover:bg-[#B8984F] text-[#1A1A1A] focus:ring-[#C9A962]/50',
        danger: 'bg-red-500 hover:bg-red-600 text-white focus:ring-red-500',
        success: 'bg-emerald-500 hover:bg-emerald-600 text-white focus:ring-emerald-500',
        whatsapp: 'bg-green-500 hover:bg-green-600 text-white focus:ring-green-500'
      }

      // Sizes
      const sizes = {
        xs: 'text-xs px-2.5 py-1.5',
        sm: 'text-sm px-3 py-2',
        md: 'text-sm px-4 py-2.5',
        lg: 'text-base px-5 py-3',
        xl: 'text-base px-6 py-3.5'
      }

      // Rounded
      const roundedClasses = {
        none: 'rounded-none',
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
        props.block ? 'w-full' : ''
      ].join(' ')
    })

    return { tag, buttonClasses }
  }
}
</script>
