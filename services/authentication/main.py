from fastapi import FastAPI, APIRouter, HTTPException
from database_sql import create_db_and_tables
# TODO: Importa tus modelos si necesitas usarlos
# from .models import Usuario

app = FastAPI()

# Crear tablas si no existen
create_db_and_tables()

router = APIRouter()

@app.get("/")
def read_root():
    return {"message": "Servicio de autenticación en funcionamiento."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# TODO: Define tus endpoints de usuarios, login, registro, etc.
# Ejemplo GET:
# @router.get("/usuarios/")
# async def get_usuarios():
#     return {"data": "Aquí van tus usuarios"}

# Ejemplo POST:
# @router.post("/usuarios/")
# async def create_usuario(usuario: UsuarioCreate):
#     return {"message": "Usuario creado exitosamente"}

# app.include_router(router, prefix="/api/v1")
