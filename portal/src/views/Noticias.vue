<template>
  <div>
    <h1>Noticias</h1>
    <noticias />
  </div>
</template>

<script>
import Noticias from '../components/noticias.vue';

export default {
  name: 'NoticiasView',
  components: {
    Noticias
  }
};
</script>