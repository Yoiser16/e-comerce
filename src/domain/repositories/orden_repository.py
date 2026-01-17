"""
Interfaz del Repositorio de Orden
"""
from abc import abstractmethod
from typing import List
from uuid import UUID
from .base import RepositorioBase
from ..entities.orden import Orden
from ...shared.enums.estados import EstadoOrden


class OrdenRepository(RepositorioBase[Orden]):
    """
    Contrato de persistencia para Orden.
    
    Punto de extensión: consultas por estado, cliente, fecha
    """
    
    @abstractmethod
    def obtener_por_cliente(self, cliente_id: UUID) -> List[Orden]:
        """Obtiene todas las órdenes de un cliente"""
        pass
    
    @abstractmethod
    def obtener_por_estado(self, estado: EstadoOrden) -> List[Orden]:
        """Obtiene órdenes por estado"""
        pass
    
    @abstractmethod
    def obtener_pendientes_procesamiento(self) -> List[Orden]:
        """Obtiene órdenes confirmadas pendientes de procesamiento"""
        pass
