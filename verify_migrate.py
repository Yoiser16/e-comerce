#!/usr/bin/env python
"""Verificar que carritos y órdenes cargan correctamente después de migraciones."""

import sys
import os

# Agregar el directorio base al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    try:
        from django.core.management import execute_from_command_line
        from django.conf import settings
        settings.configure()
        
        # Configuración manual
        import django
        from django.conf import settings as dj_settings
        
        if not dj_settings.configured:
            import ecommerce.settings as settings_module
            
        print("✓ Django inicializado")
        
        # Directa: conectar a BD
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Carritos
            cursor.execute("SELECT COUNT(*) FROM carritos")
            carritos_count = cursor.fetchone()[0]
            print(f"✓ Carritos en BD: {carritos_count}")
            
            # Órdenes
            cursor.execute("SELECT COUNT(*) FROM ordenes")
            ordenes_count = cursor.fetchone()[0]
            print(f"✓ Órdenes en BD: {ordenes_count}")
            
            # Items de carrito
            cursor.execute("SELECT COUNT(*) FROM items_carrito")
            items_carrito = cursor.fetchone()[0]
            print(f"✓ Items en carritos: {items_carrito}")
            
            # Líneas de orden
            cursor.execute("SELECT COUNT(*) FROM lineas_orden")
            lineas_orden = cursor.fetchone()[0]
            print(f"✓ Líneas en órdenes: {lineas_orden}")
            
            # Verificar que nuevas columnas existen
            cursor.execute("PRAGMA table_info(items_carrito)")
            cols = cursor.fetchall()
            col_names = [col[1] for col in cols]
            
            required_cols = ['variante_id', 'variante_sku', 'color_snapshot', 'largo_snapshot']
            missing = [c for c in required_cols if c not in col_names]
            
            if missing:
                print(f"✗ Columnas faltantes en items_carrito: {missing}")
                sys.exit(1)
            else:
                print(f"✓ Todas las columnas de variantes en items_carrito")
            
            # Verificar LineaOrden
            cursor.execute("PRAGMA table_info(lineas_orden)")
            cols = cursor.fetchall()
            col_names = [col[1] for col in cols]
            
            required_cols = ['variante_id', 'variante_sku', 'color_snapshot', 'largo_snapshot']
            missing = [c for c in required_cols if c not in col_names]
            
            if missing:
                print(f"✗ Columnas faltantes en lineas_orden: {missing}")
                sys.exit(1)
            else:
                print(f"✓ Todas las columnas de variantes en lineas_orden")
            
            print("\n✓ Migraciones aplicadas correctamente - BD lista para variantes")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
