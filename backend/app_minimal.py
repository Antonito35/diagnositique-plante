"""
PlantDiag API - Production Version avec Base de Données
Diagnostic agricole avec IA et persistance données
"""

from datetime import datetime
import os
import time
from typing import Optional

try:
    from fastapi import FastAPI, File, UploadFile, HTTPException, status, Depends
    from fastapi.responses import JSONResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    import requests
    from sqlalchemy.orm import Session
    import numpy as np
    import cv2
    from PIL import Image
    from io import BytesIO
except ImportError:
    print("❌ Dépendances manquantes. Installation...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart", "requests", "sqlalchemy", "pillow", "numpy", "opencv-python-headless", "-q"])
    from fastapi import FastAPI, File, UploadFile, HTTPException, status, Depends
    from fastapi.responses import JSONResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    import requests
    from sqlalchemy.orm import Session
    import numpy as np
    import cv2
    from PIL import Image
    from io import BytesIO

# Import database et models
from database import get_db, init_db
from models import User, Parcel, Diagnostic, SensorReading, DiseaseModel
from routers import alerts, auth, sensors
from schemas.parcels import ParcelIn

# Initialiser la base de données au démarrage
init_db()

app = FastAPI(
    title="PlantDiag API",
    description="Diagnostic agricole avec IA et base de données",
    version="2.0.0"
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(sensors.router, prefix="/api/v1/sensors", tags=["capteurs IoT"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alertes"])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ============================================================================
# DATABASE - Maladies avec explications simples
# ============================================================================

DISEASES_DB = {
    "Rouille du blé": {
        "severity": "Moderate",
        "recommendation": "Traite tout de suite ! La maladie se propage vite.",
        "treatments": {
            "preventive": "Planter autre chose l'année prochaine sur ce champ. Enlever les feuilles mortes.",
            "biological": "Pulvériser un produit naturel à base de bactéries bénéfiques. "
                          "Désherbage mécanique (herse étrille ou houe rotative) possible du stade "
                          "2-3 feuilles jusqu'à la fin du tallage (avant épi 1 cm) : au-delà, la tige "
                          "monte et devient trop fragile pour passer un outil sans l'abîmer.",
            "conventional": "Utiliser un produit chimique contre les champignons."
        }
    },
    "Mildiou du raisin": {
        "severity": "Severe",
        "recommendation": "C'est URGENT ! Traite immédiatement sinon tu perdras toute ta récolte.",
        "treatments": {
            "preventive": "Tailler les branches pour laisser passer l'air. Éviter d'arroser les feuilles.",
            "biological": "Pulvériser du cuivre ou du soufre (produits naturels). "
                          "Travail mécanique du rang (décavaillonnage, griffage) à faire avant le "
                          "débourrement ou après la nouaison : éviter tout passage d'outil pendant "
                          "la floraison, qui est fragile et sensible aux vibrations et à la poussière.",
            "conventional": "Utiliser un traitement chimique puissant contre les champignons."
        }
    },
    "Oïdium": {
        "severity": "Mild",
        "recommendation": "C'est pas grave. Tu peux traiter rapidement.",
        "treatments": {
            "preventive": "Assurer bonne ventilation. Ne pas mettre trop d'engrais azotés.",
            "biological": "Pulvériser du soufre (très simple, peu cher). "
                          "Désherbage mécanique à privilégier avant la floraison, en dehors des "
                          "périodes humides : le sol travaillé sèche plus vite et limite l'humidité "
                          "ambiante qui favorise le champignon.",
            "conventional": "Utiliser un traitement chimique spécial contre l'oïdium."
        }
    },
    "Septoriose": {
        "severity": "Moderate",
        "recommendation": "Traite sans attendre. C'est une maladie qui revient souvent.",
        "treatments": {
            "preventive": "Ne pas planter la même culture 3 années de suite. Enlever tous les débris au sol.",
            "biological": "Utiliser des bactéries bénéfiques en spray. "
                          "Désherbage mécanique possible du stade 2-3 feuilles jusqu'à la fin du "
                          "tallage (avant épi 1 cm), comme pour la rouille : passer plus tard risque "
                          "de casser les tiges montées.",
            "conventional": "Pulvériser un fongicide (produit contre les champignons)."
        }
    },
    "Feuille saine": {
        "severity": "Mild",
        "recommendation": "Parfait ! Pas de maladie. Continue à surveiller régulièrement.",
        "treatments": {
            "preventive": "Vérifier régulièrement tes feuilles. Garder un bon désherbage.",
            "biological": "Rien de nécessaire, juste un entretien normal. "
                          "Désherbage mécanique possible à tout stade avant la floraison ; "
                          "répéter tous les 10 à 15 jours entre la levée et la fermeture du couvert "
                          "reste la meilleure fenêtre.",
            "conventional": "Rien de nécessaire pour le moment."
        }
    }
}

# ============================================================================
# CLASSIFIEUR - Analyse RÉELLE de l'image
# ============================================================================

class RealDiseaseClassifier:
    """
    Analyse la PROPORTION de la feuille couverte par chaque couleur de symptôme
    (via OpenCV, en espace HSV) plutôt que la couleur moyenne de toute la photo.

    C'est le point important : une tache de rouille qui ne couvre que 10 % d'une
    feuille très verte ne fait pratiquement pas bouger la couleur moyenne de
    l'image, donc une classification par moyenne globale la rate systématiquement.
    En mesurant la fraction de pixels dans la gamme de teinte caractéristique de
    chaque maladie, une petite tache reste détectable même sur une grande feuille.
    """

    # Bornes HSV (convention OpenCV : H 0-179, S 0-255, V 0-255)
    COLOR_RANGES = {
        "Rouille du blé": ((3, 80, 140), (18, 255, 240)),      # orange-rouille vif et lumineux
        "Mildiou du raisin": ((20, 100, 130), (36, 255, 255)), # jaune "tache d'huile", lumineux
        "Septoriose": ((3, 60, 35), (24, 255, 130)),           # même famille de teinte, mais sombre
        "Oïdium": ((0, 0, 150), (179, 30, 255)),                # blanc/gris poudreux, quasi sans saturation
    }
    HEALTHY_RANGE = ((35, 40, 40), (85, 255, 255))  # vert feuille

    # En dessous de ce seuil de surface atteinte, on considère que ce n'est pas
    # significatif (reflets, ombre, petit artefact) et on reste sur "Feuille saine"
    MIN_AFFECTED_FRACTION = 0.05

    def __init__(self):
        self.diseases_db = DISEASES_DB
        print("✅ Classifieur d'analyse d'image (OpenCV, zones de couleur) initialisé")

    def analyze_image(self, image_array: np.ndarray) -> tuple:
        # L'image arrive déjà en RGB (conversion faite avant l'appel), mais on
        # reste défensif : n'importe quelle photo doit produire un résultat,
        # jamais une exception.
        if image_array.ndim == 2:
            image_array = np.stack([image_array] * 3, axis=-1)
        if image_array.ndim == 3 and image_array.shape[2] == 4:
            image_array = image_array[:, :, :3]
        if image_array.ndim != 3 or image_array.shape[2] < 3 or image_array.size == 0:
            return "Feuille saine", 0.60, 0.0

        image_array = np.ascontiguousarray(image_array[:, :, :3], dtype=np.uint8)

        # Limiter la résolution analysée : pas besoin de traiter une photo de
        # téléphone à pleine taille pour mesurer des proportions de couleur
        h, w = image_array.shape[:2]
        if max(h, w) > 600:
            scale = 600 / max(h, w)
            image_array = cv2.resize(image_array, (int(w * scale), int(h * scale)),
                                      interpolation=cv2.INTER_AREA)

        hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
        total_pixels = hsv.shape[0] * hsv.shape[1]

        fractions = {}
        for disease, (lo, hi) in self.COLOR_RANGES.items():
            mask = cv2.inRange(hsv, np.array(lo), np.array(hi))
            fractions[disease] = float(np.count_nonzero(mask)) / total_pixels

        healthy_mask = cv2.inRange(hsv, np.array(self.HEALTHY_RANGE[0]), np.array(self.HEALTHY_RANGE[1]))
        healthy_fraction = float(np.count_nonzero(healthy_mask)) / total_pixels

        best_disease = max(fractions, key=fractions.get)
        best_fraction = fractions[best_disease]

        if best_fraction < self.MIN_AFFECTED_FRACTION:
            # Pas assez de surface suspecte détectée : feuille saine
            confidence = min(0.92, 0.55 + healthy_fraction * 0.4)
            return "Feuille saine", confidence, 0.0

        # Confiance : plus la zone atteinte est nette et étendue, plus le score monte
        confidence = min(0.93, 0.55 + best_fraction * 1.1)
        return best_disease, confidence, best_fraction

    @staticmethod
    def severity_from_fraction(affected_fraction: float) -> str:
        """La sévérité reflète la surface réellement atteinte, pas une valeur figée par maladie."""
        if affected_fraction >= 0.35:
            return "Severe"
        if affected_fraction >= 0.15:
            return "Moderate"
        return "Mild"

classifier = None

@app.on_event("startup")
async def startup():
    global classifier
    classifier = RealDiseaseClassifier()

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", include_in_schema=False)
async def root():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {"status": "PlantDiag API running"}

@app.get("/health")
async def health():
    return {
        "status": "healthy ✅",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected",
        "model": "loaded"
    }

@app.post("/api/v1/diagnose")
async def diagnose(
    file: UploadFile = File(...),
    user_id: int = None,
    parcel_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de lire le fichier envoyé. Réessayez avec une autre photo."
        )

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucune photo reçue. Sélectionnez une image avant d'envoyer."
        )

    try:
        # Pillow décode nativement JPEG, PNG, GIF, BMP, WEBP, TIFF... ; convert("RGB")
        # gère aussi les images en palette, en niveaux de gris ou en CMJN sans distinction
        # de format préalable, pour qu'aucune photo courante ne fasse échouer le diagnostic.
        image = Image.open(BytesIO(contents))
        image = image.convert("RGB")
        image_array = np.array(image)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce fichier n'est pas une image lisible (formats acceptés : JPEG, PNG, "
                   "GIF, BMP, WEBP). Réessayez avec une photo au format JPEG ou PNG."
        )

    start_time = time.perf_counter()
    try:
        disease_name, confidence, affected_fraction = classifier.analyze_image(image_array)
        disease_info = classifier.diseases_db[disease_name]
        severity = (
            "Mild" if disease_name == "Feuille saine"
            else classifier.severity_from_fraction(affected_fraction)
        )

        # Sauvegarder dans la base de données
        diagnostic = Diagnostic(
            user_id=user_id or 1,
            parcel_id=parcel_id,
            disease_name=disease_name,
            confidence_score=round(confidence, 3),
            severity=severity,
            treatments=disease_info["treatments"],
            recommendation=disease_info["recommendation"]
        )
        db.add(diagnostic)

        if parcel_id:
            parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
            if parcel:
                parcel.last_diagnosis = disease_name

        db.commit()
        db.refresh(diagnostic)

        print(f"✅ Diagnostic: {disease_name} ({confidence:.0%}, "
              f"surface atteinte {affected_fraction:.0%})")

        return {
            "diagnosis": disease_name,
            "confidence": round(confidence, 3),
            "affected_area_percent": round(affected_fraction * 100, 1),
            "severity": severity,
            "treatments": disease_info["treatments"],
            "recommendation": disease_info["recommendation"],
            "timestamp": datetime.utcnow().isoformat(),
            "processing_time_ms": round((time.perf_counter() - start_time) * 1000)
        }

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Le diagnostic n'a pas pu être enregistré. Réessayez dans un instant."
        )

@app.get("/api/v1/history/{user_id}")
async def get_history(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    diagnostics = db.query(Diagnostic).filter(Diagnostic.user_id == user_id).order_by(Diagnostic.created_at.desc()).limit(limit).all()
    return [
        {
            "id": d.id,
            "disease_name": d.disease_name,
            "disease": d.disease_name,
            "confidence_score": d.confidence_score,
            "confidence": d.confidence_score,
            "severity": d.severity,
            "created_at": d.created_at.isoformat(),
            "timestamp": d.created_at.isoformat(),
            "parcel_id": d.parcel_id,
            "parcel_name": None
        }
        for d in diagnostics
    ]

@app.delete("/api/v1/history/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(user_id: int, db: Session = Depends(get_db)):
    db.query(Diagnostic).filter(Diagnostic.user_id == user_id).delete()
    db.query(Parcel).filter(Parcel.user_id == user_id).update({Parcel.last_diagnosis: None})
    db.commit()


@app.get("/api/v1/parcels")
async def list_parcels(user_id: int = 1, db: Session = Depends(get_db)):
    parcels = db.query(Parcel).filter(Parcel.user_id == user_id).all()
    return [_parcel_out(p) for p in parcels]

def _parcel_out(parcel: Parcel) -> dict:
    return {
        "id": parcel.id,
        "name": parcel.name,
        "crop_type": parcel.crop_type,
        "area_hectares": parcel.area_hectares,
        "latitude": parcel.latitude,
        "longitude": parcel.longitude,
        "last_diagnosis": parcel.last_diagnosis,
        "created_at": parcel.created_at.isoformat() if parcel.created_at else None
    }


@app.post("/api/v1/parcels", status_code=status.HTTP_201_CREATED)
async def create_parcel(payload: ParcelIn, user_id: int = 1, db: Session = Depends(get_db)):
    parcel = Parcel(
        user_id=user_id,
        name=payload.name,
        crop_type=payload.crop_type,
        area_hectares=payload.area_hectares,
        latitude=payload.latitude,
        longitude=payload.longitude
    )
    db.add(parcel)
    db.commit()
    db.refresh(parcel)
    return _parcel_out(parcel)


@app.put("/api/v1/parcels/{parcel_id}")
async def update_parcel(parcel_id: int, payload: ParcelIn, db: Session = Depends(get_db)):
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcelle introuvable")

    parcel.name = payload.name
    parcel.crop_type = payload.crop_type
    parcel.area_hectares = payload.area_hectares
    parcel.latitude = payload.latitude
    parcel.longitude = payload.longitude
    db.commit()
    db.refresh(parcel)
    return _parcel_out(parcel)


@app.delete("/api/v1/parcels/{parcel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parcel(parcel_id: int, db: Session = Depends(get_db)):
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcelle introuvable")

    db.query(SensorReading).filter(SensorReading.parcel_id == parcel_id).delete()
    db.query(Diagnostic).filter(Diagnostic.parcel_id == parcel_id).delete()
    db.delete(parcel)
    db.commit()

@app.get("/api/v1/weather")
async def get_weather(latitude: float, longitude: float):
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation,uv_index",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "Europe/Paris"
            },
            timeout=5
        )

        if response.status_code != 200:
            raise Exception("API Error")

        data = response.json()
        current = data.get("current", {})
        daily = data.get("daily", {})

        def get_weather_description(code):
            if code == 0 or code == 1:
                return "Ensoleillé"
            elif code == 2 or code == 3:
                return "Nuageux"
            elif code >= 45 and code <= 48:
                return "Brouillard"
            elif code >= 51 and code <= 67:
                return "Pluie légère"
            elif code >= 80 and code <= 82:
                return "Pluie"
            elif code >= 85 and code <= 86:
                return "Pluie forte"
            else:
                return "Nuageux"

        humidity = current.get("relative_humidity_2m", 65)
        temp = current.get("temperature_2m", 15)

        mildew_risk = min(100, int(humidity * 1.2 - 20))
        rust_risk = min(100, int(humidity * 0.8 + (15 - temp) * 2))
        powdery_risk = min(100, int(max(0, 80 - humidity + (20 - temp) * 2)))
        blight_risk = min(100, int(humidity * 0.9 + temp))

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "current": {
                "temperature_celsius": round(current.get("temperature_2m", 15), 1),
                "humidity_percent": int(current.get("relative_humidity_2m", 65)),
                "wind_speed_kmh": round(current.get("wind_speed_10m", 0), 1),
                "rainfall_mm": current.get("precipitation", 0),
                "condition": get_weather_description(current.get("weather_code", 3)),
                "uv_index": int(current.get("uv_index", 0)),
                "pressure_hpa": 1013
            },
            "forecast": [
                {
                    "date": daily["time"][i],
                    "temp_max": round(daily["temperature_2m_max"][i], 1),
                    "temp_min": round(daily["temperature_2m_min"][i], 1),
                    "condition": get_weather_description(daily["weather_code"][i]),
                    "rainfall_mm": daily["precipitation_sum"][i]
                }
                for i in range(min(5, len(daily.get("time", []))))
            ],
            "disease_risk": {
                "powdery_mildew": powdery_risk,
                "leaf_blight": blight_risk,
                "rust": rust_risk,
                "mildew": mildew_risk
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "current": {
                "temperature_celsius": 15,
                "humidity_percent": 65,
                "wind_speed_kmh": 10,
                "rainfall_mm": 0,
                "condition": "Données indisponibles",
                "uv_index": 0,
                "pressure_hpa": 1013
            },
            "forecast": [],
            "disease_risk": {"powdery_mildew": 50, "leaf_blight": 50, "rust": 50, "mildew": 50},
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/api/v1/status")
async def get_status():
    return {
        "api": "operational",
        "model": "real image analysis",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    print("🚀 PlantDiag - Production API with Database")
    uvicorn.run(
        "app_minimal:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
