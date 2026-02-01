
import os
import sys
import django
from django.db.models import Count

# Setup Django
sys.path.append(os.path.join(os.getcwd(), 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infrastructure.config.django_settings")
try:
    django.setup()
    from infrastructure.persistence.django.models import ClienteModel

    print("=== TIPOS DE DOCUMENTO EN DB ===")
    tipos = ClienteModel.objects.values('tipo_documento').annotate(count=Count('id'))
    for t in tipos:
        print(f"'{t['tipo_documento']}': {t['count']}")

except Exception as e:
    print(f"Error: {e}")
