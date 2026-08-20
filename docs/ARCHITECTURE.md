# 🏗️ ARCHITECTURE SYSTÈME - PlantDiag

## 1. Vue d'ensemble

PlantDiag est une architecture **3-tiers** déployée dans le cloud avec une app mobile, une API backend, et une base de données.

```
┌─────────────────────────────────────────────────────────────────┐
│                         UTILISATEUR AGRICULTEUR                  │
└────────────┬─────────────────────────────────────────────────────┘
             │
             │ HTTPS/TLS
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TIER 1: APPLICATION MOBILE                     │
│                          (Flutter)                                │
├─────────────────────────────────────────────────────────────────┤
│  • Camera Screen (Capture photo)                                 │
│  • Diagnosis Screen (Affichage résultat)                         │
│  • History Screen (Historique diagnostics)                       │
│  • Parcels Screen (Liste parcelles)                              │
│  • Dashboard (Vue globale)                                       │
└────────────┬─────────────────────────────────────────────────────┘
             │
             │ HTTP/REST API Calls
             │ POST /diagnose
             │ GET /history/{user_id}
             │ GET /parcels
             │ GET /sensors
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TIER 2: BACKEND API                            │
│                        (FastAPI - Python)                         │
├─────────────────────────────────────────────────────────────────┤
│  Routes:                                                         │
│  • /diagnose (POST) - Reçoit photo, retourne diagnostic          │
│  • /history (GET) - Récupère historique par user_id              │
│  • /parcels (GET/POST) - Gestion des parcelles                   │
│  • /sensors (GET) - Données IoT simulées                         │
│  • /docs (GET) - Documentation Swagger                           │
│                                                                  │
│  Services:                                                       │
│  • ML Engine (MobileNetV2 + TensorFlow Lite)                    │
│  • Database ORM (SQLAlchemy)                                     │
│  • Authentication (JWT tokens)                                   │
│  • Logging & Monitoring                                          │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ├─────────────────────────────────────────────┬────────┐
             │                                             │        │
             ▼                                             ▼        ▼
┌──────────────────────────┐  ┌─────────────────────┐ ┌───────────┐
│   TIER 3: DATABASE       │  │  ML MODEL CACHE     │ │ FILE      │
│   PostgreSQL             │  │  (In-Memory)        │ │ STORAGE   │
├──────────────────────────┤  ├─────────────────────┤ ├───────────┤
│ • Users                  │  │ • MobileNetV2       │ │ • Photos  │
│ • Parcels                │  │ • Labels (5-7 mal)  │ │ • Reports │
│ • Diagnoses              │  │ • Cached 24/7       │ │           │
│ • Sensors data           │  │                     │ │           │
│ • Treatment history      │  │                     │ │           │
└──────────────────────────┘  └─────────────────────┘ └───────────┘
```

---

## 2. Architecture Matérielle (Cloud Deployment)

### Hébergement Cloud

```
┌───────────────────────────────────────────────────────────────────┐
│                    CLOUD PROVIDER (AWS/Azure/VMware)              │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              LOAD BALANCER (ALB/Azure LB)                  │  │
│  │              (Distribute traffic across instances)          │  │
│  └────────────┬───────────────────────────────────────────────┘  │
│               │                                                    │
│  ┌────────────▼─────────────┬──────────────┬─────────────────┐   │
│  │                          │              │                 │   │
│  ▼                          ▼              ▼                 ▼   │
│  ┌──────────────────┐  ┌──────────────┐  ┌────────────┐  ┌────┐ │
│  │ App Container 1  │  │ App Container│  │ App Cont.  │  │ ..│ │
│  │ (Docker - FastAPI│  │ (Docker)     │  │ (Docker)   │  │   │ │
│  │ + Gunicorn)      │  │              │  │            │  │   │ │
│  └────────┬─────────┘  └──────┬───────┘  └──────┬─────┘  └────┘ │
│           │                   │                 │               │
│           └───────────────────┼─────────────────┘               │
│                               │                                  │
│  ┌────────────────────────────▼──────────────────────────────┐  │
│  │           SHARED STORAGE                                  │  │
│  │  • PostgreSQL Database                                   │  │
│  │  • Redis Cache                                           │  │
│  │  • S3/Blob Storage (Photos)                              │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           MONITORING & LOGGING                           │   │
│  │  • CloudWatch/Azure Monitor                              │   │
│  │  • ELK Stack (Elasticsearch, Logstash, Kibana)           │   │
│  │  • Error tracking (Sentry)                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└───────────────────────────────────────────────────────────────────┘
```

---

## 3. Diagramme de flux de données

### Scénario : Diagnostic d'une maladie

```
1. UTILISATEUR CAPTURE PHOTO
   ├─ Ouvre l'app mobile
   ├─ Va à "Scan photo"
   ├─ Prend photo ou choisit depuis galerie
   ├─ Valide et confirme
   └─ Compress automatiquement (< 1MB)

2. ENVOI À L'API
   ├─ Format: multipart/form-data
   ├─ Headers:
   │  ├─ Content-Type: multipart/form-data
   │  ├─ Authorization: Bearer {JWT_TOKEN}
   │  └─ User-Agent: FlutterApp/1.0
   ├─ Body:
   │  ├─ file: [image.jpg binary]
   │  ├─ user_id: 123
   │  └─ parcel_id: 456
   └─ POST /api/v1/diagnose

3. TRAITEMENT À L'API
   ├─ Reçoit la requête
   ├─ Valide le JWT token
   ├─ Valide le format de l'image
   ├─ Charge le modèle ML (si pas en cache)
   ├─ Pré-traite l'image (redimensionne, normalise)
   ├─ Exécute la prédiction
   │  └─ MobileNetV2 → Probabilities [disease1, disease2, ...]
   ├─ Récupère le top-1 diagnostic
   ├─ Charge les recommandations depuis DB
   ├─ Insère en base de données
   │  ├─ CREATE diagnosis record
   │  ├─ STORE image path
   │  └─ LOG timestamp & user_id
   └─ Retourne JSON response

4. AFFICHAGE DU RÉSULTAT
   ├─ App reçoit JSON:
   │  {
   │    "diagnosis": "Rouille du blé",
   │    "confidence": 0.92,
   │    "severity": "Modérée",
   │    "treatments": {
   │      "preventive": "Rotation cultures",
   │      "biological": "Bacillus subtilis",
   │      "conventional": "Triazole fongicide"
   │    },
   │    "recommendation": "Traiter rapidement"
   │  }
   ├─ Affiche maladie en grand
   ├─ Barre de confiance (92%)
   ├─ 3 onglets traitement
   └─ Bouton "Sauvegarder" ou "Ajouter à la parcelle"

5. PERSISTANCE
   ├─ Utilisateur valide le diagnostic
   ├─ App envoie POST /api/v1/history
   ├─ Diagnostic sauvegardé en PostgreSQL
   ├─ Photo stockée en S3/blob storage
   └─ Notification utilisateur "✓ Diagnostic sauvegardé"
```

---

## 4. Schéma de la base de données

```sql
-- Utilisateurs
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    farm_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Parcelles
CREATE TABLE parcels (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    crop_type VARCHAR(100),
    area_hectares DECIMAL(10,2),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Diagnostics
CREATE TABLE diagnoses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    parcel_id INTEGER REFERENCES parcels(id),
    disease_name VARCHAR(255) NOT NULL,
    confidence DECIMAL(3,2) CHECK (confidence >= 0 AND confidence <= 1),
    severity VARCHAR(50),
    image_path VARCHAR(512),
    ml_model_version VARCHAR(50),
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Recommandations de traitement
CREATE TABLE treatments (
    id SERIAL PRIMARY KEY,
    disease_id INTEGER REFERENCES diagnoses(id),
    treatment_type VARCHAR(50), -- 'preventive', 'biological', 'conventional'
    description TEXT,
    effectiveness_rate DECIMAL(3,2),
    duration_days INTEGER,
    cost_estimate DECIMAL(10,2)
);

-- Données capteurs simulées
CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    parcel_id INTEGER NOT NULL REFERENCES parcels(id),
    temperature_celsius DECIMAL(5,2),
    humidity_percent DECIMAL(5,2),
    soil_moisture_percent DECIMAL(5,2),
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## 5. Architecture des containers

### Docker Compose Setup

```yaml
version: '3.8'

services:
  # Backend API
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: plantdiag_api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/plantdiag
      REDIS_URL: redis://cache:6379
      ENVIRONMENT: production
    depends_on:
      - db
      - cache
    volumes:
      - ./backend:/app
      - ./models:/app/models
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: plantdiag_db
    environment:
      POSTGRES_USER: plantdiag_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: plantdiag
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U plantdiag_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  cache:
    image: redis:7-alpine
    container_name: plantdiag_cache
    ports:
      - "6379:6379"
    volumes:
      - cache_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Nginx Reverse Proxy (optionnel)
  nginx:
    image: nginx:alpine
    container_name: plantdiag_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infra/nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - api
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  db_data:
  cache_data:
```

---

## 6. Spécifications des performances

| Métrique | Cible | Justification |
|----------|-------|---------------|
| **Latence API** | < 2 secondes | ML inference rapide |
| **Throughput** | 100 req/sec minimum | Pour 10-20 agriculteurs simultanés |
| **Uptime** | 99.9% (SLA) | Service critique pendant saison |
| **Image photo max** | 10 MB | Compressée automatiquement |
| **Model load time** | < 500ms | Cache en mémoire |
| **Database query** | < 100ms | Index optimisé |
| **Mobile app size** | < 150 MB | Download rapide sur 4G |

---

## 7. Sécurité

### Authentication & Authorization
- ✅ JWT tokens (HS256, expiration 24h)
- ✅ Refresh tokens (7 jours)
- ✅ Password hashing (bcrypt, 12 rounds)
- ✅ Rate limiting (100 req/min par IP)

### Data Protection
- ✅ HTTPS/TLS 1.3 (chiffrage en transit)
- ✅ AES-256 pour données sensibles en base
- ✅ Photos stockées avec accès restreint
- ✅ CORS configuré (mobile app domain only)

### Input Validation
- ✅ File upload validation (magic bytes)
- ✅ Image size/format checks
- ✅ SQL injection prevention (ORM)
- ✅ XSS prevention (JSON responses only)

---

## 8. Monitoring & Observabilité

### Logs
```
Format: [TIMESTAMP] [LEVEL] [SERVICE] [REQUEST_ID] [MESSAGE]
Exemple:
[2026-08-20T14:30:45Z] [INFO] [api] [req-12345] User 123 uploaded diagnosis
[2026-08-20T14:30:46Z] [DEBUG] [api] [req-12345] ML model prediction: Rust 0.92
[2026-08-20T14:30:47Z] [INFO] [api] [req-12345] Diagnosis saved to DB
```

### Métriques
- Request latency (p50, p95, p99)
- ML model inference time
- Error rates par endpoint
- Database connection pool usage
- Cache hit rate

### Alertes
- ❌ API down (health check failed)
- ❌ Error rate > 5%
- ❌ Latency p95 > 3s
- ❌ Database connection pool exhausted
- ⚠️ Disk usage > 80%

---

## 9. Déploiement CI/CD

```yaml
Pipeline:
1. GitHub Push
   └─ Trigger GitHub Actions
2. Build Stage
   ├─ Run tests (pytest)
   ├─ Lint code (black, flake8)
   └─ Security scan (bandit)
3. Docker Build
   ├─ Build image
   ├─ Push to registry
   └─ Tag version
4. Deploy Stage
   ├─ SSH to cloud instance
   ├─ Pull latest image
   ├─ Run docker-compose up
   └─ Run health checks
5. Post-Deploy
   ├─ Smoke tests
   ├─ Monitor logs
   └─ Notify team
```

---

## 10. Scaling & Load Balancing

### Horizontal Scaling
```
Initiale (MVP):       1 instance API + 1 DB
Charge moyenne:       3-5 instances API + 1 DB (master/replica)
Haute charge:         10+ instances API + cluster DB (Postgres HA)
```

### Auto-scaling triggers
- ✅ CPU > 70%
- ✅ Memory > 80%
- ✅ Request queue > 50 items

---

**Document** : ARCHITECTURE.md  
**Version** : 1.0  
**Date** : 20 août 2026  
**Auteur** : Équipe PlantDiag
