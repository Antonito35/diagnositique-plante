# PLANTDIAG - SCRIPT DE PRÉSENTATION ORALE (15 minutes)

**Timing Total:** 15 minutes

---

## SLIDE 1 - TITRE (10 secondes)

**À dire :**
"Bonjour, je m'appelle Antoine SIMON et je présente PlantDiag, un système de diagnostic agricole par intelligence artificielle. Ce projet a été réalisé dans le cadre du Bachelor 2, en partenariat avec la Chambre d'Agriculture."

---

## SLIDE 2 - PROBLÉMATIQUE (1 min 50 secondes)

**À dire :**
"Le contexte : les agriculteurs font face à un vrai problème au quotidien.

Lorsqu'une maladie apparaît sur une culture, il faut l'identifier rapidement, sinon toute la récolte peut être perdue.

Aujourd'hui, l'identification se fait soit manuellement, ce qui prend du temps et manque de précision, soit en contactant un expert, ce qui coûte cher.

Il n'existe pas de solution accessible et mobile pour les petits et moyens agriculteurs.

Notre réponse : PlantDiag. Une application web mobile permettant de photographier une feuille et obtenir un diagnostic immédiat via intelligence artificielle.

Simple, rapide, accessible, précise."

---

## SLIDE 3 - OBJECTIFS CDC (30 secondes)

**À dire (rapide):**
"Pour respecter le cahier des charges du Bachelor 2, nous devions développer une application mobile web responsive avec une fonctionnalité IA, la déployer sur AWS avec 3 technologies imposées, et documenter complètement.

Résultat : 100% des objectifs réalisés."

---

## SLIDE 4 - DÉMONSTRATION LIVE (3 minutes)

**À dire :**
"Passons à la démonstration. L'application est actuellement en production sur AWS à cette adresse : http://13.51.48.254:8000

Je vais montrer les principales fonctionnalités :

1. D'abord, je crée une parcelle. Voilà, la parcelle est créée.

2. Maintenant, je vais faire un diagnostic. Je clique sur l'onglet 'Diagnostic', j'upload une photo de feuille... L'IA a analysé la photo et détecté une maladie avec 87% de précision. On voit aussi le type de sévérité, les traitements recommandés.

3. Regardez l'onglet 'Historique'. Tous les diagnostics sont sauvegardés en base de données.

4. L'onglet 'Alertes' montre les alertes intelligentes basées sur la localisation. Les alertes changent selon votre région.

5. La météo : je peux chercher une ville, voir les prévisions 5 jours, et ajouter mes villes préférées aux favoris.

Voilà pour la démo. L'application est intuitive, rapide, et déjà utilisable."

---

## SLIDE 5 - FONCTIONNALITÉS (1 minute)

**À dire :**
"Récapitulatif des fonctionnalités :

- Diagnostic IA : analyse photo, retourne 5 maladies ou feuille saine
- Gestion parcelles : créer, éditer, supprimer
- Historique : tous les diagnostics sauvegardés
- Météo : temps réel plus prévisions plus risques par région
- Alertes : intelligentes basées sur votre localisation et la météo

Tout est persistant - rien ne se perd."

---

## SLIDE 6 - ARCHITECTURE RÉSEAU (2 minutes)

**À dire :**
"Parlons de l'architecture technique. C'est un système 4 tiers :

TIER 1 - Présentation : Le frontend HTML/CSS/JavaScript que vous venez de voir. C'est responsive, ça fonctionne sur mobile et desktop.

TIER 2 - Métier : L'API REST que j'ai construite en FastAPI. C'est l'intelligence du système, elle gère toute la logique métier.

TIER 3 - Données : PostgreSQL 15 pour les données persistantes plus Redis pour le cache et les sessions.

TIER 4 - Services externes : OpenCV pour l'analyse d'image IA, et Open-Meteo pour la météo en temps réel.

Le flux, c'est simple : vous envoyez une photo au frontend, le frontend l'envoie à l'API, l'API la traite avec OpenCV, sauvegarde en PostgreSQL, et retourne le résultat en JSON."

---

## SLIDE 7 - TECHNOLOGIES IMPOSÉES (1 min 30 secondes)

**À dire :**
"Parlons des 3 technologies imposées par le CDC.

1. FastAPI pour le backend Python - C'est un framework moderne, asynchrone, avec validation native. Parfait pour IA puisque Python domine ce domaine.

2. PostgreSQL pour la base de données - C'est relationnelle, ACID-compliant, scalable, standard industrie. On a des relations claires entre utilisateurs, parcelles, et diagnostics.

3. Docker plus AWS pour l'infrastructure - Docker permet la containerisation, votre code s'exécute pareil en dev et production. AWS c'est production-ready et gratuit 12 mois pour nous.

Ces 3 technologies fonctionnent ensemble naturellement et répondent à toutes les contraintes."

---

## SLIDE 8 - API REST (30 secondes)

**À dire :**
"Vous pouvez consulter la documentation complète de l'API via Swagger à http://13.51.48.254:8000/docs

Nous avons 8 endpoints : 3 pour l'authentification, 3 pour l'application, 2 pour documentation.

Chaque endpoint est testé et documenté."

---

## SLIDE 9 - INTELLIGENCE ARTIFICIELLE (1 min 30 secondes)

**À dire :**
"Détaillons l'IA, c'est le coeur du projet.

Nous utilisons OpenCV et NumPy, les outils standard de computer vision en Python.

Comment ça fonctionne ? On reçoit une photo de feuille. OpenCV analyse la couleur, la saturation, le contraste, la texture. On compare ces caractéristiques aux patterns connus de 5 maladies. On retourne la maladie la plus probable plus confidence score.

Accuracy : 87%. C'est au-dessus du 85% requis par le CDC.
Performance : réponse en 1.5 secondes, bien sous les 2 secondes prévues.

Les 5 maladies : Mildiou, Oïdium, Rouille, Brûlure, Tache noire, plus la classe Feuille saine.

C'est simple mais efficace."

---

## SLIDE 10 - SÉCURITÉ (1 minute)

**À dire :**
"La sécurité, c'est important pour un système agricole.

Authentification par JWT tokens : chaque utilisateur reçoit un token unique valide 30 jours. Pas de session côté serveur, scalable.

Hachage Bcrypt : les mots de passe sont hashés avec salts, impossible à retrouver même si la BD est compromise.

Validation Pydantic : chaque donnée entrante est validée avant d'entrer en BD.

CORS configuré : protection contre les requêtes cross-origin malveillantes.

HTTPS ready : on peut activer HTTPS avec Let's Encrypt en production.

Les données utilisateur sont persistantes et sécurisées en PostgreSQL."

---

## SLIDE 11 - DÉPLOIEMENT AWS (1 min 30 secondes)

**À dire :**
"Comment est-ce déployé en production ?

Nous utilisons une instance AWS EC2 t2.micro dans la région US-East-1.

Cette instance exécute 3 conteneurs Docker : FastAPI API, PostgreSQL 15, et Redis 7.

Les volumes Docker sont persistants - les données ne se perdent pas si un conteneur s'arrête.

L'instance a une adresse IP publique : 13.51.48.254. L'application est donc accessible 24/7 depuis n'importe où.

Gratuit pendant 12 mois avec AWS Free Tier.

C'est production-ready. Pas juste une demo sur un laptop."

---

## SLIDE 12 - MÉTRIQUES (1 minute)

**À dire :**
"Regardons les chiffres du projet par rapport aux objectifs du CDC :

Endpoints API : objectif 5 plus, nous avons 8. Plus 60% !
Temps de réponse : objectif inférieur à 2 secondes, nous avons 1.5 secondes. Moins 25% !
Accuracy IA : objectif supérieur à 85%, nous avons 87%. Plus 2% !
Technologies imposées : objectif 3, nous avons 3. 100% !
Documentation : objectif complète, nous avons 6 fichiers.

Le projet dépasse les attentes sur tous les critères mesurables."

---

## SLIDE 13 - COMPÉTENCES BACHELOR 2 (45 secondes)

**À dire :**
"Ce projet démontre toutes les compétences du Bachelor 2 :

IA/ML : analyse d'image OpenCV, classification multi-classe, confidence scoring.

Backend : API REST, async/await, ORM SQLAlchemy, gestion d'erreurs.

Frontend : HTML5, CSS3, JavaScript, API consumption, responsive design.

Database : PostgreSQL, relations, transactions ACID, indexing.

DevOps/Cloud : Docker multi-container, AWS EC2, architecture scalable.

C'est un projet complet qui touche à tous les domaines."

---

## SLIDE 14 - CONCLUSION (1 minute)

**À dire :**
"En conclusion :

PlantDiag est une solution production-ready, 100% conforme au CDC, et immédiatement utilisable par des agriculteurs réels.

Application fonctionnelle et déployée en production. Code source nettoyé et versionnalisé sur GitHub. Architecture documentée et scalable. 3 technologies Bachelor 2 maîtrisées et intégrées.

C'est plus qu'une simple école - c'est un produit réel."

---

## SLIDE 15 - QUESTIONS (1 min 30 secondes)

**À dire :**
"Merci de votre attention.

L'application est accessible à : http://13.51.48.254:8000
La documentation API Swagger à : http://13.51.48.254:8000/docs
Le code source complet sur GitHub : github.com/Antonito35/diagnositique-plante

Des questions ?"

---

## QUESTIONS POSSIBLES ET RÉPONSES

**Q: "Pourquoi FastAPI et pas Node.js ?"**
R: "Parce que Python domine le domaine de l'IA et du machine learning. OpenCV, NumPy, tous les outils IA standards sont en Python. FastAPI est le framework Python le plus rapide et moderne."

**Q: "Comment fonctionne exactement l'IA ?"**
R: "OpenCV analyse les pixels : couleur, saturation, contraste, texture. On compare à des patterns connus de maladies. C'est du computer vision classique, pas du deep learning, donc c'est simple et efficace."

**Q: "Pouvez-vous scaler cette solution ?"**
R: "Oui. Aujourd'hui 1 instance EC2, mais on peut facilement passer à plusieurs instances avec un load balancer. AWS Auto-scaling est prêt. On pourrait aussi passer à Kubernetes plus tard."

**Q: "Pourquoi PostgreSQL et pas MongoDB ?"**
R: "Parce qu'on a une structure relationnelle claire : Utilisateurs vers Parcelles vers Diagnostics. PostgreSQL garantit les transactions ACID - les données ne peuvent pas être corrompues même en cas de panne."

**Q: "Combien coûte ce système ?"**
R: "Le côté application : 0 euros, c'est de l'open source. AWS : gratuit 12 mois avec Free Tier, puis environ 5-10 euros par mois pour une instance t2.micro. C'est très accessible pour une chambre d'agriculture."

**Q: "Les données sont sécurisées ?"**
R: "Oui. Authentification JWT, Bcrypt pour les mots de passe, validation des données en entrée. On peut ajouter HTTPS avec Let's Encrypt en production. Les données sont persistantes en PostgreSQL."

**Q: "Pourquoi 87% d'accuracy et pas 99% ?"**
R: "Parce qu'on n'utilise pas du deep learning lourd. On utilise OpenCV classique qui est plus simple et rapide. 87% est déjà excellent pour du computer vision classique et suffisant pour un agriculteur."

**Q: "Ça marche sur mobile ?"**
R: "Oui, c'est responsive. Fonctionne sur iPhone, Android, depuis le navigateur. Pas besoin d'app native."

---

**Durée totale : 15 minutes exactement**
**Pratique avec une horloge à côté avant la présentation !**
