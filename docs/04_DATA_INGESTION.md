# Technical Documentation
## Module 04: Data Ingestion
**Project:** PharmaSupply-ML  
**File:** `docs/04_DATA_INGESTION.md`  
**Status:** Validated

---

<details>
<summary>🇫🇷 <b>Version Française (Cliquez pour dérouler)</b></summary>  

---

# 1. Vue d'Ensemble & Objectif

Ce module constitue la première étape (staging) du pipeline MLOps PharmaSupply-ML. Il a pour rôle d'extraire de manière automatisée et sécurisée les données brutes de prévision de la demande pharmaceutique (fichiers CSV) depuis le répertoire local `data/` et de les charger dans une base de données PostgreSQL exécutée sous Docker.

---

## 2. Architecture & Composants

```
PharmaSupply-ML/
├── .env                        # Variables d'environnement (POSTGRES_*)
├── docker-compose.yml          # Services PostgreSQL
├── data/
│   └── pharmaceutical_demand.csv # Dataset brut (3 650 lignes)
├── src/
│   └── ingestion.py            # Script principal d'ingestion
└── docs/
    └── 01_data_ingestion.md    # Documentation technique

```

### Composants Clés :
1. **Docker Container (`pharmasupply-db`)** : Héberge l'instance PostgreSQL sur le port local `5432`.
2. **Custom Zsh Docker Wrapper** : Script shell déclenché en mode interactif (`zsh -i -c`) pour détecter et lancer automatiquement Docker Desktop sous WSL2.
3. **`src/ingestion.py`** : Script Python modularisé en 3 blocs distincts (Imports/Config, Fonction d'Ingestion, Bloc d'Exécution).
4. **SQLAlchemy & Pandas** : Moteur ORM et manipulation de dataframe pour l'écriture en base via `to_sql`.

---

## 3. Structure du Code (`src/ingestion.py`)

Le code suit strictement la règle d'organisation en 3 sections et est intégralement documenté en anglais :

```
# ==============================================================================
# 1. IMPORTS & CONFIGURATION
# ==============================================================================
# - Chargement dynamique du fichier .env depuis la racine du projet via Path.
# - Lecture des identifiants (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, etc.).
# - Fonction ensure_postgres_running() appelant `zsh -i -c` pour exécuter le wrapper.
# - Fonction get_db_engine() créant le moteur SQLAlchemy.

# ==============================================================================
# 2. INGESTION FUNCTION
# ==============================================================================
# - Fonction ingest_csv_to_postgres(file_path, table_name, if_exists)
# - Lecture du CSV via Pandas.
# - Insertion dans PostgreSQL via df.to_sql(..., index=False).
# - Handling des erreurs (SQLAlchemyError, FileNotFoundError).

# ==============================================================================
# 3. EXECUTION BLOCK
# ==============================================================================
# - Vérification et démarrage du conteneur via ensure_postgres_running().
# - Résolution dynamique du chemin d'accès au fichier source.
# - Lancement de l'ingestion vers la table 'raw_pharmaceutical_demand'.

```

---

## 4. Flux de Fonctionnement & Résolution Shell

1. **Gestion du Shell (Zsh/Bash vs Python) :** Lors de l'exécution du script, `ensure_postgres_running()` appelle `subprocess.run(["zsh", "-i", "-c", "docker compose up -d"], check=True)`. L'utilisation du drapeau **`-i`** (interactif) est essentielle : elle force le chargement du profil Zsh (`.zshrc`), permettant d'utiliser l'alias/wrapper Docker personnalisé qui démarre Docker Desktop sous Windows depuis WSL2.
---
2. **Chargement de la Configuration :** Le fichier `.env` situé à la racine du projet est chargé de manière explicite grâce à `ROOT_DIR = Path(__file__).resolve().parent.parent`. Les identifiants `POSTGRES_*` sont extraits.
---
3. **Lecture & Connexion :** Le fichier `data/pharmaceutical_demand.csv` est chargé en mémoire. La connexion SQL est initialisée vers `postgresql://ycs_admin:***@localhost:5432/pharmasupply_db`.
---
4. **Écriture en Base :** 3 650 lignes sont écrites dans la table staging `raw_pharmaceutical_demand`. La méthode `if_exists="replace"` garantit l'idempotence du script.

---

## 5. Commandes de Validation & Persistance

### Exécution du pipeline :
```
conda activate pharma-supply
python src/ingestion.py
```

### Vérification en Base PostgreSQL :
```
docker exec -it pharmasupply-db psql -U ycs_admin -d pharmasupply_db -c "SELECT COUNT(*) FROM raw_pharmaceutical_demand;"
```


### Persistance des Données :
* **Volumes Docker :** Les données de la base PostgreSQL sont stockées sur un volume persistant géré par Docker. Un redémarrage du PC ou de WSL2 n'entraîne aucune perte de données.
* **Stratégie Idempotente :** L'option `if_exists="replace"` permet d'exécuter le script autant de fois que nécessaire sans dupliquer les enregistrements.

</details>

---

### [EN] English Version

## 1. Overview & Purpose

This module represents the staging layer of the PharmaSupply-ML MLOps pipeline. Its purpose is to automatically and securely extract raw pharmaceutical demand forecasting datasets (CSV format) from the local `data/` directory and load them into a Dockerized PostgreSQL database.

---

## 2. Architecture & Components

```
PharmaSupply-ML/
├── .env                        # Environment variables (POSTGRES_*)
├── docker-compose.yml          # PostgreSQL services
├── data/
│   └── pharmaceutical_demand.csv # Raw dataset (3,650 rows)
├── src/
│   └── ingestion.py            # Main ingestion script
└── docs/
    └── 01_data_ingestion.md    # Technical documentation

```

### Key Components:
1. **Docker Container (`pharmasupply-db`)**: Hosts the PostgreSQL instance on local port `5432`.
2. **Custom Zsh Docker Wrapper**: Shell script triggered in interactive mode (`zsh -i -c`) to detect and automatically launch Docker Desktop within WSL2.
3. **`src/ingestion.py`**: Python script modularized into 3 distinct sections (Imports/Config, Ingestion Function, Execution Block).
4. **SQLAlchemy & Pandas**: ORM engine and dataframe manipulation for database writing via `to_sql`.

---

## 3. Code Structure (`src/ingestion.py`)

The code strictly follows the 3-section structure and is fully documented in English:

```
# ==============================================================================
# 1. IMPORTS & CONFIGURATION
# ==============================================================================
# - Dynamic loading of .env from project root via Path.
# - Parsing credentials (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, etc.).
# - ensure_postgres_running() function calling `zsh -i -c` to run the wrapper.
# - get_db_engine() function creating the SQLAlchemy engine.

# ==============================================================================
# 2. INGESTION FUNCTION
# ==============================================================================
# - ingest_csv_to_postgres(file_path, table_name, if_exists) function.
# - Optimized CSV parsing using Pandas.
# - Database insertion into PostgreSQL via df.to_sql(..., index=False).
# - Robust error handling (SQLAlchemyError, FileNotFoundError).

# ==============================================================================
# 3. EXECUTION BLOCK
# ==============================================================================
# - Container verification and activation via ensure_postgres_running().
# - Dynamic resolution of absolute path for the source file.
# - Execution of data ingestion into 'raw_pharmaceutical_demand' table.
```

---

## 4. Execution Workflow & Shell Resolution

1. **Shell Handling (Zsh/Bash vs Python):** When executing `python src/ingestion.py`, `ensure_postgres_running()` calls `subprocess.run(["zsh", "-i", "-c", "docker compose up -d"], check=True)`. The interactive flag **`-i`** is critical: it forces loading the Zsh configuration (`.zshrc`), enabling the custom Docker wrapper that starts Docker Desktop in WSL2 automatically.
---
2. **Configuration Loading:** The `.env` file at the root directory is explicitly loaded using `ROOT_DIR = Path(__file__).resolve().parent.parent`. `POSTGRES_*` variables are parsed successfully.
---
3. **Read & Connect:** The file `data/pharmaceutical_demand.csv` is loaded into memory. The SQL connection engine targets `postgresql://ycs_admin:***@localhost:5432/pharmasupply_db`.
---
4. **Database Write:** 3,650 rows are written into the `raw_pharmaceutical_demand` staging table. The `if_exists="replace"` parameter ensures script idempotency.

---

## 5. Validation Commands & Persistence

### Pipeline Execution:
```
conda activate pharma-supply
python src/ingestion.py
```

### PostgreSQL Database Verification:
```
docker exec -it pharmasupply-db psql -U ycs_admin -d pharmasupply_db -c "SELECT COUNT(*) FROM raw_pharmaceutical_demand;"
```

### Persistence:
* **Docker Volumes:** Database records are persisted using a dedicated Docker volume. System restarts or WSL2 reboots will not cause data loss.
* **Idempotency Strategy:** The `if_exists="replace"` parameter allows rerunning the script indefinitely without duplicating rows.

---
