<template>
  <div>
    <h2>Últimas Noticias</h2>
    <div v-for="noticia in noticias" :key="noticia.id" class="noticia">
      <h3>{{ noticia.titulo }}</h3>
      <p v-html="noticia.contenido"></p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Noticias",
  data() {
    return {
      noticias: [],
    };
  },
  async created() {
    try {
      const response = await fetch("https://api.example.com/noticias");
      this.noticias = await response.json();
    } catch (error) {
      console.error("Error al obtener noticias:", error);
    }
  },
};
</script>
