"""
Value Objects para Búsqueda y Filtros de Productos

Domain Layer - Objetos de valor inmutables.

Encapsulan los criterios de búsqueda como objetos de dominio,
independientes de la capa de presentación.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Set
from decimal import Decimal

from shared.enums.atributos_producto import (
    ColorCabello,
    TipoCabello,
    LargoCabello,
    OrigenCabello,
    MetodoAplicacion,
    CalidadCabello,
    OrdenProducto
)


@dataclass(frozen=True)
class RangoPrecio:
    """
    Rango de precios para filtrado.
    
    Inmutable y validado en construcción.
    """
    minimo: Optional[Decimal] = None
    maximo: Optional[Decimal] = None
    
    def __post_init__(self):
        if self.minimo is not None and self.minimo < 0:
            raise ValueError("El precio mínimo no puede ser negativo")
        if self.maximo is not None and self.maximo < 0:
            raise ValueError("El precio máximo no puede ser negativo")
        if self.minimo is not None and self.maximo is not None:
            if self.minimo > self.maximo:
                raise ValueError("El precio mínimo no puede ser mayor al máximo")
    
    @property
    def esta_definido(self) -> bool:
        """Indica si al menos un límite está definido"""
        return self.minimo is not None or self.maximo is not None
    
    def contiene(self, precio: Decimal) -> bool:
        """Verifica si un precio está dentro del rango"""
        if self.minimo is not None and precio < self.minimo:
            return False
        if self.maximo is not None and precio > self.maximo:
            return False
        return True


@dataclass(frozen=True)
class RangoLargo:
    """
    Rango de largo en pulgadas para filtrado.
    """
    minimo: Optional[int] = None
    maximo: Optional[int] = None
    
    def __post_init__(self):
        if self.minimo is not None and self.minimo < 0:
            raise ValueError("El largo mínimo no puede ser negativo")
        if self.maximo is not None and self.maximo < 0:
            raise ValueError("El largo máximo no puede ser negativo")
        if self.minimo is not None and self.maximo is not None:
            if self.minimo > self.maximo:
                raise ValueError("El largo mínimo no puede ser mayor al máximo")
    
    @property
    def esta_definido(self) -> bool:
        return self.minimo is not None or self.maximo is not None


@dataclass(frozen=True)
class FiltrosProducto:
    """
    Conjunto completo de filtros para búsqueda de productos.
    
    Inmutable - cada modificación crea una nueva instancia.
    Todos los filtros son opcionales (None = sin filtro).
    """
    # Texto libre
    texto_busqueda: Optional[str] = None
    
    # Atributos específicos de cabello
    colores: Optional[frozenset] = None  # frozenset[ColorCabello]
    tipos: Optional[frozenset] = None  # frozenset[TipoCabello]
    largos: Optional[frozenset] = None  # frozenset[LargoCabello]
    origenes: Optional[frozenset] = None  # frozenset[OrigenCabello]
    metodos: Optional[frozenset] = None  # frozenset[MetodoAplicacion]
    calidades: Optional[frozenset] = None  # frozenset[CalidadCabello]
    
    # Rangos
    rango_precio: Optional[RangoPrecio] = None
    rango_largo: Optional[RangoLargo] = None
    
    # Disponibilidad
    solo_disponibles: bool = True
    solo_con_stock: bool = True
    
    # Categoría
    categoria_id: Optional[str] = None
    
    @property
    def tiene_filtros_activos(self) -> bool:
        """Indica si hay al menos un filtro activo"""
        return any([
            self.texto_busqueda,
            self.colores,
            self.tipos,
            self.largos,
            self.origenes,
            self.metodos,
            self.calidades,
            self.rango_precio and self.rango_precio.esta_definido,
            self.rango_largo and self.rango_largo.esta_definido,
            self.categoria_id,
        ])
    
    def con_texto(self, texto: str) -> 'FiltrosProducto':
        """Crea una copia con nuevo texto de búsqueda"""
        return FiltrosProducto(
            texto_busqueda=texto,
            colores=self.colores,
            tipos=self.tipos,
            largos=self.largos,
            origenes=self.origenes,
            metodos=self.metodos,
            calidades=self.calidades,
            rango_precio=self.rango_precio,
            rango_largo=self.rango_largo,
            solo_disponibles=self.solo_disponibles,
            solo_con_stock=self.solo_con_stock,
            categoria_id=self.categoria_id,
        )
    
    def con_colores(self, colores: List[ColorCabello]) -> 'FiltrosProducto':
        """Crea una copia con nuevos colores"""
        return FiltrosProducto(
            texto_busqueda=self.texto_busqueda,
            colores=frozenset(colores) if colores else None,
            tipos=self.tipos,
            largos=self.largos,
            origenes=self.origenes,
            metodos=self.metodos,
            calidades=self.calidades,
            rango_precio=self.rango_precio,
            rango_largo=self.rango_largo,
            solo_disponibles=self.solo_disponibles,
            solo_con_stock=self.solo_con_stock,
            categoria_id=self.categoria_id,
        )


@dataclass(frozen=True)
class CriteriosBusqueda:
    """
    Criterios completos de búsqueda incluyendo paginación y ordenamiento.
    
    Este es el objeto principal que se pasa a los casos de uso.
    """
    filtros: FiltrosProducto = field(default_factory=FiltrosProducto)
    orden: OrdenProducto = OrdenProducto.RELEVANCIA
    
    # Paginación (cursor-based para mejor performance)
    pagina: int = 1
    por_pagina: int = 20
    
    # Límites de seguridad
    MAX_POR_PAGINA: int = field(default=100, init=False)
    
    def __post_init__(self):
        # Validar límites
        if self.pagina < 1:
            object.__setattr__(self, 'pagina', 1)
        if self.por_pagina < 1:
            object.__setattr__(self, 'por_pagina', 20)
        if self.por_pagina > self.MAX_POR_PAGINA:
            object.__setattr__(self, 'por_pagina', self.MAX_POR_PAGINA)
    
    @property
    def offset(self) -> int:
        """Calcula el offset para la consulta"""
        return (self.pagina - 1) * self.por_pagina
    
    @property
    def limit(self) -> int:
        """Alias para por_pagina"""
        return self.por_pagina


@dataclass(frozen=True)
class FacetaContador:
    """
    Representa un valor de faceta con su contador.
    
    Ejemplo: Color "Negro Natural" -> 15 productos
    """
    valor: str
    etiqueta: str
    cantidad: int
    seleccionado: bool = False


@dataclass(frozen=True)
class GrupoFacetas:
    """
    Grupo de facetas para un atributo específico.
    
    Ejemplo: Grupo "Colores" con todas las opciones de color.
    """
    nombre: str
    clave: str  # Para identificar en la URL/API
    valores: tuple  # tuple[FacetaContador]
    
    @property
    def total_productos(self) -> int:
        """Total de productos en todas las facetas"""
        return sum(f.cantidad for f in self.valores)
    
    @property
    def tiene_seleccion(self) -> bool:
        """Indica si hay alguna faceta seleccionada"""
        return any(f.seleccionado for f in self.valores)
