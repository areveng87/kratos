<template>
  <Sidebar>
    <div class="flex-1 p-6 overflow-auto" style="background-color: var(--color-bg-primary)">
      <div class="mb-6">
        <h1 class="text-2xl font-bold" style="color: var(--color-text-primary)">Relaciones</h1>
        <p class="mt-1" style="color: var(--color-text-secondary)">Gestión de tipos de relación</p>
      </div>
      <div class="mb-4">
        <button
          @click="mostrarModalCrear"
          class="px-4 py-2 rounded-lg font-medium transition-colors"
          style="background-color: var(--color-primary); color: white"
        >
          Nueva Relación
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

       Buscador 
      <div class="mb-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar relación..."
          class="w-full px-4 py-2 rounded-lg border transition-colors"
          style="background-color: var(--color-bg-secondary); border-color: var(--color-border); color: var(--color-text-primary)"
        />
      </div>

       Tabla de relaciones 
      <PaginatedTable
        :items="filteredRelaciones"
        :columns="columns"
        :loading="loading"
        key-field="idtiporelacion"
        @row-double-click="editarRelacion"
      >
        <template #cell-estructurajuridica="{ item }">
          <div class="flex justify-start">
            <svg
              v-if="item.estructurajuridica"
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              style="color: var(--color-success)"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              style="color: var(--color-text-tertiary)"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
        </template>

        <template #cell-acciones="{ item }">
          <div class="flex items-center space-x-2">
            <button
              @click="editarRelacion(item)"
              class="text-indigo-400 hover:text-indigo-300" 
              title="Editar relación"
            >
              <Edit class="h-4 w-4" />
            </button>
            <button
              @click="eliminarRelacion(item.idtiporelacion)"
              class="text-red-400 hover:text-red-300"
              title="Eliminar relación"
            >
              <Trash2 class="h-4 w-4" />
            </button>
          </div>
        </template>
      </PaginatedTable>

      Modal crear/editar 
      <div
        v-if="showModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="cerrarModal"
      >
        <div class="rounded-lg p-6 w-full max-w-md" style="background-color: var(--color-bg-secondary)">
          <h2 class="text-xl font-bold mb-4" style="color: var(--color-text-primary)">
            {{ isEditing ? 'Editar Relación' : 'Nueva Relación' }}
          </h2>
          
          <div class="mb-4">
            <label class="block mb-2 font-medium" style="color: var(--color-text-primary)">Descripción</label>
            <input
              v-model="formData.descripcion"
              type="text"
              class="w-full px-4 py-2 rounded-lg border"
              style="background-color: var(--color-bg-primary); border-color: var(--color-border); color: var(--color-text-primary)"
              placeholder="Ingrese la descripción"
            />
          </div>

          <div class="mb-4">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="formData.estructurajuridica"
                type="checkbox"
                class="w-4 h-4 rounded"
                style="accent-color: var(--color-primary)"
              />
              <span class="font-medium" style="color: var(--color-text-primary)">Estructura Jurídica</span>
            </label>
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
              @click="guardarRelacion"
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

import { useConfirm } from '../../../composables/useConfirm'
const { show, message, confirmar, accept, cancel } = useConfirm()

import axios from 'axios'

const toast = useToastStore()

const relaciones = ref([])
const searchQuery = ref('')
const loading = ref(false)

const showModal = ref(false)
const isEditing = ref(false)
const formData = ref({
  idtiporelacion: null,
  descripcion: '',
  estructurajuridica: false
})

const columns = [
  { key: 'descripcion', label: 'Descripción' },
  { key: 'estructurajuridica', label: 'Estructura Jurídica' },
  { key: 'acciones', label: 'Acciones', cellClass: 'text-right' }
]

const filteredRelaciones = computed(() => {
  if (!searchQuery.value) return relaciones.value
  
  const query = searchQuery.value.toLowerCase()
  return relaciones.value.filter(relacion =>
    relacion.descripcion.toLowerCase().includes(query)
  )
})

const cargarRelaciones = async () => {
  loading.value = true
  try {
    const response = await api.tiposRelacion.getAll()

    relaciones.value = response.data.data
    
  } catch (error) {
      toast.push('Error al cargar las relaciones', 'error')
  } finally {
    loading.value = false
  }
}

const mostrarModalCrear = () => {
  isEditing.value = false
  formData.value = {
    idtiporelacion: null,
    descripcion: '',
    estructurajuridica: false
  }
  showModal.value = true
}

const editarRelacion = (relacion) => {
  isEditing.value = true
  formData.value = {
    idtiporelacion: relacion.idtiporelacion,
    descripcion: relacion.descripcion,
    estructurajuridica: relacion.estructurajuridica
  }
  showModal.value = true
}

const cerrarModal = () => {
  showModal.value = false
  formData.value = {
    idtiporelacion: null,
    descripcion: '',
    estructurajuridica: false
  }
}

const guardarRelacion = async () => {
  try {

    if (isEditing.value) {
      const apiRest = await api.tiposRelacion.update(formData.value.idtiporelacion, {
        descripcion: formData.value.descripcion,
        estructurajuridica: formData.value.estructurajuridica
      })

      if (apiRest.data.code !== 200) {
        toast.push(apiRest.data.detail || 'Error al actualizar la relación', 'error')
        return
      }
      toast.push('Relación actualizada correctamente', 'success')

    } else {
      const apiRest = await api.tiposRelacion.create({
        descripcion: formData.value.descripcion,
        estructurajuridica: formData.value.estructurajuridica
      })

      console.log('apirest:', apiRest) // Debugging line

      if (apiRest.data.code !== 200) {
        toast.push(apiRest.data.detail || 'Error al crear la relación', 'error')
        return
      }

      toast.push('Relación creada correctamente', 'success')
    }
    
    await cargarRelaciones()
    cerrarModal()
    
  } catch (error) {
    console.error('Error al guardar relación:', error)
    toast.push(error.response?.data?.detail || 'Error al guardar la relación', 'error')
  }
}

const eliminarRelacion = async (idtiporelacion) => {

  const ok = await confirmar('¿Está seguro de que desea eliminar este fondo?')

  if (!ok) return

  try {
    await api.tiposRelacion.delete(idtiporelacion)
    await cargarRelaciones()
  } catch (error) {
    console.error('Error al eliminar relación:', error)
    if (error.response?.status === 400) {
      toast.push('No se puede eliminar la relación porque está en uso', 'error')
    } else {
      toast.push('Error al eliminar la relación', 'error')
    }
  }
}

onMounted(() => {
  cargarRelaciones()
})
</script>

<style scoped>
button:hover:not(:disabled) {
  opacity: 0.9;
}

input:focus {
  outline: none;
  border-color: var(--color-primary);
}
</style>
