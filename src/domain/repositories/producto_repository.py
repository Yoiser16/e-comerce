"""
Interfaz del Repositorio de Producto
"""
from abc import abstractmethod
from typing import Optional, List, Tuple, Dict, Any
from .base import RepositorioBase
from ..entities.producto import Producto
from ..value_objects.codigo_producto import CodigoProducto


class ProductoRepository(RepositorioBase[Producto]):
    """
    Contrato de persistencia para Producto.
    
    Punto de extensión: consultas de inventario, búsquedas
    """
    
    @abstractmethod
    def obtener_por_codigo(self, codigo: CodigoProducto) -> Optional[Producto]:
        """Busca un producto por código"""
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        """Busca productos por nombre (búsqueda parcial)"""
        pass
    
    @abstractmethod
    def obtener_con_stock_bajo(self) -> List[Producto]:
        """Obtiene productos que requieren reabastecimiento"""
        pass
    
    @abstractmethod
    def obtener_disponibles(self) -> List[Producto]:
        """Obtiene productos disponibles para venta"""
        pass
    
    @abstractmethod
    def obtener_con_bloqueo(self, id) -> Optional[Producto]:
        """
        Obtiene un producto con bloqueo pesimista (SELECT FOR UPDATE).
        
        IMPORTANTE: Debe ejecutarse dentro de transaction.atomic()
        para evitar bloqueos perpetuos.
        
        Uso: Control de concurrencia en operaciones críticas de stock.
        """
        pass
    
    # ===== MÉTODOS DE BÚSQUEDA AVANZADA =====
    
    @abstractmethod
    def buscar_con_filtros(self, criterios: Any) -> Tuple[List[Producto], int]:
        """
        Busca productos aplicando filtros avanzados.
        
        Args:
            criterios: CriteriosBusqueda con filtros, ordenamiento y paginación
            
        Returns:
            Tupla de (lista de productos, total sin paginar)
        """
        pass
    
    @abstractmethod
    def obtener_contadores_facetas(
        self,
        texto: Optional[str] = None,
        solo_disponibles: bool = True,
        solo_con_stock: bool = True
    ) -> Dict[str, Any]:
        """
        Obtiene contadores para facetas de filtrado.
        
        Returns:
            Dict con contadores por atributo:
            {
                'colores': {'negro_natural': 15, 'rubio': 10, ...},
                'tipos': {'liso': 20, 'ondulado': 8, ...},
                'largos': {'16': 12, '18': 8, ...},
                'origenes': {'brasileno': 25, ...},
                'metodos': {'clip_in': 30, ...},
                'calidades': {'virgin': 20, ...},
                'precio': {'min': 50.00, 'max': 500.00}
            }
        """
        pass
    
    @abstractmethod
    def obtener_sugerencias_busqueda(self, texto: str, limite: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene sugerencias para autocompletado.
        
        Returns:
            Lista de sugerencias con texto, tipo y metadata
        """
        pass
    
    @abstractmethod
    def buscar_productos_rapido(self, texto: str, limite: int = 4) -> List[Producto]:
        """
        Búsqueda rápida de productos para autocompletado.
        
        Retorna pocos resultados optimizados para UI.
        """
        pass
    
    @abstractmethod
    def obtener_destacados(self, limite: int = 8) -> List[Producto]:
        """Obtiene productos marcados como destacados"""
        pass
    
    @abstractmethod
    def obtener_mas_vendidos(self, limite: int = 8) -> List[Producto]:
        """Obtiene productos más vendidos"""
        pass
    
    @abstractmethod
    def obtener_nuevos(self, limite: int = 8) -> List[Producto]:
        """Obtiene productos más recientes"""
        pass
    
    @abstractmethod
    def obtener_todos(self, limite: int = 100, offset: int = 0) -> List[Producto]:
        """Obtiene TODOS los productos (incluyendo inactivos) para administración"""
        pass
