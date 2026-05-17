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
    host: true, // Permite conexiones desde la red local
    https: true, // Asegura que el servidor arranque en modo seguro
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Redirige las peticiones /api al backend local
        changeOrigin: true,
        secure: false
      }
    }
  }
})

