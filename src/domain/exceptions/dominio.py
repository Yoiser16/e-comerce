"""
Excepciones de dominio
"""


class ExcepcionDominio(Exception):
    """
    Excepción base para todas las excepciones del dominio.
    
    Responsabilidades:
    - Representar violaciones de reglas de negocio
    - Separar errores de dominio de errores técnicos
    - Facilitar manejo específico de errores
    """
    
    def __init__(self, mensaje: str, codigo: str = None):
        self.mensaje = mensaje
        self.codigo = codigo or self.__class__.__name__
        super().__init__(self.mensaje)


class ValorInvalido(ExcepcionDominio):
    """
    Se lanza cuando un valor no cumple con las reglas de validación.
    Uso típico: validación de Value Objects
    """
    pass


class ReglaNegocioViolada(ExcepcionDominio):
    """
    Se lanza cuando se viola una regla de negocio.
    Uso típico: validaciones en entidades, políticas
    """
    pass


class EntidadNoEncontrada(ExcepcionDominio):
    """
    Se lanza cuando no se encuentra una entidad esperada.
    Uso típico: búsqueda por ID en repositorios
    """
    pass


class EstadoInvalido(ExcepcionDominio):
    """
    Se lanza cuando una transición de estado no es válida.
    Uso típico: máquinas de estado
    """
    pass


class OperacionNoPermitida(ExcepcionDominio):
    """
    Se lanza cuando una operación no está permitida en el contexto actual.
    Uso típico: validaciones de permisos de dominio
    """
    pass
