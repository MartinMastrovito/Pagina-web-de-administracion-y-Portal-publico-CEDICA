<script setup>
    import articleItem from '../components/articleItem.vue'
    defineProps({
        articles:Array,
        pages:Number
    })
</script>

<template>
    <div>
        <h2>Lista de articulos</h2>
        <div v-if="articles.length">
            <div class="listado">
                <articleItem 
                    v-for="article in articles" 
                    :id="article.id"
                    :titulo="article.titulo"
                    :año="article.fecha_creacion" 
                    :copete="article.copete"
                    :contenido="article.contenido"
                />
            </div>
        </div>
    </div>
</template>

<style scoped >
    .listado{
        display:flex;
        flex-direction: column;
        gap:20px;
    }
</style>
