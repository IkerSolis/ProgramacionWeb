<script setup>
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

<template>
  <div class="d-flex flex-column min-vh-100">
    <Navbar tipo="user" />

    <main class="flex-grow-1">
      <router-view></router-view>
    </main>
      
    <Footer tipo="index" />
  </div>
</template>