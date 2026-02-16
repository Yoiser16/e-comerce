from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_persistence', '0023_variante_descuentos_volumen'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenmodel',
            name='estado_pago',
            field=models.CharField(
                choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado'), ('cancelado', 'Cancelado')],
                default='pendiente',
                max_length=20,
                db_index=True,
            ),
        ),
        migrations.AddField(
            model_name='ordenmodel',
            name='estado_envio',
            field=models.CharField(
                choices=[('no_enviado', 'No Enviado'), ('enviado', 'Enviado'), ('entregado', 'Entregado')],
                default='no_enviado',
                max_length=20,
                db_index=True,
            ),
        ),
    ]
