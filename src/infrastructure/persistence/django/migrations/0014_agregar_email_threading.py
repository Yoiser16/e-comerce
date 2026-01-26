# Generated migration for email threading
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_persistence', '0013_agregar_reserva_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenmodel',
            name='email_thread_id',
            field=models.CharField(blank=True, default='', help_text='Message-ID del primer email enviado', max_length=255),
        ),
    ]
