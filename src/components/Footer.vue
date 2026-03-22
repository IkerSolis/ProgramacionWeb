<script setup>
defineProps({
  tipo: {
    type: String,
    default: 'general'
  }
});
</script>

<template>
  <footer>
    <div class="container">
      <div class="row g-4 mb-4">
        <div class="col-12 col-md-4">
          <div class="footer-brand mb-2">Nexus<span>Key</span></div>
          <p style="color:var(--purple-soft); font-size:.88rem; max-width:280px;">
            Tu catálogo de videojuegos de confianza. Encuentra, compara y adquiere los mejores títulos.
          </p>
          <div class="mt-3" id="redes">
            <p class="footer-heading">Contáctanos</p>
            <a href="https://x.com" target="_blank" class="social-icon"><i class="bi bi-twitter-x"></i></a>
            <a href="https://instagram.com" target="_blank" class="social-icon"><i class="bi bi-instagram"></i></a>
            <a href="https://youtube.com" target="_blank" class="social-icon"><i class="bi bi-youtube"></i></a>
          </div>
        </div>
        
        <div class="col-4 col-md-4">
          <p class="footer-heading">Soporte</p>
          <a href="/cuenta" class="footer-link">Mi cuenta</a>
        </div>
        
        <div class="col-4 col-md-4">
          <p class="footer-heading">Legal</p>
          <a href="/mision" class="footer-link">Misión</a>
          <a href="/vision" class="footer-link">Visión</a>
          <a href="/terminos" class="footer-link">Términos</a>
        </div>
        
        <div class="col-4 col-md-4" v-if="tipo === 'index'">
          <p>
            <a href="https://jigsaw.w3.org/css-validator/check/referer" target="_blank">
              <img style="border:0;width:88px;height:31px" src="https://jigsaw.w3.org/css-validator/images/vcss-blue" alt="¡CSS Válido!" />
            </a>
            <a href="https://validator.w3.org/nu/#textarea" target="_blank">
              <img style="border:0;width:88px;height:31px" src="https://www.w3.org/Icons/valid-html401-blue" alt="¡HTML Válido!" />
            </a>
          </p>
        </div>
      </div>
      
      <hr class="footer-divider"/>
      
      <div class="d-flex flex-wrap justify-content-between align-items-center pt-2">
        <p style="font-size:.8rem; color:var(--purple-soft); margin:0;">
          &copy; 2026 NexusKey. Todos los derechos reservados.
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>

</style>