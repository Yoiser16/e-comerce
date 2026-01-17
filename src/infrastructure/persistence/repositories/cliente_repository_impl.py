"""
Implementación del repositorio de Cliente
"""
from typing import Optional, List
from uuid import UUID

from ....domain.repositories.cliente_repository import ClienteRepository
from ....domain.entities.cliente import Cliente
from ....domain.value_objects.email import Email
from ....domain.value_objects.documento_identidad import DocumentoIdentidad


class ClienteRepositoryImpl(ClienteRepository):
    """
    Implementación del repositorio de Cliente.
    
    Punto de extensión: implementar con Django ORM, SQLAlchemy, etc.
    """
    
    def obtener_por_id(self, id: UUID) -> Optional[Cliente]:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
    
    def obtener_todos(self, limite: int = 100, offset: int = 0) -> List[Cliente]:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
    
    def guardar(self, entidad: Cliente) -> Cliente:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
    
    def eliminar(self, id: UUID) -> bool:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
    
    def existe(self, id: UUID) -> bool:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
    
    def obtener_por_email(self, email: Email) -> Optional[Cliente]:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
    
    def obtener_por_documento(self, documento: DocumentoIdentidad) -> Optional[Cliente]:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
    
    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
    
    def obtener_activos(self) -> List[Cliente]:
        """Implementar con ORM"""
        raise NotImplementedError("Pendiente implementación con ORM")
