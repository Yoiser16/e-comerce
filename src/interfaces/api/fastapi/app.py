"""
Aplicación principal de FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .cliente_router import router as cliente_router
from .producto_router import router as producto_router
from .exception_handlers import exception_handler_dominio
from domain.exceptions.dominio import ExcepcionDominio
from infrastructure.config.app_config import AppConfig


def crear_app(config: AppConfig) -> FastAPI:
    """
    Factory para crear la aplicación FastAPI.
    
    Responsabilidades:
    - Configurar middleware
    - Registrar routers
    - Configurar exception handlers
    - Configurar CORS, logging, etc.
    """
    
    app = FastAPI(
        title="Sistema Empresarial de Gestión",
        description="API REST para sistema empresarial con Clean Architecture",
        version="1.0.0",
        debug=config.debug
    )
    
    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configurar según ambiente
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers
    app.add_exception_handler(ExcepcionDominio, exception_handler_dominio)
    
    # Routers
    app.include_router(cliente_router)
    app.include_router(producto_router)
    
    return app
