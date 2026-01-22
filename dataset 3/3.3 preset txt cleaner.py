import re

# -----------------------
# FICHIERS
# -----------------------

deleted_file_path = "deleted_files.txt"
params_input_path = "params_fixed.txt"
params_output_path = "params_fixed_cleaned.txt"

N_PARAMS = 16  # nombre de paramètres par preset

# -----------------------
# 1. LECTURE DES PRESETS SUPPRIMÉS
# -----------------------

deleted_presets = set()

with open(deleted_file_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("preset_") and ".wav" in line:
            preset_name = line.split(".wav")[0]
            deleted_presets.add(preset_name)

print(f"{len(deleted_presets)} presets à supprimer trouvés")

# -----------------------
# 2. LECTURE DU FICHIER PARAMS
# -----------------------

with open(params_input_path, "r", encoding="utf-8") as f:
    tokens = f.read().split()

# -----------------------
# 3. FILTRAGE
# -----------------------

clean_tokens = []
i = 0
removed_count = 0

while i < len(tokens):
    token = tokens[i]

    if token.startswith("preset_"):
        preset_name = token
        preset_block = tokens[i:i + 1 + N_PARAMS]

        if preset_name in deleted_presets:
            removed_count += 1
        else:
            clean_tokens.extend(preset_block)

        i += 1 + N_PARAMS
    else:
        # sécurité au cas où
        i += 1

# -----------------------
# 4. ÉCRITURE DU NOUVEAU FICHIER
# -----------------------

with open(params_output_path, "w", encoding="utf-8") as f:
    f.write(" ".join(clean_tokens))

print("Nettoyage terminé")
print(f"{removed_count} presets supprimés")
print(f"Fichier généré : {params_output_path}")
