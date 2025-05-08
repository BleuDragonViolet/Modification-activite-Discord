import os
import tkinter as tk
from tkinter import ttk
from pypresence import Presence
import subprocess
import threading
import time
import unicodedata

def nettoyer_description(description):
    # Supprime les caractères de contrôle invisibles
    return ''.join(c for c in description if unicodedata.category(c)[0] != 'C')


# Configuration Discord
CLIENT_ID = "-"
IMAGE_KEY = "logo"

# Connexion à Discord RPC
try:
    rpc = Presence(CLIENT_ID)
    rpc.connect()
    rpc.update(
        state="Prêt à recevoir une description...",
        details="Générateur EXE + Discord Presence",
        large_image=IMAGE_KEY,
        large_text="Mon application personnalisée"
    )
except Exception as e:
    print(f"Erreur de connexion à Discord RPC : {e}")

# Met à jour la présence Discord
def mettre_a_jour_presence():
    brut = description_texte.get("1.0", tk.END).strip()
    lignes = brut.splitlines()

    # Nettoyer + limiter à 4 lignes max
    lignes_nettoyees = [l.strip() for l in lignes if l.strip()]
    lignes_limitees = lignes_nettoyees[:4]

    # Joindre avec un séparateur visuel
    description_formatee = " · ".join(lignes_limitees)

    try:
        rpc.update(
            state=f"{description_formatee}",
            large_image=IMAGE_KEY,
            large_text="IdleMasterX"
        )
        result_label.config(text="Présence Discord mise à jour.")
    except Exception as e:
        result_label.config(text=f"Erreur RPC : {e}")


# Fonction de génération EXE
def generer_exe():
    def tache():
        nom_app = nom_app_var.get().strip() or "vide"
        description = description_texte.get("1.0", tk.END).strip()
        description = nettoyer_description(description)  # ✅ Nettoyage après récupération

        if not description:
            result_label.config(text="Veuillez écrire une description.")
            return

        script_content = f'''
import time

try:
    while True:
        print("""{description}""")
        time.sleep(10)
except KeyboardInterrupt:
    print("Arrêt du faux statut.")
'''

        # Écriture avec encodage UTF-8
        with open("temp_script.py", "w", encoding="utf-8") as f:
            f.write(script_content)

        progress_bar['value'] = 0
        for i in range(50):
            progress_bar['value'] += 2
            fenetre.update()
            time.sleep(0.02)

        cmd = [
            "pyinstaller",
            "--onefile",
            f"--name={nom_app}",
            "temp_script.py"
        ]

        result_label.config(text="Génération en cours...")
        subprocess.run(cmd)

        os.remove("temp_script.py")
        progress_bar['value'] = 100
        fenetre.update()

        result_label.config(text=f"EXE généré : dist/{nom_app}.exe")
        progress_bar['value'] = 0

    threading.Thread(target=tache).start()



# Lancer l'EXE généré
def lancer_exe():
    nom_app = nom_app_var.get().strip() or "vide"
    exe_path = os.path.join("dist", f"{nom_app}.exe")
    if os.path.exists(exe_path):
        subprocess.Popen([exe_path])
        result_label.config(text=f"EXE lancé : {exe_path}")
    else:
        result_label.config(text="Aucun EXE trouvé. Générez-le d'abord.")

# Aide déroulante
def afficher_aide():
    if aide_visible.get():
        aide_frame.pack_forget()
        fenetre.geometry("550x400")
        aide_visible.set(False)
    else:
        aide_frame.pack(pady=10, fill="both", expand=True)
        fenetre.geometry("550x700")
        aide_visible.set(True)

# Interface graphique
fenetre = tk.Tk()
fenetre.title("Générateur Discord EXE")
fenetre.geometry("550x400")
fenetre.configure(bg="#1e1e2e")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#1e1e2e", foreground="#d4d4d8", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("TEntry", font=("Segoe UI", 10))
style.configure("TProgressbar", troughcolor="#313244", background="#89b4fa", thickness=15)

nom_app_var = tk.StringVar()
aide_visible = tk.BooleanVar(value=False)

# Champs
ttk.Label(fenetre, text="Nom esthétique de l'application (optionnel) :").pack(pady=5)
ttk.Entry(fenetre, textvariable=nom_app_var, width=40).pack(pady=5)

ttk.Label(fenetre, text="Description (affichée dans Discord) :").pack(pady=5)
description_texte = tk.Text(fenetre, height=5, width=50, wrap="word")
description_texte.pack(pady=5)

# Progress bar
ttk.Label(fenetre, text="Progression de la génération :").pack(pady=(10, 0))
progress_bar = ttk.Progressbar(fenetre, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=5)

# Boutons sur la même ligne
boutons_frame = tk.Frame(fenetre, bg="#1e1e2e")
boutons_frame.pack(pady=10)

ttk.Button(boutons_frame, text="Générer l'EXE", command=generer_exe).pack(side="left", padx=5)
ttk.Button(boutons_frame, text="Lancer l'EXE", command=lancer_exe).pack(side="left", padx=5)
ttk.Button(boutons_frame, text="Actualiser Presence", command=mettre_a_jour_presence).pack(side="left", padx=5)

# Instructions
aide_frame = tk.Frame(fenetre, bg="#313244", bd=2, relief="groove")
instructions = (
    "🔧 Instructions mises à jour :\n\n"
    "1. Installe les dépendances :\n"
    "   pip install pypresence pyinstaller pillow\n\n"
    "2. Va sur : https://discord.com/developers/applications\n"
    "3. Crée une application, note son Application ID et remplace CLIENT_ID dans le code.\n\n"
    "4. Onglet 'Rich Presence' > 'Art Assets' :\n"
    "   - Upload une image (min. 512x512), nomme-la : logo\n\n"
    "5. Lance ce programme.\n"
    "6. Nom esthétique : facultatif, donne juste un nom au fichier .exe\n"
    "7. Description : contenu affiché dans ta présence Discord (multi-ligne autorisée).\n"
    "8. Utilise les boutons pour générer, lancer ou mettre à jour Discord Presence à tout moment."
)

aide_texte = tk.Label(aide_frame, text=instructions, bg="#313244", fg="#cdd6f4", justify="left", wraplength=500, anchor="w", font=("Segoe UI", 9))
aide_texte.pack(padx=10, pady=10, fill="both", expand=True)

# Zone de résultat
result_label = tk.Label(fenetre, text="", bg="#1e1e2e", fg="#d4d4d8", font=("Segoe UI", 10, "italic"))
result_label.pack(pady=10)

ttk.Button(fenetre, text="Afficher les instructions", command=afficher_aide).pack(pady=10)

fenetre.mainloop()
