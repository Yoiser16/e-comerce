"""
Vista REST para Movimientos de Inventario (Kardex)
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from asgiref.sync import sync_to_async

from interfaces.api.fastapi.dependencies import get_current_user_admin
from infrastructure.persistence.django.models import RegistroAuditoriaModel, ProductoModel
from infrastructure.logging.logger_service import LoggerService

router = APIRouter(prefix="/inventario", tags=["Inventario"])
logger = LoggerService("InventarioAPI")


class MovimientoInventarioResponse(BaseModel):
    """Respuesta de movimiento de inventario"""
    id: str
    fecha: datetime
    producto_id: str
    producto_nombre: str
    producto_imagen: Optional[str]
    tipo: str  # ENTRADA, SALIDA, AJUSTE
    cantidad: int
    usuario: str
    motivo: str
    stock_anterior: Optional[int]
    stock_nuevo: Optional[int]

    class Config:
        from_attributes = True


@router.get(
    "/movimientos",
    response_model=List[MovimientoInventarioResponse],
    summary="Obtener movimientos de inventario (Kardex)",
    description="""
    Devuelve el historial de movimientos de stock con filtros opcionales.
    
    **Tipos de movimientos:**
    - ENTRADA: Compras a proveedores, ajustes positivos
    - SALIDA: Ventas confirmadas (órdenes CONFIRMADA/ENVIADA/ENTREGADA)
    - AJUSTE: Correcciones manuales de inventario
    
    **Solo se registran movimientos de órdenes CONFIRMADAS o superiores.**
    Las órdenes en estado BORRADOR no afectan el stock.
    """,
)
async def obtener_movimientos(
    fecha_desde: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_hasta: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    tipo: Optional[str] = Query(None, description="Tipo: ENTRADA, SALIDA, AJUSTE"),
    producto_id: Optional[str] = Query(None, description="ID del producto"),
    limite: int = Query(100, ge=1, le=500, description="Límite de registros"),
    usuario_actual: dict = Depends(get_current_user_admin),
):
    """
    Obtiene movimientos de inventario desde la tabla de auditoría.
    """
    def obtener_movimientos_sync():
        # Base query: solo registros de productos con cambio de stock
        query = RegistroAuditoriaModel.objects.filter(
            entidad_tipo="Orden",
            accion="CONFIRMAR_STOCK",
            resultado="EXITO"
        )
        
        # Filtro por fecha
        if fecha_desde:
            fecha_desde_dt = datetime.strptime(fecha_desde, "%Y-%m-%d")
            query = query.filter(timestamp__gte=fecha_desde_dt)
        
        if fecha_hasta:
            fecha_hasta_dt = datetime.strptime(fecha_hasta, "%Y-%m-%d")
            fecha_hasta_dt = fecha_hasta_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(timestamp__lte=fecha_hasta_dt)
        
        # Ordenar por fecha descendente
        registros = list(query.order_by('-timestamp')[:limite])
        
        # Transformar a movimientos
        movimientos = []
        
        for registro in registros:
            if not registro.datos_nuevos or 'productos_afectados' not in registro.datos_nuevos:
                continue
            
            productos_afectados = registro.datos_nuevos['productos_afectados']
            
            for producto_data in productos_afectados:
                if producto_id and producto_data.get('producto_id') != producto_id:
                    continue
                
                # Obtener info del producto
                try:
                    producto = ProductoModel.objects.get(id=producto_data['producto_id'])
                    producto_nombre = producto.nombre
                    producto_imagen = producto.imagen_principal
                except ProductoModel.DoesNotExist:
                    producto_nombre = producto_data.get('nombre', 'Producto desconocido')
                    producto_imagen = None
                
                tipo_movimiento = "SALIDA"
                cantidad_movida = producto_data.get('cantidad_descontada', 0)
                usuario_nombre = "Sistema"
                motivo = registro.mensaje if registro.mensaje else "Venta confirmada"
                
                movimiento = MovimientoInventarioResponse(
                    id=str(registro.id),
                    fecha=registro.timestamp,
                    producto_id=producto_data['producto_id'],
                    producto_nombre=producto_nombre,
                    producto_imagen=producto_imagen,
                    tipo=tipo_movimiento,
                    cantidad=cantidad_movida,
                    usuario=usuario_nombre,
                    motivo=motivo,
                    stock_anterior=producto_data.get('stock_anterior'),
                    stock_nuevo=producto_data.get('stock_nuevo')
                )
                
                movimientos.append(movimiento)
        
        # Filtro final por tipo
        if tipo:
            movimientos = [m for m in movimientos if m.tipo == tipo]
        
        return movimientos
    
    try:
        movimientos = await sync_to_async(obtener_movimientos_sync)()
        
        logger.info(
            f"Movimientos de inventario obtenidos",
            cantidad=len(movimientos)
        )
        
        return movimientos
        
    except Exception as e:
        logger.error(f"Error al obtener movimientos de inventario", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener movimientos de inventario: {str(e)}"
        )


@router.get(
    "/stats",
    summary="Estadísticas de inventario",
    description="Obtiene estadísticas generales del inventario actual"
)
async def obtener_stats_inventario(
    usuario_actual: dict = Depends(get_current_user_admin),
):
    """
    Devuelve estadísticas del inventario.
    """
    def obtener_stats_sync():
        productos = list(ProductoModel.objects.filter(activo=True))
        
        total_productos = len(productos)
        agotados = sum(1 for p in productos if p.stock_actual == 0)
        stock_bajo = sum(1 for p in productos if 0 < p.stock_actual <= p.stock_minimo)
        saludables = sum(1 for p in productos if p.stock_actual > p.stock_minimo)
        valor_total = sum(float(p.monto_precio) * p.stock_actual for p in productos)
        
        return {
            "total_productos": total_productos,
            "agotados": agotados,
            "stock_bajo": stock_bajo,
            "saludables": saludables,
            "valor_inventario": valor_total,
            "porcentaje_saludable": round((saludables / total_productos * 100) if total_productos > 0 else 0, 1)
        }
    
    try:
        stats = await sync_to_async(obtener_stats_sync)()
        return stats
        
    except Exception as e:
        logger.error(f"Error al obtener stats de inventario", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )
