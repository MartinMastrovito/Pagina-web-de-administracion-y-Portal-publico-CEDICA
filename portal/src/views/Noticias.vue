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
    <articlesList
      :articles="articles"
      :pages="pages" 
    />
    <nav>
      <a
        v-for="page in pages"
        class="btn" 
        :href="`/noticias/${page}`">   
          {{ page }}
      </a>
    </nav>
  </main>
</template>