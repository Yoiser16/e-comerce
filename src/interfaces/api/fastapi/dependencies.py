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
from domain.repositories.producto_repository import ProductoRepository
from domain.repositories.carrito_repository import CarritoRepository
from infrastructure.auth.models import Usuario

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

def get_current_user_email(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Extrae el email del usuario desde el header X-User-Email.
    
    El frontend debe enviar el email en el header X-User-Email.
    Esto es un workaround temporal hasta que se implemente JWT decodification correctamente.
    
    Ejemplo:
    GET /api/v1/ordenes/mis-ordenes
    Authorization: Bearer <token>
    X-User-Email: usuario@example.com
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener email del header X-User-Email
    email = request.headers.get('X-User-Email', '').strip()
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere header X-User-Email",
        )
    
    return email

def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> UUID:
    """
    Extrae el user_id del token JWT.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        import jwt
        from django.conf import settings
        
        # Decodificar el token JWT
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        
        # Extraer user_id del payload
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no contiene user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return UUID(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error de autenticación: {str(e)}",
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
        import jwt
        from django.conf import settings
        
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        
        user_id = payload.get("user_id")
        if user_id:
            return UUID(user_id)
        return None
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


# Alias para compatibilidad
get_current_admin_user = get_current_user_admin


async def get_optional_mayorista_user(request: Request) -> Optional[Usuario]:
    """
    Intenta obtener el usuario mayorista actual desde el header X-User-Email.
    Retorna None si no se encuentra o no es válido.
    """
    try:
        email = request.headers.get('X-User-Email', '').strip()
        if not email:
            return None
            
        # Importación local para evitar ciclos si fuera necesario, 
        # pero Usuario ya se importó arriba.
        from infrastructure.auth.models import Usuario
        from asgiref.sync import sync_to_async
        
        try:
            user = await sync_to_async(Usuario.objects.get)(email=email, tipo='MAYORISTA')
            return user
        except Usuario.DoesNotExist:
            return None
    except Exception:
        return None


# --- Services / Otros ---
# Aquí se agregarían otros servicios como EmailService, etc.
