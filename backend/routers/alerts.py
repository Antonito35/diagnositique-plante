from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Diagnostic, Parcel, SensorReading, User
from routers.auth import get_current_user

router = APIRouter()

# Un capteur muet plus de 15 minutes est considéré hors ligne
OFFLINE_AFTER = timedelta(minutes=15)


def _sensor_alerts(parcel: Parcel, reading: SensorReading) -> list[dict]:
    alerts = []

    # Feuillage humide entre 15 et 25 °C : conditions de germination des spores
    fungal_window = 15 <= reading.air_temperature_celsius <= 25
    if reading.leaf_wetness_percent >= 70 and fungal_window:
        alerts.append({
            "level": "danger",
            "source": "Capteur IoT",
            "parcel": parcel.name,
            "title": "Risque fongique élevé",
            "text": f"Feuillage humide à {reading.leaf_wetness_percent:.0f} % sur {parcel.name}, "
                    f"par {reading.air_temperature_celsius:.0f} °C.",
            "detail": "Ces conditions favorisent la germination des spores. "
                      "Inspectez la parcelle sous 48 heures.",
        })

    if reading.soil_moisture_percent < 25:
        alerts.append({
            "level": "warning",
            "source": "Capteur IoT",
            "parcel": parcel.name,
            "title": "Stress hydrique",
            "text": f"Humidité du sol à {reading.soil_moisture_percent:.0f} % sur {parcel.name}.",
            "detail": "Seuil bas atteint. Un apport d'eau est recommandé.",
        })
    elif reading.soil_moisture_percent > 85:
        alerts.append({
            "level": "warning",
            "source": "Capteur IoT",
            "parcel": parcel.name,
            "title": "Excès d'eau",
            "text": f"Humidité du sol à {reading.soil_moisture_percent:.0f} % sur {parcel.name}.",
            "detail": "Sol saturé : risque d'asphyxie racinaire et de maladies du collet.",
        })

    if reading.battery_percent < 20:
        alerts.append({
            "level": "warning",
            "source": "Maintenance",
            "parcel": parcel.name,
            "title": "Batterie capteur faible",
            "text": f"Le capteur {reading.sensor_code} est à {reading.battery_percent:.0f} % de batterie.",
            "detail": "Remplacez la pile pour ne pas perdre la surveillance de la parcelle.",
        })

    if datetime.utcnow() - reading.recorded_at > OFFLINE_AFTER:
        alerts.append({
            "level": "warning",
            "source": "Réseau",
            "parcel": parcel.name,
            "title": "Capteur hors ligne",
            "text": f"Aucune trame reçue du capteur {reading.sensor_code} depuis "
                    f"{reading.recorded_at.strftime('%d/%m à %H:%M')} UTC.",
            "detail": "Vérifiez l'alimentation et la couverture réseau de la parcelle.",
        })

    return alerts


@router.get("/{user_id}")
async def list_alerts(user_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """Alertes croisant les relevés des capteurs et les diagnostics IA."""
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès refusé aux alertes d'un autre utilisateur")
    alerts = []
    parcels = db.query(Parcel).filter(Parcel.user_id == user_id).all()

    for parcel in parcels:
        reading = (
            db.query(SensorReading)
            .filter(SensorReading.parcel_id == parcel.id)
            .order_by(SensorReading.recorded_at.desc())
            .first()
        )
        if reading:
            alerts.extend(_sensor_alerts(parcel, reading))

    recent = (
        db.query(Diagnostic)
        .filter(Diagnostic.user_id == user_id)
        .order_by(Diagnostic.created_at.desc())
        .first()
    )
    if recent and recent.disease_name and "sain" not in recent.disease_name.lower():
        alerts.append({
            "level": "danger",
            "source": "Diagnostic IA",
            "parcel": recent.parcel.name if recent.parcel else "Diagnostic rapide",
            "title": "Maladie détectée",
            "text": f"{recent.disease_name} identifiée avec "
                    f"{round((recent.confidence_score or 0) * 100)} % de certitude.",
            "detail": recent.recommendation or "Consultez les traitements recommandés.",
        })

    if not alerts:
        alerts.append({
            "level": "info",
            "source": "Système",
            "parcel": None,
            "title": "Aucune anomalie",
            "text": "Les capteurs et les derniers diagnostics ne signalent rien d'anormal.",
            "detail": "Surveillance active. Prochain relevé dans quelques minutes.",
        })

    order = {"danger": 0, "warning": 1, "info": 2}
    alerts.sort(key=lambda a: order[a["level"]])
    return alerts
