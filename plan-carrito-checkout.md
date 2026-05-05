# Plan de Trabajo — Carrito y Simulación de Pago

## Objetivo
Implementar un carrito funcional en el navbar, una vista de checkout al estilo Steam y una simulación de pago que muestre las keys compradas al finalizar.

---

## 1. Pinia Store — Carrito

**Tarea:** Crear el store del carrito que será la fuente de verdad para toda la funcionalidad.

**Archivo:** `stores/cart.js`

**Estado y acciones necesarias:**
```javascript
export const useCartStore = defineStore('cart', {
    state: () => ({
        items: [] // Lista de keys agregadas
    }),
    actions: {
        addItem(key) {
            const exists = this.items.find(i => i.keyId === key.keyId)
            if (!exists) this.items.push(key)
        },
        removeItem(keyId) {
            this.items = this.items.filter(i => i.keyId !== keyId)
        },
        clearCart() {
            this.items = []
        }
    },
    getters: {
        total: (state) => state.items.reduce((sum, i) => sum + parseFloat(i.price), 0),
        count: (state) => state.items.length
    }
})
```

> **Nota:** Cada item del carrito debe guardar: `keyId`, `productTitle`, `platform`, `region`, `price`.

---

## 2. Botón "Agregar al Carrito" — Lógica de Autenticación

**Tarea:** Que el botón en `ProductDetail.vue` solo funcione si el usuario está logueado y no es admin.

**Lógica en el botón:**
```javascript
function addToCart(key) {
    // Verificar que el usuario esté logueado
    if (!authStore.isAuthenticated) {
        // Redirigir al login o mostrar mensaje
        router.push({ name: 'Login' })
        return
    }
    // Verificar que no sea admin
    if (authStore.user.is_staff) {
        // Mostrar mensaje: "Los administradores no pueden comprar"
        return
    }
    cartStore.addItem({
        keyId: key.id,
        productTitle: product.title,
        platform: key.platform,
        region: key.region,
        price: key.price
    })
}
```

**Estados visuales del botón según el caso:**

| Situación | Comportamiento del botón |
|-----------|--------------------------|
| No logueado | Redirige al login al hacer click |
| Logueado como admin | Botón deshabilitado con tooltip |
| Logueado como usuario | Agrega al carrito normalmente |
| Ya está en el carrito | Botón deshabilitado "En carrito" |

---

## 3. Carrito en Navbar — Dropdown Funcional

**Tarea:** El ícono del carrito en el navbar despliega una caja con las keys guardadas.

### Comportamiento
- Click en ícono del carrito → toggle del dropdown
- Click fuera del dropdown → se cierra
- Badge numérico sobre el ícono mostrando `cartStore.count`

### Estructura del dropdown
```
┌─────────────────────────────┐
│  🛒 Mi Carrito              │
├─────────────────────────────┤
│  [x] Halo Infinite          │
│      PC • Global  $15.99    │
│                             │
│  [x] God of War             │
│      PlayStation • US $29.99│
├─────────────────────────────┤
│  Subtotal:        $45.98    │
│  [      Pagar      ]        │
└─────────────────────────────┘
```

### Detalles importantes
- El botón `[x]` de cada item llama a `cartStore.removeItem(keyId)`
- Si el carrito está vacío mostrar mensaje: *"Tu carrito está vacío"*
- El botón **Pagar** redirige a la vista `/checkout`
- El botón **Pagar** solo aparece si hay items en el carrito

---

## 4. Vue Router — Ruta de Checkout

**Tarea:** Agregar la ruta protegida de checkout en `router/index.js`.

```javascript
{
    path: '/checkout',
    name: 'Checkout',
    component: () => import('../views/Checkout.vue'),
    meta: { requiresAuth: true }
}
```

**Guardia de navegación:** Redirigir al login si el usuario no está autenticado:
```javascript
router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next({ name: 'Login' })
    } else {
        next()
    }
})
```

---

## 5. Vista `Checkout.vue` — Página de Pago

**Referencia visual:** Similar al carrito/checkout de Steam.

### Estructura de la vista

```
Checkout.vue
├── Columna izquierda (70%)
│   ├── Lista de items del carrito
│   │   └── Por cada item: imagen, título, plataforma, región, precio, botón eliminar
│   └── Selector de método de pago
│       ├── 💳 Tarjeta de Crédito
│       ├── 💳 Tarjeta de Débito
│       └── 🅿️ PayPal
└── Columna derecha (30%)
    ├── Resumen del pedido
    │   ├── Lista de items con precios
    │   └── Subtotal total
    └── Botón "Confirmar Compra"
```

### Selector de método de pago

Presentar como cards seleccionables, no como dropdown:
```javascript
const paymentMethods = [
    { id: 'Credit Card', label: 'Tarjeta de Crédito', icon: '💳' },
    { id: 'Debit Card', label: 'Tarjeta de Débito', icon: '💳' },
    { id: 'PayPal', label: 'PayPal', icon: '🅿️' }
]
const selectedMethod = ref('Credit Card')
```

La card seleccionada se resalta visualmente con el color de acento de la página.

### Botón "Confirmar Compra"
- Deshabilitado si no hay método de pago seleccionado
- Al hacer click llama a la función `completePurchase()`

---

## 6. Simulación del Pago — Lógica

**Tarea:** Al confirmar la compra, crear las ventas en el backend y mostrar las keys.

### Función `completePurchase()` en `Checkout.vue`

```javascript
async function completePurchase() {
    isLoading.value = true

    // Crear una venta por cada key en el carrito
    for (const item of cartStore.items) {
        await fetch('/api/sales/', {
            method: 'POST',
            headers: {
                'Authorization': `Token ${authStore.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                key_code: item.keyId,
                payment_method: selectedMethod.value
            })
        })
    }

    // Guardar los items comprados antes de limpiar el carrito
    purchasedItems.value = [...cartStore.items]

    // Limpiar el carrito
    cartStore.clearCart()

    // Mostrar modal de confirmación
    showSuccessModal.value = true
    isLoading.value = false
}
```

---

## 7. Modal de Confirmación — Keys Compradas

**Tarea:** Al completar la compra mostrar un modal con todas las keys adquiridas.

### Estructura del modal

```
┌──────────────────────────────────────┐
│  ✅ ¡Compra realizada con éxito!     │
├──────────────────────────────────────┤
│  Tus keys:                           │
│                                      │
│  Halo Infinite (PC • Global)         │
│  XXXXX-XXXXX-XXXXX    [📋 Copiar]   │
│                                      │
│  God of War (PS • US)                │
│  XXXXX-XXXXX-XXXXX    [📋 Copiar]   │
├──────────────────────────────────────┤
│  [    Ir al catálogo    ]            │
└──────────────────────────────────────┘
```

### Botón de copiar cada key

```javascript
function copyKey(keyCode) {
    navigator.clipboard.writeText(keyCode)
    // Cambiar ícono temporalmente a ✅ para confirmar la copia
}
```

> **Importante:** Las keys mostradas en el modal vienen de la respuesta del backend al crear la venta, usando el `SaleSerializer` con `KeyCodePrivateSerializer` anidado que ya fue configurado anteriormente. Así se asegura que el campo `key` solo se exponga en este momento específico.

---

## 8. Backend — Verificación del Endpoint de Ventas

**Tarea:** Verificar que el endpoint `POST /api/sales/` funcione correctamente y marque la key como usada automáticamente.

Modificar el `SaleViewSet` para que al crear una venta, marque automáticamente la key como usada:

```python
class SaleViewSet(viewsets.ModelViewSet):
    ...
    def perform_create(self, serializer):
        sale = serializer.save(user=self.request.user)
        # Marcar la key como usada
        sale.key_code.is_used = True
        sale.key_code.save()
```

> Esto garantiza que una key vendida no aparezca más en el catálogo disponible.

---

## Orden de implementación recomendado

1. ✅ Crear el store de Pinia del carrito
2. ✅ Implementar lógica de autenticación en botón "Agregar al carrito"
3. ✅ Hacer funcional el dropdown del carrito en navbar
4. ✅ Agregar ruta `/checkout` con guardia de navegación
5. ✅ Construir vista `Checkout.vue` con lista de items y selector de pago
6. ✅ Implementar `perform_create` en el backend para marcar keys como usadas
7. ✅ Implementar función `completePurchase()` y conectar con el backend
8. ✅ Crear modal de confirmación con keys y botón de copiar
