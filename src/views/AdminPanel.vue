<script setup>
// Por ahora mantenemos la lógica primitiva, solo con un par de funciones
// de prueba para que veas que los botones responden en la consola.
const editarProducto = () => {
  console.log('Iniciando flujo para editar producto...');
};

const eliminarProducto = () => {
  console.log('Iniciando flujo para eliminar producto...');
};
</script>

<template>
  <div>
    <section class="home-top">
      <div class="container">
        <div class="row align-items-center g-5">
          <div class="col-lg-6">
            <p class="text-uppercase mb-2" style="font-size:.75rem;letter-spacing:.15em;color:var(--green-accent);font-weight:600;">
              Gestión de Inventario
            </p>
            <h1 class="home-top-title mb-3">
              Panel<br><span class="accent">de administración</span>
            </h1>
            <p class="home-top-subtitle mb-4">
              Administra los productos del catálogo: crea nuevos registros, edita información existente o elimina productos.
            </p>
            
            <div class="admin-actions d-flex flex-wrap gap-3 mt-4">
              <router-link to="/add-product" class="btn nk-btn nk-add">
                <i class="bi bi-plus-circle me-2"></i>Añadir producto
              </router-link>
              
              <button class="btn nk-btn nk-edit" @click="editarProducto">
                <i class="bi bi-pencil-square me-2"></i>Editar producto
              </button>

              <button class="btn nk-btn nk-delete" @click="eliminarProducto">
                <i class="bi bi-trash me-2"></i>Eliminar producto
              </button>
            </div>
            
          </div>    
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>

</style>