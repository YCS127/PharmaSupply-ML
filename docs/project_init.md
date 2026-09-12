# Checklist & Guide Universel d'Initialisation de Projet MLOps

Ce document récapitule la procédure opératoire permanente (SOP) pour initialiser un environnement de développement Data/MLOps propre, isolé, reproductible et prêt pour la production sous Linux (**WSL2 / Zsh**).

---

## 1. Structure du Projet & Arborescence

### 1.1. Création du dossier et des sous-répertoires
Depuis le terminal WSL (Zsh), exécuter la commande suivante pour générer la structure modulaire :

```zsh
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

```zsh
conda create -n mon-env-ml python=3.11 -y
conda activate mon-env-ml
pip install pandas numpy scikit-learn ruff
```

### 2.2. Exportation de la configuration (environment.yml)
Pour garantir la reproductibilité exacte de l'environnement par d'autres développeurs :

```zsh
conda env export --no-builds > environment.yml
```
---

## 3. Configuration du Versioning Git

### 3.1. Initialisation du dépôt local

```zsh
git init
git branch -M main
```

### 3.2. Création du fichier .gitignore
À la racine du projet, créer le fichier .gitignore pour exclure les données, caches et secrets :

```gitignore
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
```

Remarque : Ajouter si nécessaire le fichier du workspace

---

## 4. Documentation Principale : README.md

Créer le fichier README.md à la racine pour présenter le projet, la stack et la feuille de route (à adapter au projet) :

```markdown
# Nom du Projet

## Description
Présentation synthétique du problème métier et de la solution MLOps visée.

## Stack Technique (bien-sûr il faut adapter)
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

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E501"]
```

### 5.2. Configuration de l'Espace de Travail (.vscode/settings.json)
Pour forcer VS Code à utiliser automatiquement le bon interpréteur Python et formater à la sauvegarde, nous créons un dossier caché dans lequel nous insérons le fichier .json :

```json
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

```git
git add .
git commit -m "chore: initial project setup and infrastructure"
git remote add origin git@github.com:nom-utilisateur/nom-du-depot.git
git push -u origin main
```