"""
Política base del dominio
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class PoliticaNegocio(ABC, Generic[T]):
    """
    Clase base para políticas de negocio.
    
    Responsabilidades:
    - Encapsular reglas de negocio reutilizables
    - Permitir composición de políticas
    - Facilitar testing de reglas
    
    Punto de extensión: políticas de descuentos, validaciones, estrategias
    """
    
    @abstractmethod
    def evaluar(self, contexto: T) -> bool:
        """
        Evalúa si la política se cumple.
        
        Args:
            contexto: Objeto o datos sobre los que se evalúa la política
            
        Returns:
            True si la política se cumple, False en caso contrario
        """
        pass
    
    @abstractmethod
    def mensaje_violacion(self) -> str:
        """
        Retorna el mensaje descriptivo cuando la política no se cumple.
        """
        pass
