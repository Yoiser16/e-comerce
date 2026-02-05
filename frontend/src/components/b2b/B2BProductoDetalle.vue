<template>
  <div class="text-center py-16">
    <h1 class="text-2xl font-luxury text-text-dark mb-4">Detalle de Producto</h1>
    <p class="text-text-light">Producto ID: {{ $route.params.id }}</p>
    <p class="text-text-light mt-2">Componente en desarrollo...</p>
    <router-link to="/portal/catalogo" class="inline-block mt-4 text-[#C9A962] hover:underline">
      ← Volver al catálogo
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'B2BProductoDetalle'
}
</script>
