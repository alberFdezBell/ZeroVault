<template>
  <div class="min-h-screen bg-gray-900">
    <VaultDashboard v-if="!isAdmin" />
    <AdminDashboard v-else />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VaultDashboard from './views/VaultDashboard.vue'
import AdminDashboard from './views/AdminDashboard.vue'

const isAdmin = ref(false)
</script>

<style scoped>
</style>
