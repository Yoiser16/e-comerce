"""
Router de Dashboard - FastAPI
Endpoints para estadísticas y datos del panel administrativo
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import time

from .dependencies import (
    get_orden_repository,
    get_producto_repository,
    get_cliente_repository,
    get_current_user_admin
)

from domain.repositories.orden_repository import OrdenRepository
from domain.repositories.producto_repository import ProductoRepository
from domain.repositories.cliente_repository import ClienteRepository

from application.use_cases.dashboard_use_cases import (
    ObtenerEstadisticasGeneralesUseCase,
    ObtenerOrdenesRecientesUseCase,
    ObtenerProductosStockBajoUseCase
)
from application.dto.dashboard_dto import (
    EstadisticasGeneralesDTO,
    OrdenResumeDTO,
    ProductoStockBajoDTO
)

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

# ═══════════════════════════════════════════════════════════════════════════
# CACHÉ EN MEMORIA - Para reducir consultas repetidas
# ═══════════════════════════════════════════════════════════════════════════
_cache = {
    'estadisticas': {'data': None, 'timestamp': 0},
    'ordenes_recientes': {'data': None, 'timestamp': 0},
    'productos_stock_bajo': {'data': None, 'timestamp': 0},
    'ventas_por_periodo': {'data': {}, 'timestamp': 0},
    'top_productos': {'data': None, 'timestamp': 0},
}
CACHE_TTL = 30  # Segundos de validez del caché


def _get_cached(key: str, ttl: int = CACHE_TTL):
    """Obtiene datos del caché si aún son válidos"""
    cache_entry = _cache.get(key)
    if cache_entry and cache_entry['data'] is not None:
        if time.time() - cache_entry['timestamp'] < ttl:
            return cache_entry['data']
    return None


def _set_cache(key: str, data):
    """Guarda datos en el caché"""
    _cache[key] = {'data': data, 'timestamp': time.time()}


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINT UNIFICADO - Carga todo el dashboard en una sola llamada
# ═══════════════════════════════════════════════════════════════════════════
@router.get("/completo")
def obtener_dashboard_completo(
    periodo: str = "7D",
    orden_repo: OrdenRepository = Depends(get_orden_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    cliente_repo: ClienteRepository = Depends(get_cliente_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Endpoint optimizado que devuelve TODOS los datos del dashboard en una sola llamada.
    Reduce de 5+ llamadas a 1 sola, mejorando significativamente el rendimiento.
    """
    from django.utils import timezone
    
    start_time = time.time()
    
    # Verificar caché completo
    cache_key = f'dashboard_completo_{periodo}'
    cached = _get_cached(cache_key, ttl=15)  # 15 segundos para dashboard completo
    if cached:
        cached['_meta']['cached'] = True
        return cached
    
    try:
        # Cargar datos base UNA sola vez
        ordenes = orden_repo.obtener_todos(limite=10000)
        productos = producto_repo.obtener_todos(limite=10000)
        clientes = cliente_repo.obtener_todos(limite=10000)
        
        # Funciones auxiliares
        def get_estado_str(o):
            if hasattr(o.estado, 'value'):
                return o.estado.value.upper()
            return str(o.estado).upper() if o.estado else ''
        
        def get_total(o):
            if hasattr(o.total, 'monto'):
                return float(o.total.monto)
            return float(o.total) if o.total else 0.0
        
        def hacer_fecha_comparable(fecha):
            if fecha is None:
                return None
            if fecha.tzinfo is not None:
                return fecha.replace(tzinfo=None)
            return fecha
        
        def make_aware(fecha):
            if fecha is None:
                return None
            if hasattr(fecha, 'tzinfo') and fecha.tzinfo is not None:
                return fecha
            return timezone.make_aware(fecha)
        
        # ═══════════════════════════════════════════════════════════════════
        # 1. ESTADÍSTICAS GENERALES
        # ═══════════════════════════════════════════════════════════════════
        total_ventas = 0.0
        total_ordenes = len(ordenes)
        ordenes_pendientes = 0
        
        estados_pagados = ['CONFIRMADA', 'PAGADA', 'PAGADO', 'ENVIADA', 'ENTREGADA', 'COMPLETADA']
        mes_actual = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        for o in ordenes:
            estado = get_estado_str(o)
            if estado == 'PENDIENTE':
                ordenes_pendientes += 1
            
            fecha_comp = hacer_fecha_comparable(o.fecha_creacion)
            if fecha_comp and fecha_comp >= mes_actual and estado in estados_pagados:
                total_ventas += get_total(o)
        
        # Productos
        productos_activos = [p for p in productos if p.activo]
        total_productos = len(productos_activos)
        stock_bajo_count = sum(1 for p in productos_activos if p.stock_actual < 5)
        
        # Clientes
        total_clientes = len(clientes)
        hace_30_dias = datetime.now() - timedelta(days=30)
        clientes_nuevos = sum(1 for c in clientes if hacer_fecha_comparable(c.fecha_creacion) and hacer_fecha_comparable(c.fecha_creacion) >= hace_30_dias)
        
        estadisticas = {
            'total_ventas': total_ventas,
            'total_ordenes': total_ordenes,
            'ordenes_pendientes': ordenes_pendientes,
            'total_productos': total_productos,
            'productos_activos': total_productos,
            'stock_bajo': stock_bajo_count,
            'total_clientes': total_clientes,
            'clientes_nuevos': clientes_nuevos
        }
        
        # ═══════════════════════════════════════════════════════════════════
        # 2. ÓRDENES RECIENTES
        # ═══════════════════════════════════════════════════════════════════
        ordenes_con_fecha = [o for o in ordenes if o.fecha_creacion is not None]
        ordenes_recientes = sorted(ordenes_con_fecha, key=lambda o: o.fecha_creacion, reverse=True)[:5]
        
        ordenes_recientes_data = []
        for orden in ordenes_recientes:
            cliente = None
            if orden.cliente_id:
                try:
                    cliente = cliente_repo.obtener_por_id(orden.cliente_id)
                except:
                    pass
            
            estado_str = orden.estado.value if hasattr(orden.estado, 'value') else str(orden.estado)
            total_float = float(orden.total.monto) if hasattr(orden.total, 'monto') else float(orden.total) if orden.total else 0.0
            
            # Tiempo transcurrido
            ahora = datetime.now()
            fecha = hacer_fecha_comparable(orden.fecha_creacion)
            if fecha:
                diferencia = ahora - fecha
                if diferencia.days > 0:
                    tiempo = f"Hace {diferencia.days} día{'s' if diferencia.days > 1 else ''}"
                elif diferencia.seconds >= 3600:
                    horas = diferencia.seconds // 3600
                    tiempo = f"Hace {horas} hora{'s' if horas > 1 else ''}"
                else:
                    minutos = diferencia.seconds // 60
                    tiempo = f"Hace {minutos} min" if minutos > 0 else "Ahora"
            else:
                tiempo = "Reciente"
            
            ordenes_recientes_data.append({
                'id': str(orden.id),
                'cliente_nombre': cliente.nombre if cliente else "Cliente",
                'estado': estado_str.upper(),
                'total': total_float,
                'tiempo_transcurrido': tiempo
            })
        
        # ═══════════════════════════════════════════════════════════════════
        # 3. PRODUCTOS CON STOCK BAJO
        # ═══════════════════════════════════════════════════════════════════
        productos_stock_bajo = sorted(
            [p for p in productos_activos if p.stock_actual < 5],
            key=lambda p: p.stock_actual
        )[:10]
        
        def get_codigo_str(p):
            """Extrae el código como string"""
            if hasattr(p.codigo, '_valor'):
                return p.codigo._valor
            if hasattr(p.codigo, 'valor'):
                return p.codigo.valor
            return str(p.codigo) if p.codigo else ''
        
        stock_bajo_data = [{
            'id': str(p.id),
            'nombre': p.nombre,
            'codigo': get_codigo_str(p),
            'stock_actual': p.stock_actual,
            'stock_minimo': getattr(p, 'stock_minimo', 5)
        } for p in productos_stock_bajo]
        
        # ═══════════════════════════════════════════════════════════════════
        # 4. VENTAS POR PERÍODO
        # ═══════════════════════════════════════════════════════════════════
        ordenes_pagadas = [o for o in ordenes if get_estado_str(o) in estados_pagados]
        now = timezone.now()
        
        if periodo == "24H":
            inicio = now - timedelta(hours=24)
            labels = [f"{i:02d}:00" for i in range(0, 24, 4)]
            ventas = defaultdict(float)
            
            for o in ordenes_pagadas:
                fecha = make_aware(o.fecha_creacion) if o.fecha_creacion else None
                if fecha and fecha >= inicio:
                    hora_key = f"{(fecha.hour // 4) * 4:02d}:00"
                    ventas[hora_key] += get_total(o)
            
            data = [ventas.get(label, 0) for label in labels]
            
        elif periodo == "7D":
            dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
            ventas = defaultdict(float)
            inicio = now - timedelta(days=7)
            
            for o in ordenes_pagadas:
                fecha = make_aware(o.fecha_creacion) if o.fecha_creacion else None
                if fecha and fecha >= inicio:
                    dia_semana = dias[fecha.weekday()]
                    ventas[dia_semana] += get_total(o)
            
            labels = dias
            data = [ventas.get(dia, 0) for dia in dias]
            
        else:  # 30D
            labels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
            ventas = [0.0, 0.0, 0.0, 0.0]
            
            for o in ordenes_pagadas:
                fecha = make_aware(o.fecha_creacion) if o.fecha_creacion else None
                if fecha:
                    dias_atras = (now - fecha).days
                    if 0 <= dias_atras < 7:
                        ventas[3] += get_total(o)
                    elif 7 <= dias_atras < 14:
                        ventas[2] += get_total(o)
                    elif 14 <= dias_atras < 21:
                        ventas[1] += get_total(o)
                    elif 21 <= dias_atras < 28:
                        ventas[0] += get_total(o)
            
            data = ventas
        
        ventas_periodo = {'labels': labels, 'data': data, 'total': sum(data)}
        
        # ═══════════════════════════════════════════════════════════════════
        # 5. TOP PRODUCTOS
        # ═══════════════════════════════════════════════════════════════════
        productos_map = {str(p.id): p for p in productos}
        ventas_producto = defaultdict(lambda: {"cantidad": 0, "total": 0.0})
        
        for orden in ordenes:
            if get_estado_str(orden) not in estados_pagados:
                continue
            
            if hasattr(orden, 'lineas') and orden.lineas:
                for linea in orden.lineas:
                    producto_id = str(linea.producto_id)
                    cantidad = linea.cantidad if hasattr(linea, 'cantidad') else 1
                    
                    if hasattr(linea, 'subtotal'):
                        subtotal = float(linea.subtotal.monto) if hasattr(linea.subtotal, 'monto') else float(linea.subtotal) if linea.subtotal else 0
                    elif hasattr(linea, 'precio_unitario'):
                        subtotal = float(linea.precio_unitario.monto) * cantidad if hasattr(linea.precio_unitario, 'monto') else float(linea.precio_unitario) * cantidad if linea.precio_unitario else 0
                    else:
                        subtotal = 0
                    
                    ventas_producto[producto_id]["cantidad"] += cantidad
                    ventas_producto[producto_id]["total"] += subtotal
        
        top_productos_sorted = sorted(ventas_producto.items(), key=lambda x: x[1]["total"], reverse=True)[:5]
        
        top_productos_data = []
        for producto_id, stats in top_productos_sorted:
            producto = productos_map.get(producto_id)
            nombre = producto.nombre if producto else f"Producto {producto_id[:8]}"
            top_productos_data.append({
                "id": producto_id,
                "nombre": nombre,
                "cantidad": stats["cantidad"],
                "ventas": stats["total"]
            })
        
        # ═══════════════════════════════════════════════════════════════════
        # 6. VENTAS POR CATEGORÍA
        # ═══════════════════════════════════════════════════════════════════
        ventas_categoria = defaultdict(float)
        
        for orden in ordenes:
            if get_estado_str(orden) not in estados_pagados:
                continue
            
            if hasattr(orden, 'lineas') and orden.lineas:
                for linea in orden.lineas:
                    producto_id = str(linea.producto_id)
                    producto = productos_map.get(producto_id)
                    
                    category_name = "Sin Categoría"
                    if producto and producto.categoria:
                        category_name = producto.categoria
                    
                    # Calcular subtotal (reutilizando lógica segura)
                    cantidad = linea.cantidad if hasattr(linea, 'cantidad') else 1
                    if hasattr(linea, 'subtotal'):
                         if hasattr(linea.subtotal, 'monto'):
                            subtotal = float(linea.subtotal.monto)
                         else:
                            subtotal = float(linea.subtotal) if linea.subtotal else 0
                    elif hasattr(linea, 'precio_unitario'):
                         if hasattr(linea.precio_unitario, 'monto'):
                            subtotal = float(linea.precio_unitario.monto) * cantidad
                         else:
                            subtotal = float(linea.precio_unitario) * cantidad if linea.precio_unitario else 0
                    else:
                        subtotal = 0

                    ventas_categoria[category_name] += subtotal
        
        categorias_data = {
            "labels": list(ventas_categoria.keys()),
            "data": list(ventas_categoria.values())
        }

        # ═══════════════════════════════════════════════════════════════════
        # 7. DISTRIBUCIÓN DE ESTADOS
        # ═══════════════════════════════════════════════════════════════════
        conteo_estados = defaultdict(int)
        for o in ordenes:
             estado = get_estado_str(o)
             conteo_estados[estado] += 1
             
        estados_data = {
            "labels": list(conteo_estados.keys()),
            "data": list(conteo_estados.values())
        }

        # ═══════════════════════════════════════════════════════════════════
        # 8. TICKET PROMEDIO
        # ═══════════════════════════════════════════════════════════════════
        ticket_promedio = 0.0
        ventas_totales_monto = estadisticas['total_ventas']
        # Usar conteo de órdenes pagadas, no totales, para ser precisos
        ordenes_pagadas_count = sum(1 for o in ordenes if get_estado_str(o) in estados_pagados)
        
        if ordenes_pagadas_count > 0:
            ticket_promedio = ventas_totales_monto / ordenes_pagadas_count
            
        estadisticas['ticket_promedio'] = ticket_promedio
        
        # ═══════════════════════════════════════════════════════════════════
        # 9. CRECIMIENTO DE CLIENTES (Ultimos 6 meses)
        # ═══════════════════════════════════════════════════════════════════
        clientes_por_mes = defaultdict(int)
        meses_labels = []
        
        # Generar labels para últimos 6 meses
        for i in range(5, -1, -1):
            fecha = datetime.now() - timedelta(days=i*30)
            mes_key = f"{fecha.year}-{fecha.month:02d}"
            meses_labels.append(fecha.strftime("%b")) # Ene, Feb, etc.
            clientes_por_mes[mes_key] = 0
            
        # Contar clientes
        for c in clientes:
            fecha_creacion = hacer_fecha_comparable(c.fecha_creacion)
            if fecha_creacion:
                 mes_key = f"{fecha_creacion.year}-{fecha_creacion.month:02d}"
                 # Solo si entra en nuestra ventana de tiempo (aprox)
                 if mes_key in clientes_por_mes or len(clientes_por_mes) < 6: # Simplificado
                     clientes_por_mes[mes_key] += 1
        
        # Como los meses pueden no coincidir exacto con keys si no hay clientes, 
        # hacemos una aproximación simple basada en orden histórico
        crecimiento_clientes_data = {
            "labels": meses_labels,
            "data": [0] * 6 # Placeholder, la lógica real requeriría alineación exacta de fechas
        }
        
        # Lógica corregida para mapear a los últimos 6 meses de forma robusta
        datos_meses = [0] * 6
        hoy = datetime.now()
        for c in clientes:
            fecha = hacer_fecha_comparable(c.fecha_creacion)
            if fecha:
                meses_atras = (hoy.year - fecha.year) * 12 + hoy.month - fecha.month
                if 0 <= meses_atras < 6:
                    idx = 5 - meses_atras
                    datos_meses[idx] += 1
        
        crecimiento_clientes_data["data"] = datos_meses

        # ═══════════════════════════════════════════════════════════════════
        # 10. SALUD DE INVENTARIO
        # ═══════════════════════════════════════════════════════════════════
        # Agotar (0), Bajo (<5), Saludable (>5)
        inventario_stats = {
            "agotado": 0,
            "bajo": 0,
            "saludable": 0
        }
        
        for p in productos_activos:
            if p.stock_actual == 0:
                inventario_stats["agotado"] += 1
            elif p.stock_actual < 5:
                 inventario_stats["bajo"] += 1
            else:
                 inventario_stats["saludable"] += 1
                 
        # ═══════════════════════════════════════════════════════════════════
        # RESPUESTA UNIFICADA
        # ═══════════════════════════════════════════════════════════════════
        elapsed = time.time() - start_time
        
        resultado = {
            'estadisticas': estadisticas,
            'ordenes_recientes': ordenes_recientes_data,
            'productos_stock_bajo': stock_bajo_data,
            'ventas_por_periodo': ventas_periodo,
            'top_productos': top_productos_data,
            'ventas_por_categoria': categorias_data,
            'distribucion_estados': estados_data,
            'crecimiento_clientes': crecimiento_clientes_data,
            'salud_inventario': inventario_stats,
            '_meta': {
                'tiempo_carga_ms': round(elapsed * 1000, 2),
                'periodo': periodo,
                'cached': False
            }
        }
        
        # Guardar en caché
        _set_cache(cache_key, resultado)
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error en dashboard completo: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cargar dashboard: {str(e)}"
        )


@router.get("/estadisticas", response_model=EstadisticasGeneralesDTO)
def obtener_estadisticas(
    orden_repo: OrdenRepository = Depends(get_orden_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    cliente_repo: ClienteRepository = Depends(get_cliente_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Obtiene estadísticas generales del sistema
    
    Requiere: Rol ADMIN o OPERADOR
    """
    try:
        use_case = ObtenerEstadisticasGeneralesUseCase(
            orden_repo,
            producto_repo,
            cliente_repo
        )
        return use_case.ejecutar()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )


@router.get("/ordenes/recientes", response_model=List[OrdenResumeDTO])
def obtener_ordenes_recientes(
    limite: int = 5,
    orden_repo: OrdenRepository = Depends(get_orden_repository),
    cliente_repo: ClienteRepository = Depends(get_cliente_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Obtiene las órdenes más recientes
    
    Parámetros:
    - limite: Número máximo de órdenes a retornar (default: 5)
    
    Requiere: Rol ADMIN o OPERADOR
    """
    try:
        use_case = ObtenerOrdenesRecientesUseCase(orden_repo, cliente_repo)
        return use_case.ejecutar(limite)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener órdenes recientes: {str(e)}"
        )


@router.get("/productos/stock-bajo", response_model=List[ProductoStockBajoDTO])
def obtener_productos_stock_bajo(
    umbral: int = 5,
    limite: int = 10,
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Obtiene productos con stock bajo
    
    Parámetros:
    - umbral: Stock mínimo para considerar "bajo" (default: 5)
    - limite: Número máximo de productos a retornar (default: 10)
    
    Requiere: Rol ADMIN o OPERADOR
    """
    try:
        use_case = ObtenerProductosStockBajoUseCase(producto_repo)
        return use_case.ejecutar(umbral, limite)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos con stock bajo: {str(e)}"
        )


@router.get("/ventas/por-periodo")
def obtener_ventas_por_periodo(
    periodo: str = "7D",
    orden_repo: OrdenRepository = Depends(get_orden_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Obtiene ventas agrupadas por período (solo órdenes confirmadas/pagadas)
    
    Parámetros:
    - periodo: "24H", "7D" o "30D"
    """
    try:
        from django.utils import timezone
        
        ordenes = orden_repo.obtener_todos(limite=10000)
        
        # Estados que cuentan como "pagado"
        estados_pagados = ['CONFIRMADA', 'PAGADA', 'PAGADO', 'ENVIADA', 'ENTREGADA', 'COMPLETADA']
        
        def get_estado_str(o):
            if hasattr(o.estado, 'value'):
                return o.estado.value.upper()
            return str(o.estado).upper() if o.estado else ''
        
        def get_total(o):
            if hasattr(o.total, 'monto'):
                return float(o.total.monto)
            return float(o.total) if o.total else 0.0
        
        def make_aware(fecha):
            """Convierte fecha naive a aware si es necesario"""
            if fecha is None:
                return None
            if hasattr(fecha, 'tzinfo') and fecha.tzinfo is not None:
                return fecha
            return timezone.make_aware(fecha)
        
        # Filtrar solo órdenes pagadas
        ordenes_pagadas = [o for o in ordenes if get_estado_str(o) in estados_pagados]
        
        # Usar timezone aware datetime
        now = timezone.now()
        
        if periodo == "24H":
            # Últimas 24 horas, agrupadas por hora
            inicio = now - timedelta(hours=24)
            labels = [f"{i:02d}:00" for i in range(0, 24, 4)]
            ventas = defaultdict(float)
            
            for o in ordenes_pagadas:
                fecha = make_aware(o.fecha_creacion) if o.fecha_creacion else None
                if fecha and fecha >= inicio:
                    hora_key = f"{(fecha.hour // 4) * 4:02d}:00"
                    ventas[hora_key] += get_total(o)
            
            data = [ventas.get(label, 0) for label in labels]
            
        elif periodo == "7D":
            # Últimos 7 días
            dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
            ventas = defaultdict(float)
            inicio = now - timedelta(days=7)
            
            for o in ordenes_pagadas:
                fecha = make_aware(o.fecha_creacion) if o.fecha_creacion else None
                if fecha and fecha >= inicio:
                    dia_semana = dias[fecha.weekday()]
                    ventas[dia_semana] += get_total(o)
            
            labels = dias
            data = [ventas.get(dia, 0) for dia in dias]
            
        else:  # 30D
            # Últimas 4 semanas
            labels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
            ventas = [0.0, 0.0, 0.0, 0.0]
            
            for o in ordenes_pagadas:
                fecha = make_aware(o.fecha_creacion) if o.fecha_creacion else None
                if fecha:
                    dias_atras = (now - fecha).days
                    if 0 <= dias_atras < 7:
                        ventas[3] += get_total(o)
                    elif 7 <= dias_atras < 14:
                        ventas[2] += get_total(o)
                    elif 14 <= dias_atras < 21:
                        ventas[1] += get_total(o)
                    elif 21 <= dias_atras < 28:
                        ventas[0] += get_total(o)
            
            data = ventas
        
        return {
            "labels": labels,
            "data": data,
            "total": sum(data)
        }
        
    except Exception as e:
        print(f"Error en ventas por periodo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ventas: {str(e)}"
        )


@router.get("/top-productos")
def obtener_top_productos(
    limite: int = 5,
    orden_repo: OrdenRepository = Depends(get_orden_repository),
    producto_repo: ProductoRepository = Depends(get_producto_repository),
    current_user = Depends(get_current_user_admin)
):
    """
    Obtiene los productos más vendidos (solo de órdenes confirmadas/pagadas)
    """
    try:
        ordenes = orden_repo.obtener_todos(limite=10000)
        productos = producto_repo.obtener_todos(limite=10000)
        
        # Crear mapa de productos
        productos_map = {str(p.id): p for p in productos}
        
        # Estados que cuentan como "pagado"
        estados_pagados = ['CONFIRMADA', 'PAGADA', 'PAGADO', 'ENVIADA', 'ENTREGADA', 'COMPLETADA']
        
        def get_estado_str(o):
            if hasattr(o.estado, 'value'):
                return o.estado.value.upper()
            return str(o.estado).upper() if o.estado else ''
        
        # Acumular ventas por producto
        ventas_producto = defaultdict(lambda: {"cantidad": 0, "total": 0.0})
        
        for orden in ordenes:
            if get_estado_str(orden) not in estados_pagados:
                continue
            
            # Obtener líneas de la orden
            if hasattr(orden, 'lineas') and orden.lineas:
                for linea in orden.lineas:
                    producto_id = str(linea.producto_id)
                    cantidad = linea.cantidad if hasattr(linea, 'cantidad') else 1
                    
                    # Calcular subtotal de la línea
                    if hasattr(linea, 'subtotal'):
                        if hasattr(linea.subtotal, 'monto'):
                            subtotal = float(linea.subtotal.monto)
                        else:
                            subtotal = float(linea.subtotal) if linea.subtotal else 0
                    elif hasattr(linea, 'precio_unitario'):
                        if hasattr(linea.precio_unitario, 'monto'):
                            subtotal = float(linea.precio_unitario.monto) * cantidad
                        else:
                            subtotal = float(linea.precio_unitario) * cantidad if linea.precio_unitario else 0
                    else:
                        subtotal = 0
                    
                    ventas_producto[producto_id]["cantidad"] += cantidad
                    ventas_producto[producto_id]["total"] += subtotal
        
        # Ordenar por total de ventas
        top_productos = sorted(
            ventas_producto.items(),
            key=lambda x: x[1]["total"],
            reverse=True
        )[:limite]
        
        # Formatear respuesta
        resultado = []
        for producto_id, stats in top_productos:
            producto = productos_map.get(producto_id)
            nombre = producto.nombre if producto else f"Producto {producto_id[:8]}"
            imagen = None
            if producto and hasattr(producto, 'imagenes') and producto.imagenes:
                imagen = producto.imagenes[0] if isinstance(producto.imagenes, list) else str(producto.imagenes)
            
            resultado.append({
                "id": producto_id,
                "nombre": nombre,
                "cantidad": stats["cantidad"],
                "ventas": stats["total"],
                "imagen": imagen
            })
        
        return resultado
        
    except Exception as e:
        print(f"Error en top productos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener top productos: {str(e)}"
        )
