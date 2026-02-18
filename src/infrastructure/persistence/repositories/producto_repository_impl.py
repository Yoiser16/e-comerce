"""
Implementación del Repositorio de Producto con Django ORM
"""
from typing import Optional, List, Tuple, Dict, Any
from uuid import UUID
from decimal import Decimal

from django.db.models import Q, Count, Min, Max, F

from domain.repositories.producto_repository import ProductoRepository
from domain.entities.producto import Producto
from domain.entities.producto_variante import ProductoVariante
from domain.value_objects.codigo_producto import CodigoProducto
from domain.value_objects.dinero import Dinero
from domain.value_objects.criterios_busqueda import CriteriosBusqueda
from infrastructure.persistence.django.models import ProductoModel, ImagenProductoModel, ProductoVarianteModel
from infrastructure.auditing.servicio_auditoria import ServicioAuditoria
from infrastructure.logging.logger_service import LoggerService
from shared.enums.atributos_producto import OrdenProducto


class ProductoRepositoryImpl(ProductoRepository):
    """
    Implementación concreta del repositorio de Producto usando Django ORM.
    """
    
    def __init__(
        self,
        auditoria: Optional[ServicioAuditoria] = None,
        logger: Optional[LoggerService] = None
    ):
        self._auditoria = auditoria or ServicioAuditoria()
        self._logger = logger or LoggerService("ProductoRepository")
    
    def _to_domain(self, model: ProductoModel) -> Producto:
        """
        Mapea modelo Django a entidad de dominio.
        """
        # Obtener nombre de categoría si existe
        categoria_nombre = None
        if model.categoria_id:
            categoria_nombre = model.categoria.nombre if model.categoria else None
        
        producto = Producto(
            id=model.id,
            codigo=CodigoProducto(model.codigo),
            nombre=model.nombre,
            descripcion=model.descripcion,
            precio=Dinero(model.monto_precio, model.moneda_precio),
            stock_actual=model.stock_actual,
            stock_minimo=model.stock_minimo,
            fecha_creacion=model.fecha_creacion,
            fecha_modificacion=model.fecha_modificacion,
            activo=model.activo,
            categoria=categoria_nombre,
            imagen_principal=model.imagen_principal,
            color=model.color,
            tipo=model.tipo,
            largo=model.largo,
            origen=model.origen,
            metodo=model.metodo,
            calidad=model.calidad,
            destacado=model.destacado,
            disponible_b2b=model.disponible_b2b,
            porcentaje_descuento_b2b=model.porcentaje_descuento_b2b,
            cantidad_minima_mayorista=getattr(model, 'cantidad_minima_mayorista', 1),
            variantes=self._map_variantes(model)
        )

        # Incluir TODAS las imágenes adicionales del modelo ImagenProductoModel
        try:
            imagenes_qs = model.imagenes.all().order_by('orden')
            # Obtener todas las URLs de imágenes adicionales
            imagenes_adicionales = [img.url for img in imagenes_qs if img.url]
            # Si hay imágenes en el modelo, usarlas
            if imagenes_adicionales:
                producto.imagenes = imagenes_adicionales
            else:
                producto.imagenes = []
        except Exception:
            producto.imagenes = []

        return producto

    def _map_variantes(self, model: ProductoModel) -> list:
        if not hasattr(model, '_prefetched_objects_cache') or 'variantes' not in model._prefetched_objects_cache:
            return []
        variantes = []
        for variante in model.variantes.all():
            variantes.append(
                ProductoVariante(
                    id=variante.id,
                    producto_id=variante.producto_id,
                    sku=variante.sku,
                    color=variante.color,
                    largo=variante.largo,
                    precio=Dinero(variante.precio_monto, variante.precio_moneda),
                    stock_actual=variante.stock_actual,
                    stock_minimo=variante.stock_minimo,
                    imagen_url=variante.imagen_url,
                    activo=variante.activo,
                    orden=variante.orden,
                    fecha_creacion=variante.fecha_creacion,
                    fecha_modificacion=variante.fecha_modificacion
                )
            )
        return variantes
    
    def _to_model(self, entity: Producto) -> ProductoModel:
        """
        Mapea entidad de dominio a modelo Django.
        """
        return ProductoModel(
            id=entity.id,
            codigo=entity.codigo.valor,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            moneda_precio=entity.precio.moneda,
            monto_precio=entity.precio.monto,
            stock_actual=entity.stock_actual,
            stock_minimo=entity.stock_minimo,
            stock_reservado=getattr(entity, 'stock_reservado', 0),
            cantidad_minima_mayorista=getattr(entity, 'cantidad_minima_mayorista', 1),
            activo=entity.activo,
            fecha_creacion=entity.fecha_creacion,
            fecha_modificacion=entity.fecha_modificacion,
            disponible_b2b=getattr(entity, 'disponible_b2b', True),
            porcentaje_descuento_b2b=getattr(entity, 'porcentaje_descuento_b2b', None)
        )
    
    def obtener_por_id(self, id: UUID) -> Optional[Producto]:
        self._logger.info(f"Obteniendo producto por ID", producto_id=str(id))
        try:
            model = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes', 'variantes').get(id=id)
            return self._to_domain(model)
        except ProductoModel.DoesNotExist:
            return None
    
    def obtener_por_codigo(self, codigo: CodigoProducto) -> Optional[Producto]:
        self._logger.info(f"Buscando producto por código", codigo=codigo.valor)
        try:
            model = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes', 'variantes').get(codigo=codigo.valor)
            return self._to_domain(model)
        except ProductoModel.DoesNotExist:
            return None
            
    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        self._logger.info(f"Buscando productos por nombre", nombre=nombre)
        models = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes').filter(
            nombre__icontains=nombre
        )
        return [self._to_domain(model) for model in models]

    def obtener_con_stock_bajo(self) -> List[Producto]:
        self._logger.info("Buscando productos con stock bajo")
        # En SQL: WHERE stock_actual <= stock_minimo
        # Django F expression para comparar columnas
        from django.db.models import F
        models = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes').filter(stock_actual__lte=F('stock_minimo'), activo=True)
        return [self._to_domain(model) for model in models]
        
    def obtener_disponibles(self) -> List[Producto]:
        self._logger.info("Obteniendo productos disponibles")
        from django.db.models import Q
        models = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes').filter(
            activo=True
        ).filter(
            Q(stock_actual__gt=0) | Q(variantes__activo=True, variantes__stock_actual__gt=0)
        ).distinct()
        return [self._to_domain(model) for model in models]

    def obtener_variante_por_id(self, variante_id: UUID) -> Optional[dict]:
        try:
            variante = ProductoVarianteModel.objects.select_related('producto').get(id=variante_id, activo=True)
        except ProductoVarianteModel.DoesNotExist:
            return None
        return {
            'id': variante.id,
            'producto_id': variante.producto_id,
            'sku': variante.sku,
            'color': variante.color,
            'largo': variante.largo,
            'precio_monto': variante.precio_monto,
            'precio_moneda': variante.precio_moneda,
            'stock_actual': variante.stock_actual,
            'stock_minimo': variante.stock_minimo,
            'imagen_url': variante.imagen_url,
            'activo': variante.activo,
            'orden': variante.orden
        }

    def listar_variantes_producto(self, producto_id: UUID) -> List[dict]:
        variantes = ProductoVarianteModel.objects.filter(producto_id=producto_id, activo=True).order_by('orden', 'fecha_creacion')
        return [
            {
                'id': v.id,
                'producto_id': v.producto_id,
                'sku': v.sku,
                'color': v.color,
                'largo': v.largo,
                'precio_monto': v.precio_monto,
                'precio_moneda': v.precio_moneda,
                'stock_actual': v.stock_actual,
                'stock_minimo': v.stock_minimo,
                'imagen_url': v.imagen_url,
                'activo': v.activo,
                'orden': v.orden
            }
            for v in variantes
        ]

    def _sincronizar_variantes(self, producto_model: ProductoModel, variantes: list) -> None:
        existentes = {str(v.id): v for v in ProductoVarianteModel.objects.filter(producto=producto_model)}
        ids_recibidos = set()

        variantes_payload = list(variantes or [])
        if not variantes_payload:
            return
        base_existente = next((v for v in existentes.values() if not v.color and not v.largo), None)

        def _payload_dict(data):
            return data if isinstance(data, dict) else data.__dict__

        def _es_base(payload):
            return not payload.get('color') and not payload.get('largo')

        tiene_base = any(_es_base(_payload_dict(v)) for v in variantes_payload)
        if not tiene_base:
            variantes_payload.insert(0, {
                'id': base_existente.id if base_existente else None,
                'sku': f"{producto_model.codigo}-BASE",
                'color': None,
                'largo': None,
                'precio_monto': producto_model.monto_precio,
                'precio_moneda': producto_model.moneda_precio,
                'stock_actual': producto_model.stock_actual,
                'stock_minimo': producto_model.stock_minimo,
                'imagen_url': producto_model.imagen_principal,
                'activo': True,
                'orden': -1
            })

        for idx, data in enumerate(variantes_payload):
            payload = _payload_dict(data)
            variante_id = payload.get('id')
            if variante_id:
                ids_recibidos.add(str(variante_id))
            sku = payload.get('sku') or f"{producto_model.codigo}-{payload.get('color') or 'std'}-{payload.get('largo') or 'std'}"
            defaults = {
                'sku': sku,
                'color': payload.get('color'),
                'largo': payload.get('largo'),
                'precio_monto': payload.get('precio_monto') or producto_model.monto_precio,
                'precio_moneda': payload.get('precio_moneda') or producto_model.moneda_precio,
                'stock_actual': payload.get('stock_actual', 0),
                'stock_minimo': payload.get('stock_minimo', 0),
                'cantidad_minima_mayorista': payload.get('cantidad_minima_mayorista', 1),
                'imagen_url': payload.get('imagen_url'),
                'activo': payload.get('activo', True),
                'orden': payload.get('orden', idx)
            }

            if variante_id and str(variante_id) in existentes:
                ProductoVarianteModel.objects.filter(id=variante_id).update(**defaults)
            else:
                ProductoVarianteModel.objects.create(producto=producto_model, **defaults)

        for var_id, var_model in existentes.items():
            if var_id not in ids_recibidos:
                ProductoVarianteModel.objects.filter(id=var_model.id).update(activo=False)

        self._actualizar_precio_y_stock_producto(producto_model)

    def _actualizar_precio_y_stock_producto(self, producto_model: ProductoModel) -> None:
        return
    
    def obtener_con_bloqueo(self, id: UUID) -> Optional[Producto]:
        """
        Obtiene producto con bloqueo pesimista (SELECT FOR UPDATE).
        
        CRÍTICO: Previene race conditions en operaciones de stock.
        PostgreSQL bloquea la fila hasta que la transacción termine.
        
        REQUIERE: Estar dentro de transaction.atomic()
        """
        self._logger.info("Obteniendo producto con bloqueo", producto_id=str(id))
        
        try:
            # SELECT FOR UPDATE: Bloqueo pesimista a nivel de fila
            # Otras transacciones esperarán hasta que esta termine
            model = ProductoModel.objects.select_for_update().get(id=id)
            producto = self._to_domain(model)
            
            self._logger.info(
                "Producto bloqueado para actualización",
                producto_id=str(id),
                stock_actual=producto.stock_actual
            )
            
            return producto
            
        except ProductoModel.DoesNotExist:
            self._logger.warning("Producto no encontrado para bloqueo", producto_id=str(id))
            return None

    def guardar(self, entidad: Producto, categoria_id=None, atributos_adicionales=None) -> Producto:
        producto_id = str(entidad.id)
        self._logger.info(f"Guardando producto", producto_id=producto_id)
        
        # LOG: Mostrar atributos adicionales recibidos
        if atributos_adicionales:
            self._logger.info(f"📦 Atributos adicionales recibidos: {atributos_adicionales}")
        
        try:
            existe = ProductoModel.objects.filter(id=entidad.id).exists()
            accion = "UPDATE" if existe else "CREATE"
            
            # Obtener datos previos para auditoría
            datos_previos = None
            if existe:
                model_anterior = ProductoModel.objects.get(id=entidad.id)
                datos_previos = {
                    "codigo": model_anterior.codigo,
                    "stock": model_anterior.stock_actual,
                    "precio": f"{model_anterior.monto_precio} {model_anterior.moneda_precio}"
                }
                # Actualizar modelo existente
                model_anterior.nombre = entidad.nombre
                model_anterior.descripcion = entidad.descripcion
                model_anterior.moneda_precio = entidad.precio.moneda
                model_anterior.monto_precio = entidad.precio.monto
                model_anterior.stock_actual = entidad.stock_actual
                model_anterior.stock_minimo = entidad.stock_minimo
                model_anterior.cantidad_minima_mayorista = getattr(
                    entidad,
                    'cantidad_minima_mayorista',
                    model_anterior.cantidad_minima_mayorista
                )
                model_anterior.activo = entidad.activo
                # Asignar categoría si se proporciona
                if categoria_id:
                    model_anterior.categoria_id = categoria_id
                # Actualizar atributos adicionales si se proporcionan
                if atributos_adicionales:
                    if 'imagen_principal' in atributos_adicionales:
                        model_anterior.imagen_principal = atributos_adicionales['imagen_principal']
                        self._logger.info(f"🖼️ Imagen asignada: {model_anterior.imagen_principal}")
                    if 'color' in atributos_adicionales:
                        model_anterior.color = atributos_adicionales['color']
                    if 'tipo' in atributos_adicionales:
                        model_anterior.tipo = atributos_adicionales['tipo']
                    if 'largo' in atributos_adicionales:
                        model_anterior.largo = atributos_adicionales['largo']
                    if 'origen' in atributos_adicionales:
                        model_anterior.origen = atributos_adicionales['origen']
                    if 'metodo' in atributos_adicionales:
                        model_anterior.metodo = atributos_adicionales['metodo']
                    if 'calidad' in atributos_adicionales:
                        model_anterior.calidad = atributos_adicionales['calidad']
                    if 'destacado' in atributos_adicionales:
                        model_anterior.destacado = atributos_adicionales['destacado']
                    if 'disponible_b2b' in atributos_adicionales:
                        model_anterior.disponible_b2b = atributos_adicionales['disponible_b2b']
                    if 'porcentaje_descuento_b2b' in atributos_adicionales:
                        model_anterior.porcentaje_descuento_b2b = atributos_adicionales['porcentaje_descuento_b2b']
                    if 'cantidad_minima_mayorista' in atributos_adicionales:
                        model_anterior.cantidad_minima_mayorista = atributos_adicionales['cantidad_minima_mayorista']
                model = model_anterior
            else:
                # Crear nuevo modelo
                model = self._to_model(entidad)
                # Asignar categoría si se proporciona
                if categoria_id:
                    model.categoria_id = categoria_id
                # Asignar atributos adicionales si se proporcionan
                if atributos_adicionales:
                    if 'imagen_principal' in atributos_adicionales:
                        model.imagen_principal = atributos_adicionales['imagen_principal']
                    if 'color' in atributos_adicionales:
                        model.color = atributos_adicionales['color']
                    if 'tipo' in atributos_adicionales:
                        model.tipo = atributos_adicionales['tipo']
                    if 'largo' in atributos_adicionales:
                        model.largo = atributos_adicionales['largo']
                    if 'origen' in atributos_adicionales:
                        model.origen = atributos_adicionales['origen']
                    if 'metodo' in atributos_adicionales:
                        model.metodo = atributos_adicionales['metodo']
                    if 'calidad' in atributos_adicionales:
                        model.calidad = atributos_adicionales['calidad']
                    if 'destacado' in atributos_adicionales:
                        model.destacado = atributos_adicionales['destacado']
                    if 'disponible_b2b' in atributos_adicionales:
                        model.disponible_b2b = atributos_adicionales['disponible_b2b']
                    if 'porcentaje_descuento_b2b' in atributos_adicionales:
                        model.porcentaje_descuento_b2b = atributos_adicionales['porcentaje_descuento_b2b']
                    if 'cantidad_minima_mayorista' in atributos_adicionales:
                        model.cantidad_minima_mayorista = atributos_adicionales['cantidad_minima_mayorista']
            
            model.save()

            if atributos_adicionales and 'variantes' in atributos_adicionales:
                self._sincronizar_variantes(model, atributos_adicionales.get('variantes') or [])

            # Guardar imágenes adicionales si se proporcionan
            if atributos_adicionales and 'imagenes' in atributos_adicionales:
                imagenes = atributos_adicionales.get('imagenes') or []
                imagenes_limpias = [url for url in imagenes if url]

                # Si no hay imagen principal pero sí imágenes, usar la primera
                if not model.imagen_principal and imagenes_limpias:
                    model.imagen_principal = imagenes_limpias[0]
                    model.save(update_fields=['imagen_principal'])

                # Reemplazar galería completa
                ImagenProductoModel.objects.filter(producto=model).delete()

                creadas = set()
                if model.imagen_principal:
                    ImagenProductoModel.objects.create(
                        producto=model,
                        url=model.imagen_principal,
                        es_principal=True,
                        orden=0
                    )
                    creadas.add(model.imagen_principal)

                for idx, url in enumerate(imagenes_limpias):
                    if url in creadas:
                        continue
                    ImagenProductoModel.objects.create(
                        producto=model,
                        url=url,
                        es_principal=False,
                        orden=idx + 1
                    )
            
            datos_nuevos = {
                "codigo": model.codigo,
                "stock": model.stock_actual,
                "precio": f"{model.monto_precio} {model.moneda_precio}"
            }
            
            self._auditoria.registrar(
                entidad_tipo="Producto",
                entidad_id=entidad.id,
                accion=accion,
                datos_previos=datos_previos,
                datos_nuevos=datos_nuevos,
                resultado="EXITO",
                mensaje=f"Producto {accion.lower()}do exitosamente"
            )
            
            model = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes', 'variantes').get(id=model.id)
            return self._to_domain(model)
            
        except Exception as e:
            self._logger.error(f"Error al guardar producto", error=str(e))
            self._auditoria.registrar(
                entidad_tipo="Producto",
                entidad_id=entidad.id,
                accion="SAVE",
                resultado="FALLO",
            )
            raise

    def eliminar(self, id: UUID) -> bool:
        self._logger.info(f"Eliminando producto", producto_id=str(id))
        try:
            model = ProductoModel.objects.get(id=id)
            model.activo = False  # Soft delete
            model.save()
            
            self._auditoria.registrar(
                entidad_tipo="Producto",
                entidad_id=id,
                accion="DELETE",
                resultado="EXITO",
                mensaje="Producto eliminado lógicamente"
            )
            return True
        except ProductoModel.DoesNotExist:
            return False

    def eliminar_permanentemente(self, id: UUID) -> bool:
        """
        Elimina permanentemente un producto de la base de datos (hard delete).
        NO permite eliminar productos con historial de órdenes para preservar integridad de datos.
        """
        self._logger.info(f"Intentando eliminar permanentemente producto", producto_id=str(id))
        try:
            from infrastructure.persistence.django.models import LineaOrdenModel
            
            model = ProductoModel.objects.get(id=id)
            nombre_producto = model.nombre
            
            # Verificar si el producto tiene líneas de orden asociadas
            lineas_count = LineaOrdenModel.objects.filter(producto_id=id).count()
            
            if lineas_count > 0:
                # NO permitir eliminar productos con historial de ventas
                self._logger.warning(
                    f"Intento de eliminar producto con historial de órdenes bloqueado",
                    producto_id=str(id),
                    lineas_count=lineas_count
                )
                self._auditoria.registrar(
                    entidad_tipo="Producto",
                    entidad_id=id,
                    accion="DELETE_PERMANENT_BLOCKED",
                    resultado="RECHAZADO",
                    mensaje=f"Producto '{nombre_producto}' tiene {lineas_count} líneas de orden. No se puede eliminar para preservar historial."
                )
                raise ValueError(
                    f"No se puede eliminar el producto '{nombre_producto}' porque tiene {lineas_count} órdenes asociadas. "
                    f"Los productos con historial de ventas solo pueden desactivarse para preservar la integridad del historial."
                )
            
            # Solo si no tiene órdenes asociadas, eliminar permanentemente
            model.delete()
            
            self._auditoria.registrar(
                entidad_tipo="Producto",
                entidad_id=id,
                accion="DELETE_PERMANENT",
                resultado="EXITO",
                mensaje=f"Producto '{nombre_producto}' eliminado permanentemente de la BD (sin historial de órdenes)"
            )
            return True
        except ProductoModel.DoesNotExist:
            self._logger.warning(f"Intento de eliminar producto inexistente", producto_id=str(id))
            return False

    def existe(self, id: UUID) -> bool:
        return ProductoModel.objects.filter(id=id).exists()

    def obtener_todos(self, limite: int = 100, offset: int = 0) -> List[Producto]:
        self._logger.info(f"Obteniendo todos los productos", limite=limite, offset=offset)
        models = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes', 'variantes').all()[offset:offset + limite]
        return [self._to_domain(model) for model in models]

    # ===== MÉTODOS DE BÚSQUEDA AVANZADA =====
    
    def buscar_con_filtros(self, criterios: CriteriosBusqueda) -> Tuple[List[Producto], int]:
        """
        Búsqueda avanzada con filtros, ordenamiento y paginación.
        """
        self._logger.info("Ejecutando búsqueda con filtros")
        
        queryset = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes')
        filtros = criterios.filtros
        
        # Aplicar filtros de disponibilidad
        if filtros.solo_disponibles:
            queryset = queryset.filter(activo=True)
        if filtros.solo_con_stock:
            queryset = queryset.filter(variantes__stock_actual__gt=0, variantes__activo=True)
        
        # Filtro de texto (búsqueda en nombre y descripción)
        if filtros.texto_busqueda:
            texto = filtros.texto_busqueda
            queryset = queryset.filter(
                Q(nombre__icontains=texto) |
                Q(descripcion__icontains=texto) |
                Q(codigo__icontains=texto)
            )
        
        # Filtros por atributos de cabello
        if filtros.colores:
            queryset = queryset.filter(variantes__color__in=[c.value for c in filtros.colores], variantes__activo=True)
        
        if filtros.tipos:
            queryset = queryset.filter(tipo__in=[t.value for t in filtros.tipos])
        
        if filtros.largos:
            queryset = queryset.filter(variantes__largo__in=[l.value for l in filtros.largos], variantes__activo=True)
        
        if filtros.origenes:
            queryset = queryset.filter(origen__in=[o.value for o in filtros.origenes])
        
        if filtros.metodos:
            queryset = queryset.filter(metodo__in=[m.value for m in filtros.metodos])
        
        if filtros.calidades:
            queryset = queryset.filter(calidad__in=[c.value for c in filtros.calidades])
        
        # Filtros de rango de precio
        if filtros.rango_precio and filtros.rango_precio.esta_definido:
            if filtros.rango_precio.minimo is not None:
                queryset = queryset.filter(variantes__precio_monto__gte=filtros.rango_precio.minimo, variantes__activo=True)
            if filtros.rango_precio.maximo is not None:
                queryset = queryset.filter(variantes__precio_monto__lte=filtros.rango_precio.maximo, variantes__activo=True)
        
        # Filtro de rango de largo
        if filtros.rango_largo and filtros.rango_largo.esta_definido:
            # Convertir largo string a int para comparación
            if filtros.rango_largo.minimo is not None:
                largos_validos = [
                    str(i) for i in range(filtros.rango_largo.minimo, 33)
                ]
                queryset = queryset.filter(variantes__largo__in=largos_validos, variantes__activo=True)
            if filtros.rango_largo.maximo is not None:
                largos_validos = [
                    str(i) for i in range(8, filtros.rango_largo.maximo + 1)
                ]
                queryset = queryset.filter(variantes__largo__in=largos_validos, variantes__activo=True)
        
        # Contar total antes de paginar
        total = queryset.distinct().count()
        
        # Aplicar ordenamiento
        queryset = self._aplicar_ordenamiento(queryset, criterios.orden)
        
        # Aplicar paginación
        queryset = queryset.distinct()[criterios.offset:criterios.offset + criterios.limit]
        
        productos = [self._to_domain(m) for m in queryset]
        
        self._logger.info(
            "Búsqueda completada",
            total=total,
            retornados=len(productos)
        )
        
        return productos, total
    
    def _aplicar_ordenamiento(self, queryset, orden: OrdenProducto):
        """Aplica el ordenamiento según el criterio especificado"""
        ordenamientos = {
            OrdenProducto.RELEVANCIA: ['-destacado', '-total_vendidos', '-fecha_creacion'],
            OrdenProducto.PRECIO_ASC: ['monto_precio'],
            OrdenProducto.PRECIO_DESC: ['-monto_precio'],
            OrdenProducto.NOMBRE_ASC: ['nombre'],
            OrdenProducto.NOMBRE_DESC: ['-nombre'],
            OrdenProducto.MAS_VENDIDOS: ['-total_vendidos', '-valoracion_promedio'],
            OrdenProducto.MEJOR_VALORADOS: ['-valoracion_promedio', '-total_valoraciones'],
            OrdenProducto.MAS_RECIENTES: ['-fecha_creacion'],
            OrdenProducto.STOCK_DISPONIBLE: ['-stock_actual'],
        }
        
        campos = ordenamientos.get(orden, ['-fecha_creacion'])
        return queryset.order_by(*campos)
    
    def obtener_contadores_facetas(
        self,
        texto: Optional[str] = None,
        solo_disponibles: bool = True,
        solo_con_stock: bool = True
    ) -> Dict[str, Any]:
        """
        Obtiene contadores para cada faceta de filtrado.
        """
        self._logger.info("Calculando contadores de facetas")
        
        queryset = ProductoModel.objects.all()
        
        if solo_disponibles:
            queryset = queryset.filter(activo=True)
        if solo_con_stock:
            queryset = queryset.filter(stock_actual__gt=0)
        if texto:
            queryset = queryset.filter(
                Q(nombre__icontains=texto) |
                Q(descripcion__icontains=texto)
            )
        
        contadores = {}
        
        # Contadores por color
        variantes_qs = ProductoVarianteModel.objects.select_related('producto')
        if solo_disponibles:
            variantes_qs = variantes_qs.filter(producto__activo=True)
        if solo_con_stock:
            variantes_qs = variantes_qs.filter(stock_actual__gt=0, activo=True)
        if texto:
            variantes_qs = variantes_qs.filter(
                Q(producto__nombre__icontains=texto) |
                Q(producto__descripcion__icontains=texto)
            )

        colores = variantes_qs.exclude(color__isnull=True).values('color').annotate(
            cantidad=Count('id')
        )
        contadores['colores'] = {c['color']: c['cantidad'] for c in colores}
        
        # Contadores por tipo
        tipos = queryset.exclude(tipo__isnull=True).values('tipo').annotate(
            cantidad=Count('id')
        )
        contadores['tipos'] = {t['tipo']: t['cantidad'] for t in tipos}
        
        # Contadores por largo
        largos = variantes_qs.exclude(largo__isnull=True).values('largo').annotate(
            cantidad=Count('id')
        )
        contadores['largos'] = {l['largo']: l['cantidad'] for l in largos}
        
        # Contadores por origen
        origenes = queryset.exclude(origen__isnull=True).values('origen').annotate(
            cantidad=Count('id')
        )
        contadores['origenes'] = {o['origen']: o['cantidad'] for o in origenes}
        
        # Contadores por método
        metodos = queryset.exclude(metodo__isnull=True).values('metodo').annotate(
            cantidad=Count('id')
        )
        contadores['metodos'] = {m['metodo']: m['cantidad'] for m in metodos}
        
        # Contadores por calidad
        calidades = queryset.exclude(calidad__isnull=True).values('calidad').annotate(
            cantidad=Count('id')
        )
        contadores['calidades'] = {c['calidad']: c['cantidad'] for c in calidades}
        
        # Rango de precios
        precios = variantes_qs.aggregate(
            min_precio=Min('precio_monto'),
            max_precio=Max('precio_monto')
        )
        contadores['precio'] = {
            'min': precios['min_precio'] or Decimal('0'),
            'max': precios['max_precio'] or Decimal('0')
        }
        
        return contadores
    
    def obtener_sugerencias_busqueda(self, texto: str, limite: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene sugerencias de autocompletado.
        """
        self._logger.info("Generando sugerencias de búsqueda", texto=texto)
        
        sugerencias = []
        
        # Buscar en nombres de productos
        productos = ProductoModel.objects.filter(
            nombre__icontains=texto,
            activo=True
        ).values('nombre').distinct()[:limite]
        
        for p in productos:
            nombre = p['nombre']
            # Destacar el texto encontrado
            destacado = nombre.replace(texto, f"<strong>{texto}</strong>")
            sugerencias.append({
                'texto': nombre,
                'tipo': 'producto',
                'destacado': destacado,
                'metadata': {}
            })
        
        # Buscar en atributos (colores, tipos, etc.)
        colores_match = [
            c[1] for c in ProductoModel.COLOR_CHOICES 
            if texto.lower() in c[1].lower()
        ]
        for color in colores_match[:3]:
            sugerencias.append({
                'texto': color,
                'tipo': 'color',
                'destacado': color,
                'metadata': {'filtro': 'color'}
            })
        
        return sugerencias[:limite]
    
    def buscar_productos_rapido(self, texto: str, limite: int = 4) -> List[Producto]:
        """
        Búsqueda rápida para autocompletado con preview de productos.
        """
        modelos = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes').filter(
            Q(nombre__icontains=texto) | Q(codigo__icontains=texto),
            activo=True,
            stock_actual__gt=0
        ).order_by('-total_vendidos')[:limite]
        
        return [self._to_domain(m) for m in modelos]
    
    def obtener_destacados(self, limite: int = 8) -> List[Producto]:
        """Obtiene productos destacados"""
        modelos = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes').filter(
            activo=True,
            destacado=True,
            stock_actual__gt=0
        ).order_by('-total_vendidos')[:limite]
        
        return [self._to_domain(m) for m in modelos]
    
    def obtener_mas_vendidos(self, limite: int = 8) -> List[Producto]:
        """Obtiene los productos más vendidos"""
        modelos = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes').filter(
            activo=True,
            stock_actual__gt=0
        ).order_by('-total_vendidos')[:limite]
        
        return [self._to_domain(m) for m in modelos]
    
    def obtener_nuevos(self, limite: int = 8) -> List[Producto]:
        """Obtiene los productos más recientes"""
        modelos = ProductoModel.objects.select_related('categoria').prefetch_related('imagenes').filter(
            activo=True,
            es_nuevo=True,
            stock_actual__gt=0
        ).order_by('-fecha_creacion')[:limite]
        
        return [self._to_domain(m) for m in modelos]
