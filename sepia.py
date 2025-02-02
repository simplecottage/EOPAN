from tkinter import Tk, Label
from SimConnect import SimConnect, AircraftRequests
import threading
import time

# https://docs.flightsimulator.com/html/Programming_Tools/SimVars/Aircraft_SimVars/Aircraft_Engine_Variables.htm#ENG%20N1%20RPM

sm = SimConnect()
requests = AircraftRequests(sm)

def update_heading(label):
    while True:
        try:
            heading = requests.get("PLANE_ALTITUDE")
            vario = requests.get("VERTICAL_SPEED")
            rpm = requests.get("GENERAL_ENG_RPM:1")
            if heading is None:
                label.config(text="Erreur : Donnée manquante")
            else:
                label.config(text=f"alt:{heading:.1f},var:{vario:.1f}\nrpm:{rpm:.0f}")
        except Exception as e:
            label.config(text=f"Erreur de connexion : {e}")
        time.sleep(0.5)

root = Tk()
root.geometry("400x100+100+100")
root.title("Overlay MSFS2024")
root.attributes("-topmost", True)
root.overrideredirect(True)

label = Label(root, text="Connexion à MSFS...", font=("Arial", 16), bg="black", fg="white", padx=10, pady=10)
label.pack(fill="both", expand=True)

# 4. thread pour ne pas bloquer l'interface avec la mise à jour du cap
thread = threading.Thread(target=update_heading, args=(label,), daemon=True)
thread.start()

root.mainloop()
