import requests
import json
from datetime import datetime, timezone

# URL fournie par Power BI
url = (
    "https://api.powerbi.com/beta/78613bf0-3424-4615-9325-8f6a7d76a04a/datasets/775c9490-9ac3-4cde-b404-6b4ab12d8749/rows?experience=power-bi&key=snXApx7PieoiY4t0bXuktMDVyMDNLazojFQbt%2FsAA3JiH442lC4vHPTlKspYk7GAJzucUK%2BQSHg1WQ3LJeEhHw%3D%3D"
)

# Exemple de données prédictives à envoyer
data = [
    {
        "amount": 98.6,
        "v1": 0.42,
        "v2": -1.23,
        "prediction": 1,  # 1 = fraude, 0 = normal
        "horodatage": datetime.now(timezone.utc).isoformat()
    }
]

# Envoi de la requête POST
response = requests.post(
    url,
    headers={"Content-Type": "application/json"},
    data=json.dumps(data)
)

# Affichage du résultat
if response.status_code == 200:
    print(" Données envoyées avec succès à Power BI.")
else:
    print(f" Échec de l’envoi : {response.status_code} - {response.text}")
