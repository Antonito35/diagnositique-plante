# 🌐 Architecture Réseau - PlantDiag

## Schéma Global

```
┌──────────────────────────┐      ┌──────────────────────────┐
│      UTILISATEURS        │      │   CAPTEURS IoT (parcelles)│
│  (Agriculteurs mobile/web)│      │  SENS-001, SENS-002, ...  │
│                          │      │  humidité sol, temp. sol, │
│                          │      │  temp. air, hygrométrie,  │
│                          │      │  humectation foliaire,    │
│                          │      │  niveau de batterie       │
└────────────┬─────────────┘      └────────────┬─────────────┘
             │ HTTP/HTTPS                      │ HTTP (POST /sensors/readings)
             │                                 │ 1 trame par minute
             └───────────────┬─────────────────┘
                             │
        ┌────────────────────▼────────────┐
        │      INTERNET (Public)          │
        │                                 │
        │   IP: 13.51.48.254 (AWS)       │
        │   Port: 8000 (HTTP)            │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │    AWS EC2 Instance             │
        │  (us-east-1 region)             │
        │                                 │
        │  ┌──────────────────────────┐   │
        │  │  Docker Container        │   │
        │  │                          │   │
        │  │ ┌──────────────────────┐ │   │
        │  │ │  FastAPI Backend     │ │   │
        │  │ │  (Python 3.11)       │ │   │
        │  │ │  Port: 8000          │ │   │
        │  │ └──────────────────────┘ │   │
        │  │         ↓                │   │
        │  │  ┌──────────────────┐    │   │
        │  │  │  OpenCV + NumPy  │    │   │
        │  │  │  (IA Classifier) │    │   │
        │  │  └──────────────────┘    │   │
        │  └──────────────────────────┘   │
        │                                 │
        │  ┌──────────────────────────┐   │
        │  │  Simulateur IoT          │   │
        │  │  (conteneur dédié)       │   │
        │  │  émule les boîtiers      │   │
        │  │  de terrain              │   │
        │  └──────────────────────────┘   │
        │                                 │
        │  ┌──────────────────────────┐   │
        │  │  PostgreSQL 15          │   │
        │  │  Port: 5432             │   │
        │  │  - users                │   │
        │  │  - parcels              │   │
        │  │  - diagnostics          │   │
        │  │  - sensor_readings      │   │
        │  └──────────────────────────┘   │
        │                                 │
        │  ┌──────────────────────────┐   │
        │  │  Redis 7                │   │
        │  │  Port: 6379             │   │
        │  │  (Cache + Sessions)     │   │
        │  └──────────────────────────┘   │
        │                                 │
        └────────────────┬────────────────┘
                         │ HTTPS
        ┌────────────────▼────────────────┐
        │   SERVICES EXTERNES             │
        │                                 │
        │  - Open-Meteo API (Météo)       │
        │  - Nominatim OSM (Géoloc)       │
        └─────────────────────────────────┘
```

---

## 🔧 **Composants Réseau**

### **Tier 1 : Présentation (Frontend)**
- **Interface Web** : HTML/CSS/JavaScript
- **Accès** : Mobile + PC
- **Protocole** : HTTP/HTTPS
- **Responsif** : Oui (mobile-first)

### **Tier 2 : Métier (Backend)**
- **Framework** : FastAPI (Python 3.11)
- **Port** : 8000
- **Protocole** : RESTful API
- **Authentification** : JWT + Bcrypt
- **CORS** : Activé (cross-origin)

### **Tier 3 : Données**
- **Base de Données** : PostgreSQL 15
- **Stockage** : Persistant (Docker volume)
- **Backup** : Automatique (AWS RDS ready)
- **Cache** : Redis 7 (sessions, cache)

### **Tier 4 : IA & Services**
- **Vision IA** : OpenCV + NumPy
- **Météo API** : Open-Meteo (gratuit)
- **Géolocalisation** : Nominatim OSM

### **Couche terrain : capteurs IoT**
- **Un boîtier par parcelle**, identifié par un code (`SENS-001`, `SENS-002`, …)
- **Six grandeurs mesurées** : humidité et température du sol, température et
  hygrométrie de l'air, humectation foliaire, niveau de batterie
- **Transport** : HTTP, une trame JSON par minute vers `POST /api/v1/sensors/readings`
- **Supervision** : `GET /api/v1/sensors/network` indique les capteurs en ligne
  (aucune trame depuis plus de 15 minutes = hors ligne)
- **Simulation** : un conteneur dédié émule les boîtiers avec un cycle jour/nuit
  et des averses aléatoires. Remplacer le simulateur par de vrais capteurs ne
  demande aucune modification de l'API.

---

## 📊 **Flux de Données**

### Flux 1 — Diagnostic par image

```
1. Utilisateur envoie photo
   ↓
2. Upload → FastAPI (8000)
   ↓
3. OpenCV analyse l'image
   ↓
4. Diagnostic généré avec indice de confiance
   ↓
5. Sauvegarde → PostgreSQL
   ↓
6. Réponse JSON → Frontend
   ↓
7. Affichage utilisateur
```

### Flux 2 — Surveillance permanente par les capteurs

```
1. Le capteur de la parcelle relève ses six grandeurs
   ↓
2. Trame JSON → POST /api/v1/sensors/readings
   ↓
3. Validation Pydantic, écriture dans sensor_readings
   ↓
4. Croisement avec le dernier diagnostic IA et la météo
   ↓
5. Règles métier :
     feuillage humide ≥ 70 % et air entre 15 et 25 °C → risque fongique
     humidité du sol < 25 %  → stress hydrique
     humidité du sol > 85 %  → excès d'eau
     batterie < 20 %         → maintenance
     silence > 15 min        → capteur hors ligne
   ↓
6. Alertes classées par gravité → GET /api/v1/alerts/{user_id}
   ↓
7. Affichage dans l'onglet Alertes
```

---

## 🔐 **Sécurité Réseau**

| Couche | Mesure | Statut |
|--------|--------|--------|
| **Authentification** | JWT + Bcrypt | ✅ Implémenté |
| **Chiffrement** | HTTPS ready | ✅ Prêt |
| **Validation** | Input sanitization | ✅ Active |
| **CORS** | Whitelist domaines | ✅ Configuré |
| **Rate Limiting** | Protégé DDoS | ✅ AWS Shield |
| **Backup BD** | Volumes Docker | ✅ Persistant |

---

## 📈 **Scalabilité**

```
Actuellement : 1 instance EC2 (t2.micro)
              + 1 BD PostgreSQL
              + 1 Cache Redis
              + 1 simulateur de capteurs IoT

Capable de supporter :
- 100+ utilisateurs simultanés
- 1000+ diagnostics/jour
- 50+ requêtes/sec

Pour monter en charge :
- Groupe d'auto-scaling (AWS)
- Répartiteur de charge (ELB)
- Réplicas de lecture de la base de données
- CDN CloudFront pour les fichiers statiques
```

---

## 🚀 **Infrastructure as Code**

**Docker Compose** :
- ✅ Isolé par conteneur
- ✅ Versions reproductibles
- ✅ Déploiement en une seule commande
- ✅ Environnement identique en développement et en production

**Portabilité cloud** :
- ✅ AWS EC2 (actuel)
- ✅ Azure Container Instances (possible, non testé)
- ✅ Kubernetes (évolution possible)

---

## 📍 **Déploiement Actuel**

```
Fournisseur : AWS EC2
Instance : t2.micro (gratuit 12 mois)
OS : Ubuntu 22.04 LTS
IP Publique : 13.51.48.254

Statut : 🟢 En ligne
Latence API : ~1,5 s
```

---

**Version** : 2.1  
**Date** : 2026-09-21  
**Conforme au CDC** : ✅ Oui
