<template>
  <Sidebar>
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold theme-text">Árbol de Carpetas</h1>
          <p class="text-gray-400">Gestión de estructuras de carpetas y módulos</p>
        </div>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto main-content p-6 space-y-6">
      <!-- Tabla de Módulos -->
      <div class="card overflow-hidden">
        <div class="px-6 py-4 table-header table-border">
          <h2 class="text-lg font-semibold theme-text">Módulos del Sistema</h2>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="table-header table-border">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Módulo</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Estructura Asignada</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="table-divider">
              <tr
                v-for="modulo in modulos"
                :key="modulo.idmodulo"
                class="table-row-hover transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium theme-text">{{ modulo.descripcion }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div v-if="modulo.estructura_raiz_nombre" class="text-sm theme-text">
                    {{ modulo.estructura_raiz_nombre }}
                  </div>
                  <div v-else class="text-sm text-gray-400">Sin asignar</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex items-center space-x-2">
                    <button
                      v-if="!modulo.estructura_raiz_id"
                      @click="abrirAsignarModal(modulo)"
                      class="text-indigo-400 hover:text-indigo-300"
                      title="Asignar estructura"
                    >
                      <Plus class="h-4 w-4" />
                    </button>
                    <button
                      v-else
                      @click="desasignarEstructura(modulo.idmodulo)"
                      class="text-red-400 hover:text-red-300"
                      title="Desasignar estructura"
                    >
                      <X class="h-4 w-4" />
                    </button>
                    <!-- Modal -->
                    <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                      <div class="rounded-lg p-6 w-96"
                          style="background-color: var(--color-bg-secondary); border:1px solid var(--color-border);">
                        <h3 class="text-lg font-semibold theme-text mb-3">Confirmar acción</h3>
                        <p class="theme-text mb-6">{{ message }}</p>
                        <div class="flex justify-end gap-2">
                          <button @click="cancel" class="btn-secondary">Cancelar</button>
                          <button @click="accept" class="btn-primary">Sí, desasignar</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Botón para crear nueva estructura -->
      <div class="flex justify-end">
        <button
          @click="crearNuevaEstructura"
          class="btn-primary flex items-center space-x-2"
        >
          <Plus class="h-4 w-4" />
          <span>Nueva Estructura</span>
        </button>
      </div>

      <!-- Tabla de Estructuras Raíz -->
      <div class="card overflow-hidden">
        <div class="px-6 py-4 table-header table-border">
          <h2 class="text-lg font-semibold theme-text">Estructuras de Carpetas</h2>
        </div>

        <!-- Buscador -->
        <div class="px-6 py-4">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Buscar estructuras..."
            class="input-field"
          />
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="table-header table-border">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Nombre</th>
                <!-- <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Módulo Asignado</th> -->
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Estado</th>
                <th class="px-6 py-3 text-center text-xs font-medium table-header-text uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="table-divider">
              <tr
                v-for="estructura in paginatedEstructuras"
                :key="estructura.idcarpeta"
                @dblclick="editarEstructura(estructura.idcarpeta)"
                class="table-row-hover transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <FolderGit2 class="h-5 w-5 text-indigo-400 mr-2" />
                    <div class="text-sm font-medium theme-text">{{ estructura.nombre }}</div>
                  </div>
                </td>
                <!-- <td class="px-6 py-4 whitespace-nowrap">
                  <div v-if="estructura.modulo_nombre" class="text-sm theme-text">
                    {{ estructura.modulo_nombre }}
                  </div>
                  <div v-else class="text-sm text-gray-400">Sin asignar</div>
                </td> -->
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="inline-flex px-2 py-1 text-xs font-semibold rounded"
                    :class="estructura.activa ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800'"
                  >
                    {{ estructura.activa ? 'Activa' : 'Inactiva' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-right">
                  <div class="flex items-center space-x-2 justify-center">
                    <button
                      @click="editarEstructura(estructura.idcarpeta)"
                      class="text-indigo-400 hover:text-indigo-300"
                      title="Editar estructura"
                    >
                      <Edit class="h-4 w-4" />
                    </button>
                    <button
                      @click="eliminarEstructura(estructura.idcarpeta, estructura.modulo_nombre)"
                      class="text-red-400 hover:text-red-300"
                      title="Eliminar estructura"
                    >
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="pagination-bg px-6 py-3 pagination-border flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-400">Mostrar</span>
            <select v-model="itemsPerPage" @change="currentPage = 1" class="pagination-select">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
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
                v-for="page in visiblePages"
                :key="page"
                @click="currentPage = page"
                :class="['pagination-button', { 'bg-indigo-600 text-white': currentPage === page }]"
              >
                {{ page }}
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
    </main>

    <!-- Modal para asignar estructura -->
    <div
      v-if="showAsignarModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="showAsignarModal = false"
    >
      <div class="modal-content rounded-lg p-6 w-96 border border-gray-700">
        <h3 class="text-lg font-semibold theme-text mb-4">
          Asignar Estructura a {{ moduloSeleccionado?.descripcion }}
        </h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-400 mb-2">
              Seleccionar Estructura
            </label>
            <select
              v-model="estructuraSeleccionada"
              class="input-field"
            >
              <option value="">Seleccione una estructura</option>
              <option
                v-for="estructura in estructurasActivas"
                :key="estructura.idcarpeta"
                :value="estructura.idcarpeta"
              >
                {{ estructura.nombre }}
              </option>
            </select>
          </div>
          <div class="flex justify-end space-x-2">
            <button
              @click="showAsignarModal = false"
              class="px-4 py-2 border border-gray-600 rounded hover:bg-gray-700 transition-colors theme-text"
            >
              Cancelar
            </button>
            <button
              @click="asignarEstructura"
              :disabled="!estructuraSeleccionada"
              class="btn-primary"
            >
              Asignar
            </button>
          </div>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/Sidebar.vue'
import { Plus, Edit, Trash2, X, Folder, FolderGit2 } from 'lucide-vue-next'
import api from '../../api'

import { useToastStore } from '../../stores/toast'

import { useConfirm } from '../../composables/useConfirm'
const { show, message, confirmar, accept, cancel } = useConfirm()

const toast = useToastStore()

console.log('[v0] API object:', api)
console.log('[v0] API.modulos:', api.modulos)
console.log('[v0] API.estructuras:', api.estructuras)

const router = useRouter()

const modulos = ref([])
const estructuras = ref([])
const estructurasActivas = ref([])
const searchTerm = ref('')
const itemsPerPage = ref(10)
const currentPage = ref(1)
const totalItems = ref(0)
const totalPages = ref(0)
const loading = ref(true)

const showAsignarModal = ref(false)
const moduloSeleccionado = ref(null)
const estructuraSeleccionada = ref('')

const filteredEstructuras = computed(() => {
  let filtered = estructuras.value

  console.log('[v0] Filtering estructuras :', filtered)

  if (searchTerm.value) {
    const search = searchTerm.value.toLowerCase()
    filtered = filtered.filter(estructura =>
      estructura.NOMBRE?.toLowerCase().includes(search) ||
      estructura.modulo_nombre?.toLowerCase().includes(search)
    )
  }

  return filtered
})

const paginatedEstructuras = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  totalItems.value = filteredEstructuras.value.length
  totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value) || 1
  return filteredEstructuras.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const cargarDatos = async () => {
  loading.value = true
  try {
    console.log('[v0] Starting to load data...')
    console.log('[v0] API.modulos.getAll:', api.modulos?.getAll)
    console.log('[v0] API.estructuras.getRaiz:', api.estructuras?.getRaiz)
    
    const [modulosRes, estructurasRes, activasRes] = await Promise.all([
      api.modulos.getAll(),
      api.estructuras.getRaiz(),
      api.estructuras.getActivas()
    ])
    
    console.log('[v0] Data loaded successfully')
    modulos.value = modulosRes.data
    estructuras.value = estructurasRes.data
    estructurasActivas.value = activasRes.data

    console.log('Módulos:', modulos.value)

    console.log('Estructuras activas:', estructurasActivas.value)
    
  } catch (error) {
    console.error('[v0] Error al cargar datos:', error)
    toast.push('Error al cargar los datos: ' + error.message, 'error')
  } finally {
    loading.value = false
  }
}

const abrirAsignarModal = (modulo) => {
  moduloSeleccionado.value = modulo
  estructuraSeleccionada.value = ''
  showAsignarModal.value = true
}

const asignarEstructura = async () => {
  if (!estructuraSeleccionada.value) return

  console.log('[v0] Assigning structure', estructuraSeleccionada.value, 'to module', moduloSeleccionado.value.idmodulo)
  
  try {
    await api.modulos.asignarEstructura({
      idmodulo: moduloSeleccionado.value.idmodulo,
      idestructuracarpeta: estructuraSeleccionada.value
    })
    
    showAsignarModal.value = false
    await cargarDatos()
  } catch (error) {
    console.error('Error al asignar estructura:', error)
    toast.push('Error al asignar la estructura', 'error')
  }
}

const desasignarEstructura = async (idmodulo) => {
  //if (!confirm('¿Está seguro de desasignar esta estructura?')) return

  console.log('[v0] Confirming unassignment of structure from module ID:', idmodulo)  

  const ok = await confirmar('¿Está seguro de desasignar esta estructura?')
  if (!ok) return
  
  try {
    await api.modulos.desasignarEstructura(idmodulo)
    await cargarDatos()
  } catch (error) {
    console.error('Error al desasignar estructura:', error)
    toast.push('Error al desasignar la estructura', 'error')
  }
}

const crearNuevaEstructura = () => {
  router.push('/admin/arbol-carpetas/nueva')
}

const editarEstructura = (id) => {
  console.log('[v0] Navigating to edit structure with ID:', id)
  router.push(`/admin/arbol-carpetas/${id}`)
}

const eliminarEstructura = async (id, moduloNombre) => {
  if (moduloNombre) {
    toast.push(`No se puede eliminar esta estructura porque está asignada al módulo "${moduloNombre}". Primero debe desasignarla o desactivarla desde la edición.`, 'success', 10000)
    return
  }
  
  //if (!confirm('¿Está seguro de eliminar esta estructura?')) return

  const ok = await confirmar('¿Está seguro de eliminar esta estructura?')
  if (!ok) return
  
  try {
    await api.estructuras.delete(id)
    await cargarDatos()
  } catch (error) {
    console.error('Error al eliminar estructura:', error)
    if (error.response?.data?.detail) {
      toast.push(error.response.data.detail, 'error')
    } else {
      toast.push('Error al eliminar la estructura', 'error')
    }
  }
}

onMounted(() => {
  cargarDatos()
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
  background-color: var(--color-bg-secondary);
  border-radius: 0.5rem;
  border: 1px solid var(--color-border);
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

.table-row-hover:hover {
  background-color: var(--color-row-hover);
}

.table-divider tr {
  border-bottom: 1px solid var(--color-border);
}

.pagination-bg {
  background-color: var(--color-bg-secondary);
}

.pagination-border {
  border-top: 1px solid var(--color-border);
}

.pagination-select {
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.pagination-button {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: var(--color-row-hover);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-field {
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);
  border-radius: 0.25rem;
  padding: 0.5rem;
  width: 100%;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.theme-text {
  color: var(--color-text-primary);
}

.modal-content {
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
}
</style>
