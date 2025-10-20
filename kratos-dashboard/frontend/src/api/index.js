import axios from "axios"

// Configuración base de axios
//axios.defaults.baseURL = "http://localhost:8000"
axios.defaults.baseURL = "/api"
axios.defaults.headers.common["Content-Type"] = "application/json"

// Interceptor para manejar errores globalmente
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem("token")
      window.location.href = "/login"
    }
    return Promise.reject(error)
  },
)

export const api = {
//const api = {
  // Auth endpoints
  // auth: {
  //   login: (credentials) => axios.post("/auth/login", credentials),
  //   me: () => axios.get("/auth/me"),
  // },

    auth: {
    login: (credentials) => axios.post("/auth/login", credentials),
    me: () => axios.get("/auth/me"),
  },

  // Dashboard endpoints
  dashboard: {
    //getStats: () => axios.get("/dashboard/stats"),
    getStats: () => axios.get("/dashboard/stats"),
    //getChartData: () => axios.get("/dashboard/chart-data"),
    getChartData: () => axios.get("/dashboard/chart-data"),
  },

  // Operaciones endpoints
  operaciones: {
    getAll: () => axios.get("/operaciones"),
    create: (data) => axios.post("/operaciones", data),
    update: (id, data) => axios.put(`/operaciones/${id}`, data),
    delete: (id) => axios.delete(`/operaciones/${id}`),
    getPlanner: (params) => axios.get("/operaciones/planner", { params }),
  },

  // Empresas endpoints
  empresas: {
    getAll: () => axios.get("/empresas"),
    create: (data) => axios.post("/empresas", data),
    update: (id, data) => axios.put(`/empresas/${id}`, data),
    delete: (id) => axios.delete(`/empresas/${id}`),
  },

  // Usuarios endpoints
  usuarios: {
    getAll: () => axios.get("/usuarios"),
    getById: (id) => axios.get(`/usuarios/${id}`),
    create: (data) => axios.post("/usuarios", data),
    update: (id, data) => axios.put(`/usuarios/${id}`, data),
    delete: (id) => axios.delete(`/usuarios/${id}`),
  },

  // Sociedades endpoints
  sociedades: {
    getAll: () => axios.get("/sociedades"),
    getById: (id) => axios.get(`/sociedades/${id}`),
    create: (data) => axios.post("/sociedades", data),
    update: (id, data) => axios.put(`/sociedades/${id}`, data),
    delete: (id) => axios.delete(`/sociedades/${id}`),
  },

  // Representantes endpoints
  representantes: {
    getAll: () => axios.get("/representantes"),
    create: (data) => axios.post("/representantes", data),
    update: (idrepresen, data) => axios.put(`/representantes/${idrepresen}`, data),
    delete: (idrepresen) => axios.delete(`/representantes/${idrepresen}`),
  },

    // Roles endpoints
  roles: {
    getAll: () => axios.get("/roles"),
  },

    // Auditores endpoints
  auditores: {
    getSociedadesDisponibles: () => axios.get("/auditores/sociedades-disponibles"),
    getAuditorSociedades: (auditorId) => axios.get(`/auditores/${auditorId}/sociedades`),
    updateAuditorSociedades: (auditorId, data) => axios.put(`/auditores/${auditorId}/sociedades`, data),
    getOperacionesDisponibles: () => axios.get("/auditores/operaciones-disponibles"),
    getAuditorOperaciones: (auditorId) => axios.get(`/auditores/${auditorId}/operaciones`),
    updateAuditorOperaciones: (auditorId, data) => axios.put(`/auditores/${auditorId}/operaciones`, data),
  },
  // Folder structure management endpoints
  modulos: {
    getAll: () => axios.get("/modulos"),
    asignarEstructura: (data) => axios.post("/modulos/asignar", data),
    desasignarEstructura: (idmodulo) => axios.delete(`/modulos/${idmodulo}/desasignar`),
  },

  estructuras: {
    getRaiz: () => axios.get("/estructuras"),
    getActivas: () => axios.get("/estructuras/activas"),
    // uploadFile: (idestructura, { file, idcarpetapadre }, config = {}) => {
    //   const fd = new FormData();
    //   fd.append("file", file);
    //   if (idcarpetapadre !== undefined && idcarpetapadre !== null) {
    //     fd.append("idcarpetapadre", idcarpetapadre);
    //   }
    //   return axios.post(`/estructuras/${idestructura}/upload`, fd, {
    //     // no pongas Content-Type aquí; Axios lo setea solo
    //     ...config, // por si quieres onUploadProgress, etc.
    //   });
    // },
    uploadFile: (idestructura, formData) =>
      axios.post(`/estructuras/${idestructura}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }),
    // uploadFile: (idestructura, formData, config = {}) =>
    //   axios.post(`/estructuras/${idestructura}/upload`, formData, { ...config }),
    //   //axios.post(`/caca/${idestructura}/upload`, formData),
    getTree: (idestructura) => axios.get(`/estructuras/${idestructura}/tree`),
    create: (data) => axios.post("/estructuras", data),
    update: (idestructura, data) => axios.put(`/estructuras/${idestructura}`, data),
    delete: (idestructura) => axios.delete(`/estructuras/${idestructura}`),
    createCarpeta: (idestructura, data) => axios.post(`/estructuras/${idestructura}/carpetas`, data),
    // uploadFile: (idestructura, data, config = {}) =>
    //   // axios.post(`/estructuras/${idestructura}/upload`, data, {
    //   //   headers: {
    //   //     "Content-Type": "multipart/form-data",
    //   //   },
    //   // }
    //   axios.post(`/estructuras/${idestructura}/upload`, data, {
    //     ...(config || {}),
    //   }
    // ),
    
    deleteFile: (idcarpeta) => axios.delete(`/estructuras/archivos/${idcarpeta}`),
  },
    tiposRelacion: {
    getAll: () => axios.get("/tipos-relacion"),
    create: (data) => axios.post("/tipos-relacion", data),
    update: (idtiporelacion, data) => axios.put(`/tipos-relacion/${idtiporelacion}`, data),
    delete: (idtiporelacion) => axios.delete(`/tipos-relacion/${idtiporelacion}`),
  },
  countries: {
    getAll: () => axios.get("/countries"),
    getSubdivisions: (countryiso) => axios.get(`/subdivisions/${countryiso}`),
  },
  tiposAlerta: {
    getAll: () => axios.get("/tipos-alerta"),
    create: (data) => axios.post("/tipos-alerta", data),
    update: (idtipoalerta, data) => axios.put(`/tipos-alerta/${idtipoalerta}`, data),
    delete: (idtipoalerta) => axios.delete(`/tipos-alerta/${idtipoalerta}`),
  },

  procesos: {
    getAll: () => axios.get("/procesos"),
    getById: (idproceso) => axios.get(`/procesos/${idproceso}`),
    create: (data) => axios.post("/procesos", data),
    update: (idproceso, data) => axios.put(`/procesos/${idproceso}`, data),
    delete: (idproceso) => axios.delete(`/procesos/${idproceso}`),
    getEstados: (idproceso) => axios.get(`/procesos/${idproceso}/estados`),
    createCompleto: (data) => axios.post("/procesos-completo", data),
    updateCompleto: (idproceso, data) => axios.put(`/procesos-completo/${idproceso}`, data),
  },

  acciones: {
    getDisponibles: () => axios.get("/acciones"),
  },
  
  estadoRoles: {
    getByEstado: (idproceso, idestado) => axios.get(`/procesos/${idproceso}/estados/${idestado}/roles`),
    create: (idproceso, idestado, data) => axios.post(`/procesos/${idproceso}/estados/${idestado}/roles`, data),
    update: (idproceso, idestado, idrol, data) =>
      axios.put(`/procesos/${idproceso}/estados/${idestado}/roles/${idrol}`, data),
    delete: (idproceso, idestado, idrol) =>
      axios.delete(`/procesos/${idproceso}/estados/${idestado}/roles/${idrol}`),
    saveAll: (idproceso, idestado, data) =>
      axios.post(`/procesos/${idproceso}/estados/${idestado}/roles/batch`, data),
  },

  
  // Catálogos de tareas endpoints
  catalogos: {
    getTiposActivos: () => axios.get("/catalogos/tipos-activos"),
    getTiposOperaciones: () => axios.get("/catalogos/tipos-operaciones"),
    getClientes: () => axios.get("/catalogos/clientes"),
    getPaises: () => axios.get("/catalogos/paises"),
    getProvincias: (countryCode) => axios.get(`/catalogos/provincias/${countryCode}`),
    getAnalistasPBC: () => axios.get("/catalogos/analistas-pbc"),
    getOperadores: () => axios.get("/catalogos/operadores"),
  },

  // Tareas endpoints
  tareas: {
    getById: (idtarea) => axios.get(`/tareas/${idtarea}`),
    create: (data) => axios.post("/tareas", data),
    update: (idtarea, data) => axios.put(`/tareas/${idtarea}`, data),
  },
}

export default api
