from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - Render provides DATABASE_URL automatically
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine (works with PostgreSQL and SQLite)
if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, echo=False)
else:
    # Fallback to SQLite for local development
    DATABASE_URL = DATABASE_URL or "sqlite:///./stitchflow.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
