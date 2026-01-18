"""
Router de productos - FastAPI
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from .dependencies import get_producto_repository
from domain.repositories.producto_repository import ProductoRepository

from application.use_cases.producto_use_cases import (
    CrearProductoUseCase,
    ObtenerProductoUseCase,
    ListarProductosUseCase
)
from application.dto.producto_dto import CrearProductoDTO, ProductoDTO
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
