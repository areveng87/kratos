<template>
  <Sidebar>
    <div class="flex-1 overflow-auto" style="background-color: var(--color-bg-primary)">
      <div class="p-6">
        <div class="mb-6">
          <h1 class="text-3xl font-bold theme-text">Personas Naturales</h1>
        </div>

        <div class="mb-4 flex justify-between items-center">
          <button
            @click="crearPersona"
            class="px-4 py-2 rounded-md text-white font-medium"
            style="background-color: var(--color-primary)"
          >
            Nueva Persona Natural
          </button>

          <div class="relative w-64">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar..."
              class="w-full px-4 py-2 rounded-md theme-input"
              style="border: 1px solid var(--color-border)"
            />
            <Search class="absolute right-3 top-2.5 h-5 w-5 theme-text-secondary" />
          </div>
        </div>

        <div class="rounded-lg overflow-hidden" style="border: 1px solid var(--color-border); background-color: var(--color-bg-secondary)">
          <table class="w-full">
            <thead style="background-color: var(--color-bg-primary); border-bottom: 1px solid var(--color-border)">
              <tr>
                <th class="px-4 py-3 text-left text-sm font-semibold theme-text">Nombre</th>
                <th class="px-4 py-3 text-left text-sm font-semibold theme-text">Apellidos</th>
                <th class="px-4 py-3 text-left text-sm font-semibold theme-text">Tipo Documento</th>
                <th class="px-4 py-3 text-left text-sm font-semibold theme-text">NIF</th>
                <th class="px-4 py-3 text-left text-sm font-semibold theme-text">Residencia</th>
                <th class="px-4 py-3 text-left text-sm font-semibold theme-text">Nacionalidad</th>
                <th class="px-4 py-3 text-center text-sm font-semibold theme-text">Riesgos</th>
                <th class="px-4 py-3 text-center text-sm font-semibold theme-text">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="persona in filteredPersonas"
                :key="persona.id"
                class="border-b hover:bg-opacity-50"
                style="border-color: var(--color-border)"
                :style="{ 'background-color': 'var(--color-bg-secondary)' }"
              >
                <td class="px-4 py-3 text-sm theme-text">{{ persona.nombre || '-' }}</td>
                <td class="px-4 py-3 text-sm theme-text">{{ persona.apellido || '-' }}</td>
                <td class="px-4 py-3 text-sm theme-text">{{ persona.tipodocumento_nombre || '-' }}</td>
                <td class="px-4 py-3 text-sm theme-text">{{ persona.nif || '-' }}</td>
                <td class="px-4 py-3 text-sm theme-text">{{ persona.residencia_nombre || '-' }}</td>
                <td class="px-4 py-3 text-sm theme-text">{{ persona.nacionalidad_nombre || '-' }}</td>
                <td class="px-4 py-3 text-center">
                  <AlertTriangle
                    v-if="persona.riesgo"
                    class="h-5 w-5 mx-auto"
                    style="color: var(--color-error)"
                  />
                  <span v-else class="text-sm theme-text-secondary">-</span>
                </td>
                <td class="px-4 py-3 text-center">
                  <button
                    @click="editarPersona(persona.id)"
                    class="p-2 rounded hover:bg-opacity-10"
                    style="color: var(--color-primary)"
                    title="Editar"
                  >
                    <Edit class="h-4 w-4" />
                  </button>
                </td>
              </tr>
              <tr v-if="filteredPersonas.length === 0">
                <td colspan="8" class="px-4 py-8 text-center theme-text-secondary">
                  No se encontraron personas naturales
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { Search, Edit, AlertTriangle } from 'lucide-vue-next'
import api from '../api'

const router = useRouter()
const personas = ref([])
const searchQuery = ref('')

const filteredPersonas = computed(() => {

  console.log('Filtrando personas con query:', searchQuery.value)
  
  if (!searchQuery.value) return personas.value

  const query = searchQuery.value.toLowerCase()
  return personas.value.filter(persona => {
    return (
      (persona.nombre && persona.nombre.toLowerCase().includes(query)) ||
      (persona.apellido && persona.apellido.toLowerCase().includes(query)) ||
      (persona.nif && persona.nif.toLowerCase().includes(query)) ||
      (persona.tipodocumento_nombre && persona.tipodocumento_nombre.toLowerCase().includes(query)) ||
      (persona.residencia_nombre && persona.residencia_nombre.toLowerCase().includes(query)) ||
      (persona.nacionalidad_nombre && persona.nacionalidad_nombre.toLowerCase().includes(query))
    )
  })
})

const cargarPersonas = async () => {
  try {
    const response = await api.personasNaturales.getAll()

    console.log('Personas naturales cargadas:', response.data)

    personas.value = response.data.data
  } catch (error) {
    console.error('Error cargando personas:', error)
  }
}

const crearPersona = () => {
  router.push('/personas-naturales/nueva')
}

const editarPersona = (id) => {
  router.push(`/personas-naturales/${id}/editar`)
}

onMounted(() => {
  cargarPersonas()
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
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
}
</style>
