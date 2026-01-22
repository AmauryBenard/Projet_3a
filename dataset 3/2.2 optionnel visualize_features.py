import os
import numpy as np
import matplotlib.pyplot as plt

# ========================
# PARAMÈTRES
# ========================

features_dir = "features"   # dossier contenant les .npy
nb_to_show = 5              # nombre de presets à afficher

# ========================
# LISTE DES FICHIERS
# ========================

files = sorted([
    f for f in os.listdir(features_dir)
    if f.endswith(".npy")
])[:nb_to_show]

if len(files) == 0:
    raise RuntimeError("Aucun fichier .npy trouvé")

# ========================
# AFFICHAGE
# ========================

for i, filename in enumerate(files):
    path = os.path.join(features_dir, filename)
    feature = np.load(path)

    plt.figure(figsize=(8, 4))
    plt.imshow(
        feature,
        aspect="auto",
        origin="lower"
    )
    plt.colorbar(label="Amplitude (normalisée)")
    plt.title(f"{filename}")
    plt.xlabel("Temps (frames)")
    plt.ylabel("Bandes Mel")
    plt.tight_layout()
    plt.show()
