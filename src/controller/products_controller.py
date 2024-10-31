
import psycopg2
from psycopg2 import Error
import SecretConfig

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
                query = f"DELETE FROM productos WHERE id = '{producto_id}'"
                cursor.execute(query)
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
                query = "SELECT modelo, num_serie, tipo_producto FROM productos WHERE id = %s"
                cursor.execute(query, (id_producto,))
                producto = cursor.fetchone()
                
                # Verificar si el producto fue encontrado
                if producto:
                    return {
                        'modelo': producto[0],
                        'num_serie': producto[1],
                        'tipo_producto': producto[2],
                        'defecto': producto[3]
                    }
                else:
                    print("Producto no encontrado.")
                    return None
            except Exception as e:
                print(f"Error al obtener el producto: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None
    
    @staticmethod
    def actualizar_producto(product_id, update_data):
        cursor, connection = ControladorProductos.obtener_cursor()
        if cursor:
            try:
                # Construir la consulta SQL dinámicamente según los campos en update_data
                fields = [f"{key} = %s" for key in update_data.keys()]
                query = f"UPDATE productos SET {', '.join(fields)} WHERE id = %s"
                
                # Valores a actualizar
                values = list(update_data.values()) + [product_id]
                
                # Ejecutar la consulta
                cursor.execute(query, values)
                connection.commit()
                print("Producto actualizado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al actualizar el producto: {e}")
                raise e
            finally:
                cursor.close()
                connection.close()