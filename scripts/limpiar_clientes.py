#!/usr/bin/env python3
"""
Script para limpiar clientes con datos inválidos
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.config.django_settings')

import django
django.setup()

from infrastructure.persistence.django.models import ClienteModel

def limpiar_clientes_invalidos():
    """Elimina clientes de prueba con emails inválidos"""
    
    print("🧹 Limpiando clientes con datos inválidos...")
    
    # Buscar clientes de prueba (con @ en lugares incorrectos)
    clientes_test = ClienteModel.objects.filter(email__contains='@test.com')
    
    total = clientes_test.count()
    print(f"📊 Encontrados {total} clientes de prueba")
    
    if total > 0:
        clientes_test.delete()
        print(f"✅ {total} clientes eliminados")
    else:
        print("✅ No hay clientes para eliminar")
    
    print("\n🎉 Limpieza completada")

if __name__ == '__main__':
    limpiar_clientes_invalidos()
