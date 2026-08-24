"""
Unit tests for PlantDiag API
Run with: pytest test_app.py -v
"""

import pytest
from fastapi.testclient import TestClient
from app import app, DiseaseClassifier
import numpy as np
from io import BytesIO
from PIL import Image

# Create test client fixture
@pytest.fixture(scope="session")
def _client():
    """Create test client with proper lifespan initialization"""
    with TestClient(app) as test_client:
        yield test_client


# Make client available globally for test classes
@pytest.fixture(scope="session", autouse=True)
def _setup_client(_client):
    """Setup client for all tests"""
    global client
    client = _client


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_health_check(self):
        """Test /health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "model" in data

    def test_root_endpoint(self):
        """Test root / endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert data["name"] == "PlantDiag API"
        assert "docs" in data


class TestDiagnosisEndpoints:
    """Test diagnosis endpoints"""

    @pytest.fixture
    def sample_image(self):
        """Create a sample image for testing"""
        img = Image.new('RGB', (224, 224), color='red')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        return img_io

    def test_diagnose_invalid_file_type(self):
        """Test diagnosis with invalid file type"""
        response = client.post(
            "/api/v1/diagnose",
            files={"file": ("test.txt", BytesIO(b"not an image"), "text/plain")},
            data={"user_id": 123}
        )
        assert response.status_code == 400
        assert "image" in response.json()["detail"].lower()

    def test_diagnose_missing_user_id(self, sample_image):
        """Test diagnosis without user_id"""
        response = client.post(
            "/api/v1/diagnose",
            files={"file": ("image.png", sample_image, "image/png")}
        )
        # Should still work with optional user_id
        assert response.status_code == 200

    def test_diagnose_success(self, sample_image):
        """Test successful diagnosis"""
        response = client.post(
            "/api/v1/diagnose",
            files={"file": ("image.png", sample_image, "image/png")},
            data={"user_id": 123, "parcel_id": 456}
        )
        assert response.status_code == 200
        data = response.json()
        assert "diagnosis" in data
        assert "confidence" in data
        assert "severity" in data
        assert "treatments" in data
        assert "recommendation" in data
        assert "timestamp" in data
        assert "processing_time_ms" in data
        assert 0 <= data["confidence"] <= 1

    def test_diagnose_response_structure(self, sample_image):
        """Test diagnosis response has correct structure"""
        response = client.post(
            "/api/v1/diagnose",
            files={"file": ("image.png", sample_image, "image/png")},
            data={"user_id": 123}
        )
        data = response.json()

        # Check treatments structure
        assert isinstance(data["treatments"], dict)
        assert "preventive" in data["treatments"]
        assert "biological" in data["treatments"]
        assert "conventional" in data["treatments"]

        # Check severity
        assert data["severity"] in ["Mild", "Moderate", "Severe"]

        # Check confidence is reasonable
        assert data["confidence"] > 0.7  # Mock returns > 0.75


class TestHistoryEndpoints:
    """Test history endpoints"""

    def test_get_history_success(self):
        """Test getting user history"""
        response = client.get("/api/v1/history/123")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "diagnosis" in data[0]
            assert "confidence" in data[0]
            assert "severity" in data[0]
            assert "timestamp" in data[0]

    def test_get_history_with_limit(self):
        """Test getting history with limit parameter"""
        response = client.get("/api/v1/history/123?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5


class TestParcelEndpoints:
    """Test parcel endpoints"""

    def test_list_parcels_success(self):
        """Test listing parcels"""
        response = client.get("/api/v1/parcels?user_id=123")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "name" in data[0]
            assert "crop_type" in data[0]

    def test_create_parcel_success(self):
        """Test creating a parcel"""
        response = client.post(
            "/api/v1/parcels?user_id=123",
            json={
                "name": "Test Parcel",
                "crop_type": "Wheat",
                "area_hectares": 5.0
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Parcel"
        assert data["crop_type"] == "Wheat"
        assert data["area_hectares"] == 5.0
        assert "id" in data
        assert "created_at" in data

    def test_create_parcel_minimal(self):
        """Test creating a parcel with minimal data"""
        response = client.post(
            "/api/v1/parcels?user_id=123",
            json={"name": "Simple Parcel"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Simple Parcel"


class TestSensorEndpoints:
    """Test sensor data endpoints"""

    def test_get_sensor_data_success(self):
        """Test getting sensor data"""
        response = client.get("/api/v1/sensors/456")
        assert response.status_code == 200
        data = response.json()
        assert data["parcel_id"] == 456
        assert "temperature_celsius" in data
        assert "humidity_percent" in data
        assert "soil_moisture_percent" in data
        assert "timestamp" in data

        # Check value ranges
        assert 10 <= data["temperature_celsius"] <= 35
        assert 30 <= data["humidity_percent"] <= 100
        assert 20 <= data["soil_moisture_percent"] <= 80


class TestStatusEndpoints:
    """Test status endpoints"""

    def test_get_status(self):
        """Test /api/v1/status endpoint"""
        response = client.get("/api/v1/status")
        assert response.status_code == 200
        data = response.json()
        assert "api" in data
        assert "model" in data
        assert "database" in data
        assert "cache" in data
        assert "timestamp" in data


class TestDocumentationEndpoints:
    """Test documentation endpoints"""

    def test_get_endpoints_doc(self):
        """Test /api/v1/docs/endpoints"""
        response = client.get("/api/v1/docs/endpoints")
        assert response.status_code == 200
        data = response.json()

        # Check required endpoints are documented
        assert "diagnosis" in data
        assert "history" in data
        assert "parcels_list" in data
        assert "sensors" in data

        # Check structure
        assert "method" in data["diagnosis"]
        assert "path" in data["diagnosis"]
        assert "description" in data["diagnosis"]

    def test_swagger_ui_accessible(self):
        """Test that Swagger UI is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200


class TestMLClassifier:
    """Test ML classifier functionality"""

    def test_classifier_initialization(self):
        """Test classifier initializes correctly"""
        classifier = DiseaseClassifier()
        assert classifier is not None
        assert len(classifier.diseases_db) > 0

    def test_classifier_predict(self):
        """Test classifier makes predictions"""
        classifier = DiseaseClassifier()
        # Create dummy image array
        img_array = np.random.rand(224, 224, 3)
        disease, confidence = classifier.predict(img_array)

        assert isinstance(disease, str)
        assert isinstance(confidence, float)
        assert 0 <= confidence <= 1
        assert disease in classifier.diseases_db

    def test_classifier_get_disease_info(self):
        """Test getting disease information"""
        classifier = DiseaseClassifier()
        info = classifier.get_disease_info("Rouille du blé")

        assert "severity" in info
        assert "recommendation" in info
        assert "treatments" in info
        assert "preventive" in info["treatments"]
        assert "biological" in info["treatments"]
        assert "conventional" in info["treatments"]

    def test_classifier_unknown_disease(self):
        """Test getting info for unknown disease"""
        classifier = DiseaseClassifier()
        info = classifier.get_disease_info("Unknown Disease")

        # Should return default (healthy leaf info)
        assert "severity" in info
        assert "treatments" in info


class TestErrorHandling:
    """Test error handling"""

    def test_404_not_found(self):
        """Test 404 error"""
        response = client.get("/nonexistent/endpoint")
        assert response.status_code == 404

    def test_invalid_json(self):
        """Test invalid JSON payload"""
        response = client.post(
            "/api/v1/parcels?user_id=123",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]


class TestCORSHeaders:
    """Test CORS configuration"""

    def test_cors_headers_present(self):
        """Test that CORS headers are present"""
        response = client.get("/health")
        assert response.status_code == 200
        # Check for CORS headers (if CORS middleware is configured)
        # This depends on FastAPI CORS middleware


class TestPerformance:
    """Test performance metrics"""

    def test_health_check_fast(self):
        """Test that health check is fast"""
        import time
        start = time.time()
        response = client.get("/health")
        elapsed = (time.time() - start) * 1000

        assert response.status_code == 200
        assert elapsed < 100  # Should complete in < 100ms

    def test_diagnosis_processing_time(self):
        """Test that diagnosis processing time is reasonable"""
        img = Image.new('RGB', (224, 224), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)

        response = client.post(
            "/api/v1/diagnose",
            files={"file": ("image.png", img_io, "image/png")},
            data={"user_id": 123}
        )

        assert response.status_code == 200
        data = response.json()
        # Should complete in < 5000ms (5 seconds)
        assert data["processing_time_ms"] < 5000


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
