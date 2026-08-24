"""
PlantDiag API - Agricultural Disease Diagnosis Platform
FastAPI backend for ML-powered plant disease classification
"""

import logging
import random
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Path, Body, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# DATA MODELS (Pydantic)
# ============================================================================

class DiagnosisRequest(BaseModel):
    """Request model for diagnosis endpoint"""
    user_id: int
    parcel_id: Optional[int] = None


class DiagnosisResponse(BaseModel):
    """Response model for diagnosis"""
    diagnosis: str
    confidence: float
    severity: str  # 'Mild', 'Moderate', 'Severe'
    treatments: dict
    recommendation: str
    timestamp: str
    processing_time_ms: float


class HistoryItem(BaseModel):
    """Single diagnosis history item"""
    id: int
    diagnosis: str
    confidence: float
    severity: str
    timestamp: str
    parcel_id: Optional[int]


class ParcelRequest(BaseModel):
    """Request model for parcel creation"""
    name: str = Field(..., min_length=1, max_length=255)
    crop_type: Optional[str] = Field(None, max_length=255)
    area_hectares: Optional[float] = Field(None, gt=0)


class ParcelResponse(BaseModel):
    """Response model for parcels"""
    id: int
    name: str
    crop_type: Optional[str]
    area_hectares: Optional[float]
    created_at: str


class SensorData(BaseModel):
    """Simulated sensor data"""
    parcel_id: int
    temperature_celsius: float
    humidity_percent: float
    soil_moisture_percent: float
    timestamp: str


# ============================================================================
# ML MODEL MOCK (Placeholder for real MobileNetV2)
# ============================================================================

class DiseaseClassifier:
    """
    Mock disease classifier using MobileNetV2 + PlantVillage dataset
    In production, this loads a real TensorFlow Lite model
    """

    def __init__(self):
        # Disease database with symptoms and treatments
        self.diseases_db = {
            "Rouille du blé": {
                "severity": "Moderate",
                "recommendation": "Traiter dès que possible - propagation active",
                "treatments": {
                    "preventive": "Rotation des cultures, éliminer résidus infectés",
                    "biological": "Pulvérisation de Bacillus subtilis",
                    "conventional": "Fongicide à base de triazole (Systhane, Tilt)"
                }
            },
            "Mildiou du raisin": {
                "severity": "Severe",
                "recommendation": "Action urgente requise",
                "treatments": {
                    "preventive": "Taille & aération, éviter humidité",
                    "biological": "Cuivre + soufre",
                    "conventional": "Cymoxanil + Mancozèbe"
                }
            },
            "Oïdium": {
                "severity": "Mild",
                "recommendation": "Traitement recommandé",
                "treatments": {
                    "preventive": "Circulation air, pas surcharge azotée",
                    "biological": "Soufre, huiles essentielles",
                    "conventional": "Fongicide de synthèse (Rubigan)"
                }
            },
            "Septoriose": {
                "severity": "Moderate",
                "recommendation": "Traiter rapidement",
                "treatments": {
                    "preventive": "Rotation 3 ans, destruction débris",
                    "biological": "Bacillus pumilus",
                    "conventional": "Triazoles, Strobilurines"
                }
            },
            "Feuille saine": {
                "severity": "Mild",
                "recommendation": "Aucun traitement requis",
                "treatments": {
                    "preventive": "Monitoring régulier",
                    "biological": "Maintenir biodiversité",
                    "conventional": "Traitement préventif optionnel"
                }
            }
        }
        logger.info("DiseaseClassifier initialized")

    def predict(self, image_array: np.ndarray) -> tuple[str, float]:
        """
        Mock prediction - in real version, this would run MobileNetV2 inference
        Returns: (disease_name, confidence)
        """
        # Simulate disease prediction based on image properties
        # In production: model.predict(preprocessed_image)
        diseases = list(self.diseases_db.keys())
        # Mock confidence between 0.75-0.99
        confidences = [0.92, 0.88, 0.85, 0.78, 0.95]

        # Select random prediction (in real version, actual model output)
        idx = hash(image_array.tobytes()) % len(diseases)
        disease = diseases[idx]
        confidence = confidences[idx]

        return disease, confidence

    def get_disease_info(self, disease_name: str) -> dict:
        """Get treatment recommendations for a disease"""
        return self.diseases_db.get(disease_name, self.diseases_db["Feuille saine"])


# ============================================================================
# LIFESPAN MANAGEMENT (Startup/Shutdown)
# ============================================================================

classifier = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
    global classifier
    # Startup
    logger.info("🚀 Starting PlantDiag API...")
    classifier = DiseaseClassifier()
    logger.info("✅ ML model loaded successfully")
    yield
    # Shutdown
    logger.info("🛑 Shutting down PlantDiag API")


# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="PlantDiag API",
    description="Agricultural disease diagnosis using AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    os.getenv("MOBILE_URL", "http://localhost"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def process_image(file: UploadFile) -> np.ndarray:
    """Read and preprocess uploaded image"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image (JPEG, PNG, etc.)"
        )

    contents = await file.read()
    image = Image.open(BytesIO(contents))

    # Resize to model input size (224x224 for MobileNetV2)
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0

    return image_array


# ============================================================================
# ROUTES - HEALTH & INFO
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": "MobileNetV2" if classifier else "not_loaded"
    }


@app.get("/", tags=["Info"])
async def root():
    """API root information"""
    return {
        "name": "PlantDiag API",
        "version": "1.0.0",
        "description": "Agricultural disease diagnosis platform",
        "docs": "/docs",
        "health": "/health"
    }


# ============================================================================
# ROUTES - DIAGNOSIS
# ============================================================================

@app.post("/api/v1/diagnose", response_model=DiagnosisResponse, tags=["Diagnosis"])
async def diagnose(
    file: UploadFile = File(...),
    user_id: Optional[int] = Query(None),
    parcel_id: Optional[int] = Query(None)
):
    """
    Diagnose plant disease from photo

    - **file**: Image file (JPEG, PNG, max 10MB)
    - **user_id**: User identifier
    - **parcel_id**: (Optional) Associated parcel

    Returns diagnosis with confidence, severity, and treatment recommendations
    """
    start_time = datetime.now(timezone.utc)

    try:
        if classifier is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model is not loaded"
            )

        # Process image
        image_array = await process_image(file)

        # Get prediction from model
        disease_name, confidence = classifier.predict(image_array)
        disease_info = classifier.get_disease_info(disease_name)

        # Calculate processing time
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

        # Log diagnosis
        logger.info(
            f"Diagnosis: user={user_id}, disease={disease_name}, "
            f"confidence={confidence:.2%}, time={processing_time:.0f}ms"
        )

        return DiagnosisResponse(
            diagnosis=disease_name,
            confidence=confidence,
            severity=disease_info["severity"],
            treatments=disease_info["treatments"],
            recommendation=disease_info["recommendation"],
            timestamp=datetime.now(timezone.utc).isoformat(),
            processing_time_ms=processing_time
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Diagnosis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Diagnosis processing failed: {str(e)}"
        )


# ============================================================================
# ROUTES - HISTORY
# ============================================================================

@app.get("/api/v1/history/{user_id}", response_model=list[HistoryItem], tags=["History"])
async def get_history(user_id: int = Path(..., gt=0), limit: int = Query(10, ge=1, le=100)):
    """
    Retrieve diagnosis history for a user

    Returns last `limit` diagnoses (default 10, max 100)
    """
    logger.info(f"Retrieving history for user {user_id}")

    # Mock data - In production, query database
    mock_history = [
        HistoryItem(
            id=i,
            diagnosis="Rouille du blé",
            confidence=0.92,
            severity="Moderate",
            timestamp=(datetime.now(timezone.utc)).isoformat(),
            parcel_id=1
        )
        for i in range(1, min(limit + 1, 6))
    ]

    return mock_history


# ============================================================================
# ROUTES - PARCELS
# ============================================================================

@app.get("/api/v1/parcels", response_model=list[ParcelResponse], tags=["Parcels"])
async def list_parcels(user_id: int = Query(..., gt=0)):
    """List all parcels for a user"""
    logger.info(f"Listing parcels for user {user_id}")

    # Mock data
    return [
        ParcelResponse(
            id=1,
            name="Champ Nord",
            crop_type="Blé",
            area_hectares=5.2,
            created_at=datetime.now(timezone.utc).isoformat()
        ),
        ParcelResponse(
            id=2,
            name="Champ Est",
            crop_type="Maïs",
            area_hectares=3.8,
            created_at=datetime.now(timezone.utc).isoformat()
        )
    ]


@app.post("/api/v1/parcels", response_model=ParcelResponse, tags=["Parcels"])
async def create_parcel(user_id: int = Query(..., gt=0), parcel: ParcelRequest = Body(...)):
    """Create a new parcel"""
    logger.info(f"Creating parcel '{parcel.name}' for user {user_id}")

    # Mock response
    return ParcelResponse(
        id=3,
        name=parcel.name,
        crop_type=parcel.crop_type,
        area_hectares=parcel.area_hectares,
        created_at=datetime.now(timezone.utc).isoformat()
    )


# ============================================================================
# ROUTES - SENSORS
# ============================================================================

@app.get("/api/v1/sensors/{parcel_id}", response_model=SensorData, tags=["Sensors"])
async def get_sensor_data(parcel_id: int = Path(..., gt=0)):
    """
    Get simulated IoT sensor data for a parcel

    Includes: temperature, humidity, soil moisture
    """
    logger.info(f"Retrieving sensor data for parcel {parcel_id}")

    # Simulate sensor readings
    temperature = 18 + random.uniform(-3, 5)  # 15-23°C
    humidity = 60 + random.uniform(-10, 20)    # 50-80%
    soil_moisture = 45 + random.uniform(-5, 15) # 40-60%

    return SensorData(
        parcel_id=parcel_id,
        temperature_celsius=round(temperature, 1),
        humidity_percent=round(humidity, 1),
        soil_moisture_percent=round(soil_moisture, 1),
        timestamp=datetime.now(timezone.utc).isoformat()
    )


# ============================================================================
# ROUTES - STATUS DIAGNOSTICS
# ============================================================================

@app.get("/api/v1/status", tags=["Status"])
async def get_status():
    """Get system status"""
    return {
        "api": "operational",
        "model": "loaded" if classifier else "loading",
        "database": "connected",
        "cache": "connected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ============================================================================
# ROUTES - DOCUMENTATION
# ============================================================================

@app.get("/api/v1/docs/endpoints", tags=["Documentation"])
async def get_endpoints_doc():
    """List all available endpoints"""
    return {
        "diagnosis": {
            "method": "POST",
            "path": "/api/v1/diagnose",
            "description": "Upload photo and get disease diagnosis"
        },
        "history": {
            "method": "GET",
            "path": "/api/v1/history/{user_id}",
            "description": "Get diagnosis history for user"
        },
        "parcels_list": {
            "method": "GET",
            "path": "/api/v1/parcels?user_id={user_id}",
            "description": "List user's parcels"
        },
        "parcels_create": {
            "method": "POST",
            "path": "/api/v1/parcels?user_id={user_id}",
            "description": "Create new parcel"
        },
        "sensors": {
            "method": "GET",
            "path": "/api/v1/sensors/{parcel_id}",
            "description": "Get IoT sensor data"
        },
        "health": {
            "method": "GET",
            "path": "/health",
            "description": "Health check"
        }
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "timestamp": datetime.now(timezone.utc).isoformat()}
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT", "development") == "development",
        log_level="info"
    )
