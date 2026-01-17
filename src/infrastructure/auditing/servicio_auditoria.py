"""
Servicio de auditoría
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


@dataclass
class RegistroAuditoria:
    """
    Registro de auditoría inmutable.
    
    Responsabilidades:
    - Registrar quién, qué, cuándo y dónde
    - Trazabilidad completa de operaciones
    - Soporte para cumplimiento normativo
    """
    id: UUID
    timestamp: datetime
    usuario_id: Optional[UUID]
    entidad_tipo: str
    entidad_id: UUID
    accion: str
    datos_previos: Optional[Dict[str, Any]]
    datos_nuevos: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    user_agent: Optional[str]
    resultado: str  # "EXITO", "FALLO"
    mensaje: Optional[str]


class ServicioAuditoria:
    """
    Servicio de auditoría para trazabilidad.
    
    Responsabilidades:
    - Registrar todas las operaciones críticas
    - Mantener historial inmutable
    - Facilitar investigación y compliance
    
    Punto de extensión: persistencia, búsqueda, reportes
    """
    
    def registrar(
        self,
        entidad_tipo: str,
        entidad_id: UUID,
        accion: str,
        usuario_id: Optional[UUID] = None,
        datos_previos: Optional[Dict[str, Any]] = None,
        datos_nuevos: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        resultado: str = "EXITO",
        mensaje: Optional[str] = None
    ) -> RegistroAuditoria:
        """
        Registra una operación auditable.
        
        Punto de extensión: implementar persistencia
        """
        registro = RegistroAuditoria(
            id=uuid4(),
            timestamp=datetime.now(),
            usuario_id=usuario_id,
            entidad_tipo=entidad_tipo,
            entidad_id=entidad_id,
            accion=accion,
            datos_previos=datos_previos,
            datos_nuevos=datos_nuevos,
            ip_address=ip_address,
            user_agent=user_agent,
            resultado=resultado,
            mensaje=mensaje
        )
        
        # Punto de extensión: persistir en base de datos de auditoría
        
        return registro
