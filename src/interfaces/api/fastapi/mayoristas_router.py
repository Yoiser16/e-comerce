"""
Router para administrar solicitudes de mayoristas (B2B)
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from asgiref.sync import sync_to_async
from django.db import close_old_connections

from infrastructure.auth.models import Usuario
from .dependencies import get_current_admin_user, get_current_user_email, get_optional_mayorista_user

router = APIRouter(
    prefix="/api/v1",
    tags=["Mayoristas B2B"]
)


class MayoristaResponse(BaseModel):
    id: UUID
    email: str
    nombre: str
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    nombre_empresa: Optional[str] = None
    nit_empresa: Optional[str] = None
    cedula_frente: Optional[str] = None
    cedula_dorso: Optional[str] = None
    estado_mayorista: Optional[str] = None
    notas_revision: Optional[str] = None
    fecha_revision: Optional[datetime] = None
    date_joined: datetime
    descuento_mayorista: float = 0

    class Config:
        from_attributes = True


class RejectRequest(BaseModel):
    notas: Optional[str] = None


class DescuentoRequest(BaseModel):
    descuento: float


class CambiarPasswordRequest(BaseModel):
    new_password: str


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS B2B - Productos para Mayoristas
# ═══════════════════════════════════════════════════════════════════════════

class ProductoB2B(BaseModel):
    id: str
    nombre: str
    categoria: Optional[str] = None
    codigo: str
    imagen: Optional[str] = None
    precio_retail: float
    precio_mayorista: float
    stock: int
    cantidad_minima: int = 1


@router.get("/b2b/productos", response_model=List[ProductoB2B])
def obtener_productos_b2b(
    limit: int = 20, 
    offset: int = 0,
    buscar: Optional[str] = None,
    categoria: Optional[str] = None,
    limite: Optional[int] = None,
    mayorista: Optional[Usuario] = Depends(get_optional_mayorista_user)
):
    """
    Obtiene productos reales de la base de datos para mayoristas.
    Endpoint público para B2B con soporte de búsqueda y filtros.
    Si el usuario está autenticado, aplica su descuento personalizado.
    """
    # Cerrar conexiones viejas para evitar 'connection is closed'
    close_old_connections()
    try:
        from infrastructure.persistence.django.models import ProductoModel
        from django.db.models import Q
        
        # Si se proporciona limite, usarlo en vez de limit
        if limite:
            limit = limite
        
        # Consultar productos activos de la BD
        queryset = ProductoModel.objects.filter(
            activo=True,
            stock_actual__gt=0
        )
        
        # Filtro de búsqueda por nombre, código o descripción
        if buscar:
            queryset = queryset.filter(
                Q(nombre__icontains=buscar) |
                Q(codigo__icontains=buscar) |
                Q(descripcion__icontains=buscar)
            )
        
        # Filtro por categoría
        if categoria:
            queryset = queryset.filter(
                Q(categoria__nombre__iexact=categoria) |
                Q(categoria__slug__iexact=categoria)
            )
        
        productos = queryset.order_by('-total_vendidos', '-fecha_creacion')[offset:offset+limit]
        
        result = []
        for p in productos:
            result.append(ProductoB2B(
                id=str(p.id),
                nombre=p.nombre,
                categoria=p.categoria.nombre if p.categoria else None,
                codigo=p.codigo,
                imagen=p.imagen_principal,
                precio_retail=float(p.monto_precio_original or p.monto_precio),
                precio_mayorista=float(p.monto_precio) * (1.0 - (float(mayorista.descuento_mayorista) / 100.0) if mayorista and mayorista.descuento_mayorista > 0 else 0.85),  # Descuento dinámico o 15% default
                stock=p.stock_actual - p.stock_reservado,
                cantidad_minima=5 if p.metodo == 'bundle' else 1
            ))
        
        return result
    except Exception as e:
        print(f"❌ Error al obtener productos B2B: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cargar productos: {str(e)}")


@router.get("/b2b/productos/destacados", response_model=List[ProductoB2B])
def obtener_productos_destacados_b2b(
    limit: int = 10,
    mayorista: Optional[Usuario] = Depends(get_optional_mayorista_user)
):
    """
    Obtiene productos destacados reales de la base de datos para mayoristas.
    Ordena por total de ventas (bestsellers).
    """
    # Cerrar conexiones viejas para evitar 'connection is closed'
    close_old_connections()
    try:
        from infrastructure.persistence.django.models import ProductoModel
        
        # Consultar productos más vendidos
        productos = ProductoModel.objects.filter(
            activo=True,
            stock_actual__gt=0
        ).order_by('-total_vendidos', '-valoracion_promedio')[:limit]
        
        result = []
        for p in productos:
            result.append(ProductoB2B(
                id=str(p.id),
                nombre=p.nombre,
                categoria=p.categoria.nombre if p.categoria else None,
                codigo=p.codigo,
                imagen=p.imagen_principal,
                precio_retail=float(p.monto_precio_original or p.monto_precio),
                precio_mayorista=float(p.monto_precio) * (1.0 - (float(mayorista.descuento_mayorista) / 100.0) if mayorista and mayorista.descuento_mayorista > 0 else 0.85),  # Descuento dinámico o 15% default
                stock=p.stock_actual - p.stock_reservado,
                cantidad_minima=5 if p.metodo == 'bundle' else 1
            ))
        
        return result
    except Exception as e:
        print(f"❌ Error al obtener productos destacados B2B: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cargar productos: {str(e)}")


class ProductoDetalleB2B(BaseModel):
    """Schema extendido para detalle de producto B2B"""
    id: str
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[dict] = None
    categoria_nombre: Optional[str] = None
    codigo: Optional[str] = None
    sku: Optional[str] = None
    imagen_principal: Optional[str] = None
    imagenes: Optional[List[str]] = None
    precio: float  # Precio retail
    precio_mayorista: float  # Precio con descuento mayorista
    monto_precio: float  # alias para precio mayorista
    precio_original: Optional[float] = None
    stock: int
    stock_actual: int
    cantidad_minima: int = 1
    metodo: Optional[str] = None
    color: Optional[str] = None
    largo: Optional[str] = None
    tipo: Optional[str] = None
    origen: Optional[str] = None
    calidad: Optional[str] = None
    activo: bool = True


@router.get("/b2b/productos/{producto_id}", response_model=ProductoDetalleB2B)
def obtener_producto_b2b(
    producto_id: str,
    mayorista: Optional[Usuario] = Depends(get_optional_mayorista_user)
):
    """
    Obtiene detalle de un producto específico con precios mayoristas.
    """
    close_old_connections()
    try:
        from infrastructure.persistence.django.models import ProductoModel
        from uuid import UUID
        
        try:
            uid = UUID(producto_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de producto inválido")
        
        try:
            p = ProductoModel.objects.select_related('categoria').get(id=uid)
        except ProductoModel.DoesNotExist:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        precio_retail = float(p.monto_precio_original or p.monto_precio or 0)
        
        # Calcular descuento dinámico
        factor_descuento = 0.85  # Default 15% off (factor 0.85)
        if mayorista and mayorista.descuento_mayorista > 0:
            factor_descuento = 1.0 - (float(mayorista.descuento_mayorista) / 100.0)
            
        precio_mayorista = float(p.monto_precio or 0) * factor_descuento
        
        # Parsear imágenes adicionales
        imagenes = []
        if p.imagen_principal:
            imagenes.append(p.imagen_principal)
        if p.imagenes and isinstance(p.imagenes, list):
            imagenes.extend([img for img in p.imagenes if img and img != p.imagen_principal])
        
        return ProductoDetalleB2B(
            id=str(p.id),
            nombre=p.nombre,
            descripcion=p.descripcion,
            categoria={
                'id': str(p.categoria.id) if p.categoria else None,
                'nombre': p.categoria.nombre if p.categoria else None,
                'slug': p.categoria.slug if p.categoria else None
            } if p.categoria else None,
            categoria_nombre=p.categoria.nombre if p.categoria else None,
            codigo=p.codigo,
            sku=p.codigo,
            imagen_principal=p.imagen_principal,
            imagenes=imagenes,
            precio=precio_retail,
            precio_mayorista=precio_mayorista,
            monto_precio=precio_mayorista,
            precio_original=precio_retail,
            stock=p.stock_actual - p.stock_reservado,
            stock_actual=p.stock_actual,
            cantidad_minima=10 if p.metodo == 'bundle' else 1,
            metodo=p.metodo,
            color=p.color,
            largo=p.largo,
            tipo=p.tipo,
            origen=p.origen,
            calidad=p.calidad,
            activo=p.activo
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al obtener producto B2B: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cargar producto: {str(e)}")


@router.get("/mayoristas", response_model=List[MayoristaResponse])
async def listar_mayoristas(admin = Depends(get_current_admin_user)):
    """
    Lista todas las solicitudes de mayoristas (usuarios tipo MAYORISTA).
    Solo accesible por administradores.
    """
    try:
        # Obtener todos los usuarios de tipo MAYORISTA
        mayoristas = await sync_to_async(list)(
            Usuario.objects.filter(tipo='MAYORISTA').order_by('-fecha_creacion')
        )
        
        result = []
        for m in mayoristas:
            result.append(MayoristaResponse(
                id=m.id,
                email=m.email,
                nombre=m.nombre,
                apellido=m.apellido,
                telefono=m.telefono,
                tipo_documento=m.tipo_documento,
                numero_documento=m.numero_documento,
                nombre_empresa=m.nombre_empresa,
                nit_empresa=m.nit_empresa,
                cedula_frente=m.cedula_frente.url if m.cedula_frente else None,
                cedula_dorso=m.cedula_dorso.url if m.cedula_dorso else None,
                estado_mayorista=m.estado_mayorista,
                notas_revision=m.notas_revision,
                fecha_revision=m.fecha_revision,
                date_joined=m.fecha_creacion,
                descuento_mayorista=float(m.descuento_mayorista) if m.descuento_mayorista else 0
            ))
        
        return result
    except Exception as e:
        print(f"❌ Error al listar mayoristas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mayoristas/{mayorista_id}/aprobar")
async def aprobar_mayorista(
    mayorista_id: UUID,
    admin = Depends(get_current_admin_user)
):
    """
    Aprueba una solicitud de mayorista.
    """
    from django.utils import timezone
    from infrastructure.notifications.email_service import send_b2b_status_notification
    from infrastructure.notifications.inapp_notifications import create_b2b_notification
    
    try:
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        # Actualizar campos directamente (admin es dict, no Usuario)
        def do_approve():
            mayorista.estado_mayorista = 'APROBADO'
            mayorista.is_active = True
            mayorista.fecha_revision = timezone.now()
            mayorista.notas_revision = f"Aprobado por {admin.get('user_id', 'admin')}"
            mayorista.save()
        
        await sync_to_async(do_approve)()
        
        # Enviar notificación por correo
        send_b2b_status_notification(
            email=mayorista.email,
            nombre=mayorista.nombre,
            estado="APROBADO"
        )

        try:
            create_b2b_notification(
                email=mayorista.email,
                tipo='account_status',
                titulo='Cuenta aprobada',
                mensaje='Tu cuenta mayorista fue aprobada y ya esta activa.',
                data={'estado': 'APROBADO'},
            )
        except Exception as e:
            print(f"❌ Error creando notificacion de aprobacion: {e}")
        
        return {"message": f"Mayorista {mayorista.nombre} aprobado correctamente"}
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Mayorista no encontrado")
    except Exception as e:
        print(f"❌ Error al aprobar mayorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mayoristas/{mayorista_id}/rechazar")
async def rechazar_mayorista(
    mayorista_id: UUID,
    request: RejectRequest,
    admin = Depends(get_current_admin_user)
):
    """
    Rechaza una solicitud de mayorista con un motivo opcional.
    """
    from django.utils import timezone
    from infrastructure.notifications.email_service import send_b2b_status_notification
    from infrastructure.notifications.inapp_notifications import create_b2b_notification
    
    try:
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        def do_reject():
            mayorista.estado_mayorista = 'RECHAZADO'
            mayorista.fecha_revision = timezone.now()
            mayorista.notas_revision = request.notas or "Sin motivo especificado"
            mayorista.is_active = False
            mayorista.save()
        
        await sync_to_async(do_reject)()
        
        # Enviar notificación por correo
        send_b2b_status_notification(
            email=mayorista.email,
            nombre=mayorista.nombre,
            estado="RECHAZADO",
            notas=request.notas
        )

        try:
            create_b2b_notification(
                email=mayorista.email,
                tipo='account_status',
                titulo='Cuenta rechazada',
                mensaje='Tu solicitud de cuenta mayorista fue rechazada.',
                data={'estado': 'RECHAZADO', 'motivo': request.notas or ''},
            )
        except Exception as e:
            print(f"❌ Error creando notificacion de rechazo: {e}")
        
        return {"message": f"Mayorista {mayorista.nombre} rechazado"}
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Mayorista no encontrado")
    except Exception as e:
        print(f"❌ Error al rechazar mayorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mayoristas/{mayorista_id}/suspender")
async def suspender_mayorista(
    mayorista_id: UUID,
    admin = Depends(get_current_admin_user)
):
    """
    Suspende una cuenta de mayorista activa.
    """
    from django.utils import timezone
    from infrastructure.notifications.email_service import send_b2b_status_notification
    from infrastructure.notifications.inapp_notifications import create_b2b_notification
    
    try:
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        def do_suspend():
            mayorista.estado_mayorista = 'SUSPENDIDO'
            mayorista.fecha_revision = timezone.now()
            mayorista.notas_revision = f"Suspendido por {admin.get('user_id', 'admin')}"
            mayorista.save()
        
        await sync_to_async(do_suspend)()
        
        # Enviar notificación por correo
        send_b2b_status_notification(
            email=mayorista.email,
            nombre=mayorista.nombre,
            estado="SUSPENDIDO",
            notas=f"Suspendido por admin: {admin.get('user_id', 'admin')}"
        )

        try:
            create_b2b_notification(
                email=mayorista.email,
                tipo='account_status',
                titulo='Cuenta suspendida',
                mensaje='Tu cuenta mayorista fue suspendida temporalmente.',
                data={'estado': 'SUSPENDIDO'},
            )
        except Exception as e:
            print(f"❌ Error creando notificacion de suspension: {e}")
        
        return {"message": f"Mayorista {mayorista.nombre} suspendido"}
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Mayorista no encontrado")
    except Exception as e:
        print(f"❌ Error al suspender mayorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/mayoristas/{mayorista_id}/descuento")
async def actualizar_descuento(
    mayorista_id: UUID,
    request: DescuentoRequest,
    admin = Depends(get_current_admin_user)
):
    """
    Actualiza el porcentaje de descuento de un mayorista.
    """
    try:
        if request.descuento < 0 or request.descuento > 100:
            raise HTTPException(status_code=400, detail="El descuento debe estar entre 0 y 100")
        
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        def do_update():
            mayorista.descuento_mayorista = request.descuento
            mayorista.save()
        
        await sync_to_async(do_update)()
        
        return {"message": f"Descuento actualizado a {request.descuento}%"}
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Mayorista no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al actualizar descuento: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mayoristas/{mayorista_id}/cambiar-password")
async def cambiar_password_mayorista(
    mayorista_id: UUID,
    request: CambiarPasswordRequest,
    admin = Depends(get_current_admin_user)
):
    """
    Cambia la contraseña de un mayorista (solo admin).
    """
    try:
        if len(request.new_password) < 8:
            raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")

        from infrastructure.notifications.inapp_notifications import create_b2b_notification
        
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        def do_change():
            mayorista.set_password(request.new_password)
            mayorista.save()
        
        await sync_to_async(do_change)()

        try:
            create_b2b_notification(
                email=mayorista.email,
                tipo='password_changed',
                titulo='Contrasena actualizada',
                mensaje='Tu contrasena fue actualizada por el administrador.',
                data={},
            )
        except Exception as e:
            print(f"❌ Error creando notificacion de contrasena: {e}")
        
        print(f"🔑 Admin cambió contraseña del mayorista: {mayorista.email}")
        return {"message": f"Contraseña actualizada para {mayorista.email}"}
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Mayorista no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al cambiar contraseña: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mayoristas/{mayorista_id}")
async def obtener_mayorista(
    mayorista_id: UUID,
    admin = Depends(get_current_admin_user)
):
    """
    Obtiene los detalles de un mayorista específico.
    """
    try:
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        return MayoristaResponse(
            id=mayorista.id,
            email=mayorista.email,
            nombre=mayorista.nombre,
            apellido=mayorista.apellido,
            telefono=mayorista.telefono,
            tipo_documento=mayorista.tipo_documento,
            numero_documento=mayorista.numero_documento,
            nombre_empresa=mayorista.nombre_empresa,
            nit_empresa=mayorista.nit_empresa,
            cedula_frente=mayorista.cedula_frente.url if mayorista.cedula_frente else None,
            cedula_dorso=mayorista.cedula_dorso.url if mayorista.cedula_dorso else None,
            estado_mayorista=mayorista.estado_mayorista,
            notas_revision=mayorista.notas_revision,
            fecha_revision=mayorista.fecha_revision,
            date_joined=mayorista.fecha_creacion,
            descuento_mayorista=float(mayorista.descuento_mayorista) if mayorista.descuento_mayorista else 0
        )
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Mayorista no encontrado")
    except Exception as e:
        print(f"❌ Error al obtener mayorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# ENDPOINT PÚBLICO: Verificar si email ya existe (para validación en paso 1)
# =========================================================================

class VerificarEmailRequest(BaseModel):
    email: str


@router.post("/mayoristas/verificar-email")
async def verificar_email(request: VerificarEmailRequest):
    """
    Verifica si un email ya está registrado y retorna el estado.
    Este endpoint es PÚBLICO (no requiere autenticación).
    Se usa para validación en tiempo real en el formulario de registro.
    """
    try:
        user = await sync_to_async(
            Usuario.objects.filter(email=request.email).first
        )()
        
        if not user:
            return {"exists": False, "message": "Email disponible"}
        
        # Si existe, verificar tipo y estado
        if user.tipo == 'MAYORISTA':
            estado = user.estado_mayorista
            if estado == 'PENDIENTE':
                return {
                    "exists": True,
                    "status": "pending",
                    "title": "Solicitud en revisión",
                    "message": "Ya tienes una solicitud pendiente con este correo. Nuestro equipo está revisando tu información y te contactaremos pronto.",
                    "icon": "clock"
                }
            elif estado == 'EN_REVISION':
                return {
                    "exists": True,
                    "status": "reviewing",
                    "title": "Estamos revisando tu solicitud",
                    "message": "Tu solicitud está siendo evaluada por nuestro equipo. Te notificaremos por correo electrónico cuando tengamos una respuesta.",
                    "icon": "search"
                }
            elif estado == 'APROBADO':
                return {
                    "exists": True,
                    "status": "approved",
                    "title": "¡Ya tienes cuenta!",
                    "message": "Tu cuenta mayorista ya está activa. Inicia sesión para acceder al portal.",
                    "icon": "check",
                    "action": "login"
                }
            elif estado == 'RECHAZADO':
                return {
                    "exists": True,
                    "status": "rejected",
                    "title": "Solicitud rechazada",
                    "message": "Tu solicitud anterior fue rechazada. Si crees que es un error, contacta a nuestro equipo de soporte.",
                    "icon": "x",
                    "action": "support"
                }
            elif estado == 'SUSPENDIDO':
                return {
                    "exists": True,
                    "status": "suspended",
                    "title": "Cuenta suspendida",
                    "message": "Tu cuenta ha sido suspendida temporalmente. Contacta a soporte para más información.",
                    "icon": "pause",
                    "action": "support"
                }
        
        # Usuario existe pero no es mayorista (es cliente B2C)
        return {
            "exists": True,
            "status": "exists",
            "title": "Correo ya registrado",
            "message": "Este correo ya está registrado como cliente. Si deseas una cuenta mayorista, contacta a soporte.",
            "icon": "user"
        }
        
    except Exception as e:
        print(f"❌ Error al verificar email: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# ENDPOINT PÚBLICO: Registro de Mayorista (sin autenticación)
# =========================================================================

from fastapi import Form, UploadFile, File
from django.core.files.base import ContentFile
import os


@router.post("/mayoristas/registro", status_code=201)
async def registrar_mayorista(
    email: str = Form(...),
    password: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: str = Form(...),
    tipo_documento: str = Form(...),
    numero_documento: str = Form(...),
    nombre_empresa: str = Form(...),
    nit_empresa: str = Form(""),
    cedula_frente: UploadFile = File(None),
    cedula_dorso: UploadFile = File(None),
):
    """
    Registra una nueva solicitud de cuenta mayorista.
    Este endpoint es PÚBLICO (no requiere autenticación).
    Acepta archivos de imagen para la cédula.
    """
    from django.db import IntegrityError
    from django.db.models import Q
    
    try:
        # Verificar si el email o número de documento ya existen
        existing_user = await sync_to_async(
            Usuario.objects.filter(
                Q(email=email) | Q(numero_documento=numero_documento)
            ).first
        )()
        
        if existing_user:
            if existing_user.email == email:
                # Verificar estado si es mayorista
                if existing_user.tipo == 'MAYORISTA':
                    estado = existing_user.estado_mayorista
                    if estado == 'PENDIENTE':
                        raise HTTPException(
                            status_code=400, 
                            detail="Ya existe una solicitud pendiente con este correo. Tu solicitud está en revisión."
                        )
                    elif estado == 'EN_REVISION':
                        raise HTTPException(
                            status_code=400, 
                            detail="Tu solicitud está siendo revisada. Te contactaremos pronto."
                        )
                    elif estado == 'RECHAZADO':
                        raise HTTPException(
                            status_code=400, 
                            detail="Tu solicitud fue rechazada. Contacta a soporte para más información."
                        )
                raise HTTPException(
                    status_code=400, 
                    detail="Ya existe una cuenta con este correo electrónico"
                )
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Ya existe una cuenta con este número de documento"
                )
        
        # Leer archivos si existen
        frente_content = None
        dorso_content = None
        frente_name = None
        dorso_name = None
        
        if cedula_frente and cedula_frente.filename:
            frente_content = await cedula_frente.read()
            frente_name = f"cedula_frente_{numero_documento}_{cedula_frente.filename}"
            
        if cedula_dorso and cedula_dorso.filename:
            dorso_content = await cedula_dorso.read()
            dorso_name = f"cedula_dorso_{numero_documento}_{cedula_dorso.filename}"
        
        # Crear el usuario mayorista
        def create_mayorista():
            user = Usuario(
                email=email,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                tipo='MAYORISTA',
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                nombre_empresa=nombre_empresa,
                nit_empresa=nit_empresa or "",
                estado_mayorista='PENDIENTE',
                is_active=True  # Activo pero pendiente de aprobación
            )
            user.set_password(password)
            
            # Guardar imágenes de cédula si existen
            if frente_content and frente_name:
                user.cedula_frente.save(frente_name, ContentFile(frente_content), save=False)
            if dorso_content and dorso_name:
                user.cedula_dorso.save(dorso_name, ContentFile(dorso_content), save=False)
            
            user.save()
            return user
        
        user = await sync_to_async(create_mayorista)()
        
        print(f"✅ Nuevo mayorista registrado: {user.email} - {user.nombre_empresa}")
        if frente_content:
            print(f"   📄 Cédula frente: {frente_name}")
        if dorso_content:
            print(f"   📄 Cédula dorso: {dorso_name}")
        
        return {
            "message": "Solicitud de cuenta mayorista registrada exitosamente",
            "id": str(user.id),
            "email": user.email,
            "estado": "PENDIENTE"
        }
        
    except HTTPException:
        raise
    except IntegrityError as e:
        print(f"❌ Error de integridad al registrar mayorista: {e}")
        raise HTTPException(
            status_code=400, 
            detail="Ya existe una cuenta con este correo o documento"
        )
    except Exception as e:
        print(f"❌ Error al registrar mayorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS B2B - Gestión de Dirección del Mayorista
# ═══════════════════════════════════════════════════════════════════════════

class DireccionMayorista(BaseModel):
    """Esquema para dirección de mayorista"""
    direccion: str = ""
    complemento: str = ""
    departamento: str = ""
    departamento_id: Optional[int] = None
    municipio: str = ""
    municipio_id: Optional[int] = None
    barrio: str = ""
    indicaciones_entrega: str = ""
    tipo_domicilio: str = "Residencial"
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    telefono: str = ""
    nombre_contacto: str = ""

    class Config:
        from_attributes = True


class DireccionUpdateRequest(BaseModel):
    """Request para actualizar dirección"""
    direccion: str
    complemento: Optional[str] = ""
    departamento: str
    departamento_id: Optional[int] = None
    municipio: str
    municipio_id: Optional[int] = None
    barrio: Optional[str] = ""
    indicaciones_entrega: Optional[str] = ""
    tipo_domicilio: Optional[str] = "Residencial"
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    telefono: Optional[str] = None
    nombre_contacto: Optional[str] = None


@router.get("/b2b/me/direccion", response_model=DireccionMayorista)
async def obtener_mi_direccion(request: Request):
    """
    Obtiene la dirección guardada del mayorista actual.
    El email del usuario viene en el header X-User-Email.
    """
    close_old_connections()
    
    # Obtener email del header
    email = request.headers.get('X-User-Email', '').strip()
    if not email:
        raise HTTPException(
            status_code=401,
            detail="No autenticado. Se requiere header X-User-Email"
        )
    
    try:
        # Buscar usuario mayorista
        def get_user():
            try:
                return Usuario.objects.get(email=email, tipo='MAYORISTA')
            except Usuario.DoesNotExist:
                return None
        
        user = await sync_to_async(get_user)()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return DireccionMayorista(
            direccion=user.direccion or "",
            complemento=user.complemento or "",
            departamento=user.departamento or "",
            departamento_id=user.departamento_id,
            municipio=user.municipio or "",
            municipio_id=user.municipio_id,
            barrio=user.barrio or "",
            indicaciones_entrega=user.indicaciones_entrega or "",
            tipo_domicilio=user.tipo_domicilio or "Residencial",
            latitud=float(user.latitud) if user.latitud else None,
            longitud=float(user.longitud) if user.longitud else None,
            telefono=user.telefono or "",
            nombre_contacto=f"{user.nombre} {user.apellido}".strip()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al obtener dirección: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/b2b/me/direccion", response_model=DireccionMayorista)
async def actualizar_mi_direccion(request: Request, data: DireccionUpdateRequest):
    """
    Actualiza la dirección del mayorista actual.
    El email del usuario viene en el header X-User-Email.
    """
    close_old_connections()
    
    # Obtener email del header
    email = request.headers.get('X-User-Email', '').strip()
    if not email:
        raise HTTPException(
            status_code=401,
            detail="No autenticado. Se requiere header X-User-Email"
        )
    
    try:
        def update_user():
            try:
                user = Usuario.objects.get(email=email, tipo='MAYORISTA')
                
                # Actualizar campos de dirección
                user.direccion = data.direccion
                user.complemento = data.complemento or ""
                user.departamento = data.departamento
                user.departamento_id = data.departamento_id
                user.municipio = data.municipio
                user.municipio_id = data.municipio_id
                user.barrio = data.barrio or ""
                user.indicaciones_entrega = data.indicaciones_entrega or ""
                user.tipo_domicilio = data.tipo_domicilio or "Residencial"
                
                # Actualizar coordenadas si se proporcionan
                if data.latitud is not None:
                    user.latitud = data.latitud
                if data.longitud is not None:
                    user.longitud = data.longitud
                
                # Actualizar teléfono si se proporciona
                if data.telefono:
                    user.telefono = data.telefono
                
                user.save()
                return user
                
            except Usuario.DoesNotExist:
                return None
        
        user = await sync_to_async(update_user)()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        print(f"✅ Dirección actualizada para mayorista: {email}")
        
        return DireccionMayorista(
            direccion=user.direccion or "",
            complemento=user.complemento or "",
            departamento=user.departamento or "",
            departamento_id=user.departamento_id,
            municipio=user.municipio or "",
            municipio_id=user.municipio_id,
            barrio=user.barrio or "",
            indicaciones_entrega=user.indicaciones_entrega or "",
            tipo_domicilio=user.tipo_domicilio or "Residencial",
            latitud=float(user.latitud) if user.latitud else None,
            longitud=float(user.longitud) if user.longitud else None,
            telefono=user.telefono or "",
            nombre_contacto=data.nombre_contacto or f"{user.nombre} {user.apellido}".strip()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al actualizar dirección: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS CRUD - DIRECCIONES MÚLTIPLES
# ═══════════════════════════════════════════════════════════════════════════

class DireccionResponse(BaseModel):
    """Respuesta de dirección individual"""
    id: int
    etiqueta: str
    direccion: str
    complemento: Optional[str] = ""
    departamento: str
    departamento_id: Optional[int] = None
    municipio: str
    municipio_id: Optional[int] = None
    barrio: Optional[str] = ""
    indicaciones: Optional[str] = ""
    tipo_domicilio: str = "Residencial"
    nombre_contacto: Optional[str] = ""
    telefono: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    is_default: bool = False
    
    class Config:
        from_attributes = True


class DireccionCreateRequest(BaseModel):
    """Request para crear dirección"""
    etiqueta: str = "Mi dirección"
    direccion: str
    complemento: Optional[str] = ""
    departamento: str
    departamento_id: Optional[int] = None
    municipio: str
    municipio_id: Optional[int] = None
    barrio: Optional[str] = ""
    indicaciones: Optional[str] = ""
    tipo_domicilio: str = "Residencial"
    nombre_contacto: Optional[str] = ""
    telefono: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    is_default: bool = False


@router.get("/b2b/me/direcciones", response_model=List[DireccionResponse])
async def listar_mis_direcciones(
    email: str = Depends(get_current_user_email)
):
    """
    Lista todas las direcciones del mayorista autenticado.
    Ordenadas por: principal primero, luego por fecha de creación.
    """
    from infrastructure.auth.models import DireccionMayorista as DireccionModel
    
    close_old_connections()
    
    try:
        def get_direcciones():
            try:
                user = Usuario.objects.get(email=email, tipo='MAYORISTA')
                return list(user.direcciones.filter(activa=True))
            except Usuario.DoesNotExist:
                return []
        
        direcciones = await sync_to_async(get_direcciones)()
        
        return [
            DireccionResponse(
                id=d.id,
                etiqueta=d.etiqueta,
                direccion=d.direccion,
                complemento=d.complemento or "",
                departamento=d.departamento,
                departamento_id=d.departamento_id,
                municipio=d.municipio,
                municipio_id=d.municipio_id,
                barrio=d.barrio or "",
                indicaciones=d.indicaciones or "",
                tipo_domicilio=d.tipo_domicilio or "Residencial",
                nombre_contacto=d.nombre_contacto or "",
                telefono=d.telefono or "",
                latitud=float(d.latitud) if d.latitud else None,
                longitud=float(d.longitud) if d.longitud else None,
                is_default=d.is_default
            )
            for d in direcciones
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al listar direcciones: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/b2b/me/direcciones", response_model=DireccionResponse)
async def crear_direccion(
    data: DireccionCreateRequest,
    email: str = Depends(get_current_user_email)
):
    """
    Crea una nueva dirección para el mayorista autenticado.
    Si is_default=True, se desmarca la anterior principal.
    """
    from infrastructure.auth.models import DireccionMayorista as DireccionModel
    
    close_old_connections()
    
    try:
        def create_direccion():
            try:
                user = Usuario.objects.get(email=email, tipo='MAYORISTA')
                
                # Si es la primera dirección o se marca como default
                count = user.direcciones.filter(activa=True).count()
                make_default = data.is_default or count == 0
                
                direccion = DireccionModel.objects.create(
                    usuario=user,
                    etiqueta=data.etiqueta,
                    direccion=data.direccion,
                    complemento=data.complemento or "",
                    departamento=data.departamento,
                    departamento_id=data.departamento_id,
                    municipio=data.municipio,
                    municipio_id=data.municipio_id,
                    barrio=data.barrio or "",
                    indicaciones=data.indicaciones or "",
                    tipo_domicilio=data.tipo_domicilio or "Residencial",
                    nombre_contacto=data.nombre_contacto or "",
                    telefono=data.telefono,
                    latitud=data.latitud,
                    longitud=data.longitud,
                    is_default=make_default
                )
                return direccion
                
            except Usuario.DoesNotExist:
                return None
        
        direccion = await sync_to_async(create_direccion)()
        
        if not direccion:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        print(f"✅ Dirección creada para {email}: {direccion.etiqueta}")
        
        return DireccionResponse(
            id=direccion.id,
            etiqueta=direccion.etiqueta,
            direccion=direccion.direccion,
            complemento=direccion.complemento or "",
            departamento=direccion.departamento,
            departamento_id=direccion.departamento_id,
            municipio=direccion.municipio,
            municipio_id=direccion.municipio_id,
            barrio=direccion.barrio or "",
            indicaciones=direccion.indicaciones or "",
            tipo_domicilio=direccion.tipo_domicilio,
            nombre_contacto=direccion.nombre_contacto or "",
            telefono=direccion.telefono,
            latitud=float(direccion.latitud) if direccion.latitud else None,
            longitud=float(direccion.longitud) if direccion.longitud else None,
            is_default=direccion.is_default
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al crear dirección: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/b2b/me/direcciones/{direccion_id}", response_model=DireccionResponse)
async def actualizar_direccion(
    direccion_id: int,
    data: DireccionCreateRequest,
    email: str = Depends(get_current_user_email)
):
    """
    Actualiza una dirección existente del mayorista.
    """
    from infrastructure.auth.models import DireccionMayorista as DireccionModel
    
    close_old_connections()
    
    try:
        def update_direccion():
            try:
                user = Usuario.objects.get(email=email, tipo='MAYORISTA')
                direccion = DireccionModel.objects.get(id=direccion_id, usuario=user, activa=True)
                
                direccion.etiqueta = data.etiqueta
                direccion.direccion = data.direccion
                direccion.complemento = data.complemento or ""
                direccion.departamento = data.departamento
                direccion.departamento_id = data.departamento_id
                direccion.municipio = data.municipio
                direccion.municipio_id = data.municipio_id
                direccion.barrio = data.barrio or ""
                direccion.indicaciones = data.indicaciones or ""
                direccion.tipo_domicilio = data.tipo_domicilio or "Residencial"
                direccion.nombre_contacto = data.nombre_contacto or ""
                direccion.telefono = data.telefono
                direccion.latitud = data.latitud
                direccion.longitud = data.longitud
                direccion.is_default = data.is_default
                direccion.save()
                
                return direccion
                
            except (Usuario.DoesNotExist, DireccionModel.DoesNotExist):
                return None
        
        direccion = await sync_to_async(update_direccion)()
        
        if not direccion:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        
        print(f"✅ Dirección actualizada: {direccion.etiqueta}")
        
        return DireccionResponse(
            id=direccion.id,
            etiqueta=direccion.etiqueta,
            direccion=direccion.direccion,
            complemento=direccion.complemento or "",
            departamento=direccion.departamento,
            departamento_id=direccion.departamento_id,
            municipio=direccion.municipio,
            municipio_id=direccion.municipio_id,
            barrio=direccion.barrio or "",
            indicaciones=direccion.indicaciones or "",
            tipo_domicilio=direccion.tipo_domicilio,
            nombre_contacto=direccion.nombre_contacto or "",
            telefono=direccion.telefono,
            latitud=float(direccion.latitud) if direccion.latitud else None,
            longitud=float(direccion.longitud) if direccion.longitud else None,
            is_default=direccion.is_default
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al actualizar dirección: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/b2b/me/direcciones/{direccion_id}")
async def eliminar_direccion(
    direccion_id: int,
    email: str = Depends(get_current_user_email)
):
    """
    Elimina (soft delete) una dirección del mayorista.
    Si era la principal, la siguiente más reciente se vuelve principal.
    """
    from infrastructure.auth.models import DireccionMayorista as DireccionModel
    
    close_old_connections()
    
    try:
        def delete_direccion():
            try:
                user = Usuario.objects.get(email=email, tipo='MAYORISTA')
                direccion = DireccionModel.objects.get(id=direccion_id, usuario=user, activa=True)
                
                was_default = direccion.is_default
                direccion.activa = False
                direccion.is_default = False
                direccion.save()
                
                # Si era la principal, marcar la siguiente como principal
                if was_default:
                    next_default = DireccionModel.objects.filter(
                        usuario=user, activa=True
                    ).order_by('-fecha_creacion').first()
                    if next_default:
                        next_default.is_default = True
                        next_default.save()
                
                return True
                
            except (Usuario.DoesNotExist, DireccionModel.DoesNotExist):
                return False
        
        deleted = await sync_to_async(delete_direccion)()
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        
        print(f"✅ Dirección eliminada: {direccion_id}")
        
        return {"message": "Dirección eliminada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al eliminar dirección: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/b2b/me/direcciones/{direccion_id}/default")
async def marcar_direccion_principal(
    direccion_id: int,
    email: str = Depends(get_current_user_email)
):
    """
    Marca una dirección como la principal del usuario.
    Desmarca la anterior principal automáticamente.
    """
    from infrastructure.auth.models import DireccionMayorista as DireccionModel
    
    close_old_connections()
    
    try:
        def set_default():
            try:
                user = Usuario.objects.get(email=email, tipo='MAYORISTA')
                direccion = DireccionModel.objects.get(id=direccion_id, usuario=user, activa=True)
                
                # El modelo ya maneja desmarcar las anteriores en save()
                direccion.is_default = True
                direccion.save()
                
                return direccion
                
            except (Usuario.DoesNotExist, DireccionModel.DoesNotExist):
                return None
        
        direccion = await sync_to_async(set_default)()
        
        if not direccion:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        
        print(f"✅ Dirección marcada como principal: {direccion.etiqueta}")
        
        return {"message": "Dirección marcada como principal", "id": direccion_id}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al marcar dirección como principal: {e}")
        raise HTTPException(status_code=500, detail=str(e))
