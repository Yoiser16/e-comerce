
import os
import sys
import random
from datetime import datetime, timedelta
import django
from django.utils import timezone

# Setup Django
sys.path.append(os.path.join(os.getcwd(), 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infrastructure.config.django_settings")

try:
    django.setup()
    from infrastructure.persistence.django.models import (
        ClienteModel, ProductoModel, OrdenModel, LineaOrdenModel, CategoriaModel
    )
    from shared.enums.estados import EstadoOrden
    
    # Usamos strings directos validos para simplificar, ya que los modelos usan CharField
    # Pero nos aseguramos de usar valores que el Dominio acepte (como 'CC')

    print("=== GENERANDO DATOS DE PRUEBA (CORREGIDO) ===")

    # 1. Crear Categorías
    categorias_data = ["Tecnología", "Audio", "Accesorios", "Muebles", "Wearables", "Extensiones"]
    categorias_map = {}
    
    print(" -> Creando categorías...")
    for nombre in categorias_data:
        cat, created = CategoriaModel.objects.get_or_create(
            nombre=nombre,
            defaults={
                'slug': nombre.lower().replace(' ', '-'),
                'descripcion': f'Categoría de {nombre}',
                'activo': True
            }
        )
        categorias_map[nombre] = cat

    # 2. Crear Productos
    productos_nombres = [
        ("Smartphone XYZ", "Tecnología", 1200.00),
        ("Laptop Pro", "Tecnología", 2500.00),
        ("Auriculares NoiseCancel", "Audio", 300.00),
        ("Monitor 4K", "Tecnología", 450.00),
        ("Teclado Mecánico", "Accesorios", 150.00),
        ("Mouse Gamer", "Accesorios", 80.00),
        ("Silla Ergonómica", "Muebles", 350.00),
        ("Escritorio Ajustable", "Muebles", 500.00),
        ("Tablet Air", "Tecnología", 600.00),
        ("Reloj Inteligente", "Wearables", 250.00)
    ]

    # Map de imágenes por categoría
    imagenes_map = {
        "Tecnología": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&q=80",
        "Audio": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80",
        "Accesorios": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80",
        "Muebles": "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=500&q=80",
        "Wearables": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80",
        "Extensiones": "https://images.unsplash.com/photo-1562025176-791f4865ae93?w=500&q=80"
    }

    productos_db = []
    print(" -> Verificando productos...")
    for nombre, cat_nombre, precio in productos_nombres:
        cat = categorias_map.get(cat_nombre)
        img_url = imagenes_map.get(cat_nombre, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80")
        
        prod, created = ProductoModel.objects.get_or_create(
            nombre=nombre,
            defaults={
                'codigo': f"PROD-{random.randint(1000, 9999)}", # Importante: código único
                'descripcion': f"Descripción premium para {nombre}. Alta calidad y durabilidad.",
                'monto_precio': precio,
                'stock_actual': random.randint(10, 50),
                'stock_minimo': 5,
                'categoria': cat,
                'activo': True,
                'imagen_principal': img_url
            }
        )
        if created:
            print(f"    + Creado: {nombre}")
        productos_db.append(prod)

    # 3. Crear Clientes
    nombres_clientes = ["Ana García", "Carlos López", "María Rodríguez", "Juan Pérez", "Laura Martínez", "Pedro Sánchez", "Sofia Ruiz", "Diego Torres"]
    
    clientes_db = []
    print(" -> Verificando clientes...")
    for i, nombre in enumerate(nombres_clientes):
        email = f"{nombre.lower().replace(' ', '.')}@example.com"
        cliente, created = ClienteModel.objects.get_or_create(
            email=email,
            defaults={
                'nombre': nombre,
                'apellido': 'Test',
                'telefono': f"300123456{i}",
                'tipo_documento': 'CC', # Valor válido del Enum
                'numero_documento': f"1000{i}2233",
                'activo': True
            }
        )
        if created:
             print(f"    + Creado: {nombre}")
        clientes_db.append(cliente)

    # 4. Generar Órdenes (Históricas y Recientes)
    print(" -> Generando órdenes...")
    
    # Generar 50 órdenes distribuidas en los últimos 30 días
    ordenes_creadas = 0
    now = timezone.now()
    
    for i in range(50):
        # Random date in last 30 days
        days_ago = random.randint(0, 30)
        fecha = now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        cliente = random.choice(clientes_db)
        
        # Estado weighted
        estado = random.choices(
            ['completada', 'confirmada', 'enviada', 'pendiente', 'cancelada'],
            weights=[30, 20, 20, 10, 5],
            k=1
        )[0]
        
        # Check if code unique
        codigo_orden = f"ORD-{random.randint(10000, 99999)}-{i}"
        
        orden = OrdenModel.objects.create(
            cliente=cliente,
            codigo=codigo_orden,
            fecha_creacion=fecha,
            estado=estado,
            total_monto=0, # Se actualizará
            subtotal_monto=0,
            envio_monto=0
        )
        
        # Hack to overwrite auto_now_add for fecha_creacion
        orden.fecha_creacion = fecha
        orden.save()
        
        # Agregar items
        total = 0
        num_items = random.randint(1, 4)
        selected_prods = random.sample(productos_db, num_items)
        
        for prod in selected_prods:
            cantidad = random.randint(1, 3)
            precio_unitario = prod.monto_precio
            subtotal = precio_unitario * cantidad
            
            LineaOrdenModel.objects.create(
                orden=orden,
                producto=prod,
                cantidad=cantidad,
                precio_unitario_monto=precio_unitario,
                precio_unitario_moneda='USD',
                subtotal_monto=subtotal,
                subtotal_moneda='USD'
            )
            total += float(subtotal)
            
        orden.total_monto = total
        orden.subtotal_monto = total
        orden.save()
        ordenes_creadas += 1

    print(f"✅ Generados: {len(productos_db)} productos, {len(clientes_db)} clientes, {ordenes_creadas} nuevas órdenes.")
    print("¡Base de datos poblada para dashboard!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
