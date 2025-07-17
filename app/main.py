from fastapi import FastAPI
from app.routes import transferencias_650
from app.routes import rendiciones
from app.routes import entidades
from app.routes import entes_convenios
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Desarrollo Sector Público - API de Consultas al DataWareHouse",
    description="API para consultar en el DW información de distintos aplicativos .",
    version="1.0.0",
    contact={
        "name": "Damian Gonzalez",
        "email": "dgonzalez@bpba.com.ar",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usá ["http://localhost:8000"] para más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers
app.include_router(transferencias_650.router, prefix="/api", tags=["Transferencias 650"])
app.include_router(rendiciones.router, prefix="/api", tags=["Rendiciones"])
app.include_router(entidades.router, prefix="/api", tags=["Entidades"])
app.include_router(entes_convenios.router, prefix="/api", tags=["Convenios"])

from fastapi.staticfiles import StaticFiles
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")




