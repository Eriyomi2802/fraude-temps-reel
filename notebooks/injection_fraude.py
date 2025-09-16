import pandas as pd
import numpy as np
import os

# Charger les données d'origine
df = pd.read_csv("donnees/creditcard.csv")

# Séparer les classes
fraudes = df[df["Class"] == 1]
non_fraudes = df[df["Class"] == 0]

# Nombre total souhaité pour obtenir 40% de fraudes
total_cible = len(df)
n_fraudes_voulues = int(0.4 * total_cible)
n_non_fraudes_voulues = total_cible - n_fraudes_voulues

# Sur-échantillonnage des fraudes (avec remplacement s'il y en a trop peu)
fraudes_augmentees = fraudes.sample(n=n_fraudes_voulues, replace=True, random_state=42)
non_fraudes_reduites = non_fraudes.sample(n=n_non_fraudes_voulues, random_state=42)

# Combiner et mélanger
df_equilibre = pd.concat([fraudes_augmentees, non_fraudes_reduites]).sample(frac=1, random_state=42)

# Enregistrer dans un nouveau fichier
output_path = "donnees/creditcardfraude.csv"
df_equilibre.to_csv(output_path, index=False)
print(f" Nouveau fichier enregistré avec 40% de fraudes : {output_path}")
