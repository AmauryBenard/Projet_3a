import os
import numpy as np
import soundfile as sf

# -----------------------
# PARAMÈTRES
# -----------------------

audio_folder = "presets"     # dossier contenant les wav
log_file = "deleted_files.txt"

rms_threshold = 1e-4        # SEUIL À AJUSTER
eps = 1e-9

# -----------------------
# FONCTIONS
# -----------------------

def rms(signal):
    return np.sqrt(np.mean(signal**2) + eps)

# -----------------------
# TRAITEMENT
# -----------------------

deleted_files = []

for filename in os.listdir(audio_folder):
    if not filename.lower().endswith(".wav"):
        continue

    filepath = os.path.join(audio_folder, filename)

    try:
        audio, sr = sf.read(filepath)
    except Exception as e:
        print(f"Erreur lecture {filename} : {e}")
        continue

    # Mono ou stéréo
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    audio_rms = rms(audio)

    if audio_rms < rms_threshold:
        os.remove(filepath)
        deleted_files.append(f"{filename} | RMS = {audio_rms:.6e}")
        print(f"SUPPRIMÉ : {filename} (RMS={audio_rms:.2e})")
    else:
        print(f"OK       : {filename} (RMS={audio_rms:.2e})")

# -----------------------
# LOG
# -----------------------

with open(log_file, "w", encoding="utf-8") as f:
    f.write("Fichiers audio supprimés (inaudibles)\n")
    f.write("===================================\n\n")
    for name in deleted_files:
        f.write(name + "\n")

print("\nNettoyage terminé.")
print(f"{len(deleted_files)} fichiers supprimés.")
print(f"Log sauvegardé dans : {log_file}")
