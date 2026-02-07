"""
Modelo de Usuario con Roles para Autenticación y Autorización

IMPORTANTE:
- Este modelo NO es parte del dominio de negocio
- Es infraestructura para seguridad de la API
- NO confundir con Cliente del dominio
- Los clientes del negocio siguen siendo entidades de dominio

TIPOS DE USUARIO:
- STAFF: Personal interno (admin, operadores)
- MAYORISTA: Clientes B2B (distribuidores, requieren aprobación)
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class TipoUsuario(models.TextChoices):
    """
    Tipos de usuario en el sistema
    
    STAFF: Personal interno - accede al admin panel
    MAYORISTA: Clientes B2B - accede al portal mayorista (pro.*)
    """
    STAFF = 'STAFF', 'Staff Interno'
    MAYORISTA = 'MAYORISTA', 'Mayorista'


class RolUsuario(models.TextChoices):
    """
    Roles básicos del sistema para control de acceso (solo STAFF)
    
    ADMIN: Acceso total - crear, modificar, eliminar
    OPERADOR: Operaciones de negocio - crear, modificar
    LECTURA: Solo lectura - consultar
    """
    ADMIN = 'ADMIN', 'Administrador'
    OPERADOR = 'OPERADOR', 'Operador'
    LECTURA = 'LECTURA', 'Solo Lectura'


class EstadoMayorista(models.TextChoices):
    """
    Estados de aprobación para mayoristas
    
    PENDIENTE: Solicitud recibida, esperando revisión
    EN_REVISION: Documentos siendo verificados
    APROBADO: Cuenta activa, puede operar
    RECHAZADO: Solicitud rechazada
    SUSPENDIDO: Cuenta suspendida temporalmente
    """
    PENDIENTE = 'PENDIENTE', 'Pendiente de Revisión'
    EN_REVISION = 'EN_REVISION', 'En Revisión'
    APROBADO = 'APROBADO', 'Aprobado'
    RECHAZADO = 'RECHAZADO', 'Rechazado'
    SUSPENDIDO = 'SUSPENDIDO', 'Suspendido'


class UsuarioManager(BaseUserManager):
    """Manager personalizado para Usuario"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea un usuario normal"""
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea un superusuario (ADMIN)"""
        extra_fields.setdefault('rol', RolUsuario.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Usuario del sistema para autenticación
    
    Soporta dos tipos de usuarios:
    - STAFF: Personal interno (admin panel)
    - MAYORISTA: Clientes B2B (portal mayorista)
    
    NOTA: Este NO es el Cliente retail del dominio.
    - Usuario: Autenticación y autorización (infraestructura)
    - Cliente: Entidad de negocio para retail B2C (dominio)
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150, blank=True, default='')
    
    # Tipo de usuario (STAFF o MAYORISTA)
    tipo = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.STAFF
    )
    
    # Rol (solo aplica para STAFF)
    rol = models.CharField(
        max_length=20,
        choices=RolUsuario.choices,
        default=RolUsuario.LECTURA
    )
    
    # =========================================================================
    # CAMPOS ESPECÍFICOS PARA MAYORISTAS
    # =========================================================================
    telefono = models.CharField(max_length=20, blank=True, default='')
    
    # Documento de identidad
    tipo_documento = models.CharField(max_length=20, blank=True, default='CC')  # CC, NIT, CE
    numero_documento = models.CharField(max_length=50, blank=True, default='', db_index=True)
    
    # Imágenes de verificación (archivos de imagen)
    cedula_frente = models.ImageField(upload_to='cedulas/', blank=True, null=True)
    cedula_dorso = models.ImageField(upload_to='cedulas/', blank=True, null=True)
    
    # Información de empresa (opcional para mayoristas)
    nombre_empresa = models.CharField(max_length=200, blank=True, default='')
    nit_empresa = models.CharField(max_length=50, blank=True, default='')
    
    # Estado de aprobación (solo mayoristas)
    estado_mayorista = models.CharField(
        max_length=20,
        choices=EstadoMayorista.choices,
        default=EstadoMayorista.PENDIENTE,
        blank=True
    )
    
    # Notas de revisión (para el admin)
    notas_revision = models.TextField(blank=True, default='')
    fecha_revision = models.DateTimeField(null=True, blank=True)
    revisado_por = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='revisiones_realizadas'
    )
    
    # Nivel de descuento para mayoristas (porcentaje)
    descuento_mayorista = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        help_text='Porcentaje de descuento para este mayorista'
    )
    
    # =========================================================================
    # CAMPOS DE DIRECCIÓN PARA MAYORISTAS (auto-relleno en compras)
    # =========================================================================
    direccion = models.CharField(max_length=255, blank=True, default='')
    complemento = models.CharField(max_length=50, blank=True, default='', 
                                   help_text='Apartamento, oficina, local, etc.')
    departamento = models.CharField(max_length=100, blank=True, default='')
    departamento_id = models.IntegerField(null=True, blank=True,
                                          help_text='ID del departamento en API Colombia')
    municipio = models.CharField(max_length=100, blank=True, default='')
    municipio_id = models.IntegerField(null=True, blank=True,
                                       help_text='ID del municipio en API Colombia')
    barrio = models.CharField(max_length=100, blank=True, default='')
    indicaciones_entrega = models.CharField(max_length=128, blank=True, default='',
                                            help_text='Indicaciones adicionales para entrega')
    tipo_domicilio = models.CharField(max_length=20, blank=True, default='Residencial',
                                      choices=[('Residencial', 'Residencial'), 
                                               ('Laboral', 'Laboral')])
    # Coordenadas GPS (para geolocalización)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # =========================================================================
    # CAMPOS COMUNES
    # =========================================================================
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_ultima_login = models.DateTimeField(null=True, blank=True)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']
    
    class Meta:
        db_table = 'auth_usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['tipo', 'estado_mayorista']),
            models.Index(fields=['numero_documento']),
        ]
    
    def __str__(self):
        if self.tipo == TipoUsuario.MAYORISTA:
            return f"{self.nombre} {self.apellido} - Mayorista ({self.get_estado_mayorista_display()})"
        return f"{self.email} ({self.get_rol_display()})"
    
    # =========================================================================
    # PROPIEDADES
    # =========================================================================
    
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}".strip()
    
    @property
    def es_staff(self) -> bool:
        """Verifica si es usuario staff (interno)"""
        return self.tipo == TipoUsuario.STAFF
    
    @property
    def es_mayorista(self) -> bool:
        """Verifica si es usuario mayorista"""
        return self.tipo == TipoUsuario.MAYORISTA
    
    @property
    def mayorista_aprobado(self) -> bool:
        """Verifica si el mayorista está aprobado para operar"""
        return self.es_mayorista and self.estado_mayorista == EstadoMayorista.APROBADO
    
    @property
    def mayorista_pendiente(self) -> bool:
        """Verifica si el mayorista está pendiente de aprobación"""
        return self.es_mayorista and self.estado_mayorista in [
            EstadoMayorista.PENDIENTE, 
            EstadoMayorista.EN_REVISION
        ]
    
    @property
    def es_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return self.es_staff and self.rol == RolUsuario.ADMIN
    
    @property
    def es_operador(self) -> bool:
        """Verifica si el usuario es operador"""
        return self.es_staff and self.rol == RolUsuario.OPERADOR
    
    @property
    def es_lectura(self) -> bool:
        """Verifica si el usuario solo tiene permisos de lectura"""
        return self.es_staff and self.rol == RolUsuario.LECTURA
    
    @property
    def puede_escribir(self) -> bool:
        """Verifica si el usuario puede crear/modificar"""
        return self.es_staff and self.rol in [RolUsuario.ADMIN, RolUsuario.OPERADOR]
    
    @property
    def puede_eliminar(self) -> bool:
        """Verifica si el usuario puede eliminar"""
        return self.es_staff and self.rol == RolUsuario.ADMIN
    
    # =========================================================================
    # MÉTODOS
    # =========================================================================
    
    def aprobar_mayorista(self, aprobado_por: 'Usuario', notas: str = ''):
        """Aprueba la solicitud de mayorista"""
        self.estado_mayorista = EstadoMayorista.APROBADO
        self.revisado_por = aprobado_por
        self.notas_revision = notas
        self.fecha_revision = timezone.now()
        self.save()
    
    def rechazar_mayorista(self, rechazado_por: 'Usuario', motivo: str):
        """Rechaza la solicitud de mayorista"""
        self.estado_mayorista = EstadoMayorista.RECHAZADO
        self.revisado_por = rechazado_por
        self.notas_revision = motivo
        self.fecha_revision = timezone.now()
        self.is_active = False
        self.save()
    
    def suspender_mayorista(self, suspendido_por: 'Usuario', motivo: str):
        """Suspende temporalmente la cuenta de mayorista"""
        self.estado_mayorista = EstadoMayorista.SUSPENDIDO
        self.revisado_por = suspendido_por
        self.notas_revision = motivo
        self.fecha_revision = timezone.now()
        self.save()


# =============================================================================
# MODELO DE DIRECCIONES MÚLTIPLES PARA MAYORISTAS
# =============================================================================

class DireccionMayorista(models.Model):
    """
    Permite a los mayoristas tener múltiples direcciones de envío.
    Una puede ser marcada como principal (is_default).
    """
    id = models.AutoField(primary_key=True)
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='direcciones'
    )
    
    # Etiqueta para identificar la dirección (ej: "Casa", "Oficina", "Bodega")
    etiqueta = models.CharField(max_length=50, default='Mi dirección')
    
    # Dirección completa
    direccion = models.CharField(max_length=255)
    complemento = models.CharField(max_length=100, blank=True, default='',
                                   help_text='Apartamento, oficina, local, etc.')
    
    # Ubicación geográfica
    departamento = models.CharField(max_length=100)
    departamento_id = models.IntegerField(null=True, blank=True,
                                          help_text='ID del departamento en API Colombia')
    municipio = models.CharField(max_length=100)
    municipio_id = models.IntegerField(null=True, blank=True,
                                       help_text='ID del municipio en API Colombia')
    barrio = models.CharField(max_length=100, blank=True, default='')
    
    # Indicaciones adicionales
    indicaciones = models.CharField(max_length=200, blank=True, default='',
                                    help_text='Indicaciones para el repartidor')
    
    # Tipo de domicilio
    tipo_domicilio = models.CharField(
        max_length=20, 
        default='Residencial',
        choices=[('Residencial', 'Residencial'), ('Laboral', 'Laboral')]
    )
    
    # Datos de contacto específicos para esta dirección
    nombre_contacto = models.CharField(max_length=100, blank=True, default='')
    telefono = models.CharField(max_length=20)
    
    # Coordenadas GPS
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Flags
    is_default = models.BooleanField(default=False, help_text='¿Es la dirección principal?')
    activa = models.BooleanField(default=True)
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'auth_direcciones_mayorista'
        verbose_name = 'Dirección de Mayorista'
        verbose_name_plural = 'Direcciones de Mayoristas'
        ordering = ['-is_default', '-fecha_creacion']
    
    def __str__(self):
        return f"{self.etiqueta} - {self.direccion}, {self.municipio}"
    
    def save(self, *args, **kwargs):
        # Si se marca como default, quitar default de las otras direcciones del usuario
        if self.is_default:
            DireccionMayorista.objects.filter(
                usuario=self.usuario, 
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
