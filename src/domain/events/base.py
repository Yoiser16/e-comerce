"""
Evento de dominio base
"""
from abc import ABC
from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, Any


class EventoDominio(ABC):
    """
    Clase base para eventos del dominio.
    
    Responsabilidades:
    - Representar algo que ha ocurrido en el dominio
    - Inmutabilidad
    - Trazabilidad (timestamp, ID)
    
    Punto de extensión: event sourcing, arquitectura event-driven
    """
    
    def __init__(self):
        self._evento_id: UUID = uuid4()
        self._ocurrido_en: datetime = datetime.now()
    
    @property
    def evento_id(self) -> UUID:
        return self._evento_id
    
    @property
    def ocurrido_en(self) -> datetime:
        return self._ocurrido_en
    
    @property
    def nombre_evento(self) -> str:
        """Retorna el nombre del evento"""
        return self.__class__.__name__
    
    def a_dict(self) -> Dict[str, Any]:
        """
        Serializa el evento a diccionario.
        Punto de extensión: integración con message brokers
        """
        return {
            "evento_id": str(self._evento_id),
            "nombre_evento": self.nombre_evento,
            "ocurrido_en": self._ocurrido_en.isoformat()
        }
