# Guide de Déploiement - PlantDiag

## 🚀 Démarrage local

### **Prérequis**
- Python 3.11+
- Docker et Docker Compose (recommandé)
- Git

### **Installation directe (sans Docker)**

```bash
# 1. Se placer dans le dossier backend
cd backend

# 2. Créer l'environnement virtuel (optionnel)
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer le serveur
python -m uvicorn app_minimal:app --host 0.0.0.0 --port 8000 --reload
```

Sans variable `DATABASE_URL`, l'application utilise une base SQLite locale
(`plantdiag.db`), créée automatiquement. C'est suffisant pour tester en local,
mais la version déployée utilise PostgreSQL (voir plus bas).

✅ **L'API est accessible sur `http://localhost:8000`**

### **Installation avec Docker (recommandée)**

```bash
# 1. Se placer dans le dossier backend
cd backend

# 2. Lancer Docker Compose
docker compose up --build

# 3. Services démarrés :
#    - API FastAPI       : http://localhost:8000
#    - PostgreSQL 15      : port 5432
#    - Redis 7            : port 6379
#    - Simulateur de capteurs IoT (envoie des relevés toutes les minutes)
```

### **Accès depuis un autre appareil sur le même réseau**
```
http://<IP_locale_du_PC>:8000
```

---

## 🌐 Déploiement Cloud

### **AWS EC2 (solution retenue et déployée)**

```bash
# 1. Créer une instance EC2 (Ubuntu 22.04, t2.micro)
# 2. Se connecter en SSH
ssh -i "cle.pem" ubuntu@<ip-instance>

# 3. Installer Docker
sudo apt update
sudo apt install -y docker.io docker-compose-plugin

# 4. Récupérer le code source
git clone https://github.com/Antonito35/diagnositique-plante.git
cd diagnositique-plante/backend

# 5. Démarrer l'application
sudo docker compose up -d --build

# 6. Accéder à l'API
http://<ip-instance>:8000
```

### **Autres infrastructures compatibles (non déployées)**

Le CDC autorise plusieurs environnements cloud. Le projet a été validé sur AWS,
mais l'architecture Docker le rend portable sans modification vers :

- **Azure Container Instances** : build de l'image, push vers un registre
  (Azure Container Registry), déploiement du conteneur avec les mêmes
  variables d'environnement (`DATABASE_URL`, `REDIS_URL`).
- **VMware vSphere (on-premise)** : export de l'image Docker (`docker save`),
  import sur une VM du datacenter, puis `docker compose up -d`.

Ces deux options n'ont pas été testées en conditions réelles pour ce projet ;
seul le déploiement AWS EC2 est en production.

---

## 📊 Aperçu des endpoints de l'API

L'API expose 18 endpoints au total, répartis en quatre familles.
Liste complète et testable : `http://localhost:8000/docs`

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Interface web |
| GET | `/health` | Vérification de disponibilité |
| POST | `/api/v1/auth/register` | Créer un compte |
| POST | `/api/v1/auth/login` | Se connecter (jeton JWT) |
| POST | `/api/v1/diagnose` | Diagnostic de maladie par photo |
| GET | `/api/v1/history/{user_id}` | Historique des diagnostics |
| GET/POST/PUT/DELETE | `/api/v1/parcels` | Gestion des parcelles |
| POST | `/api/v1/sensors/readings` | Réception d'un relevé de capteur |
| GET | `/api/v1/sensors/network` | État du réseau de capteurs |
| GET | `/api/v1/alerts/{user_id}` | Alertes croisées (capteurs + IA + météo) |
| GET | `/api/v1/weather` | Météo en temps réel |

**Exemple : diagnostic**
```bash
curl -X POST "http://localhost:8000/api/v1/diagnose?user_id=1&parcel_id=1" \
  -F "file=@photo.jpg"
```

---

## 🗄️ Base de données

### **SQLite (développement local uniquement)**
- Fichier `plantdiag.db`, créé automatiquement
- Utilisée seulement si `DATABASE_URL` n'est pas définie

### **PostgreSQL (utilisée en production)**
Définie via la variable d'environnement, déjà configurée dans `docker-compose.yml` :
```
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/plantdiag_db
```

### **Structure principale**

```sql
-- Utilisateurs
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    created_at TIMESTAMP
);

-- Parcelles
CREATE TABLE parcels (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR,
    crop_type VARCHAR,
    area_hectares FLOAT,
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMP
);

-- Diagnostics
CREATE TABLE diagnostics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    parcel_id INTEGER REFERENCES parcels(id),
    disease_name VARCHAR,
    confidence_score FLOAT,
    severity VARCHAR,
    created_at TIMESTAMP
);

-- Relevés des capteurs IoT
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY,
    parcel_id INTEGER REFERENCES parcels(id),
    sensor_code VARCHAR,
    soil_moisture_percent FLOAT,
    soil_temperature_celsius FLOAT,
    air_temperature_celsius FLOAT,
    air_humidity_percent FLOAT,
    leaf_wetness_percent FLOAT,
    battery_percent FLOAT,
    recorded_at TIMESTAMP
);
```

---

## 🔒 Sécurité

- ✅ Authentification par jeton JWT (Bcrypt pour les mots de passe)
- ✅ Validation systématique des données entrantes (Pydantic)
- ✅ CORS activé (à restreindre à un domaine précis en production réelle)
- ✅ Validation des images envoyées, taille limitée à 10 Mo
- ✅ PostgreSQL en production, SQLite réservé au développement local

---

## 📈 Performance observée

| Métrique | Valeur mesurée |
|----------|----------------|
| Temps de réponse du diagnostic | ~1,5 s |
| Fréquence des relevés capteurs | 1 par minute et par parcelle |
| Instance de déploiement | AWS EC2 t2.micro (1 vCPU, 1 Go RAM) |

---

## 🆘 Dépannage

**Le port 8000 est déjà utilisé**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux
lsof -i :8000
kill -9 <PID>
```

**Erreur de base de données en local**
```bash
# Supprimer la base SQLite locale
rm plantdiag.db

# Relancer (recréation automatique)
python -m uvicorn app_minimal:app --reload
```

**Espace disque insuffisant sur l'instance AWS**
```bash
# Nettoyer le cache de build Docker (sans toucher aux volumes de données)
sudo docker builder prune -af
```

**Dépendances manquantes**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📞 Support

- Documentation API interactive : `http://localhost:8000/docs`
- Dépôt du projet : https://github.com/Antonito35/diagnositique-plante

---

**Version** : 2.1
**Date** : 2026-09-21
**Statut** : ✅ Prêt pour la production
