"""
Utilidades para fechas y timestamps
"""
from datetime import datetime, timedelta, timezone
from typing import Optional


class DateTimeUtil:
    """
    Utilidades para manejo de fechas y horas.
    
    Convenciones:
    - Siempre usar UTC internamente
    - Conversión a timezone local solo en presentación
    """
    
    @staticmethod
    def ahora_utc() -> datetime:
        """Retorna timestamp actual en UTC"""
        return datetime.now(timezone.utc)
    
    @staticmethod
    def desde_timestamp(timestamp: int) -> datetime:
        """Convierte timestamp Unix a datetime UTC"""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def a_timestamp(fecha: datetime) -> int:
        """Convierte datetime a timestamp Unix"""
        return int(fecha.timestamp())
    
    @staticmethod
    def agregar_dias(fecha: datetime, dias: int) -> datetime:
        """Agrega días a una fecha"""
        return fecha + timedelta(days=dias)
    
    @staticmethod
    def diferencia_dias(fecha1: datetime, fecha2: datetime) -> int:
        """Calcula diferencia en días entre dos fechas"""
        return (fecha2 - fecha1).days
    
    @staticmethod
    def es_mismo_dia(fecha1: datetime, fecha2: datetime) -> bool:
        """Verifica si dos fechas son del mismo día"""
        return fecha1.date() == fecha2.date()
