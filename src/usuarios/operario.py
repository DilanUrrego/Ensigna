class Operario:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def validar_resultado_IA(self, resultado):
        return bool(resultado)

    def realizar_comentarios(self, comentario):
        print(f"Comentario del operario: {comentario}")
