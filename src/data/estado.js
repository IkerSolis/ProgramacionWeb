
import { ref } from 'vue';

const datosGuardados = localStorage.getItem('usuarioNexus');

export const usuarioActual = ref(datosGuardados ? JSON.parse(datosGuardados) : null);