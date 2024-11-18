<script setup>
defineProps({
    copete:String,
    año:String,
    copete:String,
    contenido:String
})
</script>
<template>
    <h1>{{ titulo }}</h1>
    <h2>{{ copete }}</h2>
    <span>{{ año }}</span>
    <p>{{ contenido }}</p>
</template>