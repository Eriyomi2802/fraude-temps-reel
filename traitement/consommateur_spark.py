from kafka import KafkaConsumer
import json
import csv
import os

# Configuration
TOPIC = "transactions"
OUTPUT_FILE = "donnees/transactions_consommees.csv"
os.makedirs("donnees", exist_ok=True)

# Initialisation du consommateur Kafka
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Initialisation du fichier CSV
first = True
with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
    writer = None

    for message in consumer:
        data = message.value

        if first:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writeheader()
            first = False

        writer.writerow(data)
        print(f"Consommé : {data}")
