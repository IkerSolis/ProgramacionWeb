import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
    state: () => ({
        items: [] // Lista de keys agregadas
    }),
    actions: {
        addItem(key) {
            const exists = this.items.find(i => i.keyId === key.keyId);
            if (!exists) this.items.push(key);
        },
        removeItem(keyId) {
            this.items = this.items.filter(i => i.keyId !== keyId);
        },
        clearCart() {
            this.items = [];
        }
    },
    getters: {
        total: (state) => state.items.reduce((sum, i) => sum + parseFloat(i.price), 0),
        count: (state) => state.items.length
    }
});
