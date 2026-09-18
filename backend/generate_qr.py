#!/usr/bin/env python3
"""
Génère un code QR avec l'adresse IP locale pour accéder à l'app depuis le téléphone
"""

import subprocess
import sys
import socket
import time

# Installer qrcode si nécessaire
try:
    import qrcode
except ImportError:
    print("📦 Installation de qrcode...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]", "-q"])
    import qrcode

def get_local_ip():
    """Obtenir l'adresse IP locale (pas localhost)"""
    try:
        # Créer une socket pour trouver l'IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Se connecter à un serveur public (sans vraiment envoyer de données)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def generate_qr():
    """Générer et afficher le code QR"""
    ip = get_local_ip()
    url = f"http://{ip}:8000"

    print("\n" + "="*60)
    print("🔗 Adresse d'accès: " + url)
    print("="*60 + "\n")

    # Créer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Afficher en ASCII art
    print("📱 Code QR - Scannez avec votre téléphone:\n")
    qr.print_ascii(invert=True)

    print("\n" + "="*60)
    print("💡 Instructions:")
    print("  1. Ouvrez le terminal et lancez: python run.py")
    print("  2. Attendez que l'API démarre")
    print("  3. Scannez le QR code avec votre téléphone")
    print("  4. Ou tapez manuellement: " + url)
    print("="*60 + "\n")

    # Générer aussi une image PNG du QR
    qr_image = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr_image.add_data(url)
    qr_image.make(fit=True)
    img = qr_image.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")
    print("✅ Image QR sauvegardée dans: qr_code.png\n")

if __name__ == "__main__":
    generate_qr()
