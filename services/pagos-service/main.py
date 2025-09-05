from fastapi import FastAPI, APIRouter, HTTPException
from database_sql import create_db_and_tables
import os

# TODO: Importar el módulo de base de datos y los modelos
# from .database import [tu_motor_de_base_de_datos]
# from .models import [tus_modelos]

# TODO: Configurar la URL de la base de datos desde las variables de entorno
# DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

# Crear tablas si no existen
create_db_and_tables()

# TODO: Crea una instancia del router para organizar los endpoints
router = APIRouter()

# TODO: Define un endpoint raíz o de salud para verificar que el servicio está funcionando
@app.get("/")
def read_root():
    return {"message": "Servicio de pagos en funcionamiento."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# TODO: Implementa los endpoints de tu microservicio aquí
# Ejemplo de un endpoint GET:
# @router.get("/[ruta_del_recurso]/")
# async def get_[recurso]():
#     # TODO: Agrega la lógica de tu negocio aquí
#     return {"data": "Aquí van tus datos."}

# Ejemplo de un endpoint POST:
# @router.post("/[ruta_del_recurso]/")
# async def create_[recurso](item: [tu_modelo_pydantic]):
#     # TODO: Agrega la lógica para crear un nuevo recurso
#     return {"message": "[recurso] creado exitosamente."}


# TODO: Incluir el router en la aplicación principal
# app.include_router(router, prefix="/api/v1")

