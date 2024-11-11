import os
import sys
from pathlib import Path

# Añadir la ruta del proyecto al PYTHONPATH de manera más robusta
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import psycopg2
from psycopg2 import Error
from src.SecretConfig import SecretConfig

class ControladorProductos:
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
            print("Error al conectar a la base de datos productos:", error)
            return None, None

    @staticmethod
    def agregar_producto(id, tipo_producto, modelo, num_serie):
        cursor, connection = ControladorProductos.obtener_cursor()
        if cursor:
            try:
                query = "INSERT INTO productos (id, tipo_producto, modelo, num_serie) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id, tipo_producto, modelo, num_serie))
                connection.commit()
                print("Producto agregado correctamente.")
                return True
            except Exception as e:
                connection.rollback()
                print(f"Error al agregar producto: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
        return False

    @staticmethod
    def editar_producto(producto_id, atributo, nuevo_valor):
        cursor, connection = ControladorProductos.obtener_cursor()
        if cursor:
            try:
                query = f"UPDATE productos SET {atributo} = %s WHERE id = %s"
                cursor.execute(query, (nuevo_valor, producto_id))
                connection.commit()
                print("Producto editado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al editar producto: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def eliminar_producto(producto_id):
        cursor, connection = ControladorProductos.obtener_cursor()
        if cursor:
            try:
                query = "DELETE FROM productos WHERE id = %s"
                cursor.execute(query, (producto_id,))
                connection.commit()
                print("Producto eliminado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al eliminar producto: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def obtener_producto_por_id(id_producto):
        cursor, connection = ControladorProductos.obtener_cursor()
        if cursor:
            try:
                query = "SELECT id, tipo_producto, modelo, num_serie FROM productos WHERE id = %s"
                cursor.execute(query, (id_producto,))
                producto = cursor.fetchone()
                
                if producto:
                    return {
                        'id': producto[0],
                        'tipo_producto': producto[1],
                        'modelo': producto[2],
                        'num_serie': producto[3]
                    }
                return None
            except Exception as e:
                print(f"Error al obtener el producto: {e}")
                return None
            finally:
                if connection:
                    cursor.close()
                    connection.close()
        return None
    
    @staticmethod
    def actualizar_producto(product_id, update_data):
        cursor, connection = ControladorProductos.obtener_cursor()
        if cursor:
            try:
                # Construir la consulta SQL dinámicamente
                update_fields = []
                values = []
                
                # Mapeo de nombres de campos del formulario a nombres de columnas
                field_mapping = {
                    'tipo-producto': 'tipo_producto',
                    'modelo': 'modelo',
                    'num-serie': 'num_serie'
                }
                
                # Solo incluir campos que tienen valor
                for form_field, db_field in field_mapping.items():
                    if form_field in update_data and update_data[form_field]:
                        update_fields.append(f"{db_field} = %s")
                        values.append(update_data[form_field])
                
                if not update_fields:  # Si no hay campos para actualizar
                    return True
                
                # Añadir el ID al final de los valores
                values.append(product_id)
                
                # Construir y ejecutar la consulta
                query = f"UPDATE productos SET {', '.join(update_fields)} WHERE id = %s"
                cursor.execute(query, values)
                connection.commit()
                print("Producto actualizado correctamente")
                return True
            except Exception as e:
                if connection:
                    connection.rollback()
                print(f"Error al actualizar el producto: {e}")
                return False
            finally:
                if connection:
                    cursor.close()
                    connection.close()
        return False