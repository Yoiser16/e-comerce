"""
Health Check Endpoint

Endpoint público para verificar el estado del sistema.
Usado por balanceadores de carga, Kubernetes, y monitoreo.

NO requiere autenticación.
NO expone información sensible.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import connection
from django.core.cache import cache
import time


class HealthCheckView(APIView):
    """
    GET /health
    
    Verifica:
    - Aplicación viva
    - Conectividad a PostgreSQL
    - Cache disponible
    
    Respuestas:
    - 200 OK: Sistema operativo
    - 503 Service Unavailable: Algún componente falló
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # Sin autenticación
    throttle_classes = []  # Sin rate limiting
    
    def get(self, request):
        """
        Health check endpoint
        """
        checks = {
            'status': 'healthy',
            'timestamp': int(time.time()),
            'checks': {}
        }
        
        all_healthy = True
        
        # Check 1: Base de datos PostgreSQL
        db_status = self._check_database()
        checks['checks']['database'] = db_status
        if db_status['status'] != 'healthy':
            all_healthy = False
        
        # Check 2: Cache
        cache_status = self._check_cache()
        checks['checks']['cache'] = cache_status
        if cache_status['status'] != 'healthy':
            # Cache no es crítico, solo warning
            if cache_status['status'] == 'unhealthy':
                checks['checks']['cache']['status'] = 'degraded'
        
        # Determinar estado global
        if not all_healthy:
            checks['status'] = 'unhealthy'
            return Response(checks, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response(checks, status=status.HTTP_200_OK)
    
    def _check_database(self) -> dict:
        """
        Verifica conectividad a PostgreSQL
        """
        try:
            start = time.time()
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
            latency_ms = round((time.time() - start) * 1000, 2)
            
            return {
                'status': 'healthy',
                'latency_ms': latency_ms
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': 'Database connection failed'
                # NO exponer detalles del error
            }
    
    def _check_cache(self) -> dict:
        """
        Verifica que el cache está operativo
        """
        try:
            start = time.time()
            
            # Escribir y leer valor de prueba
            test_key = '_health_check_test'
            test_value = 'ok'
            
            cache.set(test_key, test_value, timeout=10)
            result = cache.get(test_key)
            cache.delete(test_key)
            
            latency_ms = round((time.time() - start) * 1000, 2)
            
            if result == test_value:
                return {
                    'status': 'healthy',
                    'latency_ms': latency_ms,
                    'backend': self._get_cache_backend()
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': 'Cache read/write failed'
                }
                
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': 'Cache unavailable'
            }
    
    def _get_cache_backend(self) -> str:
        """
        Retorna el tipo de backend de cache (sin exponer detalles)
        """
        from django.conf import settings
        backend = settings.CACHES.get('default', {}).get('BACKEND', '')
        
        if 'redis' in backend.lower():
            return 'redis'
        elif 'memcached' in backend.lower():
            return 'memcached'
        elif 'locmem' in backend.lower():
            return 'memory'
        else:
            return 'unknown'


class ReadinessCheckView(APIView):
    """
    GET /ready
    
    Verifica si la aplicación está lista para recibir tráfico.
    Más estricto que /health - verifica que todos los servicios
    estén completamente operativos.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = []
    
    def get(self, request):
        """
        Readiness check - todos los servicios deben estar OK
        """
        checks = {
            'ready': True,
            'timestamp': int(time.time()),
        }
        
        # Verificar base de datos
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
        except Exception:
            checks['ready'] = False
            return Response(checks, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response(checks, status=status.HTTP_200_OK)


class LivenessCheckView(APIView):
    """
    GET /live
    
    Verifica si la aplicación está viva (no colgada).
    Debe ser lo más simple posible - solo indica que el proceso responde.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = []
    
    def get(self, request):
        """
        Liveness check - la aplicación responde
        """
        return Response({'alive': True}, status=status.HTTP_200_OK)
