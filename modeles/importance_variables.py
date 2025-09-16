import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Chargement du modèle
model = joblib.load("modeles/meilleur_modele.pkl")

# Les noms des colonnes (sans Time ni Class)
features = [f"V{i}" for i in range(1, 29)] + ["Amount"]

# Importance des features
importances = model.feature_importances_
feat_importance = pd.Series(importances, index=features).sort_values(ascending=False)

# Affichage des 10 plus importantes
print("Variables les plus importantes :\n", feat_importance.head(10))

# Optionnel : visualisation
feat_importance.head(10).plot(kind='barh', title="Top 10 des variables importantes", figsize=(8, 5))
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
