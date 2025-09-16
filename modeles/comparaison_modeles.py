import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, f1_score
import joblib
import os

# Chargement des données
df = pd.read_csv("donnees/creditcard.csv")

# Variables les plus importantes
features_used = ["V4", "V10", "V14", "V12", "V11", "V17", "V7", "V3", "V16", "V2", "Amount"]

# Préparation des données
X = df[features_used]
y = df['Class']

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Liste des modèles à tester
modeles = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced'),
    "Decision Tree": DecisionTreeClassifier(class_weight='balanced', random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
}

meilleur_modele = None
meilleur_score = 0

print("\n Évaluation des modèles avec variables importantes :\n")

for nom, modele in modeles.items():
    print(f"--- {nom} ---")
    modele.fit(X_train, y_train)
    y_pred = modele.predict(X_test)
    rapport = classification_report(y_test, y_pred, target_names=["Normal", "Fraude"])
    print(rapport)

    f1_fraude = f1_score(y_test, y_pred, pos_label=1)
    if f1_fraude > meilleur_score:
        meilleur_score = f1_fraude
        meilleur_modele = (nom, modele)
    
    print("\n")

# Sauvegarde du meilleur modèle
if meilleur_modele:
    nom, modele = meilleur_modele
    os.makedirs("modeles", exist_ok=True)
    joblib.dump(modele, "modeles/meilleur_modele.pkl")
    print(f"Meilleur modèle : {nom} (F1-score fraude = {meilleur_score:.4f})")
    print("Modèle sauvegardé dans : modeles/meilleur_modele.pkl")
