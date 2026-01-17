"""
Sistema de permisos y autorización
"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from dataclasses import dataclass


@dataclass
class UsuarioActual:
    """
    Representa al usuario autenticado actual.
    Punto de extensión: integración con sistema de autenticación
    """
    id: UUID
    username: str
    email: str
    roles: list[str]
    permisos: list[str]


class PermissionChecker(ABC):
    """
    Clase base para verificación de permisos.
    
    Responsabilidades:
    - Verificar autorización
    - Control de acceso basado en roles (RBAC)
    - Control de acceso basado en atributos (ABAC)
    
    Punto de extensión: integración con IAM, OAuth2, JWT
    """
    
    @abstractmethod
    def tiene_permiso(self, usuario: UsuarioActual, permiso: str) -> bool:
        """Verifica si el usuario tiene un permiso específico"""
        pass
    
    @abstractmethod
    def tiene_rol(self, usuario: UsuarioActual, rol: str) -> bool:
        """Verifica si el usuario tiene un rol específico"""
        pass
    
    @abstractmethod
    def puede_acceder_recurso(
        self,
        usuario: UsuarioActual,
        recurso_tipo: str,
        recurso_id: UUID,
        accion: str
    ) -> bool:
        """Verifica si el usuario puede acceder a un recurso específico"""
        pass
