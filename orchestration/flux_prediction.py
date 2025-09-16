from kafka import KafkaConsumer
import joblib
import json
import numpy as np
import requests
from datetime import datetime, timezone

# Chargement du modèle équilibré
model = joblib.load("modeles/modele_fraude_equilibre.pkl")

# Kafka Consumer
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# URL vers Power BI
powerbi_url = "https://api.powerbi.com/beta/78613bf0-3424-4615-9325-8f6a7d76a04a/datasets/775c9490-9ac3-4cde-b404-6b4ab12d8749/rows?experience=power-bi&key=snXApx7PieoiY4t0bXuktMDVyMDNLazojFQbt%2FsAA3JiH442lC4vHPTlKspYk7GAJzucUK%2BQSHg1WQ3LJeEhHw%3D%3D"

# Variables utilisées pour la prédiction
features_used = ["V4", "V10", "V14", "V12", "V11", "V17", "V7", "V3", "V16", "V2", "Amount"]

print("Consommateur Kafka démarré. En attente de messages...")

for msg in consumer:
    ligne = msg.value

    try:
        # Extraire les features
        features = [float(ligne[f]) for f in features_used]
        features_array = np.array([features])

        # Obtenir la prédiction et la probabilité
        prediction = model.predict(features_array)[0]
        proba = model.predict_proba(features_array)[0][1]  # Probabilité que ce soit une fraude

        print(f"\n🔍 Prédiction: {'FRAUDE' if prediction == 1 else 'OK'} | Probabilité = {proba:.4f}")

        # Construction du message pour Power BI
        payload = [{
            "v4": float(ligne["V4"]),
            "v10": float(ligne["V10"]),
            "v14": float(ligne["V14"]),
            "v12": float(ligne["V12"]),
            "v11": float(ligne["V11"]),
            "v17": float(ligne["V17"]),
            "v7": float(ligne["V7"]),
            "v3": float(ligne["V3"]),
            "v16": float(ligne["V16"]),
            "v2": float(ligne["V2"]),
            "amount": float(ligne["Amount"]),
            "prediction": int(prediction),
            "proba_fraude": round(float(proba), 4),
            "horodatage": datetime.now(timezone.utc).isoformat()
        }]

        # Envoi vers Power BI
        res = requests.post(powerbi_url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        print(f"Données envoyées à Power BI | Status: {res.status_code}")

    except Exception as e:
        print(f" Erreur lors du traitement de la ligne : {ligne} | Erreur : {e}")
