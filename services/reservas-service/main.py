from fastapi import FastAPI, APIRouter, HTTPException
from database_mongo import get_reservas_collection, get_preferencias_collection
from models import Reserva, PreferenciasUsuario
from typing import List
from bson import ObjectId
from bson.errors import InvalidId

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
    doc = reserva.dict(exclude={"id"})
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
# Endpoints GET por ID
# ==========================
@router.get("/reservas/{reserva_id}", response_model=Reserva)
async def get_reserva(reserva_id: str):
    try:
        obj_id = ObjectId(reserva_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de reserva inválido")
    
    doc = await get_reservas_collection().find_one({"_id": obj_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    doc["id"] = str(doc["_id"])
    doc.pop("_id")
    return Reserva(**doc)


# ==========================
# Endpoints PUT (actualizar)
# ==========================
@router.put("/reservas/{reserva_id}", response_model=Reserva)
async def update_reserva(reserva_id: str, reserva: Reserva):
    try:
        obj_id = ObjectId(reserva_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de reserva inválido")

    result = await get_reservas_collection().update_one(
        {"_id": obj_id}, {"$set": reserva.dict(exclude={"id"})}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    updated = await get_reservas_collection().find_one({"_id": obj_id})
    updated["id"] = str(updated["_id"])
    updated.pop("_id")
    return Reserva(**updated)



# ==========================
# Endpoints DELETE (cancelar)
# ==========================
@router.delete("/reservas/{reserva_id}")
async def delete_reserva(reserva_id: str):
    try:
        obj_id = ObjectId(reserva_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de reserva inválido")

    result = await get_reservas_collection().delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"message": "Reserva eliminada correctamente"}



# ==========================
# Incluir router en la app
# ==========================
app.include_router(router, prefix="/api/v1")
