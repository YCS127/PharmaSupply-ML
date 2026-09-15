# PharmaSupply-ML

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Status](https://img.shields.io/badge/status-in--development-orange.svg)



---

<details>
<summary>🇫🇷 <b>Version Française (Cliquez pour dérouler)</b></summary>

---

> **Plateforme ML complète pour la prédiction de la demande et la prévention des ruptures de stock dans la chaîne logistique pharmaceutique.**

### Objectif Métier
Concevoir, entraîner et déployer une solution complète pour prédire la demande de médicaments à 30 jours et déclencher des alertes explicables afin d'éviter les ruptures d'approvisionnement.

### Périmètre & Versions du Projet
* **Version 1.0 (Actuelle) :** Prédiction de demande par séries temporelles (XGBoost/LightGBM), explicabilité avec SHAP, FastAPI, Streamlit & Docker.
* **Version 2.0 (Planifiée) :** IA générative pour la recommandation d'alternatives médicamenteuses (RAG/LLM), surveillance de la dérive des données (Data Drift) et redistribution automatisée des stocks.

### Stack Technique (V1)
* **Data Engineering & SQL :** Python 3.11, PostgreSQL, SQLAlchemy
* **Machine Learning :** XGBoost, LightGBM, SHAP
* **API & Interface :** FastAPI, Streamlit
* **DevOps & Cloud :** Docker, GCP Cloud Run / AWS

### Prérequis & Configuration Locale

#### Démarrage automatique de Docker sous WSL2 (Windows)
Si vous travaillez avec WSL2, Docker Desktop peut ne pas être exécuté en arrière-plan lors de l'exécution des commandes.

1. S'assurer que le script d'aide est exécutable :
   chmod +x scripts/docker-wrapper.sh

### Feuille de Route (Roadmap)
- [x] Initialisation du dépôt et cadrage du projet (V1)
- [x] Script de génération de données synthétiques
- [x] Modélisation & Ingestion PostgreSQL (`src/ingestion.py`, Docker Compose)
- [x] Pipeline de validation et de contrôle qualité des données (`src/validation.py`)
- [ ] Connecteur d'ingestion de données réelles (optionnel / prêt à l'emploi)
- [ ] Pipeline de Machine Learning & Explicabilité SHAP
- [ ] Développement de l'API REST (FastAPI)
- [ ] Tableau de bord interactif (Streamlit)
- [ ] Conteneurisation & Déploiement Cloud
- [ ] **Roadmap V2 :** Intégration RAG / LLM pour la recherche de médicaments alternatifs

</details>

---

### [EN] English Version

> **End-to-end ML platform for demand forecasting and stockout prevention in the pharmaceutical supply chain.**

## Business Goal
Design, train, and deploy an end-to-end solution to forecast drug demand 30 days ahead and trigger explainable alerts to prevent supply chain disruptions.

## Project Scope & Versions
* **Version 1.0 (Current):** Time-Series Demand Forecasting (XGBoost/LightGBM), SHAP Explainability, FastAPI, Streamlit & Docker.
* **Version 2.0 (Planned):** Generative AI for alternative drug recommendation (RAG/LLM), Data Drift Monitoring, and automated stock redistribution.

## Tech Stack (V1)
* **Data Engineering & SQL:** Python 3.11, PostgreSQL, SQLAlchemy
* **Machine Learning:** XGBoost, LightGBM, SHAP
* **API & UI:** FastAPI, Streamlit
* **DevOps & Cloud:** Docker, GCP Cloud Run / AWS

## Prerequisites & Local Setup

### WSL2 Docker Auto-Start (Windows)
If you are working with WSL2, Docker Desktop might not be running in the background when executing commands. 

1. Ensure the helper script is executable:
   chmod +x scripts/docker-wrapper.sh

## Project Roadmap
- [x] Repository initialization & scoping (V1)
- [x] Synthetic data generation script
- [x] PostgreSQL modeling & ingestion (`src/ingestion.py`, Docker Compose)
- [x] Automated data quality & validation pipeline (`src/validation.py`)
- [ ] Support real-world data ingestion connector (optional / plug-and-play setup)
- [ ] Machine Learning pipeline & SHAP explainability
- [ ] REST API development (FastAPI)
- [ ] Interactive dashboard (Streamlit)
- [ ] Containerization & Cloud Deployment
- [ ] **V2 Roadmap:** RAG / LLM integration for alternatives search