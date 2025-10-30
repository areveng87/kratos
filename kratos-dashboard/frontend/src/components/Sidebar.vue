<template>
  <div class="flex h-screen theme-bg">
    <!-- Sidebar -->
    <div :class="sidebarClasses">
      <!-- Header -->
      <div class="p-4 border-b sidebar-border">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="h-8 w-8 bg-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span v-if="!isCollapsed" class="text-xl font-bold theme-text">Kratos</span>
          </div>
          <button
            @click="toggleSidebar"
            class="p-1.5 rounded-lg hover:bg-gray-700 text-gray-400 hover:text-white transition-colors flex-shrink-0"
          >
            <Menu class="h-5 w-5" />
          </button>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 p-4 space-y-2">
        <router-link
          to="/"
          class="sidebar-item"
          :class="{ 'justify-center': isCollapsed }"
        >
          <LayoutDashboard class="h-5 w-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" />
          <span v-if="!isCollapsed" class="font-medium">Dashboard</span>
        </router-link>

        <router-link
          to="/operaciones"
          class="sidebar-item"
          :class="{ 'justify-center': isCollapsed }"
        >
          <ArrowRightLeft class="h-5 w-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" />
          <span v-if="!isCollapsed" class="font-medium">Operaciones</span>
        </router-link>
        
        <router-link
          to="/empresas"
          class="sidebar-item"
          :class="{ 'justify-center': isCollapsed }"
        >
          <Building2 class="h-5 w-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" />
          <span v-if="!isCollapsed" class="font-medium">Empresas</span>
        </router-link>
        
        <router-link
          to="/sociedades"
          class="sidebar-item"
          :class="{ 'justify-center': isCollapsed }"
        >
          <Building class="h-5 w-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" />
          <span v-if="!isCollapsed" class="font-medium">Sociedades</span>
        </router-link>    
        
        <!-- Personas menu with submenus -->
        <div v-if="!isCollapsed" class="space-y-1">
          <button
            @click="togglePersonasMenu"
            class="sidebar-item w-full justify-between"
          >
            <div class="flex items-center">
              <UserCircle class="h-5 w-5 flex-shrink-0 mr-3" />
              <span class="font-medium">Personas</span>
            </div>
            <ChevronDown 
              class="h-4 w-4 transition-transform" 
              :class="{ 'rotate-180': isPersonasMenuOpen }"
            />
          </button>
          
          <div v-if="isPersonasMenuOpen" class="ml-8 space-y-1">
            <router-link
              to="/personas-naturales"
              class="sidebar-item text-sm"
            >
              <UserCircle class="h-4 w-4 flex-shrink-0 mr-2" />
              <span>Personas Naturales</span>
            </router-link>
            
            <router-link
              to="/personas-juridicas"
              class="sidebar-item text-sm"
            >
              <Building class="h-4 w-4 flex-shrink-0 mr-2" />
              <span>Personas Jurídicas</span>
            </router-link>
          </div>
        </div>

        <!-- v-if="canAccessAdmin && !isCollapsed-->

        <div v-if="!isCollapsed" class="space-y-1">
          <button
            @click="toggleAdminMenu"
            class="sidebar-item w-full justify-between"
          >
            <div class="flex items-center">
              <ShieldHalf class="h-5 w-5 flex-shrink-0 mr-3" />
              <span class="font-medium">Administración</span>
            </div>
            <ChevronDown 
              class="h-4 w-4 transition-transform" 
              :class="{ 'rotate-180': isAdminMenuOpen }"
            />
          </button>
          
          <div v-if="isAdminMenuOpen" class="ml-8 space-y-1">
            <router-link
              to="/admin/arbol-carpetas"
              class="sidebar-item text-sm"
            >
              <FolderTree class="h-4 w-4 flex-shrink-0 mr-2" />
              <span>Estructuras de carpetas</span>
            </router-link>
            
            <router-link
              to="/admin/usuarios"
              class="sidebar-item text-sm"
            >
              <Users class="h-4 w-4 flex-shrink-0 mr-2" />
              <span>Usuarios</span>
            </router-link>
            
            <router-link
              to="/admin/roles"
              class="sidebar-item text-sm"
            >
              <Shield class="h-4 w-4 flex-shrink-0 mr-2" />
              <span>Roles</span>
            </router-link>
            
            <router-link
              to="/admin/matrices-riesgo"
              class="sidebar-item text-sm"
            >
              <Grid3x3 class="h-4 w-4 flex-shrink-0 mr-2" />
              <span>Matrices de Riesgo</span>
            </router-link>
            
            <div class="space-y-1">
              <button
                @click="toggleAuxiliaresMenu"
                class="sidebar-item text-sm w-full justify-between"
              >
                <div class="flex items-center">
                  <Database class="h-4 w-4 flex-shrink-0 mr-2" />
                  <span>Auxiliares</span>
                </div>
                <ChevronDown 
                  class="h-3 w-3 transition-transform" 
                  :class="{ 'rotate-180': isAuxiliaresMenuOpen }"
                />
              </button>
              
              <div v-if="isAuxiliaresMenuOpen" class="ml-6 space-y-1">
                <router-link
                  to="/admin/auxiliares/relaciones"
                  class="sidebar-item text-sm"
                >
                  <Link class="h-4 w-4 flex-shrink-0 mr-2" />
                  <span>Relaciones</span>
                </router-link>
                
                <router-link
                  to="/admin/auxiliares/fondos"
                  class="sidebar-item text-sm"
                >
                  <Wallet class="h-4 w-4 flex-shrink-0 mr-2" />
                  <span>Fondos</span>
                </router-link>
                
                <!-- <router-link
                  to="/admin/auxiliares/servicers"
                  class="sidebar-item text-sm"
                >
                  <Briefcase class="h-4 w-4 flex-shrink-0 mr-2" />
                  <span>Servicers</span>
                </router-link>-->
                
                <router-link
                  to="/admin/auxiliares/tipos-alerta"
                  class="sidebar-item text-sm"
                >
                  <AlertTriangle class="h-4 w-4 flex-shrink-0 mr-2" />
                  <span>Tipos Alerta</span>
                </router-link>
              </div>
            </div>
            
            <router-link
              to="/admin/definicion-procesos"
              class="sidebar-item text-sm"
            >
              <GitBranch class="h-4 w-4 flex-shrink-0 mr-2" />
              <span>Definición de Procesos</span>
            </router-link>
          </div>
        </div>






        <router-link
          to="/configuracion"
          class="sidebar-item"
          :class="{ 'justify-center': isCollapsed }"
        >
          <Settings class="h-5 w-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" />
          <span v-if="!isCollapsed" class="font-medium">Configuración</span>
        </router-link>
      </nav>

      <!-- User section -->
      <div class="p-4 border-t sidebar-border">
        <div class="flex items-center" :class="{ 'justify-center': isCollapsed, 'space-x-3': !isCollapsed }">
          <div class="h-8 w-8 bg-indigo-600 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-sm font-medium text-white">
              {{ getUserInitials() }}
            </span>
          </div>
          <div v-if="!isCollapsed" class="flex-1 min-w-0">
            <p class="text-sm font-medium theme-text truncate">
              {{ getUserFullName() }}
            </p>
            <p class="text-xs text-gray-400 truncate">{{ authStore.user?.rol }}</p>
          </div>
          <button
            v-if="!isCollapsed"
            @click="handleLogout"
            class="p-1.5 rounded-lg hover:bg-gray-700 text-gray-400 hover:text-white transition-colors flex-shrink-0"
            title="Cerrar sesión"
          >
            <LogOut class="h-4 w-4" />
          </button>
        </div>
        <div v-if="isCollapsed" class="mt-2 flex justify-center">
          <button
            @click="handleLogout"
            class="p-1.5 rounded-lg hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
            title="Cerrar sesión"
          >
            <LogOut class="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { 
  Menu, 
  LayoutDashboard, 
  Building2, 
  Building,
  ArrowRightLeft, 
  Users,
  Settings, 
  LogOut,
  ChevronDown,
  FolderTree,
  Shield,
  Grid3x3,
  Database,
  Link,
  Wallet,
  Briefcase,
  AlertTriangle,
  GitBranch,
  ShieldHalf,
  UserCircle 
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const isCollapsed = ref(false)
const isAdminMenuOpen = ref(false)
const isAuxiliaresMenuOpen = ref(false)
const isPersonasMenuOpen = ref(false)

const sidebarClasses = computed(() => [
  'sidebar-bg border-r sidebar-border transition-all duration-300 flex flex-col',
  isCollapsed.value ? 'w-20' : 'w-64'
])

const canAccessAdmin = computed(() => {
  const userRole = authStore.user?.rol
  return userRole === 'Supervisor' || userRole === 'Administrador'
})

function getUserInitials() {
  if (!authStore.user) return ''
  const nombre = authStore.user.nombre ? authStore.user.nombre.charAt(0) : ''
  const apellido = authStore.user.apellido ? authStore.user.apellido.charAt(0) : ''
  return nombre + apellido
}

function getUserFullName() {
  if (!authStore.user) return ''
  const nombre = authStore.user.nombre || ''
  const apellido = authStore.user.apellido || ''
  return `${nombre} ${apellido}`.trim()
}

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

function toggleAdminMenu() {
  isAdminMenuOpen.value = !isAdminMenuOpen.value
}

function toggleAuxiliaresMenu() {
  isAuxiliaresMenuOpen.value = !isAuxiliaresMenuOpen.value
}

function togglePersonasMenu() {
  isPersonasMenuOpen.value = !isPersonasMenuOpen.value
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.theme-bg {
  background-color: var(--theme-bg-color);
}

.sidebar-bg {
  background-color: var(--sidebar-bg-color);
}

.sidebar-border {
  border-color: var(--sidebar-border-color);
}

.theme-text {
  color: var(--theme-text-color);
}
</style>