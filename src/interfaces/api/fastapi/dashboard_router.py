"""
Router de Dashboard - FastAPI
Endpoints para estadísticas y datos del panel administrativo
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime, timedelta
from collections import defaultdict

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
