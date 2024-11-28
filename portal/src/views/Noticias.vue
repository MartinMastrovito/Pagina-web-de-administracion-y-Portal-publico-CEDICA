<script setup>
    import articlesList from '../components/articlesList.vue'
    import { useArticlesStore } from '../stores/articles';
    import { storeToRefs } from 'pinia';
    import { onMounted, watch } from 'vue';
    import { RouterLink, useRoute, RouterView} from 'vue-router';

    const store = useArticlesStore();
    const { articles, pages,loading, error} = storeToRefs(store);
    const route = useRoute();
    
    const fetchArticles = async() => {
        const filter = {
            page:route.params.page,
            titulo: titulo.value,
            desde: desde.value,
            hasta: hasta.value 
        }
        await store.fetchArticles(filter);
    };
    onMounted(() => {
        if(!articles.length){
            fetchArticles();
        }
    });
    watch(
        route,(newValue,oldValue) => {
            console.log("ola")
            if(newValue !== oldValue){
                fetchArticles()
            }
        }
    )
</script>

<template>
  <main>
    <form @submit.prevent="fetchArticles">
      <div class="row">
          <div class="col">
            <label for="titulo">Título:</label>
            <input
              type="text"
              id="titulo"
              v-model="titulo"
              placeholder="Buscar por título"
            />
          </div>
          <div class="col">
            <label for="desde">Desde:</label>
            <input
              type="date"
              id="desde"
              v-model="desde"
              placeholder="Buscar por fecha"
            />
          </div>
          <div class=col>
            <label for="hasta">Hasta:</label>
            <input
              type="date"
              id="hasta"
              v-model="hasta"
              placeholder="Buscar por fecha"
            />
          </div>
          <div class=col>
            <button type="submit" class="btn btn-primary">Buscar</button>
          </div>
      </div>
    </form>
    <articlesList
      :articles="articles"
      :pages="pages" 
    />
    <br>
    <nav>
      <div v-for="page in pages">
        <a v-if="page != route.params.page"
          class="btn btn-primary" 
          :href="`/noticias/${page}`">   
            {{ page }}
        </a>
        <p v-else style="color: black;" class="btn btn-secondary disabled">{{ page }}</p>
    </div>
    </nav>
  </main>
</template>
