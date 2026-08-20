# 📋 BACKLOG PRODUIT - PlantDiag

## Priorisation MoSCoW

Classement des fonctionnalités selon leur importance : **Must have** > **Should have** > **Could have** > **Won't have**

---

## 🔴 MUST HAVE (Fonctionnalités critiques - Sprint 1-3)

### US-001: Capture photo et envoi pour diagnostic
**En tant que** agriculteur  
**Je veux** prendre une photo d'une feuille malade directement depuis l'app  
**Afin de** envoyer rapidement la photo pour diagnostic  

- Critères d'acceptation :
  - ✅ Caméra mobile accessible (iOS/Android)
  - ✅ Affichage de la photo avant envoi
  - ✅ Compression automatique (max 10MB)
  - ✅ Indicateur de chargement lors de l'envoi
- Effort : 5 points
- Sprint : 1

---

### US-002: Affichage diagnostic avec taux de certitude
**En tant que** agriculteur  
**Je veux** voir le diagnostic de la maladie avec un taux de certitude  
**Afin de** comprendre la fiabilité du diagnostic  

- Critères d'acceptation :
  - ✅ Maladie identifiée affichée clairement
  - ✅ Taux de certitude en pourcentage (0-100%)
  - ✅ Icône/couleur pour la sévérité (Mild/Moderate/Severe)
  - ✅ Temps de réponse < 3 secondes
- Effort : 5 points
- Sprint : 2

---

### US-003: Recommandations de traitement (3 types)
**En tant que** agriculteur  
**Je veux** recevoir 3 options de traitement (préventif, biologique, conventionnel)  
**Afin de** choisir la meilleure approche adaptée à ma ferme  

- Critères d'acceptation :
  - ✅ Traitement préventif (rotation cultures, hygiène)
  - ✅ Traitement biologique (biopesticides, champignons bénéfiques)
  - ✅ Traitement conventionnel (fongicides chimiques)
  - ✅ Description succincte pour chaque option
  - ✅ Estimé d'efficacité (80-100%)
- Effort : 8 points
- Sprint : 2-3

---

### US-004: API endpoint /diagnose
**En tant que** développeur mobile  
**Je veux** un endpoint POST /diagnose qui accepte une photo  
**Afin de** intégrer le diagnostic dans l'app  

- Critères d'acceptation :
  - ✅ Route POST `/diagnose`
  - ✅ Accepte multipart/form-data (photo)
  - ✅ Retourne JSON avec diagnosis, confidence, treatments
  - ✅ Gestion des erreurs (photo invalide, format incorrect)
  - ✅ Logging des requêtes
- Effort : 8 points
- Sprint : 1-2

---

### US-005: Modèle IA intégré (MobileNetV2)
**En tant que** système  
**Je veux** charger un modèle MobileNetV2 pré-entraîné  
**Afin de** prédire la maladie avec latence minimale  

- Critères d'acceptation :
  - ✅ Modèle PlantVillage chargé et fonctionnel
  - ✅ Prédiction < 2 secondes
  - ✅ Accuracy > 85%
  - ✅ Support 5-7 maladies principales
  - ✅ Cache modèle en mémoire
- Effort : 13 points
- Sprint : 1-2

---

### US-006: Historique des diagnostics
**En tant que** agriculteur  
**Je veux** voir l'historique de tous mes diagnostics précédents  
**Afin de** tracker l'évolution des maladies sur mes parcelles  

- Critères d'acceptation :
  - ✅ Liste des diagnostics précédents
  - ✅ Filtre par parcelle
  - ✅ Affichage photo originale + diagnostic + date
  - ✅ Option d'export PDF
- Effort : 8 points
- Sprint : 3

---

### US-007: Gestion des parcelles
**En tant que** agriculteur  
**Je veux** créer et lister mes parcelles  
**Afin de** associer les diagnostics à des parcelles spécifiques  

- Critères d'acceptation :
  - ✅ Création parcelle (nom, surface, culture)
  - ✅ Affichage liste parcelles
  - ✅ Endpoint API GET/POST `/parcels`
  - ✅ Persistance en base de données
- Effort : 5 points
- Sprint : 2

---

### US-008: Docker & Déploiement
**En tant que** DevOps  
**Je veux** une image Docker reproductible  
**Afin de** déployer facilement sur n'importe quel serveur  

- Critères d'acceptation :
  - ✅ Dockerfile avec Python 3.9+
  - ✅ docker-compose.yml avec tous les services
  - ✅ Build sans erreurs
  - ✅ Startup < 30 secondes
  - ✅ Health checks configurés
- Effort : 8 points
- Sprint : 3

---

### US-009: Documentation API Swagger
**En tant que** présentateur  
**Je veux** une documentation automatique Swagger  
**Afin de** montrer les endpoints lors de la présentation  

- Critères d'acceptation :
  - ✅ Swagger UI accessible `/docs`
  - ✅ Tous les endpoints documentés
  - ✅ Exemples de requêtes/réponses
  - ✅ Schémas JSON complets
- Effort : 3 points
- Sprint : 3

---

## 🟡 SHOULD HAVE (Importants - Sprint 3-4)

### US-010: Simulation capteurs IoT
**En tant que** agriculteur  
**Je veux** voir les conditions actuelles (température, humidité)  
**Afin de** correler la maladie avec les conditions météo  

- Critères d'acceptation :
  - ✅ Endpoint `/sensors` qui retourne température & humidité
  - ✅ Données simulées réalistes (varie dans le temps)
  - ✅ Affichage dans le dashboard mobile
  - ✅ Alertes si conditions critiques (ex: T > 30°C + humidité > 80%)
- Effort : 8 points
- Sprint : 3

---

### US-011: Dashboard mobile récapitulatif
**En tant que** agriculteur  
**Je veux** voir un dashboard avec résumé de mes parcelles  
**Afin de** avoir une vue globale de l'état de ma ferme  

- Critères d'acceptation :
  - ✅ Nombre total de diagnostics
  - ✅ Maladie la plus fréquente
  - ✅ État des parcelles (Sain/Alerte/Critique)
  - ✅ Graphique tendance (derniers 30 jours)
- Effort : 8 points
- Sprint : 4

---

### US-012: Schéma d'architecture réseau
**En tant que** présentateur  
**Je veux** un schéma montrant flux utilisateur → API → serveurs  
**Afin de** expliquer l'architecture lors de la présentation  

- Critères d'acceptation :
  - ✅ Diagramme clair (mobile, API, DB, cloud)
  - ✅ Flèches montrant flux HTTPS
  - ✅ Types de données visualisés
  - ✅ Format PNG/PDF haute résolution
- Effort : 5 points
- Sprint : 4

---

### US-013: Tests automatisés (Backend)
**En tant que** développeur  
**Je veux** des tests unitaires pour l'API  
**Afin de** assurer la stabilité du code  

- Critères d'acceptation :
  - ✅ Tests pour endpoints principaux
  - ✅ Couverture > 70%
  - ✅ Tests ML model (prédictions correctes)
  - ✅ Exécution en < 30 secondes
- Effort : 8 points
- Sprint : 4

---

### US-014: Déploiement sur cloud
**En tant que** DevOps  
**Je veux** déployer l'application sur AWS/Azure/VMware  
**Afin de** la rendre accessible publiquement  

- Critères d'acceptation :
  - ✅ Instance cloud provisionnée
  - ✅ API accessible via URL publique
  - ✅ Domain name configuré (DNS)
  - ✅ SSL/TLS activé (HTTPS)
  - ✅ Monitoring & Logs centralisés
- Effort : 13 points
- Sprint : 4

---

## 🟢 COULD HAVE (Améliorations - Post-MVP)

### US-015: Fine-tuning modèle IA
**En tant que** data scientist  
**Je veux** fine-tuner le modèle sur des données propriétaires  
**Afin de** améliorer la précision pour nos cultures locales  

- Effort : 21 points
- Sprint : Backlog futur

---

### US-016: Carte interactive des parcelles
**En tant que** agriculteur  
**Je veux** voir mes parcelles sur une carte  
**Afin de** visualiser leur localisation géographique  

- Effort : 13 points
- Sprint : Backlog futur

---

### US-017: Export rapports PDF
**En tant que** agriculteur  
**Je veux** exporter les diagnostics en PDF  
**Afin de** les conserver pour documentation/assurance  

- Effort : 5 points
- Sprint : Backlog futur

---

### US-018: Alerts & Notifications
**En tant que** agriculteur  
**Je veux** recevoir des notifications push si conditions critiques  
**Afin de** réagir rapidement aux problèmes  

- Effort : 8 points
- Sprint : Backlog futur

---

## ⚪ WON'T HAVE (Hors scope)

### US-019: Intégration capteurs physiques
**Raison** : Pas de hardware disponible pour l'MVP  
**Future** : Ajouter après déploiement initial

---

### US-020: Système d'e-commerce
**Raison** : Hors du scope fonctionnel  
**Future** : Partenariat externe possible

---

### US-021: Multi-langues
**Raison** : MVP français uniquement  
**Future** : Ajouter après succès initial

---

### US-022: Authentification OAuth (Google/Facebook)
**Raison** : Email/Password suffisant pour MVP  
**Future** : Ajouter pour production

---

## 📊 Récapitulatif des efforts

| Catégorie | Nombre d'US | Points totaux | Sprints estimés |
|-----------|------------|---------------|-----------------|
| **MUST HAVE** | 9 | 63 points | Sprint 1-3 (8-9 sem) |
| **SHOULD HAVE** | 5 | 47 points | Sprint 3-4 (2-3 sem) |
| **COULD HAVE** | 4 | 47 points | Futur |
| **WON'T HAVE** | 4 | N/A | N/A |
| **TOTAL MVP** | 14 | 110 points | 10-12 semaines |

---

## 🎯 Priorités d'exécution

```
Sprint 1 (Sem 1-2)
  └─ US-001: Caméra
  └─ US-004: API /diagnose
  └─ US-005: Modèle IA

Sprint 2 (Sem 3-4)
  └─ US-002: Affichage diagnostic
  └─ US-003: Recommandations
  └─ US-007: Gestion parcelles

Sprint 3 (Sem 5-6)
  └─ US-006: Historique
  └─ US-008: Docker
  └─ US-009: Swagger
  └─ US-010: Capteurs IoT

Sprint 4 (Sem 7-8)
  └─ US-011: Dashboard
  └─ US-012: Schéma architecture
  └─ US-013: Tests
  └─ US-014: Déploiement cloud

Buffer & Présentation (Sem 9-10)
  └─ Corrections bugs
  └─ Optimisations
  └─ Diapositives
  └─ Rehearsal présentation
```

---

## 📝 Template User Story (à copier)

```markdown
### US-XXX: [Titre court]
**En tant que** [rôle]  
**Je veux** [action]  
**Afin de** [bénéfice]  

- Critères d'acceptation :
  - ✅ [Critère 1]
  - ✅ [Critère 2]
  - ✅ [Critère 3]
- Effort : [points] points
- Sprint : [num]
```

---

**Dernière révision** : 20 août 2026  
**Statut** : Prêt pour développement
