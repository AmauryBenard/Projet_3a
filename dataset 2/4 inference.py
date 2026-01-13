# inference.py

import torch
import librosa
import numpy as np
from model import AudioToParamsCNN  # assure-toi que model.py est dans le même dossier

# ----------- CONFIGURATION ----------- #
audio_file = "test.wav"            # fichier audio d'entrée
model_file = "audio_to_params.pth" # modèle entraîné
output_file = "predicted_params.txt"
sr_target = 22050
nb_params = 16                      # nombre de paramètres par preset
n_mels = 128
n_fft = 2048
hop_length = 512
target_length = 256                # longueur fixe pour le Mel (doit être la même que pour l'entraînement)

# ----------- CHARGEMENT DU MODELE ----------- #
model = AudioToParamsCNN(nb_params)
model.load_state_dict(torch.load(model_file))
model.eval()

# ----------- FONCTION DE PRÉTRAITEMENT ----------- #

def fix_length(spec, max_frames):
    """Pad ou coupe pour obtenir une taille fixe"""
    if spec.shape[1] < max_frames:
        pad_width = max_frames - spec.shape[1]
        spec = np.pad(spec, ((0, 0), (0, pad_width)), mode='constant')
    else:
        spec = spec[:, :max_frames]
    return spec

def preprocess_audio(file_path):
    # Chargement audio
    y, sr = librosa.load(file_path, sr=sr_target, mono=True)
    
    # Mel-spectrogramme
    mel_spec = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0
    )
    
    # Log-Mel
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    # Taille fixe
    mel_spec_db = fix_length(mel_spec_db, target_length)
    
    # Normalisation (comme à l'entraînement)
    mel_spec_db = (mel_spec_db - mel_spec_db.mean()) / (mel_spec_db.std() + 1e-8)
    
    # Conversion en tenseur PyTorch
    feature = torch.tensor(mel_spec_db, dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # (1,1,128,T)
    
    return feature

# ----------- PRÉDICTION ----------- #
feature = preprocess_audio(audio_file)
with torch.no_grad():
    predicted_params = model(feature).squeeze().numpy()

# ----------- ÉCRITURE DANS LE FICHIER ----------- #
with open(output_file, "w") as f:
    f.write(" ".join([f"{p:.6f}" for p in predicted_params]))

print(f"Paramètres prédits écrits dans {output_file}")
print(predicted_params)
