<script setup>
defineProps({
    id:Number,
    año:String,
    titulo:String,
    copete:String,
    contenido:String

})
</script>
<template>
    <div class="item">
        <h2>Titulo: {{ titulo }}</h2>
        <div class="año">
            <p>año: {{ año }}</p>
        </div>
        <div class="copete">
            <p>copete: {{ copete }}</p>
        </div>
        <div>
            <RouterLink class="btn" :to="`/noticia/${id}`">
            Ver mas
            </RouterLink>
        </div>
    </div>
</template>
<style scoped>

    .item{
        background-color: antiquewhite;
    }
    .año{
        font-size:small;
    }

    .copete{
        font-size:medium;
    }
</style>