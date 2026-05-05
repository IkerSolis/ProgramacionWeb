import { ref } from 'vue';

const datosGuardados = localStorage.getItem('usuarioNexus') || sessionStorage.getItem('usuarioNexus');
const tokenGuardado = localStorage.getItem('tokenNexus') || sessionStorage.getItem('tokenNexus');

export const usuarioActual = ref(datosGuardados ? JSON.parse(datosGuardados) : null);
export const tokenActual = ref(tokenGuardado || null);

export const authHeader = () => {
    if (tokenActual.value) {
        return { 'Authorization': `Bearer ${tokenActual.value}` };
    }
    return {};
};