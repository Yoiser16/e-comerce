"""
Router de reseñas de productos (rating con moderación)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, conint
from typing import List, Optional
from uuid import UUID
from asgiref.sync import sync_to_async
from django.db import close_old_connections
from django.db.models import Avg

import django

django.setup()

from infrastructure.persistence.django.models import (
    ResenaProductoModel,
    ProductoModel,
    ClienteModel,
    OrdenModel
)
from interfaces.api.fastapi.dependencies import get_current_user_email, get_current_user_admin


router = APIRouter(prefix="/api/v1/resenas", tags=["resenas"])


class CrearResenaInput(BaseModel):
    producto_id: UUID
    rating: conint(ge=1, le=5)


class ResenaItem(BaseModel):
    id: str
    producto_id: str
    producto_nombre: str
    rating: int
    cliente: str
    fecha_creacion: str


class ResumenResenas(BaseModel):
    producto_id: str
    promedio: float
    total: int


class CambiarEstadoInput(BaseModel):
    estado: str


def _cliente_display(cliente: ClienteModel) -> str:
    if not cliente:
        return "Cliente"
    nombre = (cliente.nombre or "").strip()
    apellido = (cliente.apellido or "").strip()
    # Mostrar solo primer nombre + inicial del primer apellido para evitar exponer PII completa
    primer_nombre = nombre.split()[0] if nombre else "Cliente"
    inicial_apellido = apellido.split()[0][:1] if apellido else ""
    if inicial_apellido:
        return f"{primer_nombre} {inicial_apellido}."
    return primer_nombre


def _get_cliente_por_email(email: str) -> Optional[ClienteModel]:
    close_old_connections()
    return ClienteModel.objects.filter(email=email).first()


def _get_orden_compra(cliente: ClienteModel, producto: ProductoModel) -> Optional[OrdenModel]:
    close_old_connections()
    estados_validos = ['confirmada', 'en_proceso', 'enviada', 'completada']
    return (
        OrdenModel.objects
        .filter(cliente=cliente, estado__in=estados_validos, lineas__producto=producto)
        .order_by('-fecha_creacion')
        .distinct()
        .first()
    )


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_resena(
    datos: CrearResenaInput,
    email: str = Depends(get_current_user_email)
):
    """
    Crea o actualiza una reseña (rating) para un producto.
    Solo permite reseñas si el cliente compró el producto.
    """
    try:
        cliente = await sync_to_async(_get_cliente_por_email)(email)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        producto = await sync_to_async(ProductoModel.objects.filter(id=datos.producto_id).first)()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        orden = await sync_to_async(_get_orden_compra)(cliente, producto)
        if not orden:
            raise HTTPException(status_code=403, detail="Solo clientes con compra pueden calificar este producto")

        def _upsert():
            close_old_connections()
            resena, created = ResenaProductoModel.objects.get_or_create(
                producto=producto,
                cliente=cliente,
                defaults={
                    'rating': int(datos.rating),
                    'estado': 'pendiente',
                    'orden': orden
                }
            )
            if not created:
                resena.rating = int(datos.rating)
                resena.estado = 'pendiente'
                resena.orden = orden
                resena.save()
            return resena

        resena = await sync_to_async(_upsert)()

        return {
            "id": str(resena.id),
            "mensaje": "Tu calificación fue enviada y está pendiente de aprobación"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear reseña: {str(e)}")


@router.get("/producto/{producto_id}", response_model=List[ResenaItem])
async def listar_resenas_producto(
    producto_id: UUID,
    limit: int = 6,
    offset: int = 0
):
    """Lista reseñas aprobadas de un producto."""
    def _listar():
        close_old_connections()
        qs = (
            ResenaProductoModel.objects
            .select_related('cliente', 'producto')
            .filter(producto_id=producto_id, estado='aprobada')
            .order_by('-fecha_creacion')
        )
        items = list(qs[offset:offset + limit])
        return [
            {
                'id': str(r.id),
                'producto_id': str(r.producto_id),
                'producto_nombre': r.producto.nombre if r.producto else '',
                'rating': int(r.rating),
                'cliente': _cliente_display(r.cliente),
                'fecha_creacion': r.fecha_creacion.isoformat()
            }
            for r in items
        ]

    return await sync_to_async(_listar)()


@router.get("/producto/{producto_id}/resumen", response_model=ResumenResenas)
async def resumen_resenas_producto(producto_id: UUID):
    """Resumen de reseñas aprobadas (promedio y total)."""
    def _resumen():
        close_old_connections()
        qs = ResenaProductoModel.objects.filter(producto_id=producto_id, estado='aprobada')
        total = qs.count()
        promedio = qs.aggregate(avg=Avg('rating'))['avg'] or 0
        return {
            'producto_id': str(producto_id),
            'promedio': float(promedio),
            'total': int(total)
        }

    return await sync_to_async(_resumen)()


@router.get("/destacadas", response_model=List[ResenaItem])
async def listar_resenas_destacadas(limit: int = 6):
    """Lista reseñas aprobadas recientes para la home."""
    def _listar():
        close_old_connections()
        qs = (
            ResenaProductoModel.objects
            .select_related('cliente', 'producto')
            .filter(estado='aprobada')
            .order_by('-fecha_creacion')
        )
        items = list(qs[:limit])
        return [
            {
                'id': str(r.id),
                'producto_id': str(r.producto_id),
                'producto_nombre': r.producto.nombre if r.producto else '',
                'rating': int(r.rating),
                'cliente': _cliente_display(r.cliente),
                'fecha_creacion': r.fecha_creacion.isoformat()
            }
            for r in items
        ]

    return await sync_to_async(_listar)()


@router.get("/admin", response_model=List[ResenaItem])
async def listar_resenas_admin(
    estado: str = 'pendiente',
    _: dict = Depends(get_current_user_admin)
):
    """Lista reseñas para moderación (admin)."""
    def _listar():
        close_old_connections()
        qs = (
            ResenaProductoModel.objects
            .select_related('cliente', 'producto')
            .filter(estado=estado)
            .order_by('-fecha_creacion')
        )
        return [
            {
                'id': str(r.id),
                'producto_id': str(r.producto_id),
                'producto_nombre': r.producto.nombre if r.producto else '',
                'rating': int(r.rating),
                'cliente': _cliente_display(r.cliente),
                'fecha_creacion': r.fecha_creacion.isoformat()
            }
            for r in qs
        ]

    return await sync_to_async(_listar)()


@router.patch("/{resena_id}/estado")
async def cambiar_estado_resena(
    resena_id: UUID,
    datos: CambiarEstadoInput,
    _: dict = Depends(get_current_user_admin)
):
    """Aprueba o rechaza una reseña."""
    estados_validos = {'pendiente', 'aprobada', 'rechazada'}
    if datos.estado not in estados_validos:
        raise HTTPException(status_code=400, detail="Estado inválido")

    def _actualizar():
        close_old_connections()
        resena = ResenaProductoModel.objects.filter(id=resena_id).first()
        if not resena:
            return None
        resena.estado = datos.estado
        resena.save()
        return resena

    resena = await sync_to_async(_actualizar)()
    if not resena:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    return {"id": str(resena.id), "estado": resena.estado}
