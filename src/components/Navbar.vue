<script setup>
import { ref, computed } from 'vue';
import { usuarioActual } from '../data/estado.js';
import { useRouter } from 'vue-router';
import { useCartStore } from '../stores/cart.js';

const router = useRouter();
const cartStore = useCartStore();

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

const irACheckout = () => {
  cerrarMenu();
  router.push('/checkout');
};

const cerrarSesion = () => {
  localStorage.removeItem('usuarioNexus');
  
  usuarioActual.value = null;
  
  cerrarMenu();

  router.push('/login');
};

</script>

<template>
  <nav class="navbar navbar-expand-lg sticky-top nk-navbar">
    <div class="container-fluid px-4">
        
        <router-link class="navbar-brand d-flex align-items-center" to="/" style="color: var(--white-off);" @click="cerrarMenu">
            <img src="https://nexuskey-media-imagenes.s3.us-east-2.amazonaws.com/img/logo.jpeg" alt="Logo" style="width: 60px; height: auto;" class="me-2">
            Nexus<span>Key</span>
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navegacion">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navegacion">
            <ul class="navbar-nav ms-auto align-items-center mb-2 mb-lg-0"> 
                
                <li class="nav-item">
                    <router-link class="nav-link d-flex align-items-center gap-2" style="color: var(--white-off);" to="/catalogo" @click="cerrarMenu">
                      <i class="bi bi-controller fs-5"></i> Catálogo
                    </router-link>
                </li>
                
                <li class="nav-item">
                    <a class="nav-link d-flex align-items-center gap-2" style="color: var(--white-off);" href="#redes" @click="cerrarMenu">
                      <i class="bi bi-people fs-5"></i> Redes Sociales
                    </a>
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

                <li class="nav-item ms-lg-2 mt-2 mt-lg-0 dropdown" v-if="usuarioActual && !usuarioActual.is_staff">
                    <a class="btn d-flex align-items-center gap-2 shadow-sm" 
                       href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside"
                       style="background-color: var(--green-accent); color: var(--purple-dark); border-radius: 50px; padding: 0.4rem 1.2rem; font-weight: 700; border: none; transition: all 0.2s ease;">
                        <i class="bi bi-cart-fill" style="font-size: 1.1rem;"></i>
                        <span>Carrito</span>
                        <span class="badge rounded-pill ms-1" style="background-color: var(--purple-dark); color: var(--white-off); font-size: 0.75rem; padding: 0.35em 0.6em;">
                            {{ cartStore.count }}
                        </span>
                    </a>
                    
                    <ul class="dropdown-menu dropdown-menu-end p-3 nk-dropdown" style="width: 320px;">
                        <li v-if="cartStore.count === 0">
                            <p class="text-center text-muted mb-0 my-3">🛒 Tu carrito está vacío</p>
                        </li>
                        <template v-else>
                            <li v-for="item in cartStore.items" :key="item.keyId" class="mb-3 d-flex justify-content-between align-items-center border-bottom pb-2" style="border-color: rgba(157, 113, 200, 0.2) !important;">
                                <div class="text-truncate flex-grow-1 pe-2">
                                    <h6 class="mb-1 text-white text-truncate" style="font-size: 0.95rem;">{{ item.productTitle }}</h6>
                                    <small style="color: var(--purple-soft);">{{ item.platform }} • {{ item.region }} <span class="text-success fw-bold ms-1">${{ item.price }}</span></small>
                                </div>
                                <button class="btn btn-sm text-danger border-0 flex-shrink-0 px-2" @click="cartStore.removeItem(item.keyId)">
                                    <i class="bi bi-x-lg"></i>
                                </button>
                            </li>
                            <li class="d-flex justify-content-between align-items-center mt-2 mb-3">
                                <span class="text-white fw-bold">Subtotal:</span>
                                <span class="text-success fw-bold fs-5">${{ cartStore.total.toFixed(2) }}</span>
                            </li>
                            <li>
                                <button class="btn w-100 fw-bold" style="background-color: var(--green-accent); color: #000;" @click="irACheckout">
                                    Pagar
                                </button>
                            </li>
                        </template>
                    </ul>
                </li>

                <li class="nav-item ms-lg-3 dropdown" v-if="usuarioActual">
                    <a class="nav-link dropdown-toggle text-white" href="#" data-bs-toggle="dropdown">
                        <i class="bi bi-person-circle me-1"></i> 
                        Hola, {{ usuarioActual.username }} </a>
                    <ul class="dropdown-menu dropdown-menu-end nk-dropdown py-2">
                        <li v-if="usuarioActual.is_staff">
                            <router-link class="dropdown-item" to="/panel">
                                <i class="bi bi-shield-lock me-2"></i>Panel Admin
                            </router-link>
                        </li>
                        <li v-if="usuarioActual.is_staff"><hr class="dropdown-divider" style="border-color: rgba(157, 113, 200, 0.2);"></li>
                        <li>
                            <a class="dropdown-item text-danger fw-bold" href="#" @click.prevent="cerrarSesion">
                                <i class="bi bi-box-arrow-right me-2"></i>Cerrar Sesión
                            </a>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
  </nav>
</template>

<style scoped>
.nk-navbar {
  background-color: rgba(26, 10, 46, 0.85) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(157, 113, 200, 0.2);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
  padding: 0.8rem 0;
  transition: all 0.3s ease;
}

.nav-link {
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: color 0.2s, transform 0.2s;
}

.nav-link:hover {
  color: var(--green-accent) !important;
  transform: translateY(-2px);
}

.navbar-brand span {
  color: var(--green-accent);
  font-weight: 800;
}

/* Estilos para Dropdowns (Usuario y Carrito) */
.nk-dropdown {
  background-color: rgba(26, 10, 46, 0.95) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(157, 113, 200, 0.3) !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7) !important;
  border-radius: 12px;
  margin-top: 10px !important;
}

.nk-dropdown .dropdown-item {
  color: var(--white-off);
  transition: all 0.2s;
  border-radius: 6px;
  margin: 2px 8px;
  width: auto;
  padding: 0.5rem 1rem;
}

.nk-dropdown .dropdown-item:hover {
  background-color: rgba(157, 113, 200, 0.15) !important;
  color: var(--green-accent) !important;
  transform: translateX(4px);
}

.nk-dropdown .dropdown-item.text-danger:hover {
  background-color: rgba(220, 53, 69, 0.15) !important;
  color: #ff6b6b !important;
}
</style>