import os
import numpy as np
import torch
from torch.utils.data import Dataset

class AudioParamDataset(Dataset):
    def __init__(self, features_dir, param_file):
        self.features_dir = features_dir
        self.params = {}

        # Charger tout le fichier en une seule fois
        with open(param_file, "r") as f:
            tokens = f.read().split()  # sépare tous les mots/nombres

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith("preset_"):  # début d'un preset
                name = token
                values = []
                i += 1
                # On lit tous les nombres jusqu'au prochain preset ou fin
                while i < len(tokens) and not tokens[i].startswith("preset_"):
                    try:
                        values.append(float(tokens[i]))
                    except ValueError:
                        pass
                    i += 1
                self.params[name] = values
            else:
                i += 1

        self.files = sorted(self.params.keys())

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        name = self.files[idx]

        # Charger le feature correspondant
        feature = np.load(os.path.join(self.features_dir, name + ".npy"))
        feature = torch.tensor(feature, dtype=torch.float32).unsqueeze(0)

        target = torch.tensor(self.params[name], dtype=torch.float32)

        return feature, target
