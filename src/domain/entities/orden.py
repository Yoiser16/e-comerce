"""
Entidad Orden
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from .base import EntidadBase
from ..value_objects.dinero import Dinero
from ..value_objects.linea_orden import LineaOrden
from ..exceptions.dominio import ReglaNegocioViolada
from ...shared.enums.estados import EstadoOrden


class Orden(EntidadBase):
    """
    Representa una orden de compra/venta.
    
    Responsabilidades:
    - Gestionar líneas de la orden
    - Calcular totales
    - Controlar flujo de estados
    - Aplicar reglas de negocio transaccionales
    
    Punto de extensión: máquina de estados, validaciones por estado, políticas de descuento
    """
    
    def __init__(
        self,
        cliente_id: UUID,
        lineas: Optional[List[LineaOrden]] = None,
        estado: EstadoOrden = EstadoOrden.BORRADOR,
        id: Optional[UUID] = None,
        fecha_creacion: Optional[datetime] = None,
        fecha_modificacion: Optional[datetime] = None,
        activo: bool = True
    ):
        super().__init__(id, fecha_creacion, fecha_modificacion, activo)
        self._cliente_id = cliente_id
        self._lineas = lineas or []
        self._estado = estado
    
    @property
    def cliente_id(self) -> UUID:
        return self._cliente_id
    
    @property
    def lineas(self) -> List[LineaOrden]:
        return self._lineas.copy()
    
    @property
    def estado(self) -> EstadoOrden:
        return self._estado
    
    @property
    def total(self) -> Dinero:
        """Calcula el total de la orden"""
        if not self._lineas:
            return Dinero(Decimal("0.00"), "USD")
        
        total = sum(linea.subtotal.monto for linea in self._lineas)
        return Dinero(total, self._lineas[0].subtotal.moneda)
    
    @property
    def cantidad_items(self) -> int:
        """Cantidad total de items en la orden"""
        return sum(linea.cantidad for linea in self._lineas)
    
    def agregar_linea(self, linea: LineaOrden) -> None:
        """Agrega una línea a la orden"""
        if self._estado != EstadoOrden.BORRADOR:
            raise ReglaNegocioViolada(
                "Solo se pueden agregar líneas a órdenes en estado borrador"
            )
        
        self._lineas.append(linea)
        self.marcar_modificado()
    
    def confirmar(self) -> None:
        """Confirma la orden (transición de estado)"""
        if self._estado != EstadoOrden.BORRADOR:
            raise ReglaNegocioViolada(
                "Solo se pueden confirmar órdenes en estado borrador"
            )
        
        if not self._lineas:
            raise ReglaNegocioViolada(
                "No se puede confirmar una orden sin líneas"
            )
        
        self._estado = EstadoOrden.CONFIRMADA
        self.marcar_modificado()
    
    def procesar(self) -> None:
        """Procesa la orden (transición de estado)"""
        if self._estado != EstadoOrden.CONFIRMADA:
            raise ReglaNegocioViolada(
                "Solo se pueden procesar órdenes confirmadas"
            )
        
        self._estado = EstadoOrden.EN_PROCESO
        self.marcar_modificado()
    
    def completar(self) -> None:
        """Completa la orden (transición de estado)"""
        if self._estado != EstadoOrden.EN_PROCESO:
            raise ReglaNegocioViolada(
                "Solo se pueden completar órdenes en proceso"
            )
        
        self._estado = EstadoOrden.COMPLETADA
        self.marcar_modificado()
    
    def cancelar(self) -> None:
        """Cancela la orden (transición de estado)"""
        if self._estado in [EstadoOrden.COMPLETADA, EstadoOrden.CANCELADA]:
            raise ReglaNegocioViolada(
                "No se puede cancelar una orden completada o ya cancelada"
            )
        
        self._estado = EstadoOrden.CANCELADA
        self.marcar_modificado()
