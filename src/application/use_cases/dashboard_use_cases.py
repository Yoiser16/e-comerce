"""
Casos de uso para el dashboard administrativo
"""
from typing import List
from datetime import datetime, timedelta
from decimal import Decimal

from domain.repositories.orden_repository import OrdenRepository
from domain.repositories.producto_repository import ProductoRepository
from domain.repositories.cliente_repository import ClienteRepository

from application.dto.dashboard_dto import (
    EstadisticasGeneralesDTO,
    OrdenResumeDTO,
    ProductoStockBajoDTO
)


class ObtenerEstadisticasGeneralesUseCase:
    """Obtiene estadísticas generales del sistema"""
    
    def __init__(
        self,
        orden_repo: OrdenRepository,
        producto_repo: ProductoRepository,
        cliente_repo: ClienteRepository
    ):
        self.orden_repo = orden_repo
        self.producto_repo = producto_repo
        self.cliente_repo = cliente_repo
    
    def ejecutar(self) -> EstadisticasGeneralesDTO:
        """Calcula todas las estadísticas"""
        
        # Obtener todas las órdenes
        ordenes = self.orden_repo.obtener_todos(limite=10000)
        
        # Calcular total de ventas del mes actual
        mes_actual = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ordenes_mes = [o for o in ordenes if o.fecha_creacion and o.fecha_creacion >= mes_actual]
        
        # Calcular total de ventas (manejando Dinero y float)
        total_ventas = 0.0
        for o in ordenes_mes:
            if hasattr(o.total, 'monto'):
                total_ventas += float(o.total.monto)
            else:
                total_ventas += float(o.total)
        
        # Contar órdenes pendientes
        ordenes_pendientes = sum(1 for o in ordenes if o.estado.value == 'PENDIENTE')
        
        # Obtener productos
        productos = self.producto_repo.obtener_todos(limite=10000)
        productos_activos = [p for p in productos if p.activo]
        
        # Contar productos con stock bajo (menos de 5 unidades)
        stock_bajo = sum(1 for p in productos_activos if p.stock_actual < 5)
        
        # Obtener clientes
        clientes = self.cliente_repo.obtener_todos(limite=10000)
        
        # Clientes nuevos (últimos 30 días)
        hace_30_dias = datetime.now() - timedelta(days=30)
        clientes_nuevos = sum(1 for c in clientes if c.fecha_creacion and c.fecha_creacion >= hace_30_dias)
        
        return EstadisticasGeneralesDTO(
            total_ventas=total_ventas,
            total_ordenes=len(ordenes),
            ordenes_pendientes=ordenes_pendientes,
            total_productos=len(productos),
            productos_activos=len(productos_activos),
            stock_bajo=stock_bajo,
            total_clientes=len(clientes),
            clientes_nuevos=clientes_nuevos
        )


class ObtenerOrdenesRecientesUseCase:
    """Obtiene las órdenes más recientes"""
    
    def __init__(self, orden_repo: OrdenRepository, cliente_repo: ClienteRepository):
        self.orden_repo = orden_repo
        self.cliente_repo = cliente_repo
    
    def ejecutar(self, limite: int = 5) -> List[OrdenResumeDTO]:
        """Obtiene las últimas órdenes"""
        
        ordenes = self.orden_repo.obtener_todos(limite=1000)
        
        # Filtrar órdenes con fecha_creacion válida
        ordenes_con_fecha = [o for o in ordenes if o.fecha_creacion is not None]
        
        # Ordenar por fecha de creación descendente
        ordenes_recientes = sorted(
            ordenes_con_fecha,
            key=lambda o: o.fecha_creacion,
            reverse=True
        )[:limite]
        
        resultado = []
        for orden in ordenes_recientes:
            # Obtener cliente
            cliente = self.cliente_repo.obtener_por_id(orden.cliente_id)
            
            # Calcular tiempo transcurrido
            tiempo = self._calcular_tiempo_transcurrido(orden.fecha_creacion)
            
            resultado.append(OrdenResumeDTO(
                id=str(orden.id),
                cliente_nombre=cliente.nombre if cliente else "Cliente desconocido",
                cliente_email=cliente.email.valor if cliente else "",
                estado=orden.estado.value,
                total=float(orden.total),
                fecha_creacion=orden.fecha_creacion,
                tiempo_transcurrido=tiempo
            ))
        
        return resultado
    
    def _calcular_tiempo_transcurrido(self, fecha: datetime) -> str:
        """Calcula el tiempo transcurrido de forma legible"""
        if fecha is None:
            return "Fecha desconocida"
        
        ahora = datetime.now()
        
        # Asegurar que ambas fechas sean naive o ambas aware
        if fecha.tzinfo is not None and ahora.tzinfo is None:
            from datetime import timezone
            ahora = ahora.replace(tzinfo=timezone.utc)
        elif fecha.tzinfo is None and ahora.tzinfo is not None:
            ahora = ahora.replace(tzinfo=None)
        
        diferencia = ahora - fecha
        
        if diferencia.days > 0:
            if diferencia.days == 1:
                return "Ayer"
            elif diferencia.days < 7:
                return f"Hace {diferencia.days} días"
            elif diferencia.days < 30:
                semanas = diferencia.days // 7
                return f"Hace {semanas} semana{'s' if semanas > 1 else ''}"
            else:
                meses = diferencia.days // 30
                return f"Hace {meses} mes{'es' if meses > 1 else ''}"
        
        horas = diferencia.seconds // 3600
        if horas > 0:
            return f"Hace {horas} hora{'s' if horas > 1 else ''}"
        
        minutos = diferencia.seconds // 60
        if minutos > 0:
            return f"Hace {minutos} minuto{'s' if minutos > 1 else ''}"
        
        return "Hace un momento"


class ObtenerProductosStockBajoUseCase:
    """Obtiene productos con stock bajo"""
    
    def __init__(self, producto_repo: ProductoRepository):
        self.producto_repo = producto_repo
    
    def ejecutar(self, umbral: int = 5, limite: int = 10) -> List[ProductoStockBajoDTO]:
        """Obtiene productos con stock menor al umbral"""
        
        productos = self.producto_repo.obtener_todos(limite=10000)
        
        # Filtrar productos activos con stock bajo
        productos_bajo_stock = [
            p for p in productos
            if p.activo and p.stock_actual < umbral
        ]
        
        # Ordenar por stock ascendente (más críticos primero)
        productos_bajo_stock.sort(key=lambda p: p.stock_actual)
        
        # Limitar resultados
        productos_bajo_stock = productos_bajo_stock[:limite]
        
        return [
            ProductoStockBajoDTO(
                id=str(p.id),
                nombre=p.nombre,
                stock_actual=p.stock_actual,
                stock_minimo=umbral,
                precio=float(p.precio.monto) if hasattr(p, 'precio') else 0.0,
                imagen_url=getattr(p, 'imagen_url', None) or getattr(p, 'imagenes', [None])[0] if hasattr(p, 'imagenes') and p.imagenes else None
            )
            for p in productos_bajo_stock
        ]
