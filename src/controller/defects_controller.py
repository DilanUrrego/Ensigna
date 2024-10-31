
import psycopg2
from psycopg2 import Error
import SecretConfig

class ControladorDefectos:
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
            print("Error al conectar a la base de datos defectos:", error)
            return None, None

    @staticmethod
    def agregar_defecto(id_producto, defecto:str, tipo_defecto:str = None):
        cursor, connection = ControladorDefectos.obtener_cursor()
        if cursor:
            try:
                if tipo_defecto is None:
                    query = "INSERT INTO defectos (id_producto, defecto) VALUES (%s, %s)"
                    cursor.execute(query, (id_producto, defecto))
                    connection.commit()
                    print("Defecto agregado correctamente.")
                    return True
                else:
                    query = "INSERT INTO defectos (id_producto, defecto, tipo_defecto) VALUES (%s, %s, %s)"
                    cursor.execute(query, (id_producto, defecto, tipo_defecto))
                    connection.commit()
                    print("Defecto agregado correctamente.")
                    return True
            except Exception as e:
                connection.rollback()
                print(f"Error al agregar Defecto: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
        return False


    @staticmethod
    def editar_defecto(id_producto, defecto):
        cursor, connection = ControladorDefectos.obtener_cursor()
        if cursor:
            try:
                query = f"UPDATE defectos SET defecto = %s WHERE id = %s"
                cursor.execute(query, (defecto, id_producto))
                connection.commit()
                print("Defecto editado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al editar defecto: {e}")
            finally:
                cursor.close()
                connection.close()


    @staticmethod
    def eliminar_defecto(id_producto):
        cursor, connection = ControladorDefectos.obtener_cursor()
        if cursor:
            try:
                query = f"DELETE FROM defectos WHERE id = '{id_producto}'"
                cursor.execute(query)
                connection.commit()
                print("Defecto eliminado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al eliminar defecto: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def obtener_defectos_por_producto(id_producto):
        cursor, connection = ControladorDefectos.obtener_cursor()
        if cursor:
            try:
                query = "SELECT defecto FROM dfectos WHERE id_producto = %s"
                cursor.execute(query, (id_producto,))
                comentarios = cursor.fetchall()
                return [comentario[0] for comentario in comentarios]  # Lista de comentarios
            except Exception as e:
                print(f"Error al obtener defectos: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
        return []
