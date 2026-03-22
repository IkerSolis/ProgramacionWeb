<script setup>
import { ref } from 'vue';
import SearchBar from '../components/SearchBar.vue';
import GameCard from '../components/GameCard.vue';
import HeroCarousel from '../components/HeroCarousel.vue';

const juegosDestacados = ref([
    { id: 1, titulo: "Cyberpunk 2077", plataforma: "PC / Steam Key", imagen: "/img/cyberpunk.webp", precioOriginal: "899.00", precioFinal: "449.50", descuento: 50 },
    { id: 2, titulo: "Hora Pico: Rumble", plataforma: "Xbox Key", imagen: "/img/horaPico-Rumbel.png", precioOriginal: "299.00", precioFinal: "239.20", descuento: 20 },
    { id: 3, titulo: "Elden Ring", plataforma: "PC / Steam Key", imagen: "/img/eldenring.webp", precioOriginal: "799.00", precioFinal: "799.00", descuento: 0 },
    { id: 4, titulo: "Helldivers 2", plataforma: "PS5 Key", imagen: "/img/helldivers.jpg", precioOriginal: "699.00", precioFinal: "699.00", descuento: 0 }
]);

const manejarBusqueda = (filtros) => { console.log('Buscando:', filtros); };
const sumarAlCarrito = (juego) => { console.log(`Añadido: ${juego.titulo}`); };
</script>

<template>
  <div>
    <HeroCarousel />

    <SearchBar @buscar="manejarBusqueda" />

    <section class="featured-games py-5" style="background-color: var(--purple-dark); border-bottom: 1px solid rgba(107, 63, 160, 0.3);">
      <div class="container">
        <div class="d-flex align-items-center mb-4 pb-2">
          <i class="bi bi-star-fill me-3 fs-2" style="color: var(--green-accent); filter: drop-shadow(0 0 8px rgba(127,255,110,0.6));"></i>
          <h2 class="mb-0" style="color: var(--white-off); font-size: 2rem;">
            Juegos <span style="color: var(--green-accent);">Destacados</span>
          </h2>
        </div>
        <div class="row g-4">
          <div class="col-12 col-sm-6 col-lg-3" v-for="juego in juegosDestacados" :key="juego.id">
            <GameCard :juego="juego" @agregar-carrito="sumarAlCarrito(juego)" />
          </div>
        </div>
      </div>
    </section>

  </div>
</template>