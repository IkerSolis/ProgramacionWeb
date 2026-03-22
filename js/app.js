import { Navbar } from './navbar.js'
import { Footer } from './footer.js'

const app = Vue.createApp({})

app.component('navbar-comp', Navbar)
app.component('footer-comp', Footer)

app.mount('#app')