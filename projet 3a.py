import tkinter as tk
from tkinter import ttk
import random

# --- Paramètres du synthé (exemple) ---
SYNTH_PARAMETERS = [
    "Cutoff", "Resonance", "Attack", "Decay", "Sustain",
    "Release", "Mix", "Delay", "Reverb", "Distortion"
]

# --- Fonction pour générer une seed aléatoire ---
def generate_seed(length=10):
    return "".join(str(random.randint(0, 9)) for _ in range(length))

# --- Fonction pour analyser la seed ---
def analyze_seed(seed):
    results = []
    for i, char in enumerate(seed):
        if i < len(SYNTH_PARAMETERS):
            param_name = SYNTH_PARAMETERS[i]
        else:
            param_name = f"ExtraParam{i+1}"
        value = int(char)
        results.append((param_name, value))
    return results

# --- Callback pour le bouton "Générer" ---
def on_generate():
    seed = generate_seed()
    seed_entry.delete(0, tk.END)
    seed_entry.insert(0, seed)
    on_analyze()

# --- Callback pour le bouton "Analyser" ---
def on_analyze():
    seed = seed_entry.get().strip()
    if not seed.isdigit():
        output_text.set("Erreur : la seed doit être une suite de chiffres.")
        return
    analysis = analyze_seed(seed)
    result_lines = [f"{name}: {val}" for name, val in analysis]
    output_text.set("\n".join(result_lines))

# --- Interface graphique ---
root = tk.Tk()
root.title("Seed Synth Generator")

mainframe = ttk.Frame(root, padding=20)
mainframe.grid(row=0, column=0, sticky="NSEW")

# Champ pour entrer ou générer la seed
ttk.Label(mainframe, text="Seed :").grid(row=0, column=0, sticky="W")
seed_entry = ttk.Entry(mainframe, width=30)
seed_entry.grid(row=0, column=1, padx=5)

generate_button = ttk.Button(mainframe, text="Générer aléatoirement", command=on_generate)
generate_button.grid(row=0, column=2, padx=5)

analyze_button = ttk.Button(mainframe, text="Analyser", command=on_analyze)
analyze_button.grid(row=0, column=3, padx=5)

# Zone d'affichage des résultats
output_text = tk.StringVar()
output_label = ttk.Label(mainframe, textvariable=output_text, justify="left", font=("Courier", 10))
output_label.grid(row=1, column=0, columnspan=4, pady=15, sticky="W")

root.mainloop()
