"""
Enumeración de estados de Orden
"""
from enum import Enum


class EstadoOrden(Enum):
    """
    Estados posibles de una Orden.
    
    Máquina de estados:
    PENDIENTE -> CONFIRMADA -> EN_PROCESO -> ENVIADA -> COMPLETADA
         |           |             |            |
         v           v             v            v
                      CANCELADA
    
    PENDIENTE: Orden creada desde checkout (WhatsApp/Asesor)
    CONFIRMADA: Pago verificado o confirmado por asesor
    EN_PROCESO: En preparación/empaque
    ENVIADA: Despachada al cliente
    COMPLETADA: Entregada exitosamente
    CANCELADA: Orden cancelada
    """
    
    PENDIENTE = "pendiente"
    BORRADOR = "borrador"
    CONFIRMADA = "confirmada"
    EN_PROCESO = "en_proceso"
    ENVIADA = "enviada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    
    def puede_transicionar_a(self, nuevo_estado: 'EstadoOrden') -> bool:
        """
        Valida si es posible transicionar al nuevo estado.
        """
        transiciones_validas = {
            EstadoOrden.PENDIENTE: [EstadoOrden.CONFIRMADA, EstadoOrden.CANCELADA],
            EstadoOrden.BORRADOR: [EstadoOrden.CONFIRMADA, EstadoOrden.CANCELADA],
            EstadoOrden.CONFIRMADA: [EstadoOrden.EN_PROCESO, EstadoOrden.CANCELADA],
            EstadoOrden.EN_PROCESO: [EstadoOrden.ENVIADA, EstadoOrden.CANCELADA],
            EstadoOrden.ENVIADA: [EstadoOrden.COMPLETADA, EstadoOrden.CANCELADA],
            EstadoOrden.COMPLETADA: [],
            EstadoOrden.CANCELADA: [],
        }
        
        return nuevo_estado in transiciones_validas.get(self, [])
