# Project Dependencies & Technical Stack / Dépendances du Projet

This document tracks the Python libraries and tools used in **PharmaSupply-ML**.

---

<details>
<summary>🇫🇷 <b>Version Française (Cliquez pour dérouler)</b></summary>  

#
> Ce document est vivant. Les dépendances listées ci-dessous représentent la stack actuelle et les bibliothèques pressenties. Au fur et à mesure des expérimentations et des besoins de performance (choix des algorithmes, optimisation, métriques), toute nouvelle bibliothèque installée sera documentée ici et reflétée dans `environment.yml` / `requirements.txt`.


### 1. Ingestion & Manipulation de Données
* **`pandas`** : Manipulation et analyse de données. Utilisé pour charger, transformer et structurer les jeux de données (fichiers CSV/Parquet et DataFrames).
* **`numpy`** : Calcul scientifique et opérations vectorielles. Sert de socle mathématique pour Pandas et la génération de données synthétiques.

### 2. Base de Données & Intégration SQL
* **`sqlalchemy`** : Abstraction de base de données (ORM / Core). Permet d'interagir avec PostgreSQL en Python (ex. `df.to_sql()`) sans écrire de SQL brut complexe.
* **`psycopg2-binary`** : Pilote (*driver*) PostgreSQL à bas niveau. Utilisé par SQLAlchemy pour communiquer directement avec le conteneur Docker PostgreSQL.

### 3. Modélisation & Machine Learning *(À venir)*
* **`scikit-learn`** : Algorithmes ML de base, métriques d'évaluation et pipelines de pré-traitement.
* **`xgboost` / `lightgbm`** : Algorithmes de Gradient Boosting optimisés pour les séries temporelles et la prédiction de demande.

### 4. Environnement & Configuration
* **`python-dotenv`** : Chargement des variables d'environnement (identifiants PostgreSQL) à partir d'un fichier `.env` sécurisé.

</details>

---

### [EN] English Version

> This document is dynamic. The dependencies listed below reflect the current stack and prospective libraries. As experiments progress (algorithm selection, optimization, performance tracking), any newly added library will be documented here and updated in `environment.yml` / `requirements.txt`.

### 1. Data Ingestion & Manipulation
* **`pandas`**: Data manipulation and analysis. Used for loading, transforming, and structuring datasets (CSV/Parquet files and DataFrames).
* **`numpy`**: Scientific computing and high-performance vector operations. Serves as the mathematical foundation for Pandas and synthetic data generation.

### 2. Database & SQL Integration
* **`sqlalchemy`**: Database abstraction toolkit (ORM / Core). Enables smooth interaction between Python and PostgreSQL (e.g., `df.to_sql()`) without writing complex raw SQL.
* **`psycopg2-binary`**: Low-level PostgreSQL database adapter for Python. Acts as the underlying driver used by SQLAlchemy to communicate with the PostgreSQL Docker container.

### 3. Machine Learning & Modeling *(Upcoming)*
* **`scikit-learn`**: Machine learning algorithms, evaluation metrics, and preprocessing pipelines.
* **`xgboost` / `lightgbm`**: Optimized gradient boosting frameworks for time-series and demand forecasting.

### 4. Environment & Configuration
* **`python-dotenv`**: Reads key-value pairs from a `.env` file and sets them as environment variables (e.g., database credentials).

</details>