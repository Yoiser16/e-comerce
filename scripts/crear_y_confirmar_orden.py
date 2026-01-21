#!/usr/bin/env python3
"""
Script para crear y confirmar una orden de prueba
para generar movimientos de inventario reales
"""
import sys
import os

# Configurar path para Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.config.django_settings')

import django
django.setup()

from decimal import Decimal
from uuid import uuid4
from infrastructure.persistence.django.models import (
    OrdenModel, 
    ProductoModel, 
    LineaOrdenModel,
    ClienteModel
)

def crear_y_confirmar_orden():
    """Crea y confirma una orden para generar movimientos reales"""
    
    # Obtener primer producto disponible
    producto = ProductoModel.objects.filter(activo=True, stock_actual__gt=0).first()
    
    if not producto:
        print("❌ No hay productos con stock disponible")
        return
    
    print(f"📦 Producto seleccionado: {producto.nombre}")
    print(f"   Stock actual: {producto.stock_actual}")
    print(f"   Precio: ${producto.monto_precio:,.0f} COP")
    
    # Crear o obtener cliente de prueba
    cliente, created = ClienteModel.objects.get_or_create(
        email='test@test.com',
        defaults={
            'id': uuid4(),
            'nombre': 'Cliente Test',
            'telefono': '3001234567',
            'tipo_documento': 'CC',
            'numero_documento': '123456789'
        }
    )
    
    cantidad = 2
    subtotal = Decimal(producto.monto_precio) * cantidad
    envio = Decimal('10000')
    total = subtotal + envio
    
    # Crear orden en BORRADOR
    orden = OrdenModel.objects.create(
        id=uuid4(),
        codigo=f"TEST-{uuid4().hex[:6].upper()}",
        estado='borrador',
        cliente=cliente,
        direccion_envio='Calle Test 123',
        departamento='Cundinamarca',
        municipio='Bogotá',
        barrio='Chapinero',
        subtotal_monto=subtotal,
        envio_monto=envio,
        total_monto=total,
        total_moneda='COP',
        metodo_pago='whatsapp'
    )
    
    # Agregar línea de producto
    linea = LineaOrdenModel.objects.create(
        id=uuid4(),
        orden=orden,
        producto_id=producto.id,
        cantidad=cantidad,
        precio_unitario_monto=Decimal(producto.monto_precio),
        precio_unitario_moneda='COP',
        subtotal_monto=subtotal,
        subtotal_moneda='COP'
    )
    
    print(f"\n✅ Orden creada: {orden.codigo}")
    print(f"   ID: {orden.id}")
    print(f"   Estado: {orden.estado}")
    print(f"   Total: ${orden.total_monto:,.0f} COP")
    print(f"   Items: {linea.cantidad} x {producto.nombre}")
    
    # Confirmar orden (esto generará movimientos de inventario)
    print(f"\n⏳ Confirmando orden...")
    
    from infrastructure.persistence.repositories.orden_repository_impl import OrdenRepositoryImpl
    from infrastructure.auditing.servicio_auditoria import ServicioAuditoria
    
    repo = OrdenRepositoryImpl(auditoria=ServicioAuditoria())
    
    try:
        orden_confirmada = repo.confirmar_con_stock(orden.id)
        print(f"✅ Orden confirmada exitosamente!")
        print(f"   Nuevo estado: {orden_confirmada.estado.value}")
        
        # Verificar stock actualizado
        producto_actualizado = ProductoModel.objects.get(id=producto.id)
        print(f"\n📊 Stock actualizado:")
        print(f"   Antes: {producto.stock_actual}")
        print(f"   Después: {producto_actualizado.stock_actual}")
        print(f"   Diferencia: -{linea.cantidad}")
        
        print(f"\n🎉 ¡Movimiento de inventario generado!")
        print(f"   Ve a: Panel Admin → Inventario → Movimientos/Kardex")
        
        return orden.id
        
    except Exception as e:
        print(f"❌ Error al confirmar orden: {e}")
        return None

if __name__ == '__main__':
    crear_y_confirmar_orden()
