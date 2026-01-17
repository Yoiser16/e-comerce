"""
Controlador base para FastAPI
"""
from abc import ABC


class ControladorBase(ABC):
    """
    Clase base para controladores FastAPI.
    
    Responsabilidades:
    - Manejar requests HTTP
    - Delegar a casos de uso
    - Transformar excepciones a respuestas HTTP
    - Validación de entrada
    
    Punto de extensión: middleware, autenticación, rate limiting
    """
    pass
