<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useCartStore } from '../stores/cart';
import { tokenActual } from '../data/estado.js';

const cartStore = useCartStore();
const router = useRouter();

const paymentMethods = [
    { id: 'Credit Card', label: 'Tarjeta de Crédito', icon: 'bi-credit-card-2-front-fill' },
    { id: 'Debit Card', label: 'Tarjeta de Débito', icon: 'bi-credit-card-fill' },
    { id: 'PayPal', label: 'PayPal', icon: 'bi-paypal' }
];
const selectedMethod = ref('Credit Card');
const isLoading = ref(false);
const showSuccessModal = ref(false);
const purchasedItems = ref([]);

const completePurchase = async () => {
    isLoading.value = true;
    try {
        const salesPromises = cartStore.items.map(item => {
            return fetch('http://localhost:8000/api/sales/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${tokenActual.value}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    key_code: item.keyId,
                    payment_method: selectedMethod.value
                })
            }).then(async res => {
                if (!res.ok) throw new Error(await res.text());
                return res.json();
            });
        });

        const results = await Promise.all(salesPromises);
        
        purchasedItems.value = results.map((r, index) => {
            const originalItem = cartStore.items[index];
            return {
                productTitle: originalItem.productTitle,
                platform: r.key_code.platform,
                region: r.key_code.region,
                keyString: r.key_code.key,
                copied: false
            };
        });

        cartStore.clearCart();
        showSuccessModal.value = true;

    } catch (error) {
        console.error("Error al procesar la compra:", error);
        alert("Hubo un error procesando el pago. Intente de nuevo.");
    } finally {
        isLoading.value = false;
    }
};

const copyKey = (item) => {
    navigator.clipboard.writeText(item.keyString);
    item.copied = true;
    setTimeout(() => {
        item.copied = false;
    }, 2000);
};

const goCatalog = () => {
    showSuccessModal.value = false;
    router.push('/catalogo');
};
</script>

<template>
  <div class="checkout-wrapper py-5">
    <div class="container">
      <h2 class="mb-4 text-white fw-bold"><i class="bi bi-cart-check-fill me-2" style="color: var(--green-accent);"></i>Finalizar Compra</h2>
      
      <div v-if="cartStore.items.length === 0 && !showSuccessModal" class="text-center py-5 rounded-4" style="background: var(--bg-secondary);">
        <i class="bi bi-cart-x fs-1 mb-3 d-block" style="color: var(--purple-soft);"></i>
        <h4 class="text-white">Tu carrito está vacío</h4>
        <p style="color: var(--purple-soft);">Agrega productos antes de proceder al pago.</p>
        <router-link to="/catalogo" class="btn nk-btn-buy mt-3 px-4">Ir al Catálogo</router-link>
      </div>

      <div v-else-if="!showSuccessModal" class="row g-4">
        
        <!-- Columna Izquierda -->
        <div class="col-lg-8">
          
          <!-- Lista de Items -->
          <div class="checkout-box p-4 rounded-4 mb-4">
            <h4 class="text-white mb-4">Revisar Pedido</h4>
            <div class="items-list d-flex flex-column gap-3">
              <div v-for="item in cartStore.items" :key="item.keyId" class="item-card p-3 rounded-3 d-flex justify-content-between align-items-center">
                <div>
                  <h5 class="text-white mb-1">{{ item.productTitle }}</h5>
                  <div class="d-flex gap-2 mt-2">
                    <span class="badge nk-badge-platform">{{ item.platform }}</span>
                    <span class="badge nk-badge-region">{{ item.region }}</span>
                  </div>
                </div>
                <div class="text-end">
                  <h4 class="key-price mb-2">${{ item.price }}</h4>
                  <button class="btn btn-sm text-danger border-0 p-0" @click="cartStore.removeItem(item.keyId)">
                    <i class="bi bi-trash-fill me-1"></i> Eliminar
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Selector de Método de Pago -->
          <div class="checkout-box p-4 rounded-4">
            <h4 class="text-white mb-4">Método de Pago</h4>
            <div class="row g-3">
              <div v-for="method in paymentMethods" :key="method.id" class="col-md-4">
                <div 
                  class="payment-card p-3 text-center rounded-3 h-100" 
                  :class="{ 'selected': selectedMethod === method.id }"
                  @click="selectedMethod = method.id"
                >
                  <i :class="['bi', method.icon, 'fs-2 d-block mb-2']"></i>
                  <span class="fw-bold">{{ method.label }}</span>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- Columna Derecha -->
        <div class="col-lg-4">
          <div class="checkout-box summary-box p-4 rounded-4 sticky-top" style="top: 2rem;">
            <h4 class="text-white mb-4">Resumen</h4>
            
            <div class="d-flex justify-content-between mb-2">
              <span style="color: var(--white-off);">Subtotal ({{ cartStore.count }} items)</span>
              <span class="text-white fw-bold">${{ cartStore.total.toFixed(2) }}</span>
            </div>
            <div class="d-flex justify-content-between mb-3 pb-3 border-bottom border-secondary">
              <span style="color: var(--white-off);">Impuestos</span>
              <span class="text-white fw-bold">$0.00</span>
            </div>
            
            <div class="d-flex justify-content-between mb-4">
              <span class="text-white fs-5 fw-bold">Total</span>
              <span class="key-price fs-4 fw-bold">${{ cartStore.total.toFixed(2) }}</span>
            </div>

            <button 
              class="btn nk-btn-buy w-100 py-3 fw-bold fs-5 d-flex align-items-center justify-content-center gap-2"
              :disabled="isLoading"
              @click="completePurchase"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <i v-else class="bi bi-check-circle-fill"></i>
              {{ isLoading ? 'Procesando...' : 'Confirmar Compra' }}
            </button>
            <p class="text-center small mt-3 mb-0" style="color: var(--purple-soft);">Al confirmar, aceptas nuestros términos y condiciones. Esta es una transacción segura.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Éxito -->
    <div v-if="showSuccessModal" class="success-overlay d-flex align-items-center justify-content-center">
      <div class="success-modal p-4 p-md-5 rounded-4 text-center">
        <i class="bi bi-check-circle-fill text-success" style="font-size: 4rem;"></i>
        <h2 class="text-white mt-3 mb-2 fw-bold">¡Compra exitosa!</h2>
        <p class="mb-4" style="color: var(--purple-soft); font-size: 1.1rem;">Tus llaves están listas para ser activadas.</p>
        
        <div class="keys-container text-start mb-4">
          <div v-for="(item, index) in purchasedItems" :key="index" class="purchased-key-card p-3 rounded-3 mb-3">
            <h5 class="text-white mb-1 fw-bold">{{ item.productTitle }}</h5>
            <small class="d-block mb-2" style="color: var(--green-accent);">{{ item.platform }} • {{ item.region }}</small>
            <div class="d-flex align-items-center gap-2">
              <code class="key-code-display flex-grow-1 p-2 rounded-2 text-center fs-5">{{ item.keyString }}</code>
              <button class="btn btn-outline-success border-0 px-3 py-2" @click="copyKey(item)" :title="item.copied ? '¡Copiado!' : 'Copiar al portapapeles'">
                <i :class="item.copied ? 'bi bi-check2-all' : 'bi bi-clipboard'"></i>
              </button>
            </div>
          </div>
        </div>

        <button class="btn nk-btn-buy px-5 py-2 fw-bold" @click="goCatalog">Volver al Catálogo</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.checkout-wrapper {
  min-height: 100vh;
  background-color: var(--bg-primary, #0f0a1c);
}

.checkout-box {
  background: var(--bg-secondary, #1a1a2e);
  border: 1px solid rgba(157, 113, 200, 0.2);
}

.summary-box {
  border-color: rgba(20, 203, 129, 0.3);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.item-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255,255,255,0.05);
}

.key-price {
  color: var(--green-accent, #14cb81);
  font-family: 'Orbitron', sans-serif;
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

.payment-card {
  background: rgba(0,0,0,0.3);
  border: 2px solid transparent;
  color: var(--white-off);
  cursor: pointer;
  transition: all 0.2s ease;
}

.payment-card:hover {
  background: rgba(157, 113, 200, 0.15);
  border-color: rgba(157, 113, 200, 0.6);
  color: #fff;
}

.payment-card.selected {
  background: rgba(20, 203, 129, 0.1);
  border-color: var(--green-accent, #14cb81);
  color: var(--green-accent, #14cb81);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(20, 203, 129, 0.2);
}

.nk-btn-buy {
  background: linear-gradient(135deg, var(--green-accent) 0%, #10a66a 100%);
  color: #000;
  border: none;
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.nk-btn-buy:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(20, 203, 129, 0.4);
}

.nk-btn-buy:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Modal de Éxito */
.success-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 10, 28, 0.98);
  z-index: 1050;
}

.success-modal {
  background: var(--bg-secondary, #1a1a2e);
  border: 1px solid rgba(20, 203, 129, 0.4);
  box-shadow: 0 20px 50px rgba(0,0,0,0.6);
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.purchased-key-card {
  background: rgba(0,0,0,0.4);
  border: 1px dashed rgba(20, 203, 129, 0.3);
}

.key-code-display {
  background: #000;
  color: var(--green-accent);
  border: 1px solid #333;
  letter-spacing: 2px;
  font-family: 'Courier New', Courier, monospace;
}
</style>
