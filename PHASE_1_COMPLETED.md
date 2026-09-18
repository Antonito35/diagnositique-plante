# ✅ Phase 1 — Comptes utilisateurs / Authentification JWT (Complétée)

Date : 2026-09-18  
Status : **COMPLÉTÉE**

## Résumé

Phase 1 implémente un système complet d'authentification JWT stateless avec gestion sécurisée des mots de passe via bcrypt, et une interface mobile intuitive pour l'inscription et la connexion.

## Backend (FastAPI/Python)

### Modifications
- ✅ **`models.py`** : Extension de la table `User`
  - Ajout `hashed_password` (String, NOT NULL)
  - Ajout `is_active` (Boolean, défaut True)
  - Ajout `is_organic` (Boolean, défaut False) — utilisé Phase 5
  - `email` rendu NOT NULL au niveau applicatif (Pydantic)
  - Import de `Boolean` depuis SQLAlchemy

- ✅ **`services/auth_service.py`** (nouveau) — Logique d'authentification
  - `hash_password()` : Hachage bcrypt des mots de passe
  - `verify_password()` : Vérification contre le hash
  - `create_access_token()` : Génération JWT HS256 (expiration 7 jours)
  - `decode_access_token()` : Décodage et validation du JWT

- ✅ **`schemas/auth.py`** (nouveau) — Schémas Pydantic pour validation
  - `UserRegisterRequest`, `UserLoginRequest`
  - `UserOut`, `AuthTokenResponse`
  - `UserUpdate` pour modifications de profil

- ✅ **`routers/auth.py`** (nouveau) — Endpoints API
  - `POST /api/v1/auth/register` → auto-login après inscription
  - `POST /api/v1/auth/login` → retour du token JWT
  - `GET /api/v1/auth/me` → profil utilisateur (protégé JWT)
  - `PUT /api/v1/auth/me` → mise à jour profil (protégé JWT)
  - Dépendance `get_current_user()` pour protéger les routes

- ✅ **Alembic** — Migrations de schéma
  - Création de `alembic/` avec configuration SQLite/Postgres
  - Migration initiale : `830e7523b7b1` ajoutant les colonnes à `User`
  - Configuration `alembic.ini` et `alembic/env.py` pour lire `DATABASE_URL` depuis l'env

- ✅ **`app_minimal.py`** — Intégration
  - Import du routeur `auth`
  - `app.include_router(auth.router, ...)` pour enregistrer les endpoints

### Configuration attendue (`.env`)
```
SECRET_KEY=your-secret-key-change-in-production  # À changer en prod
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 jours
DATABASE_URL=sqlite:///./plantdiag.db  # ou postgresql://...
```

### Vérification backend (Swagger)
```
1. POST /api/v1/auth/register
   Payload: {"email": "test@test.com", "password": "pass1234", "name": "Test User"}
   Response: {"access_token": "eyJ...", "token_type": "bearer", "user": {...}}

2. POST /api/v1/auth/login
   Payload: {"email": "test@test.com", "password": "pass1234"}
   Response: {"access_token": "...", "token_type": "bearer", "user": {...}}

3. GET /api/v1/auth/me
   Headers: Authorization: Bearer <token>
   Response: {"id": 1, "email": "test@test.com", "name": "Test User", ...}

4. PUT /api/v1/auth/me
   Headers: Authorization: Bearer <token>
   Payload: {"name": "Nouveau Nom", "is_organic": true}
```

## Mobile (Flutter/Dart)

### Nouvelles dépendances (pubspec.yaml)
- ✅ `go_router: ^12.0.0` — Navigation avec routes nommées et redirection d'état
- ✅ `flutter_secure_storage: ^9.0.0` — Stockage sécurisé du JWT
- ✅ `flutter_riverpod: ^2.4.0` — State management (activation Riverpod)
- ✅ Suppression de `provider` (non utilisé)

### Services
- ✅ **`lib/services/api_client.dart`** (nouveau)
  - Instance Dio singleton avec intercepteur JWT
  - `InterceptorsWrapper` pour injecter token en Authorization header
  - Gestion 401 (suppression du token, redirection possible)
  - `setToken()`, `removeToken()`, `getToken()` pour gestion sécurisée

- ✅ **`lib/services/auth_service.dart`** (nouveau)
  - `register()`, `login()`, `logout()`, `getMe()`, `updateProfile()`
  - Retours fortement typés (`AuthResponse`, `User`)
  - Gestion d'erreurs avec messages lisibles
  - Classes `AuthResponse` et `User` pour sérialisation JSON

### Riverpod Providers
- ✅ **`lib/providers/auth_provider.dart`** (nouveau)
  - `currentUserProvider` : `StateNotifier<User?>` — l'état utilisateur courant
  - `CurrentUserNotifier` : logique d'état (register, login, logout, etc.)
  - `isAuthenticatedProvider` : Provider booléen pour vérifier l'authentification
  - `checkToken()` : vérification du token stocké au démarrage

### Écrans d'authentification
- ✅ **`lib/screens/auth/splash_screen.dart`** (nouveau)
  - Affichage au démarrage
  - Appel `checkToken()` pour vérifier l'authentification existante
  - Redirection automatique via go_router selon l'état

- ✅ **`lib/screens/auth/login_screen.dart`** (nouveau)
  - Formulaire email + mot de passe
  - Intégration `currentUserProvider.notifier.login()`
  - Gestion d'état loading et erreurs
  - Lien vers l'inscription

- ✅ **`lib/screens/auth/register_screen.dart`** (nouveau)
  - Formulaire nom complet + email + mot de passe + confirmation
  - Validation client : confirmation mot de passe, longueur minimum
  - Intégration `currentUserProvider.notifier.register()`
  - Auto-login après inscription

### Navigation & Routing
- ✅ **`lib/app_router.dart`** (nouveau)
  - `goRouterProvider` : instance go_router unique
  - `redirect` global basé sur l'état d'authentification (`currentUserProvider`)
  - Routes : `/` (splash), `/login`, `/register`, `/home`
  - `HomeScreen` (placeholder pour Phase 8)

### Main entry point
- ✅ **`lib/main.dart`** (remplacé)
  - `ProviderScope` wrappant toute l'app (Riverpod)
  - `MaterialApp.router` avec go_router configuration
  - Thème Material 3 avec seed vert 0xFF2D6A4F
  - Texte Poppins via Google Fonts
  - Support light/dark theme système

### Vérification mobile (émulateur Flutter)
```
1. Lancer : flutter pub get && flutter run
2. Splash screen → vérification token existant → redirection /login
3. /login : formulaire d'accès
   - Cliquer "S'inscrire" → /register
   - Remplir inscription → appel API register → redirection /home
4. /home : connexion réussie
5. Tuer l'app, relancer : devrait rester connecté (token persistent)
6. Cliquer "Déconnexion" : suppression token, redirection /login
```

## Flux utilisateur complet

```
Nouvel utilisateur :
  App démarre → Splash vérified pas de token → Redirection /login
  → "S'inscrire" → /register form → POST /auth/register → Token sauvegardé
  → Redirection /home → Accès API protégé

Utilisateur existant :
  App démarre → Splash → checkToken() → Token trouvé + validation API /auth/me
  → Redirection /home directement → Pas de login requis

Déconnexion :
  Cliquer "Logout" → Token supprimé → Redirection /login
```

## Points d'amélioration (Roadmap)

- Refresh token (durée 7 jours reste acceptable pour une appli agricole ouverte quotidiennement)
- Vérification d'email (OTP ou lien)
- Récupération de mot de passe oublié
- 2FA (authentification à deux facteurs)
- SSO (Single Sign-On) avec identité fédérée

## Vérification de santé

✅ **Phase 1 est complète et testable :**
- Backend prêt : endpoints Swagger accessibles
- Mobile prêt : écrans auth fonctionnels, Riverpod branché, go_router configuré
- Base de données : migrations appliquées, schéma à jour
- Token JWT : stateless, validé côté serveur, persistant côté client

**Pas de dépendances bloquées entre Phase 1 et Phase 2.**

---

## Prochaines étapes (Phase 2)

Phase 2 ajoutera la gestion des fermes et des parcelles avec une carte interactive OSM. Les endpoints existants sur `/api/v1/parcels` seront adaptés pour utiliser l'authentification JWT et les fermes comme conteneur hiérarchique.
