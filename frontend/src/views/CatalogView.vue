<template>
  <section>
    <h1>Catálogo de tiendas</h1>
    <p>Encuentra calzado compatible con tu talla estimada.</p>

    <div class="search-row">
      <label>
        Talla
        <input v-model="size" placeholder="Ej: 42" />
      </label>
      <button @click="loadCatalog">Buscar catálogos</button>
    </div>

    <div v-if="items.length === 0 && loaded" class="empty-state">
      No se encontraron productos para la talla seleccionada.
    </div>

    <div class="grid" v-if="items.length">
      <article v-for="item in items" :key="item.id">
        <img :src="item.image" alt="item.name" />
        <h3>{{ item.name }}</h3>
        <p>{{ item.vendor }}</p>
        <p><strong>{{ item.price }} {{ item.currency }}</strong></p>
        <a :href="item.url" target="_blank">Ver oferta</a>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "../stores/userStore";

const store = useUserStore();
const size = ref("");
const items = ref([]);
const loaded = ref(false);
const error = ref("");

onMounted(() => {
  if (store.shoeSize) {
    size.value = store.shoeSize;
    loadCatalog();
  }
});


async function loadCatalog() {
  error.value = "";
  items.value = [];
  loaded.value = false;

  if (!size.value) {
    error.value = "Introduce una talla para buscar.";
    return;
  }

  try {
    const response = await fetch(`/api/stores/?size=${encodeURIComponent(size.value)}`);
    if (!response.ok) {
      throw new Error("Error al cargar el catálogo.");
    }
    const data = await response.json();
    items.value = data.items || [];
  } catch (err) {
    error.value = err.message;
  } finally {
    loaded.value = true;
  }
}
</script>

<style>
section {
  max-width: 1080px;
  margin: 0 auto;
  padding: 1rem 0;
  animation: fadeInUp 0.95s ease both;
}
h1 {
  font-size: clamp(2rem, 3vw, 2.8rem);
  margin-bottom: 0.4rem;
  color: #111111;
}
p {
  color: #4a4a4a;
  line-height: 1.75;
}
.search-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: flex-end;
  margin-top: 1.5rem;
}
.search-row > button {
  align-self: flex-end;
}
label {
  display: grid;
  gap: 0.5rem;
  min-width: 220px;
  color: #232323;
}
input {
  width: 100%;
  padding: 0.95rem 1rem;
  border-radius: 18px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  background: #ffffff;
  color: #111111;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
input:focus {
  border-color: rgba(0, 0, 0, 0.24);
  box-shadow: 0 0 0 0.28rem rgba(0, 0, 0, 0.08);
}
button {
  padding: 0.95rem 1.4rem;
  border-radius: 999px;
  background: #111111;
  color: #f8f2e6;
  box-shadow: 0 18px 30px rgba(0, 0, 0, 0.18);
}
button:hover {
  box-shadow: 0 24px 40px rgba(0, 0, 0, 0.22);
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
  margin-top: 1.75rem;
}
article {
  display: grid;
  gap: 0.9rem;
  overflow: hidden;
  border-radius: 28px;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 34px 80px rgba(0, 0, 0, 0.08);
  padding: 1.3rem;
  transition: transform 0.26s ease, border-color 0.26s ease, box-shadow 0.26s ease;
}
article:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 0, 0, 0.12);
  box-shadow: 0 42px 95px rgba(0, 0, 0, 0.12);
}
article img {
  width: 100%;
  min-height: 190px;
  max-height: 220px;
  object-fit: cover;
  border-radius: 18px;
}
article h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #111111;
}
article p {
  margin: 0;
  color: #444444;
}
article a {
  color: #111111;
  text-decoration: underline;
  font-weight: 600;
}
.empty-state {
  margin-top: 1.5rem;
  color: #5b5b5b;
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
