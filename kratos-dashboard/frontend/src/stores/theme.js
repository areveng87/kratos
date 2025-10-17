import { defineStore } from "pinia"
import { ref, watch } from "vue"

export const useThemeStore = defineStore("theme", () => {
  const isDarkMode = ref(true) // Default to dark mode

  // Initialize theme from localStorage or default to dark
  const initializeTheme = () => {
    const savedTheme = localStorage.getItem("theme")
    if (savedTheme) {
      isDarkMode.value = savedTheme === "dark"
    }
    applyTheme()
  }

  // Apply theme to document
  const applyTheme = () => {
    if (isDarkMode.value) {
      document.documentElement.classList.add("dark")
      document.documentElement.classList.remove("light")
    } else {
      document.documentElement.classList.add("light")
      document.documentElement.classList.remove("dark")
    }
  }

  // Toggle theme
  const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem("theme", isDarkMode.value ? "dark" : "light")
    applyTheme()
  }

  // Set specific theme
  const setTheme = (theme) => {
    isDarkMode.value = theme === "dark"
    localStorage.setItem("theme", theme)
    applyTheme()
  }

  // Watch for changes and apply theme
  watch(isDarkMode, () => {
    applyTheme()
  })

  return {
    isDarkMode,
    initializeTheme,
    toggleTheme,
    setTheme,
  }
})
