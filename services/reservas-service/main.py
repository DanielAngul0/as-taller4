from fastapi import FastAPI, APIRouter, HTTPException
from .database_mongo import get_reservas_collection, get_preferencias_collection
from .models import Reserva, PreferenciasUsuario
from typing import List
from bson import ObjectId

app = FastAPI()
router = APIRouter()

# ==========================
# Endpoints de Salud
# ==========================
@app.get("/")
def read_root():
    return {"message": "Servicio de reservas en funcionamiento."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ==========================
# Endpoints GET
# ==========================
@router.get("/reservas/", response_model=List[Reserva])
async def list_reservas():
    reservas = []
    cursor = get_reservas_collection().find()
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id")
        reservas.append(Reserva(**doc))
    return reservas

@router.get("/preferencias/", response_model=List[PreferenciasUsuario])
async def list_preferencias():
    preferencias = []
    cursor = get_preferencias_collection().find()
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id")
        preferencias.append(PreferenciasUsuario(**doc))
    return preferencias

# ==========================
# Endpoints POST
# ==========================
@router.post("/reservas/", response_model=Reserva)
async def create_reserva(reserva: Reserva):
    doc = reserva.dict()
    result = await get_reservas_collection().insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return Reserva(**doc)

@router.post("/preferencias/", response_model=PreferenciasUsuario)
async def create_preferencia(preferencia: PreferenciasUsuario):
    doc = preferencia.dict()
    result = await get_preferencias_collection().insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return PreferenciasUsuario(**doc)

# ==========================
# Incluir router en la app
# ==========================
app.include_router(router, prefix="/api/v1")
