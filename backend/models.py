from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parcels = relationship("Parcel", back_populates="user")
    diagnostics = relationship("Diagnostic", back_populates="user")

class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    crop_type = Column(String)
    area_hectares = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    last_diagnosis = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="parcels")
    diagnostics = relationship("Diagnostic", back_populates="parcel")

class Diagnostic(Base):
    __tablename__ = "diagnostics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    parcel_id = Column(Integer, ForeignKey("parcels.id"), nullable=True)
    disease_name = Column(String)
    confidence_score = Column(Float)
    severity = Column(String)
    treatments = Column(JSON)
    recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="diagnostics")
    parcel = relationship("Parcel", back_populates="diagnostics")

class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    rainfall = Column(Float)
    condition = Column(String)
    disease_risk = Column(JSON)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class DiseaseModel(Base):
    __tablename__ = "disease_models"

    id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String, unique=True)
    description = Column(String)
    symptoms = Column(JSON)
    treatments = Column(JSON)
    severity = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)
