import pyodbc
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import re

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.config = {
            'server': os.getenv('DB_SERVER', 'localhost'),
            'database': os.getenv('DB_NAME', 'KratosDB'),
            'username': os.getenv('DB_USER', 'sa'),
            'password': os.getenv('DB_PASSWORD', 'YourPassword123'),
            'driver': '{ODBC Driver 17 for SQL Server}'
        }
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        try:
            conn_str = f"DRIVER={self.config['driver']};SERVER={self.config['server']};DATABASE={self.config['database']};UID={self.config['username']};PWD={self.config['password']}"
            return pyodbc.connect(conn_str)
        except Exception as e:
            raise Exception(f"Error de conexión a base de datos: {str(e)}")
    
    def execute_query(self, query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = True):
        """Ejecuta una consulta y retorna los resultados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # print("Executed query:", query)
            # print("With parameters:", params)

            # Detecta si es DML/DDL (requiere commit)
            first = query.lstrip().split()[0].upper()
            #is_write = first in {"INSERT", "UPDATE", "DELETE", "MERGE", "CREATE", "ALTER", "DROP", "TRUNCATE"}
            
            # Detecta si hay alguna sentencia de escritura en TODO el SQL
            upper_sql = query.lstrip().upper()
            is_write = re.search(r'\b(INSERT|UPDATE|DELETE|MERGE|CREATE|ALTER|DROP|TRUNCATE)\b', upper_sql) is not None
            
            result = None
            has_resultset = cursor.description is not None  # True en SELECT y DML con OUTPUT

            if has_resultset:
                if fetch_one:
                    result = cursor.fetchone()
                elif fetch_all:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
            else:                
                result = cursor.rowcount

            if is_write:
                print("Committing transaction...")
                conn.commit() #commit antes de cerrar y antes de return

            return result
        
        finally:
            try:
                cursor.close()
            finally:
                conn.close()
    
    def execute_transaction(self, queries: list):
        """Ejecuta múltiples consultas en una transacción"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for query, params in queries:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

# Instancia global del manager
db_manager = DatabaseManager()
