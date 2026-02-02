"""
Aplicación principal de FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from django.core.wsgi import get_wsgi_application

from .cliente_router import router as cliente_router
from .producto_router import router as producto_router
from .carrito_router import router as carrito_router
from .busqueda_router import router as busqueda_router
from .favoritos_router import router as favoritos_router
from .dashboard_router import router as dashboard_router
from .categoria_router import router as categoria_router
from .upload_router import router as upload_router
from .orden_router import router as orden_router
from .inventario_router import router as inventario_router
from .auth_router import router as auth_router
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
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers
    app.add_exception_handler(ExcepcionDominio, exception_handler_dominio)
    
    # IMPORTANTE: Routers de FastAPI - paths específicos antes que dinámicos
    app.include_router(auth_router)         # Autenticación
    app.include_router(upload_router)     # Upload de imágenes
    app.include_router(cliente_router)
    app.include_router(busqueda_router)   # /productos/buscar, /destacados (específicos)
    app.include_router(producto_router)   # /productos/{id} (dinámico)
    app.include_router(carrito_router)
    app.include_router(favoritos_router)
    app.include_router(dashboard_router)  # Dashboard administrativo
    app.include_router(categoria_router)  # Categorías
    app.include_router(orden_router)      # Órdenes
    app.include_router(inventario_router) # Inventario y movimientos
    
    # Servir archivos estáticos
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Montar Django SOLO para /admin/
    # FastAPI maneja todos los endpoints /api/v1/*
    from django.core.wsgi import get_wsgi_application
    from starlette.middleware.wsgi import WSGIMiddleware
    django_app = get_wsgi_application()
    
    app.mount("/admin", WSGIMiddleware(django_app))
    
    # Servir frontend Vue (debe ser lo último para no interferir con otras rutas)
    import os
    from pathlib import Path
    frontend_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "frontend" / "dist"
    if frontend_path.exists():
        from fastapi.responses import FileResponse
        
        # Servir assets del frontend
        app.mount("/assets", StaticFiles(directory=str(frontend_path / "assets")), name="frontend-assets")
        
        # Servir archivos estáticos del frontend (imágenes, videos, etc.)
        for file in frontend_path.iterdir():
            if file.is_file() and file.suffix in ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.mp4', '.webm']:
                @app.get(f"/{file.name}")
                async def serve_media(filename: str = file.name):
                    return FileResponse(str(frontend_path / filename))
        
        # Servir index.html para todas las rutas no manejadas (SPA routing)
        @app.get("/{full_path:path}")
        async def serve_frontend(full_path: str):
            # Si es una ruta de API o admin, no sirvas el frontend
            if full_path.startswith("api/") or full_path.startswith("admin/") or full_path.startswith("static/"):
                return {"detail": "Not Found"}
            
            # Sirve index.html para rutas del frontend
            index_file = frontend_path / "index.html"
            if index_file.exists():
                return FileResponse(str(index_file))
            return {"detail": "Frontend not built"}
    
    return app
