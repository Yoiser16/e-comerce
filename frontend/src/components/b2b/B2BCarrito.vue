<template>
  <div class="text-center py-16">
    <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
    </svg>
    <h1 class="text-2xl font-luxury text-text-dark mb-4">Mi Carrito Mayorista</h1>
    <p class="text-text-light">Tu carrito está vacío</p>
    <router-link 
      to="/portal/catalogo" 
      class="inline-block mt-4 px-6 py-3 bg-[#1A1A1A] text-white rounded-lg hover:bg-black transition-colors"
    >
      Explorar Catálogo
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'B2BCarrito'
}
</script>
