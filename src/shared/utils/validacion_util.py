"""
Utilidades de validación
"""
import re
from typing import Any, Optional


class ValidacionUtil:
    """
    Utilidades comunes de validación.
    """
    
    @staticmethod
    def es_email_valido(email: str) -> bool:
        """Valida formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, email))
    
    @staticmethod
    def es_telefono_valido(telefono: str) -> bool:
        """Valida formato básico de teléfono"""
        solo_digitos = re.sub(r'[^\d+]', '', telefono)
        return len(solo_digitos) >= 8
    
    @staticmethod
    def no_nulo(valor: Any, nombre_campo: str = "Campo") -> Any:
        """Valida que un valor no sea nulo"""
        if valor is None:
            raise ValueError(f"{nombre_campo} no puede ser nulo")
        return valor
    
    @staticmethod
    def no_vacio(valor: str, nombre_campo: str = "Campo") -> str:
        """Valida que una cadena no esté vacía"""
        if not valor or not valor.strip():
            raise ValueError(f"{nombre_campo} no puede estar vacío")
        return valor.strip()
    
    @staticmethod
    def en_rango(valor: int, minimo: int, maximo: int, nombre_campo: str = "Valor") -> int:
        """Valida que un número esté en un rango"""
        if valor < minimo or valor > maximo:
            raise ValueError(f"{nombre_campo} debe estar entre {minimo} y {maximo}")
        return valor
