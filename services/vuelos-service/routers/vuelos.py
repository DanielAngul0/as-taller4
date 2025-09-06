from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from database_sql import SessionLocal
from models import Vuelo, VueloCreate, VueloRead

router = APIRouter(prefix="/vuelos", tags=["vuelos"])

# ===========================
# Dependencia para la base de datos
# ===========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================
# Búsqueda avanzada de vuelos
# ==========================
@router.get("/buscar", response_model=List[VueloRead])
def buscar_vuelos(
    origen: Optional[str] = None,
    destino: Optional[str] = None,
    fecha_inicio: Optional[datetime] = Query(None, description="Fecha mínima de salida"),
    fecha_fin: Optional[datetime] = Query(None, description="Fecha máxima de salida"),
    precio_min: Optional[float] = None,
    precio_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Vuelo)

    if origen:
        query = query.filter(Vuelo.origen.ilike(f"%{origen}%"))
    if destino:
        query = query.filter(Vuelo.destino.ilike(f"%{destino}%"))
    if fecha_inicio:
        query = query.filter(Vuelo.fecha_salida >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Vuelo.fecha_salida <= fecha_fin)
    if precio_min:
        query = query.filter(Vuelo.precio >= precio_min)
    if precio_max:
        query = query.filter(Vuelo.precio <= precio_max)

    return query.all()


# ===========================
# CRUD básico
# ===========================
@router.get("/", response_model=List[VueloRead])
def listar_vuelos(db: Session = Depends(get_db)):
    return db.query(Vuelo).all()

@router.get("/{vuelo_id}", response_model=VueloRead)
def obtener_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo
