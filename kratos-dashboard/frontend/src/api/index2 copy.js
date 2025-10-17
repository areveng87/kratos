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
  //   login: (credentials) => axios.post("/api/auth/login", credentials),
  //   me: () => axios.get("/api/auth/me"),
  // },

    auth: {
    login: (credentials) => axios.post("/auth/login", credentials),
    me: () => axios.get("/auth/me"),
  },

  // Dashboard endpoints
  dashboard: {
    //getStats: () => axios.get("/api/dashboard/stats"),
    getStats: () => axios.get("/dashboard/stats"),
    //getChartData: () => axios.get("/api/dashboard/chart-data"),
    getChartData: () => axios.get("/dashboard/chart-data"),
  },

  // Operaciones endpoints
  operaciones: {
    getAll: () => axios.get("/api/operaciones"),
    create: (data) => axios.post("/api/operaciones", data),
    update: (id, data) => axios.put(`/api/operaciones/${id}`, data),
    delete: (id) => axios.delete(`/api/operaciones/${id}`),
    getPlanner: (params) => axios.get("/api/operaciones/planner", { params }),
  },

  // Empresas endpoints
  empresas: {
    getAll: () => axios.get("/api/empresas"),
    create: (data) => axios.post("/api/empresas", data),
    update: (id, data) => axios.put(`/api/empresas/${id}`, data),
    delete: (id) => axios.delete(`/api/empresas/${id}`),
  },

  // Usuarios endpoints
  usuarios: {
    getAll: () => axios.get("/api/usuarios"),
    getById: (id) => axios.get(`/api/usuarios/${id}`),
    create: (data) => axios.post("/api/usuarios", data),
    update: (id, data) => axios.put(`/api/usuarios/${id}`, data),
    delete: (id) => axios.delete(`/api/usuarios/${id}`),
  },

  // Sociedades endpoints
  sociedades: {
    getAll: () => axios.get("/api/sociedades"),
    getById: (id) => axios.get(`/api/sociedades/${id}`),
    create: (data) => axios.post("/api/sociedades", data),
    update: (id, data) => axios.put(`/api/sociedades/${id}`, data),
    delete: (id) => axios.delete(`/api/sociedades/${id}`),
  },

  // Representantes endpoints
  representantes: {
    getAll: () => axios.get("/api/representantes"),
    create: (data) => axios.post("/api/representantes", data),
    update: (idrepresen, data) => axios.put(`/api/representantes/${idrepresen}`, data),
    delete: (idrepresen) => axios.delete(`/api/representantes/${idrepresen}`),
  },

    // Roles endpoints
  roles: {
    getAll: () => axios.get("/api/roles"),
  },

    // Auditores endpoints
  auditores: {
    getSociedadesDisponibles: () => axios.get("/api/auditores/sociedades-disponibles"),
    getAuditorSociedades: (auditorId) => axios.get(`/api/auditores/${auditorId}/sociedades`),
    updateAuditorSociedades: (auditorId, data) => axios.put(`/api/auditores/${auditorId}/sociedades`, data),
    getOperacionesDisponibles: () => axios.get("/api/auditores/operaciones-disponibles"),
    getAuditorOperaciones: (auditorId) => axios.get(`/api/auditores/${auditorId}/operaciones`),
    updateAuditorOperaciones: (auditorId, data) => axios.put(`/api/auditores/${auditorId}/operaciones`, data),
  },
  // Folder structure management endpoints
  modulos: {
    getAll: () => axios.get("/api/modulos"),
    asignarEstructura: (data) => axios.post("/api/modulos/asignar", data),
    desasignarEstructura: (idmodulo) => axios.delete(`/api/modulos/${idmodulo}/desasignar`),
  },

  estructuras: {
    getRaiz: () => axios.get("/api/estructuras"),
    getActivas: () => axios.get("/api/estructuras/activas"),
    // uploadFile: (idestructura, { file, idcarpetapadre }, config = {}) => {
    //   const fd = new FormData();
    //   fd.append("file", file);
    //   if (idcarpetapadre !== undefined && idcarpetapadre !== null) {
    //     fd.append("idcarpetapadre", idcarpetapadre);
    //   }
    //   return axios.post(`/api/estructuras/${idestructura}/upload`, fd, {
    //     // no pongas Content-Type aquí; Axios lo setea solo
    //     ...config, // por si quieres onUploadProgress, etc.
    //   });
    // },
    uploadFile: (idestructura, formData) =>
      axios.post(`/api/estructuras/${idestructura}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }),
    // uploadFile: (idestructura, formData, config = {}) =>
    //   axios.post(`/api/estructuras/${idestructura}/upload`, formData, { ...config }),
    //   //axios.post(`/api/caca/${idestructura}/upload`, formData),
    getTree: (idestructura) => axios.get(`/api/estructuras/${idestructura}/tree`),
    create: (data) => axios.post("/api/estructuras", data),
    update: (idestructura, data) => axios.put(`/api/estructuras/${idestructura}`, data),
    delete: (idestructura) => axios.delete(`/api/estructuras/${idestructura}`),
    createCarpeta: (idestructura, data) => axios.post(`/api/estructuras/${idestructura}/carpetas`, data),
    // uploadFile: (idestructura, data, config = {}) =>
    //   // axios.post(`/api/estructuras/${idestructura}/upload`, data, {
    //   //   headers: {
    //   //     "Content-Type": "multipart/form-data",
    //   //   },
    //   // }
    //   axios.post(`/api/estructuras/${idestructura}/upload`, data, {
    //     ...(config || {}),
    //   }
    // ),
    
    deleteFile: (idcarpeta) => axios.delete(`/api/estructuras/archivos/${idcarpeta}`),
  },
    tiposRelacion: {
    getAll: () => axios.get("/api/tipos-relacion"),
    create: (data) => axios.post("/api/tipos-relacion", data),
    update: (idtiporelacion, data) => axios.put(`/api/tipos-relacion/${idtiporelacion}`, data),
    delete: (idtiporelacion) => axios.delete(`/api/tipos-relacion/${idtiporelacion}`),
  },
  countries: {
    getAll: () => axios.get("/api/countries"),
    getSubdivisions: (countryiso) => axios.get(`/api/subdivisions/${countryiso}`),
  },
  tiposAlerta: {
    getAll: () => axios.get("/api/tipos-alerta"),
    create: (data) => axios.post("/api/tipos-alerta", data),
    update: (idtipoalerta, data) => axios.put(`/api/tipos-alerta/${idtipoalerta}`, data),
    delete: (idtipoalerta) => axios.delete(`/api/tipos-alerta/${idtipoalerta}`),
  },

  procesos: {
    getAll: () => axios.get("/api/procesos"),
    getById: (idproceso) => axios.get(`/api/procesos/${idproceso}`),
    create: (data) => axios.post("/api/procesos", data),
    update: (idproceso, data) => axios.put(`/api/procesos/${idproceso}`, data),
    delete: (idproceso) => axios.delete(`/api/procesos/${idproceso}`),
    getEstados: (idproceso) => axios.get(`/api/procesos/${idproceso}/estados`),
    createCompleto: (data) => axios.post("/api/procesos/completo", data),
    updateCompleto: (idproceso, data) => axios.put(`/api/procesos/${idproceso}/completo`, data),
  },

  acciones: {
    getDisponibles: () => axios.get("/api/acciones"),
  },
}

export default api
