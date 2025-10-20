from pydantic import BaseModel, EmailStr
from typing import Dict, Optional, List
from datetime import datetime, date
from enum import Enum

# models.py (o donde tengas tus esquemas)
from typing import Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    code: int
    detail: str = ""
    data: Optional[object] = None


class RolEnum(str, Enum):
    ADMINISTRADOR = "Administrador"
    ANALISTA_PBC = "Analista PBC"
    OCI_INTERNO = "OCI Interno"
    OCI_EXTERNO = "OCI Externo"
    SPV = "SPV"
    SERVICER_SUPERVISOR = "Servicer Supervisor"
    SERVICER_OPERADOR = "Servicer Operador"
    AUDITOR = "Auditor"

class EstadoOperacion(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"

class TipoOperacion(str, Enum):
    COMPRA = "COMPRA"
    VENTA = "VENTA"
    TRANSFERENCIA = "TRANSFERENCIA"

# Modelos de request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    apellido: Optional[str] = None
    nif: Optional[str] = None
    telefono: Optional[str] = None
    telefono2: Optional[str] = None
    rol_id: int
    servicer: Optional[int] = None
    sociedad: Optional[int] = None
    propio: bool = True
    activo: bool = True
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class UpdateUserRequest(BaseModel):
    email: EmailStr
    nombre: str
    password: Optional[str] = None
    apellido: Optional[str] = None
    nif: Optional[str] = None
    telefono: Optional[str] = None
    telefono2: Optional[str] = None
    rol_id: int
    servicer: Optional[int] = None
    sociedad: Optional[int] = None
    propio: bool = True
    activo: bool = True
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class CreateEmpresaRequest(BaseModel):
    nombre: str
    rut: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

class CreateOperacionRequest(BaseModel):
    empresa_id: int
    tipo_operacion: TipoOperacion
    monto: float
    descripcion: Optional[str] = None

class CreateSociedadRequest(BaseModel):
    codcli: Optional[str] = None
    cuenta: Optional[str] = None
    nifcli: Optional[str] = None
    razon: Optional[str] = None
    nomcli: str  # Compañía - required field
    dtocli: Optional[str] = None
    dircli: Optional[str] = None
    codprovi: Optional[str] = None
    pobcli: Optional[str] = None
    telcli: Optional[str] = None
    e_mail: Optional[str] = None
    codpais: Optional[str] = None
    contacto: Optional[str] = None
    idrepresen: Optional[int] = None  # Fondo (representante)
    ext_cartera: Optional[str] = None  # Cartera
    ext_analistapordefecto: Optional[int] = None  # Analista
    ext_actividad: Optional[str] = None
    ext_estado: Optional[str] = None
    ext_spv: bool = False
    observaciones: Optional[str] = None

class UpdateSociedadRequest(BaseModel):
    codcli: Optional[str] = None
    cuenta: Optional[str] = None
    nifcli: Optional[str] = None
    razon: Optional[str] = None
    nomcli: str  # Compañía - required field
    dtocli: Optional[str] = None
    dircli: Optional[str] = None
    codprovi: Optional[str] = None
    pobcli: Optional[str] = None
    telcli: Optional[str] = None
    e_mail: Optional[str] = None
    codpais: Optional[str] = None
    contacto: Optional[str] = None
    idrepresen: Optional[int] = None  # Fondo (representante)
    ext_cartera: Optional[str] = None  # Cartera
    ext_analistapordefecto: Optional[int] = None  # Analista
    ext_actividad: Optional[str] = None
    ext_estado: Optional[str] = None
    ext_spv: bool = False
    observaciones: Optional[str] = None

# Modelos de response
class UserResponse(BaseModel):
    id: int
    email: str
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    nif: Optional[str] = None
    telefono: Optional[str] = None
    telefono2: Optional[str] = None
    rol: Optional[str] = None
    rol_id: Optional[int] = None
    propio: Optional[bool] = False
    servicer: Optional[int] = None
    servicer_nombre: Optional[str] = None
    sociedad: Optional[int] = None
    sociedad_nombre: Optional[str] = None
    expediente_propio: Optional[bool] = None
    activo: Optional[bool]=None
    ultimo_login: Optional[datetime] = None
    fecha_creacion: Optional[datetime] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class EmpresaResponse(BaseModel):
    id: int
    nombre: str
    codigo: int
    rut: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    activo: Optional[int] = 1
    fecha_creacion: Optional[datetime] = None

class OperacionResponse(BaseModel):
    id: int
    empresa_id: int
    empresa_nombre: str
    usuario_id: int
    usuario_nombre: str
    tipo_operacion: str
    monto: float
    estado: str
    descripcion: Optional[str] = None
    fecha_operacion: datetime

class DashboardStats(BaseModel):
    total_usuarios: int
    total_empresas: int
    total_operaciones: int
    operaciones_pendientes: int
    ingresos_mes: float
    gastos_mes: float
    operaciones_recientes: List[dict]
    empresas_activas: List[dict]

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[dict]

class RolResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool

class SociedadResponse(BaseModel):
    idcliente: int
    codcli: Optional[str] = None
    cuenta: Optional[str] = None
    nifcli: Optional[str] = None
    razon: Optional[str] = None
    nomcli: str  # Compañía
    dtocli: Optional[str] = None
    dircli: Optional[str] = None
    codprovi: Optional[str] = None
    pobcli: Optional[str] = None
    telcli: Optional[str] = None
    e_mail: Optional[str] = None
    codpais: Optional[str] = None
    contacto: Optional[str] = None
    idrepresen: Optional[int] = None
    representante_nombre: Optional[str] = None  # Fondo - nombre del representante
    ext_cartera: Optional[str] = None  # Cartera
    ext_analistapordefecto: Optional[int] = None
    analista_nombre: Optional[str] = None  # Analista - nombre del usuario
    ext_actividad: Optional[str] = None
    ext_estado: Optional[str] = None
    ext_spv: bool = False
    observaciones: Optional[str] = None

class RepresentanteResponse(BaseModel):
    idrepresen: int
    descripcion: str

class PlannerOperacionResponse(BaseModel):
    id: Optional[int] = None
    fecha_prevista_firma: Optional[datetime] = None  # FECHA_PREVISTA
    servicer: Optional[str] = None  # From EMPRESAS.NOMEMPRESA via CODEMPRESA
    fecha_util_cambio: Optional[datetime] = None  # From TAREAS_LOG.FECHA (latest)
    tipo_operacion: Optional[str] = None  # PROCESO (from joined table)
    referencia_expediente: Optional[str] = None  # REFERENCIA
    sociedad: Optional[str] = None  # CLIENTE (from joined ERP_CLIENTES)
    estado: Optional[str] = None  # ESTADO
    analista_pbc: Optional[int] = None  # EXT_ANALISTAPBC - this is an integer ID
    analista_pbc_nombre: Optional[str] = None  # From USUARIOS.NOMBRE via EXT_ANALISTAPBC
    urgente: bool = False  # EXT_URGENTE
    proceso: Optional[str] = None  # PROCESO (from PLANNER_PROCESOS.TITULO)
    cliente: Optional[str] = None  # CLIENTE (from ERP_CLIENTES.NOMCLI)
    idproceso: Optional[int] = None  # IDPROCESO
    idcliente: Optional[int] = None  # IDCLIENTE
    titulo: Optional[str] = None  # TITULO
    descripcion: Optional[str] = None  # DESCRIPCION

class PlannerOperacionesFilters(BaseModel):
    estado: Optional[str] = None
    referencia_expediente: Optional[str] = None
    analista: Optional[str] = None
    sin_analista: bool = False
    search: Optional[str] = None

class AuditorSociedadResponse(BaseModel):
    idcliente: int
    nomcli: str  # Sociedad
    ext_cartera: Optional[str] = None  # Cartera
    representante_nombre: Optional[str] = None  # Fondo

class UpdateAuditorSociedadesRequest(BaseModel):
    sociedades_ids: List[int]  # List of IDCLIENTE values to assign to the auditor

class AuditorOperacionResponse(BaseModel):
    idtarea: int
    idcliente: Optional[int] = None
    nomcli: Optional[str] = None
    fechaultimocambio: Optional[datetime] = None
    fechaprevista: Optional[datetime] = None
    referencia: Optional[str] = None
    estado: Optional[str] = None
    idanalista: Optional[int] = None
    nomanalista: Optional[str] = None
    nomempresa: Optional[str] = None

class UpdateAuditorOperacionesRequest(BaseModel):
    operaciones_ids: List[int]  # List of IDCLIENTE values to assign to the auditor


# Models for folder structure management
class ModuloResponse(BaseModel):
    idmodulo: int
    descripcion: str
    estructura_raiz_id: Optional[int] = None
    estructura_raiz_nombre: Optional[str] = None

class EstructuraCarpetaResponse(BaseModel):
    idcarpeta: int
    idcarpetapadre: Optional[int] = None
    nombre: str
    archivo: bool
    activa: bool
    modulo_id: Optional[int] = None
    modulo_nombre: Optional[str] = None
    archivo_url: Optional[str] = None
    archivo_size: Optional[int] = None

class CreateEstructuraRequest(BaseModel):
    nombre: str
    activa: bool = True

class UpdateEstructuraRequest(BaseModel):
    nombre: str
    activa: bool

class CreateCarpetaRequest(BaseModel):
    idestructura: int
    idcarpetapadre: Optional[int] = None
    nombre: str
    archivo: Optional[bool] = False
    activa: Optional[bool] = True
    file: Optional[str] = None  # Para subir un archivo

class AsignarModuloEstructuraRequest(BaseModel):
    idmodulo: int
    idestructuracarpeta: int

# Models for representantes CRUD operations
class CreateRepresentanteRequest(BaseModel):
    descripcion: str

class UpdateRepresentanteRequest(BaseModel):
    descripcion: str

# Models for TipoRelacion CRUD operations
class TipoRelacionResponse(BaseModel):
    idtiporelacion: int
    descripcion: str
    estructurajuridica: bool

class CreateTipoRelacionRequest(BaseModel):
    descripcion: str
    estructurajuridica: bool = False

class UpdateTipoRelacionRequest(BaseModel):
    descripcion: str
    estructurajuridica: bool

# Models for TipoAlerta CRUD operations
class TipoAlertaResponse(BaseModel):
    idtipoalerta: int
    descripcion: str

class CreateTipoAlertaRequest(BaseModel):
    descripcion: str

class UpdateTipoAlertaRequest(BaseModel):
    descripcion: str



# Models for Proceso CRUD operations
class ProcesoResponse(BaseModel):
    idproceso: int
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int

class CreateProcesoRequest(BaseModel):
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int = 0

class UpdateProcesoRequest(BaseModel):
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int


# Models for Acciones and ProcesoEstados
class AccionResponse(BaseModel):
    idaccion: int
    descripcion: str
    activa: bool
    proceso: bool

class ProcesoEstadoResponse(BaseModel):
    idestado: int
    idproceso: int
    visibilidad: bool
    titulo: str
    orden: int
    finaliza: bool
    idestadopadre: Optional[int] = None

class CreateProcesoEstadoRequest(BaseModel):
    #idproceso: int
    idestado: int
    #idaccion: int
    titulo:str
    visibilidad: bool
    orden: int
    finaliza: bool = False

class UpdateProcesoEstadoRequest(BaseModel):
    visibilidad: bool
    orden: int
    finaliza: bool

class CreateProcesoWithEstadosRequest(BaseModel):
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int = 0
    estados: List[CreateProcesoEstadoRequest] = []

class UpdateProcesoWithEstadosRequest(BaseModel):
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int
    estados: List[dict] = []  # Can include idestado for updates or idaccion for new ones

    
# Models for Proceso Estado Roles
class EstadoRolResponse(BaseModel):
    id: int
    idproceso: int
    idestado: int
    idrol: int
    rol_nombre: Optional[str] = None
    lectura: bool
    escritura: bool
    cambioestado: bool

class CreateEstadoRolRequest(BaseModel):
    idproceso: int
    idestado: int
    idrol: int
    lectura: bool = False
    escritura: bool = False
    cambioestado: bool = False

class UpdateEstadoRolRequest(BaseModel):
    lectura: bool
    escritura: bool
    cambioestado: bool


# Models for Proceso Estado Roles
class EstadoRolResponse(BaseModel):
    id: int
    idproceso: int
    idestado: int
    idrol: int
    rol_nombre: Optional[str] = None
    lectura: bool
    escritura: bool
    cambioestado: bool

class CreateEstadoRolRequest(BaseModel):
    idproceso: int
    idestado: int
    idrol: int
    lectura: bool = False
    escritura: bool = False
    cambioestado: bool = False

class UpdateEstadoRolRequest(BaseModel):
    idrol: int
    lectura: bool
    escritura: bool
    cambioestado: bool

class SaveEstadoRolesBatchRequest(BaseModel):
    idproceso: int
    idestado: int
    roles: List[dict]  # List of role objects with idrol, lectura, escritura, cambioestado


# Models for TipoAlerta CRUD operations
class TipoAlertaResponse(BaseModel):
    idtipoalerta: int
    descripcion: str

class CreateTipoAlertaRequest(BaseModel):
    descripcion: str

class UpdateTipoAlertaRequest(BaseModel):
    descripcion: str

# Models for Proceso CRUD operations
class ProcesoResponse(BaseModel):
    idproceso: int
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int

class CreateProcesoRequest(BaseModel):
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int = 0

class UpdateProcesoRequest(BaseModel):
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int

# Models for Acciones and ProcesoEstados
class AccionResponse(BaseModel):
    idaccion: int
    descripcion: str
    activa: bool
    proceso: bool

class ProcesoEstadoResponse(BaseModel):
    idestado: int  # This is the reference to ACCIONES.IDACCION
    idproceso: int
    visibilidad: bool
    titulo: str
    orden: int
    finaliza: bool
    idestadopadre: Optional[int] = None

class CreateProcesoEstadoRequest(BaseModel):
    idproceso: int
    idestado: int  # This is the IDACCION from ACCIONES table
    visibilidad: bool
    orden: int
    finaliza: bool = False

class UpdateProcesoEstadoRequest(BaseModel):
    visibilidad: bool
    orden: int
    finaliza: bool

class CreateProcesoWithEstadosRequest(BaseModel):
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int = 0
    estados: List[CreateProcesoEstadoRequest] = []

class UpdateProcesoWithEstadosRequest(BaseModel):
    descripcion: str
    prefijo: Optional[str] = None
    visibilidad: int
    estados: List[dict] = []  # Can include idestado for updates or idaccion for new ones

# Models for Proceso Estado Roles
class EstadoRolResponse(BaseModel):
    id: int
    idproceso: int
    idestado: int
    idrol: int
    rol_nombre: Optional[str] = None
    lectura: bool
    escritura: bool
    cambioestado: bool

class CreateEstadoRolRequest(BaseModel):
    idproceso: int
    idestado: int
    idrol: int
    lectura: bool = False
    escritura: bool = False
    cambioestado: bool = False

class UpdateEstadoRolRequest(BaseModel):
    lectura: bool
    escritura: bool
    cambioestado: bool

class SaveEstadoRolesBatchRequest(BaseModel):
    idproceso: int
    idestado: int
    roles: List[Dict]  # List of role objects with idrol, lectura, escritura, cambioestado

# APIResponse model for consistent API responses
class APIResponse(BaseModel):
    code: int
    detail: str = ""
    data: Optional[object] = None

# Models for Tarea (operation) management
class TareaInmuebleRequest(BaseModel):
    # idcliente: Optional[int] = None  # Sociedad
    # ext_tipoactivo: Optional[str] = None  # Tipo de activo
    # ext_activosotros: Optional[str] = None  # Otros (tipo activo)
    # localidad: Optional[str] = None
    # pais: Optional[str] = None
    # provincia: Optional[str] = None
    # ext_analistapbc: Optional[int] = None
    # codempresa: Optional[str] = None  # Servicer
    # referencia: Optional[str] = None
    # ext_asignador_analistapbc: Optional[int] = None  # Read-only, set by system
    # ext_operador: Optional[int] = None
    # ext_urgente: bool = False
    idcliente: Optional[int] = None
    tipo_operacion: Optional[int] = None          # ← añadir si lo necesitas
    ext_tipoactivo: Optional[int] = None         # ← int (id del tipo)
    ext_activosotros: Optional[str] = None
    localidad: Optional[str] = None
    pais: Optional[str] = None
    provincia: Optional[str] = None
    ext_analistapbc: Optional[int] = None
    codempresa: Optional[int] = None             # ← int (id/código servicer)
    referencia: Optional[str] = None
    ext_asignador_analistapbc: Optional[int] = None
    ext_operador: Optional[int] = None
    ext_urgente: bool = False

CreateTareaRequest = TareaInmuebleRequest
UpdateTareaRequest = TareaInmuebleRequest
class TareaResponse(BaseModel):
    idtarea: int
    idcliente: Optional[int] = None
    cliente_nombre: Optional[str] = None
    ext_tipoactivo: Optional[str] = None
    tipoactivo_nombre: Optional[str] = None
    ext_activosotros: Optional[str] = None
    localidad: Optional[str] = None
    pais: Optional[int] = None
    pais_nombre: Optional[str] = None
    provincia: Optional[int] = None
    provincia_nombre: Optional[str] = None
    ext_analistapbc: Optional[int] = None
    analistapbc_nombre: Optional[str] = None
    codempresa: Optional[str] = None
    servicer_nombre: Optional[str] = None
    referencia: Optional[str] = None
    ext_asignador_analistapbc: Optional[int] = None
    asignador_nombre: Optional[str] = None
    ext_operador: Optional[int] = None
    operador_nombre: Optional[str] = None
    ext_urgente: bool = False
    fecha_alta: Optional[datetime] = None

class TipoActivoResponse(BaseModel):
    id: int
    descripcion: str

class ClienteResponse(BaseModel):
    idcliente: int
    nomcli: str

class PaisResponse(BaseModel):
    codigo: str
    nombre: str

class ProvinciaResponse(BaseModel):
    codigo: str
    nombre: str

class OperadorResponse(BaseModel):
    id: int
    nombre: str
