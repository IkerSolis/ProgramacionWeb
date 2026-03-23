<script setup>
import { ref } from 'vue';
import { usuarioActual } from '../data/estado.js';
import { useRouter } from 'vue-router';

const cantidadCarrito = ref(0);
const router = useRouter();

const cerrarMenu = () => {
  const menu = document.getElementById('navegacion');
  // Bootstrap le agrega la clase 'show' cuando el menú está desplegado
  if (menu && menu.classList.contains('show')) {
    // Usamos el objeto global de Bootstrap para cerrarlo con su animación nativa
    const bsCollapse = window.bootstrap.Collapse.getInstance(menu);
    if (bsCollapse) {
      bsCollapse.hide();
    }
  }
};

const cerrarSesion = () => {
  localStorage.removeItem('usuarioNexus');
  
  usuarioActual.value = null;
  
  cerrarMenu();

  router.push('/login');
};

</script>

<template>
  <nav class="navbar navbar-expand-lg sticky-top" style="background-color: var(--purple-mid);">
    <div class="container-fluid">
        
        <router-link class="navbar-brand d-flex align-items-center" to="/" style="color: var(--white-off);" @click="cerrarMenu">
            <img src="/img/logo.jpeg" alt="Logo" style="width: 60px; height: auto;" class="me-2">
            Nexus<span>Key</span>
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navegacion">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navegacion">
            <ul class="navbar-nav ms-auto align-items-center mb-2 mb-lg-0"> 
                
                <li class="nav-item">
                    <router-link class="nav-link" style="color: var(--white-off);" to="/catalogo" @click="cerrarMenu">Catálogo</router-link>
                </li>
                
                <li class="nav-item">
                    <a class="nav-link" style="color: var(--white-off);" href="#redes" @click="cerrarMenu">Redes Sociales</a>
                </li>
                
                <li class="nav-item ms-lg-3" v-if="!usuarioActual">
                    <router-link class="btn btn-outline-light d-flex align-items-center gap-2" 
                       to="/login" 
                       style="border-radius: 50px; padding: 0.4rem 1.2rem; border-color: var(--white-off); color: var(--white-off);"
                       @click="cerrarMenu">
                        <i class="bi bi-person-circle" style="font-size: 1.1rem;"></i>
                        <span>Iniciar Sesión</span>
                    </router-link>
                </li>

                <li class="nav-item ms-lg-2 mt-2 mt-lg-0" v-if="usuarioActual?.role === 'user'">
                    <router-link class="btn d-flex align-items-center gap-2 shadow-sm" 
                       to="/carrito" 
                       style="background-color: var(--green-accent); color: var(--purple-dark); border-radius: 50px; padding: 0.4rem 1.2rem; font-weight: 700; border: none; transition: all 0.2s ease;"
                       @click="cerrarMenu">
                        <i class="bi bi-cart-fill" style="font-size: 1.1rem;"></i>
                        <span>Carrito</span>
                        <span class="badge rounded-pill ms-1" style="background-color: var(--purple-dark); color: var(--white-off); font-size: 0.75rem; padding: 0.35em 0.6em;">
                            {{ cantidadCarrito || 0 }}
                        </span>
                    </router-link>
                </li>

                <li class="nav-item ms-lg-3 dropdown" v-if="usuarioActual">
                    <a class="nav-link dropdown-toggle text-white" href="#" data-bs-toggle="dropdown">
                        <i class="bi bi-person-circle me-1"></i> 
                        Hola, {{ usuarioActual.username }} </a>
                    <ul class="dropdown-menu dropdown-menu-end" style="background-color: var(--purple-mid);">
                        <li v-if="usuarioActual.role === 'admin'">
                        <router-link class="dropdown-item text-white" to="/panel">Panel Admin</router-link>
                        </li>
                        <li><hr class="dropdown-divider" style="border-color: var(--purple-light);"></li>
                        <li><a class="dropdown-item text-danger" href="#" @click.prevent="cerrarSesion">Cerrar Sesión</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
  </nav>
</template>

<style scoped>

</style>