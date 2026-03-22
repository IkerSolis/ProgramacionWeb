<script setup>
// Recibimos un objeto "juego" desde el componente padre
defineProps({
  juego: {
    type: Object,
    required: true
  }
});

// Avisamos al componente padre que se hizo clic en el carrito
const emit = defineEmits(['agregar-carrito']);

const agregarAlCarrito = () => {
  emit('agregar-carrito');
};
</script>

<template>
  <div class="product-card position-relative h-100 d-flex flex-column">
    
    <span v-if="juego.descuento > 0" class="position-absolute top-0 end-0 mt-3 me-3 badge rounded-pill px-2 py-1" 
          style="background-color: var(--green-accent); color: #000; font-weight: 800; font-family: 'Orbitron', sans-serif; z-index: 2; box-shadow: 0 4px 10px rgba(127,255,110,0.4);">
        -{{ juego.descuento }}%
    </span>
    
    <img :src="juego.imagen" :alt="juego.titulo" class="img-fluid">
    
    <div class="mt-3 text-start d-flex flex-column flex-grow-1">
        <p class="product-name mb-1 fs-5">{{ juego.titulo }}</p>
        <p class="text-muted mb-3" style="font-size: 0.8rem;">{{ juego.plataforma }}</p>
        
        <div class="mt-auto d-flex justify-content-between align-items-center">
            <div class="d-flex flex-column">
                <small v-if="juego.descuento > 0" class="text-decoration-line-through text-muted" style="font-size: 0.75rem;">
                    ${{ juego.precioOriginal }}
                </small>
                <span class="fw-bold fs-5" style="color: var(--green-accent); font-family: 'Orbitron', sans-serif;">
                    ${{ juego.precioFinal }}
                </span>
            </div>
            
            <button class="nk-btn nk-add p-2" title="Añadir al carrito" @click="agregarAlCarrito">
                <i class="bi bi-cart-plus fs-5"></i>
            </button>
        </div>
    </div>
  </div>
</template>

<style scoped>

</style>