# PlantDiag - Diagnostic Agricole par Intelligence Artificielle

**Solution de diagnostic des maladies des cultures à partir d'une photo, avec surveillance continue par capteurs de parcelle.**

[![Statut](https://img.shields.io/badge/statut-production-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-blue)]()
[![Licence](https://img.shields.io/badge/licence-MIT-green)]()

---

## Le problème

Les agriculteurs mettent souvent plusieurs jours à identifier une maladie sur leurs cultures, faute d'outil accessible. PlantDiag répond à ce besoin avec un diagnostic en moins de deux secondes à partir d'une simple photo.

## La solution

Une application web responsive qui combine intelligence artificielle et capteurs de terrain pour :
- Analyser une photo de plante et identifier la maladie
- Surveiller en continu l'humidité du sol, la température et l'humectation du feuillage
- Croiser ces relevés avec la météo locale pour générer des alertes régionales
- Conserver l'historique des diagnostics par parcelle

---

## Démarrage rapide

### 1. Installation

```bash
cd backend
pip install -r requirements.txt
```

### 2. Lancer l'application (avec Docker, recommandé)

```bash
docker compose up --build
```

Cette commande démarre quatre conteneurs : l'API, PostgreSQL, Redis et le simulateur de capteurs IoT.

### 3. Accéder à l'application

- **Interface web** : http://localhost:8000
- **Documentation API interactive** : http://localhost:8000/docs

### 4. Utilisation

1. Créer une parcelle (nom et type de culture)
2. Prendre ou importer une photo de la plante
3. Consulter le diagnostic, les traitements recommandés et les alertes de la parcelle

---

## Fonctionnalités

| Fonction | Détail |
|----------|--------|
| **Diagnostic par photo** | Upload d'image → analyse IA → résultat en moins de 2 secondes |
| **Capteurs IoT** | Un boîtier par parcelle, six mesures relevées chaque minute |
| **Gestion des parcelles** | Créer, modifier, supprimer, tout persiste en base de données |
| **Alertes croisées** | Combine capteurs, diagnostics IA et météo, classées par gravité |
| **Météo en temps réel** | Conditions actuelles et prévisions à cinq jours |
| **Historique complet** | Tous les diagnostics conservés avec leur indice de confiance |
| **Authentification** | Comptes utilisateurs sécurisés par jeton JWT |
| **API REST** | 18 endpoints documentés via Swagger |

---

## Architecture

```
Capteurs IoT (parcelles)          Utilisateurs (mobile / web)
        │                                   │
        └──────────────┬────────────────────┘
                        ▼
              API FastAPI (Python)
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   PostgreSQL         Redis      Modèle IA (TFLite) + Open-Meteo
  (données)          (cache)          (diagnostic + météo)
```

Détail complet du schéma réseau : [ARCHITECTURE_RESEAU.md](ARCHITECTURE_RESEAU.md)

---

## Stack technique

| Couche | Technologie |
|--------|-------------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Python 3.11, FastAPI |
| **Base de données** | PostgreSQL 15, Redis 7 |
| **Intelligence artificielle** | TensorFlow (transfer learning MobileNetV2), TensorFlow Lite |
| **Météo** | API Open-Meteo |
| **Capteurs IoT** | Service Python dédié, protocole HTTP |
| **Infrastructure** | Docker, Docker Compose, AWS EC2 |

Justification détaillée des choix technologiques : [JUSTIFICATION_TECHNOLOGIES.md](JUSTIFICATION_TECHNOLOGIES.md)

---

## Principaux endpoints de l'API

```bash
# Authentification
POST /api/v1/auth/register
POST /api/v1/auth/login

# Diagnostic
POST /api/v1/diagnose
  Corps : file (image), paramètres user_id, parcel_id
  Réponse : maladie, indice de confiance, traitements recommandés

# Parcelles
GET    /api/v1/parcels
POST   /api/v1/parcels
PUT    /api/v1/parcels/{id}
DELETE /api/v1/parcels/{id}

# Capteurs IoT
POST /api/v1/sensors/readings
GET  /api/v1/sensors/latest
GET  /api/v1/sensors/network

# Alertes et météo
GET /api/v1/alerts/{user_id}
GET /api/v1/weather?latitude=X&longitude=Y
```

Liste complète et testable : http://localhost:8000/docs

**Exemple avec curl :**
```bash
curl -X POST "http://localhost:8000/api/v1/diagnose" \
  -F "file=@photo.jpg"
```

---

## Maladies détectées

Modèle entraîné par transfer learning (MobileNetV2, poids ImageNet gelés)
sur PlantVillage : 54 305 photos réelles labellisées, **38 classes** couvrant
**14 cultures** (pommier, myrtillier, cerisier, maïs, vigne, agrumes, pêcher,
poivron, pomme de terre, framboisier, soja, courge, fraisier, tomate).
Précision mesurée sur le jeu de test PlantVillage (10 849 images jamais vues
à l'entraînement, séparées avant tout entraînement) : **96,70 %**.

Liste complète des 38 classes : [backend/diseases_data.py](backend/diseases_data.py)

⚠️ Le blé et le colza ne font pas partie de PlantVillage : aucune source de
données fiable et librement accessible n'a été trouvée pour ces cultures
dans le temps imparti. C'est une limite connue, pas un oubli.

---

## Sécurité

- Authentification par jeton JWT (validité 30 jours)
- Mots de passe hachés avec Bcrypt et sel
- Validation systématique des données entrantes (Pydantic)
- CORS configuré
- Isolation des données par utilisateur

---

## Déploiement

### Local
```bash
python -m uvicorn app_minimal:app --reload
```

### Docker
```bash
docker compose up --build
```

### Cloud (AWS)
Instance EC2 avec Docker installé, puis `docker compose up -d`.
Procédure complète : [GUIDE_DEPLOIEMENT.md](GUIDE_DEPLOIEMENT.md)

---

## Documentation du projet

| Document | Contenu |
|----------|---------|
| [ARCHITECTURE_RESEAU.md](ARCHITECTURE_RESEAU.md) | Schéma réseau détaillé, couche IoT, flux de données |
| [JUSTIFICATION_TECHNOLOGIES.md](JUSTIFICATION_TECHNOLOGIES.md) | Choix et justification des 3 technologies imposées |
| [GUIDE_DEPLOIEMENT.md](GUIDE_DEPLOIEMENT.md) | Procédure de déploiement complète |
| [RESUME_FINAL.md](RESUME_FINAL.md) | Conformité au cahier des charges |
| [CHECKLIST_FINAL.md](CHECKLIST_FINAL.md) | Checklist avant soutenance |
| [SOUTENANCE_SCRIPT.md](SOUTENANCE_SCRIPT.md) | Script de présentation orale |
| API Swagger | http://localhost:8000/docs |

---

## Pédagogie

Ce projet couvre les cinq domaines techniques du Bachelor 2 :

- **Intelligence artificielle** : transfer learning (TensorFlow/MobileNetV2), 96,70 % de précision mesurée
- **Backend** : API REST asynchrone (FastAPI)
- **Frontend** : interface web responsive
- **Base de données** : modèle relationnel, ORM, migrations
- **Réseau, IoT et DevOps** : capteurs de parcelle, conteneurs Docker, déploiement cloud

---

## Auteur

**Antoine SIMON**
Bachelor 2 Informatique — Sup de Vinci
Projet réalisé pour la Chambre d'Agriculture

---

## Licence

MIT © 2026 PlantDiag
