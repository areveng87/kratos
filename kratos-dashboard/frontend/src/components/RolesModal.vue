<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click.self="cerrar"
  >
    <div
      class="rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto"
      style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)"
    >
      <!-- Header -->
      <div class="mb-6">
        <h2 class="text-xl font-bold" style="color: var(--color-text-primary)">
          Gestión de Roles - {{ estadoNombre }}
        </h2>
        <p class="mt-1" style="color: var(--color-text-secondary)">
          Asignar roles y permisos para esta acción
        </p>
      </div>

      <!-- Selector de roles -->
      <div class="mb-6 flex gap-2">
        <select
          v-model="rolSeleccionado"
          class="flex-1 px-4 py-2 rounded-lg border"
          style="background-color: var(--color-bg-primary); border-color: var(--color-border); color: var(--color-text-primary)"
        >
          <option value="">Seleccione un rol...</option>
          <option v-for="rol in rolesDisponibles" :key="rol.id" :value="rol.id">
            {{ rol.nombre }}
          </option>
        </select>
        <button
          @click="agregarRol"
          :disabled="!rolSeleccionado"
          class="btn-primary"
        >
          Agregar
        </button>
      </div>

      <!-- Tabla de roles asignados -->
      <div v-if="rolesAsignados.length === 0" class="text-center py-8" style="color: var(--color-text-secondary)">
        No hay roles asignados
      </div>

      <div v-else class="overflow-x-auto mb-6">
        <table class="w-full">
          <thead>
            <tr style="border-bottom: 1px solid var(--color-border)">
              <th class="text-left p-3" style="color: var(--color-text-primary)">Rol</th>
              <th class="text-center p-3" style="color: var(--color-text-primary)">Lectura</th>
              <th class="text-center p-3" style="color: var(--color-text-primary)">Escritura</th>
              <th class="text-center p-3" style="color: var(--color-text-primary)">Cambio Fase</th>
              <th class="text-center p-3" style="color: var(--color-text-primary)">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(rolAsignado, index) in rolesAsignados"
              :key="rolAsignado.idrol"
              class="border-b"
              style="border-color: var(--color-border)"
            >
              <td class="p-3" style="color: var(--color-text-primary)">
                {{ obtenerNombreRol(rolAsignado.idrol) }}
              </td>
              <td class="p-3 text-center">
                <button @click="togglePermiso(index, 'lectura')" class="inline-flex items-center justify-center">
                  <CheckCircle2 v-if="rolAsignado.lectura" :size="20" style="color: var(--color-success)" />
                  <Circle v-else :size="20" style="color: var(--color-text-tertiary)" />
                </button>
              </td>
              <td class="p-3 text-center">
                <button @click="togglePermiso(index, 'escritura')" class="inline-flex items-center justify-center">
                  <CheckCircle2 v-if="rolAsignado.escritura" :size="20" style="color: var(--color-success)" />
                  <Circle v-else :size="20" style="color: var(--color-text-tertiary)" />
                </button>
              </td>
              <td class="p-3 text-center">
                <button @click="togglePermiso(index, 'cambioestado')" class="inline-flex items-center justify-center">
                  <CheckCircle2 v-if="rolAsignado.cambioestado" :size="20" style="color: var(--color-success)" />
                  <Circle v-else :size="20" style="color: var(--color-text-tertiary)" />
                </button>
              </td>
              <td class="p-3 text-center">
                <button @click="eliminarRol(index)" class="btn-danger-sm" title="Eliminar">
                  <Trash2 :size="16" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Botones de acción -->
      <div class="flex justify-end gap-3">
        <button @click="cerrar" class="btn-secondary">Cancelar</button>
        <button @click="guardar" class="btn-primary">Guardar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { CheckCircle2, Circle, Trash2 } from 'lucide-vue-next'
import api from '../api'

const props = defineProps({
  idproceso: {
    type: Number,
    required: true
  },
  idestado: {
    type: Number,
    required: true
  },
  estadoNombre: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'saved'])

const roles = ref([])
const rolesAsignados = ref([])
const rolSeleccionado = ref('')

const rolesDisponibles = computed(() => {
  const asignadosIds = new Set(rolesAsignados.value.map(r => r.idrol))
  return roles.value.filter(rol => !asignadosIds.has(rol.id))
})

const cargarRoles = async () => {
  try {
    const response = await api.roles.getAll()
    roles.value = response.data.data || []
  } catch (error) {
    console.error('Error al cargar roles:', error)
    alert('Error al cargar los roles disponibles')
  }
}

const cargarRolesAsignados = async () => {
  if (!props.idproceso || !props.idestado) return
  
  try {
    const response = await api.estadoRoles.getByEstado(props.idproceso, props.idestado)
    rolesAsignados.value = response.data.data || []
  } catch (error) {
    console.error('Error al cargar roles asignados:', error)
    rolesAsignados.value = []
  }
}

const obtenerNombreRol = (idrol) => {
  const rol = roles.value.find(r => r.id === idrol)
  return rol ? rol.nombre : 'Desconocido'
}

const agregarRol = () => {
  if (!rolSeleccionado.value) return
  
  rolesAsignados.value.push({
    idrol: parseInt(rolSeleccionado.value),
    lectura: true,
    escritura: false,
    cambioestado: false
  })
  
  rolSeleccionado.value = ''
}

const eliminarRol = (index) => {
  if (confirm('¿Está seguro de eliminar este rol?')) {
    rolesAsignados.value.splice(index, 1)
  }
}

const togglePermiso = (index, permiso) => {
  rolesAsignados.value[index][permiso] = !rolesAsignados.value[index][permiso]
}

const guardar = async () => {
  try {
    console.log('Guardando roles para proceso', props.idproceso, 'estado', props.idestado, 'roles:', rolesAsignados.value)
    await api.estadoRoles.saveAll(props.idproceso, props.idestado, {
      idproceso: props.idproceso,
      idestado: props.idestado,
      roles: rolesAsignados.value
    })
    alert('Roles guardados correctamente')
    emit('saved')
    cerrar()
  } catch (error) {
    console.error('Error al guardar roles:', error)
    alert(error.response?.data?.detail || 'Error al guardar los roles')
  }
}

const cerrar = () => {
  emit('close')
}

watch(() => props.idproceso, async (newVal) => {
  if (newVal) {
    await cargarRoles()
    await cargarRolesAsignados()
  }
}, { immediate: true })
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
