<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { cuentasPrueba } from '../data/users.js';
import { usuarioActual } from '../data/estado.js';

// Variables reactivas para el formulario
const email = ref('');
const password = ref('');

const router = useRouter();

// Variable y función para mostrar/ocultar la contraseña
const mostrarPassword = ref(false);
const togglePassword = () => {
  mostrarPassword.value = !mostrarPassword.value;
};

// Función que se ejecutará al enviar el formulario
const iniciarSesion = () => {
  // Buscamos si existe un usuario con ese correo y contraseña
  const usuarioEncontrado = cuentasPrueba.find(u => 
    u.email === email.value && u.password === password.value
  );

  if (usuarioEncontrado) {
    localStorage.setItem('usuarioNexus', JSON.stringify(usuarioEncontrado));
    
    usuarioActual.value = usuarioEncontrado;
    
    if (usuarioActual.value.role === 'admin') {
      router.push('/panel');
    } else {
      router.push('/');
    }
  } else {
    alert("Credenciales incorrectas.");
  }
};
</script>

<template>
  <div class="login-wrapper">
    <div class="login-card">

      <div class="text-center mb-1">
        <router-link to="/" class="login-brand text-decoration-none">
          Nexus<span>Key</span>
        </router-link>
      </div>
      <p class="login-subtitle text-center">Bienvenido de vuelta, jugador</p>

      <p class="login-title text-center">Iniciar Sesión</p>

      <form novalidate @submit.prevent="iniciarSesion">

        <div class="mb-3">
          <label class="login-label" for="email">Correo electrónico</label>
          <input
            id="email"
            type="email"
            class="login-input"
            placeholder="tu@correo.com"
            autocomplete="email"
            v-model="email"
          />
        </div>

        <div class="mb-3">
          <label class="login-label" for="password">Contraseña</label>
          <div class="login-input-group">
            <input
              id="password"
              :type="mostrarPassword ? 'text' : 'password'"
              class="login-input"
              placeholder="••••••••"
              autocomplete="current-password"
              v-model="password"
            />
            <button type="button" class="login-input-icon" @click="togglePassword" aria-label="Mostrar contraseña">
              <i :class="mostrarPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-4">
          <label class="login-check">
            <input type="checkbox"/> Recuérdame
          </label>
          <a href="#" class="login-link">¿Olvidaste tu contraseña?</a>
        </div>

        <button type="submit" class="btn-login">
          <i class="bi bi-controller me-2"></i>Entrar
        </button>

      </form>

      <div class="login-divider">o continúa con</div>

      <div class="d-flex flex-column gap-2">
        <a href="#" class="btn-social">
          <i class="bi bi-google"></i> Google
        </a>
      </div>

      <p class="login-footer-text mt-4 text-center">
        ¿Aún no tienes cuenta? 
        <router-link to="/registro" class="login-link fw-bold">Regístrate gratis</router-link>
      </p>

    </div>
  </div>
</template>

<style scoped>
/* CSS AUXILIAR */
@import url('https://cdn.jsdelivr.net/gh/Os-corona/prograWeb-CSS-Auxiliar@main/styles-log-in.css');

.login-wrapper {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>