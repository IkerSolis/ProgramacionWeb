<script setup>
import { API_BASE_URL } from '../api/config.js';
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authHeader } from '../data/estado.js';

const route = useRoute()
const router = useRouter()
const productId = route.params.id

const juego = ref({
  title: '',
  description: 'Descripción pendiente',
  genre: 'Por definir',
  cover: ''
})

const keys = ref([])
const keysToDelete = ref([])

const plataformasDisponibles = ['PC', 'PlayStation', 'Xbox', 'Nintendo']
const regionesDisponibles = ['Global', 'MX', 'US', 'EU', 'Asia']

const cargarDatos = async () => {
  try {
    const resProd = await fetch(`${API_BASE_URL}/api/products/${productId}/`)
    if (resProd.ok) {
      const data = await resProd.json()
      juego.value = {
        title: data.title,
        description: data.description,
        genre: data.genre,
        cover: data.cover || data.image_url || ''
      }
    }

    const resKeys = await fetch(`${API_BASE_URL}/api/keycodes/?product=${productId}`, {
      headers: { ...authHeader() }
    })
    if (resKeys.ok) {
      keys.value = await resKeys.json()
      // Marcar llaves existentes como no nuevas
      keys.value.forEach(k => k.isNew = false)
    }
  } catch (error) {
    console.error("Error al cargar datos:", error)
    errores.value.push("No se pudieron cargar los datos del producto.")
  }
}

onMounted(() => {
  cargarDatos()
})

const addKey = () => {
  keys.value.push({ key: '', platform: 'PC', region: 'Global', price: 0, isNew: true })
}

const removeKey = (index) => {
  const removed = keys.value.splice(index, 1)[0]
  if (removed.id) {
    keysToDelete.value.push(removed.id)
  }
}

const errores = ref([])
const exito = ref(false)

const validarFormulario = () => {
  errores.value = []
  exito.value = false

  if (!juego.value.title) errores.value.push("El título es obligatorio")
  if (!juego.value.cover) errores.value.push("La imagen es obligatoria")
  
  keys.value.forEach((k, idx) => {
    if (!k.key && k.isNew) errores.value.push(`La nueva llave #${idx + 1} no puede estar vacía.`)
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
    cover: juego.value.cover
  };

  try {
    const resProduct = await fetch(`${API_BASE_URL}/api/products/${productId}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...authHeader()
      },
      body: JSON.stringify(productPayload)
    });

    if (resProduct.ok) {
      for (const id of keysToDelete.value) {
        await fetch(`${API_BASE_URL}/api/keycodes/${id}/`, {
          method: 'DELETE',
          headers: { ...authHeader() }
        });
      }
      keysToDelete.value = []

      for (const k of keys.value) {
        if (k.id) {
          await fetch(`${API_BASE_URL}/api/keycodes/${k.id}/`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              ...authHeader()
            },
            body: JSON.stringify({ platform: k.platform, region: k.region, price: k.price, key: k.key })
          });
        } else {
          const keyPayload = {
            product: productId,
            key: k.key,
            platform: k.platform,
            region: k.region,
            price: k.price,
            is_used: false
          };
          await fetch(`${API_BASE_URL}/api/keycodes/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              ...authHeader()
            },
            body: JSON.stringify(keyPayload)
          });
        }
      }

      exito.value = true;
      setTimeout(() => {
        exito.value = false;
        router.push('/panel');
      }, 2000);
    } else {
      errores.value.push("Error del servidor al actualizar producto.");
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
        <i class="bi bi-pencil-square fs-1 mb-2 d-block" style="color: var(--green-accent);"></i>
        <h2 class="mb-0 text-white">Editar <span style="color: var(--green-accent);">Videojuego</span></h2>
        <p style="color: var(--purple-soft); font-size: 0.9rem;">Actualiza la información y gestiona los códigos</p>
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
        <i class="bi bi-check-circle-fill me-2"></i> ¡Juego y llaves actualizados con éxito!
      </div>

      <form @submit.prevent="guardarJuego" novalidate>

        <h5 class="section-subtitle mb-3"><i class="bi bi-info-circle me-2"></i>Información del Producto</h5>
        
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
          <button type="button" class="btn-close-key" @click="removeKey(index)" title="Eliminar llave">
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
          <i class="bi bi-cloud-arrow-up-fill me-2"></i> Guardar Cambios
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
</style>
