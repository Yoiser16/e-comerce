"""
Eventos relacionados con Cliente
"""
from uuid import UUID
from .base import EventoDominio


class ClienteCreado(EventoDominio):
    """
    Evento: Se ha creado un nuevo cliente.
    Punto de extensión: notificaciones, integraciones, auditoría
    """
    
    def __init__(self, cliente_id: UUID, email: str):
        super().__init__()
        self.cliente_id = cliente_id
        self.email = email


class ClienteActualizado(EventoDominio):
    """
    Evento: Se ha actualizado un cliente.
    """
    
    def __init__(self, cliente_id: UUID):
        super().__init__()
        self.cliente_id = cliente_id


class ClienteDesactivado(EventoDominio):
    """
    Evento: Se ha desactivado un cliente.
    """
    
    def __init__(self, cliente_id: UUID):
        super().__init__()
        self.cliente_id = cliente_id
