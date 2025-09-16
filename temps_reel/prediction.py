import json
import pickle
import pandas as pd
from kafka import KafkaConsumer

# Chargement du modèle équilibré
with open('modeles/modele_fraude_equilibre.pkl', 'rb') as f:
    modele = pickle.load(f)

# Initialisation du consommateur Kafka
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Préparation des données
def preprocess(ligne):
    df = pd.DataFrame([ligne])
    df = df.drop(columns=['Time', 'Class'], errors='ignore')
    df = df.astype(float)
    return df

# Consommation et prédiction
for message in consumer:
    data = message.value
    try:
        features = preprocess(data)
        prediction = modele.predict(features)[0]
        print(f"Transaction prédite : {'FRAUDE' if prediction == 1 else 'Normale'} → {data}")
    except Exception as e:
        print(f"Erreur de traitement: {e}")
