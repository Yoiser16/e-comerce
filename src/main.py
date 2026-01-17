"""
Punto de entrada principal de la aplicación
"""
# from infrastructure.config.app_config import AppConfig
# from infrastructure.logging.logger_service import LoggerService
# from interfaces.api.fastapi.app import crear_app
# import uvicorn


def main():
    """
    Bootstrap de la aplicación.
    
    Responsabilidades:
    - Cargar configuración
    - Inicializar servicios
    - Configurar logging
    - Inyectar dependencias
    - Iniciar servidor
    
    Punto de extensión: dependency injection container
    """
    
    # Cargar configuración
    # config = AppConfig.desde_variables_entorno()
    
    # Configurar logging
    # logger = LoggerService("main")
    # logger.info("Iniciando aplicación", ambiente=config.ambiente)
    
    # Crear aplicación FastAPI
    # app = crear_app(config)
    
    # Iniciar servidor
    # uvicorn.run(
    #     app,
    #     host="0.0.0.0",
    #     port=8000,
    #     log_level="info" if not config.debug else "debug"
    # )
    
    print("Sistema Empresarial - Clean Architecture")
    print("Estructura base creada exitosamente")
    print("Pendiente: configurar Django, FastAPI y dependencias")


if __name__ == "__main__":
    main()
