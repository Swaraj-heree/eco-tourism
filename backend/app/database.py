import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("TURSO_DATABASE_URL")

if DATABASE_URL:
    # --- PRODUCTION MODE: Render PostgreSQL ---
    # Render URLs often start with postgres://, but SQLAlchemy requires postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    engine = create_engine(DATABASE_URL)
else:
    # --- LOCAL DEVELOPMENT MODE: Standard SQLite ---
    SQLALCHEMY_DATABASE_URL = "sqlite:///./eco_tourism.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()