from .producto import Producto

class Lavadora(Producto):
    def __init__(self, id, modelo, fecha_creacion):
        super().__init__(id, "Lavadora", modelo, fecha_creacion, "En producción")
