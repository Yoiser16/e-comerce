"""
Entidad base del dominio
"""
from abc import ABC
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class EntidadBase(ABC):
    """
    Clase base para todas las entidades del dominio.
    
    Responsabilidades:
    - Identidad única (UUID)
    - Auditoría básica (creación, modificación)
    - Igualdad por identidad
    """
    
    def __init__(
        self,
        id: Optional[UUID] = None,
        fecha_creacion: Optional[datetime] = None,
        fecha_modificacion: Optional[datetime] = None,
        activo: bool = True
    ):
        self._id = id or uuid4()
        self._fecha_creacion = fecha_creacion or datetime.now()
        self._fecha_modificacion = fecha_modificacion or datetime.now()
        self._activo = activo
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion
    
    @property
    def fecha_modificacion(self) -> datetime:
        return self._fecha_modificacion
    
    @property
    def activo(self) -> bool:
        return self._activo
    
    @activo.setter
    def activo(self, valor: bool) -> None:
        """Actualiza el estado activo/inactivo"""
        self._activo = valor
        self.marcar_modificado()
    
    def marcar_modificado(self) -> None:
        """Actualiza la fecha de modificación"""
        self._fecha_modificacion = datetime.now()
    
    def desactivar(self) -> None:
        """Desactivación lógica"""
        self._activo = False
        self.marcar_modificado()
    
    def activar(self) -> None:
        """Reactivación"""
        self._activo = True
        self.marcar_modificado()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, EntidadBase):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
