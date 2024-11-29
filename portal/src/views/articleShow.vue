<script setup>
    import { useArticlesStore } from '../stores/articles';
    import { storeToRefs } from 'pinia';
    import { onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router';

    const store = useArticlesStore();
    const { articles, loading, error} = storeToRefs(store);
    const route = useRoute();
    const desanitizedContent = ref('');

    const desanitizeHtml = (html) => {
    const tempDiv = document.createElement('div');
    html = html.replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&') // También puedes manejar &amp; para el carácter &
        .replace(/&quot;/g, '"') // Para comillas dobles
        .replace(/&apos;/g, "'"); // Para comillas simples
    tempDiv.innerHTML = html;
    return tempDiv.innerHTML;
    };

    const fetchArticles = async() => {
        const filter = {
            id:route.params.id,
        }
        await store.fetchArticles(filter);

        if (articles.value && articles.value.contenido) {
            desanitizedContent.value = desanitizeHtml(articles.value.contenido);
        }
        else{
            desanitizedContent.value = desanitizeHtml(articles.value.contenido);
        }
    };
    onMounted(() => {
        if(!articles.length){
            fetchArticles();
        }
    });
</script>

<template>
    <h1>{{articles.titulo}}</h1>
    <span>{{articles.fecha_creacion}}</span>
    <h2>{{articles.copete}}</h2>
    <span v-html="desanitizedContent"></span>
</template>

<style scoped>
    template{
        text-align: start;
    }
</style>