"""
Value Object Dinero
"""
from decimal import Decimal, ROUND_HALF_UP
from .base import ValueObject
from ..exceptions.dominio import ValorInvalido


class Dinero(ValueObject):
    """
    Value Object para representar valores monetarios.
    
    Responsabilidades:
    - Garantizar precisión decimal
    - Manejar moneda
    - Operaciones aritméticas seguras
    - Redondeo consistente
    """
    
    def __init__(self, monto: Decimal, moneda: str = "USD"):
        if not isinstance(monto, Decimal):
            raise ValorInvalido("El monto debe ser un Decimal")
        
        if monto < 0:
            raise ValorInvalido("El monto no puede ser negativo")
        
        if not moneda or len(moneda) != 3:
            raise ValorInvalido("La moneda debe ser código ISO de 3 letras")
        
        # Redondear a 2 decimales
        self._monto = monto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self._moneda = moneda.upper()
    
    @property
    def monto(self) -> Decimal:
        return self._monto
    
    @property
    def moneda(self) -> str:
        return self._moneda
    
    def sumar(self, otro: 'Dinero') -> 'Dinero':
        """Suma dos cantidades de dinero"""
        if self._moneda != otro._moneda:
            raise ValorInvalido(
                f"No se pueden sumar monedas diferentes: {self._moneda} y {otro._moneda}"
            )
        return Dinero(self._monto + otro._monto, self._moneda)
    
    def restar(self, otro: 'Dinero') -> 'Dinero':
        """Resta dos cantidades de dinero"""
        if self._moneda != otro._moneda:
            raise ValorInvalido(
                f"No se pueden restar monedas diferentes: {self._moneda} y {otro._moneda}"
            )
        
        resultado = self._monto - otro._monto
        if resultado < 0:
            raise ValorInvalido("El resultado no puede ser negativo")
        
        return Dinero(resultado, self._moneda)
    
    def multiplicar(self, factor: Decimal) -> 'Dinero':
        """Multiplica el monto por un factor"""
        if factor < 0:
            raise ValorInvalido("El factor no puede ser negativo")
        
        return Dinero(self._monto * factor, self._moneda)
    
    def __str__(self) -> str:
        return f"{self._monto} {self._moneda}"
