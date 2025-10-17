<template>
  <div
    class="min-h-screen relative flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8
           bg-fixed bg-cover bg-center bg-no-repeat"
    :style="{ backgroundImage: `url(${bg})` }">
  <!-- Fondo -->
  <div class="absolute inset-0 -z-10 bg-[url('${bg}')] bg-cover bg-center bg-no-repeat" ></div>
  <!-- Overlay claro para legibilidad -->
  <div class="absolute inset-0 -z-10 bg-white/45"></div>

    <div class="max-w-md w-full space-y-8">
      <!-- Logo y título -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 bg-indigo-600 rounded-xl flex items-center justify-center mb-6">
          <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-white">Kratos</h2>
        <p class="mt-2 text-gray-400">Sistema de Gestión de Muebles</p>
      </div>

      <!-- Formulario de login -->
      <div class="card p-8">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
              Correo electrónico
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="input-field"
              placeholder="admin@kratos.com"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
              Contraseña
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="input-field"
              placeholder="••••••••"
            />
          </div>

          <!-- Error message -->
          <div v-if="authStore.error" class="bg-red-900 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
            {{ authStore.error }}
          </div>

          <button
            type="submit"
            :disabled="authStore.loading"
            class="btn-primary w-full flex justify-center items-center"
          >
            <svg v-if="authStore.loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ authStore.loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}
          </button>
        </form>

        <!-- Credenciales de prueba -->
        <div class="mt-6 p-4 bg-gray-700 rounded-lg">
          <p class="text-sm text-gray-300 mb-2">Credenciales de prueba:</p>
          <p class="text-xs text-gray-400">Email: admin@kratos.com</p>
          <p class="text-xs text-gray-400">Password: admin123</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import bg from '../../../public/images/bg.png'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const handleLogin = async () => {
  const result = await authStore.login(form.value)
  
  if (result.success) {
    router.push('/')
  }
}

onMounted(() => {
  // Limpiar errores previos
  authStore.error = null
})
</script>
