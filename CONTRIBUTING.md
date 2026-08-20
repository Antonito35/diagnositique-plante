# 🤝 Guide de Contribution - PlantDiag

Merci d'être intéressé par la contribution à PlantDiag ! Ce guide vous aidera à comprendre comment contribuer efficacement au projet.

---

## 📋 Table des matières

1. [Code de conduite](#code-de-conduite)
2. [Comment contribuer](#comment-contribuer)
3. [Processus de développement](#processus-de-développement)
4. [Standards de code](#standards-de-code)
5. [Tests](#tests)
6. [Commits](#commits)
7. [Pull Requests](#pull-requests)

---

## 📜 Code de conduite

Nous nous engageons à maintenir un environnement inclusif et respectueux.

### Notre engagement
- ✅ Être respectueux envers tous les contributeurs
- ✅ Accepter les critiques constructives
- ✅ Nous concentrer sur le meilleur pour la communauté
- ❌ Pas de harcèlement, discrimination ou abus

### Signaler des violations
Contactez : team@plantdiag.farm

---

## 🎯 Comment contribuer

### Types de contributions

#### 1. **Corrections de bugs**
```bash
git checkout -b bugfix/nom-du-bug
# Corriger le bug
# Ajouter des tests
git commit -m "fix: description du bug"
```

#### 2. **Nouvelles fonctionnalités**
```bash
git checkout -b feature/nom-de-la-fonctionnalite
# Implémenter la fonctionnalité
# Ajouter des tests
# Documenter les changements
git commit -m "feat: description courte"
```

#### 3. **Documentation**
```bash
git checkout -b docs/mise-a-jour
# Mettre à jour la documentation
git commit -m "docs: description"
```

#### 4. **Refactorisation**
```bash
git checkout -b refactor/nom
# Refactoriser le code
# Tests doivent passer
git commit -m "refactor: description"
```

#### 5. **Améliorations de performance**
```bash
git checkout -b perf/nom
git commit -m "perf: description"
```

---

## 🔄 Processus de développement

### 1. Fork le dépôt

```bash
# Cliquer "Fork" sur GitHub
git clone https://github.com/YOUR_USERNAME/plantdiag.git
cd plantdiag
git remote add upstream https://github.com/originalrepo/plantdiag.git
```

### 2. Créer une branche

```bash
# Mettre à jour main
git checkout main
git pull upstream main

# Créer une branche
git checkout -b feature/ma-fonctionnalite

# Convention de nommage:
# feature/nom-descriptif
# bugfix/nom-du-bug
# docs/sujet
# refactor/nom
```

### 3. Développer

```bash
# Faire les modifications
# Tester continuellement
pytest backend/test_app.py -v

# Vérifier le formatting
black backend/
flake8 backend/
```

### 4. Tester

```bash
# Tests unitaires
pytest backend/test_app.py -v --cov=backend

# Tests d'intégration
docker-compose up -d
pytest backend/test_app.py -v

# Tests manuels
curl http://localhost:8000/docs
```

### 5. Commit

```bash
# Vérifier les changements
git status
git diff

# Ajouter les fichiers
git add .  # ou git add fichier_specifique

# Commit avec message descriptif
git commit -m "feat: add new feature

Description plus détaillée si nécessaire.
- Détail 1
- Détail 2"
```

### 6. Push

```bash
git push origin feature/ma-fonctionnalite
```

### 7. Pull Request

- Aller sur GitHub
- Cliquer "New Pull Request"
- Sélectionner votre branche
- Remplir le template PR
- Soumettre

---

## 📝 Standards de code

### Python (Backend)

#### Format
```bash
# Utiliser black
black backend/

# Vérifier les erreurs
flake8 backend/ --max-line-length=100
```

#### Style

```python
# ✅ BON
def diagnose_disease(image_array: np.ndarray) -> dict:
    """Diagnose plant disease from image."""
    prediction = model.predict(image_array)
    return {"disease": prediction["name"], "confidence": prediction["score"]}

# ❌ MAUVAIS
def diagnose(img):
    p = model.predict(img)
    return p
```

#### Documentation

```python
def analyze_image(image_path: str, parcel_id: int) -> dict:
    """
    Analyze plant image for disease diagnosis.

    Args:
        image_path: Path to the image file
        parcel_id: ID of the parcel being analyzed

    Returns:
        dict: Diagnosis results with confidence and recommendations

    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image format is invalid
    """
```

#### Type Hints
```python
# ✅ Toujours utiliser les type hints
def get_user_diagnoses(user_id: int, limit: int = 10) -> list[dict]:
    pass

# Types complexes
from typing import Optional, Union
def process(data: Optional[dict] = None) -> Union[str, int]:
    pass
```

### Dart (Mobile)

#### Format
```bash
dart format lib/
```

#### Conventions
```dart
// ✅ BON
class DiagnosisWidget extends StatefulWidget {
  final int parcelId;
  final String disease;

  const DiagnosisWidget({
    required this.parcelId,
    required this.disease,
  });
}

// ❌ MAUVAIS
class diagnosisWidget extends StatelessWidget {
  var parcelId;
  var disease;
}
```

---

## ✅ Tests

### Backend - Tests requis

```bash
# Avant de faire une PR, tous ces tests doivent passer:

# 1. Linter
black --check backend/
flake8 backend/

# 2. Unit tests
pytest backend/test_app.py -v

# 3. Coverage (minimum 70%)
pytest backend/test_app.py --cov=backend --cov-report=term
```

### Ajouter des tests

```python
# backend/test_app.py

def test_new_feature():
    """Test description."""
    result = new_function()
    assert result == expected_value

def test_error_handling():
    """Test error scenarios."""
    with pytest.raises(ValueError):
        invalid_function()
```

### Coverage minimal

- Nouvelles fonctionnalités : minimum 80%
- Bug fixes : couvrir le cas qui causait le bug
- Refactorisation : maintenir la couverture

---

## 📌 Commits

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat** : Nouvelle fonctionnalité
- **fix** : Correction de bug
- **docs** : Documentation
- **style** : Formatage, typo
- **refactor** : Refactorisation sans changement fonctionnel
- **perf** : Amélioration de performance
- **test** : Ajout/modification de tests
- **ci** : CI/CD configuration
- **chore** : Autres (dépendances, config)

### Exemples

```bash
# ✅ BON
git commit -m "feat(api): add disease confidence threshold validation"
git commit -m "fix(mobile): handle network timeout on photo upload

- Retry logic with exponential backoff
- Show user-friendly error message
- Log detailed error for debugging"

git commit -m "docs(setup): update installation instructions for windows"

# ❌ MAUVAIS
git commit -m "Fix stuff"
git commit -m "Updated files"
git commit -m "wip"
```

---

## 🔀 Pull Requests

### Checklist avant soumettre

- [ ] Je suis sur une branche à jour (`git pull upstream main`)
- [ ] Les tests passent (`pytest`)
- [ ] Le code est formaté (`black`, `flake8`)
- [ ] La documentation est à jour
- [ ] Les commits sont propres et descriptifs
- [ ] La PR a un titre descriptif

### Template PR

```markdown
## 📝 Description
Brève description de ce que fait cette PR.

## 🔗 Issue liée
Ferme #123

## 🧪 Comment tester
1. Étape 1
2. Étape 2
3. Étape 3

## ✅ Checklist
- [ ] Tests ajoutés/mis à jour
- [ ] Documentation mise à jour
- [ ] Pas de breaking changes
- [ ] Code formaté et bien commenté
```

### Critères d'acceptation

Pour qu'une PR soit acceptée :

1. ✅ Tests passent (100%)
2. ✅ Code reviewé et approuvé
3. ✅ Pas de conflits merge
4. ✅ Documentation à jour
5. ✅ Commits propres
6. ✅ Pas de regressions

---

## 🐛 Rapporter des bugs

### Créer une issue

1. Aller à [Issues](https://github.com/plantdiag/plantdiag/issues)
2. Cliquer "New Issue"
3. Fournir :

```markdown
## Description du bug
Description claire et concise.

## Pas à reproduire
1. Étape 1
2. Étape 2
3. Étape 3

## Résultat attendu
Ce qui devrait se passer.

## Résultat réel
Ce qui se passe réellement.

## Environnement
- OS: Windows 11 / macOS / Linux
- Python: 3.11
- Flutter: 3.13
```

---

## 💬 Questions ?

- **Documentation** : Voir `/docs`
- **Discussions** : GitHub Discussions
- **Email** : team@plantdiag.farm
- **Chat** : Discord (lien)

---

## 📚 Ressources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Dart Style Guide](https://dart.dev/guides/language/effective-dart/style)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

## ⭐ Merci !

Votre contribution aide à rendre PlantDiag meilleur pour les agriculteurs du monde entier !

**N'hésitez pas à poser des questions.** Les mainteneurs sont là pour aider. 🙌

---

**Version** : 1.0  
**Dernière maj** : 20 août 2026  
**Statut** : En vigueur
