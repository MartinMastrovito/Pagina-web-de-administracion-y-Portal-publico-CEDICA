<script setup>
    import articleItem from '../components/articleItem.vue'
    import { useArticlesStore } from '../stores/articles';
    import { storeToRefs } from 'pinia';
    import { onMounted, } from 'vue';
    import { RouterLink, useRoute } from 'vue-router';

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



</script>

<template>
    <div>
        <h2>Lista de articulos</h2>
        <p v-if="loading">Cargando...</p>
        <p v-if="error">{{ error }}</p>
        <div v-if="!loading && articles.length">
            <div class="listado">
                <articleItem 
                    v-for="article in articles" 
                    :id="article.id"
                    :titulo="article.titulo"
                    :año="article.fecha_publicacion" 
                    :copete="article.copete"
                    :contenido="article.contenido"
                />
            </div>
            <nav>
                <RouterLink
                    v-for="page in pages"
                    class="btn" 
                    :to="`/noticias/${page}`">   
                        {{ page }}
                </RouterLink>
            </nav>
        </div>
        <p v-if="!loading && !articles.length">No hay articulos para mostrar</p>
    </div>
</template>

<style scoped >
    .listado{
        display:flex;
        flex-direction: column;
        gap:20px;
    }
</style>
