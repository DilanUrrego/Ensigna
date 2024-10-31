
import sys
sys.path.append( "src" )

import psycopg2
from psycopg2 import sql
from src.usuarios.usuario import Usuario
import SecretConfig
import hashlib

import psycopg2

import psycopg2
from psycopg2 import Error

class ControladorUsuarios:
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
            print("Error al conectar a la base de datos usuarios:", error)
            return None, None

    @staticmethod
    def agregar_usuario(nombre, correo, contrasena, rol):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nombre, correo, contrasena, rol))
                connection.commit()
                print("Usuario agregado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al agregar usuario: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def editar_usuario(usuario_id, atributo, nuevo_valor):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = f"UPDATE usuarios SET {atributo} = %s WHERE id = %s"
                cursor.execute(query, (nuevo_valor, usuario_id))
                connection.commit()
                print("Usuario editado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al editar usuario: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def verificar_credenciales(correo, contrasena):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "SELECT rol FROM usuarios WHERE correo = %s AND contrasena = %s"
                cursor.execute(query, (correo, contrasena))
                result = cursor.fetchone()
                connection.close()
                if result:
                    return result[0]  # Devuelve el rol del usuario si las credenciales son correctas
                else:
                    return None
            except Exception as e:
                print("Error al verificar las credenciales:", e)
                connection.close()
                return None