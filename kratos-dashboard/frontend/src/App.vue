<template>
  <div id="app" class="min-h-screen transition-colors duration-300" :class="themeClasses">
    <router-view />
    <Toaster />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'

import Toaster from './components/Toaster.vue'

const authStore = useAuthStore()
const themeStore = useThemeStore()

// Computed property for theme classes
const themeClasses = computed(() => ({
  'dark bg-gray-900': themeStore.isDarkMode,
  'light bg-gray-50': !themeStore.isDarkMode
}))

themeStore.initializeTheme()

onMounted(async () => {
  // Verificar si hay un token guardado al iniciar la app
  await authStore.checkAuth()
})
</script>
