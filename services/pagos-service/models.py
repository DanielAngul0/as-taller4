from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    reserva_id = Column(Integer, nullable=False)
    monto = Column(Numeric(10,2), nullable=False)
    metodo_pago = Column(String(50), nullable=False)
    estado = Column(String(20), nullable=False, default='pendiente')
    fecha_pago = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Pago(id={self.id}, usuario_id={self.usuario_id}, monto={self.monto})>"

# Modelos Pydantic
class PagoBase(BaseModel):
    usuario_id: int
    reserva_id: int
    monto: float
    metodo_pago: str
    estado: Optional[str] = "pendiente"

class PagoCreate(PagoBase):
    pass

class PagoRead(PagoBase):
    id: int
    fecha_pago: datetime

    class Config:
        orm_mode = True
