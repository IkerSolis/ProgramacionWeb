import { ref } from 'vue';

const datosGuardados = localStorage.getItem('usuarioNexus');
const tokenGuardado = localStorage.getItem('tokenNexus');

export const usuarioActual = ref(datosGuardados ? JSON.parse(datosGuardados) : null);
export const tokenActual = ref(tokenGuardado || null);

export const authHeader = () => {
    if (tokenActual.value) {
        return { 'Authorization': `Token ${tokenActual.value}` };
    }
    return {};
};