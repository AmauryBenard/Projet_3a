import numpy as np

# -----------------------
# CONFIGURATION
# -----------------------

real_file = "test_multi.txt"
predicted_file = "predicted_params_multi.txt"

NB_PARAMS = 16
NB_PRESETS_TO_DISPLAY = 5

# -----------------------
# PARSING DES FICHIERS
# -----------------------

def load_presets(file_path):
    """
    Lit un fichier du type :
    preset_002 v1 v2 ... v16 preset_003 v1 v2 ... v16 ...
    Retourne un dict : {preset_name: np.array(params)}
    """
    with open(file_path, "r", encoding="utf-8") as f:
        tokens = f.read().split()

    presets = {}
    i = 0

    while i < len(tokens):
        if tokens[i].startswith("preset_"):
            preset_name = tokens[i]
            params = np.array([float(v) for v in tokens[i+1:i+1+NB_PARAMS]])
            presets[preset_name] = params
            i += 1 + NB_PARAMS
        else:
            i += 1

    return presets

# -----------------------
# MÉTRIQUES
# -----------------------

def compute_metrics(real, predicted):
    mae = np.mean(np.abs(real - predicted))
    rmse = np.sqrt(np.mean((real - predicted) ** 2))
    similarity = max(0.0, 1.0 - mae) * 100.0
    return mae, rmse, similarity

def verdict_from_score(score):
    if score > 90:
        return "Très proche"
    elif score > 75:
        return "Proche"
    elif score > 60:
        return "Moyen"
    else:
        return "Faible"

# -----------------------
# CHARGEMENT
# -----------------------

real_presets = load_presets(real_file)
pred_presets = load_presets(predicted_file)

# normalisation des noms (preset_02 ↔ preset_002)
def normalize(name):
    num = int(name.split("_")[1])
    return f"preset_{num:03d}"

real_presets_norm = {normalize(k): v for k, v in real_presets.items()}
pred_presets_norm = {normalize(k): v for k, v in pred_presets.items()}

common_presets = sorted(set(real_presets_norm.keys()) & set(pred_presets_norm.keys()))

if len(common_presets) == 0:
    print("Aucun preset commun trouvé")
    exit()

# -----------------------
# AFFICHAGE DES 5 PREMIERS
# -----------------------

print("=== COMPARAISON DES 5 PREMIERS PRESETS ===\n")

all_mae = []
all_rmse = []
all_scores = []

for preset_name in common_presets[:NB_PRESETS_TO_DISPLAY]:
    real = real_presets_norm[preset_name]
    pred = pred_presets_norm[preset_name]

    mae, rmse, score = compute_metrics(real, pred)

    print(f"{preset_name}")
    print(f"MAE  : {mae:.6f}")
    print(f"RMSE : {rmse:.6f}")
    print(f"Score: {score:.2f} / 100")
    print(f"Interprétation : {verdict_from_score(score)}\n")

# -----------------------
# ÉVALUATION GLOBALE
# -----------------------

for preset_name in common_presets:
    real = real_presets_norm[preset_name]
    pred = pred_presets_norm[preset_name]

    mae, rmse, score = compute_metrics(real, pred)

    all_mae.append(mae)
    all_rmse.append(rmse)
    all_scores.append(score)

mean_mae = np.mean(all_mae)
mean_rmse = np.mean(all_rmse)
mean_score = np.mean(all_scores)

print("=== ÉVALUATION GLOBALE ===\n")
print(f"Nombre de presets comparés : {len(common_presets)}")
print(f"MAE moyen  : {mean_mae:.6f}")
print(f"RMSE moyen : {mean_rmse:.6f}")
print(f"Score moyen: {mean_score:.2f} / 100")
print(f"Interprétation globale : {verdict_from_score(mean_score)}")
