<script setup>
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

        <table v-if="!loading && articles.length">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Fecha publicacion</th>
                    <th>Titulo</th>
                    <th>Copete</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="article in articles" :key="article.id">
                    <td>{{ article.id }}</td>
                    <td>{{ article.fecha_publicacion }}</td>
                    <td>{{ article.titulo }}</td>
                    <td>{{ article.copete }}</td>
                </tr>
            </tbody>
        </table>
        <p v-if="!loading && !articles.length">No hay articulos para mostrar</p>
    </div>
</template>
