"""
Casos de uso relacionados con Producto
"""
from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from application.use_cases.base import CasoUsoBase
from application.dto.producto_dto import CrearProductoDTO, ProductoDTO, ActualizarProductoDTO
from domain.repositories.producto_repository import ProductoRepository
from domain.entities.producto import Producto
from domain.value_objects.codigo_producto import CodigoProducto
from domain.value_objects.dinero import Dinero
from domain.exceptions.dominio import EntidadNoEncontrada, ReglaNegocioViolada


class CrearProductoUseCase(CasoUsoBase[CrearProductoDTO, ProductoDTO]):
    """Caso de uso: Crear un nuevo producto"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
    
    def ejecutar(self, request: CrearProductoDTO) -> ProductoDTO:
        # Validar si ya existe código
        codigo = CodigoProducto(request.codigo)
        if self._repo.obtener_por_codigo(codigo):
            raise ReglaNegocioViolada(f"Ya existe un producto con código {request.codigo}")
            
        producto = Producto(
            codigo=codigo,
            nombre=request.nombre,
            descripcion=request.descripcion,
            precio=Dinero(request.precio_monto, request.precio_moneda),
            stock_actual=request.stock_actual,
            stock_minimo=request.stock_minimo,
            cantidad_minima_mayorista=request.cantidad_minima_mayorista
        )
        
        # Pasar atributos adicionales al repositorio
        atributos_adicionales = {
            'imagen_principal': request.imagen_principal,
            'imagenes': request.imagenes,
            'color': request.color,
            'tipo': request.tipo,
            'largo': request.largo,
            'origen': request.origen,
            'metodo': request.metodo,
            'calidad': request.calidad,
            'destacado': request.destacado,
            'disponible_b2b': request.disponible_b2b,
            'porcentaje_descuento_b2b': request.porcentaje_descuento_b2b,
            'cantidad_minima_mayorista': request.cantidad_minima_mayorista,
            'variantes': request.variantes
        }
        
        guardado = self._repo.guardar(
            producto, 
            categoria_id=request.categoria,
            atributos_adicionales=atributos_adicionales
        )
        return ProductoDTO.desde_entidad(guardado)


class ObtenerProductoUseCase(CasoUsoBase[UUID, ProductoDTO]):
    """Caso de uso: Obtener producto por ID"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
        
    def ejecutar(self, request: UUID) -> ProductoDTO:
        producto = self._repo.obtener_por_id(request)
        if not producto:
            raise EntidadNoEncontrada(f"Producto {request} no encontrado")
        return ProductoDTO.desde_entidad(producto)


class ListarProductosUseCase(CasoUsoBase[None, List[ProductoDTO]]):
    """Caso de uso: Listar productos disponibles"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
        
    def ejecutar(self, request: None = None) -> List[ProductoDTO]:
        productos = self._repo.obtener_disponibles()
        return [ProductoDTO.desde_entidad(p) for p in productos]


class ListarTodosProductosUseCase(CasoUsoBase[dict, List[ProductoDTO]]):
    """Caso de uso: Listar TODOS los productos (para admin)"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
        
    def ejecutar(self, request: dict = None) -> List[ProductoDTO]:
        request = request or {}
        limite = request.get('limite', 100)
        offset = request.get('offset', 0)
        productos = self._repo.obtener_todos(limite=limite, offset=offset)
        return [ProductoDTO.desde_entidad(p) for p in productos]


class ActualizarProductoUseCase(CasoUsoBase[ActualizarProductoDTO, ProductoDTO]):
    """Caso de uso: Actualizar un producto existente"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
    
    def ejecutar(self, request: ActualizarProductoDTO) -> ProductoDTO:
        # Obtener producto existente
        producto = self._repo.obtener_por_id(request.id)
        if not producto:
            raise EntidadNoEncontrada(f"Producto {request.id} no encontrado")
        
        # Actualizar campos si se proporcionaron
        if request.nombre is not None:
            producto.nombre = request.nombre
        if request.descripcion is not None:
            producto.descripcion = request.descripcion
        if request.precio_monto is not None:
            producto.precio = Dinero(request.precio_monto, producto.precio.moneda)
        if request.stock_actual is not None:
            producto.stock_actual = request.stock_actual
        if request.cantidad_minima_mayorista is not None:
            producto.cantidad_minima_mayorista = request.cantidad_minima_mayorista
        
        # Preparar atributos adicionales para actualizar
        atributos_adicionales = {}
        if request.imagen_principal is not None:
            atributos_adicionales['imagen_principal'] = request.imagen_principal
        if request.imagenes is not None:
            atributos_adicionales['imagenes'] = request.imagenes
        if request.color is not None:
            atributos_adicionales['color'] = request.color
        if request.tipo is not None:
            atributos_adicionales['tipo'] = request.tipo
        if request.largo is not None:
            atributos_adicionales['largo'] = request.largo
        if request.origen is not None:
            atributos_adicionales['origen'] = request.origen
        if request.metodo is not None:
            atributos_adicionales['metodo'] = request.metodo
        if request.calidad is not None:
            atributos_adicionales['calidad'] = request.calidad
        if request.stock_minimo is not None:
            producto.stock_minimo = request.stock_minimo
        if request.activo is not None:
            producto.activo = request.activo
        if request.destacado is not None:
            atributos_adicionales['destacado'] = request.destacado
        if request.disponible_b2b is not None:
            atributos_adicionales['disponible_b2b'] = request.disponible_b2b
        if request.porcentaje_descuento_b2b is not None:
            atributos_adicionales['porcentaje_descuento_b2b'] = request.porcentaje_descuento_b2b
        if request.cantidad_minima_mayorista is not None:
            atributos_adicionales['cantidad_minima_mayorista'] = request.cantidad_minima_mayorista
        if request.variantes is not None:
            atributos_adicionales['variantes'] = request.variantes
        
        # Guardar y pasar la categoría y atributos adicionales al repositorio
        guardado = self._repo.guardar(
            producto, 
            categoria_id=request.categoria,
            atributos_adicionales=atributos_adicionales if atributos_adicionales else None
        )
        return ProductoDTO.desde_entidad(guardado)


class EliminarProductoUseCase(CasoUsoBase[UUID, bool]):
    """Caso de uso: Eliminar (desactivar) un producto"""
    
    def __init__(self, producto_repository: ProductoRepository):
        self._repo = producto_repository
    
    def ejecutar(self, request: UUID) -> bool:
        producto = self._repo.obtener_por_id(request)
        if not producto:
            raise EntidadNoEncontrada(f"Producto {request} no encontrado")
        
        return self._repo.eliminar(request)
