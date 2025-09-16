import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Chargement des données
df = pd.read_csv("donnees/creditcardfraude.csv")

# Séparation features / target
X = df.drop(['Class', 'Time'], axis=1)
y = df['Class']

# Split train / test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Appliquer SMOTE pour équilibrer les classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Entraînement du modèle
clf = RandomForestClassifier(n_estimators=30, random_state=42)
clf.fit(X_resampled, y_resampled)

# Évaluation
y_pred = clf.predict(X_test)
print("Rapport de classification :\n")
print(classification_report(y_test, y_pred, target_names=["Normal", "Fraude"]))

# Sauvegarde
os.makedirs("modeles", exist_ok=True)
joblib.dump(clf, "modeles/modele_fraude_equilibre.pkl")
print("Modèle équilibré sauvegardé dans modeles/modele_fraude_equilibre.pkl")