import sys
import os
from pathlib import Path

# Añadir la ruta del proyecto al PYTHONPATH de manera más robusta
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.usuarios.usuario import Usuario
from src.SecretConfig import SecretConfig

import psycopg2
from psycopg2 import sql
import hashlib
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
    def registrar_usuario(nombre, correo, contrasena, rol):
        try:
            # Usar obtener_cursor para obtener conexión y cursor
            cursor, conn = ControladorUsuarios.obtener_cursor()
            
            if cursor:
                # Hashear la contraseña
                contrasena_hasheada = hashlib.sha256(contrasena.encode()).hexdigest()
                
                # Insertar usuario
                cursor.execute("""
                    INSERT INTO usuarios (nombre, correo, contrasena, rol)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                """, (nombre, correo, contrasena_hasheada, rol))
                
                usuario_id = cursor.fetchone()[0]
                conn.commit()
                
                cursor.close()
                conn.close()
                
                return True
            else:
                raise Exception("No se pudo establecer conexión a la base de datos.")
            
        except Exception as e:
            print(f"Error en registrar_usuario: {e}")
            raise Exception("Error al registrar el usuario en la base de datos")

    @staticmethod
    def agregar_usuario(nombre, correo, contrasena, rol):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                # Hashear la contraseña
                contrasena_hasheada = hashlib.sha256(contrasena.encode()).hexdigest()
                
                query = "INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nombre, correo, contrasena_hasheada, rol))
                connection.commit()
                print("Usuario agregado correctamente.")
                return True
            except Exception as e:
                connection.rollback()
                print(f"Error al agregar usuario: {e}")
                return False
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def editar_usuario(usuario_id, atributo, nuevo_valor):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                # Si el atributo es contraseña, hashearla antes de guardar
                if atributo == 'contrasena':
                    nuevo_valor = hashlib.sha256(nuevo_valor.encode()).hexdigest()
                
                query = sql.SQL("UPDATE usuarios SET {} = %s WHERE id = %s").format(
                    sql.Identifier(atributo)
                )
                cursor.execute(query, (nuevo_valor, usuario_id))
                connection.commit()
                print("Usuario editado correctamente.")
                return True
            except Exception as e:
                connection.rollback()
                print(f"Error al editar usuario: {e}")
                return False
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def eliminar_usuario(usuario_id):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "DELETE FROM usuarios WHERE id = %s"
                cursor.execute(query, (usuario_id,))
                connection.commit()
                print("Usuario eliminado correctamente.")
                return True
            except Exception as e:
                connection.rollback()
                print(f"Error al eliminar usuario: {e}")
                return False
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def verificar_credenciales(correo, contrasena):
        try:
            cursor, conn = ControladorUsuarios.obtener_cursor()
            if cursor:
                # Hashear la contraseña proporcionada
                contrasena_hasheada = hashlib.sha256(contrasena.encode()).hexdigest()
                
                # Verificar credenciales
                cursor.execute("""
                    SELECT rol FROM usuarios 
                    WHERE correo = %s AND contrasena = %s;
                """, (correo, contrasena_hasheada))
                
                resultado = cursor.fetchone()
                
                cursor.close()
                conn.close()
                
                return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error en verificar_credenciales: {e}")
            return None

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "SELECT nombre, correo, rol FROM usuarios WHERE id = %s"
                cursor.execute(query, (usuario_id,))
                result = cursor.fetchone()
                
                if result:
                    return {
                        'nombre': result[0],
                        'correo': result[1],
                        'rol': result[2]
                    }
                return None
                
            except Exception as e:
                print(f"Error al obtener usuario: {e}")
                return None
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def listar_usuarios():
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "SELECT id, nombre, correo, rol FROM usuarios"
                cursor.execute(query)
                usuarios = cursor.fetchall()
                
                return [{
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'correo': usuario[2],
                    'rol': usuario[3]
                } for usuario in usuarios]
                
            except Exception as e:
                print(f"Error al listar usuarios: {e}")
                return []
            finally:
                cursor.close()
                connection.close()
