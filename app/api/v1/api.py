from fastapi import APIRouter
from .endpoints import health
from .endpoints import whatsapp_callback, static_files,poc

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(whatsapp_callback.router, prefix="/whats", tags=["whatsapp"])
api_router.include_router(static_files.router, prefix="/files",tags=["files"])
api_router.include_router(poc.router, prefix="/poc",tags=["poc"])