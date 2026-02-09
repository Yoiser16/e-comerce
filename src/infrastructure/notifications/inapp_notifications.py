"""
Servicio para notificaciones in-app B2B.
"""
from uuid import uuid4

from infrastructure.auth.models import Usuario
from infrastructure.persistence.django.models import NotificacionModel


def create_b2b_notification(email: str, tipo: str, titulo: str, mensaje: str, data: dict | None = None):
    if not email:
        return None

    usuario = Usuario.objects.filter(email=email, tipo='MAYORISTA').first()
    if not usuario:
        return None

    return NotificacionModel.objects.create(
        id=uuid4(),
        usuario_id=usuario.id,
        email=email,
        tipo=tipo,
        titulo=titulo,
        mensaje=mensaje,
        data=data or {},
        leida=False,
    )
