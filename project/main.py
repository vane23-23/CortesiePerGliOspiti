from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

from interface.Camera import Camera
from interface.Cliente import Cliente
from interface.Prenotazione import Prenotazione
from interface.Servizio import Servizio

# ======== VARIABILI GLOBALI ========
prenotazioni = []

# ======== FUNZIONI GUI PRINCIPALI ========
def crea_prenotazione():
    try:
        nome = entry_nome.get()
        cognome = entry_cognome.get()
        cf = entry_cf.get()
        email = entry_email.get()
        telefono = entry_telefono.get()
        eta = int(entry_eta.get())
        id_cliente = f"CL{datetime.now().strftime('%f')}"

        cliente = Cliente(nome, cognome, cf, email, telefono, eta, id_cliente)

        tipo_camera = camera_var.get()
        camera = Camera(tipo_camera)

        data_inizio = datetime.strptime(entry_data_inizio.get(), "%Y-%m-%d")
        data_fine = datetime.strptime(entry_data_fine.get(), "%Y-%m-%d")

        if data_inizio <= datetime.now():
            raise ValueError("Prenotazioni devono essere effettuate con almeno 1 giorno di anticipo.")
        if data_fine <= data_inizio:
            raise ValueError("La data di fine deve essere successiva a quella di inizio.")

        colazione = colazione_var.get() == 1
        codice_prenotazione = f"PR{datetime.now().strftime('%H%M%S')}"

        # Aggiunta servizi extra solo se suite
        servizi = []
        if camera.tipo == "suite":
            if servizio_camera_var.get():
                servizi.append(Servizio("Servizio in camera", 30))
            if lavanderia_var.get():
                servizi.append(Servizio("Lavanderia", 20))

        pren = Prenotazione(codice_prenotazione, cliente, camera, data_inizio, data_fine, colazione, servizi)
        prenotazioni.append(pren)

        messagebox.showinfo("Successo", f"Prenotazione creata!\nCosto: €{pren.costo_totale:.2f}")
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def mostra_storico():
    finestra_storico = tk.Toplevel(finestra)
    finestra_storico.title("Storico Prenotazioni")

    for idx, p in enumerate(prenotazioni):
        testo = (
            f"{idx+1}. {p.cliente.nome} {p.cliente.cognome} - {p.camera.tipo} "
            f"({p.data_inizio.strftime('%Y-%m-%d')} → {p.data_fine.strftime('%Y-%m-%d')}) "
            f"- Totale: €{p.costo_totale:.2f}"
        )
        tk.Label(finestra_storico, text=testo).pack(anchor="w")

def disdici_prenotazione():
    if not prenotazioni:
        messagebox.showwarning("Attenzione", "Nessuna prenotazione disponibile.")
        return

    pren = prenotazioni[-1]  # esempio: disdiciamo l'ultima
    oggi = datetime.now()
    rimborso, stato = pren.calcolo_rimborso(oggi)

    messagebox.showinfo("Disdetta", f"Prenotazione disdetta.\n{stato}\nRimborso: €{rimborso:.2f}")
    prenotazioni.remove(pren)

# ======== FINESTRA PRINCIPALE ========
finestra = tk.Tk()
finestra.title("Sistema Informativo Hotel")
finestra.geometry("450x700")

tk.Label(finestra, text="Dati cliente", font=("Helvetica", 14)).pack()

entry_nome = tk.Entry(finestra)
entry_nome.insert(0, "Nome")
entry_nome.pack()

entry_cognome = tk.Entry(finestra)
entry_cognome.insert(0, "Cognome")
entry_cognome.pack()

entry_cf = tk.Entry(finestra)
entry_cf.insert(0, "Codice Fiscale")
entry_cf.pack()

entry_email = tk.Entry(finestra)
entry_email.insert(0, "Email")
entry_email.pack()

entry_telefono = tk.Entry(finestra)
entry_telefono.insert(0, "Telefono")
entry_telefono.pack()

entry_eta = tk.Entry(finestra)
entry_eta.insert(0, "Età")
entry_eta.pack()

tk.Label(finestra, text="Camera").pack()
camera_var = tk.StringVar(value="singola")
tk.OptionMenu(finestra, camera_var, "singola", "matrimoniale", "suite").pack()

tk.Label(finestra, text="Data inizio (YYYY-MM-DD)").pack()
entry_data_inizio = tk.Entry(finestra)
entry_data_inizio.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
entry_data_inizio.pack()

tk.Label(finestra, text="Data fine (YYYY-MM-DD)").pack()
entry_data_fine = tk.Entry(finestra)
entry_data_fine.insert(0, (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"))
entry_data_fine.pack()

colazione_var = tk.IntVar()
tk.Checkbutton(finestra, text="Colazione (10€/gg)", variable=colazione_var).pack()

# ====== SERVIZI EXTRA (solo per suite) ======
tk.Label(finestra, text="Servizi Extra (solo suite)").pack()
servizio_camera_var = tk.BooleanVar()
tk.Checkbutton(finestra, text="Servizio in camera (30€)", variable=servizio_camera_var).pack()

lavanderia_var = tk.BooleanVar()
tk.Checkbutton(finestra, text="Lavanderia (20€)", variable=lavanderia_var).pack()

tk.Button(finestra, text="Crea prenotazione", command=crea_prenotazione).pack(pady=10)
tk.Button(finestra, text="Mostra storico prenotazioni", command=mostra_storico).pack(pady=5)
tk.Button(finestra, text="Disdici ultima prenotazione", command=disdici_prenotazione).pack(pady=5)

finestra.mainloop()