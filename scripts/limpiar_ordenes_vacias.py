#!/usr/bin/env python3
"""
Script para eliminar órdenes vacías (sin líneas) de la base de datos
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.config.django_settings')
django.setup()

from infrastructure.persistence.django.models import OrdenModel, LineaOrdenModel

def limpiar_ordenes_vacias():
    """Elimina todas las órdenes que no tienen líneas (productos)"""
    
    # Obtener todas las órdenes
    todas_ordenes = OrdenModel.objects.all()
    ordenes_vacias = []
    
    for orden in todas_ordenes:
        # Contar líneas de la orden
        num_lineas = LineaOrdenModel.objects.filter(orden_id=orden.id).count()
        if num_lineas == 0:
            ordenes_vacias.append(orden)
    
    if not ordenes_vacias:
        print("✅ No hay órdenes vacías para limpiar")
        return
    
    print(f"🗑️  Encontradas {len(ordenes_vacias)} órdenes vacías:")
    for orden in ordenes_vacias:
        print(f"   - {orden.codigo} (Estado: {orden.estado}, Fecha: {orden.fecha_creacion})")
    
    confirmar = input(f"\n¿Eliminar estas {len(ordenes_vacias)} órdenes? (s/N): ")
    
    if confirmar.lower() != 's':
        print("❌ Operación cancelada")
        return
    
    # Eliminar órdenes vacías
    contador = 0
    for orden in ordenes_vacias:
        orden.delete()
        contador += 1
    
    print(f"\n✅ {contador} órdenes vacías eliminadas")

if __name__ == '__main__':
    limpiar_ordenes_vacias()
