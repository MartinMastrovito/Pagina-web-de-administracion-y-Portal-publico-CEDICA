<template id="app" class="container-fluid">
    <header class="header conteiner-fluid">
      <div class="header-content">
        <h1>Centro de equitación</h1>
        <p>La Plata, buenos Aires</p>
        <img src="@/assets/logo.png" alt="Logo de CEDICA" class="logo" />
      </div>
      <nav>
          <RouterLink class="btn btn-primary" to="/">Home</RouterLink>
          <RouterLink class="btn btn-primary" to="/noticias/1">Noticias</RouterLink>
          <RouterLink class="btn btn-primary" to="/contacto">Contacto</RouterLink>
      </nav>
    </header>
    <main class="container-fluid">
      <RouterView/>
    </main>
    <footer class="navbar fixed-bottom">
      <p>&copy; 2024 CEDICA. Todos los derechos reservados.</p>
    </footer>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
console.log(import.meta.env.VITE_ARTICLES_API);
</script>

<style>
/* Estilos específicos para App.vue */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  padding-bottom: 70px;
}

header {
  text-align: center;
  background-color: #4842b935;
  color: white;
}

footer {
  background-color: #42b983;
  color: white;
  width: 100%;
  bottom: 0;
}

.logo{
  max-width: 50%;
  margin-top:15px;
}

nav{
  display:flex;
  justify-content: space-around;
}
</style>
