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
        activo: bool = True,
        categoria: Optional[str] = None,
        imagen_principal: Optional[str] = None,
        color: Optional[str] = None,
        tipo: Optional[str] = None,
        largo: Optional[str] = None,
        origen: Optional[str] = None,
        metodo: Optional[str] = None,
        calidad: Optional[str] = None
    ):
        super().__init__(id, fecha_creacion, fecha_modificacion, activo)
        self._codigo = codigo
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio = precio
        self._stock_actual = stock_actual
        self._stock_minimo = stock_minimo
        self._categoria = categoria
        self._imagen_principal = imagen_principal
        self._color = color
        self._tipo = tipo
        self._largo = largo
        self._origen = origen
        self._metodo = metodo
        self._calidad = calidad
    
    @property
    def categoria(self) -> Optional[str]:
        return self._categoria
    
    @categoria.setter
    def categoria(self, valor: Optional[str]) -> None:
        self._categoria = valor
        self.marcar_modificado()
    
    @property
    def imagen_principal(self) -> Optional[str]:
        return self._imagen_principal
    
    @imagen_principal.setter
    def imagen_principal(self, valor: Optional[str]) -> None:
        self._imagen_principal = valor
        self.marcar_modificado()
    
    @property
    def color(self) -> Optional[str]:
        return self._color
    
    @property
    def tipo(self) -> Optional[str]:
        return self._tipo
    
    @property
    def largo(self) -> Optional[str]:
        return self._largo
    
    @property
    def origen(self) -> Optional[str]:
        return self._origen
    
    @property
    def metodo(self) -> Optional[str]:
        return self._metodo
    
    @property
    def calidad(self) -> Optional[str]:
        return self._calidad
    
    @property
    def codigo(self) -> CodigoProducto:
        return self._codigo
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Actualiza el nombre del producto"""
        self._nombre = valor
        self.marcar_modificado()
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        """Actualiza la descripción del producto"""
        self._descripcion = valor
        self.marcar_modificado()
    
    @property
    def precio(self) -> Dinero:
        return self._precio
    
    @precio.setter
    def precio(self, valor: Dinero) -> None:
        """Actualiza el precio del producto"""
        self._precio = valor
        self.marcar_modificado()
    
    @property
    def stock_actual(self) -> int:
        return self._stock_actual
    
    @stock_actual.setter
    def stock_actual(self, valor: int) -> None:
        """Actualiza el stock actual"""
        self._stock_actual = valor
        self.marcar_modificado()
    
    @property
    def stock_minimo(self) -> int:
        return self._stock_minimo
    
    @stock_minimo.setter
    def stock_minimo(self, valor: int) -> None:
        """Actualiza el stock mínimo"""
        self._stock_minimo = valor
        self.marcar_modificado()
    
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
