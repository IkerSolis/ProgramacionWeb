<script setup>
import { ref } from 'vue'
import { authHeader } from '../data/estado.js';

const searchQuery = ref('');
const searchResults = ref([]);
const isSearching = ref(false);
const searchError = ref('');

const buscarEnIGDB = async () => {
  if (!searchQuery.value.trim()) return;
  isSearching.value = true;
  searchError.value = '';
  searchResults.value = [];
  
  try {
    const res = await fetch(`/api/igdb/search/?q=${encodeURIComponent(searchQuery.value)}`, {
      headers: { ...authHeader() }
    });
    if (res.ok) {
      searchResults.value = await res.json();
    } else {
      searchError.value = 'No se encontraron resultados o hubo un error.';
    }
  } catch(err) {
    searchError.value = 'Error al conectar con la búsqueda de IGDB.';
  } finally {
    isSearching.value = false;
  }
};

const seleccionarJuego = (game) => {
  juego.value.title = game.name || '';
  juego.value.description = game.summary || 'Descripción pendiente';
  juego.value.genre = game.genres && game.genres.length > 0 ? game.genres.map(g => g.name).join(', ') : 'Por definir';
  
  if (game.cover && game.cover.url) {
    let coverUrl = game.cover.url.startsWith('//') ? 'https:' + game.cover.url : game.cover.url;
    coverUrl = coverUrl.replace('t_thumb', 't_cover_big');
    juego.value.cover = coverUrl;
  } else {
    juego.value.cover = '';
  }
  
  juego.value.igdb_id = game.id || null;
  searchResults.value = [];
  searchQuery.value = '';
};

const juego = ref({
  title: '',
  description: 'Descripción pendiente',
  genre: 'Por definir',
  cover: '',
  igdb_id: null
})

const keys = ref([
  { key: '', platform: 'PC', region: 'Global', price: 0 }
])

const plataformasDisponibles = ['PC', 'PlayStation', 'Xbox', 'Nintendo']
const regionesDisponibles = ['Global', 'MX', 'US', 'EU', 'Asia']

const addKey = () => {
  keys.value.push({ key: '', platform: 'PC', region: 'Global', price: 0 })
}

const removeKey = (index) => {
  if (keys.value.length > 1) {
    keys.value.splice(index, 1)
  } else {
    alert('Debe haber al menos una llave.')
  }
}

const errores = ref([])
const exito = ref(false)

const validarFormulario = () => {
  errores.value = []
  exito.value = false

  if (!juego.value.title) errores.value.push("El título es obligatorio")
  if (!juego.value.cover) errores.value.push("La imagen es obligatoria")
  
  if (keys.value.length === 0) errores.value.push("Debes añadir al menos una llave.")
  
  keys.value.forEach((k, idx) => {
    if (!k.key) errores.value.push(`La llave #${idx + 1} no puede estar vacía.`)
    if (k.price < 0) errores.value.push(`El precio de la llave #${idx + 1} no puede ser negativo.`)
  })

  return errores.value.length === 0
}

const guardarJuego = async () => {
  if (!validarFormulario()) return

  const productPayload = {
    title: juego.value.title,
    description: juego.value.description,
    genre: juego.value.genre,
    cover: juego.value.cover,
    igdb_id: juego.value.igdb_id
  };

  try {
    const resProduct = await fetch('/api/products/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeader()
      },
      body: JSON.stringify(productPayload)
    });

    if (resProduct.ok) {
      const productData = await resProduct.json();
      const productId = productData.id;

      // Guardar las llaves
      for (const k of keys.value) {
        const keyPayload = {
          product: productId,
          key: k.key,
          platform: k.platform,
          region: k.region,
          price: k.price,
          is_used: false
        };
        await fetch('/api/keycodes/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...authHeader()
          },
          body: JSON.stringify(keyPayload)
        });
      }

      exito.value = true;

      // Limpiar formulario
      juego.value = { title: '', description: 'Descripción pendiente', genre: 'Por definir', cover: '', igdb_id: null };
      keys.value = [{ key: '', platform: 'PC', region: 'Global', price: 0 }];
      
      setTimeout(() => exito.value = false, 3000);
    } else {
      const errorData = await resProduct.json();
      console.error("Error al guardar producto:", errorData);
      errores.value.push("Error del servidor al crear producto.");
    }
  } catch (error) {
    console.error("Error de red:", error);
    errores.value.push("No se pudo conectar con el backend.");
  }
}
</script>

<template>
  <div class="container py-5 form-container">
    <div class="mb-4">
      <router-link to="/panel" class="back-link">
        <i class="bi bi-arrow-left me-2"></i>Volver al Panel
      </router-link>
    </div>

    <div class="admin-card">
      <div class="admin-card-header text-center mb-4">
        <i class="bi bi-plus-square-dotted fs-1 mb-2 d-block" style="color: var(--green-accent);"></i>
        <h2 class="mb-0 text-white">Añadir <span style="color: var(--green-accent);">Videojuego</span></h2>
        <p style="color: var(--purple-soft); font-size: 0.9rem;">Registra un nuevo producto y sus códigos</p>
      </div>

      <div v-if="errores.length" class="alert alert-danger custom-alert">
        <div class="d-flex align-items-center mb-2" style="font-weight: bold;">
          <i class="bi bi-exclamation-triangle-fill me-2"></i> Por favor corrige lo siguiente:
        </div>
        <ul class="mb-0">
          <li v-for="(error, index) in errores" :key="index">{{ error }}</li>
        </ul>
      </div>

      <div v-if="exito" class="alert alert-success custom-alert-success text-center">
        <i class="bi bi-check-circle-fill me-2"></i> ¡Juego y llaves guardados con éxito!
      </div>

      <form @submit.prevent="guardarJuego" novalidate>

        <h5 class="section-subtitle mb-3"><i class="bi bi-search me-2"></i>Buscador IGDB (Opcional)</h5>
        <div class="mb-4 position-relative">
          <div class="d-flex gap-2">
            <div class="admin-input-group flex-grow-1">
              <span class="admin-icon"><i class="bi bi-search"></i></span>
              <input v-model="searchQuery" @keydown.enter.prevent="buscarEnIGDB" type="text" class="admin-input" placeholder="Buscar juego en IGDB para autocompletar...">
            </div>
            <button type="button" class="btn nk-btn-primary" @click="buscarEnIGDB" :disabled="isSearching">
              <span v-if="isSearching" class="spinner-border spinner-border-sm me-2"></span>
              {{ isSearching ? 'Buscando...' : 'Buscar' }}
            </button>
          </div>
          <div v-if="searchError" class="text-danger mt-2 small">{{ searchError }}</div>
          
          <!-- Resultados IGDB -->
          <div v-if="searchResults.length > 0" class="search-results-dropdown shadow">
            <div class="d-flex justify-content-between align-items-center px-3 py-2 border-bottom" style="border-color: rgba(255,255,255,0.1) !important;">
              <span class="text-muted small">Resultados de búsqueda</span>
              <button type="button" class="btn-close btn-close-white" style="font-size: 0.5rem;" @click="searchResults = []"></button>
            </div>
            <div class="list-group list-group-flush">
              <button type="button" v-for="res in searchResults" :key="res.id" class="list-group-item list-group-item-action search-item" @click="seleccionarJuego(res)">
                <div class="d-flex align-items-center gap-3">
                  <img v-if="res.cover" :src="(res.cover.url.startsWith('//') ? 'https:' + res.cover.url : res.cover.url).replace('t_thumb', 't_cover_small')" class="search-img" alt="cover">
                  <div v-else class="search-img-placeholder"><i class="bi bi-image"></i></div>
                  <div>
                    <h6 class="mb-0 text-white" style="text-align: left;">{{ res.name }}</h6>
                    <small class="text-muted text-start d-block">{{ res.first_release_date ? new Date(res.first_release_date * 1000).getFullYear() : 'Año N/A' }}</small>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <h5 class="section-subtitle mb-3 mt-4"><i class="bi bi-info-circle me-2"></i>Información del Producto</h5>
        
        <div class="mb-4">
          <label class="admin-label">Título del juego</label>
          <div class="admin-input-group">
            <span class="admin-icon"><i class="bi bi-controller"></i></span>
            <input v-model="juego.title" type="text" class="admin-input" placeholder="Ej: Halo Infinite" required>
          </div>
        </div>

        <div class="mb-4">
          <label class="admin-label">Género(s)</label>
          <div class="admin-input-group">
            <span class="admin-icon"><i class="bi bi-tags"></i></span>
            <input v-model="juego.genre" type="text" class="admin-input" placeholder="Ej: Shooter, Aventura" required>
          </div>
        </div>

        <div class="mb-4">
          <label class="admin-label">Descripción</label>
          <div class="admin-input-group" style="align-items: flex-start;">
            <span class="admin-icon" style="padding-top: 0.8rem;"><i class="bi bi-text-paragraph"></i></span>
            <textarea v-model="juego.description" class="admin-input" placeholder="Escribe la descripción del juego..." rows="4" required style="resize: vertical;"></textarea>
          </div>
        </div>

        <div class="mb-4">
          <label class="admin-label">URL de la imagen (Portada)</label>
          <div class="admin-input-group">
            <span class="admin-icon"><i class="bi bi-image"></i></span>
            <input v-model="juego.cover" type="text" class="admin-input" placeholder="/img/mi-juego.jpg" required>
          </div>
        </div>

        <h5 class="section-subtitle mt-5 mb-3 d-flex justify-content-between align-items-center">
          <span><i class="bi bi-key me-2"></i>Llaves (KeyCodes)</span>
          <button type="button" class="btn btn-sm nk-btn-outline-add" @click="addKey">
            <i class="bi bi-plus"></i> Añadir otra llave
          </button>
        </h5>

        <div v-for="(k, index) in keys" :key="index" class="key-block mb-4 p-3 position-relative">
          <button v-if="keys.length > 1" type="button" class="btn-close-key" @click="removeKey(index)" title="Eliminar llave">
            <i class="bi bi-x-circle-fill"></i>
          </button>
          
          <div class="row g-3">
            <div class="col-md-12">
              <label class="admin-label">Código / Llave #{{ index + 1 }}</label>
              <div class="admin-input-group">
                <span class="admin-icon"><i class="bi bi-upc-scan"></i></span>
                <input v-model="k.key" type="text" class="admin-input" placeholder="XXXX-XXXX-XXXX" required>
              </div>
            </div>
            
            <div class="col-md-4">
              <label class="admin-label">Plataforma</label>
              <select v-model="k.platform" class="admin-input-group admin-select w-100 p-2">
                <option v-for="plat in plataformasDisponibles" :key="plat" :value="plat">{{ plat }}</option>
              </select>
            </div>

            <div class="col-md-4">
              <label class="admin-label">Región</label>
              <select v-model="k.region" class="admin-input-group admin-select w-100 p-2">
                <option v-for="reg in regionesDisponibles" :key="reg" :value="reg">{{ reg }}</option>
              </select>
            </div>

            <div class="col-md-4">
              <label class="admin-label">Precio ($)</label>
              <div class="admin-input-group">
                <span class="admin-icon" style="color: var(--green-accent);"><i class="bi bi-currency-dollar"></i></span>
                <input v-model="k.price" type="number" step="0.01" class="admin-input" placeholder="0.00" required>
              </div>
            </div>
          </div>
        </div>

        <button type="submit" class="btn-guardar w-100 mt-4">
          <i class="bi bi-cloud-arrow-up-fill me-2"></i> Guardar Todo en el Catálogo
        </button>

      </form>
    </div>
  </div>
</template>

<style scoped>
.form-container { max-width: 800px; }
.back-link { color: var(--purple-soft); text-decoration: none; font-weight: 600; transition: color 0.3s ease; }
.back-link:hover { color: var(--green-accent); }
.admin-card { background-color: var(--card-bg, #1a1a2e); border: 1px solid var(--purple-mid, #9d71c8); border-radius: 20px; padding: 2.5rem; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4); }
.section-subtitle { color: #fff; font-weight: 700; border-bottom: 1px solid rgba(157, 113, 200, 0.3); padding-bottom: 0.5rem; }
.admin-label { color: var(--white-off, #f8f9fa); font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem; display: block; }
.admin-input-group { display: flex; background-color: var(--purple-dark, #2a1b3d); border: 1px solid var(--purple-mid, #9d71c8); border-radius: 10px; overflow: hidden; transition: border-color 0.3s ease; }
.admin-input-group:focus-within { border-color: var(--green-accent, #14cb81); box-shadow: 0 0 0 2px rgba(20, 203, 129, 0.2); }
.admin-icon { display: flex; align-items: center; justify-content: center; padding: 0 1rem; color: var(--purple-soft, #c9a0ff); background-color: rgba(0, 0, 0, 0.2); }
.admin-input { flex: 1; background: transparent; border: none; color: var(--white-off, #f8f9fa); padding: 0.8rem; outline: none; }
.admin-input::placeholder { color: rgba(157, 113, 200, 0.4); }
.admin-select { color: var(--white-off, #f8f9fa); outline: none; cursor: pointer; }
.admin-select option { background-color: var(--purple-dark, #2a1b3d); color: #fff; }
.key-block { background: rgba(0,0,0,0.15); border: 1px dashed rgba(157, 113, 200, 0.4); border-radius: 12px; }
.btn-close-key { position: absolute; top: -10px; right: -10px; background: #1a1a2e; border: none; color: #ff4d4f; font-size: 1.2rem; border-radius: 50%; cursor: pointer; padding: 0; display: flex; transition: transform 0.2s; }
.btn-close-key:hover { transform: scale(1.1); }
.nk-btn-outline-add { color: var(--green-accent, #14cb81); border: 1px dashed var(--green-accent, #14cb81); background: transparent; border-radius: 6px; transition: 0.3s; }
.nk-btn-outline-add:hover { background: rgba(20, 203, 129, 0.1); border-style: solid; }
.custom-alert { background-color: rgba(255, 77, 109, 0.1); border: 1px solid #ff4d6d; color: #ff99ac; border-radius: 10px; }
.custom-alert-success { background-color: rgba(20, 203, 129, 0.1); border: 1px solid var(--green-accent); color: var(--green-accent); border-radius: 10px; }
.btn-guardar { background: linear-gradient(135deg, var(--green-accent, #14cb81) 0%, #10a66a 100%); color: #000; border: none; padding: 1rem; border-radius: 10px; font-weight: 700; font-size: 1.1rem; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; }
.btn-guardar:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(20, 203, 129, 0.4); }

.search-results-dropdown { position: absolute; top: 100%; left: 0; right: 0; z-index: 1000; background: var(--purple-dark, #2a1b3d); border: 1px solid var(--green-accent); border-radius: 8px; margin-top: 0.5rem; max-height: 350px; overflow-y: auto; }
.search-item { background: transparent; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--white-off); transition: background 0.2s; padding: 0.8rem 1rem; border-radius: 0; }
.search-item:hover { background: rgba(20, 203, 129, 0.1); color: var(--green-accent); }
.search-img { width: 40px; height: 55px; object-fit: cover; border-radius: 4px; }
.search-img-placeholder { width: 40px; height: 55px; background: rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; border-radius: 4px; color: #555; }
.nk-btn-primary { background: linear-gradient(135deg, var(--green-accent) 0%, #10a66a 100%); color: #000; font-weight: 700; border: none; border-radius: 8px; padding: 0.8rem 1.5rem; transition: all 0.3s ease; }
.nk-btn-primary:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(20, 203, 129, 0.4); color: #000; }
</style>