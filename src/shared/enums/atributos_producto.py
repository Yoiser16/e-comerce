"""
Enums para Atributos de Productos de Extensiones de Cabello

Shared Layer - Enumeraciones reutilizables.

Estos enums definen los atributos específicos para productos
de extensiones de cabello humano.
"""
from enum import Enum


class ColorCabello(str, Enum):
    """
    Colores disponibles para extensiones de cabello.
    
    El valor string permite serialización directa a JSON
    y comparación con valores de base de datos.
    """
    # Negros
    NEGRO_NATURAL = "negro_natural"
    NEGRO_AZABACHE = "negro_azabache"
    
    # Castaños
    CASTANO_OSCURO = "castano_oscuro"
    CASTANO_MEDIO = "castano_medio"
    CASTANO_CLARO = "castano_claro"
    CASTANO_CHOCOLATE = "castano_chocolate"
    
    # Rubios
    RUBIO_OSCURO = "rubio_oscuro"
    RUBIO_MEDIO = "rubio_medio"
    RUBIO_CLARO = "rubio_claro"
    RUBIO_PLATINO = "rubio_platino"
    RUBIO_CENIZO = "rubio_cenizo"
    RUBIO_MIEL = "rubio_miel"
    
    # Rojos
    PELIRROJO = "pelirrojo"
    COBRIZO = "cobrizo"
    BORGONA = "borgona"
    
    # Fantasía
    ROSA = "rosa"
    AZUL = "azul"
    MORADO = "morado"
    VERDE = "verde"
    GRIS = "gris"
    
    # Especiales
    OMBRE = "ombre"
    BALAYAGE = "balayage"
    HIGHLIGHTS = "highlights"
    
    @classmethod
    def categorias(cls) -> dict:
        """Agrupa colores por categoría para facetas"""
        return {
            "negros": [cls.NEGRO_NATURAL, cls.NEGRO_AZABACHE],
            "castanos": [cls.CASTANO_OSCURO, cls.CASTANO_MEDIO, cls.CASTANO_CLARO, cls.CASTANO_CHOCOLATE],
            "rubios": [cls.RUBIO_OSCURO, cls.RUBIO_MEDIO, cls.RUBIO_CLARO, cls.RUBIO_PLATINO, cls.RUBIO_CENIZO, cls.RUBIO_MIEL],
            "rojos": [cls.PELIRROJO, cls.COBRIZO, cls.BORGONA],
            "fantasia": [cls.ROSA, cls.AZUL, cls.MORADO, cls.VERDE, cls.GRIS],
            "especiales": [cls.OMBRE, cls.BALAYAGE, cls.HIGHLIGHTS],
        }


class TipoCabello(str, Enum):
    """
    Tipos de textura del cabello.
    """
    LISO = "liso"
    ONDULADO = "ondulado"
    RIZADO = "rizado"
    AFRO = "afro"
    KINKY = "kinky"
    BODY_WAVE = "body_wave"
    DEEP_WAVE = "deep_wave"
    WATER_WAVE = "water_wave"
    LOOSE_WAVE = "loose_wave"


class LargoCabello(str, Enum):
    """
    Largos disponibles en pulgadas.
    
    El valor numérico está en el nombre para facilitar ordenamiento.
    """
    PULGADAS_8 = "8"
    PULGADAS_10 = "10"
    PULGADAS_12 = "12"
    PULGADAS_14 = "14"
    PULGADAS_16 = "16"
    PULGADAS_18 = "18"
    PULGADAS_20 = "20"
    PULGADAS_22 = "22"
    PULGADAS_24 = "24"
    PULGADAS_26 = "26"
    PULGADAS_28 = "28"
    PULGADAS_30 = "30"
    PULGADAS_32 = "32"
    PULGADAS_34 = "34"
    PULGADAS_36 = "36"
    PULGADAS_38 = "38"
    PULGADAS_40 = "40"
    
    @property
    def valor_numerico(self) -> int:
        """Retorna el valor numérico para comparaciones"""
        return int(self.value)
    
    @classmethod
    def rango(cls, min_pulgadas: int, max_pulgadas: int) -> list:
        """Retorna largos dentro de un rango"""
        return [l for l in cls if min_pulgadas <= l.valor_numerico <= max_pulgadas]


class OrigenCabello(str, Enum):
    """
    Origen/procedencia del cabello.
    """
    BRASILENO = "brasileno"
    PERUANO = "peruano"
    INDIO = "indio"
    MALAYO = "malayo"
    CAMBOYANO = "camboyano"
    MONGOL = "mongol"
    EUROPEO = "europeo"
    VIETNAMITA = "vietnamita"
    CHINO = "chino"
    RUSO = "ruso"


class MetodoAplicacion(str, Enum):
    """
    Método de aplicación de las extensiones.
    """
    CLIP_IN = "clip_in"
    TAPE_IN = "tape_in"
    KERATIN_BOND = "keratin_bond"
    MICRO_LINK = "micro_link"
    SEW_IN = "sew_in"
    FUSION = "fusion"
    HALO = "halo"
    PONYTAIL = "ponytail"
    BUNDLE = "bundle"
    CLOSURE = "closure"
    FRONTAL = "frontal"
    WIG = "wig"


class CalidadCabello(str, Enum):
    """
    Niveles de calidad del cabello.
    """
    REMY = "remy"
    VIRGIN = "virgin"
    DOUBLE_DRAWN = "double_drawn"
    SINGLE_DRAWN = "single_drawn"
    RAW = "raw"


class OrdenProducto(str, Enum):
    """
    Opciones de ordenamiento para resultados de búsqueda.
    """
    RELEVANCIA = "relevancia"
    PRECIO_ASC = "precio_asc"
    PRECIO_DESC = "precio_desc"
    NOMBRE_ASC = "nombre_asc"
    NOMBRE_DESC = "nombre_desc"
    MAS_VENDIDOS = "mas_vendidos"
    MEJOR_VALORADOS = "mejor_valorados"
    MAS_RECIENTES = "mas_recientes"
    STOCK_DISPONIBLE = "stock_disponible"
