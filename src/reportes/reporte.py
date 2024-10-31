class Reporte:
    def __init__(self, codigo, fecha_reporte, contenido):
        self.codigo = codigo
        self.fecha_reporte = fecha_reporte
        self.contenido = contenido

    def crear_reporte(self):
        print("Reporte creado")

    def consultar_reporte(self):
        print(f"Reporte {self.codigo} consultado")

    def enviar_reporte(self):
        print(f"Reporte {self.codigo} enviado")
