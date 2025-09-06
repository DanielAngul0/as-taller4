from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}', role='{self.role}')>"


# ===========================
# Pydantic Models
# ===========================

class UsuarioBase(BaseModel):
    nombre: str
    email: str


class UsuarioCreate(UsuarioBase):
    password: str
    role: str = "user"   # 👈 valor por defecto


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    email: str
    role: str
    fecha_registro: datetime

    class Config:
        orm_mode = True


class UsuarioLogin(BaseModel):
    email: str
    password: str