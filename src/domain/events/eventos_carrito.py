"""
Eventos de Dominio del Carrito de Compras

Eventos preparados para:
- Auditoría
- Notificaciones
- Métricas
- Antifraude
- Integración con sistemas externos
"""
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional

from .base import EventoDominio


class CarritoCreado(EventoDominio):
    """
    Evento: Se ha creado un nuevo carrito para un usuario.
    
    Uso:
    - Iniciar timer de expiración
    - Métricas de carritos creados
    - Analytics de sesiones de compra
    """
    
    def __init__(self, carrito_id: UUID, usuario_id: UUID, expira_en: datetime):
        super().__init__()
        self.carrito_id = carrito_id
        self.usuario_id = usuario_id
        self.expira_en = expira_en


class ProductoAgregadoAlCarrito(EventoDominio):
    """
    Evento: Se ha agregado un producto al carrito.
    
    Uso:
    - Tracking de productos populares
    - Retargeting
    - Métricas de engagement
    - Auditoría de operaciones
    """
    
    def __init__(
        self,
        carrito_id: UUID,
        usuario_id: UUID,
        producto_id: UUID,
        sku: str,
        nombre_producto: str,
        cantidad: int,
        precio_unitario: Decimal,
        moneda: str
    ):
        super().__init__()
        self.carrito_id = carrito_id
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.sku = sku
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.moneda = moneda


class ProductoEliminadoDelCarrito(EventoDominio):
    """
    Evento: Se ha eliminado un producto del carrito.
    
    Uso:
    - Análisis de abandono
    - Detección de problemas de UX
    - Auditoría
    """
    
    def __init__(
        self,
        carrito_id: UUID,
        usuario_id: UUID,
        producto_id: UUID,
        sku: str,
        cantidad_eliminada: int
    ):
        super().__init__()
        self.carrito_id = carrito_id
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.sku = sku
        self.cantidad_eliminada = cantidad_eliminada


class CantidadProductoActualizada(EventoDominio):
    """
    Evento: Se ha actualizado la cantidad de un producto en el carrito.
    
    Uso:
    - Tracking de comportamiento
    - Análisis de indecisión
    - Auditoría
    """
    
    def __init__(
        self,
        carrito_id: UUID,
        usuario_id: UUID,
        producto_id: UUID,
        cantidad_anterior: int,
        cantidad_nueva: int
    ):
        super().__init__()
        self.carrito_id = carrito_id
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.cantidad_anterior = cantidad_anterior
        self.cantidad_nueva = cantidad_nueva


class PrecioProductoActualizadoEnCarrito(EventoDominio):
    """
    Evento: El precio de un producto en el carrito ha sido actualizado.
    
    Se dispara cuando hay sincronización de precios por cambio en catálogo.
    
    Uso:
    - Notificar al usuario del cambio de precio
    - Auditoría de cambios de precio
    - Antifraude (detección de manipulación)
    """
    
    def __init__(
        self,
        carrito_id: UUID,
        usuario_id: UUID,
        producto_id: UUID,
        precio_anterior: Decimal,
        precio_nuevo: Decimal,
        moneda: str
    ):
        super().__init__()
        self.carrito_id = carrito_id
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.precio_anterior = precio_anterior
        self.precio_nuevo = precio_nuevo
        self.moneda = moneda


class CarritoBloqueado(EventoDominio):
    """
    Evento: El carrito ha sido bloqueado para validación final.
    
    Uso:
    - Reservar stock temporalmente
    - Iniciar validación de inventario
    - Anti-race conditions en checkout
    - Métricas de intentos de checkout
    """
    
    def __init__(
        self,
        carrito_id: UUID,
        usuario_id: UUID,
        total_final: Decimal,
        moneda: str,
        cantidad_items: int
    ):
        super().__init__()
        self.carrito_id = carrito_id
        self.usuario_id = usuario_id
        self.total_final = total_final
        self.moneda = moneda
        self.cantidad_items = cantidad_items


class CarritoConfirmado(EventoDominio):
    """
    Evento: El carrito ha sido confirmado y convertido a orden.
    
    IDEMPOTENTE: Confirmar un carrito ya confirmado no genera error,
    pero tampoco genera evento duplicado.
    
    Uso:
    - Disparar creación de orden
    - Descontar stock definitivo
    - Métricas de conversión
    - Analytics de compra
    - Notificación de compra exitosa
    """
    
    def __init__(
        self,
        carrito_id: UUID,
        usuario_id: UUID,
        total_final: Decimal,
        moneda: str,
        cantidad_items: int,
        orden_id: Optional[UUID] = None
    ):
        super().__init__()
        self.carrito_id = carrito_id
        self.usuario_id = usuario_id
        self.total_final = total_final
        self.moneda = moneda
        self.cantidad_items = cantidad_items
        self.orden_id = orden_id  # Se asigna después de crear la orden


class CarritoExpirado(EventoDominio):
    """
    Evento: El carrito ha expirado por timeout o abandono.
    
    Uso:
    - Liberar stock reservado
    - Campañas de recuperación de carrito
    - Métricas de abandono
    - Análisis de comportamiento
    """
    
    def __init__(
        self,
        carrito_id: UUID,
        usuario_id: UUID,
        total_al_expirar: Decimal,
        moneda: str,
        cantidad_items: int,
        razon: str = "timeout"
    ):
        super().__init__()
        self.carrito_id = carrito_id
        self.usuario_id = usuario_id
        self.total_al_expirar = total_al_expirar
        self.moneda = moneda
        self.cantidad_items = cantidad_items
        self.razon = razon


class CarritoRecalculado(EventoDominio):
    """
    Evento: Los totales del carrito han sido recalculados.
    
    Uso:
    - Auditoría de recálculos
    - Detección de discrepancias
    - Sincronización con frontend
    """
    
    def __init__(
        self,
        carrito_id: UUID,
        total_bruto_anterior: Decimal,
        total_bruto_nuevo: Decimal,
        total_final_anterior: Decimal,
        total_final_nuevo: Decimal,
        moneda: str
    ):
        super().__init__()
        self.carrito_id = carrito_id
        self.total_bruto_anterior = total_bruto_anterior
        self.total_bruto_nuevo = total_bruto_nuevo
        self.total_final_anterior = total_final_anterior
        self.total_final_nuevo = total_final_nuevo
        self.moneda = moneda
