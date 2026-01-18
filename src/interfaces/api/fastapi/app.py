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
from .favoritos_router import router as favoritos_router
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
        debug=config.debug,
        redirect_slashes=False  # Importante: evita redirecciones automáticas que causan 307
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
    
    # IMPORTANTE: Routers de FastAPI - paths específicos antes que dinámicos
    app.include_router(cliente_router)
    app.include_router(busqueda_router)   # /productos/buscar, /destacados (específicos)
    app.include_router(producto_router)   # /productos/{id} (dinámico)
    app.include_router(carrito_router)
    app.include_router(favoritos_router)
    
    # Montar Django como fallback en "/"
    # FastAPI procesa primero, Django solo maneja lo que no matcheó
    from django.core.wsgi import get_wsgi_application
    from starlette.middleware.wsgi import WSGIMiddleware
    django_app = get_wsgi_application()
    app.mount("/", WSGIMiddleware(django_app))
    
    return app
