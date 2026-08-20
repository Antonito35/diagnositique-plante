-- PlantDiag Database Initialization Script
-- PostgreSQL 15+

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS public;

-- ============================================================================
-- USERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    farm_name VARCHAR(255),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    verification_token VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);

-- ============================================================================
-- PARCELS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS parcels (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    crop_type VARCHAR(100),
    area_hectares DECIMAL(10,2),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    soil_type VARCHAR(100),
    irrigation_type VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_parcels_user_id ON parcels(user_id);
CREATE INDEX idx_parcels_is_active ON parcels(is_active);
CREATE INDEX idx_parcels_crop_type ON parcels(crop_type);

-- ============================================================================
-- DIAGNOSES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS diagnoses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parcel_id INTEGER REFERENCES parcels(id) ON DELETE SET NULL,
    disease_name VARCHAR(255) NOT NULL,
    confidence DECIMAL(5,4) CHECK (confidence >= 0 AND confidence <= 1),
    severity VARCHAR(50) CHECK (severity IN ('Mild', 'Moderate', 'Severe')),
    image_path VARCHAR(512),
    image_url VARCHAR(1024),
    ml_model_version VARCHAR(50),
    processing_time_ms INTEGER,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_diagnoses_user_id ON diagnoses(user_id);
CREATE INDEX idx_diagnoses_parcel_id ON diagnoses(parcel_id);
CREATE INDEX idx_diagnoses_disease_name ON diagnoses(disease_name);
CREATE INDEX idx_diagnoses_created_at ON diagnoses(created_at DESC);

-- ============================================================================
-- TREATMENTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS treatments (
    id SERIAL PRIMARY KEY,
    diagnosis_id INTEGER NOT NULL REFERENCES diagnoses(id) ON DELETE CASCADE,
    treatment_type VARCHAR(50) CHECK (treatment_type IN ('preventive', 'biological', 'conventional')),
    name VARCHAR(255),
    description TEXT,
    effectiveness_rate DECIMAL(5,2) CHECK (effectiveness_rate >= 0 AND effectiveness_rate <= 100),
    estimated_cost DECIMAL(10,2),
    duration_days INTEGER,
    active_substance VARCHAR(255),
    phytosanitary_product VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_treatments_diagnosis_id ON treatments(diagnosis_id);
CREATE INDEX idx_treatments_treatment_type ON treatments(treatment_type);

-- ============================================================================
-- SENSOR_DATA TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS sensor_data (
    id BIGSERIAL PRIMARY KEY,
    parcel_id INTEGER NOT NULL REFERENCES parcels(id) ON DELETE CASCADE,
    temperature_celsius DECIMAL(5,2),
    humidity_percent DECIMAL(5,2) CHECK (humidity_percent >= 0 AND humidity_percent <= 100),
    soil_moisture_percent DECIMAL(5,2) CHECK (soil_moisture_percent >= 0 AND soil_moisture_percent <= 100),
    wind_speed_kmh DECIMAL(5,2),
    rainfall_mm DECIMAL(5,2),
    device_id VARCHAR(100),
    is_simulated BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sensor_data_parcel_id ON sensor_data(parcel_id);
CREATE INDEX idx_sensor_data_created_at ON sensor_data(created_at DESC);
CREATE INDEX idx_sensor_data_parcel_created ON sensor_data(parcel_id, created_at DESC);

-- ============================================================================
-- ALERTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    parcel_id INTEGER NOT NULL REFERENCES parcels(id) ON DELETE CASCADE,
    alert_type VARCHAR(100),
    severity VARCHAR(50) CHECK (severity IN ('Info', 'Warning', 'Critical')),
    message TEXT NOT NULL,
    is_acknowledged BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_at TIMESTAMP
);

CREATE INDEX idx_alerts_parcel_id ON alerts(parcel_id);
CREATE INDEX idx_alerts_is_acknowledged ON alerts(is_acknowledged);
CREATE INDEX idx_alerts_created_at ON alerts(created_at DESC);

-- ============================================================================
-- API_KEYS TABLE (for future mobile app auth)
-- ============================================================================
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_is_active ON api_keys(is_active);

-- ============================================================================
-- AUDIT_LOG TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100),
    resource_type VARCHAR(100),
    resource_id INTEGER,
    changes JSONB,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_resource ON audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at DESC);

-- ============================================================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================================================

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER parcels_updated_at BEFORE UPDATE ON parcels
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER diagnoses_updated_at BEFORE UPDATE ON diagnoses
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- ============================================================================
-- MOCK DATA FOR TESTING
-- ============================================================================

-- Create test user
INSERT INTO users (email, password_hash, farm_name, phone, is_active, is_verified)
VALUES ('farmer@example.com', '$2b$12$mock_password_hash', 'Demo Farm', '+33612345678', true, true)
ON CONFLICT (email) DO NOTHING;

-- Get user ID for reference
DO $$
DECLARE
    user_id INTEGER;
BEGIN
    SELECT id INTO user_id FROM users WHERE email = 'farmer@example.com' LIMIT 1;

    IF user_id IS NOT NULL THEN
        -- Insert sample parcels
        INSERT INTO parcels (user_id, name, crop_type, area_hectares, soil_type)
        VALUES
            (user_id, 'Champ Nord', 'Blé', 5.2, 'Limon'),
            (user_id, 'Champ Est', 'Maïs', 3.8, 'Argilo-calcaire'),
            (user_id, 'Champ Ouest', 'Soja', 4.5, 'Limoneux')
        ON CONFLICT DO NOTHING;
    END IF;
END $$;

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

GRANT CONNECT ON DATABASE plantdiag TO plantdiag_user;
GRANT USAGE ON SCHEMA public TO plantdiag_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO plantdiag_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO plantdiag_user;

-- ============================================================================
-- FUNCTIONS FOR API
-- ============================================================================

-- Get user diagnoses with recent sensor data
CREATE OR REPLACE FUNCTION get_parcel_diagnosis_summary(p_parcel_id INTEGER)
RETURNS TABLE(
    diagnosis_count BIGINT,
    latest_disease VARCHAR,
    latest_confidence DECIMAL,
    avg_confidence DECIMAL,
    latest_sensor_temp DECIMAL,
    latest_sensor_humidity DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(d.*)::BIGINT,
        d.disease_name,
        d.confidence,
        AVG(d.confidence),
        s.temperature_celsius,
        s.humidity_percent
    FROM diagnoses d
    LEFT JOIN sensor_data s ON d.parcel_id = s.parcel_id
    WHERE d.parcel_id = p_parcel_id
    GROUP BY d.parcel_id, d.disease_name, d.confidence, s.temperature_celsius, s.humidity_percent
    ORDER BY d.created_at DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- END OF INITIALIZATION SCRIPT
-- ============================================================================

-- Show summary
SELECT
    current_database() as database,
    current_user as user,
    now() as initialized_at;
