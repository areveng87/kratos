<template>
  <Sidebar>
    <!-- Header -->
    <header class="header-bg header-border px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold theme-text">Dashboard</h1>
          <p class="text-gray-400">Bienvenido de vuelta, {{ welcomeMessage }}</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="text-right">
            <p class="text-sm text-gray-400">Último acceso</p>
            <p class="text-sm theme-text">{{ lastLoginFormatted }}</p>
          </div>
          <div class="h-8 w-8 bg-indigo-600 rounded-full flex items-center justify-center">
            <span class="text-sm font-medium text-white">
              {{ userInitials }}
            </span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 overflow-y-auto main-content p-6">
      <!-- Loading state -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Dashboard content -->
      <div v-else class="space-y-6">
        <!-- Metrics grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard
            title="Total Usuarios"
            :value="stats.total_usuarios"
            :change="12"
            :icon="Users"
            icon-bg-color="bg-blue-600"
            :chart-data="[10, 15, 12, 18, 20, 25, 22]"
            chart-color="#3b82f6"
          />
          
          <MetricCard
            title="Total Empresas"
            :value="stats.total_empresas"
            :change="8"
            :icon="Building2"
            icon-bg-color="bg-green-600"
            :chart-data="[5, 8, 6, 10, 12, 15, 14]"
            chart-color="#10b981"
          />
          
          <MetricCard
            title="Operaciones"
            :value="stats.total_operaciones"
            :change="24"
            :icon="ArrowRightLeft"
            icon-bg-color="bg-purple-600"
            :chart-data="[20, 25, 30, 28, 35, 40, 38]"
            chart-color="#8b5cf6"
          />
          
          <MetricCard
            title="Ingresos Mes"
            :value="stats.ingresos_mes"
            :change="15"
            :icon="DollarSign"
            icon-bg-color="bg-emerald-600"
            format="currency"
            :chart-data="[100000, 120000, 110000, 140000, 160000, 180000, 170000]"
            chart-color="#10b981"
          />
        </div>

        <!-- Charts and tables row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Revenue chart -->
          <Chart 
            title="Resumen de Operaciones"
            :data="chartData"
          />

          <!-- Recent operations -->
          <div class="card-bg card-border rounded-lg p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold theme-text">Operaciones Recientes</h3>
              <router-link 
                to="/operaciones" 
                class="text-indigo-400 hover:text-indigo-300 text-sm font-medium"
              >
                Ver todas
              </router-link>
            </div>

            <div class="space-y-4">
              <div 
                v-for="operacion in stats.operaciones_recientes" 
                :key="operacion.id"
                class="flex items-center justify-between p-4 table-row-bg rounded-lg hover:table-row-hover transition-colors"
              >
                <div class="flex items-center space-x-4">
                  <div :class="[
                    'p-2 rounded-lg',
                    operacion.tipo === 'VENTA' ? 'bg-green-600' : 'bg-blue-600'
                  ]">
                    <component 
                      :is="operacion.tipo === 'VENTA' ? TrendingUp : TrendingDown" 
                      class="h-4 w-4 text-white" 
                    />
                  </div>
                  <div>
                    <p class="theme-text font-medium">{{ operacion.empresa }}</p>
                    <p class="text-gray-400 text-sm">{{ operacion.tipo }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="theme-text font-medium">
                    {{ formatCurrency(operacion.monto) }}
                  </p>
                  <span :class="[
                    'status-badge',
                    operacion.estado === 'COMPLETADA' ? 'status-completed' :
                    operacion.estado === 'PENDIENTE' ? 'status-pending' :
                    operacion.estado === 'EN_PROCESO' ? 'status-processing' : 'status-cancelled'
                  ]">
                    {{ operacion.estado }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Bottom row -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Top companies -->
          <div class="card-bg card-border rounded-lg p-6">
            <h3 class="text-lg font-semibold theme-text mb-6">Empresas Más Activas</h3>
            <div class="space-y-4">
              <div 
                v-for="empresa in stats.empresas_activas" 
                :key="empresa.nombre"
                class="flex items-center justify-between"
              >
                <div class="flex items-center space-x-3">
                  <div class="h-8 w-8 bg-gray-600 rounded-lg flex items-center justify-center">
                    <Building2 class="h-4 w-4 text-gray-300" />
                  </div>
                  <span class="theme-text font-medium">{{ empresa.nombre }}</span>
                </div>
                <div class="text-right">
                  <p class="theme-text text-sm">{{ empresa.operaciones }} ops</p>
                  <p class="text-gray-400 text-xs">{{ formatCurrency(empresa.ventas) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick stats -->
          <div class="card-bg card-border rounded-lg p-6">
            <h3 class="text-lg font-semibold theme-text mb-6">Estadísticas Rápidas</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Operaciones Pendientes</span>
                <span class="theme-text font-medium">{{ stats.operaciones_pendientes }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Gastos del Mes</span>
                <span class="theme-text font-medium">{{ formatCurrency(stats.gastos_mes) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Balance</span>
                <span :class="[
                  'font-medium',
                  (stats.ingresos_mes - stats.gastos_mes) >= 0 ? 'text-green-400' : 'text-red-400'
                ]">
                  {{ formatCurrency(stats.ingresos_mes - stats.gastos_mes) }}
                </span>
              </div>
            </div>
          </div>

          <!-- System status -->
          <div class="card-bg card-border rounded-lg p-6">
            <h3 class="text-lg font-semibold theme-text mb-6">Estado del Sistema</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Base de Datos</span>
                <span class="flex items-center text-green-400">
                  <div class="h-2 w-2 bg-green-400 rounded-full mr-2"></div>
                  Conectada
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">API Backend</span>
                <span class="flex items-center text-green-400">
                  <div class="h-2 w-2 bg-green-400 rounded-full mr-2"></div>
                  Operativa
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400">Última Sincronización</span>
                <span class="theme-text text-sm">{{ formatTime(new Date()) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </Sidebar>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import Sidebar from '../components/Sidebar.vue'
import MetricCard from '../components/MetricCard.vue'
import Chart from '../components/Chart.vue'
import { 
  Users, 
  Building2, 
  ArrowRightLeft, 
  DollarSign,
  TrendingUp,
  TrendingDown
} from 'lucide-vue-next'
import { api } from '../api'

const authStore = useAuthStore()

const loading = ref(true)
const stats = ref({
  total_usuarios: 0,
  total_empresas: 0,
  total_operaciones: 0,
  operaciones_pendientes: 0,
  ingresos_mes: 0,
  gastos_mes: 0,
  operaciones_recientes: [],
  empresas_activas: []
})

const chartData = ref({
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  ventas: [120000, 150000, 180000, 160000, 200000, 220000],
  compras: [80000, 90000, 110000, 95000, 130000, 140000]
})

const welcomeMessage = computed(() => authStore.user?.nombre || 'Usuario')

const lastLoginFormatted = computed(() => {
  return formatDate(authStore.user?.ultimo_login)
})

const userInitials = computed(() => {
  const nombre = authStore.user?.nombre?.charAt(0) || ''
  const apellido = authStore.user?.apellido?.charAt(0) || ''
  return nombre + apellido
})

const loadDashboardData = async () => {
  try {
    loading.value = true
    const response = await api.dashboard.getStats()
    stats.value = response.data
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return 'No consta'
  return new Date(date).toLocaleDateString('es-CL', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('es-CL', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

onMounted(async () => {
  await loadDashboardData()
})
</script>

<style scoped>
.header-bg {
  background-color: var(--header-bg-color);
}

.header-border {
  border-bottom: 1px solid var(--header-border-color);
}

.main-content {
  background-color: var(--main-content-bg-color);
}

.card-bg {
  background-color: var(--card-bg-color);
}

.card-border {
  border: 1px solid var(--card-border-color);
}

.theme-text {
  color: var(--theme-text-color);
}

.table-row-bg {
  background-color: var(--table-row-bg-color);
}

.table-row-hover {
  background-color: var(--table-row-hover-color);
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  line-height: 1rem;
}

.status-completed {
  background-color: var(--status-completed-bg-color);
}

.status-pending {
  background-color: var(--status-pending-bg-color);
}

.status-processing {
  background-color: var(--status-processing-bg-color);
}

.status-cancelled {
  background-color: var(--status-cancelled-bg-color);
}
</style>
