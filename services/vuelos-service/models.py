from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    aerolinea = Column(String(100), nullable=False)
    origen = Column(String(50), nullable=False)
    destino = Column(String(50), nullable=False)
    fecha_salida = Column(DateTime, nullable=False)
    fecha_llegada = Column(DateTime, nullable=False)
    aeronave = Column(String(50))
    precio = Column(Float, nullable=False)
    asientos_disponibles = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Vuelo(id={self.id}, origen='{self.origen}', destino='{self.destino}', precio={self.precio})>"


# ===========================
# Pydantic Models
# ===========================

class VueloBase(BaseModel):
    aerolinea: str
    origen: str
    destino: str
    fecha_salida: datetime
    fecha_llegada: datetime
    aeronave: str | None = None
    precio: float
    asientos_disponibles: int

class VueloCreate(VueloBase):
    pass

class VueloRead(VueloBase):
    id: int
    class Config:
        orm_mode = True
