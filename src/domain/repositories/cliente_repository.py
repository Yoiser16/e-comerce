"""
Interfaz del Repositorio de Cliente
"""
from abc import abstractmethod
from typing import Optional, List
from .base import RepositorioBase
from ..entities.cliente import Cliente
from ..value_objects.email import Email
from ..value_objects.documento_identidad import DocumentoIdentidad


class ClienteRepository(RepositorioBase[Cliente]):
    """
    Contrato de persistencia para Cliente.
    
    Punto de extensión: consultas específicas de negocio
    """
    
    @abstractmethod
    def obtener_por_email(self, email: Email) -> Optional[Cliente]:
        """Busca un cliente por email"""
        pass
    
    @abstractmethod
    def obtener_por_documento(self, documento: DocumentoIdentidad) -> Optional[Cliente]:
        """Busca un cliente por documento de identidad"""
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por nombre (búsqueda parcial)"""
        pass
    
    @abstractmethod
    def obtener_activos(self) -> List[Cliente]:
        """Obtiene todos los clientes activos"""
        pass
