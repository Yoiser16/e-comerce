"""
Router de Dashboard - FastAPI
Endpoints para estadísticas y datos del panel administrativo
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from .dependencies import (
    get_orden_repository,
    get_producto_repository,
    get_cliente_repository,
    get_current_user_admin
)

from domain.repositories.orden_repository import OrdenRepository
from domain.repositories.producto_repository import ProductoRepository
from domain.repositories.cliente_repository import ClienteRepository

from application.use_cases.dashboard_use_cases import (
    ObtenerEstadisticasGeneralesUseCase,
    ObtenerOrdenesRecientesUseCase,
    ObtenerProductosStockBajoUseCase
)
from application.dto.dashboard_dto import (
    EstadisticasGeneralesDTO,
    OrdenResumeDTO,
    ProductoStockBajoDTO
)

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/estadisticas", response_model=EstadisticasGeneralesDTO)
def obtener_estadisticas(
    orden_repo: OrdenRepository = Depends(get_orden_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    cliente_repo: ClienteRepository = Depends(get_cliente_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Obtiene estadísticas generales del sistema
    
    Requiere: Rol ADMIN o OPERADOR
    """
    try:
        use_case = ObtenerEstadisticasGeneralesUseCase(
            orden_repo,
            producto_repo,
            cliente_repo
        )
        return use_case.ejecutar()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )


@router.get("/ordenes/recientes", response_model=List[OrdenResumeDTO])
def obtener_ordenes_recientes(
    limite: int = 5,
    orden_repo: OrdenRepository = Depends(get_orden_repository),
    cliente_repo: ClienteRepository = Depends(get_cliente_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Obtiene las órdenes más recientes
    
    Parámetros:
    - limite: Número máximo de órdenes a retornar (default: 5)
    
    Requiere: Rol ADMIN o OPERADOR
    """
    try:
        use_case = ObtenerOrdenesRecientesUseCase(orden_repo, cliente_repo)
        return use_case.ejecutar(limite)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener órdenes recientes: {str(e)}"
        )


@router.get("/productos/stock-bajo", response_model=List[ProductoStockBajoDTO])
def obtener_productos_stock_bajo(
    umbral: int = 5,
    limite: int = 10,
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Obtiene productos con stock bajo
    
    Parámetros:
    - umbral: Stock mínimo para considerar "bajo" (default: 5)
    - limite: Número máximo de productos a retornar (default: 10)
    
    Requiere: Rol ADMIN o OPERADOR
    """
    try:
        use_case = ObtenerProductosStockBajoUseCase(producto_repo)
        return use_case.ejecutar(umbral, limite)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos con stock bajo: {str(e)}"
        )
