# Procédure Opératoire : Infrastructure Base de Données & Conteneurisation Docker

## 1. Contexte & Rationale MLOps

L'objectif de cette étape est d'isoler l'infrastructure de stockage des données de notre pipeline MLOps. Dans un environnement de développement professionnel, l'installation directe des bases de données sur l'OS hôte (ou au sein de l'environnement virtuel Python) est proscrite pour éviter les effets de bord, les conflits de dépendances et les divergences de version entre développeurs (*« It works on my machine »*).

La technologie **Docker** associée à **Docker Compose** permet de garantir la **parité Dev/Prod** (*Dev-Prod Parity*) en instanciant un service PostgreSQL conteneurisé dont la configuration est entièrement déclarative, versionnée et reproductible.

---

## 2. Définition des Composants

### 2.1. Docker Engine & WSL2
Le moteur de conteneurisation s'exécute sur la couche Linux (WSL2/Ubuntu). Il assure le cloisonnement du processeur, de la mémoire et du réseau pour la base de données sans le surcoût d'une machine virtuelle classique.

### 2.2. Image vs Conteneur vs Volume
* **Image (`postgres:16-alpine`) :** Modèle immuable contenant l'exécutable PostgreSQL et son environnement d'exécution minimaliste.
* **Conteneur (`pharmasupply-db`) :** Instance vivante et isolée générée à partir de l'image.
* **Volume (`postgres_data`) :** Espace de stockage persistant géré par Docker sur le disque hôte, évitant la perte des données en cas d'arrêt ou de destruction du conteneur.

### 2.3. Réseau & Exposition des Ports
La redirection de port (`5432:5432`) fait le pont entre la boucle locale de l'hôte WSL/Windows et le port interne du conteneur. Cela permet aux scripts Python d'interagir avec la base de données comme si elle était installée localement.

---

## 3. Architecture des Fichiers de Configuration

```text
.
├── .env                  # Variables d'environnement sensibles (non versionné)
├── .env.example          # Gabarit des variables d'environnement (versionné)
├── docker-compose.yml    # Orchestration du service PostgreSQL
└── docs/
    └── DOCKER_SETUP.md   # La présente documentation
```

### 3.1. Fichier .env (Sécurité & Isolation des Secrets)  
Le fichier .env héberge les identifiants d'accès. Il ne doit jamais être poussé sur Git.

```
POSTGRES_USER=mlops_user
POSTGRES_PASSWORD=mlops_secure_password
POSTGRES_DB=pharmasupply_db
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

### 3.2. Fichier docker-compose.yml (Déclaration de l'Infrastructure)  
Ce fichier orchestre le démarrage du conteneur en associant l'image, les variables d'environnement,  
les volumes et la vérification d'état (healthcheck).

```yaml
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
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    driver: local

```
### Explication de la configuration


* **`image: postgres:16-alpine`** : Image officielle PostgreSQL 16 basée sur Alpine Linux (ultra-légère).
* **`container_name: pharmasupply-db`** : Nom explicite donné au conteneur.
* **`restart: always`** : Redémarre automatiquement le conteneur en cas de crash ou de redémarrage système.
* **`env_file: - .env`** : Charge les variables définies dans le fichier `.env`.
* **`environment`** : Transmet l'utilisateur, le mot de passe et le nom de la base au conteneur.
* **`ports`** : Mappe le port local `5432` au port `5432` interne du conteneur.
* **`volumes`** : Persiste les données de la base dans le volume nommé `postgres_data`.
* **`healthcheck`** : Teste toutes les 5 secondes (`pg_isready`) pour vérifier si la base est prête à recevoir des connexions.

## 4. Cycle de Vie & Commandes d'Exploitation  
Toutes les commandes s'exécutent depuis la racine du projet dans le terminal WSL.

| Action | Commande | Description |
| :--- | :--- | :--- |
| **Démarrage** | `docker compose up -d` | Télécharge l'image, crée le volume et lance le conteneur en arrière-plan. |
| **Vérification** | `docker compose ps` | Affiche l'état du conteneur (doit indiquer `healthy`). |
| **Consultation Logs** | `docker compose logs -f` | Affiche le flux de journaux PostgreSQL en temps réel. |
| **Arrêt (sans perte)** | `docker compose stop` | Arrête le conteneur en préservant la donnée dans le volume. |
| **Nettoyage complet** | `docker compose down -v` | Supprime le conteneur, le réseau et **purge le volume de données**. |

## 5. Interaction avec le Pipeline Python (Infrastructures Unifiées)  
Une fois le conteneur opérationnel (healthy), la chaîne de connexion SQLAlchemy est construite  
dynamiquement à partir des variables d'environnement :  

$$\text{URL DB} = \text{postgresql://} + \text{USER} + \text{:} + \text{PASSWORD} + \text{@} + \text{HOST} + \text{:} + \text{PORT} + \text{/} + \text{DB}$$

Le script d'ingestion Python (src/data/ingest_to_db.py) utilisera cette chaîne de connexion pour lire le fichier CSV (data/pharmaceutical_demand.csv) et structurer la table SQL correspondante.