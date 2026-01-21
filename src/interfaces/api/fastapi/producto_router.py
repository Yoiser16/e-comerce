"""
Router de productos - FastAPI
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from uuid import UUID

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
        return use_case.ejecutar(datos)
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
    """
    try:
        use_case = ListarProductosUseCase(repo)
        return use_case.ejecutar()
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
    Incluye activos e inactivos.
    """
    try:
        use_case = ListarTodosProductosUseCase(repo)
        return use_case.ejecutar({'limite': limite, 'offset': offset})
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
        return use_case.ejecutar(datos)
    except ExcepcionDominio as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: UUID,
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Elimina (desactiva) un producto.
    """
    try:
        use_case = EliminarProductoUseCase(repo)
        use_case.ejecutar(producto_id)
        return None
    except ExcepcionDominio as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
