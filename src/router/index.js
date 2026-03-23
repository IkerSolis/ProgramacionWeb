import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import Catalog from '../views/Catalog.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminPanel from '../views/AdminPanel.vue' // <-- 1. Importas la vista
import AddProduct from '../views/addProduct.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    { path: '/catalogo', name: 'catalogo', component: Catalog },
    { path: '/login', name: 'login', component: Login },
    { path: '/registro', name: 'registro', component: Register },
    { path: '/panel', name: 'panel', component: AdminPanel },
    { path: '/add-product', name: 'añadirProducto', component: AddProduct }
  ]
})

export default router