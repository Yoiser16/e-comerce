"""
Tipos de documento de identidad
"""
from enum import Enum


class TipoDocumento(Enum):
    """
    Tipos de documentos de identidad soportados.
    Punto de extensión: agregar según región/país
    """
    
    DNI = "DNI"
    PASAPORTE = "pasaporte"
    CEDULA = "cedula"
    RUC = "RUC"
    NIT = "NIT"
    RFC = "RFC"
    CUIT = "CUIT"
