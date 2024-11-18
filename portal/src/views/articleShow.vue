<script setup>
    import { useArticlesStore } from '../stores/articles';
    import { storeToRefs } from 'pinia';
    import { onMounted } from 'vue';
    
    const filter = {
        id: this.$route.params.id
    }

    const store = useArticlesStore();
    const { articles, loading, error} = storeToRefs(store);

    const fetchArticles = async() => {
        await store.fetchArticles(filter);
    };
    onMounted(() => {
        if(!articles.length){
            fetchArticles();
        }
    });
</script>

<template>
    <h1>ID: {{this.$route.params.id}}</h1>
    <h1>titulo</h1>
    <h2>copete</h2>
    <span>año</span>
    <p>contenido</p>
</template>