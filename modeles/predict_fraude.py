import joblib
import numpy as np
from kafka import KafkaConsumer
import json

# Chargement du modèle ML
modele = joblib.load("modeles/modele_fraude_equilibre.pkl")

# Champs à utiliser (ce sont ceux du dataset, sauf "Time", "Amount", "Class")
features = [f"V{i}" for i in range(1, 29)] + ["Amount"]

# Initialisation du consommateur
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

for message in consumer:
    donnees = message.value

    try:
        # Création du vecteur d'entrée
        x = np.array([[float(donnees[feature]) for feature in features]])

        # Prédiction
        prediction = modele.predict(x)[0]
        proba = modele.predict_proba(x)[0][1]  # probabilité d’être fraude

        print(f"Prédiction : {'FRAUDE' if prediction == 1 else 'OK'} (proba = {proba:.2f})")
    except Exception as e:
        print(f"Erreur traitement : {e}")
