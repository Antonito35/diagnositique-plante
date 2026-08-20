# 🚀 GUIDE D'INSTALLATION - PlantDiag

## Prérequis

### Système
- Windows 11 / macOS / Linux
- 8GB RAM minimum
- 20GB disque disponible

### Logiciels requis
- **Git** : https://git-scm.com/download
- **Docker** & **Docker Compose** : https://www.docker.com/products/docker-desktop
- **Python 3.9+** : https://www.python.org/downloads/
- **Flutter 3.13+** : https://flutter.dev/docs/get-started/install
- **VS Code** : https://code.visualstudio.com/ (recommandé)

---

## Installation rapide (Docker - Recommandé)

### 1. Cloner le projet

```bash
git clone https://github.com/yourteam/plantdiag.git
cd plantdiag
```

### 2. Démarrer tous les services

```bash
docker-compose up --build
```

Les services démarreront :
- **API** : http://localhost:8000
- **Swagger UI** : http://localhost:8000/docs
- **PostgreSQL** : localhost:5432
- **Redis** : localhost:6379
- **pgAdmin** : http://localhost:5050

### 3. Vérifier la santé

```bash
curl http://localhost:8000/health
```

**Réponse attendue :**
```json
{
  "status": "healthy",
  "timestamp": "...",
  "model": "loaded"
}
```

---

## Installation locale (Sans Docker)

### Backend - FastAPI

#### 1. Configuration de l'environnement Python

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

#### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

#### 3. Configuration environnement

```bash
# Copier fichier exemple
cp .env.example .env

# Éditer .env avec vos paramètres
# DATABASE_URL, REDIS_URL, SECRET_KEY, etc.
```

#### 4. Initialiser la base de données

```bash
# Assurez-vous que PostgreSQL est en cours d'exécution
# Créer la base de données
createdb plantdiag

# Charger le schéma
psql plantdiag < ../infra/init.sql
```

#### 5. Lancer l'API

```bash
python -m uvicorn app:app --reload

# Ou directement
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

L'API est accessible : http://localhost:8000

**Logs attendus :**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     🚀 Starting PlantDiag API...
INFO:     ✅ ML model loaded successfully
INFO:     Application startup complete [PID 12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 6. Lancer les tests

```bash
pytest test_app.py -v
```

**Couverture de test :**
- ✅ Health checks
- ✅ Diagnosis endpoint
- ✅ History retrieval
- ✅ Parcel management
- ✅ Sensor data
- ✅ Error handling
- ✅ Performance (< 100ms health check)

---

### Mobile - Flutter

#### 1. Installation de Flutter

```bash
# Vérifier installation
flutter --version

# Doctor check
flutter doctor
```

#### 2. Récupérer dépendances

```bash
cd mobile
flutter pub get
```

#### 3. Lancer sur émulateur Android

```bash
# Lister les émulateurs
flutter emulators

# Lancer un émulateur
flutter emulators launch Pixel_4_API_30

# Lancer l'app
flutter run -d emulator-5554
```

#### 4. Lancer sur iOS (macOS uniquement)

```bash
# Lancer sur simulateur
flutter run -d iPhone

# Ou build pour device réel
flutter run -d your-ios-device
```

#### 5. Build pour production

```bash
# Android APK
flutter build apk --release
# Output: build/app/outputs/apk/release/app-release.apk

# iOS
flutter build ios --release
```

---

## Configuration PostgreSQL

### Avec Docker Compose (Automatique)
La base de données est créée automatiquement via `infra/init.sql`

### Manuellement

#### Installation PostgreSQL
```bash
# macOS
brew install postgresql

# Windows (via installer)
# https://www.postgresql.org/download/windows/

# Linux (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib
```

#### Créer l'utilisateur et la base

```bash
psql -U postgres

CREATE USER plantdiag_user WITH PASSWORD 'plantdiag_password_dev';
CREATE DATABASE plantdiag OWNER plantdiag_user;
ALTER DATABASE plantdiag SET client_encoding = 'UTF8';
ALTER DATABASE plantdiag SET default_transaction_isolation = 'read committed';

# Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE plantdiag TO plantdiag_user;

# Quitter
\q
```

#### Charger le schéma

```bash
psql -U plantdiag_user -d plantdiag < infra/init.sql
```

#### Vérifier

```bash
psql -U plantdiag_user -d plantdiag

# Dans psql
\dt  # Lister les tables
SELECT * FROM users LIMIT 1;
```

---

## Configuration Redis

### Avec Docker Compose (Automatique)
Redis démarre automatiquement sur `localhost:6379`

### Installation locale

```bash
# macOS
brew install redis
redis-server

# Linux
sudo apt-get install redis-server
redis-server

# Windows (WSL recommandé)
wsl
sudo apt-get install redis-server
redis-server
```

---

## Tester l'API

### 1. Swagger UI (Interface graphique)

```
http://localhost:8000/docs
```

- Cliquer sur chaque endpoint
- Cliquer "Try it out"
- Remplir les paramètres
- Cliquer "Execute"

### 2. Via cURL (Terminal)

```bash
# Health check
curl http://localhost:8000/health

# Créer une parcelle
curl -X POST "http://localhost:8000/api/v1/parcels?user_id=123" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Parcel","crop_type":"Wheat","area_hectares":5.0}'

# Diagnostic (avec image)
curl -X POST "http://localhost:8000/api/v1/diagnose" \
  -F "file=@photo.jpg" \
  -F "user_id=123" \
  -F "parcel_id=456"

# Récupérer l'historique
curl "http://localhost:8000/api/v1/history/123"

# Données capteurs
curl "http://localhost:8000/api/v1/sensors/456"
```

### 3. Via Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Créer une parcelle
response = requests.post(
    f"{BASE_URL}/api/v1/parcels?user_id=123",
    json={
        "name": "Test Parcel",
        "crop_type": "Wheat",
        "area_hectares": 5.0
    }
)
print(response.json())

# Diagnosis
with open("photo.jpg", "rb") as f:
    files = {"file": f}
    data = {"user_id": 123, "parcel_id": 456}
    response = requests.post(
        f"{BASE_URL}/api/v1/diagnose",
        files=files,
        data=data
    )
    print(response.json())
```

### 4. Via Postman

1. Télécharger Postman : https://www.postman.com/downloads/
2. Importer la collection : [plantdiag-postman.json](../backend/plantdiag-postman.json)
3. Configurer les variables :
   - `{{BASE_URL}}` = `http://localhost:8000`
   - `{{USER_ID}}` = `123`
4. Exécuter les requests

---

## Troubleshooting

### API ne démarre pas

```bash
# Vérifier les erreurs
docker-compose logs api

# Vérifier les ports utilisés
# Windows
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :8000

# Tuer le processus
kill -9 <PID>
```

### Erreur PostgreSQL "connection refused"

```bash
# Vérifier que Postgres est lancé
docker-compose logs postgres

# Vérifier les credentials
psql -U plantdiag_user -d plantdiag
```

### Erreur "No such image or build error"

```bash
# Reconstruire les images
docker-compose build --no-cache

# Supprimer les volumes (attention : données perdues)
docker-compose down -v

# Redémarrer
docker-compose up
```

### Port déjà utilisé

```bash
# Changer le port dans docker-compose.yml
# ports:
#   - "9000:8000"  # Au lieu de 8000:8000

# Ou l'arrêter
docker-compose down
```

### Model ML ne charge pas

```bash
# Vérifier que le fichier existe
ls -la models/

# Logs détaillés
docker-compose logs api | grep -i model

# Réinstaller les dépendances
pip install --force-reinstall tensorflow
```

---

## Développement

### Avant de coder

```bash
# Créer une branche
git checkout -b feature/votre-fonctionnalite

# Installer pre-commit hooks (optionnel)
pip install pre-commit
pre-commit install
```

### Format du code

```bash
# Python (Backend)
pip install black flake8

# Formatter
black backend/

# Linter
flake8 backend/ --max-line-length=100

# Dart (Mobile)
dart format lib/
flutter analyze
```

### Commits

```bash
git add .
git commit -m "feat: add diagnosis endpoint"
git commit -m "fix: handle invalid images"
git commit -m "docs: update API documentation"
```

**Types de commits :**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `refactor:` Refactorisation
- `test:` Tests

---

## Production

### Déploiement sur AWS

```bash
# 1. Build l'image Docker
docker build -t plantdiag:1.0.0 .

# 2. Tag pour ECR
docker tag plantdiag:1.0.0 YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/plantdiag:1.0.0

# 3. Push sur ECR
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com
docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/plantdiag:1.0.0

# 4. Déployer sur ECS/Fargate ou EC2
```

### Déploiement sur Azure

```bash
# Via Container Registry
az acr build --registry REGISTRY_NAME --image plantdiag:1.0.0 .

# Via App Service
az webapp deployment container config --name APP_NAME --resource-group GROUP_NAME --enable-cd true
```

### Variables d'environnement (Production)

```bash
# Ne JAMAIS committer de secrets !
# Utiliser des secrets managers

# AWS Secrets Manager
# Azure Key Vault
# HashiCorp Vault
```

### Checklist avant production

- [ ] Tests passent (pytest)
- [ ] Linting OK (flake8, black)
- [ ] Secrets configurés (pas en git)
- [ ] HTTPS/SSL configuré
- [ ] CORS configuré correctement
- [ ] Logging en place
- [ ] Monitoring en place
- [ ] Backup/DR plan
- [ ] Documentation à jour

---

## Support

- **Documentation technique** : [/docs](./docs/)
- **API Reference** : http://localhost:8000/docs
- **Issues GitHub** : https://github.com/yourteam/plantdiag/issues
- **Email** : team@plantdiag.farm

---

**Version** : 1.0  
**Dernière maj** : 20 août 2026  
**Statut** : Production-ready ✅
