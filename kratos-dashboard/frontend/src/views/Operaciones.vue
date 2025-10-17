<template>
  <Sidebar>
    <!-- Header -->
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold theme-text">Operaciones</h1>
          <p class="text-gray-400">Gestión de operaciones comerciales</p>
        </div>
        <button
          @click="handleShowCreateModal"
          class="btn-primary flex items-center space-x-2"
        >
          <Plus class="h-4 w-4" />
          <span>Nueva Operación</span>
        </button>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 overflow-y-auto main-content p-6">
      <!-- Updated filters to match the image design -->
      <div class="card p-4 mb-6">
        <div class="flex flex-wrap items-center gap-4">
          <!-- Global search - moved to first position -->
          <div class="flex items-center space-x-2">
            <label class="text-sm font-medium theme-text">Buscar:</label>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Buscar en todas las columnas..."
              class="input-field min-w-64"
              @input="debounceSearch"
            />
          </div>

          <!-- Estados filter -->
          <div class="flex items-center space-x-2">
            <label class="text-sm font-medium theme-text">Estados:</label>
            <select v-model="filters.estado" class="input-field min-w-48" @change="loadOperaciones">
              <option value="">Todos los estados</option>
              <option value="Analizando Riesgos">Analizando Riesgos</option>
              <option value="Sin Hitos">Sin Hitos</option>
              <option value="Elevado a OCI">Elevado a OCI</option>
              <option value="En Proceso">En Proceso</option>
              <option value="Aprobado">Aprobado</option>
            </select>
          </div>

          <!-- Referencia Expediente filter -->
          <div class="flex items-center space-x-2">
            <label class="text-sm font-medium theme-text">Referencia Expediente:</label>
            <input
              v-model="filters.referencia_expediente"
              type="text"
              placeholder="Buscar referencia..."
              class="input-field min-w-48"
              @input="debounceSearch"
            />
          </div>

          <!-- Analista filter -->
          <div class="flex items-center space-x-2">
            <label class="text-sm font-medium theme-text">Analista:</label>
            <input
              v-model="filters.analista"
              type="text"
              placeholder="Nombre del analista..."
              class="input-field min-w-48"
              @input="debounceSearch"
            />
          </div>

          <!-- Sin Analista checkbox -->
          <div class="flex items-center space-x-2">
            <input
              v-model="filters.sin_analista"
              type="checkbox"
              id="sin-analista"
              class="rounded border-gray-300"
              @change="loadOperaciones"
            />
            <label for="sin-analista" class="text-sm font-medium theme-text">Sin Analista</label>
          </div>
        </div>
      </div>

      <!-- Updated table structure to match the image columns -->
      <div class="card overflow-hidden">
        <PaginatedTable
          :items="paginatedOperaciones"
          :columns="tableColumns"
          :loading="loading"
          :empty-text="'No se encontraron operaciones'"
          :loading-text="'Cargando operaciones...'"
          @row-double-click="handleRowDoubleClick"
        >
          <!-- Custom slot for estado column with styled span and Minus icon -->
          <template #cell-estado="{ item }">
            <span 
              v-if="item.estado" 
              class="inline-flex px-2 py-1 text-xs font-semibold rounded"
              :class="getEstadoClass(item.estado)"
            >
              {{ item.estado }}
            </span>
            <div v-else class="flex justify-center">
              <Minus class="h-4 w-4 text-gray-400" />
            </div>
          </template>

          <!-- Custom slot for urgente column with icons -->
          <template #cell-urgente="{ item }">
            <div class="flex justify-center">
              <AlertTriangle 
                v-if="item.urgente" 
                class="h-4 w-4 text-red-500" 
                :title="'Operación urgente'"
              />
              <Minus 
                v-else 
                class="h-4 w-4 text-gray-400" 
                :title="'No urgente'"
              />
            </div>
          </template>
        </PaginatedTable>
      </div>
    </main>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import PaginatedTable from '../components/PaginatedTable.vue'
import { Plus, AlertTriangle, Minus } from 'lucide-vue-next'
import { api } from '../api'

const router = useRouter()

const operaciones = ref([])
const loading = ref(true)
const showCreateModal = ref(false)

const currentPage = ref(1)
const itemsPerPage = ref(10)

const filters = ref({
  estado: '',
  referencia_expediente: '',
  analista: '',
  sin_analista: false,
  search: ''
})

let searchTimeout = null

const debounceSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadOperaciones()
  }, 500)
}

const filteredOperaciones = computed(() => {
  return operaciones.value.filter(op => {
    if (filters.value.estado && op.estado !== filters.value.estado) return false
    if (filters.value.referencia_expediente && op.referencia_expediente !== filters.value.referencia_expediente) return false
    if (filters.value.analista && op.analista_pbc_nombre !== filters.value.analista) return false
    if (filters.value.sin_analista && op.analista_pbc_nombre) return false
    if (filters.value.search && !Object.values(op).some(value => value.toString().toLowerCase().includes(filters.value.search.toLowerCase()))) return false
    return true
  })
})

const totalItems = computed(() => filteredOperaciones.value.length)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))

const paginatedOperaciones = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredOperaciones.value.slice(start, end)
})

const loadOperaciones = async () => {
  loading.value = true
  try {
    const params = {}
    
    // Only add non-empty filters
    if (filters.value.estado) params.estado = filters.value.estado
    if (filters.value.referencia_expediente) params.referencia_expediente = filters.value.referencia_expediente
    if (filters.value.analista) params.analista = filters.value.analista
    if (filters.value.sin_analista) params.sin_analista = filters.value.sin_analista
    if (filters.value.search) params.search = filters.value.search

    const response = await api.operaciones.getPlanner(params)
    operaciones.value = response.data
  } catch (error) {
    console.error('Error loading planner operations:', error)
    operaciones.value = []
  } finally {
    loading.value = false
  }
}

const tableColumns = [
  { 
    key: 'fecha_prevista_firma', 
    label: 'Fecha Prevista Firma',
    headerClass: 'bg-yellow-100',
    cellClass: 'theme-text font-medium bg-yellow-50'
  },
  { key: 'servicer', label: 'Servicer' },
  { key: 'fecha_util_cambio', label: 'Fecha útil cambio' },
  { key: 'tipo_operacion', label: 'Tipo de operación' },
  { key: 'referencia_expediente', label: 'Referencia expediente' },
  { key: 'sociedad', label: 'Sociedad' },
  { key: 'estado', label: 'ESTADO' },
  { key: 'analista_pbc_nombre', label: 'Analista PBC' },
  { key: 'urgente', label: 'Urgente', cellClass: 'text-center' }
]

const getEstadoClass = (estado) => {
  const estadoClasses = {
    'Analizando Riesgos': 'bg-yellow-100 text-yellow-800',
    'Sin Hitos': 'bg-gray-100 text-gray-800',
    'Elevado a OCI': 'bg-red-100 text-red-800',
    'En Proceso': 'bg-blue-100 text-blue-800',
    'Aprobado': 'bg-green-100 text-green-800'
  }
  return estadoClasses[estado] || 'bg-gray-100 text-gray-800'
}

const handleRowDoubleClick = (operacion) => {
  router.push({ name: 'DetallesOperacion', params: { id: operacion.id } })
}

const handleShowCreateModal = () => {
  showCreateModal.value = true
}

onMounted(async () => {
  await loadOperaciones()
})
</script>

<style scoped>
.header-bg {
  background-color: var(--color-bg-secondary);
}

.header-border {
  border-bottom: 1px solid var(--color-border);
}

.main-content {
  background-color: var(--color-bg-primary);
}

.card {
  border-radius: 0.5rem;
  border: 1px solid var(--color-border);
  background-color: var(--color-bg-primary);
}

.table-header {
  background-color: var(--color-bg-secondary);
}

.table-header-text {
  color: var(--color-text-secondary);
}

.table-border {
  border-color: var(--color-border);
}

.table-row-hover {
  transition: background-color 0.3s;
}

.table-row-hover:hover {
  background-color: var(--color-row-hover);
}

.table-divider {
  border-color: var(--color-border);
}

.input-field {
  border: 1px solid var(--color-border);
  border-radius: 0.25rem;
  padding: 0.5rem;
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
}

.input-field:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 1px var(--color-primary);
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary:hover {
  opacity: 0.9;
}

.theme-text {
  color: var(--color-text-primary);
}

/* Special styling for fecha prevista firma column */
.bg-yellow-50 {
  background-color: #fefce8;
}

.bg-yellow-100 {
  background-color: #fef3c7;
}

/* Added pagination styles matching sociedades */
.pagination-bg {
  background-color: var(--color-bg-secondary);
}

.pagination-border {
  border-top: 1px solid var(--color-border);
}

.pagination-select {
  border: 1px solid var(--color-border);
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-size: 0.875rem;
}

.pagination-button {
  border: 1px solid var(--color-border);
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: var(--color-bg-secondary);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
