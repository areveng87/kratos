<template>
  <Sidebar>
    <div class="p-6">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-4">
          <button
            @click="handleGoBack"
            class="flex items-center px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <ArrowLeft class="w-4 h-4 mr-2" />
            Volver
          </button>
          <h1 class="text-2xl font-bold text-gray-900">
            Detalles de Operación
          </h1>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <AlertCircle class="h-5 w-5 text-red-400" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error</h3>
            <div class="mt-2 text-sm text-red-700">
              {{ error }}
            </div>
          </div>
        </div>
      </div>

      <!-- Operation details -->
      <div v-else-if="operacion" class="space-y-6">
        <!-- Main info card -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Información General</h2>
          </div>
          <div class="px-6 py-4">
            <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
              <div>
                <dt class="text-sm font-medium text-gray-500">ID</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ operacion.id }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Referencia Expediente</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ operacion.referencia_expediente || '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Sociedad</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ operacion.sociedad || '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Estado</dt>
                <dd class="mt-1">
                  <span v-if="operacion.estado" 
                    class="inline-flex px-2 py-1 text-xs font-semibold rounded"
                    :class="getEstadoClass(operacion.estado)">
                    {{ operacion.estado }}
                  </span>
                  <span v-else class="text-gray-400">-</span>
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Urgente</dt>
                <dd class="mt-1">
                  <div class="flex items-center">
                    <AlertTriangle v-if="operacion.urgente" class="w-4 h-4 text-red-500" />
                    <Minus v-else class="w-4 h-4 text-gray-400" />
                    <span class="ml-2 text-sm text-gray-900">
                      {{ operacion.urgente ? 'Sí' : 'No' }}
                    </span>
                  </div>
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Analista PBC</dt>
                <dd class="mt-1 text-sm text-gray-900">
                  {{ operacion.analista_pbc_nombre || '-' }}
                </dd>
              </div>
            </dl>
          </div>
        </div>

        <!-- Additional details card -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Detalles Adicionales</h2>
          </div>
          <div class="px-6 py-4">
            <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
              <div>
                <dt class="text-sm font-medium text-gray-500">Servicer</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ operacion.servicer || '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Tipo de Operación</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ operacion.tipo_operacion || '-' }}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Fecha Prevista Firma</dt>
                <dd class="mt-1 text-sm text-gray-900">
                  {{ operacion.fecha_prevista_firma || '-' }}
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Fecha Útil Cambio</dt>
                <dd class="mt-1 text-sm text-gray-900">
                  {{ operacion.fecha_util_cambio || '-' }}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import { ArrowLeft, AlertCircle, AlertTriangle, Minus } from 'lucide-vue-next'
import { api } from '../api'

// Hooks at the top level
const route = useRoute()
const router = useRouter()

// Reactive state
const operacion = ref(null)
const loading = ref(true)
const error = ref(null)

// Methods
const getEstadoClass = (estado) => {
  const classes = {
    'Aprobado': 'bg-green-100 text-green-800',
    'Pendiente': 'bg-yellow-100 text-yellow-800',
    'Rechazado': 'bg-red-100 text-red-800',
    'En Proceso': 'bg-blue-100 text-blue-800',
    'Analizando Riesgos': 'bg-yellow-100 text-yellow-800',
    'Sin Hitos': 'bg-gray-100 text-gray-800',
    'Elevado a OCI': 'bg-red-100 text-red-800'
  }
  return classes[estado] || 'bg-gray-100 text-gray-800'
}

const handleGoBack = () => {
  router.go(-1)
}

const loadOperacion = async () => {
  try {
    const operacionId = route.params.id
    if (!operacionId) {
      throw new Error('ID de operación no proporcionado')
    }

    const response = await api.operaciones.getPlanner()
    const operaciones = response.data
    operacion.value = operaciones.find(op => op.id == operacionId)
    
    if (!operacion.value) {
      throw new Error('Operación no encontrada')
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadOperacion()
})
</script>
