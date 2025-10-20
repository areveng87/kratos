from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from database import db_manager
from models import *
from auth import auth_manager
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict]:
        """Autentica un usuario"""
        query = """
            SELECT u.id, u.email, u.password_hash, u.nombre, u.apellido, 
                   r.nombre as rol, u.rol_id, u.activo, u.ultimo_login, u.fecha_creacion, u.fecha_inicio, u.fecha_fin
            FROM USUARIOS u 
            INNER JOIN ROLES r ON u.rol_id = r.id 
            WHERE u.email = ? AND u.activo = 1
        """
        
        user = db_manager.execute_query(query, (email.strip(),), fetch_one=True)
        
        if not user or not auth_manager.verify_password(password.strip(), user.password_hash):
            return None
        
        # Actualizar último login
        update_query = "UPDATE USUARIOS SET ultimo_login = GETDATE() WHERE id = ?"
        db_manager.execute_query(update_query, (user.id,), fetch_all=False)
        
        return {
            "id": user.id,
            "email": user.email.strip(),
            "nombre": user.nombre.strip(),
            "apellido": user.apellido.strip(),
            "rol": user.rol.strip(),
            "rol_id": user.rol_id,
            "activo": user.activo,
            "ultimo_login": user.ultimo_login,
            "fecha_creacion": user.fecha_creacion,
            "fecha_inicio": user.fecha_inicio,
            "fecha_fin": user.fecha_fin
        }
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        """Obtiene un usuario por ID"""
        query = """
            SELECT u.id, u.email, u.nombre, u.apellido, u.nif, u.telefono, u.telefono2,
                   r.nombre as rol, u.rol_id, u.activo, u.ultimo_login, u.fecha_creacion, u.fecha_inicio, u.fecha_fin
            FROM USUARIOS u 
            INNER JOIN ROLES r ON u.rol_id = r.id 
            WHERE u.id = ?
        """
        
        user = db_manager.execute_query(query, (user_id,), fetch_one=True)
        
        if not user:
            return None
        
        return {
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "nif": user.nif,
            "telefono": user.telefono,
            "telefono2": user.telefono2,
            "rol": user.rol,
            "rol_id": user.rol_id,
            "activo": user.activo,
            "ultimo_login": user.ultimo_login,
            "fecha_creacion": user.fecha_creacion,
            "fecha_inicio": user.fecha_inicio,
            "fecha_fin": user.fecha_fin
        }

    @staticmethod
    def get_all_users() -> List[Dict]:
        """Obtiene todos los usuarios"""
        query = """
            SELECT u.id, u.email, u.nombre, u.apellido, u.nif, u.telefono, u.telefono2,
                   r.nombre as rol, u.rol_id, r.codemresa as servicer, u.idcliente as sociedad, u.activo, u.ultimo_login, u.fecha_creacion, u.solopropios as 'expediente_propio', u.fecha_inicio, u.fecha_fin
            FROM USUARIOS u 
            INNER JOIN ROLES r ON u.rol_id = r.id 
            ORDER BY u.nombre, u.apellido
        """

        query = """ 
        SELECT 
                u.id, u.email, u.nombre, u.apellido, u.nif, u.telefono, u.telefono2,
                r.nombre AS rol, u.rol_id,

                u.codempresa            AS servicer,
                ec.nomempresa           AS servicer_nombre,   
                u.idcliente             AS sociedad,
                c.nomcli                AS sociedad_nombre,   

                u.activo, u.ultimo_login, u.fecha_creacion,
                u.solopropios           AS expediente_propio,
                u.fecha_inicio,
                u.fecha_fin
            FROM USUARIOS u
            INNER JOIN ROLES r
                ON u.rol_id = r.id
            LEFT JOIN empresas_clientes ec
                ON ec.codempresa = u.codempresa
            LEFT JOIN erp_clientes c
                ON c.idcliente = u.idcliente
            ORDER BY u.nombre, u.apellido;

        """
        
        users = db_manager.execute_query(query)
        result = []
        
        for user in users:
            result.append({
                "id": user.id,
                "email": user.email,
                "nombre": user.nombre,
                "apellido": user.apellido,
                "nif": user.nif,
                "telefono": user.telefono,
                "telefono2": user.telefono2,
                "rol": user.rol,
                "rol_id": user.rol_id,
                "servicer": user.servicer,
                "servicer_nombre": user.servicer_nombre,
                "sociedad": user.sociedad,
                "sociedad_nombre": user.sociedad_nombre,
                "expediente_propio": user.expediente_propio,
                "activo": user.activo,
                "ultimo_login": user.ultimo_login,
                "fecha_creacion": user.fecha_creacion,
                "fecha_inicio": user.fecha_inicio,
                "fecha_fin": user.fecha_fin
            })
        
        return result

class DashboardService:
    @staticmethod
    def get_dashboard_stats() -> Dict:
        """Obtiene estadísticas del dashboard"""
        stats = {}
        
        # Total usuarios activos
        query = "SELECT COUNT(*) FROM USUARIOS WHERE activo = 1"
        result = db_manager.execute_query(query, fetch_one=True)
        stats['total_usuarios'] = result[0]
        
        # Total empresas activas
        query = "SELECT COUNT(*) FROM EMPRESAS WHERE activo = 1"
        result = db_manager.execute_query(query, fetch_one=True)
        stats['total_empresas'] = result[0]
        
        # Total operaciones
        query = "SELECT COUNT(*) FROM OPERACIONES"
        result = db_manager.execute_query(query, fetch_one=True)
        stats['total_operaciones'] = result[0]
        
        # Operaciones pendientes
        query = "SELECT COUNT(*) FROM OPERACIONES WHERE estado = 'PENDIENTE'"
        result = db_manager.execute_query(query, fetch_one=True)
        stats['operaciones_pendientes'] = result[0]
        
        # Ingresos del mes (ventas)
        query = """
            SELECT ISNULL(SUM(monto), 0) 
            FROM OPERACIONES 
            WHERE tipo_operacion = 'VENTA' 
            AND MONTH(fecha_operacion) = MONTH(GETDATE()) 
            AND YEAR(fecha_operacion) = YEAR(GETDATE())
            AND estado = 'COMPLETADA'
        """
        result = db_manager.execute_query(query, fetch_one=True)
        stats['ingresos_mes'] = float(result[0])
        
        # Gastos del mes (compras)
        query = """
            SELECT ISNULL(SUM(monto), 0) 
            FROM OPERACIONES 
            WHERE tipo_operacion = 'COMPRA' 
            AND MONTH(fecha_operacion) = MONTH(GETDATE()) 
            AND YEAR(fecha_operacion) = YEAR(GETDATE())
            AND estado = 'COMPLETADA'
        """
        result = db_manager.execute_query(query, fetch_one=True)
        stats['gastos_mes'] = float(result[0])
        
        # Operaciones recientes
        query = """
            SELECT TOP 5 o.id, e.nombre, o.tipo_operacion, o.monto, o.estado, o.fecha_operacion,
                   u.nombre + ' ' + u.apellido as usuario
            FROM OPERACIONES o
            INNER JOIN EMPRESAS e ON o.empresa_id = e.id
            INNER JOIN USUARIOS u ON o.usuario_id = u.id
            ORDER BY o.fecha_operacion DESC
        """
        operaciones = db_manager.execute_query(query)
        stats['operaciones_recientes'] = []
        for op in operaciones:
            stats['operaciones_recientes'].append({
                "id": op.id,
                "empresa": op.nombre,
                "tipo": op.tipo_operacion,
                "monto": float(op.monto),
                "estado": op.estado,
                "fecha": op.fecha_operacion.isoformat(),
                "usuario": op.usuario
            })
        
        # Empresas más activas
        query = """
            SELECT TOP 5 e.nombre, COUNT(o.id) as total_operaciones,
                   SUM(CASE WHEN o.tipo_operacion = 'VENTA' THEN o.monto ELSE 0 END) as ventas
            FROM EMPRESAS e
            LEFT JOIN OPERACIONES o ON e.id = o.empresa_id
            WHERE e.activo = 1
            GROUP BY e.id, e.nombre
            ORDER BY total_operaciones DESC
        """
        empresas = db_manager.execute_query(query)
        stats['empresas_activas'] = []
        for emp in empresas:
            stats['empresas_activas'].append({
                "nombre": emp.nombre,
                "operaciones": emp.total_operaciones or 0,
                "ventas": float(emp.ventas or 0)
            })
        
        return stats
    
    @staticmethod
    def get_chart_data() -> Dict:
        """Obtiene datos para gráficos"""
        # Datos de operaciones por mes (últimos 6 meses)
        query = """
            SELECT 
                FORMAT(fecha_operacion, 'yyyy-MM') as mes,
                tipo_operacion,
                SUM(monto) as total
            FROM OPERACIONES
            WHERE fecha_operacion >= DATEADD(month, -6, GETDATE())
            AND estado = 'COMPLETADA'
            GROUP BY FORMAT(fecha_operacion, 'yyyy-MM'), tipo_operacion
            ORDER BY mes
        """
        
        data = db_manager.execute_query(query)
        
        # Procesar datos para el gráfico
        chart_data = {
            "labels": [],
            "ventas": [],
            "compras": []
        }
        
        months = {}
        for row in data:
            mes = row.mes
            if mes not in months:
                months[mes] = {"VENTA": 0, "COMPRA": 0}
            months[mes][row.tipo_operacion] = float(row.total)
        
        for mes in sorted(months.keys()):
            chart_data["labels"].append(mes)
            chart_data["ventas"].append(months[mes]["VENTA"])
            chart_data["compras"].append(months[mes]["COMPRA"])
        
        return chart_data

class OperacionService:
    @staticmethod
    def get_all_operaciones() -> List[Dict]:
        """Obtiene todas las operaciones"""
        query = """
            SELECT o.id, o.empresa_id, e.nombre as empresa_nombre, 
                   o.usuario_id, u.nombre + ' ' + u.apellido as usuario_nombre,
                   o.tipo_operacion, o.monto, o.estado, o.descripcion, o.fecha_operacion
            FROM OPERACIONES o
            INNER JOIN EMPRESAS e ON o.empresa_id = e.id
            INNER JOIN USUARIOS u ON o.usuario_id = u.id
            ORDER BY o.fecha_operacion DESC
        """
        
        operaciones = db_manager.execute_query(query)
        result = []
        
        for op in operaciones:
            result.append({
                "id": op.id,
                "empresa_id": op.empresa_id,
                "empresa_nombre": op.empresa_nombre,
                "usuario_id": op.usuario_id,
                "usuario_nombre": op.usuario_nombre,
                "tipo_operacion": op.tipo_operacion,
                "monto": float(op.monto),
                "estado": op.estado,
                "descripcion": op.descripcion,
                "fecha_operacion": op.fecha_operacion
            })
        
        return result

    @staticmethod
    def get_planner_operaciones(filters: Optional[Dict] = None) -> List[Dict]:
        """Obtiene operaciones del planner con filtros"""
        base_query = """
            SELECT DISTINCT 
                PLANNER_TAREAS.IDTAREA,
                PLANNER_TAREAS.FECHA_PREVISTA,
                PLANNER_TAREAS.TITULO,
                PLANNER_TAREAS.DESCRIPCION,
                PLANNER_TAREAS.FECHA_REALIZACION,
                PLANNER_TAREAS.REFERENCIA,
                PLANNER_TAREAS.EXT_ANALISTAPBC,
                PLANNER_TAREAS.EXT_URGENTE,
                PLANNER_TAREAS.ESTADO,
                PLANNER_TAREAS.IDPROCESO,
                PLANNER_TAREAS.IDCLIENTE,
                PLANNER_TAREAS.CODEMPRESA,
                PLANNER_PROCESOS.DESCRIPCION AS PROCESO,
                ERP_CLIENTES.NOMCLI AS CLIENTE,
                EMPRESAS_CLIENTES.NOMEMPRESA AS SERVICER,
                USUARIOS.NOMBRE AS ANALISTA_NOMBRE,
                TAREAS_LOG.FECHA AS FECHA_ULTIMO_CAMBIO
            FROM PLANNER_TAREAS 
                INNER JOIN PLANNER_PROCESOS ON PLANNER_TAREAS.IDPROCESO = PLANNER_PROCESOS.IDPROCESO
                LEFT JOIN ERP_CLIENTES ON PLANNER_TAREAS.IDCLIENTE = ERP_CLIENTES.IDCLIENTE
                LEFT JOIN EMPRESAS_CLIENTES ON PLANNER_TAREAS.CODEMPRESA = EMPRESAS_CLIENTES.CODEMPRESA
                LEFT JOIN USUARIOS ON PLANNER_TAREAS.EXT_ANALISTAPBC = USUARIOS.ID
                LEFT JOIN (
                    SELECT IDTAREA, MAX(FECHA) AS FECHA
                    FROM TAREAS_LOG 
                    GROUP BY IDTAREA
                ) TAREAS_LOG ON PLANNER_TAREAS.IDTAREA = TAREAS_LOG.IDTAREA
        """
        
        where_conditions = []
        params = []
        
        if filters:
            if filters.get('estado'):
                where_conditions.append("PLANNER_TAREAS.ESTADO = ?")
                params.append(filters['estado'])
            
            if filters.get('referencia_expediente'):
                where_conditions.append("PLANNER_TAREAS.REFERENCIA LIKE ?")
                params.append(f"%{filters['referencia_expediente']}%")
            
            if filters.get('analista'):
                where_conditions.append("PLANNER_TAREAS.EXT_ANALISTAPBC = ?")
                params.append(filters['analista'])
            
            if filters.get('sin_analista'):
                where_conditions.append("(PLANNER_TAREAS.EXT_ANALISTAPBC IS NULL OR PLANNER_TAREAS.EXT_ANALISTAPBC = '')")
            
            if filters.get('search'):
                # search_term = f"%{filters['search']}%"
                # search_conditions = [
                #     "PLANNER_TAREAS.TITULO LIKE ?",
                #     "PLANNER_TAREAS.DESCRIPCION LIKE ?",
                #     "PLANNER_TAREAS.REFERENCIA LIKE ?",
                #     "ERP_CLIENTES.NOMCLI LIKE ?",
                #     "PLANNER_TAREAS.ESTADO LIKE ?",
                #     "PLANNER_PROCESOS.TITULO LIKE ?",
                #     "EMPRESAS.NOMEMPRESA LIKE ?",
                #     "USUARIOS.NOMBRE LIKE ?"
                # ]
                # where_conditions.append(f"({' OR '.join(search_conditions)})")
                # params.extend([search_term] * len(search_conditions))
                # normaliza en Python: quita espacios y pasa a minúsculas
                term = f"%{filters['search'].strip().lower()}%"

                #print("Search term normalized:", term)

                cols = [
                    "PLANNER_TAREAS.TITULO",
                    "PLANNER_TAREAS.DESCRIPCION",
                    "PLANNER_TAREAS.REFERENCIA",
                    "ERP_CLIENTES.NOMCLI",
                    "PLANNER_TAREAS.ESTADO",
                    "PLANNER_PROCESOS.TITULO",
                    "EMPRESAS_CLIENTES.NOMEMPRESA",
                    "USUARIOS.NOMBRE"
                ]

                # SQL Server: trim + lower en la columna y LIKE con el término normalizado
                search_conditions = [f"LOWER(LTRIM(RTRIM({c}))) LIKE ?" for c in cols]
                where_conditions.append("(" + " OR ".join(search_conditions) + ")")
                params.extend([term] * len(cols))
        
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        base_query += " ORDER BY PLANNER_TAREAS.FECHA_PREVISTA DESC"

        try:
            operaciones = db_manager.execute_query(base_query, params if params else None)
            result = []
            
            for op in operaciones:
                analista_pbc = getattr(op, 'EXT_ANALISTAPBC', None)
                if analista_pbc is not None and str(analista_pbc).strip():
                    try:
                        analista_pbc = int(analista_pbc)
                    except (ValueError, TypeError):
                        analista_pbc = None
                else:
                    analista_pbc = None
                
                urgente = getattr(op, 'EXT_URGENTE', False)
                if urgente is not None:
                    urgente = bool(urgente)
                else:
                    urgente = False
                
                result.append({
                    "id": getattr(op, 'IDTAREA', None),
                    "fecha_prevista_firma": getattr(op, 'FECHA_PREVISTA', None),
                    "servicer": getattr(op, 'SERVICER', None),
                    "fecha_util_cambio": getattr(op, 'FECHA_ULTIMO_CAMBIO', None),
                    "tipo_operacion": getattr(op, 'PROCESO', None),
                    "referencia_expediente": getattr(op, 'REFERENCIA', None),
                    "sociedad": getattr(op, 'CLIENTE', None),
                    "estado": getattr(op, 'ESTADO', None),
                    "analista_pbc": analista_pbc,
                    "analista_pbc_nombre": getattr(op, 'ANALISTA_NOMBRE', None),
                    "urgente": urgente,
                    "proceso": getattr(op, 'PROCESO', None),
                    "cliente": getattr(op, 'CLIENTE', None),
                    "idproceso": getattr(op, 'IDPROCESO', None),
                    "idcliente": getattr(op, 'IDCLIENTE', None),
                    "titulo": getattr(op, 'TITULO', None),
                    "descripcion": getattr(op, 'DESCRIPCION', None)
                })
            
            return result
        except Exception as e:
            return [
            ]

class EmpresaService:
    @staticmethod
    def get_all_empresas() -> List[Dict]:
        """Obtiene todas las empresas activas"""
        query = """
            SELECT id, NOMEMPRESA AS nombre, codempresa, RUTAEMPRESA AS rut, direccion, tlf as telefono, email, activo, fecha_creacion
            FROM EMPRESAS_CLIENTES 
            ORDER BY nombre
        """
        
        empresas = db_manager.execute_query(query)
        result = []
        
        for emp in empresas:
            result.append({
                "id": emp.id,
                "nombre": emp.nombre,
                "codigo": emp.codempresa,
                "rut": emp.rut,
                "direccion": emp.direccion,
                "telefono": emp.telefono,
                "email": emp.email,
                "activo": emp.activo,
                "fecha_creacion": emp.fecha_creacion
            })
        
        #print("Empresas obtenidas:", result)

        return result
    
    @staticmethod
    def get_empresas_clientes() -> List[Dict]:
        """Obtiene las empresas clientes para el selector"""
        query = """
            SELECT EMPRESAS_CLIENTES.CODEMPRESA, EMPRESAS_CLIENTES.NOMEMPRESA
            FROM EMPRESAS_CLIENTES
            ORDER BY EMPRESAS_CLIENTES.NOMEMPRESA
        """
        
        empresas = db_manager.execute_query(query)
        result = []
        
        for emp in empresas:
            result.append({
                "codempresa": emp.CODEMPRESA,
                "nomempresa": emp.NOMEMPRESA
            })       
        
        return result

class SociedadService:
    @staticmethod
    def get_all_sociedades() -> List[Dict]:
        """Obtiene todas las sociedades con información relacionada"""
        query = """
            SELECT 
                c.IDCLIENTE, c.CODCLI, c.CUENTA, c.NIFCLI, c.RAZON, c.NOMCLI,
                c.DTOCLI, c.DIRCLI, c.CODPROVI, c.POBCLI, c.TELCLI, c.E_MAIL,
                c.CODPAIS, c.CONTACTO, c.IDREPRESEN, c.EXT_CARTERA, 
                c.EXT_ANALISTAPORDEFECTO, c.EXT_ACTIVIDAD, c.EXT_ESTADO, 
                c.EXT_SPV, c.OBSERVACIONES,
                r.DESCRIPCION as representante_nombre,
                u.nombre + ' ' + u.apellido as analista_nombre
            FROM ERP_CLIENTES c
            LEFT JOIN ERP_REPRESEN r ON c.IDREPRESEN = r.IDREPRESEN
            LEFT JOIN USUARIOS u ON c.EXT_ANALISTAPORDEFECTO = u.id
            ORDER BY c.NOMCLI
        """
        
        sociedades = db_manager.execute_query(query)
        result = []
        
        for soc in sociedades:
            result.append({
                "idcliente": soc.IDCLIENTE,
                "codcli": soc.CODCLI,
                "cuenta": soc.CUENTA,
                "nifcli": soc.NIFCLI,
                "razon": soc.RAZON,
                "nomcli": soc.NOMCLI,
                "dtocli": soc.DTOCLI,
                "dircli": soc.DIRCLI,
                "codprovi": soc.CODPROVI,
                "pobcli": soc.POBCLI,
                "telcli": soc.TELCLI,
                "e_mail": soc.E_MAIL,
                "codpais": soc.CODPAIS,
                "contacto": soc.CONTACTO,
                "idrepresen": soc.IDREPRESEN,
                "representante_nombre": soc.representante_nombre,
                "ext_cartera": soc.EXT_CARTERA,
                "ext_analistapordefecto": soc.EXT_ANALISTAPORDEFECTO,
                "analista_nombre": soc.analista_nombre,
                "ext_actividad": soc.EXT_ACTIVIDAD,
                "ext_estado": soc.EXT_ESTADO,
                "ext_spv": bool(soc.EXT_SPV),
                "observaciones": soc.OBSERVACIONES
            })

        return result

    @staticmethod
    def get_sociedad_by_id(sociedad_id: int) -> Optional[Dict]:
        """Obtiene una sociedad por ID"""
        query = """
            SELECT 
                c.IDCLIENTE, c.CODCLI, c.CUENTA, c.NIFCLI, c.RAZON, c.NOMCLI,
                c.DTOCLI, c.DIRCLI, c.CODPROVI, c.POBCLI, c.TELCLI, c.E_MAIL,
                c.CODPAIS, c.CONTACTO, c.IDREPRESEN, c.EXT_CARTERA, 
                c.EXT_ANALISTAPORDEFECTO, c.EXT_ACTIVIDAD, c.EXT_ESTADO, 
                c.EXT_SPV, c.OBSERVACIONES,
                r.DESCRIPCION as representante_nombre,
                u.nombre + ' ' + u.apellido as analista_nombre
            FROM ERP_CLIENTES c
            LEFT JOIN ERP_REPRESEN r ON c.IDREPRESEN = r.IDREPRESEN
            LEFT JOIN USUARIOS u ON c.EXT_ANALISTAPORDEFECTO = u.id
            WHERE c.IDCLIENTE = ?
        """
        
        soc = db_manager.execute_query(query, (sociedad_id,), fetch_one=True)
        
        if not soc:
            return None
        
        return {
            "idcliente": soc.IDCLIENTE,
            "codcli": soc.CODCLI,
            "cuenta": soc.CUENTA,
            "nifcli": soc.NIFCLI,
            "razon": soc.RAZON,
            "nomcli": soc.NOMCLI,
            "dtocli": soc.DTOCLI,
            "dircli": soc.DIRCLI,
            "codprovi": soc.CODPROVI,
            "pobcli": soc.POBCLI,
            "telcli": soc.TELCLI,
            "e_mail": soc.E_MAIL,
            "codpais": soc.CODPAIS,
            "contacto": soc.CONTACTO,
            "idrepresen": soc.IDREPRESEN,
            "representante_nombre": soc.representante_nombre,
            "ext_cartera": soc.EXT_CARTERA,
            "ext_analistapordefecto": soc.EXT_ANALISTAPORDEFECTO,
            "analista_nombre": soc.analista_nombre,
            "ext_actividad": soc.EXT_ACTIVIDAD,
            "ext_estado": soc.EXT_ESTADO,
            "ext_spv": bool(soc.EXT_SPV),
            "observaciones": soc.OBSERVACIONES
        }

    @staticmethod
    def get_all_representantes() -> List[Dict]:
        """Obtiene todos los representantes"""
        query = """
            SELECT IDREPRESEN, DESCRIPCION
            FROM ERP_REPRESEN
            ORDER BY DESCRIPCION
        """
        
        representantes = db_manager.execute_query(query)
        result = []
        
        for rep in representantes:
            result.append({
                "idrepresen": rep.IDREPRESEN,
                "descripcion": rep.DESCRIPCION
            })
        
        return result
    
    @staticmethod
    def create_representante(descripcion: str) -> int:
        """Crea un nuevo representante (fondo)"""

        print("Creating representante with description:", descripcion)

        desc_norm = (descripcion or "").strip()
        if not desc_norm:
            raise ValueError("La descripción no puede estar vacía")
        
        # 1) ¿Ya existe?
        exists_query = """
            SELECT TOP 1 IDREPRESEN AS id
            FROM dbo.ERP_REPRESEN
            WHERE UPPER(LTRIM(RTRIM(DESCRIPCION))) = UPPER(LTRIM(RTRIM(?)))
        """
        row = db_manager.execute_query(exists_query, (desc_norm,), fetch_one=True)

        if row:
            # Ya existe: devuelve el id existente
            raise ValueError("El fondo ya existe")

    # 2) No existe: insertar y devolver nuevo id
    
        query = """
            SET NOCOUNT ON;
            INSERT INTO ERP_REPRESEN (DESCRIPCION)
            VALUES (?);
            SELECT CAST(SCOPE_IDENTITY() AS INT) as id;
        """
        
        result = db_manager.execute_query(query, (descripcion,), fetch_one=True)

        print("Created representante with ID:", result[0])

        return int(result[0])
    
    @staticmethod
    def update_representante(idrepresen: int, descripcion: str) -> None:
        """Actualiza un representante (fondo)"""
        query = """
            UPDATE ERP_REPRESEN
            SET DESCRIPCION = ?
            WHERE IDREPRESEN = ?
        """
        
        db_manager.execute_query(query, (descripcion, idrepresen))
    
    @staticmethod
    def delete_representante(idrepresen: int) -> bool:
        """Elimina un representante si no está asignado a ninguna sociedad"""
        # Check if assigned to any sociedad
        check_query = """
            SELECT COUNT(*) as count
            FROM ERP_CLIENTES
            WHERE IDREPRESEN = ?
        """
        
        result = db_manager.execute_query(check_query, (idrepresen,), fetch_one=True)
        
        if result.count > 0:
            return False
        
        # Delete the representante
        delete_query = """
            DELETE FROM ERP_REPRESEN
            WHERE IDREPRESEN = ?
        """
        db_manager.execute_query(delete_query, (idrepresen,))
        
        return True
    
    
class RoleService:
    @staticmethod
    def get_all_roles() -> List[Dict]:
        """Obtiene todos los roles activos de la base de datos"""
        query = """
            SELECT ID, NOMBRE, DESCRIPCION, ACTIVO, FECHA_CREACION
            FROM ROLES
            WHERE ACTIVO = 1
            ORDER BY NOMBRE
        """
        
        roles = db_manager.execute_query(query)
        result = []
        
        for role in roles:
            result.append({
                "id": role.ID,
                "nombre": role.NOMBRE,
                "descripcion": role.DESCRIPCION,
                "activo": bool(role.ACTIVO),
                "fecha_creacion": role.FECHA_CREACION
            })
        

        print("Roles fetched:", result)
        return result


class AuditorSociedadService:
    @staticmethod
    def get_sociedades_for_table() -> List[Dict]:
        """Obtiene todas las sociedades con información para la tabla de asignación"""
        query = """
            SELECT 
                C.IDCLIENTE, 
                C.NOMCLI, 
                C.EXT_CARTERA AS CARTERA, 
                R.DESCRIPCION AS FONDO
            FROM ERP_CLIENTES C
            LEFT JOIN ERP_REPRESEN R ON R.IDREPRESEN = C.IDREPRESEN
            ORDER BY C.NOMCLI
        """
        
        sociedades = db_manager.execute_query(query)
        result = []
        
        for soc in sociedades:
            result.append({
                "idcliente": soc.IDCLIENTE,
                "nomcli": soc.NOMCLI,
                "ext_cartera": soc.CARTERA,
                "representante_nombre": soc.FONDO
            })
        
        return result
    
    @staticmethod
    def get_auditor_sociedades(usuario_id: int) -> List[int]:
        """Obtiene los IDs de sociedades asignadas a un auditor"""
        query = """
            SELECT IDCLIENTE
            FROM AUDITORES_SOCIEDADES
            WHERE IDUSUARIO = ?
        """
        
        sociedades = db_manager.execute_query(query, (usuario_id,))
        return [soc.IDCLIENTE for soc in sociedades]
    
    @staticmethod
    def update_auditor_sociedades(usuario_id: int, sociedades_ids: List[int]) -> None:
        """Actualiza las sociedades asignadas a un auditor"""
        # First, delete all existing assignments
        delete_query = "DELETE FROM AUDITORES_SOCIEDADES WHERE IDUSUARIO = ?"
        db_manager.execute_query(delete_query, (usuario_id,))
        
        # Then, insert new assignments
        if sociedades_ids:
            insert_query = "INSERT INTO AUDITORES_SOCIEDADES (IDUSUARIO, IDCLIENTE) VALUES (?, ?)"
            for idcliente in sociedades_ids:
                db_manager.execute_query(insert_query, (usuario_id, idcliente))

class AuditorOperacionService:
    @staticmethod
    def get_operaciones_for_table() -> List[Dict]:
        """Obtiene todas las operaciones con información para la tabla de asignación"""
        query = """
            WITH TareasConRank AS (
                    SELECT
                        IDTAREA,
                        IDHITO,
                        FECHA AS FECHALOG,
                        IDACCION,
                        ACCION,
                        ROW_NUMBER() OVER (PARTITION BY IDTAREA ORDER BY FECHA DESC) AS rn
                    FROM
                        TAREAS_LOG
                ),
                Filtradas AS (
                    SELECT
                        IDTAREA,
                        FECHALOG,
                        ACCION
                    FROM
                        TareasConRank
                    WHERE
                        rn = 1
                        AND (IDACCION = 47 OR IDACCION = 50)
                        --AND ACCION = 'Aprobado PBC'
                )
                SELECT DISTINCT 
                    PLANNER_TAREAS.*, 
                    PLANNER_PROCESOS.TITULO AS PROCESO, 
                    ERP_CLIENTES.NOMCLI AS NOMCLIENTE,
                    USUARIOS.NOMBRE AS ANALISTA,
                    ERP_CLIENTES.EXT_ANALISTAPORDEFECTO AS IDANALISTA,
                    Filtradas.FECHALOG,
                    Filtradas.ACCION,
                    E.NOMEMPRESA,
                    USUARIOS.NOMBRE AS NOMANALISTA
                FROM 
                    PLANNER_TAREAS
                INNER JOIN 
                    PLANNER_PROCESOS ON PLANNER_TAREAS.IDPROCESO = PLANNER_PROCESOS.IDPROCESO
                LEFT JOIN 
                    EMPRESAS_CLIENTES E ON E.CODEMPRESA = PLANNER_TAREAS.CODEMPRESA
                LEFT JOIN 
                    ERP_CLIENTES ON PLANNER_TAREAS.IDCLIENTE = ERP_CLIENTES.IDCLIENTE
                LEFT JOIN 
                    Filtradas ON PLANNER_TAREAS.IDTAREA = Filtradas.IDTAREA
                LEFT JOIN 
                    USUARIOS ON ERP_CLIENTES.EXT_ANALISTAPORDEFECTO = USUARIOS.ID
                WHERE 1 = 1 
                AND (PLANNER_TAREAS.IDESTADO = 47 OR PLANNER_TAREAS.IDESTADO = 50)
        """
        
        operaciones = db_manager.execute_query(query)
        result = []
        
        for op in operaciones:
            result.append({
                "idtarea": op.IDTAREA,
                "idcliente": op.IDCLIENTE,
                "nomcli": op.NOMCLIENTE,
                "fechaultimocambio": op.FECHALOG,
                "fechaprevista": op.FECHA_PREVISTA,
                "referencia": op.REFERENCIA,
                "estado": op.ESTADO,
                "idanalista": op.IDANALISTA,
                "nomanalista": op.NOMANALISTA,
                "nomempresa": op.NOMEMPRESA,
            })

    #         idtarea: int
    # idcliente: Optional[int] = None
    # nomcli: Optional[str] = None
    # fechaultimocambio: Optional[datetime] = None
    # fechaprevista: Optional[datetime] = None
    # referencia: Optional[str] = None
    # estado: Optional[str] = None
    # idanalista: Optional[int] = None
    # nomanalista: Optional[str] = None

        #print("Operaciones fetched for auditor assignment:", result)
        
        return result
    
    @staticmethod
    def get_auditor_operaciones(usuario_id: int) -> List[int]:
        """Obtiene los IDs de operaciones asignadas a un auditor"""
        query = """
            SELECT IDTAREA
            FROM AUDITORES_TAREAS
            WHERE IDUSUARIO = ?
        """
        print("Fetching auditor operaciones for user ID:", usuario_id)
        operaciones = db_manager.execute_query(query, (usuario_id,))
        return [op.IDTAREA for op in operaciones]

    @staticmethod
    def update_auditor_operaciones(usuario_id: int, operaciones_ids: List[int]) -> None:
        """Actualiza las operaciones asignadas a un auditor"""
        # First, delete all existing assignments
        delete_query = "DELETE FROM AUDITORES_TAREAS WHERE IDUSUARIO = ?"
        db_manager.execute_query(delete_query, (usuario_id,))
        
        # Then, insert new assignments
        if operaciones_ids:
            insert_query = "INSERT INTO AUDITORES_TAREAS (IDUSUARIO, IDTAREA) VALUES (?, ?)"
            for idtarea in operaciones_ids:
                db_manager.execute_query(insert_query, (usuario_id, idtarea))


class EstructuraCarpetaService:
    @staticmethod
    def get_all_modulos() -> List[Dict]:
        """Obtiene todos los módulos con su estructura raíz asignada"""
        query = """
            SELECT 
                M.IDMODULO,
                M.DESCRIPCION,
                MEC.IDESTRUCTURACARPETA as estructura_raiz_id,
                EC.NOMBRE as estructura_raiz_nombre
            FROM MODULOS M
            LEFT JOIN MODULO_ESTRUCTURA_CARPETAS MEC ON M.IDMODULO = MEC.IDMODULO
            LEFT JOIN ESTRUCTURA_CARPETAS EC ON MEC.IDESTRUCTURACARPETA = EC.IDCARPETA
            ORDER BY M.DESCRIPCION
        """
        
        modulos = db_manager.execute_query(query)
        result = []
        
        for mod in modulos:
            result.append({
                "idmodulo": mod.IDMODULO,
                "descripcion": mod.DESCRIPCION,
                "estructura_raiz_id": mod.estructura_raiz_id,
                "estructura_raiz_nombre": mod.estructura_raiz_nombre
            })
        
        return result
    
    @staticmethod
    def get_estructuras_raiz() -> List[Dict]:
        """Obtiene todas las estructuras raíz (sin padre)"""
        query = """
            SELECT 
                EC.IDCARPETA,
                EC.NOMBRE,
                EC.ACTIVA,
                EC.ARCHIVO,
                EC.IDCARPETAPADRE,
                M.IDMODULO as modulo_id,
                M.DESCRIPCION as modulo_nombre
            FROM ESTRUCTURA_CARPETAS EC
            LEFT JOIN MODULO_ESTRUCTURA_CARPETAS MEC ON EC.IDCARPETA = MEC.IDESTRUCTURACARPETA
            LEFT JOIN MODULOS M ON MEC.IDMODULO = M.IDMODULO
            WHERE EC.IDCARPETAPADRE IS NULL AND EC.ARCHIVO = 0
            ORDER BY EC.NOMBRE
        """

        query = """
            SELECT 
                EC.IDCARPETA,
                EC.NOMBRE,
                EC.ACTIVA,
                EC.ARCHIVO,
                EC.IDCARPETAPADRE
            FROM ESTRUCTURA_CARPETAS EC
            WHERE EC.IDCARPETAPADRE IS NULL AND EC.ARCHIVO = 0
            ORDER BY EC.NOMBRE
        """
        
        estructuras = db_manager.execute_query(query)
        result = []
        
        for est in estructuras:
            result.append({
                "idcarpeta": est.IDCARPETA,
                "nombre": est.NOMBRE,
                "activa": bool(est.ACTIVA),
                "archivo": bool(est.ARCHIVO),
                "idcarpetapadre": est.IDCARPETAPADRE
                # ,"modulo_id": est.modulo_id,
                # "modulo_nombre": est.modulo_nombre
            })
        
        return result
    
    @staticmethod
    def get_estructura_tree2(idestructura: int) -> Dict:
        """Obtiene el árbol completo de una estructura"""

        query = """
            SELECT 
                IDCARPETA,
                IDCARPETAPADRE,
                NOMBRE,
                ARCHIVO,
                ACTIVA,
                ARCHIVO_URL,
                ARCHIVO_SIZE
            FROM ESTRUCTURA_CARPETAS
            WHERE IDCARPETA = ? OR IDCARPETAPADRE = ? OR IDCARPETA IN (
                SELECT IDCARPETA FROM ESTRUCTURA_CARPETAS WHERE IDCARPETAPADRE = ?
            )
            ORDER BY ARCHIVO, NOMBRE
        """
        
        items = db_manager.execute_query(query, (idestructura, idestructura, idestructura))

        print(f"Items fetched for estructura {idestructura}:", items)
        
        # Build tree structure
        tree = {}
        for item in items:
            tree[item.IDCARPETA] = {
                "idcarpeta": item.IDCARPETA,
                "idcarpetapadre": item.IDCARPETAPADRE,
                "nombre": item.NOMBRE,
                "archivo": bool(item.ARCHIVO),
                "activa": bool(item.ACTIVA),
                "archivo_url": item.ARCHIVO_URL if hasattr(item, 'ARCHIVO_URL') else None,
                "archivo_size": item.ARCHIVO_SIZE if hasattr(item, 'ARCHIVO_SIZE') else None,
                "hijos": []
            }

        print("Tree structure before linking:", tree)
        
        # Link children to parents
        root = None
        for item_id, item in tree.items():
            if item["idcarpetapadre"] is None:
                root = item
            else:
                parent = tree.get(item["idcarpetapadre"])
                if parent:
                    parent["hijos"].append(item)
        
        print('root', root)
        
        return root if root else {}
    
    @staticmethod
    def get_estructura_tree(raiz_id: int) -> dict:
        """
        Devuelve el árbol completo de carpetas/archivos comenzando en `raiz_id`.
        """
        # 1) Trae la raíz y todos sus hijos (y los hijos de sus hijos...)
        query = """
        ;WITH RECURSIVE_CTE AS (
            SELECT 
                IDCARPETA,
                IDCARPETAPADRE,
                NOMBRE,
                ARCHIVO,
                ACTIVA,
                ARCHIVO_URL,
                ARCHIVO_SIZE
            FROM ESTRUCTURA_CARPETAS
            WHERE IDCARPETA = ?

            UNION ALL

            SELECT 
                ec.IDCARPETA,
                ec.IDCARPETAPADRE,
                ec.NOMBRE,
                ec.ARCHIVO,
                ec.ACTIVA,
                ec.ARCHIVO_URL,
                ec.ARCHIVO_SIZE
            FROM ESTRUCTURA_CARPETAS ec
            INNER JOIN RECURSIVE_CTE r
                ON ec.IDCARPETAPADRE = r.IDCARPETA
        )
        SELECT *
        FROM RECURSIVE_CTE
        ORDER BY ARCHIVO, NOMBRE
        OPTION (MAXRECURSION 0);  -- sin límite de niveles
        """

        rows = db_manager.execute_query(query, (raiz_id,), fetch_one=False, fetch_all=True)
        if not rows:
            return {}

        # 2) Crea diccionario de nodos
        nodos = {}
        for r in rows:
            nodos[r.IDCARPETA] = {
                "idcarpeta": r.IDCARPETA,
                "idcarpetapadre": r.IDCARPETAPADRE,
                "nombre": r.NOMBRE,
                "archivo": bool(r.ARCHIVO),
                "activa": bool(r.ACTIVA),
                "archivo_url": getattr(r, "ARCHIVO_URL", None),
                "archivo_size": getattr(r, "ARCHIVO_SIZE", None),
                "hijos": []
            }

        # 3) Enlaza hijos con padres
        raiz = nodos.get(raiz_id)
        for n in nodos.values():
            padre_id = n["idcarpetapadre"]
            if padre_id and padre_id in nodos:
                nodos[padre_id]["hijos"].append(n)

        # 4) (Opcional) Ordena hijos (carpetas primero si ARCHIVO=0, luego por nombre)
        def ordenar_rec(node: dict):
            node["hijos"].sort(key=lambda x: (x["archivo"], x["nombre"]))
            for h in node["hijos"]:
                ordenar_rec(h)

        if raiz:
            ordenar_rec(raiz)
            return raiz
        return {}

    # @staticmethod
    # def create_estructura(nombre: str, activa: bool = True) -> int:
    #     """Crea una nueva estructura raíz"""
    #     query = """
    #         INSERT INTO ESTRUCTURA_CARPETAS (NOMBRE, ARCHIVO, ACTIVA, IDCARPETAPADRE)
    #         VALUES (?, 0, ?, NULL);
    #         SELECT SCOPE_IDENTITY() as id;
    #     """
        
    #     result = db_manager.execute_query(query, (nombre, activa), fetch_one=True)
    #     return int(result.id)

    @staticmethod
    def create_estructura(nombre: str, activa: bool = True) -> int:
        query = """
            INSERT INTO ESTRUCTURA_CARPETAS (NOMBRE, ARCHIVO, ACTIVA, IDCARPETAPADRE)
            OUTPUT INSERTED.IDCARPETA AS id
            VALUES (?, 0, ?, NULL)
        """

        query = """SET NOCOUNT ON;

        INSERT INTO ESTRUCTURA_CARPETAS (NOMBRE, ARCHIVO, ACTIVA, IDCARPETAPADRE)
        VALUES (?, 0, ?, NULL);

        SELECT CAST(SCOPE_IDENTITY() AS INT) AS id;
        """
        row = db_manager.execute_query(query, (nombre, activa), fetch_one=True)
        # pyodbc Row permite acceso por alias ('id') o por índice [0]
        new_id = getattr(row, "id", row[0])
        return int(new_id)

    
    @staticmethod
    def update_estructura(idestructura: int, nombre: str, activa: bool) -> None:
        """Actualiza una estructura"""
        query = """
            UPDATE ESTRUCTURA_CARPETAS
            SET NOMBRE = ?, ACTIVA = ?
            WHERE IDCARPETA = ?
        """
        
        db_manager.execute_query(query, (nombre, activa, idestructura))
    
    @staticmethod
    def delete_estructura(idestructura: int) -> bool:
        """Elimina una estructura si no está asignada a ningún módulo"""
        # Check if assigned to any module
        check_query = """
            SELECT COUNT(*) as count
            FROM MODULO_ESTRUCTURA_CARPETAS
            WHERE IDESTRUCTURACARPETA = ?
        """
        
        result = db_manager.execute_query(check_query, (idestructura,), fetch_one=True)
        
        if result.count > 0:
            return False
        
        # Delete all children first
        delete_children_query = """
            DELETE FROM ESTRUCTURA_CARPETAS
            WHERE IDCARPETAPADRE = ?
        """
        db_manager.execute_query(delete_children_query, (idestructura,))
        
        # Delete the structure
        delete_query = """
            DELETE FROM ESTRUCTURA_CARPETAS
            WHERE IDCARPETA = ?
        """
        db_manager.execute_query(delete_query, (idestructura,))
        
        return True
    
    @staticmethod
    def asignar_modulo_estructura(idmodulo: int, idestructuracarpeta: int) -> None:
        """Asigna una estructura a un módulo"""
        # First, remove any existing assignment for this module
        delete_query = """
            DELETE FROM MODULO_ESTRUCTURA_CARPETAS
            WHERE IDMODULO = ?
        """
        db_manager.execute_query(delete_query, (idmodulo,))
        
        # Insert new assignment
        insert_query = """
            INSERT INTO MODULO_ESTRUCTURA_CARPETAS (IDMODULO, IDESTRUCTURACARPETA)
            VALUES (?, ?)
        """
        db_manager.execute_query(insert_query, (idmodulo, idestructuracarpeta))
    
    @staticmethod
    def desasignar_modulo_estructura(idmodulo: int) -> None:
        """Desasigna la estructura de un módulo"""
        query = """
            DELETE FROM MODULO_ESTRUCTURA_CARPETAS
            WHERE IDMODULO = ?
        """
        db_manager.execute_query(query, (idmodulo,))
    
    @staticmethod
    # def create_carpeta(idestructura: int, idcarpetapadre: Optional[int], nombre: str, archivo: bool = False) -> int:
    #     """Crea una nueva carpeta o archivo en la estructura"""
    #     query = """
    #         INSERT INTO ESTRUCTURA_CARPETAS (NOMBRE, ARCHIVO, ACTIVA, IDCARPETAPADRE)
    #         VALUES (?, ?, 1, ?);
    #         SELECT SCOPE_IDENTITY() as id;
    #     """
        
    #     result = db_manager.execute_query(query, (nombre, archivo, idcarpetapadre), fetch_one=True)
    #     return int(result.id)

    @staticmethod
    def create_carpeta(idestructura: int, idcarpetapadre: Optional[int], nombre: str, archivo: bool = False) -> int:
        
        print(f"Creating carpeta with nombre='{nombre}', archivo={archivo}, idcarpetapadre={idcarpetapadre}")
        
        query = """
         SET NOCOUNT ON;

            INSERT INTO ESTRUCTURA_CARPETAS (NOMBRE, ARCHIVO, ACTIVA, IDCARPETAPADRE)
            OUTPUT INSERTED.IDCARPETA AS id
            VALUES (?, ?, 1, ?);

            SELECT CAST(SCOPE_IDENTITY() AS INT) AS id;
        """

        query = """
         SET NOCOUNT ON;

            INSERT INTO ESTRUCTURA_CARPETAS (NOMBRE, ARCHIVO, ACTIVA, IDCARPETAPADRE)
            VALUES (?, ?, 1, ?);

            SELECT CAST(SCOPE_IDENTITY() AS INT) AS id;
        """
        row = db_manager.execute_query(query, (nombre, archivo, idcarpetapadre), fetch_one=True)
        new_id = getattr(row, "id", row[0]if row else None)

        if not new_id:
            raise RuntimeError("No se pudo obtener el ID generado")
    
        return int(new_id)

    @staticmethod
    def create_file_record(
        idestructura: int,
        idcarpetapadre: Optional[int],
        nombre: str,
        archivo_url: str,
        archivo_size: int,
        archivo_tipo: str
    ) -> int:
        """Crea un registro de archivo con información completa"""
        query = """
            INSERT INTO ESTRUCTURA_CARPETAS (
                NOMBRE, ARCHIVO, ACTIVA, IDCARPETAPADRE,
                ARCHIVO_URL, ARCHIVO_SIZE, ARCHIVO_TIPO, FECHA_SUBIDA
            )
            VALUES (?, 1, 1, ?, ?, ?, ?, GETDATE());
            SELECT SCOPE_IDENTITY() as id;
        """
        
        result = db_manager.execute_query(
            query,
            (nombre, idcarpetapadre, archivo_url, archivo_size, archivo_tipo),
            fetch_one=True
        )
        return int(result)
    
    @staticmethod
    def get_file_info(idcarpeta: int) -> Optional[Dict]:
        """Obtiene información de un archivo"""
        query = """
            SELECT
                IDCARPETA, NOMBRE, ARCHIVO_URL, ARCHIVO_SIZE,
                ARCHIVO_TIPO, FECHA_SUBIDA
            FROM ESTRUCTURA_CARPETAS
            WHERE IDCARPETA = ? AND ARCHIVO = 1
        """
        
        file = db_manager.execute_query(query, (idcarpeta,), fetch_one=True)
        
        if not file:
            return None
        
        return {
            "idcarpeta": file.IDCARPETA,
            "nombre": file.NOMBRE,
            "archivo_url": file.ARCHIVO_URL,
            "archivo_size": file.ARCHIVO_SIZE,
            "archivo_tipo": file.ARCHIVO_TIPO,
            "fecha_subida": file.FECHA_SUBIDA
        }
    
    @staticmethod
    def delete_carpeta(idcarpeta: int) -> None:
        """Elimina una carpeta o archivo"""
        query = """
            DELETE FROM ESTRUCTURA_CARPETAS
            WHERE IDCARPETA = ?
        """
        db_manager.execute_query(query, (idcarpeta,))
    
    @staticmethod
    def get_estructuras_activas() -> List[Dict]:
        """Obtiene solo las estructuras activas para asignación"""
        query = """
            SELECT IDCARPETA, NOMBRE
            FROM ESTRUCTURA_CARPETAS
            WHERE IDCARPETAPADRE IS NULL AND ARCHIVO = 0 AND ACTIVA = 1
            ORDER BY NOMBRE
        """
        
        estructuras = db_manager.execute_query(query)
        result = []
        
        for est in estructuras:
            result.append({
                "idcarpeta": est.IDCARPETA,
                "nombre": est.NOMBRE
            })
        
        return result
    

class CountryService:
    @staticmethod
    def get_all_countries() -> List[Dict]:
        """Obtiene todos los países"""
        query = """
                SELECT COUNTRY_CODE, NAME FROM COUNTRIES ORDER BY NAME
            """
            
        countries = db_manager.execute_query(query)
        result = []
        
        for op in countries:
            result.append({
                "codigo": getattr(op, 'COUNTRY_CODE', None),
                "descripcion": getattr(op, 'NAME', None)
            })
        
        return result
    
    @staticmethod
    def get_subdivisions(codigopais) -> List[Dict]:
        """Obtiene todos los países para un selector"""
        try:
            query = """
                SELECT COUNTRY_CODE, SUBDIVISION_CODE, NAME FROM SUBDIVISIONS
                WHERE COUNTRY_CODE = ?
                ORDER BY NAME
            """
            subdivisions = db_manager.execute_query(query, (codigopais,))
            
            result = []

            for op in subdivisions:
                result.append({
                    "codigopais": getattr(op, 'COUNTRY_CODE', None),
                    "codigosubdivision": getattr(op, 'SUBDIVISION_CODE', None),
                    "descripcion": getattr(op, 'NAME', None)
                })
            
            return result
        except Exception as e:
            return None
        
class TipoRelacionService:
    @staticmethod
    def get_all_tipos_relacion() -> List[Dict]:
        """Obtiene todos los tipos de relación"""
        query = """
            SELECT IDTIPORELACION, DESCRIPCION, ESTRUCTURAJURIDICA
            FROM ERP_CONTACTOS_TIPOSRELACION
            ORDER BY DESCRIPCION
        """
        
        tipos = db_manager.execute_query(query)
        result = []
        
        for tipo in tipos:
            result.append({
                "idtiporelacion": tipo.IDTIPORELACION,
                "descripcion": tipo.DESCRIPCION,
                "estructurajuridica": bool(tipo.ESTRUCTURAJURIDICA)
            })
        
        return result
    
    @staticmethod
    def create_tipo_relacion(descripcion: str, estructurajuridica: bool) -> int:
        """Crea un nuevo tipo de relación"""

        print("Creating representante with description:", descripcion)

        desc_norm = (descripcion or "").strip()
        if not desc_norm:
            raise ValueError("La descripción no puede estar vacía")
        
        # 1) ¿Ya existe?
        exists_query = """
            SELECT TOP 1 IDTIPORELACION AS id
            FROM dbo.ERP_CONTACTOS_TIPOSRELACION
            WHERE UPPER(LTRIM(RTRIM(DESCRIPCION))) = UPPER(LTRIM(RTRIM(?)))
        """
        row = db_manager.execute_query(exists_query, (desc_norm,), fetch_one=True)

        if row:
            # Ya existe: devuelve el id existente
            raise ValueError("Ya existe una relación con esta descripción")

        query = """
            INSERT INTO ERP_CONTACTOS_TIPOSRELACION (DESCRIPCION, ESTRUCTURAJURIDICA, CODEMPRESA)
            VALUES (?, ?, NULL);
            SELECT SCOPE_IDENTITY() as id;
        """
        
        result = db_manager.execute_query(query, (descripcion, estructurajuridica), fetch_one=True)
        return int(result)
    
    @staticmethod
    def update_tipo_relacion(idtiporelacion: int, descripcion: str, estructurajuridica: bool) -> None:
        """Actualiza un tipo de relación"""
        query = """
            UPDATE ERP_CONTACTOS_TIPOSRELACION
            SET DESCRIPCION = ?, ESTRUCTURAJURIDICA = ?
            WHERE IDTIPORELACION = ?
        """
        
        db_manager.execute_query(query, (descripcion, estructurajuridica, idtiporelacion))
    
    @staticmethod
    def delete_tipo_relacion(idtiporelacion: int) -> bool:
        """Elimina un tipo de relación si no está en uso"""
        # Check if in use (you may need to adjust this based on your schema)
        
        # check_query = """
        #     SELECT COUNT(*) as count
        #     FROM ERP_CONTACTOS_TIPOSRELACION
        #     WHERE IDTIPORELACION = ?
        # """
        
        # result = db_manager.execute_query(check_query, (idtiporelacion,), fetch_one=True)
        
        # if result.count > 0:
        #     return False
        
        # Delete the tipo relacion
        delete_query = """
            DELETE FROM ERP_CONTACTOS_TIPOSRELACION
            WHERE IDTIPORELACION = ?
        """
        db_manager.execute_query(delete_query, (idtiporelacion,))
        
        return True
    
class TipoAlertaService:
    @staticmethod
    def get_all_tipos_alerta() -> List[Dict]:
        """Obtiene todos los tipos de alerta"""
        query = """
            SELECT IDTIPOALERTA, DESCRIPCION
            FROM TIPOS_ALERTAS
            ORDER BY DESCRIPCION
        """
        
        tipos = db_manager.execute_query(query)
        result = []
        
        for tipo in tipos:
            result.append({
                "idtipoalerta": tipo.IDTIPOALERTA,
                "descripcion": tipo.DESCRIPCION
            })
        
        return result
    
    @staticmethod
    def create_tipo_alerta(descripcion: str) -> int:
        """Crea un nuevo tipo de alerta"""

        print("Creating representante with description:", descripcion)

        desc_norm = (descripcion or "").strip()
        if not desc_norm:
            raise ValueError("La descripción no puede estar vacía")
        
        # 1) ¿Ya existe?
        exists_query = """
            SELECT TOP 1 IDTIPOALERTA AS id
            FROM TIPOS_ALERTAS
            WHERE UPPER(LTRIM(RTRIM(DESCRIPCION))) = UPPER(LTRIM(RTRIM(?)))
        """
        row = db_manager.execute_query(exists_query, (desc_norm,), fetch_one=True)

        if row:
            # Ya existe: devuelve el id existente
            raise ValueError("Ya existe una alerta con esta descripción")
        
        query = """
            INSERT INTO TIPOS_ALERTAS (DESCRIPCION)
            VALUES (?);
            SELECT SCOPE_IDENTITY() as id;
        """
        
        result = db_manager.execute_query(query, (descripcion,), fetch_one=True)
        return int(result)
    
    @staticmethod
    def update_tipo_alerta(idtipoalerta: int, descripcion: str) -> None:
        """Actualiza un tipo de alerta"""
        query = """
            UPDATE TIPOS_ALERTAS
            SET DESCRIPCION = ?
            WHERE IDTIPOALERTA = ?
        """
        
        db_manager.execute_query(query, (descripcion, idtipoalerta))
    
    @staticmethod
    def delete_tipo_alerta(idtipoalerta: int) -> bool:
        """Elimina un tipo de alerta si no está en uso"""
        # Check if in use (adjust based on your schema if there are references)
        # For now, we'll allow deletion
        delete_query = """
            DELETE FROM TIPOS_ALERTAS
            WHERE IDTIPOALERTA = ?
        """
        db_manager.execute_query(delete_query, (idtipoalerta,))
        
        return True


class ProcesoService:
    @staticmethod
    def get_all_procesos() -> List[Dict]:
        """Obtiene todos los procesos"""
        query = """
            SELECT IDPROCESO, DESCRIPCION, PREFIJO, VISIBILIDAD
            FROM PLANNER_PROCESOS
            ORDER BY DESCRIPCION
        """
        
        procesos = db_manager.execute_query(query)
        result = []
        
        for proceso in procesos:
            result.append({
                "idproceso": proceso.IDPROCESO,
                "descripcion": proceso.DESCRIPCION,
                "prefijo": proceso.PREFIJO,
                "visibilidad": proceso.VISIBILIDAD
            })
        
        return result
    
    @staticmethod
    def get_proceso_by_id(idproceso: int) -> Optional[Dict]:
        """Obtiene un proceso por ID con sus estados"""
        query = """
            SELECT IDPROCESO, DESCRIPCION, PREFIJO, VISIBILIDAD
            FROM PLANNER_PROCESOS
            WHERE IDPROCESO = ?
        """
        
        proceso = db_manager.execute_query(query, (idproceso,), fetch_one=True)
        
        if not proceso:
            return None
        
        # Get estados for this proceso
        estados_query = """
            SELECT 
                PE.IDESTADO, PE.IDPROCESO, PE.VISIBILIDAD, PE.TITULO, 
                PE.ORDEN, PE.FINALIZA, PE.IDESTADOPADRE,
                A.IDACCION, A.DESCRIPCION as ACCION_DESCRIPCION
            FROM PLANNER_PROCESOS_ESTADOS PE
            LEFT JOIN ACCIONES A ON PE.TITULO = A.DESCRIPCION
            WHERE PE.IDPROCESO = ?
            ORDER BY PE.ORDEN
        """
        
        estados = db_manager.execute_query(estados_query, (idproceso,))
        estados_list = []
        
        for estado in estados:
            estados_list.append({
                "idestado": estado.IDESTADO,
                "idproceso": estado.IDPROCESO,
                "visibilidad": bool(estado.VISIBILIDAD),
                "titulo": estado.TITULO,
                "orden": estado.ORDEN,
                "finaliza": bool(estado.FINALIZA) if estado.FINALIZA is not None else False,
                "idestadopadre": estado.IDESTADOPADRE,
                "idaccion": estado.IDACCION if hasattr(estado, 'IDACCION') else None
            })
        
        return {
            "idproceso": proceso.IDPROCESO,
            "descripcion": proceso.DESCRIPCION,
            "prefijo": proceso.PREFIJO,
            "visibilidad": proceso.VISIBILIDAD,
            "estados": estados_list
        }
        
    @staticmethod
    def create_proceso(descripcion: str, prefijo: Optional[str], visibilidad: int) -> int:
        """Crea un nuevo proceso"""
        query = """
            INSERT INTO PLANNER_PROCESOS (CODEMPRESA, VISIBILIDAD, IDAREA, DESCRIPCION, PREFIJO)
            VALUES (NULL, ?, 0, ?, ?);
            SELECT SCOPE_IDENTITY() as id;
        """
        
        result = db_manager.execute_query(query, (visibilidad, descripcion, prefijo), fetch_one=True)
        return int(result)
    
    @staticmethod
    def update_proceso(idproceso: int, descripcion: str, prefijo: Optional[str], visibilidad: int) -> None:
        """Actualiza un proceso"""
        query = """
            UPDATE PLANNER_PROCESOS
            SET DESCRIPCION = ?, PREFIJO = ?, VISIBILIDAD = ?
            WHERE IDPROCESO = ?
        """
        
        db_manager.execute_query(query, (descripcion, prefijo, visibilidad, idproceso))
    
    @staticmethod
    def delete_proceso(idproceso: int) -> bool:
        """Elimina un proceso si no está en uso"""
        # Check if in use in PLANNER_TAREAS
        check_query = """
            SELECT COUNT(*) as count
            FROM PLANNER_TAREAS
            WHERE IDPROCESO = ?
        """
        
        result = db_manager.execute_query(check_query, (idproceso,), fetch_one=True)
        
        if result.count > 0:
            return False
        
        # Delete the proceso
        delete_query = """
            DELETE FROM PLANNER_PROCESOS
            WHERE IDPROCESO = ?
        """
        db_manager.execute_query(delete_query, (idproceso,))
        
        return True


class AccionService:
    @staticmethod
    def get_acciones_for_proceso() -> List[Dict]:
        """Obtiene acciones activas para procesos"""
        query = """
            SELECT IDACCION, DESCRIPCION, ACTIVA, PROCESO
            FROM ACCIONES
            WHERE ACTIVA = 1 AND PROCESO = 1
            ORDER BY DESCRIPCION
        """
        
        acciones = db_manager.execute_query(query)
        result = []
        
        for accion in acciones:
            result.append({
                "idaccion": accion.IDACCION,
                "descripcion": accion.DESCRIPCION,
                "activa": bool(accion.ACTIVA),
                "proceso": bool(accion.PROCESO)
            })
        
        return result

class ProcesoEstadoService:
    @staticmethod
    def get_estados_by_proceso(idproceso: int) -> List[Dict]:
        """Obtiene todos los estados de un proceso"""
        query = """
            SELECT IDESTADO, IDPROCESO, VISIBILIDAD, TITULO, ORDEN, FINALIZA, IDESTADOPADRE
            FROM PLANNER_PROCESOS_ESTADOS
            WHERE IDPROCESO = ?
            ORDER BY ORDEN
        """
        
        estados = db_manager.execute_query(query, (idproceso,))
        result = []
        
        for estado in estados:
            result.append({
                "idestado": estado.IDESTADO,
                "idproceso": estado.IDPROCESO,
                "visibilidad": bool(estado.VISIBILIDAD),
                "titulo": estado.TITULO,
                "orden": estado.ORDEN,
                "finaliza": bool(estado.FINALIZA) if estado.FINALIZA is not None else False,
                "idestadopadre": estado.IDESTADOPADRE
            })
        
        return result
    
    @staticmethod
    def create_estado(idaccion: int, idproceso: int, titulo: str, visibilidad: bool, orden: int, finaliza: bool) -> int:
        """Crea un nuevo estado para un proceso"""
        query = """
            INSERT INTO PLANNER_PROCESOS_ESTADOS (IDESTADO, IDPROCESO, VISIBILIDAD, TITULO, ORDEN, FINALIZA)
            VALUES (?, ?, ?, ?, ?, ?);
            SELECT SCOPE_IDENTITY() as id;
        """
        
        result = db_manager.execute_query(query, (idaccion, idproceso, visibilidad, titulo, orden, finaliza), fetch_one=True)
        return int(result)
    
    @staticmethod
    def update_estado(idestado: int, visibilidad: bool, orden: int, finaliza: bool) -> None:
        """Actualiza un estado"""
        query = """
            UPDATE PLANNER_PROCESOS_ESTADOS
            SET VISIBILIDAD = ?, ORDEN = ?, FINALIZA = ?
            WHERE IDESTADO = ?
        """
        
        db_manager.execute_query(query, (visibilidad, orden, finaliza, idestado))
    
    @staticmethod
    def delete_estado(idestado: int) -> None:
        """Elimina un estado"""
        query = """
            DELETE FROM PLANNER_PROCESOS_ESTADOS
            WHERE IDESTADO = ?
        """
        db_manager.execute_query(query, (idestado,))
    
    @staticmethod
    def delete_estados_by_proceso(idproceso: int) -> None:
        """Elimina todos los estados de un proceso"""
        query = """
            DELETE FROM PLANNER_PROCESOS_ESTADOS
            WHERE IDPROCESO = ?
        """
        db_manager.execute_query(query, (idproceso,))
#proceso: int) -> None:
        """Elimina todos los estados de un proceso"""
        query = """
            DELETE FROM PLANNER_PROCESOS_ESTADOS
            WHERE IDPROCESO = ?
        """
        db_manager.execute_query(query, (idproceso,))


class ProcesoEstadoRolService:
    @staticmethod
    def get_roles_by_estado(idproceso: int, idestado: int) -> List[Dict]:
        """Obtiene todos los roles asignados a un estado"""
        query = """
            SELECT 
                PER.ID, PER.IDPROCESO, PER.IDESTADO, PER.IDROL,
                R.NOMBRE as rol_nombre,
                PER.LECTURA, PER.ESCRITURA, PER.CAMBIOESTADO
            FROM PLANNER_PROCESOS_ESTADOS_ROLES PER
            INNER JOIN ROLES R ON PER.IDROL = R.ID
            WHERE PER.IDPROCESO = ? AND PER.IDESTADO = ?
            ORDER BY R.NOMBRE
        """
        
        roles = db_manager.execute_query(query, (idproceso, idestado))
        result = []
        
        for rol in roles:
            result.append({
                "id": rol.ID,
                "idproceso": rol.IDPROCESO,
                "idestado": rol.IDESTADO,
                "idrol": rol.IDROL,
                "rol_nombre": rol.rol_nombre,
                "lectura": bool(rol.LECTURA),
                "escritura": bool(rol.ESCRITURA),
                "cambioestado": bool(rol.CAMBIOESTADO)
            })
        
        return result
    
    @staticmethod
    def create_estado_rol(idproceso: int, idestado: int, idrol: int, lectura: bool, escritura: bool, cambioestado: bool) -> int:
        """Crea un nuevo rol para un estado"""
        query = """
            INSERT INTO PLANNER_PROCESOS_ESTADOS_ROLES (IDPROCESO, IDESTADO, IDROL, LECTURA, ESCRITURA, CAMBIOESTADO)
            VALUES (?, ?, ?, ?, ?, ?);
            SELECT SCOPE_IDENTITY() as id;
        """
        
        result = db_manager.execute_query(query, (idproceso, idestado, idrol, lectura, escritura, cambioestado), fetch_one=True)
        return int(result)
    
    @staticmethod
    def update_estado_rol(id: int, lectura: bool, escritura: bool, cambioestado: bool) -> None:
        """Actualiza un rol de estado"""
        query = """
            UPDATE PLANNER_PROCESOS_ESTADOS_ROLES
            SET LECTURA = ?, ESCRITURA = ?, CAMBIOESTADO = ?
            WHERE ID = ?
        """
        
        db_manager.execute_query(query, (lectura, escritura, cambioestado, id))
    
    @staticmethod
    def delete_estado_rol(id: int) -> None:
        """Elimina un rol de estado"""
        query = """
            DELETE FROM PLANNER_PROCESOS_ESTADOS_ROLES
            WHERE ID = ?
        """
        db_manager.execute_query(query, (id,))
    
    @staticmethod
    def delete_roles_by_estado(idproceso: int, idestado: int) -> None:
        """Elimina todos los roles de un estado"""
        query = """
            DELETE FROM PLANNER_PROCESOS_ESTADOS_ROLES
            WHERE IDPROCESO = ? AND IDESTADO = ?
        """
        db_manager.execute_query(query, (idproceso, idestado))
    
    @staticmethod
    def save_roles_batch(idproceso: int, idestado: int, roles: List[Dict]) -> None:
        """Guarda múltiples roles para un estado (elimina existentes y crea nuevos)"""
        # First, delete all existing roles for this estado
        ProcesoEstadoRolService.delete_roles_by_estado(idproceso, idestado)
        
        # Then, insert new roles
        for rol_data in roles:
            ProcesoEstadoRolService.create_estado_rol(
                idproceso,
                idestado,
                rol_data.get("idrol"),
                rol_data.get("lectura", False),
                rol_data.get("escritura", False),
                rol_data.get("cambioestado", False)
            )


class CatalogoService:
    @staticmethod
    def get_tipos_activos() -> List[Dict]:
        """Obtiene todos los tipos de activos"""
        query = """
            SELECT ID, DESCRIPCION
            FROM TIPOS_ACTIVOS
            ORDER BY DESCRIPCION
        """
        
        tipos = db_manager.execute_query(query)
        result = []
        
        for tipo in tipos:
            result.append({
                "id": tipo.ID,
                "descripcion": tipo.DESCRIPCION
            })
        
        return result
    
    def get_tipos_operaciones() -> List[Dict]:
        """Obtiene todos los tipos de operaciones"""
        query = """
            SELECT IDPROCESO AS ID, DESCRIPCION
            FROM PLANNER_PROCESOS
            ORDER BY DESCRIPCION
        """
        
        tipos = db_manager.execute_query(query)
        result = []
        
        for tipo in tipos:
            result.append({
                "id": tipo.ID,
                "descripcion": tipo.DESCRIPCION
            })
        
        return result
    
    @staticmethod
    def get_clientes() -> List[Dict]:
        """Obtiene todos los clientes (sociedades)"""
        query = """
            SELECT IDCLIENTE, NOMCLI
            FROM ERP_CLIENTES
            ORDER BY NOMCLI
        """
        
        clientes = db_manager.execute_query(query)
        result = []
        
        for cliente in clientes:
            result.append({
                "idcliente": cliente.IDCLIENTE,
                "nomcli": cliente.NOMCLI
            })
        
        return result
    
    @staticmethod
    def get_paises() -> List[Dict]:
        """Obtiene todos los países"""
        query = """
            SELECT COUNTRY_CODE AS CODIGO, NAME AS NOMBRE
            FROM COUNTRIES
            ORDER BY NAME
        """
        
        paises = db_manager.execute_query(query)
        result = []
        
        for pais in paises:
            result.append({
                "codigo": pais.CODIGO,
                "nombre": pais.NOMBRE
            })
        
        return result
    
    @staticmethod
    def get_provincias(country_code: str) -> List[Dict]:
        """Obtiene las provincias de un país"""
        query = """
            SELECT subdivision_code as codigo, name as nombre
            FROM SUBDIVISIONS
            WHERE country_code = ?
            ORDER BY name
        """
        
        provincias = db_manager.execute_query(query, (country_code,))
        result = []
        
        for provincia in provincias:
            result.append({
                "codigo": provincia.codigo,
                "nombre": provincia.nombre
            })
        
        return result
    
    @staticmethod
    def get_analistas_pbc() -> List[Dict]:
        """Obtiene analistas PBC (IDPERFIL=2)"""
        query = """
            SELECT ID, NOMBRE
            FROM USUARIOS
            WHERE IDPERFIL = 2
            ORDER BY NOMBRE
        """
        
        analistas = db_manager.execute_query(query)
        result = []
        
        for analista in analistas:
            result.append({
                "id": analista.ID,
                "nombre": analista.NOMBRE
            })
        
        return result
    
    @staticmethod
    def get_operadores() -> List[Dict]:
        """Obtiene operadores (IDPERFIL=7)"""
        query = """
            SELECT ID, NOMBRE
            FROM USUARIOS
            WHERE IDPERFIL = 7
            ORDER BY NOMBRE
        """
        
        operadores = db_manager.execute_query(query)
        result = []
        
        for operador in operadores:
            result.append({
                "id": operador.ID,
                "nombre": operador.NOMBRE
            })
        
        return result

class TareaService:
    @staticmethod
    def create_tarea(data: Dict, user_id: int) -> int:
        """Crea una nueva tarea (operación)"""
        query = """
            INSERT INTO PLANNER_TAREAS (
                CODEMPRESA, IDPROCESO, IDESTADO, VISIBILIDAD,
                IDCLIENTE, EXT_TIPOACTIVO, EXT_ACTIVOSOTROS,
                LOCALIDAD, PAIS, PROVINCIA, EXT_ANALISTAPBC,
                REFERENCIA, EXT_ASIGNADOR_ANALISTAPBC, EXT_OPERADOR,
                EXT_URGENTE, FECHA_ALTA, IDUSUARIO_ALTA
            )
            VALUES (?, ?, 0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?);
            SELECT SCOPE_IDENTITY() as id;
        """

        print("Creating tarea with data:", data)
        
        # Set asignador if analista is being assigned
        asignador = user_id if data.get('ext_analistapbc') else None
        
        result = db_manager.execute_query(query, (
            data.get('codempresa'),
            data.get('tipo_operacion'),
            data.get('idcliente'),            
            data.get('ext_tipoactivo'),
            data.get('ext_activosotros'),
            data.get('localidad'),
            data.get('pais'),
            data.get('provincia'),
            data.get('ext_analistapbc'),
            data.get('referencia'),
            asignador,
            data.get('ext_operador'),
            data.get('ext_urgente', False),
            user_id
        ), fetch_one=True)
        
        return int(result)
    
    @staticmethod
    def get_tarea_by_id(idtarea: int) -> Optional[Dict]:
        """Obtiene una tarea por ID con información relacionada"""
        query = """
            SELECT 
                T.IDTAREA, T.IDCLIENTE, T.EXT_TIPOACTIVO, T.EXT_ACTIVOSOTROS,
                T.LOCALIDAD, T.PAIS, T.PROVINCIA, T.EXT_ANALISTAPBC,
                T.CODEMPRESA, T.REFERENCIA, T.EXT_ASIGNADOR_ANALISTAPBC,
                T.EXT_OPERADOR, T.EXT_URGENTE, T.FECHA_ALTA,
                C.NOMCLI as cliente_nombre,
                TA.DESCRIPCION as tipoactivo_nombre,
                P.NAME as pais_nombre,
                S.name as provincia_nombre,
                A.NOMBRE as analistapbc_nombre,
                E.NOMEMPRESA as servicer_nombre,
                AS_USER.NOMBRE as asignador_nombre,
                O.NOMBRE as operador_nombre
            FROM PLANNER_TAREAS T
            LEFT JOIN ERP_CLIENTES C ON T.IDCLIENTE = C.IDCLIENTE
            LEFT JOIN TIPOS_ACTIVOS TA ON T.EXT_TIPOACTIVO = TA.ID
            LEFT JOIN COUNTRIES P ON T.PAIS = P.COUNTRY_CODE
            LEFT JOIN SUBDIVISIONS S ON T.PROVINCIA = S.subdivision_code
            LEFT JOIN USUARIOS A ON T.EXT_ANALISTAPBC = A.ID
            LEFT JOIN EMPRESAS_CLIENTES E ON T.CODEMPRESA = E.CODEMPRESA
            LEFT JOIN USUARIOS AS_USER ON T.EXT_ASIGNADOR_ANALISTAPBC = AS_USER.ID
            LEFT JOIN USUARIOS O ON T.EXT_OPERADOR = O.ID
            WHERE T.IDTAREA = ?
        """

        query = """
            SELECT 
            P.COUNTRY_CODE as 'pais',
            t.idtarea,
        T.[codempresa]
        ,T.[idproceso]
        ,T.[idestado]
        ,T.[idetiqueta]
        ,T.[visibilidad]
        ,T.[titulo]
        ,T.[descripcion]
        ,T.[orden]
        ,T.[fecha_alta]
        ,T.[fecha_prevista]
        ,T.[fecha_realizacion]
        ,T.[fecha_cierre]
        ,T.[idsolicitud]
        ,T.[idusuario_alta]
        ,T.[idusuario_realizacion]
        ,T.[idcliente]
        ,T.[facturacion]
        ,T.[idcuotalin]
        ,T.[numdoc]
        ,T.[idserie]
        ,T.[cancelada]
        ,T.[archivada]
        ,T.[idtareaorigen]
        ,T.[idcontacto]
        ,T.[finalizada]
        ,T.[contador]
        ,T.[prefijo]
        ,T.[seleccionar]
        ,T.[ext_objeto]
        ,T.[ext_tipoactivo]
        ,T.[ext_localidadinmueble]
        ,T.[ext_codprovi_inmueble]
        ,T.[ext_importe]
        ,T.[ext_bloqueo]
        ,T.[ext_tributacion]
        ,T.[ext_activosotros]
        ,T.[ext_analistapbc]
        ,T.[idhitoactivo]
        ,T.[riesgo]
        ,T.[idrepresen]
        ,T.[upsize_ts]
        ,T.[estado]
        ,T.[ext_asignador_analistapbc]
        ,T.[ext_operador]
        ,T.[referencia]
        ,T.[ext_enviado_pbc]
        ,T.[ext_urgente]
        ,T.[localidad]
        ,T.[provincia]
        ,
                C.NOMCLI as cliente_nombre,
                TA.DESCRIPCION as tipoactivo_nombre,
				P.country_code AS pais_codigo,
                P.NAME as pais_nombre,
				S.subdivision_code as provincia_codigo,
                S.name as provincia_nombre,
                A.NOMBRE as analistapbc_nombre,
                E.NOMEMPRESA as servicer_nombre,
                AS_USER.NOMBRE as asignador_nombre,
                O.NOMBRE as operador_nombre
            FROM PLANNER_TAREAS T
            LEFT JOIN ERP_CLIENTES C ON T.IDCLIENTE = C.IDCLIENTE
            LEFT JOIN TIPOS_ACTIVOS TA ON T.EXT_TIPOACTIVO = TA.ID
            LEFT JOIN COUNTRIES P ON T.PAIS = P.COUNTRY_CODE
            LEFT JOIN SUBDIVISIONS S ON T.PROVINCIA = S.subdivision_code
            LEFT JOIN USUARIOS A ON T.EXT_ANALISTAPBC = A.ID
            LEFT JOIN EMPRESAS_CLIENTES E ON T.CODEMPRESA = E.CODEMPRESA
            LEFT JOIN USUARIOS AS_USER ON T.EXT_ASIGNADOR_ANALISTAPBC = AS_USER.ID
            LEFT JOIN USUARIOS O ON T.EXT_OPERADOR = O.ID
            WHERE T.IDTAREA = ?
            """
        
        tarea = db_manager.execute_query(query, (idtarea,), fetch_one=True)
        
        if not tarea:
            return None

        #print("Fetched tarea:", tarea.pais)
        
        payload = {
            # Identificadores / básicos
            "idtarea": getattr(tarea, "idtarea", None),
            "codempresa": getattr(tarea, "codempresa", None),
            "idproceso": getattr(tarea, "idproceso", None),
            "idestado": getattr(tarea, "idestado", None),
            "idetiqueta": getattr(tarea, "idetiqueta", None),
            "idcliente": getattr(tarea, "idcliente", None),

            # Texto / metadatos
            "visibilidad": getattr(tarea, "visibilidad", None),
            "titulo": getattr(tarea, "titulo", None),
            "descripcion": getattr(tarea, "descripcion", None),
            "orden": getattr(tarea, "orden", None),
            "fecha_alta": getattr(tarea, "fecha_alta", None),
            "fecha_prevista": getattr(tarea, "fecha_prevista", None),
            "fecha_realizacion": getattr(tarea, "fecha_realizacion", None),
            "fecha_cierre": getattr(tarea, "fecha_cierre", None),
            "idsolicitud": getattr(tarea, "idsolicitud", None),
            "idusuario_alta": getattr(tarea, "idusuario_alta", None),
            "idusuario_realizacion": getattr(tarea, "idusuario_realizacion", None),

            # Facturación / docs (si aplica en tu SELECT)
            "facturacion": getattr(tarea, "facturacion", None),
            "idcuotalin": getattr(tarea, "idcuotalin", None),
            "numdoc": getattr(tarea, "numdoc", None),
            "idserie": getattr(tarea, "idserie", None),

            # Estados booleanos
            "cancelada": getattr(tarea, "cancelada", None),
            "archivada": getattr(tarea, "archivada", None),
            "finalizada": getattr(tarea, "finalizada", None),
            "ext_bloqueo": getattr(tarea, "ext_bloqueo", None),
            "ext_enviado_pbc": getattr(tarea, "ext_enviado_pbc", None),
            "ext_urgente": bool(getattr(tarea, "ext_urgente", False)),

            # Vinculaciones
            "idtareaorigen": getattr(tarea, "idtareaorigen", None),
            "idcontacto": getattr(tarea, "idcontacto", None),
            "idrepresen": getattr(tarea, "idrepresen", None),
            "idhitoactivo": getattr(tarea, "idhitoactivo", None),

            # Extras/extendidos
            "contador": getattr(tarea, "contador", None),
            "prefijo": getattr(tarea, "prefijo", None),
            "seleccionar": getattr(tarea, "seleccionar", None),
            "ext_objeto": getattr(tarea, "ext_objeto", None),
            "ext_tipoactivo": getattr(tarea, "ext_tipoactivo", None),
            "ext_localidadinmueble": getattr(tarea, "ext_localidadinmueble", None),
            "ext_codprovi_inmueble": getattr(tarea, "ext_codprovi_inmueble", None),
            "ext_importe": getattr(tarea, "ext_importe", None),
            "ext_tributacion": getattr(tarea, "ext_tributacion", None),
            "ext_activosotros": getattr(tarea, "ext_activosotros", None),
            "ext_analistapbc": getattr(tarea, "ext_analistapbc", None),
            "ext_asignador_analistapbc": getattr(tarea, "ext_asignador_analistapbc", None),
            "ext_operador": getattr(tarea, "ext_operador", None),

            # Localización “plana”
            "localidad": getattr(tarea, "localidad", None),
            "provincia": getattr(tarea, "provincia", None),
            "pais": getattr(tarea, "pais", None),

            # Catálogos / “nombres bonitos”
            "cliente_nombre": getattr(tarea, "cliente_nombre", None),
            "tipoactivo_nombre": getattr(tarea, "tipoactivo_nombre", None),
            "pais_nombre": getattr(tarea, "pais_nombre", None),
            "provincia_nombre": getattr(tarea, "provincia_nombre", None),
            "analistapbc_nombre": getattr(tarea, "analistapbc_nombre", None),
            "asignador_nombre": getattr(tarea, "asignador_nombre", None),
            "operador_nombre": getattr(tarea, "operador_nombre", None),
            "servicer_nombre": getattr(tarea, "servicer_nombre", None),

            # Otros del modelo (si los has incluido en el SELECT)
            "riesgo": getattr(tarea, "riesgo", None),
            "estado": getattr(tarea, "estado", None),
            "referencia": getattr(tarea, "referencia", None),
        }

        #print("pais: ", tarea.pais)
        #print("Tarea payload:", payload)

        return payload

        
        return {
            "idtarea": tarea.IDTAREA,
            "idcliente": tarea.IDCLIENTE,
            "cliente_nombre": tarea.cliente_nombre,
            "ext_tipoactivo": tarea.EXT_TIPOACTIVO,
            "tipoactivo_nombre": tarea.tipoactivo_nombre,
            "ext_activosotros": tarea.EXT_ACTIVOSOTROS,
            "localidad": tarea.LOCALIDAD,
            "pais": tarea.PAIS,
            "pais_nombre": tarea.pais_nombre,
            "provincia": tarea.PROVINCIA,
            "provincia_nombre": tarea.provincia_nombre,
            "ext_analistapbc": tarea.EXT_ANALISTAPBC,
            "analistapbc_nombre": tarea.analistapbc_nombre,
            "codempresa": tarea.CODEMPRESA,
            "servicer_nombre": tarea.servicer_nombre,
            "referencia": tarea.REFERENCIA,
            "ext_asignador_analistapbc": tarea.EXT_ASIGNADOR_ANALISTAPBC,
            "asignador_nombre": tarea.asignador_nombre,
            "ext_operador": tarea.EXT_OPERADOR,
            "operador_nombre": tarea.operador_nombre,
            "ext_urgente": bool(tarea.EXT_URGENTE),
            "fecha_alta": tarea.FECHA_ALTA
        }
    
    @staticmethod
    def update_tarea(idtarea: int, data: Dict, user_id: int) -> None:
        """Actualiza una tarea existente"""
        # Get current tarea to check if analista is being changed
        current_query = "SELECT EXT_ANALISTAPBC FROM PLANNER_TAREAS WHERE IDTAREA = ?"
        current = db_manager.execute_query(current_query, (idtarea,), fetch_one=True)
        
        # Update asignador if analista is being changed
        asignador = data.ext_asignador_analistapbc
        if current and current.EXT_ANALISTAPBC != data.ext_analistapbc:
            asignador = user_id
        
        query = """
            UPDATE PLANNER_TAREAS
            SET CODEMPRESA = ?, IDCLIENTE = ?, EXT_TIPOACTIVO = ?,
                EXT_ACTIVOSOTROS = ?, LOCALIDAD = ?, PAIS = ?,
                PROVINCIA = ?, EXT_ANALISTAPBC = ?, REFERENCIA = ?,
                EXT_ASIGNADOR_ANALISTAPBC = ?, EXT_OPERADOR = ?,
                EXT_URGENTE = ?
            WHERE IDTAREA = ?
        """
        
        db_manager.execute_query(query, (
            data.codempresa,
            data.idcliente,
            data.ext_tipoactivo,
            data.ext_activosotros,
            data.localidad,
            data.pais,
            data.provincia,
            data.ext_analistapbc,
            data.referencia,
            asignador,
            data.ext_operador,
            data.ext_urgente if data.ext_urgente else False,
            idtarea
        ))

# class ProcesoEstadoRolService:
#     @staticmethod
#     def get_roles_by_estado(idproceso: int, idestado: int) -> List[Dict]:
#         """Obtiene todos los roles asignados a un estado"""
#         query = """
#             SELECT 
#                 PER.ID, PER.IDPROCESO, PER.IDESTADO, PER.IDROL,
#                 R.NOMBRE as rol_nombre,
#                 PER.LECTURA, PER.ESCRITURA, PER.CAMBIOESTADO
#             FROM PLANNER_PROCESOS_ESTADOS_ROLES PER
#             INNER JOIN ROLES R ON PER.IDROL = R.ID
#             WHERE PER.IDPROCESO = ? AND PER.IDESTADO = ?
#             ORDER BY R.NOMBRE
#         """
        
#         roles = db_manager.execute_query(query, (idproceso, idestado))
#         result = []
        
#         for rol in roles:
#             result.append({
#                 "id": rol.ID,
#                 "idproceso": rol.IDPROCESO,
#                 "idestado": rol.IDESTADO,
#                 "idrol": rol.IDROL,
#                 "rol_nombre": rol.rol_nombre,
#                 "lectura": bool(rol.LECTURA),
#                 "escritura": bool(rol.ESCRITURA),
#                 "cambioestado": bool(rol.CAMBIOESTADO)
#             })
        
#         return result
    
#     @staticmethod
#     def create_estado_rol(idproceso: int, idestado: int, idrol: int, lectura: bool, escritura: bool, cambioestado: bool) -> int:
#         """Crea un nuevo rol para un estado"""
#         query = """
#             INSERT INTO PLANNER_PROCESOS_ESTADOS_ROLES (IDPROCESO, IDESTADO, IDROL, LECTURA, ESCRITURA, CAMBIOESTADO)
#             VALUES (?, ?, ?, ?, ?, ?);
#             SELECT SCOPE_IDENTITY() as id;
#         """
        
#         result = db_manager.execute_query(query, (idproceso, idestado, idrol, lectura, escritura, cambioestado), fetch_one=True)
#         return int(result.id)
    
#     @staticmethod
#     def update_estado_rol(id: int, lectura: bool, escritura: bool, cambioestado: bool) -> None:
#         """Actualiza un rol de estado"""
#         query = """
#             UPDATE PLANNER_PROCESOS_ESTADOS_ROLES
#             SET LECTURA = ?, ESCRITURA = ?, CAMBIOESTADO = ?
#             WHERE ID = ?
#         """
        
#         db_manager.execute_query(query, (lectura, escritura, cambioestado, id))
    
#     @staticmethod
#     def delete_estado_rol(id: int) -> None:
#         """Elimina un rol de estado"""
#         query = """
#             DELETE FROM PLANNER_PROCESOS_ESTADOS_ROLES
#             WHERE ID = ?
#         """
#         db_manager.execute_query(query, (id,))
    
#     @staticmethod
#     def delete_roles_by_estado(idproceso: int, idestado: int) -> None:
#         """Elimina todos los roles de un estado"""
#         query = """
#             DELETE FROM PLANNER_PROCESOS_ESTADOS_ROLES
#             WHERE IDPROCESO = ? AND IDESTADO = ?
#         """
#         db_manager.execute_query(query, (idproceso, idestado))
