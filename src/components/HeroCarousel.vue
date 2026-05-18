<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// 1. Definimos los datos de cada diapositiva (slide)
const slides = ref([
  {
    id: 0,
    tipo: 'mixto', // Tiene texto e imagen
    badge: 'Tu tienda de keys definitiva',
    titulo: 'Expande tu catálogo<br><span class="accent">de videojuegos</span>',
    texto: 'Miles de títulos para todas las plataformas. Desde indie hasta AAA, encuentra el juego perfecto para ti.',
    imagen: '/img/collage.png'
  },
  {
    id: 1,
    tipo: 'mixto',
    titulo: '<span class="accent">Misión</span>',
    badge: 'Lo que buscamos',
    texto: '"Nuestra misión es proporcionar a la comunidad gamer un acceso directo y económico a licencias digitales de videojuegos, eliminando los sobreprecios impuestos por intermediarios y garantizando un sistema de entrega automatizada las 24 horas, los 7 días de la semana."',
    imagen: '/img/mision.jpg'
  },
  {
    id: 2,
    tipo: 'texto',
    titulo: '<span class="accent">Visión</span>',
    texto: 'Ser el marketplace de llaves virtuales líder en la región para el año 2030, reconocidos por ofrecer la plataforma más robusta, segura y rápida del mercado. Aspiramos a expandir nuestro catálogo a todas las plataformas de software global.'
  },
  {
    id: 4,
    tipo: 'mixto',
    badge: 'Comprueba las ofertas que ocurren ahora mismo',
    titulo: '<span class="accent">Ofertas Actuales!</span>',
    texto: '"Conoce las nuevas ofertas de Verano."',
    imagen: '/img/banner.png'
  }
]);

const slideActual = ref(0);
const tiempoSlide = 20000; // 6 segundos por cada slide
let intervalo = null;

// 2. Funciones para controlar el carrusel
const siguienteSlide = () => {
  slideActual.value = (slideActual.value + 1) % slides.value.length;
};

const irASlide = (index) => {
  slideActual.value = index;
  reiniciarTemporizador(); // Si el usuario hace clic, reiniciamos el tiempo
};

// 3. Control del tiempo
const iniciarTemporizador = () => {
  intervalo = setInterval(siguienteSlide, tiempoSlide);
};

const reiniciarTemporizador = () => {
  clearInterval(intervalo);
  iniciarTemporizador();
};

// Arrancamos el temporizador cuando el componente se carga
onMounted(() => {
  iniciarTemporizador();
  
  if (route.hash === '#mision') irASlide(1);
  if (route.hash === '#vision') irASlide(2);
});

watch(() => route.hash, (newHash) => {
  if (newHash === '#mision') irASlide(1);
  if (newHash === '#vision') irASlide(2);
});

// Lo limpiamos si el usuario se va a otra página (para no consumir memoria)
onUnmounted(() => {
  clearInterval(intervalo);
});
</script>

<template>
  <section id="hero-carousel" class="home-top carousel-container position-relative">
    <div class="container relative-wrapper" id="mision" >
      
      <transition name="fade-slide" mode="out-in">
        
        <div :key="slideActual" class="row align-items-center g-5 min-slide-height">
          
          <template v-if="slides[slideActual].tipo === 'mixto'">
            <div class="col-lg-6">
              <p class="text-uppercase mb-2" style="font-size:.75rem;letter-spacing:.15em;color:var(--green-accent);font-weight:600;">
                <i class="bi bi-controller me-1"></i> {{ slides[slideActual].badge }}
              </p>
              <h1 class="home-top-title mb-3" v-html="slides[slideActual].titulo"></h1>
              <p class="home-top-subtitle mb-4">{{ slides[slideActual].texto }}</p>
            </div>    
            <div class="col-lg-6 d-flex justify-content-center">
              <img :src="slides[slideActual].imagen" alt="Collage" width="100%" style="padding: 5px; border-radius: 17px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            </div>
          </template>

          <template v-else>
            <div class="col-12 text-center d-flex flex-column align-items-center justify-content-center">
              <h1 class="home-top-title mb-4" v-html="slides[slideActual].titulo"></h1>
              <p class="home-top-subtitle mx-auto" style="max-width: 800px; font-size: 1.2rem; line-height: 1.6;">
                {{ slides[slideActual].texto }}
              </p>
            </div>
          </template>

        </div>
      </transition>
    </div>

    <div class="carousel-dots">
      <button 
        v-for="(slide, index) in slides" 
        :key="index"
        class="dot-btn"
        :class="{ 'active': slideActual === index }"
        @click="irASlide(index)"
        aria-label="Cambiar slide"
      ></button>
    </div>

    <div class="progress-container">
      <div class="progress-bar-fill" :key="`progress-${slideActual}`"></div>
    </div>
  </section>
</template>

<style scoped>

.carousel-container {
  overflow: hidden;
  padding-bottom: 6rem;
  position: relative;
}

/*El pseudo-elemento que crea el fondo animado */
.carousel-container::before {
  content: '';
  position: absolute;
  inset: -50px; 
  z-index: 0; /* Lo ponemos detrás de todo el contenido */

  background-image: url('/img/patron-logos.svg');

  background-repeat: repeat;

  background-size: 80px 80px;

  opacity: 0.2;
  filter: blur(4px);

  animation: moverDiagonal 30s linear infinite;
  pointer-events: none;
}

.relative-wrapper {
  position: relative;
  z-index: 1;
}

.min-slide-height {
  min-height: 400px;
}
/* Definimos la animación para el recorrido diagonal */
@keyframes moverDiagonal {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 60px 60px;
  }
}
.min-slide-height {
  min-height: 400px;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.carousel-dots {
  position: absolute;
  bottom: 25px;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 12px;
  z-index: 10;
}
.dot-btn {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: var(--purple-light);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
  opacity: 0.5;
}
.dot-btn:hover {
  opacity: 1;
}
.dot-btn.active {
  background-color: var(--green-accent);
  width: 35px;
  border-radius: 10px;
  opacity: 1;
  box-shadow: 0 0 10px rgba(127,255,110,0.5);
}

.progress-container {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: rgba(107, 63, 160, 0.2);
}
.progress-bar-fill {
  height: 100%;
  background-color: var(--green-accent);
  width: 0%;
  animation: llenarBarra 20s linear forwards;
}

@keyframes llenarBarra {
  0% { width: 0%; }
  100% { width: 100%; }
}
</style>