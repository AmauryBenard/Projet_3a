import os
import numpy as np
import librosa

# ========================
# PARAMÈTRES
# ========================

input_dir = "presets"              # dossier des wav découpés
output_dir = "features"            # dossier des features
sr_target = 22050                  # fréquence cible
n_mels = 128                       # nombre de bandes Mel
n_fft = 2048
hop_length = 512
max_frames = 256                   # taille temporelle fixe

# ========================
# DOSSIER SORTIE
# ========================

os.makedirs(output_dir, exist_ok=True)

# ========================
# FONCTION UTILE
# ========================

def fix_length(spec, max_frames):
    """Pad ou coupe pour obtenir une taille fixe"""
    if spec.shape[1] < max_frames:
        pad_width = max_frames - spec.shape[1]
        spec = np.pad(spec, ((0, 0), (0, pad_width)), mode='constant')
    else:
        spec = spec[:, :max_frames]
    return spec

# ========================
# TRAITEMENT DES PRESETS
# ========================

for filename in sorted(os.listdir(input_dir)):
    if not filename.endswith(".wav"):
        continue

    filepath = os.path.join(input_dir, filename)

    # Chargement audio
    audio, sr = librosa.load(filepath, sr=sr_target, mono=True)

    # Mel-spectrogramme
    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0
    )

    # Log-Mel
    mel_db = librosa.power_to_db(mel, ref=np.max)

    # Taille fixe
    mel_db = fix_length(mel_db, max_frames)

    # Normalisation (important pour ML)
    mel_db = (mel_db - mel_db.mean()) / (mel_db.std() + 1e-8)

    # Sauvegarde
    preset_id = filename.replace(".wav", "")
    out_path = os.path.join(output_dir, preset_id + ".npy")

    np.save(out_path, mel_db)

    print(f"Features extraites : {preset_id}")

print("Extraction terminée.")
