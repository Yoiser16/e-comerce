"""
Implementación del Repositorio de Carrito para PostgreSQL con Django ORM

Infrastructure Layer - Adaptador de persistencia.

Implementa el puerto CarritoRepository definido en la capa de dominio.
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from django.db import transaction, IntegrityError
from django.db.models import F

from domain.entities.carrito import Carrito
from domain.repositories.carrito_repository import CarritoRepository
from domain.value_objects.item_carrito import ItemCarrito
from domain.value_objects.dinero import Dinero
from domain.exceptions.dominio import ConcurrenciaConflicto
from shared.enums.estado_carrito import EstadoCarrito
from infrastructure.persistence.django.models import CarritoModel, ItemCarritoModel


class CarritoRepositoryDjango(CarritoRepository):
    """
    Implementación del repositorio de carritos usando Django ORM.
    
    Características:
    - Optimistic locking con versión
    - Transacciones atómicas
    - Mapeo completo entre modelos ORM y entidades de dominio
    """
    
    def obtener_por_id(self, id: UUID) -> Optional[Carrito]:
        """Obtiene un carrito por su ID."""
        try:
            modelo = CarritoModel.objects.prefetch_related('items').get(id=id)
            return self._modelo_a_entidad(modelo)
        except CarritoModel.DoesNotExist:
            return None
    
    def obtener_carrito_activo_usuario(self, usuario_id: UUID) -> Optional[Carrito]:
        """Obtiene el carrito activo de un usuario (si existe)."""
        try:
            modelo = CarritoModel.objects.prefetch_related('items').get(
                usuario_id=usuario_id,
                estado__in=['CREADO', 'ACTIVO', 'BLOQUEADO']
            )
            return self._modelo_a_entidad(modelo)
        except CarritoModel.DoesNotExist:
            return None
    
    @transaction.atomic
    def guardar(self, carrito: Carrito) -> Carrito:
        """
        Guarda o actualiza un carrito con sus items.
        
        Utiliza optimistic locking para detectar conflictos de concurrencia.
        """
        try:
            modelo_existente = CarritoModel.objects.select_for_update().filter(id=carrito.id).first()
            
            if modelo_existente:
                # Verificar versión para optimistic locking
                if modelo_existente.version != carrito.version - 1:
                    raise ConcurrenciaConflicto(
                        f"El carrito fue modificado por otra sesión. "
                        f"Versión esperada: {carrito.version - 1}, actual: {modelo_existente.version}"
                    )
                
                # Actualizar carrito existente
                CarritoModel.objects.filter(id=carrito.id).update(
                    estado=carrito.estado.value,
                    version=carrito.version,
                    total_bruto_monto=carrito.total_bruto.monto,
                    total_bruto_moneda=carrito.total_bruto.moneda,
                    total_descuentos_monto=carrito.total_descuentos.monto,
                    total_descuentos_moneda=carrito.total_descuentos.moneda,
                    total_final_monto=carrito.total_final.monto,
                    total_final_moneda=carrito.total_final.moneda,
                    fecha_expiracion=carrito.fecha_expiracion,
                    fecha_bloqueo=carrito.fecha_bloqueo,
                    fecha_confirmacion=carrito.fecha_confirmacion,
                    motivo_bloqueo=carrito.motivo_bloqueo,
                    motivo_expiracion=carrito.motivo_expiracion,
                    orden_generada_id=carrito.orden_generada_id,
                )
                
                # Sincronizar items
                self._sincronizar_items(carrito)
                
            else:
                # Crear nuevo carrito
                modelo = CarritoModel.objects.create(
                    id=carrito.id,
                    usuario_id=carrito.usuario_id,
                    estado=carrito.estado.value,
                    version=carrito.version,
                    total_bruto_monto=carrito.total_bruto.monto,
                    total_bruto_moneda=carrito.total_bruto.moneda,
                    total_descuentos_monto=carrito.total_descuentos.monto,
                    total_descuentos_moneda=carrito.total_descuentos.moneda,
                    total_final_monto=carrito.total_final.monto,
                    total_final_moneda=carrito.total_final.moneda,
                    fecha_expiracion=carrito.fecha_expiracion,
                    fecha_bloqueo=carrito.fecha_bloqueo,
                    fecha_confirmacion=carrito.fecha_confirmacion,
                    motivo_bloqueo=carrito.motivo_bloqueo,
                    motivo_expiracion=carrito.motivo_expiracion,
                    orden_generada_id=carrito.orden_generada_id,
                )
                
                # Crear items
                for item in carrito.items:
                    self._crear_item(modelo.id, item)
            
            return carrito
            
        except IntegrityError as e:
            if 'unique_carrito_activo_por_usuario' in str(e):
                raise ConcurrenciaConflicto(
                    "Ya existe un carrito activo para este usuario"
                )
            raise
    
    def eliminar(self, id: UUID) -> bool:
        """Elimina un carrito (soft delete no implementado, hard delete)."""
        deleted, _ = CarritoModel.objects.filter(id=id).delete()
        return deleted > 0
    
    def listar(self, skip: int = 0, limit: int = 100) -> List[Carrito]:
        """Lista todos los carritos con paginación."""
        modelos = CarritoModel.objects.prefetch_related('items').all()[skip:skip + limit]
        return [self._modelo_a_entidad(m) for m in modelos]
    
    def contar(self) -> int:
        """Cuenta el total de carritos."""
        return CarritoModel.objects.count()
    
    @transaction.atomic
    def bloquear_para_checkout(self, carrito_id: UUID, version: int) -> Optional[Carrito]:
        """
        Bloquea un carrito para checkout usando SELECT FOR UPDATE y reserva stock temporalmente.
        """
        from infrastructure.persistence.django.models import ProductoModel, ItemCarritoModel, ProductoVarianteModel
        try:
            modelo = CarritoModel.objects.select_for_update(nowait=True).get(
                id=carrito_id,
                estado__in=['CREADO', 'ACTIVO']
            )
            # Verificar versión
            if modelo.version != version:
                raise ConcurrenciaConflicto(
                    f"El carrito fue modificado. Versión esperada: {version}, actual: {modelo.version}"
                )
            # Reservar stock de cada producto/variante
            for item in ItemCarritoModel.objects.filter(carrito_id=carrito_id):
                if item.variante_id:
                    variante = ProductoVarianteModel.objects.select_for_update().get(id=item.variante_id)
                    if variante.stock_actual < item.cantidad:
                        raise ConcurrenciaConflicto(f"Stock insuficiente para variante {variante.sku}")
                    variante.stock_actual -= item.cantidad
                    variante.save(update_fields=["stock_actual"])
                    ProductoModel.objects.filter(id=item.producto_id).update(stock_actual=F('stock_actual') - item.cantidad)
                else:
                    producto = ProductoModel.objects.select_for_update().get(id=item.producto_id)
                    if producto.stock_actual < item.cantidad:
                        raise ConcurrenciaConflicto(f"Stock insuficiente para {producto.nombre}")
                    producto.stock_actual -= item.cantidad
                    producto.save(update_fields=["stock_actual"])
            # Bloquear carrito
            modelo.estado = 'BLOQUEADO'
            modelo.fecha_bloqueo = datetime.now()
            modelo.version = F('version') + 1
            modelo.save(update_fields=['estado', 'fecha_bloqueo', 'version'])
            modelo.refresh_from_db()
            return self._modelo_a_entidad(modelo)
        except CarritoModel.DoesNotExist:
            return None

    @transaction.atomic
    def liberar_stock_por_expiracion(self, carrito_id: UUID) -> None:
        """
        Libera el stock reservado de un carrito expirado.
        """
        from infrastructure.persistence.django.models import ProductoModel, ItemCarritoModel, ProductoVarianteModel
        items = ItemCarritoModel.objects.filter(carrito_id=carrito_id)
        for item in items:
            if item.variante_id:
                variante = ProductoVarianteModel.objects.select_for_update().get(id=item.variante_id)
                variante.stock_actual += item.cantidad
                variante.save(update_fields=["stock_actual"])
                ProductoModel.objects.filter(id=item.producto_id).update(stock_actual=F('stock_actual') + item.cantidad)
            else:
                producto = ProductoModel.objects.select_for_update().get(id=item.producto_id)
                producto.stock_actual += item.cantidad
                producto.save(update_fields=["stock_actual"])
    
    def obtener_carritos_expirados(self, fecha_limite: datetime) -> List[Carrito]:
        """Obtiene carritos que deberían expirar."""
        modelos = CarritoModel.objects.prefetch_related('items').filter(
            estado__in=['CREADO', 'ACTIVO'],
            fecha_expiracion__lte=fecha_limite
        )
        return [self._modelo_a_entidad(m) for m in modelos]
    
    def obtener_carritos_por_usuario(
        self,
        usuario_id: UUID,
        incluir_historico: bool = False
    ) -> List[Carrito]:
        """Obtiene todos los carritos de un usuario."""
        queryset = CarritoModel.objects.prefetch_related('items').filter(usuario_id=usuario_id)
        
        if not incluir_historico:
            queryset = queryset.exclude(estado__in=['CONFIRMADO', 'EXPIRADO'])
        
        return [self._modelo_a_entidad(m) for m in queryset]
    
    def obtener_carritos_por_estado(self, estado: EstadoCarrito) -> List[Carrito]:
        """Obtiene todos los carritos en un estado específico."""
        modelos = CarritoModel.objects.prefetch_related('items').filter(estado=estado.value)
        return [self._modelo_a_entidad(m) for m in modelos]
    
    def obtener_historial_usuario(
        self, 
        usuario_id: UUID, 
        incluir_expirados: bool = False
    ) -> List[Carrito]:
        """Obtiene el historial de carritos de un usuario."""
        queryset = CarritoModel.objects.prefetch_related('items').filter(usuario_id=usuario_id)
        
        if not incluir_expirados:
            queryset = queryset.exclude(estado='EXPIRADO')
        
        return [self._modelo_a_entidad(m) for m in queryset.order_by('-fecha_creacion')]
    
    def existe(self, id: UUID) -> bool:
        """Verifica si existe un carrito con el ID dado."""
        return CarritoModel.objects.filter(id=id).exists()
    
    def contar_por_estado(self, estado: EstadoCarrito) -> int:
        """Cuenta carritos por estado."""
        return CarritoModel.objects.filter(estado=estado.value).count()
    
    def obtener_todos(self, limite: int = 100, offset: int = 0) -> List[Carrito]:
        """Obtiene todos los carritos con paginación."""
        modelos = CarritoModel.objects.prefetch_related('items').all()[offset:offset + limite]
        return [self._modelo_a_entidad(m) for m in modelos]
    
    # ===== MÉTODOS PRIVADOS DE MAPEO =====
    
    def _modelo_a_entidad(self, modelo: CarritoModel) -> Carrito:
        """Convierte un modelo ORM a una entidad de dominio."""
        items = [self._item_modelo_a_vo(im) for im in modelo.items.all()]
        
        carrito = Carrito(
            usuario_id=modelo.usuario_id,
            id=modelo.id
        )
        
        # Restaurar estado interno
        carrito._estado = EstadoCarrito(modelo.estado)
        carrito._version = modelo.version
        carrito._items = items
        carrito._fecha_creacion = modelo.fecha_creacion
        carrito._fecha_modificacion = modelo.fecha_modificacion
        carrito._fecha_expiracion = modelo.fecha_expiracion
        carrito._fecha_bloqueo = modelo.fecha_bloqueo
        carrito._fecha_confirmacion = modelo.fecha_confirmacion
        carrito._motivo_bloqueo = modelo.motivo_bloqueo
        carrito._motivo_expiracion = modelo.motivo_expiracion
        carrito._orden_generada_id = modelo.orden_generada_id
        
        return carrito
    
    def _item_modelo_a_vo(self, modelo: ItemCarritoModel) -> ItemCarrito:
        """Convierte un modelo de item ORM a un Value Object."""
        variante_id = modelo.variante_id or modelo.producto_id
        return ItemCarrito(
            producto_id=modelo.producto_id,
            variante_id=variante_id,
            sku=modelo.sku_snapshot,
            nombre_snapshot=modelo.nombre_snapshot,
            precio_unitario_snapshot=Dinero(
                monto=modelo.precio_unitario_monto,
                moneda=modelo.precio_unitario_moneda
            ),
            cantidad=modelo.cantidad,
            variante_sku=modelo.variante_sku,
            color_snapshot=modelo.color_snapshot,
            largo_snapshot=modelo.largo_snapshot
        )
    
    def _sincronizar_items(self, carrito: Carrito) -> None:
        """Sincroniza los items del carrito con la base de datos."""
        def _key(item: ItemCarrito) -> UUID:
            return item.variante_id or item.producto_id

        def _key_db(item: ItemCarritoModel) -> UUID:
            return item.variante_id or item.producto_id

        items_actuales = { _key(item): item for item in carrito.items }
        items_db = {
            _key_db(im): im
            for im in ItemCarritoModel.objects.filter(carrito_id=carrito.id)
        }
        
        # Eliminar items que ya no están
        items_a_eliminar = set(items_db.keys()) - set(items_actuales.keys())
        for item_key in items_a_eliminar:
            ItemCarritoModel.objects.filter(
                carrito_id=carrito.id,
                variante_id=item_key
            ).delete()
            ItemCarritoModel.objects.filter(
                carrito_id=carrito.id,
                variante_id__isnull=True,
                producto_id=item_key
            ).delete()
        
        # Actualizar o crear items
        for item_key, item in items_actuales.items():
            if item_key in items_db:
                # Actualizar
                ItemCarritoModel.objects.filter(id=items_db[item_key].id).update(
                    producto_id=item.producto_id,
                    variante_id=item.variante_id,
                    sku_snapshot=item.sku,
                    nombre_snapshot=item.nombre_snapshot,
                    precio_unitario_monto=item.precio_unitario_snapshot.monto,
                    precio_unitario_moneda=item.precio_unitario_snapshot.moneda,
                    variante_sku=item.variante_sku,
                    color_snapshot=item.color_snapshot,
                    largo_snapshot=item.largo_snapshot,
                    cantidad=item.cantidad,
                    subtotal_monto=item.subtotal.monto,
                    subtotal_moneda=item.subtotal.moneda,
                )
            else:
                # Crear
                self._crear_item(carrito.id, item)
    
    def _crear_item(self, carrito_id: UUID, item: ItemCarrito) -> None:
        """Crea un item de carrito en la base de datos."""
        ItemCarritoModel.objects.create(
            carrito_id=carrito_id,
            producto_id=item.producto_id,
            variante_id=item.variante_id,
            sku_snapshot=item.sku,
            nombre_snapshot=item.nombre_snapshot,
            precio_unitario_monto=item.precio_unitario_snapshot.monto,
            precio_unitario_moneda=item.precio_unitario_snapshot.moneda,
            variante_sku=item.variante_sku,
            color_snapshot=item.color_snapshot,
            largo_snapshot=item.largo_snapshot,
            cantidad=item.cantidad,
            subtotal_monto=item.subtotal.monto,
            subtotal_moneda=item.subtotal.moneda,
        )
