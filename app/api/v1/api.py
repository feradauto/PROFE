from fastapi import APIRouter
from .endpoints import health
from .endpoints import whatsapp_callback

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(whatsapp_callback.router, prefix="/whats", tags=["whatsapp"])