<template>
  <Sidebar>
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold theme-text">Usuarios</h1>
          <p class="text-gray-400">Gestión de usuarios del sistema</p>
        </div>
        <!-- <button
          @click="showCreateModal = true"
          class="btn-primary flex items-center space-x-2"
        > -->
        <button
          @click="goToNewUsuario"
          class="btn-primary flex items-center space-x-2"
        >
          <Plus class="h-4 w-4" />
          <span>Nuevo Usuario</span>
        </button>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto main-content p-6">
      <div class="card p-4 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Buscar usuarios por nombre, email, rol, servicer o sociedad..."
              class="input-field"
            />
          </div>
          <div class="flex gap-4">
          <select v-model="roleFilter" class="input-field w-48">
            <option value="">Todos los roles</option>
            <!-- Using dynamic roles from database for filter dropdown -->
            <option 
              v-for="role in roles" 
              :key="role.id" 
              :value="role.id"
            >
              {{ role.nombre }}
            </option>
          </select>
        </div>
        </div>
      </div>

      <div class="card overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="table-header table-border">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Nombre</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Email</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Rol</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Servicer</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Sociedad</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Expediente Propio</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Activo</th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="table-divider">
              <tr
                v-for="usuario in paginatedUsuarios"
                :key="usuario.id"
                @click="viewUsuario(usuario.id)"
                class="transition-colors hover:bg-[#6366f3] hover:text-white cursor-pointer"
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
                  <div v-if="usuario.servicer_nombre" class="text-sm theme-text">
                    {{ usuario.servicer_nombre }}
                  </div>
                  <div v-else class="flex justify-left">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div v-if="usuario.sociedad_nombre" class="text-sm theme-text">
                    {{ usuario.sociedad_nombre}}
                  </div>
                  <div v-else class="flex justify-left">
                    <Minus class="h-4 w-4 text-gray-400" />
                  </div>
                </td>                
                <td class="px-6 py-4 whitespace-nowrap text-left justify-left">
                  <CheckCircle 
                    v-if="usuario.expediente_propio" 
                    class="h-5 w-5 text-green-500 mx-auto justify-left" 
                    title="Expediente Propio"
                  />
                  <XCircle 
                    v-else 
                    class="h-5 w-5 text-gray-300 mx-auto justify-left" 
                    title="Sin Expediente Propio"
                  />
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="inline-flex px-2 py-1 text-xs font-semibold rounded"
                    :class="getEstadoClass(usuario.activo)">
                    {{ usuario.activo ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex items-center space-x-2">
                    <button 
                      @click.stop="goToEditUsuario(usuario.id)"
                      class="text-indigo-400 hover:text-indigo-300"
                      title="Editar usuario"
                    >
                      <Edit class="h-4 w-4" />
                    </button>
                    <!-- <button 
                      @click.stop="deleteUsuario(usuario.id)"
                      class="text-red-400 hover:text-red-300"
                      title="Eliminar usuario"
                    >
                      <Trash2 class="h-4 w-4" />
                    </button> -->
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
        <!-- <div class="modal-bg rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto"> -->
        <div class="modal-bg rounded-lg p-6 w-full sm:max-w-3xl md:max-w-4xl lg:max-w-5xl xl:max-w-6xl max-h-[90vh] overflow-y-auto">
          <h3 class="text-lg font-semibold theme-text mb-4">
            {{ showEditModal ? 'Editar Usuario' : 'Nuevo Usuario' }}
          </h3>
          
          <form @submit.prevent="saveUser" class="space-y-4">
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
                <label class="block text-sm font-medium modal-label mb-2">Apellido</label>
                <input
                  v-model="currentUsuario.apellido"
                  type="text"
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
                <label class="block text-sm font-medium modal-label mb-2">NIF/Pasaporte</label>
                <input
                  v-model="currentUsuario.nif"
                  type="text"
                  class="input-field"
                  placeholder="12345678A"
                />
              </div>

              <div>
                <label v-if="!showEditModal" class="block text-sm font-medium modal-label mb-2">Contraseña *</label>
                <label v-else class="block text-sm font-medium modal-label mb-2">Contraseña</label>
                <input
                  v-model="currentUsuario.password"
                  type="password"
                  :required="!showEditModal"
                  class="input-field"
                  placeholder="Contraseña"
                />
                <p v-if="showEditModal" class="text-xs text-gray-500 mt-1">
                  Dejar vacío para mantener la contraseña actual
                </p>
              </div>
              
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium modal-label mb-2">Teléfono</label>
                  <input
                    v-model="currentUsuario.telefono"
                    type="tel"
                    class="input-field"
                    placeholder="+34 123 456 789"
                  />
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
            </div>
            

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label v-if="!showEditModal" class="block text-sm font-medium modal-label mb-2">Rol *</label>
                <label v-else class="block text-sm font-medium modal-label mb-2">Rol</label>
                <select
                  v-model="currentUsuario.rol_id"
                  required
                  class="input-field w-full"
                >
                  <option value="">Seleccionar rol</option>
                   <option 
                  v-for="role in roles" 
                  :key="role.id" 
                  :value="role.id"
                >
                  {{ role.nombre }}
                </option>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/Sidebar.vue'
import { Plus, Edit, Trash2, User, AlertTriangle, CheckCircle, XCircle, Minus } from 'lucide-vue-next'
import { api } from '../../api'
import { useCompanyStore } from '../../stores/company'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const companyStore = useCompanyStore()
const authStore = useAuthStore()

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
const roles = ref([])
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
      usuario.nif?.toLowerCase().includes(search) ||
      usuario.rol_nombre?.toLowerCase().includes(search) ||
      usuario.servicer_nombre?.toLowerCase().includes(search) ||
      usuario.sociedad_nombre?.toLowerCase().includes(search)
    )
  }
  console.log('roleFilter: ',roleFilter.value)

  console.log('user role: ', filtered[0]?.rol_id)
  if (roleFilter.value) {
    filtered = filtered.filter(usuario => usuario.rol_id === roleFilter.value)
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
    case 1: return 'bg-blue-100 text-blue-800';
    case 2: return 'bg-emerald-100 text-emerald-800';
    case 3: return 'bg-amber-100 text-amber-800';
    case 4: return 'bg-violet-100 text-violet-800';
    case 5: return 'bg-rose-100 text-rose-800';
    case 6: return 'bg-indigo-100 text-indigo-800';
    case 7: return 'bg-cyan-100 text-cyan-800';
    case 8: return 'bg-orange-100 text-orange-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}

const getRoleName = (rol_id) => {
  try {
    const role = roles.value.find(r => r.id === rol_id)
    return role ? role.nombre : 'Desconocido'
  } catch (error) {
    console.error('Error getting role name:', error)
    return ''
  }
}

const fetchRoles = async () => {
  try {
    const response = await api.roles.getAll()    

    roles.value = response.data.data || []

    console.log("Roles:", roles.value)

  } catch (error) {
    console.error('Error al cargar roles:', error)
    roles.value = []
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

const saveUser = async () => {
  console.log('Saving usuario:', currentUsuario.value)

  saving.value = true
  try {
    if (showEditModal.value) {
      console.log('updating user: ', editingId.value)
      await api.usuarios.update(editingId.value, currentUsuario.value)
      console.log('[v0] Usuario updated successfully')
    } else {
      console.log('creating user: ', editingId.value)
      await api.usuarios.create(currentUsuario.value)
      console.log('[v0] Usuario created successfully')
    }

    await loadUsuarios()
    closeModal()
  } catch (error) {
    console.error('Error saving usuario:', error)
    alert('Error al guardar el usuario')
  } finally {
    saving.value = false
  }
}

const createUsuario = async () => {
 console.log('Creating usuario:', currentUsuario.value)

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
  console.log('Updating usuario:', currentUsuario.value)
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
    const companyCode = companyStore.getCurrentCompanyCode
    const response = await api.usuarios.getAll(companyCode)
    usuarios.value = response.data
    console.log('[v0] Loaded usuarios:', usuarios.value.length, 'records')
  } catch (error) {
    console.error('Error loading usuarios:', error)
  } finally {
    loading.value = false
  }
}

const getEstadoClass = (estado) => {
  if(estado)
    return 'bg-green-100 text-green-800'
  else
    return 'bg-orange-100 text-orange-800'
}

const goToNewUsuario = () => {
  router.push('/admin/usuarios/nuevo')
}

const goToEditUsuario = (id) => {
  router.push(`/admin/usuarios/${id}/editar`)
}

watch(() => companyStore.selectedCompany, () => {
  loadUsuarios()
})

onMounted(async () => {
  loadUsuarios()
  await Promise.all([fetchRoles()])
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
