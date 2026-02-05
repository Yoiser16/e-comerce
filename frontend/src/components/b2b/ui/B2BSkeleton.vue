<template>
  <div :class="skeletonClasses" :style="customStyle">
    <div class="animate-pulse bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%] w-full h-full rounded-inherit"></div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'B2BSkeleton',
  props: {
    variant: {
      type: String,
      default: 'rectangular',
      validator: (v) => ['text', 'circular', 'rectangular', 'rounded'].includes(v)
    },
    width: [String, Number],
    height: [String, Number],
    lines: {
      type: Number,
      default: 1
    }
  },
  setup(props) {
    const skeletonClasses = computed(() => {
      const variants = {
        text: 'rounded h-4',
        circular: 'rounded-full',
        rectangular: '',
        rounded: 'rounded-lg'
      }
      return ['overflow-hidden', variants[props.variant]].join(' ')
    })

    const customStyle = computed(() => {
      const style = {}
      if (props.width) {
        style.width = typeof props.width === 'number' ? `${props.width}px` : props.width
      }
      if (props.height) {
        style.height = typeof props.height === 'number' ? `${props.height}px` : props.height
      }
      return style
    })

    return { skeletonClasses, customStyle }
  }
}
</script>

<style scoped>
.rounded-inherit {
  border-radius: inherit;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.animate-pulse {
  animation: shimmer 1.5s infinite;
}
</style>
