from fastapi import FastAPI, APIRouter, HTTPException
from database_sql import create_db_and_tables
from routers import auth
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

# Registrar router
app.include_router(auth.router)
