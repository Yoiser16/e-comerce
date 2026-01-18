"""
Entidad Carrito - Agregado Root

Carrito de compras enterprise con:
- State Machine
- Optimistic Locking
- Cálculos server-side
- Snapshots de productos
- Eventos de dominio

REGLAS CRÍTICAS:
- Un usuario SOLO puede tener un carrito ACTIVO
- Totales SIEMPRE recalculados en backend
- CONFIRMADO y EXPIRADO son inmutables
- Confirmar es IDEMPOTENTE
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from decimal import Decimal

from .base import EntidadBase
from ..value_objects.dinero import Dinero
from ..value_objects.item_carrito import ItemCarrito
from ..exceptions.dominio import ReglaNegocioViolada
from shared.enums.estado_carrito import EstadoCarrito


# Tiempo de expiración por defecto: 24 horas
TIEMPO_EXPIRACION_HORAS = 24


class Carrito(EntidadBase):
    """
    Agregado Root: Carrito de Compras
    
    Responsabilidades:
    - Gestionar items del carrito (agregar, quitar, actualizar)
    - Calcular totales (bruto, descuentos, final)
    - Controlar máquina de estados
    - Garantizar integridad de datos
    - Gestionar versionamiento (optimistic locking)
    - Controlar expiración
    
    Invariantes:
    - Solo un carrito ACTIVO por usuario
    - No productos duplicados
    - Cantidades > 0
    - Totales calculados server-side
    - Estados inmutables: CONFIRMADO, EXPIRADO
    """
    
    def __init__(
        self,
        usuario_id: UUID,
        items: Optional[List[ItemCarrito]] = None,
        estado: EstadoCarrito = EstadoCarrito.CREADO,
        total_descuentos: Optional[Dinero] = None,
        moneda: str = "USD",
        version: int = 1,
        expira_en: Optional[datetime] = None,
        id: Optional[UUID] = None,
        fecha_creacion: Optional[datetime] = None,
        fecha_modificacion: Optional[datetime] = None,
        activo: bool = True
    ):
        super().__init__(id, fecha_creacion, fecha_modificacion, activo)
        self._usuario_id = usuario_id
        self._items: List[ItemCarrito] = items or []
        self._estado = estado
        self._total_descuentos = total_descuentos or Dinero(Decimal("0.00"), moneda)
        self._moneda = moneda
        self._version = version
        self._expira_en = expira_en or (datetime.now() + timedelta(hours=TIEMPO_EXPIRACION_HORAS))
        
        # Validar unicidad de productos
        self._validar_no_duplicados()
    
    # ==========================================
    # PROPIEDADES DE LECTURA
    # ==========================================
    
    @property
    def usuario_id(self) -> UUID:
        return self._usuario_id
    
    @property
    def items(self) -> List[ItemCarrito]:
        """Retorna copia de los items para evitar mutación externa"""
        return self._items.copy()
    
    @property
    def estado(self) -> EstadoCarrito:
        return self._estado
    
    @property
    def moneda(self) -> str:
        return self._moneda
    
    @property
    def version(self) -> int:
        return self._version
    
    @property
    def expira_en(self) -> datetime:
        return self._expira_en
    
    @property
    def esta_expirado(self) -> bool:
        """Verifica si el carrito ha expirado por tiempo"""
        return datetime.now() > self._expira_en
    
    @property
    def esta_vacio(self) -> bool:
        return len(self._items) == 0
    
    @property
    def cantidad_items(self) -> int:
        """Cantidad total de unidades en el carrito"""
        return sum(item.cantidad for item in self._items)
    
    @property
    def cantidad_productos(self) -> int:
        """Cantidad de productos únicos en el carrito"""
        return len(self._items)
    
    # ==========================================
    # CÁLCULOS SERVER-SIDE (NUNCA del cliente)
    # ==========================================
    
    @property
    def total_bruto(self) -> Dinero:
        """
        Calcula el total bruto (suma de subtotales sin descuentos).
        SIEMPRE calculado server-side.
        """
        if not self._items:
            return Dinero(Decimal("0.00"), self._moneda)
        
        total = sum(item.subtotal.monto for item in self._items)
        return Dinero(total, self._moneda)
    
    @property
    def total_descuentos(self) -> Dinero:
        """Total de descuentos aplicados"""
        return self._total_descuentos
    
    @property
    def total_final(self) -> Dinero:
        """
        Calcula el total final (bruto - descuentos).
        SIEMPRE calculado server-side.
        """
        monto_final = self.total_bruto.monto - self._total_descuentos.monto
        if monto_final < Decimal("0"):
            monto_final = Decimal("0.00")
        return Dinero(monto_final, self._moneda)
    
    # ==========================================
    # OPERACIONES DE NEGOCIO
    # ==========================================
    
    def agregar_producto(self, item: ItemCarrito) -> None:
        """
        Agrega un producto al carrito.
        
        Reglas:
        - Solo en estados que permiten modificación
        - No permite duplicados (por producto_id)
        - Cantidad debe ser > 0 (validado en ItemCarrito)
        
        Args:
            item: ItemCarrito con snapshot del producto
            
        Raises:
            ReglaNegocioViolada: Si el estado no permite modificaciones
            ReglaNegocioViolada: Si el producto ya existe en el carrito
        """
        self._validar_permite_modificaciones()
        self._validar_producto_no_duplicado(item.producto_id)
        
        self._items.append(item)
        self._activar_si_creado()
        self._incrementar_version()
        self.marcar_modificado()
    
    def quitar_producto(self, producto_id: UUID) -> ItemCarrito:
        """
        Elimina un producto del carrito.
        
        Args:
            producto_id: ID del producto a eliminar
            
        Returns:
            ItemCarrito eliminado
            
        Raises:
            ReglaNegocioViolada: Si el estado no permite modificaciones
            ReglaNegocioViolada: Si el producto no existe en el carrito
        """
        self._validar_permite_modificaciones()
        
        item_a_eliminar = self._buscar_item(producto_id)
        if not item_a_eliminar:
            raise ReglaNegocioViolada(
                f"El producto {producto_id} no existe en el carrito"
            )
        
        self._items.remove(item_a_eliminar)
        self._incrementar_version()
        self.marcar_modificado()
        
        return item_a_eliminar
    
    def actualizar_cantidad(self, producto_id: UUID, nueva_cantidad: int) -> None:
        """
        Actualiza la cantidad de un producto en el carrito.
        
        Args:
            producto_id: ID del producto
            nueva_cantidad: Nueva cantidad (debe ser > 0)
            
        Raises:
            ReglaNegocioViolada: Si el estado no permite modificaciones
            ReglaNegocioViolada: Si el producto no existe
            ReglaNegocioViolada: Si la cantidad es <= 0
        """
        self._validar_permite_modificaciones()
        
        if nueva_cantidad <= 0:
            raise ReglaNegocioViolada(
                f"La cantidad debe ser mayor a 0. Recibido: {nueva_cantidad}"
            )
        
        item_existente = self._buscar_item(producto_id)
        if not item_existente:
            raise ReglaNegocioViolada(
                f"El producto {producto_id} no existe en el carrito"
            )
        
        # Crear nuevo item con cantidad actualizada (inmutabilidad)
        item_actualizado = item_existente.con_cantidad(nueva_cantidad)
        
        # Reemplazar en la lista
        index = self._items.index(item_existente)
        self._items[index] = item_actualizado
        
        self._incrementar_version()
        self.marcar_modificado()
    
    def actualizar_precio_producto(self, producto_id: UUID, nuevo_precio: Dinero) -> Decimal:
        """
        Actualiza el precio de un producto (por sincronización con catálogo).
        
        Returns:
            Diferencia de precio (nuevo - anterior)
        """
        self._validar_permite_modificaciones()
        
        item_existente = self._buscar_item(producto_id)
        if not item_existente:
            raise ReglaNegocioViolada(
                f"El producto {producto_id} no existe en el carrito"
            )
        
        precio_anterior = item_existente.precio_unitario_snapshot.monto
        item_actualizado = item_existente.con_precio_actualizado(nuevo_precio)
        
        index = self._items.index(item_existente)
        self._items[index] = item_actualizado
        
        self._incrementar_version()
        self.marcar_modificado()
        
        return nuevo_precio.monto - precio_anterior
    
    def aplicar_descuento(self, monto_descuento: Dinero) -> None:
        """
        Aplica un descuento al carrito.
        
        Args:
            monto_descuento: Monto del descuento a aplicar
        """
        self._validar_permite_modificaciones()
        
        if monto_descuento.monto < Decimal("0"):
            raise ReglaNegocioViolada("El descuento no puede ser negativo")
        
        if monto_descuento.monto > self.total_bruto.monto:
            raise ReglaNegocioViolada(
                "El descuento no puede ser mayor al total bruto"
            )
        
        self._total_descuentos = monto_descuento
        self._incrementar_version()
        self.marcar_modificado()
    
    def recalcular(self) -> None:
        """
        Fuerza recálculo de totales.
        Los totales ya son propiedades calculadas, esto marca el carrito como modificado.
        """
        self._incrementar_version()
        self.marcar_modificado()
    
    # ==========================================
    # TRANSICIONES DE ESTADO
    # ==========================================
    
    def activar(self) -> None:
        """Activa el carrito (CREADO -> ACTIVO)"""
        self._transicionar_a(EstadoCarrito.ACTIVO)
    
    def bloquear(self) -> None:
        """
        Bloquea el carrito para checkout.
        
        Estado BLOQUEADO:
        - No permite modificaciones
        - Reserva stock temporalmente
        - Anti-race conditions
        """
        if self.esta_vacio:
            raise ReglaNegocioViolada(
                "No se puede bloquear un carrito vacío"
            )
        
        self._transicionar_a(EstadoCarrito.BLOQUEADO)
    
    def desbloquear(self) -> None:
        """Desbloquea el carrito (rollback a ACTIVO)"""
        self._transicionar_a(EstadoCarrito.ACTIVO)
    
    def confirmar(self) -> bool:
        """
        Confirma el carrito (BLOQUEADO -> CONFIRMADO).
        
        IDEMPOTENTE: Si ya está confirmado, retorna False sin error.
        
        Returns:
            True si se confirmó, False si ya estaba confirmado
        """
        if self._estado == EstadoCarrito.CONFIRMADO:
            return False  # Ya confirmado, idempotencia
        
        if self.esta_vacio:
            raise ReglaNegocioViolada(
                "No se puede confirmar un carrito vacío"
            )
        
        self._transicionar_a(EstadoCarrito.CONFIRMADO)
        return True
    
    def expirar(self, razon: str = "timeout") -> bool:
        """
        Expira el carrito.
        
        Returns:
            True si se expiró, False si ya estaba expirado/confirmado
        """
        if self._estado.es_inmutable:
            return False
        
        self._transicionar_a(EstadoCarrito.EXPIRADO)
        return True
    
    # ==========================================
    # MÉTODOS PRIVADOS
    # ==========================================
    
    def _validar_permite_modificaciones(self) -> None:
        """Valida que el estado actual permita modificaciones"""
        if not self._estado.permite_modificaciones:
            raise ReglaNegocioViolada(
                f"El carrito en estado {self._estado.value} no permite modificaciones"
            )
    
    def _validar_no_duplicados(self) -> None:
        """Valida que no haya productos duplicados"""
        productos_ids = [item.producto_id for item in self._items]
        if len(productos_ids) != len(set(productos_ids)):
            raise ReglaNegocioViolada(
                "No se permiten productos duplicados en el carrito"
            )
    
    def _validar_producto_no_duplicado(self, producto_id: UUID) -> None:
        """Valida que un producto no exista ya en el carrito"""
        if self._buscar_item(producto_id):
            raise ReglaNegocioViolada(
                f"El producto {producto_id} ya existe en el carrito. "
                "Use actualizar_cantidad para modificar."
            )
    
    def _buscar_item(self, producto_id: UUID) -> Optional[ItemCarrito]:
        """Busca un item por producto_id"""
        for item in self._items:
            if item.producto_id == producto_id:
                return item
        return None
    
    def _activar_si_creado(self) -> None:
        """Si está en CREADO, transiciona a ACTIVO"""
        if self._estado == EstadoCarrito.CREADO:
            self._estado = EstadoCarrito.ACTIVO
    
    def _transicionar_a(self, nuevo_estado: EstadoCarrito) -> None:
        """Realiza transición de estado validando reglas"""
        if not self._estado.puede_transicionar_a(nuevo_estado):
            raise ReglaNegocioViolada(
                f"No se puede transicionar de {self._estado.value} a {nuevo_estado.value}"
            )
        
        self._estado = nuevo_estado
        self._incrementar_version()
        self.marcar_modificado()
    
    def _incrementar_version(self) -> None:
        """Incrementa la versión para optimistic locking"""
        self._version += 1
    
    # ==========================================
    # REPRESENTACIÓN
    # ==========================================
    
    def __str__(self) -> str:
        return (
            f"Carrito({self.id}, usuario={self._usuario_id}, "
            f"estado={self._estado.value}, items={len(self._items)}, "
            f"total={self.total_final})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
