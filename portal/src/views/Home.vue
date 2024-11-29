<template>
  <div class="container-fluid home">
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
  .home{
    text-align: center;
  }
</style>

