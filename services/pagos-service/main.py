# services/pagos-service/main.py
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database_sql import create_db_and_tables, get_db
from models import Pago, PagoCreate, PagoRead

app = FastAPI()
router = APIRouter()

# Crear tablas al iniciar
create_db_and_tables()

# ==========================
# Endpoints de Salud
# ==========================
@app.get("/")
def read_root():
    return {"message": "Servicio de pagos en funcionamiento."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ==========================
# Endpoints CRUD de Pagos
# ==========================

# Listar todos los pagos
@router.get("/pagos/", response_model=List[PagoRead])
def list_pagos(db: Session = Depends(get_db)):
    pagos = db.query(Pago).all()
    return pagos

# Obtener un pago por ID
@router.get("/pagos/{pago_id}", response_model=PagoRead)
def get_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

# Crear un nuevo pago
@router.post("/pagos/", response_model=PagoRead)
def create_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    nuevo_pago = Pago(
        usuario_id=pago.usuario_id,
        reserva_id=pago.reserva_id,
        monto=pago.monto,
        metodo_pago=pago.metodo_pago,
        estado=pago.estado
    )
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

# Actualizar un pago
@router.put("/pagos/{pago_id}", response_model=PagoRead)
def update_pago(pago_id: int, pago: PagoCreate, db: Session = Depends(get_db)):
    pago_db = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago_db:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    pago_db.usuario_id = pago.usuario_id
    pago_db.reserva_id = pago.reserva_id
    pago_db.monto = pago.monto
    pago_db.metodo_pago = pago.metodo_pago
    pago_db.estado = pago.estado

    db.commit()
    db.refresh(pago_db)
    return pago_db

# Eliminar un pago
@router.delete("/pagos/{pago_id}")
def delete_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    db.delete(pago)
    db.commit()
    return {"message": "Pago eliminado correctamente"}

# ==========================
# Incluir router en la app
# ==========================
app.include_router(router, prefix="/api/v1")
