"""
DTOs para Búsqueda y Filtros de Productos

Application Layer - Objetos de transferencia de datos.

Estos DTOs definen el contrato de entrada/salida para la API,
separando la interfaz externa del dominio interno.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Any
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from enum import Enum

from shared.enums.atributos_producto import (
    ColorCabello,
    TipoCabello,
    LargoCabello,
    OrigenCabello,
    MetodoAplicacion,
    CalidadCabello,
    OrdenProducto
)


# ===== REQUEST DTOs (Entrada) =====

class BusquedaProductoRequestDTO(BaseModel):
    """
    DTO de entrada para búsqueda de productos.
    
    Todos los campos son opcionales para permitir búsquedas flexibles.
    """
    # Texto libre
    q: Optional[str] = Field(None, description="Texto de búsqueda", max_length=200)
    
    # Filtros por atributos
    colores: Optional[List[ColorCabello]] = Field(None, description="Filtrar por colores")
    tipos: Optional[List[TipoCabello]] = Field(None, description="Filtrar por tipo de cabello")
    largos: Optional[List[LargoCabello]] = Field(None, description="Filtrar por largo")
    origenes: Optional[List[OrigenCabello]] = Field(None, description="Filtrar por origen")
    metodos: Optional[List[MetodoAplicacion]] = Field(None, description="Filtrar por método de aplicación")
    calidades: Optional[List[CalidadCabello]] = Field(None, description="Filtrar por calidad")
    
    # Rangos
    precio_min: Optional[Decimal] = Field(None, ge=0, description="Precio mínimo")
    precio_max: Optional[Decimal] = Field(None, ge=0, description="Precio máximo")
    largo_min: Optional[int] = Field(None, ge=0, description="Largo mínimo en pulgadas")
    largo_max: Optional[int] = Field(None, le=50, description="Largo máximo en pulgadas")
    
    # Disponibilidad
    solo_disponibles: bool = Field(True, description="Solo productos activos")
    solo_con_stock: bool = Field(True, description="Solo productos con stock")
    
    # Categoría
    categoria: Optional[str] = Field(None, description="ID o slug de categoría")
    
    # Ordenamiento
    orden: OrdenProducto = Field(OrdenProducto.RELEVANCIA, description="Criterio de ordenamiento")
    
    # Paginación
    pagina: int = Field(1, ge=1, description="Número de página")
    por_pagina: int = Field(20, ge=1, le=100, description="Resultados por página")
    
    @field_validator('precio_max')
    @classmethod
    def validar_rango_precio(cls, v, info):
        if v is not None and info.data.get('precio_min') is not None:
            if v < info.data['precio_min']:
                raise ValueError('precio_max debe ser mayor o igual a precio_min')
        return v
    
    class Config:
        use_enum_values = True


class FiltrosRapidosDTO(BaseModel):
    """
    DTO para filtros rápidos predefinidos.
    
    Usado para botones de acceso rápido en UI.
    """
    filtro: str = Field(..., description="Identificador del filtro rápido")
    # Opciones: "ofertas", "nuevos", "mas_vendidos", "mejor_valorados"


# ===== RESPONSE DTOs (Salida) =====

class ProductoBusquedaDTO(BaseModel):
    """
    DTO de producto para resultados de búsqueda.
    
    Versión ligera del producto con solo datos necesarios para listado.
    """
    id: UUID
    codigo: str
    nombre: str
    descripcion_corta: str = Field(..., max_length=150)
    
    # Precio
    precio: Decimal
    precio_original: Optional[Decimal] = None  # Para mostrar descuento
    moneda: str = "USD"
    
    # Atributos de cabello
    color: Optional[ColorCabello] = None
    tipo: Optional[TipoCabello] = None
    largo: Optional[LargoCabello] = None
    origen: Optional[OrigenCabello] = None
    metodo: Optional[MetodoAplicacion] = None
    calidad: Optional[CalidadCabello] = None
    
    # Disponibilidad
    disponible: bool
    stock_disponible: int
    
    # Imágenes
    imagen_principal: Optional[str] = None
    imagenes_miniatura: List[str] = Field(default_factory=list)
    
    # Valoraciones
    valoracion_promedio: Optional[float] = None
    total_valoraciones: int = 0
    
    # Metadata
    es_nuevo: bool = False
    tiene_descuento: bool = False
    porcentaje_descuento: Optional[int] = None
    
    class Config:
        from_attributes = True


class FacetaDTO(BaseModel):
    """
    DTO para una opción de faceta individual.
    """
    valor: str = Field(..., description="Valor interno para filtrado")
    etiqueta: str = Field(..., description="Etiqueta para mostrar al usuario")
    cantidad: int = Field(..., ge=0, description="Cantidad de productos")
    seleccionado: bool = Field(False, description="Si está actualmente seleccionado")


class GrupoFacetasDTO(BaseModel):
    """
    DTO para un grupo de facetas.
    """
    nombre: str = Field(..., description="Nombre del grupo para mostrar")
    clave: str = Field(..., description="Clave para identificar en la API")
    tipo: str = Field("checkbox", description="Tipo de UI: checkbox, radio, range")
    opciones: List[FacetaDTO] = Field(default_factory=list)
    
    # Para rangos (precio, largo)
    rango_min: Optional[Decimal] = None
    rango_max: Optional[Decimal] = None
    valor_min_seleccionado: Optional[Decimal] = None
    valor_max_seleccionado: Optional[Decimal] = None


class PaginacionDTO(BaseModel):
    """
    DTO con información de paginación.
    """
    pagina_actual: int
    por_pagina: int
    total_resultados: int
    total_paginas: int
    tiene_siguiente: bool
    tiene_anterior: bool
    
    # Para paginación cursor-based (futuro)
    cursor_siguiente: Optional[str] = None
    cursor_anterior: Optional[str] = None


class ResultadoBusquedaDTO(BaseModel):
    """
    DTO principal de respuesta de búsqueda.
    
    Incluye productos, facetas, paginación y metadata.
    """
    # Resultados
    productos: List[ProductoBusquedaDTO] = Field(default_factory=list)
    
    # Facetas para filtrado
    facetas: List[GrupoFacetasDTO] = Field(default_factory=list)
    
    # Paginación
    paginacion: PaginacionDTO
    
    # Metadata
    query_original: Optional[str] = None
    tiempo_busqueda_ms: int = 0
    filtros_aplicados: dict = Field(default_factory=dict)
    
    # Sugerencias
    terminos_sugeridos: List[str] = Field(default_factory=list)
    productos_sugeridos: List[ProductoBusquedaDTO] = Field(default_factory=list)
    
    # Ordenamiento actual
    orden_actual: OrdenProducto = OrdenProducto.RELEVANCIA
    opciones_orden: List[dict] = Field(default_factory=list)
    
    @classmethod
    def vacio(cls, request: BusquedaProductoRequestDTO) -> 'ResultadoBusquedaDTO':
        """Crea un resultado vacío"""
        return cls(
            productos=[],
            facetas=[],
            paginacion=PaginacionDTO(
                pagina_actual=request.pagina,
                por_pagina=request.por_pagina,
                total_resultados=0,
                total_paginas=0,
                tiene_siguiente=False,
                tiene_anterior=False,
            ),
            query_original=request.q,
            orden_actual=request.orden,
            opciones_orden=[
                {"valor": o.value, "etiqueta": o.value.replace("_", " ").title()}
                for o in OrdenProducto
            ]
        )


class SugerenciaBusquedaDTO(BaseModel):
    """
    DTO para sugerencias de autocompletado.
    """
    texto: str
    tipo: str  # "producto", "categoria", "marca", "busqueda_reciente"
    destacado: Optional[str] = None  # Texto con match resaltado
    metadata: dict = Field(default_factory=dict)


class AutocompletadoResponseDTO(BaseModel):
    """
    DTO de respuesta para autocompletado.
    """
    sugerencias: List[SugerenciaBusquedaDTO] = Field(default_factory=list)
    productos_rapidos: List[ProductoBusquedaDTO] = Field(default_factory=list, max_length=4)
