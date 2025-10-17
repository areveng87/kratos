<template>
  <Sidebar>
    <!-- Updated header to use theme-responsive classes -->
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold theme-text">Sociedades</h1>
          <p class="text-gray-400">Gestión de sociedades y clientes</p>
        </div>
        <button
          @click="showCreateModal = true"
          class="btn-primary flex items-center space-x-2"
        >
          <Plus class="h-4 w-4" />
          <span>Nueva Sociedad</span>
        </button>
      </div>
    </header>

    <!-- Updated main content to use theme-responsive classes -->
    <main class="flex-1 overflow-y-auto main-content p-6">
      <!-- Updated search and filters section to match card styling -->
      <div class="card p-4 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <input
              v-model="searchText"
              type="text"
              placeholder="Buscar sociedades..."
              class="input-field"
            />
          </div>
          <div>
            <select
              v-model="selectedFondo"
              class="input-field"
            >
              <option value="">Todos los fondos</option>
              <option v-for="fondo in fondos" :key="fondo.id" :value="fondo.id">
                {{ fondo.descripcion }}
              </option>
            </select>
          </div>
          <div>
            <select
              v-model="selectedCartera"
              class="input-field"
            >
              <option value="">Todas las carteras</option>
              <option v-for="cartera in carteras" :key="cartera" :value="cartera">
                {{ cartera }}
              </option>
            </select>
          </div>
          <div>
            <button
              @click="clearFilters"
              class="btn-secondary w-full"
            >
              Limpiar Filtros
            </button>
          </div>
        </div>
      </div>

      <!-- Updated table to match dark theme styling -->
      <!-- <PaginatedTable
        :columns="tableColumns"
        :data="paginatedSociedades"
        :totalPages="totalPages"
        :currentPage="currentPage"
        @pageChange="currentPage = $event"
      >
        <template #nomcli="{ row }">
          <div class="text-center">
            <span v-if="row.nomcli" class="text-gray-200">
              {{ row.nomcli }}
            </span>
            <Minus v-else class="h-4 w-4 text-gray-500 mx-auto" />
          </div>
        </template>

        <template #representante_nombre="{ row }">
          <div class="text-center">
            <span v-if="row.representante_nombre" class="text-gray-200">
              {{ row.representante_nombre }}
            </span>
            <Minus v-else class="h-4 w-4 text-gray-500 mx-auto" />
          </div>
        </template>

        <template #ext_cartera="{ row }">
          <div class="text-center">
            <span v-if="row.ext_cartera" class="text-gray-200">
              {{ row.ext_cartera }}
            </span>
            <Minus v-else class="h-4 w-4 text-gray-500 mx-auto" />
          </div>
        </template>

        <template #analista_nombre="{ row }">
          <div class="text-center">
            <span v-if="row.analista_nombre" class="text-gray-200">
              {{ row.analista_nombre }}
            </span>
            <Minus v-else class="h-4 w-4 text-gray-500 mx-auto" />
          </div>
        </template>

        <template #actions="{ row }">
          <div class="flex items-center space-x-2">
            <button
              @click="editSociedad(row)"
              class="text-indigo-400 hover:text-indigo-300"
              title="Editar sociedad"
            >
              <Edit class="h-4 w-4" />
            </button>
            <button
              @click="deleteSociedad(row)"
              class="text-red-400 hover:text-red-300"
              title="Eliminar sociedad"
            >
              <Trash2 class="h-4 w-4" />
            </button>
          </div>
        </template>
      </PaginatedTable> -->

      <PaginatedTable
  :columns="tableColumns"
  :items="filteredSociedades"      
  :loading="loading"
  :initial-items-per-page="itemsPerPage"
  @page-change="currentPage = $event"           
  @items-per-page-change="itemsPerPage = $event"
  @row-double-click="editSociedad"              
>
  <!-- OJO: slots deben ser cell-<key> y usar { item } -->
  <template #cell-nomcli="{ item }">
    <div>
      <span v-if="item.nomcli" class="text-sm theme-text">{{ item.nomcli }}</span>
      <Minus v-else class="h-4 w-4 text-gray-500 mx-auto" />
    </div>
  </template>

  <template #cell-representante_nombre="{ item }">
    <div>
      <span v-if="item.representante_nombre" class="text-sm theme-text">{{ item.representante_nombre }}</span>
      <Minus v-else class="h-4 w-4 text-gray-500 mx-auto" />
    </div>
  </template>

  <template #cell-ext_cartera="{ item }">
    <div>
      <span v-if="item.ext_cartera" class="text-sm theme-text">{{ item.ext_cartera }}</span>
      <Minus v-else class="h-4 w-4 text-gray-500 mx-auto" />
    </div>
  </template>

  <template #cell-analista_nombre="{ item }">
    <div>
      <span v-if="item.analista_nombre" class="text-sm theme-text">{{ item.analista_nombre }}</span>
      <Minus v-else class="h-4 w-4 text-gray-500 mx-auto" />
    </div>
  </template>

  <template #cell-actions="{ item }">
    <div class="flex items-center space-x-2">
      <button @click="editSociedad(item)" class="text-indigo-400 hover:text-indigo-300" title="Editar sociedad">
        <Edit class="h-4 w-4" />
      </button>
      <button @click="deleteSociedad(item)" class="text-red-400 hover:text-red-300" title="Eliminar sociedad">
        <Trash2 class="h-4 w-4" />
      </button>
    </div>
  </template>
</PaginatedTable>






      <!-- Updated modal to use theme-responsive classes -->
      <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="modal-bg rounded-lg p-6 w-full max-w-md">
          <h3 class="text-lg font-semibold theme-text mb-4">
            {{ showCreateModal ? 'Nueva Sociedad' : 'Editar Sociedad' }}
          </h3>
          
          <form @submit.prevent="showCreateModal ? createSociedad() : updateSociedad()" class="space-y-4">
            <div>
              <label class="block text-sm font-medium modal-label mb-2">Compañía *</label>
              <input
                v-model="formData.nomcli"
                type="text"
                required
                class="input-field"
                placeholder="Nombre de la compañía"
              />
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">Fondo</label>
              <select
                v-model="formData.idrepresen"
                class="input-field"
              >
                <option value="">Seleccionar fondo</option>
                <option v-for="fondo in fondos" :key="fondo.id" :value="fondo.id">
                  {{ fondo.descripcion }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">Cartera</label>
              <input
                v-model="formData.ext_cartera"
                type="text"
                class="input-field"
                placeholder="Nombre de la cartera"
              />
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">Analista</label>
              <select
                v-model="formData.ext_analistapordefecto"
                class="input-field"
              >
                <option value="">Seleccionar analista</option>
                <option v-for="usuario in usuarios" :key="usuario.id" :value="usuario.id">
                  {{ usuario.nombre }} {{ usuario.apellido }}
                </option>
              </select>
            </div>

            <div class="flex justify-end space-x-3">
              <button
                type="button"
                @click="closeModal"
                class="btn-secondary"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="btn-primary"
              >
                {{ saving ? 'Guardando...' : (showCreateModal ? 'Crear' : 'Actualizar') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import PaginatedTable from '../components/PaginatedTable.vue'
import { Plus, Edit, Trash2, Building2, Minus } from 'lucide-vue-next'
import { api } from '../api'

const sociedades = ref([])
const fondos = ref([])
const usuarios = ref([])
const loading = ref(true)
const saving = ref(false)
const searchText = ref('')
const selectedFondo = ref('')
const selectedCartera = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingId = ref(null)

const currentPage = ref(1)
const itemsPerPage = ref(10)

const formData = ref({
  nomcli: '',
  idrepresen: '',
  ext_cartera: '',
  ext_analistapordefecto: ''
})

const carteras = computed(() => {
  const uniqueCarteras = [...new Set(sociedades.value.map(s => s.ext_cartera).filter(Boolean))]
  return uniqueCarteras.sort()
})

const filteredSociedades = computed(() => {
  let filtered = sociedades.value

  console.log("Filtrando sociedades, total inicial:", filtered.length)

  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    filtered = filtered.filter(sociedad =>
      sociedad.nomcli?.toLowerCase().includes(search) ||
      sociedad.fondo_nombre?.toLowerCase().includes(search) ||
      sociedad.ext_cartera?.toLowerCase().includes(search) ||
      sociedad.analista_nombre?.toLowerCase().includes(search)
    )
  }

  if (selectedFondo.value) {
    filtered = filtered.filter(sociedad => sociedad.idrepresen === selectedFondo.value)
  }

  if (selectedCartera.value) {
    filtered = filtered.filter(sociedad => sociedad.ext_cartera === selectedCartera.value)
  }

  console.log("Sociedades tras filtrar:", filtered.length)

  return filtered
})

const totalItems = computed(() =>{ 
  console.log('Total de items:', filteredSociedades.value.length)
  console.log('filter sociedades: ', filteredSociedades.value)
  return filteredSociedades.value.length 
})
const totalPages = computed(() =>{
  let result = Math.ceil(totalItems.value / itemsPerPage.value)

  console.log('Total de páginas:', result)
  return result
})

const paginatedSociedades = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value

  console.log(`Mostrando página ${currentPage.value}, items ${start} a ${end}`)

  let result = filteredSociedades.value.slice(start, end)

  console.log("Sociedades en la página actual:", result)
  return result
})

const loadSociedades = async () => {
  try {
    const response = await api.sociedades.getAll()
    sociedades.value = response.data
  } catch (error) {
    console.error('Error loading sociedades:', error)
  }
}

const loadFondos = async () => {
  try {
    const response = await api.representantes.getAll()
    fondos.value = response.data
  } catch (error) {
    console.error('Error loading fondos:', error)
  }
}

const loadUsuarios = async () => {
  try {
    const response = await api.usuarios.getAll()
    usuarios.value = response.data
  } catch (error) {
    console.error('Error loading usuarios:', error)
  }
}

const clearFilters = () => {
  searchText.value = ''
  selectedFondo.value = ''
  selectedCartera.value = ''
  currentPage.value = 1
}

const resetForm = () => {
  formData.value = {
    nomcli: '',
    idrepresen: '',
    ext_cartera: '',
    ext_analistapordefecto: ''
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingId.value = null
  resetForm()
}

const createSociedad = async () => {
  saving.value = true
  try {
    await api.sociedades.create(formData.value)
    await loadSociedades()
    closeModal()
  } catch (error) {
    console.error('Error creating sociedad:', error)
  } finally {
    saving.value = false
  }
}

const editSociedad = (sociedad) => {
  editingId.value = sociedad.id
  formData.value = {
    nomcli: sociedad.nomcli,
    idrepresen: sociedad.idrepresen,
    ext_cartera: sociedad.ext_cartera,
    ext_analistapordefecto: sociedad.ext_analistapordefecto
  }
  showEditModal.value = true
}

const updateSociedad = async () => {
  saving.value = true
  try {
    await api.sociedades.update(editingId.value, formData.value)
    await loadSociedades()
    closeModal()
  } catch (error) {
    console.error('Error updating sociedad:', error)
  } finally {
    saving.value = false
  }
}

const deleteSociedad = async (sociedad) => {
  if (confirm(`¿Está seguro de eliminar la sociedad "${sociedad.nomcli}"?`)) {
    try {
      await api.sociedades.delete(sociedad.id)
      await loadSociedades()
    } catch (error) {
      console.error('Error deleting sociedad:', error)
    }
  }
}

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      loadSociedades(),
      loadFondos(),
      loadUsuarios()
    ])
  } catch (err) {
    console.error('Error inicializando:', err)
  } finally {
    loading.value = false
  }
})


const tableColumns = [
  { key: 'nomcli', label: 'Compañía' },
  { key: 'representante_nombre', label: 'Fondo' },
  { key: 'ext_cartera', label: 'Cartera' },
  { key: 'analista_nombre', label: 'Analista' },
  { key: 'actions', label: 'Acciones' }
]
</script>
