from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Importa la base declarativa desde models.py
from models import Base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """Crea todas las tablas definidas en models.py si no existen."""
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()