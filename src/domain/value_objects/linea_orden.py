"""
Value Object Línea de Orden
"""
from decimal import Decimal
from uuid import UUID
from .base import ValueObject
from .dinero import Dinero
from ..exceptions.dominio import ValorInvalido


class LineaOrden(ValueObject):
    """
    Value Object para una línea de orden.
    
    Responsabilidades:
    - Mantener producto, cantidad y precio
    - Calcular subtotal
    - Validar cantidades
    """
    
    def __init__(
        self,
        producto_id: UUID,
        cantidad: int,
        precio_unitario: Dinero
    ):
        if cantidad <= 0:
            raise ValorInvalido("La cantidad debe ser mayor a cero")
        
        self._producto_id = producto_id
        self._cantidad = cantidad
        self._precio_unitario = precio_unitario
    
    @property
    def producto_id(self) -> UUID:
        return self._producto_id
    
    @property
    def cantidad(self) -> int:
        return self._cantidad
    
    @property
    def precio_unitario(self) -> Dinero:
        return self._precio_unitario
    
    @property
    def subtotal(self) -> Dinero:
        """Calcula el subtotal de la línea"""
        return self._precio_unitario.multiplicar(Decimal(self._cantidad))
    
    def __str__(self) -> str:
        return f"Producto {self._producto_id}: {self._cantidad} x {self._precio_unitario} = {self.subtotal}"
