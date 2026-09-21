from typing import Optional

from pydantic import BaseModel, Field


class ParcelIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    crop_type: str = Field(min_length=1, max_length=60)
    area_hectares: Optional[float] = Field(default=None, ge=0, le=100000)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
