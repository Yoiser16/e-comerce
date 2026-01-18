"""
Value Object: ItemCarrito

Representa un item dentro del carrito de compras.
Contiene SNAPSHOT del producto para garantizar integridad de precios.

REGLA CRÍTICA: El precio NUNCA se confía al cliente.
Los snapshots se toman al momento de agregar el producto.
"""
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from .base import ValueObject
from .dinero import Dinero
from ..exceptions.dominio import ReglaNegocioViolada


@dataclass(frozen=True)
class ItemCarrito(ValueObject):
    """
    Item del carrito de compras con snapshot de producto.
    
    Atributos:
        producto_id: Identificador único del producto
        sku: Código SKU del producto (snapshot)
        nombre_snapshot: Nombre del producto al momento de agregar (snapshot)
        precio_unitario_snapshot: Precio unitario al momento de agregar (snapshot)
        cantidad: Cantidad de unidades
        
    El subtotal se calcula automáticamente: precio_unitario * cantidad
    
    INMUTABLE: Para modificar cantidad, crear nuevo ItemCarrito
    """
    
    producto_id: UUID
    sku: str
    nombre_snapshot: str
    precio_unitario_snapshot: Dinero
    cantidad: int
    
    def __post_init__(self):
        """Validaciones de negocio al crear el item"""
        self._validar_cantidad()
        self._validar_sku()
        self._validar_nombre()
        self._validar_precio()
    
    def _validar_cantidad(self) -> None:
        """La cantidad debe ser mayor a 0"""
        if self.cantidad <= 0:
            raise ReglaNegocioViolada(
                f"La cantidad debe ser mayor a 0. Recibido: {self.cantidad}"
            )
    
    def _validar_sku(self) -> None:
        """El SKU no puede estar vacío"""
        if not self.sku or not self.sku.strip():
            raise ReglaNegocioViolada("El SKU del producto no puede estar vacío")
    
    def _validar_nombre(self) -> None:
        """El nombre snapshot no puede estar vacío"""
        if not self.nombre_snapshot or not self.nombre_snapshot.strip():
            raise ReglaNegocioViolada("El nombre del producto no puede estar vacío")
    
    def _validar_precio(self) -> None:
        """El precio debe ser positivo"""
        if self.precio_unitario_snapshot.monto <= Decimal("0"):
            raise ReglaNegocioViolada(
                f"El precio unitario debe ser positivo. Recibido: {self.precio_unitario_snapshot}"
            )
    
    @property
    def subtotal(self) -> Dinero:
        """
        Calcula el subtotal del item.
        SIEMPRE calculado server-side, nunca desde el cliente.
        """
        monto_subtotal = self.precio_unitario_snapshot.monto * Decimal(str(self.cantidad))
        return Dinero(monto_subtotal, self.precio_unitario_snapshot.moneda)
    
    def con_cantidad(self, nueva_cantidad: int) -> 'ItemCarrito':
        """
        Crea un nuevo ItemCarrito con cantidad actualizada.
        Mantiene los snapshots originales.
        """
        return ItemCarrito(
            producto_id=self.producto_id,
            sku=self.sku,
            nombre_snapshot=self.nombre_snapshot,
            precio_unitario_snapshot=self.precio_unitario_snapshot,
            cantidad=nueva_cantidad
        )
    
    def con_precio_actualizado(self, nuevo_precio: Dinero) -> 'ItemCarrito':
        """
        Crea un nuevo ItemCarrito con precio actualizado.
        Se usa cuando el precio del producto cambió y se quiere sincronizar.
        """
        return ItemCarrito(
            producto_id=self.producto_id,
            sku=self.sku,
            nombre_snapshot=self.nombre_snapshot,
            precio_unitario_snapshot=nuevo_precio,
            cantidad=self.cantidad
        )
    
    def __eq__(self, other: object) -> bool:
        """Dos items son iguales si tienen el mismo producto_id"""
        if not isinstance(other, ItemCarrito):
            return False
        return self.producto_id == other.producto_id
    
    def __hash__(self) -> int:
        return hash(self.producto_id)
    
    def __str__(self) -> str:
        return f"{self.cantidad}x {self.nombre_snapshot} @ {self.precio_unitario_snapshot} = {self.subtotal}"
