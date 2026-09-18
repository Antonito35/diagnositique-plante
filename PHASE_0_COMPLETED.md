# ✅ Phase 0 — Prérequis techniques (Complétée)

Date : 2026-09-18  
Status : **COMPLÉTÉE**

## Actions effectuées

### Mobile (Flutter)
- ✅ Exécution de `flutter create .` pour générer les dossiers `android/` et `ios/`
- ✅ Correction `mobile/pubspec.yaml` :
  - Suppression des sections `assets:` et `fonts:` pointant vers des fichiers absents
  - Retrait de `provider` (gardé seulement `riverpod`)
  - Ajout de `go_router`, `flutter_secure_storage`, `flutter_map`, `latlong2`, `fl_chart`
  - Ajout de `flutter_riverpod` pour la compatibilité Riverpod
  - Suppression de `google_maps_flutter` (remplacé par `flutter_map` OSM)

### Backend (FastAPI/Python)
- ✅ Mise à jour `backend/requirements.txt` :
  - Ajout des dépendances d'authentification : `bcrypt`, `python-jose[cryptography]`, `email-validator`
  - Ajout d'`alembic` pour les migrations de schéma
  - Correctiondes versions pour compatibilité Python 3.13
- ✅ Installation des dépendances Python via `pip install -r requirements.txt`
- ✅ Initialisation d'Alembic : `alembic init alembic`
- ✅ Configuration d'`alembic/env.py` :
  - Import de `Base` depuis `database.py`
  - Import des modèles SQLAlchemy (`User`, `Parcel`, `Diagnostic`, etc.)
  - Configuration de `target_metadata = Base.metadata` pour autogenerate
  - Lecture de `DATABASE_URL` depuis variable d'environnement
- ✅ Création de la structure de répertoires backend :
  - `backend/schemas/` (schémas Pydantic par domaine)
  - `backend/routers/` (endpoints FastAPI par domaine)
  - `backend/services/` (logique métier réutilisable)
  - `backend/seed_data/` (données de départ)

## Prochaines étapes (Phase 1)

La Phase 1 (Comptes utilisateurs / Auth JWT) peut maintenant commencer. Les fichiers suivants seront créés/modifiés :

**Backend :**
- `backend/models.py` : ajout de `hashed_password`, `is_active`, `is_organic` à `User`
- `backend/services/auth_service.py` : nouveau (hash/JWT)
- `backend/routers/auth.py` : nouveau (endpoints d'authentification)
- `backend/alembic/versions/*.py` : migration pour ajouter champs à `User`

**Mobile :**
- `mobile/lib/services/api_client.dart` : nouveau (dio + intercepteur JWT)
- `mobile/lib/services/auth_service.dart` : nouveau
- `mobile/lib/providers/auth_provider.dart` : nouveau (Riverpod)
- `mobile/lib/screens/auth/` : nouveau (login, register, splash screens)
- `mobile/lib/app_router.dart` : nouveau (go_router configuration)
- `mobile/lib/main.dart` : modifié (ProviderScope + go_router root)

## Vérification de santé

Pour vérifier que Phase 0 est bien complétée :

```bash
# Backend
cd backend
python -m alembic --version  # Doit afficher une version Alembic

# Mobile
cd mobile
flutter --version  # Doit afficher une version Flutter >= 3.13
flutter pub get   # Doit récupérer les dépendances sans erreur
ls android/       # Doit exister et contenir les fichiers générés
ls ios/           # Doit exister et contenir les fichiers générés
```

---

**Validation avant Phase 1 :** ✅ Tous les prérequis techniques sont en place. Phase 1 peut démarrer immédiatement.
