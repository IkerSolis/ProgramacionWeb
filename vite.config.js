import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import basicSsl from '@vitejs/plugin-basic-ssl'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    basicSsl() // Esto activa HTTPS automáticamente
  ],
  server: {
    https: true // Asegura que el servidor arranque en modo seguro
  }
})

