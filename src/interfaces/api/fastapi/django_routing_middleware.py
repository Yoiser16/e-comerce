"""
Middleware para delegar rutas específicas a Django.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from django.core.handlers.asgi import ASGIHandler
import re


class DjangoRoutingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que delega rutas específicas a Django.
    Solo procesa rutas que coinciden con patrones definidos.
    """
    
    def __init__(self, app: ASGIApp, django_patterns: list):
        super().__init__(app)
        self.django_app = ASGIHandler()
        # Compilar patrones de regex
        self.patterns = [re.compile(pattern) for pattern in django_patterns]
    
    async def dispatch(self, request, call_next):
        path = request.url.path
        
        # Verificar si el path debe ser manejado por Django
        for pattern in self.patterns:
            if pattern.match(path):
                # Delegar a Django
                return await self.django_app(request.scope, request.receive, request._send)
        
        # Si no matchea, continuar con FastAPI
        return await call_next(request)
