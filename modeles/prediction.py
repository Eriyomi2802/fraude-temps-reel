import pickle
import json
import psycopg2
import numpy as np
from datetime import datetime
from kafka import KafkaConsumer

# Chargement du modèle
with open("modeles/modele_fraude.pkl", "rb") as f:
    modele = pickle.load(f)

# Connexion à PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="fraude_db",
    user="aldiouma",
    password="aldiouma123"
)
cursor = conn.cursor()

# Initialisation du consommateur Kafka
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fraude-consumer'
)

print(" En attente de messages Kafka...")

for message in consumer:
    donnee = message.value
    try:
        # Préparation des features (exclure Time, Amount si non utilisées dans l'entraînement)
        features = [float(donnee[col]) for col in donnee if col not in ["Time", "Amount", "Class"]]
        features_array = np.array(features).reshape(1, -1)

        # Prédiction
        prediction = int(modele.predict(features_array)[0])
        print(f"Prédiction : {prediction} | Montant : {donnee['Amount']}")

        # Insertion dans PostgreSQL
        cursor.execute(
            """
            INSERT INTO predictions (time, amount, prediction, prediction_date)
            VALUES (%s, %s, %s, %s)
            """,
            (
                int(float(donnee["Time"])),
                float(donnee["Amount"]),
                prediction,
                datetime.now()
            )
        )
        conn.commit()

    except Exception as e:
        print(f"Erreur de traitement : {e}")
