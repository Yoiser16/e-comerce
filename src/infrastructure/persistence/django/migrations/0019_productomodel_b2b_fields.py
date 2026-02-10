from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_persistence', '0018_notificaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='productomodel',
            name='disponible_b2b',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddField(
            model_name='productomodel',
            name='porcentaje_descuento_b2b',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Porcentaje de descuento B2B', null=True),
        ),
    ]
