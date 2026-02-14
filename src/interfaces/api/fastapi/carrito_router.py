"""
Router del Carrito de Compras - FastAPI

Interfaces Layer - Puntos de entrada HTTP.

Endpoints:
- GET /api/v1/carrito - Obtener carrito activo
- POST /api/v1/carrito - Crear carrito
- POST /api/v1/carrito/items - Agregar producto
- DELETE /api/v1/carrito/items/{producto_id} - Quitar producto
- PATCH /api/v1/carrito/items/{producto_id} - Actualizar cantidad
- POST /api/v1/carrito/recalcular - Sincronizar precios
- POST /api/v1/carrito/bloquear - Bloquear para checkout
- POST /api/v1/carrito/desbloquear - Desbloquear
- POST /api/v1/carrito/confirmar - Confirmar (convertir a orden)
- DELETE /api/v1/carrito - Vaciar carrito
- GET /api/v1/carrito/resumen - Obtener resumen (para badge)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from uuid import UUID

from .dependencies import (
    get_carrito_repository,
    get_producto_repository,
    get_current_user_id,
    get_optional_user_id
)
from domain.repositories.carrito_repository import CarritoRepository
from domain.repositories.producto_repository import ProductoRepository
from domain.exceptions.dominio import (
    EntidadNoEncontrada,
    ReglaNegocioViolada,
    ConcurrenciaConflicto
)

from application.use_cases.carrito_use_cases import (
    CrearCarritoUseCase,
    ObtenerCarritoActivoUseCase,
    ObtenerOCrearCarritoUseCase,
    AgregarProductoAlCarritoUseCase,
    QuitarProductoDelCarritoUseCase,
    ActualizarCantidadProductoUseCase,
    RecalcularCarritoUseCase,
    BloquearCarritoUseCase,
    DesbloquearCarritoUseCase,
    ConfirmarCarritoUseCase,
    VaciarCarritoUseCase,
    ObtenerResumenCarritoUseCase
)
from application.dto.carrito_dto import (
    AgregarProductoAlCarritoActivoDTO,
    QuitarProductoDTO,
    ActualizarCantidadDTO,
    BloquearCarritoDTO,
    ConfirmarCarritoDTO,
    CarritoDTO,
    CarritoResumenDTO,
    OperacionCarritoResultadoDTO
)
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/carrito", tags=["carrito"])


# ===== Request Body Models =====
class AgregarProductoRequest(BaseModel):
    """Request body para agregar producto al carrito"""
    producto_id: UUID
    variante_id: UUID
    cantidad: int = 1


class ActualizarCantidadRequest(BaseModel):
    """Request body para actualizar cantidad"""
    cantidad: int


# ===== ENDPOINTS =====

@router.get("", response_model=Optional[CarritoDTO])
@router.get("/", response_model=Optional[CarritoDTO])
def obtener_carrito_activo(
    usuario_id: UUID = Depends(get_current_user_id),
    repo: CarritoRepository = Depends(get_carrito_repository)
):
    """
    Obtiene el carrito activo del usuario autenticado.
    
    Retorna null si no tiene carrito activo.
    """
    try:
        use_case = ObtenerCarritoActivoUseCase(repo)
        return use_case.ejecutar(usuario_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=CarritoDTO, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=CarritoDTO, status_code=status.HTTP_201_CREATED)
def crear_u_obtener_carrito(
    usuario_id: UUID = Depends(get_current_user_id),
    repo: CarritoRepository = Depends(get_carrito_repository)
):
    """
    Crea un nuevo carrito o retorna el existente.
    
    Un usuario solo puede tener un carrito activo.
    """
    try:
        use_case = ObtenerOCrearCarritoUseCase(repo)
        return use_case.ejecutar(usuario_id)
    except ConcurrenciaConflicto as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resumen", response_model=Optional[CarritoResumenDTO])
def obtener_resumen_carrito(
    usuario_id: Optional[UUID] = Depends(get_optional_user_id),
    repo: CarritoRepository = Depends(get_carrito_repository)
):
    """
    Obtiene un resumen ligero del carrito (para badge/header).
    
    Solo retorna: cantidad de items, total, estado.
    Permite usuarios no autenticados (retorna None).
    """
    try:
        # Si no hay usuario logueado, retornar None (carrito vacío)
        if not usuario_id:
            return None
            
        use_case = ObtenerResumenCarritoUseCase(repo)
        return use_case.ejecutar(usuario_id)
    except Exception as e:
        # En caso de error, retornar None en lugar de 500
        print(f"Error obteniendo resumen del carrito: {e}")
        return None


@router.post("/items", response_model=OperacionCarritoResultadoDTO)
def agregar_producto_al_carrito(
    request: AgregarProductoRequest,
    usuario_id: UUID = Depends(get_current_user_id),
    carrito_repo: CarritoRepository = Depends(get_carrito_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Agrega un producto al carrito activo.
    
    - Si no existe carrito, lo crea automáticamente
    - Valida stock disponible
    - Toma snapshot del precio actual
    - No permite productos duplicados (usar actualizar cantidad)
    """
    try:
        # Crear DTO con usuario_id del token
        datos = AgregarProductoAlCarritoActivoDTO(
            usuario_id=usuario_id,
            producto_id=request.producto_id,
            variante_id=request.variante_id,
            cantidad=request.cantidad
        )
        
        use_case = AgregarProductoAlCarritoUseCase(carrito_repo, producto_repo)
        return use_case.ejecutar(datos)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioViolada as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConcurrenciaConflicto as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/items/{producto_id}", response_model=OperacionCarritoResultadoDTO)
def quitar_producto_del_carrito(
    producto_id: UUID,
    carrito_id: UUID,
    variante_id: UUID,
    usuario_id: UUID = Depends(get_current_user_id),
    repo: CarritoRepository = Depends(get_carrito_repository)
):
    """
    Quita un producto del carrito.
    """
    try:
        request = QuitarProductoDTO(
            carrito_id=carrito_id,
            producto_id=producto_id,
            variante_id=variante_id
        )
        use_case = QuitarProductoDelCarritoUseCase(repo)
        return use_case.ejecutar(request, usuario_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioViolada as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/items/{producto_id}", response_model=OperacionCarritoResultadoDTO)
def actualizar_cantidad_producto(
    producto_id: UUID,
    carrito_id: UUID,
    variante_id: UUID,
    nueva_cantidad: int,
    usuario_id: UUID = Depends(get_current_user_id),
    carrito_repo: CarritoRepository = Depends(get_carrito_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Actualiza la cantidad de un producto en el carrito.
    
    - Valida stock disponible
    - Cantidad debe ser > 0
    """
    try:
        request = ActualizarCantidadDTO(
            carrito_id=carrito_id,
            producto_id=producto_id,
            variante_id=variante_id,
            nueva_cantidad=nueva_cantidad
        )
        use_case = ActualizarCantidadProductoUseCase(carrito_repo, producto_repo)
        return use_case.ejecutar(request, usuario_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioViolada as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recalcular/{carrito_id}", response_model=CarritoDTO)
def recalcular_carrito(
    carrito_id: UUID,
    usuario_id: UUID = Depends(get_current_user_id),
    carrito_repo: CarritoRepository = Depends(get_carrito_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Recalcula los totales del carrito y sincroniza precios con el catálogo.
    
    Útil cuando los precios pueden haber cambiado.
    """
    try:
        use_case = RecalcularCarritoUseCase(carrito_repo, producto_repo)
        return use_case.ejecutar(carrito_id, usuario_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioViolada as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bloquear", response_model=OperacionCarritoResultadoDTO)
def bloquear_carrito_para_checkout(
    datos: BloquearCarritoDTO,
    usuario_id: UUID = Depends(get_current_user_id),
    carrito_repo: CarritoRepository = Depends(get_carrito_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Bloquea el carrito para proceder al checkout.
    
    - No permite más modificaciones
    - Valida stock de todos los productos
    - Requiere versión para optimistic locking
    - Estado: BLOQUEADO
    """
    try:
        use_case = BloquearCarritoUseCase(carrito_repo, producto_repo)
        return use_case.ejecutar(datos, usuario_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioViolada as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ConcurrenciaConflicto as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/desbloquear/{carrito_id}", response_model=OperacionCarritoResultadoDTO)
def desbloquear_carrito(
    carrito_id: UUID,
    usuario_id: UUID = Depends(get_current_user_id),
    repo: CarritoRepository = Depends(get_carrito_repository)
):
    """
    Desbloquea el carrito si el checkout fue cancelado.
    
    Permite volver a modificar el carrito.
    """
    try:
        use_case = DesbloquearCarritoUseCase(repo)
        return use_case.ejecutar(carrito_id, usuario_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioViolada as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/confirmar", response_model=OperacionCarritoResultadoDTO)
def confirmar_carrito(
    datos: ConfirmarCarritoDTO,
    usuario_id: UUID = Depends(get_current_user_id),
    repo: CarritoRepository = Depends(get_carrito_repository)
):
    """
    Confirma el carrito y lo convierte en una orden.
    
    - IDEMPOTENTE: Confirmar un carrito ya confirmado no genera error
    - Requiere que el carrito esté BLOQUEADO
    - Estado final: CONFIRMADO
    """
    try:
        use_case = ConfirmarCarritoUseCase(repo)
        return use_case.ejecutar(datos, usuario_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioViolada as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{carrito_id}", response_model=OperacionCarritoResultadoDTO)
def vaciar_carrito(
    carrito_id: UUID,
    usuario_id: UUID = Depends(get_current_user_id),
    repo: CarritoRepository = Depends(get_carrito_repository)
):
    """
    Vacía todos los productos del carrito.
    """
    try:
        use_case = VaciarCarritoUseCase(repo)
        return use_case.ejecutar(carrito_id, usuario_id)
    except EntidadNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioViolada as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
