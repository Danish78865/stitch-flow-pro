from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - can be configured via environment variable
# Use Railway's persistent volume path if available
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stitchflow.db")
if os.path.exists("/app/data"):
    DATABASE_URL = "sqlite:////app/data/stitchflow.db"

# Create engine with SQLite threading fix
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
