from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

# Base declarativa para SQLAlchemy
Base = declarative_base()

# Modelo de SQLAlchemy para la tabla 'usuarios'
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"

# Modelos Pydantic para validación en FastAPI
class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioRead(UsuarioBase):
    id: int
    fecha_registro: datetime

    class Config:
        orm_mode = True  # Permite compatibilidad con ORM
