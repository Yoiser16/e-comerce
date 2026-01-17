
import os
import sys
import django
from decimal import Decimal
from uuid import uuid4

# Configurar entorno
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infrastructure.config.django_settings")
django.setup()

from domain.entities.producto import Producto
from domain.value_objects.codigo_producto import CodigoProducto
from domain.value_objects.dinero import Dinero
from infrastructure.persistence.repositories.producto_repository_impl import ProductoRepositoryImpl

def test_producto_repo():
    print("--- INICIANDO TEST DE PRODUCTO ---")
    repo = ProductoRepositoryImpl()
    
    # 1. Crear producto
    codigo = f"TEST-{str(uuid4())[:4]}"
    producto = Producto(
        codigo=CodigoProducto(codigo),
        nombre="Producto Prueba",
        descripcion="Un producto de prueba creado autómaticamente",
        precio=Dinero(Decimal("99.99"), "USD"),
        stock_actual=10,
        stock_minimo=2
    )
    
    print(f"Guardando producto {codigo}...")
    guardado = repo.guardar(producto)
    print(f"Producto guardado con ID: {guardado.id}")
    
    # 2. Obtener por ID
    recuperado = repo.obtener_por_id(guardado.id)
    if recuperado and recuperado.nombre == "Producto Prueba":
        print("✅ Recuperado por ID correctamente")
    else:
        print("❌ Error recuperando por ID")
        
    # 3. Obtener por Código
    recuperado_codigo = repo.obtener_por_codigo(CodigoProducto(codigo))
    if recuperado_codigo and recuperado_codigo.id == guardado.id:
        print("✅ Recuperado por Código correctamente")
    else:
        print("❌ Error recuperando por Código")
        
    # 4. Verificar inventario
    bajos = repo.obtener_con_stock_bajo()
    print(f"Busqueda de stock bajo ejecutada. Encontrados: {len(bajos)}")

if __name__ == "__main__":
    test_producto_repo()
