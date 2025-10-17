<template>
  <Sidebar>
    <!-- Header -->
    <header class="bg-gray-800 border-b border-gray-700 px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button
            @click="$router.go(-1)"
            class="text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft class="h-5 w-5" />
          </button>
          <div>
            <h1 class="text-2xl font-bold text-white">Detalle de Usuario</h1>
            <p class="text-gray-400">Información completa del usuario</p>
          </div>
        </div>
        <button
          @click="editMode = !editMode"
          class="btn-primary flex items-center space-x-2"
        >
          <Edit class="h-4 w-4" />
          <span>{{ editMode ? 'Cancelar' : 'Editar' }}</span>
        </button>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 overflow-y-auto bg-gray-900 p-6">
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="text-white">Cargando...</div>
      </div>

      <div v-else-if="usuario" class="max-w-4xl mx-auto">
        <!-- User Profile Card -->
        <div class="card p-6 mb-6">
          <div class="flex items-center space-x-6 mb-6">
            <div class="h-20 w-20 bg-indigo-600 rounded-full flex items-center justify-center">
              <User class="h-10 w-10 text-white" />
            </div>
            <div>
              <h2 class="text-2xl font-bold text-white">
                {{ usuario.nombre }} {{ usuario.apellido }}
              </h2>
              <p class="text-gray-400">{{ usuario.email }}</p>
              <div class="flex items-center space-x-4 mt-2">
                <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                  :class="getRoleClass(usuario.rol_id)">
                  {{ getRoleName(usuario.rol_id) }}
                </span>
                <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                  :class="usuario.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                  {{ usuario.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </div>
            </div>
          </div>

          <!-- User Information Form -->
          <form v-if="editMode" @submit.prevent="updateUsuario" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Nombre *</label>
                <input
                  v-model="editedUsuario.nombre"
                  type="text"
                  required
                  class="input-field"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Apellido *</label>
                <input
                  v-model="editedUsuario.apellido"
                  type="text"
                  required
                  class="input-field"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Email *</label>
              <input
                v-model="editedUsuario.email"
                type="email"
                required
                class="input-field"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">NIF *</label>
                <input
                  v-model="editedUsuario.nif"
                  type="text"
                  required
                  class="input-field"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Teléfono</label>
                <input
                  v-model="editedUsuario.telefono"
                  type="tel"
                  class="input-field"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Teléfono 2</label>
              <input
                v-model="editedUsuario.telefono2"
                type="tel"
                class="input-field"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Rol *</label>
                <select
                  v-model="editedUsuario.rol_id"
                  required
                  class="input-field"
                >
                  <option value="1">Administrador</option>
                  <option value="2">Usuario</option>
                  <option value="3">Cliente</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Estado</label>
                <select
                  v-model="editedUsuario.activo"
                  class="input-field"
                >
                  <option :value="true">Activo</option>
                  <option :value="false">Inactivo</option>
                </select>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="cancelEdit"
                class="btn-secondary"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="btn-primary"
              >
                {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>

          <!-- Read-only view -->
          <div v-else class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Nombre</label>
                <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ usuario.nombre }}</div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Apellido</label>
                <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ usuario.apellido }}</div>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ usuario.email }}</div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">NIF</label>
                <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ usuario.nif }}</div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Teléfono</label>
                <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ usuario.telefono || 'Sin teléfono' }}</div>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Teléfono 2</label>
              <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ usuario.telefono2 || 'Sin teléfono 2' }}</div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Rol</label>
                <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ getRoleName(usuario.rol_id) }}</div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Estado</label>
                <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ usuario.activo ? 'Activo' : 'Inactivo' }}</div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Fecha de Creación</label>
                <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ formatDate(usuario.fecha_creacion) }}</div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Último Login</label>
                <div class="text-white bg-gray-700 px-3 py-2 rounded-md">{{ usuario.ultimo_login ? formatDate(usuario.ultimo_login) : 'Nunca' }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Additional Information Card -->
        <div class="card p-6">
          <h3 class="text-lg font-semibold text-white mb-4">Información Adicional</h3>
          <div class="text-gray-400">
            <p>Aquí se pueden agregar más datos del usuario en el futuro, como:</p>
            <ul class="list-disc list-inside mt-2 space-y-1">
              <li>Historial de operaciones</li>
              <li>Empresas asociadas</li>
              <li>Configuraciones personales</li>
              <li>Logs de actividad</li>
            </ul>
          </div>
        </div>
      </div>

      <div v-else class="text-center text-gray-400">
        Usuario no encontrado
      </div>
    </main>
  </Sidebar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { ArrowLeft, Edit, User } from 'lucide-vue-next'
import { api } from '../api'

const route = useRoute()
const router = useRouter()

const usuario = ref(null)
const editedUsuario = ref({})
const loading = ref(true)
const saving = ref(false)
const editMode = ref(false)

const loadUsuario = async () => {
  try {
    const response = await api.usuarios.getById(route.params.id)
    usuario.value = response.data
    editedUsuario.value = { ...response.data }
  } catch (error) {
    console.error('Error loading user:', error)
    router.push('/usuarios')
  } finally {
    loading.value = false
  }
}

const updateUsuario = async () => {
  try {
    saving.value = true
    await api.usuarios.update(usuario.value.id, editedUsuario.value)
    usuario.value = { ...editedUsuario.value }
    editMode.value = false
  } catch (error) {
    console.error('Error updating user:', error)
  } finally {
    saving.value = false
  }
}

const cancelEdit = () => {
  editedUsuario.value = { ...usuario.value }
  editMode.value = false
}

const getRoleName = (rolId) => {
  const roles = {
    1: 'Administrador',
    2: 'Usuario',
    3: 'Cliente'
  }
  return roles[rolId] || 'Desconocido'
}

const getRoleClass = (rolId) => {
  const classes = {
    1: 'bg-purple-100 text-purple-800',
    2: 'bg-blue-100 text-blue-800',
    3: 'bg-green-100 text-green-800'
  }
  return classes[rolId] || 'bg-gray-100 text-gray-800'
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadUsuario()
})
</script>
