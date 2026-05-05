<script setup>
import { ref } from 'vue';

const textoBusqueda = ref('');
const plataforma = ref('');
const region = ref('');
const precio = ref(''); // max price

const emit = defineEmits(['buscar']);

const ejecutarBusqueda = () => {
  emit('buscar', {
    q: textoBusqueda.value,
    plat: plataforma.value,
    reg: region.value,
    maxP: precio.value
  });
};
</script>

<template>
  <section class="search-section py-5" style="background: var(--card-bg, #1a1a2e); border-bottom: 2px solid rgba(20, 203, 129, 0.3);">
    <div class="container">
      <h2 class="text-center mb-4 fw-bold" style="color: var(--white-off); font-size: 2.2rem;">
        ¿Qué quieres <span style="color: var(--green-accent);">jugar hoy?</span>
      </h2>
      <div class="row justify-content-center">
        <div class="col-lg-10 col-xl-9">
          <!-- Search Bar Container -->
          <div class="d-flex flex-column flex-md-row gap-2 bg-dark p-2 rounded-4 shadow-lg border" style="border-color: var(--purple-mid) !important; background-color: var(--purple-dark) !important;">
            
            <!-- Input Principal -->
            <div class="flex-grow-1 position-relative d-flex align-items-center">
              <i class="bi bi-search text-muted ms-3 fs-5"></i>
              <input 
                type="text" 
                class="form-control form-control-lg border-0 bg-transparent text-white search-main-input" 
                placeholder="Busca por título o género..."
                v-model="textoBusqueda"
                @keyup.enter="ejecutarBusqueda"
                style="box-shadow: none;"
              />
            </div>
            
            <div class="vr bg-secondary d-none d-md-block mx-1"></div>
            
            <!-- Filtro Plataforma -->
            <select class="form-select form-select-lg border-0 bg-transparent text-white w-auto search-select" v-model="plataforma">
              <option value="" class="text-dark">Plataforma</option>
              <option value="PC" class="text-dark">PC</option>
              <option value="PlayStation" class="text-dark">PlayStation</option>
              <option value="Xbox" class="text-dark">Xbox</option>
              <option value="Nintendo" class="text-dark">Nintendo</option>
            </select>

            <div class="vr bg-secondary d-none d-md-block mx-1"></div>
            
            <!-- Filtro Región -->
            <select class="form-select form-select-lg border-0 bg-transparent text-white w-auto search-select" v-model="region">
              <option value="" class="text-dark">Región</option>
              <option value="Global" class="text-dark">Global</option>
              <option value="US" class="text-dark">US</option>
              <option value="EU" class="text-dark">EU</option>
              <option value="MX" class="text-dark">MX</option>
              <option value="Asia" class="text-dark">Asia</option>
            </select>

            <div class="vr bg-secondary d-none d-md-block mx-1"></div>

            <!-- Filtro Precio Máximo -->
            <div class="d-flex align-items-center px-2">
              <span class="text-muted me-1 fw-bold" style="font-size: 0.9rem;">Máx $</span>
              <input type="number" class="form-control form-control-lg border-0 bg-transparent text-white p-0 text-center search-price" placeholder="---" style="width: 60px; box-shadow: none;" v-model="precio" @keyup.enter="ejecutarBusqueda" min="0">
            </div>

            <!-- Botón Buscar -->
            <button class="btn btn-lg px-4 ms-1 search-action-btn" @click="ejecutarBusqueda">
              <i class="bi bi-search me-2 d-md-none"></i>Buscar
            </button>    
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.search-main-input::placeholder, .search-price::placeholder {
  color: rgba(255, 255, 255, 0.7);
}
.search-select {
  cursor: pointer;
  color: var(--white-off) !important;
}
.search-select option {
  background: var(--card-bg);
  color: #fff;
}
.search-select:focus, .search-main-input:focus, .search-price:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.05) !important;
}
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none; 
  margin: 0; 
}
.search-action-btn {
  background: linear-gradient(135deg, var(--green-accent) 0%, #10a66a 100%);
  color: #000;
  font-weight: 800;
  border-radius: 12px;
  border: none;
  transition: transform 0.2s, box-shadow 0.2s;
}
.search-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(20, 203, 129, 0.4);
}

.text-muted {
  color: var(--purple-soft, #c9a0ff) !important;
}
</style>