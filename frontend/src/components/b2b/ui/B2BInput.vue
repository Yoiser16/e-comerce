<template>
  <div class="w-full">
    <!-- Label -->
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700 mb-1.5">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-0.5">*</span>
    </label>

    <!-- Input Container -->
    <div class="relative">
      <!-- Prefix Icon -->
      <div v-if="$slots.prefix" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
        <slot name="prefix"></slot>
      </div>

      <!-- Input -->
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :min="min"
        :max="max"
        :step="step"
        :class="inputClasses"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />

      <!-- Suffix Icon / Clear Button -->
      <div v-if="$slots.suffix || clearable" class="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
        <button 
          v-if="clearable && modelValue"
          type="button"
          class="text-gray-400 hover:text-gray-600 transition-colors"
          @click="$emit('update:modelValue', '')"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <slot name="suffix"></slot>
      </div>
    </div>

    <!-- Helper Text / Error -->
    <p v-if="error" class="mt-1.5 text-sm text-red-500 flex items-center gap-1">
      <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      {{ error }}
    </p>
    <p v-else-if="hint" class="mt-1.5 text-sm text-gray-500">{{ hint }}</p>
  </div>
</template>

<script>
import { computed } from 'vue'

let idCounter = 0

export default {
  name: 'B2BInput',
  props: {
    modelValue: [String, Number],
    type: {
      type: String,
      default: 'text'
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
    readonly: Boolean,
    required: Boolean,
    clearable: Boolean,
    min: [String, Number],
    max: [String, Number],
    step: [String, Number]
  },
  emits: ['update:modelValue', 'blur', 'focus'],
  setup(props, { slots }) {
    const inputId = `b2b-input-${++idCounter}`

    const inputClasses = computed(() => {
      const base = [
        'w-full border rounded-lg transition-all duration-200',
        'focus:ring-2 focus:ring-[#C9A962]/30 focus:border-[#C9A962] outline-none',
        'placeholder:text-gray-400'
      ]

      const sizes = {
        sm: 'text-sm py-2 px-3',
        md: 'text-sm py-2.5 px-4',
        lg: 'text-base py-3 px-4'
      }

      const states = props.error
        ? 'border-red-300 bg-red-50/50 focus:ring-red-200 focus:border-red-400'
        : props.disabled
          ? 'border-gray-200 bg-gray-100 text-gray-500 cursor-not-allowed'
          : 'border-gray-200 bg-white hover:border-gray-300'

      const paddingLeft = slots.prefix ? 'pl-10' : ''
      const paddingRight = slots.suffix || props.clearable ? 'pr-10' : ''

      return [...base, sizes[props.size], states, paddingLeft, paddingRight].join(' ')
    })

    return { inputId, inputClasses }
  }
}
</script>
