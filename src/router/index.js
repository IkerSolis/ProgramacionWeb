import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import Catalog from '../views/Catalog.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminPanel from '../views/AdminPanel.vue'
import AddProduct from '../views/addProduct.vue'
import EditProduct from '../views/EditProduct.vue'
import { usuarioActual } from '../data/estado.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    { path: '/catalogo', name: 'catalogo', component: Catalog },
    { path: '/product/:id', name: 'ProductDetail', component: () => import('../views/ProductDetail.vue') },
    { 
      path: '/checkout', 
      name: 'Checkout', 
      component: () => import('../views/Checkout.vue'),
      meta: { requiresAuth: true }
    },
    { path: '/login', name: 'login', component: Login },
    { path: '/registro', name: 'registro', component: Register },
    { 
      path: '/panel', 
      name: 'panel', 
      component: AdminPanel,
      meta: { requiresAdmin: true }
    },
    { 
      path: '/add-product', 
      name: 'añadirProducto', 
      component: AddProduct,
      meta: { requiresAdmin: true }
    },
    { 
      path: '/edit-product/:id', 
      name: 'editProduct', 
      component: EditProduct,
      meta: { requiresAdmin: true }
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      // Si navegamos a un hash, desplazarse hacia el contenedor superior en vez del elemento exacto si es necesario
      if (to.hash === '#mision' || to.hash === '#vision') {
        return { el: '#hero-carousel', behavior: 'smooth' };
      }
      return { el: to.hash, behavior: 'smooth' }
    } else if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAdmin) {
    if (!usuarioActual.value) {
      next({ name: 'login' })
    } else if (!usuarioActual.value.is_staff) {
      next({ name: 'home' })
    } else {
      next()
    }
  } else if (to.meta.requiresAuth) {
    if (!usuarioActual.value) {
      next({ name: 'login' })
    } else if (usuarioActual.value.is_staff) {
      next({ name: 'home' }) // admins no compran
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router