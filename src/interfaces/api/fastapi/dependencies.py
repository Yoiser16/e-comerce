"""
Dependencias para inyección en FastAPI
"""
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Generator, Optional
from uuid import UUID

from infrastructure.persistence.repositories.cliente_repository_impl import ClienteRepositoryImpl
from domain.repositories.cliente_repository import ClienteRepository
from domain.repositories.producto_repository import ProductoRepository
from domain.repositories.carrito_repository import CarritoRepository

# Seguridad Bearer para JWT
security = HTTPBearer(auto_error=False)


# --- Repositories ---

def get_cliente_repository() -> Generator[ClienteRepository, None, None]:
    """Provee una instancia de ClienteRepository"""
    try:
        repo = ClienteRepositoryImpl()
        yield repo
    except Exception as e:
        raise e

def get_producto_repository() -> Generator[ProductoRepository, None, None]:
    """Provee una instancia de ProductoRepository"""
    from infrastructure.persistence.repositories.producto_repository_impl import ProductoRepositoryImpl
    try:
        repo = ProductoRepositoryImpl()
        yield repo
    except Exception as e:
        raise e

def get_carrito_repository() -> Generator[CarritoRepository, None, None]:
    """Provee una instancia de CarritoRepository"""
    from infrastructure.persistence.repositories.carrito_repository_django import CarritoRepositoryDjango
    try:
        repo = CarritoRepositoryDjango()
        yield repo
    except Exception as e:
        raise e

def get_orden_repository():
    """Provee una instancia de OrdenRepository"""
    from infrastructure.persistence.repositories.orden_repository_impl import OrdenRepositoryImpl
    try:
        repo = OrdenRepositoryImpl()
        yield repo
    except Exception as e:
        raise e


# --- Autenticación ---

def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> UUID:
    """
    Extrae el user_id del token JWT.
    
    TODO: Implementar validación completa del JWT.
    Por ahora retorna un UUID fijo para desarrollo.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # TODO: Decodificar JWT y extraer user_id
    # Por ahora, para desarrollo, extraemos el user_id del header X-User-ID
    # En producción, esto debe venir del token JWT validado
    try:
        # Placeholder - en producción usar jwt.decode()
        from uuid import uuid4
        # Retornar UUID fijo para testing
        return UUID("00000000-0000-0000-0000-000000000001")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_optional_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[UUID]:
    """
    Extrae el user_id si está autenticado, None si es anónimo.
    """
    if not credentials:
        return None
    
    try:
        from uuid import uuid4
        return UUID("00000000-0000-0000-0000-000000000001")
    except Exception:
        return None


def get_current_user_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Verifica que el usuario actual sea ADMIN o OPERADOR.
    
    En desarrollo, permite acceso sin token.
    En producción, requiere validación JWT.
    """
    import os
    
    # En desarrollo, permitir acceso sin autenticación
    if os.getenv('AMBIENTE', 'development') == 'development':
        return {"user_id": "dev-admin", "rol": "ADMIN"}
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Se requiere token de acceso.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # TODO: Decodificar JWT, extraer usuario y verificar rol
    # Por ahora en desarrollo, permitir acceso
    return {"user_id": "admin", "rol": "ADMIN"}


# --- Services / Otros ---
# Aquí se agregarían otros servicios como EmailService, etc.
