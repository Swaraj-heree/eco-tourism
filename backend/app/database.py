import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
    # --- PRODUCTION MODE: Vercel + Turso Cloud ---
    
    # Clean the URL and strictly format it for the pure-Python client
    clean_url = TURSO_DATABASE_URL.replace("libsql://", "").replace("https://", "")
    db_url = f"sqlite+libsql://{clean_url}/?secure=true"
    
    engine = create_engine(
        db_url,
        connect_args={"auth_token": TURSO_AUTH_TOKEN}
    )
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