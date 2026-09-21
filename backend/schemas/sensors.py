from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SensorReadingIn(BaseModel):
    """Trame envoyée par un capteur IoT de parcelle."""
    parcel_id: int
    sensor_code: str = Field(min_length=1, max_length=32)
    soil_moisture_percent: float = Field(ge=0, le=100)
    soil_temperature_celsius: float = Field(ge=-30, le=70)
    air_temperature_celsius: float = Field(ge=-40, le=60)
    air_humidity_percent: float = Field(ge=0, le=100)
    leaf_wetness_percent: float = Field(ge=0, le=100)
    battery_percent: float = Field(ge=0, le=100)
    recorded_at: Optional[datetime] = None


class SensorReadingOut(BaseModel):
    id: int
    parcel_id: int
    sensor_code: str
    soil_moisture_percent: float
    soil_temperature_celsius: float
    air_temperature_celsius: float
    air_humidity_percent: float
    leaf_wetness_percent: float
    battery_percent: float
    recorded_at: datetime

    class Config:
        from_attributes = True
