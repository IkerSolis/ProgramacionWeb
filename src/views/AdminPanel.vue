<script setup>
import { ref, onMounted } from 'vue';
import { usuarioActual, authHeader } from '../data/estado.js';

const editarProducto = () => {
  console.log('Iniciando flujo para editar producto...');
};

const eliminarProducto = () => {
  console.log('Iniciando flujo para eliminar producto...');
};

const usuarios = ref([]);
const errorMsg = ref('');

const cargarUsuarios = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/users/', {
      headers: { ...authHeader() }
    });
    if (res.ok) {
      usuarios.value = await res.json();
    } else {
      errorMsg.value = "Error cargando usuarios.";
    }
  } catch (err) {
    errorMsg.value = "Error de conexión.";
  }
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
      cargarUsuarios();
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
      cargarUsuarios();
    } else {
      alert("Error al actualizar usuario.");
    }
  } catch (err) {
    alert("Error de conexión.");
  }
};

onMounted(() => {
  cargarUsuarios();
});
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

    <!-- Nueva sección: Gestión de Usuarios -->
    <section class="container py-5">
      <h2 class="mb-4" style="color:var(--text-primary); font-weight:700;">Gestión de Usuarios</h2>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      
      <div class="table-responsive nk-table-container">
        <table class="table nk-table align-middle mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Email</th>
              <th>Rol</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in usuarios" :key="user.id">
              <td>{{ user.id }}</td>
              <td class="fw-bold" style="color: var(--text-primary);">{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span class="badge" :class="user.is_staff ? 'nk-badge-admin' : 'nk-badge-user'">
                  <i :class="user.is_staff ? 'bi bi-shield-check me-1' : 'bi bi-person me-1'"></i>
                  {{ user.is_staff ? 'Admin' : 'Usuario' }}
                </span>
              </td>
              <td>
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
.nk-table-container {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.nk-table {
  color: var(--text-secondary);
  --bs-table-bg: transparent;
}

.nk-table thead th {
  color: var(--text-primary);
  font-weight: 600;
  border-bottom: 2px solid rgba(20, 203, 129, 0.2);
  padding-bottom: 1rem;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
}

.nk-table tbody td {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1.2rem 0.5rem;
}

.nk-table tbody tr:last-child td {
  border-bottom: none;
}

.nk-table tbody tr:hover td {
  background-color: rgba(255, 255, 255, 0.02);
  color: var(--text-primary);
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

.nk-btn-outline {
  color: var(--green-accent);
  border: 1px solid var(--green-accent);
  background: transparent;
  transition: all 0.3s ease;
  border-radius: 6px;
}

.nk-btn-outline:hover:not(:disabled) {
  background: var(--green-accent);
  color: #000;
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

button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>