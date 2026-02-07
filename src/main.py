"""
Punto de entrada principal de la aplicación
"""
import os
import sys
import django
import uvicorn

# Configurar path para que encuentre los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 1. Configurar Django antes de cualquier otra cosa
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infrastructure.config.django_settings")
django.setup()

# 2. Importar dependencias que usan Django
from infrastructure.config.app_config import AppConfig
from infrastructure.logging.logger_service import LoggerService
from interfaces.api.fastapi.app import crear_app

# 3. Configuración Global
config = AppConfig.desde_variables_entorno()
logger = LoggerService("main")
logger.info("Iniciando aplicación", ambiente=config.ambiente)

# 4. Crear Aplicación FastAPI
app = crear_app(config)

def main():
    """
    Función principal de ejecución.
    """
    print("Sistema Empresarial - Clean Architecture")
    print(f"Ambiente: {config.ambiente}")
    print("Iniciando servidor REST...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.debug,
        log_level="info"
    )

if __name__ == "__main__":
    main()
