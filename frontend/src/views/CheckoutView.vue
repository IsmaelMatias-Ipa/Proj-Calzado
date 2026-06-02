<template>
  <section>
    <h1>Checkout</h1>
    <p>Completa tu suscripción premium para recibir recomendaciones avanzadas.</p>
    <form @submit.prevent="subscribe">
      <label>
        Email
        <input v-model="email" type="email" placeholder="tu@correo.com" required />
      </label>
      <label>
        Plan
        <select v-model="planId">
          <option value="basic">Básico - $9.99/mes</option>
          <option value="pro">Pro - $19.99/mes</option>
        </select>
      </label>
      <button type="submit">Suscribirme</button>
    </form>

    <div v-if="message" class="message">{{ message }}</div>
    <div v-if="error" class="error">{{ error }}</div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "../stores/userStore";

const email = ref("");
const planId = ref("basic");
const message = ref("");
const error = ref("");
const store = useUserStore();

async function subscribe() {
  error.value = "";
  message.value = "";

  try {
    const response = await fetch("/api/payments/subscribe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: "anonymous", email: email.value, plan_id: planId.value }),
    });
    if (!response.ok) {
      throw new Error("No se pudo procesar la suscripción.");
    }
    const data = await response.json();
    message.value = data.message;
    store.setSubscriptionStatus(data.success ? "active" : "failed");
  } catch (err) {
    error.value = err.message;
  }
}
</script>

<style>
section {
  max-width: 700px;
  margin: 0 auto;
  padding: 1rem 0;
  animation: fadeInUp 0.95s ease both;
}
h1 {
  font-size: clamp(2rem, 3vw, 2.8rem);
  margin-bottom: 0.3rem;
}
p {
  color: #c9d4ff;
  line-height: 1.7;
}
form {
  display: grid;
  gap: 1.25rem;
  margin-top: 1.5rem;
  padding: 1.5rem;
  border-radius: 28px;
  background: rgba(18, 27, 48, 0.88);
  border: 1px solid rgba(120, 175, 255, 0.16);
  box-shadow: 0 28px 70px rgba(4, 7, 24, 0.22);
  transition: transform 0.28s ease, box-shadow 0.28s ease;
}
form:hover {
  transform: translateY(-2px);
}
label {
  display: grid;
  gap: 0.55rem;
  color: #d1d9ff;
}
input,
select {
  width: 100%;
  min-height: 3rem;
  padding: 1rem 1.1rem;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
  color: #eef2ff;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
input:focus,
select:focus {
  outline: none;
  border-color: rgba(72, 164, 255, 0.8);
  box-shadow: 0 0 0 0.28rem rgba(72, 164, 255, 0.16);
}
button {
  width: fit-content;
  padding: 1rem 1.6rem;
  background: radial-gradient(circle at top left, #39f2ff, #3366ff 60%);
  color: #021028;
  font-weight: 700;
  box-shadow: 0 22px 40px rgba(17, 95, 223, 0.28);
}
button:hover {
  box-shadow: 0 26px 46px rgba(17, 95, 223, 0.34);
}
.message {
  margin-top: 1rem;
  color: #83ffc7;
}
.error {
  margin-top: 1rem;
  color: #ff7caf;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
