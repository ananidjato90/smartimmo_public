# SmartImmo – Plateforme immobilière pour le Togo

SmartImmo est une application web conçue pour faciliter la recherche, la location et la vente d'appartements, de maisons et de terrains sur le territoire togolais. La solution s'appuie sur un backend **Python/FastAPI**, un frontend **Angular**, une base de données **MySQL** et un orchestrateur **Docker**. Un agent IA open source basé sur **Ollama** (modèle `llama3`) permet aux utilisateurs de formuler des requêtes immobilières en langage naturel.

## Table des matières
- [Architecture](#architecture)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Structure du projet](#structure-du-projet)
- [Prérequis](#prérequis)
- [Installation pour le développement](#installation-pour-le-développement)
- [Démarrage avec Docker](#démarrage-avec-docker)
- [Configuration de l'environnement](#configuration-de-lenvironnement)
- [Base de données et seed](#base-de-données-et-seed)
- [Agent IA](#agent-ia)
- [API REST](#api-rest)
- [Interface Angular](#interface-angular)
- [Tests et qualité](#tests-et-qualité)
- [Roadmap suggérée](#roadmap-suggérée)

## Architecture

```
workspace/
├── backend/           # API FastAPI + ORM SQLAlchemy + intégration Ollama
│   ├── app/
│   │   ├── api/       # Routes versionnées (v1)
│   │   ├── models.py  # Modèles ORM (users, properties, favorites…)
│   │   ├── schemas.py # Schémas Pydantic (validation et sérialisation)
│   │   ├── services/  # Intégrations tierces (agent IA, etc.)
│   │   ├── seed.py    # Script d'initialisation de données
│   │   └── main.py    # Point d'entrée FastAPI
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/          # Application Angular standalone components
│   ├── src/
│   │   ├── app/       # Pages, composants et services métiers
│   │   └── environments/
│   ├── angular.json
│   └── Dockerfile
├── docker-compose.yml # Orchestration backend, frontend, MySQL, Ollama
└── README.md
```

## Fonctionnalités principales

- Gestion des annonces : création, consultation, mise à jour et suppression de propriétés (appartement, maison, terrain, commercial).
- Recherche multi-critères (ville, type, prix, chambres, statut, propriétés mises en avant).
- Gestion des utilisateurs et des favoris.
- Assistant conversationnel en langage naturel propulsé par Ollama pour suggérer des biens et filtrer les annonces.
- UI moderne en Angular avec Angular Material, formulaire de recherche et panneau d’assistance IA.
- Images associées aux annonces et différenciation des biens vedettes.

## Structure du projet

### Backend (`backend/`)
- **FastAPI** pour l'exposition des endpoints REST (`/api/v1`).
- **SQLAlchemy 2.x** pour l'ORM et la définition des modèles.
- **MySQL** comme base de données relationnelle (pilote `PyMySQL`).
- **Pydantic 2.x** pour la validation des données.
- **Passlib (bcrypt)** pour le hachage des mots de passe.
- **httpx** pour la communication asynchrone avec Ollama.

### Frontend (`frontend/`)
- **Angular 17** avec composants standalone.
- **Angular Material** pour la couche UI.
- **RxJS** pour la consommation des services REST.
- **Services** dédiés pour les propriétés, favoris, utilisateurs et IA.
- **Composants** : carte propriété, filtres, panneau assistant IA.

### Orchestration
- **Docker Compose** assemble les services `backend`, `frontend`, `db` (MySQL) et `llm` (Ollama).
- **Nginx** sert le bundle Angular et reverse-proxy vers le backend (`/api`).

## Prérequis

| Outil                | Version conseillée |
|----------------------|--------------------|
| Python               | 3.11+              |
| Node.js & npm        | Node 20 / npm 10   |
| Angular CLI          | 17.x               |
| Docker & Compose     | 24+ / compose v2   |
| MySQL client (option)| 8.x                |

## Installation pour le développement

### 1. Backend FastAPI

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copie du fichier d'environnement
cp .env.example .env

# Lancement du serveur (rechargement auto)
uvicorn app.main:app --reload
```

Le backend écoute par défaut sur `http://localhost:8000`.

### 2. Frontend Angular

```bash
cd frontend
npm install
npm start
```

Le frontend est disponible sur `http://localhost:4200`.

Veillez à mettre à jour l'URL de l'API dans `src/environments/environment.ts` si nécessaire.

### Raccourci : commandes essentielles (mode développeur)

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (dans un autre terminal)
cd frontend
npm install
npm start

# (Optionnel) seed de données de démonstration
cd backend
python -m app.seed
```

## Démarrage avec Docker

```bash
# À la racine du projet
docker compose up --build
```

Services exposés :

| Service   | URL                         |
|-----------|-----------------------------|
| Frontend  | http://localhost:4200       |
| Backend   | http://localhost:8000       |
| Swagger   | http://localhost:8000/docs  |
| Redoc     | http://localhost:8000/redoc |
| MySQL     | localhost:3306              |
| Ollama    | http://localhost:11434      |

> **Remarque :** Le service `llm` télécharge automatiquement le modèle `llama3` au premier démarrage. Le téléchargement peut prendre plusieurs minutes selon la connexion.

### Raccourci : commandes essentielles (mode Docker)

```bash
docker compose up --build

# (Optionnel) seed de données après le démarrage des services
docker compose exec backend python -m app.seed
```

## Configuration de l'environnement

Variables disponibles dans `backend/.env.example` :

```env
APP_NAME=Smart Immo API
ENVIRONMENT=development
DEBUG=True

MYSQL_USER=smartimmo
MYSQL_PASSWORD=smartimmo
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_DATABASE=smartimmo

CORS_ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200

OLLAMA_HOST=http://llm:11434
OLLAMA_MODEL=llama3
```

Pour un déploiement, adaptez `MYSQL_*`, `CORS_ALLOWED_ORIGINS`, `OLLAMA_HOST` et `OLLAMA_MODEL` à votre infrastructure.

## Base de données et seed

Le script `backend/app/seed.py` initialise :
- Un utilisateur administrateur `demo@smartimmo.tg` (mot de passe `DemoPass123!`).
- Trois annonces exemples (appartement à Lomé, villa avec piscine, terrain à Kpalimé).

### Exécuter le seed (hors Docker)

```bash
cd backend
python -m app.seed
```

### Exécuter le seed (Docker)

```bash
docker compose exec backend python -m app.seed
```

## Agent IA

- Basé sur **Ollama** et le modèle open source `llama3` (modifiable via `OLLAMA_MODEL`).
- Endpoint d'API : `POST /api/v1/ai/query` avec payload `{ "prompt": "..." }`.
- Le service `app/services/ai_agent.py` interroge Ollama via HTTP (`/api/generate`).
- L'UI Angular fournit un panneau latéral où les utilisateurs saisissent des requêtes en langage naturel (ex: *« Je cherche un terrain de 500 m² à Lomé autour de 15 millions »*).

## API REST

### Endpoints principaux (FastAPI)

| Méthode | Route                             | Description                              |
|---------|-----------------------------------|------------------------------------------|
| GET     | `/api/v1/health`                  | Vérification de l'état du service        |
| POST    | `/api/v1/users`                   | Créer un utilisateur                     |
| POST    | `/api/v1/users/login`             | Authentification simplifiée              |
| GET     | `/api/v1/properties`              | Lister les annonces (filtres via query)  |
| POST    | `/api/v1/properties`              | Créer une annonce                        |
| GET     | `/api/v1/properties/{id}`         | Récupérer une annonce                    |
| PUT     | `/api/v1/properties/{id}`         | Mettre à jour une annonce                |
| DELETE  | `/api/v1/properties/{id}`         | Supprimer une annonce                    |
| GET     | `/api/v1/favorites`               | Lister les favoris de l'utilisateur      |
| POST    | `/api/v1/favorites/{property_id}` | Ajouter une annonce aux favoris          |
| DELETE  | `/api/v1/favorites/{property_id}` | Retirer une annonce des favoris          |
| POST    | `/api/v1/ai/query`                | Interroger l'assistant IA                |

> **Authentification** : pour simplifier la démonstration, l'API considère le premier utilisateur actif comme « utilisateur courant ». Implémentez un vrai système JWT/Session pour la production.

## Interface Angular

### Pages principales
- **Accueil** : zone de recherche, grille de cartes, assistant IA.
- **Détails d'une propriété** : galerie, caractéristiques, résumé.
- **Favoris** : liste des annonces sauvegardées.

### Composants clés
- `SearchFiltersComponent` : formulaire réactif avec filtres dynamiques.
- `PropertyCardComponent` : carte synthétique d'un bien.
- `AiAssistantPanelComponent` : dialogue avec l'IA, affichage des recommandations.

### Services Angular
- `ApiService` : communication REST avec le backend (annonces, favoris, utilisateurs).
- `AiAgentService` : envoi des prompts à l'endpoint IA.

## Tests et qualité

- **Backend** : intégrer `pytest` + `httpx.AsyncClient` pour des tests d'API (à planifier).
- **Frontend** : tests unitaires via Karma/Jasmine (`npm test`), tests end-to-end via Cypress ou Playwright (à ajouter).
- **CI/CD** : pipeline suggéré avec lint (`ruff`, `eslint`), build Docker et déploiement automatisé.

## Roadmap suggérée

1. **Authentification avancée** : JWT, rôles (administrateur, agent, client), réinitialisation de mot de passe.
2. **Gestion des médias** : stockage S3 ou service local avec optimisation d'images.
3. **Notifications** : alertes email/SMS pour nouvelles annonces correspondant aux filtres enregistrés.
4. **Tableau de bord agents** : statistiques de visites, gestion des prospects, calendrier de visites.
5. **Optimisation IA** : fine-tuning sur corpus local, ajout de fonctionnalités de conversation continue, recommandations personnalisées.
6. **Internationalisation** : support multilingue (français, anglais).
7. **Tests automatisés** : couverture complète backend/frontend, tests contractuels d'API.


# Récapitulatif des commandes pour lancer l'application en local 
## Backend (FastAPI)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm --version
nvm install 20
nvm use 20
rm -rf node_modules package-lock.json
npm install


pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend (Angular)
```bash
cd frontend
npm install
npm start
Accès UI : http://localhost:4200
```

## Seed des données (optionnel, après lancement backend)
```bash
cd backend
python -m app.seed
```

## Alternative Docker Compose
```bash
docker compose up --build
```

Attendre le téléchargement initial du modèle Ollama (llama3).
Accès frontend : http://localhost:4200 • API : http://localhost:8000
(Exécuter docker compose exec backend python -m app.seed pour remplir l’exemple de données).

---

### Support

Pour toute question ou contribution, créez une issue ou ouvrez une pull request. Bonne exploration de SmartImmo !
