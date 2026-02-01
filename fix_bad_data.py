
import os
import sys
import django

# Setup Django
sys.path.append(os.path.join(os.getcwd(), 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infrastructure.config.django_settings")
try:
    django.setup()
    from infrastructure.persistence.django.models import ClienteModel

    print("=== LIMPIEZA DE DATOS ===")
    bad_clients = ClienteModel.objects.filter(tipo_documento='')
    count = bad_clients.count()
    
    if count > 0:
        print(f"Encontrados {count} clientes con tipo_documento inválido.")
        bad_clients.delete()
        print("✅ Clientes inválidos eliminados.")
    else:
        print("No se encontraron clientes inválidos.")

except Exception as e:
    print(f"Error: {e}")
