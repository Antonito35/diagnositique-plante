# FICHE PROJET - Diagnostic de Maladies Agricoles par IA

## 1. PROBLÉMATIQUE

### Contexte
La Chambre d'Agriculture fait face à un enjeu majeur : **les pertes de rendement liées aux maladies foliaires** représentent entre 20-30% des pertes agricoles annuelles. Les agriculteurs manquent d'outils accessibles et rapides pour identifier précisément les maladies et mettre en place un traitement adapté.

### Problème identifié
- ❌ Diagnostic manuel par visite coûteux et lent
- ❌ Délai entre identification et traitement (risque de propagation)
- ❌ Manque de données historiques pour optimiser les traitements futurs
- ❌ Choix entre traitements biologiques/conventionnels sans recommandation précise
- ❌ Pas de suivi de l'état des parcelles en temps réel

---

## 2. OBJECTIFS

### Objectif principal
**Développer une plateforme de diagnostic IA pour maladies agricoles** permettant aux agriculteurs d'identifier rapidement une maladie foliaire et de recevoir des recommandations de traitement personnalisées.

### Objectifs secondaires
1. **Réduire le temps de diagnostic** : de plusieurs jours à quelques minutes
2. **Améliorer la précision** : taux de certitude > 85% pour les diagnostics
3. **Historiser les données** : constituer une base de diagnostics pour chaque parcelle
4. **Monitorer les conditions** : capteurs IoT pour humidité, température
5. **Accessibilité** : application mobile intuitive utilisable en champ

---

## 3. PÉRIMÈTRE

### Inclus (In Scope)
✅ Application mobile iOS/Android (Flutter) pour capture photo  
✅ Modèle IA (MobileNetV2 + PlantVillage dataset) pour 5-7 maladies principales  
✅ API REST FastAPI pour traitement et historique  
✅ Simulation de capteurs IoT (température, humidité du sol/air)  
✅ Tableau de bord avec historique des diagnostics  
✅ Visualisation des parcelles (liste/carte simple)  
✅ Conteneurisation Docker  
✅ Déploiement sur cloud (AWS/Azure/VMware école)  

### Exclus (Out of Scope)
❌ Intégration de capteurs physiques réels  
❌ Système de e-commerce pour produits phytosanitaires  
❌ Intégration avec logiciels de gestion agricole tiers  
❌ Support multi-langues (français uniquement pour MVP)  
❌ Authentification OAuth complexe  

---

## 4. CONTRAINTES

| Contrainte | Description | Impact |
|-----------|-----------|--------|
| **Temps** | 15 semaines (fin novembre 2026) | Prioriser MoSCoW strict |
| **Ressources** | Équipe de ~4 étudiants | Tâches parallélisables nécessaires |
| **Infrastructure** | VM école ou cloud gratuit | Pas de budget commercial |
| **Données** | PlantVillage dataset public | Pas de collection de données propriétaires |
| **Modèle IA** | MobileNetV2 pré-entraîné | Pas de fine-tuning complexe |
| **Déploiement** | One-click deploiement | Infrastructure as Code (Terraform/Docker) |

---

## 5. LIVRABLES FINAUX

### 📱 Livrables techniques
1. **Application mobile** (APK/IPA déployable)
   - Écran de capture photo
   - Affichage diagnostic avec taux de certitude
   - Tableau de bord historique
   - Vue parcelles

2. **Backend API** (Swagger documentation)
   - Endpoint `/diagnose` (POST photo → diagnostic)
   - Endpoint `/history` (GET historique utilisateur)
   - Endpoint `/parcels` (GET/POST parcelles)
   - Endpoint `/sensors` (GET données IoT simulées)

3. **Infrastructure**
   - Image Docker (docker-compose.yml)
   - Configuration déploiement cloud
   - Schéma architecture réseau

4. **Code source**
   - Dépôt GitHub/GitLab avec historique clair
   - README, CONTRIBUTING.md
   - Documentation technique

### 📊 Livrables de suivi
1. **Fiche projet complète** ✓ (ce document)
2. **Tableau Trello/Kanban** avec jalons
3. **Backlog Agile** avec User Stories MoSCoW
4. **Documentation collaborative** (Architecture, API)

### 🎤 Livrables présentation
1. **Diaporama** (10-12 slides)
   - Contexte & Chambre d'Agriculture
   - Problématique & Intérêt économique/écologique
   - Architecture technique
   - Démonstration live (photos)
   - Roadmap future

2. **Démonstration live** (15 min)
   - Photo d'une feuille malade
   - Affichage du diagnostic avec taux
   - Récupération de l'historique
   - Endpoints Swagger

---

## 6. TIMELINE RÉALISTE

```
Semaine 1-2 (Août 20-31)    → Fiche projet + Trello + Git setup
Semaine 3-5 (Sept 1-17)     → API FastAPI + Modèle IA intégré
Semaine 6-8 (Sept 18-Oct 2) → App mobile v1 + IoT simulation
Semaine 9-10 (Oct 3-16)     → Docker + Tests + Bug fixes
Semaine 11-12 (Oct 17-30)   → Déploiement cloud + Schéma réseau
Semaine 13-15 (Oct 31-Nov 13) → Préparation présentation + Démonstration
```

---

## 7. CRITÈRES DE SUCCÈS

- ✅ API déployée et accessible (Swagger functional)
- ✅ App mobile capture photo et envoie à l'API
- ✅ Diagnostic retourné avec taux > 80%
- ✅ Historique persisté et récupérable
- ✅ Docker image buildable et runnable
- ✅ Présentation < 15 min avec démo live réussie
- ✅ Dépôt Git avec >= 50 commits clairs

---

## 8. TECHNOLOGIES CHOISIES

| Couche | Technologie | Justification |
|--------|-------------|---------------|
| **Mobile** | Flutter | Cross-platform, performance, facile à déployer |
| **Backend** | FastAPI (Python) | ML-friendly, async, auto-documentation Swagger |
| **IA** | MobileNetV2 + TensorFlow Lite | Léger, optimisé mobile, PlantVillage compatible |
| **IoT** | Python simulation | Pas besoin hardware réel, focus logic |
| **Container** | Docker + docker-compose | Déploiement reproductible |
| **Cloud** | AWS/Azure/VMware école | Infrastructure disponible, free tier/académique |
| **VCS** | Git (GitHub/GitLab) | Standard industrie, historique transparent |

---

## 9. RISQUES & MITIGATION

| Risque | Probabilité | Impact | Mitigation |
|--------|-----------|--------|-----------|
| Modèle IA peu performant | Moyen | Haut | Tester PlantVillage rapidement, fallback modèle simplifié |
| Problèmes build mobile | Moyen | Moyen | Commencer émulateur Android, Xcode en parallèle |
| Déploiement cloud échoue | Faible | Moyen | Docker local like production, test déploiement semaine 9 |
| Équipe désynchronisée | Moyen | Moyen | Daily standups, Trello mise à jour quotidienne |
| Démo live échoue | Faible | Haut | Préparer vidéo fallback, tester internet école |

---

## 10. RÔLES & RESPONSABILITÉS (Exemple)

```
Antoine (Lead)        → Backlog, architecture, présentation, tests
Développeur 1         → Backend FastAPI + IA
Développeur 2         → App mobile Flutter
Développeur 3         → DevOps (Docker, Cloud, Schéma réseau)
Tous                  → Contribution Git, documentation
```

---

**Document signé le** : 20 août 2026  
**Version** : 1.0  
**Statut** : Approuvé et prêt pour développement
