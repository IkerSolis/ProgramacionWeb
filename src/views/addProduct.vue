<script setup>
import { ref } from 'vue'

const juego = ref({
  titulo: '',
  plataformas: [],
  imagen: '',
  precioOriginal: '',
  precioFinal: '',
  descuento: 0
})

const guardarJuego = () => {
  if (!validarFormulario()) {
    return
  }
  // Obtener juegos existentes (SOLO UNA VEZ)
  const juegos = JSON.parse(localStorage.getItem('juegos')) || []

  const juegosBase = [
    { id: 1 },
    { id: 2 },
    { id: 3 },
    { id: 4 }
  ]

  // Obtener todos los IDs
  const todosLosIds = [
    ...juegosBase.map(j => j.id),
    ...juegos.map(j => j.id)
  ]

  const maxId = todosLosIds.length > 0 ? Math.max(...todosLosIds) : 0
  const nuevoId = maxId + 1

  // Guardar juego
  juegos.push({
    ...juego.value,
    id: nuevoId
  })

  localStorage.setItem('juegos', JSON.stringify(juegos))

  console.log('Juego guardado:', juego.value)

  // Limpiar formulario
  juego.value = {
    titulo: '',
    plataformas: [],
    imagen: '',
    precioOriginal: '',
    precioFinal: '',
    descuento: 0
  }
}

  const errores = ref([])

  const validarFormulario = () => {
  errores.value = []

  if (!juego.value.titulo) {
    errores.value.push("El título es obligatorio")
  }

  if (juego.value.plataformas.length === 0) {
    errores.value.push("Debes seleccionar al menos una plataforma")
  }

  if (!juego.value.imagen) {
    errores.value.push("La imagen es obligatoria")
  }

  if (juego.value.precioOriginal === '') {
    errores.value.push("El precio original es obligatorio")
  }

  if (juego.value.precioFinal === '') {
    errores.value.push("El precio final es obligatorio")
  }

  if (juego.value.precioOriginal < 0) {
    errores.value.push("El precio original no puede ser menor a 0")
  }

  if (juego.value.precioFinal < 0) {
    errores.value.push("El precio final no puede ser menor a 0")
  }

  if (Number(juego.value.precioFinal) < Number(juego.value.precioOriginal)) {
    errores.value.push("El precio final no puede ser menor al precio original")
  }

  return errores.value.length === 0
}

</script>

<template>
  <div class="container py-5">
    <h2 class="mb-4">Añadir videojuego</h2>

    <div v-if="errores.length" class="alert alert-danger">
      <ul class="mb-0">
        <li v-for="(error, index) in errores" :key="index">
          {{ error }}
        </li>
      </ul>
    </div>

    <form @submit.prevent="guardarJuego">

      <div class="mb-3">
        <label class="form-label">Título del juego</label>
        <input v-model="juego.titulo" type="text" class="form-control" required>
      </div>

      <div class="mb-3">
        <label class="form-label">Plataformas</label>

        <div class="form-check">
          <input v-model="juego.plataformas" type="checkbox" value="PC" class="form-check-input">
          <label class="form-check-label">Steam</label>
        </div>

        <div class="form-check">
          <input v-model="juego.plataformas" type="checkbox" value="PlayStation" class="form-check-input">
          <label class="form-check-label">PlayStation</label>
        </div>

        <div class="form-check">
          <input v-model="juego.plataformas" type="checkbox" value="Xbox" class="form-check-input">
          <label class="form-check-label">Xbox</label>
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">URL de la imagen</label>
        <input v-model="juego.imagen" type="text" class="form-control">
      </div>

      <div class="mb-3">
        <label class="form-label">Precio original</label>
        <input v-model="juego.precioOriginal" type="number" class="form-control">
      </div>

      <div class="mb-3">
        <label class="form-label">Precio final</label>
        <input v-model="juego.precioFinal" type="number" class="form-control">
      </div>

      <div class="mb-3">
        <label class="form-check-label">Descuento</label>
        <input v-model="juego.descuento" type="number" class="form-control">
      </div>

      <button type="submit" class="btn btn-success">
        Guardar videojuego
      </button>
    </form>

  </div>
</template>