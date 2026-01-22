import re

# Fichier d'entrée et sortie
input_file = "params.txt"
output_file = "params_fixed.txt"

# Lire le contenu
with open(input_file, "r") as f:
    content = f.read()

# Fonction pour remplacer preset_XX par preset_0XX si XX < 100
def fix_preset(match):
    num = int(match.group(1))
    return f"preset_{num:03d}"

# Regex pour trouver preset suivi de nombres
pattern = re.compile(r"preset_(\d+)")

# Remplacement
fixed_content = pattern.sub(fix_preset, content)

# Écrire dans le nouveau fichier
with open(output_file, "w") as f:
    f.write(fixed_content)

print(f"Fichier corrigé enregistré sous {output_file}")
