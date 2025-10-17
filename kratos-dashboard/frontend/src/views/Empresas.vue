<template>
  <Sidebar>
    <!-- Header -->
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold theme-text">Empresas</h1>
          <p class="text-gray-400">Gestión de empresas y clientes</p>
        </div>
        <button
          @click="showCreateModal = true"
          class="btn-primary flex items-center space-x-2"
        >
          <Plus class="h-4 w-4" />
          <span>Nueva Empresa</span>
        </button>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 overflow-y-auto main-content p-6">
      <!-- Search -->
      <div class="card p-4 mb-6">
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Buscar empresas..."
              class="input-field"
            />
          </div>
        </div>
      </div>

      <!-- Companies table -->
      <div class="card overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="table-header table-border">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Empresa
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Contacto
                </th>
                <!-- <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Fecha Registro
                </th> -->
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Estado
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody class="table-divider">
              <tr
                v-for="empresa in paginatedEmpresas"
                :key="empresa.id"
                class="transition-colors hover:bg-[#6366f3] hover:text-white cursor-pointer"
                @dblclick="handleRowDoubleClick(empresa)"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="h-10 w-10 bg-indigo-600 rounded-full flex items-center justify-center">
                      <Building2 class="h-5 w-5 text-white" />
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium theme-text">{{ empresa.nombre }}</div>
                      <div class="text-sm text-gray-400">{{ empresa.rut }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm theme-text">{{ empresa.email || 'Sin email' }}</div>
                  <div class="text-sm text-gray-400">{{ empresa.telefono || 'Sin teléfono' }}</div>
                </td>
                <!-- <td class="px-6 py-4 whitespace-nowrap text-sm table-text">
                  {{ formatDate(empresa.fecha_creacion) }}
                </td> -->
                <td class="px-6 py-4 whitespace-nowrap text-sm table-text">
                  <span class="inline-flex px-2 py-1 text-xs font-semibold rounded"
                    :class="getEstadoClass(empresa.activo)">
                    {{ empresa.activo ? 'Activa' : 'Inactiva' }}
                  </span>
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

        <!-- Added pagination controls -->
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

      <!-- Create Company Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="modal-bg rounded-lg p-6 w-full max-w-md">
          <h3 class="text-lg font-semibold theme-text mb-4">Nueva Empresa</h3>
          
          <form @submit.prevent="createEmpresa" class="space-y-4">
            <div>
              <label class="block text-sm font-medium modal-label mb-2">Nombre *</label>
              <input
                v-model="newEmpresa.nombre"
                type="text"
                required
                class="input-field"
                placeholder="Nombre de la empresa"
              />
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">RUT *</label>
              <input
                v-model="newEmpresa.rut"
                type="text"
                required
                class="input-field"
                placeholder="12.345.678-9"
              />
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">Dirección</label>
              <input
                v-model="newEmpresa.direccion"
                type="text"
                class="input-field"
                placeholder="Dirección completa"
              />
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">Teléfono</label>
              <input
                v-model="newEmpresa.telefono"
                type="tel"
                class="input-field"
                placeholder="+56 9 1234 5678"
              />
            </div>

            <div>
              <label class="block text-sm font-medium modal-label mb-2">Email</label>
              <input
                v-model="newEmpresa.email"
                type="email"
                class="input-field"
                placeholder="contacto@empresa.com"
              />
            </div>

            <div class="flex justify-end space-x-3">
              <button
                type="button"
                @click="showCreateModal = false"
                class="btn-secondary"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="creating"
                class="btn-primary"
              >
                {{ creating ? 'Creando...' : 'Crear' }}
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
import { Plus, Edit, Trash2, Building2, MapPin, Phone, Mail, Minus } from 'lucide-vue-next'
import { api } from '../api'

const empresas = ref([])
const loading = ref(true)
const creating = ref(false)
const showCreateModal = ref(false)
const searchTerm = ref('')

const currentPage = ref(1)
const itemsPerPage = ref(10)

const newEmpresa = ref({
  nombre: '',
  rut: '',
  direccion: '',
  telefono: '',
  email: ''
})

const filteredEmpresas = computed(() => {
  return empresas.value.filter(empresa => {
    return !searchTerm.value || 
      empresa.nombre.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      empresa.rut.includes(searchTerm.value)
  })
})

const totalItems = computed(() => filteredEmpresas.value.length)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))

const paginatedEmpresas = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredEmpresas.value.slice(start, end)
})

const loadEmpresas = async () => {
  try {
    const response = await api.empresas.getAll()
    empresas.value = response.data
  } catch (error) {
    console.error('Error loading companies:', error)
  }
}

const createEmpresa = async () => {
  try {
    creating.value = true
    await api.empresas.create(newEmpresa.value)
    
    // Reset form and close modal
    newEmpresa.value = {
      nombre: '',
      rut: '',
      direccion: '',
      telefono: '',
      email: ''
    }
    showCreateModal.value = false
    
    // Reload companies
    await loadEmpresas()
  } catch (error) {
    console.error('Error creating company:', error)
  } finally {
    creating.value = false
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CL', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getEstadoClass = (estado) => {
  switch (estado) {
    case 0:
      return 'bg-orange-100 text-orange-800'
    case 1:
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

onMounted(async () => {
  loading.value = true
  await loadEmpresas()
  loading.value = false
})
</script>
