<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  juego: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['agregar-carrito']);
const router = useRouter();

const agregarAlCarrito = () => {
  emit('agregar-carrito');
};

const irAlDetalle = () => {
  router.push({ name: 'ProductDetail', params: { id: props.juego.id } });
};
</script>

<template>
  <div class="game-card position-relative h-100 d-flex flex-column" @click="irAlDetalle" style="cursor: pointer;">
    <div class="card-img-container">
      <img :src="juego.cover || '/img/placeholder.jpg'" :alt="juego.title" class="card-img">
    </div>
    
    <div class="card-body mt-2 d-flex flex-column flex-grow-1 text-start">
      <p class="game-title mb-1 text-truncate" :title="juego.title">{{ juego.title }}</p>
      <p class="game-genre mb-2 text-truncate">{{ juego.genre || 'Género no definido' }}</p>
      
      <div class="platforms mb-2 d-flex flex-wrap gap-1" v-if="juego.plataformas && juego.plataformas.length">
        <span v-for="plat in juego.plataformas" :key="plat" class="platform-badge">{{ plat }}</span>
      </div>
      <div class="platforms mb-2" v-else>
        <span class="platform-badge" style="opacity:0.5;">Sin keys</span>
      </div>

      <div class="mt-auto d-flex justify-content-between align-items-end">
        <div class="d-flex flex-column">
          <small class="text-muted" style="font-size: 0.7rem;">Desde</small>
          <span v-if="juego.lowestPrice" class="game-price">${{ parseFloat(juego.lowestPrice).toFixed(2) }}</span>
          <span v-else class="text-danger fw-bold" style="font-size:0.9rem;">Agotado</span>
        </div>
        <button class="btn-cart p-2" title="Añadir al carrito" @click.stop="agregarAlCarrito" :disabled="!juego.hasKeys">
          <i class="bi bi-cart-plus fs-5"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.game-card {
  background-color: var(--card-bg, #1a1a2e);
  border: 1px solid var(--purple-mid, #9d71c8);
  border-radius: 12px;
  padding: 0.75rem;
  transition: transform 0.2s, box-shadow 0.2s;
}
.game-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.5);
  border-color: var(--green-accent, #14cb81);
}
.card-img-container {
  width: 100%;
  aspect-ratio: 3/4;
  overflow: hidden;
  border-radius: 8px;
}
.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.game-card:hover .card-img {
  transform: scale(1.05);
}
.game-title {
  font-weight: 700;
  color: var(--white-off, #f8f9fa);
  font-size: 1rem;
}
.game-genre {
  font-size: 0.75rem;
  color: var(--purple-soft, #c9a0ff);
}
.platform-badge {
  font-size: 0.65rem;
  background: rgba(157, 113, 200, 0.2);
  color: var(--white-off);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}
.game-price {
  color: var(--green-accent, #14cb81);
  font-weight: 800;
  font-size: 1.1rem;
  font-family: 'Orbitron', sans-serif;
}
.btn-cart {
  background: rgba(20, 203, 129, 0.1);
  border: 1px solid var(--green-accent, #14cb81);
  color: var(--green-accent, #14cb81);
  border-radius: 8px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-cart:hover:not(:disabled) {
  background: var(--green-accent, #14cb81);
  color: #000;
}
.btn-cart:disabled {
  border-color: #555;
  color: #555;
  background: transparent;
  cursor: not-allowed;
}

.text-muted {
  color: var(--purple-soft, #c9a0ff) !important;
}
</style>