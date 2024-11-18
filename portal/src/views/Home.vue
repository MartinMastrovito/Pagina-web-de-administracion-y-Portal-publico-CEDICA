<template>
  <div class="home">
    <header class="header">
      <div class="header-content">
        <h1>Centro de Equitación</h1>
        <p>La Plata, Buenos Aires</p>
        <img src="@/assets/logo.png" alt="Logo de CEDICA" class="logo" />
      </div>
    </header>

    <nav class="nav">
      <ul>
        <li><a href="#info">Información</a></li>
        <li><a href="#tareas">Tareas</a></li>
        <li><a href="#contacto">Contacto</a></li>
        <li><a href="#noticias">Noticias</a></li>
      </ul>
    </nav>

    <main class="container">
      <section id="info" class="info">
        <h2 class="section-title">Sobre CEDICA</h2>
        <p>
          El Centro de Equitación para Personas con Discapacidad y Carenciadas, 
          CEDICA, es una Asociación Civil sin Fines de Lucro, fundada en 1994 en La Plata, Buenos Aires.
          La misión de CEDICA es la inclusión social, trabajando para igualar oportunidades y mejorar la calidad de vida de sus alumnos y alumnas.
        </p>
        <p>
          La actividad se centra en la <strong>Rehabilitación Ecuestre</strong>, 
          una terapia que utiliza el caballo como herramienta de recuperación en las dimensiones biológica, psíquica y social.
        </p>
      </section>

      <section id="tareas" class="tareas">
        <h2 class="section-title">Tareas y Actividades</h2>
        <Tareas />
      </section>

      <section id="noticias" class="noticias">
        <h2 class="section-title">Noticias</h2>
        <Noticias />
      </section>

      <section id="contacto" class="contacto">
        <h2 class="section-title">Contacto</h2>
        <Contacto />
      </section>
    </main>

    <footer class="footer">
      <p>&copy; 2024 CEDICA. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script>
import Contacto from "@/components/contacto.vue";
import Tareas from "@/components/tareas.vue";
import Noticias from "@/components/noticias.vue";

export default {
  name: "Home",
  components: {
    Contacto,
    Tareas,
    Noticias,
  },
};
</script>

<style scoped>
/* General Styles */
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9; /* Fondo claro para todo */
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Asegura que siempre ocupe toda la pantalla */
}

/* Header Styles */
.header {
  background: #f5f5f5;
  padding: 20px 0;
  text-align: center;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  max-width: 150px;
  margin-top: 15px;
}

/* Navigation Styles */
.nav {
  background: #333;
  color: white;
  padding: 10px 0;
}

.nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.nav a {
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  display: block;
}

.nav a:hover {
  background: #575757;
  border-radius: 5px;
}

/* Main Container */
.container {
  flex: 1; /* Hace que el contenedor ocupe todo el espacio disponible */
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
  box-sizing: border-box;
}

/* Sections */
section {
  margin-bottom: 40px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Footer */
.footer {
  background: #333;
  color: white;
  text-align: center;
  padding: 10px 0;
  margin-top: 40px;
}


</style>
