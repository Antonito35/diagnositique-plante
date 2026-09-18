#!/bin/bash

# 🚀 Script de Déploiement PlantDiag sur AWS EC2
# Exécuter après SSH sur instance Ubuntu 22.04

set -e

echo "========================================="
echo "🌿 PlantDiag - Déploiement AWS"
echo "========================================="

# 1. Mise à jour du système
echo "📦 1/5 - Mise à jour du système..."
sudo apt update
sudo apt upgrade -y

# 2. Installation de Docker
echo "🐳 2/5 - Installation de Docker..."
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
sudo systemctl start docker
sudo systemctl enable docker

# 3. Clonage du projet
echo "📥 3/5 - Clonage du projet..."
cd /home/ubuntu
git clone https://github.com/YOUR_REPO/plantdiag.git
cd plantdiag/backend

# 4. Configuration
echo "⚙️ 4/5 - Configuration de l'application..."
# Créer le fichier .env si nécessaire
cat > .env << EOF
DATABASE_URL=sqlite:///./plantdiag.db
ENVIRONMENT=production
EOF

# 5. Lancement avec Docker
echo "🚀 5/5 - Lancement de l'application..."
sudo docker-compose up -d

# 6. Affichage du résultat
echo ""
echo "========================================="
echo "✅ DÉPLOIEMENT RÉUSSI !"
echo "========================================="
echo ""
echo "📱 Application accessible sur :"
echo "   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo ""
echo "📊 Swagger API :"
echo "   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000/docs"
echo ""
echo "🔍 Vérifier les logs :"
echo "   sudo docker-compose logs -f"
echo ""
echo "========================================="
