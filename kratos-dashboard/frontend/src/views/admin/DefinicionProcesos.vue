<template>
  <Sidebar>
    <div class="flex-1 p-6 overflow-auto" style="background-color: var(--color-bg-primary)">
      <div class="mb-6">
        <h1 class="text-2xl font-bold" style="color: var(--color-text-primary)">Definición de Procesos</h1>
        <p class="mt-1" style="color: var(--color-text-secondary)">Gestión de procesos del planner</p>
      </div>

      <!-- Botón para crear nuevo proceso -->
      <div class="mb-4">
        <button @click="navegarACrear" class="btn-primary">
          Nuevo Proceso
        </button>
      </div>

      <!-- Buscador -->
      <div class="mb-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar proceso..."
          class="w-full px-4 py-2 rounded-lg border transition-colors"
          style="background-color: var(--color-bg-secondary); border-color: var(--color-border); color: var(--color-text-primary)"
        />
      </div>

      <!-- Tabla con PaginatedTable -->
      <PaginatedTable
        :items="procesosFiltrados"
        :columns="columns"
        :loading="loading"
        loadingText="Cargando procesos..."
        emptyText="No hay procesos registrados"
        keyField="idproceso"
        :initialItemsPerPage="10"
      >
        <!-- Columna de visibilidad con icono -->
        <template #cell-visibilidad="{ item }">
          <div class="flex justify-center">
            <Eye v-if="item.visibilidad === 1" :size="18" style="color: var(--color-success)" title="Visible" />
            <EyeOff v-else :size="18" style="color: var(--color-text-tertiary)" title="Oculto" />
          </div>
        </template>

        <!-- Columna de acciones -->
        <template #cell-acciones="{ item }">
          <div class="flex space-x-2 justify-center">
            <button @click="navegarAEditar(item.idproceso)" 
              class="text-indigo-400 hover:text-indigo-300" 
              title="Editar">
              <Edit :size="16" />
            </button>
            <button @click="eliminarProceso(item)" 
              class="text-red-400 hover:text-red-300"
              title="Eliminar">
              <Trash2 :size="16" />
            </button>
          </div>
        </template>
      </PaginatedTable>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Edit, Trash2, Eye, EyeOff } from 'lucide-vue-next'
import Sidebar from '../../components/Sidebar.vue'
import PaginatedTable from '../../components/PaginatedTable.vue'
import api from '../../api'

const router = useRouter()
const procesos = ref([])
const loading = ref(false)
const searchQuery = ref('')

const columns = [
  { key: 'descripcion', label: 'Descripción' },
  { key: 'prefijo', label: 'Prefijo' },
  { key: 'visibilidad', label: 'Visibilidad', headerClass: 'text-center', cellClass: 'text-center' },
  { key: 'acciones', label: 'Acciones', headerClass: 'text-center', cellClass: 'text-center' }
]

const procesosFiltrados = computed(() => {
  if (!searchQuery.value) return procesos.value
  
  const query = searchQuery.value.toLowerCase()
  return procesos.value.filter(proceso =>
    proceso.descripcion?.toLowerCase().includes(query) ||
    proceso.prefijo?.toLowerCase().includes(query)
  )
})

const cargarProcesos = async () => {
  loading.value = true
  try {
    const response = await api.procesos.getAll()
    procesos.value = response.data.data || []
  } catch (error) {
    console.error('Error al cargar procesos:', error)
    alert('Error al cargar los procesos')
  } finally {
    loading.value = false
  }
}

const navegarACrear = () => {
  router.push('/admin/definicion-procesos/nuevo')
}

const navegarAEditar = (idproceso) => {
  router.push(`/admin/definicion-procesos/${idproceso}`)
}

const eliminarProceso = async (proceso) => {
  if (!confirm(`¿Está seguro de eliminar el proceso "${proceso.descripcion}"?`)) {
    return
  }
  
  try {
    await api.procesos.delete(proceso.idproceso)
    alert('Proceso eliminado correctamente')
    await cargarProcesos()
  } catch (error) {
    console.error('Error al eliminar proceso:', error)
    alert(error.response?.data?.detail || 'Error al eliminar el proceso')
  }
}

onMounted(() => {
  cargarProcesos()
})
</script>

<style scoped>
button:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-bg-primary);
  border: none;
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.btn-secondary {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
