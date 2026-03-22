<script setup>
import { ref, computed } from 'vue';

const form = ref({
  username: '',
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  passwordConfirm: '',
  terminos: false,
  novedades: false
});

const mostrarPassword = ref(false);
const mostrarConfirmPassword = ref(false);

const togglePassword = () => mostrarPassword.value = !mostrarPassword.value;
const toggleConfirmPassword = () => mostrarConfirmPassword.value = !mostrarConfirmPassword.value;

// Calculamos la fuerza de la contraseña (0 a 4)
const nivelSeguridad = computed(() => {
  let score = 0;
  const pw = form.value.password;
  if (pw.length >= 6) score++;
  if (pw.length >= 8) score++;
  if (/[A-Z]/.test(pw)) score++;
  if (/[0-9]/.test(pw) || /[^A-Za-z0-9]/.test(pw)) score++;
  return score;
});

const textoSeguridad = computed(() => {
  // Si el campo está vacío, no mostramos nada
  if (form.value.password.length === 0) return { texto: '', color: 'transparent' };
  
  switch (nivelSeguridad.value) {
    case 0: 
    case 1: return { texto: 'Débil', color: '#ff4d6d' }; 
    case 2: return { texto: 'Regular', color: '#ffd166' };
    case 3: return { texto: 'Fuerte', color: 'var(--green-accent)' };
    case 4: return { texto: 'Muy Fuerte', color: 'var(--green-accent)' };
    default: return { texto: '', color: 'transparent' };
  }
});

const registrarCuenta = () => {
  if (form.value.password !== form.value.passwordConfirm) {
    alert("Las contraseñas no coinciden. Intenta de nuevo.");
    return;
  }
  console.log('Enviando datos de registro:', form.value);
};
</script>

<template>
  <div class="login-wrapper">
    <div class="login-card" style="max-width: 480px;">

      <div class="text-center mb-1">
        <router-link to="/" class="login-brand text-decoration-none">
          Nexus<span>Key</span>
        </router-link>
      </div>
      <p class="login-subtitle text-center">Únete a la comunidad. Es gratis.</p>

      <p class="login-title text-center">Crear Cuenta</p>

      <form novalidate @submit.prevent="registrarCuenta">

        <div class="mb-3">
          <label class="login-label" for="username">Nombre de usuario</label>
          <div class="login-input-group">
            <input id="username" type="text" class="login-input" placeholder="Tu_Gamertag" autocomplete="username" v-model="form.username" required />
            <span class="login-input-icon" style="cursor:default;"><i class="bi bi-person"></i></span>
          </div>
        </div>

        <div class="row g-2 mb-3">
          <div class="col-6">
            <label class="login-label" for="firstName">Nombre</label>
            <input id="firstName" type="text" class="login-input" placeholder="Mario" autocomplete="given-name" v-model="form.firstName" />
          </div>
          <div class="col-6">
            <label class="login-label" for="lastName">Apellido</label>
            <input id="lastName" type="text" class="login-input" placeholder="Bros" autocomplete="family-name" v-model="form.lastName" />
          </div>
        </div>

        <div class="mb-3">
          <label class="login-label" for="email">Correo electrónico</label>
          <div class="login-input-group">
            <input id="email" type="email" class="login-input" placeholder="tu@correo.com" autocomplete="email" v-model="form.email" required />
            <span class="login-input-icon" style="cursor:default;"><i class="bi bi-envelope"></i></span>
          </div>
        </div>

        <div class="mb-3">
          <label class="login-label" for="password">Contraseña</label>
          <div class="login-input-group">
            <input id="password" :type="mostrarPassword ? 'text' : 'password'" class="login-input" placeholder="Mínimo 8 caracteres" autocomplete="new-password" v-model="form.password" required />
            <button type="button" class="login-input-icon" @click="togglePassword">
              <i :class="mostrarPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
          
          <div class="d-flex gap-1 mt-2">
            <div style="height:4px;flex:1;border-radius:2px; transition: 0.3s;" :style="{ background: nivelSeguridad >= 1 ? textoSeguridad.color : 'var(--purple-light)', opacity: nivelSeguridad >= 1 ? '1' : '.3' }"></div>
            <div style="height:4px;flex:1;border-radius:2px; transition: 0.3s;" :style="{ background: nivelSeguridad >= 2 ? textoSeguridad.color : 'var(--purple-light)', opacity: nivelSeguridad >= 2 ? '1' : '.3' }"></div>
            <div style="height:4px;flex:1;border-radius:2px; transition: 0.3s;" :style="{ background: nivelSeguridad >= 3 ? textoSeguridad.color : 'var(--purple-light)', opacity: nivelSeguridad >= 3 ? '1' : '.3' }"></div>
            <div style="height:4px;flex:1;border-radius:2px; transition: 0.3s;" :style="{ background: nivelSeguridad >= 4 ? textoSeguridad.color : 'var(--purple-light)', opacity: nivelSeguridad >= 4 ? '1' : '.3' }"></div>
          </div>
          
          <div class="d-flex justify-content-between align-items-center mt-1">
            <span style="font-size:.75rem; font-weight: 700; transition: color 0.3s;" :style="{ color: textoSeguridad.color }">
              {{ textoSeguridad.texto }}
            </span>
            <span style="font-size:.72rem; color:var(--purple-soft);">
              Usa letras, números y símbolos.
            </span>
          </div>
        </div>

        <div class="mb-3">
          <label class="login-label" for="passwordConfirm">Confirmar contraseña</label>
          <div class="login-input-group">
            <input id="passwordConfirm" :type="mostrarConfirmPassword ? 'text' : 'password'" class="login-input" placeholder="Repite tu contraseña" autocomplete="new-password" v-model="form.passwordConfirm" required />
            <button type="button" class="login-input-icon" @click="toggleConfirmPassword">
              <i :class="mostrarConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
        </div>

        <div class="d-flex flex-column gap-2 mb-4">
          <label class="login-check">
            <input type="checkbox" v-model="form.terminos" required />
            Acepto los <router-link to="/terminos" class="login-link ms-1" style="color:var(--green-accent);">Términos y Condiciones</router-link>
          </label>
          <label class="login-check">
            <input type="checkbox" v-model="form.novedades" />
            Quiero recibir ofertas y novedades por correo
          </label>
        </div>

        <button type="submit" class="btn-login">
          <i class="bi bi-person-plus me-2"></i>Crear mi cuenta
        </button>

      </form>

      <div class="login-divider">o regístrate con</div>

      <div class="d-flex flex-column gap-2">
        <a href="#" class="btn-social">
          <i class="bi bi-google"></i> Google
        </a>
      </div>

      <p class="login-footer-text mt-4">
        ¿Ya tienes cuenta? <router-link to="/login" class="login-link fw-bold">Inicia sesión</router-link>
      </p>

    </div>
  </div>
</template>

<style scoped>
@import url('https://cdn.jsdelivr.net/gh/Os-corona/prograWeb-CSS-Auxiliar@main/styles-log-in.css');

.login-wrapper {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}
</style>