"""
DTOs relacionados con Producto
"""
from dataclasses import dataclass, field
from typing import Optional, List
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
    precio_moneda: str = "MXN"
    stock_actual: int = 0
    stock_minimo: int = 0
    categoria: Optional[str] = None
    imagen_principal: Optional[str] = None
    color: Optional[str] = None
    tipo: Optional[str] = None
    largo: Optional[str] = None
    origen: Optional[str] = None
    metodo: Optional[str] = None
    calidad: Optional[str] = None


@dataclass
class ActualizarProductoDTO:
    """DTO para actualizar un producto"""
    id: Optional[UUID] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_monto: Optional[Decimal] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None
    categoria: Optional[str] = None
    imagen_principal: Optional[str] = None
    activo: Optional[bool] = None
    color: Optional[str] = None
    tipo: Optional[str] = None
    largo: Optional[str] = None
    origen: Optional[str] = None
    metodo: Optional[str] = None
    calidad: Optional[str] = None


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
    categoria: Optional[str] = None
    imagen_principal: Optional[str] = None
    color: Optional[str] = None
    tipo: Optional[str] = None
    largo: Optional[str] = None
    origen: Optional[str] = None
    metodo: Optional[str] = None
    calidad: Optional[str] = None
    
    @classmethod
    def desde_entidad(cls, producto: Producto) -> 'ProductoDTO':
        """Crea un DTO desde una entidad Producto"""
        # Obtener atributos adicionales si existen
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
            fecha_modificacion=producto.fecha_modificacion,
            categoria=getattr(producto, 'categoria', None),
            imagen_principal=getattr(producto, 'imagen_principal', None),
            color=getattr(producto, 'color', None),
            tipo=getattr(producto, 'tipo', None),
            largo=getattr(producto, 'largo', None),
            origen=getattr(producto, 'origen', None),
            metodo=getattr(producto, 'metodo', None),
            calidad=getattr(producto, 'calidad', None),
        )
