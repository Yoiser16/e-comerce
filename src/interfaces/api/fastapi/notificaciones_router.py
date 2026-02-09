"""
Router de notificaciones in-app (B2B).
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from asgiref.sync import sync_to_async
from django.utils import timezone

from interfaces.api.fastapi.dependencies import get_current_user_email
from infrastructure.persistence.django.models import NotificacionModel


router = APIRouter(prefix="/api/v1/notificaciones", tags=["notificaciones"])


class NotificacionDTO(BaseModel):
    id: str
    tipo: str
    titulo: str
    mensaje: str
    data: dict
    leida: bool
    fecha_creacion: str
    fecha_leida: Optional[str] = None


class NotificacionesResponse(BaseModel):
    items: List[NotificacionDTO]
    unread_count: int


def _listar_notificaciones_sync(email: str, limit: int, offset: int, solo_no_leidas: bool) -> NotificacionesResponse:
    base_qs = NotificacionModel.objects.filter(email=email).order_by('-fecha_creacion')
    if solo_no_leidas:
        base_qs = base_qs.filter(leida=False)

    unread_count = NotificacionModel.objects.filter(email=email, leida=False).count()
    notificaciones = list(base_qs[offset:offset + limit])

    items = []
    for n in notificaciones:
        items.append(NotificacionDTO(
            id=str(n.id),
            tipo=n.tipo,
            titulo=n.titulo,
            mensaje=n.mensaje,
            data=n.data or {},
            leida=n.leida,
            fecha_creacion=n.fecha_creacion.isoformat(),
            fecha_leida=n.fecha_leida.isoformat() if n.fecha_leida else None,
        ))

    return NotificacionesResponse(items=items, unread_count=unread_count)


@router.get("", response_model=NotificacionesResponse)
async def listar_notificaciones(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    solo_no_leidas: bool = Query(False),
    email: str = Depends(get_current_user_email),
):
    return await sync_to_async(_listar_notificaciones_sync)(email, limit, offset, solo_no_leidas)


@router.post("/{notificacion_id}/leer")
async def marcar_leida(notificacion_id: str, email: str = Depends(get_current_user_email)):
    updated = await sync_to_async(
        lambda: NotificacionModel.objects.filter(id=notificacion_id, email=email, leida=False)
        .update(leida=True, fecha_leida=timezone.now())
    )()

    if updated == 0:
        raise HTTPException(status_code=404, detail="Notificacion no encontrada")

    return {"ok": True}


@router.post("/leer-todas")
async def marcar_todas_leidas(email: str = Depends(get_current_user_email)):
    await sync_to_async(
        lambda: NotificacionModel.objects.filter(email=email, leida=False)
        .update(leida=True, fecha_leida=timezone.now())
    )()

    return {"ok": True}
