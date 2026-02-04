"""
Router de productos - FastAPI
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from uuid import UUID
import time

from .dependencies import get_producto_repository
from domain.repositories.producto_repository import ProductoRepository

from application.use_cases.producto_use_cases import (
    CrearProductoUseCase,
    ObtenerProductoUseCase,
    ListarProductosUseCase,
    ListarTodosProductosUseCase,
    ActualizarProductoUseCase,
    EliminarProductoUseCase
)
from application.dto.producto_dto import CrearProductoDTO, ProductoDTO, ActualizarProductoDTO
from domain.exceptions.dominio import ExcepcionDominio

router = APIRouter(prefix="/api/v1/productos", tags=["productos"])

# ═══════════════════════════════════════════════════════════════════════════
# CACHÉ DE PRODUCTOS - Reduce consultas repetidas
# ═══════════════════════════════════════════════════════════════════════════
_productos_cache = {
    'lista': None,
    'timestamp': 0,
    'todos': None,
    'todos_timestamp': 0
}
PRODUCTOS_CACHE_TTL = 60  # 60 segundos para productos


def invalidar_cache_productos():
    """Invalida el caché de productos (llamar después de crear/actualizar/eliminar)"""
    _productos_cache['lista'] = None
    _productos_cache['todos'] = None


@router.post("/", response_model=ProductoDTO, status_code=status.HTTP_201_CREATED)
def crear_producto(
    datos: CrearProductoDTO,
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Crea un nuevo producto en el catálogo.
    """
    try:
        use_case = CrearProductoUseCase(repo)
        resultado = use_case.ejecutar(datos)
        invalidar_cache_productos()  # Invalidar caché
        return resultado
    except ExcepcionDominio as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ProductoDTO])
def listar_productos(
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Lista todos los productos disponibles para la venta.
    Usa caché para mejorar rendimiento.
    """
    try:
        # Verificar caché
        if (_productos_cache['lista'] is not None and 
            time.time() - _productos_cache['timestamp'] < PRODUCTOS_CACHE_TTL):
            return _productos_cache['lista']
        
        use_case = ListarProductosUseCase(repo)
        resultado = use_case.ejecutar()
        
        # Guardar en caché
        _productos_cache['lista'] = resultado
        _productos_cache['timestamp'] = time.time()
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/destacados", response_model=List[ProductoDTO])
def listar_productos_destacados(
    limite: int = 8,
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Lista los productos destacados para mostrar en la página principal.
    """
    try:
        productos = repo.obtener_destacados(limite=limite)
        return [ProductoDTO.desde_entidad(p) for p in productos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/todos", response_model=List[ProductoDTO])
def listar_todos_productos(
    limite: int = 100,
    offset: int = 0,
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Lista TODOS los productos (para administración).
    Incluye activos e inactivos. Usa caché para mejorar rendimiento.
    """
    try:
        # Verificar caché (solo si offset=0 y limite estándar)
        if (offset == 0 and limite >= 100 and 
            _productos_cache['todos'] is not None and 
            time.time() - _productos_cache['todos_timestamp'] < PRODUCTOS_CACHE_TTL):
            return _productos_cache['todos']
        
        use_case = ListarTodosProductosUseCase(repo)
        resultado = use_case.ejecutar({'limite': limite, 'offset': offset})
        
        # Guardar en caché solo para consultas base
        if offset == 0 and limite >= 100:
            _productos_cache['todos'] = resultado
            _productos_cache['todos_timestamp'] = time.time()
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{producto_id}", response_model=ProductoDTO)
def obtener_producto(
    producto_id: UUID,
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Obtiene el detalle de un producto por su ID.
    """
    try:
        use_case = ObtenerProductoUseCase(repo)
        return use_case.ejecutar(producto_id)
    except ExcepcionDominio as e:
        raise e


@router.put("/{producto_id}", response_model=ProductoDTO)
def actualizar_producto(
    producto_id: UUID,
    datos: ActualizarProductoDTO,
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Actualiza un producto existente.
    """
    try:
        # Asegurar que el ID del path coincida con el DTO
        datos.id = producto_id
        use_case = ActualizarProductoUseCase(repo)
        resultado = use_case.ejecutar(datos)
        invalidar_cache_productos()  # Invalidar caché
        return resultado
    except ExcepcionDominio as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: UUID,
    permanente: bool = False,
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Elimina un producto.
    - Si permanente=False: Desactiva el producto (soft delete)
    - Si permanente=True: Elimina permanentemente de la BD (hard delete) - SOLO si no tiene historial de órdenes
    """
    try:
        if permanente:
            # Eliminación permanente (hard delete) - valida que no tenga historial
            repo.eliminar_permanentemente(producto_id)
        else:
            # Eliminación suave (soft delete) - solo desactiva
            use_case = EliminarProductoUseCase(repo)
            use_case.ejecutar(producto_id)
        
        invalidar_cache_productos()  # Invalidar caché
        return None
    except ValueError as e:
        # Error de validación (ej: producto con historial de órdenes)
        raise HTTPException(status_code=400, detail=str(e))
    except ExcepcionDominio as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
