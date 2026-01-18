"""
Casos de Uso para Búsqueda y Filtros de Productos

Application Layer - Orquestación de operaciones de búsqueda.

Casos de uso:
- BuscarProductos: búsqueda principal con filtros
- ObtenerFacetas: obtener contadores de facetas
- Autocompletar: sugerencias de búsqueda
- ObtenerFiltrosRapidos: filtros predefinidos
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass
import time

from application.use_cases.base import CasoUsoBase
from application.dto.busqueda_dto import (
    BusquedaProductoRequestDTO,
    ResultadoBusquedaDTO,
    ProductoBusquedaDTO,
    GrupoFacetasDTO,
    FacetaDTO,
    PaginacionDTO,
    AutocompletadoResponseDTO,
    SugerenciaBusquedaDTO
)
from domain.value_objects.criterios_busqueda import (
    CriteriosBusqueda,
    FiltrosProducto,
    RangoPrecio,
    RangoLargo
)
from domain.repositories.producto_repository import ProductoRepository
from shared.enums.atributos_producto import (
    ColorCabello,
    TipoCabello,
    LargoCabello,
    OrigenCabello,
    MetodoAplicacion,
    CalidadCabello,
    OrdenProducto
)


class BuscarProductosUseCase(CasoUsoBase[BusquedaProductoRequestDTO, ResultadoBusquedaDTO]):
    """
    Caso de uso principal: Buscar productos con filtros avanzados.
    
    Responsabilidades:
    - Convertir DTO a criterios de dominio
    - Ejecutar búsqueda en repositorio
    - Calcular facetas
    - Construir respuesta paginada
    """
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
    
    def ejecutar(self, request: BusquedaProductoRequestDTO) -> ResultadoBusquedaDTO:
        inicio = time.time()
        
        # Convertir DTO a criterios de dominio
        criterios = self._construir_criterios(request)
        
        # Ejecutar búsqueda
        productos, total = self._repo.buscar_con_filtros(criterios)
        
        # Calcular facetas (sobre el conjunto sin paginación)
        facetas = self._calcular_facetas(request)
        
        # Construir respuesta
        tiempo_ms = int((time.time() - inicio) * 1000)
        
        return ResultadoBusquedaDTO(
            productos=self._mapear_productos(productos),
            facetas=facetas,
            paginacion=self._construir_paginacion(request, total),
            query_original=request.q,
            tiempo_busqueda_ms=tiempo_ms,
            filtros_aplicados=self._extraer_filtros_aplicados(request),
            orden_actual=request.orden,
            opciones_orden=self._opciones_orden()
        )
    
    def _construir_criterios(self, request: BusquedaProductoRequestDTO) -> CriteriosBusqueda:
        """Convierte el DTO de request a criterios de dominio"""
        
        # Construir rango de precio
        rango_precio = None
        if request.precio_min is not None or request.precio_max is not None:
            rango_precio = RangoPrecio(
                minimo=request.precio_min,
                maximo=request.precio_max
            )
        
        # Construir rango de largo
        rango_largo = None
        if request.largo_min is not None or request.largo_max is not None:
            rango_largo = RangoLargo(
                minimo=request.largo_min,
                maximo=request.largo_max
            )
        
        # Construir filtros
        filtros = FiltrosProducto(
            texto_busqueda=request.q,
            colores=frozenset(request.colores) if request.colores else None,
            tipos=frozenset(request.tipos) if request.tipos else None,
            largos=frozenset(request.largos) if request.largos else None,
            origenes=frozenset(request.origenes) if request.origenes else None,
            metodos=frozenset(request.metodos) if request.metodos else None,
            calidades=frozenset(request.calidades) if request.calidades else None,
            rango_precio=rango_precio,
            rango_largo=rango_largo,
            solo_disponibles=request.solo_disponibles,
            solo_con_stock=request.solo_con_stock,
            categoria_id=request.categoria
        )
        
        return CriteriosBusqueda(
            filtros=filtros,
            orden=request.orden,
            pagina=request.pagina,
            por_pagina=request.por_pagina
        )
    
    def _calcular_facetas(self, request: BusquedaProductoRequestDTO) -> List[GrupoFacetasDTO]:
        """Calcula las facetas disponibles para los filtros actuales"""
        facetas = []
        
        # Obtener contadores del repositorio
        contadores = self._repo.obtener_contadores_facetas(
            texto=request.q,
            solo_disponibles=request.solo_disponibles,
            solo_con_stock=request.solo_con_stock
        )
        
        # Faceta de Colores
        if 'colores' in contadores:
            facetas.append(GrupoFacetasDTO(
                nombre="Color",
                clave="colores",
                tipo="checkbox",
                opciones=[
                    FacetaDTO(
                        valor=color,
                        etiqueta=self._etiqueta_color(color),
                        cantidad=cantidad,
                        seleccionado=request.colores and color in [c.value for c in request.colores]
                    )
                    for color, cantidad in contadores['colores'].items()
                    if cantidad > 0
                ]
            ))
        
        # Faceta de Tipos
        if 'tipos' in contadores:
            facetas.append(GrupoFacetasDTO(
                nombre="Tipo de Cabello",
                clave="tipos",
                tipo="checkbox",
                opciones=[
                    FacetaDTO(
                        valor=tipo,
                        etiqueta=self._etiqueta_tipo(tipo),
                        cantidad=cantidad,
                        seleccionado=request.tipos and tipo in [t.value for t in request.tipos]
                    )
                    for tipo, cantidad in contadores['tipos'].items()
                    if cantidad > 0
                ]
            ))
        
        # Faceta de Largos
        if 'largos' in contadores:
            facetas.append(GrupoFacetasDTO(
                nombre="Largo",
                clave="largos",
                tipo="checkbox",
                opciones=[
                    FacetaDTO(
                        valor=largo,
                        etiqueta=f'{largo}"',
                        cantidad=cantidad,
                        seleccionado=request.largos and largo in [l.value for l in request.largos]
                    )
                    for largo, cantidad in sorted(contadores['largos'].items(), key=lambda x: int(x[0]))
                    if cantidad > 0
                ]
            ))
        
        # Faceta de Origen
        if 'origenes' in contadores:
            facetas.append(GrupoFacetasDTO(
                nombre="Origen",
                clave="origenes",
                tipo="checkbox",
                opciones=[
                    FacetaDTO(
                        valor=origen,
                        etiqueta=self._etiqueta_origen(origen),
                        cantidad=cantidad,
                        seleccionado=request.origenes and origen in [o.value for o in request.origenes]
                    )
                    for origen, cantidad in contadores['origenes'].items()
                    if cantidad > 0
                ]
            ))
        
        # Faceta de Método
        if 'metodos' in contadores:
            facetas.append(GrupoFacetasDTO(
                nombre="Método de Aplicación",
                clave="metodos",
                tipo="checkbox",
                opciones=[
                    FacetaDTO(
                        valor=metodo,
                        etiqueta=self._etiqueta_metodo(metodo),
                        cantidad=cantidad,
                        seleccionado=request.metodos and metodo in [m.value for m in request.metodos]
                    )
                    for metodo, cantidad in contadores['metodos'].items()
                    if cantidad > 0
                ]
            ))
        
        # Faceta de Calidad
        if 'calidades' in contadores:
            facetas.append(GrupoFacetasDTO(
                nombre="Calidad",
                clave="calidades",
                tipo="checkbox",
                opciones=[
                    FacetaDTO(
                        valor=calidad,
                        etiqueta=calidad.replace('_', ' ').title(),
                        cantidad=cantidad,
                        seleccionado=request.calidades and calidad in [c.value for c in request.calidades]
                    )
                    for calidad, cantidad in contadores['calidades'].items()
                    if cantidad > 0
                ]
            ))
        
        # Faceta de Precio (rango)
        if 'precio' in contadores:
            facetas.append(GrupoFacetasDTO(
                nombre="Precio",
                clave="precio",
                tipo="range",
                opciones=[],
                rango_min=contadores['precio']['min'],
                rango_max=contadores['precio']['max'],
                valor_min_seleccionado=request.precio_min,
                valor_max_seleccionado=request.precio_max
            ))
        
        return facetas
    
    def _mapear_productos(self, productos: List) -> List[ProductoBusquedaDTO]:
        """Mapea entidades de dominio a DTOs de respuesta"""
        return [
            ProductoBusquedaDTO(
                id=p.id,
                codigo=p.codigo.valor if hasattr(p.codigo, 'valor') else str(p.codigo),
                nombre=p.nombre,
                descripcion_corta=p.descripcion[:150] if p.descripcion else '',
                precio=p.precio.monto if hasattr(p.precio, 'monto') else p.precio,
                precio_original=getattr(p, 'precio_original', None),
                moneda=p.precio.moneda if hasattr(p.precio, 'moneda') else 'USD',
                color=getattr(p, 'color', None),
                tipo=getattr(p, 'tipo', None),
                largo=getattr(p, 'largo', None),
                origen=getattr(p, 'origen', None),
                metodo=getattr(p, 'metodo', None),
                calidad=getattr(p, 'calidad', None),
                disponible=p.disponible,
                stock_disponible=p.stock_actual,
                imagen_principal=getattr(p, 'imagen_principal', None),
                valoracion_promedio=getattr(p, 'valoracion_promedio', None),
                total_valoraciones=getattr(p, 'total_valoraciones', 0),
                es_nuevo=getattr(p, 'es_nuevo', False),
                tiene_descuento=getattr(p, 'tiene_descuento', False),
                porcentaje_descuento=getattr(p, 'porcentaje_descuento', None)
            )
            for p in productos
        ]
    
    def _construir_paginacion(self, request: BusquedaProductoRequestDTO, total: int) -> PaginacionDTO:
        """Construye información de paginación"""
        total_paginas = (total + request.por_pagina - 1) // request.por_pagina if total > 0 else 0
        
        return PaginacionDTO(
            pagina_actual=request.pagina,
            por_pagina=request.por_pagina,
            total_resultados=total,
            total_paginas=total_paginas,
            tiene_siguiente=request.pagina < total_paginas,
            tiene_anterior=request.pagina > 1
        )
    
    def _extraer_filtros_aplicados(self, request: BusquedaProductoRequestDTO) -> dict:
        """Extrae los filtros actualmente aplicados para mostrar en UI"""
        filtros = {}
        
        if request.q:
            filtros['busqueda'] = request.q
        if request.colores:
            filtros['colores'] = [c.value for c in request.colores]
        if request.tipos:
            filtros['tipos'] = [t.value for t in request.tipos]
        if request.largos:
            filtros['largos'] = [l.value for l in request.largos]
        if request.origenes:
            filtros['origenes'] = [o.value for o in request.origenes]
        if request.metodos:
            filtros['metodos'] = [m.value for m in request.metodos]
        if request.calidades:
            filtros['calidades'] = [c.value for c in request.calidades]
        if request.precio_min:
            filtros['precio_min'] = float(request.precio_min)
        if request.precio_max:
            filtros['precio_max'] = float(request.precio_max)
        
        return filtros
    
    def _opciones_orden(self) -> List[dict]:
        """Retorna las opciones de ordenamiento disponibles"""
        return [
            {"valor": "relevancia", "etiqueta": "Más Relevantes"},
            {"valor": "precio_asc", "etiqueta": "Precio: Menor a Mayor"},
            {"valor": "precio_desc", "etiqueta": "Precio: Mayor a Menor"},
            {"valor": "mas_vendidos", "etiqueta": "Más Vendidos"},
            {"valor": "mejor_valorados", "etiqueta": "Mejor Valorados"},
            {"valor": "mas_recientes", "etiqueta": "Más Recientes"},
        ]
    
    # Helpers para etiquetas legibles
    def _etiqueta_color(self, valor: str) -> str:
        return valor.replace('_', ' ').title()
    
    def _etiqueta_tipo(self, valor: str) -> str:
        return valor.replace('_', ' ').title()
    
    def _etiqueta_origen(self, valor: str) -> str:
        return valor.replace('_', ' ').title()
    
    def _etiqueta_metodo(self, valor: str) -> str:
        return valor.replace('_', '-').title()


class AutocompletarBusquedaUseCase(CasoUsoBase[str, AutocompletadoResponseDTO]):
    """
    Caso de uso: Autocompletado de búsqueda.
    
    Retorna sugerencias mientras el usuario escribe.
    """
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
    
    def ejecutar(self, texto: str) -> AutocompletadoResponseDTO:
        if not texto or len(texto) < 2:
            return AutocompletadoResponseDTO()
        
        # Obtener sugerencias del repositorio
        sugerencias = self._repo.obtener_sugerencias_busqueda(texto, limite=8)
        productos_rapidos = self._repo.buscar_productos_rapido(texto, limite=4)
        
        return AutocompletadoResponseDTO(
            sugerencias=[
                SugerenciaBusquedaDTO(
                    texto=s['texto'],
                    tipo=s.get('tipo', 'busqueda'),
                    destacado=s.get('destacado'),
                    metadata=s.get('metadata', {})
                )
                for s in sugerencias
            ],
            productos_rapidos=[
                ProductoBusquedaDTO(
                    id=p.id,
                    codigo=p.codigo.valor if hasattr(p.codigo, 'valor') else str(p.codigo),
                    nombre=p.nombre,
                    descripcion_corta=p.descripcion[:150] if p.descripcion else '',
                    precio=p.precio.monto if hasattr(p.precio, 'monto') else p.precio,
                    moneda='USD',
                    disponible=p.disponible,
                    stock_disponible=p.stock_actual,
                    imagen_principal=getattr(p, 'imagen_principal', None),
                )
                for p in productos_rapidos
            ]
        )


class ObtenerProductosDestacadosUseCase(CasoUsoBase[int, List[ProductoBusquedaDTO]]):
    """
    Caso de uso: Obtener productos destacados para homepage.
    """
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
    
    def ejecutar(self, limite: int = 8) -> List[ProductoBusquedaDTO]:
        productos = self._repo.obtener_destacados(limite)
        
        return [
            ProductoBusquedaDTO(
                id=p.id,
                codigo=p.codigo.valor if hasattr(p.codigo, 'valor') else str(p.codigo),
                nombre=p.nombre,
                descripcion_corta=p.descripcion[:150] if p.descripcion else '',
                precio=p.precio.monto if hasattr(p.precio, 'monto') else p.precio,
                moneda='USD',
                disponible=p.disponible,
                stock_disponible=p.stock_actual,
                imagen_principal=getattr(p, 'imagen_principal', None),
                es_nuevo=getattr(p, 'es_nuevo', False),
            )
            for p in productos
        ]


class ObtenerProductosMasVendidosUseCase(CasoUsoBase[int, List[ProductoBusquedaDTO]]):
    """
    Caso de uso: Obtener productos más vendidos.
    """
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
    
    def ejecutar(self, limite: int = 8) -> List[ProductoBusquedaDTO]:
        productos = self._repo.obtener_mas_vendidos(limite)
        
        return [
            ProductoBusquedaDTO(
                id=p.id,
                codigo=p.codigo.valor if hasattr(p.codigo, 'valor') else str(p.codigo),
                nombre=p.nombre,
                descripcion_corta=p.descripcion[:150] if p.descripcion else '',
                precio=p.precio.monto if hasattr(p.precio, 'monto') else p.precio,
                moneda='USD',
                disponible=p.disponible,
                stock_disponible=p.stock_actual,
                imagen_principal=getattr(p, 'imagen_principal', None),
                total_valoraciones=getattr(p, 'total_valoraciones', 0),
            )
            for p in productos
        ]
