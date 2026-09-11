# PharmaSupply-ML

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

## Project Roadmap
- [x] Repository initialization & scoping (V1)
- [ ] Synthetic data generation script
- [ ] PostgreSQL modeling & ingestion (Docker Compose)
- [ ] Machine Learning pipeline & SHAP explainability
- [ ] REST API development (FastAPI)
- [ ] Interactive dashboard (Streamlit)
- [ ] Containerization & Cloud Deployment
- [ ] **V2 Roadmap:** RAG / LLM integration for alternatives search
