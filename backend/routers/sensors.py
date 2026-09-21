from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import Parcel, SensorReading
from schemas.sensors import SensorReadingIn, SensorReadingOut

router = APIRouter()


@router.post("/readings", response_model=SensorReadingOut, status_code=status.HTTP_201_CREATED)
async def ingest_reading(payload: SensorReadingIn, db: Session = Depends(get_db)):
    """Point d'entrée des capteurs IoT : une trame par relevé."""
    parcel = db.query(Parcel).filter(Parcel.id == payload.parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcelle introuvable")

    reading = SensorReading(
        parcel_id=payload.parcel_id,
        sensor_code=payload.sensor_code,
        soil_moisture_percent=payload.soil_moisture_percent,
        soil_temperature_celsius=payload.soil_temperature_celsius,
        air_temperature_celsius=payload.air_temperature_celsius,
        air_humidity_percent=payload.air_humidity_percent,
        leaf_wetness_percent=payload.leaf_wetness_percent,
        battery_percent=payload.battery_percent,
        recorded_at=payload.recorded_at or datetime.utcnow(),
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@router.get("/latest")
async def latest_readings(user_id: int = 1, db: Session = Depends(get_db)):
    """Dernier relevé connu pour chaque parcelle de l'utilisateur."""
    parcels = db.query(Parcel).filter(Parcel.user_id == user_id).all()

    results = []
    for parcel in parcels:
        reading = (
            db.query(SensorReading)
            .filter(SensorReading.parcel_id == parcel.id)
            .order_by(SensorReading.recorded_at.desc())
            .first()
        )
        results.append({
            "parcel_id": parcel.id,
            "parcel_name": parcel.name,
            "crop_type": parcel.crop_type,
            "reading": {
                "sensor_code": reading.sensor_code,
                "soil_moisture_percent": round(reading.soil_moisture_percent, 1),
                "soil_temperature_celsius": round(reading.soil_temperature_celsius, 1),
                "air_temperature_celsius": round(reading.air_temperature_celsius, 1),
                "air_humidity_percent": round(reading.air_humidity_percent, 1),
                "leaf_wetness_percent": round(reading.leaf_wetness_percent, 1),
                "battery_percent": round(reading.battery_percent, 1),
                "recorded_at": reading.recorded_at.isoformat(),
            } if reading else None,
        })
    return results


@router.get("/{parcel_id}/history", response_model=list[SensorReadingOut])
async def reading_history(parcel_id: int, hours: int = 24, db: Session = Depends(get_db)):
    """Série temporelle des relevés, pour tracer l'évolution d'une parcelle."""
    since = datetime.utcnow() - timedelta(hours=hours)
    return (
        db.query(SensorReading)
        .filter(SensorReading.parcel_id == parcel_id, SensorReading.recorded_at >= since)
        .order_by(SensorReading.recorded_at.asc())
        .all()
    )


@router.get("/network")
async def network_status(db: Session = Depends(get_db)):
    """État du réseau de capteurs : utilisé pour le tableau de bord et la soutenance."""
    since = datetime.utcnow() - timedelta(minutes=15)

    rows = (
        db.query(
            SensorReading.sensor_code,
            SensorReading.parcel_id,
            func.max(SensorReading.recorded_at).label("last_seen"),
            func.count(SensorReading.id).label("readings"),
        )
        .group_by(SensorReading.sensor_code, SensorReading.parcel_id)
        .all()
    )

    sensors = []
    for code, parcel_id, last_seen, count in rows:
        latest = (
            db.query(SensorReading)
            .filter(SensorReading.sensor_code == code)
            .order_by(SensorReading.recorded_at.desc())
            .first()
        )
        sensors.append({
            "sensor_code": code,
            "parcel_id": parcel_id,
            "online": last_seen >= since,
            "last_seen": last_seen.isoformat(),
            "readings_total": count,
            "battery_percent": round(latest.battery_percent, 1) if latest else None,
        })

    return {
        "sensors_total": len(sensors),
        "sensors_online": sum(1 for s in sensors if s["online"]),
        "readings_total": sum(s["readings_total"] for s in sensors),
        "sensors": sensors,
    }
