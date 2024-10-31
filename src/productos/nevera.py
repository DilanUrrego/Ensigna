from .producto import Producto

class Nevera(Producto):
    def __init__(self, id, modelo, fecha_creacion):
        super().__init__(id, "Nevera", modelo, fecha_creacion,  "En producción")
