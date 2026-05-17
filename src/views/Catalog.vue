<script setup>
import { API_BASE_URL } from '../api/config.js';
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import GameCard from '../components/GameCard.vue';
import { useCartStore } from '../stores/cart.js';
import { usuarioActual } from '../data/estado.js';

const route = useRoute();
const router = useRouter();
const cartStore = useCartStore();

const productos = ref([]);
const keycodes = ref([]);
const searchQuery = ref('');

// Paginación
const currentPage = ref(1);
const itemsPerPage = 20;

// Filtros
const filterMinPrice = ref(null);
const filterMaxPrice = ref(null);
const filterPlatforms = ref({
  PC: false,
  PlayStation: false,
  Xbox: false,
  Nintendo: false
});
const filterRegion = ref('');

// Reset de paginación al cambiar filtros
watch([filterMinPrice, filterMaxPrice, filterPlatforms, filterRegion], () => {
  currentPage.value = 1;
}, { deep: true });

const cargarDatos = async () => {
  try {
    const resProds = await fetch(`${API_BASE_URL}/api/products/`);
    const resKeys = await fetch(`${API_BASE_URL}/api/keycodes/`);
    
    if (resProds.ok && resKeys.ok) {
      productos.value = await resProds.json();
      keycodes.value = await resKeys.json();
    }
  } catch (err) {
    console.error("Error cargando catálogo", err);
  }
};

onMounted(() => {
  if (route.query.q) searchQuery.value = route.query.q;
  if (route.query.maxP) filterMaxPrice.value = route.query.maxP;
  if (route.query.plat) {
    if (filterPlatforms.value[route.query.plat] !== undefined) {
      filterPlatforms.value[route.query.plat] = true;
    }
  }
  if (route.query.reg) filterRegion.value = route.query.reg;

  cargarDatos();
});

const productosConPrecio = computed(() => {
  let filtrados = productos.value.map(prod => {
    // Buscar keys del producto
    const keysDelProd = keycodes.value.filter(k => k.product === prod.id && !k.is_used);
    
    // Obtener precio más bajo
    let lowestPrice = 0;
    if (keysDelProd.length > 0) {
      lowestPrice = Math.min(...keysDelProd.map(k => parseFloat(k.price)));
    }
    
    // Obtener plataformas únicas
    const plataformas = [...new Set(keysDelProd.map(k => k.platform))];
    const regiones = [...new Set(keysDelProd.map(k => k.region))];

    return {
      ...prod,
      lowestPrice: lowestPrice > 0 ? lowestPrice : null,
      plataformas: plataformas,
      regiones: regiones,
      hasKeys: keysDelProd.length > 0
    };
  });

  // Filtro por búsqueda
  if (searchQuery.value.trim() !== '') {
    const q = searchQuery.value.toLowerCase();
    filtrados = filtrados.filter(p => p.title.toLowerCase().includes(q) || p.genre.toLowerCase().includes(q));
  }

  // Filtro Precio Mínimo
  if (filterMinPrice.value !== null && filterMinPrice.value !== '') {
    filtrados = filtrados.filter(p => p.lowestPrice !== null && p.lowestPrice >= filterMinPrice.value);
  }
  
  // Filtro Precio Máximo
  if (filterMaxPrice.value !== null && filterMaxPrice.value !== '') {
    filtrados = filtrados.filter(p => p.lowestPrice !== null && p.lowestPrice <= filterMaxPrice.value);
  }

  // Filtro Plataformas
  const selectedPlatforms = Object.keys(filterPlatforms.value).filter(k => filterPlatforms.value[k]);
  if (selectedPlatforms.length > 0) {
    filtrados = filtrados.filter(p => p.plataformas.some(plat => selectedPlatforms.includes(plat)));
  }

  // Filtro Región
  if (filterRegion.value !== '') {
    filtrados = filtrados.filter(p => p.regiones.includes(filterRegion.value));
  }

  return filtrados;
});

const totalPages = computed(() => Math.ceil(productosConPrecio.value.length / itemsPerPage) || 1);

const paginatedProductos = computed(() => {
  // Asegurarnos de que currentPage no sea mayor a totalPages
  const current = currentPage.value > totalPages.value ? totalPages.value : currentPage.value;
  const start = (current - 1) * itemsPerPage;
  return productosConPrecio.value.slice(start, start + itemsPerPage);
});

const nextPg = () => { if (currentPage.value < totalPages.value) currentPage.value++; }
const prevPg = () => { if (currentPage.value > 1) currentPage.value--; }

const sumarAlCarrito = (juego) => {
  if (!usuarioActual.value) {
    alert("Inicia sesión para poder comprar.");
    router.push('/login');
    return;
  }
  if (usuarioActual.value.is_staff) {
    alert("Los administradores no pueden hacer compras.");
    return;
  }

  // Buscar la llave más barata disponible de este juego
  const keysDelProd = keycodes.value.filter(k => k.product === juego.id && !k.is_used);
  if (keysDelProd.length === 0) return;
  
  const cheapestKey = keysDelProd.reduce((prev, curr) => parseFloat(curr.price) < parseFloat(prev.price) ? curr : prev);

  cartStore.addItem({
    keyId: cheapestKey.id,
    productTitle: juego.title,
    platform: cheapestKey.platform,
    region: cheapestKey.region,
    price: cheapestKey.price
  });
};
</script>

<template>
  <div class="catalog-page">
    <div class="container py-5">
      <!-- Título de página -->
      <div class="mb-4 text-center">
         <h1 class="catalog-title mb-1 text-white">Catálogo de <span style="color: var(--green-accent);">Juegos</span></h1>
         <p style="color:var(--purple-soft); font-size:.92rem;">Encuentra las mejores ofertas y llaves al instante.</p>
      </div>

      <!-- Barra de búsqueda superior -->
      <div class="row mb-5 justify-content-center">
        <div class="col-md-8">
          <div class="search-bar-container">
            <i class="bi bi-search search-icon"></i>
            <input v-model="searchQuery" @input="currentPage = 1" type="text" class="catalog-search" placeholder="Buscar videojuegos por título, género...">
          </div>
        </div>
      </div>

      <div class="row g-4">
        <!-- Sidebar Filtros -->
        <div class="col-lg-3 col-md-4">
          <div class="filters-sidebar">
            <h4 class="filters-title"><i class="bi bi-funnel-fill me-2"></i>Filtros</h4>
            <hr class="filters-divider">
            
            <div class="filter-group mb-4">
              <h5 class="filter-subtitle">Precio</h5>
              <div class="d-flex align-items-center gap-2">
                <input v-model="filterMinPrice" type="number" class="filter-input" placeholder="Mín" min="0" />
                <span class="text-white">-</span>
                <input v-model="filterMaxPrice" type="number" class="filter-input" placeholder="Máx" min="0" />
              </div>
            </div>

            <div class="filter-group mb-4">
              <h5 class="filter-subtitle">Plataforma</h5>
              <div class="form-check custom-checkbox mb-2">
                <input v-model="filterPlatforms.PC" class="form-check-input" type="checkbox" id="plat-pc">
                <label class="form-check-label" for="plat-pc">PC</label>
              </div>
              <div class="form-check custom-checkbox mb-2">
                <input v-model="filterPlatforms.PlayStation" class="form-check-input" type="checkbox" id="plat-ps">
                <label class="form-check-label" for="plat-ps">PlayStation</label>
              </div>
              <div class="form-check custom-checkbox mb-2">
                <input v-model="filterPlatforms.Xbox" class="form-check-input" type="checkbox" id="plat-xbox">
                <label class="form-check-label" for="plat-xbox">Xbox</label>
              </div>
              <div class="form-check custom-checkbox mb-2">
                <input v-model="filterPlatforms.Nintendo" class="form-check-input" type="checkbox" id="plat-nin">
                <label class="form-check-label" for="plat-nin">Nintendo</label>
              </div>
            </div>

            <div class="filter-group mb-4">
              <h5 class="filter-subtitle">Región</h5>
              <select v-model="filterRegion" class="filter-select w-100 p-2">
                <option value="">Cualquier región</option>
                <option value="Global">Global</option>
                <option value="US">US</option>
                <option value="EU">EU</option>
                <option value="MX">MX</option>
                <option value="Asia">Asia</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Grid Productos -->
        <div class="col-lg-9 col-md-8">
          <div v-if="paginatedProductos.length === 0" class="text-center py-5">
            <i class="bi bi-controller fs-1 text-muted"></i>
            <h4 class="mt-3 text-white">No se encontraron productos</h4>
            <p class="text-muted">Intenta buscar con otros términos.</p>
          </div>
          
          <div class="row row-cols-2 row-cols-lg-3 row-cols-xl-4 g-3">
            <div class="col" v-for="juego in paginatedProductos" :key="juego.id">
              <GameCard :juego="juego" @agregar-carrito="sumarAlCarrito(juego)" />
            </div>
          </div>

          <!-- Paginación -->
          <div v-if="totalPages > 1" class="d-flex justify-content-center align-items-center mt-5 gap-3">
            <button class="btn nk-btn-outline" @click="prevPg" :disabled="currentPage === 1">
              <i class="bi bi-chevron-left"></i> Anterior
            </button>
            <span class="text-muted fw-bold">Página {{ currentPage }} de {{ totalPages }}</span>
            <button class="btn nk-btn-outline" @click="nextPg" :disabled="currentPage === totalPages">
              Siguiente <i class="bi bi-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.catalog-title { font-weight: 800; }
.search-bar-container {
  position: relative;
  display: flex;
  align-items: center;
}
.search-icon {
  position: absolute;
  left: 1.2rem;
  color: var(--purple-soft, #c9a0ff);
  font-size: 1.2rem;
}
.catalog-search {
  width: 100%;
  background: var(--purple-dark, #2a1b3d);
  border: 2px solid var(--purple-mid, #9d71c8);
  border-radius: 50px;
  padding: 1rem 1rem 1rem 3rem;
  color: var(--white-off, #f8f9fa);
  font-size: 1rem;
  transition: all 0.3s;
}
.catalog-search:focus {
  outline: none;
  border-color: var(--green-accent, #14cb81);
  box-shadow: 0 0 15px rgba(20, 203, 129, 0.2);
}

.filters-sidebar {
  background: var(--card-bg, #1a1a2e);
  border: 1px solid var(--purple-mid, #9d71c8);
  border-radius: 12px;
  padding: 1.5rem;
}
.filters-title { color: var(--white-off); font-weight: 700; font-size: 1.2rem; margin-bottom: 0; }
.filters-divider { border-top: 1px solid rgba(157, 113, 200, 0.4); margin: 1rem 0; }
.filter-subtitle { color: var(--green-accent); font-size: 0.95rem; font-weight: 600; margin-bottom: 0.8rem; }
.filter-input {
  width: 100%;
  background: var(--purple-dark);
  border: 1px solid var(--purple-mid);
  border-radius: 6px;
  padding: 0.4rem 0.6rem;
  color: white;
  outline: none;
}
.filter-input:focus { border-color: var(--green-accent); }
.custom-checkbox .form-check-input {
  background-color: transparent;
  border-color: var(--purple-mid);
}
.custom-checkbox .form-check-input:checked {
  background-color: var(--green-accent);
  border-color: var(--green-accent);
}
.custom-checkbox .form-check-label { color: var(--purple-soft); font-size: 0.9rem; }
.filter-select {
  background: var(--purple-dark);
  border: 1px solid var(--purple-mid);
  color: white;
  border-radius: 6px;
  outline: none;
}
.filter-select option { background: var(--purple-dark); }

.nk-btn-outline {
  color: var(--green-accent, #14cb81);
  border: 1px solid var(--green-accent, #14cb81);
  background: transparent;
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-weight: 600;
  transition: all 0.3s;
}
.nk-btn-outline:hover:not(:disabled) {
  background: rgba(20, 203, 129, 0.1);
  color: var(--green-accent);
  transform: translateY(-2px);
}
.nk-btn-outline:disabled {
  border-color: #555;
  color: #555;
}
</style>