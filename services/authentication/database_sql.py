from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@auth-db:5432/auth_db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Para crear las tablas ---
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

# --- Para usar sesiones en los endpoints ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()