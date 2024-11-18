<template>
  <div class="contacto">
    <h1>Contáctanos</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Nombre completo</label>
        <input
          type="text"
          id="name"
          v-model="name"
          required
          placeholder="Ingresa tu nombre completo"
        />
      </div>
      <div class="form-group">
        <label for="email">Correo electrónico</label>
        <input
          type="email"
          id="email"
          v-model="email"
          required
          placeholder="Ingresa tu correo electrónico"
        />
        <span v-if="emailError" class="error">{{ emailError }}</span>
      </div>
      <div class="form-group">
        <label for="message">Mensaje</label>
        <textarea
          id="message"
          v-model="message"
          required
          placeholder="Escribe tu mensaje aquí"
        ></textarea>
      </div>
      <div class="form-group">
        <label for="captcha">Captcha</label>
        <input
          type="text"
          id="captcha"
          v-model="captcha"
          required
          placeholder="Escribe el resultado de 5+3"
        />
      </div>
      <button type="submit">Enviar</button>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      email: "",
      message: "",
      captcha: "",
      successMessage: "",
      errorMessage: "",
      emailError: "",
    };
  },
  methods: {
    validateEmail(email) {
      const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      return re.test(email);
    },
    async submitForm() {
      // Validar correo electrónico
      if (!this.validateEmail(this.email)) {
        this.emailError = "Por favor, ingresa un correo electrónico válido.";
        return;
      } else {
        this.emailError = "";
      }

      try {
        // Enviar datos al servidor
        const response = await fetch("http://localhost:5000/api/consulta", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            nombre_completo: this.name,
            email: this.email,
            mensaje: this.message,
            captcha: this.captcha,
            estado: "Pendiente",  // O cualquier valor que consideres predeterminado
            fecha: new Date().toISOString(),  // Establece la fecha actual
          }),
        });

        if (!response.ok) {
          throw new Error("No se pudo enviar el mensaje. Inténtalo nuevamente.");
        }

        const result = await response.json();
        if (result.message === "Consulta guardada correctamente") {
          this.successMessage = "Consulta enviada correctamente.";
          this.errorMessage = "";
        }

        // Limpiar el formulario
        this.name = "";
        this.email = "";
        this.message = "";
        this.captcha = "";
      } catch (error) {
        this.errorMessage = error.message;
        this.successMessage = "";
      }
    },
  },
};
</script>

<style scoped>
.contacto {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: #fff;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #218838;
}
.error {
  color: red;
  font-size: 0.9em;
}
.success {
  color: green;
  font-size: 0.9em;
}
</style>
