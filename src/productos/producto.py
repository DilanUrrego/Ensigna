class Producto:
    def __init__(self, id, tipo_de_producto, modelo, fecha_creacion,  estado):
        self.id = id
        self.tipo_de_producto = tipo_de_producto
        self.modelo = modelo
        self.fecha_creacion = fecha_creacion
        self.estado = estado

    def __str__(self):
        return f"{self.tipo_de_producto} - ({self.estado})"
