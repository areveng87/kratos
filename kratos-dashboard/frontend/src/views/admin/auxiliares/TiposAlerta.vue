<template>
  <Sidebar>
    <div class="flex-1 p-6 overflow-auto" style="background-color: var(--color-bg-primary)">
      <div class="mb-6">
        <h1 class="text-2xl font-bold" style="color: var(--color-text-primary)">Tipos de Alerta</h1>
        <p class="mt-1" style="color: var(--color-text-secondary)">Gestión de tipos de alerta</p>
      </div>

      <div class="mb-4">
        <button @click="abrirModalCrear" class="btn-primary">
          Nuevo tipo de alerta
        </button>
         <!-- Modal -->
        <div v-if="show" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div class="rounded-lg p-6 w-96"
              style="background-color: var(--color-bg-secondary); border:1px solid var(--color-border);">
            <h3 class="text-lg font-semibold theme-text mb-3">Confirmar acción</h3>
            <p class="theme-text mb-6">{{ message }}</p>
            <div class="flex justify-end gap-2">
              <button @click="cancel" class="btn-secondary">Cancelar</button>
              <button @click="accept" class="btn-primary">Sí, eliminar</button>
            </div>
          </div>
        </div>
      </div>

      <div class="mb-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar tipo de alerta..."
          class="w-full px-4 py-2 rounded-lg border transition-colors"
          style="background-color: var(--color-bg-secondary); border-color: var(--color-border); color: var(--color-text-primary)"
        />
      </div>
      
      <PaginatedTable
        :items="tiposFiltrados"
        :columns="columns"
        :loading="loading"
        loadingText="Cargando tipos de alerta..."
        emptyText="No hay tipos de alerta registrados"
        keyField="idtipoalerta"
        :initialItemsPerPage="10"
      >
        <template #cell-acciones="{ item }">
          <div class="flex items-right space-x-2">
            <button 
              @click="abrirModalEditar(item)" 
              class="text-indigo-400 hover:text-indigo-300"
              title="Editar">
              <Edit class="h-4 w-4" />
            </button>
            <button 
              @click="eliminarTipoAlerta(item)" 
              class="text-red-400 hover:text-red-300"
              title="Eliminar">
              <Trash2 class="h-4 w-4" />
            </button>
          </div>
        </template>
      </PaginatedTable>

      <div
        v-if="mostrarModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="cerrarModal"
      >
        <div
          class="rounded-lg p-6 w-full max-w-md"
          style="background-color: var(--color-bg-secondary)"
        >
          <h2 class="text-xl font-bold mb-4" style="color: var(--color-text-primary)">
            {{ modoEdicion ? 'Editar Tipo de Alerta' : 'Nuevo Tipo de Alerta' }}
          </h2>

          <form @submit.prevent="guardarTipoAlerta">
            <div class="mb-4">
              <label class="block mb-2" style="color: var(--color-text-primary)">
                Descripción <span class="text-red-500">*</span>
              </label>
              <input
                v-model="tipoAlertaForm.descripcion"
                type="text"
                required
                class="w-full px-4 py-2 rounded-lg border transition-colors"
                style="background-color: var(--color-bg-primary); border-color: var(--color-border); color: var(--color-text-primary)"
                placeholder="Ingrese la descripción"
              />
            </div>

            <div class="flex justify-end space-x-2">
              <button type="button" @click="cerrarModal" class="btn-secondary">
                Cancelar
              </button>
              <button type="submit" class="btn-primary">
                {{ modoEdicion ? 'Actualizar' : 'Crear' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Edit2, Edit, Trash2 } from 'lucide-vue-next'
import Sidebar from '../../../components/Sidebar.vue'
import PaginatedTable from '../../../components/PaginatedTable.vue'
import api from '../../../api'

import { useToastStore } from '../../../stores/toast'

import { useConfirm } from '../../../composables/useConfirm'
const { show, message, confirmar, accept, cancel } = useConfirm()

const toast = useToastStore()

const tiposAlerta = ref([])
const loading = ref(false)
const searchQuery = ref('')
const mostrarModal = ref(false)
const modoEdicion = ref(false)
const tipoAlertaForm = ref({
  idtipoalerta: null,
  descripcion: ''
})

const columns = [
  { key: 'descripcion', label: 'Descripción' },
  { key: 'acciones', label: 'Acciones', headerClass: 'text-left', cellClass: 'text-right' }
]

const tiposFiltrados = computed(() => {
  if (!searchQuery.value) return tiposAlerta.value
  
  const query = searchQuery.value.toLowerCase()
  return tiposAlerta.value.filter(tipo =>
    tipo.descripcion?.toLowerCase().includes(query)
  )
})

const cargarTiposAlerta = async () => {
  loading.value = true
  try {
    const response = await api.tiposAlerta.getAll()
    tiposAlerta.value = response.data.data || []
  } catch (error) {
    toast.push('Error al cargar los tipos de alerta', 'error')
  } finally {
    loading.value = false
  }
}

const abrirModalCrear = () => {
  modoEdicion.value = false
  tipoAlertaForm.value = {
    idtipoalerta: null,
    descripcion: ''
  }
  mostrarModal.value = true
}

const abrirModalEditar = (tipoAlerta) => {
  modoEdicion.value = true
  tipoAlertaForm.value = {
    idtipoalerta: tipoAlerta.idtipoalerta,
    descripcion: tipoAlerta.descripcion
  }
  mostrarModal.value = true
}

const cerrarModal = () => {
  mostrarModal.value = false
  tipoAlertaForm.value = {
    idtipoalerta: null,
    descripcion: ''
  }
}

const guardarTipoAlerta = async () => {
  try {
    if (modoEdicion.value) {
      const apiRest = await api.tiposAlerta.update(tipoAlertaForm.value.idtipoalerta, {
        descripcion: (tipoAlertaForm.value.descripcion ?? '').trim()
      })

      if (apiRest.data.code !== 200) {
        toast.push(apiRest.data.detail || 'Error al actualizar el tipo de alerta', 'error')
        return
      }

      toast.push('Tipo de alerta actualizado correctamente', 'success')

    } else {
      const apiRest = await api.tiposAlerta.create({
        descripcion: tipoAlertaForm.value.descripcion
      })
      if (apiRest.data.code !== 200) {
        toast.push(apiRest.data.detail || 'Error al crear el tipo de alerta', 'error')
        return
      }
      toast.push('Tipo de alerta creado correctamente', 'success')
    }
    
    cerrarModal()
    await cargarTiposAlerta()
  } catch (error) {
    console.error('Error al guardar tipo de alerta:', error)
    toast.push(error.response?.data?.detail || 'Error al guardar el tipo de alerta', 'error')
  }
}

const eliminarTipoAlerta = async (tipoAlerta) => {

  const ok = await confirmar(`¿Está seguro de eliminar el tipo de alerta "${tipoAlerta.descripcion}"?`)
  if (!ok) return

  try {

    var apiRest = await api.tiposAlerta.delete(tipoAlerta.idtipoalerta)
    if (apiRest.data.code !== 200) {
      toast.push(apiRest.data.detail || 'Error al eliminar el tipo de alerta', 'error')
      return
    }
    toast.push('Tipo de alerta eliminado correctamente', 'success')
    await cargarTiposAlerta()

  } catch (error) {
    console.error('Error al eliminar tipo de alerta:', error)
    toast.push(error.response?.data?.detail || 'Error al eliminar el tipo de alerta', 'error')
  }
}

onMounted(() => {
  cargarTiposAlerta()
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
