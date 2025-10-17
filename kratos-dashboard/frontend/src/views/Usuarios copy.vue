<template>
  <Sidebar>
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold theme-text">Usuarios</h1>
          <p class="text-gray-400">Gestión de usuarios del sistema</p>
        </div>
        <button
          @click="showCreateModal = true"
          class="btn-primary flex items-center space-x-2"
        >
          <Plus class="h-4 w-4" />
          <span>Nuevo Usuario</span>
        </button>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto main-content p-6">
      <div class="card p-4 mb-6">
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Buscar usuarios por nombre, email o NIF..."
              class="input-field"
            />
          </div>
          <select v-model="roleFilter" class="input-field w-48">
            <option value="">Todos los roles</option>
            <option value="1">Administrador</option>
            <option value="2">Usuario</option>
            <option value="3">Cliente</option>
          </select>
        </div>
      </div>

      <div class="card overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="table-header table-border">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Usuario</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Contacto</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Rol</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Estado</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Último Login</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="table-divider">
              <tr
                v-for="usuario in paginatedUsuarios"
                :key="usuario.id"
                @click="viewUsuario(usuario.id)"
                class="table-row-hover transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="h-10 w-10 bg-indigo-600 rounded-full flex items-center justify-center">
                      <User class="h-5 w-5 text-white" />
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium theme-text">
                        {{ usuario.nombre }} {{ usuario.apellido }}
                      </div>
                      <div class="text-sm text-gray-400">{{ usuario.nif }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm theme-text">{{ usuario.email }}</div>
                  <div class="text-sm text-gray-400">{{ usuario.telefono || 'Sin teléfono' }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                    :class="getRoleClass(usuario.rol_id)">
                    {{ getRoleName(usuario.rol_id) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                    :class="usuario.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                    {{ usuario.activo ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm table-text">
                  {{ usuario.ultimo_login ? formatDate(usuario.ultimo_login) : 'Nunca' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex items-center space-x-2">
                    <button 
                      @click.stop="editUsuario(usuario)"
                      class="text-indigo-400 hover:text-indigo-300"
                      title="Editar usuario"
                    >
                      <Edit class="h-4 w-4" />
                    </button>
                    <button 
                      @click.stop="deleteUsuario(usuario.id)"
                      class="text-red-400 hover:text-red-300"
                      title="Eliminar usuario"
                    >
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

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

      <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="modal-bg rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto">
          <h3 class="text-lg font-semibold theme-text mb-4">
            {{ showEditModal ? 'Editar Usuario' : 'Nuevo Usuario' }}
          </h3>
          
          <form @submit.prevent="showEditModal ? updateUsuario() : createUsuario()" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium modal-label mb-2">Nombre *</label>
                <input
                  v-model="currentUsuario.nombre"
                  type="text"
                  required
                  class="input-field"
                  placeholder="Nombre"
                />
              </div>

              <div>
                <label class="block text-sm font-medium modal-label mb-2">Apellido *</label>
                <input
                  v-model="currentUsuario.apellido"
                  type="text"
                  required
                  class="input-field"
                  placeholder="Apellido"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">Email *</label>
              <input
                v-model="currentUsuario.email"
                type="email"
                required
                class="input-field"
                placeholder="usuario@ejemplo.com"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium modal-label mb-2">NIF *</label>
                <input
                  v-model="currentUsuario.nif"
                  type="text"
                  required
                  class="input-field"
                  placeholder="12345678A"
                />
              </div>

              <div>
                <label class="block text-sm font-medium modal-label mb-2">Teléfono</label>
                <input
                  v-model="currentUsuario.telefono"
                  type="tel"
                  class="input-field"
                  placeholder="+34 123 456 789"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">Teléfono 2</label>
              <input
                v-model="currentUsuario.telefono2"
                type="tel"
                class="input-field"
                placeholder="+34 987 654 321"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium modal-label mb-2">Rol *</label>
                <select
                  v-model="currentUsuario.rol_id"
                  required
                  class="input-field"
                >
                  <option value="">Seleccionar rol</option>
                  <option value="1">Administrador</option>
                  <option value="2">Usuario</option>
                  <option value="3">Cliente</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium modal-label mb-2">Estado</label>
                <select
                  v-model="currentUsuario.activo"
                  class="input-field"
                >
                  <option :value="true">Activo</option>
                  <option :value="false">Inactivo</option>
                </select>
              </div>
            </div>

            <div v-if="!showEditModal">
              <label class="block text-sm font-medium modal-label mb-2">Contraseña *</label>
              <input
                v-model="currentUsuario.password"
                type="password"
                :required="!showEditModal"
                class="input-field"
                placeholder="Contraseña"
              />
            </div>

            <div class="flex justify-end space-x-3 pt-4">
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
                {{ saving ? 'Guardando...' : (showEditModal ? 'Actualizar' : 'Crear') }}
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
import { Plus, Edit, Trash2, User } from 'lucide-vue-next'
import { api } from '../api'

const searchTerm = ref('')
const roleFilter = ref('')
const itemsPerPage = ref(10)
const currentPage = ref(1)
const totalItems = ref(0)
const totalPages = ref(0)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const currentUsuario = ref({
  nombre: '',
  apellido: '',
  email: '',
  nif: '',
  telefono: '',
  telefono2: '',
  rol_id: '',
  activo: true,
  password: ''
})
const usuarios = ref([])
const saving = ref(false)
const loading = ref(true)
const editingId = ref(null)

const filteredUsuarios = computed(() => {
  let filtered = usuarios.value

  if (searchTerm.value) {
    const search = searchTerm.value.toLowerCase()
    filtered = filtered.filter(usuario =>
      usuario.nombre?.toLowerCase().includes(search) ||
      usuario.apellido?.toLowerCase().includes(search) ||
      usuario.email?.toLowerCase().includes(search) ||
      usuario.nif?.toLowerCase().includes(search)
    )
  }

  if (roleFilter.value) {
    filtered = filtered.filter(usuario => usuario.rol_id.toString() === roleFilter.value)
  }

  return filtered
})

const paginatedUsuarios = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  totalItems.value = filteredUsuarios.value.length
  totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value)
  return filteredUsuarios.value.slice(start, end)
})

const getRoleClass = (rol_id) => {
  switch (rol_id) {
    case '1':
      return 'bg-blue-100 text-blue-800';
    case '2':
      return 'bg-green-100 text-green-800';
    case '3':
      return 'bg-yellow-100 text-yellow-800';
    default:
      return '';
  }
}

const getRoleName = (rol_id) => {
  switch (rol_id) {
    case '1':
      return 'Administrador';
    case '2':
      return 'Usuario';
    case '3':
      return 'Cliente';
    default:
      return 'Desconocido';
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
}

const viewUsuario = (id) => {
  console.log('[v0] Viewing usuario with id:', id)
}

const editUsuario = (usuario) => {
  editingId.value = usuario.id
  currentUsuario.value = { ...usuario }
  showEditModal.value = true
}

const deleteUsuario = async (id) => {
  if (confirm('¿Está seguro de eliminar este usuario?')) {
    try {
      await api.usuarios.delete(id)
      await loadUsuarios()
      console.log('[v0] Usuario deleted successfully')
    } catch (error) {
      console.error('Error deleting usuario:', error)
    }
  }
}

const createUsuario = async () => {
  saving.value = true
  try {
    await api.usuarios.create(currentUsuario.value)
    await loadUsuarios()
    closeModal()
    console.log('[v0] Usuario created successfully')
  } catch (error) {
    console.error('Error creating usuario:', error)
  } finally {
    saving.value = false
  }
}

const updateUsuario = async () => {
  saving.value = true
  try {
    await api.usuarios.update(editingId.value, currentUsuario.value)
    await loadUsuarios()
    closeModal()
    console.log('[v0] Usuario updated successfully')
  } catch (error) {
    console.error('Error updating usuario:', error)
  } finally {
    saving.value = false
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingId.value = null
  currentUsuario.value = {
    nombre: '',
    apellido: '',
    email: '',
    nif: '',
    telefono: '',
    telefono2: '',
    rol_id: '',
    activo: true,
    password: ''
  }
}

const loadUsuarios = async () => {
  loading.value = true
  try {
    console.log('[v0] Loading usuarios from API...')
    const response = await api.usuarios.getAll()
    usuarios.value = response.data
    console.log('[v0] Loaded usuarios:', usuarios.value.length, 'records')
  } catch (error) {
    console.error('Error loading usuarios:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUsuarios()
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
}

.table-header {
  background-color: var(--color-bg-secondary);
}

.table-header-text {
  padding: 0.75rem;
  text-align: left;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

.table-border {
  border-color: var(--color-border);
}

.table-row-hover {
  cursor: pointer;
  transition: background-color 0.3s;
}

.table-row-hover:hover {
  background-color: var(--color-row-hover);
}

.table-text {
  color: var(--color-text-muted);
}

.pagination-bg {
  background-color: var(--color-bg-secondary);
}

.pagination-border {
  border-top: 1px solid var(--color-border);
}

.pagination-select {
  width: auto;
}

.pagination-button {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.modal-bg {
  background-color: var(--color-bg-primary);
}

.modal-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
}

.input-field {
  border: 1px solid var(--color-border);
  border-radius: 0.25rem;
  padding: 0.5rem;
  width: 100%;
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

.status-badge {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.25rem;
}

.status-completed {
  background-color: var(--color-success-bg);
  color: var(--color-success-text);
}

.status-cancelled {
  background-color: var(--color-danger-bg);
  color: var(--color-danger-text);
}
</style>
