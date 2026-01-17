"""
Event Bus - Bus de eventos para arquitectura event-driven
"""
from abc import ABC, abstractmethod
from typing import List, Callable
from ...domain.events.base import EventoDominio


class EventBus(ABC):
    """
    Bus de eventos del dominio.
    
    Responsabilidades:
    - Publicar eventos de dominio
    - Suscribir handlers a eventos
    - Desacoplar productores de consumidores
    
    Punto de extensión: implementación con message broker
    """
    
    @abstractmethod
    def publicar(self, evento: EventoDominio) -> None:
        """Publica un evento"""
        pass
    
    @abstractmethod
    def suscribir(self, tipo_evento: type, handler: Callable[[EventoDominio], None]) -> None:
        """Suscribe un handler a un tipo de evento"""
        pass


class EventBusMemoria(EventBus):
    """
    Implementación en memoria del Event Bus.
    Para desarrollo y testing.
    """
    
    def __init__(self):
        self._suscriptores: dict = {}
    
    def publicar(self, evento: EventoDominio) -> None:
        """Publica un evento a todos los suscriptores"""
        tipo_evento = type(evento)
        
        if tipo_evento in self._suscriptores:
            for handler in self._suscriptores[tipo_evento]:
                handler(evento)
    
    def suscribir(self, tipo_evento: type, handler: Callable[[EventoDominio], None]) -> None:
        """Suscribe un handler"""
        if tipo_evento not in self._suscriptores:
            self._suscriptores[tipo_evento] = []
        
        self._suscriptores[tipo_evento].append(handler)
