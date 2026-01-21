"""
Router de Inventario - Movimientos y Kardex
"""
from fastapi import APIRouter
from interfaces.api.rest.views.inventario_views import router as inventario_view_router

router = APIRouter(prefix="/api/v1")
router.include_router(inventario_view_router)
