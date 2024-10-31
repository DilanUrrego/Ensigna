
import psycopg2
from psycopg2 import Error
import SecretConfig

class ControladorComentarios:
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
            print("Error al conectar a la base de datos comentarios:", error)
            return None, None

    @staticmethod
    def agregar_comentario(id_producto, comentario:str):
        cursor, connection = ControladorComentarios.obtener_cursor()
        if cursor:
            try:
                query = "INSERT INTO comentarios (id_producto, comentario) VALUES (%s, %s)"
                cursor.execute(query, (id_producto, comentario))
                connection.commit()
                print("Comentario agregado correctamente.")
                return True
            except Exception as e:
                connection.rollback()
                print(f"Error al agregar Comentario: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
        return False


    @staticmethod
    def editar_comentario(id_producto, comentario):
        cursor, connection = ControladorComentarios.obtener_cursor()
        if cursor:
            try:
                query = f"UPDATE comentarios SET comentario = %s WHERE id = %s"
                cursor.execute(query, (comentario, id_producto))
                connection.commit()
                print("Comentario editado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al editar comentario: {e}")
            finally:
                cursor.close()
                connection.close()


    @staticmethod
    def eliminar_comentario(id_producto):
        cursor, connection = ControladorComentarios.obtener_cursor()
        if cursor:
            try:
                query = f"DELETE FROM comentarios WHERE id = '{id_producto}'"
                cursor.execute(query)
                connection.commit()
                print("Comentario eliminado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al eliminar comentario: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def obtener_comentarios_por_producto(id_producto):
        cursor, connection = ControladorComentarios.obtener_cursor()
        if cursor:
            try:
                query = "SELECT comentario FROM comentarios WHERE id_producto = %s"
                cursor.execute(query, (id_producto,))
                comentarios = cursor.fetchall()
                return [comentario[0] for comentario in comentarios]  # Lista de comentarios
            except Exception as e:
                print(f"Error al obtener comentarios: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
        return []
