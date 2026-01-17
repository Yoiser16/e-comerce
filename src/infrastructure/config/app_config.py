"""
Configuración de la aplicación
"""
from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    host: str
    port: int
    database: str
    username: str
    password: str
    engine: str = "mysql"  # mysql, postgresql, etc.


@dataclass
class LoggingConfig:
    """Configuración de logging"""
    nivel: str = "INFO"
    formato: str = "json"
    archivo: Optional[str] = None


@dataclass
class AppConfig:
    """
    Configuración centralizada de la aplicación.
    
    Responsabilidades:
    - Centralizar configuración
    - Validar configuración al inicio
    - Separar entornos (dev, staging, prod)
    
    Punto de extensión: integración con servicios de configuración externa
    """
    ambiente: str
    debug: bool
    secret_key: str
    database: DatabaseConfig
    logging: LoggingConfig
    
    @classmethod
    def desde_variables_entorno(cls) -> 'AppConfig':
        """Carga configuración desde variables de entorno"""
        
        ambiente = os.getenv("AMBIENTE", "development")
        
        database_config = DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            database=os.getenv("DB_NAME", "empresa_db"),
            username=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            engine=os.getenv("DB_ENGINE", "mysql")
        )
        
        logging_config = LoggingConfig(
            nivel=os.getenv("LOG_LEVEL", "INFO"),
            formato=os.getenv("LOG_FORMAT", "json"),
            archivo=os.getenv("LOG_FILE")
        )
        
        return cls(
            ambiente=ambiente,
            debug=ambiente == "development",
            secret_key=os.getenv("SECRET_KEY", "dev-secret-key-change-in-production"),
            database=database_config,
            logging=logging_config
        )
