import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# === Chargement des données ===
chemin_fichier = "donnees/creditcard.csv"  
df = pd.read_csv(chemin_fichier)

# === Préparation des données ===
X = df.drop(['Class', 'Time'], axis=1)  # On enlève 'Class' (target) et 'Time' (inutile pour le modèle)
y = df['Class']  # Cible : 1 = fraude, 0 = normal

# === Séparation entraînement / test ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === Entraînement du modèle ===
clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced'  # Gère le déséquilibre de classe
)
clf.fit(X_train, y_train)

# === Évaluation ===
y_pred = clf.predict(X_test)
print(" Rapport de classification :\n")
print(classification_report(y_test, y_pred))

# === Sauvegarde du modèle ===
os.makedirs('modeles', exist_ok=True)
joblib.dump(clf, 'modeles/modele_fraude.pkl')
print("Modèle sauvegardé dans : modeles/modele_fraude.pkl")
