# Technical Documentation

## Module 03b: Data Validation (`src/validation.py`)

**Project:** PharmaSupply-ML  
**File:** `docs/03b_DATA_VALIDATION.md` (`src/validation.py`)  
**Status:** Validated  

---

<details>
<summary>🇫🇷 <b>Version Française (Cliquez pour dérouler)</b></summary>  

## 1. Vue d'ensemble et objectifs

Ce module assure la qualité et l'intégrité des données brutes stockées dans la base PostgreSQL avant leur utilisation par le pipeline de Feature Engineering et d'entraînement ML. 

L'objectif est d'agir comme une **porte de contrôle (Quality Gate)** automatisée pour bloquer immédiatement l'exécution du pipeline en cas d'anomalie ou de corruption des données.

---

## 2. Contrôles de qualité exécutés

Le script `src/validation.py` effectue trois niveaux d'assertions strictes sur la table `raw_pharmaceutical_demand` :

1. **Test de non-vacuité :**
   * Vérifie que la table contient au moins une ligne enregistrée.
2. **Conformité du schéma et valeurs nulles :**
   * S'assure de l'absence totale de valeurs manquantes (`NaN`/`NULL`) sur les colonnes critiques : `date`, `product_id`, `target_demand`, `sales_volume` et `stock_on_hand`.
3. **Assertions de cohérence métier (Ranges logiques) :**
   * **`target_demand` :** Doit être strictement supérieur ou égal à 0 (pas de demande négative).
   * **`stock_on_hand` :** Doit être strictement supérieur ou égal à 0 (pas de stock négatif).

---

## 3. Comportement en cas d'échec

Les vérifications s'appuient sur des instructions `assert` en Python. Si un seul des contrôles échoue :
* Une exception `AssertionError` est levée avec un message explicite.
* L'exécution du script s'arrête immédiatement, empêchant toute propagation de données invalides vers le modèle Machine Learning.

---

## 4. Exécution

Pour lancer la validation des données dans ton environnement Conda (`pharma-supply`) :

```bash
python src/validation.py
```

</details>

---

### [EN] English Version



## 1. Overview & Objectives

This module ensures the quality and integrity of raw data stored in the PostgreSQL database prior to its consumption by the Feature Engineering and ML training pipeline.

The core objective is to act as an automated **Quality Gate** that immediately halts pipeline execution whenever data anomalies or corruption are detected.

---

## 2. Executed Data Quality Checks

The `src/validation.py` script executes three levels of strict assertions on the `raw_pharmaceutical_demand` table:

1. **Non-Empty Table Check:**
   * Verifies that the target database table contains at least one record.
2. **Schema Compliance & Null Value Check:**
   * Ensures the complete absence of missing values (`NaN`/`NULL`) across critical columns: `date`, `product_id`, `target_demand`, `sales_volume`, and `stock_on_hand`.
3. **Business Logic Assertions (Valid Ranges):**
   * **`target_demand`:** Must be non-negative ($\ge 0$).
   * **`stock_on_hand`:** Must be non-negative ($\ge 0$).

---

## 3. Failure Behavior

Validation logic relies on standard Python `assert` statements. If any check fails:
* An `AssertionError` exception is raised with an explicit diagnostic message.
* Execution terminates immediately, preventing invalid or corrupted data from propagating to downstream machine learning steps.

---

## 4. Execution

To run the data validation pipeline within your Conda environment (`pharma-supply`):

```bash
python src/validation.py
```

