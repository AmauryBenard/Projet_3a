import librosa
import numpy as np
from scipy.spatial.distance import cosine

# ========================
# PARAMÈTRES
# ========================

sr_target = 22050
n_mels = 128
n_fft = 2048
hop_length = 512
max_frames = 256


# ========================
# OUTILS
# ========================

def fix_length(spec, max_frames):
    if spec.shape[1] < max_frames:
        pad = max_frames - spec.shape[1]
        spec = np.pad(spec, ((0, 0), (0, pad)), mode="constant")
    else:
        spec = spec[:, :max_frames]
    return spec


def extract_mel_features(wav_path):
    y, sr = librosa.load(wav_path, sr=sr_target, mono=True)

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0
    )

    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = fix_length(mel_db, max_frames)

    # normalisation identique à ton entraînement
    mel_db = (mel_db - mel_db.mean()) / (mel_db.std() + 1e-8)

    return mel_db


# ========================
# COMPARAISON
# ========================

def compare_audio(audio_ref, audio_pred):
    feat_ref = extract_mel_features(audio_ref)
    feat_pred = extract_mel_features(audio_pred)

    # Erreur spectrale moyenne (L1)
    l1_error = np.mean(np.abs(feat_ref - feat_pred))

    # Similarité cosinus
    cosine_sim = 1.0 - cosine(feat_ref.flatten(), feat_pred.flatten())

    # Score global (pondéré)
    similarity_score = (
        0.6 * (1.0 / (1.0 + l1_error)) +
        0.4 * max(0.0, cosine_sim)
    ) * 100.0

    return l1_error, cosine_sim, similarity_score


# ========================
# MAIN
# ========================

def main():
    print("=== Comparaison audio entre deux presets ===\n")

    audio_ref = input("Chemin vers l'audio RÉFÉRENCE (.wav) :\n> ").strip()
    audio_pred = input("\nChemin vers l'audio PRÉDIT (.wav) :\n> ").strip()

    l1, cos_sim, score = compare_audio(audio_ref, audio_pred)

    print("\n=== Résultats ===")
    print(f"Erreur spectrale moyenne (L1) : {l1:.6f}")
    print(f"Similarité cosinus            : {cos_sim:.4f}")
    print(f"Score de ressemblance audio   : {score:.2f} / 100")

    if score > 85:
        verdict = "Très proche perceptivement"
    elif score > 70:
        verdict = "Proche"
    elif score > 55:
        verdict = "Moyennement proche"
    else:
        verdict = "Peu similaire"

    print(f"Interprétation : {verdict}")


if __name__ == "__main__":
    main()
