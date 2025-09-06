from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
import requests
import os

# ===========================
# Inicialización de la app
# ===========================
app = FastAPI(title="API Gateway Taller Microservicios")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea un enrutador para las peticiones de los microservicios.
router = APIRouter(prefix="/api/v1")

# ===========================
# Definición de servicios
# ===========================
SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001/api/v1/auth"),
    "vuelos": os.getenv("VUELOS_SERVICE_URL", "http://vuelos-service:8002/api/v1/vuelos"),
    "reservas": os.getenv("RESERVAS_SERVICE_URL", "http://reservas-service:8003/api/v1/reservas"),
    "pagos": os.getenv("PAGOS_SERVICE_URL", "http://pagos-service:8004/api/v1/pagos"),
}


def proxy_response(r: requests.Response) -> Response:
    # Reenviar status, cuerpo y content-type del servicio destino
    return Response(
        content=r.content,
        status_code=r.status_code,
        media_type=r.headers.get("content-type", "application/json")
    )

# ===========================
# Rutas para reenviar peticiones a los microservicios.
# ===========================

# GET
@router.get("/{service_name}/{path:path}")
async def forward_get(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    try:
        r = requests.get(f"{SERVICES[service_name]}/{path}", params=request.query_params)
        return proxy_response(r)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream {service_name} error: {e}")

# POST
@router.post("/{service_name}/{path:path}")
async def forward_post(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    try:
        r = requests.post(f"{SERVICES[service_name]}/{path}", json=await request.json())
        return proxy_response(r)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream {service_name} error: {e}")

# PUT
@router.put("/{service_name}/{path:path}")
async def forward_put(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    try:
        r = requests.put(f"{SERVICES[service_name]}/{path}", json=await request.json())
        return proxy_response(r)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream {service_name} error: {e}")

# DELETE
@router.delete("/{service_name}/{path:path}")
async def forward_delete(service_name: str, path: str):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    try:
        r = requests.delete(f"{SERVICES[service_name]}/{path}")
        return proxy_response(r)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream {service_name} error: {e}")

# ===========================
# Registro del router
# ===========================
app.include_router(router)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "La API Gateway está funcionando correctamente."}

