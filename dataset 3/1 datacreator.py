import os
import numpy as np
import librosa
import soundfile as sf

# ========================
# PARAMÈTRES
# ========================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
input_wav = os.path.join(SCRIPT_DIR, "input.wav")

output_dir = "presets"
segment_duration = 5.0   # durée de chaque segment en secondes
preset_index = 2

# ========================
# CRÉATION DOSSIER SORTIE
# ========================

os.makedirs(output_dir, exist_ok=True)

# ========================
# CHARGEMENT AUDIO
# ========================

audio, sr = librosa.load(input_wav, sr=None, mono=True)
total_duration = len(audio)/sr
num_segments = int(np.ceil(total_duration / segment_duration))

# ========================
# DÉCOUPAGE FIXE & EXPORT
# ========================

for i in range(num_segments):
    start_sample = int(i * segment_duration * sr)
    end_sample = int(min((i + 1) * segment_duration * sr, len(audio)))

    segment = audio[start_sample:end_sample]

    filename = f"preset_{preset_index:03d}.wav"
    filepath = os.path.join(output_dir, filename)

    sf.write(filepath, segment, sr)
    print(f"Exporté : {filename}")

    preset_index += 1

print("Découpage terminé.")
