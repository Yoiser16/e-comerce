"""
Caso de uso base
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TRequest = TypeVar('TRequest')
TResponse = TypeVar('TResponse')


class CasoUsoBase(ABC, Generic[TRequest, TResponse]):
    """
    Clase base para casos de uso.
    
    Responsabilidades:
    - Orquestar flujo de negocio
    - Coordinar repositorios y servicios
    - Manejar transaccionalidad
    - Emitir eventos de dominio
    
    Punto de extensión: logging, autorización, validación transversal
    """
    
    @abstractmethod
    def ejecutar(self, request: TRequest) -> TResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            request: Datos de entrada del caso de uso
            
        Returns:
            Resultado de la ejecución
        """
        pass
