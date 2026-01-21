"""
Casos de uso para el dashboard administrativo
"""
from typing import List
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from domain.repositories.orden_repository import OrdenRepository
from domain.repositories.producto_repository import ProductoRepository
from domain.repositories.cliente_repository import ClienteRepository

from application.dto.dashboard_dto import (
    EstadisticasGeneralesDTO,
    OrdenResumeDTO,
    ProductoStockBajoDTO
)


def hacer_fecha_comparable(fecha):
    """Convierte una fecha a naive (sin timezone) para comparaciones seguras"""
    if fecha is None:
        return None
    if fecha.tzinfo is not None:
        return fecha.replace(tzinfo=None)
    return fecha


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
        
        # Valores por defecto en caso de error
        total_ventas = 0.0
        total_ordenes = 0
        ordenes_pendientes = 0
        total_productos = 0
        productos_activos = 0
        stock_bajo = 0
        total_clientes = 0
        clientes_nuevos = 0
        
        # Estadísticas de órdenes
        try:
            ordenes = self.orden_repo.obtener_todos(limite=10000)
            total_ordenes = len(ordenes)
            
            # Función para obtener estado como string
            def get_estado_str(o):
                if hasattr(o.estado, 'value'):
                    return o.estado.value.upper()
                return str(o.estado).upper() if o.estado else ''
            
            # Calcular total de ventas del mes actual - SOLO ÓRDENES CONFIRMADAS/PAGADAS
            mes_actual = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            estados_pagados = ['CONFIRMADA', 'PAGADA', 'PAGADO', 'ENVIADA', 'ENTREGADA', 'COMPLETADA']
            
            ordenes_pagadas_mes = [
                o for o in ordenes 
                if hacer_fecha_comparable(o.fecha_creacion) 
                and hacer_fecha_comparable(o.fecha_creacion) >= mes_actual
                and get_estado_str(o) in estados_pagados
            ]
            
            # Calcular total de ventas (solo órdenes pagadas)
            for o in ordenes_pagadas_mes:
                if hasattr(o.total, 'monto'):
                    total_ventas += float(o.total.monto)
                else:
                    total_ventas += float(o.total) if o.total else 0.0
            
            # Contar órdenes pendientes
            ordenes_pendientes = sum(1 for o in ordenes if get_estado_str(o) == 'PENDIENTE')
        except Exception as e:
            print(f"⚠️ Error al procesar órdenes: {e}")
        
        # Estadísticas de productos
        try:
            productos = self.producto_repo.obtener_todos(limite=10000)
            total_productos = len(productos)
            productos_activos_list = [p for p in productos if p.activo]
            productos_activos = len(productos_activos_list)
            
            # Contar productos con stock bajo (menos de 5 unidades)
            stock_bajo = sum(1 for p in productos_activos_list if p.stock_actual < 5)
        except Exception as e:
            print(f"⚠️ Error al procesar productos: {e}")
        
        # Estadísticas de clientes
        try:
            clientes = self.cliente_repo.obtener_todos(limite=10000)
            total_clientes = len(clientes)
            
            # Clientes nuevos (últimos 30 días)
            hace_30_dias = datetime.now() - timedelta(days=30)
            clientes_nuevos = sum(1 for c in clientes if hacer_fecha_comparable(c.fecha_creacion) and hacer_fecha_comparable(c.fecha_creacion) >= hace_30_dias)
        except Exception as e:
            print(f"⚠️ Error al procesar clientes: {e}")
        
        return EstadisticasGeneralesDTO(
            total_ventas=total_ventas,
            total_ordenes=total_ordenes,
            ordenes_pendientes=ordenes_pendientes,
            total_productos=total_productos,
            productos_activos=productos_activos,
            stock_bajo=stock_bajo,
            total_clientes=total_clientes,
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
            # Obtener cliente (puede ser None si cliente_id es None)
            cliente = None
            if orden.cliente_id:
                try:
                    cliente = self.cliente_repo.obtener_por_id(orden.cliente_id)
                except Exception:
                    cliente = None
            
            # Calcular tiempo transcurrido
            tiempo = self._calcular_tiempo_transcurrido(orden.fecha_creacion)
            
            # Manejar estado como enum o string
            estado_str = orden.estado.value if hasattr(orden.estado, 'value') else str(orden.estado)
            
            # Manejar total como Dinero o float
            total_float = float(orden.total.monto) if hasattr(orden.total, 'monto') else float(orden.total) if orden.total else 0.0
            
            # Manejar email del cliente
            cliente_email = ''
            if cliente:
                if hasattr(cliente.email, 'valor'):
                    cliente_email = cliente.email.valor
                else:
                    cliente_email = str(cliente.email) if cliente.email else ''
            
            resultado.append(OrdenResumeDTO(
                id=str(orden.id),
                cliente_nombre=cliente.nombre if cliente else "Cliente desconocido",
                cliente_email=cliente_email,
                estado=estado_str.upper(),
                total=total_float,
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
