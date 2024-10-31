class Notificacion:
    def __init__(self, id_notificacion, fecha, tipo, mensaje):
        self.id_notificacion = id_notificacion
        self.fecha = fecha
        self.tipo = tipo
        self.mensaje = mensaje

    def mostrar_notificacion(self):
        print(f"Notificación: {self.mensaje}")
