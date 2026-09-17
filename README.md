# PharmaSupply-ML — From Exploratory Notebooks to Industrial MLOps & LLM Architecture
> **Industrial MLOps (V1) & Generative AI (V2) Blueprint | Production-Ready Educational Guide**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Status-In--Development-orange.svg)]()


---
<details>
<summary>🇫🇷 <b>Version Française (Cliquez pour dérouler)</b></summary>  

## Philosophie du Projet

Ce dépôt répond à un double enjeu d'ingénierie :

* **Une architecture MLOps de base (Production-Ready) :** Implémentation pratique des fondamentaux du cycle de vie ML (ingestion idempotente, validation stricte des données, serving par API, monitoring) avec une trajectoire d'extension vers l'IA générative (RAG / LLM en V2).
* **Un guide pédagogique « From Lab to Prod » :** Démarche pas à pas montrant comment encapsuler une analyse exploratoire classique dans une enveloppe MLOps modulaire, testable et conteneurisée.

---

## Vue d'ensemble de l'architecture

``` text
+-----------------------+     +------------------------+     +------------------------+
|  Synthetic Data Gen   | --> | PostgreSQL (Docker)    | --> | Data Validation        |
|  (Raw CSV Generation) |     | (Idempotent Ingestion) |     | (Automated Assertions) |
+-----------------------+     +------------------------+     +------------------------+
                                                                         |
                                                                         v
+-----------------------+     +------------------------+     +------------------------+
|  FastAPI / Streamlit  | <-- | XGBoost / LightGBM     | <-- | Feature Engineering    |
|  (Serving & Dashboard)|     | (30-Day Forecasting)   |     | (Lags, Rolling Means)  |
+-----------------------+     +------------------------+     +------------------------+
            |
            | (V2 Extension)
            v
+-------------------------------------------------------------------------------------+
| Generative AI Module: RAG / LLM Agent                                              |
| (Automated Alternative Drug Recommendations during Active Stockouts)               |
+-------------------------------------------------------------------------------------+
```

## Environnement de Développement

Le projet est développé sous **WSL2 (Ubuntu)** en environnement shell **Bash / Zsh** couplé à **Miniconda**.

**Pourquoi ce choix d'architecture de dev ?**
* **Parité Dev/Prod (Linux native) :** L'exécution du code dans un sous-système Linux (WSL2) garantit une parité stricte avec les conteneurs Docker et les serveurs de déploiement en production, évitant les problèmes de compatibilité spécifiques à Windows (chemins de fichiers, dépendances C/C++).
* **Isolation stricte avec Conda :** Utilisation de `miniconda` pour gérer précisément les dépendances Python et C/C++ complexes (indispensables pour des librairies comme XGBoost, LightGBM ou PyTorch) sans polluer l'environnement système.
* **Productivité Shell :** L'écosystème Bash/Zsh offre une automatisation fluide des scripts CLI, des commandes Docker et des pipelines CI/CD.



## Données : Génération Synthétique & Prêt pour le Réel

En raison de la confidentialité stricte et de la réglementation sur les données pharmaceutiques (GDPR / HIPAA), ce projet s'appuie sur une **génération automatisée de données synthétiques** (`src/generate_data.py`). 

Cependant, l'architecture respecte le principe de **découplage** :
* **Simulation réaliste :** Le générateur reproduit les comportements d'une vraie Supply Chain (saisonnalité des pathologies, délais de réapprovisionnement, risques de rupture).
* **Connecteur Réel ("Plug & Play") :** Le pipeline d'ingestion est conçu de manière générique. Un simple basculement de variable d'environnement (`DATA_SOURCE=production` ou via un paramètre de configuration) permet de brancher le pipeline sur une vraie base de données ou des fichiers réels sans modifier le cœur de l'application.


## Paradigme MLOps : Encapsulation du Lab vers la Production

### Pour clarifier la structure du projet, deux concepts clés sont distingués :
>* **Lab (Cœur Métier) :** L'espace d'analyse et d'expérimentation où sont développés les traitements statistiques, le nettoyage métier, le feature engineering et la modélisation.
>* **Prod (Enveloppe Ops) :** L'infrastructure logicielle automatisée qui entoure le code métier pour garantir l'idempotence, la persistance, la validation de schéma, le serving et l'extensibilité.
>
>L'objectif de ce projet est d'**encapsuler le Lab dans la Prod** sans en altérer la logique analytique.



#### Couche de données : Sécurisation de l'accès
* **Lab :** Code d'extraction et requêtage des données pour l'analyse.
* **Prod :** Module d'ingestion (`src/ingestion.py`) et base PostgreSQL (Docker) garantissant l'idempotence, la persistance et la gestion des accès concurrents.

#### Contrôle qualité & Préparation : De la validation technique au nettoyage métier
* **Lab :** Traitement analytique des données (imputation des valeurs manquantes, corrections métier, feature engineering).
* **Prod :** Enveloppe de validation automatique (`src/validation.py`) placée en amont pour vérifier la conformité du schéma (types, valeurs aberrantes) et garantir que le code Lab s'exécute toujours sur des données valides.

#### Exécution & Serving : De la prédiction locale à l'API
* **Lab :** Exécution ponctuelle de `model.predict()` dans une cellule de notebook.
* **Prod :** Exposition des prédictions via une API REST sous FastAPI, conteneurisée et prête à être consommée par un dashboard (Streamlit) ou un système tiers.

#### Extension GenAI (V2) : Intégration RAG & Agent
* **Lab :** Requêtage ad hoc d'un LLM ou scripts d'analyse de texte isolés.
* **Prod :** Module RAG autonome interconnecté aux prédictions de ruptures pour recommander automatiquement des alternatives thérapeutiques.
---

## Démarrage rapide (Quickstart)


> ⚠️ **Prérequis de structure :** les étapes ci-dessous reposent sur les scripts du dossier `src/`. Assurez-vous que les fichiers correspondant à chaque brique (`generate_data.py`, `ingestion.py`, `validation.py`, `train.py`, etc.) ont bien été créés au préalable dans votre environnement avant d'exécuter les commandes


1. **Cloner le dépôt et se placer dans le projet**

```bash
git clone https://github.com/votre-user/PharmaSupply-ML.git
cd PharmaSupply-ML
```

2. **Créer et activer l'environnement virtuel Conda**

```bash
# Dépendances installées : SQLAlchemy, psycopg2, pandas, pydantic, scikit-learn, xgboost, fastapi, streamlit, etc.
conda create -n pharmasupply python -y
conda activate pharmasupply
pip install -r requirements.txt
```

3. **Démarrer l'infrastructure (Base de données PostgreSQL via Docker)**

```bash
docker compose up -d
```

4. **Générer les données synthétiques et exécuter l'ingestion**

```bash
python src/generate_data.py
python src/ingestion.py
```

5. **Exécuter le pipeline de validation des données**

```bash
python src/validation.py
```

6. **Entraîner le modèle de prévision**

```bash
python src/train.py
```

7. **Lancer le service API FastApi**

```bash
uvicorn src.api:app --reload
```

8. **Lancer le servie Dashboard (new terminal)**

```bash
streamlit run src/streamlit.py
```


---

## 🗺️ Feuille de route du projet & Évolutions

### V1 — Moteur MLOps de prévision de la demande (Cœur d'infrastructure)

* [x] **Initialisation & Cadrage :** Structure du dépôt, environnement Conda et Docker Compose (PostgreSQL).
* [x] **Génération & Ingestion Idempotente :**
  * Script de génération du jeu de données synthétique (`src/generate_data.py`).
  * Persistance et structuration dans la base PostgreSQL (`src/ingestion.py`).
* [x] **Garde-fou Ops & Qualité :** Pipeline de validation technique automatique (`src/validation.py`).
* [ ] **Pipeline ML & Feature Engineering :** Génération de variables temporelles/lags et entraînement XGBoost (`src/train.py`).
* [ ] **Explicabilité & Monitoring :** Intégration SHAP et détection du *Data Drift* sur la distribution des lots.
* [ ] **Serving REST API :** Exposition des prédictions en temps réel via FastAPI (`src/api.py`).
* [ ] **Interface Décisionnelle :** Tableau de bord interactif pour la Supply Chain (`src/dashboard.py`).

---

### V2 — Intelligence Générative & Optimisation Avancée (Perspectives)

* [ ] **Copilote RAG / LLM :** Agent d'IA générative pour recommander des médicaments substitutifs en cas de rupture de stock.
* [ ] **Redistribution Automatisée :** Algorithme d'optimisation sous contraintes pour rééquilibrer les stocks inter-officines.
* [ ] **Déploiement Cloud & CI/CD :** Pipeline GitHub Actions et hébergement de l'infrastructure conteneurisée.

#




</details>

---

### [EN] English Version
> 
This repository addresses a dual engineering challenge:

* **A Production-Ready Core MLOps Architecture:** Practical implementation of ML lifecycle fundamentals (idempotent ingestion, strict data validation, API serving, monitoring) with an extension roadmap toward Generative AI (RAG / LLM in V2).
* **A "From Lab to Prod" Educational Guide:** A step-by-step approach demonstrating how to wrap a classic exploratory analysis inside a modular, testable, and containerized MLOps architecture.

---

## Architecture Overview

``` text
+-----------------------+     +------------------------+     +------------------------+
|  Synthetic Data Gen   | --> | PostgreSQL (Docker)    | --> | Data Validation        |
|  (Raw CSV Generation) |     | (Idempotent Ingestion) |     | (Automated Assertions) |
+-----------------------+     +------------------------+     +------------------------+
                                                                          |
                                                                          v
+-----------------------+     +------------------------+     +------------------------+
|  FastAPI / Streamlit  | <-- | XGBoost / LightGBM     | <-- | Feature Engineering    |
|  (Serving & Dashboard)|     | (30-Day Forecasting)   |     | (Lags, Rolling Means)  |
+-----------------------+     +------------------------+     +------------------------+
            |
            | (V2 Extension)
            v
+-------------------------------------------------------------------------------------+
| Generative AI Module: RAG / LLM Agent                                               |
| (Automated Alternative Drug Recommendations during Active Stockouts)                |
+-------------------------------------------------------------------------------------+
```
---

## 💡 MLOps Paradigm: From Lab to Production

This project bridges the gap between exploratory data science and industrial software engineering. Each module highlights key engineering decisions:

### 1. Persistent Data Layer vs. Raw CSV
* **Lab Approach:** Reading directly from a static `.csv` using `pd.read_csv()`. It lacks concurrency, schema constraints, and real-world parity.
* **Production Approach:** Ingesting raw data into **PostgreSQL via Docker** (`src/ingestion.py`). This guarantees Dev/Prod parity, transactional integrity, and idempotency.

### 2. Automated Data Quality vs. Manual Inspection
* **Lab Approach:** Checking `df.isna()` interactively in a Jupyter Notebook cell.
* **Production Approach:** Executing strict automated schema assertions (`src/validation.py`) within the pipeline to halt processing instantly if corrupted or negative values enter the system.

---

## 🚀 Quickstart

Follow these steps to run the ingestion and data quality validation locally:

```bash
# 1. Clone the repository
git clone https://github.com/<votre-user>/PharmaSupply-ML.git
cd PharmaSupply-ML

# 2. Start PostgreSQL container
docker compose up -d

# 3. Run data quality validation pipeline
python src/validation.py
```

---

## 🗺️ Project Roadmap & Evolution

### V1 — Core MLOps Forecasting Engine (Current Focus)
- [x] Repository initialization & scoping
- [x] Synthetic data generation script
- [x] PostgreSQL modeling & idempotent ingestion (`src/ingestion.py`, Docker Compose)
- [x] Automated data quality & validation pipeline (`src/validation.py`)
- [ ] Feature engineering module (lags, temporal features, rolling means)
- [ ] Machine Learning pipeline & SHAP explainability
- [ ] REST API development (FastAPI)
- [ ] Interactive dashboard (Streamlit)
- [ ] Containerization & Cloud Deployment

### V2 — Generative AI & Supply Chain Intelligence (Planned)
- [ ] **RAG / LLM Integration:** Automated alternative drug recommendations during active stockouts.
- [ ] **Data Drift & Monitoring:** Continuous monitoring of feature drift and model performance decay in production.
- [ ] **Automated Stock Redistribution:** Optimization algorithm for inter-pharmacy inventory balancing.