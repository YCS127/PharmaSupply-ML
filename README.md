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

## Project Philosophy

This repository addresses a dual engineering challenge:

* **A Production-Ready Core MLOps Architecture:** Practical implementation of ML lifecycle fundamentals (idempotent ingestion, strict data validation, API serving, monitoring) with an extension roadmap toward Generative AI (RAG / LLM in V2).
* **A "From Lab to Prod" Educational Guide:** A step-by-step approach demonstrating how to wrap a classic exploratory analysis inside a modular, testable, and containerized MLOps architecture.

---

## Architecture Overview

```text
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

## Development Environment

The project is developed under **WSL2 (Ubuntu)** using a **Bash / Zsh** shell environment paired with **Miniconda**.

**Why this dev architecture choice?**
* **Dev/Prod Parity (Native Linux):** Executing code within a Linux subsystem (WSL2) guarantees strict parity with Docker containers and production deployment servers, preventing Windows-specific compatibility issues (file paths, C/C++ dependencies).
* **Strict Isolation with Conda:** Using `miniconda` to precisely manage Python and complex C/C++ dependencies (essential for libraries like XGBoost, LightGBM, or PyTorch) without polluting the system environment.
* **Shell Productivity:** The Bash/Zsh ecosystem enables seamless automation of CLI scripts, Docker commands, and CI/CD pipelines.

---

## Data: Synthetic Generation & Real-World Readiness

Due to strict confidentiality and pharmaceutical data regulations (GDPR / HIPAA), this project relies on **automated synthetic data generation** (`src/generate_data.py`).

However, the architecture strictly respects the **decoupling** principle:
* **Realistic Simulation:** The generator reproduces real Supply Chain behaviors (pathology seasonality, lead times, stockout risks).
* **"Plug & Play" Real Connector:** The ingestion pipeline is designed generically. A simple environment variable switch (`DATA_SOURCE=production` or via a configuration parameter) allows plugging the pipeline into a real database or actual files without modifying the core application code.

---

## MLOps Paradigm: Encapsulating Lab into Production

### To clarify the project structure, two key concepts are distinguished:
> * **Lab (Core Business Logic):** The analytical and experimental workspace where statistical processing, business cleaning, feature engineering, and modeling are developed.
> * **Prod (Ops Wrapper):** The automated software infrastructure surrounding the business code to guarantee idempotency, persistence, schema validation, serving, and extensibility.
>
> The objective of this project is to **encapsulate the Lab into Prod** without altering its analytical logic.

#### Data Layer: Securing Access
* **Lab:** Data extraction and querying scripts for analysis.
* **Prod:** Ingestion module (`src/ingestion.py`) and PostgreSQL database (Docker) guaranteeing idempotency, persistence, and concurrent access management.

#### Quality Control & Preparation: From Technical Validation to Business Cleaning
* **Lab:** Analytical processing (missing value imputation, business logic corrections, feature engineering).
* **Prod:** Automated validation wrapper (`src/validation.py`) placed upstream to check schema compliance (data types, outliers) and ensure that Lab code always runs on valid data.

#### Execution & Serving: From Local Prediction to API
* **Lab:** Ad-hoc execution of `model.predict()` inside a notebook cell.
* **Prod:** Exposing predictions via a FastAPI REST API, containerized and ready to be consumed by a Streamlit dashboard or third-party systems.

#### GenAI Extension (V2): RAG & Agent Integration
* **Lab:** Ad-hoc LLM querying or isolated text analysis scripts.
* **Prod:** Autonomous RAG module interconnected with stockout predictions to automatically recommend therapeutic alternatives.

---

## Quickstart

> ⚠️ **Structural Prerequisite:** The steps below rely on scripts located in the `src/` directory. Ensure that the files corresponding to each module (`generate_data.py`, `ingestion.py`, `validation.py`, `train.py`, etc.) have been created in your environment before running the commands.

1. **Clone the repository and navigate to the project directory**

```bash
git clone https://github.com/votre-user/PharmaSupply-ML.git
cd PharmaSupply-ML
```

2. **Create and activate the Conda virtual environment**

```bash
# Installed dependencies: SQLAlchemy, psycopg2, pandas, pydantic, scikit-learn, xgboost, fastapi, streamlit, etc.
conda create -n pharmasupply python -y
conda activate pharmasupply
pip install -r requirements.txt
```

3. **Start the infrastructure (PostgreSQL Database via Docker)**

```bash
docker compose up -d
```

4. **Generate synthetic data and run ingestion**

```bash
python src/generate_data.py
python src/ingestion.py
```

5. **Run the data validation pipeline**

```bash
python src/validation.py
```

6. **Train the forecasting model**

```bash
python src/train.py
```

7. **Launch the FastAPI REST API service**

```bash
uvicorn src.api:app --reload
```

8. **Launch the Dashboard service (new terminal window)**

```bash
streamlit run src/streamlit.py
```

---

## 🗺️ Project Roadmap & Future Developments

### V1 — Demand Forecasting MLOps Engine (Core Infrastructure)

* [x] **Initialization & Scoping:** Repository structure, Conda environment, and Docker Compose setup (PostgreSQL).
* [x] **Synthetic Generation & Idempotent Ingestion:**
  * Synthetic dataset generation script (`src/generate_data.py`).
  * Persistence and structuring in PostgreSQL (`src/ingestion.py`).
* [x] **Ops Guardrails & Quality:** Automated technical validation pipeline (`src/validation.py`).
* [ ] **ML Pipeline & Feature Engineering:** Time-series feature generation (lags, rolling statistics) and XGBoost model training (`src/train.py`).
* [ ] **Explainability & Monitoring:** SHAP integration and Data Drift detection across batch distributions.
* [ ] **REST API Serving:** Real-time prediction serving via FastAPI (`src/api.py`).
* [ ] **Decision Dashboard:** Interactive Supply Chain user interface built with Streamlit (`src/dashboard.py`).

---

### V2 — Generative AI & Advanced Supply Chain Optimization (Outlook)

* [ ] **RAG / LLM Copilot:** Generative AI agent for automated alternative drug recommendations during active stockouts.
* [ ] **Automated Inventory Redistribution:** Constrained optimization algorithm for balancing inventory across pharmacies.
* [ ] **Cloud Deployment & CI/CD:** GitHub Actions pipeline and containerized infrastructure hosting.