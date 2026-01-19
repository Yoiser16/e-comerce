"""
DTOs para estadísticas del dashboard
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class EstadisticasGeneralesDTO:
    """Estadísticas generales del sistema"""
    total_ventas: float
    total_ordenes: int
    ordenes_pendientes: int
    total_productos: int
    productos_activos: int
    stock_bajo: int
    total_clientes: int
    clientes_nuevos: int


@dataclass
class OrdenResumeDTO:
    """Resumen de una orden para el dashboard"""
    id: str
    cliente_nombre: str
    cliente_email: str
    estado: str
    total: float
    fecha_creacion: datetime
    tiempo_transcurrido: str


@dataclass
class ProductoStockBajoDTO:
    """Producto con stock bajo"""
    id: str
    nombre: str
    stock_actual: int
    stock_minimo: int
    precio: float
    imagen_url: Optional[str] = None
