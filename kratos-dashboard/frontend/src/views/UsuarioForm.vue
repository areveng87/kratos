<template>
  <Sidebar>
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button
            @click="goBack"
            class="text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft class="h-5 w-5" />
          </button>
          <div>
            <h1 class="text-2xl font-bold theme-text">
              {{ isEditing ? 'Editar Usuario' : 'Nuevo Usuario' }}
            </h1>
            <p class="text-gray-400">
              {{ isEditing ? 'Actualiza la información del usuario' : 'Crea un nuevo usuario en el sistema' }}
            </p>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto main-content p-6">
      <div class="max-w mx-auto">
        <div class="card p-6 max-w">
          <form @submit.prevent="saveUser" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium modal-label mb-2">Nombre *</label>
                <input
                  v-model="usuario.nombre"
                  type="text"
                  required
                  class="input-field"
                  placeholder="Nombre"
                />
              </div>

              <div>
                <label class="block text-sm font-medium modal-label mb-2">Apellido</label>
                <input
                  v-model="usuario.apellido"
                  type="text"
                  class="input-field"
                  placeholder="Apellido"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium modal-label mb-2">Email *</label>
                    <input
                        v-model="usuario.email"
                        type="email"
                        required
                        class="input-field"
                        placeholder="usuario@ejemplo.com"
                    />
                </div>
                <div>
                    <label class="block text-sm font-medium modal-label mb-2">NIF/Pasaporte</label>
                    <input
                    v-model="usuario.nif"
                    type="text"
                    class="input-field"
                    placeholder="12345678A"
                    />
                </div>
            </div>
            

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              

                <div>
                    <label v-if="!isEditing" class="block text-sm font-medium modal-label mb-2">Contraseña *</label>
                    <label v-else class="block text-sm font-medium modal-label mb-2">Contraseña</label>
                    <input
                    v-model="usuario.password"
                    type="password"
                    :required="!isEditing"
                    class="input-field"
                    placeholder="Contraseña"
                    />
                    <p v-if="isEditing" class="text-xs text-gray-500 mt-1">
                    Dejar vacío para mantener la contraseña actual
                    </p>
                </div>

                <div>
                <label v-if="!isEditing" class="block text-sm font-medium modal-label mb-2">Repita contraseña *</label>
                <label v-else class="block text-sm font-medium modal-label mb-2">Repita contraseña</label>
                <input
                  v-model="repeatPassword"
                  type="password"
                  :required="repassRequired"
                  :class="['input-field', { 'border-red-500': passwordMismatch }]"
                  placeholder="Repita contraseña"
                />
                <p v-if="passwordMismatch" class="text-xs text-red-500 mt-1">
                  Las contraseñas no coinciden
                </p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium modal-label mb-2">Teléfono</label>
                <input
                  v-model="usuario.telefono"
                  type="tel"
                  class="input-field"
                  placeholder="+34 123 456 789"
                />
              </div>

              <div>
                <label class="block text-sm font-medium modal-label mb-2">Teléfono 2</label>
                <input
                  v-model="usuario.telefono2"
                  type="tel"
                  class="input-field"
                  placeholder="+34 987 654 321"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">             

              <div>
                <label class="block text-sm font-medium modal-label mb-2">Estado</label>
                <select
                  v-model="usuario.activo"
                  class="input-field"
                >
                  <option :value="true">Activo</option>
                  <option :value="false">Inactivo</option>
                </select>
              </div>

              <!-- Checkbox Propio -->
              <div class="flex items-center space-x-2">
                <input
                    id="propio"
                    type="checkbox"
                    v-model="usuario.propio"
                    class="h-4 w-4 rounded border-gray-300"
                />
                <label for="propio" class="block text-sm font-medium modal-label mb-2">Propio</label>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium modal-label mb-2">Rol *</label>
                    <!-- <label v-else class="block text-sm font-medium modal-label mb-2">Rol</label> -->
                    <select
                    v-model="usuario.rol_id"
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

                <div v-if="!isSPV && !isAuditor">
                    <label  class="block text-sm font-medium modal-label mb-2">Servicer *</label>
                    <!-- <label v-else class="block text-sm font-medium modal-label mb-2">Rol</label> -->
                    <select
                    v-model="usuario.servicer"
                    required="isSPV"
                    class="input-field w-full"
                    >
                    <option value="">Seleccionar servicer</option>
                    <option 
                        v-for="company in companies" 
                        :key="company.id" 
                        :value="company.id"
                    >
                        {{ company.nombre }}
                    </option>
                    </select>
                </div>

                <div v-if="isSPV && !isAuditor">
                    <label  class="block text-sm font-medium modal-label mb-2">Sociedad *</label>
                    <select
                    v-model="usuario.sociedad"
                    required="isSPV"
                    class="input-field w-full"
                    >
                    <option value="">Seleccionar sociedad</option>
                    <option 
                        v-for="society in societies" 
                        :key="society.idcliente" 
                        :value="society.idcliente"
                    >
                        {{ society.nomcli }}
                    </option>
                    </select>
                </div>                

            </div>

            <!-- Fechas solo visibles para Auditor -->
            <div v-if="isAuditor" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium modal-label mb-2">Fecha Inicio *</label>
                <input
                  v-model="usuario.fecha_inicio"
                  type="date"
                  class="input-field"
                  :max="usuario.fecha_fin || undefined"
                  :required="isAuditor"
                />
              </div>

              <div>
                <label class="block text-sm font-medium modal-label mb-2">Fecha Fin *</label>
                <input
                  v-model="usuario.fecha_fin"
                  type="date"
                  class="input-field"
                  :min="usuario.fecha_inicio || undefined"
                  :required="isAuditor"
                />
              </div>
            </div>

            <div v-if="isAuditor" class="mt-8 pt-6 border-t border-gray-700">
              <h2 class="text-xl font-bold theme-text mb-4">Sociedades Asignadas
                <span class="text-gray-400">({{ selectedSociedades.length }})</span>
              </h2>
              
              <div class="mb-4">
                <input
                  v-model="searchSociedades"
                  type="text"
                  class="input-field"
                  placeholder="Buscar sociedades..."
                />
              </div>

              <!--<div class="overflow-x-auto">
                <table class="w-full">
                  <thead>
                    <tr class="border-b border-gray-700">
                      <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">
                        <input
                          type="checkbox"
                          :checked="allSociedadesSelected"
                          @change="toggleAllSociedades"
                          class="rounded border-gray-600 bg-gray-700"
                        />
                      </th>
                      <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Sociedad</th>
                      <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Cartera</th>
                      <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Fondo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="sociedad in paginatedSociedades"
                      :key="sociedad.idcliente"
                      class="border-b border-gray-700 hover:bg-gray-800 transition-colors"
                    >
                      <td class="py-3 px-4">
                        <input
                          type="checkbox"
                          :checked="selectedSociedades.includes(sociedad.idcliente)"
                          @change="toggleSociedad(sociedad.idcliente)"
                          class="rounded border-gray-600 bg-gray-700"
                        />
                      </td>
                      <td class="py-3 px-4 text-sm theme-text">{{ sociedad.nomcli }}</td>
                      <td class="py-3 px-4 text-sm text-gray-400">{{ sociedad.ext_cartera || '-' }}</td>
                      <td class="py-3 px-4 text-sm text-gray-400">{{ sociedad.representante_nombre || '-' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="flex items-center justify-between mt-4">
                <p class="text-sm text-gray-400">
                  {{ selectedSociedades.length }} sociedades seleccionadas de {{ filteredSociedades.length }} total
                </p>
                
                <div v-if="totalPages > 1" class="flex items-center space-x-2">
                  <button
                    type="button"
                    @click="goToPage(currentPage - 1)"
                    :disabled="currentPage === 1"
                    class="px-3 py-1 text-sm border border-gray-600 rounded hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Anterior
                  </button>
                  
                  <div class="flex space-x-1">
                    <button
                      v-for="page in visiblePages"
                      :key="page"
                      type="button"
                      @click="goToPage(page)"
                      :class="[
                        'px-3 py-1 text-sm border rounded transition-colors',
                        currentPage === page
                          ? 'bg-blue-600 border-blue-600 text-white'
                          : 'border-gray-600 hover:bg-gray-700'
                      ]"
                    >
                      {{ page }}
                    </button>
                  </div>
                  
                  <button
                    type="button"
                    @click="goToPage(currentPage + 1)"
                    :disabled="currentPage === totalPages"
                    class="px-3 py-1 text-sm border border-gray-600 rounded hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Siguiente
                  </button>
                </div>
               
                
              
              </div>-->
              
              <div class="card overflow-hidden">
  <div class="overflow-x-auto">
    <table class="w-full">
      <thead class="table-header table-border">
        <tr>
          <!-- <th class="px-6 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider">
            <input
              type="checkbox"
              :checked="selectedSociedades.length === paginatedSociedades.length && paginatedSociedades.length > 0"
              @change="toggleSelectAllPage($event)"
              class="h-4 w-4 rounded border-gray-300"
              title="Seleccionar página actual"
            />
          </th> -->
          <th class="text-left py-3 px-6 text-sm font-medium text-gray-400">
                        <input
                          type="checkbox"
                          :checked="allSociedadesSelected"
                          @change="toggleAllSociedades"
                          class="rounded border-gray-600 bg-gray-700"
                        />
                      </th>
          <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Sociedad</th>
          <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Cartera</th>
          <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Fondo</th>
        </tr>
      </thead>

      <tbody class="table-divider">
        <tr
          v-for="soc in paginatedSociedades"
          :key="soc.idcliente"
          class="table-row-hover hover:bg-[#6366f3] transition-colors"
          @click="toggleRow(soc.idcliente)"
        >
          <td class="px-6 py-4 whitespace-nowrap" @click.stop>
            <input
              type="checkbox"
              class="rounded border-gray-600 bg-gray-700"
              v-model="selectedSociedades"
              :value="soc.idcliente"
            />
          </td>

          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium theme-text">
              {{ soc.nomcli || 'Sin nombre' }}
            </div>
          </td>

          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium theme-text"> 
              {{ soc.ext_cartera || '-' }} 
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium theme-text"> 
              {{ soc.representante_nombre || '-' }} 
            </div>
          </td>
      </tr>
      </tbody>
    </table>
  </div>

  <!-- Paginación estilo “empresas” -->
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

<!-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -->
<div v-if="isAuditor" class="mt-8 pt-6 border-t border-gray-700">
              <h2 class="text-xl font-bold theme-text mb-4">Operaciones Asignadas
                <span class="text-gray-400">({{ selectedOperaciones.length }})</span>
              </h2>
              
              <div class="mb-4">
                <input
                  v-model="searchOperaciones"
                  type="text"
                  class="input-field"
                  placeholder="Buscar operaciones..."
                />
              </div>

    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="table-header table-border">
            <tr>
              <th class="text-left py-3 px-6 text-sm font-medium text-gray-400">
                <input
                  type="checkbox"
                  :checked="allOperationsSelected"
                  @change="toggleAllOperations"
                  class="rounded border-gray-600 bg-gray-700"
                />
              </th>

              <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Servicer</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Fecha últ. cambio</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Referencia</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Sociedad</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Estado</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Analista PBC</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-400">Fecha Prevista Firma</th>
            </tr>
          </thead>

          <tbody class="table-divider">
            <tr
              v-for="op in paginatedOperations"
              :key="op.idcliente"
              class="table-row-hover hover:bg-[#6366f3] transition-colors"
              @click="toggleOperacion(op.idcliente)"
            >
              <td class="px-6 py-4 whitespace-nowrap" @click.stop>
                <input
                  type="checkbox"
                  class="rounded border-gray-600 bg-gray-700"
                  v-model="selectedOperaciones"
                  :value="op.idcliente"
                />
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium theme-text">
                  {{ op.nomempresa || 'Sin nombre' }}
                </div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium theme-text"> 
                  {{ formatDate(op.fechaultimocambio) || '-' }} 
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium theme-text"> 
                  {{ op.referencia || '-' }} 
                </div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium theme-text">
                  {{ op.nomcli || 'Sin nombre' }}
                </div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                 <span 
                    v-if="op.estado" 
                    class="inline-flex px-2 py-1 text-xs font-semibold rounded"
                    :class="getEstadoClass(op.estado)"
                  >
                     {{ op.estado }}
                  </span>
                <div v-else class="flex justify-center">
                  <Minus class="h-4 w-4 text-gray-400" />
                </div>
              </td>

              

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium theme-text">
                  {{ op.nomanalista || '-' }}
                </div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium theme-text">
                  {{ formatDate(op.fechaprevista) || '-' }}
                </div>
              </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginación estilo “empresas” -->
      <div class="pagination-bg px-6 py-3 pagination-border flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-400">Mostrar</span>
          <select v-model="itemsPerOperationPage" @change="currentOperationPage = 1" class="pagination-select">
            <option :value="10">10</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select> 
          <span class="text-sm text-gray-400">de {{ totalItems }} registros</span>
        </div>

        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-400">
            Página {{ currentOperationPage }} de {{ totalOperationPages }}
          </span>
          <div class="flex space-x-1">
            <button
              @click="currentOperationPage = 1"
              :disabled="currentOperationPage === 1"
              class="pagination-button"
            >
              ««
            </button>
            <button
              @click="currentOperationPage--"
              :disabled="currentOperationPage === 1"
              class="pagination-button"
            >
              «
            </button>
            <button
              @click="currentOperationPage++"
              :disabled="currentOperationPage === totalOperationPages"
              class="pagination-button"
            >
              »
            </button>
            <button
              @click="currentOperationPage = totalOperationPages"
              :disabled="currentOperationPage === totalOperationPages"
              class="pagination-button"
            >
              »»
            </button>
          </div>
        </div>
      </div>
    </div>
</div>
<!-- ---------------------------------------------------------------------------------------------------------------------------------------- -->
              
            </div>

            <div class="flex justify-end space-x-3 pt-4 border-t border-gray-700">
              <button
                type="button"
                @click="goBack"
                class="btn-secondary"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="btn-primary"
              >
                {{ saving ? 'Guardando...' : (isEditing ? 'Actualizar Usuario' : 'Crear Usuario') }}
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
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { ArrowLeft } from 'lucide-vue-next'
import { api } from '../api'
import { useCompanyStore } from '../stores/company'

import { useToastStore } from '../stores/toast'
import axios from 'axios'

const toast = useToastStore()

const route = useRoute()
const router = useRouter()
const companyStore = useCompanyStore()

const usuario = ref({
  nombre: '',
  apellido: '',
  email: '',
  nif: '',
  telefono: '',
  telefono2: '',
  rol_id: '',
  servicer: '',
  sociedad: '',
  propio:true,
  activo: true,
  password: '',
  fecha_inicio: null,   // 👈 nuevo
  fecha_fin: null       // 👈 nuevo
})

const roles = ref([])
const societies = ref([])
const companies = ref([])
const saving = ref(false)
const loading = ref(false)
const repeatPassword = ref('')

const sociedadesDisponibles = ref([])
const selectedSociedades = ref([])
const searchSociedades = ref('')

const currentPage = ref(1)
const itemsPerPage = ref(10)

const operacionesDisponibles = ref([])
const selectedOperaciones = ref([])
const searchOperaciones = ref('')

const currentOperationPage = ref(1)
const itemsPerOperationPage = ref(10)

const isEditing = computed(() => !!route.params.id)

const repassRequired = computed(() => {
  // If creating new user, always required
  if (!isEditing.value) return true
  
  // If editing, only required if password field has a value
  return usuario.value.password !== '' && usuario.value.password !== null
})

//Verifica si el perfil seleccionado es SPV
const isSPV = computed(() => {
  try {
    const role = roles.value.find(r => r.id === usuario.value.rol_id)

    console.log("Rol: ",role)

    return role ? role.nombre.toLowerCase().startsWith('spv') : false
  } catch (error) {
    console.error('Error checking SPV role:', error)
    return false
  }
})

const isAuditor = computed(() => {
  try {
    const role = roles.value.find(r => r.id === usuario.value.rol_id)

    console.log("Rol: ",role)

    return role ? role.nombre.toLowerCase().startsWith('auditor') : false
  } catch (error) {
    console.error('Error checking Auditor role:', error)
    return false
  }
})

const filteredSociedades = computed(() => {
  if (!searchSociedades.value) return sociedadesDisponibles.value
  const search = searchSociedades.value.toLowerCase()
  return sociedadesDisponibles.value.filter(soc => 
    soc.nomcli?.toLowerCase().includes(search) ||
    soc.ext_cartera?.toLowerCase().includes(search) ||
    soc.representante_nombre?.toLowerCase().includes(search)
  )
})

const filteredOperaciones = computed(() => {
  if (!searchOperaciones.value) return operacionesDisponibles.value
  const search = searchOperaciones.value.toLowerCase()
  return operacionesDisponibles.value.filter(op => 
    op.nomempresa?.toLowerCase().includes(search) ||
    op.nomcli?.toLowerCase().includes(search) ||
    op.referencia?.toLowerCase().includes(search) ||
    op.nomanalista?.toLowerCase().includes(search)
  )
})

const getEstadoClass = (estado) => {
  const estadoClasses = {
    'Analizando Riesgos': 'bg-yellow-100 text-yellow-800',
    'Sin Hitos': 'bg-gray-100 text-gray-800',
    'Elevado a OCI': 'bg-red-100 text-red-800',
    'En Proceso': 'bg-blue-100 text-blue-800',
    'Aprobado': 'bg-green-100 text-green-800'
  }
  return estadoClasses[estado] || 'bg-gray-100 text-gray-800'
}

const totalPages = computed(() => {
  return Math.ceil(filteredSociedades.value.length / itemsPerPage.value)
})

const paginatedSociedades = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredSociedades.value.slice(start, end)
})

const paginatedOperations = computed(() => {
  const start = (currentOperationPage.value - 1) * itemsPerOperationPage.value
  const end = start + itemsPerOperationPage.value
  return filteredOperaciones.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let startPage = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let endPage = Math.min(totalPages.value, startPage + maxVisible - 1)
  
  if (endPage - startPage < maxVisible - 1) {
    startPage = Math.max(1, endPage - maxVisible + 1)
  }
  
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }
  
  return pages
})

// const allSociedadesSelected = computed(() => {
//   if (filteredSociedades.value.length === 0) return false
//   return filteredSociedades.value.every(soc => selectedSociedades.value.includes(soc.idcliente))
// })

const allSociedadesSelected = computed(() => {
  if (paginatedSociedades.value.length === 0) return false
  return paginatedSociedades.value.every(soc => selectedSociedades.value.includes(soc.idcliente))
})

const allOperationsSelected = computed(() => {
  if (paginatedOperations.value.length === 0) return false
  return paginatedOperations.value.every(op => selectedOperaciones.value.includes(op.id))
})

// const toggleAllSociedades = () => {
//   if (allSociedadesSelected.value) {
//     const filteredIds = filteredSociedades.value.map(s => s.idcliente)
//     selectedSociedades.value = selectedSociedades.value.filter(id => !filteredIds.includes(id))
//   } else {
//     const filteredIds = filteredSociedades.value.map(s => s.idcliente)
//     const newSelections = filteredIds.filter(id => !selectedSociedades.value.includes(id))
//     selectedSociedades.value = [...selectedSociedades.value, ...newSelections]
//   }
// }


const toggleAllSociedades = () => {
  if (allSociedadesSelected.value) {
    const paginatedIds = paginatedSociedades.value.map(s => s.idcliente)
    selectedSociedades.value = selectedSociedades.value.filter(id => !paginatedIds.includes(id))
  } else {
    const paginatedIds = paginatedSociedades.value.map(s => s.idcliente)
    const newSelections = paginatedIds.filter(id => !selectedSociedades.value.includes(id))
    selectedSociedades.value = [...selectedSociedades.value, ...newSelections]
  }
}

const toggleSociedad = (idcliente) => {
  const index = selectedSociedades.value.indexOf(idcliente)
  if (index > -1) {
    selectedSociedades.value.splice(index, 1)
  } else {
    selectedSociedades.value.push(idcliente)
  }
}


const fetchSociedadesDisponibles = async () => {
  try {
    const response = await api.auditores.getSociedadesDisponibles()
    sociedadesDisponibles.value = response.data
  } catch (error) {
    console.error('Error al cargar sociedades:', error)
    sociedadesDisponibles.value = []
  }
}

const loadAuditorSociedades = async () => {
  if (!isEditing.value || !isAuditor.value) return
  try {
    const response = await api.auditores.getAuditorSociedades(route.params.id)
    selectedSociedades.value = response.data.sociedades_ids || []
  } catch (error) {
    console.error('Error al cargar sociedades del auditor:', error)
    selectedSociedades.value = []
  }
}


const toggleAllOperations = () => {
  if (allOperationsSelected.value) {
    const paginatedIds = paginatedOperations.value.map(s => s.id)
    selectedOperaciones.value = selectedOperaciones.value.filter(id => !paginatedIds.includes(id))
  } else {
    const paginatedIds = paginatedOperations.value.map(s => s.id)
    const newSelections = paginatedIds.filter(id => !selectedOperaciones.value.includes(id))
    selectedOperaciones.value = [...selectedOperaciones.value, ...newSelections]
  }
}

const toggleOperacion = (id) => {
  const index = selectedOperaciones.value.indexOf(id)
  if (index > -1) {
    selectedOperaciones.value.splice(index, 1)
  } else {
    selectedOperaciones.value.push(id)
  }
}


const fetchOperationsDisponibles = async () => {
  try {
    const response = await api.auditores.getOperacionesDisponibles()
    const d = response.data;

    console.log("Operaciones disponibles: ",d)

    operacionesDisponibles.value = d
  } catch (error) {
    console.error('Error al cargar operaciones:', error)
    operacionesDisponibles.value = []
  }
}

const loadAuditorOperaciones = async () => {
  if (!isEditing.value || !isAuditor.value) return
  try {
    const response = await api.auditores.getAuditorOperaciones(route.params.id)

    console.log("Operaciones del auditor: ", response.data)

    selectedOperaciones.value = response.data.operaciones_ids || []
  } catch (error) {
    console.error('Error al cargar operaciones del auditor:', error)
    selectedOperaciones.value = []
  }
}




const passwordMismatch = computed(() => {
  // Only check if repeat password field has content
  if (!repeatPassword.value) return false
  
  // Check if passwords match
  return usuario.value.password !== repeatPassword.value
})

const goBack = () => {
  router.push('/usuarios')
}

const fetchRoles = async () => {
  try {
    const response = await api.roles.getAll()
    roles.value = response.data.data || []
  } catch (error) {
    console.error('Error al cargar roles:', error)
    roles.value = []
  }
}

//Sociedades
const fetchSocieties = async () => {
  try {
    const response = await api.sociedades.getAll()
    societies.value = response.data || []

    console.log("Sociedades: ",societies.value)
  } catch (error) {
    console.error('Error al cargar sociedades:', error)
    societies.value = []
  }
}

//Empresas
const fetchCompanies = async () => {
  try {
    const response = await api.empresas.getAll()
    companies.value = response.data || []
  } catch (error) {
    console.error('Error al cargar empresas:', error)
    companies.value = []
  }
}

// Vue: método o función util
const formatDate = (s) => {
  if (!s) return '';
  const [yyyy, mm, dd] = s.slice(0, 10).split('-'); // "2025-06-11"
  return `${dd}-${mm}-${yyyy}`;                      // "11-06-2025"
};

const loadUsuario = async () => {
  
  if (!isEditing.value) return
  
  loading.value = true

  console.log("in loadUsuario")
  try {
    const companyCode = companyStore.getCurrentCompanyCode

    const response = await api.usuarios.getById(route.params.id, companyCode)

    usuario.value = { ...response.data, password: '' }
  } catch (error) {
    console.error('Error loading user:', error)
    alert('Error al cargar el usuario')
    router.push('/usuarios')
  } finally {
    loading.value = false
  }
}

const saveUser = async () => {
  if (passwordMismatch.value) {
    //alert('Las contraseñas no coinciden')
    toast.push('Las contraseñas deben coincidir', 'error')
    return
  }

  if(isSPV.value) {
    usuario.value.servicer = null
    if(!usuario.value.sociedad) {
      //alert('Debe seleccionar una sociedad para el rol SPV')
      toast.push('Debe seleccionar una sociedad para el rol SPV', 'error')
      return
    }
  } else if(!isAuditor.value) {
    usuario.value.sociedad = null
    if(!usuario.value.servicer) {
      toast.push('Debe seleccionar un servicer para este rol', 'error')
      return
    }
  } else {
    usuario.value.sociedad = null
    usuario.value.servicer = null
  }

  saving.value = true

  let userId = null

  try {

    const payload = { ...usuario.value } // por si quieres loguear/ajustar antes de enviar
    let apiRes = null

    const companyCode = companyStore.getCurrentCompanyCode

    console.log("Usuario:", usuario.value)

    let message = null
    
    console.log("es edicion: ", isEditing.value)

    if (isEditing.value) {
console.log("dentro de la edicion")

      // await api.usuarios.update(route.params.id, usuario.value)
      // userId = route.params.id

      // console.log("usuario a actualizar: ", userId)

      const { data } = await api.usuarios.update(route.params.id, usuario.value)
      apiRes = data // { code, detail, data }

      message = "Usuario actualizado correctamente"
    } else {
      // let response = await api.usuarios.create(usuario.value)

      // console.log("Response creación usuario:", response)
      // userId = response.data.id

      const { data } = await api.usuarios.create(payload)
      apiRes = data // { code, detail, data }

      message = 'Usuario creado correctamente'
    }

    // Manejo uniforme de respuesta { code, detail, data }
    if (apiRes.code !== 200) {
      // Ej.: code 409 cuando email duplicado
      toast.push(apiRes.detail || 'No se pudo guardar el usuario', 'error')
      return
    }

    // Obtén el ID persistido
    const userId = apiRes?.data?.id ?? (isEditing.value ? Number(route.params.id) : null)
    if (!userId) {
      toast.push('No se recibió el ID del usuario guardado', 'error')
      return
    }

    if (isAuditor.value) {
      console.log("sociedades a actualizar: ", selectedSociedades.value)

      await api.auditores.updateAuditorSociedades(userId, {
        sociedades_ids: selectedSociedades.value
      })

      console.log("operaciones a actualizar: ", selectedOperaciones.value)

      await api.auditores.updateAuditorOperaciones(userId, {
        operaciones_ids: selectedOperaciones.value
      })
    }
    if(userId != null && userId > 0)
    {
      toast.push(message, 'success');
      router.push('/usuarios')
    }
    else{
      if(isEditing.value)
        toast.push("No ha sido posible actualizar el usuario", 'error');
      else
        toast.push("No ha sido posible crear el usuario", 'error');
    }
      
console.log("saliendo de save")
    
  } catch (error) {
    console.error('Error saving usuario:', error)
    //alert('Error al guardar el usuario')
    toast.push(error.response?.data?.detail || 'Error al guardar el usuario', 'error')
  } finally {
    saving.value = false
  }
}

// watch(() => usuario.value.rol_id, async (newRolId) => {
//   if (isAuditor.value && isEditing.value) {
//     await loadAuditorSociedades()
//   }
// })

onMounted(async () => {
  await fetchRoles()
  await fetchSocieties()

  //for Auditors
  await fetchSociedadesDisponibles()
  await fetchOperationsDisponibles()

  await fetchCompanies()
  await loadUsuario()

  if (isEditing.value && isAuditor.value) {
    await loadAuditorSociedades()
    await loadAuditorOperaciones()
  }

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

.modal-label {
  color: var(--color-text-secondary);
}

.input-field {
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  width: 100%;
  color: var(--color-text-primary);
  transition: border-color 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: var(--color-primary);
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 0.375rem;
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

.btn-secondary {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: var(--color-bg-secondary);
}
</style>
