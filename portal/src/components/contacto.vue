<template>
  <div>
    <h2>Contacto</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="name">Nombre completo:</label>
        <input type="text" id="name" v-model="name" required>
      </div>
      <div>
        <label for="email">Correo electrónico:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div>
        <label for="message">Mensaje:</label>
        <textarea id="message" v-model="message" required></textarea>
      </div>
      <div>
        <label for="captcha">Captcha:</label>
        <input type="text" id="captcha" v-model="captcha" required>
      </div>
      <button type="submit">Enviar</button>
    </form>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success">{{ successMessage }}</div>
  </div>
</template>

<script>
export default {
  name: 'Contacto',
  data() {
    return {
      name: '',
      email: '',
      message: '',
      captcha: '',
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async submitForm() {
      if (!this.validateEmail(this.email)) {
        this.errorMessage = 'Por favor, ingrese un correo electrónico válido.';
        return;
      }

      try {
        const response = await fetch('https://api.example.com/contact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            message: this.message,
            captcha: this.captcha
          })
        });

        if (!response.ok) {
          throw new Error('Error al enviar el formulario');
        }

        this.successMessage = 'Mensaje enviado con éxito.';
        this.errorMessage = '';
        this.name = '';
        this.email = '';
        this.message = '';
        this.captcha = '';
      } catch (error) {
        this.errorMessage = error.message;
        this.successMessage = '';
      }
    },
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    }
  }
};
</script>

<style scoped>
/* Estilos específicos para el componente Contacto */
.error {
  color: red;
}
.success {
  color: green;
}
</style>