<template>
  <section>
    <h1>Bienvenido a ShoeFlow</h1>
    <p>Calcula tu talla exacta y descubre el mejor catálogo de calzado filtrado por tu medida.</p>
      <div class="roulette-section">
        <div class="roulette" aria-hidden="true">
          <!-- Placeholder image for the roulette; replace later with actual images -->
          <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" alt="Ruleta de imágenes (placeholder)" />
        </div>

        <div class="categories" role="navigation" aria-label="Categorías principales">
          <button class="category-button" type="button">
            <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" alt="HOMBRES" />
            <span>HOMBRES</span>
          </button>
          <button class="category-button" type="button">
            <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" alt="DAMAS" />
            <span>DAMAS</span>
          </button>
          <button class="category-button" type="button">
            <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" alt="INFANTES" />
            <span>INFANTES</span>
          </button>
          <button class="category-button" type="button">
            <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" alt="OTROS" />
            <span>OTROS</span>
          </button>
        </div>
      </div>

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
  color: #111111;
}
p {
  max-width: 680px;
  margin: 1rem 0 0;
  color: #3a3a3a;
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
  padding: 1.8rem;
  background: #ffffff;
  border: 1px solid rgba(17, 17, 17, 0.08);
  border-radius: 24px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.08);
  transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
}
article:hover {
  transform: translateY(-4px);
  border-color: rgba(17, 17, 17, 0.16);
  box-shadow: 0 32px 90px rgba(0, 0, 0, 0.12);
}
article h2 {
  margin: 0 0 0.75rem;
  font-size: 1.25rem;
  color: #111111;
}
article p {
  margin: 0;
  color: #4f4f4f;
  line-height: 1.7;
}
/* Ruleta y categorías */
.roulette-section {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
  align-items: center;
  margin-top: 1.5rem;
}
.roulette {
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  height: 286px;
  background: #ffffff;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 18px 40px rgba(0,0,0,0.06);
}
.roulette img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.categories {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}
.category-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  background: #ffffff;
  border: 1px solid rgba(0,0,0,0.06);
  padding: 0.6rem 0.9rem;
  border-radius: 12px;
  cursor: pointer;
  min-width: 120px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.06);
}
.category-button img {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 8px;
  display: block;
}
.category-button span {
  font-weight: 700;
  color: #111111;
  font-size: 0.9rem;
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
