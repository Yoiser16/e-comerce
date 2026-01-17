
import os
import sys
import django
from decimal import Decimal
from uuid import uuid4

# Configurar entorno
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infrastructure.config.django_settings")
django.setup()

from domain.entities.cliente import Cliente
from domain.entities.producto import Producto
from domain.entities.orden import Orden
from domain.value_objects.email import Email
from domain.value_objects.codigo_producto import CodigoProducto
from domain.value_objects.documento_identidad import DocumentoIdentidad
from domain.value_objects.dinero import Dinero
from domain.value_objects.linea_orden import LineaOrden
from shared.enums.tipos_documento import TipoDocumento

from infrastructure.persistence.repositories.cliente_repository_impl import ClienteRepositoryImpl
from infrastructure.persistence.repositories.producto_repository_impl import ProductoRepositoryImpl
from infrastructure.persistence.repositories.orden_repository_impl import OrdenRepositoryImpl

def test_flujo_completo():
    print("--- INICIANDO TEST DE INTEGRACIÓN: ORDENES ---")
    
    repo_cliente = ClienteRepositoryImpl()
    repo_producto = ProductoRepositoryImpl()
    repo_orden = OrdenRepositoryImpl()
    
    # 1. Crear un Cliente
    email_val = f"user_{str(uuid4())[:4]}@test.com"
    cliente = Cliente(
        nombre="Test User",
        apellido="Integration",
        email=Email(email_val),
        documento=DocumentoIdentidad(TipoDocumento.DNI, str(uuid4())[:8])
    )
    cliente = repo_cliente.guardar(cliente)
    print(f"✅ Cliente creado: {cliente.id}")
    
    # 2. Crear un Producto
    codigo_val = f"SKU-{str(uuid4())[:4]}"
    producto = Producto(
        codigo=CodigoProducto(codigo_val),
        nombre="Laptop Gamer",
        descripcion="Potente",
        precio=Dinero(Decimal("1500.00")),
        stock_actual=50
    )
    producto = repo_producto.guardar(producto)
    print(f"✅ Producto creado: {producto.id}")
    
    # 3. Crear una Orden
    orden = Orden(cliente_id=cliente.id)
    
    # 4. Agregar Línea a la Orden
    linea = LineaOrden(
        producto_id=producto.id,
        cantidad=2,
        precio_unitario=producto.precio
    )
    orden.agregar_linea(linea)
    
    # 5. Guardar Orden (y sus líneas)
    print("Guardando orden...")
    orden_guardada = repo_orden.guardar(orden)
    print(f"✅ Orden guardada: {orden_guardada.id}")
    
    # 6. Verificaciones
    recuperada = repo_orden.obtener_por_id(orden_guardada.id)
    
    if len(recuperada.lineas) == 1:
        print("✅ Lineas persistidas correctamente")
    else:
        print(f"❌ Error: Se esperaban 1 linea, encontradas {len(recuperada.lineas)}")
        
    total_esperado = Decimal("3000.00") # 1500 * 2
    if recuperada.total.monto == total_esperado:
        print("✅ Total calculado correctamente")
    else:
        print(f"❌ Error en total: {recuperada.total.monto}")

    # 7. Limpieza (Opcional, soft delete)
    # repo_orden.eliminar(recuperada.id)

if __name__ == "__main__":
    test_flujo_completo()
