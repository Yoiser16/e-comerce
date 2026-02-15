"""
Entidad ProductoVariante
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

from .base import EntidadBase
from ..value_objects.dinero import Dinero


@dataclass
class ProductoVariante(EntidadBase):
    """
    Variante de producto con precio y stock propios.
    """
    producto_id: UUID
    sku: str
    color: Optional[str]
    largo: Optional[str]
    precio: Dinero
    stock_actual: int
    stock_minimo: int
    cantidad_minima_mayorista: int
    imagen_url: Optional[str] = None
    activo: bool = True
    orden: int = 0

    def __init__(
        self,
        producto_id: UUID,
        sku: str,
        color: Optional[str],
        largo: Optional[str],
        precio: Dinero,
        stock_actual: int,
        stock_minimo: int,
        cantidad_minima_mayorista: int = 1,
        imagen_url: Optional[str] = None,
        activo: bool = True,
        orden: int = 0,
        id: Optional[UUID] = None,
        fecha_creacion: Optional[datetime] = None,
        fecha_modificacion: Optional[datetime] = None,
    ):
        super().__init__(id, fecha_creacion, fecha_modificacion, activo)
        self.producto_id = producto_id
        self.sku = sku
        self.color = color
        self.largo = largo
        self.precio = precio
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.cantidad_minima_mayorista = cantidad_minima_mayorista
        self.imagen_url = imagen_url
        self.orden = orden
