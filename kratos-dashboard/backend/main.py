from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import pyodbc
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import shutil
from pathlib import Path

from models import *
from services import CountryService, UserService, DashboardService, OperacionService, EmpresaService, SociedadService, RoleService, AuditorSociedadService, AuditorOperacionService, EstructuraCarpetaService, TipoRelacionService, TipoAlertaService, ProcesoService, AccionService, ProcesoEstadoService, ProcesoEstadoRolService, CatalogoService, TareaService, HitoService, ImportesHitosService, LogService, PersonasNaturalesService
from auth import auth_manager

import shutil
from pathlib import Path

from fastapi.responses import JSONResponse

from fastapi import Form, UploadFile, File

load_dotenv()

app = FastAPI(title="Kratos API", version="1.0.0")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://goshawk-mutual-phoenix.ngrok-free.app", "http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = Path("uploads/estructuras")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = auth_manager.verify_token(credentials.credentials)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")

# Auth endpoints
#@app.post("/api/auth/login", response_model=LoginResponse)
@app.post("/api/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    user = UserService.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Crear token
    token = auth_manager.create_access_token({
        "user_id": user["id"], 
        "email": user["email"], 
        "rol": user["rol"]
    })
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**user)
    )

#@app.get("/api/auth/me", response_model=UserResponse)
@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user(user_id: int = Depends(verify_token)):
    user = UserService.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return UserResponse(**user)

# Dashboard endpoints
#@app.get("/api/dashboard/stats", response_model=DashboardStats)
@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(user_id: int = Depends(verify_token)):
    stats = DashboardService.get_dashboard_stats()
    return DashboardStats(**stats)

@app.get("/api/dashboard/chart-data")
async def get_chart_data(user_id: int = Depends(verify_token)):
    return DashboardService.get_chart_data()

# Operaciones endpoints
@app.get("/api/operaciones", response_model=List[OperacionResponse])
async def get_operaciones(user_id: int = Depends(verify_token)):
    operaciones = OperacionService.get_all_operaciones()
    return [OperacionResponse(**op) for op in operaciones]

@app.post("/api/operaciones", response_model=OperacionResponse)
async def create_operacion(
    operacion_data: CreateOperacionRequest, 
    user_id: int = Depends(verify_token)
):
    from database import db_manager
    
    query = """
        INSERT INTO OPERACIONES (empresa_id, usuario_id, tipo_operacion, monto, descripcion)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?)
    """
    
    result = db_manager.execute_query(
        query, 
        (operacion_data.empresa_id, user_id, operacion_data.tipo_operacion, 
         operacion_data.monto, operacion_data.descripcion),
        fetch_one=True
    )
    
    # Get the created operation
    operaciones = OperacionService.get_all_operaciones()
    created_op = next((op for op in operaciones if op["id"] == result.id), None)
    
    if not created_op:
        raise HTTPException(status_code=500, detail="Error al crear operación")
    
    return OperacionResponse(**created_op)

# New endpoint for planner operations
@app.get("/api/operaciones/planner", response_model=List[PlannerOperacionResponse])
async def get_planner_operaciones(
    estado: Optional[str] = None,
    referencia_expediente: Optional[str] = None,
    analista: Optional[str] = None,
    sin_analista: bool = False,
    search: Optional[str] = None,
    user_id: int = Depends(verify_token)
):
    filters = {
        'estado': estado,
        'referencia_expediente': referencia_expediente,
        'analista': analista,
        'sin_analista': sin_analista,
        'search': search
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None and v != ''}
    
    print("Fetching planner operaciones with filters:", filters)

    operaciones = OperacionService.get_planner_operaciones(filters)

    #print("Planner operaciones fetched:", operaciones)

    return [PlannerOperacionResponse(**op) for op in operaciones]

# Empresas endpoints
@app.get("/api/empresas", response_model=List[EmpresaResponse])
async def get_empresas(user_id: int = Depends(verify_token)):
    empresas = EmpresaService.get_all_empresas()

    return [EmpresaResponse(**emp) for emp in empresas]

@app.get("/api/empresas-clientes")
async def get_empresas_clientes(user_id: int = Depends(verify_token)):
    """Obtiene las empresas clientes para el selector"""
    empresas = EmpresaService.get_empresas_clientes()
    return empresas

@app.post("/api/empresas", response_model=EmpresaResponse)
async def create_empresa(
    empresa_data: CreateEmpresaRequest, 
    user_id: int = Depends(verify_token)
):
    from database import db_manager
    
    query = """
        INSERT INTO EMPRESAS (nombre, rut, direccion, telefono, email)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?)
    """
    
    result = db_manager.execute_query(
        query, 
        (empresa_data.nombre, empresa_data.rut, empresa_data.direccion,
         empresa_data.telefono, empresa_data.email),
        fetch_one=True
    )
    
    # Get the created company
    empresas = EmpresaService.get_all_empresas()
    created_emp = next((emp for emp in empresas if emp["id"] == result.id), None)
    
    if not created_emp:
        raise HTTPException(status_code=500, detail="Error al crear empresa")
    
    return EmpresaResponse(**created_emp)

# Usuarios endpoints
@app.get("/api/usuarios", response_model=List[UserResponse])
async def get_usuarios(user_id: int = Depends(verify_token)):
    try:
        usuarios = UserService.get_all_users()
        return [UserResponse(**user) for user in usuarios]
    except Exception as e:
        print(f"Error fetching users for {user_id}: {e}")
        return []
    

@app.get("/api/usuarios/{usuario_id}", response_model=UserResponse)
async def get_usuario_by_id(
    usuario_id: int,
    user_id: int = Depends(verify_token)
):

    print("in usuarios id")

    usuario = UserService.get_user_by_id(usuario_id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return UserResponse(**usuario)

# @app.post("/api/usuarios", response_model=UserResponse)
# async def create_usuario(
#     usuario_data: CreateUserRequest, 
#     user_id: int = Depends(verify_token)
# ):
    
#     print("Creating user with data:", usuario_data)

#     from database import db_manager
    
#     # Hash password
#     password_hash = auth_manager.hash_password(usuario_data.password)
    
#     query = """
#         INSERT INTO USUARIOS (email, password_hash, nombre, apellido, nif, telefono, telefono2, rol_id, codempresa, idcliente, solopropios, activo, fecha_inicio, fecha_fin)
#         OUTPUT INSERTED.id
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """
#     params = (usuario_data.email, password_hash, usuario_data.nombre, usuario_data.apellido,
#          usuario_data.nif, usuario_data.telefono, usuario_data.telefono2, 
#          usuario_data.rol_id, usuario_data.servicer, usuario_data.sociedad, usuario_data.propio, usuario_data.activo,
#          usuario_data.fecha_inicio, usuario_data.fecha_fin)
#     try:
#         result = db_manager.execute_query(
#             query, 
#             params,
#             fetch_one=True
#         )
#         print("User created with ID:", result.id)

#     except pyodbc.IntegrityError as e:
#         # 2627 = violación de UNIQUE KEY; 2601 = violación de índice único
#         msg = str(e)
#         if "UQ_USUARIOS_EMAIL" in msg or "2627" in msg or "2601" in msg:
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail="Ya existe un usuario con este email."
#             )
#         # Otros errores de integridad
#         raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")
    
#     except Exception as e:
#         print("Error creating user:", e)
#         raise HTTPException(status_code=500, detail="Error al crear usuario")
    
#     # Get the created user
#     usuarios = UserService.get_all_users()
#     created_user = next((user for user in usuarios if user["id"] == result.id), None)
    
#     if not created_user:
#         raise HTTPException(status_code=500, detail="Error al crear usuario")
    
#     return UserResponse(**created_user)

@app.post("/api/usuarios", response_model=APIResponse)
async def create_usuario(
    usuario_data: CreateUserRequest, 
    user_id: int = Depends(verify_token)
):
    from database import db_manager

    try:
        # 1) Hash
        password_hash = auth_manager.hash_password(usuario_data.password)

        # 2) Insert
        query = """
            INSERT INTO USUARIOS (
                email, password_hash, nombre, apellido, nif, telefono, telefono2,
                rol_id, codempresa, idcliente, solopropios, activo, fecha_inicio, fecha_fin
            )
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            usuario_data.email, password_hash, usuario_data.nombre, usuario_data.apellido,
            usuario_data.nif, usuario_data.telefono, usuario_data.telefono2,
            usuario_data.rol_id, usuario_data.servicer, usuario_data.sociedad,
            usuario_data.propio, usuario_data.activo, usuario_data.fecha_inicio, usuario_data.fecha_fin
        )
        inserted = db_manager.execute_query(query, params, fetch_one=True)

        # 3) Cargar el usuario creado
        usuarios = UserService.get_all_users()
        created_user = next((u for u in usuarios if u["id"] == inserted.id), None)
        if not created_user:
            return APIResponse(code=500, detail="Error al crear usuario", data=None)

        return APIResponse(code=200, detail="", data=UserResponse(**created_user))

    except pyodbc.IntegrityError as e:
        # SQL Server duplicate key: 2627 (constraint) o 2601 (índice único)
        msg = str(e)
        if "2627" in msg or "2601" in msg or "UQ_USUARIOS_EMAIL" in msg:
            return APIResponse(code=409, detail="Ya existe un usuario con este email.", data=None)
        return APIResponse(code=500, detail="Error de integridad de datos.", data=None)

    except Exception as e:
        # aquí puedes loguear e
        return APIResponse(code=500, detail="Error interno al crear usuario.", data=None)

@app.put("/api/usuarios/{usuario_id}", response_model=APIResponse)
async def update_usuario(
    usuario_id: int,
    usuario_data: UpdateUserRequest,
    user_id: int = Depends(verify_token)
):
    from database import db_manager
    
    try:
        # query = """
        #     UPDATE USUARIOS 
        #     SET nombre = ?, apellido = ?, email = ?, nif = ?, telefono = ?, telefono2 = ?, rol_id = ?, activo = ?
        #     WHERE id = ?
        # """
        print("Updating user ID:", usuario_id, "with data:", usuario_data)

        set_parts = [
            "nombre = ?",
            "apellido = ?",
            "email = ?",
            "nif = ?",
            "telefono = ?",
            "telefono2 = ?",
            "rol_id = ?",
            "codempresa = ?",
            "idcliente = ?",
            "solopropios = ?",
            "activo = ?",
            "fecha_inicio = ?",
            "fecha_fin = ?"
        ]
        params = [
            usuario_data.nombre,
            usuario_data.apellido,
            usuario_data.email,
            usuario_data.nif,
            usuario_data.telefono,
            usuario_data.telefono2,
            usuario_data.rol_id,
            usuario_data.servicer,
            usuario_data.sociedad,
            usuario_data.propio,
            usuario_data.activo,
            usuario_data.fecha_inicio,
            usuario_data.fecha_fin
        ]

        # Condicional para password
        if usuario_data.password and usuario_data.password.strip():
            password_hash = auth_manager.hash_password(usuario_data.password)
            set_parts.append("password_hash = ?")
            params.append(password_hash)
        
        query = f"""
            UPDATE USUARIOS
            SET {", ".join(set_parts)}
            WHERE id = ?
        """
        params.append(usuario_id)
        
        rowcount = db_manager.execute_query(
            query, 
            tuple(params),
            #fetch_one=True
        )

        if not rowcount:
            # No se actualizó nada: id no existe
            return APIResponse(code=404, detail="Usuario no encontrado", data=None)
        
        # Get the updated user
        updated_user = UserService.get_user_by_id(usuario_id)
    
        if not updated_user:
            # Caso raro: actualizado pero no se puede leer
            return APIResponse(code=404, detail="Usuario no encontrado tras actualizar", data=None)
    
        #return UserResponse(**updated_user)
        return APIResponse(code=200, detail="Usuario actualizado correctamente", data=UserResponse(**updated_user).model_dump())
        
    except Exception as e:
        return APIResponse(code=500, detail=f"Error inesperado: {e}", data=None)

@app.delete("/api/usuarios/{usuario_id}")
async def delete_usuario(
    usuario_id: int,
    user_id: int = Depends(verify_token)
):
    from database import db_manager
    
    # Check if user exists
    existing_user = UserService.get_user_by_id(usuario_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    query = "DELETE FROM USUARIOS WHERE id = ?"
    db_manager.execute_query(query, (usuario_id,))
    
    return {"message": "Usuario eliminado correctamente"}

# Sociedades endpoints
@app.get("/api/sociedades", response_model=List[SociedadResponse])
async def get_sociedades(user_id: int = Depends(verify_token)):
    sociedades = SociedadService.get_all_sociedades()
    return [SociedadResponse(**soc) for soc in sociedades]

@app.get("/api/sociedades/{sociedad_id}", response_model=SociedadResponse)
async def get_sociedad_by_id(
    sociedad_id: int,
    user_id: int = Depends(verify_token)
):
    sociedad = SociedadService.get_sociedad_by_id(sociedad_id)
    
    if not sociedad:
        raise HTTPException(status_code=404, detail="Sociedad no encontrada")
    
    return SociedadResponse(**sociedad)

@app.post("/api/sociedades", response_model=SociedadResponse)
async def create_sociedad(
    sociedad_data: CreateSociedadRequest, 
    user_id: int = Depends(verify_token)
):
    from database import db_manager
    
    query = """
        INSERT INTO ERP_CLIENTES (
            CODCLI, CUENTA, NIFCLI, RAZON, NOMCLI, DTOCLI, DIRCLI, CODPROVI, 
            POBCLI, TELCLI, E_MAIL, CODPAIS, CONTACTO, IDREPRESEN, EXT_CARTERA, 
            EXT_ANALISTAPORDEFECTO, EXT_ACTIVIDAD, EXT_ESTADO, EXT_SPV, OBSERVACIONES
        )
        OUTPUT INSERTED.IDCLIENTE
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    result = db_manager.execute_query(
        query, 
        (sociedad_data.codcli, sociedad_data.cuenta, sociedad_data.nifcli, 
         sociedad_data.razon, sociedad_data.nomcli, sociedad_data.dtocli,
         sociedad_data.dircli, sociedad_data.codprovi, sociedad_data.pobcli,
         sociedad_data.telcli, sociedad_data.e_mail, sociedad_data.codpais,
         sociedad_data.contacto, sociedad_data.idrepresen, sociedad_data.ext_cartera,
         sociedad_data.ext_analistapordefecto, sociedad_data.ext_actividad,
         sociedad_data.ext_estado, sociedad_data.ext_spv, sociedad_data.observaciones),
        fetch_one=True
    )
    
    # Get the created sociedad
    created_sociedad = SociedadService.get_sociedad_by_id(result.IDCLIENTE)
    
    if not created_sociedad:
        raise HTTPException(status_code=500, detail="Error al crear sociedad")
    
    return SociedadResponse(**created_sociedad)

@app.put("/api/sociedades/{sociedad_id}", response_model=SociedadResponse)
async def update_sociedad(
    sociedad_id: int,
    sociedad_data: UpdateSociedadRequest,
    user_id: int = Depends(verify_token)
):
    from database import db_manager
    
    query = """
        UPDATE ERP_CLIENTES 
        SET CODCLI = ?, CUENTA = ?, NIFCLI = ?, RAZON = ?, NOMCLI = ?, DTOCLI = ?,
            DIRCLI = ?, CODPROVI = ?, POBCLI = ?, TELCLI = ?, E_MAIL = ?, CODPAIS = ?,
            CONTACTO = ?, IDREPRESEN = ?, EXT_CARTERA = ?, EXT_ANALISTAPORDEFECTO = ?,
            EXT_ACTIVIDAD = ?, EXT_ESTADO = ?, EXT_SPV = ?, OBSERVACIONES = ?
        WHERE IDCLIENTE = ?
    """
    
    db_manager.execute_query(
        query, 
        (sociedad_data.codcli, sociedad_data.cuenta, sociedad_data.nifcli,
         sociedad_data.razon, sociedad_data.nomcli, sociedad_data.dtocli,
         sociedad_data.dircli, sociedad_data.codprovi, sociedad_data.pobcli,
         sociedad_data.telcli, sociedad_data.e_mail, sociedad_data.codpais,
         sociedad_data.contacto, sociedad_data.idrepresen, sociedad_data.ext_cartera,
         sociedad_data.ext_analistapordefecto, sociedad_data.ext_actividad,
         sociedad_data.ext_estado, sociedad_data.ext_spv, sociedad_data.observaciones,
         sociedad_id)
    )
    
    # Get the updated sociedad
    updated_sociedad = SociedadService.get_sociedad_by_id(sociedad_id)
    
    if not updated_sociedad:
        raise HTTPException(status_code=404, detail="Sociedad no encontrada")
    
    return SociedadResponse(**updated_sociedad)

@app.delete("/api/sociedades/{sociedad_id}")
async def delete_sociedad(
    sociedad_id: int,
    user_id: int = Depends(verify_token)
):
    from database import db_manager
    
    # Check if sociedad exists
    existing_sociedad = SociedadService.get_sociedad_by_id(sociedad_id)
    if not existing_sociedad:
        raise HTTPException(status_code=404, detail="Sociedad no encontrada")
    
    query = "DELETE FROM ERP_CLIENTES WHERE IDCLIENTE = ?"
    db_manager.execute_query(query, (sociedad_id,))
    
    return {"message": "Sociedad eliminada correctamente"}

#@app.get("/api/representantes", response_model=List[RepresentanteResponse])
@app.get("/api/representantes", response_model=APIResponse)
async def get_representantes(user_id: int = Depends(verify_token)):
    try:
        representantes = SociedadService.get_all_representantes()
        return APIResponse(code=200, detail="", data=[RepresentanteResponse(**rep) for rep in representantes])
    except Exception as e:
        print("Error al obtener representantes:", e)
        return APIResponse(code=500, detail="Error al obtener representantes", data=None)

@app.post("/api/representantes", response_model=APIResponse)
async def create_representante(
    data: CreateRepresentanteRequest,
    user_id: int = Depends(verify_token)
):
    try:
        """Crea un nuevo representante (fondo)"""
        idrepresen = SociedadService.create_representante(data.descripcion)
        
        # Get the created representante
        representantes = SociedadService.get_all_representantes()

        created = next((r for r in representantes if r["idrepresen"] == idrepresen), None)
        
        if not created:
            #Conflict: resource already exists 
            return APIResponse(code=409, detail="Error al crear fondo", data=None)

        return APIResponse(code=200, detail="", data=RepresentanteResponse(**created))
    
    except Exception as e:
        print("Error al crear representante:", e)
        return APIResponse(code=500, detail="Error al crear fondo: " + str(e), data=None)

@app.put("/api/representantes/{idrepresen}", response_model=APIResponse)
async def update_representante(
    idrepresen: int,
    data: UpdateRepresentanteRequest,
    user_id: int = Depends(verify_token)
):
    try:
        """Actualiza un representante (fondo)"""
        SociedadService.update_representante(idrepresen, data.descripcion)
        
        # Get the updated representante
        representantes = SociedadService.get_all_representantes()
        updated = next((r for r in representantes if r["idrepresen"] == idrepresen), None)
        
        if not updated:
            return APIResponse(status_code=404, detail="Fondo no encontrado", data=None)

        return APIResponse(code=200, detail="Fondo actualizado correctamente", data=RepresentanteResponse(**updated))

    except Exception as e:
        print("Error al actualizar representante:", e)
        return APIResponse(code=500, detail="Error al actualizar fondo", data=None)

@app.delete("/api/representantes/{idrepresen}")
async def delete_representante(
    idrepresen: int,
    user_id: int = Depends(verify_token)
):
    # """Elimina un representante (fondo) si no está asignado"""
    # success = SociedadService.delete_representante(idrepresen)
    
    # if not success:
    #     raise HTTPException(
    #         status_code=400, 
    #         detail="No se puede eliminar el fondo porque está asignado a una o más sociedades"
    #     )
    
    # return {"message": "Fondo eliminado correctamente"}

    try:
        """Elimina un representante (fondo) si no está asignado"""
        success = SociedadService.delete_representante(idrepresen)

        if not success:
            return APIResponse(status_code=400, detail="No se puede eliminar el fondo porque está asignado a una o más sociedades", data=None)

        return APIResponse(code=200, detail="Fondo eliminado correctamente", data=None)

    except Exception as e:
        print("Error al eliminar representante:", e)
        return APIResponse(code=500, detail="Error al eliminar fondo", data=None)

# Roles endpoint
@app.get("/api/roles")
async def get_roles(user_id: int = Depends(verify_token)):
    """Obtiene todos los roles activos de la base de datos"""
    roles = RoleService.get_all_roles()
    return {"data": roles}

# Auditor societies management endpoints
@app.get("/api/auditores/sociedades-disponibles", response_model=List[AuditorSociedadResponse])
async def get_sociedades_disponibles(user_id: int = Depends(verify_token)):
    """Obtiene todas las sociedades disponibles para asignar a auditores"""
    sociedades = AuditorSociedadService.get_sociedades_for_table()
    return [AuditorSociedadResponse(**soc) for soc in sociedades]

@app.get("/api/auditores/{auditor_id}/sociedades")
async def get_auditor_sociedades(
    auditor_id: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene las sociedades asignadas a un auditor"""
    sociedades_ids = AuditorSociedadService.get_auditor_sociedades(auditor_id)
    return {"sociedades_ids": sociedades_ids}

@app.put("/api/auditores/{auditor_id}/sociedades")
async def update_auditor_sociedades(
    auditor_id: int,
    data: UpdateAuditorSociedadesRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza las sociedades asignadas a un auditor"""
    AuditorSociedadService.update_auditor_sociedades(auditor_id, data.sociedades_ids)
    return {"message": "Sociedades actualizadas correctamente"}

@app.get("/api/auditores/operaciones-disponibles", response_model=List[AuditorOperacionResponse])
async def get_operaciones_disponibles(user_id: int = Depends(verify_token)):
    """Obtiene todas las operaciones disponibles para asignar a auditores"""
    operaciones = AuditorOperacionService.get_operaciones_for_table()
    return [AuditorOperacionResponse(**op) for op in operaciones]

@app.get("/api/auditores/{auditor_id}/operaciones")
async def get_auditor_operaciones(
    auditor_id: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene las operaciones asignadas a un auditor"""
    operaciones_ids = AuditorOperacionService.get_auditor_operaciones(auditor_id)
    return {"operaciones_ids": operaciones_ids}

@app.put("/api/auditores/{auditor_id}/operaciones")
async def update_auditor_operaciones(
    auditor_id: int,
    data: UpdateAuditorOperacionesRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza las operaciones asignadas a un auditor"""
    AuditorOperacionService.update_auditor_operaciones(auditor_id, data.operaciones_ids)
    return {"message": "Operaciones actualizadas correctamente"}

# Folder structure management endpoints
@app.get("/api/modulos", response_model=List[ModuloResponse])
async def get_modulos(user_id: int = Depends(verify_token)):
    """Obtiene todos los módulos con sus estructuras asignadas"""
    modulos = EstructuraCarpetaService.get_all_modulos()
    return [ModuloResponse(**mod) for mod in modulos]

@app.get("/api/estructuras", response_model=List[EstructuraCarpetaResponse])
async def get_estructuras_raiz(user_id: int = Depends(verify_token)):
    """Obtiene todas las estructuras raíz"""
    estructuras = EstructuraCarpetaService.get_estructuras_raiz()
    result = [EstructuraCarpetaResponse(**est) for est in estructuras]
    print("Estructuras raíz fetched:", result)
    return result

@app.get("/api/estructuras/activas")
async def get_estructuras_activas(user_id: int = Depends(verify_token)):
    """Obtiene solo las estructuras activas para asignación"""
    estructuras = EstructuraCarpetaService.get_estructuras_activas()
    
    return estructuras

@app.get("/api/estructuras/{idestructura}/tree")
async def get_estructura_tree(
    idestructura: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene el árbol completo de una estructura"""
    tree = EstructuraCarpetaService.get_estructura_tree(idestructura)
    return tree

@app.post("/api/estructuras")
async def create_estructura(
    data: CreateEstructuraRequest,
    user_id: int = Depends(verify_token)
):
    print("Creating estructura with data:", data)
    """Crea una nueva estructura raíz"""
    idestructura = EstructuraCarpetaService.create_estructura(data.nombre, data.activa)

    print("Created estructura with ID:", idestructura)
    return {"idcarpeta": idestructura, "message": "Estructura creada correctamente"}

@app.put("/api/estructuras/{idestructura}")
async def update_estructura(
    idestructura: int,
    data: UpdateEstructuraRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza una estructura"""
    EstructuraCarpetaService.update_estructura(idestructura, data.nombre, data.activa)
    return {"message": "Estructura actualizada correctamente"}

@app.delete("/api/estructuras/{idestructura}")
async def delete_estructura(
    idestructura: int,
    user_id: int = Depends(verify_token)
):
    """Elimina una estructura si no está asignada"""
    success = EstructuraCarpetaService.delete_estructura(idestructura)
    
    if not success:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar la estructura porque está asignada a un módulo"
        )
    
    return {"message": "Estructura eliminada correctamente"}

@app.post("/api/modulos/asignar")
async def asignar_modulo_estructura(
    data: AsignarModuloEstructuraRequest,
    user_id: int = Depends(verify_token)
):
    """Asigna una estructura a un módulo"""
    EstructuraCarpetaService.asignar_modulo_estructura(data.idmodulo, data.idestructuracarpeta)
    return {"message": "Estructura asignada correctamente"}

@app.delete("/api/modulos/{idmodulo}/desasignar")
async def desasignar_modulo_estructura(
    idmodulo: int,
    user_id: int = Depends(verify_token)
):
    """Desasigna la estructura de un módulo"""
    EstructuraCarpetaService.desasignar_modulo_estructura(idmodulo)
    return {"message": "Estructura desasignada correctamente"}

# async def upload_file(
#     idestructura: int,
#     idcarpetapadre: Optional[int] = None,
#     file: UploadFile = File(...),
#     user_id: int = Depends(verify_token)
# ):

@app.post("/api/estructuras/{idestructura}/upload")
async def upload_file(
    idestructura: int,
    idcarpetapadre: Optional[int] = Form(None),
    file: UploadFile = File(...),
    user_id: int = Depends(verify_token)
):
    try:
        """Sube un archivo a una carpeta de la estructura"""
        # Validar tamaño (10MB máximo)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB en bytes

        print("Uploading file:", file.filename, "to estructura:", idestructura, "carpeta padre:", idcarpetapadre)
        
        # Leer el archivo para obtener su tamaño
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"El archivo excede el tamaño máximo permitido de 10MB. Tamaño: {file_size / (1024*1024):.2f}MB"
            )
        
        # Crear carpeta para la estructura si no existe
        estructura_dir = UPLOAD_DIR / str(idestructura)
        estructura_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = Path(file.filename).suffix
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = estructura_dir / safe_filename
        
        # Guardar archivo
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Crear registro en la base de datos
        file_url = f"/uploads/estructuras/{idestructura}/{safe_filename}"

        print("File saved at:", file_path)
        print("File URL:", file_url)
        print("File size:", file_size)
        print("Parent:", idcarpetapadre)
        
        idcarpeta = EstructuraCarpetaService.create_file_record(
            idestructura,
            idcarpetapadre,
            file.filename,
            file_url,
            file_size,
            file.content_type
        )
        
        return {
            "idcarpeta": idcarpeta,
            "archivo_url": file_url,
            "archivo_size": file_size,
            "message": "Archivo subido correctamente"
        }
    except Exception as e:
        print("Error uploading file:", e)
        raise HTTPException(status_code=500, detail="Error al subir el archivo")
    



@app.post("/api/estructuras/{idestructura}/carpetas")
async def create_carpeta(
    idestructura: int,
    data: CreateCarpetaRequest,
    user_id: int = Depends(verify_token)
):
    
    print("Creating carpeta with data:", data)
    
    """Crea una nueva carpeta o archivo en la estructura"""
    idcarpeta = EstructuraCarpetaService.create_carpeta(
        idestructura, 
        data.idcarpetapadre, 
        data.nombre, 
        data.archivo
    )
    return {"idcarpeta": idcarpeta, "message": "Carpeta creada correctamente"}


@app.delete("/api/estructuras/archivos/{idcarpeta}")
async def delete_file(
    idcarpeta: int,
    user_id: int = Depends(verify_token)
):
    """Elimina un archivo y su registro"""
    file_info = EstructuraCarpetaService.get_file_info(idcarpeta)
    
    if not file_info:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    # Eliminar archivo físico si existe
    if file_info.get("archivo_url"):
        file_path = Path("." + file_info["archivo_url"])
        if file_path.exists():
            file_path.unlink()
    
    # Eliminar registro de la base de datos
    EstructuraCarpetaService.delete_carpeta(idcarpeta)
    
    return {"message": "Archivo eliminado correctamente"}

# TipoRelacion endpoints for Relaciones view
@app.get("/api/tipos-relacion", response_model=APIResponse)
async def get_tipos_relacion(user_id: int = Depends(verify_token)):
    try:
        """Obtiene todos los tipos de relación"""
        tipos = TipoRelacionService.get_all_tipos_relacion()

        return APIResponse(code=200, detail='', data=[TipoRelacionResponse(**tipo) for tipo in tipos])

    except Exception as e:
        print("Error al obtener las relaciones:", e)
        return APIResponse(code=500, detail="Error al obtener las relaciones", data=None)

@app.post("/api/tipos-relacion", response_model=APIResponse)
async def create_tipo_relacion(
    data: CreateTipoRelacionRequest,
    user_id: int = Depends(verify_token)
):
    try:
        """Crea un nuevo tipo de relación"""
        idtiporelacion = TipoRelacionService.create_tipo_relacion(
            data.descripcion, 
            data.estructurajuridica
        )
        
        # Get the created tipo relacion
        tipos = TipoRelacionService.get_all_tipos_relacion()
        created = next((t for t in tipos if t["idtiporelacion"] == idtiporelacion), None)
        
        if not created:
            return APIResponse(code=500, detail="Error al crear tipo de relación", data=None)
        
        return APIResponse(code=200, detail="Relación creada correctamente", data=TipoRelacionResponse(**created))
    
    except Exception as e:
        return APIResponse(code=500, detail="Error al crear la relación: " + str(e), data=None)

@app.put("/api/tipos-relacion/{idtiporelacion}", response_model=APIResponse)
async def update_tipo_relacion(
    idtiporelacion: int,
    data: UpdateTipoRelacionRequest,
    user_id: int = Depends(verify_token)
):
    try:
        """Actualiza un tipo de relación"""
        TipoRelacionService.update_tipo_relacion(
            idtiporelacion, 
            data.descripcion, 
            data.estructurajuridica
        )
        
        # Get the updated tipo relacion
        tipos = TipoRelacionService.get_all_tipos_relacion()
        updated = next((t for t in tipos if t["idtiporelacion"] == idtiporelacion), None)
        
        if not updated:
            raise APIResponse(code=404, detail="Tipo de relación no encontrado", data=None)
        
        return APIResponse(code=200, detail="La relación se ha actualizado", data=TipoRelacionResponse(**updated))
    except Exception as e:
        print("Error al actualizar relación:", e)
        return APIResponse(code=500, detail="Error al actualizar la relación", data=None)

@app.delete("/api/tipos-relacion/{idtiporelacion}")
async def delete_tipo_relacion(
    idtiporelacion: int,
    user_id: int = Depends(verify_token)
):
    try:

        print("Deleting tipo relacion ID:", idtiporelacion)

        """Elimina un tipo de relación si no está en uso"""
        success = TipoRelacionService.delete_tipo_relacion(idtiporelacion)
        
        print("Delete tipo relacion success:", success)

        if not success:
            return APIResponse(
                code=400, 
                detail="No se puede eliminar el tipo de relación porque está en uso",
                data=None
            )
        
        return APIResponse(code=200, detail="Tipo de relación eliminado correctamente", data=None)
    
    except Exception as e:
        return APIResponse(code=500, detail="Error al eliminar la relación", data=None)
    
# TipoAlerta endpoints for Tipos Alerta view
@app.get("/api/tipos-alerta", response_model=APIResponse)
async def get_tipos_alerta(user_id: int = Depends(verify_token)):
    """Obtiene todos los tipos de alerta"""
    try:
        tipos = TipoAlertaService.get_all_tipos_alerta()
        return APIResponse(code=200, detail="Tipos de alerta obtenidos correctamente", data=[TipoAlertaResponse(**tipo) for tipo in tipos])
    except Exception as e:
        return APIResponse(code=500, detail="Error al obtener los tipos de alerta", data=None)

@app.post("/api/tipos-alerta", response_model=APIResponse)
async def create_tipo_alerta(
    data: CreateTipoAlertaRequest,
    user_id: int = Depends(verify_token)
):
    """Crea un nuevo tipo de alerta"""
    try:
        idtipoalerta = TipoAlertaService.create_tipo_alerta(data.descripcion)
        
        # Get the created tipo alerta
        tipos = TipoAlertaService.get_all_tipos_alerta()
        created = next((t for t in tipos if t["idtipoalerta"] == idtipoalerta), None)
        
        if not created:
            return APIResponse(code=500, detail="Error al crear tipo de alerta", data=None)

        return APIResponse(code=200, detail="Tipo de alerta creado correctamente", data=TipoAlertaResponse(**created))
    except Exception as e:
        return APIResponse(code=500, detail="Error al crear el tipo de alerta: " + str(e), data=None)

@app.put("/api/tipos-alerta/{idtipoalerta}", response_model=APIResponse)
async def update_tipo_alerta(
    idtipoalerta: int,
    data: UpdateTipoAlertaRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza un tipo de alerta"""
    try:
        TipoAlertaService.update_tipo_alerta(idtipoalerta, data.descripcion)
        
        # Get the updated tipo alerta
        tipos = TipoAlertaService.get_all_tipos_alerta()
        updated = next((t for t in tipos if t["idtipoalerta"] == idtipoalerta), None)
        
        if not updated:
            return APIResponse(code=404, detail="Tipo de alerta no encontrado", data=None)

        return APIResponse(code=200, detail="Tipo de alerta actualizado correctamente", data=TipoAlertaResponse(**updated))
    
    except Exception as e:
        return APIResponse(code=500, detail="Error al actualizar el tipo de alerta", data=None)

@app.delete("/api/tipos-alerta/{idtipoalerta}")
async def delete_tipo_alerta(
    idtipoalerta: int,
    user_id: int = Depends(verify_token)
):
    """Elimina un tipo de alerta"""
    try:
        success = TipoAlertaService.delete_tipo_alerta(idtipoalerta)
        
        if not success:
            return APIResponse(code=400, 
                detail="No se puede eliminar el tipo de alerta porque está en uso",
                data=None
            )
        
        return APIResponse(code=200, detail="Tipo de alerta eliminado correctamente", data=None)
    
    except Exception as e:
        return APIResponse(code=500, detail="Error al eliminar la relación", data=None)


# Proceso endpoints for Definición Procesos view
@app.get("/api/procesos")
async def get_procesos(user_id: int = Depends(verify_token)):
    """Obtiene todos los procesos"""
    procesos = ProcesoService.get_all_procesos()
    return APIResponse(
        code=200,
        detail="Procesos obtenidos correctamente",
        data=procesos
    )

@app.post("/api/procesos")
async def create_proceso(
    data: CreateProcesoRequest,
    user_id: int = Depends(verify_token)
):
    """Crea un nuevo proceso"""
    idproceso = ProcesoService.create_proceso(
        data.descripcion,
        data.prefijo,
        data.visibilidad
    )
    
    # Get the created proceso
    procesos = ProcesoService.get_all_procesos()
    created = next((p for p in procesos if p["idproceso"] == idproceso), None)
    
    if not created:
        raise HTTPException(status_code=500, detail="Error al crear proceso")
    
    return APIResponse(
        code=201,
        detail="Proceso creado correctamente",
        data=created
    )

@app.put("/api/procesos/{idproceso}")
async def update_proceso(
    idproceso: int,
    data: UpdateProcesoRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza un proceso"""
    ProcesoService.update_proceso(
        idproceso,
        data.descripcion,
        data.prefijo,
        data.visibilidad
    )
    
    # Get the updated proceso
    procesos = ProcesoService.get_all_procesos()
    updated = next((p for p in procesos if p["idproceso"] == idproceso), None)
    
    if not updated:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    
    return APIResponse(
        code=200,
        detail="Proceso actualizado correctamente",
        data=updated
    )

@app.delete("/api/procesos/{idproceso}")
async def delete_proceso(
    idproceso: int,
    user_id: int = Depends(verify_token)
):
    """Elimina un proceso si no está en uso"""
    success = ProcesoService.delete_proceso(idproceso)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el proceso porque está asignado a una o más tareas"
        )
    
    return APIResponse(
        code=200,
        detail="Proceso eliminado correctamente",
        data=None
    )

# New endpoints for acciones and proceso estados
@app.get("/api/acciones")
async def get_acciones_for_proceso(user_id: int = Depends(verify_token)):
    """Obtiene acciones activas para procesos"""
    acciones = AccionService.get_acciones_for_proceso()
    return APIResponse(
        code=200,
        detail="Acciones obtenidas correctamente",
        data=acciones
    )

@app.get("/api/procesos/{idproceso}")
async def get_proceso_by_id(
    idproceso: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene un proceso por ID con sus estados"""
    proceso = ProcesoService.get_proceso_by_id(idproceso)
    
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    
    return APIResponse(
        code=200,
        detail="Proceso obtenido correctamente",
        data=proceso
    )

@app.post("/api/procesos/{idproceso}/estados")
async def create_proceso_estado(
    idproceso: int,
    data: CreateProcesoEstadoRequest,
    user_id: int = Depends(verify_token)
):
    """Crea un nuevo estado para un proceso"""
    # Get accion to use its descripcion as titulo
    acciones = AccionService.get_acciones_for_proceso()
    accion = next((a for a in acciones if a["idaccion"] == data.idaccion), None)
    
    if not accion:
        raise HTTPException(status_code=404, detail="Acción no encontrada")
    
    idestado = ProcesoEstadoService.create_estado(
        idproceso,
        accion["descripcion"],
        data.visibilidad,
        data.orden,
        data.finaliza
    )
    
    return APIResponse(
        code=201,
        detail="Estado creado correctamente",
        data={"idestado": idestado}
    )

@app.put("/api/procesos/estados/{idestado}")
async def update_proceso_estado(
    idestado: int,
    data: UpdateProcesoEstadoRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza un estado"""
    ProcesoEstadoService.update_estado(
        idestado,
        data.visibilidad,
        data.orden,
        data.finaliza
    )
    
    return APIResponse(
        code=200,
        detail="Estado actualizado correctamente",
        data=None
    )

@app.delete("/api/procesos/estados/{idestado}")
async def delete_proceso_estado(
    idestado: int,
    user_id: int = Depends(verify_token)
):
    """Elimina un estado"""
    ProcesoEstadoService.delete_estado(idestado)
    
    return APIResponse(
        code=200,
        detail="Estado eliminado correctamente",
        data=None
    )

@app.get("/api/procesos/{idproceso}/estados")
async def get_proceso_estados(
    idproceso: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene los estados de un proceso"""
    estados = ProcesoEstadoService.get_estados_by_proceso(idproceso)
    
    return APIResponse(
        code=200,
        detail="Estados obtenidos correctamente",
        data=estados
    )

@app.post("/api/procesos-completo")
async def create_proceso_with_estados(
    data: CreateProcesoWithEstadosRequest,
    user_id: int = Depends(verify_token)
):
    """Crea un proceso con sus estados"""
    # Create proceso
    idproceso = ProcesoService.create_proceso(
        data.descripcion,
        data.prefijo,
        data.visibilidad
    )
    print("idproceso que voy a usar para estados:", idproceso, type(idproceso))
    
    # Create estados
    acciones = AccionService.get_acciones_for_proceso()
    for estado_data in data.estados:
        accion = next((a for a in acciones if a["idaccion"] == estado_data.idaccion), None)
        if accion:
            ProcesoEstadoService.create_estado(
                accion["idaccion"],
                idproceso,
                accion["descripcion"],
                estado_data.visibilidad,
                estado_data.orden,
                estado_data.finaliza
            )
    # Get the created proceso with estados
    proceso = ProcesoService.get_proceso_by_id(idproceso)
    
    return APIResponse(
        code=201,
        detail="Proceso creado correctamente",
        data=proceso
    )

@app.put("/api/procesos-completo/{idproceso}")
async def update_proceso_with_estados(
    idproceso: int,
    data: UpdateProcesoWithEstadosRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza un proceso con sus estados"""
    # Update proceso
    ProcesoService.update_proceso(
        idproceso,
        data.descripcion,
        data.prefijo,
        data.visibilidad
    )
    
    # Delete all existing estados
    ProcesoEstadoService.delete_estados_by_proceso(idproceso)
    
    # Create new estados
    acciones = AccionService.get_acciones_for_proceso()
    for estado_dict in data.estados:
        # estado_dict can have either idaccion (new) or idestado (existing, but we're recreating all)

        idaccion = estado_dict.get("idestado")
        titulo = estado_dict.get("titulo")
        
        # If we have idaccion, get the accion descripcion
        if idaccion:
            accion = next((a for a in acciones if a["idaccion"] == idaccion), None)
            if accion:
                titulo = accion["descripcion"]
        
        if titulo:

            print("Creating estado for proceso:", idproceso, "with titulo:", titulo, "and idaccion:", idaccion)

            ProcesoEstadoService.create_estado(
                idaccion,
                idproceso,
                titulo,
                estado_dict.get("visibilidad", True),
                estado_dict.get("orden", 0),
                estado_dict.get("finaliza", False)
            )
    
    # Get the updated proceso with estados
    proceso = ProcesoService.get_proceso_by_id(idproceso)
    
    return APIResponse(
        code=200,
        detail="Proceso actualizado correctamente",
        data=proceso
    )


# New endpoints for gestion de roles de estados
@app.get("/api/procesos/{idproceso}/estados/{idestado}/roles")
async def get_estado_roles(
    idproceso: int,
    idestado: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene los roles asignados a un estado"""
    roles = ProcesoEstadoRolService.get_roles_by_estado(idproceso, idestado)
    
    return APIResponse(
        code=200,
        detail="Roles obtenidos correctamente",
        data=roles
    )

@app.post("/api/procesos/{idproceso}/estados/{idestado}/roles")
async def create_estado_rol(
    idproceso: int,
    idestado: int,
    data: CreateEstadoRolRequest,
    user_id: int = Depends(verify_token)
):
    """Crea un nuevo rol para un estado"""
    id_rol = ProcesoEstadoRolService.create_estado_rol(
        idproceso,
        idestado,
        data.idrol,
        data.lectura,
        data.escritura,
        data.cambioestado
    )
    
    return APIResponse(
        code=201,
        detail="Rol agregado correctamente",
        data={"id": id_rol}
    )

@app.put("/api/procesos/estados/roles/{id}")
async def update_estado_rol(
    id: int,
    data: UpdateEstadoRolRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza un rol de estado"""
    ProcesoEstadoRolService.update_estado_rol(
        id,
        data.lectura,
        data.escritura,
        data.cambioestado
    )
    
    return APIResponse(
        code=200,
        detail="Rol actualizado correctamente",
        data=None
    )

@app.delete("/api/procesos/estados/roles/{id}")
async def delete_estado_rol(
    id: int,
    user_id: int = Depends(verify_token)
):
    """Elimina un rol de estado"""
    ProcesoEstadoRolService.delete_estado_rol(id)
    
    return APIResponse(
        code=200,
        detail="Rol eliminado correctamente",
        data=None
    )

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/countries")
async def get_countries():
    try:
        countries = await CountryService.get_all_countries()
        return APIResponse(code=200, details='', data=countries)
    except Exception as e:
        return APIResponse(code=500, detail="Database connection error: " + str(e), data=None)

@app.get("/api/subdivisions/{countryiso}")
async def get_subdivisions(countryiso: str):
    try:
        subdivisions = await CountryService.get_subdivisions(countryiso)
        return APIResponse(code=200, details='', data=subdivisions)
    except Exception as e:
        return APIResponse(code=500, detail="Database connection error: " + str(e), data=None)
    

# New endpoints for gestion de roles de estados
@app.get("/api/procesos/{idproceso}/estados/{idestado}/roles")
async def get_estado_roles(
    idproceso: int,
    idestado: int,
    user_id: int = Depends(verify_token)
):
    try:
        """Obtiene los roles asignados a un estado"""
        roles = ProcesoEstadoRolService.get_roles_by_estado(idproceso, idestado)
        
        return APIResponse(
            code=200,
            detail="Roles obtenidos correctamente",
            data=roles
        )
    except Exception as e:
        print("Error al obtener roles de estado:", e)
        return APIResponse(
            code=500,
            detail="Error al obtener los roles: " + str(e),
            data=None
        )

@app.post("/api/procesos/{idproceso}/estados/{idestado}/roles")
async def create_estado_rol(
    idproceso: int,
    idestado: int,
    data: CreateEstadoRolRequest,
    user_id: int = Depends(verify_token)
):
    try:
            """Crea un nuevo rol para un estado"""
            id_rol = ProcesoEstadoRolService.create_estado_rol(
                idproceso,
                idestado,
                data.idrol,
                data.lectura,
                data.escritura,
                data.cambioestado
            )
            
            return APIResponse(
                code=201,
                detail="Rol agregado correctamente",
                data={"id": id_rol}
            )
    except Exception as e:
        print("Error al crear rol de estado:", e)
        return APIResponse(
            code=500,
            detail="Error al agregar el rol: " + str(e),
            data=None
        )

@app.put("/api/procesos/estados/roles/{id}")
async def update_estado_rol(
    id: int,
    data: UpdateEstadoRolRequest,
    user_id: int = Depends(verify_token)
):
    try:
        """Actualiza un rol de estado"""
        ProcesoEstadoRolService.update_estado_rol(
            id,
            data.lectura,
            data.escritura,
            data.cambioestado
        )
        
        return APIResponse(
            code=200,
            detail="Rol actualizado correctamente",
            data=None
        )
    except Exception as e:
        print("Error al actualizar rol de estado:", e)
        return APIResponse(
            code=500,
            detail="Error al actualizar el rol: " + str(e),
            data=None
        )

@app.delete("/api/procesos/estados/roles/{id}")
async def delete_estado_rol(
    id: int,
    user_id: int = Depends(verify_token)
):
    try:
        """Elimina un rol de estado"""
        ProcesoEstadoRolService.delete_estado_rol(id)
        
        return APIResponse(
            code=200,
            detail="Rol eliminado correctamente",
            data=None
        )
    except Exception as e:
        print("Error al eliminar rol de estado:", e)
        return APIResponse(
            code=500,
            detail="Error al eliminar el rol: " + str(e),
            data=None
        )

@app.post("/api/procesos/{idproceso}/estados/{idestado}/roles/batch")
async def save_estado_roles_batch(
    idproceso: int,
    idestado: int,
    data: SaveEstadoRolesBatchRequest,
    user_id: int = Depends(verify_token)
):
    try:
        """Guarda múltiples roles para un estado en una sola operación"""
        ProcesoEstadoRolService.save_roles_batch(
            idproceso,
            idestado,
            data.roles
        )
        
        return APIResponse(
            code=200,
            detail="Roles guardados correctamente",
            data=None
        )
    except Exception as e:
        print("Error al guardar roles en batch:", e)
        return APIResponse(
            code=500,
            detail="Error al guardar los roles: " + str(e),
            data=None
        )


# Catalogos endpoints for tareas (operaciones)
@app.get("/api/catalogos/tipos-activos")
async def get_tipos_activos(user_id: int = Depends(verify_token)):
    """Obtiene todos los tipos de activos"""
    tipos = CatalogoService.get_tipos_activos()
    return APIResponse(
        code=200,
        detail="Tipos de activos obtenidos correctamente",
        data=tipos
    )

@app.get("/api/catalogos/tipos-operaciones")
async def get_tipos_operaciones(user_id: int = Depends(verify_token)):
    """Obtiene todos los tipos de operaciones"""
    tipos = CatalogoService.get_tipos_operaciones()
    return APIResponse(
        code=200,
        detail="Tipos de operaciones obtenidos correctamente",
        data=tipos
    )

@app.get("/api/catalogos/clientes")
async def get_clientes(user_id: int = Depends(verify_token)):
    """Obtiene todos los clientes (sociedades)"""
    clientes = CatalogoService.get_clientes()
    return APIResponse(
        code=200,
        detail="Clientes obtenidos correctamente",
        data=clientes
    )

@app.get("/api/catalogos/paises")
async def get_paises(user_id: int = Depends(verify_token)):
    """Obtiene todos los países"""
    paises = CatalogoService.get_paises()
    return APIResponse(
        code=200,
        detail="Países obtenidos correctamente",
        data=paises
    )

@app.get("/api/catalogos/provincias/{country_code}")
async def get_provincias(
    country_code: str,
    user_id: int = Depends(verify_token)
):
    """Obtiene las provincias de un país"""
    provincias = CatalogoService.get_provincias(country_code)
    return APIResponse(
        code=200,
        detail="Provincias obtenidas correctamente",
        data=provincias
    )

@app.get("/api/catalogos/analistas-pbc")
async def get_analistas_pbc(user_id: int = Depends(verify_token)):
    """Obtiene los analistas PBC (usuarios con perfil 2)"""
    analistas = CatalogoService.get_analistas_pbc()
    return APIResponse(
        code=200,
        detail="Analistas PBC obtenidos correctamente",
        data=analistas
    )

@app.get("/api/catalogos/operadores")
async def get_operadores(user_id: int = Depends(verify_token)):
    """Obtiene los operadores (usuarios con perfil 7)"""
    operadores = CatalogoService.get_operadores()
    return APIResponse(
        code=200,
        detail="Operadores obtenidos correctamente",
        data=operadores
    )

# Tareas (operaciones) endpoints
@app.get("/api/tareas/{idtarea}")
async def get_tarea_by_id(
    idtarea: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene una tarea por ID"""
    tarea = TareaService.get_tarea_by_id(idtarea)
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    #print("Tarea fetched:", tarea)
    
    return APIResponse(
        code=200,
        detail="Tarea obtenida correctamente",
        data=tarea
    )

@app.post("/api/tareas")
async def create_tarea(
    data: CreateTareaRequest,
    user_id: int = Depends(verify_token)
):
    """Crea una nueva tarea (operación)"""
    idtarea = TareaService.create_tarea(data.model_dump(), user_id)
    
    # Get the created tarea
    tarea = TareaService.get_tarea_by_id(idtarea)
    
    return APIResponse(
        code=201,
        detail="Tarea creada correctamente",
        data=tarea
    )

# @app.put("/api/tareas/{idtarea}")
# async def update_tarea(
#     idtarea: int,
#     data: UpdateTareaRequest,
#     user_id: int = Depends(verify_token)
# ):
#     """Actualiza una tarea"""
#     TareaService.update_tarea(idtarea, data, user_id)
    
#     # Get the updated tarea
#     tarea = TareaService.get_tarea_by_id(idtarea)
    
#     return APIResponse(
#         code=200,
#         detail="Tarea actualizada correctamente",
#         data=tarea
#     )

@app.put("/api/tareas/{idtarea}/hitos/activate/{idhito}")
async def activate_hito(
    idtarea: int,
    idhito: int,
    user_id: int = Depends(verify_token)
):
    #If gIdrol = 2 Then
    role = UserService.get_user_by_id(user_id)["rol_id"]
    print("User role for activating hito:", role)
    
    """Activa un hito"""
    result = HitoService.activate_hito(idtarea, idhito)    
    
    #TODO: ENVIAR CORREO AL OPERADOR
    #Tipo de envíos de correos para Analista:
    #Solicitada Documentacion, Aprobado PBC, Fallido PBC y Denegado pbc envia un correo al operador

    return APIResponse(
        code=200,
        detail="Hito activado correctamente",
        data=result
    )

# New endpoints for catalogos de hitos
@app.get("/api/catalogos/monedas")
async def get_monedas(user_id: int = Depends(verify_token)):
    """Obtiene todas las monedas"""
    monedas = ImportesHitosService.get_monedas()
    return APIResponse(
        code=200,
        detail="Monedas obtenidas correctamente",
        data=monedas
    )

@app.get("/api/catalogos/tributaciones")
async def get_tributaciones(user_id: int = Depends(verify_token)):
    """Obtiene todas las tributaciones"""
    tributaciones = ImportesHitosService.get_tributaciones()
    return APIResponse(
        code=200,
        detail="Tributaciones obtenidas correctamente",
        data=tributaciones
    )

@app.get("/api/catalogos/tipos-pago")
async def get_tipos_pago(user_id: int = Depends(verify_token)):
    """Obtiene todos los tipos de pago (hitos)"""
    tipos = ImportesHitosService.get_tipos_pago()
    return APIResponse(
        code=200,
        detail="Tipos de pago obtenidos correctamente",
        data=tipos
    )

# New endpoints CRUD for hitos
@app.get("/api/tareas/{idtarea}/hitos")
async def get_hitos_by_tarea(
    idtarea: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene todos los hitos de una tarea"""
    hitos = HitoService.get_hitos_by_tarea(idtarea)
    
    return APIResponse(
        code=200,
        detail="Hitos obtenidos correctamente",
        data=hitos
    )

@app.post("/api/tareas/{idtarea}/hitos")
async def create_hito(
    idtarea: int,
    data: CreateHitoRequest,
    user_id: int = Depends(verify_token)
):
    """Crea un nuevo hito para una tarea"""
    
    # Check if any hito is activated
    if HitoService.has_activated_hitos(idtarea):
        raise HTTPException(
            status_code=400,
            detail="No se pueden agregar hitos cuando ya hay hitos activados"
        )
    
    data.fecha = data.fecha or datetime.utcnow().date()
    
    idtareaplazo = HitoService.create_hito(idtarea, data.numhito, data.descripcion, data.importe, data.fecha)
    
    # Get the created hito
    hitos = HitoService.get_hitos_by_tarea(idtarea)
    created = next((h for h in hitos if h["idtareaplazo"] == idtareaplazo), None)
    
    return APIResponse(
        code=201,
        detail="Hito creado correctamente",
        data=created
    )

@app.put("/api/tareas/hitos/{idtareaplazo}")
async def update_hito(
    idtareaplazo: int,
    data: UpdateHitoRequest,
    user_id: int = Depends(verify_token)
):
    """Actualiza un hito"""
    
    # Check if any hito is activated in this tarea
    hito_info = HitoService.get_hito_by_id(idtareaplazo)
    if not hito_info:
        raise HTTPException(status_code=404, detail="Hito no encontrado")
    
    if HitoService.has_activated_hitos(hito_info["idtarea"]):
        raise HTTPException(
            status_code=400,
            detail="No se pueden editar hitos cuando ya hay hitos activados"
        )
    
    HitoService.update_hito(idtareaplazo, data)
    
    # Get the updated hito
    updated = HitoService.get_hito_by_id(idtareaplazo)
    
    return APIResponse(
        code=200,
        detail="Hito actualizado correctamente",
        data=updated
    )

@app.delete("/api/tareas/hitos/{idtareaplazo}")
async def delete_hito(
    idtareaplazo: int,
    user_id: int = Depends(verify_token)
):
    """Elimina un hito"""
    
    # Check if any hito is activated in this tarea
    hito_info = HitoService.get_hito_by_id(idtareaplazo)
    if not hito_info:
        raise HTTPException(status_code=404, detail="Hito no encontrado")
    
    if HitoService.has_activated_hitos(hito_info["idtarea"]):
        raise HTTPException(
            status_code=400,
            detail="No se pueden eliminar hitos cuando ya hay hitos activados"
        )
    
    HitoService.delete_hito(idtareaplazo)
    
    return APIResponse(
        code=200,
        detail="Hito eliminado correctamente",
        data=None
    )

@app.put("/api/tareas/{idtarea}/hitos/reorder")
async def reorder_hitos(
    idtarea: int,
    data: ReorderHitosRequest,
    user_id: int = Depends(verify_token)
):
    """Reordena los hitos de una tarea"""
    
    # Check if any hito is activated
    if HitoService.has_activated_hitos(idtarea):
        raise HTTPException(
            status_code=400,
            detail="No se pueden reordenar hitos cuando ya hay hitos activados"
        )
    
    # HitoService.reorder_hitos(idtarea, data.hitos)
    HitoService.reorder_hitos(data.hitos)
    
    return APIResponse(
        code=200,
        detail="Hitos reordenados correctamente",
        data=None
    )

# Tareas (operaciones) endpoints
@app.get("/api/tareas/{idtarea}")
async def get_tarea_by_id(
    idtarea: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene una tarea por ID"""
    tarea = TareaService.get_tarea_by_id(idtarea)
    
    if not tarea:
        raise APIResponse(code=404, detail="Tarea no encontrada", data=None)
    
    return APIResponse(
        code=200,
        detail="Tarea obtenida correctamente",
        data=tarea
    )

@app.post("/api/tareas")
async def create_tarea(
    data: CreateTareaRequest,
    user_id: int = Depends(verify_token)
):
    """Crea una nueva tarea (operación)"""
    idtarea = TareaService.create_tarea(data, user_id)
    
    # Get the created tarea
    tarea = TareaService.get_tarea_by_id(idtarea)

    if not tarea:
        raise APIResponse(code=404, detail="No ha sido posible crear la tarea", data=None)
    
    return APIResponse(
        code=201,
        detail="Tarea creada correctamente",
        data=tarea
    )

@app.put("/api/tareas/{idtarea}")
async def update_tarea(
    idtarea: int,
    data: UpdateTareaRequest,
    user_id: int = Depends(verify_token)
):
    print("Updating tarea ID:", idtarea, "with data:", data)
    """Actualiza una tarea"""
    TareaService.update_tarea(idtarea, data, user_id)
    
    # Get the updated tarea
    tarea = TareaService.get_tarea_by_id(idtarea)

    if not tarea:
        raise APIResponse(code=404, detail="No ha sido posible actualizar la tarea", data=None)
    
    return APIResponse(
        code=200,
        detail="Tarea actualizada correctamente",
        data=tarea
    )
@app.post("/api/tareas/{idtarea}/hitos/logs/{idhito}")
async def create_log_hito(
    idtarea: int,
    idhito: int,
    data: LogRequest,
    user_id: int = Depends(verify_token)
):
    try:
        print("data received for log:", data)
        """Crea un nuevo log para un hito"""
        idlog = LogService.create_tarea_log(user_id, idtarea, idhito, data.idaccion, data.comentario)

        # Get the created log
        log = LogService.get_tarea_log_by_id(idlog)

        if not log:
            raise APIResponse(code=404, detail="no ha sido posible crear el log", data=None)

        return APIResponse(
            code=201,
            detail="Log creado correctamente",
            data=log
        )
    except Exception as e:
        print("Error creating log:" + str(e))
        return APIResponse(code=500, detail="Error al crear el log: " + str(e), data=None)

# Personas Naturales endpoints
@app.get("/api/personas-naturales")
async def get_personas_naturales(user_id: int = Depends(verify_token)):
    """Obtiene todas las personas naturales"""
    personas = PersonasNaturalesService.get_all_personas_naturales()
    return APIResponse(
        code=200,
        detail="Personas naturales obtenidas correctamente",
        data=personas
    )

@app.get("/api/personas-naturales/{persona_id}")
async def get_persona_natural_by_id(
    persona_id: int,
    user_id: int = Depends(verify_token)
):
    """Obtiene una persona natural por ID"""
    persona = PersonasNaturalesService.get_persona_by_id(persona_id)
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona natural no encontrada")
    
    return APIResponse(
        code=200,
        detail="Persona natural obtenida correctamente",
        data=persona
    )

@app.get("/api/catalogos/tipos-documento")
async def get_tipos_documento(user_id: int = Depends(verify_token)):
    """Obtiene todos los tipos de documento"""
    tipos = PersonasNaturalesService.get_tipos_documento()
    return APIResponse(
        code=200,
        detail="Tipos de documento obtenidos correctamente",
        data=tipos
    )

# for r in app.routes:
#     try:
#         print(r.methods, r.path)
#     except:
#         pass


# print("App file:", __file__)

if __name__ == "__main__":

#     print("caca")

#     for r in app.router.routes:
#         try:
#             print(r.methods, r.path)
#         except:
#             pass

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# from fastapi import FastAPI, UploadFile, File, Form, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# app = FastAPI()
# security = HTTPBearer()

# def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     return 1  # stub

# @app.post("/api/caca/{idestructura}/upload")
# async def upload_file(
#     idestructura: int,
#     idcarpetapadre: int | None = Form(None),
#     file: UploadFile = File(...),
#     user_id: int = Depends(verify_token),
# ):
#     return {"ok": True}
