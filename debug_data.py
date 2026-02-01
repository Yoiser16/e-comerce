
import os
import sys
import django
from django.db.models import Count, Max, Min
from datetime import datetime

# Setup Django
sys.path.append(os.path.join(os.getcwd(), 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infrastructure.config.django_settings")
django.setup()

try:
    # Importar modelos (ajustar path según estructura)
    from infrastructure.persistence.django.models import OrdenModel, ProductoModel, ClienteModel
    
    print("=== DIAGNÓSTICO DE DATOS ===")
    
    # 1. Conteo Total
    total_ordenes = OrdenModel.objects.count()
    print(f"Total Órdenes en DB: {total_ordenes}")
    
    if total_ordenes == 0:
        print("!! LA BASE DE DATOS DE ÓRDENES ESTÁ VACÍA !!")
    else:
        # 2. Rango de Fechas
        fechas = OrdenModel.objects.aggregate(
            primera=Min('fecha_creacion'),
            ultima=Max('fecha_creacion')
        )
        print(f"Rango de Fechas: {fechas['primera']} - {fechas['ultima']}")
        
        # 3. Distribución de Estados
        print("\nDistribución de Estados:")
        estados = OrdenModel.objects.values('estado').annotate(count=Count('id'))
        for e in estados:
            print(f" - {e['estado']}: {e['count']}")
            
        # 4. Chequeo de Estados Pagados (Dashboard Logic)
        estados_pagados = ['CONFIRMADA', 'PAGADA', 'PAGADO', 'ENVIADA', 'ENTREGADA', 'COMPLETADA']
        pagadas = OrdenModel.objects.filter(estado__in=estados_pagados).count()
        print(f"\nÓrdenes consideradas 'Ventas' (Pagadas/Confirmadas): {pagadas}")

    print("\n=== PRODUCTOS ===")
    print(f"Total Productos: {ProductoModel.objects.count()}")
    
    print("\n=== CLIENTES ===")
    print(f"Total Clientes: {ClienteModel.objects.count()}")

except Exception as e:
    print(f"Error ejecutando diagnóstico: {e}")
    # Listar tablas para debug
    from django.apps import apps
    print("\nModelos disponibles:")
    for model in apps.get_models():
        print(model._meta.label)
