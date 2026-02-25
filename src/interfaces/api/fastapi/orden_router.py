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

from infrastructure.persistence.django.models import OrdenModel, LineaOrdenModel, ClienteModel, ProductoModel, ProductoVarianteModel
from infrastructure.notifications.email_service import send_order_status_email
from interfaces.api.fastapi.dependencies import get_current_user_email


router = APIRouter(prefix="/api/v1/ordenes", tags=["ordenes"])


# ═══════════════════════════════════════════════════════════════════════════
# DTOs / Schemas
# ═══════════════════════════════════════════════════════════════════════════

class LineaOrdenInput(BaseModel):
    producto_id: Optional[str] = None
    variante_id: Optional[str] = None
    variante_sku: Optional[str] = None
    color: Optional[str] = None
    largo: Optional[str] = None
    cantidad: int
    precio_unitario: float
    nombre: Optional[str] = None


class CrearOrdenInput(BaseModel):
    """Input para crear orden desde checkout"""
    email: EmailStr
    nombre: str
    apellido: Optional[str] = ''
    telefono: str
    tipo_documento: Optional[str] = 'CC'
    numero_documento: Optional[str] = ''
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
    estado_pago: str
    estado_envio: str
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
    guia_envio: Optional[str] = ''
    link_rastreo: Optional[str] = ''
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
    estado_pago: str
    estado_envio: str
    cliente_nombre: str
    cliente_email: str
    cliente_telefono: str
    total: float
    total_items: int
    metodo_pago: str
    fecha_creacion: datetime
    # Campos adicionales para evitar segunda llamada
    subtotal_monto: Optional[float] = 0.0
    envio_monto: Optional[float] = 0.0
    direccion_envio: Optional[str] = ''
    departamento: Optional[str] = ''
    municipio: Optional[str] = ''
    barrio: Optional[str] = ''
    notas_envio: Optional[str] = ''
    guia_envio: Optional[str] = ''
    link_rastreo: Optional[str] = ''
    cliente_tipo_doc: Optional[str] = ''
    cliente_num_doc: Optional[str] = ''
    items: Optional[List[dict]] = None  # Solo se incluye si include_items=true


class CambiarEstadoInput(BaseModel):
    estado: Optional[str] = None
    estado_pago: Optional[str] = None
    estado_envio: Optional[str] = None
    guia_envio: Optional[str] = None
    link_rastreo: Optional[str] = None


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

def _legacy_estado_from_states(estado_pago: str, estado_envio: str) -> str:
    pago = (estado_pago or 'pendiente').lower()
    envio = (estado_envio or 'no_enviado').lower()

    if pago == 'cancelado':
        return 'cancelada'
    if envio == 'entregado':
        return 'completada'
    if envio == 'enviado':
        return 'enviada'
    if pago == 'pagado':
        return 'confirmada'
    return 'pendiente'


def _states_from_legacy_estado(estado: str) -> tuple[str, str]:
    raw = (estado or 'pendiente').lower()
    if raw in {'cancelada', 'cancelado'}:
        return ('cancelado', 'no_enviado')
    if raw in {'completada', 'entregada', 'entregado'}:
        return ('pagado', 'entregado')
    if raw in {'enviada', 'enviado'}:
        return ('pagado', 'enviado')
    if raw in {'confirmada', 'pagada', 'pagado'}:
        return ('pagado', 'no_enviado')
    return ('pendiente', 'no_enviado')

def _listar_ordenes_sync(estado: Optional[str], limite: int, include_items: bool = False) -> List[dict]:
    """Lista órdenes (sync) - Optimizado con annotate y prefetch_related"""
    from django.db.models import Count, Prefetch
    
    # Query base optimizada con select_related para cliente
    queryset = (OrdenModel.objects
                .select_related('cliente')
                .annotate(num_items=Count('lineas'))
                .order_by('-fecha_creacion'))
    
    # Si se incluyen items, hacer prefetch optimizado
    if include_items:
        queryset = queryset.prefetch_related(
            Prefetch('lineas', queryset=LineaOrdenModel.objects.select_related('producto').prefetch_related('producto__imagenes').only(
                'id', 'orden_id', 'producto_id', 'cantidad', 
                'precio_unitario_monto', 'subtotal_monto',
                'variante_sku', 'color_snapshot', 'largo_snapshot',
                'producto__id', 'producto__nombre', 'producto__codigo', 'producto__imagen_principal'
            ))
        )
    
    if estado:
        queryset = queryset.filter(estado=estado.lower())
    
    # Usar only() para traer solo los campos necesarios
    queryset = queryset.only(
        'id', 'codigo', 'estado', 'estado_pago', 'estado_envio', 'metodo_pago', 'fecha_creacion',
        'total_monto', 'subtotal_monto', 'envio_monto',
        'direccion_envio', 'departamento', 'municipio', 'barrio', 'notas_envio', 'guia_envio', 'link_rastreo',
        'cliente__id', 'cliente__nombre', 'cliente__apellido', 
        'cliente__email', 'cliente__telefono',
        'cliente__tipo_documento', 'cliente__numero_documento'
    )
    
    ordenes = list(queryset[:limite])
    
    resultado = []
    for orden in ordenes:
        pago_fallback, envio_fallback = _states_from_legacy_estado(orden.estado)
        estado_pago = getattr(orden, 'estado_pago', None) or pago_fallback
        estado_envio = getattr(orden, 'estado_envio', None) or envio_fallback
        orden_data = {
            'id': str(orden.id),
            'codigo': orden.codigo or f"ORD-{str(orden.id)[:8]}",
            'estado': orden.estado.upper(),
            'estado_pago': estado_pago.upper(),
            'estado_envio': estado_envio.upper(),
            'cliente_nombre': f"{orden.cliente.nombre} {orden.cliente.apellido}".strip() if orden.cliente else "Sin cliente",
            'cliente_email': orden.cliente.email if orden.cliente else "",
            'cliente_telefono': orden.cliente.telefono if orden.cliente else "",
            'cliente_tipo_doc': orden.cliente.tipo_documento if orden.cliente else "",
            'cliente_num_doc': orden.cliente.numero_documento if orden.cliente else "",
            'total': float(orden.total_monto),
            'subtotal_monto': float(orden.subtotal_monto),
            'envio_monto': float(orden.envio_monto),
            'direccion_envio': orden.direccion_envio or '',
            'departamento': orden.departamento or '',
            'municipio': orden.municipio or '',
            'barrio': orden.barrio or '',
            'notas_envio': orden.notas_envio or '',
            'guia_envio': orden.guia_envio or '',
            'link_rastreo': orden.link_rastreo or '',
            'total_items': orden.num_items,
            'metodo_pago': orden.metodo_pago or 'whatsapp',
            'fecha_creacion': orden.fecha_creacion,
            'items': None
        }
        
        # Incluir items si se solicitó
        if include_items:
            items = []
            for linea in orden.lineas.all():
                imagen_url = ''
                if linea.producto:
                    imagen_url = getattr(linea.producto, 'imagen_principal', None) or ''
                    if not imagen_url and hasattr(linea.producto, 'imagenes'):
                        primera_img = linea.producto.imagenes.first()
                        if primera_img:
                            imagen_url = primera_img.url
                if imagen_url and not imagen_url.startswith('http'):
                    imagen_url = f"http://localhost:8000{imagen_url}"
                items.append({
                    'id': str(linea.id),
                    'producto_id': str(linea.producto_id),
                    'sku': linea.producto.codigo if linea.producto else 'N/A',
                    'variante_sku': linea.variante_sku or '',
                    'color': linea.color_snapshot or '',
                    'largo': linea.largo_snapshot or '',
                    'nombre': linea.producto.nombre if linea.producto else 'Producto',
                    'cantidad': linea.cantidad,
                    'precio_unitario': float(linea.precio_unitario_monto),
                    'subtotal': float(linea.subtotal_monto),
                    'imagen': imagen_url
                })
            orden_data['items'] = items
        
        resultado.append(orden_data)
    
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
                .prefetch_related(
                    Prefetch('lineas', queryset=LineaOrdenModel.objects.select_related('producto'))
                )
                .order_by('-fecha_creacion'))
    
    ordenes = list(queryset)
    
    resultado = []
    for orden in ordenes:
        pago_fallback, envio_fallback = _states_from_legacy_estado(orden.estado)
        estado_pago = getattr(orden, 'estado_pago', None) or pago_fallback
        estado_envio = getattr(orden, 'estado_envio', None) or envio_fallback
        # Obtener items de la orden
        items = []
        for linea in orden.lineas.all():
            producto = linea.producto
            # Intentar obtener imagen: primero imagen_principal, luego primera imagen de la galería
            imagen_url = None
            if producto:
                imagen_url = getattr(producto, 'imagen_principal', None) or None
                if not imagen_url:
                    primera_img = producto.imagenes.first() if hasattr(producto, 'imagenes') else None
                    if primera_img:
                        imagen_url = primera_img.url
            
            items.append({
                'id': str(linea.id),
                'producto_id': str(producto.id) if producto else '',
                'sku': getattr(producto, 'codigo', '') if producto else '',
                'variante_sku': linea.variante_sku or '',
                'color': linea.color_snapshot or '',
                'largo': linea.largo_snapshot or '',
                'nombre': getattr(producto, 'nombre', '') if producto else '',
                'cantidad': linea.cantidad,
                'precio': float(getattr(linea, 'precio_unitario_monto', 0) or 0),
                'moneda': getattr(linea, 'precio_unitario_moneda', 'USD'),
                'imagen': imagen_url
            })
        
        resultado.append({
            'id': str(orden.id),
            'numero': orden.codigo or f"ORD-{str(orden.id)[:8]}",
            'estado': orden.estado,
            'estado_pago': estado_pago,
            'estado_envio': estado_envio,
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
        if item.variante_id:
            try:
                variante = ProductoVarianteModel.objects.select_related('producto').get(id=item.variante_id)
                if item.producto_id and str(variante.producto_id) != str(item.producto_id):
                    raise ProductoVarianteModel.DoesNotExist
                disponible = variante.stock_actual >= item.cantidad
                todos_disponibles = todos_disponibles and disponible

                productos_info.append({
                    'producto_id': str(variante.producto_id),
                    'variante_id': str(variante.id),
                    'nombre': variante.producto.nombre,
                    'color': variante.color,
                    'largo': variante.largo,
                    'stock_solicitado': item.cantidad,
                    'stock_disponible': variante.stock_actual,
                    'disponible': disponible,
                    'mensaje': 'Stock disponible' if disponible else f'Solo hay {variante.stock_actual} disponibles'
                })
            except ProductoVarianteModel.DoesNotExist:
                productos_info.append({
                    'producto_id': item.producto_id or '',
                    'variante_id': item.variante_id,
                    'nombre': item.nombre or 'Producto desconocido',
                    'stock_solicitado': item.cantidad,
                    'stock_disponible': 0,
                    'disponible': False,
                    'mensaje': 'Variante no encontrada'
                })
                todos_disponibles = False
            continue

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
    from infrastructure.auth.models import Usuario
    from uuid import UUID
    
    with transaction.atomic():
        if not data.items:
            raise Exception("La orden debe incluir al menos un producto")

        def normalize_uuid(value):
            if not value:
                return None
            if isinstance(value, str) and value.strip().lower() in {'null', 'none', 'undefined'}:
                return None
            try:
                return str(UUID(str(value)))
            except Exception:
                return None

        # 0. VALIDAR STOCK PRIMERO (con bloqueo pesimista)
        for item in data.items:
            variante_id = normalize_uuid(item.variante_id)
            producto_id = normalize_uuid(item.producto_id)

            if variante_id:
                try:
                    variante = ProductoVarianteModel.objects.select_for_update().select_related('producto').get(id=variante_id)
                    if producto_id and str(variante.producto_id) != str(producto_id):
                        raise Exception("Variante no corresponde al producto solicitado")
                    if variante.stock_actual < item.cantidad:
                        raise Exception(
                            f"Stock insuficiente para variante {variante.sku}. "
                            f"Disponible: {variante.stock_actual}, Solicitado: {item.cantidad}"
                        )
                except ProductoVarianteModel.DoesNotExist:
                    raise Exception(f"Variante no encontrada: {variante_id}")
                continue

            if producto_id and producto_id != '00000000-0000-0000-0000-000000000000':
                try:
                    producto = ProductoModel.objects.select_for_update().get(id=producto_id)
                    if producto.stock_actual < item.cantidad:
                        raise Exception(
                            f"Stock insuficiente para {producto.nombre}. "
                            f"Disponible: {producto.stock_actual}, Solicitado: {item.cantidad}"
                        )
                except ProductoModel.DoesNotExist:
                    raise Exception(f"Producto no encontrado: {producto_id}")
        
        # 1. Obtener o crear cliente
        # Buscar primero por email
        cliente = ClienteModel.objects.filter(email=data.email).first()
    
        tipo_doc = data.tipo_documento or None
        numero_doc = data.numero_documento or None

        if not numero_doc:
            usuario = Usuario.objects.filter(email=data.email, tipo='MAYORISTA').first()
            if usuario and usuario.numero_documento:
                tipo_doc = usuario.tipo_documento or 'CC'
                numero_doc = usuario.numero_documento

        if not numero_doc:
            numero_doc = f"AUTO-{uuid4().hex[:8].upper()}"
        if not tipo_doc:
            tipo_doc = 'CC'

        # Si no encontramos por email, buscar por número de documento
        if not cliente and numero_doc and not numero_doc.startswith('AUTO-'):
            cliente = ClienteModel.objects.filter(numero_documento=numero_doc).first()
            if cliente:
                # Actualizar email del cliente existente
                cliente.email = data.email
                cliente.save()

        if not cliente:
            cliente = ClienteModel.objects.create(
                id=uuid4(),
                email=data.email,
                nombre=data.nombre,
                apellido=data.apellido,
                telefono=data.telefono,
                tipo_documento=tipo_doc,
                numero_documento=numero_doc,
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
            # Actualizar documento SOLO si el cliente no tiene uno (evita violación de unique constraint)
            if numero_doc and not cliente.numero_documento:
                cliente.numero_documento = numero_doc
                actualizado = True
            if tipo_doc and not cliente.tipo_documento:
                cliente.tipo_documento = tipo_doc
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
        # Si el pago fue por Wompi, la orden ya está pagada
        estado_pago = 'pagado' if data.metodo_pago == 'wompi' else 'pendiente'
        estado_envio = 'no_enviado'
        estado_inicial = _legacy_estado_from_states(estado_pago, estado_envio)
    
        orden = OrdenModel.objects.create(
            id=uuid4(),
            cliente=cliente,
            codigo=codigo,
            direccion_envio=data.direccion,
            departamento=data.departamento,
            municipio=data.municipio,
            barrio=data.barrio or '',
            notas_envio=data.notas or '',
            estado=estado_inicial,
            estado_pago=estado_pago,
            estado_envio=estado_envio,
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
            variante_id = normalize_uuid(item.variante_id)
            producto_id = normalize_uuid(item.producto_id)
            producto = None
            variante = None
            producto_nombre = item.nombre or 'Producto'
        
            if variante_id:
                try:
                    variante = ProductoVarianteModel.objects.select_related('producto').get(id=variante_id)
                    producto = variante.producto
                    producto_nombre = producto.nombre
                except (ProductoVarianteModel.DoesNotExist, Exception):
                    variante = None
                    producto = None

            # Intentar buscar el producto si hay producto_id válido
            if not producto and producto_id and producto_id != '00000000-0000-0000-0000-000000000000':
                try:
                    producto = ProductoModel.objects.get(id=producto_id)
                    producto_nombre = producto.nombre
                except (ProductoModel.DoesNotExist, Exception):
                    producto = None
        
            subtotal = Decimal(str(item.precio_unitario)) * item.cantidad
        
            if not producto:
                raise Exception(f"Producto no encontrado para item: {item.nombre or item.producto_id}")

            LineaOrdenModel.objects.create(
                id=uuid4(),
                orden=orden,
                producto=producto,
                variante_id=variante_id,
                cantidad=item.cantidad,
                precio_unitario_monto=Decimal(str(item.precio_unitario)),
                precio_unitario_moneda='COP',
                subtotal_monto=subtotal,
                subtotal_moneda='COP',
                variante_sku=item.variante_sku or (variante.sku if variante else '') or '',
                color_snapshot=item.color or (variante.color or '' if variante else ''),
                largo_snapshot=item.largo or (variante.largo or '' if variante else '')
            )

            # DESCONTAR STOCK AQUÍ (orden PENDIENTE)
            # El stock se devuelve solo si se CANCELA la orden
            # ⚠️ IMPORTANTE: Descontar SOLO de variante O producto base, NUNCA ambos
            if variante:
                # Si hay variante: descontar SOLO de la variante
                stock_anterior = variante.stock_actual
                variante.stock_actual -= item.cantidad
                variante.save()
                print(
                    f'📦 Stock descontado de VARIANTE: {producto.nombre} ({variante.sku}) - {item.cantidad} unidades. '
                    f'Stock anterior: {stock_anterior}, stock nuevo: {variante.stock_actual}'
                )
            else:
                # Si NO hay variante: descontar del producto base
                stock_anterior = producto.stock_actual
                producto.stock_actual -= item.cantidad
                producto.save()
                print(f'📦 Stock descontado de PRODUCTO BASE: {producto.nombre} - {item.cantidad} unidades. Stock anterior: {stock_anterior}, Stock nuevo: {producto.stock_actual}')

            items_response.append({
                'producto_id': producto_id or 'sin-id',
                'variante_id': variante_id,
                'nombre': producto_nombre,
                'cantidad': item.cantidad,
                'precio_unitario': item.precio_unitario,
                'subtotal': float(subtotal),
                'variante_sku': item.variante_sku or (variante.sku if variante else '') or '',
                'color': item.color or (variante.color or '' if variante else ''),
                'largo': item.largo or (variante.largo or '' if variante else '')
            })
    
    # Preparar datos de productos para el email (con imágenes)
    productos_email = []
    for item in data.items:
        producto_data = {
            'nombre': item.nombre or 'Producto',
            'cantidad': item.cantidad,
            'precio_unitario': float(item.precio_unitario),
            'imagen': ''
        }
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

        # Si el pago fue con tarjeta (Wompi), enviar también el email de pedido confirmado
        if data.metodo_pago == 'wompi':
            print(f"📧 Enviando email de pedido confirmado a {cliente.email} - Orden: {orden.codigo}")
            send_order_status_email(
                email=cliente.email,
                nombre=f"{cliente.nombre} {cliente.apellido}".strip(),
                codigo=orden.codigo,
                estado='confirmada',
                total=float(orden.total_monto),
                direccion=direccion_completa,
                productos=productos_email,
                thread_id=orden.email_thread_id or msg_id or None,
            )
            print("✅ Email de pedido confirmado enviado exitosamente")
    except Exception as e:
        # No bloquear la creación de la orden por fallos de email
        print(f"❌ Error enviando email de confirmación: {e}")
        import traceback
        traceback.print_exc()

    return {
        'id': str(orden.id),
        'codigo': orden.codigo,
        'estado': orden.estado,
        'estado_pago': estado_pago,
        'estado_envio': estado_envio,
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
        'guia_envio': orden.guia_envio or '',
        'link_rastreo': orden.link_rastreo or '',
        'subtotal_monto': float(orden.subtotal_monto),
        'envio_monto': float(orden.envio_monto),
        'total': float(orden.total_monto),
        'metodo_pago': orden.metodo_pago,
        'items': items_response,
        'fecha_creacion': orden.fecha_creacion
    }


def _obtener_orden_sync(orden_id: str) -> dict:
    """Obtiene detalle de una orden (sync)"""
    orden = OrdenModel.objects.select_related('cliente').prefetch_related('lineas__producto', 'lineas__producto__imagenes').get(id=orden_id)
    
    items = []
    for linea in orden.lineas.all():
        imagen_url = ''
        if linea.producto:
            imagen_url = getattr(linea.producto, 'imagen_principal', None) or ''
            if not imagen_url and hasattr(linea.producto, 'imagenes'):
                primera_img = linea.producto.imagenes.first()
                if primera_img:
                    imagen_url = primera_img.url
        if imagen_url and not imagen_url.startswith('http'):
            imagen_url = f"http://localhost:8000{imagen_url}"
        items.append({
            'id': str(linea.id),
            'producto_id': str(linea.producto_id),
            'sku': linea.producto.codigo if linea.producto else 'N/A',
            'variante_sku': linea.variante_sku or '',
            'color': linea.color_snapshot or '',
            'largo': linea.largo_snapshot or '',
            'nombre': linea.producto.nombre if linea.producto else 'Producto',
            'cantidad': linea.cantidad,
            'precio_unitario': float(linea.precio_unitario_monto),
            'subtotal': float(linea.subtotal_monto),
            'imagen': imagen_url
        })
    
    return {
        'id': str(orden.id),
        'codigo': orden.codigo,
        'estado': orden.estado.upper(),
        'estado_pago': (orden.estado_pago or _states_from_legacy_estado(orden.estado)[0]).upper(),
        'estado_envio': (orden.estado_envio or _states_from_legacy_estado(orden.estado)[1]).upper(),
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
        'guia_envio': orden.guia_envio or '',
        'link_rastreo': orden.link_rastreo or '',
        'subtotal_monto': float(orden.subtotal_monto),
        'envio_monto': float(orden.envio_monto),
        'total': float(orden.total_monto),
        'metodo_pago': orden.metodo_pago or 'whatsapp',
        'items': items,
        'fecha_creacion': orden.fecha_creacion
    }


def _guardar_rastreo_sync(
    orden_id: str,
    guia_envio: Optional[str] = None,
    link_rastreo: Optional[str] = None
) -> dict:
    """Guarda solo guía y link de rastreo SIN cambiar estado ni enviar email."""
    from django.db import transaction

    with transaction.atomic():
        orden = OrdenModel.objects.select_for_update().get(id=orden_id)
        if orden.estado_pago != 'pagado':
            raise ValueError("No se puede actualizar rastreo si el pago no está confirmado")

        if guia_envio is not None:
            orden.guia_envio = guia_envio or ''
        if link_rastreo is not None:
            orden.link_rastreo = link_rastreo or ''
        orden.save()

    return {
        "mensaje": "Datos de rastreo guardados",
        "guia_envio": orden.guia_envio or '',
        "link_rastreo": orden.link_rastreo or ''
    }


def _enviar_email_estado(orden: OrdenModel, estado_nuevo: str) -> None:
    try:
        if not orden.cliente:
            return

        lineas_orden = LineaOrdenModel.objects.filter(orden=orden).select_related('producto').prefetch_related('producto__imagenes')
        productos_email = []
        for linea in lineas_orden:
            producto_data = {
                'nombre': linea.producto.nombre if linea.producto else 'Producto',
                'cantidad': linea.cantidad,
                'precio_unitario': float(linea.precio_unitario_monto),
                'imagen': ''
            }
            if linea.producto:
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
            thread_id=orden.email_thread_id or None,
            guia_envio=orden.guia_envio or None,
            link_rastreo=orden.link_rastreo or None,
        )
        print("✅ Email enviado exitosamente")
    except Exception as e:
        print(f"❌ Error enviando email de cambio de estado: {e}")
        import traceback
        traceback.print_exc()


def _devolver_stock_si_cancelada(orden: OrdenModel) -> None:
    print(f'↩️ Cancelando orden {orden.codigo} - Devolviendo stock...')
    from infrastructure.persistence.django.models import ProductoVarianteModel
    
    lineas = LineaOrdenModel.objects.filter(orden=orden).select_related('producto')
    for linea in lineas:
        if linea.variante_id:
            # 🎯 Si la orden usó una VARIANTE, devolver stock a la variante
            try:
                variante = ProductoVarianteModel.objects.select_for_update().get(id=linea.variante_id)
                stock_anterior = variante.stock_actual
                variante.stock_actual += linea.cantidad
                variante.save()
                print(
                    f'✅ Stock devuelto a VARIANTE: {linea.producto.nombre} ({linea.color_snapshot} {linea.largo_snapshot}) '
                    f'- {linea.cantidad} unidades. Stock anterior: {stock_anterior}, Stock nuevo: {variante.stock_actual}'
                )
            except ProductoVarianteModel.DoesNotExist:
                print(f'⚠️ ADVERTENCIA: Variante {linea.variante_id} no encontrada. Devolviendo al producto base como fallback.')
                if linea.producto:
                    producto = ProductoModel.objects.select_for_update().get(id=linea.producto_id)
                    stock_anterior = producto.stock_actual
                    producto.stock_actual += linea.cantidad
                    producto.save()
                    print(f'✅ Stock devuelto a PRODUCTO BASE: {producto.nombre} - {linea.cantidad} unidades.')
        elif linea.producto:
            # Si NO hay variante, devolver al producto base
            producto = ProductoModel.objects.select_for_update().get(id=linea.producto_id)
            stock_anterior = producto.stock_actual
            producto.stock_actual += linea.cantidad
            producto.save()
            print(
                f'✅ Stock devuelto a PRODUCTO: {producto.nombre} - {linea.cantidad} unidades. '
                f'Stock anterior: {stock_anterior}, Stock nuevo: {producto.stock_actual}'
            )



def _actualizar_estado_pago_sync(orden_id: str, estado_pago: str) -> dict:
    from django.db import transaction

    estados_validos = ['pendiente', 'pagado', 'cancelado']
    estado_nuevo = (estado_pago or '').lower()
    if estado_nuevo not in estados_validos:
        raise ValueError(f"Estado de pago inválido. Estados válidos: {estados_validos}")

    with transaction.atomic():
        orden = OrdenModel.objects.select_for_update().get(id=orden_id)

        if estado_nuevo == 'pagado':
            if not orden.lineas.exists():
                raise ValueError("No se puede confirmar una orden sin productos")

        if estado_nuevo == 'cancelado' and orden.estado_pago != 'cancelado':
            _devolver_stock_si_cancelada(orden)
            orden.estado_envio = 'no_enviado'
        if estado_nuevo in {'pendiente', 'cancelado'}:
            orden.estado_envio = 'no_enviado'

        orden.estado_pago = estado_nuevo
        orden.estado = _legacy_estado_from_states(orden.estado_pago, orden.estado_envio)
        orden.save()

        _enviar_email_estado(orden, orden.estado)

    return {"mensaje": "Estado de pago actualizado", "estado_pago": estado_nuevo.upper()}


def _actualizar_estado_envio_sync(
    orden_id: str,
    estado_envio: str,
    guia_envio: Optional[str] = None,
    link_rastreo: Optional[str] = None,
    enviar_email: bool = True  # Por defecto envía email al cambiar estado
) -> dict:
    from django.db import transaction

    estados_validos = ['no_enviado', 'enviado', 'entregado']
    estado_nuevo = (estado_envio or '').lower()
    if estado_nuevo not in estados_validos:
        raise ValueError(f"Estado de envío inválido. Estados válidos: {estados_validos}")

    with transaction.atomic():
        orden = OrdenModel.objects.select_for_update().get(id=orden_id)
        if orden.estado_pago != 'pagado':
            raise ValueError("No se puede actualizar envío si el pago no está confirmado")

        # Guardar el estado anterior para saber si cambió
        estado_anterior = orden.estado_envio
        
        orden.estado_envio = estado_nuevo
        if guia_envio is not None:
            orden.guia_envio = guia_envio or ''
        if link_rastreo is not None:
            orden.link_rastreo = link_rastreo or ''
        if estado_nuevo == 'no_enviado':
            orden.guia_envio = ''
            orden.link_rastreo = ''
        orden.estado = _legacy_estado_from_states(orden.estado_pago, orden.estado_envio)
        orden.save()

        # Solo enviar email si: 1) Cambió el estado Y 2) enviar_email es True
        if enviar_email and estado_anterior != estado_nuevo:
            _enviar_email_estado(orden, orden.estado)

    return {"mensaje": "Estado de envío actualizado", "estado_envio": estado_nuevo.upper()}


def _actualizar_estado_legacy_sync(orden_id: str, estado: str) -> dict:
    from django.db import transaction

    estados_validos = ['pendiente', 'confirmada', 'en_proceso', 'enviada', 'completada', 'cancelada']
    estado_nuevo = (estado or '').lower()
    if estado_nuevo not in estados_validos:
        raise ValueError(f"Estado inválido. Estados válidos: {estados_validos}")

    estado_pago, estado_envio = _states_from_legacy_estado(estado_nuevo)

    with transaction.atomic():
        orden = OrdenModel.objects.select_for_update().get(id=orden_id)

        if estado_pago == 'pagado':
            if not orden.lineas.exists():
                raise ValueError("No se puede confirmar una orden sin productos")

        if estado_pago == 'cancelado' and orden.estado_pago != 'cancelado':
            _devolver_stock_si_cancelada(orden)

        orden.estado_pago = estado_pago
        orden.estado_envio = estado_envio
        orden.estado = estado_nuevo
        orden.save()

        _enviar_email_estado(orden, orden.estado)

    return {"mensaje": "Estado actualizado", "estado": estado_nuevo.upper()}


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════

@router.get("", response_model=List[OrdenListItem])
@router.get("/", response_model=List[OrdenListItem])
async def listar_ordenes(
    estado: Optional[str] = None, 
    limite: int = 50,
    include_items: bool = False
):
    """
    Lista todas las órdenes (para admin).
    
    Parámetros:
    - estado: Filtrar por estado (pendiente, confirmada, etc.)
    - limite: Número máximo de órdenes a retornar
    - include_items: Si es True, incluye los items de cada orden (evita segunda llamada)
    """
    try:
        resultado = await sync_to_async(_listar_ordenes_sync)(estado, limite, include_items)
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


def _obtener_productos_frecuentes_sync(email: str, limit: int = 10) -> List[dict]:
    """
    Obtiene los productos más comprados por un cliente basado en su historial de órdenes.
    Solo incluye órdenes confirmadas/completadas.
    """
    from django.db.models import Sum, Count
    from collections import defaultdict
    
    cliente = ClienteModel.objects.filter(email=email).first()
    if not cliente:
        return []
    
    # Estados válidos para considerar como compras reales
    estados_validos = ['confirmada', 'enviada', 'entregada', 'completada', 'procesando']
    
    # Obtener todas las órdenes del cliente con estados válidos
    ordenes = OrdenModel.objects.filter(
        cliente=cliente,
        estado__in=estados_validos
    ).prefetch_related('lineas', 'lineas__producto')
    
    # Agregar productos y sus cantidades
    productos_frecuentes = defaultdict(lambda: {
        'cantidad_total': 0,
        'veces_comprado': 0,
        'ultima_compra': None,
        'producto': None
    })
    
    for orden in ordenes:
        for linea in orden.lineas.all():
            if linea.producto:
                prod_id = str(linea.producto.id)
                productos_frecuentes[prod_id]['cantidad_total'] += linea.cantidad
                productos_frecuentes[prod_id]['veces_comprado'] += 1
                productos_frecuentes[prod_id]['producto'] = linea.producto
                # Guardar la fecha más reciente
                if (productos_frecuentes[prod_id]['ultima_compra'] is None or 
                    orden.fecha_creacion > productos_frecuentes[prod_id]['ultima_compra']):
                    productos_frecuentes[prod_id]['ultima_compra'] = orden.fecha_creacion
    
    # Ordenar por cantidad total comprada (descendente)
    productos_ordenados = sorted(
        productos_frecuentes.items(),
        key=lambda x: x[1]['cantidad_total'],
        reverse=True
    )[:limit]
    
    resultado = []
    for prod_id, data in productos_ordenados:
        producto = data['producto']
        if producto:
            resultado.append({
                'id': str(producto.id),
                'name': producto.nombre,
                'category': getattr(producto.categoria, 'nombre', 'Sin categoría') if producto.categoria else 'Sin categoría',
                'price': float(producto.precio_mayorista or producto.precio or 0),
                'originalPrice': float(producto.precio or 0),
                'stock': producto.stock_actual,
                'image': producto.imagen_principal or '',
                'lastQty': data['cantidad_total'],
                'timesOrdered': data['veces_comprado'],
                'lastOrderDate': data['ultima_compra'].isoformat() if data['ultima_compra'] else None
            })
    
    return resultado


@router.get("/mis-productos-frecuentes", response_model=List[dict])
async def obtener_mis_productos_frecuentes(email: str, limit: int = 10):
    """
    Obtiene los productos más comprados por el usuario autenticado.
    
    Query Parameters:
    - email: Email del usuario
    - limit: Cantidad máxima de productos a retornar (default: 10)
    
    Retorna lista de productos ordenados por cantidad total comprada.
    """
    try:
        resultado = await sync_to_async(_obtener_productos_frecuentes_sync)(email, limit)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos frecuentes: {str(e)}"
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
        if (
            "Stock insuficiente" in error_msg
            or "Producto no encontrado" in error_msg
            or "Variante no encontrada" in error_msg
            or "Variante no corresponde" in error_msg
            or "La orden debe incluir" in error_msg
        ):
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
        resultado = await sync_to_async(_actualizar_estado_pago_sync)(orden_id, 'pagado')
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


@router.post("/{orden_id}/guardar-rastreo")
async def guardar_rastreo(orden_id: str, data: CambiarEstadoInput):
    """
    Guarda datos de rastreo (guía y link) SIN cambiar el estado de envío.
    No envía email automáticamente. Útil para guardar info antes de cambiar a "ENVIADO".
    
    Body:
    - guia_envio: Número de guía
    - link_rastreo: Link de rastreo
    """
    try:
        resultado = await sync_to_async(_guardar_rastreo_sync)(
            orden_id,
            data.guia_envio,
            data.link_rastreo
        )
        return resultado
    except OrdenModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar rastreo: {str(e)}"
        )


@router.patch("/{orden_id}")
async def actualizar_estado(orden_id: str, data: CambiarEstadoInput):
    """Actualiza el estado de una orden"""
    try:
        if data.estado_pago and data.estado_envio:
            raise ValueError("Envía solo un cambio de estado a la vez")

        if data.estado_pago:
            resultado = await sync_to_async(_actualizar_estado_pago_sync)(orden_id, data.estado_pago)
        elif data.estado_envio:
            resultado = await sync_to_async(_actualizar_estado_envio_sync)(
                orden_id,
                data.estado_envio,
                data.guia_envio,
                data.link_rastreo
            )
        elif data.estado:
            resultado = await sync_to_async(_actualizar_estado_legacy_sync)(orden_id, data.estado)
        else:
            raise ValueError("Debe enviar estado_pago o estado_envio")
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
