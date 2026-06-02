<template>
  <section>
    <h1>Escáner de pie</h1>
    <p>Sube una foto de tu pie o introduce su URL para calcular tu talla recomendada con IA.</p>
    
    <div class="tabs">
      <button :class="{ active: scanMode === 'file' }" @click="selectMode('file')">Subir archivo</button>
      <button :class="{ active: scanMode === 'url' }" @click="selectMode('url')">Usar URL</button>
    </div>

    <!-- Modo subir archivo (Por defecto y recomendado) -->
    <div v-if="scanMode === 'file'" class="upload-container">
      <div 
        class="dropzone" 
        :class="{ dragging: isDragging }"
        @dragover.prevent="isDragging = true"
        @dragleave="isDragging = false"
        @drop.prevent="handleDrop"
        @click="$refs.fileInput.click()"
      >
        <input 
          ref="fileInput" 
          type="file" 
          accept="image/*" 
          style="display: none" 
          @change="handleFileChange" 
        />
        <div v-if="!previewUrl" class="dropzone-prompt">
          <svg style="width:48px;height:48px;color:#7094ff;margin-bottom:1rem;" viewBox="0 0 24 24"><path fill="currentColor" d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/></svg>
          <p>Arrastra tu foto aquí o haz clic para buscar</p>
          <span class="file-limits">Soporta JPG, PNG (Max 5MB)</span>
        </div>
        <img v-else :src="previewUrl" class="image-preview" alt="Vista previa del pie" />
      </div>
      
      <button 
        type="button" 
        class="btn-scan" 
        :disabled="!uploadFile || isAnalyzing" 
        @click="submitFile"
      >
        {{ isAnalyzing ? 'Analizando...' : 'Calcular talla' }}
      </button>
    </div>

    <!-- Modo URL -->
    <div v-else>
      <form @submit.prevent="submitImage">
        <label>
          URL de la imagen del pie
          <input v-model="imageUrl" type="url" placeholder="https://..." required />
        </label>
        <div class="samples">
          <span>Fotos de prueba rápidas:</span>
          <button type="button" class="btn-sample" @click="useSample('https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600')">
            Modelo A (Talla 42)
          </button>
          <button type="button" class="btn-sample" @click="useSample('https://images.unsplash.com/photo-1560343090-f0409e92791a?w=600')">
            Modelo B (Talla 40)
          </button>
        </div>
        <button type="submit" :disabled="isAnalyzing">
          {{ isAnalyzing ? 'Analizando...' : 'Calcular talla' }}
        </button>
      </form>
    </div>

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

const scanMode = ref("file");
const imageUrl = ref("");
const uploadFile = ref(null);
const previewUrl = ref("");
const isDragging = ref(false);
const isAnalyzing = ref(false);

const result = ref(null);
const error = ref("");
const store = useUserStore();

function selectMode(mode) {
  scanMode.value = mode;
  error.value = "";
  result.value = null;
}

function handleFileChange(event) {
  const file = event.target.files[0];
  if (file && file.type.startsWith("image/")) {
    uploadFile.value = file;
    previewUrl.value = URL.createObjectURL(file);
    result.value = null;
    error.value = "";
  }
}

function handleDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) {
    uploadFile.value = file;
    previewUrl.value = URL.createObjectURL(file);
    result.value = null;
    error.value = "";
  }
}

function useSample(url) {
  imageUrl.value = url;
}

async function submitFile() {
  if (!uploadFile.value) return;
  error.value = "";
  result.value = null;
  isAnalyzing.value = true;

  const formData = new FormData();
  formData.append("file", uploadFile.value);

  try {
    const response = await fetch("/api/measure/upload", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error("Error al procesar la imagen subida.");
    }
    const data = await response.json();
    result.value = data;
    store.setSize(data.shoe_size);
  } catch (err) {
    error.value = err.message;
  } finally {
    isAnalyzing.value = false;
  }
}

async function submitImage() {
  error.value = "";
  result.value = null;
  isAnalyzing.value = true;

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
  } finally {
    isAnalyzing.value = false;
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
.tabs {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 0.75rem;
}
.tabs button {
  background: transparent;
  color: #a4b3e6;
  border: none;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0.5rem 1.1rem;
  border-radius: 10px;
  box-shadow: none;
  transition: color 0.2s, background-color 0.2s;
  align-self: auto;
}
.tabs button:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.04);
}
.tabs button.active {
  color: #fff;
  background: rgba(78, 152, 255, 0.16);
  border: 1px solid rgba(78, 152, 255, 0.3);
}
.upload-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 1.5rem;
}
.dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 240px;
  background: rgba(16, 23, 45, 0.84);
  border: 2px dashed rgba(123, 145, 255, 0.25);
  border-radius: 28px;
  cursor: pointer;
  padding: 2rem;
  transition: border-color 0.25s ease, background-color 0.25s ease, transform 0.25s ease;
  overflow: hidden;
  text-align: center;
}
.dropzone:hover,
.dropzone.dragging {
  border-color: rgba(75, 164, 255, 0.8);
  background-color: rgba(20, 29, 56, 0.88);
}
.dropzone.dragging {
  transform: scale(0.99);
}
.dropzone-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.dropzone-prompt p {
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #eef2ff;
}
.file-limits {
  font-size: 0.85rem;
  color: #8b99c7;
}
.image-preview {
  max-width: 100%;
  max-height: 220px;
  border-radius: 18px;
  object-fit: contain;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}
.btn-scan {
  align-self: center;
  padding: 0.95rem 2.2rem;
  background: linear-gradient(135deg, #3567ff, #1ab7d3);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 18px 30px rgba(7, 81, 190, 0.24);
  cursor: pointer;
  border-radius: 999px;
  border: none;
  font-size: 1rem;
}
.btn-scan:hover {
  box-shadow: 0 24px 40px rgba(7, 81, 190, 0.32);
}
.btn-scan:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
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
button[type="submit"] {
  align-self: start;
  padding: 0.95rem 1.4rem;
  background: linear-gradient(135deg, #3567ff, #1ab7d3);
  color: #fff;
  box-shadow: 0 18px 30px rgba(7, 81, 190, 0.24);
  font-weight: 600;
}
button[type="submit"]:hover {
  box-shadow: 0 24px 40px rgba(7, 81, 190, 0.32);
}
.samples {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  margin: 0.5rem 0 1rem 0;
}
.samples span {
  font-size: 0.85rem;
  color: #a4b3e6;
  margin-right: 0.5rem;
}
.btn-sample {
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #cdd8ff;
  cursor: pointer;
  box-shadow: none;
  align-self: auto;
}
.btn-sample:hover {
  background: rgba(75, 164, 255, 0.2);
  border-color: rgba(75, 164, 255, 0.4);
  color: #fff;
  box-shadow: none;
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
