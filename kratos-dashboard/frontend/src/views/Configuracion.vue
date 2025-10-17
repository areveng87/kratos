<template>
  <Sidebar>
    <!-- Header -->
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold theme-text">Configuración</h1>
          <p class="text-gray-400">Configuración del sistema y perfil de usuario</p>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 overflow-y-auto main-content p-6">
      <div class="max-w-4xl mx-auto space-y-6">
        <!-- User Profile -->
        <div class="card-bg card-border rounded-lg p-6">
          <h3 class="text-lg font-semibold theme-text mb-6">Perfil de Usuario</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Nombre</label>
              <input
                :value="userProfile.nombre"
                type="text"
                class="input-field"
                readonly
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Apellido</label>
              <input
                :value="userProfile.apellido"
                type="text"
                class="input-field"
                readonly
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <input
                :value="userProfile.email"
                type="email"
                class="input-field"
                readonly
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Rol</label>
              <input
                :value="userProfile.rol"
                type="text"
                class="input-field"
                readonly
              />
            </div>
          </div>
        </div>

        <!-- System Settings -->
        <div class="card-bg card-border rounded-lg p-6">
          <h3 class="text-lg font-semibold theme-text mb-6">Configuración del Sistema</h3>
          
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="theme-text font-medium">Notificaciones por Email</h4>
                <p class="text-gray-400 text-sm">Recibir notificaciones de operaciones importantes</p>
              </div>
              <button
                @click="toggleSetting('emailNotifications')"
                :class="getToggleClasses(settings.emailNotifications)"
              >
                <span :class="getToggleSpanClasses(settings.emailNotifications)" />
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <h4 class="theme-text font-medium">Modo Oscuro</h4>
                <p class="text-gray-400 text-sm">Usar tema oscuro en la interfaz</p>
              </div>
              <button
                @click="toggleDarkMode"
                :class="getToggleClasses(themeStore.isDarkMode)"
              >
                <span :class="getToggleSpanClasses(themeStore.isDarkMode)" />
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <h4 class="theme-text font-medium">Auto-guardado</h4>
                <p class="text-gray-400 text-sm">Guardar automáticamente los cambios</p>
              </div>
              <button
                @click="toggleSetting('autoSave')"
                :class="getToggleClasses(settings.autoSave)"
              >
                <span :class="getToggleSpanClasses(settings.autoSave)" />
              </button>
            </div>
          </div>
        </div>

        <!-- Database Status -->
        <div class="card-bg card-border rounded-lg p-6">
          <h3 class="text-lg font-semibold theme-text mb-6">Estado del Sistema</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Base de Datos</span>
                <span class="flex items-center text-green-400">
                  <div class="h-2 w-2 bg-green-400 rounded-full mr-2"></div>
                  Conectada
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">API Backend</span>
                <span class="flex items-center text-green-400">
                  <div class="h-2 w-2 bg-green-400 rounded-full mr-2"></div>
                  Operativa
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Versión</span>
                <span class="theme-text">v1.0.0</span>
              </div>
            </div>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Última Sincronización</span>
                <span class="theme-text">{{ formatTime(new Date()) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Tiempo de Actividad</span>
                <span class="theme-text">24h 15m</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Usuarios Activos</span>
                <span class="theme-text">1</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="card-bg card-border rounded-lg p-6">
          <h3 class="text-lg font-semibold theme-text mb-6">Acciones</h3>
          
          <div class="flex flex-wrap gap-4">
            <button class="btn-secondary flex items-center space-x-2">
              <Download class="h-4 w-4" />
              <span>Exportar Datos</span>
            </button>
            <button class="btn-secondary flex items-center space-x-2">
              <RefreshCw class="h-4 w-4" />
              <span>Sincronizar</span>
            </button>
            <button class="bg-red-600 hover:bg-red-700 text-white font-medium py-2.5 px-4 rounded-lg transition-colors duration-200 flex items-center space-x-2">
              <LogOut class="h-4 w-4" />
              <span>Cerrar Sesión</span>
            </button>
          </div>
        </div>
      </div>
    </main>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'
import Sidebar from '../components/Sidebar.vue'
import { Download, RefreshCw, LogOut } from 'lucide-vue-next'

const authStore = useAuthStore()
const themeStore = useThemeStore()

const userProfile = ref({
  nombre: '',
  apellido: '',
  email: '',
  rol: ''
})

const settings = ref({
  emailNotifications: true,
  autoSave: true
})

const getToggleClasses = (isActive) => [
  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
  isActive ? 'bg-indigo-600' : 'bg-gray-600'
]

const getToggleSpanClasses = (isActive) => [
  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
  isActive ? 'translate-x-6' : 'translate-x-1'
]

const toggleSetting = (setting) => {
  settings.value[setting] = !settings.value[setting]
  console.log(`Setting ${setting} changed to:`, settings.value[setting])
}

const toggleDarkMode = () => {
  themeStore.toggleTheme()
  console.log('Dark mode toggled to:', themeStore.isDarkMode)
}

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('es-CL', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  userProfile.value = {
    nombre: authStore.user.nombre,
    apellido: authStore.user.apellido,
    email: authStore.user.email,
    rol: authStore.user.rol
  }
  
  themeStore.initializeTheme()
})
</script>

<style scoped>
.header-bg {
  background-color: var(--header-bg-color);
}

.header-border {
  border-bottom: 1px solid var(--header-border-color);
}

.main-content {
  background-color: var(--main-content-bg-color);
}

.card-bg {
  background-color: var(--card-bg-color);
}

.card-border {
  border: 1px solid var(--card-border-color);
}

.theme-text {
  color: var(--theme-text-color);
}
</style>
