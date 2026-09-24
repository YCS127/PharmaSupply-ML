# Technical Documentation
## Phase 2: Data Infrastructure & Ingestion
**Project:** PharmaSupply-ML
**Framework:** Standard MLOps Blueprint
**File:** `docs/02_DATA_INFRASTRUCTURE_AND_INGESTION.md`
**Status:** Validated

---

<details>
<summary>🇫🇷 <b>Version Française (Cliquez pour dérouler)</b></summary>

### *Ce document détaille l'infrastructure de stockage des données conteneurisée sous Docker (PostgreSQL) ainsi que le pipeline d'ingestion automatisé (`src/ingestion.py`).*

---

## 1. Contexte & Architecture MLOps

L'objectif de cette étape est d'isoler l'infrastructure de stockage des données pour garantir la **parité Dev/Prod** (*Dev-Prod Parity*). Dans notre environnement sous Linux (WSL2), PostgreSQL est instancié via Docker Compose pour offrir une base de données relationnelle isolée, versionnée et reproductible.

~~~~text
PharmaSupply-ML/
├── .env                        # Credentials PostgreSQL (non versionné)
├── .env.example                # Gabarit des variables d'environnement
├── docker-compose.yml          # Services PostgreSQL & volumes
├── data/
│   └── pharmaceutical_demand.csv # Jeu de données brut (3 650 lignes)
├── src/
│   └── ingestion.py            # Pipeline automatisé d'ingestion
└── docs/
    └── 02_DATA_INFRASTRUCTURE_AND_INGESTION.md
~~~~

---

## 2. Infrastructure Conteneurisée (Docker Compose)

### 2.1. Fichier `docker-compose.yml`
La base de données PostgreSQL 16 (image Alpine ultra-légère) est configurée avec persistance des données sur un volume dédié :

~~~~yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: pharmasupply-db
    restart: always
    env_file:
      - .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local
~~~~

### 2.2. Commandes de Gestion du Conteneur
Toutes les commandes s'exécutent depuis la racine du projet :

| Action | Commande | Description |
| :--- | :--- | :--- |
| **Démarrage** | `docker compose up -d` | Télécharge l'image, crée le volume et lance le service. |
| **Vérification** | `docker compose ps` | Confirme l'état de santé (`healthy`). |
| **Consultation Logs** | `docker compose logs -f` | Affiche le flux de journaux PostgreSQL en temps réel. |
| **Arrêt Sécurisé** | `docker compose stop` | Arrête le conteneur en préservant les données dans le volume. |
| **Purge Complète** | `docker compose down -v` | Supprime le conteneur et purge le volume de données. |

---

## 3. Pipeline d'Ingestion (`src/ingestion.py`)

Le script `src/ingestion.py` extrait les données brutes du fichier CSV local (`data/pharmaceutical_demand.csv`) et les charge dans la table de staging `raw_pharmaceutical_demand`.

### 3.1. Structure du Code
Le module est découpé en trois blocs distincts :

1. **Imports & Configuration :** Chargement dynamique des identifiants depuis `.env` et gestion du démarrage de Docker via un sous-processus interactif (`zsh -i -c`) sous WSL2.
2. **Fonction d'Ingestion :** Parsing optimisé du fichier CSV via `pandas` et écriture en base de données via `SQLAlchemy` (`df.to_sql()`).
3. **Bloc d'Exécution (`main`) :** Validation de l'état du conteneur, résolution des chemins relatifs et exécution idempotente de l'ingestion (`if_exists="replace"`).

---

## 4. Exécution & Validation

### 4.1. Lancement du Pipeline
~~~~bash
conda activate pharmasupply-ml
python src/ingestion.py
~~~~

### 4.2. Vérification de la Base de Données
~~~~bash
docker exec -it pharmasupply-db psql -U mlops_user -d pharmasupply_db -c "SELECT COUNT(*) FROM raw_pharmaceutical_demand;"
~~~~

</details>

---

### [EN] English Version

### *This document details the containerized data storage infrastructure using Docker (PostgreSQL) and the automated data ingestion pipeline (`src/ingestion.py`).*

---

## 1. Context & MLOps Architecture

The primary goal of this phase is to isolate the data storage layer to guarantee **Dev-Prod Parity**. Under Linux (WSL2), PostgreSQL is instantiated using Docker Compose to provide an isolated, versioned, and reproducible relational database.

~~~~text
PharmaSupply-ML/
├── .env                        # PostgreSQL credentials (ignored by Git)
├── .env.example                # Environment variable template
├── docker-compose.yml          # PostgreSQL services & persistent volumes
├── data/
│   └── pharmaceutical_demand.csv # Raw dataset (3,650 rows)
├── src/
│   └── ingestion.py            # Automated ingestion pipeline
└── docs/
    └── 02_DATA_INFRASTRUCTURE_AND_INGESTION.md
~~~~

---

## 2. Containerized Infrastructure (Docker Compose)

### 2.1. `docker-compose.yml` File
The PostgreSQL 16 database (lightweight Alpine image) is configured with volume persistence:

~~~~yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: pharmasupply-db
    restart: always
    env_file:
      - .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local
~~~~

### 2.2. Container Management Commands
All commands should be executed from the project root:

| Action | Command | Description |
| :--- | :--- | :--- |
| **Start** | `docker compose up -d` | Pulls image, creates volume, and starts container in detached mode. |
| **Verify** | `docker compose ps` | Confirms container health status (`healthy`). |
| **View Logs** | `docker compose logs -f` | Streams live PostgreSQL output logs. |
| **Stop (Safe)** | `docker compose stop` | Stops container while preserving data in the volume. |
| **Full Cleanup** | `docker compose down -v` | Removes container and **purges the data volume**. |

---

## 3. Ingestion Pipeline (`src/ingestion.py`)

The `src/ingestion.py` script extracts raw data from the local CSV file (`data/pharmaceutical_demand.csv`) and loads it into the `raw_pharmaceutical_demand` staging table.

### 3.1. Code Architecture
The module is divided into three distinct sections:

1. **Imports & Configuration:** Dynamic credential parsing from `.env` and automatic container activation via interactive shell (`zsh -i -c`) in WSL2.
2. **Ingestion Function:** Optimized CSV parsing using `pandas` and database writing using `SQLAlchemy` (`df.to_sql()`).
3. **Execution Block (`main`):** Container health assertion, path resolution, and idempotent execution (`if_exists="replace"`).

---

## 4. Execution & Validation

### 4.1. Run Pipeline
~~~~bash
conda activate pharmasupply-ml
python src/ingestion.py
~~~~

### 4.2. Query Staging Table
~~~~bash
docker exec -it pharmasupply-db psql -U mlops_user -d pharmasupply_db -c "SELECT COUNT(*) FROM raw_pharmaceutical_demand;"
~~~~