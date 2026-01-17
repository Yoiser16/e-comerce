"""
Entidad Cliente
"""
from typing import Optional
from uuid import UUID
from datetime import datetime

from .base import EntidadBase
from ..value_objects.email import Email
from ..value_objects.telefono import Telefono
from ..value_objects.documento_identidad import DocumentoIdentidad


class Cliente(EntidadBase):
    """
    Representa un cliente del sistema.
    
    Responsabilidades:
    - Mantener información de identidad del cliente
    - Gestionar estado del cliente
    - Aplicar reglas de negocio sobre clientes
    
    Punto de extensión: validaciones de negocio, reglas de clasificación
    """
    
    def __init__(
        self,
        nombre: str,
        apellido: str,
        email: Email,
        documento: DocumentoIdentidad,
        telefono: Optional[Telefono] = None,
        id: Optional[UUID] = None,
        fecha_creacion: Optional[datetime] = None,
        fecha_modificacion: Optional[datetime] = None,
        activo: bool = True
    ):
        super().__init__(id, fecha_creacion, fecha_modificacion, activo)
        self._nombre = nombre
        self._apellido = apellido
        self._email = email
        self._documento = documento
        self._telefono = telefono
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def apellido(self) -> str:
        return self._apellido
    
    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"
    
    @property
    def email(self) -> Email:
        return self._email
    
    @property
    def documento(self) -> DocumentoIdentidad:
        return self._documento
    
    @property
    def telefono(self) -> Optional[Telefono]:
        return self._telefono
    
    def actualizar_email(self, nuevo_email: Email) -> None:
        """Actualiza el email del cliente"""
        self._email = nuevo_email
        self.marcar_modificado()
    
    def actualizar_telefono(self, nuevo_telefono: Telefono) -> None:
        """Actualiza el teléfono del cliente"""
        self._telefono = nuevo_telefono
        self.marcar_modificado()
