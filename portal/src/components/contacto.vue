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
      <!-- reCAPTCHA -->
      <div id="recaptcha-container" class="form-group"></div>
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
      captchaToken: "", // Token del reCAPTCHA
      successMessage: "",
      errorMessage: "",
      emailError: "",
    };
  },
  mounted() {
    // Carga dinámica del script de reCAPTCHA
    const script = document.createElement("script");
    script.src = "https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);

    // Define la función onloadCallback para renderizar el reCAPTCHA
    window.onloadCallback = () => {
      window.grecaptcha.render("recaptcha-container", {
        sitekey: "6LfMIYYqAAAAAB6jARfFQKbeatxyfbg0J0isoNEj", // Reemplaza con tu clave de sitio
        callback: this.onCaptchaSuccess, // Método a llamar cuando se resuelve el captcha
      });
    };
  },
  methods: {
    validateEmail(email) {
      const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      return re.test(email);
    },
    onCaptchaSuccess(token) {
      this.captchaToken = token; // Captura el token al resolver el reCAPTCHA
    },
    async submitForm() {
      if (!this.validateEmail(this.email)) {
        this.emailError = "Por favor, ingresa un correo electrónico válido.";
        return;
      }

      if (!this.captchaToken) {
        this.errorMessage = "Por favor, completa el reCAPTCHA.";
        return;
      }

      try {
        const response = await fetch("https://admin-grupo30.proyecto2024.linti.unlp.edu.ar/api/consulta", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            nombre_completo: this.name,
            email: this.email,
            mensaje: this.message,
            captcha: this.captchaToken, // Envía el token del reCAPTCHA
            estado: "Pendiente", // Estado predeterminado
            fecha: new Date().toISOString(), // Fecha actual
          }),
        });

        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.error || "No se pudo enviar el mensaje. Inténtalo nuevamente.");
        }

        this.successMessage = "Consulta enviada correctamente.";
        this.errorMessage = "";
        this.resetForm();
      } catch (error) {
        this.errorMessage = error.message;
        this.successMessage = "";
      }
    },
    resetForm() {
      this.name = "";
      this.email = "";
      this.message = "";
      this.captchaToken = "";
      // Reinicia el reCAPTCHA
      if (window.grecaptcha) {
        window.grecaptcha.reset();
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
