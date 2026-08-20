# 🌿 PlantDiag - Plateforme de Diagnostic IA pour Maladies Agricoles

## 📋 Vue d'ensemble

**PlantDiag** est une plateforme de diagnostic intelligente permettant aux agriculteurs d'identifier rapidement les maladies foliaires via une photo et de recevoir des recommandations de traitement personnalisées.

### 🎯 Objectif
Réduire le temps de diagnostic de plusieurs jours à quelques minutes et optimiser le choix de traitement (biologique vs. conventionnel).

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  Mobile App         │
│  (Flutter)          │
│  - Photo capture    │
│  - Historique       │
│  - Parcelles        │
└──────────┬──────────┘
           │ HTTPS
┌──────────▼──────────┐
│  FastAPI Backend    │
│  - /diagnose        │
│  - /history         │
│  - /parcels         │
│  - /sensors         │
│  - Swagger UI       │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  ML Model (TF Lite) │
│  + PostgreSQL DB    │
│  + IoT Simulation   │
└─────────────────────┘

    ☁️ Deployed on Cloud (AWS/Azure/VMware)
        Docker Container
```

---

## 📦 Structure du projet

```
project/
├── backend/                    # API FastAPI + ML
│   ├── app.py                 # Entrée principale
│   ├── requirements.txt        # Dépendances Python
│   ├── models/                # Modèles ML
│   │   ├── disease_classifier.py
│   │   └── plantvillage_utils.py
│   ├── routes/                # Endpoints API
│   │   ├── diagnose.py
│   │   ├── history.py
│   │   ├── parcels.py
│   │   └── sensors.py
│   ├── database/              # ORM + Migrations
│   │   └── models.py
│   └── config.py              # Configuration
│
├── mobile/                     # App Flutter
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/
│   │   │   ├── camera_screen.dart
│   │   │   ├── diagnosis_screen.dart
│   │   │   ├── history_screen.dart
│   │   │   └── parcels_screen.dart
│   │   └── services/
│   │       └── api_service.dart
│   └── pubspec.yaml
│
├── infra/                      # Infrastructure & DevOps
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── terraform/             # IaC pour cloud
│   └── architecture.md
│
├── docs/                       # Documentation
│   ├── API.md                 # Swagger documentation
│   ├── SETUP.md               # Guide d'installation
│   └── architecture.md        # Schéma réseau
│
├── FICHE_PROJET.md            # Spécification complète
├── BACKLOG.md                 # User stories + MoSCoW
├── README.md                  # Ce fichier
└── .gitignore
```

---

## 🚀 Démarrage rapide

### Prérequis
- Python 3.9+
- Flutter 3.x
- Docker & Docker Compose
- Git

### Backend (API FastAPI)

```bash
# 1. Installation
cd backend
python -m venv venv
source venv/bin/activate  # Ou venv\Scripts\activate sur Windows
pip install -r requirements.txt

# 2. Lancer l'API
python -m uvicorn app:app --reload

# 3. Accéder à Swagger
# http://localhost:8000/docs
```

### Mobile (Flutter)

```bash
cd mobile
flutter pub get
flutter run  # Émulateur Android/iOS
```

### Déploiement Docker

```bash
# Build + Run
docker-compose up --build

# API sera accessible sur http://localhost:8000
```

---

## 📊 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/diagnose` | Envoyer photo pour diagnostic |
| GET | `/history/{user_id}` | Récupérer l'historique |
| POST | `/parcels` | Créer une parcelle |
| GET | `/parcels` | Lister les parcelles |
| GET | `/sensors` | Récupérer données IoT simulées |
| GET | `/docs` | Documentation Swagger |

**Exemple : Diagnostic**
```bash
curl -X POST "http://localhost:8000/diagnose" \
  -F "file=@photo.jpg" \
  -F "user_id=123" \
  -F "parcel_id=456"
```

**Réponse**
```json
{
  "diagnosis": "Rouille du blé",
  "confidence": 0.92,
  "treatments": {
    "preventive": "Rotation des cultures",
    "biological": "Pulvérisation de Bacillus subtilis",
    "conventional": "Fongicide à base de triazole"
  },
  "severity": "Modérée",
  "recommendation": "Traiter rapidement - propagation active"
}
```

---

## 🤖 Modèle IA

- **Architecture** : MobileNetV2 (pré-entraîné)
- **Dataset** : PlantVillage (5-7 maladies principales)
- **Maladies supportées** :
  - Rouille du blé
  - Mildiou du raisin
  - Oïdium
  - Septoriose
  - Brûlure bactérienne
  - Rouille brune du riz
  - Feuille blanche du maïs

- **Performance** : Accuracy > 85%, latence < 2s

---

## 🛡️ Sécurité

- ✅ Données utilisateur chiffrées en transit (HTTPS/TLS)
- ✅ Hachage des passwords (bcrypt)
- ✅ Stockage secure des modèles IA
- ✅ Validation des inputs (photo format, taille max 10MB)
- ✅ Rate limiting sur les endpoints
- ✅ Logs sécurisés (PII masqué)

---

## 📱 Fonctionnalités

### v1.0 (MVP)
- ✅ Capture photo et diagnostic instantané
- ✅ Affichage résultat avec taux de certitude
- ✅ Historique par parcelle
- ✅ Simulation capteurs IoT
- ✅ API Swagger complète

### v2.0 (Future)
- 📋 Fine-tuning modèle sur données propriétaires
- 🗺️ Carte interactive des parcelles
- 🔔 Alertes automatiques (conditions critiques)
- 📊 Analytics + rapports PDF
- 🌐 Multi-langues
- 👥 Partage entre agriculteurs

---

## 🔧 Technologie

| Composant | Tech Stack |
|-----------|-----------|
| **Mobile** | Flutter, Dart, camera plugin, http |
| **Backend** | FastAPI, Python 3.9, SQLAlchemy |
| **ML** | TensorFlow Lite, MobileNetV2, OpenCV |
| **Database** | PostgreSQL, Redis (cache) |
| **Infrastructure** | Docker, docker-compose, Cloud (AWS/Azure) |
| **VCS** | Git, GitHub/GitLab |

---

## 📈 Métriques de succès

- ✅ API response time < 2 secondes
- ✅ Diagnostic accuracy > 85%
- ✅ App performance (< 100MB RAM)
- ✅ 100% uptime (SLA 99.9%)
- ✅ Présentation < 15 minutes

---

## 📚 Documentation

- [FICHE_PROJET.md](FICHE_PROJET.md) - Spécification complète
- [BACKLOG.md](BACKLOG.md) - User stories MoSCoW
- [API.md](docs/API.md) - Documentation API détaillée
- [ARCHITECTURE.md](docs/architecture.md) - Schéma réseau & déploiement
- [SETUP.md](docs/SETUP.md) - Guide d'installation détaillé

---

## 👥 Contribution

```bash
# 1. Clone le repo
git clone https://github.com/yourteam/plantdiag.git

# 2. Crée une branche
git checkout -b feature/your-feature

# 3. Commit avec messages clairs
git commit -m "feat: add diagnosis endpoint"

# 4. Push & Pull Request
git push origin feature/your-feature
```

**Conventions**
- Commits : `feat:`, `fix:`, `docs:`, `refactor:`
- Branches : `feature/xxx`, `bugfix/xxx`, `docs/xxx`
- Code style : Black (Python), Dartfmt (Dart)

---

## 📞 Support

Pour des questions : antoine.simon@chambre-agriculture.fr  
Docs technique : Voir `/docs`  
Issues & Bug reports : GitHub Issues

---

**Version** : 1.0  
**Dernière maj** : 20 août 2026  
**Statut** : En développement 🚀
