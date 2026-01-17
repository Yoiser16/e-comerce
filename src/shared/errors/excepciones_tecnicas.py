"""
Excepciones técnicas (infraestructura)
Separadas de las excepciones de dominio
"""


class ExcepcionTecnica(Exception):
    """
    Excepción base para errores técnicos/infraestructura.
    
    Diferencia clave con ExcepcionDominio:
    - ExcepcionDominio: violación de reglas de negocio
    - ExcepcionTecnica: problemas técnicos (DB, red, etc.)
    """
    
    def __init__(self, mensaje: str, codigo: str = None, causa: Exception = None):
        self.mensaje = mensaje
        self.codigo = codigo or self.__class__.__name__
        self.causa = causa
        super().__init__(self.mensaje)


class ErrorBaseDatos(ExcepcionTecnica):
    """Error en operaciones de base de datos"""
    pass


class ErrorConexion(ExcepcionTecnica):
    """Error de conexión (DB, API externa, etc.)"""
    pass


class ErrorConfiguracion(ExcepcionTecnica):
    """Error en configuración de la aplicación"""
    pass


class ErrorSerializacion(ExcepcionTecnica):
    """Error en serialización/deserialización"""
    pass


class ErrorIntegracion(ExcepcionTecnica):
    """Error en integración con sistema externo"""
    pass


class ErrorAutenticacion(ExcepcionTecnica):
    """Error de autenticación"""
    pass


class ErrorAutorizacion(ExcepcionTecnica):
    """Error de autorización"""
    pass
