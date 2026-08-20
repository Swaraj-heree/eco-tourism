import os
import libsql
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
    # --- PRODUCTION MODE: Vercel + Turso Cloud (AWS) ---
    
    # 1. Force HTTP connection (Vercel serverless works best with HTTP)
    http_url = TURSO_DATABASE_URL.replace("libsql://", "https://")
    
    # 2. Inject the official libsql SDK directly
    def turso_connector():
        return libsql.connect(database=http_url, auth_token=TURSO_AUTH_TOKEN)
        
    engine = create_engine(
        "sqlite://",  # This empty sqlite URL stops SQLAlchemy from looking for the broken plugin!
        creator=turso_connector,
        connect_args={"check_same_thread": False}
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