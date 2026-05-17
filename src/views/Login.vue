<script setup>
import { API_BASE_URL } from '../api/config.js';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { usuarioActual, tokenActual } from '../data/estado.js';

// Variables reactivas para el formulario
const email = ref('');
const password = ref('');
const rememberMe = ref(false);
const errorMsg = ref('');

const router = useRouter();

// Variable y función para mostrar/ocultar la contraseña
const mostrarPassword = ref(false);
const togglePassword = () => {
  mostrarPassword.value = !mostrarPassword.value;
};

// Función que se ejecutará al enviar el formulario
const iniciarSesion = async () => {
  errorMsg.value = '';
  try {
    const res = await fetch(`${API_BASE_URL}/api/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: email.value,
        password: password.value,
        remember_me: rememberMe.value
      })
    });

    if (res.ok) {
      const data = await res.json();
      
      // Limpiar ambas fuentes de almacenamiento primero por seguridad
      localStorage.removeItem('tokenNexus');
      localStorage.removeItem('usuarioNexus');
      sessionStorage.removeItem('tokenNexus');
      sessionStorage.removeItem('usuarioNexus');

      const usuarioEncontrado = {
        id: data.id,
        username: data.username,
        email: data.email,
        role: data.is_staff ? 'admin' : 'user',
        is_staff: data.is_staff
      };

      // Guardar token y datos según el check de "Recuérdame"
      const storage = rememberMe.value ? localStorage : sessionStorage;
      storage.setItem('tokenNexus', data.token);
      storage.setItem('usuarioNexus', JSON.stringify(usuarioEncontrado));
      
      tokenActual.value = data.token;
      usuarioActual.value = usuarioEncontrado;
      
      if (usuarioEncontrado.role === 'admin') {
        router.push('/panel');
      } else {
        router.push('/');
      }
    } else {
      errorMsg.value = "Credenciales incorrectas.";
    }
  } catch (error) {
    console.error("Error conectando con la API:", error);
    errorMsg.value = "Error de conexión con el servidor.";
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

        <div v-if="errorMsg" class="alert alert-danger" role="alert" style="font-size: 0.9rem; padding: 0.5rem;">
          {{ errorMsg }}
        </div>

        <div class="mb-3">
          <label class="login-label" for="email">Usuario o Correo</label>
          <input
            id="email"
            type="text"
            class="login-input"
            placeholder="Tu usuario o correo"
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
            <input type="checkbox" v-model="rememberMe"/> Recuérdame
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