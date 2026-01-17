"""
Enumeración de estados de Orden
"""
from enum import Enum


class EstadoOrden(Enum):
    """
    Estados posibles de una Orden.
    
    Máquina de estados:
    BORRADOR -> CONFIRMADA -> EN_PROCESO -> COMPLETADA
                    |
                    v
                CANCELADA
    
    Punto de extensión: agregar estados según flujo de negocio
    """
    
    BORRADOR = "borrador"
    CONFIRMADA = "confirmada"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    
    def puede_transicionar_a(self, nuevo_estado: 'EstadoOrden') -> bool:
        """
        Valida si es posible transicionar al nuevo estado.
        Punto de extensión: implementar validaciones de estado
        """
        transiciones_validas = {
            EstadoOrden.BORRADOR: [EstadoOrden.CONFIRMADA, EstadoOrden.CANCELADA],
            EstadoOrden.CONFIRMADA: [EstadoOrden.EN_PROCESO, EstadoOrden.CANCELADA],
            EstadoOrden.EN_PROCESO: [EstadoOrden.COMPLETADA, EstadoOrden.CANCELADA],
            EstadoOrden.COMPLETADA: [],
            EstadoOrden.CANCELADA: [],
        }
        
        return nuevo_estado in transiciones_validas.get(self, [])
