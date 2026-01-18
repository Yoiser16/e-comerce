"""
Aplicación principal de FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application

from .cliente_router import router as cliente_router
from .producto_router import router as producto_router
from .carrito_router import router as carrito_router
from .busqueda_router import router as busqueda_router
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
        title="E-Commerce Extensiones de Cabello",
        description="API REST para e-commerce de extensiones de cabello humano con Clean Architecture",
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
    
    # Routers - ORDEN IMPORTANTE: rutas específicas antes que rutas con parámetros
    app.include_router(cliente_router)
    app.include_router(busqueda_router)   # Primero: /productos/destacados, /productos/buscar
    app.include_router(producto_router)   # Después: /productos/{producto_id}
    app.include_router(carrito_router)
    
    # Montar Django para rutas de autenticación y admin
    django_app = get_wsgi_application()
    app.mount("/", WSGIMiddleware(django_app))
    
    return app
