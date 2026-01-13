import torch
from torch.utils.data import DataLoader
from dataset import AudioParamDataset
from model import AudioToParamsCNN

features_dir = "features"
param_file = "params_fixed.txt"
batch_size = 16
epochs = 50

dataset = AudioParamDataset(features_dir, param_file)
loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

nb_params = len(next(iter(dataset))[1])

model = AudioToParamsCNN(nb_params)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(epochs):
    loss_sum = 0.0

    for x, y in loader:
        pred = model(x)
        loss = criterion(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss_sum += loss.item()

    print(f"Epoch {epoch+1} | Loss: {loss_sum/len(loader):.6f}")


# ---- Sauvegarde du modèle après entraînement ----
torch.save(model.state_dict(), "audio_to_params.pth")
print("Modèle sauvegardé dans audio_to_params.pth")



