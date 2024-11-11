import os
import sys
from pathlib import Path
from datetime import datetime

# Añadir la ruta del proyecto al PYTHONPATH
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import psycopg2
from psycopg2 import Error
from src.SecretConfig import SecretConfig

class ControladorReportes:
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
            print("Error al conectar a la base de datos reportes:", error)
            return None, None

    @staticmethod
    def crear_reporte(id_producto, nombre_producto, tipo_defecto, descripcion, estado):
        cursor, connection = ControladorReportes.obtener_cursor()
        if cursor:
            try:
                # Verificar si el producto existe
                cursor.execute("SELECT id FROM productos WHERE id = %s", (id_producto,))
                if not cursor.fetchone():
                    raise Exception("El producto no existe")

                query = """
                INSERT INTO reportes (id_producto, nombre_producto, tipo_defecto, descripcion, estado)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """
                cursor.execute(query, (id_producto, nombre_producto, tipo_defecto, descripcion, estado))
                reporte_id = cursor.fetchone()[0]
                connection.commit()
                return {"success": True, "reporte_id": reporte_id}
            except Exception as e:
                if connection:
                    connection.rollback()
                print(f"Error al crear reporte: {e}")
                return {"success": False, "error": str(e)}
            finally:
                if connection:
                    cursor.close()
                    connection.close()
        return {"success": False, "error": "Error de conexión a la base de datos"}