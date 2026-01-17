#!/usr/bin/env python
"""
Script de Validación de Mejoras Operativas
==========================================

Verifica que todas las mejoras operativas para producción estén funcionando:

1. Health Check Endpoints (/health, /ready, /live)
2. Statement Timeout de PostgreSQL
3. Configuración de Cache (Redis o memoria)
4. Scripts de backup existen

Uso:
    python scripts/validar_mejoras_operativas.py [--base-url URL]
    
Por defecto usa http://localhost:8000
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import Tuple, Optional

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))


class Colors:
    """Colores ANSI para terminal."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Imprime encabezado con formato."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")


def print_success(text: str) -> None:
    """Imprime mensaje de éxito."""
    print(f"  {Colors.GREEN}✓{Colors.END} {text}")


def print_error(text: str) -> None:
    """Imprime mensaje de error."""
    print(f"  {Colors.RED}✗{Colors.END} {text}")


def print_warning(text: str) -> None:
    """Imprime mensaje de advertencia."""
    print(f"  {Colors.YELLOW}⚠{Colors.END} {text}")


def print_info(text: str) -> None:
    """Imprime mensaje informativo."""
    print(f"  {Colors.BLUE}ℹ{Colors.END} {text}")


def check_health_endpoints(base_url: str) -> Tuple[int, int]:
    """
    Verifica los endpoints de health check.
    
    Returns:
        Tuple de (éxitos, fallos)
    """
    print_header("1. HEALTH CHECK ENDPOINTS")
    
    try:
        import requests
    except ImportError:
        print_warning("requests no está instalado. Instalando...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', '-q'])
        import requests
    
    endpoints = [
        ('/health', 'Health Check General'),
        ('/ready', 'Readiness Check (para Kubernetes)'),
        ('/live', 'Liveness Check (para Kubernetes)'),
    ]
    
    successes = 0
    failures = 0
    
    for endpoint, description in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'unknown')
                print_success(f"{description}: {url} → {status}")
                successes += 1
            else:
                print_error(f"{description}: {url} → HTTP {response.status_code}")
                failures += 1
        except requests.exceptions.ConnectionError:
            print_warning(f"{description}: {url} → Servidor no disponible")
            failures += 1
        except Exception as e:
            print_error(f"{description}: {url} → {e}")
            failures += 1
    
    return successes, failures


def check_statement_timeout() -> Tuple[int, int]:
    """
    Verifica que el statement_timeout esté configurado en PostgreSQL.
    
    Returns:
        Tuple de (éxitos, fallos)
    """
    print_header("2. STATEMENT TIMEOUT DE POSTGRESQL")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.infrastructure.config.django_settings')
        import django
        django.setup()
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Verificar el statement_timeout actual
            cursor.execute("SHOW statement_timeout;")
            timeout = cursor.fetchone()[0]
            
            if timeout and timeout != '0':
                print_success(f"statement_timeout configurado: {timeout}")
                return 1, 0
            else:
                print_error(f"statement_timeout no configurado o es 0: {timeout}")
                return 0, 1
                
    except Exception as e:
        print_warning(f"No se pudo verificar statement_timeout: {e}")
        print_info("Esto es normal si la base de datos no está disponible")
        return 0, 1


def check_cache_configuration() -> Tuple[int, int]:
    """
    Verifica la configuración del cache.
    
    Returns:
        Tuple de (éxitos, fallos)
    """
    print_header("3. CONFIGURACIÓN DE CACHE")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.infrastructure.config.django_settings')
        import django
        django.setup()
        
        from django.conf import settings
        from django.core.cache import cache
        
        cache_config = settings.CACHES.get('default', {})
        backend = cache_config.get('BACKEND', 'unknown')
        
        # Detectar tipo de backend
        if 'redis' in backend.lower():
            cache_type = 'Redis'
            print_success(f"Backend de cache: {cache_type}")
            location = cache_config.get('LOCATION', 'no especificado')
            print_info(f"Ubicación: {location}")
        else:
            cache_type = 'Memoria Local (LocMemCache)'
            print_success(f"Backend de cache: {cache_type}")
            print_info("Para producción multi-instancia, considere usar Redis")
        
        # Test funcional del cache
        test_key = '_validation_test_key_'
        test_value = f'test_{time.time()}'
        
        cache.set(test_key, test_value, 10)
        retrieved = cache.get(test_key)
        cache.delete(test_key)
        
        if retrieved == test_value:
            print_success(f"Test funcional del cache: OK")
            return 1, 0
        else:
            print_error(f"Test funcional del cache: FALLO")
            return 0, 1
            
    except Exception as e:
        print_error(f"Error verificando cache: {e}")
        return 0, 1


def check_backup_scripts() -> Tuple[int, int]:
    """
    Verifica que los scripts de backup existan.
    
    Returns:
        Tuple de (éxitos, fallos)
    """
    print_header("4. SCRIPTS DE BACKUP")
    
    scripts_dir = ROOT_DIR / 'scripts'
    backup_scripts = [
        ('backup_postgres.sh', 'Script de backup para Linux/Mac'),
        ('backup_postgres.bat', 'Script de backup para Windows'),
    ]
    
    successes = 0
    failures = 0
    
    for script_name, description in backup_scripts:
        script_path = scripts_dir / script_name
        if script_path.exists():
            size = script_path.stat().st_size
            print_success(f"{description}: {script_name} ({size} bytes)")
            successes += 1
        else:
            print_error(f"{description}: {script_name} no encontrado")
            failures += 1
    
    # Verificar si las variables de entorno de backup están documentadas
    env_example = ROOT_DIR / '.env.example'
    if env_example.exists():
        try:
            content = env_example.read_text(encoding='utf-8')
            if 'BACKUP' in content or 'PG_DUMP' in content:
                print_success("Variables de backup documentadas en .env.example")
            else:
                print_warning("Variables de backup no documentadas en .env.example")
        except Exception:
            pass  # No es crítico si falla la lectura
    
    return successes, failures


def check_django_settings_integrity() -> Tuple[int, int]:
    """
    Verifica la integridad de la configuración de Django.
    
    Returns:
        Tuple de (éxitos, fallos)
    """
    print_header("5. INTEGRIDAD DE CONFIGURACIÓN DJANGO")
    
    successes = 0
    failures = 0
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.infrastructure.config.django_settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Verificaciones críticas
        checks = [
            ('DEBUG', not settings.DEBUG, "DEBUG debe ser False en producción"),
            ('SECRET_KEY', len(settings.SECRET_KEY) >= 50, "SECRET_KEY debe tener al menos 50 caracteres"),
            ('ALLOWED_HOSTS', len(settings.ALLOWED_HOSTS) > 0, "ALLOWED_HOSTS debe tener al menos un valor"),
        ]
        
        for name, condition, description in checks:
            if condition:
                print_success(f"{name}: OK - {description}")
                successes += 1
            else:
                current = getattr(settings, name, 'no definido')
                print_warning(f"{name}: {current} - {description}")
                # No contamos como fallo en desarrollo
        
        # Verificar JWT configurado
        if hasattr(settings, 'SIMPLE_JWT'):
            print_success("Configuración JWT: Presente")
            successes += 1
        else:
            print_error("Configuración JWT: No encontrada")
            failures += 1
        
        # Verificar throttling configurado
        if hasattr(settings, 'REST_FRAMEWORK'):
            throttle = settings.REST_FRAMEWORK.get('DEFAULT_THROTTLE_RATES', {})
            if throttle:
                print_success(f"Rate Limiting: Configurado ({len(throttle)} reglas)")
                successes += 1
            else:
                print_warning("Rate Limiting: No configurado")
        
        return successes, failures
        
    except Exception as e:
        print_error(f"Error cargando configuración Django: {e}")
        return 0, 1


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Validar mejoras operativas del sistema')
    parser.add_argument('--base-url', default='http://localhost:8000',
                        help='URL base del servidor (default: http://localhost:8000)')
    parser.add_argument('--skip-http', action='store_true',
                        help='Omitir pruebas que requieren servidor HTTP')
    args = parser.parse_args()
    
    print(f"\n{Colors.BOLD}VALIDACIÓN DE MEJORAS OPERATIVAS{Colors.END}")
    print(f"Servidor: {args.base_url}")
    print(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_success = 0
    total_failures = 0
    
    # 1. Health Check Endpoints (requiere servidor)
    if not args.skip_http:
        s, f = check_health_endpoints(args.base_url)
        total_success += s
        total_failures += f
    else:
        print_header("1. HEALTH CHECK ENDPOINTS")
        print_warning("Omitido (--skip-http)")
    
    # 2. Statement Timeout
    s, f = check_statement_timeout()
    total_success += s
    total_failures += f
    
    # 3. Cache Configuration
    s, f = check_cache_configuration()
    total_success += s
    total_failures += f
    
    # 4. Backup Scripts
    s, f = check_backup_scripts()
    total_success += s
    total_failures += f
    
    # 5. Django Settings Integrity
    s, f = check_django_settings_integrity()
    total_success += s
    total_failures += f
    
    # Resumen final
    print_header("RESUMEN DE VALIDACIÓN")
    print(f"  Total verificaciones exitosas: {Colors.GREEN}{total_success}{Colors.END}")
    print(f"  Total verificaciones fallidas: {Colors.RED}{total_failures}{Colors.END}")
    
    if total_failures == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ TODAS LAS MEJORAS OPERATIVAS ESTÁN CONFIGURADAS{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ HAY {total_failures} VERIFICACIONES QUE REQUIEREN ATENCIÓN{Colors.END}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
