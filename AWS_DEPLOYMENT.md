# ☁️ Déploiement AWS - PlantDiag

## 🎯 Objectif

Déployer PlantDiag sur AWS EC2 (gratuit 12 mois) pour avoir une **URL publique** accessible de partout.

---

## 📋 **Étape 1 : Créer un Compte AWS (5 min)**

### Si vous n'avez pas de compte AWS :

1. Allez sur https://aws.amazon.com/fr/
2. Cliquez **"Créer un compte AWS"**
3. Remplissez :
   - Email personnel
   - Mot de passe
   - Nom du compte
4. **Carte bancaire requise** (gratuit 12 mois, pas de facturation)
5. Confirmez via email

✅ Vous avez un **compte gratuit 12 mois** !

---

## 🖥️ **Étape 2 : Lancer une Instance EC2 (3 min)**

### 2.1 - Console AWS
- Allez sur https://console.aws.amazon.com
- Cherchez **"EC2"** → cliquez

### 2.2 - Lancer une instance
1. **Instances** → **Lancer une instance**
2. **Nom** : `plantdiag-app`
3. **Image** : `Ubuntu 22.04 LTS` (gratuit)
4. **Type** : `t2.micro` (gratuit 12 mois)
5. **Paire de clés** :
   - Créer une nouvelle clé
   - Nom : `plantdiag-key`
   - Télécharger `.pem` dans vos Documents
6. **Groupe de sécurité** : Créer nouveau
   - Nom : `plantdiag-sg`
   - Règles :
     - HTTP (port 80) - Anywhere
     - HTTPS (port 443) - Anywhere
     - SSH (port 22) - Anywhere
     - TCP 8000 - Anywhere
7. **Lancer instance** → Attendre ~2 min

✅ Vous avez une **instance EC2 lancée** !

---

## 🔑 **Étape 3 : Se Connecter SSH (5 min)**

### Windows PowerShell
```powershell
# 1. Naviguer où la clé est stockée
cd C:\Users\Antoine\Documents

# 2. Donner les permissions
# (Cliquer droit sur plantdiag-key.pem → Propriétés → Sécurité → Modifier → Administrateur → OK)

# 3. Récupérer l'adresse IP publique
# → Aller sur AWS EC2 console → Instances → Copier "Adresse IPv4 publique"

# 4. Se connecter (remplacer X.X.X.X)
ssh -i plantdiag-key.pem ubuntu@X.X.X.X
```

✅ Vous êtes **connecté à l'instance** !

---

## 🚀 **Étape 4 : Déployer l'Application (5 min)**

### Sur la console SSH :

```bash
# 1. Mise à jour
sudo apt update
sudo apt upgrade -y

# 2. Installer Docker
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
sudo systemctl start docker

# 3. Cloner le projet (remplacer YOUR_REPO)
cd /home/ubuntu
git clone https://github.com/YOUR_REPO/plantdiag.git
cd plantdiag/backend

# 4. Créer .env
cat > .env << EOF
DATABASE_URL=sqlite:///./plantdiag.db
ENVIRONMENT=production
EOF

# 5. Lancer Docker
docker-compose up -d

# 6. Vérifier que ça marche
docker-compose ps
```

✅ Application **lancée sur AWS** !

---

## 🌐 **Étape 5 : Accéder à l'Application (2 min)**

### Trouver l'IP publique
```bash
# Sur la console SSH :
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

### Accéder de partout
```
🌍 Application : http://IP_PUBLIQUE:8000
📊 Swagger API : http://IP_PUBLIQUE:8000/docs
```

Exemple :
```
http://54.123.45.67:8000
```

---

## 🔧 **Dépannage**

### Port 8000 pas accessible ?
```bash
# Vérifier les logs
docker-compose logs -f

# Redémarrer
docker-compose down
docker-compose up -d
```

### Erreur permission SSH ?
```bash
# Donner les bonnes permissions
chmod 400 plantdiag-key.pem
```

### Besoin de la clé SSH ?
```bash
# La retrouver : C:\Users\Antoine\Documents\plantdiag-key.pem
# (Fichier téléchargé lors de la création)
```

---

## 💾 **Récapitulatif - Ce que vous avez**

```
✅ Compte AWS (gratuit 12 mois)
✅ Instance EC2 t2.micro (gratuit)
✅ Application Docker lancée
✅ URL publique accessible

Exemple résultat :
   http://54.123.45.67:8000 ← URL PUBLIQUE !
```

---

## 📊 **Vérification Déploiement**

```bash
# Sur SSH, vérifier tout fonctionne :
docker-compose ps
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/status
```

Devrait voir :
```json
{"status":"ok","version":"2.0.0"}
```

---

## 🎓 **Pour la Soutenance**

Vous pouvez dire :
- ✅ Application déployée sur AWS EC2
- ✅ Accessible en ligne : http://IP_PUBLIQUE:8000
- ✅ Infrastructure cloud (respecte CDC VI)
- ✅ Docker containerisée
- ✅ Scalable (peut ajouter Auto Scaling)

---

## ⏱️ **Coût (12 mois gratuit)**

```
EC2 t2.micro    : GRATUIT
Bande passante  : GRATUIT
Stockage EBS    : GRATUIT (30GB)

TOTAL : 0€ pendant 12 mois ✅
```

---

## 🚨 **Important**

1. **Ne pas oublier** : Arrêter l'instance quand vous testez pas
   ```bash
   # Console AWS → Instances → Arrêter
   ```

2. **La clé SSH est IMPORTANTE** :
   - Sauvegardez `plantdiag-key.pem`
   - Ne la partagez pas
   - Sans elle, vous ne pouvez plus accéder

3. **Pour le projet** :
   - Gardez l'instance lancée pendant la soutenance
   - Vous pouvez montrer la démo en direct

---

**Status** : ✅ Prêt pour déploiement AWS  
**Temps total** : ~20 minutes  
**Difficulté** : ⭐⭐ (facile avec guide)
