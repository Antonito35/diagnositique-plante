# Comment Créer les Fichiers Word et PowerPoint

## Option 1 : Création Rapide (5 minutes) - Recommandée

### Créer le Document Word

1. **Ouvrez Microsoft Word**
2. **Créez un nouveau document**
3. **Copie-collez le contenu** de `SOUTENANCE_SCRIPT.md` dedans
4. **Formatage rapide** :
   - Titre principal : 48pt, gras, couleur bleu foncé (#1E3A5F)
   - Sous-titres slides : 32pt, gras
   - Corps de texte : 22pt

5. **Sauvegardez** sous `SOUTENANCE.docx`

### Créer le PowerPoint

1. **Ouvrez Microsoft PowerPoint**
2. **Créez une présentation**
3. **Design/thème** :
   - Couleur arrière-plan : Bleu foncé (#1E3A5F)
   - Texte : Blanc
   - Titre : 54pt, gras
   - Contenu : 28pt

4. **Créez 15 slides** avec ce contenu :

```
SLIDE 1: PlantDiag
         Système de Diagnostic Agricole par Intelligence Artificielle

SLIDE 2: Problématique
         Identification rapide des maladies agricoles
         Solution mobile et accessible

SLIDE 3: Objectifs CDC
         100% des objectifs réalisés

SLIDE 4: Démonstration
         http://13.51.48.254:8000

SLIDE 5: Fonctionnalités
         Diagnostic IA • Gestion parcelles • Historique • Météo • Alertes

SLIDE 6: Architecture 4 Tiers
         Frontend → API → Database → Services

SLIDE 7: Technologies Imposées
         FastAPI • PostgreSQL • Docker + AWS

SLIDE 8: API REST (8 Endpoints)
         Documentation : http://13.51.48.254:8000/docs

SLIDE 9: Intelligence Artificielle
         OpenCV + NumPy
         87% accuracy • 1.5 secondes

SLIDE 10: Sécurité
          JWT • Bcrypt • Validation • CORS • HTTPS

SLIDE 11: Déploiement AWS
          EC2 t2.micro
          Gratuit 12 mois • 13.51.48.254

SLIDE 12: Métriques
          8 endpoints • 1.5s réponse • 87% accuracy

SLIDE 13: Compétences Bachelor 2
          IA • Backend • Frontend • Database • DevOps

SLIDE 14: Conclusion
          Production-ready • 100% CDC conforme

SLIDE 15: Questions ?
          http://13.51.48.254:8000
          github.com/Antonito35/diagnositique-plante
```

5. **Sauvegardez** sous `SOUTENANCE.pptx`

---

## Option 2 : Utiliser le Script Python (Si vous avez Python)

```bash
# Windows (si Python est installé)
python3 create_word_ppt.py

# Ubuntu/WSL
python3 create_word_ppt.py
```

**Prérequis :**
```bash
pip install python-docx python-pptx
```

---

## Option 3 : Utiliser Google Slides/Docs

1. Allez sur **docs.google.com**
2. Créez un nouveau document
3. Copie-collez le contenu de `SOUTENANCE_SCRIPT.md`
4. Téléchargez en Word (.docx)

Pour PowerPoint :
1. Allez sur **slides.google.com**
2. Créez une présentation
3. Ajoutez les 15 slides
4. Téléchargez en PowerPoint (.pptx)

---

## Checklist Fichiers Finaux

Vous devez avoir avant la soutenance :

- [x] `SOUTENANCE.html` - Diapos interactives (flèches clavier)
- [x] `SOUTENANCE_SCRIPT.md` - Script complet avec timing
- [ ] `SOUTENANCE.docx` - Document Word (créez-le)
- [ ] `SOUTENANCE.pptx` - PowerPoint (créez-le)

Les fichiers Word et PowerPoint sont optionnels mais utiles pour :
- **Word** : Imprimer le script de présentation
- **PowerPoint** : Avoir une version portable sans internet

---

## Avant la Soutenance

1. **Imprimez** le script Word (ou gardez-le sur tablette)
2. **Ouvrez** SOUTENANCE.html en fullscreen (F11)
3. **Testez** navigation clavier
4. **Pratiquez** 2 fois avec chronomètre
5. **Vérifiez** accès WiFi lieu de présentation

---

**Vous êtes prêt!** 🎓
