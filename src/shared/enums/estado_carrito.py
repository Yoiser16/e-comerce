"""
Enumeración de estados del Carrito de Compras

State Machine:
    CREADO -> ACTIVO -> BLOQUEADO -> CONFIRMADO
                |           |
                v           v
            EXPIRADO    EXPIRADO

Estados inmutables: CONFIRMADO, EXPIRADO
"""
from enum import Enum


class EstadoCarrito(Enum):
    """
    Estados posibles del Carrito de Compras.
    
    Máquina de estados:
    - CREADO: Carrito recién inicializado
    - ACTIVO: Permite modificaciones (agregar, quitar, actualizar)
    - BLOQUEADO: Validación final, anti-race conditions, no permite modificaciones
    - CONFIRMADO: Carrito convertido a orden, INMUTABLE
    - EXPIRADO: Carrito abandonado/timeout, INMUTABLE
    """
    
    CREADO = "creado"
    ACTIVO = "activo"
    BLOQUEADO = "bloqueado"
    CONFIRMADO = "confirmado"
    EXPIRADO = "expirado"
    
    @property
    def permite_modificaciones(self) -> bool:
        """Indica si el estado permite agregar/quitar/actualizar items"""
        return self in (EstadoCarrito.CREADO, EstadoCarrito.ACTIVO)
    
    @property
    def es_inmutable(self) -> bool:
        """Indica si el carrito ya no puede cambiar de estado"""
        return self in (EstadoCarrito.CONFIRMADO, EstadoCarrito.EXPIRADO)
    
    @property
    def puede_bloquear(self) -> bool:
        """Indica si puede transicionar a BLOQUEADO"""
        return self == EstadoCarrito.ACTIVO
    
    @property
    def puede_confirmar(self) -> bool:
        """Indica si puede transicionar a CONFIRMADO"""
        return self == EstadoCarrito.BLOQUEADO
    
    @property
    def puede_expirar(self) -> bool:
        """Indica si puede transicionar a EXPIRADO"""
        return self in (EstadoCarrito.CREADO, EstadoCarrito.ACTIVO, EstadoCarrito.BLOQUEADO)
    
    def puede_transicionar_a(self, nuevo_estado: 'EstadoCarrito') -> bool:
        """
        Valida si es posible transicionar al nuevo estado.
        
        Transiciones válidas:
        - CREADO -> ACTIVO, EXPIRADO
        - ACTIVO -> BLOQUEADO, EXPIRADO
        - BLOQUEADO -> CONFIRMADO, EXPIRADO, ACTIVO (rollback)
        - CONFIRMADO -> (ninguna, inmutable)
        - EXPIRADO -> (ninguna, inmutable)
        """
        transiciones_validas = {
            EstadoCarrito.CREADO: [EstadoCarrito.ACTIVO, EstadoCarrito.EXPIRADO],
            EstadoCarrito.ACTIVO: [EstadoCarrito.BLOQUEADO, EstadoCarrito.EXPIRADO],
            EstadoCarrito.BLOQUEADO: [EstadoCarrito.CONFIRMADO, EstadoCarrito.EXPIRADO, EstadoCarrito.ACTIVO],
            EstadoCarrito.CONFIRMADO: [],
            EstadoCarrito.EXPIRADO: [],
        }
        
        return nuevo_estado in transiciones_validas.get(self, [])
