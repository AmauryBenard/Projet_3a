import numpy as np

def parse_input(prompt):
    """
    Demande une suite de nombres séparés par des espaces
    et la convertit en tableau numpy
    """
    values = input(prompt)
    try:
        array = np.array([float(v) for v in values.strip().split()])
        return array
    except ValueError:
        print("Erreur : veuillez entrer uniquement des nombres séparés par des espaces.")
        return None

def main():
    print("=== Comparaison de paramètres audio ===\n")

    real_params = parse_input("Entrez les paramètres RÉELS :\n> ")
    if real_params is None:
        return

    predicted_params = parse_input("\nEntrez les paramètres PRÉDITS :\n> ")
    if predicted_params is None:
        return

    if len(real_params) != len(predicted_params):
        print("\nErreur : les deux suites n'ont pas la même longueur.")
        print(f"Réels : {len(real_params)} | Prédits : {len(predicted_params)}")
        return

    # Calculs d'erreur
    mae = np.mean(np.abs(real_params - predicted_params))
    rmse = np.sqrt(np.mean((real_params - predicted_params) ** 2))

    # Score de similarité (0–100)
    similarity_score = max(0.0, 1.0 - mae) * 100.0

    print("\n=== Résultats ===")
    print(f"MAE  (erreur moyenne absolue) : {mae:.6f}")
    print(f"RMSE (erreur quadratique)     : {rmse:.6f}")
    print(f"Score de ressemblance         : {similarity_score:.2f} / 100")

    # Interprétation simple
    if similarity_score > 90:
        verdict = "Très proche"
    elif similarity_score > 75:
        verdict = "Proche"
    elif similarity_score > 60:
        verdict = "Moyen"
    else:
        verdict = "Faible"

    print(f"Interprétation : {verdict}")

if __name__ == "__main__":
    main()
