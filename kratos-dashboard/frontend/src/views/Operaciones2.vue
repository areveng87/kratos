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
          @click="showCreateModal = true"
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
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="table-header table-border">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Fecha Prevista Firma
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Servicer
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Fecha útil cambio
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Tipo de operación
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Referencia expediente
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Sociedad
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  ESTADO
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Analista PBC
                </th>
                <th class="px-4 py-3 text-center text-xs font-medium table-header-text uppercase tracking-wider">
                  Urgente
                </th>
                <th class="px-4 py-3 text-center text-xs font-medium table-header-text uppercase tracking-wider">
                  Acción
                </th>
              </tr>
            </thead>
            <tbody class="table-divider">
              <tr
                v-for="operacion in paginatedOperaciones"
                :key="operacion.id"
                class="transition-colors hover:bg-[#6366f3] hover:text-white cursor-pointer"
                @dblclick="handleRowDoubleClick(operacion)"
                tabindex="0"
                @keyup.enter="handleRowDoubleClick(operacion)"  
              ><!-- opcional: accesible con Enter -->
                <td class="px-4 py-3 whitespace-nowrap text-sm theme-text font-medium">
                  {{ formatDate(operacion.fecha_prevista_firma) }}
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                  <div v-if="!operacion.servicer" class="flex justify-center">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                  <span v-else class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                    {{ operacion.servicer }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                  <div v-if="!formatDate(operacion.fecha_util_cambio)" class="flex justify-center">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                  <span v-else class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                    {{ formatDate(operacion.fecha_util_cambio) }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                  <div v-if="!operacion.tipo_operacion" class="flex justify-center">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                  <span v-else class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                    {{ operacion.tipo_operacion }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                  <div v-if="!operacion.referencia_expediente" class="flex justify-center">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                  <span v-else class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                    {{ operacion.referencia_expediente }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                  <div v-if="!operacion.sociedad" class="flex justify-center">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                  <span v-else class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                    {{ operacion.sociedad }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <div v-if="!operacion.estado" class="flex justify-center">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                  <span v-else class="inline-flex px-2 py-1 text-xs font-semibold rounded"
                    :class="getEstadoClass(operacion.estado)">
                    {{ operacion.estado }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                  <div v-if="!operacion.analista_pbc_nombre" class="flex justify-center">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                  <span v-else class="px-4 py-3 whitespace-nowrap text-sm theme-text">
                    {{ operacion.analista_pbc_nombre }}
                  </span>
                </td>
                <!-- Replaced text with icons for urgente column -->
                <td class="px-4 py-3 whitespace-nowrap text-center">
                  <div class="flex justify-center items-center">
                    <AlertTriangle 
                      v-if="operacion.urgente" 
                      class="h-5 w-5 text-red-500" 
                      :title="'Urgente'"
                    />
                    <Minus 
                      v-else 
                      class="h-5 w-5 text-gray-400" 
                      :title="'No urgente'"
                    />
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex items-center space-x-2">
                    <button class="text-indigo-400 hover:text-indigo-300">
                      <Edit class="h-4 w-4" />
                    </button>
                    <button class="text-red-400 hover:text-red-300">
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Loading state -->
        <div v-if="loading" class="flex justify-center items-center py-8">
          <div class="text-gray-500">Cargando operaciones...</div>
        </div>

<!-- Empty state -->
        <div v-else-if="filteredOperaciones.length === 0" class="flex justify-center items-center py-8">
          <div class="text-gray-500">No se encontraron operaciones</div>
        </div>

        <!-- Added pagination controls matching sociedades pattern -->
        <div class="pagination-bg px-6 py-3 pagination-border flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-400">Mostrar</span>
            <select v-model="itemsPerPage" @change="currentPage = 1" class="pagination-select">
              <option :value="10">10</option>
              <option :value="50">50</option>
              <option :value="100">100</option>
            </select>
            <span class="text-sm text-gray-400">de {{ totalItems }} registros</span>
          </div>
          
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-400">
              Página {{ currentPage }} de {{ totalPages }}
            </span>
            <div class="flex space-x-1">
              <button
                @click="currentPage = 1"
                :disabled="currentPage === 1"
                class="pagination-button"
              >
                ««
              </button>
              <button
                @click="currentPage--"
                :disabled="currentPage === 1"
                class="pagination-button"
              >
                «
              </button>
              <button
                @click="currentPage++"
                :disabled="currentPage === totalPages"
                class="pagination-button"
              >
                »
              </button>
              <button
                @click="currentPage = totalPages"
                :disabled="currentPage === totalPages"
                class="pagination-button"
              >
                »»
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Removed modal since this view is now read-only for planner data -->
    </main>
  </Sidebar>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { Plus, AlertTriangle, Minus, Edit, Trash2 } from 'lucide-vue-next'
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
  return operaciones.value
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

const getEstadoClass = (estado) => {
  switch (estado) {
    case 'Analizando Riesgos':
      return 'bg-orange-100 text-orange-800'
    case 'Sin Hitos':
      return 'bg-gray-100 text-gray-800'
    case 'Elevado a OCI':
      return 'bg-blue-100 text-blue-800'
    case 'En Proceso':
    case 'En proceso':
      return 'bg-yellow-100 text-yellow-800'
    case 'Aprobado':
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const handleRowDoubleClick = (operacion) => {

  console.log('Doble clic en operación:', operacion)

  router.push({ name: 'DetallesOperacion', params: { id: operacion.id } })
}

const formatDate = (date) => {
  if (!date) return null
  return new Date(date).toLocaleDateString('es-CL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
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

/* .table-row-hover {
  transition: background-color 0.3s;
}

.table-row-hover:hover {
  background-color: var(--color-row-hover);
} */

.table-row-hover {
  transition: background-color 0.3s;
}
.table-row-hover:hover {
  background-color: var(--color-row-hover, rgba(3,85,161,.08)); /* fallback si no hay variable */
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
