"""
Constantes de configuración del sistema
"""


class ConfigConstants:
    """Constantes de configuración"""
    
    # Paginación
    LIMITE_PAGINACION_DEFAULT = 50
    LIMITE_PAGINACION_MAXIMO = 500
    
    # Timeouts
    TIMEOUT_DB_SEGUNDOS = 30
    TIMEOUT_API_SEGUNDOS = 10
    
    # Reintentos
    MAX_REINTENTOS_DB = 3
    MAX_REINTENTOS_API = 2
    
    # Cache
    TTL_CACHE_SEGUNDOS = 300  # 5 minutos
    
    # Seguridad
    MIN_LONGITUD_PASSWORD = 8
    MAX_INTENTOS_LOGIN = 5
    TIEMPO_BLOQUEO_MINUTOS = 30


class BusinessConstants:
    """Constantes de negocio"""
    
    # Stock
    STOCK_MINIMO_DEFAULT = 10
    STOCK_CRITICO = 5
    
    # Precios
    PRECIO_MINIMO = 0.01
    MAX_DESCUENTO_PORCENTAJE = 90
    
    # Órdenes
    MAX_LINEAS_POR_ORDEN = 100
    DIAS_VIGENCIA_ORDEN_BORRADOR = 7


class ErrorCodes:
    """Códigos de error estandarizados"""
    
    # Validación
    VALIDACION_FALLO = "VALIDATION_ERROR"
    CAMPO_REQUERIDO = "REQUIRED_FIELD"
    FORMATO_INVALIDO = "INVALID_FORMAT"
    
    # Negocio
    REGLA_NEGOCIO_VIOLADA = "BUSINESS_RULE_VIOLATED"
    ESTADO_INVALIDO = "INVALID_STATE"
    OPERACION_NO_PERMITIDA = "OPERATION_NOT_ALLOWED"
    
    # Recursos
    RECURSO_NO_ENCONTRADO = "RESOURCE_NOT_FOUND"
    RECURSO_YA_EXISTE = "RESOURCE_ALREADY_EXISTS"
    
    # Técnicos
    ERROR_INTERNO = "INTERNAL_ERROR"
    ERROR_BASE_DATOS = "DATABASE_ERROR"
    ERROR_TIMEOUT = "TIMEOUT_ERROR"
