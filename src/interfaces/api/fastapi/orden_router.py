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
from infrastructure.notifications.email_service import send_order_status_email
from interfaces.api.fastapi.dependencies import get_current_user_email


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
    cliente_tipo_doc: Optional[str] = ''
    cliente_num_doc: Optional[str] = ''
    direccion_envio: str
    departamento: str
    municipio: str
    barrio: Optional[str] = ''
    notas_envio: Optional[str] = ''
    subtotal_monto: Optional[float] = 0.0
    envio_monto: Optional[float] = 0.0
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


class ValidarStockInput(BaseModel):
    """Input para validar disponibilidad de stock"""
    items: List[LineaOrdenInput]


class ValidarStockResponse(BaseModel):
    """Response de validacion de stock"""
    disponible: bool
    productos: List[dict]
    mensaje: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# Funciones SYNC que seran envueltas en async
# ═══════════════════════════════════════════════════════════════════════════

def _listar_ordenes_sync(estado: Optional[str], limite: int) -> List[dict]:
    """Lista órdenes (sync) - Optimizado con annotate"""
    from django.db.models import Count
    
    queryset = (OrdenModel.objects
                .select_related('cliente')
                .annotate(num_items=Count('lineas'))
                .order_by('-fecha_creacion'))
    
    if estado:
        queryset = queryset.filter(estado=estado.lower())
    
    ordenes = list(queryset[:limite])
    
    resultado = []
    for orden in ordenes:
        resultado.append({
            'id': str(orden.id),
            'codigo': orden.codigo or f"ORD-{str(orden.id)[:8]}",
            'estado': orden.estado,
            'cliente_nombre': f"{orden.cliente.nombre} {orden.cliente.apellido}" if orden.cliente else "Sin cliente",
            'cliente_email': orden.cliente.email if orden.cliente else "",
            'cliente_telefono': orden.cliente.telefono if orden.cliente else "",
            'total': float(orden.total_monto),
            'total_items': orden.num_items,
            'metodo_pago': orden.metodo_pago or 'whatsapp',
            'fecha_creacion': orden.fecha_creacion
        })
    
    return resultado


def _listar_ordenes_por_email_sync(email: str) -> List[dict]:
    """Lista órdenes de un cliente por email (sync)"""
    from django.db.models import Count, Prefetch
    
    cliente = ClienteModel.objects.filter(email=email).first()
    if not cliente:
        return []
    
    queryset = (OrdenModel.objects
                .filter(cliente=cliente)
                .select_related('cliente')
                .prefetch_related('lineas')
                .order_by('-fecha_creacion'))
    
    ordenes = list(queryset)
    
    resultado = []
    for orden in ordenes:
        # Obtener items de la orden
        items = []
        for linea in orden.lineas.all():
            items.append({
                'id': str(linea.id),
                'producto_id': str(linea.producto.id) if linea.producto else '',
                'nombre': getattr(linea.producto, 'nombre', '') if linea.producto else '',
                'cantidad': linea.cantidad,
                'precio': float(getattr(linea, 'precio_unitario_monto', 0) or 0),
                'moneda': getattr(linea, 'precio_unitario_moneda', 'USD'),
                'imagen': linea.producto.imagen_principal if linea.producto and hasattr(linea.producto, 'imagen_principal') else None
            })
        
        resultado.append({
            'id': str(orden.id),
            'numero': orden.codigo or f"ORD-{str(orden.id)[:8]}",
            'estado': orden.estado,
            'fecha': orden.fecha_creacion,
            'total': float(orden.total_monto),
            'subtotal': float(orden.subtotal_monto),
            'envio': float(orden.envio_monto),
            'items': items,
            'metodo_pago': orden.metodo_pago or 'whatsapp'
        })
    
    return resultado


def _validar_stock_sync(items: List[LineaOrdenInput]) -> dict:
    """Valida disponibilidad de stock sin hacer descuentos (lectura solamente)"""
    productos_info = []
    todos_disponibles = True
    
    for item in items:
        if item.producto_id and item.producto_id != '00000000-0000-0000-0000-000000000000':
            try:
                producto = ProductoModel.objects.get(id=item.producto_id)
                disponible = producto.stock_actual >= item.cantidad
                todos_disponibles = todos_disponibles and disponible
                
                productos_info.append({
                    'producto_id': str(producto.id),
                    'nombre': producto.nombre,
                    'stock_solicitado': item.cantidad,
                    'stock_disponible': producto.stock_actual,
                    'disponible': disponible,
                    'mensaje': f'Stock disponible' if disponible else f'Solo hay {producto.stock_actual} disponibles'
                })
            except ProductoModel.DoesNotExist:
                productos_info.append({
                    'producto_id': item.producto_id,
                    'nombre': item.nombre or 'Producto desconocido',
                    'stock_solicitado': item.cantidad,
                    'stock_disponible': 0,
                    'disponible': False,
                    'mensaje': 'Producto no encontrado'
                })
                todos_disponibles = False
    
    return {
        'disponible': todos_disponibles,
        'productos': productos_info,
        'mensaje': 'Stock disponible para todos los productos' if todos_disponibles else 'Stock insuficiente para algunos productos'
    }


def _crear_orden_sync(data: CrearOrdenInput) -> dict:
    """Crea una orden (sync) con validacion atomica de stock"""
    from django.db import transaction
    
    with transaction.atomic():
        # 0. VALIDAR STOCK PRIMERO (con bloqueo pesimista)
        for item in data.items:
            if item.producto_id and item.producto_id != '00000000-0000-0000-0000-000000000000':
                try:
                    producto = ProductoModel.objects.select_for_update().get(id=item.producto_id)
                    if producto.stock_actual < item.cantidad:
                        raise Exception(
                            f"Stock insuficiente para {producto.nombre}. "
                            f"Disponible: {producto.stock_actual}, Solicitado: {item.cantidad}"
                        )
                except ProductoModel.DoesNotExist:
                    raise Exception(f"Producto no encontrado: {item.producto_id}")
        
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
            
            # DESCONTAR STOCK AQUÍ (orden PENDIENTE)
            # El stock se devuelve solo si se CANCELA la orden
            stock_anterior = producto.stock_actual
            producto.stock_actual -= item.cantidad
            producto.save()
            print(f'📦 Stock descontado: {producto.nombre} - {item.cantidad} unidades. Stock anterior: {stock_anterior}, Stock nuevo: {producto.stock_actual}')
        
        items_response.append({
            'producto_id': item.producto_id or 'sin-id',
            'nombre': producto_nombre,
            'cantidad': item.cantidad,
            'precio_unitario': item.precio_unitario,
            'subtotal': float(subtotal)
        })
    
    # Preparar datos de productos para el email (con imágenes)
    productos_email = []
    for item in data.items:
        producto_data = {'nombre': item.nombre or 'Producto', 'cantidad': item.cantidad, 'imagen': ''}
        if item.producto_id and item.producto_id != '00000000-0000-0000-0000-000000000000':
            try:
                producto_obj = ProductoModel.objects.get(id=item.producto_id)
                producto_data['nombre'] = producto_obj.nombre
                # Obtener URL de la primera imagen si existe (imagenes es ForeignKey related_name)
                primera_imagen_obj = producto_obj.imagenes.filter(es_principal=True).first()
                if not primera_imagen_obj:
                    primera_imagen_obj = producto_obj.imagenes.order_by('orden').first()
                
                if primera_imagen_obj:
                    url_imagen = primera_imagen_obj.url
                    producto_data['imagen'] = url_imagen if url_imagen.startswith('http') else f"http://localhost:8000{url_imagen}"
            except Exception as e:
                print(f"⚠️ Error obteniendo imagen del producto {item.producto_id}: {e}")
        productos_email.append(producto_data)
    
    try:
        direccion_completa = ", ".join(filter(None, [orden.direccion_envio, orden.municipio, orden.departamento]))
        
        print(f"📧 Enviando email de confirmación a {cliente.email} - Orden: {orden.codigo}")
        msg_id = send_order_status_email(
            email=cliente.email,
            nombre=f"{cliente.nombre} {cliente.apellido}".strip(),
            codigo=orden.codigo,
            estado='pendiente',
            total=float(orden.total_monto),
            direccion=direccion_completa,
            productos=productos_email,
        )
        # Guardar Message-ID para threading
        if msg_id:
            orden.email_thread_id = msg_id
            orden.save()
        print(f"✅ Email de confirmación enviado exitosamente - Message ID: {msg_id}")
    except Exception as e:
        # No bloquear la creación de la orden por fallos de email
        print(f"❌ Error enviando email de confirmación: {e}")
        import traceback
        traceback.print_exc()

    return {
        'id': str(orden.id),
        'codigo': orden.codigo,
        'estado': orden.estado,
        'cliente_nombre': f"{cliente.nombre} {cliente.apellido}",
        'cliente_email': cliente.email,
        'cliente_telefono': cliente.telefono or '',
        'cliente_tipo_doc': cliente.tipo_documento or 'CC',
        'cliente_num_doc': cliente.numero_documento or '',
        'direccion_envio': orden.direccion_envio,
        'departamento': orden.departamento,
        'municipio': orden.municipio,
        'barrio': orden.barrio or '',
        'notas_envio': orden.notas_envio or '',
        'subtotal_monto': float(orden.subtotal_monto),
        'envio_monto': float(orden.envio_monto),
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
    """Actualiza estado de una orden (sync) y devuelve stock si se CANCELA"""
    from django.db import transaction
    
    estados_validos = ['pendiente', 'confirmada', 'en_proceso', 'enviada', 'completada', 'cancelada']
    estado_nuevo = estado.lower()
    
    if estado_nuevo not in estados_validos:
        raise ValueError(f"Estado inválido. Estados válidos: {estados_validos}")
    
    with transaction.atomic():
        orden = OrdenModel.objects.select_for_update().get(id=orden_id)
        estado_anterior = orden.estado
        
        # Si cambia a CANCELADA → Devolver stock
        if estado_nuevo == 'cancelada' and estado_anterior != 'cancelada':
            print(f'↩️ Cancelando orden {orden.codigo} - Devolviendo stock...')
            
            # Obtener líneas de la orden
            lineas = LineaOrdenModel.objects.filter(orden=orden).select_related('producto')
            
            for linea in lineas:
                if linea.producto:
                    # Bloqueo pesimista del producto
                    producto = ProductoModel.objects.select_for_update().get(id=linea.producto_id)
                    
                    # Devolver stock
                    stock_anterior = producto.stock_actual
                    producto.stock_actual += linea.cantidad
                    producto.save()
                    
                    print(f'✅ Stock devuelto: {producto.nombre} - {linea.cantidad} unidades. '
                          f'Stock anterior: {stock_anterior}, Stock nuevo: {producto.stock_actual}')
        
        # Actualizar estado
        orden.estado = estado_nuevo
        orden.save()

        try:
            if orden.cliente:
                # Obtener productos con imágenes
                lineas_orden = LineaOrdenModel.objects.filter(orden=orden).select_related('producto').prefetch_related('producto__imagenes')
                productos_email = []
                for linea in lineas_orden:
                    producto_data = {
                        'nombre': linea.producto.nombre if linea.producto else 'Producto',
                        'cantidad': linea.cantidad,
                        'imagen': ''
                    }
                    if linea.producto:
                        # Buscar imagen principal o la primera disponible
                        primera_imagen_obj = linea.producto.imagenes.filter(es_principal=True).first()
                        if not primera_imagen_obj:
                            primera_imagen_obj = linea.producto.imagenes.order_by('orden').first()
                        
                        if primera_imagen_obj:
                            url_imagen = primera_imagen_obj.url
                            producto_data['imagen'] = url_imagen if url_imagen.startswith('http') else f"http://localhost:8000{url_imagen}"
                    
                    productos_email.append(producto_data)
                
                direccion_completa = ", ".join(filter(None, [orden.direccion_envio, orden.municipio, orden.departamento]))
                
                print(f"📧 Enviando email de cambio de estado a {orden.cliente.email} - Estado: {estado_nuevo}")
                send_order_status_email(
                    email=orden.cliente.email,
                    nombre=f"{orden.cliente.nombre} {orden.cliente.apellido}".strip(),
                    codigo=orden.codigo,
                    estado=estado_nuevo,
                    total=float(orden.total_monto),
                    direccion=direccion_completa,
                    productos=productos_email,
                    thread_id=orden.email_thread_id or None,  # Threading: encadenar como respuesta
                )
                print(f"✅ Email enviado exitosamente")
        except Exception as e:
            # No bloquear el cambio de estado por fallas de email
            print(f"❌ Error enviando email de cambio de estado: {e}")
            import traceback
            traceback.print_exc()
    
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


@router.get("/mis-ordenes", response_model=List[dict])
async def obtener_mis_ordenes(email: str):
    """
    Obtiene todas las órdenes del usuario autenticado.
    
    Query Parameters:
    - email: Email del usuario
    
    Retorna lista de órdenes con todos sus detalles.
    """
    try:
        resultado = await sync_to_async(_listar_ordenes_por_email_sync)(email)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener órdenes: {str(e)}"
        )


@router.post("/validar-stock", response_model=ValidarStockResponse)
async def validar_stock(data: ValidarStockInput):
    """
    Valida disponibilidad de stock sin hacer descuentos.
    Util para mostrar advertencias en carrito/checkout antes de enviar la orden.
    
    Response:
    - disponible: bool - Si hay stock para todos los productos
    - productos: list - Detalle de cada producto (stock_disponible, stock_solicitado, etc)
    - mensaje: str - Mensaje amigable
    """
    try:
        resultado = await sync_to_async(_validar_stock_sync)(data.items)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al validar stock: {str(e)}"
        )


@router.post("", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=OrdenResponse, status_code=status.HTTP_201_CREATED)
async def crear_orden(data: CrearOrdenInput):
    """
    Crea una nueva orden desde el checkout con validacion atomica de stock.
    - Valida stock de forma atomica (transaccion con bloqueo pesimista)
    - Si el cliente no existe (por email), lo crea automaticamente.
    - Genera codigo unico KH-XXXX
    - Descuenta stock automaticamente si hay disponible
    - Estado inicial: PENDIENTE
    """
    try:
        resultado = await sync_to_async(_crear_orden_sync)(data)
        return resultado
    except Exception as e:
        # Diferenciar errores de stock de otros errores
        error_msg = str(e)
        if "Stock insuficiente" in error_msg or "Producto no encontrado" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_msg
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la orden: {error_msg}"
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


@router.post("/{orden_id}/confirmar")
async def confirmar_orden(orden_id: str):
    """
    Confirma el pago de una orden (cambia estado a CONFIRMADA).
    
    Este endpoint es llamado por el admin cuando confirma que el pago fue recibido.
    El stock ya fue descontado cuando la orden se creó en estado PENDIENTE.
    """
    try:
        resultado = await sync_to_async(_actualizar_estado_sync)(orden_id, 'confirmada')
        return resultado
    except OrdenModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al confirmar orden: {str(e)}"
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
