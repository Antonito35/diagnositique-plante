#!/usr/bin/env python3
import subprocess
import sys
import time
import socket

print("🚀 Installation des dépendances...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart", "qrcode[pil]", "httpx", "-q"])

print("✅ Génération du code QR...")
import qrcode

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

ip = get_local_ip()
url = f"http://{ip}:8000"

print(f"\n{'='*60}")
print(f"🔗 Adresse: {url}")
print(f"{'='*60}\n")

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)

print("📱 Code QR - Scannez avec votre téléphone:\n")
qr.print_ascii(invert=True)

print(f"\n{'='*60}")
print("✅ Serveur lancé sur port 8000...")
print(f"{'='*60}\n")

time.sleep(1)

subprocess.call([sys.executable, "-m", "uvicorn", "app_minimal:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
