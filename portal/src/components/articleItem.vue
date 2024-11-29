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
        <h2>{{ titulo }}</h2>
        <div class="año">
            <p>Creacion: {{ año }}</p>
        </div>
        <div class="copete">
            <p>{{ copete }}</p>
        </div>
        <div>
            <RouterLink class="btn btn-info" :to="`/noticia/${id}`">
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