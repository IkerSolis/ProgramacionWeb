<script setup>
import { API_BASE_URL } from '../api/config.js';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCartStore } from '../stores/cart.js';
import { usuarioActual } from '../data/estado.js';

const route = useRoute();
const router = useRouter();
const productId = route.params.id;

const product = ref(null);
const images = ref([]);
const keys = ref([]);
const activeImage = ref(0);
const loading = ref(true);
const cartStore = useCartStore();

const loadData = async () => {
  try {
    const [resProd, resImgs, resKeys] = await Promise.all([
      fetch(`${API_BASE_URL}/api/products/${productId}/`),
      fetch(`${API_BASE_URL}/api/products/${productId}/images/`),
      fetch(`${API_BASE_URL}/api/keycodes/?product=${productId}&is_used=false`)
    ]);

    if (resProd.ok) {
      product.value = await resProd.json();
    } else {
      router.push('/catalogo');
    }

    if (resImgs.ok) {
      images.value = await resImgs.json();
      const backupCover = product.value?.cover || product.value?.image_url;
      if (images.value.length === 0 && backupCover) {
        images.value = [backupCover];
      }
    }

    if (resKeys.ok) {
      keys.value = await resKeys.json();
    }
  } catch (error) {
    console.error("Error cargando detalles del producto:", error);
  } finally {
    loading.value = false;
  }
};

const nextImage = () => {
  if (images.value.length > 0) {
    activeImage.value = (activeImage.value + 1) % images.value.length;
  }
};

const prevImage = () => {
  if (images.value.length > 0) {
    activeImage.value = (activeImage.value - 1 + images.value.length) % images.value.length;
  }
};

const setActiveImage = (index) => {
  activeImage.value = index;
};

const agregarAlCarrito = (key) => {
  if (!usuarioActual.value) {
    alert("Inicia sesión para poder comprar.");
    router.push('/login');
    return;
  }
  if (usuarioActual.value.is_staff) {
    alert("Los administradores no pueden hacer compras.");
    return;
  }
  
  cartStore.addItem({
    keyId: key.id,
    productTitle: product.value.title,
    platform: key.platform,
    region: key.region,
    price: key.price
  });
  
  // Opcional: mostrar una notificación rápida en vez de alert
};

onMounted(() => {
  loadData();
});
</script>

<template>
  <div class="product-detail-wrapper pb-5">
    <!-- Loading State -->
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="min-height: 60vh;">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <div v-else-if="product" class="container mt-4">
      
      <!-- Navegación superior -->
      <nav aria-label="breadcrumb" class="mb-4">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><router-link to="/catalogo" class="text-decoration-none nk-link">Catálogo</router-link></li>
          <li class="breadcrumb-item active text-white" aria-current="page">{{ product.title }}</li>
        </ol>
      </nav>

      <div class="row g-4">
        
        <!-- Columna Izquierda: Galería e Info -->
        <div class="col-lg-8">
          
          <!-- Galería Principal (Carousel) -->
          <div class="gallery-container mb-4 position-relative">
            <div class="main-image-wrapper">
              <img :src="images.length > 0 ? images[activeImage] : 'https://via.placeholder.com/800x450/2a1b3d/9d71c8?text=No+Image'" class="main-image" :alt="product.title">
            </div>
            
            <button v-if="images.length > 1" class="gallery-btn prev" @click="prevImage"><i class="bi bi-chevron-left"></i></button>
            <button v-if="images.length > 1" class="gallery-btn next" @click="nextImage"><i class="bi bi-chevron-right"></i></button>

            <!-- Miniaturas -->
            <div v-if="images.length > 1" class="thumbnails-container mt-2 d-flex gap-2 overflow-auto py-2">
              <div 
                v-for="(img, idx) in images" 
                :key="idx" 
                class="thumbnail-wrapper"
                :class="{ 'active': activeImage === idx }"
                @click="setActiveImage(idx)"
              >
                <img :src="img" class="thumbnail-img">
              </div>
            </div>
          </div>

          <!-- Descripción del Juego -->
          <div class="product-info-box p-4 rounded-4 mb-4">
            <h2 class="mb-3 product-title">{{ product.title }}</h2>
            <div class="d-flex gap-2 mb-3">
              <span class="badge nk-badge-genre">{{ product.genre }}</span>
              <span v-if="product.igdb_id" class="badge bg-secondary">IGDB Base</span>
            </div>
            <hr class="nk-divider">
            <h5 class="text-white mt-4 mb-3">Acerca del juego</h5>
            <p class="product-description">{{ product.description || 'No hay descripción disponible para este título.' }}</p>
          </div>
        </div>

        <!-- Columna Derecha: Opciones de Compra -->
        <div class="col-lg-4">
          <div class="purchase-box p-4 rounded-4" style="top: 2rem;">
            <h4 class="mb-4 text-white"><i class="bi bi-key-fill me-2 text-success"></i>Comprar Keys</h4>
            
            <div v-if="keys.length > 0" class="keys-list d-flex flex-column gap-3">
              <div v-for="key in keys" :key="key.id" class="key-card p-3 rounded-3">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div class="d-flex gap-2">
                    <span class="badge nk-badge-platform"><i class="bi bi-pc-display me-1"></i>{{ key.platform }}</span>
                    <span class="badge nk-badge-region">{{ key.region }}</span>
                  </div>
                  <h3 class="key-price mb-0">${{ key.price }}</h3>
                </div>
                
                <div class="d-grid mt-3">
                  <button class="btn nk-btn-buy" 
                    @click="agregarAlCarrito(key)"
                    :disabled="cartStore.items.some(i => i.keyId === key.id) || (usuarioActual && usuarioActual.is_staff)"
                    :title="usuarioActual?.is_staff ? 'Administradores no compran' : ''">
                    <i class="bi bi-cart-plus me-2"></i> 
                    {{ cartStore.items.some(i => i.keyId === key.id) ? 'En Carrito' : 'Añadir al carrito' }}
                  </button>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-5 no-keys-box rounded-3">
              <i class="bi bi-emoji-frown fs-1 text-muted mb-3 d-block"></i>
              <h5 class="text-white">Agotado</h5>
              <p class="text-muted mb-0">No hay llaves disponibles para este producto en este momento.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-detail-wrapper {
  min-height: 100vh;
  background-color: var(--bg-primary, #0f0a1c);
  color: var(--text-primary, #fff);
}

.nk-link {
  color: var(--purple-soft, #c9a0ff);
  transition: color 0.2s;
}
.nk-link:hover {
  color: var(--green-accent, #14cb81);
}

/* Galería */
.gallery-container {
  background: var(--bg-secondary, #1a1a2e);
  padding: 10px;
  border-radius: 12px;
  border: 1px solid rgba(157, 113, 200, 0.2);
}
.main-image-wrapper {
  width: 100%;
  aspect-ratio: 16/9;
  overflow: hidden;
  border-radius: 8px;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.main-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.gallery-btn {
  position: absolute;
  top: calc(50% - 20px - 40px); /* Ajustado por las miniaturas */
  background: rgba(0,0,0,0.6);
  color: #fff;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
  z-index: 2;
}
.gallery-btn:hover {
  background: var(--green-accent, #14cb81);
  color: #000;
}
.gallery-btn.prev { left: 20px; }
.gallery-btn.next { right: 20px; }

.thumbnails-container {
  scrollbar-width: thin;
  scrollbar-color: var(--purple-mid) transparent;
}
.thumbnail-wrapper {
  width: 120px;
  height: 67px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s, opacity 0.2s;
  opacity: 0.6;
}
.thumbnail-wrapper:hover {
  opacity: 0.9;
}
.thumbnail-wrapper.active {
  border-color: var(--green-accent, #14cb81);
  opacity: 1;
}
.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Info del Producto */
.product-info-box {
  background: var(--bg-secondary, #1a1a2e);
  border: 1px solid rgba(157, 113, 200, 0.2);
}
.product-title {
  font-weight: 800;
  font-size: 2.2rem;
  color: var(--white-off, #f8f9fa);
}
.product-description {
  color: var(--purple-soft, #c9a0ff);
  line-height: 1.6;
  white-space: pre-line;
}
.nk-divider {
  border-color: rgba(157, 113, 200, 0.3);
}
.nk-badge-genre {
  background: rgba(157, 113, 200, 0.2);
  color: #c9a0ff;
  border: 1px solid rgba(157, 113, 200, 0.4);
  font-size: 0.9rem;
  padding: 0.5em 1em;
}

/* Caja de Compra */
.purchase-box {
  background: var(--bg-secondary, #1a1a2e);
  border: 1px solid rgba(20, 203, 129, 0.3);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.key-card {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(157, 113, 200, 0.15);
  transition: transform 0.2s, border-color 0.2s;
}
.key-card:hover {
  transform: translateY(-2px);
  border-color: rgba(20, 203, 129, 0.4);
}
.key-price {
  color: var(--green-accent, #14cb81);
  font-family: 'Orbitron', sans-serif;
  font-weight: 700;
}
.nk-btn-buy {
  background: linear-gradient(135deg, var(--green-accent) 0%, #10a66a 100%);
  color: #000;
  font-weight: 700;
  border: none;
  padding: 0.8rem;
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.nk-btn-buy:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(20, 203, 129, 0.4);
  color: #000;
}
.nk-badge-platform {
  background: #2a2a2a;
  color: #fff;
  border: 1px solid #444;
}
.nk-badge-region {
  background: rgba(157, 113, 200, 0.2);
  color: #c9a0ff;
  border: 1px solid rgba(157, 113, 200, 0.3);
}
.no-keys-box {
  background: rgba(0, 0, 0, 0.2);
  border: 1px dashed rgba(255, 255, 255, 0.1);
}
</style>
