"""
Dependencias para inyección en FastAPI
"""
from fastapi import Depends
from typing import Generator

from infrastructure.persistence.repositories.cliente_repository_impl import ClienteRepositoryImpl
from domain.repositories.cliente_repository import ClienteRepository
from domain.repositories.producto_repository import ProductoRepository

# --- Repositories ---

def get_cliente_repository() -> Generator[ClienteRepository, None, None]:
    """Provee una instancia de ClienteRepository"""
    try:
        repo = ClienteRepositoryImpl()
        yield repo
    except Exception as e:
        raise e

def get_producto_repository() -> Generator[ProductoRepository, None, None]:
    """Provee una instancia de ProductoRepository"""
    from infrastructure.persistence.repositories.producto_repository_impl import ProductoRepositoryImpl
    try:
        repo = ProductoRepositoryImpl()
        yield repo
    except Exception as e:
        raise e

# --- Services / Otros ---
# Aquí se agregarían otros servicios como EmailService, etc.
