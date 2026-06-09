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
  color-scheme: light;
  color: #111111;
  background: #f8f2e6;
  font-family: Inter, system-ui, sans-serif;
}
*, *::before, *::after {
  box-sizing: border-box;
}
body {
  margin: 0;
  min-height: 100vh;
  background: linear-gradient(180deg, #fbf5ed 0%, #f3e2cf 100%);
  color: #111111;
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
  background: rgba(255, 255, 255, 0.96);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.08);
}
.toolbar a {
  color: #111111;
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
  background: #111111;
  color: #f8f2e6;
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
  background: #111111;
  color: #f8f2e6;
}
button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 24px rgba(0, 0, 0, 0.14);
}
button:active {
  transform: translateY(1px);
}
input,
select {
  background: #ffffff;
  color: #111111;
  border: 1px solid rgba(0, 0, 0, 0.14);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.04);
}
input:focus,
select:focus {
  outline: none;
  border-color: rgba(0, 0, 0, 0.24);
  box-shadow: 0 0 0 0.3rem rgba(0, 0, 0, 0.08);
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
    box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
  }
  50% {
    box-shadow: 0 0 35px 0 rgba(0, 0, 0, 0.08);
  }
}
</style>
