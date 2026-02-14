"""
DTOs relacionados con Producto
"""
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from domain.entities.producto import Producto
from domain.entities.producto_variante import ProductoVariante


@dataclass
class ProductoVarianteDTO:
    """DTO de salida para variante de producto"""
    id: Optional[UUID]
    sku: str
    color: Optional[str]
    largo: Optional[str]
    precio_monto: Decimal
    precio_moneda: str
    stock_actual: int
    stock_minimo: int
    imagen_url: Optional[str] = None
    activo: bool = True
    orden: int = 0

    @classmethod
    def desde_entidad(cls, variante: ProductoVariante) -> 'ProductoVarianteDTO':
        return cls(
            id=variante.id,
            sku=variante.sku,
            color=variante.color,
            largo=variante.largo,
            precio_monto=variante.precio.monto,
            precio_moneda=variante.precio.moneda,
            stock_actual=variante.stock_actual,
            stock_minimo=variante.stock_minimo,
            imagen_url=variante.imagen_url,
            activo=variante.activo,
            orden=variante.orden
        )


@dataclass
class ProductoVarianteInputDTO:
    """DTO de entrada para variante de producto"""
    id: Optional[UUID] = None
    sku: Optional[str] = None
    color: Optional[str] = None
    largo: Optional[str] = None
    precio_monto: Decimal = Decimal('0')
    precio_moneda: str = "COP"
    stock_actual: int = 0
    stock_minimo: int = 0
    imagen_url: Optional[str] = None
    activo: bool = True
    orden: int = 0


@dataclass
class CrearProductoDTO:
    """DTO para crear un producto"""
    codigo: str
    nombre: str
    descripcion: str
    precio_monto: Decimal
    precio_moneda: str = "COP"
    stock_actual: int = 0
    stock_minimo: int = 0
    categoria: Optional[str] = None
    imagen_principal: Optional[str] = None
    imagenes: List[str] = field(default_factory=list)
    color: Optional[str] = None
    tipo: Optional[str] = None
    largo: Optional[str] = None
    origen: Optional[str] = None
    metodo: Optional[str] = None
    calidad: Optional[str] = None
    destacado: bool = False
    disponible_b2b: bool = True
    porcentaje_descuento_b2b: Optional[int] = None
    variantes: List[ProductoVarianteInputDTO] = field(default_factory=list)


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
    imagenes: Optional[List[str]] = None
    activo: Optional[bool] = None
    color: Optional[str] = None
    tipo: Optional[str] = None
    largo: Optional[str] = None
    origen: Optional[str] = None
    metodo: Optional[str] = None
    calidad: Optional[str] = None
    destacado: Optional[bool] = None
    disponible_b2b: Optional[bool] = None
    porcentaje_descuento_b2b: Optional[int] = None
    variantes: Optional[List[ProductoVarianteInputDTO]] = None


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
    imagenes: List[str] = field(default_factory=list)
    color: Optional[str] = None
    tipo: Optional[str] = None
    largo: Optional[str] = None
    origen: Optional[str] = None
    metodo: Optional[str] = None
    calidad: Optional[str] = None
    destacado: bool = False
    disponible_b2b: bool = True
    porcentaje_descuento_b2b: Optional[int] = None
    variantes: List[ProductoVarianteDTO] = field(default_factory=list)
    
    @classmethod
    def desde_entidad(cls, producto: Producto) -> 'ProductoDTO':
        """Crea un DTO desde una entidad Producto"""
        # Obtener atributos adicionales si existen
        variantes = [ProductoVarianteDTO.desde_entidad(v) for v in getattr(producto, 'variantes', []) or []]

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
            imagenes=getattr(producto, 'imagenes', []) or [],
            color=getattr(producto, 'color', None),
            tipo=getattr(producto, 'tipo', None),
            largo=getattr(producto, 'largo', None),
            origen=getattr(producto, 'origen', None),
            metodo=getattr(producto, 'metodo', None),
            calidad=getattr(producto, 'calidad', None),
            destacado=getattr(producto, 'destacado', False),
            disponible_b2b=getattr(producto, 'disponible_b2b', True),
            porcentaje_descuento_b2b=getattr(producto, 'porcentaje_descuento_b2b', None),
            variantes=variantes,
        )
