# Universal MLOps Project Initialization Checklist & Guide / Checklist & Guide Universel d'Initialisation de Projet MLOps

<details>
<summary>🇫🇷 <b>Version Française (Cliquez pour dérouler)</b></summary>  

---

### *Ce document récapitule la procédure opératoire permanente (SOP) pour initialiser un environnement de développement Data/MLOps propre, isolé, reproductible et prêt pour la production sous Linux (**WSL2 / Zsh**)*

---

## 1. Structure du Projet & Arborescence

### 1.1. Création du dossier et des sous-répertoires
Depuis le terminal WSL (Zsh), exécuter la commande suivante pour générer la structure modulaire :

```
mkdir nom-du-projet
cd nom-du-projet
mkdir -p src/data src/features src/models src/visualization sql docs tests .vscode
```

### 1.2. Rôle des répertoires
* **src/data/** : Scripts de génération, nettoyage et pipelines d'ingestion.
* **src/features/** : Scripts de transformation et d'ingénierie des variables.
* **src/models/** : Scripts d'entraînement, évaluation et fonctions d'inférence.
* **sql/** : Fichiers DDL (création de tables) et requêtes analytiques.
* **docs/** : Documentation technique, procédures d'initialisation et fiches d'architecture.
* **tests/** : Tests unitaires et d'intégration (pytest).
* **.vscode/** : Configuration partagée de l'éditeur de code.

---

## 2. Environnement Virtuel Python & Dépendances

### 2.1. Création et activation de l'environnement Conda

```
conda create -n mon-env-ml python=3.11 -y
conda activate mon-env-ml
pip install pandas numpy scikit-learn ruff
```

### 2.2. Exportation de la configuration (environment.yml)
Pour garantir la reproductibilité exacte de l'environnement par d'autres développeurs :

```
conda env export --no-builds > environment.yml
```

---

## 3. Configuration du Versioning Git

### 3.1. Initialisation du dépôt local

```
git init
git branch -M main
```

### 3.2. Création du fichier .gitignore
À la racine du projet, créer le fichier .gitignore pour exclure les données, caches et secrets :

```
# Fichiers de données volumineux  
src/data/*.csv
src/data/*.parquet
src/data/*.json

# Environnement Python & Caches  
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.env

# Fichiers système & IDE  
.DS_Store
.vscode/*
!.vscode/settings.json

Remarque : Ajouter si nécessaire le fichier du workspace
```

---

## 4. Documentation Principale : README.md

Créer le fichier README.md à la racine pour présenter le projet, la stack et la feuille de route (à adapter au projet) :

```
# Nom du Projet

## Description
Présentation synthétique du problème métier et de la solution MLOps visée.

## Stack Technique
* Langage : Python 3.11
* Linter & Formatter : Ruff
* Base de Données : PostgreSQL / Docker
* Versioning : Git / GitHub

## Feuille de Route (Roadmap)
- [x] Initialisation du dépôt et de l'environnement
- [ ] Script de génération et d'ingestion de données
- [ ] Conteneurisation de la base de données avec Docker Compose
- [ ] Entraînement du modèle et suivi des métriques
```

---

## 5. Industrialisation de la Qualité de Code

### 5.1. Configuration de Ruff (pyproject.toml)
Créer un fichier pyproject.toml à la racine pour unifier les règles du linter et du formatter :

```
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E501"]
```

### 5.2. Configuration de l'Espace de Travail (.vscode/settings.json)
Pour forcer VS Code à utiliser automatiquement le bon interpréteur Python et formater à la sauvegarde, nous créons un dossier caché dans lequel nous insérons le fichier .json :

```
{
  "python.defaultInterpreterPath": "~/.conda/envs/mon-env-ml/bin/python",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

---

## 6. Liaison GitHub & Premier Commit

Exécuter la séquence suivante pour valider le socle initial sur GitHub :

```
git add .
git commit -m "chore: initial project setup and infrastructure"
git remote add origin git@github.com:nom-utilisateur/nom-du-depot.git
git push -u origin main
```

</details>



#### [EN] English Version

### *This document outlines the universal Standard Operating Procedure (SOP) for initializing a clean, isolated, reproducible, and production-ready Data/MLOps development environment on Linux (**WSL2 / Zsh**)*

---

## 1. Project Structure & Directory Layout

### 1.1. Directory Creation
From your WSL (Zsh) terminal, run the following command to generate the modular structure:


```
mkdir project-name
cd project-name
mkdir -p src/data src/features src/models src/visualization sql docs tests .vscode
```

### 1.2. Directory Roles
* **src/data/**: Generation scripts, cleaning pipelines, and data ingestion logic.
* **src/features/**: Data transformation and feature engineering scripts.
* **src/models/**: Model training, evaluation, and inference code.
* **sql/**: DDL scripts (table creation) and analytical queries.
* **docs/**: Technical documentation, setup procedures, and architecture guides.
* **tests/**: Unit and integration tests (pytest).
* **.vscode/**: Shared workspace configuration for VS Code.

---

## 2. Python Virtual Environment & Dependencies

### 2.1. Conda Environment Creation and Activation


```
conda create -n my-ml-env python=3.11 -y
conda activate my-ml-env
pip install pandas numpy scikit-learn ruff
```

### 2.2. Exporting Configuration (environment.yml)
To ensure full environment reproducibility across team members:

```
conda env export --no-builds > environment.yml
```

---

## 3. Git Version Control Setup

### 3.1. Local Repository Initialization

```
git init
git branch -M main
```

### 3.2. Creating the .gitignore File
At the project root, create a `.gitignore` file to exclude datasets, caches, and secrets:

```
# Large Data Files  
src/data/*.csv
src/data/*.parquet
src/data/*.json

# Python Environment & Caches  
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.env

# System & IDE Files  
.DS_Store
.vscode/*
!.vscode/settings.json

Note: Add your workspace settings file if necessary.
```

---

## 4. Primary Documentation: README.md

Create a `README.md` at the project root to detail the project scope, stack, and roadmap:

```
# Project Name

## Description
Brief overview of the business problem and the target MLOps solution.

## Technical Stack
* Language: Python 3.11
* Linter & Formatter: Ruff
* Database: PostgreSQL / Docker
* Versioning: Git / GitHub

## Roadmap
- [x] Repository and environment setup
- [ ] Data generation and ingestion script
- [ ] Database containerization with Docker Compose
- [ ] Model training and metric tracking
```

---

## 5. Code Quality Automation

### 5.1. Ruff Configuration (pyproject.toml)
Create a `pyproject.toml` file at the root level to enforce linter and formatter rules:

```
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E501"]
```

### 5.2. Workspace Configuration (.vscode/settings.json)
Configure VS Code to use the active Conda Python interpreter and format code on save:

```
{
  "python.defaultInterpreterPath": "~/.conda/envs/my-ml-env/bin/python",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

---

## 6. GitHub Connection & Initial Commit

Execute the following commands to commit and push the initial codebase:

```
git add .
git commit -m "chore: initial project setup and infrastructure"
git remote add origin git@github.com:username/repository-name.git
git push -u origin main
```