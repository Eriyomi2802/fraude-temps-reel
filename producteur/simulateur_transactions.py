import csv
import time
from kafka import KafkaProducer
import json

# Initialisation du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Chemin complet vers le fichier CSV
fichier = "C:/Users/aldio/OneDrive/Bureau/fraude-temps-reel/donnees/creditcardfraude.csv"

# Paramètre de vitesse (200 lignes / minute = 0.3 sec / ligne)
vitesse_envoi = 500 # lignes par minute
intervalle = 60 / vitesse_envoi  # en secondes

# Lecture et envoi ligne par ligne
with open(fichier, newline='') as csvfile:
    lecteur = csv.DictReader(csvfile)
    for ligne in lecteur:
        producer.send('transactions', ligne)
        print(f" Envoyé : {ligne}")
        time.sleep(intervalle)

producer.flush()
