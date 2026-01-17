"""
Value Object base
"""
from abc import ABC


class ValueObject(ABC):
    """
    Clase base para Value Objects.
    
    Responsabilidades:
    - Inmutabilidad
    - Igualdad por valor (no por identidad)
    - Validación en construcción
    """
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
    
    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))
    
    def __repr__(self) -> str:
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
