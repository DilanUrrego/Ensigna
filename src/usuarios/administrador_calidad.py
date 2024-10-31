class AdministradorDeCalidad:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def registrar_producto(self, producto):
        print(f"Producto registrado: {producto.nombre}")

    def actualizar_producto(self, producto, nuevo_estado):
        producto.estado = nuevo_estado
        print(f"Producto actualizado a: {nuevo_estado}")

    def eliminar_producto(self, producto):
        print(f"Producto eliminado: {producto.nombre}")

    def realizar_comentarios(self, comentario):
        print(f"Comentario del administrador: {comentario}")
