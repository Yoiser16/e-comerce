"""
Value Object Email
"""
import re
from .base import ValueObject
from ..exceptions.dominio import ValorInvalido


class Email(ValueObject):
    """
    Value Object para direcciones de email.
    
    Responsabilidades:
    - Validar formato de email
    - Normalizar (lowercase)
    - Garantizar inmutabilidad
    """
    
    _EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(self, valor: str):
        valor_normalizado = valor.strip().lower()
        
        if not valor_normalizado:
            raise ValorInvalido("El email no puede estar vacío")
        
        if not self._EMAIL_REGEX.match(valor_normalizado):
            raise ValorInvalido(f"Email inválido: {valor}")
        
        self._valor = valor_normalizado
    
    @property
    def valor(self) -> str:
        return self._valor
    
    def __str__(self) -> str:
        return self._valor
