from fastapi import FastAPI
from database_sql import Base, engine
from routers import vuelos

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vuelos Service")

@app.get("/")
def root():
    return {"message": "Servicio de vuelos en funcionamiento."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Registrar router
app.include_router(vuelos.router, prefix="/api/v1")
