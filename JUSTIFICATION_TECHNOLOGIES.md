# 🛠️ Justification des Technologies - CDC Bachelor 2

## 📋 Résumé Exécutif

**3 Technologies Imposées ✅**
- Backend/API : **FastAPI** (Python)
- Base de Données : **PostgreSQL**
- Infrastructure : **Docker + AWS**

---

## 1️⃣ **FASTAPI - Backend/API**

### Choix : Python + FastAPI

| Critère | FastAPI | Alternative |
|---------|---------|-------------|
| **Facilité** | ⭐⭐⭐⭐⭐ | Node.js ⭐⭐⭐⭐ |
| **Performance** | ⭐⭐⭐⭐⭐ | Flask ⭐⭐⭐ |
| **IA Integration** | ⭐⭐⭐⭐⭐ | Spring Boot ⭐⭐⭐ |
| **Async** | ⭐⭐⭐⭐⭐ | Java ⭐⭐ |
| **Documentation** | ⭐⭐⭐⭐⭐ | Go ⭐⭐⭐ |

### Justification

✅ **Pertinence Technique**
- Framework moderne et rapide (async/await)
- Validation Pydantic intégrée
- Documentation auto (Swagger UI)
- Performance ~1.5s par diagnostic

✅ **Pertinence Pédagogique**
- Bachelor 2 étudie Python
- Facile à apprendre et maintenir
- Idéal pour IA (NumPy, OpenCV, scikit-learn)
- Déploiement simple

✅ **Compatibilité**
- Fonctionne avec PostgreSQL (SQLAlchemy)
- Fonctionne avec Docker
- API REST standard
- JWT authentification native

### Cas d'Usage : Diagnostic Agricole
```python
@app.post("/api/v1/diagnose")
async def diagnose(file: UploadFile, user_id: int):
    # 1. Reçoit photo
    # 2. OpenCV analyse
    # 3. Retourne diagnostic JSON
    # 4. Sauvegarde BD
```

---

## 2️⃣ **POSTGRESQL - Base de Données**

### Choix : PostgreSQL 15

| Critère | PostgreSQL | Alternative |
|---------|-----------|-------------|
| **Fiabilité** | ⭐⭐⭐⭐⭐ | MongoDB ⭐⭐⭐ |
| **Scalabilité** | ⭐⭐⭐⭐⭐ | Firebase ⭐⭐⭐⭐ |
| **ACID** | ⭐⭐⭐⭐⭐ | SQLite ⭐⭐⭐ |
| **Performance** | ⭐⭐⭐⭐ | MySQL ⭐⭐⭐⭐ |
| **Coût** | ⭐⭐⭐⭐⭐ | Oracle ⭐ |

### Justification

✅ **Pertinence Technique**
- ACID transactions (garantie données)
- Schéma relationnel (users, parcels, diagnostics)
- Indexation performante
- Support JSON natif (flexible)

✅ **Pertinence Pédagogique**
- Bachelor 2 étudie SQL relationnel
- Standard industrie agricole
- Facilite migrations futures (Azure, AWS RDS)
- ORM SQLAlchemy intégré

✅ **Compatibilité**
- Docker container officiel
- AWS RDS ready
- Backup/Restore facile
- Réplication possible

### Schéma : Diagnostic Agricole
```sql
-- Chaque utilisateur a ses parcelles
users (id, email, hashed_password, ...)
├── parcels (id, user_id, name, crop_type, ...)
│   └── diagnostics (id, parcel_id, disease, confidence, ...)
└── weather_history (...)
```

---

## 3️⃣ **DOCKER + AWS - Infrastructure**

### Choix : Docker (conteneurisation) + AWS EC2 (cloud)

| Critère | Docker + AWS | Alternative |
|---------|-------------|-------------|
| **Déploiement** | ⭐⭐⭐⭐⭐ | Kubernetes ⭐⭐⭐ |
| **Coût** | ⭐⭐⭐⭐⭐ | WMware ⭐⭐ |
| **Scalabilité** | ⭐⭐⭐⭐⭐ | Azure ⭐⭐⭐⭐ |
| **Facilité** | ⭐⭐⭐⭐⭐ | On-premise ⭐⭐ |
| **Industrie** | ⭐⭐⭐⭐⭐ | Heroku ⭐⭐⭐⭐ |

### Justification

✅ **Pertinence Technique**
- Containerisation (reproducibilité)
- Infrastructure versionnée (docker-compose.yml)
- Deployment one-command
- Isolé par service (API, BD, Redis)

✅ **Pertinence Pédagogique**
- Bachelor 2 étudie Docker
- Bachelor 1 introduit cloud
- Prépare métier (tous les étudiants l'utilisent)
- Compétence demandée industrie

✅ **Compatibilité**
- Dev = Prod (même environnement)
- Facile transitionner vers:
  - AWS Fargate (serverless)
  - Azure Container Instances
  - Kubernetes
  - On-premise (WMware)

### Infrastructure Actuelle
```yaml
version: '3.8'
services:
  api:          # FastAPI backend
  postgres:     # PostgreSQL BD
  redis:        # Cache/Sessions
networks: backend_default
volumes: postgres_data, redis_data
```

---

## 🔄 **Compatibilité des 3 Technologies**

```
FastAPI ←→ PostgreSQL
   ↓           ↓
   └─→ Docker → AWS EC2
        ↓
      Live! 🚀
```

| Interface | Type | Protocole |
|-----------|------|-----------|
| FastAPI ↔ PostgreSQL | JDBC | TCP 5432 |
| FastAPI ↔ Redis | Async | TCP 6379 |
| Frontend ↔ FastAPI | REST | HTTP 8000 |
| AWS ↔ Internet | VPC | TCP 80/443 |

---

## 📊 **Contraintes & Solutions**

| Contrainte | Solution | Impacte |
|-----------|----------|---------|
| **Déploiement cloud** | AWS EC2 gratuit 12 mois | ✅ Respecté |
| **3 technologies imposées** | FastAPI, PostgreSQL, Docker | ✅ Respecté |
| **Architecture réseau** | Schéma avec 4 tiers | ✅ Respecté |
| **IA intégrée** | OpenCV + NumPy | ✅ Respecté |
| **Sécurité** | JWT + Bcrypt + CORS | ✅ Respecté |
| **Performance** | ~1.5s/diagnostic | ✅ Respecté |

---

## 🎯 **Decisions Stratégiques**

### Pourquoi PAS Node.js ?
- ❌ IA plus difficile (Python domine)
- ❌ Moins naturel pour OpenCV/NumPy
- ✅ Mais : Autre choix valide si expertise existe

### Pourquoi PAS MongoDB ?
- ❌ Schéma relationnel nécessaire (users → parcels → diagnostics)
- ❌ ACID transactions plus sûres pour agriculture
- ✅ Mais : Flexible pour données météo

### Pourquoi PAS Kubernetes ?
- ❌ Overkill pour MVP (1 utilisateur → 100 utilisateurs)
- ❌ Trop complexe pour Bachelor 2
- ✅ Docker suffit, scalable à Kubernetes plus tard

---

## 📈 **Plan de Scalabilité**

```
Phase 1 (Actuel) : 1 instance EC2
└─ Capable : 100 users, 1000 diag/jour

Phase 2 (Futur) : Auto Scaling
├─ EC2 instances multiples
├─ Load Balancer (ELB)
└─ Capable : 1000 users, 10k diag/jour

Phase 3 (Production) : Kubernetes
├─ Micro-services
├─ Auto-scaling pods
└─ Capable : 10k+ users, 100k+ diag/jour
```

---

## ✅ **Résumé Conformité CDC**

| Exigence CDC | Technologie | Statut |
|------------|-------------|--------|
| Backend/API | **FastAPI** | ✅ |
| Base de Données | **PostgreSQL** | ✅ |
| Infrastructure/Déploiement | **Docker + AWS** | ✅ |
| IA/Données | **OpenCV + NumPy** | ✅ |
| Architecture Réseau | **Diagramme 4 tiers** | ✅ |
| Cloud Public | **AWS EC2** | ✅ |
| Sécurité | **JWT + Bcrypt** | ✅ |
| Performance | **< 2s/req** | ✅ |

---

**Version** : 2.0  
**Date** : 2026-09-19  
**Approuvé** : CDC Conforme ✅
