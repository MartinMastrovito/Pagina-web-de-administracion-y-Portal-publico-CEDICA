<script setup>
    import { useArticlesStore } from '../stores/articles';
    import { storeToRefs } from 'pinia';
    import { onMounted } from 'vue';
    import { useRoute } from 'vue-router';

    const store = useArticlesStore();
    const { articles, loading, error} = storeToRefs(store);
    const route = useRoute();

    const fetchArticles = async() => {
        const filter = {
            id:route.params.id,
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
    <h1>{{articles.titulo}}</h1>
    <h2>{{articles.copete}}</h2>
    <span>{{articles.año}}</span>
    <p>{{articles.contenido}}</p>
</template>

<style scoped>
    template{
        text-align: start;
    }
</style>