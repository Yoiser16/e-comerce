"""
Entidad Producto
"""
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from .base import EntidadBase
from ..value_objects.dinero import Dinero
from ..value_objects.codigo_producto import CodigoProducto


class Producto(EntidadBase):
    """
    Representa un producto del catálogo.
    
    Responsabilidades:
    - Mantener información del producto
    - Controlar disponibilidad y stock
    - Aplicar reglas de pricing
    
    Punto de extensión: estrategias de pricing, gestión de inventario
    """
    
    def __init__(
        self,
        codigo: CodigoProducto,
        nombre: str,
        descripcion: str,
        precio: Dinero,
        stock_actual: int = 0,
        stock_minimo: int = 0,
        id: Optional[UUID] = None,
        fecha_creacion: Optional[datetime] = None,
        fecha_modificacion: Optional[datetime] = None,
        activo: bool = True
    ):
        super().__init__(id, fecha_creacion, fecha_modificacion, activo)
        self._codigo = codigo
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio = precio
        self._stock_actual = stock_actual
        self._stock_minimo = stock_minimo
    
    @property
    def codigo(self) -> CodigoProducto:
        return self._codigo
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @property
    def precio(self) -> Dinero:
        return self._precio
    
    @property
    def stock_actual(self) -> int:
        return self._stock_actual
    
    @property
    def stock_minimo(self) -> int:
        return self._stock_minimo
    
    @property
    def disponible(self) -> bool:
        """Verifica si el producto está disponible para venta"""
        return self._activo and self._stock_actual > 0
    
    @property
    def requiere_reabastecimiento(self) -> bool:
        """Verifica si el stock está bajo el mínimo"""
        return self._stock_actual <= self._stock_minimo
    
    def actualizar_precio(self, nuevo_precio: Dinero) -> None:
        """Actualiza el precio del producto"""
        self._precio = nuevo_precio
        self.marcar_modificado()
    
    def ajustar_stock(self, cantidad: int) -> None:
        """Ajusta el stock (puede ser positivo o negativo)"""
        self._stock_actual += cantidad
        self.marcar_modificado()
