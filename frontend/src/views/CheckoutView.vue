<template>
  <section>
    <h1>Checkout Premium</h1>
    <p>Completa tu suscripción premium para recibir recomendaciones avanzadas.</p>
    
    <!-- Bloque de autenticación si no tiene token -->
    <div v-if="!store.accessToken" class="auth-card">
      <h2>Inicia sesión para suscribirte</h2>
      <p>Debes iniciar sesión con una red social para verificar tu identidad antes del pago.</p>
      <div class="auth-buttons">
        <button type="button" class="btn-auth google" @click="simulatedLogin('google')">
          <svg style="width:20px;height:20px;margin-right:8px" viewBox="0 0 24 24"><path fill="currentColor" d="M12.24 10.285V13.4h6.887c-.275 1.565-1.88 4.604-6.887 4.604-4.33 0-7.866-3.577-7.866-8s3.536-8 7.866-8c2.46 0 4.105 1.025 5.047 1.926l2.427-2.334C17.955 2.192 15.34 1 12.24 1 6.033 1 1 6.033 1 12.24s5.033 11.24 11.24 11.24c6.478 0 10.793-4.537 10.793-10.986 0-.745-.08-1.3-.176-1.859H12.24z"/></svg>
          Iniciar sesión con Google
        </button>
        <button type="button" class="btn-auth facebook" @click="simulatedLogin('facebook')">
          <svg style="width:20px;height:20px;margin-right:8px" viewBox="0 0 24 24"><path fill="currentColor" d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1v2h3v3h-3v6.95c4.56-.93 8-4.96 8-9.75z"/></svg>
          Iniciar sesión con Facebook
        </button>
      </div>
    </div>

    <!-- Bloque de suscripción si ya está autenticado -->
    <div v-else>
      <div class="user-badge">
        <span>Conectado como: <strong>{{ store.userEmail }}</strong></span>
        <a href="#" class="btn-logout" @click.prevent="logout">Cerrar sesión</a>
      </div>
      
      <form @submit.prevent="subscribe">
        <label>
          Email de facturación
          <input v-model="email" type="email" placeholder="tu@correo.com" required />
        </label>
        <label>
          Plan de suscripción
          <select v-model="planId">
            <option value="basic">Básico - $9.99/mes</option>
            <option value="pro">Pro - $19.99/mes</option>
          </select>
        </label>
        
        <div class="stripe-simulation-notice">
          <span>🔒 Modo demostración activo. No se realizará ningún cargo real.</span>
        </div>

        <button type="submit">Activar Suscripción</button>
      </form>
    </div>

    <div v-if="message" class="message">{{ message }}</div>
    <div v-if="error" class="error">{{ error }}</div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "../stores/userStore";

const email = ref("");
const planId = ref("basic");
const message = ref("");
const error = ref("");
const store = useUserStore();

onMounted(() => {
  if (store.userEmail) {
    email.value = store.userEmail;
  }
});

async function simulatedLogin(provider) {
  error.value = "";
  message.value = "";
  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ provider: provider, token: "mock-social-token-12345" })
    });
    
    if (!response.ok) {
      throw new Error("Error en la autenticación simulada.");
    }
    
    const data = await response.json();
    store.setToken(data.access_token);
    const mockEmail = `test.${provider}@shoeflow.com`;
    store.setEmail(mockEmail);
    email.value = mockEmail;
    message.value = `¡Sesión iniciada con éxito mediante ${provider}!`;
  } catch (err) {
    error.value = err.message;
  }
}

function logout() {
  store.setToken("");
  store.setEmail("");
  store.setSubscriptionStatus("");
  email.value = "";
  message.value = "Sesión cerrada correctamente.";
}

async function subscribe() {
  error.value = "";
  message.value = "";

  try {
    const response = await fetch("/api/payments/subscribe", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${store.accessToken}`
      },
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
  color: #111111;
}
p {
  color: #4a4a4a;
  line-height: 1.7;
}
form,
.auth-card {
  display: grid;
  gap: 1.25rem;
  margin-top: 1.5rem;
  padding: 1.8rem;
  border-radius: 28px;
  background: #fff8f0;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 28px 70px rgba(0, 0, 0, 0.08);
  transition: transform 0.28s ease, box-shadow 0.28s ease;
}
form:hover,
.auth-card:hover {
  transform: translateY(-2px);
}
.auth-card h2 {
  margin: 0;
  font-size: 1.4rem;
  color: #111111;
}
.auth-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.5rem;
}
.btn-auth {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.85rem 1.4rem;
  border-radius: 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
  color: #111111;
  flex: 1;
  min-width: 200px;
  background: #ffffff;
}
.btn-auth.google {
  color: #111111;
}
.btn-auth.google:hover {
  background: #f4e5db;
}
.btn-auth.facebook {
  color: #111111;
}
.btn-auth.facebook:hover {
  background: #f4e5db;
}
.user-badge {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1.2rem;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  margin-top: 1rem;
}
.user-badge strong {
  color: #111111;
}
.btn-logout {
  color: #111111;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
}
.btn-logout:hover {
  text-decoration: underline;
}
.stripe-simulation-notice {
  font-size: 0.85rem;
  color: #4f4f4f;
  background: #f7efe5;
  border: 1px dashed rgba(0, 0, 0, 0.08);
  padding: 0.75rem 1rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
}
label {
  display: grid;
  gap: 0.55rem;
  color: #111111;
}
input,
select {
  width: 100%;
  min-height: 3rem;
  padding: 1rem 1.1rem;
  border-radius: 18px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  background: #ffffff;
  color: #111111;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
input:focus,
select:focus {
  outline: none;
  border-color: rgba(0, 0, 0, 0.24);
  box-shadow: 0 0 0 0.28rem rgba(0, 0, 0, 0.08);
}
button[type="submit"] {
  width: fit-content;
  padding: 1rem 1.6rem;
  background: #111111;
  color: #f8f2e6;
  font-weight: 700;
  box-shadow: 0 22px 40px rgba(0, 0, 0, 0.18);
}
button[type="submit"]:hover {
  background: #000000;
}
.message {
  margin-top: 1rem;
  color: #111111;
}
.error {
  margin-top: 1rem;
  color: #b00020;
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
