"""
Implementación del Repositorio de Orden con Django ORM
"""
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from django.db import transaction

from domain.entities.orden import Orden
from domain.value_objects.linea_orden import LineaOrden
from domain.value_objects.dinero import Dinero
from domain.repositories.orden_repository import OrdenRepository
from shared.enums.estados import EstadoOrden
from infrastructure.persistence.django.models import OrdenModel, LineaOrdenModel, ProductoModel
from infrastructure.auditing.servicio_auditoria import ServicioAuditoria
from infrastructure.logging.logger_service import LoggerService


class OrdenRepositoryImpl(OrdenRepository):
    """
    Implementación del repositorio de órdenes.
    Maneja la persistencia del agregado completo (Orden + Lineas).
    """

    def __init__(
        self,
        auditoria: Optional[ServicioAuditoria] = None,
        logger: Optional[LoggerService] = None
    ):
        self._auditoria = auditoria or ServicioAuditoria()
        self._logger = logger or LoggerService("OrdenRepository")

    def _to_domain(self, model: OrdenModel) -> Orden:
        """Convierte modelo ORM a entidad de dominio"""
        lineas = []
        for linea_model in model.lineas.all():
            lineas.append(LineaOrden(
                producto_id=linea_model.producto_id,
                cantidad=linea_model.cantidad,
                precio_unitario=Dinero(
                    linea_model.precio_unitario_monto,
                    linea_model.precio_unitario_moneda
                )
            ))

        return Orden(
            id=model.id,
            cliente_id=model.cliente_id,
            lineas=lineas,
            estado=EstadoOrden(model.estado),
            fecha_creacion=model.fecha_creacion,
            fecha_modificacion=model.fecha_modificacion,
            activo=model.activo
        )

    def _to_model(self, entity: Orden) -> OrdenModel:
        """
        Convierte entidad a modelo. 
        NOTA: Solo crea la cabecera, las líneas se manejan por separado.
        """
        return OrdenModel(
            id=entity.id,
            cliente_id=entity.cliente_id,
            estado=entity.estado.value,
            total_monto=entity.total.monto,
            total_moneda=entity.total.moneda,
            activo=entity.activo,
            fecha_creacion=entity.fecha_creacion,
            fecha_modificacion=entity.fecha_modificacion
        )

    def obtener_por_id(self, id: UUID) -> Optional[Orden]:
        self._logger.info("Obteniendo orden por ID", orden_id=str(id))
        try:
            # prefetch_related optimiza la carga de lineas
            model = OrdenModel.objects.prefetch_related('lineas').get(id=id)
            return self._to_domain(model)
        except OrdenModel.DoesNotExist:
            return None

    def obtener_por_cliente(self, cliente_id: UUID) -> List[Orden]:
        self._logger.info("Obteniendo ordenes por cliente", cliente_id=str(cliente_id))
        models = OrdenModel.objects.filter(cliente_id=cliente_id).prefetch_related('lineas')
        return [self._to_domain(m) for m in models]

    def obtener_por_estado(self, estado: EstadoOrden) -> List[Orden]:
        self._logger.info("Obteniendo ordenes por estado", estado=estado.value)
        models = OrdenModel.objects.filter(estado=estado.value).prefetch_related('lineas')
        return [self._to_domain(m) for m in models]

    def obtener_pendientes_procesamiento(self) -> List[Orden]:
        return self.obtener_por_estado(EstadoOrden.CONFIRMADA)
        
    def obtener_todos(self, limite: int = 100, offset: int = 0) -> List[Orden]:
        models = OrdenModel.objects.all()[offset:offset+limite].prefetch_related('lineas')
        return [self._to_domain(m) for m in models]

    def existe(self, id: UUID) -> bool:
        return OrdenModel.objects.filter(id=id).exists()

    @transaction.atomic
    def guardar(self, entidad: Orden) -> Orden:
        """
        Guarda la orden y sus líneas en una transacción atómica.
        Si falla algo, se hace rollback de todo.
        """
        self._logger.info("Guardando orden", orden_id=str(entidad.id))
        
        try:
            es_nueva = not OrdenModel.objects.filter(id=entidad.id).exists()
            accion = "CREATE" if es_nueva else "UPDATE"

            # 1. Guardar cabecera (OrdenModel)
            orden_model = self._to_model(entidad)
            orden_model.save()

            # 2. Gestionar Líneas (Borrarlas todas y recrearlas es lo más seguro para DDD)
            # Esto simplifica la lógica de sincronización de listas
            if not es_nueva:
                orden_model.lineas.all().delete()

            # 3. Crear nuevas líneas
            nuevas_lineas = []
            for linea in entidad.lineas:
                # Validar que el producto existe
                if not ProductoModel.objects.filter(id=linea.producto_id).exists():
                     raise ValueError(f"Producto {linea.producto_id} no existe")

                nuevas_lineas.append(LineaOrdenModel(
                    orden=orden_model,
                    producto_id=linea.producto_id,
                    cantidad=linea.cantidad,
                    precio_unitario_monto=linea.precio_unitario.monto,
                    precio_unitario_moneda=linea.precio_unitario.moneda,
                    subtotal_monto=linea.subtotal.monto,
                    subtotal_moneda=linea.subtotal.moneda
                ))
            
            # Bulk create es mucho más eficiente
            LineaOrdenModel.objects.bulk_create(nuevas_lineas)

            # 4. Auditoría
            self._auditoria.registrar(
                entidad_tipo="Orden",
                entidad_id=entidad.id,
                accion=accion,
                resultado="EXITO",
                mensaje=f"Orden guardada con {len(nuevas_lineas)} lineas"
            )

            return self._to_domain(orden_model)

        except Exception as e:
            self._logger.error("Error guardando orden", error=str(e))
            self._auditoria.registrar(
                entidad_tipo="Orden",
                entidad_id=entidad.id,
                accion="SAVE",
                resultado="FALLO",
                mensaje=str(e)
            )
            raise

    def eliminar(self, id: UUID) -> bool:
        self._logger.info("Eliminando orden", orden_id=str(id))
        try:
            model = OrdenModel.objects.get(id=id)
            model.activo = False
            model.save()
            return True
        except OrdenModel.DoesNotExist:
            return False
    
    @transaction.atomic
    def confirmar_con_stock(self, orden_id: UUID) -> Orden:
        """
        Confirma orden SIN validación/descuento de stock.
        
        NOTA IMPORTANTE: El stock ya fue descontado cuando la orden fue creada en estado PENDIENTE.
        Este método SOLO cambia el estado a CONFIRMADA.
        
        SISTEMA HÍBRIDO:
        - PENDIENTE: Stock descontado (validación atómica al crear)
        - CONFIRMADA: Solo cambio de estado
        - CANCELADA: Stock devuelto
        """
        from domain.exceptions.dominio import EntidadNoEncontrada, ReglaNegocioViolada
        
        self._logger.info("Confirmando orden", orden_id=str(orden_id))
        
        try:
            # 1. Obtener orden
            orden = self.obtener_por_id(orden_id)
            if not orden:
                raise EntidadNoEncontrada(f"Orden {orden_id} no encontrada")
            
            # 2. Validar estado de la orden
            # Permitir confirmar desde BORRADOR o PENDIENTE
            if orden.estado not in [EstadoOrden.BORRADOR, EstadoOrden.PENDIENTE]:
                raise ReglaNegocioViolada(
                    f"Solo se pueden confirmar órdenes en estado BORRADOR o PENDIENTE. Estado actual: {orden.estado.value}"
                )
            
            if not orden.lineas:
                raise ReglaNegocioViolada("No se puede confirmar una orden sin líneas")
            
            # 3. Confirmar orden (cambio de estado)
            # NOTA: El stock ya fue descontado al crear la orden en PENDIENTE
            orden.confirmar()
            
            # 4. Actualizar modelo de orden en base de datos
            orden_model = OrdenModel.objects.get(id=orden_id)
            orden_model.estado = orden.estado.value
            orden_model.total_monto = orden.total.monto
            orden_model.total_moneda = orden.total.moneda
            orden_model.save()
            
            # Convertir a dominio para retornar
            orden_confirmada = self._to_domain(orden_model)
            
            # 5. Auditoría exitosa
            self._auditoria.registrar(
                entidad_tipo="Orden",
                entidad_id=orden_id,
                accion="CONFIRMAR_ORDEN",
                resultado="EXITO",
                mensaje="Orden confirmada"
            )
            
            self._logger.info(
                "Orden confirmada exitosamente",
                orden_id=str(orden_id)
            )
            
            return orden_confirmada
            
        except (EntidadNoEncontrada, ReglaNegocioViolada) as e:
            # Excepciones de negocio: re-lanzar
            self._logger.warning(
                "Fallo en confirmación de orden",
                orden_id=str(orden_id),
                error=str(e)
            )
            raise
            
        except Exception as e:
            # Errores inesperados
            self._logger.error(
                "Error crítico al confirmar orden",
                orden_id=str(orden_id),
                error=str(e)
            )
            
            self._auditoria.registrar(
                entidad_tipo="Orden",
                entidad_id=orden_id,
                accion="CONFIRMAR_ORDEN",
                resultado="FALLO",
                mensaje=f"Error inesperado: {str(e)}"
            )
            
            raise
