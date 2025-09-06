import os
from motor.motor_asyncio import AsyncIOMotorClient

# URL de conexión a MongoDB desde variables de entorno
MONGO_URL = os.getenv("MONGO_URL", "mongodb://reservas-db:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "reservas_db")

# Cliente asíncrono de MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Funciones para obtener las colecciones
def get_reservas_collection():
    return db["reservas"]

def get_preferencias_collection():
    return db["preferencias_usuario"]
