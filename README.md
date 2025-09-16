
# 💳 Détection de Fraude en Temps Réel 

## 🎯 Objectif

Ce projet vise à détecter automatiquement des comportements frauduleux à partir de données temps réel via un pipeline de streaming.

## 👨‍💻 Auteur

**Hélène CAKPOSSE** – Data Engineer 
---

## 🧱 Stack technique

| Composant        | Rôle                                                    |
|------------------|----------------------------------------------------------|
| Python           | Traitement, simulation et logique de détection          |
| Kafka            | Ingestion et transmission temps réel des événements     |
| Spark Streaming  | Analyse et détection en streaming des données           |
| Airflow          | Orchestration (optionnelle)                             |
| Docker           | Conteneurisation de tous les services                   |
| Power BI         | Visualisation des alertes en temps réel (en cours)      |

---

## 📁 Structure du projet

| Composant       | Rôle                                                |
| --------------- | --------------------------------------------------- |
| Python          | Traitement, simulation et logique de détection      |
| Kafka           | Ingestion et transmission temps réel des événements |
| Spark Streaming | Analyse et détection en streaming des données       |
| Airflow         | Orchestration (optionnelle)                         |
| Docker          | Conteneurisation de tous les services               |
| Power BI        | Visualisation des alertes en temps réel (en cours)  |


## ⚙️ Démo – Lancer le projet en local

### 1. Cloner le projet

```bash
git clone https://github.com/ebqydnjni/fraude-temps-reel.git
cd fraude-temps-reel
```

### 2. Lancer l’infrastructure avec Docker

Assurez-vous d’avoir Docker installé, puis exécutez :

```bash
docker-compose up -d
```

> Cela démarre Kafka, Zookeeper et les autres services nécessaires.

### 3. Entraîner le modèle de détection de fraude

```bash
python modeles/entrainement_modele_equilibre.py
```

Entraîne un modèle Random Forest équilibré avec SMOTE.

### 4. Injecter des fraudes simulées dans les données

```bash
python notebooks/injection_fraude.py
```

🔁 Modifie le fichier CSV pour inclure 40 % de fraudes simulées.

### 5. Lancer le système de prédiction en temps réel

```bash
python orchestration/flux_prediction.py
```

📡 Consomme les transactions Kafka, prédit les fraudes et envoie les résultats à Power BI.

### 6. Simuler l'envoi de transactions

Dans un **autre terminal** :

```bash
python producteur/simulateur_transactions.py
```

📦 Envoie les transactions vers le topic Kafka `transactions`.

### 7. Observer les prédictions localement

```bash
python modeles/predict_fraude.py
```

🔍 Affiche les prédictions avec leur probabilité.

---

## 📊 Visualisation

Le tableau de bord **Power BI** est en cours de conception pour visualiser les alertes de fraude en temps réel.

