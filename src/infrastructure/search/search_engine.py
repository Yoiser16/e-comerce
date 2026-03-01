"""
Motor de Búsqueda Avanzado - Estilo Retail Premium (Amazon/MercadoLibre)

Características:
- Normalización de texto (acentos, mayúsculas)
- Tokenización inteligente
- Sinónimos para dominio belleza/cabello
- Ranking por relevancia con pesos
- Fuzzy matching para tolerancia a errores tipográficos
- Búsqueda parcial y por prefijo
"""

import re
import unicodedata
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class CampoBusqueda(Enum):
    """Campos donde buscar con sus pesos de relevancia"""
    NOMBRE = 10.0          # Máxima prioridad
    CODIGO = 8.0           # SKU/código exacto
    CATEGORIA = 6.0        # Categoría del producto
    METODO = 5.0           # Método de aplicación
    DESCRIPCION = 3.0      # Descripción (menos peso)
    TAGS = 4.0             # Tags/etiquetas


@dataclass
class ResultadoBusqueda:
    """Resultado de búsqueda con score de relevancia"""
    producto_id: str
    score: float
    matches: Dict[str, List[str]]  # campo -> palabras que matchearon


class SearchEngine:
    """
    Motor de búsqueda avanzado para e-commerce de belleza.
    
    Implementa algoritmos similares a Amazon/MercadoLibre:
    - TF-IDF simplificado
    - Fuzzy matching con distancia de Levenshtein
    - Sinónimos específicos del dominio
    - Boost por popularidad y stock
    """
    
    # Sinónimos específicos para el dominio de belleza/cabello
    SINONIMOS: Dict[str, Set[str]] = {
        # Extensiones
        'extensiones': {'extension', 'extensión', 'pelo', 'cabello', 'hair', 'extensions'},
        'extension': {'extensiones', 'extensión', 'pelo', 'cabello'},
        'pelo': {'cabello', 'hair', 'extensiones', 'extension'},
        'cabello': {'pelo', 'hair', 'extensiones'},
        
        # Pelucas
        'peluca': {'pelucas', 'wig', 'wigs', 'peruca'},
        'pelucas': {'peluca', 'wig', 'wigs'},
        'wig': {'peluca', 'pelucas', 'wigs'},
        
        # Colores
        'negro': {'black', 'azabache', 'oscuro', 'jet'},
        'rubio': {'blonde', 'rubia', 'dorado', 'golden'},
        'castaño': {'brown', 'marron', 'cafe', 'chocolate'},
        'rojo': {'red', 'pelirrojo', 'cobrizo', 'burgundy'},
        'platino': {'platinum', 'plata', 'gris', 'silver', 'grey'},
        
        # Tipos de cabello
        'natural': {'humano', 'human', 'real', 'remy', 'virgen'},
        'humano': {'natural', 'human', 'real', 'remy'},
        'sintetico': {'artificial', 'synthetic', 'fibra'},
        'kanekalon': {'sintetico', 'fibra', 'trenzas'},
        
        # Métodos de aplicación
        'clip': {'clips', 'clip-in', 'clipin'},
        'tape': {'cinta', 'adhesivo', 'tape-in', 'tapein'},
        'keratina': {'keratin', 'fusion', 'bonding'},
        'microlink': {'micro', 'anillo', 'ring', 'micro-ring'},
        'cosido': {'sew', 'coser', 'sew-in', 'sewin', 'cortina'},
        'frontal': {'frontales', 'lace', 'encaje', 'lace-front'},
        'closure': {'cierre', 'closures', 'top'},
        
        # Largos
        'corto': {'short', 'bob', '10', '12', '14'},
        'mediano': {'medium', '16', '18', '20'},
        'largo': {'long', '22', '24', '26', '28', '30'},
        
        # Texturas
        'liso': {'lacio', 'straight', 'recto'},
        'ondulado': {'wave', 'waves', 'onda', 'body'},
        'rizado': {'curly', 'curl', 'rizo', 'afro'},
        
        # Calidad
        'premium': {'lujo', 'luxury', 'alta', 'top', 'best'},
        'profesional': {'salon', 'pro', 'stylist'},
        
        # Accesorios
        'bonding': {'pegamento', 'glue', 'adhesivo'},
        'remover': {'removedor', 'quitar', 'eliminar'},
        'cuidado': {'care', 'tratamiento', 'shampoo', 'acondicionador'},
    }
    
    # Stopwords en español - palabras a ignorar
    STOPWORDS: Set[str] = {
        'de', 'la', 'el', 'en', 'y', 'a', 'los', 'las', 'un', 'una',
        'para', 'con', 'por', 'del', 'al', 'es', 'su', 'que', 'se',
        'como', 'mas', 'pero', 'sus', 'le', 'ha', 'me', 'si', 'ya',
        'o', 'muy', 'sin', 'sobre', 'este', 'ser', 'entre', 'cuando',
        'todo', 'esta', 'desde', 'son', 'e', 'nos', 'durante', 'hay',
        'ver', 'precio', 'producto', 'productos', 'comprar'
    }
    
    def __init__(self):
        self._sinonimos_invertidos = self._construir_indice_sinonimos()
    
    def _construir_indice_sinonimos(self) -> Dict[str, Set[str]]:
        """Construye índice invertido de sinónimos para búsqueda bidireccional"""
        indice = {}
        for palabra, sinonimos in self.SINONIMOS.items():
            # Agregar la palabra principal
            if palabra not in indice:
                indice[palabra] = set()
            indice[palabra].update(sinonimos)
            indice[palabra].add(palabra)
            
            # Agregar cada sinónimo apuntando al grupo
            for sinonimo in sinonimos:
                if sinonimo not in indice:
                    indice[sinonimo] = set()
                indice[sinonimo].update(sinonimos)
                indice[sinonimo].add(palabra)
        
        return indice
    
    @staticmethod
    def normalizar_texto(texto: str) -> str:
        """
        Normaliza texto para búsqueda:
        - Convierte a minúsculas
        - Elimina acentos
        - Elimina caracteres especiales
        """
        if not texto:
            return ""
        
        # Minúsculas
        texto = texto.lower().strip()
        
        # Eliminar acentos (NFD descompone, luego filtramos marcas diacríticas)
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        
        # Normalizar espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        
        return texto
    
    def tokenizar(self, texto: str, incluir_sinonimos: bool = True) -> List[str]:
        """
        Tokeniza texto en palabras de búsqueda.
        Opcionalmente expande con sinónimos.
        """
        texto_normalizado = self.normalizar_texto(texto)
        
        # Separar por espacios y caracteres especiales
        tokens = re.split(r'[\s\-_,./]+', texto_normalizado)
        
        # Filtrar stopwords y tokens vacíos/cortos
        tokens = [t for t in tokens if t and len(t) >= 2 and t not in self.STOPWORDS]
        
        if not incluir_sinonimos:
            return tokens
        
        # Expandir con sinónimos
        tokens_expandidos = set(tokens)
        for token in tokens:
            if token in self._sinonimos_invertidos:
                tokens_expandidos.update(self._sinonimos_invertidos[token])
        
        return list(tokens_expandidos)
    
    @staticmethod
    def distancia_levenshtein(s1: str, s2: str) -> int:
        """Calcula distancia de edición entre dos strings"""
        if len(s1) < len(s2):
            return SearchEngine.distancia_levenshtein(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        fila_anterior = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            fila_actual = [i + 1]
            for j, c2 in enumerate(s2):
                inserciones = fila_anterior[j + 1] + 1
                eliminaciones = fila_actual[j] + 1
                sustituciones = fila_anterior[j] + (c1 != c2)
                fila_actual.append(min(inserciones, eliminaciones, sustituciones))
            fila_anterior = fila_actual
        
        return fila_anterior[-1]
    
    def match_fuzzy(self, query: str, texto: str, umbral: float = 0.7) -> Tuple[bool, float]:
        """
        Verifica si hay match fuzzy entre query y texto.
        Retorna (hay_match, score_similitud)
        """
        query_norm = self.normalizar_texto(query)
        texto_norm = self.normalizar_texto(texto)
        
        # Match exacto
        if query_norm in texto_norm:
            return True, 1.0
        
        # Match por palabras
        query_tokens = query_norm.split()
        texto_tokens = texto_norm.split()
        
        matches = 0
        for qt in query_tokens:
            for tt in texto_tokens:
                # Match por prefijo (búsqueda mientras escribe)
                if tt.startswith(qt) or qt.startswith(tt):
                    matches += 1
                    break
                # Match fuzzy para palabras largas
                elif len(qt) >= 4 and len(tt) >= 4:
                    distancia = self.distancia_levenshtein(qt, tt)
                    max_len = max(len(qt), len(tt))
                    similitud = 1 - (distancia / max_len)
                    if similitud >= umbral:
                        matches += 1
                        break
        
        if matches == 0:
            return False, 0.0
        
        score = matches / len(query_tokens)
        return score >= 0.5, score
    
    def calcular_score(
        self,
        query_tokens: List[str],
        producto: Dict,
        boost_vendidos: float = 1.0,
        boost_stock: float = 1.0
    ) -> Tuple[float, Dict[str, List[str]]]:
        """
        Calcula score de relevancia para un producto.
        
        Args:
            query_tokens: Tokens de búsqueda (ya expandidos con sinónimos)
            producto: Dict con campos del producto
            boost_vendidos: Multiplicador por popularidad
            boost_stock: Multiplicador por disponibilidad
        
        Returns:
            (score_total, dict_de_matches_por_campo)
        """
        score_total = 0.0
        matches_por_campo = {}
        
        # Campos a buscar con sus pesos
        campos = [
            ('nombre', CampoBusqueda.NOMBRE.value),
            ('codigo', CampoBusqueda.CODIGO.value),
            ('categoria', CampoBusqueda.CATEGORIA.value),
            ('metodo', CampoBusqueda.METODO.value),
            ('descripcion', CampoBusqueda.DESCRIPCION.value),
        ]
        
        for campo, peso in campos:
            valor = producto.get(campo, '') or ''
            valor_norm = self.normalizar_texto(valor)
            
            if not valor_norm:
                continue
            
            matches = []
            for token in query_tokens:
                hay_match, score_match = self.match_fuzzy(token, valor_norm)
                if hay_match:
                    matches.append(token)
                    # Score ponderado por campo y calidad del match
                    score_total += peso * score_match
            
            if matches:
                matches_por_campo[campo] = matches
        
        # Aplicar boosts
        if score_total > 0:
            # Boost por ventas (productos populares)
            ventas = producto.get('total_vendidos', 0) or 0
            if ventas > 0:
                score_total *= (1 + min(ventas / 100, 0.5))  # Max 50% boost
            
            # Boost por stock disponible
            stock = producto.get('stock_actual', 0) or 0
            if stock > 10:
                score_total *= 1.1
            elif stock == 0:
                score_total *= 0.5  # Penalizar sin stock
            
            # Boost por destacado
            if producto.get('destacado'):
                score_total *= 1.2
        
        return score_total, matches_por_campo
    
    def generar_query_sql(self, texto: str) -> Tuple[str, List[str], str]:
        """
        Genera componentes para query SQL avanzado.
        
        Returns:
            (where_clause, parametros, order_clause)
        """
        tokens = self.tokenizar(texto, incluir_sinonimos=True)
        tokens_originales = self.tokenizar(texto, incluir_sinonimos=False)
        
        if not tokens:
            return "", [], ""
        
        # Construir condiciones OR para cada token
        condiciones = []
        params = []
        
        for token in tokens:
            # Búsqueda en múltiples campos
            condiciones.append("""
                (
                    LOWER(UNACCENT(p.nombre)) LIKE %s OR
                    LOWER(UNACCENT(p.codigo)) LIKE %s OR
                    LOWER(UNACCENT(c.nombre)) LIKE %s OR
                    LOWER(UNACCENT(p.metodo)) LIKE %s OR
                    LOWER(UNACCENT(p.descripcion)) LIKE %s
                )
            """)
            like_param = f"%{token}%"
            params.extend([like_param] * 5)
        
        where_clause = " AND ".join([f"({c})" for c in condiciones])
        
        # Ordenamiento por relevancia
        # Priorizar: nombre exacto > nombre contiene > otros campos
        order_parts = []
        for token in tokens_originales[:3]:  # Solo primeros 3 tokens para orden
            order_parts.append(f"""
                CASE 
                    WHEN LOWER(UNACCENT(p.nombre)) = '{token}' THEN 100
                    WHEN LOWER(UNACCENT(p.nombre)) LIKE '{token}%' THEN 80
                    WHEN LOWER(UNACCENT(p.nombre)) LIKE '%{token}%' THEN 60
                    WHEN LOWER(UNACCENT(p.codigo)) = '{token}' THEN 70
                    WHEN LOWER(UNACCENT(c.nombre)) LIKE '%{token}%' THEN 40
                    ELSE 0
                END
            """)
        
        order_clause = " + ".join(order_parts) if order_parts else "p.total_vendidos"
        order_clause = f"({order_clause}) DESC, p.total_vendidos DESC, p.fecha_creacion DESC"
        
        return where_clause, params, order_clause


# Instancia global del motor de búsqueda
search_engine = SearchEngine()
