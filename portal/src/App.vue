<template id="app">
    <header class="header">
      <div class="header-content">
        <h1>Centro de equitación</h1>
        <p>La Plata, buenos Aires</p>
        <img src="@/assets/logo.png" alt="Logo de CEDICA" class="logo" />
      </div>
      <nav>
          <RouterLink class="btn" to="/">Home</RouterLink>
          <RouterLink class="btn" to="/noticias/1">Noticias</RouterLink>
          <RouterLink class="btn" to="/contacto">Contacto</RouterLink>
      </nav>
    </header>
    <main>
      <RouterView/>
    </main>
    <footer class="footer">
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
}

header {
  text-align: center;
  background-color: #4842b935;
  padding: 20px;
  color: white;
}

footer {
  background-color: #42b983;
  padding: 10px;
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

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #007bff;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}

.btn-primary {
  background-color: #007bff;
}
</style>
