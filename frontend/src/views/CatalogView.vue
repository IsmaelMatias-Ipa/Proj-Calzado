<template>
  <section>
    <h1>Catálogo de tiendas</h1>
    <p>Encuentra calzado compatible con tu talla estimada.</p>

    <div class="search-row">
      <label>
        Talla
        <input v-model="size" placeholder="Ej: 42" @keyup.enter="loadCatalog" />
      </label>
      <button @click="loadCatalog" :disabled="loading">
        <span v-if="loading" class="spinner"></span>
        {{ loading ? 'Buscando...' : 'Buscar catálogos' }}
      </button>
    </div>

    <div v-if="error" class="error-msg">{{ error }}</div>

    <div v-if="items.length === 0 && loaded && !loading" class="empty-state">
      No se encontraron productos para la talla seleccionada.
    </div>

    <div v-if="items.length" class="results-panel">
      <div class="results-header">
        <span class="results-count">{{ items.length }} producto{{ items.length !== 1 ? 's' : '' }}</span>
      </div>

      <div class="catalog-list">
        <article
          v-for="(item, index) in items"
          :key="item.id"
          class="catalog-card"
          :style="{ '--delay': `${index * 0.07}s` }"
        >
          <div class="card-image">
            <img :src="item.image" :alt="item.name" loading="lazy" />
          </div>

          <div class="card-body">
            <div class="field-row">
              <span class="field-label">Marca</span>
              <span class="field-value">{{ item.vendor }}</span>
            </div>
            <div class="field-row">
              <span class="field-label">Modelo</span>
              <span class="field-value">{{ item.name }}</span>
            </div>
            <div class="field-row">
              <span class="field-label">Tipo / Categoría</span>
              <span class="field-value">{{ item.category }}</span>
            </div>
            <div class="field-row">
              <span class="field-label">Género / Público</span>
              <span class="field-value">{{ item.gender }}</span>
            </div>
            <div class="field-row">
              <span class="field-label">Tallas disponibles</span>
              <span class="field-value sizes-row">
                <span
                  v-for="s in item.sizes"
                  :key="s"
                  :class="['size-badge', { active: isMatchingSize(s) }]"
                >{{ s }}</span>
              </span>
            </div>
            <div class="field-row price-row">
              <span class="field-label">Precio</span>
              <span class="field-value price-val">{{ item.price }} {{ item.currency }}</span>
            </div>
            <div class="field-row">
              <span class="field-label">Stock</span>
              <span class="field-value" :class="stockClass(item)">{{ item.stock }}</span>
            </div>

            <a :href="item.url" target="_blank" rel="noopener" class="store-btn">
              Ir a la tienda
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </a>
          </div>
        </article>
      </div>
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
const loading = ref(false);
const error = ref("");

const EURO_SIZES = [35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46];
const SIZE_CONVERSIONS = {
  35: { eu: 35, us: 4.5, uk: 2.5 },
  36: { eu: 36, us: 5.5, uk: 3.5 },
  37: { eu: 37, us: 6.5, uk: 4.5 },
  38: { eu: 38, us: 7.5, uk: 5.5 },
  39: { eu: 39, us: 8.5, uk: 6.5 },
  40: { eu: 40, us: 9.5, uk: 7.5 },
  41: { eu: 41, us: 10.5, uk: 8.5 },
  42: { eu: 42, us: 11.5, uk: 9.5 },
  43: { eu: 43, us: 12.5, uk: 10.5 },
  44: { eu: 44, us: 13.5, uk: 11.5 },
  45: { eu: 45, us: 14.5, uk: 12.5 },
  46: { eu: 46, us: 15.5, uk: 13.5 },
};

const CATEGORIES = ["Zapatillas", "Casual", "Running", "Training", "Skate", "Basketball"];
const GENDERS = ["Unisex", "Hombre", "Mujer"];

function cleanSizeInput(val) {
  const num = parseFloat(String(val).trim().replace(/[^0-9.]+/g, ''));
  return isNaN(num) ? null : num;
}

function isMatchingSize(s) {
  const inputSize = cleanSizeInput(size.value);
  if (inputSize === null) return false;

  const sizeStr = String(s).trim().toLowerCase();
  const sizeNum = parseFloat(sizeStr);
  if (!isNaN(sizeNum) && Math.abs(sizeNum - inputSize) < 0.1) return true;

  for (const eu of EURO_SIZES) {
    const conv = SIZE_CONVERSIONS[eu];
    for (const system of ['eu', 'us', 'uk']) {
      const cv = conv[system];
      if (Math.abs(cv - inputSize) < 0.1) {
        if (sizeStr.includes(String(eu)) || sizeStr.includes(String(cv))) return true;
        if (!isNaN(sizeNum) && Math.abs(sizeNum - cv) < 0.1) return true;
        break;
      }
    }
  }

  return sizeStr.includes(String(Math.round(inputSize)));
}

function generateSizes(itemSize) {
  const base = parseInt(itemSize, 10);
  if (isNaN(base)) return [itemSize];
  const conv = SIZE_CONVERSIONS[base];
  if (!conv) return [String(base)];
  const result = [String(base)];
  if (conv.us) result.push(`US ${conv.us}`);
  if (conv.uk) result.push(`UK ${conv.uk}`);
  return result;
}

function generateStock() {
  const n = Math.floor(Math.random() * 30) + 1;
  return n > 5 ? `${n} en stock` : 'Agotado';
}

function parseCategory(name) {
  const n = name.toLowerCase();
  if (n.includes('running') || n.includes('pegasus') || n.includes('gel-kayano')) return 'Running';
  if (n.includes('air force') || n.includes('jordan') || n.includes('basketball')) return 'Basketball';
  if (n.includes('skate') || n.includes('old skool')) return 'Skate';
  if (n.includes('sneaker') || n.includes('classic') || n.includes('club')) return 'Zapatillas';
  return 'Casual';
}

function parseGender(name) {
  const n = name.toLowerCase();
  if (n.includes('woman') || n.includes('mujer')) return 'Mujer';
  if (n.includes('man') || n.includes('hombre')) return 'Hombre';
  return 'Unisex';
}

function stockClass(item) {
  if (!item.stock || item.stock === 'Agotado') return 'out-of-stock';
  return 'in-stock';
}

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
  loading.value = false;

  if (!size.value) {
    error.value = "Introduce una talla para buscar.";
    return;
  }

  loading.value = true;

  try {
    const response = await fetch(`/api/stores/?size=${encodeURIComponent(size.value)}`);
    if (!response.ok) {
      throw new Error("Error al cargar el catálogo.");
    }
    const data = await response.json();
    const raw = data.items || [];
    items.value = raw.map((item) => ({
      ...item,
      category: CATEGORIES[Math.floor(Math.random() * CATEGORIES.length)],
      gender: GENDERS[Math.floor(Math.random() * GENDERS.length)],
      sizes: generateSizes(item.size),
      stock: generateStock(),
    }));
  } catch (err) {
    error.value = err.message;
  } finally {
    loaded.value = true;
    loading.value = false;
  }
}
</script>

<style scoped>
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

section > p {
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

label {
  display: grid;
  gap: 0.5rem;
  min-width: 220px;
  color: #232323;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.95rem 1rem;
  border-radius: 18px;
  border: 1px solid rgba(0,0,0,0.12);
  background: #ffffff;
  color: #111111;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

input:focus {
  border-color: rgba(0,0,0,0.24);
  box-shadow: 0 0 0 0.28rem rgba(0,0,0,0.08);
  outline: none;
}

button {
  padding: 0.95rem 1.4rem;
  border-radius: 999px;
  background: #111111;
  color: #f8f2e6;
  box-shadow: 0 18px 30px rgba(0,0,0,0.18);
  border: none;
  cursor: pointer;
  transition: transform 0.22s ease, box-shadow 0.22s ease, opacity 0.22s ease;
  font-family: inherit;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 24px 40px rgba(0,0,0,0.22);
}

button:active:not(:disabled) {
  transform: translateY(0);
}

button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #f8f2e6;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-msg {
  margin-top: 1rem;
  padding: 0.85rem 1.2rem;
  border-radius: 16px;
  background: rgba(180,60,60,0.08);
  color: #8a2e2e;
  border: 1px solid rgba(180,60,60,0.15);
}

.empty-state {
  margin-top: 1.5rem;
  padding: 2.5rem 2rem;
  text-align: center;
  color: #5b5b5b;
  background: rgba(255,255,255,0.5);
  border-radius: 24px;
  border: 1px dashed rgba(0,0,0,0.1);
  font-size: 0.95rem;
}

/* ===== RESULTS PANEL ===== */
.results-panel {
  margin-top: 2rem;
  animation: panelSlideUp 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes panelSlideUp {
  from {
    opacity: 0;
    transform: translateY(200px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.results-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
}

.results-count {
  font-size: 0.85rem;
  color: #5b5b5b;
  background: rgba(255,255,255,0.7);
  padding: 0.35rem 1rem;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.06);
}

.catalog-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 740px) {
  .catalog-list {
    grid-template-columns: 1fr 1fr;
  }
}

/* ===== CARD ===== */
.catalog-card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 24px;
  border: 1px solid rgba(0,0,0,0.07);
  box-shadow: 0 20px 50px rgba(0,0,0,0.06);
  overflow: hidden;
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.3s ease, border-color 0.3s ease;
  animation: cardFadeIn 0.5s ease both;
  animation-delay: var(--delay, 0s);
}

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.catalog-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 30px 70px rgba(0,0,0,0.10);
  border-color: rgba(0,0,0,0.12);
}

.card-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f3ede5;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.catalog-card:hover .card-image img {
  transform: scale(1.07);
}

.card-body {
  padding: 1.15rem 1.25rem 1.3rem;
  display: grid;
  gap: 0.55rem;
}

.field-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.75rem;
}

.field-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #7a7a7a;
  flex-shrink: 0;
}

.field-value {
  font-size: 0.9rem;
  color: #111111;
  text-align: right;
  font-weight: 500;
}

.sizes-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  justify-content: flex-end;
}

.size-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  background: #f0ece6;
  color: #3a3a3a;
  font-size: 0.76rem;
  font-weight: 500;
  transition: background 0.25s ease, color 0.25s ease, transform 0.25s ease;
  white-space: nowrap;
}

.size-badge.active {
  background: #111111;
  color: #f8f2e6;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.price-row {
  border-top: 1px solid rgba(0,0,0,0.06);
  padding-top: 0.6rem;
  margin-top: 0.15rem;
}

.price-val {
  font-size: 1.05rem;
  font-weight: 700;
  color: #111111;
}

.in-stock {
  color: #2a7a3a;
}

.out-of-stock {
  color: #b04848;
}

/* ===== STORE BUTTON ===== */
.store-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 999px;
  background: #111111;
  color: #f8f2e6;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  transition: background 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
}

.store-btn:hover {
  background: #2a2a2a;
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(0,0,0,0.18);
}

.store-btn:active {
  transform: translateY(0);
}

.store-btn svg {
  width: 14px;
  height: 14px;
  transition: transform 0.25s ease;
}

.store-btn:hover svg {
  transform: translate(3px, -3px);
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
