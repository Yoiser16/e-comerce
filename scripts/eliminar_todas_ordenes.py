#!/usr/bin/env python3
"""
Script para eliminar todas las órdenes de la base de datos
"""
import sys
import os

# Configurar path para Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.config.django_settings')

import django
django.setup()

from infrastructure.persistence.django.models import OrdenModel, LineaOrdenModel

def eliminar_todas_ordenes():
    """Elimina todas las órdenes y sus líneas"""
    
    print("⚠️  ELIMINANDO TODAS LAS ÓRDENES...")
    
    # Contar antes
    total_ordenes = OrdenModel.objects.count()
    total_lineas = LineaOrdenModel.objects.count()
    
    print(f"📊 Encontradas:")
    print(f"   - {total_ordenes} órdenes")
    print(f"   - {total_lineas} líneas de orden")
    
    if total_ordenes == 0:
        print("✅ No hay órdenes para eliminar")
        return
    
    # Eliminar primero las líneas (FK constraint)
    LineaOrdenModel.objects.all().delete()
    print(f"✅ {total_lineas} líneas eliminadas")
    
    # Eliminar órdenes
    OrdenModel.objects.all().delete()
    print(f"✅ {total_ordenes} órdenes eliminadas")
    
    print("\n🎉 Base de datos limpia - Todas las órdenes eliminadas")

if __name__ == '__main__':
    eliminar_todas_ordenes()
