"""
Modelos Django para la Capa de Persistencia
NOTA: Esta es la capa de infraestructura, separada del dominio
"""
from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from decimal import Decimal


class ClienteModel(models.Model):
    """
    Modelo ORM para Cliente.
    Mapea la entidad de dominio a la base de datos.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=50, unique=True, db_index=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    # Campos de dirección para auto-relleno en próximas compras
    direccion = models.CharField(max_length=255, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    municipio = models.CharField(max_length=100, null=True, blank=True)
    barrio = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['numero_documento']),
            models.Index(fields=['activo', '-fecha_creacion']),
        ]
    
    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido} ({self.email})"


class ProductoModel(models.Model):
    """
    Modelo ORM para Producto de Extensiones de Cabello.
    
    Incluye atributos específicos para:
    - Color, tipo, largo, origen
    - Método de aplicación
    - Calidad del cabello
    - Imágenes y valoraciones
    """
    # Choices para atributos
    COLOR_CHOICES = [
        ('negro_natural', 'Negro Natural'),
        ('negro_azabache', 'Negro Azabache'),
        ('castano_oscuro', 'Castaño Oscuro'),
        ('castano_medio', 'Castaño Medio'),
        ('castano_claro', 'Castaño Claro'),
        ('castano_chocolate', 'Castaño Chocolate'),
        ('rubio_oscuro', 'Rubio Oscuro'),
        ('rubio_medio', 'Rubio Medio'),
        ('rubio_claro', 'Rubio Claro'),
        ('rubio_platino', 'Rubio Platino'),
        ('rubio_cenizo', 'Rubio Cenizo'),
        ('rubio_miel', 'Rubio Miel'),
        ('pelirrojo', 'Pelirrojo'),
        ('cobrizo', 'Cobrizo'),
        ('borgona', 'Borgoña'),
        ('rosa', 'Rosa'),
        ('azul', 'Azul'),
        ('morado', 'Morado'),
        ('verde', 'Verde'),
        ('gris', 'Gris'),
        ('ombre', 'Ombré'),
        ('balayage', 'Balayage'),
        ('highlights', 'Highlights'),
    ]
    
    TIPO_CHOICES = [
        ('liso', 'Liso'),
        ('ondulado', 'Ondulado'),
        ('rizado', 'Rizado'),
        ('afro', 'Afro'),
        ('kinky', 'Kinky'),
        ('body_wave', 'Body Wave'),
        ('deep_wave', 'Deep Wave'),
        ('water_wave', 'Water Wave'),
        ('loose_wave', 'Loose Wave'),
    ]
    
    LARGO_CHOICES = [
        ('8', '8 pulgadas'),
        ('10', '10 pulgadas'),
        ('12', '12 pulgadas'),
        ('14', '14 pulgadas'),
        ('16', '16 pulgadas'),
        ('18', '18 pulgadas'),
        ('20', '20 pulgadas'),
        ('22', '22 pulgadas'),
        ('24', '24 pulgadas'),
        ('26', '26 pulgadas'),
        ('28', '28 pulgadas'),
        ('30', '30 pulgadas'),
        ('32', '32 pulgadas'),
    ]
    
    ORIGEN_CHOICES = [
        ('brasileno', 'Brasileño'),
        ('peruano', 'Peruano'),
        ('indio', 'Indio'),
        ('malayo', 'Malayo'),
        ('camboyano', 'Camboyano'),
        ('mongol', 'Mongol'),
        ('europeo', 'Europeo'),
        ('vietnamita', 'Vietnamita'),
        ('chino', 'Chino'),
        ('ruso', 'Ruso'),
    ]
    
    METODO_CHOICES = [
        ('clip_in', 'Clip-In'),
        ('tape_in', 'Tape-In'),
        ('keratin_bond', 'Keratin Bond'),
        ('micro_link', 'Micro Link'),
        ('sew_in', 'Sew-In'),
        ('fusion', 'Fusión'),
        ('halo', 'Halo'),
        ('ponytail', 'Ponytail'),
        ('bundle', 'Bundle'),
        ('closure', 'Closure'),
        ('frontal', 'Frontal'),
        ('wig', 'Peluca'),
    ]
    
    CALIDAD_CHOICES = [
        ('remy', 'Remy'),
        ('virgin', 'Virgin'),
        ('double_drawn', 'Double Drawn'),
        ('single_drawn', 'Single Drawn'),
        ('raw', 'Raw'),
    ]
    
    # Campos base
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    codigo = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    descripcion_corta = models.CharField(max_length=150, blank=True)
    
    # Categoría (relación con CategoriaModel)
    categoria = models.ForeignKey(
        'CategoriaModel', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='productos',
        db_index=True,
        help_text='Categoría a la que pertenece este producto'
    )
    
    # Precio
    moneda_precio = models.CharField(max_length=3, default='USD')
    monto_precio = models.DecimalField(max_digits=10, decimal_places=2)
    monto_precio_original = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Stock
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    stock_reservado = models.IntegerField(
        default=0,
        help_text='Stock temporalmente reservado por ordenes pendientes'
    )
    
    # Atributos específicos de cabello
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, null=True, blank=True, db_index=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, null=True, blank=True, db_index=True)
    largo = models.CharField(max_length=50, choices=LARGO_CHOICES, null=True, blank=True, db_index=True)
    origen = models.CharField(max_length=50, choices=ORIGEN_CHOICES, null=True, blank=True, db_index=True)
    metodo = models.CharField(max_length=50, choices=METODO_CHOICES, null=True, blank=True, db_index=True)
    calidad = models.CharField(max_length=50, choices=CALIDAD_CHOICES, null=True, blank=True, db_index=True)
    
    # Peso en gramos (importante para extensiones)
    peso_gramos = models.IntegerField(null=True, blank=True)
    
    # Imágenes
    imagen_principal = models.URLField(max_length=500, null=True, blank=True)
    
    # Valoraciones (denormalizadas para performance)
    valoracion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.00'))
    total_valoraciones = models.IntegerField(default=0)
    
    # Contadores de venta (para ordenar por popularidad)
    total_vendidos = models.IntegerField(default=0, db_index=True)
    
    # Flags
    activo = models.BooleanField(default=True)
    es_nuevo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    # Búsqueda full-text (PostgreSQL)
    # search_vector = SearchVectorField(null=True)  # Descomentar si usas PostgreSQL

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['nombre']),
            models.Index(fields=['activo', 'stock_actual']),
            # Índices para filtros
            models.Index(fields=['color', 'activo']),
            models.Index(fields=['tipo', 'activo']),
            models.Index(fields=['largo', 'activo']),
            models.Index(fields=['origen', 'activo']),
            models.Index(fields=['metodo', 'activo']),
            models.Index(fields=['calidad', 'activo']),
            models.Index(fields=['monto_precio', 'activo']),
            # Índices compuestos para búsquedas comunes
            models.Index(fields=['activo', 'stock_actual', '-total_vendidos']),
            models.Index(fields=['activo', 'color', 'tipo']),
        ]

    def __str__(self) -> str:
        return f"{self.nombre} ({self.codigo})"
    
    @property
    def tiene_descuento(self) -> bool:
        """Indica si el producto tiene precio de descuento"""
        return self.monto_precio_original is not None and self.monto_precio_original > self.monto_precio
    
    @property
    def porcentaje_descuento(self) -> int:
        """Calcula el porcentaje de descuento"""
        if not self.tiene_descuento:
            return 0
        return int(((self.monto_precio_original - self.monto_precio) / self.monto_precio_original) * 100)
    
    @property
    def disponible(self) -> bool:
        """Indica si el producto está disponible para venta"""
        return self.activo and self.stock_actual > 0


class ImagenProductoModel(models.Model):
    """
    Modelo para imágenes adicionales de productos.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    producto = models.ForeignKey(ProductoModel, on_delete=models.CASCADE, related_name='imagenes')
    url = models.URLField(max_length=500)
    es_principal = models.BooleanField(default=False)
    orden = models.IntegerField(default=0)
    alt_text = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'imagenes_producto'
        ordering = ['orden']


class CategoriaModel(models.Model):
    """
    Modelo para Categorías de productos.
    
    Incluye:
    - Nombre y descripción
    - Imagen opcional para el ecommerce
    - Prioridad para el diseño (1=grande, 2-3=más pequeño)
    - Estado activo/inactivo
    """
    PRIORIDAD_CHOICES = [
        (1, 'Prioridad Alta (Grande)'),
        (2, 'Prioridad Media'),
        (3, 'Prioridad Baja'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    descripcion = models.TextField(blank=True)
    descripcion_corta = models.CharField(max_length=150, blank=True, help_text='Texto corto para mostrar en tarjetas')
    
    # Imagen para el ecommerce (URLs largas compatibles con Unsplash, etc.)
    imagen = models.URLField(max_length=2000, null=True, blank=True)
    
    # Prioridad para diseño (1=más grande en grid, 2-3=más pequeño)
    prioridad = models.IntegerField(choices=PRIORIDAD_CHOICES, default=2)
    
    # Orden manual dentro del mismo nivel de prioridad
    orden = models.IntegerField(default=0)
    
    # Flags
    activo = models.BooleanField(default=True)
    mostrar_en_home = models.BooleanField(default=True, help_text='Mostrar en página principal')
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['prioridad', 'orden', 'nombre']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['activo', 'prioridad']),
            models.Index(fields=['activo', 'mostrar_en_home', 'prioridad']),
        ]
    
    def __str__(self) -> str:
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class OrdenModel(models.Model):
    """
    Modelo ORM para Orden.
    El cliente siempre es requerido - si no existe, se crea automáticamente.
    """
    # Estados de la orden
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_proceso', 'En Proceso'),
        ('enviada', 'Enviada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    # Métodos de pago
    METODO_PAGO_CHOICES = [
        ('epayco', 'ePayco'),
        ('whatsapp', 'WhatsApp/Asesor'),
        ('transferencia', 'Transferencia'),
        ('contraentrega', 'Contra Entrega'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    # Cliente siempre requerido (se crea automáticamente si no existe)
    cliente = models.ForeignKey(
        ClienteModel, 
        on_delete=models.PROTECT, 
        related_name='ordenes',
        null=True,
        blank=True
    )
    
    # Código único de la orden (ej: KH-1234)
    codigo = models.CharField(max_length=20, unique=True, db_index=True, default='')
    
    # Dirección de envío para esta orden específica
    direccion_envio = models.CharField(max_length=300, default='')
    departamento = models.CharField(max_length=100, default='')
    municipio = models.CharField(max_length=100, default='')
    barrio = models.CharField(max_length=100, blank=True, default='')
    notas_envio = models.TextField(blank=True, default='')
    
    # Estado y método de pago
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default='whatsapp')
    
    # Totales
    subtotal_monto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    envio_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_monto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_moneda = models.CharField(max_length=3, default='COP')
    
    # Email threading (para encadenar notificaciones)
    email_thread_id = models.CharField(max_length=255, blank=True, default='', help_text='Message-ID del primer email enviado')
    
    # Control
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ordenes'
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['cliente']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_creacion']),
            models.Index(fields=['codigo']),
            # Índices compuestos para consultas frecuentes del admin
            models.Index(fields=['estado', '-fecha_creacion']),
            models.Index(fields=['activo', '-fecha_creacion']),
            models.Index(fields=['cliente', '-fecha_creacion']),
            # Índice para ordenar por fecha (desc) - muy usado en listados
            models.Index(fields=['-fecha_creacion', 'estado']),
        ]

    def __str__(self) -> str:
        return f"Orden {self.codigo} - {self.cliente}"


class LineaOrdenModel(models.Model):
    """
    Modelo ORM para Línea de Orden.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    orden = models.ForeignKey(OrdenModel, on_delete=models.CASCADE, related_name='lineas', db_index=True)
    producto = models.ForeignKey(ProductoModel, on_delete=models.PROTECT, related_name='lineas_orden', db_index=True)
    cantidad = models.IntegerField()
    precio_unitario_monto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario_moneda = models.CharField(max_length=3)
    subtotal_monto = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal_moneda = models.CharField(max_length=3)

    class Meta:
        db_table = 'lineas_orden'
        verbose_name = 'Línea de Orden'
        verbose_name_plural = 'Líneas de Orden'
        ordering = ['orden', 'producto']
        indexes = [
            # Índice compuesto para JOINs frecuentes orden+producto
            models.Index(fields=['orden', 'producto']),
            # Índice para búsquedas por orden (ya tiene FK pero reforzamos)
            models.Index(fields=['orden_id']),
        ]

    def __str__(self) -> str:
        return f"{self.cantidad}x {self.producto} en Orden {self.orden_id}"


class RegistroAuditoriaModel(models.Model):
    """
    Modelo ORM para Registro de Auditoría.
    
    Responsabilidades:
    - Trazabilidad inmutable de operaciones críticas
    - Soporte para compliance y forense
    - No se actualiza ni elimina después de crear
    """
    id = models.UUIDField(primary_key=True, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    usuario_id = models.UUIDField(null=True, blank=True)
    entidad_tipo = models.CharField(max_length=50, db_index=True)
    entidad_id = models.UUIDField(db_index=True)
    accion = models.CharField(max_length=20, db_index=True)
    datos_previos = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    resultado = models.CharField(max_length=20)
    mensaje = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'auditoria_registros'
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['entidad_tipo', 'entidad_id']),
            models.Index(fields=['accion', 'timestamp']),
            models.Index(fields=['resultado', 'timestamp']),
            models.Index(fields=['usuario_id', 'timestamp']),
        ]
        # Protección contra modificaciones accidentales
        permissions = [
            ('view_auditoria', 'Can view audit logs'),
        ]

    def __str__(self) -> str:
        return f"Auditoría {self.accion} - {self.entidad_tipo} {self.entidad_id} [{self.resultado}]"
    
    def save(self, *args, **kwargs):
        """Solo permite INSERT, no UPDATE"""
        if self.pk and RegistroAuditoriaModel.objects.filter(pk=self.pk).exists():
            raise ValueError("Los registros de auditoría son inmutables y no pueden actualizarse")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Bloquea eliminación de registros de auditoría"""
        raise ValueError("Los registros de auditoría no pueden eliminarse")


class AuditoriaAccesoAPI(models.Model):
    """
    Registra todos los accesos a la API REST
    
    Propósito:
    - Trazabilidad de autenticación
    - Detección de accesos no autorizados
    - Análisis de uso de la API
    - Compliance y seguridad
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Usuario (null si no autenticado)
    usuario_id = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    
    # Información del request
    endpoint = models.CharField(max_length=200, db_index=True)
    metodo = models.CharField(max_length=10)  # GET, POST, etc.
    
    # Información del cliente
    ip_address = models.CharField(max_length=45)  # IPv4 o IPv6
    user_agent = models.CharField(max_length=200, blank=True)
    
    # Resultado
    resultado_exitoso = models.BooleanField(default=False, db_index=True)
    codigo_estado = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'auditoria_acceso_api'
        verbose_name = 'Auditoría de Acceso API'
        verbose_name_plural = 'Auditorías de Acceso API'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp', 'usuario_id']),
            models.Index(fields=['-timestamp', 'endpoint']),
            models.Index(fields=['-timestamp', 'resultado_exitoso']),
        ]
    
    def __str__(self):
        return f"{self.metodo} {self.endpoint} - {self.timestamp}"


class CarritoModel(models.Model):
    """
    Modelo ORM para Carrito de Compras.
    
    Características Enterprise:
    - Optimistic locking con versión
    - Máquina de estados con transiciones controladas
    - Un solo carrito activo por usuario
    - Snapshot de productos para integridad de precios
    - Auditoría completa
    """
    ESTADO_CHOICES = [
        ('CREADO', 'Creado'),
        ('ACTIVO', 'Activo'),
        ('BLOQUEADO', 'Bloqueado'),
        ('CONFIRMADO', 'Confirmado'),
        ('EXPIRADO', 'Expirado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    usuario_id = models.UUIDField(db_index=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='CREADO', db_index=True)
    
    # Optimistic locking
    version = models.IntegerField(default=1)
    
    # Totales precalculados (server-side only)
    total_bruto_monto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_bruto_moneda = models.CharField(max_length=3, default='USD')
    total_descuentos_monto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_descuentos_moneda = models.CharField(max_length=3, default='USD')
    total_final_monto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_final_moneda = models.CharField(max_length=3, default='USD')
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_expiracion = models.DateTimeField(null=True, blank=True)
    fecha_bloqueo = models.DateTimeField(null=True, blank=True)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    motivo_bloqueo = models.CharField(max_length=100, null=True, blank=True)
    motivo_expiracion = models.CharField(max_length=100, null=True, blank=True)
    
    # Orden generada (si fue confirmado)
    orden_generada_id = models.UUIDField(null=True, blank=True, unique=True)
    
    class Meta:
        db_table = 'carritos'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        ordering = ['-fecha_modificacion']
        indexes = [
            models.Index(fields=['usuario_id', 'estado']),
            models.Index(fields=['estado', '-fecha_modificacion']),
            models.Index(fields=['fecha_expiracion', 'estado']),
        ]
        constraints = [
            # Un solo carrito activo por usuario
            models.UniqueConstraint(
                fields=['usuario_id'],
                condition=models.Q(estado__in=['CREADO', 'ACTIVO', 'BLOQUEADO']),
                name='unique_carrito_activo_por_usuario'
            ),
        ]
    
    def __str__(self) -> str:
        return f"Carrito {self.id} - Usuario {self.usuario_id} [{self.estado}]"


class ItemCarritoModel(models.Model):
    """
    Modelo ORM para Items del Carrito.
    
    Almacena SNAPSHOTS de productos:
    - Precio al momento de agregar
    - Nombre al momento de agregar
    - SKU como referencia
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    carrito = models.ForeignKey(CarritoModel, on_delete=models.CASCADE, related_name='items')
    
    # Referencia al producto
    producto_id = models.UUIDField(db_index=True)
    
    # Snapshots (nunca se actualizan desde catálogo automáticamente)
    sku_snapshot = models.CharField(max_length=50)
    nombre_snapshot = models.CharField(max_length=200)
    precio_unitario_monto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario_moneda = models.CharField(max_length=3, default='USD')
    
    # Cantidad
    cantidad = models.PositiveIntegerField(default=1)
    
    # Subtotal precalculado
    subtotal_monto = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal_moneda = models.CharField(max_length=3, default='USD')
    
    # Timestamps
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'items_carrito'
        verbose_name = 'Item de Carrito'
        verbose_name_plural = 'Items de Carrito'
        ordering = ['fecha_agregado']
        constraints = [
            # No duplicar productos en el mismo carrito
            models.UniqueConstraint(
                fields=['carrito', 'producto_id'],
                name='unique_producto_por_carrito'
            ),
        ]
    
    def __str__(self) -> str:
        return f"{self.cantidad}x {self.nombre_snapshot} en Carrito {self.carrito_id}"
    
    def save(self, *args, **kwargs):
        """Calcula subtotal antes de guardar"""
        self.subtotal_monto = self.precio_unitario_monto * self.cantidad
        self.subtotal_moneda = self.precio_unitario_moneda
        super().save(*args, **kwargs)


class FavoritoModel(models.Model):
    """
    Modelo para productos favoritos de usuarios.
    Permite a los clientes guardar productos para ver después.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    usuario_id = models.UUIDField(db_index=True)  # ID del Usuario autenticado
    producto = models.ForeignKey(ProductoModel, on_delete=models.CASCADE, related_name='favoritos')
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'favoritos'
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        ordering = ['-fecha_agregado']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario_id', 'producto'],
                name='unique_favorito_por_usuario'
            ),
        ]
    
    def __str__(self) -> str:
        return f"Favorito: {self.producto.nombre} - Usuario {self.usuario_id}"


class ProductoVistoModel(models.Model):
    """
    Modelo para historial de productos vistos por usuarios.
    Similar a "Inspirado en lo último que viste" de MercadoLibre.
    Almacena los últimos productos que el usuario ha visto.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    usuario_id = models.UUIDField(db_index=True)  # ID del Usuario (puede ser cliente B2B o retail)
    email = models.EmailField(db_index=True, null=True, blank=True)  # Email como alternativa
    producto = models.ForeignKey(ProductoModel, on_delete=models.CASCADE, related_name='vistos')
    fecha_visto = models.DateTimeField(auto_now=True)  # Se actualiza cada vez que lo ve
    veces_visto = models.PositiveIntegerField(default=1)  # Contador de cuántas veces lo vio
    
    class Meta:
        db_table = 'productos_vistos'
        verbose_name = 'Producto Visto'
        verbose_name_plural = 'Productos Vistos'
        ordering = ['-fecha_visto']
        indexes = [
            models.Index(fields=['usuario_id', '-fecha_visto']),
            models.Index(fields=['email', '-fecha_visto']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['usuario_id', 'producto'],
                name='unique_visto_por_usuario'
            ),
        ]
    
    def registrar_vista(self):
        """Incrementa el contador de vistas y actualiza la fecha"""
        self.veces_visto += 1
        self.save()
    
    def __str__(self) -> str:
        return f"Visto: {self.producto.nombre} - Usuario {self.usuario_id} ({self.veces_visto}x)"
