from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .config import get_settings

settings = get_settings()

# Create engine
engine = create_engine(
    f"postgresql://{settings.TIMESCALE_DB_USER}:{settings.TIMESCALE_DB_PASSWORD}"
    f"@{settings.TIMESCALE_DB_HOST}:{settings.TIMESCALE_DB_PORT}/{settings.TIMESCALE_DB_NAME}"
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 