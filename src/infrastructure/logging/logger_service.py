"""
Sistema de logging centralizado
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class LoggerService:
    """
    Servicio centralizado de logging.
    
    Responsabilidades:
    - Logging estructurado
    - Contexto de trazabilidad (correlation ID)
    - Integración con sistemas externos (ELK, CloudWatch, etc.)
    
    Punto de extensión: integración con observability platforms
    """
    
    def __init__(self, nombre: str):
        self._logger = logging.getLogger(nombre)
        self._contexto: Dict[str, Any] = {}
    
    def establecer_contexto(
        self,
        correlation_id: Optional[UUID] = None,
        usuario_id: Optional[UUID] = None,
        **kwargs
    ) -> None:
        """Establece contexto de logging para trazabilidad"""
        if correlation_id:
            self._contexto['correlation_id'] = str(correlation_id)
        if usuario_id:
            self._contexto['usuario_id'] = str(usuario_id)
        self._contexto.update(kwargs)
    
    def info(self, mensaje: str, **kwargs) -> None:
        """Log de nivel INFO"""
        self._log(logging.INFO, mensaje, **kwargs)
    
    def warning(self, mensaje: str, **kwargs) -> None:
        """Log de nivel WARNING"""
        self._log(logging.WARNING, mensaje, **kwargs)
    
    def error(self, mensaje: str, excepcion: Optional[Exception] = None, **kwargs) -> None:
        """Log de nivel ERROR"""
        if excepcion:
            kwargs['excepcion'] = str(excepcion)
            kwargs['tipo_excepcion'] = excepcion.__class__.__name__
        self._log(logging.ERROR, mensaje, **kwargs)
    
    def debug(self, mensaje: str, **kwargs) -> None:
        """Log de nivel DEBUG"""
        self._log(logging.DEBUG, mensaje, **kwargs)
    
    def _log(self, nivel: int, mensaje: str, **kwargs) -> None:
        """Método interno de logging con contexto"""
        datos = {
            'timestamp': datetime.now().isoformat(),
            'mensaje': mensaje,
            **self._contexto,
            **kwargs
        }
        
        # Logging estructurado (JSON)
        self._logger.log(nivel, str(datos))
