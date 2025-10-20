import { defineStore } from "pinia"
import { ref, computed } from "vue"
import axios from "axios"

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null)
  const token = ref(localStorage.getItem("token"))
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  // Configurar axios con el token
  const setAuthHeader = (authToken) => {
    if (authToken) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${authToken}`
    } else {
      delete axios.defaults.headers.common["Authorization"]
    }
  }

  // Inicializar axios si hay token
  if (token.value) {
    setAuthHeader(token.value)
  }

  const login = async (credentials) => {
    try {
      loading.value = true
      error.value = null

      //const response = await axios.post("/api/auth/login", credentials)
      const response = await axios.post("/auth/login", credentials)
      const { access_token, user: userData } = response.data

      token.value = access_token
      user.value = userData

      localStorage.setItem("token", access_token)
      setAuthHeader(access_token)

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.detail || "Error de autenticación"
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem("token")
    setAuthHeader(null)
  }

  const checkAuth = async () => {
    if (!token.value) return

    try {
      //const response = await axios.get("/api/auth/me")
      const response = await axios.get("/auth/me")
      user.value = response.data
    } catch (err) {
      // Token inválido o expirado
      logout()
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
    checkAuth,
  }
})
