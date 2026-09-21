"""
Simulateur de capteurs IoT de parcelle.

Tourne comme un service distinct et envoie ses relevés à l'API par HTTP,
exactement comme le feraient des boîtiers installés sur le terrain.
Les valeurs suivent un cycle jour/nuit pour rester réalistes.
"""

import math
import os
import random
import time
from datetime import datetime, timezone

import requests

API_URL = os.getenv("API_URL", "http://api:8000")
INTERVAL_SECONDS = int(os.getenv("SENSOR_INTERVAL_SECONDS", "60"))
USER_ID = int(os.getenv("SENSOR_USER_ID", "1"))

DEMO_PARCELS = [
    {"name": "Champ Nord", "crop_type": "Blé", "area_hectares": 12.5,
     "latitude": 48.4111, "longitude": -1.7472},
    {"name": "Parcelle du Verger", "crop_type": "Pommier", "area_hectares": 4.2,
     "latitude": 48.3606, "longitude": -1.7488},
]


class SensorState:
    """Garde en mémoire l'état physique simulé d'un boîtier."""

    def __init__(self, parcel_id: int, sensor_code: str):
        self.parcel_id = parcel_id
        self.sensor_code = sensor_code
        self.soil_moisture = random.uniform(35, 65)
        self.battery = random.uniform(70, 100)

    def read(self) -> dict:
        now = datetime.now(timezone.utc)
        # Position dans le cycle solaire : 0 la nuit, 1 en milieu de journée
        hour_angle = (now.hour + now.minute / 60 - 6) / 24 * 2 * math.pi
        daylight = max(0.0, math.sin(hour_angle))

        air_temperature = 12 + 9 * daylight + random.uniform(-0.8, 0.8)
        air_humidity = 92 - 38 * daylight + random.uniform(-3, 3)
        # Le sol amortit les variations de l'air
        soil_temperature = 13 + 4 * daylight + random.uniform(-0.4, 0.4)

        # Rosée nocturne, évaporation dès que le soleil monte
        leaf_wetness = (88 - 70 * daylight) + random.uniform(-6, 6)

        # Le sol s'assèche en journée ; averse aléatoire une fois sur vingt
        self.soil_moisture -= daylight * random.uniform(0.3, 0.9)
        if random.random() < 0.05:
            self.soil_moisture += random.uniform(8, 20)
        self.soil_moisture = min(100.0, max(8.0, self.soil_moisture))

        self.battery = max(5.0, self.battery - random.uniform(0.01, 0.05))

        return {
            "parcel_id": self.parcel_id,
            "sensor_code": self.sensor_code,
            "soil_moisture_percent": round(self.soil_moisture, 1),
            "soil_temperature_celsius": round(soil_temperature, 1),
            "air_temperature_celsius": round(air_temperature, 1),
            "air_humidity_percent": round(min(100, max(0, air_humidity)), 1),
            "leaf_wetness_percent": round(min(100, max(0, leaf_wetness)), 1),
            "battery_percent": round(self.battery, 1),
        }


def wait_for_api() -> None:
    while True:
        try:
            response = requests.get(f"{API_URL}/health", timeout=5)
            if response.ok:
                print("[iot] API disponible", flush=True)
                return
        except requests.RequestException:
            pass
        print("[iot] API indisponible, nouvelle tentative dans 5 s", flush=True)
        time.sleep(5)


def fetch_parcels() -> list[dict]:
    response = requests.get(f"{API_URL}/api/v1/parcels", params={"user_id": USER_ID}, timeout=10)
    response.raise_for_status()
    return response.json()


def seed_demo_parcels() -> list[dict]:
    """Sans parcelle en base, le réseau de capteurs n'aurait rien à mesurer."""
    for parcel in DEMO_PARCELS:
        try:
            requests.post(
                f"{API_URL}/api/v1/parcels",
                params={"user_id": USER_ID},
                json=parcel,
                timeout=10,
            ).raise_for_status()
            print(f"[iot] parcelle de démonstration créée : {parcel['name']}", flush=True)
        except requests.RequestException as exc:
            print(f"[iot] création de parcelle impossible : {exc}", flush=True)
    return fetch_parcels()


def build_sensors(parcels: list[dict]) -> list[SensorState]:
    return [
        SensorState(parcel["id"], f"SENS-{parcel['id']:03d}")
        for parcel in parcels
    ]


def main() -> None:
    print(f"[iot] simulateur démarré, cible {API_URL}, période {INTERVAL_SECONDS} s", flush=True)
    wait_for_api()

    parcels = fetch_parcels()
    if not parcels:
        parcels = seed_demo_parcels()

    sensors = build_sensors(parcels)
    print(f"[iot] {len(sensors)} capteur(s) actif(s)", flush=True)

    while True:
        # Une parcelle créée depuis l'application reçoit son capteur au cycle suivant
        try:
            current = fetch_parcels()
            known = {s.parcel_id for s in sensors}
            for parcel in current:
                if parcel["id"] not in known:
                    sensors.append(SensorState(parcel["id"], f"SENS-{parcel['id']:03d}"))
                    print(f"[iot] nouveau capteur sur {parcel['name']}", flush=True)
            live = {p["id"] for p in current}
            sensors = [s for s in sensors if s.parcel_id in live]
        except requests.RequestException as exc:
            print(f"[iot] lecture des parcelles impossible : {exc}", flush=True)

        for sensor in sensors:
            payload = sensor.read()
            try:
                response = requests.post(
                    f"{API_URL}/api/v1/sensors/readings", json=payload, timeout=10
                )
                if response.ok:
                    print(
                        f"[iot] {payload['sensor_code']} "
                        f"sol {payload['soil_moisture_percent']}% "
                        f"air {payload['air_temperature_celsius']}°C "
                        f"feuillage {payload['leaf_wetness_percent']}%",
                        flush=True,
                    )
                else:
                    print(f"[iot] refus de l'API ({response.status_code})", flush=True)
            except requests.RequestException as exc:
                print(f"[iot] envoi impossible : {exc}", flush=True)

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
