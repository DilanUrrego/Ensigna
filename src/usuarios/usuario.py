import sys
sys.path.append( "src" )

class Usuario:
    def __init__(self, nombre, correo, contrasena):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    def crear_cuenta(self):
        print(f"Cuenta creada para: {self.nombre}")

    def iniciar_sesion(self):
        print(f"{self.nombre} ha iniciado sesión")
