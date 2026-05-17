<script setup>
import { API_BASE_URL } from '../api/config.js';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import SearchBar from '../components/SearchBar.vue';
import GameCard from '../components/GameCard.vue';
import HeroCarousel from '../components/HeroCarousel.vue';

const router = useRouter();

const juegosNuevos = ref([]);
const cargando = ref(true);

onMounted(async () => {
  try {
    const resProds = await fetch(`${API_BASE_URL}/api/products/`);
    const resKeys = await fetch(`${API_BASE_URL}/api/keycodes/`);
    
    if (resProds.ok && resKeys.ok) {
      const productosData = await resProds.json();
      const keycodesData = await resKeys.json();
      
      // Tomamos los últimos 4 productos agregados (al final del array) y los invertimos
      let ultimos = productosData.slice(-4).reverse();
      
      juegosNuevos.value = ultimos.map(prod => {
        const keysDelProd = keycodesData.filter(k => k.product === prod.id && !k.is_used);
        let lowestPrice = 0;
        if (keysDelProd.length > 0) {
          lowestPrice = Math.min(...keysDelProd.map(k => parseFloat(k.price)));
        }
        const plataformas = [...new Set(keysDelProd.map(k => k.platform))];

        return {
          ...prod,
          lowestPrice: lowestPrice > 0 ? lowestPrice : null,
          plataformas: plataformas,
          hasKeys: keysDelProd.length > 0
        };
      });
    }
  } catch(err) {
    console.error("Error al cargar juegos nuevos", err);
  } finally {
    cargando.value = false;
  }
});

const manejarBusqueda = (filtros) => { 
  // Redirigir al catálogo pasando los filtros por la URL
  router.push({ name: 'catalogo', query: filtros });
};

const sumarAlCarrito = (juego) => { 
  console.log(`Añadido al carrito: ${juego.title}`); 
};
</script>

<template>
  <div>
    <HeroCarousel />

    <SearchBar @buscar="manejarBusqueda" />

    <section class="featured-container py-5">
      <div class="container">
        <div class="d-flex align-items-center mb-4 pb-2">
          <i class="bi bi-stars me-3 fs-2" style="color: var(--green-accent); filter: drop-shadow(0 0 8px rgba(127,255,110,0.6));"></i>
          <h2 class="mb-0" style="color: var(--white-off); font-size: 2.2rem; font-weight: 800;">
            Juegos <span style="color: var(--green-accent);">Nuevos</span>
          </h2>
        </div>
        
        <div v-if="cargando" class="text-center py-5">
          <div class="spinner-border text-success" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
        </div>
        
        <div v-else-if="juegosNuevos.length === 0" class="text-center text-muted py-5">
          <i class="bi bi-controller fs-1 d-block mb-3"></i>
          Aún no hay juegos en el catálogo.
        </div>

        <div v-else class="row g-4">
          <div class="col-12 col-sm-6 col-lg-3" v-for="juego in juegosNuevos" :key="juego.id">
            <GameCard :juego="juego" @agregar-carrito="sumarAlCarrito(juego)" />
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.featured-container {
  background-color: var(--bg-primary, #0f0f1a);
}
</style>