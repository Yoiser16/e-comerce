"""
Casos de Uso del Carrito de Compras

Application Layer - Orquestación de operaciones de negocio.

Todos los casos de uso:
- Validan ownership del usuario
- Delegan lógica de negocio al dominio
- Emiten eventos de dominio
- No contienen lógica de presentación
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from application.use_cases.base import CasoUsoBase
from application.dto.carrito_dto import (
    CrearCarritoDTO,
    AgregarProductoAlCarritoActivoDTO,
    QuitarProductoDTO,
    ActualizarCantidadDTO,
    BloquearCarritoDTO,
    ConfirmarCarritoDTO,
    CarritoDTO,
    CarritoResumenDTO,
    OperacionCarritoResultadoDTO
)
from domain.entities.carrito import Carrito
from domain.repositories.carrito_repository import CarritoRepository
from domain.repositories.producto_repository import ProductoRepository
from domain.value_objects.item_carrito import ItemCarrito
from domain.value_objects.dinero import Dinero
from domain.exceptions.dominio import EntidadNoEncontrada, ReglaNegocioViolada
from shared.enums.estado_carrito import EstadoCarrito


class CrearCarritoUseCase(CasoUsoBase[CrearCarritoDTO, CarritoDTO]):
    """
    Caso de uso: Crear un nuevo carrito para un usuario.
    
    Reglas:
    - Si el usuario ya tiene un carrito activo, retornarlo en lugar de crear uno nuevo
    - Un usuario solo puede tener un carrito activo
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, request: CrearCarritoDTO) -> CarritoDTO:
        # Verificar si ya existe un carrito activo
        carrito_existente = self._repo.obtener_carrito_activo_usuario(request.usuario_id)
        if carrito_existente:
            return CarritoDTO.desde_entidad(carrito_existente)
        
        # Crear nuevo carrito
        carrito = Carrito(usuario_id=request.usuario_id)
        carrito_guardado = self._repo.guardar(carrito)
        
        # TODO: Emitir evento CarritoCreado
        
        return CarritoDTO.desde_entidad(carrito_guardado)


class ObtenerCarritoActivoUseCase(CasoUsoBase[UUID, Optional[CarritoDTO]]):
    """
    Caso de uso: Obtener el carrito activo de un usuario.
    
    Retorna None si no tiene carrito activo.
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, usuario_id: UUID) -> Optional[CarritoDTO]:
        carrito = self._repo.obtener_carrito_activo_usuario(usuario_id)
        if not carrito:
            return None
        return CarritoDTO.desde_entidad(carrito)


class ObtenerOCrearCarritoUseCase(CasoUsoBase[UUID, CarritoDTO]):
    """
    Caso de uso: Obtener carrito activo o crear uno nuevo.
    
    Combina ObtenerCarritoActivo y CrearCarrito para simplificar flujo.
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, usuario_id: UUID) -> CarritoDTO:
        # Intentar obtener carrito activo
        carrito = self._repo.obtener_carrito_activo_usuario(usuario_id)
        
        if not carrito:
            # Crear nuevo carrito
            carrito = Carrito(usuario_id=usuario_id)
            carrito = self._repo.guardar(carrito)
        
        return CarritoDTO.desde_entidad(carrito)


class AgregarProductoAlCarritoUseCase(CasoUsoBase[AgregarProductoAlCarritoActivoDTO, OperacionCarritoResultadoDTO]):
    """
    Caso de uso: Agregar un producto al carrito activo del usuario.
    
    Reglas:
    - Si no existe carrito activo, lo crea
    - Valida que el producto exista y esté disponible
    - Toma snapshot del producto (precio, nombre, SKU)
    - No permite duplicados
    - Cantidad debe ser > 0
    """
    
    def __init__(
        self,
        carrito_repository: CarritoRepository,
        producto_repository: ProductoRepository
    ):
        self._carrito_repo = carrito_repository
        self._producto_repo = producto_repository
    
    def ejecutar(self, request: AgregarProductoAlCarritoActivoDTO) -> OperacionCarritoResultadoDTO:
        # Obtener o crear carrito
        carrito = self._carrito_repo.obtener_carrito_activo_usuario(request.usuario_id)
        if not carrito:
            carrito = Carrito(usuario_id=request.usuario_id)
        
        # Obtener producto
        producto = self._producto_repo.obtener_por_id(request.producto_id)
        if not producto:
            raise EntidadNoEncontrada(f"Producto {request.producto_id} no encontrado")
        
        # Validar disponibilidad
        if not producto.disponible:
            raise ReglaNegocioViolada(f"El producto '{producto.nombre}' no está disponible")
        
        # Validar stock suficiente
        if producto.stock_actual < request.cantidad:
            raise ReglaNegocioViolada(
                f"Stock insuficiente. Disponible: {producto.stock_actual}, Solicitado: {request.cantidad}"
            )
        
        # Crear item con snapshot del producto
        item = ItemCarrito(
            producto_id=producto.id,
            sku=producto.codigo.valor,
            nombre_snapshot=producto.nombre,
            precio_unitario_snapshot=producto.precio,
            cantidad=request.cantidad
        )
        
        # Agregar al carrito
        carrito.agregar_producto(item)
        
        # Guardar
        carrito_guardado = self._carrito_repo.guardar(carrito)
        
        # TODO: Emitir evento ProductoAgregadoAlCarrito
        
        return OperacionCarritoResultadoDTO.exitoso(
            carrito_guardado,
            f"Producto '{producto.nombre}' agregado al carrito"
        )


class QuitarProductoDelCarritoUseCase(CasoUsoBase[QuitarProductoDTO, OperacionCarritoResultadoDTO]):
    """
    Caso de uso: Quitar un producto del carrito.
    
    Valida ownership del carrito con el usuario autenticado.
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, request: QuitarProductoDTO, usuario_id: UUID) -> OperacionCarritoResultadoDTO:
        # Obtener carrito
        carrito = self._repo.obtener_por_id(request.carrito_id)
        if not carrito:
            raise EntidadNoEncontrada(f"Carrito {request.carrito_id} no encontrado")
        
        # Validar ownership
        if carrito.usuario_id != usuario_id:
            raise ReglaNegocioViolada("No tienes permiso para modificar este carrito")
        
        # Quitar producto
        item_eliminado = carrito.quitar_producto(request.producto_id)
        
        # Guardar
        carrito_guardado = self._repo.guardar(carrito)
        
        # TODO: Emitir evento ProductoEliminadoDelCarrito
        
        return OperacionCarritoResultadoDTO.exitoso(
            carrito_guardado,
            f"Producto '{item_eliminado.nombre_snapshot}' eliminado del carrito"
        )


class ActualizarCantidadProductoUseCase(CasoUsoBase[ActualizarCantidadDTO, OperacionCarritoResultadoDTO]):
    """
    Caso de uso: Actualizar la cantidad de un producto en el carrito.
    
    Valida:
    - Ownership del carrito
    - Cantidad > 0
    - Stock disponible
    """
    
    def __init__(
        self,
        carrito_repository: CarritoRepository,
        producto_repository: ProductoRepository
    ):
        self._carrito_repo = carrito_repository
        self._producto_repo = producto_repository
    
    def ejecutar(self, request: ActualizarCantidadDTO, usuario_id: UUID) -> OperacionCarritoResultadoDTO:
        # Obtener carrito
        carrito = self._carrito_repo.obtener_por_id(request.carrito_id)
        if not carrito:
            raise EntidadNoEncontrada(f"Carrito {request.carrito_id} no encontrado")
        
        # Validar ownership
        if carrito.usuario_id != usuario_id:
            raise ReglaNegocioViolada("No tienes permiso para modificar este carrito")
        
        # Validar stock disponible
        producto = self._producto_repo.obtener_por_id(request.producto_id)
        if producto and producto.stock_actual < request.nueva_cantidad:
            raise ReglaNegocioViolada(
                f"Stock insuficiente. Disponible: {producto.stock_actual}"
            )
        
        # Actualizar cantidad
        carrito.actualizar_cantidad(request.producto_id, request.nueva_cantidad)
        
        # Guardar
        carrito_guardado = self._carrito_repo.guardar(carrito)
        
        # TODO: Emitir evento CantidadProductoActualizada
        
        return OperacionCarritoResultadoDTO.exitoso(
            carrito_guardado,
            f"Cantidad actualizada a {request.nueva_cantidad}"
        )


class RecalcularCarritoUseCase(CasoUsoBase[UUID, CarritoDTO]):
    """
    Caso de uso: Recalcular totales del carrito.
    
    Sincroniza precios con el catálogo actual.
    Útil cuando los precios pueden haber cambiado.
    """
    
    def __init__(
        self,
        carrito_repository: CarritoRepository,
        producto_repository: ProductoRepository
    ):
        self._carrito_repo = carrito_repository
        self._producto_repo = producto_repository
    
    def ejecutar(self, carrito_id: UUID, usuario_id: UUID) -> CarritoDTO:
        # Obtener carrito
        carrito = self._carrito_repo.obtener_por_id(carrito_id)
        if not carrito:
            raise EntidadNoEncontrada(f"Carrito {carrito_id} no encontrado")
        
        # Validar ownership
        if carrito.usuario_id != usuario_id:
            raise ReglaNegocioViolada("No tienes permiso para acceder a este carrito")
        
        # Sincronizar precios con catálogo
        cambios_precio = []
        for item in carrito.items:
            producto = self._producto_repo.obtener_por_id(item.producto_id)
            if producto and producto.precio.monto != item.precio_unitario_snapshot.monto:
                diferencia = carrito.actualizar_precio_producto(
                    item.producto_id,
                    producto.precio
                )
                cambios_precio.append((item.nombre_snapshot, diferencia))
        
        # Marcar como recalculado
        carrito.recalcular()
        
        # Guardar
        carrito_guardado = self._carrito_repo.guardar(carrito)
        
        # TODO: Emitir evento CarritoRecalculado si hubo cambios
        
        return CarritoDTO.desde_entidad(carrito_guardado)


class BloquearCarritoUseCase(CasoUsoBase[BloquearCarritoDTO, OperacionCarritoResultadoDTO]):
    """
    Caso de uso: Bloquear carrito para checkout.
    
    Estado BLOQUEADO:
    - No permite modificaciones
    - Reserva stock temporalmente
    - Anti-race conditions
    - Paso previo a confirmar
    """
    
    def __init__(
        self,
        carrito_repository: CarritoRepository,
        producto_repository: ProductoRepository
    ):
        self._carrito_repo = carrito_repository
        self._producto_repo = producto_repository
    
    def ejecutar(self, request: BloquearCarritoDTO, usuario_id: UUID) -> OperacionCarritoResultadoDTO:
        # Obtener carrito
        carrito = self._carrito_repo.obtener_por_id(request.carrito_id)
        if not carrito:
            raise EntidadNoEncontrada(f"Carrito {request.carrito_id} no encontrado")
        
        # Validar ownership
        if carrito.usuario_id != usuario_id:
            raise ReglaNegocioViolada("No tienes permiso para modificar este carrito")
        
        # Validar versión (optimistic locking)
        if carrito.version != request.version:
            raise ReglaNegocioViolada(
                "El carrito fue modificado por otra sesión. Por favor, recarga la página."
            )
        
        # Validar stock de todos los productos
        for item in carrito.items:
            producto = self._producto_repo.obtener_por_id(item.producto_id)
            if not producto:
                raise ReglaNegocioViolada(f"Producto {item.nombre_snapshot} ya no está disponible")
            if producto.stock_actual < item.cantidad:
                raise ReglaNegocioViolada(
                    f"Stock insuficiente para '{item.nombre_snapshot}'. "
                    f"Disponible: {producto.stock_actual}"
                )
        
        # Bloquear carrito
        carrito.bloquear()
        
        # Guardar
        carrito_guardado = self._carrito_repo.guardar(carrito)
        
        # TODO: Emitir evento CarritoBloqueado
        
        return OperacionCarritoResultadoDTO.exitoso(
            carrito_guardado,
            "Carrito bloqueado para checkout"
        )


class DesbloquearCarritoUseCase(CasoUsoBase[UUID, OperacionCarritoResultadoDTO]):
    """
    Caso de uso: Desbloquear carrito (rollback).
    
    Permite volver a modificar el carrito si el checkout fue cancelado.
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, carrito_id: UUID, usuario_id: UUID) -> OperacionCarritoResultadoDTO:
        # Obtener carrito
        carrito = self._repo.obtener_por_id(carrito_id)
        if not carrito:
            raise EntidadNoEncontrada(f"Carrito {carrito_id} no encontrado")
        
        # Validar ownership
        if carrito.usuario_id != usuario_id:
            raise ReglaNegocioViolada("No tienes permiso para modificar este carrito")
        
        # Desbloquear
        carrito.desbloquear()
        
        # Guardar
        carrito_guardado = self._repo.guardar(carrito)
        
        return OperacionCarritoResultadoDTO.exitoso(
            carrito_guardado,
            "Carrito desbloqueado"
        )


class ConfirmarCarritoUseCase(CasoUsoBase[ConfirmarCarritoDTO, OperacionCarritoResultadoDTO]):
    """
    Caso de uso: Confirmar carrito (convertir a orden).
    
    IDEMPOTENTE: Confirmar un carrito ya confirmado no genera error.
    
    Requiere que el carrito esté en estado BLOQUEADO.
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, request: ConfirmarCarritoDTO, usuario_id: UUID) -> OperacionCarritoResultadoDTO:
        # Obtener carrito
        carrito = self._repo.obtener_por_id(request.carrito_id)
        if not carrito:
            raise EntidadNoEncontrada(f"Carrito {request.carrito_id} no encontrado")
        
        # Validar ownership
        if carrito.usuario_id != usuario_id:
            raise ReglaNegocioViolada("No tienes permiso para modificar este carrito")
        
        # Confirmar (idempotente)
        confirmado = carrito.confirmar()
        
        if confirmado:
            # Guardar
            carrito_guardado = self._repo.guardar(carrito)
            
            # TODO: Emitir evento CarritoConfirmado
            # TODO: Crear orden a partir del carrito
            
            return OperacionCarritoResultadoDTO.exitoso(
                carrito_guardado,
                "Carrito confirmado exitosamente"
            )
        else:
            return OperacionCarritoResultadoDTO.exitoso(
                carrito,
                "El carrito ya estaba confirmado"
            )


class VaciarCarritoUseCase(CasoUsoBase[UUID, OperacionCarritoResultadoDTO]):
    """
    Caso de uso: Vaciar todos los productos del carrito.
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, carrito_id: UUID, usuario_id: UUID) -> OperacionCarritoResultadoDTO:
        # Obtener carrito
        carrito = self._repo.obtener_por_id(carrito_id)
        if not carrito:
            raise EntidadNoEncontrada(f"Carrito {carrito_id} no encontrado")
        
        # Validar ownership
        if carrito.usuario_id != usuario_id:
            raise ReglaNegocioViolada("No tienes permiso para modificar este carrito")
        
        # Quitar todos los productos
        productos_eliminados = len(carrito.items)
        for item in list(carrito.items):
            carrito.quitar_producto(item.producto_id)
        
        # Guardar
        carrito_guardado = self._repo.guardar(carrito)
        
        return OperacionCarritoResultadoDTO.exitoso(
            carrito_guardado,
            f"Carrito vaciado ({productos_eliminados} productos eliminados)"
        )


class ExpirarCarritosUseCase(CasoUsoBase[None, int]):
    """
    Caso de uso: Expirar carritos abandonados.
    
    Job de limpieza que se ejecuta periódicamente.
    Retorna la cantidad de carritos expirados.
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, request: None = None) -> int:
        # Obtener carritos expirados
        carritos_expirados = self._repo.obtener_carritos_expirados(datetime.now())
        count = 0
        for carrito in carritos_expirados:
            try:
                if carrito.expirar("timeout"):
                    self._repo.guardar(carrito)
                    # Liberar stock reservado
                    if hasattr(self._repo, 'liberar_stock_por_expiracion'):
                        self._repo.liberar_stock_por_expiracion(carrito.id)
                    count += 1
                    # TODO: Emitir evento CarritoExpirado
            except Exception:
                # Log error pero continuar con otros carritos
                pass
        return count


class ObtenerResumenCarritoUseCase(CasoUsoBase[UUID, Optional[CarritoResumenDTO]]):
    """
    Caso de uso: Obtener resumen del carrito (para header/badge).
    
    Versión ligera que solo retorna datos esenciales.
    """
    
    def __init__(self, carrito_repository: CarritoRepository):
        self._repo = carrito_repository
    
    def ejecutar(self, usuario_id: UUID) -> Optional[CarritoResumenDTO]:
        carrito = self._repo.obtener_carrito_activo_usuario(usuario_id)
        if not carrito:
            return None
        return CarritoResumenDTO.desde_entidad(carrito)
