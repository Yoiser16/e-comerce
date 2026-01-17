"""
Value Object Código de Producto
"""
from .base import ValueObject
from ..exceptions.dominio import ValorInvalido


class CodigoProducto(ValueObject):
    """
    Value Object para códigos de producto (SKU).
    
    Responsabilidades:
    - Validar formato
    - Normalizar (uppercase)
    - Garantizar inmutabilidad
    """
    
    def __init__(self, valor: str):
        valor_normalizado = valor.strip().upper()
        
        if not valor_normalizado:
            raise ValorInvalido("El código de producto no puede estar vacío")
        
        if len(valor_normalizado) < 3:
            raise ValorInvalido("El código de producto debe tener al menos 3 caracteres")
        
        if not valor_normalizado.replace("-", "").replace("_", "").isalnum():
            raise ValorInvalido("El código de producto solo puede contener letras, números, guiones y guiones bajos")
        
        self._valor = valor_normalizado
    
    @property
    def valor(self) -> str:
        return self._valor
    
    def __str__(self) -> str:
        return self._valor
