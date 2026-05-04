<script setup>
import { ref } from 'vue'

const juego = ref({
  title: '',
  description: 'Descripción pendiente',
  genre: 'Por definir',
  plataformas: [],
  cover: '',
  precioOriginal: '',
  precioFinal: '',
  descuento: 0
})

const errores = ref([])
const exito = ref(false)

const validarFormulario = () => {
  errores.value = []
  exito.value = false

  if (!juego.value.title) errores.value.push("El título es obligatorio")
  if (juego.value.plataformas.length === 0) errores.value.push("Debes seleccionar al menos una plataforma")
  if (!juego.value.cover) errores.value.push("La imagen es obligatoria")
  if (juego.value.precioOriginal === '') errores.value.push("El precio original es obligatorio")
  if (juego.value.precioFinal === '') errores.value.push("El precio final es obligatorio")
  if (juego.value.precioOriginal < 0) errores.value.push("El precio original no puede ser negativo")
  if (juego.value.precioFinal < 0) errores.value.push("El precio final no puede ser negativo")

  if (Number(juego.value.precioFinal) < Number(juego.value.precioOriginal)) {
    errores.value.push("El precio final no puede ser menor al precio original")
  }

  return errores.value.length === 0
}

const guardarJuego = async () => {
  if (!validarFormulario()) return

  const payload = {
    title: juego.value.title,
    description: juego.value.description,
    genre: juego.value.genre,
    cover: juego.value.cover
  };

  try {
    const response = await fetch('http://127.0.0.1:8000/api/products/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      exito.value = true; // Mostramos el mensaje de éxito

      // Limpiar formulario
      juego.value = {
        title: '', description: 'Descripción pendiente', genre: 'Por definir', plataformas: [], cover: '',
        precioOriginal: '', precioFinal: '', descuento: 0
      };
      
      // Ocultamos el mensaje de éxito después de 3 segundos
      setTimeout(() => exito.value = false, 3000);
    } else {
      const errorData = await response.json();
      console.error("Error al guardar:", errorData);
      errores.value.push("Error del servidor: Revisa la consola.");
    }
  } catch (error) {
    console.error("Error de red:", error);
    errores.value.push("No se pudo conectar con el backend (Django).");
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
        <p style="color: var(--purple-soft); font-size: 0.9rem;">Registra un nuevo producto en la base de datos de NexusKey</p>
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
        <i class="bi bi-check-circle-fill me-2"></i> ¡Juego guardado en la base de datos con éxito!
      </div>

      <form @submit.prevent="guardarJuego" novalidate>

        <div class="mb-4">
          <label class="admin-label">Título del juego</label>
          <div class="admin-input-group">
            <span class="admin-icon"><i class="bi bi-controller"></i></span>
            <input v-model="juego.title" type="text" class="admin-input" placeholder="Ej: Halo Infinite" required>
          </div>
        </div>

        <div class="mb-4">
          <label class="admin-label d-block mb-2">Plataformas disponibles</label>
          <div class="d-flex flex-wrap gap-3">
            <label class="platform-checkbox">
              <input v-model="juego.plataformas" type="checkbox" value="Steam">
              <span class="platform-btn"><i class="bi bi-steam me-2"></i>Steam</span>
            </label>
            <label class="platform-checkbox">
              <input v-model="juego.plataformas" type="checkbox" value="PlayStation">
              <span class="platform-btn"><i class="bi bi-playstation me-2"></i>PlayStation</span>
            </label>
            <label class="platform-checkbox">
              <input v-model="juego.plataformas" type="checkbox" value="Xbox">
              <span class="platform-btn"><i class="bi bi-xbox me-2"></i>Xbox</span>
            </label>
          </div>
        </div>

        <div class="mb-4">
          <label class="admin-label">URL de la imagen (Portada)</label>
          <div class="admin-input-group">
            <span class="admin-icon"><i class="bi bi-image"></i></span>
            <input v-model="juego.cover" type="text" class="admin-input" placeholder="/img/mi-juego.jpg" required>
          </div>
        </div>

        <div class="row g-3 mb-4">
          <div class="col-md-4">
            <label class="admin-label">Precio Original</label>
            <div class="admin-input-group">
              <span class="admin-icon"><i class="bi bi-currency-dollar"></i></span>
              <input v-model="juego.precioOriginal" type="number" step="0.01" class="admin-input" placeholder="0.00" required>
            </div>
          </div>
          <div class="col-md-4">
            <label class="admin-label">Precio Final</label>
            <div class="admin-input-group">
              <span class="admin-icon" style="color: var(--green-accent);"><i class="bi bi-tag-fill"></i></span>
              <input v-model="juego.precioFinal" type="number" step="0.01" class="admin-input" placeholder="0.00" required>
            </div>
          </div>
          <div class="col-md-4">
            <label class="admin-label">Descuento (%)</label>
            <div class="admin-input-group">
              <span class="admin-icon"><i class="bi bi-percent"></i></span>
              <input v-model="juego.descuento" type="number" class="admin-input" placeholder="0">
            </div>
          </div>
        </div>

        <button type="submit" class="btn-guardar w-100 mt-2">
          <i class="bi bi-cloud-arrow-up-fill me-2"></i> Guardar en Catálogo
        </button>

      </form>
    </div>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 700px;
}

.back-link {
  color: var(--purple-soft);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--green-accent);
}

.admin-card {
  background-color: var(--card-bg);
  border: 1px solid var(--purple-mid);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

/* Estilos de Inputs (Similares al Login) */
.admin-label {
  color: var(--white-off);
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.admin-input-group {
  display: flex;
  background-color: var(--purple-dark);
  border: 1px solid var(--purple-mid);
  border-radius: 10px;
  overflow: hidden;
  transition: border-color 0.3s ease;
}

.admin-input-group:focus-within {
  border-color: var(--green-accent);
  box-shadow: 0 0 0 2px rgba(127, 255, 110, 0.2);
}

.admin-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 1rem;
  color: var(--purple-soft);
  background-color: rgba(0, 0, 0, 0.2);
}

.admin-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--white-off);
  padding: 0.8rem;
  outline: none;
}

.admin-input::placeholder {
  color: rgba(157, 113, 200, 0.4);
}

/* Estilo para los Checkboxes de Plataformas como "Botones" */
.platform-checkbox input[type="checkbox"] {
  display: none;
}

.platform-btn {
  display: inline-block;
  padding: 0.5rem 1.2rem;
  border-radius: 50px;
  background-color: var(--purple-dark);
  border: 1px solid var(--purple-mid);
  color: var(--purple-soft);
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.9rem;
}

.platform-checkbox input[type="checkbox"]:checked + .platform-btn {
  background-color: var(--green-dim);
  border-color: var(--green-accent);
  color: var(--purple-dark);
  box-shadow: 0 0 15px rgba(127, 255, 110, 0.3);
}

/* Alertas Personalizadas */
.custom-alert {
  background-color: rgba(255, 77, 109, 0.1);
  border: 1px solid #ff4d6d;
  color: #ff99ac;
  border-radius: 10px;
}

.custom-alert-success {
  background-color: rgba(127, 255, 110, 0.1);
  border: 1px solid var(--green-accent);
  color: var(--green-accent);
  border-radius: 10px;
}

/* Botón Principal */
.btn-guardar {
  background: linear-gradient(135deg, var(--green-accent) 0%, var(--green-dim) 100%);
  color: var(--purple-dark);
  border: none;
  padding: 1rem;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-guardar:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(127, 255, 110, 0.4);
}
</style>