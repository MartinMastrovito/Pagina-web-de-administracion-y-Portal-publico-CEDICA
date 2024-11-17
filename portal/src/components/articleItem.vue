<script setup>
defineProps({
    año:String,
    titulo:String,
    copete:String
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
    </div>
</template>
<style>

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