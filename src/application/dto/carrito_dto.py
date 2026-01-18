"""
DTOs relacionados con Carrito de Compras

Data Transfer Objects para comunicación entre capas.
Evita exponer entidades de dominio a la capa de presentación.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from domain.entities.carrito import Carrito
from domain.value_objects.item_carrito import ItemCarrito


# ==========================================
# DTOs DE ENTRADA (Request)
# ==========================================

@dataclass
class CrearCarritoDTO:
    """DTO para crear un nuevo carrito"""
    usuario_id: UUID


@dataclass
class AgregarProductoDTO:
    """DTO para agregar un producto al carrito"""
    carrito_id: UUID
    producto_id: UUID
    cantidad: int


@dataclass
class AgregarProductoAlCarritoActivoDTO:
    """DTO para agregar producto al carrito activo del usuario"""
    usuario_id: UUID
    producto_id: UUID
    cantidad: int


@dataclass
class QuitarProductoDTO:
    """DTO para quitar un producto del carrito"""
    carrito_id: UUID
    producto_id: UUID


@dataclass
class ActualizarCantidadDTO:
    """DTO para actualizar cantidad de un producto"""
    carrito_id: UUID
    producto_id: UUID
    nueva_cantidad: int


@dataclass
class AplicarDescuentoDTO:
    """DTO para aplicar descuento al carrito"""
    carrito_id: UUID
    monto_descuento: Decimal
    moneda: str = "USD"


@dataclass
class BloquearCarritoDTO:
    """DTO para bloquear carrito para checkout"""
    carrito_id: UUID
    version: int  # Para optimistic locking


@dataclass
class ConfirmarCarritoDTO:
    """DTO para confirmar carrito"""
    carrito_id: UUID
    version: int  # Para optimistic locking


# ==========================================
# DTOs DE SALIDA (Response)
# ==========================================

@dataclass
class ItemCarritoDTO:
    """DTO de salida para un item del carrito"""
    producto_id: UUID
    sku: str
    nombre: str
    precio_unitario: Decimal
    cantidad: int
    subtotal: Decimal
    moneda: str
    
    @classmethod
    def desde_value_object(cls, item: ItemCarrito) -> 'ItemCarritoDTO':
        """Crea DTO desde Value Object"""
        return cls(
            producto_id=item.producto_id,
            sku=item.sku,
            nombre=item.nombre_snapshot,
            precio_unitario=item.precio_unitario_snapshot.monto,
            cantidad=item.cantidad,
            subtotal=item.subtotal.monto,
            moneda=item.precio_unitario_snapshot.moneda
        )


@dataclass
class CarritoDTO:
    """DTO de salida para Carrito completo"""
    id: UUID
    usuario_id: UUID
    estado: str
    items: List[ItemCarritoDTO]
    cantidad_items: int
    cantidad_productos: int
    total_bruto: Decimal
    total_descuentos: Decimal
    total_final: Decimal
    moneda: str
    version: int
    expira_en: datetime
    esta_vacio: bool
    permite_modificaciones: bool
    fecha_creacion: datetime
    fecha_modificacion: datetime
    
    @classmethod
    def desde_entidad(cls, carrito: Carrito) -> 'CarritoDTO':
        """Crea DTO desde entidad Carrito"""
        items_dto = [
            ItemCarritoDTO.desde_value_object(item)
            for item in carrito.items
        ]
        
        return cls(
            id=carrito.id,
            usuario_id=carrito.usuario_id,
            estado=carrito.estado.value,
            items=items_dto,
            cantidad_items=carrito.cantidad_items,
            cantidad_productos=carrito.cantidad_productos,
            total_bruto=carrito.total_bruto.monto,
            total_descuentos=carrito.total_descuentos.monto,
            total_final=carrito.total_final.monto,
            moneda=carrito.moneda,
            version=carrito.version,
            expira_en=carrito.expira_en,
            esta_vacio=carrito.esta_vacio,
            permite_modificaciones=carrito.estado.permite_modificaciones,
            fecha_creacion=carrito.fecha_creacion,
            fecha_modificacion=carrito.fecha_modificacion
        )


@dataclass
class CarritoResumenDTO:
    """DTO resumido del carrito (para header/badge)"""
    id: UUID
    cantidad_items: int
    total_final: Decimal
    moneda: str
    estado: str
    
    @classmethod
    def desde_entidad(cls, carrito: Carrito) -> 'CarritoResumenDTO':
        """Crea DTO resumen desde entidad"""
        return cls(
            id=carrito.id,
            cantidad_items=carrito.cantidad_items,
            total_final=carrito.total_final.monto,
            moneda=carrito.moneda,
            estado=carrito.estado.value
        )


@dataclass
class OperacionCarritoResultadoDTO:
    """DTO para resultado de operaciones en carrito"""
    exito: bool
    mensaje: str
    carrito: Optional[CarritoDTO] = None
    
    @classmethod
    def exitoso(cls, carrito: Carrito, mensaje: str) -> 'OperacionCarritoResultadoDTO':
        return cls(
            exito=True,
            mensaje=mensaje,
            carrito=CarritoDTO.desde_entidad(carrito)
        )
    
    @classmethod
    def fallido(cls, mensaje: str) -> 'OperacionCarritoResultadoDTO':
        return cls(
            exito=False,
            mensaje=mensaje,
            carrito=None
        )
