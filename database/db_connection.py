from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add parent directory to path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from database.models import Base

# Create DB Engine
engine = create_engine(config.DB_PATH, connect_args={'check_same_thread': False} if 'sqlite' in config.DB_PATH else {})

# Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create tables if they don't exist"""
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {config.DB_PATH}")

def get_session():
    """Returns a new database session"""
    return SessionLocal()

if __name__ == "__main__":
    init_db()
