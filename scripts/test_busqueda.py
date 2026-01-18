"""
Tests del Módulo de Búsqueda y Filtros Avanzados

Ejecutar: python scripts/test_busqueda.py
"""
import sys
import os
from uuid import uuid4
from decimal import Decimal

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


# ===== TESTS DE ENUMS =====

def test_enums_colores():
    """Test: Enum de colores de cabello"""
    from shared.enums.atributos_producto import ColorCabello
    
    print("🧪 Test: Enum ColorCabello")
    
    # Verificar que existen los colores principales
    assert ColorCabello.NEGRO_NATURAL.value == "negro_natural"
    assert ColorCabello.RUBIO_PLATINO.value == "rubio_platino"
    assert ColorCabello.CASTANO_CHOCOLATE.value == "castano_chocolate"
    
    # Verificar categorías
    categorias = ColorCabello.categorias()
    assert "negros" in categorias
    assert "rubios" in categorias
    assert ColorCabello.NEGRO_NATURAL in categorias["negros"]
    
    print("   ✅ Enum ColorCabello correcto")


def test_enums_tipos():
    """Test: Enum de tipos de cabello"""
    from shared.enums.atributos_producto import TipoCabello
    
    print("🧪 Test: Enum TipoCabello")
    
    assert TipoCabello.LISO.value == "liso"
    assert TipoCabello.ONDULADO.value == "ondulado"
    assert TipoCabello.BODY_WAVE.value == "body_wave"
    
    print("   ✅ Enum TipoCabello correcto")


def test_enums_largos():
    """Test: Enum de largos con valor numérico"""
    from shared.enums.atributos_producto import LargoCabello
    
    print("🧪 Test: Enum LargoCabello")
    
    assert LargoCabello.PULGADAS_18.value == "18"
    assert LargoCabello.PULGADAS_18.valor_numerico == 18
    
    # Test rango
    rango = LargoCabello.rango(14, 20)
    assert LargoCabello.PULGADAS_16 in rango
    assert LargoCabello.PULGADAS_18 in rango
    assert LargoCabello.PULGADAS_24 not in rango
    
    print("   ✅ Enum LargoCabello correcto")


def test_enums_orden():
    """Test: Enum de ordenamiento"""
    from shared.enums.atributos_producto import OrdenProducto
    
    print("🧪 Test: Enum OrdenProducto")
    
    assert OrdenProducto.PRECIO_ASC.value == "precio_asc"
    assert OrdenProducto.MAS_VENDIDOS.value == "mas_vendidos"
    assert OrdenProducto.RELEVANCIA.value == "relevancia"
    
    print("   ✅ Enum OrdenProducto correcto")


# ===== TESTS DE VALUE OBJECTS =====

def test_rango_precio():
    """Test: RangoPrecio value object"""
    from domain.value_objects.criterios_busqueda import RangoPrecio
    
    print("🧪 Test: RangoPrecio value object")
    
    # Rango válido
    rango = RangoPrecio(minimo=Decimal("50"), maximo=Decimal("200"))
    assert rango.esta_definido
    assert rango.contiene(Decimal("100"))
    assert not rango.contiene(Decimal("250"))
    assert not rango.contiene(Decimal("30"))
    
    # Solo mínimo
    rango_min = RangoPrecio(minimo=Decimal("100"))
    assert rango_min.contiene(Decimal("150"))
    assert not rango_min.contiene(Decimal("50"))
    
    # Solo máximo
    rango_max = RangoPrecio(maximo=Decimal("100"))
    assert rango_max.contiene(Decimal("50"))
    assert not rango_max.contiene(Decimal("150"))
    
    print("   ✅ RangoPrecio correcto")


def test_rango_precio_validacion():
    """Test: RangoPrecio validaciones"""
    from domain.value_objects.criterios_busqueda import RangoPrecio
    
    print("🧪 Test: RangoPrecio validaciones")
    
    # Min > Max debe fallar
    try:
        RangoPrecio(minimo=Decimal("200"), maximo=Decimal("100"))
        assert False, "Debería fallar con min > max"
    except ValueError:
        pass
    
    # Precio negativo debe fallar
    try:
        RangoPrecio(minimo=Decimal("-50"))
        assert False, "Debería fallar con precio negativo"
    except ValueError:
        pass
    
    print("   ✅ Validaciones de RangoPrecio correctas")


def test_filtros_producto():
    """Test: FiltrosProducto value object"""
    from domain.value_objects.criterios_busqueda import FiltrosProducto, RangoPrecio
    from shared.enums.atributos_producto import ColorCabello, TipoCabello
    
    print("🧪 Test: FiltrosProducto value object")
    
    # Filtros vacíos
    filtros_vacios = FiltrosProducto()
    assert not filtros_vacios.tiene_filtros_activos
    
    # Filtros con valores
    filtros = FiltrosProducto(
        texto_busqueda="brasileño",
        colores=frozenset([ColorCabello.NEGRO_NATURAL, ColorCabello.CASTANO_OSCURO]),
        tipos=frozenset([TipoCabello.LISO]),
        rango_precio=RangoPrecio(minimo=Decimal("50"), maximo=Decimal("300"))
    )
    
    assert filtros.tiene_filtros_activos
    assert filtros.texto_busqueda == "brasileño"
    assert ColorCabello.NEGRO_NATURAL in filtros.colores
    
    print("   ✅ FiltrosProducto correcto")


def test_filtros_inmutables():
    """Test: FiltrosProducto es inmutable"""
    from domain.value_objects.criterios_busqueda import FiltrosProducto
    from shared.enums.atributos_producto import ColorCabello
    
    print("🧪 Test: FiltrosProducto inmutabilidad")
    
    filtros = FiltrosProducto(texto_busqueda="original")
    
    # con_texto crea nueva instancia
    filtros_nuevo = filtros.con_texto("nuevo texto")
    
    assert filtros.texto_busqueda == "original"
    assert filtros_nuevo.texto_busqueda == "nuevo texto"
    
    # con_colores crea nueva instancia
    filtros_con_color = filtros.con_colores([ColorCabello.RUBIO_PLATINO])
    assert filtros.colores is None
    assert ColorCabello.RUBIO_PLATINO in filtros_con_color.colores
    
    print("   ✅ FiltrosProducto es inmutable")


def test_criterios_busqueda():
    """Test: CriteriosBusqueda value object"""
    from domain.value_objects.criterios_busqueda import CriteriosBusqueda, FiltrosProducto
    from shared.enums.atributos_producto import OrdenProducto
    
    print("🧪 Test: CriteriosBusqueda value object")
    
    criterios = CriteriosBusqueda(
        filtros=FiltrosProducto(texto_busqueda="extensión"),
        orden=OrdenProducto.PRECIO_ASC,
        pagina=2,
        por_pagina=20
    )
    
    assert criterios.offset == 20  # (pagina 2 - 1) * 20
    assert criterios.limit == 20
    
    # Límite máximo
    criterios_exceso = CriteriosBusqueda(por_pagina=500)
    assert criterios_exceso.por_pagina == 100  # MAX_POR_PAGINA
    
    print("   ✅ CriteriosBusqueda correcto")


# ===== TESTS DE DTOs =====

def test_dto_busqueda_request():
    """Test: DTO de request de búsqueda"""
    from application.dto.busqueda_dto import BusquedaProductoRequestDTO
    from shared.enums.atributos_producto import ColorCabello, OrdenProducto
    
    print("🧪 Test: BusquedaProductoRequestDTO")
    
    request = BusquedaProductoRequestDTO(
        q="brasileño liso",
        colores=[ColorCabello.NEGRO_NATURAL],
        precio_min=Decimal("50"),
        precio_max=Decimal("200"),
        orden=OrdenProducto.PRECIO_ASC,
        pagina=1,
        por_pagina=20
    )
    
    assert request.q == "brasileño liso"
    assert ColorCabello.NEGRO_NATURAL in request.colores
    assert request.precio_min == Decimal("50")
    
    print("   ✅ BusquedaProductoRequestDTO correcto")


def test_dto_busqueda_validacion():
    """Test: Validaciones del DTO de búsqueda"""
    from application.dto.busqueda_dto import BusquedaProductoRequestDTO
    from pydantic import ValidationError
    
    print("🧪 Test: Validaciones de BusquedaProductoRequestDTO")
    
    # Precio negativo debe fallar
    try:
        BusquedaProductoRequestDTO(precio_min=Decimal("-50"))
        assert False, "Debería fallar con precio negativo"
    except ValidationError:
        pass
    
    # Página 0 debe fallar
    try:
        BusquedaProductoRequestDTO(pagina=0)
        assert False, "Debería fallar con página 0"
    except ValidationError:
        pass
    
    # por_pagina > 100 debe fallar
    try:
        BusquedaProductoRequestDTO(por_pagina=500)
        assert False, "Debería fallar con por_pagina > 100"
    except ValidationError:
        pass
    
    print("   ✅ Validaciones de DTO correctas")


def test_dto_producto_busqueda():
    """Test: DTO de producto en resultados"""
    from application.dto.busqueda_dto import ProductoBusquedaDTO
    from shared.enums.atributos_producto import ColorCabello, TipoCabello
    
    print("🧪 Test: ProductoBusquedaDTO")
    
    producto = ProductoBusquedaDTO(
        id=uuid4(),
        codigo="EXT-BRA-001",
        nombre="Extensión Brasileña Virgin",
        descripcion_corta="Cabello 100% humano brasileño",
        precio=Decimal("150.00"),
        precio_original=Decimal("200.00"),
        moneda="USD",
        color=ColorCabello.NEGRO_NATURAL,
        tipo=TipoCabello.LISO,
        disponible=True,
        stock_disponible=50,
        tiene_descuento=True,
        porcentaje_descuento=25
    )
    
    assert producto.codigo == "EXT-BRA-001"
    assert producto.tiene_descuento
    assert producto.porcentaje_descuento == 25
    
    print("   ✅ ProductoBusquedaDTO correcto")


def test_dto_paginacion():
    """Test: DTO de paginación"""
    from application.dto.busqueda_dto import PaginacionDTO
    
    print("🧪 Test: PaginacionDTO")
    
    paginacion = PaginacionDTO(
        pagina_actual=2,
        por_pagina=20,
        total_resultados=85,
        total_paginas=5,
        tiene_siguiente=True,
        tiene_anterior=True
    )
    
    assert paginacion.total_paginas == 5
    assert paginacion.tiene_siguiente
    assert paginacion.tiene_anterior
    
    print("   ✅ PaginacionDTO correcto")


def test_dto_facetas():
    """Test: DTOs de facetas"""
    from application.dto.busqueda_dto import FacetaDTO, GrupoFacetasDTO
    
    print("🧪 Test: DTOs de facetas")
    
    faceta = FacetaDTO(
        valor="negro_natural",
        etiqueta="Negro Natural",
        cantidad=25,
        seleccionado=False
    )
    
    grupo = GrupoFacetasDTO(
        nombre="Color",
        clave="colores",
        tipo="checkbox",
        opciones=[faceta]
    )
    
    assert grupo.nombre == "Color"
    assert len(grupo.opciones) == 1
    assert grupo.opciones[0].cantidad == 25
    
    print("   ✅ DTOs de facetas correctos")


# ===== EJECUTAR TODOS LOS TESTS =====

def run_all_tests():
    print("\n" + "="*60)
    print("🔍 TESTS DEL MÓDULO DE BÚSQUEDA Y FILTROS")
    print("="*60 + "\n")
    
    tests = [
        test_enums_colores,
        test_enums_tipos,
        test_enums_largos,
        test_enums_orden,
        test_rango_precio,
        test_rango_precio_validacion,
        test_filtros_producto,
        test_filtros_inmutables,
        test_criterios_busqueda,
        test_dto_busqueda_request,
        test_dto_busqueda_validacion,
        test_dto_producto_busqueda,
        test_dto_paginacion,
        test_dto_facetas,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"   ❌ FALLÓ: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 RESULTADOS: {passed} pasaron, {failed} fallaron")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
