import { defineStore } from "pinia"
import { ref, computed } from "vue"
import axios from "axios"

export const useCompanyStore = defineStore("company", () => {
  const companies = ref([])
  const selectedCompany = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Load selected company from localStorage on initialization
  const savedCompany = localStorage.getItem("selectedCompany")
  if (savedCompany) {
    try {
      selectedCompany.value = JSON.parse(savedCompany)
    } catch (e) {
      console.error("Error parsing saved company:", e)
      localStorage.removeItem("selectedCompany")
    }
  }

  const isCompanySelected = computed(() => !!selectedCompany.value)

  const loadCompanies = async () => {
    try {
      loading.value = true
      error.value = null

      const response = await axios.get("/api/empresas-clientes")
      companies.value = response.data

      // If no company is selected and we have companies, don't auto-select
      // Let the user choose explicitly

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.detail || "Error cargando empresas"
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const selectCompany = (company) => {
    selectedCompany.value = company
    localStorage.setItem("selectedCompany", JSON.stringify(company))
  }

  const clearSelectedCompany = () => {
    selectedCompany.value = null
    localStorage.removeItem("selectedCompany")
  }

  const getCurrentCompanyCode = computed(() => {
    return selectedCompany.value?.codempresa || null
  })

  return {
    companies,
    selectedCompany,
    loading,
    error,
    isCompanySelected,
    getCurrentCompanyCode,
    loadCompanies,
    selectCompany,
    clearSelectedCompany,
  }
})
