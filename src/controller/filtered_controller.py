import os
import sys
from pathlib import Path

# Añadir la ruta del proyecto al PYTHONPATH de manera más robusta
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import psycopg2
from psycopg2 import Error
from src.SecretConfig import SecretConfig

class ControladorFiltrado:
    @staticmethod
    def obtener_cursor():
        try:
            connection = psycopg2.connect(
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                host=SecretConfig.PGHOST,
                port=SecretConfig.PGPORT,
                sslmode='require'
            )
            cursor = connection.cursor()
            return cursor, connection
        except (Exception, Error) as error:
            print("Error al conectar a la base de datos:", error)
            return None, None

    @staticmethod
    def filtrar_productos(numero_serie=None, tipo_defecto=None, tipo_producto=None):
        cursor, connection = ControladorFiltrado.obtener_cursor()
        if cursor:
            try:
                conditions = []
                params = []
                
                # Consulta base
                query = """
                    SELECT DISTINCT 
                        p.id, p.tipo_producto, p.modelo, p.num_serie, 
                        COALESCE(r.tipo_defecto, 'Sin defectos reportados') AS tipo_defecto
                    FROM productos p
                    LEFT JOIN reportes r ON p.id = r.id_producto
                """
                
                # Agregar condiciones según los filtros proporcionados
                if numero_serie:
                    conditions.append("p.num_serie = %s")
                    params.append(numero_serie)
                
                if tipo_defecto:
                    conditions.append("r.tipo_defecto = %s")
                    params.append(tipo_defecto)
                
                if tipo_producto:
                    conditions.append("p.tipo_producto = %s")
                    params.append(tipo_producto)
                
                # Agregar las condiciones a la consulta si existen
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                
                cursor.execute(query, params)
                productos = cursor.fetchall()
                
                # Convertir los resultados a una lista de diccionarios
                resultado = []
                for producto in productos:
                    resultado.append({
                        'id': producto[0],
                        'tipo_producto': producto[1],
                        'modelo': producto[2],
                        'num_serie': producto[3],
                        'tipo_defecto': producto[4]
                    })
                
                return resultado
            
            except Exception as e:
                print(f"Error al filtrar productos: {e}")
                return []
            
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        return []