"""
Signals para notificaciones in-app.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from infrastructure.persistence.django.models import OrdenModel
from infrastructure.notifications.inapp_notifications import create_b2b_notification


@receiver(pre_save, sender=OrdenModel)
def orden_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = OrdenModel.objects.get(pk=instance.pk)
            instance._previous_estado = previous.estado
        except OrdenModel.DoesNotExist:
            instance._previous_estado = None
    else:
        instance._previous_estado = None


@receiver(post_save, sender=OrdenModel)
def orden_post_save(sender, instance, created, **kwargs):
    email = instance.cliente.email if instance.cliente else ''
    if not email:
        return

    if created:
        try:
            create_b2b_notification(
                email=email,
                tipo='orden_estado',
                titulo='Pedido creado',
                mensaje=f"Tu pedido {instance.codigo} fue creado.",
                data={
                    'orden_id': str(instance.id),
                    'codigo': instance.codigo,
                    'estado': instance.estado,
                },
            )
        except Exception as e:
            print(f"❌ Error creando notificacion de orden: {e}")
        return

    previous_estado = getattr(instance, '_previous_estado', None)
    if previous_estado and previous_estado != instance.estado:
        try:
            create_b2b_notification(
                email=email,
                tipo='orden_estado',
                titulo='Actualizacion de estado',
                mensaje=f"Tu pedido {instance.codigo} ahora esta {instance.estado}.",
                data={
                    'orden_id': str(instance.id),
                    'codigo': instance.codigo,
                    'estado': instance.estado,
                },
            )
        except Exception as e:
            print(f"❌ Error creando notificacion de estado: {e}")
