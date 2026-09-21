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
- Idéal pour IA (TensorFlow, NumPy, écosystème scikit-learn)
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
    # 2. Le modèle IA (TensorFlow Lite) analyse
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
- Déploiement en une seule commande
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
      En ligne ! 🚀
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
| **IA intégrée** | TensorFlow (transfer learning) | ✅ Respecté |
| **Sécurité** | JWT + Bcrypt + CORS | ✅ Respecté |
| **Performance** | ~1.5s/diagnostic | ✅ Respecté |

---

## 🎯 **Décisions Stratégiques**

### Pourquoi PAS Node.js ?
- ❌ IA plus difficile (Python domine, TensorFlow est natif Python)
- ❌ Écosystème IA de Node.js beaucoup plus restreint
- ✅ Mais : autre choix valide si l'équipe a l'expertise

### Pourquoi PAS MongoDB ?
- ❌ Schéma relationnel nécessaire (users → parcels → diagnostics)
- ❌ Transactions ACID plus sûres pour l'agriculture
- ✅ Mais : flexible pour des données météo peu structurées

### Pourquoi PAS Kubernetes ?
- ❌ Disproportionné pour un MVP (1 utilisateur → 100 utilisateurs)
- ❌ Trop complexe pour le niveau Bachelor 2
- ✅ Docker suffit aujourd'hui, migration vers Kubernetes possible plus tard

---

## 📈 **Plan de Scalabilité**

```
Phase 1 (Actuel) : 1 instance EC2
└─ Capacité visée : 100 utilisateurs, 1 000 diagnostics/jour

Phase 2 (Futur) : Auto-scaling
├─ Plusieurs instances EC2
├─ Répartiteur de charge (ELB)
└─ Capacité visée : 1 000 utilisateurs, 10 000 diagnostics/jour

Phase 3 (Production à grande échelle) : Kubernetes
├─ Architecture en micro-services
├─ Pods à mise à l'échelle automatique
└─ Capacité visée : 10 000+ utilisateurs, 100 000+ diagnostics/jour
```

---

## ✅ **Résumé Conformité CDC**

| Exigence CDC | Technologie | Statut |
|------------|-------------|--------|
| Backend/API | **FastAPI** | ✅ |
| Base de Données | **PostgreSQL** | ✅ |
| Infrastructure/Déploiement | **Docker + AWS** | ✅ |
| IA/Données | **TensorFlow (transfer learning MobileNetV2)** | ✅ |
| Architecture Réseau | **Terrain IoT + 4 tiers** | ✅ |
| Cloud Public | **AWS EC2** | ✅ |
| Sécurité | **JWT + Bcrypt** | ✅ |
| Performance | **~1,5 s / requête** | ✅ |

---

**Version** : 2.1  
**Date** : 2026-09-21  
**Approuvé** : Conforme au CDC ✅
