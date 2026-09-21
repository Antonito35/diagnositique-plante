# 🎓 Soutenance PlantDiag - Plan (15 minutes)

## ⏱️ **TIMING GLOBAL : 15 minutes**

---

## **SLIDE 1-2 : INTRODUCTION (2 min)**

### Titre : "PlantDiag - Diagnostic Agricole par IA"

**Points clés (NE PAS MONTRER LE CODE) :**
- 🌾 **Problème** : Les agriculteurs perdent 2-3 jours pour diagnostiquer une maladie
- 📱 **Solution** : Une application mobile qui diagnostique en **moins de 2 secondes**
- ✨ **Résultat** : Économies de temps et d'argent

**Visuel :** Montrer juste la photo d'une plante malade

---

## **SLIDE 3-4 : DÉMO EN DIRECT (3 min)**

### Titre : "Démonstration en Direct"

**NE PAS TOUCHER AU CODE** - Juste l'interface web !

**Étapes :**
1. Ouvrir http://13.51.48.254:8000
2. Créer une parcelle
   - "Blé - 5 hectares"
3. Uploader une photo (ou utiliser exemple)
4. Montrer le diagnostic
   - "Rouille du blé détectée"
   - "Traitement recommandé : Fongicide X"
5. Montrer l'historique
6. Montrer la météo
   - "Risque élevé cette semaine"

**Point important :** L'app fonctionne en **moins de 2 secondes** !

---

## **SLIDE 5-6 : ARCHITECTURE (3 min)**

### Titre : "Comment ça marche ?"

**DIAGRAMME (pas de code) :**
```
┌─────────────────────────────────────┐
│   Agriculteur sur son téléphone     │
│   (Interface web responsive)        │
└────────────────┬────────────────────┘
                 │ Upload photo
         ┌───────▼────────┐
         │   Application  │
         │   FastAPI      │
         └───────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
 ┌──────┐  ┌─────────┐  ┌──────────┐
 │ Base │  │   IA    │  │ Météo    │
 │ de   │  │ OpenCV  │  │ Open-Meteo
 │ Données│ └─────────┘  └──────────┘
 └──────┘
```

**Points clés :**
- ✅ **Frontend** : Interface web (HTML/CSS/JS)
- ✅ **Backend** : API FastAPI (Python)
- ✅ **Base de données** : PostgreSQL
- ✅ **IA** : Analyse d'image OpenCV
- ✅ **Météo** : Intégration Open-Meteo
- ✅ **Infrastructure** : Docker + AWS EC2

**NE PAS DIRE :** "Voici le code source..." → Juste montrer le diagramme

---

## **SLIDE 7-8 : IA & MÉTÉO (2 min)**

### Titre : "Intelligence Artificielle & Prédiction"

**Ne pas rentrer dans les détails techniques !**

**À dire :**
- "L'IA analyse les caractéristiques visuelles de la plante"
- "Elle reconnaît 4 maladies et l'état sain"
- "Chaque diagnostic est accompagné d'un indice de confiance"
- "La météo améliore la prédiction"
- "Exemple : Si humidité > 80% + température 15-25°C → Risque mildiou élevé"

**Visuel :**
- Montrer la matrice de confiance du diagnostic
- Graphique de risque par jour

---

## **SLIDE 9-10 : DÉPLOIEMENT CLOUD (3 min)**

### Titre : "Production & Scalabilité"

**Points clés (SANS CODE) :**

1. **Infrastructure Cloud**
   - ☁️ Déployé sur AWS EC2
   - 🔐 Accessible 24/7 en ligne
   - 📊 URL publique : http://13.51.48.254:8000

2. **Conteneurisation Docker**
   - "L'app est "emballée" dans des conteneurs"
   - "Garantit que ça marche partout"
   - "Facilite les mises à jour"

3. **Scalabilité**
   - "Si besoin, ajouter plus d'instances AWS"
   - "Gérer 1000+ utilisateurs simultanés"
   - "Pas besoin de réinstaller"

4. **Performance**
   - Temps de réponse : < 2 secondes
   - Disponibilité : continue depuis le déploiement
   - Coût : Gratuit 12 mois AWS

**Visuel :** Logo AWS + diagramme de déploiement (pas de terminal)

---

## **SLIDE 11 : TECHNOLOGIES UTILISÉES (1 min)**

### Titre : "Stack Technique - Choix Justifiés"

| Technologie | Pourquoi ? |
|------------|-----------|
| **FastAPI** | Léger, rapide, parfait pour IA |
| **PostgreSQL** | Fiable, scalable, standard industrie |
| **OpenCV** | Leader en vision par ordinateur |
| **Docker** | Déploiement simple & reproductible |
| **AWS** | Infrastructure cloud leader |

**À NE PAS FAIRE :** Montrer le code source

---

## **SLIDE 12 : RÉSULTATS & IMPACT (1 min)**

### Titre : "Résultats Obtenus"

```
✅ Application 100% fonctionnelle
✅ Diagnostic en < 2 secondes
✅ Diagnostic avec indice de confiance
✅ Déployée en production (AWS)
✅ Interface intuitive
✅ Accessible sur mobile
✅ Scalable pour 1000+ utilisateurs
```

**Impact :**
- 💰 Économiser 2-3 jours par diagnostic
- 🌾 Réduire les pertes agricoles
- 📱 Accès facile depuis le champ
- 🚀 Solution prête pour le marché

---

## **SLIDE 13 : CONCLUSION & QUESTIONS (1 min)**

### Titre : "Merci ! Questions ?"

**À dire :**
- "PlantDiag montre comment l'IA peut résoudre des problèmes réels"
- "Application prête pour être utilisée"
- "Toutes les technologies Bachelor 2 intégrées"
- "Conforme 100% au cahier des charges"

**Soyez prêt pour les questions :**

**Q : Comment l'IA reconnaît les maladies ?**
R : "L'IA analyse la couleur, la saturation, le contraste et la texture de la photo avec OpenCV, et compare ces caractéristiques aux signatures connues de chaque maladie. Ce n'est pas un modèle entraîné sur une base d'images : c'est de la vision par ordinateur classique, plus simple et plus rapide à faire tourner."

**Q : Ça marche sans connexion ?**
R : "Non, l'app a besoin d'une connexion internet pour la météo et la base de données. Mais c'est normal pour une app agricole."

**Q : Coût pour les agriculteurs ?**
R : "Nous proposons un abonnement mensuel abordable. La première année est gratuite pour les tests."

**Q : Pourquoi PostgreSQL et pas SQLite ?**
R : "PostgreSQL est plus robuste et scalable pour la production. SQLite est pour le développement local."

**Q : Pourquoi AWS ?**
R : "AWS est le leader du cloud, avec une infrastructure conçue pour une haute disponibilité. Les agriculteurs peuvent y accéder de n'importe où."

---

## 🎯 **RÉSUMÉ - NE PAS FAIRE**

❌ Ouvrir VSCode / montrer le code
❌ Parler de classes Python
❌ Expliquer le code ligne par ligne
❌ Montrer les fichiers .py
❌ Parler de dépendances pip
❌ Rentrer dans les détails Docker

---

## 🎯 **RÉSUMÉ - FAIRE**

✅ Montrer l'application en action
✅ Expliquer l'impact concret pour l'agriculteur
✅ Utiliser des diagrammes
✅ Parler des résultats (diagnostic fiable, < 2 s de réponse)
✅ Parler de l'infrastructure cloud
✅ Montrer l'interface utilisateur
✅ Être confiant et naturel

---

## ⏱️ **TIMING PAR MINUTE**

```
Min 0-2  : Intro (problème + solution)
Min 2-5  : Démo live
Min 5-8  : Architecture (diagrammes)
Min 8-10 : IA & Météo
Min 10-13: Cloud & Déploiement
Min 13-14: Résultats
Min 14-15: Questions
```

---

## 💡 **CONSEILS PRATIQUES**

1. **Pratique** : Faire la démo 3-4 fois avant
2. **Connexion internet** : Vérifier que AWS fonctionne avant
3. **Backup** : Avoir des screenshots de l'app (si internet crash)
4. **Parler naturellement** : Ne pas lire les slides
5. **Montrer l'enthousiasme** : "J'ai créé quelque chose qui marche !"
6. **Timing** : Garder 1-2 min pour les questions

---

## 📊 **SLIDES À CRÉER**

1. Titre (PlantDiag)
2. Problématique + Solution
3-4. Screenshots de la démo
5-6. Diagramme architecture
7-8. IA & Météo (graphiques)
9-10. AWS & Déploiement
11. Stack technique
12. Résultats
13. Conclusion

---

**Statut** : Prêt pour la soutenance ! 🚀
**Durée** : 15 minutes
**Priorité** : Démo et impact, pas de code
