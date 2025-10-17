<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <div 
      class="bg-white shadow-lg transition-all duration-300 ease-in-out"
      :class="sidebarCollapsed ? 'w-16' : 'w-64'"
      @mouseenter="sidebarCollapsed = false"
      @mouseleave="sidebarCollapsed = true"
    >
      <div class="p-4">
        <!-- Logo -->
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-sm">K</span>
          </div>
          <h1 v-show="!sidebarCollapsed" class="text-xl font-bold text-gray-800">KRATOS</h1>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="mt-8">
        <div class="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
          <span v-show="!sidebarCollapsed">MENÚ PRINCIPAL</span>
        </div>
        
        <div class="space-y-1">
          <a 
            v-for="item in navigationItems" 
            :key="item.name"
            href="#" 
            class="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors"
            :class="{ 'bg-blue-50 text-blue-600': item.active }"
          >
            <component :is="item.icon" class="w-5 h-5" />
            <span v-show="!sidebarCollapsed" class="ml-3">{{ item.name }}</span>
          </a>
        </div>

        <!-- User Role Badge -->
        <div v-show="!sidebarCollapsed" class="mt-8 px-4">
          <div class="bg-blue-100 text-blue-800 px-3 py-2 rounded-lg text-sm">
            <div class="font-medium">{{ currentUser.name }}</div>
            <div class="text-xs">{{ getRoleName(currentUser.role) }}</div>
          </div>
        </div>

        <!-- Logout -->
        <div class="absolute bottom-4 w-full px-4">
          <button 
            @click="logout"
            class="flex items-center w-full px-4 py-3 text-gray-700 hover:bg-red-50 hover:text-red-600 transition-colors rounded-lg"
          >
            <LogOut class="w-5 h-5" />
            <span v-show="!sidebarCollapsed" class="ml-3">Cerrar Sesión</span>
          </button>
        </div>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-hidden">
      <!-- Header -->
      <header class="bg-white shadow-sm border-b border-gray-200">
        <div class="px-6 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-2xl font-semibold text-gray-900">Dashboard - {{ getRoleName(currentUser.role) }}</h1>
              <p class="text-gray-600">Panel de control del sistema Kratos</p>
            </div>
            <div class="flex items-center space-x-4">
              <div class="relative">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input 
                  type="text" 
                  placeholder="Buscar..." 
                  class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span class="text-white text-sm font-medium">{{ currentUser.name.charAt(0) }}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- Dashboard Content -->
      <main class="p-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div 
            v-for="stat in dashboardStats" 
            :key="stat.title"
            class="bg-white rounded-xl shadow-sm p-6 border border-gray-100"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-600 text-sm font-medium">{{ stat.title }}</p>
                <p class="text-2xl font-bold text-gray-900 mt-1">{{ stat.value }}</p>
                <div class="flex items-center mt-2">
                  <span 
                    class="text-sm font-medium"
                    :class="stat.change > 0 ? 'text-green-600' : 'text-red-600'"
                  >
                    {{ stat.change > 0 ? '+' : '' }}{{ stat.change }}%
                  </span>
                  <component 
                    :is="stat.change > 0 ? 'TrendingUp' : 'TrendingDown'" 
                    class="w-4 h-4 ml-1"
                    :class="stat.change > 0 ? 'text-green-600' : 'text-red-600'"
                  />
                </div>
              </div>
              <div class="w-16 h-12">
                <!-- Mini chart placeholder -->
                <svg class="w-full h-full" viewBox="0 0 64 48">
                  <path 
                    :d="generateMiniChart()" 
                    fill="none" 
                    :stroke="stat.change > 0 ? '#10b981' : '#ef4444'" 
                    stroke-width="2"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Revenue Overview -->
          <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-gray-900">Resumen de Operaciones</h3>
              <select class="border border-gray-300 rounded-lg px-3 py-1 text-sm">
                <option>Última Semana</option>
                <option>Último Mes</option>
                <option>Último Trimestre</option>
              </select>
            </div>
            <div class="h-64">
              <!-- Chart placeholder -->
              <div class="flex items-end justify-between h-full space-x-2">
                <div 
                  v-for="(day, index) in weeklyData" 
                  :key="index"
                  class="flex-1 bg-blue-500 rounded-t-lg opacity-80 hover:opacity-100 transition-opacity cursor-pointer"
                  :style="{ height: day.value + '%' }"
                  :title="`${day.day}: ${day.actual}`"
                ></div>
              </div>
              <div class="flex justify-between mt-2 text-xs text-gray-500">
                <span v-for="day in weeklyData" :key="day.day">{{ day.day }}</span>
              </div>
            </div>
          </div>

          <!-- Users by Role -->
          <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 mb-6">Usuarios por Rol</h3>
            <div class="space-y-4">
              <div 
                v-for="role in usersByRole" 
                :key="role.name"
                class="flex items-center justify-between"
              >
                <div class="flex items-center space-x-3">
                  <div 
                    class="w-3 h-3 rounded-full"
                    :style="{ backgroundColor: role.color }"
                  ></div>
                  <span class="text-gray-700">{{ role.name }}</span>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-gray-900 font-medium">{{ role.count }}</span>
                  <div class="w-20 h-2 bg-gray-200 rounded-full">
                    <div 
                      class="h-full rounded-full"
                      :style="{ 
                        width: (role.count / Math.max(...usersByRole.map(r => r.count))) * 100 + '%',
                        backgroundColor: role.color 
                      }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100">
          <div class="p-6 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Actividad Reciente</h3>
              <div class="relative">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input 
                  type="text" 
                  placeholder="Buscar actividad..." 
                  class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm"
                />
              </div>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuario</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acción</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Empresa</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="activity in recentActivity" :key="activity.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <span class="text-blue-600 text-sm font-medium">{{ activity.user.charAt(0) }}</span>
                      </div>
                      <div class="ml-3">
                        <div class="text-sm font-medium text-gray-900">{{ activity.user }}</div>
                        <div class="text-sm text-gray-500">{{ activity.role }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ activity.action }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ activity.company }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                      :class="getStatusClass(activity.status)"
                    >
                      {{ activity.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ activity.date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  Home, 
  Users, 
  Settings, 
  Building2, 
  LogOut, 
  Search, 
  TrendingUp, 
  TrendingDown,
  BarChart3,
  Shield
} from 'lucide-vue-next'

// Reactive data
const sidebarCollapsed = ref(true)

const currentUser = ref({
  name: 'Juan Pérez',
  role: 1, // 1 = Administrador
  email: 'juan.perez@kratos.com'
})

const navigationItems = ref([
  { name: 'Dashboard', icon: Home, active: true },
  { name: 'Sociedades', icon: Building2, active: false },
  { name: 'Operaciones', icon: BarChart3, active: false },
  { name: 'SPV', icon: Shield, active: false },
  { name: 'Configuración', icon: Settings, active: false }
])

const dashboardStats = ref([
  { title: 'Usuarios Activos', value: '127', change: 12 },
  { title: 'Empresas', value: '45', change: 8 },
  { title: 'Operaciones', value: '1,234', change: -3 },
  { title: 'Sociedades', value: '89', change: 15 }
])

const weeklyData = ref([
  { day: 'LUN', value: 65, actual: 45 },
  { day: 'MAR', value: 45, actual: 32 },
  { day: 'MIE', value: 85, actual: 67 },
  { day: 'JUE', value: 75, actual: 54 },
  { day: 'VIE', value: 55, actual: 38 },
  { day: 'SAB', value: 35, actual: 23 },
  { day: 'DOM', value: 25, actual: 15 }
])

const usersByRole = ref([
  { name: 'Administrador', count: 5, color: '#3b82f6' },
  { name: 'Analista PBC', count: 12, color: '#10b981' },
  { name: 'OCI Interno', count: 8, color: '#f59e0b' },
  { name: 'OCI Externo', count: 15, color: '#ef4444' },
  { name: 'SPV', count: 6, color: '#8b5cf6' },
  { name: 'Servicer Supervisor', count: 4, color: '#06b6d4' },
  { name: 'Servicer Operator', count: 18, color: '#84cc16' }
])

const recentActivity = ref([
  {
    id: 1,
    user: 'María García',
    role: 'Analista PBC',
    action: 'Creó nueva operación',
    company: 'Inmobiliaria ABC',
    status: 'Completado',
    date: '2 min'
  },
  {
    id: 2,
    user: 'Carlos López',
    role: 'SPV',
    action: 'Actualizó sociedad',
    company: 'Constructora XYZ',
    status: 'En Proceso',
    date: '5 min'
  },
  {
    id: 3,
    user: 'Ana Martín',
    role: 'OCI Interno',
    action: 'Revisión de documentos',
    company: 'Desarrollos DEF',
    status: 'Pendiente',
    date: '12 min'
  }
])

// Methods
const getRoleName = (roleId) => {
  const roles = {
    1: 'Administrador',
    2: 'Analista PBC',
    3: 'OCI Interno',
    4: 'OCI Externo',
    5: 'SPV',
    6: 'Servicer Supervisor',
    7: 'Servicer Operator',
    8: 'Auditor'
  }
  return roles[roleId] || 'Usuario'
}

const getStatusClass = (status) => {
  const classes = {
    'Completado': 'bg-green-100 text-green-800',
    'En Proceso': 'bg-yellow-100 text-yellow-800',
    'Pendiente': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const generateMiniChart = () => {
  // Simple line chart path
  return 'M0,40 Q16,20 32,30 T64,10'
}

const logout = () => {
  // Implementar lógica de logout
  console.log('Cerrando sesión...')
}
</script>
