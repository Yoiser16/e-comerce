# Generated migration to increase attribute field lengths

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_persistence', '0010_agregar_categoria_a_productos'),
    ]

    operations = [
        # Aumentar longitud de campos de atributos
        migrations.AlterField(
            model_name='productomodel',
            name='largo',
            field=models.CharField(blank=True, choices=[('12 Pulgadas', '12 Pulgadas'), ('14 Pulgadas', '14 Pulgadas'), ('16 Pulgadas', '16 Pulgadas'), ('18 Pulgadas', '18 Pulgadas'), ('20 Pulgadas', '20 Pulgadas'), ('22 Pulgadas', '22 Pulgadas'), ('24 Pulgadas', '24 Pulgadas'), ('26 Pulgadas', '26 Pulgadas'), ('28 Pulgadas', '28 Pulgadas'), ('30 Pulgadas', '30 Pulgadas')], db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='productomodel',
            name='color',
            field=models.CharField(blank=True, choices=[('Negro', 'Negro'), ('Castaño Oscuro', 'Castaño Oscuro'), ('Castaño Medio', 'Castaño Medio'), ('Castaño Claro', 'Castaño Claro'), ('Rubio Oscuro', 'Rubio Oscuro'), ('Rubio Medio', 'Rubio Medio'), ('Rubio Claro', 'Rubio Claro'), ('Rojo', 'Rojo'), ('Borgogña', 'Borgogña'), ('Caoba', 'Caoba')], db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='productomodel',
            name='tipo',
            field=models.CharField(blank=True, choices=[('Liso', 'Liso'), ('Ondulado', 'Ondulado'), ('Rizado', 'Rizado'), ('Afro', 'Afro'), ('Kinky', 'Kinky'), ('Body Wave', 'Body Wave'), ('Deep Wave', 'Deep Wave'), ('Water Wave', 'Water Wave'), ('Loose Wave', 'Loose Wave')], db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='productomodel',
            name='origen',
            field=models.CharField(blank=True, choices=[('Cabello Virgen Brasileño', 'Cabello Virgen Brasileño'), ('Cabello Virgen Peruano', 'Cabello Virgen Peruano'), ('Cabello Virgen Malasio', 'Cabello Virgen Malasio'), ('Cabello Virgen Indio', 'Cabello Virgen Indio'), ('Cabello Procesado', 'Cabello Procesado')], db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='productomodel',
            name='metodo',
            field=models.CharField(blank=True, choices=[('Tejido', 'Tejido'), ('Pegado', 'Pegado'), ('Clip-in', 'Clip-in'), ('Cosido', 'Cosido'), ('Fusión', 'Fusión')], db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='productomodel',
            name='calidad',
            field=models.CharField(blank=True, choices=[('Densidad 100%', 'Densidad 100%'), ('Densidad 150%', 'Densidad 150%'), ('Densidad 200%', 'Densidad 200%'), ('Densidad 250%', 'Densidad 250%'), ('Densidad 300%', 'Densidad 300%')], db_index=True, max_length=50, null=True),
        ),
    ]
