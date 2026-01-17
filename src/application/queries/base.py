"""
Query base - Patrón CQRS
"""
from abc import ABC
from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class Query(ABC):
    """
    Clase base para queries (CQRS).
    
    Responsabilidades:
    - Representar intención de consultar datos
    - Inmutabilidad
    - Separación de lectura/escritura
    
    Punto de extensión: query bus, caching, proyecciones
    """
    usuario_id: Optional[UUID] = None
