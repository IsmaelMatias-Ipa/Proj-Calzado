<template>
  <div id="app">
    <header class="toolbar">
      <router-link to="/">Home</router-link>
      <router-link to="/scanner">Escáner</router-link>
      <router-link to="/catalog">Catálogo</router-link>
      <router-link to="/checkout">Checkout</router-link>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup></script>

<style>
:root {
  color-scheme: dark;
  color: #e8f0ff;
  background: #080b12;
  font-family: Inter, system-ui, sans-serif;
}
*, *::before, *::after {
  box-sizing: border-box;
}
body {
  margin: 0;
  min-height: 100vh;
  background: radial-gradient(circle at top left, rgba(45, 90, 255, 0.18), transparent 25%),
    radial-gradient(circle at bottom right, rgba(10, 255, 200, 0.14), transparent 20%),
    linear-gradient(180deg, #040611 0%, #0d1121 60%, #121827 100%);
  color: #eef2ff;
  overflow-x: hidden;
}
#app {
  min-height: 100vh;
}
.toolbar {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem 1.5rem;
  margin: 0 auto;
  backdrop-filter: blur(18px);
  background: rgba(14, 18, 34, 0.72);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18);
}
.toolbar a {
  color: #d7e2ff;
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.9rem;
  padding: 0.75rem 1rem;
  border-radius: 999px;
  transition: transform 0.22s ease, background 0.22s ease, color 0.22s ease;
}
.toolbar a:hover,
.toolbar a.router-link-active {
  background: rgba(78, 152, 255, 0.2);
  color: #ffffff;
  transform: translateY(-2px);
}
main {
  padding: 2rem 1.5rem 3rem;
  max-width: 1180px;
  margin: 0 auto;
  animation: pageFade 0.9s ease both;
}
button,
input,
select {
  font: inherit;
}
button {
  border: none;
  border-radius: 999px;
  transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease, opacity 0.18s ease;
}
button:hover {
  transform: translateY(-1px);
}
button:active {
  transform: translateY(1px);
}
input,
select {
  background: rgba(255, 255, 255, 0.06);
  color: #eef2ff;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.03);
}
input:focus,
select:focus {
  outline: none;
  border-color: rgba(64, 152, 255, 0.75);
  box-shadow: 0 0 0 0.3rem rgba(45, 105, 255, 0.16);
}
@keyframes pageFade {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes glowPulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(79, 146, 255, 0);
  }
  50% {
    box-shadow: 0 0 35px 0 rgba(79, 146, 255, 0.16);
  }
}
</style>
