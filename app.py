from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sklearn.cluster import KMeans

app = Flask(__name__)
CORS(app)

# Profils de concentration pour entraîner KMeans
donnees_initiales = [
    [3] * 12 + [7],  # Haute concentration
    [2] * 12 + [6],  # Moyenne concentration
    [1] * 12 + [4]  # Faible concentration
]


# Fonction de normalisation
def normaliser(valeurs):
    normalisees = []
    for i, val in enumerate(valeurs):
        if i == 12:
            normalisees.append((val - 4) / 3)  # Dernière question (4-7)
        else:
            normalisees.append((val - 1) / 2)  # Autres questions (1-3)
    return normalisees


# Normaliser les données initiales
donnees_normalisees = [normaliser(v) for v in donnees_initiales]

# Entraîner KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(donnees_normalisees)

# Mapper les clusters aux niveaux
labels_to_levels = {}
for idx, label in enumerate(kmeans.labels_):
    if donnees_initiales[idx][0] == 3:
        labels_to_levels[label] = "élevé"
    elif donnees_initiales[idx][0] == 2:
        labels_to_levels[label] = "moyen"
    else:
        labels_to_levels[label] = "faible"


@app.route('/api/analyser', methods=['POST'])
def analyser():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Données manquantes"}), 400

        valeurs = data.get('valeursConcentration', [])
        print(f"Valeurs reçues: {valeurs}")

        while len(valeurs) < 13:
            valeurs.append(2)
        valeurs = valeurs[:13]

        valeurs_normalisees = normaliser(valeurs)

        # Prédiction avec KMeans
        cluster = kmeans.predict([valeurs_normalisees])[0]
        niveau = labels_to_levels.get(cluster, "inconnu")

        organisation = np.mean(valeurs_normalisees[:4])
        concentration = np.mean(valeurs_normalisees[4:8])
        motivation = np.mean(valeurs_normalisees[8:12])
        score_moyen = np.mean(valeurs_normalisees)

        result = {
            "status": "success",
            "niveau": niveau,
            "cluster_id": int(cluster),
            "score_moyen": float(score_moyen),
            "scores_details": {
                "organisation": float(organisation),
                "concentration": float(concentration),
                "motivation": float(motivation)
            },
            "valeurs_normalisees": [float(x) for x in valeurs_normalisees]
        }

        print(f"Résultat KMeans: {result}")
        return jsonify(result)

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


# Route pour générer l'emploi du temps
@app.route('/api/generate_schedule', methods=['POST'])
def generate_schedule_route():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Données manquantes"}), 400

        print("Données reçues pour la génération d'emploi du temps:", data)

        # Utiliser la fonction de traitement de génération d'emploi du temps

    except Exception as e:
        print(f"Erreur lors de la génération de l'emploi du temps: {str(e)}")
        return jsonify({"error": str(e), "status": "error"}), 500


# Route de test
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "status": "API en ligne",
        "message": "L'API fonctionne correctement"
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)