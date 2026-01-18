"""
Router de Búsqueda y Filtros de Productos - FastAPI

Interfaces Layer - Endpoints de búsqueda avanzada.

Endpoints:
- GET /api/v1/productos/buscar - Búsqueda con filtros
- GET /api/v1/productos/autocompletar - Autocompletado
- GET /api/v1/productos/facetas - Obtener facetas
- GET /api/v1/productos/destacados - Productos destacados
- GET /api/v1/productos/mas-vendidos - Más vendidos
- GET /api/v1/productos/nuevos - Productos nuevos
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from decimal import Decimal

from .dependencies import get_producto_repository
from domain.repositories.producto_repository import ProductoRepository

from application.use_cases.busqueda_use_cases import (
    BuscarProductosUseCase,
    AutocompletarBusquedaUseCase,
    ObtenerProductosDestacadosUseCase,
    ObtenerProductosMasVendidosUseCase
)
from application.dto.busqueda_dto import (
    BusquedaProductoRequestDTO,
    ResultadoBusquedaDTO,
    AutocompletadoResponseDTO,
    ProductoBusquedaDTO,
    GrupoFacetasDTO
)
from shared.enums.atributos_producto import (
    ColorCabello,
    TipoCabello,
    LargoCabello,
    OrigenCabello,
    MetodoAplicacion,
    CalidadCabello,
    OrdenProducto
)

router = APIRouter(prefix="/api/v1/productos", tags=["busqueda"])


# ===== BÚSQUEDA PRINCIPAL =====

@router.get("/buscar", response_model=ResultadoBusquedaDTO)
def buscar_productos(
    # Texto libre
    q: Optional[str] = Query(None, description="Texto de búsqueda", max_length=200),
    
    # Filtros por atributos
    colores: Optional[List[ColorCabello]] = Query(None, description="Filtrar por colores"),
    tipos: Optional[List[TipoCabello]] = Query(None, description="Filtrar por tipo de cabello"),
    largos: Optional[List[LargoCabello]] = Query(None, description="Filtrar por largo"),
    origenes: Optional[List[OrigenCabello]] = Query(None, description="Filtrar por origen"),
    metodos: Optional[List[MetodoAplicacion]] = Query(None, description="Filtrar por método"),
    calidades: Optional[List[CalidadCabello]] = Query(None, description="Filtrar por calidad"),
    
    # Rangos
    precio_min: Optional[Decimal] = Query(None, ge=0, description="Precio mínimo"),
    precio_max: Optional[Decimal] = Query(None, ge=0, description="Precio máximo"),
    largo_min: Optional[int] = Query(None, ge=8, le=32, description="Largo mínimo"),
    largo_max: Optional[int] = Query(None, ge=8, le=32, description="Largo máximo"),
    
    # Disponibilidad
    solo_disponibles: bool = Query(True, description="Solo productos activos"),
    solo_con_stock: bool = Query(True, description="Solo productos con stock"),
    
    # Ordenamiento
    orden: OrdenProducto = Query(OrdenProducto.RELEVANCIA, description="Ordenar por"),
    
    # Paginación
    pagina: int = Query(1, ge=1, description="Página"),
    por_pagina: int = Query(20, ge=1, le=100, description="Resultados por página"),
    
    # Repositorio
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Búsqueda avanzada de productos con filtros múltiples.
    
    Soporta:
    - Búsqueda por texto en nombre y descripción
    - Filtros por atributos de cabello (color, tipo, largo, etc.)
    - Rango de precios
    - Ordenamiento múltiple
    - Paginación
    - Facetas dinámicas con contadores
    
    Ejemplo:
    ```
    /api/v1/productos/buscar?q=brasileño&colores=negro_natural&largos=18&precio_max=200
    ```
    """
    try:
        # Construir DTO de request
        request = BusquedaProductoRequestDTO(
            q=q,
            colores=colores,
            tipos=tipos,
            largos=largos,
            origenes=origenes,
            metodos=metodos,
            calidades=calidades,
            precio_min=precio_min,
            precio_max=precio_max,
            largo_min=largo_min,
            largo_max=largo_max,
            solo_disponibles=solo_disponibles,
            solo_con_stock=solo_con_stock,
            orden=orden,
            pagina=pagina,
            por_pagina=por_pagina
        )
        
        use_case = BuscarProductosUseCase(repo)
        return use_case.ejecutar(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== AUTOCOMPLETADO =====

@router.get("/autocompletar", response_model=AutocompletadoResponseDTO)
def autocompletar_busqueda(
    q: str = Query(..., min_length=2, max_length=100, description="Texto a autocompletar"),
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Autocompletado de búsqueda mientras el usuario escribe.
    
    Retorna:
    - Sugerencias de búsqueda (nombres, categorías)
    - Vista previa de 4 productos relevantes
    
    Optimizado para respuesta rápida (<100ms).
    """
    try:
        use_case = AutocompletarBusquedaUseCase(repo)
        return use_case.ejecutar(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== FACETAS =====

@router.get("/facetas", response_model=List[GrupoFacetasDTO])
def obtener_facetas(
    q: Optional[str] = Query(None, description="Texto de búsqueda para contextualizar"),
    solo_disponibles: bool = Query(True),
    solo_con_stock: bool = Query(True),
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Obtiene las facetas disponibles con contadores.
    
    Útil para construir UI de filtros con cantidad de productos por opción.
    
    Retorna grupos de facetas:
    - Colores (con cantidad de productos por color)
    - Tipos de cabello
    - Largos disponibles
    - Orígenes
    - Métodos de aplicación
    - Calidades
    - Rango de precios (min/max)
    """
    try:
        contadores = repo.obtener_contadores_facetas(
            texto=q,
            solo_disponibles=solo_disponibles,
            solo_con_stock=solo_con_stock
        )
        
        # Construir respuesta de facetas
        facetas = []
        
        if contadores.get('colores'):
            facetas.append(GrupoFacetasDTO(
                nombre="Color",
                clave="colores",
                tipo="checkbox",
                opciones=[
                    {"valor": k, "etiqueta": k.replace('_', ' ').title(), "cantidad": v, "seleccionado": False}
                    for k, v in contadores['colores'].items() if v > 0
                ]
            ))
        
        if contadores.get('tipos'):
            facetas.append(GrupoFacetasDTO(
                nombre="Tipo de Cabello",
                clave="tipos",
                tipo="checkbox",
                opciones=[
                    {"valor": k, "etiqueta": k.replace('_', ' ').title(), "cantidad": v, "seleccionado": False}
                    for k, v in contadores['tipos'].items() if v > 0
                ]
            ))
        
        if contadores.get('largos'):
            facetas.append(GrupoFacetasDTO(
                nombre="Largo",
                clave="largos",
                tipo="checkbox",
                opciones=[
                    {"valor": k, "etiqueta": f'{k}"', "cantidad": v, "seleccionado": False}
                    for k, v in sorted(contadores['largos'].items(), key=lambda x: int(x[0])) if v > 0
                ]
            ))
        
        if contadores.get('origenes'):
            facetas.append(GrupoFacetasDTO(
                nombre="Origen",
                clave="origenes",
                tipo="checkbox",
                opciones=[
                    {"valor": k, "etiqueta": k.title(), "cantidad": v, "seleccionado": False}
                    for k, v in contadores['origenes'].items() if v > 0
                ]
            ))
        
        if contadores.get('metodos'):
            facetas.append(GrupoFacetasDTO(
                nombre="Método de Aplicación",
                clave="metodos",
                tipo="checkbox",
                opciones=[
                    {"valor": k, "etiqueta": k.replace('_', '-').title(), "cantidad": v, "seleccionado": False}
                    for k, v in contadores['metodos'].items() if v > 0
                ]
            ))
        
        if contadores.get('calidades'):
            facetas.append(GrupoFacetasDTO(
                nombre="Calidad",
                clave="calidades",
                tipo="checkbox",
                opciones=[
                    {"valor": k, "etiqueta": k.replace('_', ' ').title(), "cantidad": v, "seleccionado": False}
                    for k, v in contadores['calidades'].items() if v > 0
                ]
            ))
        
        if contadores.get('precio'):
            facetas.append(GrupoFacetasDTO(
                nombre="Precio",
                clave="precio",
                tipo="range",
                opciones=[],
                rango_min=contadores['precio']['min'],
                rango_max=contadores['precio']['max']
            ))
        
        return facetas
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== PRODUCTOS DESTACADOS =====

@router.get("/destacados", response_model=List[ProductoBusquedaDTO])
def obtener_productos_destacados(
    limite: int = Query(8, ge=1, le=20, description="Cantidad de productos"),
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Obtiene productos destacados para homepage.
    
    Productos marcados como destacados por el administrador.
    """
    try:
        use_case = ObtenerProductosDestacadosUseCase(repo)
        return use_case.ejecutar(limite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== MÁS VENDIDOS =====

@router.get("/mas-vendidos", response_model=List[ProductoBusquedaDTO])
def obtener_productos_mas_vendidos(
    limite: int = Query(8, ge=1, le=20, description="Cantidad de productos"),
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Obtiene los productos más vendidos.
    
    Ordenados por cantidad total de ventas.
    """
    try:
        use_case = ObtenerProductosMasVendidosUseCase(repo)
        return use_case.ejecutar(limite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== PRODUCTOS NUEVOS =====

@router.get("/nuevos", response_model=List[ProductoBusquedaDTO])
def obtener_productos_nuevos(
    limite: int = Query(8, ge=1, le=20, description="Cantidad de productos"),
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Obtiene los productos más recientes.
    
    Productos marcados como nuevos, ordenados por fecha de creación.
    """
    try:
        productos = repo.obtener_nuevos(limite)
        
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
                es_nuevo=True
            )
            for p in productos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== FILTROS RÁPIDOS =====

@router.get("/filtro-rapido/{filtro}")
def aplicar_filtro_rapido(
    filtro: str,
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1, le=100),
    repo: ProductoRepository = Depends(get_producto_repository)
):
    """
    Aplica un filtro rápido predefinido.
    
    Filtros disponibles:
    - `ofertas`: Productos con descuento
    - `nuevos`: Productos marcados como nuevos
    - `mas-vendidos`: Top productos por ventas
    - `mejor-valorados`: Top productos por valoración
    - `liso`: Cabello liso
    - `ondulado`: Cabello ondulado
    - `rizado`: Cabello rizado
    """
    try:
        filtros_map = {
            'ofertas': {'tiene_descuento': True},
            'nuevos': {'es_nuevo': True},
            'liso': {'tipos': [TipoCabello.LISO]},
            'ondulado': {'tipos': [TipoCabello.ONDULADO]},
            'rizado': {'tipos': [TipoCabello.RIZADO]},
            'brasileno': {'origenes': [OrigenCabello.BRASILENO]},
            'peruano': {'origenes': [OrigenCabello.PERUANO]},
            'indio': {'origenes': [OrigenCabello.INDIO]},
            'virgin': {'calidades': [CalidadCabello.VIRGIN]},
            'remy': {'calidades': [CalidadCabello.REMY]},
        }
        
        if filtro not in filtros_map and filtro not in ['mas-vendidos', 'mejor-valorados']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Filtro '{filtro}' no válido"
            )
        
        # Para filtros especiales, usar use cases dedicados
        if filtro == 'mas-vendidos':
            use_case = ObtenerProductosMasVendidosUseCase(repo)
            return use_case.ejecutar(por_pagina)
        
        # Construir request con el filtro
        request_data = filtros_map.get(filtro, {})
        request = BusquedaProductoRequestDTO(
            pagina=pagina,
            por_pagina=por_pagina,
            **request_data
        )
        
        use_case = BuscarProductosUseCase(repo)
        return use_case.ejecutar(request)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
