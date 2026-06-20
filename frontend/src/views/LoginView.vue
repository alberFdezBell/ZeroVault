<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="bg-gray-950 border border-gray-800 rounded-xl p-8 shadow-2xl">
        <!-- Logo -->
        <div class="flex items-center justify-center space-x-3 mb-8">
          <span class="text-4xl">🛡️</span>
          <span class="text-2xl font-bold tracking-wider text-emerald-400">ZeroVault</span>
        </div>

        <p class="text-center text-gray-400 mb-8">Gestor seguro de secretos con cifrado de cliente</p>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-950/50 border border-red-900 rounded-lg text-red-300 text-sm">
          {{ errorMessage }}
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Email Input -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Correo Electrónico</label>
            <input
              v-model="email"
              type="email"
              placeholder="usuario@empresa.com"
              class="w-full bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 text-gray-100 placeholder-gray-600 focus:outline-none focus:border-emerald-500 transition"
              required
            />
          </div>

          <!-- Password Input -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Contraseña Maestra</label>
            <input
              v-model="password"
              type="password"
              placeholder="Tu contraseña maestra"
              class="w-full bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 text-gray-100 placeholder-gray-600 focus:outline-none focus:border-emerald-500 transition"
              required
            />
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-emerald-500/50 text-gray-950 px-4 py-3 rounded-lg font-semibold transition mt-6 shadow-lg shadow-emerald-500/10"
          >
            {{ loading ? '⏳ Autenticando...' : '🔓 Acceder' }}
          </button>
        </form>

        <!-- Demo Credentials -->
        <div class="mt-8 p-4 bg-blue-950/30 border border-blue-900/50 rounded-lg text-sm text-blue-300">
          <p class="font-semibold mb-2">🧪 Demo - Credenciales de Prueba:</p>
          <p>Email: <code class="bg-gray-900 px-2 py-1 rounded">empleado@empresa.com</code></p>
          <p>Password: <code class="bg-gray-900 px-2 py-1 rounded">demo123456</code></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../api'
import { deriveMasterKey, generateAuthenticationHash } from '../crypto/vaultCrypto'

const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    // Step 1: Get master key salt from server
    const preLoginResponse = await authService.preLogin(email.value)
    const masterKeySalt = preLoginResponse.data.master_key_salt

    // Step 2: Derive master key locally
    const masterKey = await deriveMasterKey(password.value, masterKeySalt)

    // Step 3: Generate authentication hash
    const authHash = await generateAuthenticationHash(masterKey, email.value)

    // Step 4: Send login request
    const loginResponse = await authService.login(email.value, authHash)

    // Step 5: Store token and user info
    localStorage.setItem('access_token', loginResponse.data.access_token)
    localStorage.setItem('user_id', loginResponse.data.user_id)
    localStorage.setItem('user_role', loginResponse.data.role)
    localStorage.setItem('user_email', email.value)

    // Step 6: Redirect based on role
    if (loginResponse.data.role === 'admin') {
      router.push('/admin')
    } else {
      router.push('/vault')
    }
  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = error.response?.data?.detail || 'Error al autenticarse. Verifica tu email y contraseña.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
code {
  font-family: monospace;
}
</style>
