# 📚 API DOCUMENTATION - PlantDiag

## Base URL
```
http://localhost:8000  (Development)
https://api.plantdiag.farm  (Production)
```

## Authentication
All endpoints (except `/health` and `/docs`) require a JWT bearer token.

**Header:**
```
Authorization: Bearer {JWT_TOKEN}
```

---

## Endpoints

### 1. Health Check

#### `GET /health`
Check if API is operational.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-08-20T14:30:45.123456Z",
  "model": "loaded"
}
```

**Status Codes:**
- `200` - OK
- `503` - Service Unavailable

---

### 2. Diagnosis

#### `POST /api/v1/diagnose`
Upload an image and get disease diagnosis.

**Request:**
```
Content-Type: multipart/form-data

Parameters:
  - file (required): Image file (JPEG, PNG, WebP)
  - user_id (required): User identifier
  - parcel_id (optional): Associated parcel ID
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/v1/diagnose" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@photo.jpg" \
  -F "user_id=123" \
  -F "parcel_id=456"
```

**Example (Python):**
```python
import requests

url = "http://localhost:8000/api/v1/diagnose"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
files = {"file": open("photo.jpg", "rb")}
data = {"user_id": 123, "parcel_id": 456}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

**Response (200 OK):**
```json
{
  "diagnosis": "Rouille du blé",
  "confidence": 0.92,
  "severity": "Moderate",
  "treatments": {
    "preventive": "Rotation des cultures, éliminer résidus infectés",
    "biological": "Pulvérisation de Bacillus subtilis",
    "conventional": "Fongicide à base de triazole (Systhane, Tilt)"
  },
  "recommendation": "Traiter dès que possible - propagation active",
  "timestamp": "2026-08-20T14:30:46.234567Z",
  "processing_time_ms": 1250.5
}
```

**Possible Diagnoses:**
- `Rouille du blé`
- `Mildiou du raisin`
- `Oïdium`
- `Septoriose`
- `Brûlure bactérienne`
- `Feuille blanche du maïs`
- `Feuille saine`

**Status Codes:**
- `200` - Diagnosis successful
- `400` - Invalid image format or missing parameters
- `401` - Unauthorized (invalid token)
- `413` - Payload too large (image > 10MB)
- `500` - Server error during processing

---

### 3. History

#### `GET /api/v1/history/{user_id}`
Retrieve diagnosis history for a user.

**Parameters:**
```
Path:
  - user_id (required): User identifier

Query:
  - limit (optional, default=10): Maximum number of records
  - parcel_id (optional): Filter by parcel
  - start_date (optional): ISO format date (2026-08-20)
  - end_date (optional): ISO format date
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/history/123?limit=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "id": 45,
    "diagnosis": "Rouille du blé",
    "confidence": 0.92,
    "severity": "Moderate",
    "timestamp": "2026-08-20T14:30:46.234567Z",
    "parcel_id": 456
  },
  {
    "id": 44,
    "diagnosis": "Oïdium",
    "confidence": 0.88,
    "severity": "Mild",
    "timestamp": "2026-08-19T10:15:20.123456Z",
    "parcel_id": 456
  }
]
```

**Status Codes:**
- `200` - OK
- `401` - Unauthorized
- `404` - User not found
- `500` - Server error

---

### 4. Parcels

#### `GET /api/v1/parcels`
List all parcels for a user.

**Parameters:**
```
Query:
  - user_id (required): User identifier
  - limit (optional, default=50): Maximum records
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/parcels?user_id=123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
[
  {
    "id": 456,
    "name": "Champ Nord",
    "crop_type": "Blé",
    "area_hectares": 5.2,
    "created_at": "2026-08-15T09:00:00.000000Z"
  },
  {
    "id": 457,
    "name": "Champ Est",
    "crop_type": "Maïs",
    "area_hectares": 3.8,
    "created_at": "2026-08-16T10:30:00.000000Z"
  }
]
```

---

#### `POST /api/v1/parcels`
Create a new parcel.

**Request:**
```
Content-Type: application/json

{
  "name": "Champ Ouest",
  "crop_type": "Soja",
  "area_hectares": 4.5
}
```

**Parameters:**
```
Query:
  - user_id (required): User identifier
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/parcels?user_id=123" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Champ Ouest",
    "crop_type": "Soja",
    "area_hectares": 4.5
  }'
```

**Response (201 Created):**
```json
{
  "id": 458,
  "name": "Champ Ouest",
  "crop_type": "Soja",
  "area_hectares": 4.5,
  "created_at": "2026-08-20T14:30:00.000000Z"
}
```

**Status Codes:**
- `201` - Created
- `400` - Invalid data
- `401` - Unauthorized
- `500` - Server error

---

### 5. Sensors

#### `GET /api/v1/sensors/{parcel_id}`
Get simulated IoT sensor data for a parcel.

**Parameters:**
```
Path:
  - parcel_id (required): Parcel identifier
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/sensors/456" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "parcel_id": 456,
  "temperature_celsius": 22.5,
  "humidity_percent": 65.3,
  "soil_moisture_percent": 48.2,
  "timestamp": "2026-08-20T14:30:45.123456Z"
}
```

**Sensor Ranges:**
- **Temperature:** 15-30°C
- **Humidity:** 40-90%
- **Soil Moisture:** 30-70%

**Status Codes:**
- `200` - OK
- `401` - Unauthorized
- `404` - Parcel not found
- `500` - Server error

---

### 6. Status

#### `GET /api/v1/status`
Get detailed system status.

**Response (200 OK):**
```json
{
  "api": "operational",
  "model": "loaded",
  "database": "connected",
  "cache": "connected",
  "timestamp": "2026-08-20T14:30:45.123456Z"
}
```

---

### 7. Documentation

#### `GET /docs`
Interactive Swagger documentation (OpenAPI 3.0).

Access in browser: `http://localhost:8000/docs`

#### `GET /redoc`
ReDoc alternative documentation.

Access in browser: `http://localhost:8000/redoc`

#### `GET /api/v1/docs/endpoints`
JSON list of all endpoints.

**Response:**
```json
{
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
  ...
}
```

---

## Error Handling

### Error Response Format
```json
{
  "error": "Error message describing what went wrong",
  "timestamp": "2026-08-20T14:30:45.123456Z",
  "request_id": "req-12345-67890"
}
```

### Common Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| `400` | Bad Request | Check request format and parameters |
| `401` | Unauthorized | Provide valid JWT token |
| `404` | Not Found | Check resource ID/path |
| `413` | Payload Too Large | Image > 10MB, reduce size |
| `429` | Rate Limited | Wait before retrying (100 req/min) |
| `500` | Server Error | Server issue, try again later |

---

## Rate Limiting

**Limits:**
- 100 requests per minute per IP
- 1000 requests per hour per user

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1692545445
```

---

## Authentication Example

### Getting a JWT Token

```bash
# In future: /auth/login endpoint
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "secure_password"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1440
}
```

### Using the Token

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  "http://localhost:8000/api/v1/parcels?user_id=123"
```

---

## WebSocket (Future)

For real-time sensor data streaming:

```
ws://localhost:8000/ws/sensors/{parcel_id}
```

---

## Versioning

Current version: **v1**  
Base path: `/api/v1`

Future versions will be available at `/api/v2`, `/api/v3`, etc.

---

## Testing the API

### Using Swagger UI
1. Navigate to `http://localhost:8000/docs`
2. Click on each endpoint to expand
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using Postman
1. Import this collection: [Link to Postman collection]
2. Set `{{BASE_URL}}` to `http://localhost:8000`
3. Set `{{TOKEN}}` in environment variables
4. Run requests

### Using Python Requests
```python
import requests

BASE_URL = "http://localhost:8000"
TOKEN = "your_jwt_token"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Diagnose
with open("photo.jpg", "rb") as f:
    files = {"file": f}
    data = {"user_id": 123, "parcel_id": 456}
    response = requests.post(
        f"{BASE_URL}/api/v1/diagnose",
        headers=headers,
        files=files,
        data=data
    )
    print(response.json())

# Get history
response = requests.get(
    f"{BASE_URL}/api/v1/history/123",
    headers=headers
)
print(response.json())

# Get sensors
response = requests.get(
    f"{BASE_URL}/api/v1/sensors/456",
    headers=headers
)
print(response.json())
```

---

**Document Version:** 1.0  
**Last Updated:** 20 août 2026  
**API Version:** 1.0.0
