"""
Router de clientes - FastAPI
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

from .dependencies import get_cliente_repository
from domain.repositories.cliente_repository import ClienteRepository

from application.use_cases.cliente_use_cases import (
    CrearClienteUseCase,
    ObtenerClienteUseCase,
    ActualizarClienteUseCase
)
from application.dto.cliente_dto import CrearClienteDTO, ClienteDTO, ActualizarClienteDTO
from domain.exceptions.dominio import ExcepcionDominio


router = APIRouter(prefix="/api/v1/clientes", tags=["clientes"])


# Endpoint de prueba simple
@router.get("/test")
def test_endpoint():
    """Endpoint de prueba para verificar que el router funciona"""
    return {"status": "ok", "message": "Router de clientes funcionando"}


# DTO para auto-registro desde checkout
class AutoRegisterDTO(BaseModel):
    email: EmailStr
    nombre: str
    apellido: Optional[str] = ""
    telefono: Optional[str] = ""


class AutoRegisterResponse(BaseModel):
    success: bool
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    user_id: Optional[str] = None


@router.post("/auto-register", response_model=AutoRegisterResponse)
async def auto_register_cliente(
    datos: AutoRegisterDTO,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """
    Auto-registra un cliente desde el checkout.
    Si el email ya existe, retorna éxito sin crear duplicado.
    No requiere contraseña - el usuario usará Google Sign-In para futuras sesiones.
    """
    try:
        # Verificar si el cliente ya existe por email
        cliente_existente = None
        try:
            # Buscar cliente por email
            from infrastructure.persistence.django_cliente_repository import DjangoClienteRepository
            if hasattr(repo, 'buscar_por_email'):
                cliente_existente = repo.buscar_por_email(datos.email)
        except Exception:
            pass
        
        if cliente_existente:
            return AutoRegisterResponse(
                success=True,
                message="Cliente ya registrado. Use Google para iniciar sesión.",
                user_id=str(cliente_existente.id) if hasattr(cliente_existente, 'id') else None
            )
        
        # Crear nuevo cliente
        from infrastructure.auth.models import Usuario, RolUsuario
        from rest_framework_simplejwt.tokens import RefreshToken
        
        # Crear usuario en Django
        user, created = Usuario.objects.get_or_create(
            email=datos.email,
            defaults={
                'nombre': f"{datos.nombre} {datos.apellido}".strip(),
                'rol': RolUsuario.LECTURA
            }
        )
        
        if created:
            user.set_unusable_password()  # Sin contraseña, solo Google Sign-In
            user.save()
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        return AutoRegisterResponse(
            success=True,
            message="Cliente registrado exitosamente",
            access_token=str(access),
            refresh_token=str(refresh),
            user_id=str(user.id)
        )
        
    except Exception as e:
        # Si hay error, no bloquear el checkout
        return AutoRegisterResponse(
            success=False,
            message=f"No se pudo registrar automáticamente: {str(e)}"
        )


@router.post("/", response_model=ClienteDTO, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    datos: CrearClienteDTO,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """
    Crea un nuevo cliente.
    """
    try:
        use_case = CrearClienteUseCase(repo)
        return use_case.ejecutar(datos)
    except ExcepcionDominio as e:
        # El exception handler global lo capturará, 
        # pero también podemos relanzarlo o transformarlo aquí si fuera necesario.
        # Al no capturarlo, dejamos que el middleware de excepciones haga su trabajo.
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ClienteDTO])
def listar_clientes(
    limite: int = 1000,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """
    Lista todos los clientes (para panel admin).
    """
    try:
        clientes = repo.obtener_todos(limite=limite)
        # Convertir entidades de dominio a DTOs
        return [
            ClienteDTO(
                id=str(c.id.valor) if hasattr(c.id, 'valor') else str(c.id),
                nombre=c.nombre,
                apellido=c.apellido,
                email=c.email.valor if hasattr(c.email, 'valor') else str(c.email),
                telefono=c.telefono.numero if c.telefono and hasattr(c.telefono, 'numero') else None,
                tipo_documento=c.documento.tipo.value if c.documento else None,
                numero_documento=c.documento.numero if c.documento else None,
                fecha_creacion=c.fecha_creacion,
                fecha_modificacion=c.fecha_modificacion,
                activo=c.activo
            )
            for c in clientes
        ]
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al listar clientes: {str(e)}")


@router.get("/{cliente_id}", response_model=ClienteDTO)
def obtener_cliente(
    cliente_id: UUID,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """
    Obtiene un cliente por ID.
    """
    try:
        use_case = ObtenerClienteUseCase(repo)
        return use_case.ejecutar(cliente_id)
    except ExcepcionDominio as e:
        raise e


@router.put("/", response_model=ClienteDTO)
def actualizar_cliente(
    datos: ActualizarClienteDTO,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """
    Actualiza datos de un cliente.
    """
    try:
        use_case = ActualizarClienteUseCase(repo)
        return use_case.ejecutar(datos)
    except ExcepcionDominio as e:
        raise e
