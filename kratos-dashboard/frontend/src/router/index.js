import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "../stores/auth"
import Login from "../views/Login.vue"
import Dashboard from "../views/Dashboard.vue"
import Operaciones from "../views/Operaciones2.vue"
import Empresas from "../views/Empresas.vue"
import Usuarios from "../views/Usuarios.vue"
import UserDetail from "../views/UserDetail.vue"
import UsuarioForm from "../views/UsuarioForm.vue"
import Sociedades from "../views/Sociedades.vue"
import Configuracion from "../views/Configuracion.vue"
import DetallesOperacion from "../views/DetallesOperacion.vue"
import ArbolCarpetas from "../views/admin/ArbolCarpetas.vue"
import AdminUsuarios from "../views/admin/AdminUsuarios.vue"
import AdminUsuarioForm from "../views/admin/AdminUsuarioForm.vue"
import Roles from "../views/admin/Roles.vue"
import MatricesRiesgo from "../views/admin/MatricesRiesgo.vue"
import Relaciones from "../views/admin/auxiliares/Relaciones.vue"
import Fondos from "../views/admin/auxiliares/Fondos.vue"
import Servicers from "../views/admin/auxiliares/Servicers.vue"
import TiposAlerta from "../views/admin/auxiliares/TiposAlerta.vue"
import DefinicionProcesos from "../views/admin/DefinicionProcesos.vue"
import EstructuraEditor from "../views/admin/EstructuraEditor.vue"
import ProcesoForm from "../views/admin/ProcesoForm.vue"
import TareaForm from "../views/TareaForm.vue"
import PersonasNaturales from "../views/PersonasNaturales.vue"

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { requiresGuest: true },
  },
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/operaciones",
    name: "Operaciones",
    component: Operaciones,
    meta: { requiresAuth: true },
  },
  {
    path: "/operaciones/:id",
    name: "DetallesOperacion",
    component: DetallesOperacion,
    meta: { requiresAuth: true },
  },
  {
    path: "/operaciones/nueva",
    name: "NuevaOperacion",
    component: TareaForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/operaciones/:id/editar",
    name: "EditarOperacion",
    component: TareaForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/empresas",
    name: "Empresas",
    component: Empresas,
    meta: { requiresAuth: true },
  },
  {
    path: "/sociedades",
    name: "Sociedades",
    component: Sociedades,
    meta: { requiresAuth: true },
  },
  {
    path: "/personas-naturales",
    name: "PersonasNaturales",
    component: PersonasNaturales,
    meta: { requiresAuth: true },
  },
  {
    path: "/usuarios",
    name: "Usuarios",
    component: Usuarios,
    meta: { requiresAuth: true },
  },
  {
    path: "/usuarios/nuevo",
    name: "NuevoUsuario",
    component: UsuarioForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/usuarios/:id/editar",
    name: "EditarUsuario",
    component: UsuarioForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/usuarios/:id",
    name: "UserDetail",
    component: UserDetail,
    meta: { requiresAuth: true },
  },
  {
    path: "/configuracion",
    name: "Configuracion",
    component: Configuracion,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/arbol-carpetas",
    name: "ArbolCarpetas",
    component: ArbolCarpetas,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/arbol-carpetas/nueva",
    name: "NuevaEstructura",
    component: EstructuraEditor,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/arbol-carpetas/:id",
    name: "EditarEstructura",
    component: EstructuraEditor,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/usuarios",
    name: "AdminUsuarios",
    component: AdminUsuarios,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
 {
    path: "/admin/usuarios/nuevo",
    name: "NuevoUsuario",
    component: AdminUsuarioForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/usuarios/:id/editar",
    name: "EditarUsuario",
    component: AdminUsuarioForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/roles",
    name: "Roles",
    component: Roles,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/matrices-riesgo",
    name: "MatricesRiesgo",
    component: MatricesRiesgo,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/auxiliares/relaciones",
    name: "Relaciones",
    component: Relaciones,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/auxiliares/fondos",
    name: "Fondos",
    component: Fondos,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/auxiliares/servicers",
    name: "Servicers",
    component: Servicers,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/auxiliares/tipos-alerta",
    name: "TiposAlerta",
    component: TiposAlerta,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/definicion-procesos",
    name: "DefinicionProcesos",
    component: DefinicionProcesos,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/definicion-procesos/nuevo",
    name: "NuevoProceso",
    component: ProcesoForm,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/admin/definicion-procesos/:id",
    name: "EditarProceso",
    component: ProcesoForm,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Guard de navegación
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // if (!authStore.isInitialized) {
  //   await authStore.initializeAuth()
  // }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login")
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next("/")
  } else if (to.meta.requiresAdmin) {
    const userRole = authStore.user?.rol
    if (userRole === "Supervisor" || userRole === "Administrador") {
      next()
    } else {
      next("/")
    }
  } else {
    next()
  }
})

export default router
