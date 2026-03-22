<script setup>
import { ref } from 'vue';
import GameCard from '../components/GameCard.vue';

const juegosCatalogo = ref([
    {
        id: 1,
        titulo: "Hora Pico: Rumble Arena",
        plataforma: "Xbox Key",
        imagen: "/img/horaPico-Rumbel.png",
        precioOriginal: "299.00",
        precioFinal: "299.00",
        descuento: 0
    },
    {
        id: 2,
        titulo: "Cyberpunk 2077",
        plataforma: "PC / Steam Key",
        imagen: "/img/cyberpunk.webp",
        precioOriginal: "899.00",
        precioFinal: "449.50",
        descuento: 50
    },
    {
        id: 3,
        titulo: "Helldivers 2",
        plataforma: "PS5 Key",
        imagen: "/img/helldivers.jpg",
        precioOriginal: "699.00",
        precioFinal: "699.00",
        descuento: 0
    },
    {
        id: 4,
        titulo: "Elden Ring",
        plataforma: "PC / Steam Key",
        imagen: "/img/eldenring.webp",
        precioOriginal: "799.00",
        precioFinal: "799.00",
        descuento: 0
    }

]);

const sumarAlCarrito = (juego) => {
    console.log(`Añadiste ${juego.titulo} al carrito desde el catálogo`);
};
</script>

<template>
  <div>
    <section class="catalog-header">
      <div class="container">
        <div class="d-flex flex-wrap align-items-end justify-content-between gap-3">
          <div>
            <h1 class="catalog-header-title mb-1">
              Catálogo de <span>Videojuegos</span>
            </h1>
            <p style="color:var(--purple-soft); font-size:.92rem; margin:0;">
              Explora nuestra colección completa. Filtra, busca y encuentra tu próximo juego favorito.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="catalog-products py-5">
      <h2 class="visually-hidden">Listado de productos</h2>
      <div class="container">
        <div class="row g-4">
          <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="juego in juegosCatalogo" :key="juego.id">
            <GameCard :juego="juego" @agregar-carrito="sumarAlCarrito(juego)" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>

</style>