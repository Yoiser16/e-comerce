from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_persistence', '0021_merge_20260213_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoDescuentoVolumenModel',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('cantidad_minima', models.IntegerField(default=1)),
                ('descuento_porcentaje', models.PositiveSmallIntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
                ('orden', models.IntegerField(default=0)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descuentos_volumen', to='ecommerce_persistence.productomodel')),
            ],
            options={
                'db_table': 'productos_descuentos_volumen',
                'verbose_name': 'Descuento por Volumen',
                'verbose_name_plural': 'Descuentos por Volumen',
                'ordering': ['cantidad_minima', 'orden'],
            },
        ),
        migrations.AddIndex(
            model_name='productodescuentovolumenmodel',
            index=models.Index(fields=['producto', 'activo'], name='productos_d_producto_3e0aa0_idx'),
        ),
        migrations.AddIndex(
            model_name='productodescuentovolumenmodel',
            index=models.Index(fields=['producto', 'cantidad_minima'], name='productos_d_producto_6b6c5f_idx'),
        ),
        migrations.AddConstraint(
            model_name='productodescuentovolumenmodel',
            constraint=models.UniqueConstraint(fields=('producto', 'cantidad_minima'), name='unique_descuento_por_cantidad'),
        ),
    ]
