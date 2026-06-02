<template>
  <section>
    <h1>Escáner de pie</h1>
    <p>Introduce la URL de la imagen de tu pie para calcular tu talla.</p>
    <form @submit.prevent="submitImage">
      <label>
        URL de la imagen
        <input v-model="imageUrl" type="url" placeholder="https://..." required />
      </label>
      <button type="submit">Calcular talla</button>
    </form>

    <div v-if="result" class="result-card">
      <h2>Talla estimada: {{ result.shoe_size }}</h2>
      <p>Consejo: {{ result.brand_advice }}</p>
      <p>Confianza: {{ Math.round(result.confidence * 100) }}%</p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "../stores/userStore";

const imageUrl = ref("");
const result = ref(null);
const error = ref("");
const store = useUserStore();

async function submitImage() {
  error.value = "";
  result.value = null;

  try {
    const response = await fetch("/api/measure/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_url: imageUrl.value, user_id: "anonymous" }),
    });
    if (!response.ok) {
      throw new Error("Error al procesar la imagen");
    }
    const data = await response.json();
    result.value = data;
    store.setSize(data.shoe_size);
  } catch (err) {
    error.value = err.message;
  }
}
</script>

<style>
section {
  max-width: 720px;
  margin: 0 auto;
  padding: 1rem 0;
  animation: fadeInUp 0.95s ease both;
}
h1 {
  font-size: clamp(2rem, 3vw, 2.8rem);
  margin-bottom: 0.5rem;
}
p {
  color: #c3d0ff;
  line-height: 1.75;
}
form {
  display: grid;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: rgba(16, 23, 45, 0.84);
  border: 1px solid rgba(123, 145, 255, 0.18);
  border-radius: 28px;
  box-shadow: 0 30px 70px rgba(0, 0, 0, 0.16);
  transition: transform 0.28s ease, box-shadow 0.28s ease;
}
form:hover {
  transform: translateY(-2px);
}
label {
  display: grid;
  gap: 0.5rem;
  color: #d2dcff;
}
input {
  width: 100%;
  min-height: 3rem;
  padding: 0.95rem 1rem;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
  color: #eef2ff;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
input:focus {
  border-color: rgba(75, 164, 255, 0.8);
  box-shadow: 0 0 0 0.3rem rgba(73, 160, 255, 0.18);
}
button {
  align-self: start;
  padding: 0.95rem 1.4rem;
  background: linear-gradient(135deg, #3567ff, #1ab7d3);
  color: #fff;
  box-shadow: 0 18px 30px rgba(7, 81, 190, 0.24);
}
button:hover {
  box-shadow: 0 24px 40px rgba(7, 81, 190, 0.32);
}
.result-card {
  margin-top: 1.75rem;
  padding: 1.5rem;
  border-radius: 24px;
  background: rgba(21, 32, 59, 0.9);
  border: 1px solid rgba(180, 210, 255, 0.16);
  box-shadow: 0 20px 50px rgba(6, 18, 42, 0.24);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.result-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 28px 60px rgba(6, 18, 42, 0.28);
}
.result-card h2 {
  margin: 0 0 0.85rem;
  color: #f5f9ff;
}
.result-card p {
  margin: 0.45rem 0;
  color: #b7c6ef;
}
.error {
  margin-top: 1rem;
  color: #ff6d85;
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
