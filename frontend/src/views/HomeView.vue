<template>
  <section>
    <h1>Bienvenido a ShoeFlow</h1>
    <p>Calcula tu talla exacta y descubre el mejor catálogo de calzado filtrado por tu medida.</p>
    <div class="cards">
      <article>
        <h2>Escanea tu pie</h2>
        <p>Sube una foto y obtiene tu talla recomendada con IA.</p>
      </article>
      <article>
        <h2>Catálogo personalizado</h2>
        <p>Compara ofertas de diferentes tiendas según tu talla.</p>
      </article>
      <article>
        <h2>Suscripción premium</h2>
        <p>Accede a recomendaciones avanzadas y atención prioritaria.</p>
      </article>
    </div>
  </section>
</template>

<script setup></script>

<style>
section {
  max-width: 980px;
  margin: 0 auto;
  padding: 2rem 0;
  animation: fadeInUp 0.95s ease both;
}
h1 {
  font-size: clamp(2.4rem, 4vw, 4rem);
  margin: 0;
  letter-spacing: -0.04em;
  line-height: 1.03;
}
p {
  max-width: 680px;
  margin: 1rem 0 0;
  color: #c8d2ff;
  font-size: 1.05rem;
  line-height: 1.8;
}
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
  margin-top: 2rem;
}
article {
  padding: 1.5rem;
  background: rgba(19, 29, 59, 0.82);
  border: 1px solid rgba(112, 148, 255, 0.18);
  border-radius: 24px;
  box-shadow: 0 24px 80px rgba(9, 17, 34, 0.25);
  backdrop-filter: blur(16px);
  transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
}
article:hover {
  transform: translateY(-4px);
  border-color: rgba(87, 171, 255, 0.35);
  box-shadow: 0 32px 90px rgba(7, 15, 40, 0.32);
}
article h2 {
  margin: 0 0 0.75rem;
  font-size: 1.25rem;
  color: #f5f8ff;
}
article p {
  margin: 0;
  color: #a9b4f2;
  line-height: 1.7;
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
