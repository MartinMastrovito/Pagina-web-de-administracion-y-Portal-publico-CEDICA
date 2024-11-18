<script setup>
    import articleItem from '../components/articleItem.vue'
    import { useArticlesStore } from '../stores/articles';
    import { storeToRefs } from 'pinia';
    import { onMounted } from 'vue';

    const store = useArticlesStore();
    const { articles, loading, error} = storeToRefs(store);

    const fetchArticles = async() => {
        await store.fetchArticles();
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
