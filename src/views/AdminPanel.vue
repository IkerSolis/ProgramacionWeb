<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { usuarioActual, authHeader } from '../data/estado.js';

const usuarios = ref([]);
const productos = ref([]);
const keycodes = ref([]);
const errorMsg = ref('');
const router = useRouter();

// Paginación
const currentPage = ref(1);
const itemsPerPage = 10;

const totalPages = computed(() => Math.ceil(productos.value.length / itemsPerPage));

const paginatedProductos = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return productos.value.slice(start, end);
});

const cargarDatos = async () => {
  try {
    // Cargar Usuarios
    const resUsers = await fetch('http://localhost:8000/api/users/', {
      headers: { ...authHeader() }
    });
    if (resUsers.ok) usuarios.value = await resUsers.json();

    // Cargar Productos
    const resProd = await fetch('http://localhost:8000/api/products/');
    if (resProd.ok) productos.value = await resProd.json();

    // Cargar KeyCodes
    const resKeys = await fetch('http://localhost:8000/api/keycodes/');
    if (resKeys.ok) keycodes.value = await resKeys.json();

  } catch (err) {
    errorMsg.value = "Error de conexión al cargar datos.";
  }
};

const getKeysByProduct = (productId) => {
  return keycodes.value.filter(k => k.product === productId);
};

const eliminarUsuario = async (id) => {
  if (usuarioActual.value && usuarioActual.value.id === id) {
    alert("No puedes eliminar tu propia cuenta desde aquí.");
    return;
  }
  if(!confirm("¿Estás seguro de eliminar este usuario?")) return;
  try {
    const res = await fetch(`http://localhost:8000/api/users/${id}/`, {
      method: 'DELETE',
      headers: { ...authHeader() }
    });
    if (res.ok) {
      cargarDatos();
    } else {
      alert("Error al eliminar usuario.");
    }
  } catch (err) {
    alert("Error de conexión.");
  }
};

const hacerAdmin = async (id, isStaffActual) => {
  if (usuarioActual.value && usuarioActual.value.id === id) {
    alert("No puedes cambiar tu propio rol.");
    return;
  }
  try {
    const res = await fetch(`http://localhost:8000/api/users/${id}/`, {
      method: 'PATCH',
      headers: { 
        'Content-Type': 'application/json',
        ...authHeader() 
      },
      body: JSON.stringify({ is_staff: !isStaffActual })
    });
    if (res.ok) {
      cargarDatos();
    } else {
      alert("Error al actualizar usuario.");
    }
  } catch (err) {
    alert("Error de conexión.");
  }
};

// Acciones reales de Productos
const editarProducto = (id) => {
  router.push(`/edit-product/${id}`);
};

const eliminarProducto = async (id) => {
  if(!confirm("¿Estás seguro de eliminar este producto y todas sus llaves?")) return;
  try {
    const res = await fetch(`http://localhost:8000/api/products/${id}/`, {
      method: 'DELETE',
      headers: { ...authHeader() }
    });
    if (res.ok) {
      cargarDatos();
    } else {
      alert("Error al eliminar el producto.");
    }
  } catch(err) {
    alert("Error de conexión.");
  }
};

const eliminarClave = async (id) => {
  if(!confirm("¿Estás seguro de eliminar esta llave?")) return;
  try {
    const res = await fetch(`http://localhost:8000/api/keycodes/${id}/`, {
      method: 'DELETE',
      headers: { ...authHeader() }
    });
    if (res.ok) {
      cargarDatos();
    } else {
      alert("Error al eliminar la llave.");
    }
  } catch(err) {
    alert("Error de conexión.");
  }
};

const añadirClave = (productId) => {
  // Redirigimos al modo de edición para añadir la llave
  router.push(`/edit-product/${productId}`);
};

onMounted(() => {
  cargarDatos();
});
</script>

<template>
  <div>
    <section class="home-top">
      <div class="container d-flex justify-content-between align-items-center py-4">
        <div>
          <p class="text-uppercase mb-2" style="font-size:.75rem;letter-spacing:.15em;color:var(--green-accent);font-weight:600;">
            Gestión General
          </p>
          <h1 class="home-top-title mb-0" style="font-size: 2.5rem;">
            Panel <span class="accent">Administrativo</span>
          </h1>
        </div>
        <div>
          <router-link to="/add-product" class="btn nk-btn-primary btn-lg shadow-sm">
            <i class="bi bi-plus-circle-fill me-2"></i>Registrar Nuevo Producto
          </router-link>
        </div>
      </div>
    </section>

    <!-- Gestión de Productos y Claves -->
    <section class="container py-4">
      <h2 class="mb-4 section-title"><i class="bi bi-box-seam me-2"></i> Catálogo y Claves</h2>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>

      <div class="product-list">
        <!-- Tarjeta por cada producto (ahora más compacta y paginada) -->
        <div v-for="product in paginatedProductos" :key="product.id" class="product-card mb-3">
          <!-- Cabecera del Producto -->
          <div class="product-header d-flex justify-content-between align-items-center flex-wrap gap-3">
            <div class="d-flex align-items-center gap-3">
              <div class="product-img-wrapper">
                <img :src="product.cover || product.image_url || 'https://via.placeholder.com/60x80/2a1b3d/9d71c8?text=NK'" class="product-img" alt="cover">
              </div>
              <div>
                <h4 class="product-title mb-1">{{ product.title }}</h4>
                <div class="d-flex gap-2 align-items-center">
                  <span class="badge" :class="product.is_available ? 'nk-badge-success' : 'nk-badge-danger'">
                    {{ product.is_available ? 'Activo en Tienda' : 'Inactivo' }}
                  </span>
                  <small class="text-muted">{{ product.genre }}</small>
                </div>
              </div>
            </div>
            <div class="product-actions d-flex gap-2">
              <button class="btn btn-sm nk-btn-outline" @click="editarProducto(product.id)">
                <i class="bi bi-pencil-square"></i> Editar
              </button>
              <button class="btn btn-sm nk-btn-delete-outline" @click="eliminarProducto(product.id)">
                <i class="bi bi-trash"></i> Eliminar
              </button>
            </div>
          </div>
          
          <!-- Lista de Claves del Producto -->
          <div class="keys-section mt-4">
            <h6 class="keys-title mb-3"><i class="bi bi-key-fill me-2"></i>Claves Asociadas</h6>
            <div class="table-responsive nk-table-container-sm">
              <table class="table nk-table-sm align-middle mb-0">
                <thead>
                  <tr>
                    <th>Plataforma</th>
                    <th>Región</th>
                    <th>Precio</th>
                    <th>Estado</th>
                    <th>Registro</th>
                    <th class="text-end">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="key in getKeysByProduct(product.id)" :key="key.id">
                    <td><span class="badge nk-badge-platform">{{ key.platform }}</span></td>
                    <td class="text-secondary">{{ key.region }}</td>
                    <td class="fw-bold" style="color: var(--green-accent);">${{ key.price }}</td>
                    <td>
                      <span class="badge" :class="key.is_used ? 'nk-badge-danger' : 'nk-badge-success'">
                        {{ key.is_used ? 'Usada / Vendida' : 'Disponible' }}
                      </span>
                    </td>
                    <td class="text-muted small">{{ new Date(key.created_at).toLocaleDateString() }}</td>
                    <td class="text-end">
                      <button class="btn btn-sm nk-btn-delete-icon" title="Eliminar clave" @click="eliminarClave(key.id)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </tr>
                  <tr v-if="getKeysByProduct(product.id).length === 0">
                    <td colspan="6" class="text-center text-muted py-3">No hay claves registradas para este producto.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Botón para añadir nueva clave al producto -->
            <div class="mt-3 text-end">
              <button class="btn btn-sm nk-btn-outline-add" @click="añadirClave(product.id)">
                <i class="bi bi-plus-lg me-1"></i> Añadir Clave para {{ product.title }}
              </button>
            </div>
          </div>
        </div>
        <div v-if="productos.length === 0" class="text-center py-5 text-muted nk-table-container">
          <i class="bi bi-box-seam display-4 d-block mb-3 opacity-50"></i>
          <p>No hay productos en el catálogo todavía.</p>
        </div>

        <!-- Controles de Paginación -->
        <div v-if="totalPages > 1" class="pagination-controls d-flex justify-content-center align-items-center mt-4 mb-2 gap-3">
          <button class="btn btn-sm nk-btn-outline" :disabled="currentPage === 1" @click="currentPage--">
            <i class="bi bi-chevron-left"></i> Anterior
          </button>
          <span class="pagination-info">
            Página <span class="fw-bold">{{ currentPage }}</span> de {{ totalPages }}
          </span>
          <button class="btn btn-sm nk-btn-outline" :disabled="currentPage === totalPages" @click="currentPage++">
            Siguiente <i class="bi bi-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- Gestión de Usuarios -->
    <section class="container py-5 mb-5">
      <h2 class="mb-4 section-title"><i class="bi bi-people-fill me-2"></i>Gestión de Usuarios</h2>
      
      <div class="table-responsive nk-table-container">
        <table class="table nk-table align-middle mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Email</th>
              <th>Rol</th>
              <th class="text-end">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in usuarios" :key="user.id">
              <td class="text-muted">{{ user.id }}</td>
              <td class="fw-bold" style="color: var(--text-primary);">{{ user.username }}</td>
              <td class="text-secondary">{{ user.email }}</td>
              <td>
                <span class="badge" :class="user.is_staff ? 'nk-badge-admin' : 'nk-badge-user'">
                  <i :class="user.is_staff ? 'bi bi-shield-check me-1' : 'bi bi-person me-1'"></i>
                  {{ user.is_staff ? 'Admin' : 'Usuario' }}
                </span>
              </td>
              <td class="text-end">
                <button 
                  class="btn btn-sm me-2 nk-btn-outline" 
                  @click="hacerAdmin(user.id, user.is_staff)"
                  :disabled="usuarioActual && usuarioActual.id === user.id"
                  :title="usuarioActual && usuarioActual.id === user.id ? 'No puedes cambiar tu propio rol' : ''"
                >
                  <i class="bi bi-arrow-repeat"></i> Cambiar Rol
                </button>
                <button 
                  class="btn btn-sm nk-btn-delete-outline" 
                  @click="eliminarUsuario(user.id)"
                  :disabled="usuarioActual && usuarioActual.id === user.id"
                  :title="usuarioActual && usuarioActual.id === user.id ? 'No puedes eliminarte a ti mismo' : ''"
                >
                  <i class="bi bi-trash"></i> Eliminar
                </button>
              </td>
            </tr>
            <tr v-if="usuarios.length === 0">
              <td colspan="5" class="text-center text-muted py-4">No hay usuarios o cargando...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Colores de NexusKey (variables globales asumidas o redefinidas aquí) */
.section-title {
  color: var(--text-primary, #fff);
  font-weight: 700;
  font-size: 1.5rem;
}

/* Botón principal superior */
.nk-btn-primary {
  background: linear-gradient(135deg, var(--green-accent) 0%, #10a66a 100%);
  color: #000;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 1.5rem;
  transition: all 0.3s ease;
  text-decoration: none;
}
.nk-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(20, 203, 129, 0.4);
  color: #000;
}

/* Product Card (Reducida) */
.product-card {
  background: var(--bg-secondary, #1a1a2e);
  border: 1px solid rgba(157, 113, 200, 0.2);
  border-radius: 10px;
  padding: 1rem 1.25rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: border-color 0.3s ease;
}
.product-card:hover {
  border-color: rgba(20, 203, 129, 0.4);
}

.product-img-wrapper {
  width: 45px;
  height: 60px;
  border-radius: 4px;
  overflow: hidden;
  background-color: #2a1b3d;
  flex-shrink: 0;
}
.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-title {
  color: var(--text-primary, #fff);
  font-weight: 700;
  font-size: 1.05rem;
}

/* Paginación */
.pagination-controls {
  background: rgba(0, 0, 0, 0.15);
  padding: 0.8rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}
.pagination-info {
  color: var(--text-secondary, #aeb0b4);
  font-size: 0.9rem;
}

/* Tablas */
.nk-table-container {
  background: var(--bg-secondary, #1a1a2e);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.nk-table-container-sm {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.02);
  padding: 0.5rem;
}

.nk-table, .nk-table-sm {
  color: var(--text-secondary, #aeb0b4);
  --bs-table-bg: transparent;
  --bs-table-color: var(--text-secondary, #aeb0b4);
}

.nk-table thead th, .nk-table-sm thead th {
  color: var(--text-primary, #fff);
  font-weight: 600;
  border-bottom: 2px solid rgba(20, 203, 129, 0.2);
  padding-bottom: 1rem;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
}

.nk-table-sm thead th {
  padding-bottom: 0.5rem;
  font-size: 0.75rem;
  border-bottom: 1px solid rgba(20, 203, 129, 0.2);
}

.nk-table tbody td {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1.2rem 0.5rem;
}

.nk-table-sm tbody td {
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  padding: 0.8rem 0.5rem;
  font-size: 0.9rem;
}

.nk-table tbody tr:last-child td, .nk-table-sm tbody tr:last-child td {
  border-bottom: none;
}

.nk-table tbody tr:hover td, .nk-table-sm tbody tr:hover td {
  background-color: rgba(255, 255, 255, 0.02);
  color: var(--text-primary, #fff);
}

/* Badges */
.nk-badge-success {
  background: rgba(20, 203, 129, 0.15);
  color: var(--green-accent, #14cb81);
  border: 1px solid rgba(20, 203, 129, 0.3);
  padding: 0.4em 0.7em;
  font-weight: 600;
  border-radius: 6px;
}

.nk-badge-danger {
  background: rgba(255, 77, 79, 0.15);
  color: #ff4d4f;
  border: 1px solid rgba(255, 77, 79, 0.3);
  padding: 0.4em 0.7em;
  font-weight: 600;
  border-radius: 6px;
}

.nk-badge-platform {
  background: rgba(157, 113, 200, 0.15);
  color: #c9a0ff;
  border: 1px solid rgba(157, 113, 200, 0.3);
  padding: 0.3em 0.6em;
  font-weight: 500;
  border-radius: 4px;
  font-size: 0.8rem;
}

.nk-badge-admin {
  background: rgba(20, 203, 129, 0.15);
  color: var(--green-accent);
  border: 1px solid rgba(20, 203, 129, 0.3);
  padding: 0.5em 0.8em;
  font-weight: 600;
  border-radius: 6px;
}

.nk-badge-user {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.5em 0.8em;
  font-weight: 500;
  border-radius: 6px;
}

/* Botones Outline y Acciones */
.nk-btn-outline {
  color: #c9a0ff;
  border: 1px solid rgba(157, 113, 200, 0.5);
  background: transparent;
  transition: all 0.3s ease;
  border-radius: 6px;
}
.nk-btn-outline:hover:not(:disabled) {
  background: rgba(157, 113, 200, 0.15);
  color: #fff;
  border-color: #c9a0ff;
}

.nk-btn-delete-outline {
  color: #ff4d4f;
  border: 1px solid rgba(255, 77, 79, 0.5);
  background: transparent;
  transition: all 0.3s ease;
  border-radius: 6px;
}
.nk-btn-delete-outline:hover:not(:disabled) {
  background: rgba(255, 77, 79, 0.15);
  color: #ff4d4f;
  border-color: #ff4d4f;
}

.nk-btn-delete-icon {
  color: #ff4d4f;
  background: transparent;
  border: none;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  transition: background 0.2s;
}
.nk-btn-delete-icon:hover {
  background: rgba(255, 77, 79, 0.15);
}

.nk-btn-outline-add {
  color: var(--green-accent, #14cb81);
  border: 1px dashed rgba(20, 203, 129, 0.5);
  background: transparent;
  transition: all 0.3s ease;
  border-radius: 6px;
  font-size: 0.85rem;
}
.nk-btn-outline-add:hover {
  background: rgba(20, 203, 129, 0.1);
  border-style: solid;
}

.keys-title {
  color: #c9a0ff;
  font-size: 0.95rem;
  font-weight: 600;
}

button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>