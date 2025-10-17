<template>
  <div class="company-selector-container">
    <div class="flex items-center space-x-3">
      <Building2 class="h-5 w-5 text-gray-400" />
      <div class="flex items-center space-x-2">
        <span class="text-sm font-medium text-gray-400">Empresa:</span>
        <select
          v-model="selectedCompanyModel"
          @change="handleCompanyChange"
          class="company-select"
          :disabled="loading || !canSelectCompany"
        >
          <option value="">Seleccionar empresa...</option>
          <option
            v-for="company in companies"
            :key="company.codempresa"
            :value="company.codempresa"
          >
            {{ company.nomempresa }}
          </option>
        </select>
      </div>
      <div v-if="loading" class="flex items-center">
        <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-indigo-500"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCompanyStore } from '../stores/company'
import { useAuthStore } from '../stores/auth'
import { Building2 } from 'lucide-vue-next'

const companyStore = useCompanyStore()
const authStore = useAuthStore()

const selectedCompanyModel = ref('')

const canSelectCompany = computed(() => {
  const userRole = authStore.user?.rol
  return userRole === 'Administrador' || userRole === 'Servicer Supervisor'
})

const companies = computed(() => companyStore.companies)
const loading = computed(() => companyStore.loading)

watch(() => companyStore.selectedCompany, (newCompany) => {
  selectedCompanyModel.value = newCompany?.codempresa || ''
}, { immediate: true })

const handleCompanyChange = () => {
  if (selectedCompanyModel.value) {
    const company = companies.value.find(c => c.codempresa === selectedCompanyModel.value)
    if (company) {
      companyStore.selectCompany(company)
      emit('company-changed', company)
    }
  } else {
    companyStore.clearSelectedCompany()
    emit('company-changed', null)
  }
}

const emit = defineEmits(['company-changed'])

onMounted(async () => {
  await companyStore.loadCompanies()
})
</script>

<style scoped>
.company-selector-container {
  padding: 0.75rem 1.5rem;
  background-color: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border);
}

.company-select {
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  padding: 0.375rem 0.75rem;
  color: var(--color-text-primary);
  font-size: 0.875rem;
  min-width: 200px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.company-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 243, 0.1);
}

.company-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
