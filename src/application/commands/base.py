"""
Command base - Patrón CQRS
"""
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


@dataclass(frozen=True)
class Command(ABC):
    """
    Clase base para comandos (CQRS).
    
    Responsabilidades:
    - Representar intención de cambiar el estado del sistema
    - Inmutabilidad
    - Trazabilidad
    
    Punto de extensión: command bus, validaciones, autorización
    """
    command_id: UUID = None
    timestamp: datetime = None
    usuario_id: Optional[UUID] = None
    
    def __post_init__(self):
        # Asignar valores por defecto si no se proporcionan
        if self.command_id is None:
            object.__setattr__(self, 'command_id', uuid4())
        if self.timestamp is None:
            object.__setattr__(self, 'timestamp', datetime.now())
