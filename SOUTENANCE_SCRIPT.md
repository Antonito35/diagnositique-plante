# PLANTDIAG - SCRIPT DE PRÉSENTATION ORALE (15 minutes)

**Support associé :** SOUTENANCE.pptx (16 diapositives) et SOUTENANCE.docx (version imprimable de ce script)

---

## SLIDE 1 - TITRE (10 secondes)

**À dire :**
"Bonjour, je m'appelle Antoine SIMON et je présente PlantDiag, un système de diagnostic agricole par intelligence artificielle. Ce projet a été réalisé dans le cadre du Bachelor 2, en partenariat avec la Chambre d'Agriculture."

---

## SLIDE 2 - PROBLÉMATIQUE (1 min 20)

**À dire :**
"Le contexte : les agriculteurs font face à un vrai problème au quotidien.

Lorsqu'une maladie apparaît sur une culture, il faut l'identifier rapidement, sinon toute la récolte peut être perdue.

Aujourd'hui, l'identification se fait soit manuellement, ce qui prend du temps et manque de précision, soit en contactant un expert, ce qui coûte cher. Il n'existe pas de solution accessible et mobile pour les petits et moyens agriculteurs.

Notre réponse : photographier une feuille et obtenir un diagnostic immédiat, complété par une surveillance permanente des parcelles grâce à des capteurs."

---

## SLIDE 3 - OBJECTIFS CDC (25 secondes)

**À dire (rapide) :**
"Pour respecter le cahier des charges du Bachelor 2, nous devions développer une application mobile web responsive avec une fonctionnalité IA, la déployer sur AWS avec une architecture réseau intégrant des capteurs IoT, et utiliser 3 technologies imposées documentées.

Résultat : 100 % des objectifs réalisés."

---

## SLIDE 4 - DÉMONSTRATION EN DIRECT (3 minutes)

**À dire :**
"Passons à la démonstration. L'application est actuellement en production sur AWS à cette adresse : http://13.51.48.254:8000

Je vais montrer les principales fonctionnalités :

1. D'abord, je crée une parcelle. Elle part directement en base de données.
2. Maintenant, je vais faire un diagnostic. Je clique sur l'onglet 'Diagnostic', j'upload une photo de feuille... L'IA a analysé la photo et détecté une maladie avec un indice de confiance élevé. On voit aussi la sévérité et les traitements recommandés.
3. Onglet 'Capteurs' : voici le réseau. Chaque parcelle a son boîtier, qui remonte six mesures. Vous voyez le nombre de capteurs en ligne et le nombre total de trames reçues.
4. Onglet 'Alertes' : c'est là que tout se croise. Le serveur compare les relevés des capteurs, le dernier diagnostic et la météo, puis classe les alertes par gravité.
5. La météo : je peux chercher une ville, voir les prévisions sur cinq jours, et enregistrer mes villes favorites.

Voilà pour la démo. L'application est intuitive, rapide, et déjà utilisable."

---

## SLIDE 5 - FONCTIONNALITÉS (30 secondes)

**À dire :**
"Récapitulatif des fonctionnalités : diagnostic IA, capteurs de parcelle, gestion des parcelles, historique, météo temps réel et alertes croisées.

Tout est persistant en base de données - rien ne dépend du navigateur."

---

## SLIDE 6 - ARCHITECTURE RÉSEAU (1 min 20)

**À dire :**
"Parlons de l'architecture technique. Elle part du terrain : chaque parcelle porte un capteur qui envoie ses mesures à l'API.

Viennent ensuite quatre tiers. TIER 1, la présentation : le frontend HTML/CSS/JavaScript responsive. TIER 2, le métier : l'API REST FastAPI qui gère toute la logique. TIER 3, les données : PostgreSQL pour le stockage persistant, Redis pour le cache. TIER 4, les services externes : OpenCV pour l'analyse d'image et Open-Meteo pour la météo.

Le flux d'un diagnostic est simple : la photo part du frontend vers l'API, elle est traitée par OpenCV, sauvegardée en base, et le résultat revient en JSON."

---

## SLIDE 7 - CAPTEURS IoT (1 min 10)

**À dire :**
"Parlons des capteurs, parce que c'est ce qui rend la surveillance continue possible.

Chaque boîtier mesure six grandeurs : l'humidité et la température du sol, la température et l'hygrométrie de l'air, l'humectation du feuillage, et son propre niveau de batterie. Il envoie une trame par minute, en HTTP, vers l'API.

La grandeur la plus importante est l'humectation foliaire. Quand le feuillage reste mouillé et que la température est douce, entre 15 et 25 degrés, les spores germent : c'est exactement la règle qui déclenche notre alerte de risque fongique.

Le serveur détecte aussi le stress hydrique, l'excès d'eau, une batterie faible et un capteur devenu muet depuis plus de quinze minutes.

Aujourd'hui, ces capteurs sont simulés par un conteneur dédié - le cahier des charges l'autorise explicitement. Mais ils parlent le même protocole que de vrais boîtiers : les remplacer ne demanderait aucune modification de l'API."

---

## SLIDE 8 - TECHNOLOGIES IMPOSÉES (1 min 05)

**À dire :**
"Parlons des 3 technologies imposées par le CDC.

FastAPI pour le backend Python - framework asynchrone, validation native, idéal pour l'IA puisque Python domine ce domaine.

PostgreSQL pour la base de données - relationnelle, transactions ACID, adaptée aux relations entre utilisateurs, parcelles, diagnostics et relevés de capteurs.

Docker et AWS pour l'infrastructure - le conteneur garantit un comportement identique en développement et en production. Pas Kubernetes, disproportionné pour un MVP."

---

## SLIDE 9 - INTERFACE DE PROGRAMMATION (25 secondes)

**À dire :**
"L'API expose 18 endpoints, répartis en quatre familles : authentification, parcelles, capteurs IoT, diagnostic et suivi.

Tout est testable en direct via Swagger, à l'adresse slash docs."

---

## SLIDE 10 - INTELLIGENCE ARTIFICIELLE (1 min 05)

**À dire :**
"Nous utilisons OpenCV et NumPy, les outils standards de la vision par ordinateur en Python.

On reçoit la photo, OpenCV analyse la couleur, la saturation, le contraste et la texture, on compare ces caractéristiques aux signatures des maladies connues, et on retourne la plus probable avec un indice de confiance.

Précision : 87 %, au-dessus des 85 % requis par le CDC. Performance : réponse en 1,5 seconde."

---

## SLIDE 11 - SÉCURITÉ (40 secondes)

**À dire :**
"Six couches de sécurité : jetons JWT valables trente jours sans session côté serveur, mots de passe hachés avec Bcrypt et sel, validation systématique des données entrantes - y compris les trames des capteurs -, CORS configuré, HTTPS prêt via Let's Encrypt, et isolation des données par utilisateur."

---

## SLIDE 12 - DÉPLOIEMENT (50 secondes)

**À dire :**
"Une instance AWS EC2 t2.micro sous Ubuntu, adresse IP publique, disponible en continu, gratuite pendant douze mois.

Elle exécute quatre conteneurs Docker : l'API, PostgreSQL, Redis et le simulateur de capteurs. Les volumes sont persistants, les données survivent à tout redémarrage.

C'est de la production, pas une démonstration sur un ordinateur portable."

---

## SLIDE 13 - RÉSULTATS MESURÉS (40 secondes)

**À dire :**
"Face aux objectifs : 18 endpoints livrés pour 5 demandés. 1,5 seconde de temps de réponse contre moins de 2 exigées. 87 % de précision contre 85 demandés. Un relevé par minute et par capteur, soit une surveillance continue.

Chaque critère mesurable est atteint ou dépassé."

---

## SLIDE 14 - COMPÉTENCES BACHELOR 2 (25 secondes)

**À dire :**
"Ce projet couvre les cinq domaines du Bachelor 2 : intelligence artificielle, développement backend, développement frontend, bases de données, et réseau avec l'IoT et le cloud."

---

## SLIDE 15 - CONCLUSION (30 secondes)

**À dire :**
"PlantDiag est fonctionnel, conforme au cahier des charges, documenté et évolutif.

Il est immédiatement utilisable par un agriculteur, depuis son téléphone, dans son champ."

---

## SLIDE 16 - QUESTIONS (1 min 30)

**À dire :**
"Merci de votre attention.

L'application, la documentation de l'API et le code source complet sont aux adresses affichées. Je suis à votre disposition pour vos questions."

---

## QUESTIONS POSSIBLES ET RÉPONSES

**Q : "Les capteurs sont-ils réels ?"**
R : "Non, ils sont simulés par un conteneur dédié, et le cahier des charges l'autorise explicitement : « capteurs IoT simulés ou réels ». Les trames partent en HTTP vers l'API exactement comme le feraient de vrais capteurs, et le serveur ne fait pas de différence."

**Q : "Comment passeriez-vous à de vrais capteurs ?"**
R : "En remplaçant le conteneur par des boîtiers physiques qui envoient la même trame JSON sur le même endpoint. Aucune ligne de l'API ne changerait."

**Q : "Pourquoi mesurer l'humectation du feuillage ?"**
R : "Parce que c'est le facteur déclenchant des maladies fongiques. Une spore a besoin d'eau libre sur la feuille pour germer, et d'une température douce. L'humidité de l'air ne suffit pas à le dire."

**Q : "Pourquoi FastAPI plutôt que Node.js ?"**
R : "Parce que toute la chaîne d'intelligence artificielle est en Python : OpenCV, NumPy. FastAPI est en plus asynchrone et génère sa documentation automatiquement."

**Q : "Comment fonctionne exactement l'IA ?"**
R : "C'est de la vision par ordinateur classique, pas du deep learning. OpenCV extrait des caractéristiques de l'image - couleur, saturation, contraste, texture - et je les compare aux signatures des maladies connues."

**Q : "Pourquoi 87 % de précision et pas 99 % ?"**
R : "Un réseau de neurones convolutif ferait mieux, mais demanderait un jeu de données annoté et beaucoup plus de ressources serveur. Pour une première indication fiable en une seconde, 87 % est pertinent. C'est aussi une évolution possible du projet."

**Q : "Pourquoi PostgreSQL plutôt que MongoDB ?"**
R : "Parce que le modèle est relationnel : utilisateur, parcelle, diagnostic, relevé de capteur. PostgreSQL garantit les transactions ACID."

**Q : "Cette solution peut-elle monter en charge ?"**
R : "Oui. Une seule instance EC2 suffit aujourd'hui. L'étape suivante serait un groupe d'auto-scaling derrière un répartiteur de charge, puis des réplicas en lecture."

**Q : "Combien coûte le système ?"**
R : "Le logiciel est open source, donc gratuit. AWS est gratuit pendant douze mois, puis environ cinq à dix euros par mois pour une instance t2.micro."

**Q : "Les données sont-elles sécurisées ?"**
R : "Oui : jetons JWT, mots de passe hachés avec Bcrypt, validation systématique des données entrantes, CORS configuré, isolation par utilisateur."

**Q : "Que se passe-t-il si un capteur tombe en panne ?"**
R : "Le serveur le détecte : au-delà de quinze minutes sans trame, le capteur est marqué hors ligne et une alerte de maintenance remonte."

**Q : "Ça marche sur mobile ?"**
R : "Oui, l'interface est responsive et s'ouvre dans le navigateur, sans installation. L'appareil photo du téléphone est directement utilisable."

---

**Durée totale : 15 minutes**
**Pratiquer avec un chronomètre avant la présentation.**
