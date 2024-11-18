<template>
  <div>
    <h2>Tareas</h2>
    <ul>
      <li v-for="tarea in tareas" :key="tarea.id">{{ tarea.descripcion }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Tareas",
  data() {
    return {
      tareas: [],
    };
  },
  async created() {
    try {
      const response = await fetch("https://api.example.com/tareas");
      this.tareas = await response.json();
    } catch (error) {
      console.error("Error al obtener tareas:", error);
    }
  },
};
</script>
