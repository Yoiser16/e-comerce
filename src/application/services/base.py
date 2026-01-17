"""
Servicio de aplicación base
"""
from abc import ABC


class ServicioAplicacion(ABC):
    """
    Clase base para servicios de aplicación.
    
    Responsabilidades:
    - Lógica de aplicación que no pertenece a un caso de uso específico
    - Coordinación entre múltiples casos de uso
    - Servicios transversales (notificaciones, etc.)
    
    Punto de extensión: logging, transacciones, eventos
    """
    pass
