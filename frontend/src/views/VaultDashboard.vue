<template>
  <div class="flex h-screen bg-gray-900 text-gray-100 font-sans">
    <aside class="w-64 bg-gray-950 border-r border-gray-800 p-6 flex flex-col justify-between">
      <div>
        <div class="flex items-center space-x-3 mb-8">
          <span class="text-2xl">🛡️</span>
          <span class="text-xl font-bold tracking-wider text-emerald-400">ZeroVault</span>
        </div>
        <nav class="space-y-2">
          <a href="#" class="flex items-center space-x-3 px-4 py-2.5 bg-emerald-600/10 text-emerald-400 rounded-lg font-medium transition">
            <span>🔑</span> <span>Todos los Secretos</span>
          </a>
          <a href="#" class="flex items-center space-x-3 px-4 py-2.5 text-gray-400 hover:bg-gray-900 hover:text-gray-200 rounded-lg transition">
            <span>⭐</span> <span>Favoritos</span>
          </a>
        </nav>
      </div>
      <div class="border-t border-gray-800 pt-4 text-sm text-gray-500">
        Sesión Protegida localmente
      </div>
    </aside>

    <main class="flex-1 flex flex-col overflow-hidden">
      <header class="h-16 bg-gray-950/50 border-b border-gray-800 px-8 flex items-center justify-between">
        <div class="w-96">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar credenciales por etiqueta (ej. AWS)..." 
            class="w-full bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-emerald-500 transition"
          />
        </div>
        <button @click="openCreateModal" class="bg-emerald-500 hover:bg-emerald-600 text-gray-950 px-4 py-2 rounded-lg text-sm font-semibold transition shadow-lg shadow-emerald-500/10">
          + Nuevo Secreto
        </button>
      </header>

      <section class="flex-1 overflow-y-auto p-8">
        <div class="max-w-4xl mx-auto">
          <h2 class="text-lg font-semibold mb-4 text-gray-400">Tus Credenciales</h2>
          
          <div class="bg-gray-950 border border-gray-800 rounded-xl divide-y divide-gray-800">
            <div v-for="secret in filteredSecrets" :key="secret.id" class="p-4 flex items-center justify-between hover:bg-gray-900/50 transition">
              <div class="flex items-center space-x-4">
                <div class="w-10 h-10 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg flex items-center justify-center font-bold">
                  {{ secret.label.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <h3 class="font-medium text-gray-200">{{ secret.label }}</h3>
                  <p class="text-xs text-gray-500">Última modificación: {{ secret.updated_at }}</p>
                </div>
              </div>
              <div class="flex space-x-2">
                <button @click="revealSecret(secret.id)" class="px-3 py-1.5 bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-md text-xs font-medium transition">
                  👁️ Mostrar
                </button>
                <button class="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-md text-xs font-medium transition">
                  Eliminar
                </button>
              </div>
            </div>

            <div v-if="filteredSecrets.length === 0" class="p-8 text-center text-gray-500">
              No se encontraron secretos con esa etiqueta.
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Estado reactivo reactivo simulado
const searchQuery = ref('');
const secrets = ref([
  { id: '1', label: 'Consola de AWS - Producción', updated_at: '2026-06-20' },
  { id: '2', label: 'Base de Datos PostgreSQL Finanzas', updated_at: '2026-06-19' },
  { id: '3', label: 'API Key de Stripe', updated_at: '2026-06-15' }
]);

const filteredSecrets = computed(() => {
  return secrets.value.filter(s => 
    s.label.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const revealSecret = (id) => {
  alert(`Invocando desencriptación local en RAM con DEK para el ID: ${id}`);
};

const openCreateModal = () => {
  alert("Modal de creación: Los datos aquí escritos se cifrarán con AES-GCM antes de enviarse al backend.");
};
</script>