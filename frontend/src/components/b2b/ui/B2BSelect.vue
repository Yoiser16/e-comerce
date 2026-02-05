<template>
  <div class="w-full">
    <!-- Label -->
    <label v-if="label" :for="selectId" class="block text-sm font-medium text-gray-700 mb-1.5">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-0.5">*</span>
    </label>

    <!-- Select -->
    <div class="relative">
      <select
        :id="selectId"
        :value="modelValue"
        :disabled="disabled"
        :class="selectClasses"
        @change="$emit('update:modelValue', $event.target.value)"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option 
          v-for="option in normalizedOptions" 
          :key="option.value" 
          :value="option.value"
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>
      
      <!-- Chevron -->
      <div class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>

    <!-- Helper Text / Error -->
    <p v-if="error" class="mt-1.5 text-sm text-red-500">{{ error }}</p>
    <p v-else-if="hint" class="mt-1.5 text-sm text-gray-500">{{ hint }}</p>
  </div>
</template>

<script>
import { computed } from 'vue'

let idCounter = 0

export default {
  name: 'B2BSelect',
  props: {
    modelValue: [String, Number],
    options: {
      type: Array,
      required: true
    },
    label: String,
    placeholder: String,
    hint: String,
    error: String,
    size: {
      type: String,
      default: 'md',
      validator: (v) => ['sm', 'md', 'lg'].includes(v)
    },
    disabled: Boolean,
    required: Boolean
  },
  emits: ['update:modelValue'],
  setup(props) {
    const selectId = `b2b-select-${++idCounter}`

    const normalizedOptions = computed(() => {
      return props.options.map(opt => {
        if (typeof opt === 'string' || typeof opt === 'number') {
          return { value: opt, label: opt }
        }
        return opt
      })
    })

    const selectClasses = computed(() => {
      const base = [
        'w-full appearance-none border rounded-lg transition-all duration-200',
        'focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none',
        'cursor-pointer pr-10'
      ]

      const sizes = {
        sm: 'text-sm py-2 px-3',
        md: 'text-sm py-2.5 px-4',
        lg: 'text-base py-3 px-4'
      }

      const states = props.error
        ? 'border-red-300 bg-red-50/50'
        : props.disabled
          ? 'border-gray-200 bg-gray-100 text-gray-500 cursor-not-allowed'
          : 'border-gray-200 bg-white hover:border-gray-300'

      return [...base, sizes[props.size], states].join(' ')
    })

    return { selectId, normalizedOptions, selectClasses }
  }
}
</script>
