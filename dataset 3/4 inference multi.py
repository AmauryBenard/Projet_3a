import torch
import librosa
import numpy as np
from model import AudioToParamsCNN

# ----------- CONFIGURATION ----------- #

input_audio_file = "test_multi.wav"          # audio long (ex: 250 sec)
model_file = "audio_to_params_30.pth"
output_file = "predicted_params_multi.txt"

sr_target = 22050
segment_duration = 5.0                       # durée d'un preset en secondes
start_preset_index = 2                       # numéro de départ (preset_02)

nb_params = 16
n_mels = 128
n_fft = 2048
hop_length = 512
target_length = 256

# ----------- CHARGEMENT DU MODÈLE ----------- #

model = AudioToParamsCNN(nb_params)
model.load_state_dict(torch.load(model_file, map_location="cpu"))
model.eval()

# ----------- OUTILS ----------- #

def fix_length(spec, max_frames):
    if spec.shape[1] < max_frames:
        pad_width = max_frames - spec.shape[1]
        spec = np.pad(spec, ((0, 0), (0, pad_width)), mode="constant")
    else:
        spec = spec[:, :max_frames]
    return spec

def preprocess_audio_segment(y):
    mel_spec = librosa.feature.melspectrogram(
        y=y,
        sr=sr_target,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0
    )

    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_spec_db = fix_length(mel_spec_db, target_length)

    mel_spec_db = (mel_spec_db - mel_spec_db.mean()) / (mel_spec_db.std() + 1e-8)

    feature = torch.tensor(
        mel_spec_db, dtype=torch.float32
    ).unsqueeze(0).unsqueeze(0)  # (1,1,128,T)

    return feature

# ----------- CHARGEMENT AUDIO ----------- #

audio, sr = librosa.load(input_audio_file, sr=sr_target, mono=True)

samples_per_segment = int(segment_duration * sr_target)
total_segments = len(audio) // samples_per_segment

print(f"{total_segments} segments détectés")

# ----------- INFÉRENCE ----------- #

preset_index = start_preset_index
all_outputs = []

with torch.no_grad():
    for i in range(total_segments):
        start = i * samples_per_segment
        end = start + samples_per_segment

        segment = audio[start:end]

        if len(segment) < samples_per_segment:
            continue

        feature = preprocess_audio_segment(segment)
        predicted_params = model(feature).squeeze().numpy()

        preset_name = f"preset_{preset_index:03d}"
        params_str = " ".join([f"{p:.6f}" for p in predicted_params])

        all_outputs.append(f"{preset_name} {params_str}")

        preset_index += 1

# ----------- ÉCRITURE FICHIER ----------- #

with open(output_file, "w", encoding="utf-8") as f:
    f.write(" ".join(all_outputs))

print(f"Inférence terminée")
print(f"Fichier généré : {output_file}")
print(f"{len(all_outputs)} presets écrits")
