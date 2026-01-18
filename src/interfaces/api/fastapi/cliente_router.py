"""
Router de clientes - FastAPI
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from .dependencies import get_cliente_repository
from domain.repositories.cliente_repository import ClienteRepository

from application.use_cases.cliente_use_cases import (
    CrearClienteUseCase,
    ObtenerClienteUseCase,
    ActualizarClienteUseCase
)
from application.dto.cliente_dto import CrearClienteDTO, ClienteDTO, ActualizarClienteDTO
from domain.exceptions.dominio import ExcepcionDominio

router = APIRouter(prefix="/api/v1/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteDTO, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    datos: CrearClienteDTO,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """
    Crea un nuevo cliente.
    """
    try:
        use_case = CrearClienteUseCase(repo)
        return use_case.ejecutar(datos)
    except ExcepcionDominio as e:
        # El exception handler global lo capturará, 
        # pero también podemos relanzarlo o transformarlo aquí si fuera necesario.
        # Al no capturarlo, dejamos que el middleware de excepciones haga su trabajo.
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cliente_id}", response_model=ClienteDTO)
def obtener_cliente(
    cliente_id: UUID,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """
    Obtiene un cliente por ID.
    """
    try:
        use_case = ObtenerClienteUseCase(repo)
        return use_case.ejecutar(cliente_id)
    except ExcepcionDominio as e:
        raise e


@router.put("/", response_model=ClienteDTO)
def actualizar_cliente(
    datos: ActualizarClienteDTO,
    repo: ClienteRepository = Depends(get_cliente_repository)
):
    """
    Actualiza datos de un cliente.
    """
    try:
        use_case = ActualizarClienteUseCase(repo)
        return use_case.ejecutar(datos)
    except ExcepcionDominio as e:
        raise e
