"""
Tests del Módulo de Carrito de Compras

Ejecutar: python scripts/test_carrito.py
"""
import sys
import os
from uuid import uuid4
from decimal import Decimal
from datetime import datetime, timedelta

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


# ===== TESTS DE ESTADO =====

def test_estado_carrito_transiciones():
    """Test: Transiciones válidas de estado del carrito"""
    from shared.enums.estado_carrito import EstadoCarrito
    
    print("🧪 Test: Transiciones de estado del carrito")
    
    # CREADO puede ir a ACTIVO y EXPIRADO
    assert EstadoCarrito.CREADO.puede_transicionar_a(EstadoCarrito.ACTIVO)
    assert EstadoCarrito.CREADO.puede_transicionar_a(EstadoCarrito.EXPIRADO)
    assert not EstadoCarrito.CREADO.puede_transicionar_a(EstadoCarrito.CONFIRMADO)
    
    # ACTIVO puede ir a BLOQUEADO y EXPIRADO
    assert EstadoCarrito.ACTIVO.puede_transicionar_a(EstadoCarrito.BLOQUEADO)
    assert EstadoCarrito.ACTIVO.puede_transicionar_a(EstadoCarrito.EXPIRADO)
    assert not EstadoCarrito.ACTIVO.puede_transicionar_a(EstadoCarrito.CONFIRMADO)
    
    # BLOQUEADO puede ir a ACTIVO, CONFIRMADO y EXPIRADO
    assert EstadoCarrito.BLOQUEADO.puede_transicionar_a(EstadoCarrito.ACTIVO)
    assert EstadoCarrito.BLOQUEADO.puede_transicionar_a(EstadoCarrito.CONFIRMADO)
    
    # CONFIRMADO no puede transicionar
    assert not EstadoCarrito.CONFIRMADO.puede_transicionar_a(EstadoCarrito.ACTIVO)
    assert EstadoCarrito.CONFIRMADO.es_inmutable
    
    print("   ✅ Transiciones de estado correctas")


# ===== TESTS DE ITEM CARRITO =====

def test_item_carrito_inmutable():
    """Test: ItemCarrito es inmutable y calcula subtotal"""
    from domain.value_objects.item_carrito import ItemCarrito
    from domain.value_objects.dinero import Dinero
    
    print("🧪 Test: ItemCarrito inmutabilidad y cálculos")
    
    producto_id = uuid4()
    precio = Dinero(Decimal("100.00"), "USD")
    
    item = ItemCarrito(
        producto_id=producto_id,
        nombre_snapshot="Extensión Brasileña 18\"",
        sku="EXT-BRA-18",
        cantidad=3,
        precio_unitario_snapshot=precio
    )
    
    # Subtotal se calcula correctamente
    assert item.subtotal.monto == Decimal("300.00")
    
    # con_cantidad crea una nueva instancia
    item_actualizado = item.con_cantidad(5)
    assert item.cantidad == 3  # Original no cambió
    assert item_actualizado.cantidad == 5
    assert item_actualizado.subtotal.monto == Decimal("500.00")
    
    print("   ✅ ItemCarrito inmutable y cálculos correctos")


# ===== TESTS DE CARRITO =====

def test_carrito_agregar_productos():
    """Test: Agregar productos al carrito"""
    from domain.entities.carrito import Carrito
    from domain.value_objects.item_carrito import ItemCarrito
    from domain.value_objects.dinero import Dinero
    from shared.enums.estado_carrito import EstadoCarrito
    
    print("🧪 Test: Agregar productos al carrito")
    
    usuario_id = uuid4()
    carrito = Carrito(usuario_id=usuario_id)
    
    # Verificar estado inicial
    assert carrito.estado == EstadoCarrito.CREADO
    assert carrito.esta_vacio
    
    # Agregar primer producto
    item1 = ItemCarrito(
        producto_id=uuid4(),
        nombre_snapshot="Extensión Peruana 20\"",
        sku="EXT-PER-20",
        cantidad=2,
        precio_unitario_snapshot=Dinero(Decimal("150.00"), "USD")
    )
    
    carrito.agregar_producto(item1)
    
    assert carrito.cantidad_productos == 1
    assert carrito.cantidad_items == 2
    assert carrito.total_bruto.monto == Decimal("300.00")
    assert carrito.estado == EstadoCarrito.ACTIVO  # Auto-activación
    
    print("   ✅ Productos agregados correctamente")


def test_carrito_no_duplicados():
    """Test: No permite productos duplicados"""
    from domain.entities.carrito import Carrito
    from domain.value_objects.item_carrito import ItemCarrito
    from domain.value_objects.dinero import Dinero
    from domain.exceptions.dominio import ReglaNegocioViolada
    
    print("🧪 Test: Validación de productos duplicados")
    
    usuario_id = uuid4()
    producto_id = uuid4()
    carrito = Carrito(usuario_id=usuario_id)
    
    item = ItemCarrito(
        producto_id=producto_id,
        nombre_snapshot="Extensión",
        sku="EXT-001",
        cantidad=1,
        precio_unitario_snapshot=Dinero(Decimal("100.00"), "USD")
    )
    
    carrito.agregar_producto(item)
    
    # Intentar agregar el mismo producto debe fallar
    item_duplicado = ItemCarrito(
        producto_id=producto_id,  # Mismo ID
        nombre_snapshot="Extensión",
        sku="EXT-001",
        cantidad=2,
        precio_unitario_snapshot=Dinero(Decimal("100.00"), "USD")
    )
    
    try:
        carrito.agregar_producto(item_duplicado)
        assert False, "Debería fallar con producto duplicado"
    except ReglaNegocioViolada as e:
        assert "ya existe" in str(e)
    
    print("   ✅ Validación de duplicados correcta")


def test_carrito_actualizar_cantidad():
    """Test: Actualizar cantidad de un producto"""
    from domain.entities.carrito import Carrito
    from domain.value_objects.item_carrito import ItemCarrito
    from domain.value_objects.dinero import Dinero
    
    print("🧪 Test: Actualizar cantidad de producto")
    
    usuario_id = uuid4()
    producto_id = uuid4()
    carrito = Carrito(usuario_id=usuario_id)
    
    item = ItemCarrito(
        producto_id=producto_id,
        nombre_snapshot="Extensión",
        sku="EXT-001",
        cantidad=1,
        precio_unitario_snapshot=Dinero(Decimal("100.00"), "USD")
    )
    
    carrito.agregar_producto(item)
    carrito.actualizar_cantidad(producto_id, 5)
    
    assert carrito.cantidad_items == 5
    assert carrito.total_bruto.monto == Decimal("500.00")
    
    print("   ✅ Cantidad actualizada correctamente")


def test_carrito_quitar_producto():
    """Test: Quitar producto del carrito"""
    from domain.entities.carrito import Carrito
    from domain.value_objects.item_carrito import ItemCarrito
    from domain.value_objects.dinero import Dinero
    
    print("🧪 Test: Quitar producto del carrito")
    
    usuario_id = uuid4()
    producto_id = uuid4()
    carrito = Carrito(usuario_id=usuario_id)
    
    item = ItemCarrito(
        producto_id=producto_id,
        nombre_snapshot="Extensión",
        sku="EXT-001",
        cantidad=2,
        precio_unitario_snapshot=Dinero(Decimal("100.00"), "USD")
    )
    
    carrito.agregar_producto(item)
    assert not carrito.esta_vacio
    
    item_eliminado = carrito.quitar_producto(producto_id)
    
    assert carrito.esta_vacio
    assert item_eliminado.producto_id == producto_id
    
    print("   ✅ Producto eliminado correctamente")


def test_carrito_bloquear_confirmar():
    """Test: Flujo bloquear -> confirmar"""
    from domain.entities.carrito import Carrito
    from domain.value_objects.item_carrito import ItemCarrito
    from domain.value_objects.dinero import Dinero
    from shared.enums.estado_carrito import EstadoCarrito
    
    print("🧪 Test: Flujo bloquear -> confirmar")
    
    usuario_id = uuid4()
    carrito = Carrito(usuario_id=usuario_id)
    
    item = ItemCarrito(
        producto_id=uuid4(),
        nombre_snapshot="Extensión",
        sku="EXT-001",
        cantidad=1,
        precio_unitario_snapshot=Dinero(Decimal("100.00"), "USD")
    )
    
    carrito.agregar_producto(item)
    
    # Bloquear
    carrito.bloquear()
    assert carrito.estado == EstadoCarrito.BLOQUEADO
    # El estado BLOQUEADO no permite modificaciones
    assert not carrito.estado.permite_modificaciones
    
    # Confirmar
    result = carrito.confirmar()
    assert result == True
    assert carrito.estado == EstadoCarrito.CONFIRMADO
    
    # Idempotencia
    result2 = carrito.confirmar()
    assert result2 == False  # Ya estaba confirmado
    
    print("   ✅ Flujo bloquear -> confirmar correcto")


def test_carrito_no_modificar_confirmado():
    """Test: No se puede modificar un carrito confirmado"""
    from domain.entities.carrito import Carrito
    from domain.value_objects.item_carrito import ItemCarrito
    from domain.value_objects.dinero import Dinero
    from domain.exceptions.dominio import ReglaNegocioViolada
    
    print("🧪 Test: Carrito confirmado es inmutable")
    
    usuario_id = uuid4()
    carrito = Carrito(usuario_id=usuario_id)
    
    item = ItemCarrito(
        producto_id=uuid4(),
        nombre_snapshot="Extensión",
        sku="EXT-001",
        cantidad=1,
        precio_unitario_snapshot=Dinero(Decimal("100.00"), "USD")
    )
    
    carrito.agregar_producto(item)
    carrito.bloquear()
    carrito.confirmar()
    
    # Verificar que está confirmado
    assert carrito.estado.es_inmutable
    
    # Intentar agregar producto debe fallar
    new_item = ItemCarrito(
        producto_id=uuid4(),
        nombre_snapshot="Otro producto",
        sku="EXT-002",
        cantidad=1,
        precio_unitario_snapshot=Dinero(Decimal("50.00"), "USD")
    )
    
    try:
        carrito.agregar_producto(new_item)
        assert False, "Debería fallar al modificar carrito confirmado"
    except ReglaNegocioViolada as e:
        assert "no permite modificaciones" in str(e)
    
    print("   ✅ Carrito confirmado es inmutable")


def test_carrito_version_incrementa():
    """Test: Versión incrementa con cada operación"""
    from domain.entities.carrito import Carrito
    from domain.value_objects.item_carrito import ItemCarrito
    from domain.value_objects.dinero import Dinero
    
    print("🧪 Test: Versionamiento optimistic locking")
    
    usuario_id = uuid4()
    carrito = Carrito(usuario_id=usuario_id)
    version_inicial = carrito.version
    
    producto_id = uuid4()
    item = ItemCarrito(
        producto_id=producto_id,
        nombre_snapshot="Extensión",
        sku="EXT-001",
        cantidad=1,
        precio_unitario_snapshot=Dinero(Decimal("100.00"), "USD")
    )
    
    carrito.agregar_producto(item)
    assert carrito.version == version_inicial + 1
    
    carrito.actualizar_cantidad(producto_id, 3)
    assert carrito.version == version_inicial + 2
    
    print("   ✅ Versión incrementa correctamente")


def test_eventos_carrito():
    """Test: Eventos de dominio del carrito"""
    from domain.events.eventos_carrito import (
        CarritoCreado,
        ProductoAgregadoAlCarrito
    )
    
    print("🧪 Test: Eventos de dominio")
    
    # Evento CarritoCreado (requiere expira_en)
    carrito_id = uuid4()
    usuario_id = uuid4()
    expira_en = datetime.now() + timedelta(hours=24)
    evento = CarritoCreado(carrito_id, usuario_id, expira_en)
    
    assert evento.carrito_id == carrito_id
    assert evento.usuario_id == usuario_id
    assert evento.expira_en == expira_en
    assert evento.ocurrido_en is not None
    
    # Evento ProductoAgregadoAlCarrito
    evento_producto = ProductoAgregadoAlCarrito(
        carrito_id=carrito_id,
        usuario_id=usuario_id,
        producto_id=uuid4(),
        sku="EXT-001",
        nombre_producto="Extensión",
        cantidad=2,
        precio_unitario=Decimal("100.00"),
        moneda="USD"
    )
    
    assert evento_producto.cantidad == 2
    assert evento_producto.precio_unitario == Decimal("100.00")
    
    print("   ✅ Eventos de dominio correctos")


def test_carrito_expiracion():
    """Test: Carrito tiene fecha de expiración"""
    from domain.entities.carrito import Carrito
    
    print("🧪 Test: Carrito expiración")
    
    usuario_id = uuid4()
    carrito = Carrito(usuario_id=usuario_id)
    
    # Carrito tiene fecha de expiración
    assert carrito.expira_en is not None
    assert carrito.expira_en > datetime.now()
    
    # No está expirado recién creado
    assert not carrito.esta_expirado
    
    print("   ✅ Expiración configurada correctamente")


# ===== EJECUTAR TODOS LOS TESTS =====

def run_all_tests():
    print("\n" + "="*60)
    print("🛒 TESTS DEL MÓDULO DE CARRITO DE COMPRAS")
    print("="*60 + "\n")
    
    tests = [
        test_estado_carrito_transiciones,
        test_item_carrito_inmutable,
        test_carrito_agregar_productos,
        test_carrito_no_duplicados,
        test_carrito_actualizar_cantidad,
        test_carrito_quitar_producto,
        test_carrito_bloquear_confirmar,
        test_carrito_no_modificar_confirmado,
        test_carrito_version_incrementa,
        test_eventos_carrito,
        test_carrito_expiracion,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"   ❌ FALLÓ: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 RESULTADOS: {passed} pasaron, {failed} fallaron")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
