<template>
  <Sidebar>
    <div class="flex-1 p-6 overflow-auto" style="background-color: var(--color-bg-primary)">
      <div class="mb-6">
        <h1 class="text-2xl font-bold" style="color: var(--color-text-primary)">Fondos</h1>
        <p class="mt-1" style="color: var(--color-text-secondary)">Gestión de fondos</p>
      </div>

      <!-- Botón crear nuevo fondo -->
      <div class="mb-4">
        <button
          @click="mostrarModalCrear"
          class="btn-primary flex items-center space-x-2"
        >
          <Plus class="h-4 w-4" />
          <span class="font-medium">Nuevo Fondo</span>
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

      <!-- Buscador -->
      <div class="mb-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar fondo..."
          class="w-full px-4 py-2 rounded-lg border transition-colors"
          style="background-color: var(--color-bg-secondary); border-color: var(--color-border); color: var(--color-text-primary)"
        />
      </div>

      <!-- Tabla de fondos -->
      <PaginatedTable
        :items="filteredFondos"
        :columns="columns"
        :loading="loading"
        key-field="idrepresen"
        @row-double-click="editarFondo"
      >
        <template #cell-acciones="{ item }">
          <div class="flex items-center space-x-2">
            <button
              @click="editarFondo(item)"
              class="text-indigo-400 hover:text-indigo-300"
              title="Editar fondo"
            >
              <Edit class="h-4 w-4" />
            </button>
            <button
              @click="eliminarFondo(item.idrepresen)"
              class="text-red-400 hover:text-red-300" title="Eliminar fondo"
            >
              <Trash2 class="h-4 w-4" />
            </button>
          </div>
        </template>
      </PaginatedTable>

      <!-- Modal crear/editar -->
      <div
        v-if="showModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="cerrarModal"
      >
        <div class="rounded-lg p-6 w-full max-w-md" style="background-color: var(--color-bg-secondary)">
          <h2 class="text-xl font-bold mb-4" style="color: var(--color-text-primary)">
            {{ isEditing ? 'Editar Fondo' : 'Nuevo Fondo' }}
          </h2>
          
          <div class="mb-4">
            <label class="block mb-2 font-medium" style="color: var(--color-text-primary)">Nombre</label>
            <input
              v-model="formData.descripcion"
              type="text"
              class="w-full px-4 py-2 rounded-lg border"
              style="background-color: var(--color-bg-primary); border-color: var(--color-border); color: var(--color-text-primary)"
              placeholder="Ingrese el nombre del fondo"
            />
          </div>

          <div class="flex justify-end gap-2">
            <button
              @click="cerrarModal"
              class="px-4 py-2 rounded-lg transition-colors"
              style="background-color: var(--color-bg-tertiary); color: var(--color-text-primary)"
            >
              Cancelar
            </button>
            <button
              @click="guardarFondo"
              :disabled="!formData.descripcion"
              class="px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
              style="background-color: var(--color-primary); color: white"
            >
              {{ isEditing ? 'Actualizar' : 'Crear' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Sidebar from '../../../components/Sidebar.vue'
import PaginatedTable from '../../../components/PaginatedTable.vue'
import api from '../../../api'
import { Plus, Edit, Trash2, User, AlertTriangle, CheckCircle, XCircle, Minus } from 'lucide-vue-next'

import { useToastStore } from '../../../stores/toast'
import axios from 'axios'

import { useConfirm } from '../../../composables/useConfirm'
const { show, message, confirmar, accept, cancel } = useConfirm()

const toast = useToastStore()

const fondos = ref([])
const searchQuery = ref('')
const loading = ref(false)

const showModal = ref(false)
const isEditing = ref(false)
const formData = ref({
  idrepresen: null,
  descripcion: ''
})

const columns = [
  { key: 'descripcion', label: 'Nombre' },
  { key: 'acciones', label: 'Acciones', cellClass: 'text-right' }
]

const filteredFondos = computed(() => {
  if (!searchQuery.value) return fondos.value
  
  const query = searchQuery.value.toLowerCase()
  return fondos.value.filter(fondo =>
    fondo.descripcion.toLowerCase().includes(query)
  )
})

const cargarFondos = async () => {
  loading.value = true
  try {
    const response = await api.representantes.getAll()

    console.log('Response from getAll:', response) // Debugging line

    if (response.data.code !== 200) {
      toast.push(response.data.detail || 'Error al cargar los fondos')
    }

    fondos.value = response.data.data
  } catch (error) {
    console.error('Error al cargar fondos:', error)
    toast.push(error.response?.data?.data?.detail || 'Error al cargar los fondos')
  } finally {
    loading.value = false
  }
}

const mostrarModalCrear = () => {
  isEditing.value = false
  formData.value = {
    idrepresen: null,
    descripcion: ''
  }
  showModal.value = true
}

const editarFondo = (fondo) => {
  isEditing.value = true
  formData.value = {
    idrepresen: fondo.idrepresen,
    descripcion: fondo.descripcion
  }
  showModal.value = true
}

const cerrarModal = () => {
  showModal.value = false
  formData.value = {
    idrepresen: null,
    descripcion: ''
  }
}

const guardarFondo = async () => {
  try {
    if (isEditing.value) {
      const apiRest = await api.representantes.update(formData.value.idrepresen, {
        descripcion: formData.value.descripcion
      })

      if (apiRest.data.code !== 200) {
        toast.push(apiRest.data.detail || 'Error al actualizar el fondo', 'error')
        return
      }
      else {
        toast.push('Fondo actualizado correctamente', 'success')
      }
    } else {
      const apiRest = await api.representantes.create({
        descripcion: formData.value.descripcion
      })
      console.log('apirest:', apiRest) // Debugging line
      if (apiRest.data.code !== 200) {
        toast.push(apiRest.data.detail || 'Error al crear el fondo', 'error')
        return
      } else {
        toast.push('Fondo creado correctamente', 'success')
      }
    }
    
    await cargarFondos()
    cerrarModal()
  } catch (error) {
    console.error('Error al guardar fondo:', error)
    if (error.response?.status === 409) {
      toast.push('El fondo ya existe', 'error')
    } else {
      toast.push(error.response?.data?.detail || 'Error al guardar el fondo')
    }
    //alert('Error al guardar el fondo')
  }
}

const eliminarFondo = async (idrepresen) => {

  const ok = await confirmar('¿Está seguro de que desea eliminar este fondo?')
  if (!ok) return
  // if (!confirm('¿Está seguro de que desea eliminar este fondo?')) {
  //   return
  // }
  
  try {
    const apiRest = await api.representantes.delete(idrepresen)

    if (apiRest.data.code !== 200) {
      toast.push(apiRest.data.detail || 'Error al eliminar el fondo', 'error')
      return
    } else {
      toast.push('Fondo eliminado correctamente', 'success')
    }

    await cargarFondos()

  } catch (error) {
    console.error('Error al eliminar fondo:', error)
    if (error.response?.status === 400) {
      toast.push('No se puede eliminar el fondo porque está asignado a una o más sociedades', 'error')
    } else {
      toast.push('Error al eliminar el fondo', 'error')
    }
  }
}

onMounted(() => {
  cargarFondos()
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

input:focus {
  outline: none;
  border-color: var(--color-primary);
}
</style>
