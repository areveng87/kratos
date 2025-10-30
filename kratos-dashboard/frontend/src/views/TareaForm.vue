<template>
<Sidebar>
  <div class="flex-1 p-6 overflow-auto" style="background-color: var(--color-bg-primary)">
    <div class="mb-6">
        <h1 class="text-2xl font-bold" style="color: var(--color-text-primary)">
          {{ isEdit ? 'Editar operación' : 'Nuevo operación' }}
        </h1>
        <p class="mt-1" style="color: var(--color-text-secondary)">
          {{ isEdit ? 'Modificar operación existente' : 'Crear una nueva operación' }}
        </p>
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
    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header con tabs -->
      <div class="border-b" style="border-color: var(--color-border); background-color: var(--color-bg-secondary)">
        <div class="flex px-6">
          <button
            v-for="tab in visibleTabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="px-4 py-3 font-medium transition-colors"
            :class="[
              activeTab === tab.id
                ? 'border-b-2 theme-text'
                : 'theme-text-secondary hover:theme-text'
            ]"
            :style="activeTab === tab.id ? 'border-color: var(--color-primary)' : ''"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <!-- Tab content -->
      <div class="flex-1 overflow-y-auto p-6">
        <!-- Tab 1: Inmueble -->
        <div v-if="activeTab === 'inmueble'" class="w-full">
          <div class="grid grid-cols-2 gap-6">
            <!-- Sociedad -->
            <div >
              <label class="block text-sm font-medium theme-text mb-2">Sociedad *</label>
              <select
                v-model="form.idcliente"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
                required
              >
                <option value="">Seleccione una sociedad</option>
                <option v-for="cliente in clientes" :key="cliente.idcliente" :value="cliente.idcliente">
                  {{ cliente.nomcli }}
                </option>
              </select>
            </div>

            <!-- Tipo de Operación -->
            <div>
              <label class="block text-sm font-medium theme-text mb-2">Tipo de Operación *</label>
              <select
                v-model="form.tipo_operacion"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
                required
              >
                <option value="">Seleccione un tipo de operación</option>
                <option v-for="tipo in tiposOperaciones" :key="tipo.id" :value="tipo.id">
                  {{ tipo.descripcion }}
                </option>
              </select>
            </div>

            <!-- Tipo de activo y Otros -->
            <div>
              <label class="block text-sm font-medium theme-text mb-2">Tipo de activo *</label>
              <select
                v-model="form.ext_tipoactivo"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
                required
              >
                <option value="">Seleccione un tipo</option>
                <option v-for="tipo in tiposActivos" :key="tipo.id" :value="tipo.id">
                  {{ tipo.descripcion }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium theme-text mb-2">Otros</label>
              <input
                v-model="form.ext_activosotros"
                type="text"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
              />
            </div>

            <!-- País -->
            <div>
              <label class="block text-sm font-medium theme-text mb-2">País</label>
              <select
                v-model="form.pais"
                @change="onPaisChange"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
              >
                <option value="">Seleccione un país</option>
                <option v-for="pais in paises" :key="pais.codigo" :value="pais.codigo">
                  {{ pais.nombre }}
                </option>
              </select>
            </div>

            <!-- Provincia -->
            <div>
              <label class="block text-sm font-medium theme-text mb-2">Provincia</label>
              <select
                v-model="form.provincia"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
                :disabled="!form.pais"
              >
                <option value="">Seleccione una provincia</option>
                <option v-for="prov in provincias" :key="prov.codigo" :value="prov.codigo">
                  {{ prov.nombre }}
                </option>
              </select>
            </div>

            <!-- Localidad y Urgente -->
            <div class="col-span-2 flex gap-4">
              <div class="flex-1">
                <label class="block text-sm font-medium theme-text mb-2">Localidad</label>
                <input
                  v-model="form.localidad"
                  type="text"
                  class="w-full px-3 py-2 rounded border theme-input"
                  style="border-color: var(--color-border)"
                  :disabled="!form.pais"
                />
              </div>
              <div class="flex items-end pb-2">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input
                    v-model="form.ext_urgente"
                    type="checkbox"
                    class="w-4 h-4"
                  />
                  <span class="text-sm theme-text">Urgente</span>
                </label>
              </div>
            </div>  

            <!-- Analista PBC -->
            <div class="col-span-2">
              <label class="block text-sm font-medium theme-text mb-2">Analista PBC</label>
              <select
                v-model="form.ext_analistapbc"
                @change="onAnalistaChange"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
              >
                <option value="">Seleccione un analista</option>
                <option v-for="analista in analistasPBC" :key="analista.id" :value="analista.id">
                  {{ analista.nombre }}
                </option>
              </select>
            </div>

            <!-- Servicer y Referencia Expediente -->
            <div>
              <label class="block text-sm font-medium theme-text mb-2">Servicer</label>
              <select
                v-model="form.codempresa"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
              >
                <option value="">Seleccione un servicer</option>
                <option v-for="emp in empresasClientes" :key="emp.codigo" :value="emp.codigo">
                  {{ emp.nombre }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium theme-text mb-2">Referencia Expediente</label>
              <input
                v-model="form.referencia"
                type="text"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
              />
            </div>

            <!-- Analista asignado por (read-only) -->
            <div class="col-span-2">
              <label class="block text-sm font-medium theme-text mb-2">Analista asignado por</label>
              <input
                :value="asignadorNombre"
                type="text"
                class="w-full px-3 py-2 rounded border theme-input bg-gray-100"
                style="border-color: var(--color-border)"
                readonly
                disabled
              />
            </div>

            <!-- Operador -->
            <div class="col-span-2">
              <label class="block text-sm font-medium theme-text mb-2">Operador</label>
              <select
                v-model="form.ext_operador"
                class="w-full px-3 py-2 rounded border theme-input"
                style="border-color: var(--color-border)"
              >
                <option value="">Seleccione un operador</option>
                <option v-for="operador in operadores" :key="operador.id" :value="operador.id">
                  {{ operador.nombre }}
                </option>
              </select>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="flex justify-end gap-3 mt-8">
            <button
              @click="cancelar"
              class="px-4 py-2 rounded font-medium text-white"
              style="background-color: #ef4444"
            >
              Cancelar
            </button>
            <button v-if="isEdit"
              @click="borrarExpediente"
              class="px-4 py-2 rounded font-medium text-white"
              style="background-color: #ef4444"
            >
              Borrar Expediente
            </button>
            <button
              @click="guardar"
              class="px-4 py-2 rounded font-medium text-white"
              style="background-color: #10b981"
            >
              {{ isEdit ? 'Guardar Cambios' : 'Reportar Alta' }}
            </button>            
          </div>
        </div>

        <!-- Tab 2: Importe / Hitos -->
        <div v-else-if="activeTab === 'importe-hitos'">
          <ImportesHitos
            v-if="isEdit && route.params.id"
            ref="importesHitosRef"
            :idtarea="parseInt(route.params.id)"
            :importeTotal="form.ext_importe"
            :moneda="form.ext_moneda"
            :tributacion="form.ext_tributacion"
            @update="onImportesUpdate"
          />
        </div>

        <!-- Otros tabs (placeholder) -->
        <div v-else class="text-center py-12">
          <p class="theme-text-secondary">Tab "{{ activeTab }}" en desarrollo</p>
        </div>
      </div>
    </div>
  </div>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'
import Sidebar from '../components/Sidebar.vue'
import ImportesHitos from '../components/ImportesHitos.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeTab = ref('inmueble')
const importesHitosRef = ref(null)

const tabs = [
  { id: 'inmueble', label: 'Inmueble' },
  { id: 'importe-hitos', label: 'Importe / Hitos' },
  { id: 'intervinientes', label: 'Intervinientes' },
  { id: 'documentos', label: 'Documentos' },
  { id: 'operaciones', label: 'Operaciones' },
  { id: 'worldcheck', label: 'WorldCheck Análisis' },
]

// Form data
const form = ref({
  idcliente: 0,
  tipo_operacion: 0,
  ext_tipoactivo: 0,
  ext_activosotros: '',
  localidad: '',
  pais: '',
  provincia: '',
  ext_analistapbc: '',
  codempresa: 0,
  referencia: '',
  ext_asignador_analistapbc: null,
  ext_operador: '',
  ext_urgente: false,
  ext_importe: null,
  ext_moneda: 0,
  ext_tributacion: null,
})

// Catálogos
const clientes = ref([])
const tiposActivos = ref([])
const tiposOperaciones = ref([])
const paises = ref([])
const provincias = ref([])
const analistasPBC = ref([])
const operadores = ref([])
const empresasClientes = ref([])
const usuarios = ref([])

// Computed
const isEdit = computed(() => !!route.params.id)
const asignadorNombre = computed(() => {
  if (!form.value.ext_asignador_analistapbc) return ''
  const usuario = usuarios.value.find(u => u.id === form.value.ext_asignador_analistapbc)
  return usuario ? usuario.nombre : ''
})

const visibleTabs = computed(() =>
  isEdit.value ? tabs : tabs.filter(t => t.id === 'inmueble')
)

// Methods
const cargarCatalogos = async () => {
  try {
    const [
      clientesRes,
      tiposRes,
      tiposOperacionesRes,
      paisesRes,
      analistasRes,
      operadoresRes,
      empresasRes,
      usuariosRes
    ] = await Promise.all([
      api.catalogos.getClientes(),
      api.catalogos.getTiposActivos(),
      api.catalogos.getTiposOperaciones(),
      api.catalogos.getPaises(),
      api.catalogos.getAnalistasPBC(),
      api.catalogos.getOperadores(),
      api.empresas.getAll(),
      api.usuarios.getAll()
    ])

    clientes.value = clientesRes.data.data || []
    tiposActivos.value = tiposRes.data.data || []
    tiposOperaciones.value = tiposOperacionesRes.data.data || []
    paises.value = paisesRes.data.data || []
    analistasPBC.value = analistasRes.data.data || []
    operadores.value = operadoresRes.data.data || []
    empresasClientes.value = empresasRes.data || []
    usuarios.value = usuariosRes.data || []

    console.log('empresasClientes:', empresasRes.data)

  } catch (error) {
    console.error('Error cargando catálogos:', error)
  }
}

const cancelar = () => {
  router.push('/operaciones')
}

const onPaisChange = async () => {
  form.value.provincia = ''
  provincias.value = []
  
  if (form.value.pais) {
    try {
      const response = await api.catalogos.getProvincias(form.value.pais)
      provincias.value = response.data.data || []      
    } catch (error) {
      console.error('Error cargando provincias:', error)
    }
  }
}

const onAnalistaChange = () => {
  // Cuando se asigna un analista, el usuario actual es el asignador
  if (form.value.ext_analistapbc && authStore.user) {
    form.value.ext_asignador_analistapbc = authStore.user.id
  } else {
    form.value.ext_asignador_analistapbc = null
  }
}

const cargarTarea = async () => {
  if (!isEdit.value) return
  
  try {
    const response = await api.tareas.getById(route.params.id)
    const tarea = response.data.data

    console.log('Tarea obtenida del API:', tarea)
    
    // Cargar datos en el formulario
    Object.keys(form.value).forEach(key => {      
      if (tarea[key] !== undefined) {
        form.value[key] = tarea[key]      
      }
    })
    
    // Cargar provincias si hay país seleccionado
    if (form.value.pais) {
      await onPaisChange()
    }
    if('provincia' in tarea){
      form.value.provincia = tarea.provincia
    }
  } catch (error) {
    console.error('Error cargando tarea:', error)
  }
}

const guardar = async () => {

  try {
    console.log('Guardando tarea con datos:', form.value)

    if (isEdit.value && importesHitosRef.value) {
      const datosImportes = importesHitosRef.value.getDatosActuales()
      form.value.ext_importe = datosImportes.ext_importe
      form.value.ext_moneda = datosImportes.ext_moneda
      form.value.ext_tributacion = datosImportes.ext_tributacion
    }

    if (isEdit.value) {

      console.log('Actualizando tarea con datos:', form.value)

      await api.tareas.update(route.params.id, form.value)

    } else {
      await api.tareas.create(form.value)
    }
    
    router.push('/operaciones')
  } catch (error) {
    console.error('Error guardando tarea:', error)
    alert('Error al guardar la operación')
  }
}

const borrarExpediente = () => {
  if (confirm('¿Está seguro de que desea borrar este expediente?')) {
    // TODO: Implementar eliminación
    router.push('/operaciones')
  }
}

// Bloquear cambio de pestaña en creación
const selectTab = (id) => {
  if (!isEdit.value && id !== 'inmueble') return
  activeTab.value = id
}

const onImportesUpdate = (data) => {
  if(data == null) return;

  console.log("Importes actualizados:", data)
  
  form.value.ext_importe = data.importeTotal
  form.value.ext_moneda = data.moneda
  form.value.ext_tributacion = data.tributacion
}

onMounted(async () => {

  await cargarCatalogos()

  if (!isEdit.value) activeTab.value = 'inmueble'

  await cargarTarea()
})
</script>

<style scoped>
.theme-text {
  color: var(--color-text-primary);
}

.theme-text-secondary {
  color: var(--color-text-secondary);
}

.theme-input {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
}

.theme-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
