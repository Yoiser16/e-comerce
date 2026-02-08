<template>
  <div 
    class="group bg-white rounded-xl border border-gray-100 overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
    :class="{ 'opacity-60': !product.inStock }"
  >
    <!-- Image Section -->
    <router-link 
      :to="`/portal/producto/${product.id}`"
      class="block relative aspect-square bg-gray-50 overflow-hidden cursor-pointer"
    >
      <video
        v-if="isVideo && !imageError"
        :src="videoSrc"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        muted
        playsinline
        loop
        autoplay
        @error="handleImageError"
      ></video>
      <img
        v-else
        :src="imageSrc"
        :alt="product.name"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        @error="handleImageError"
      />

      <!-- Badges Container -->
      <div class="absolute top-3 left-3 flex flex-col gap-2">
        <span 
          v-if="product.isNew"
          class="px-2.5 py-1 bg-emerald-500 text-white text-[10px] font-bold uppercase tracking-wider rounded-full shadow-lg"
        >
          Nuevo
        </span>
        <span 
          v-if="product.stock <= 5 && product.stock > 0"
          class="px-2.5 py-1 bg-amber-500 text-white text-[10px] font-bold uppercase tracking-wider rounded-full shadow-lg animate-pulse"
        >
          ¡Últimas {{ product.stock }} uds!
        </span>
        <span 
          v-if="product.isBestSeller"
          class="px-2.5 py-1 bg-rose-500 text-white text-[10px] font-bold uppercase tracking-wider rounded-full shadow-lg"
        >
          🔥 Top Ventas
        </span>
        <span 
          v-if="discountPercentage > 0"
          class="px-2.5 py-1 bg-[#1A1A1A] text-white text-[10px] font-bold rounded-full shadow-lg"
        >
          -{{ discountPercentage }}%
        </span>
      </div>

      <!-- Stock Badge (Right) -->
      <div class="absolute top-3 right-3">
        <span 
          class="px-2 py-1 text-[10px] font-semibold rounded-full"
          :class="stockBadgeClass"
        >
          {{ stockLabel }}
        </span>
      </div>
    </router-link>

    <!-- Product Info -->
    <div class="p-4">
      <!-- Category -->
      <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">{{ product.category }}</p>
      
      <!-- Name -->
      <router-link :to="`/portal/producto/${product.id}`" class="block">
        <h3 class="font-semibold text-gray-900 text-sm line-clamp-2 min-h-[2.5rem] mb-2 leading-snug hover:text-[#C9A962] transition-colors">
          {{ product.name }}
        </h3>
      </router-link>

      <!-- SKU -->
      <p v-if="product.sku" class="text-gray-400 text-xs mb-2">SKU: {{ product.sku }}</p>

      <!-- Pricing -->
      <div class="flex items-end justify-between gap-2 mb-3">
        <div>
          <p v-if="product.retailPrice" class="text-gray-400 text-xs line-through">
            ${{ formatPrice(product.retailPrice) }}
          </p>
          <p class="text-[#C9A962] font-bold text-lg">
            ${{ formatPrice(product.wholesalePrice) }}
          </p>
        </div>
        <div v-if="savingsAmount > 0" class="text-right">
          <p class="text-emerald-600 text-xs font-medium">
            Ahorras ${{ formatPrice(savingsAmount) }}
          </p>
        </div>
      </div>

      <!-- Min Order -->
      <div class="flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-100">
        <span>Mín. {{ product.minOrder }} uds</span>
        <span class="flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z"/>
          </svg>
          {{ product.stock }} disponibles
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'B2BProductCard',
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  emits: ['add-to-cart'],
  setup(props, { emit }) {
    const quantity = ref(props.product.minOrder || 1)
    const imageError = ref(false)

    const placeholderImage = computed(() => {
      const initials = props.product.name?.substring(0, 3).toUpperCase() || 'IMG'
      return `https://placehold.co/400x400/f5f5f5/1a1a1a?text=${encodeURIComponent(initials)}`
    })

    // Si la imagen es válida, úsala; si no, usa el placeholder
    const imageSrc = computed(() => {
      // Si hay error de carga o la imagen es null/undefined/vacía, usar placeholder
      if (imageError.value || !props.product.image || props.product.image === null || props.product.image === undefined || props.product.image === '') {
        return placeholderImage.value
      }
      return props.product.image
    })

    const isVideo = computed(() => {
      const src = (props.product.image || '').toLowerCase()
      return src.includes('.mp4') || src.includes('.webm') || src.includes('.ogg')
    })

    const videoSrc = computed(() => props.product.image || '')

    const discountPercentage = computed(() => {
      if (!props.product.retailPrice || !props.product.wholesalePrice) return 0
      return Math.round((1 - props.product.wholesalePrice / props.product.retailPrice) * 100)
    })

    const savingsAmount = computed(() => {
      if (!props.product.retailPrice || !props.product.wholesalePrice) return 0
      return props.product.retailPrice - props.product.wholesalePrice
    })

    const stockBadgeClass = computed(() => {
      if (!props.product.inStock || props.product.stock === 0) {
        return 'bg-red-100 text-red-700'
      }
      if (props.product.stock <= 5) {
        return 'bg-amber-100 text-amber-700'
      }
      return 'bg-emerald-100 text-emerald-700'
    })

    const stockLabel = computed(() => {
      if (!props.product.inStock || props.product.stock === 0) {
        return 'Agotado'
      }
      if (props.product.stock <= 5) {
        return 'Poco stock'
      }
      return 'En stock'
    })

    function formatPrice(value) {
      return value?.toLocaleString('es-CO') || '0'
    }

    function handleImageError(event) {
      imageError.value = true
      event.target.src = placeholderImage.value
    }

    function incrementQuantity() {
      if (quantity.value < props.product.stock) {
        quantity.value++
      }
    }

    function decrementQuantity() {
      if (quantity.value > (props.product.minOrder || 1)) {
        quantity.value--
      }
    }

    function addToCart() {
      emit('add-to-cart', {
        product: props.product,
        quantity: quantity.value
      })
    }

    return {
      quantity,
      placeholderImage,
      imageSrc,
      isVideo,
      videoSrc,
      discountPercentage,
      savingsAmount,
      stockBadgeClass,
      stockLabel,
      formatPrice,
      handleImageError,
      incrementQuantity,
      decrementQuantity,
      addToCart
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
