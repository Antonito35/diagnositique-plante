from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./plantdiag.db")

# SQLite configuration
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialiser la base de données"""
    # Importer les modèles pour que SQLAlchemy les connaisse
    from models import User, Parcel, Diagnostic, WeatherHistory, DiseaseModel
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec les tables")
