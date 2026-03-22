<script setup>
import { ref } from 'vue';

// Variables que elige el usuario
const textoBusqueda = ref('');
const plataforma = ref('');
const genero = ref('');
const precio = ref('');

// 2. Definimos el "emit". Esto sirve para avisarle a la página principal 
// que el usuario hizo clic en buscar y pasarle los datos filtrados.
const emit = defineEmits(['buscar']);

const ejecutarBusqueda = () => {
  emit('buscar', {
    texto: textoBusqueda.value,
    plataforma: plataforma.value,
    genero: genero.value,
    precio: precio.value
  });
  
  // Nota: Cuando configuremos Vue Router, aquí agregaremos una línea para 
  // redirigir al usuario automáticamente a la página de /catalogo
};
</script>

<template>
  <section class="search-section">
    <div>
      <h1 class="text-uppercase mb-2" style="font-size:.75rem;letter-spacing:.15em;color:var(--green-accent);font-weight:600;padding-left: 50px;">
        <i class="bi bi-controller me-1"></i> Busca tu juego en nuestro catálogo
      </h1>
    </div>
    <div class="container">
      <div class="row g-2 align-items-center">
        
        <div class="col-12 col-md-6">
          <div class="input-group">
            <input 
              type="text" 
              class="form-control search-input" 
              placeholder="Buscar juego..."
              v-model="textoBusqueda"
              @keyup.enter="ejecutarBusqueda"
            />
            <button class="search-btn" @click="ejecutarBusqueda">
              <i class="bi bi-search"></i>
            </button>    
          </div>
        </div>

        <div class="col-4 col-md-2">
          <select class="filter-select w-100" v-model="plataforma">
            <option value="">Plataforma</option>
            <option value="pc">PC</option>
            <option value="playstation">PlayStation</option>
            <option value="xbox">Xbox</option>
          </select>
        </div>

        <div class="col-4 col-md-2">
          <select class="filter-select w-100" v-model="genero">
            <option value="">Género</option>
            <option value="accion">Acción</option>
            <option value="rpg">RPG</option>
            <option value="estrategia">Estrategia</option>
            <option value="deportes">Deportes</option>
          </select>
        </div>

        <div class="col-4 col-md-2">  
          <select class="filter-select w-100" v-model="precio">
            <option value="">Precio</option>
            <option value="bajo">Menos de $200</option>
            <option value="medio">$200 - $600</option>
            <option value="alto">Más de $600</option>
          </select>
        </div>

      </div>
    </div>
  </section>
</template>

<style scoped>

.filter-select {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
</style>