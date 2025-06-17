class Camera:
    def _init_(self, tipo):
        self.tipo = tipo
        if tipo == "singola":
            self.costo_giornaliero = 60
        elif tipo == "matrimoniale":
            self.costo_giornaliero = 80
        elif tipo == "suite":
            self.costo_giornaliero = 150
        else:
            raise ValueError("Tipo camera non valido")
