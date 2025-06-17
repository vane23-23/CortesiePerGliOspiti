class Servizio:
    def _init_(self, codice, disponibilita, prezzo):
        self.codice = codice
        self.disponibilita = disponibilita
        self.prezzo = prezzo
        self.completato = False
        self.disdetto = False