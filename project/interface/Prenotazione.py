class Prenotazione:
    def _init_(self, codice, cliente, camera, data_inizio, data_fine, colazione=False):
        if data_inizio <= datetime.now():
            raise ValueError("Le prenotazioni devono essere effettuate almeno un giorno prima")

        self.codice = codice
        self.cliente = cliente
        self.camera = camera
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.colazione = colazione
        self.servizi = []
        self.pagata = False
        self.costo_totale = 0
        self.calcola_costo()

    def aggiungi_servizio(self, servizio):
        self.servizi.append(servizio)
        self.costo_totale += servizio.prezzo

    def calcola_costo(self):
        giorni = (self.data_fine - self.data_inizio).days
        self.costo_totale = giorni * self.camera.costo_giornaliero

        # Pasti
        if self.camera.tipo != "suite" and self.colazione:
            self.costo_totale += 10 * giorni

    def disdici(self, data_attuale):
        giorni_alla_prenotazione = (self.data_inizio - data_attuale).days
        if giorni_alla_prenotazione >= 7:
            rimborso = self.costo_totale
        elif 1 <= giorni_alla_prenotazione < 7:
            rimborso = self.costo_totale * 0.5
        else:
            rimborso = 0

        return rimborso

    def paga(self):
        self.pagata = True
        print(f"Prenotazione {self.codice} pagata. Totale: €{self.costo_totale:.2f}")
