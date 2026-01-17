"""
DTOs relacionados con Producto
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from domain.entities.producto import Producto


@dataclass
class CrearProductoDTO:
    """DTO para crear un producto"""
    codigo: str
    nombre: str
    descripcion: str
    precio_monto: Decimal
    precio_moneda: str
    stock_actual: int
    stock_minimo: int


@dataclass
class ActualizarProductoDTO:
    """DTO para actualizar un producto"""
    id: UUID
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_monto: Optional[Decimal] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None


@dataclass
class ProductoDTO:
    """DTO de salida para Producto"""
    id: UUID
    codigo: str
    nombre: str
    descripcion: str
    precio: str  # Formateado
    precio_monto: Decimal
    precio_moneda: str
    stock_actual: int
    stock_minimo: int
    activo: bool
    fecha_creacion: datetime
    fecha_modificacion: datetime
    
    @classmethod
    def desde_entidad(cls, producto: Producto) -> 'ProductoDTO':
        """Crea un DTO desde una entidad Producto"""
        return cls(
            id=producto.id,
            codigo=producto.codigo.valor,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=str(producto.precio),
            precio_monto=producto.precio.monto,
            precio_moneda=producto.precio.moneda,
            stock_actual=producto.stock_actual,
            stock_minimo=producto.stock_minimo,
            activo=producto.activo,
            fecha_creacion=producto.fecha_creacion,
            fecha_modificacion=producto.fecha_modificacion
        )
