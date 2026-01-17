"""
Casos de uso relacionados con Producto
"""
from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from application.use_cases.base import CasoUsoBase
from application.dto.producto_dto import CrearProductoDTO, ProductoDTO, ActualizarProductoDTO
from domain.repositories.producto_repository import ProductoRepository
from domain.entities.producto import Producto
from domain.value_objects.codigo_producto import CodigoProducto
from domain.value_objects.dinero import Dinero
from domain.exceptions.dominio import EntidadNoEncontrada, ReglaNegocioViolada


class CrearProductoUseCase(CasoUsoBase[CrearProductoDTO, ProductoDTO]):
    """Caso de uso: Crear un nuevo producto"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
    
    def ejecutar(self, request: CrearProductoDTO) -> ProductoDTO:
        # Validar si ya existe código
        codigo = CodigoProducto(request.codigo)
        if self._repo.obtener_por_codigo(codigo):
            raise ReglaNegocioViolada(f"Ya existe un producto con código {request.codigo}")
            
        producto = Producto(
            codigo=codigo,
            nombre=request.nombre,
            descripcion=request.descripcion,
            precio=Dinero(request.precio_monto, request.precio_moneda),
            stock_actual=request.stock_actual,
            stock_minimo=request.stock_minimo
        )
        
        guardado = self._repo.guardar(producto)
        return ProductoDTO.desde_entidad(guardado)


class ObtenerProductoUseCase(CasoUsoBase[UUID, ProductoDTO]):
    """Caso de uso: Obtener producto por ID"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
        
    def ejecutar(self, request: UUID) -> ProductoDTO:
        producto = self._repo.obtener_por_id(request)
        if not producto:
            raise EntidadNoEncontrada(f"Producto {request} no encontrado")
        return ProductoDTO.desde_entidad(producto)


class ListarProductosUseCase(CasoUsoBase[None, List[ProductoDTO]]):
    """Caso de uso: Listar productos disponibles"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
        
    def ejecutar(self, request: None = None) -> List[ProductoDTO]:
        productos = self._repo.obtener_disponibles()
        return [ProductoDTO.desde_entidad(p) for p in productos]
