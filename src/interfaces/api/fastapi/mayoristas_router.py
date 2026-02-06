"""
Router para administrar solicitudes de mayoristas (B2B)
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from asgiref.sync import sync_to_async
from django.db import close_old_connections

from infrastructure.auth.models import Usuario
from .dependencies import get_current_admin_user

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
def obtener_productos_b2b(limit: int = 20, offset: int = 0):
    """
    Obtiene productos reales de la base de datos para mayoristas.
    Endpoint público para B2B.
    """
    # Cerrar conexiones viejas para evitar 'connection is closed'
    close_old_connections()
    try:
        from infrastructure.persistence.django.models import ProductoModel
        
        # Consultar productos activos de la BD
        productos = ProductoModel.objects.filter(
            activo=True,
            stock_actual__gt=0
        ).order_by('-total_vendidos', '-fecha_creacion')[offset:offset+limit]
        
        result = []
        for p in productos:
            result.append(ProductoB2B(
                id=str(p.id),
                nombre=p.nombre,
                categoria=p.categoria.nombre if p.categoria else None,
                codigo=p.codigo,
                imagen=p.imagen_principal,
                precio_retail=float(p.monto_precio_original or p.monto_precio),
                precio_mayorista=float(p.monto_precio) * 0.85,  # 15% descuento mayorista
                stock=p.stock_actual - p.stock_reservado,
                cantidad_minima=5 if p.metodo == 'bundle' else 1
            ))
        
        return result
    except Exception as e:
        print(f"❌ Error al obtener productos B2B: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cargar productos: {str(e)}")


@router.get("/b2b/productos/destacados", response_model=List[ProductoB2B])
def obtener_productos_destacados_b2b(limit: int = 10):
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
                precio_mayorista=float(p.monto_precio) * 0.85,  # 15% descuento mayorista
                stock=p.stock_actual - p.stock_reservado,
                cantidad_minima=5 if p.metodo == 'bundle' else 1
            ))
        
        return result
    except Exception as e:
        print(f"❌ Error al obtener productos destacados B2B: {e}")
        raise HTTPException(status_code=500, detail=f"Error al cargar productos: {str(e)}")


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
    
    try:
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        # Actualizar campos directamente (admin es dict, no Usuario)
        def do_approve():
            mayorista.estado_mayorista = 'APROBADO'
            mayorista.fecha_revision = timezone.now()
            mayorista.notas_revision = f"Aprobado por {admin.get('user_id', 'admin')}"
            mayorista.save()
        
        await sync_to_async(do_approve)()
        
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
    
    try:
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        def do_reject():
            mayorista.estado_mayorista = 'RECHAZADO'
            mayorista.fecha_revision = timezone.now()
            mayorista.notas_revision = request.notas or "Sin motivo especificado"
            mayorista.is_active = False
            mayorista.save()
        
        await sync_to_async(do_reject)()
        
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
    
    try:
        mayorista = await sync_to_async(Usuario.objects.get)(id=mayorista_id, tipo='MAYORISTA')
        
        def do_suspend():
            mayorista.estado_mayorista = 'SUSPENDIDO'
            mayorista.fecha_revision = timezone.now()
            mayorista.notas_revision = f"Suspendido por {admin.get('user_id', 'admin')}"
            mayorista.save()
        
        await sync_to_async(do_suspend)()
        
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


@router.post("/verificar-email")
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


@router.post("/registro", status_code=201)
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
