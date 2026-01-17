"""
Repositorio base (interfaz)
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List
from uuid import UUID

T = TypeVar('T')


class RepositorioBase(ABC, Generic[T]):
    """
    Interfaz base para todos los repositorios.
    
    Responsabilidades:
    - Definir contrato de persistencia
    - Independiente de tecnología de persistencia
    - Operaciones CRUD básicas
    
    Punto de extensión: implementaciones específicas (Django ORM, SQLAlchemy, etc.)
    """
    
    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Optional[T]:
        """
        Obtiene una entidad por su ID.
        
        Returns:
            La entidad si existe, None en caso contrario
        """
        pass
    
    @abstractmethod
    def obtener_todos(self, limite: int = 100, offset: int = 0) -> List[T]:
        """
        Obtiene todas las entidades con paginación.
        """
        pass
    
    @abstractmethod
    def guardar(self, entidad: T) -> T:
        """
        Guarda o actualiza una entidad.
        
        Returns:
            La entidad guardada
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: UUID) -> bool:
        """
        Elimina una entidad por su ID.
        
        Returns:
            True si se eliminó, False si no existía
        """
        pass
    
    @abstractmethod
    def existe(self, id: UUID) -> bool:
        """
        Verifica si existe una entidad con el ID dado.
        """
        pass
