<template>
  <Sidebar>
    <div class="flex-1 p-6 overflow-auto" style="background-color: var(--color-bg-primary)">
      <div class="mb-6">
        <h1 class="text-2xl font-bold" style="color: var(--color-text-primary)">
          {{ isNew ? 'Nuevo Proceso' : 'Editar Proceso' }}
        </h1>
        <p class="mt-1" style="color: var(--color-text-secondary)">
          {{ isNew ? 'Crear un nuevo proceso' : 'Modificar proceso existente' }}
        </p>
      </div>

      <!-- Formulario principal -->
      <div class="rounded-lg p-6 mb-6" style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block mb-2 font-medium" style="color: var(--color-text-primary)">
              Descripción <span class="text-red-500">*</span>
            </label>
            <input
              v-model="proceso.descripcion"
              type="text"
              class="w-full px-4 py-2 rounded-lg border"
              style="background-color: var(--color-bg-primary); border-color: var(--color-border); color: var(--color-text-primary)"
              placeholder="Descripción del proceso"
              required
            />
          </div>

          <div>
            <label class="block mb-2 font-medium" style="color: var(--color-text-primary)">Prefijo</label>
            <input
              v-model="proceso.prefijo"
              type="text"
              class="w-full px-4 py-2 rounded-lg border"
              style="background-color: var(--color-bg-primary); border-color: var(--color-border); color: var(--color-text-primary)"
              placeholder="Prefijo del proceso"
            />
          </div>

          <div>
            <label class="flex items-center space-x-2 cursor-pointer">
              <input
                v-model="proceso.visibilidad"
                type="checkbox"
                class="w-4 h-4 rounded"
                style="accent-color: var(--color-primary)"
              />
              <span style="color: var(--color-text-primary)">Proceso visible</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Tablas de acciones disponibles y del proceso -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Tabla de acciones disponibles -->
        <div class="rounded-lg p-6" style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)">
          <h3 class="text-lg font-semibold mb-4" style="color: var(--color-text-primary)">Acciones Disponibles (doble clic para agregar)</h3>
          
          <div v-if="accionesDisponibles.length === 0" class="text-center py-8" style="color: var(--color-text-secondary)">
            No hay acciones disponibles
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr style="border-bottom: 1px solid var(--color-border)">
                  <th class="text-left p-3" style="color: var(--color-text-primary)">Descripción</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="accion in accionesDisponibles"
                  :key="accion.idaccion"
                  @dblclick="agregarAccion(accion)"
                  class="border-b cursor-pointer hover:bg-opacity-50 transition-colors"
                  style="border-color: var(--color-border); background-color: var(--color-bg-primary)"
                  title="Doble clic para agregar"
                >
                  <td class="p-3" style="color: var(--color-text-primary)">{{ accion.descripcion }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Tabla de acciones del proceso -->
        <div class="rounded-lg p-6" style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)">
          <h3 class="text-lg font-semibold mb-4" style="color: var(--color-text-primary)">Acciones del Proceso</h3>
          
          <div v-if="estados.length === 0" class="text-center py-8" style="color: var(--color-text-secondary)">
            No hay acciones agregadas
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr style="border-bottom: 1px solid var(--color-border)">
                  <th class="text-left p-3" style="color: var(--color-text-primary)">Orden</th>
                  <th class="text-left p-3" style="color: var(--color-text-primary)">Descripción</th>
                  <th class="text-center p-3" style="color: var(--color-text-primary)">Finaliza</th>
                  <th class="text-center p-3" style="color: var(--color-text-primary)">Visible</th>
                  <th class="text-center p-3" style="color: var(--color-text-primary)">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(estado, index) in estados"
                  :key="estado.tempId"
                  draggable="true"
                  @dragstart="onDragStart(index)"
                  @dragover.prevent
                  @drop="onDrop(index)"
                  @contextmenu.prevent="mostrarMenuContextual($event, index)"
                  class="border-b cursor-move hover:bg-opacity-50 transition-colors"
                  style="border-color: var(--color-border); background-color: var(--color-bg-primary)"
                >
                  <td class="p-3" style="color: var(--color-text-primary)">{{ index + 1 }}</td>
                  <td class="p-3" style="color: var(--color-text-primary)">{{ estado.titulo }}</td>
                  <td class="p-3 text-center">
                    <button @click="toggleFinaliza(index)" class="inline-flex items-center justify-center">
                      <CheckCircle2 v-if="estado.finaliza" :size="20" style="color: var(--color-success)" />
                      <Circle v-else :size="20" style="color: var(--color-text-tertiary)" />
                    </button>
                  </td>
                  <td class="p-3 text-center">
                    <button @click="toggleVisible(index)" class="inline-flex items-center justify-center">
                      <Eye v-if="estado.visibilidad" :size="20" style="color: var(--color-success)" />
                      <EyeOff v-else :size="20" style="color: var(--color-text-tertiary)" />
                    </button>
                  </td>
                  <td class="p-3">
                    <div class="flex space-x-2 justify-center">
                      <button class="btn-secondary-sm" title="Roles">
                        <Users :size="16" />
                      </button>
                      <button @click="eliminarEstado(index)" 
                      class="btn-danger-sm" 
                      title="Eliminar">
                        <Trash2 :size="16" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Menú contextual -->
      <div
        v-if="menuContextual.visible"
        :style="{ top: menuContextual.y + 'px', left: menuContextual.x + 'px' }"
        class="fixed z-50 rounded-lg shadow-lg py-2"
        style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)"
        @click="cerrarMenuContextual"
      >
        <button
          @click="moverArriba"
          :disabled="menuContextual.index === 0"
          class="w-full px-4 py-2 text-left hover:bg-opacity-50 transition-colors flex items-center space-x-2"
          :class="{ 'opacity-50 cursor-not-allowed': menuContextual.index === 0 }"
          style="color: var(--color-text-primary)"
        >
          <ArrowUp :size="16" />
          <span>Subir</span>
        </button>
        <button
          @click="moverAbajo"
          :disabled="menuContextual.index === estados.length - 1"
          class="w-full px-4 py-2 text-left hover:bg-opacity-50 transition-colors flex items-center space-x-2"
          :class="{ 'opacity-50 cursor-not-allowed': menuContextual.index === estados.length - 1 }"
          style="color: var(--color-text-primary)"
        >
          <ArrowDown :size="16" />
          <span>Bajar</span>
        </button>
      </div>

      <!-- Botones de acción -->
      <div class="flex justify-end gap-3">
        <button @click="cancelar" class="btn-secondary">Cancelar</button>
        <button @click="guardar" class="btn-primary" :disabled="!proceso.descripcion">Guardar</button>
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Plus, Trash2, Users, Eye, EyeOff, CheckCircle2, Circle, ArrowUp, ArrowDown } from 'lucide-vue-next'
import Sidebar from '../../components/Sidebar.vue'
import api from '../../api'

const router = useRouter()
const route = useRoute()

const isNew = computed(() => route.params.id === undefined || route.params.id === 'nuevo')

const proceso = ref({
  descripcion: '',
  prefijo: '',
  visibilidad: true
})

const acciones = ref([])
const estados = ref([])
const draggedIndex = ref(null)

const menuContextual = ref({
  visible: false,
  x: 0,
  y: 0,
  index: null
})

const accionesDisponibles = computed(() => {
  const accionesAgregadas = new Set(estados.value.map(e => e.idaccion))
  return acciones.value.filter(accion => !accionesAgregadas.has(accion.idaccion))
})

const cargarAcciones = async () => {
  try {
    const response = await api.acciones.getDisponibles()
    acciones.value = response.data.data || []
  } catch (error) {
    console.error('Error al cargar acciones:', error)
    alert('Error al cargar las acciones disponibles')
  }
}

const cargarProceso = async () => {
  if (isNew.value) return
  
  try {
    const [procesoResponse, estadosResponse] = await Promise.all([
      api.procesos.getById(route.params.id),
      api.procesos.getEstados(route.params.id)
    ])
    
    const procesoData = procesoResponse.data.data
    proceso.value = {
      descripcion: procesoData.descripcion,
      prefijo: procesoData.prefijo,
      visibilidad: procesoData.visibilidad === 1
    }
    
    estados.value = (estadosResponse.data.data || []).map((estado, index) => ({
      ...estado,
      tempId: `estado-${index}-${Date.now()}`
    }))
  } catch (error) {
    console.error('Error al cargar proceso:', error)
    alert('Error al cargar el proceso')
  }
}

const agregarAccion = (accion) => {
  estados.value.push({
    tempId: `estado-${Date.now()}`,
    idaccion: accion.idaccion,
    titulo: accion.descripcion,
    visibilidad: true,
    finaliza: false,
    orden: estados.value.length + 1
  })
}

const eliminarEstado = (index) => {
  if (confirm('¿Está seguro de eliminar esta acción?')) {
    estados.value.splice(index, 1)
  }
}

const toggleFinaliza = (index) => {
  estados.value[index].finaliza = !estados.value[index].finaliza
}

const toggleVisible = (index) => {
  estados.value[index].visibilidad = !estados.value[index].visibilidad
}

const onDragStart = (index) => {
  draggedIndex.value = index
}

const onDrop = (dropIndex) => {
  if (draggedIndex.value === null) return
  
  const draggedItem = estados.value[draggedIndex.value]
  estados.value.splice(draggedIndex.value, 1)
  estados.value.splice(dropIndex, 0, draggedItem)
  draggedIndex.value = null
}

const mostrarMenuContextual = (event, index) => {
  menuContextual.value = {
    visible: true,
    x: event.clientX,
    y: event.clientY,
    index
  }
}

const cerrarMenuContextual = () => {
  menuContextual.value.visible = false
}

const moverArriba = () => {
  const index = menuContextual.value.index
  if (index > 0) {
    const item = estados.value[index]
    estados.value.splice(index, 1)
    estados.value.splice(index - 1, 0, item)
  }
  cerrarMenuContextual()
}

const moverAbajo = () => {
  const index = menuContextual.value.index
  if (index < estados.value.length - 1) {
    const item = estados.value[index]
    estados.value.splice(index, 1)
    estados.value.splice(index + 1, 0, item)
  }
  cerrarMenuContextual()
}

const guardar = async () => {
  if (!proceso.value.descripcion) {
    alert('La descripción es obligatoria')
    return
  }

  console.log('estados:', estados.value )
  
  const data = {
    descripcion: proceso.value.descripcion,
    prefijo: proceso.value.prefijo || '',
    visibilidad: proceso.value.visibilidad ? 1 : 0,
    estados: estados.value.map((estado, index) => ({
      idaccion: estado.idaccion,
      titulo: estado.titulo,
      visibilidad: estado.visibilidad,
      finaliza: estado.finaliza,
      orden: index + 1
    }))
  }
  
  try {
    if (isNew.value) {

      console.log(data)

      await api.procesos.createCompleto(data)
      alert('Proceso creado correctamente')
    } else {
      await api.procesos.updateCompleto(route.params.id, data)
      alert('Proceso actualizado correctamente')
    }
    router.push('/admin/definicion-procesos')
  } catch (error) {
    console.error('Error al guardar proceso:', error)
    alert(error.response?.data?.detail || 'Error al guardar el proceso')
  }
}

const cancelar = () => {
  router.push('/admin/definicion-procesos')
}

onMounted(async () => {
  await cargarAcciones()
  await cargarProceso()
  
  // Cerrar menú contextual al hacer clic fuera
  document.addEventListener('click', (e) => {
    if (menuContextual.value.visible && !e.target.closest('.menu-contextual')) {
      cerrarMenuContextual()
    }
  })
})
</script>

<style scoped>
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: opacity 0.2s;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary-sm {
  background-color: var(--color-primary);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: opacity 0.2s;
}

.btn-primary-sm:hover {
  opacity: 0.9;
}

.btn-secondary {
  background-color: var(--color-bg-tertiary);
  color: var(--color-text-primary);
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 0.2s;
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background-color: var(--color-bg-hover);
}

.btn-secondary-sm {
  background-color: var(--color-bg-tertiary);
  color: var(--color-text-primary);
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: background-color 0.2s;
  border: 1px solid var(--color-border);
}

.btn-secondary-sm:hover {
  background-color: var(--color-bg-hover);
}

.btn-danger-sm {
  background-color: #ef4444;
  color: white;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: opacity 0.2s;
}

.btn-danger-sm:hover {
  opacity: 0.9;
}
</style>
