class Servizio:
    def __init__(self, codice, disponibilita, prezzo):
        self.codice = codice
        self.disponibilita = disponibilita
        self.prezzo = prezzo
        self.completato = False
        self.disdetto = False