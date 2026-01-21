"""
Router de Órdenes para FastAPI

Endpoints:
- POST /ordenes - Crear orden (desde checkout)
- GET /ordenes - Listar órdenes (admin)
- GET /ordenes/{id} - Detalle de orden
- PATCH /ordenes/{id}/estado - Cambiar estado
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import uuid4
from decimal import Decimal
from datetime import datetime
from asgiref.sync import sync_to_async
import random

# Importar modelos Django
import django
django.setup()

from infrastructure.persistence.django.models import OrdenModel, LineaOrdenModel, ClienteModel, ProductoModel


router = APIRouter(prefix="/api/v1/ordenes", tags=["ordenes"])


# ═══════════════════════════════════════════════════════════════════════════
# DTOs / Schemas
# ═══════════════════════════════════════════════════════════════════════════

class LineaOrdenInput(BaseModel):
    producto_id: Optional[str] = None
    cantidad: int
    precio_unitario: float
    nombre: Optional[str] = None


class CrearOrdenInput(BaseModel):
    """Input para crear orden desde checkout"""
    email: EmailStr
    nombre: str
    apellido: Optional[str] = ''
    telefono: str
    direccion: str
    departamento: str
    municipio: str
    barrio: Optional[str] = ''
    notas: Optional[str] = ''
    items: List[LineaOrdenInput]
    subtotal: float
    envio: float
    total: float
    metodo_pago: str = 'whatsapp'


class OrdenResponse(BaseModel):
    id: str
    codigo: str
    estado: str
    cliente_nombre: str
    cliente_email: str
    cliente_telefono: str
    cliente_tipo_doc: str
    cliente_num_doc: str
    direccion_envio: str
    departamento: str
    municipio: str
    barrio: str
    notas_envio: str
    subtotal_monto: float
    envio_monto: float
    total: float
    metodo_pago: str
    items: List[dict]
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True


class OrdenListItem(BaseModel):
    id: str
    codigo: str
    estado: str
    cliente_nombre: str
    cliente_email: str
    cliente_telefono: str
    total: float
    total_items: int
    metodo_pago: str
    fecha_creacion: datetime


class CambiarEstadoInput(BaseModel):
    estado: str


# ═══════════════════════════════════════════════════════════════════════════
# Funciones SYNC que serán envueltas en async
# ═══════════════════════════════════════════════════════════════════════════

def _listar_ordenes_sync(estado: Optional[str], limite: int) -> List[dict]:
    """Lista órdenes (sync)"""
    queryset = OrdenModel.objects.select_related('cliente').order_by('-fecha_creacion')
    
    if estado:
        queryset = queryset.filter(estado=estado.lower())
    
    ordenes = list(queryset[:limite])
    
    resultado = []
    for orden in ordenes:
        total_items = orden.lineas.count() if hasattr(orden, 'lineas') else 0
        
        resultado.append({
            'id': str(orden.id),
            'codigo': orden.codigo or f"ORD-{str(orden.id)[:8]}",
            'estado': orden.estado.upper(),
            'cliente_nombre': f"{orden.cliente.nombre} {orden.cliente.apellido}" if orden.cliente else "Sin cliente",
            'cliente_email': orden.cliente.email if orden.cliente else "",
            'cliente_telefono': orden.cliente.telefono if orden.cliente else "",
            'total': float(orden.total_monto),
            'total_items': total_items,
            'metodo_pago': orden.metodo_pago or 'whatsapp',
            'fecha_creacion': orden.fecha_creacion
        })
    
    return resultado


def _crear_orden_sync(data: CrearOrdenInput) -> dict:
    """Crea una orden (sync)"""
    # 1. Obtener o crear cliente
    cliente = ClienteModel.objects.filter(email=data.email).first()
    
    if not cliente:
        cliente = ClienteModel.objects.create(
            id=uuid4(),
            email=data.email,
            nombre=data.nombre,
            apellido=data.apellido,
            telefono=data.telefono,
            tipo_documento='CC',
            numero_documento=f"AUTO-{uuid4().hex[:8].upper()}",
            activo=True
        )
    else:
        # Actualizar datos si cambiaron
        actualizado = False
        if cliente.nombre != data.nombre:
            cliente.nombre = data.nombre
            actualizado = True
        if cliente.apellido != data.apellido:
            cliente.apellido = data.apellido
            actualizado = True
        if cliente.telefono != data.telefono:
            cliente.telefono = data.telefono
            actualizado = True
        if actualizado:
            cliente.save()
    
    # 2. Generar código único
    while True:
        numero = random.randint(1000, 9999)
        codigo = f"KH-{numero}"
        if not OrdenModel.objects.filter(codigo=codigo).exists():
            break
    
    # 3. Crear la orden
    orden = OrdenModel.objects.create(
        id=uuid4(),
        cliente=cliente,
        codigo=codigo,
        direccion_envio=data.direccion,
        departamento=data.departamento,
        municipio=data.municipio,
        barrio=data.barrio or '',
        notas_envio=data.notas or '',
        estado='pendiente',
        metodo_pago=data.metodo_pago,
        subtotal_monto=Decimal(str(data.subtotal)),
        envio_monto=Decimal(str(data.envio)),
        total_monto=Decimal(str(data.total)),
        total_moneda='COP',
        activo=True
    )
    
    # 4. Crear líneas de la orden
    items_response = []
    for item in data.items:
        producto = None
        producto_nombre = item.nombre or 'Producto'
        
        # Intentar buscar el producto si hay producto_id válido
        if item.producto_id and item.producto_id != '00000000-0000-0000-0000-000000000000':
            try:
                producto = ProductoModel.objects.get(id=item.producto_id)
                producto_nombre = producto.nombre
            except (ProductoModel.DoesNotExist, Exception):
                producto = None
        
        subtotal = Decimal(str(item.precio_unitario)) * item.cantidad
        
        # Solo crear línea si hay producto válido
        if producto:
            LineaOrdenModel.objects.create(
                id=uuid4(),
                orden=orden,
                producto=producto,
                cantidad=item.cantidad,
                precio_unitario_monto=Decimal(str(item.precio_unitario)),
                precio_unitario_moneda='COP',
                subtotal_monto=subtotal,
                subtotal_moneda='COP'
            )
        
        items_response.append({
            'producto_id': item.producto_id or 'sin-id',
            'nombre': producto_nombre,
            'cantidad': item.cantidad,
            'precio_unitario': item.precio_unitario,
            'subtotal': float(subtotal)
        })
    
    return {
        'id': str(orden.id),
        'codigo': orden.codigo,
        'estado': orden.estado,
        'cliente_nombre': f"{cliente.nombre} {cliente.apellido}",
        'cliente_email': cliente.email,
        'cliente_telefono': cliente.telefono or '',
        'direccion_envio': orden.direccion_envio,
        'departamento': orden.departamento,
        'municipio': orden.municipio,
        'subtotal': float(orden.subtotal_monto),
        'envio': float(orden.envio_monto),
        'total': float(orden.total_monto),
        'metodo_pago': orden.metodo_pago,
        'items': items_response,
        'fecha_creacion': orden.fecha_creacion
    }


def _obtener_orden_sync(orden_id: str) -> dict:
    """Obtiene detalle de una orden (sync)"""
    orden = OrdenModel.objects.select_related('cliente').prefetch_related('lineas__producto').get(id=orden_id)
    
    items = []
    for linea in orden.lineas.all():
        items.append({
            'id': str(linea.id),
            'producto_id': str(linea.producto_id),
            'sku': linea.producto.codigo if linea.producto else 'N/A',
            'nombre': linea.producto.nombre if linea.producto else 'Producto',
            'cantidad': linea.cantidad,
            'precio_unitario': float(linea.precio_unitario_monto),
            'subtotal': float(linea.subtotal_monto)
        })
    
    return {
        'id': str(orden.id),
        'codigo': orden.codigo,
        'estado': orden.estado.upper(),
        'cliente_nombre': f"{orden.cliente.nombre} {orden.cliente.apellido}".strip() if orden.cliente else "Sin cliente",
        'cliente_email': orden.cliente.email if orden.cliente else "",
        'cliente_telefono': orden.cliente.telefono if orden.cliente else "",
        'cliente_tipo_doc': orden.cliente.tipo_documento if orden.cliente else "",
        'cliente_num_doc': orden.cliente.numero_documento if orden.cliente else "",
        'direccion_envio': orden.direccion_envio or '',
        'departamento': orden.departamento or '',
        'municipio': orden.municipio or '',
        'barrio': orden.barrio or '',
        'notas_envio': orden.notas_envio or '',
        'subtotal_monto': float(orden.subtotal_monto),
        'envio_monto': float(orden.envio_monto),
        'total': float(orden.total_monto),
        'metodo_pago': orden.metodo_pago or 'whatsapp',
        'items': items,
        'fecha_creacion': orden.fecha_creacion
    }


def _actualizar_estado_sync(orden_id: str, estado: str) -> dict:
    """Actualiza estado de una orden (sync)"""
    estados_validos = ['pendiente', 'confirmada', 'en_proceso', 'enviada', 'completada', 'cancelada']
    estado_nuevo = estado.lower()
    
    if estado_nuevo not in estados_validos:
        raise ValueError(f"Estado inválido. Estados válidos: {estados_validos}")
    
    orden = OrdenModel.objects.get(id=orden_id)
    orden.estado = estado_nuevo
    orden.save()
    
    return {"mensaje": "Estado actualizado", "estado": estado_nuevo.upper()}


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════

@router.get("", response_model=List[OrdenListItem])
@router.get("/", response_model=List[OrdenListItem])
async def listar_ordenes(estado: Optional[str] = None, limite: int = 50):
    """Lista todas las órdenes (para admin)"""
    try:
        resultado = await sync_to_async(_listar_ordenes_sync)(estado, limite)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar órdenes: {str(e)}"
        )


@router.post("", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED)
async def crear_orden(data: CrearOrdenInput):
    """
    Crea una nueva orden desde el checkout.
    - Si el cliente no existe (por email), lo crea automáticamente.
    - Genera código único KH-XXXX
    - Estado inicial: PENDIENTE
    """
    try:
        resultado = await sync_to_async(_crear_orden_sync)(data)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la orden: {str(e)}"
        )


@router.get("/{orden_id}", response_model=OrdenResponse)
async def obtener_orden(orden_id: str):
    """Obtiene el detalle de una orden"""
    try:
        resultado = await sync_to_async(_obtener_orden_sync)(orden_id)
        return resultado
    except OrdenModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener orden: {str(e)}"
        )


@router.patch("/{orden_id}")
async def actualizar_estado(orden_id: str, data: CambiarEstadoInput):
    """Actualiza el estado de una orden"""
    try:
        resultado = await sync_to_async(_actualizar_estado_sync)(orden_id, data.estado)
        return resultado
    except OrdenModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar estado: {str(e)}"
        )
