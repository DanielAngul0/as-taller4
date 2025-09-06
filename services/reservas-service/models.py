from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class PreferenciasUsuario(BaseModel):
    usuario_id: int
    preferencias: Dict[str, Optional[str]]  # comida, asiento, equipaje_extra

class HistorialAccion(BaseModel):
    accion: str
    fecha: datetime

class Reserva(BaseModel):
    id: Optional[str] = None
    usuario_id: int
    vuelo_id: int
    estado: str = "pendiente"  # pendiente, pagado, cancelado
    fecha_reserva: datetime = Field(default_factory=datetime.utcnow)
    historial: List[HistorialAccion] = []
    
    class Config:
        orm_mode = True
