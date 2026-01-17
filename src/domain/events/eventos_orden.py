"""
Eventos relacionados con Orden
"""
from uuid import UUID
from decimal import Decimal
from .base import EventoDominio


class OrdenCreada(EventoDominio):
    """
    Evento: Se ha creado una nueva orden.
    """
    
    def __init__(self, orden_id: UUID, cliente_id: UUID):
        super().__init__()
        self.orden_id = orden_id
        self.cliente_id = cliente_id


class OrdenConfirmada(EventoDominio):
    """
    Evento: Se ha confirmado una orden.
    Punto de extensión: iniciar procesamiento, reservar stock, notificaciones
    """
    
    def __init__(self, orden_id: UUID, total: Decimal):
        super().__init__()
        self.orden_id = orden_id
        self.total = total


class OrdenProcesada(EventoDominio):
    """
    Evento: Una orden está siendo procesada.
    """
    
    def __init__(self, orden_id: UUID):
        super().__init__()
        self.orden_id = orden_id


class OrdenCompletada(EventoDominio):
    """
    Evento: Una orden ha sido completada.
    """
    
    def __init__(self, orden_id: UUID):
        super().__init__()
        self.orden_id = orden_id


class OrdenCancelada(EventoDominio):
    """
    Evento: Una orden ha sido cancelada.
    Punto de extensión: liberar stock, reembolsos, notificaciones
    """
    
    def __init__(self, orden_id: UUID, razon: str = None):
        super().__init__()
        self.orden_id = orden_id
        self.razon = razon
