"""
Value Object Telefono
"""
import re
from .base import ValueObject
from ..exceptions.dominio import ValorInvalido


class Telefono(ValueObject):
    """
    Value Object para números telefónicos.
    
    Responsabilidades:
    - Validar formato
    - Normalizar (solo dígitos)
    - Garantizar inmutabilidad
    """
    
    def __init__(self, valor: str):
        # Normalizar: eliminar espacios, guiones, paréntesis
        valor_normalizado = re.sub(r'[^\d+]', '', valor.strip())
        
        if not valor_normalizado:
            raise ValorInvalido("El teléfono no puede estar vacío")
        
        if len(valor_normalizado) < 8:
            raise ValorInvalido("El teléfono debe tener al menos 8 dígitos")
        
        self._valor = valor_normalizado
    
    @property
    def valor(self) -> str:
        return self._valor
    
    def __str__(self) -> str:
        return self._valor
