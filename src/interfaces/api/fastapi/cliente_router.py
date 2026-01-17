"""
Router de clientes - FastAPI
"""
# from fastapi import APIRouter, HTTPException, status, Depends
# from typing import List
# from uuid import UUID
#
# from .base_controller import ControladorBase
# from ....application.use_cases.cliente_use_cases import (
#     CrearClienteUseCase,
#     ObtenerClienteUseCase,
#     ActualizarClienteUseCase
# )
# from ....application.dto.cliente_dto import CrearClienteDTO, ClienteDTO, ActualizarClienteDTO
# from ....domain.exceptions.dominio import ExcepcionDominio
#
# router = APIRouter(prefix="/api/v1/clientes", tags=["clientes"])
#
#
# class ClienteController(ControladorBase):
#     """
#     Controlador de endpoints de Cliente.
#     """
#     pass
#
#
# @router.post("/", response_model=ClienteDTO, status_code=status.HTTP_201_CREATED)
# async def crear_cliente(datos: CrearClienteDTO):
#     """
#     Crea un nuevo cliente.
#     Punto de extensión: inyección de dependencias para use case
#     """
#     try:
#         # use_case = CrearClienteUseCase(cliente_repository)
#         # return use_case.ejecutar(datos)
#         pass
#     except ExcepcionDominio as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
#
#
# @router.get("/{cliente_id}", response_model=ClienteDTO)
# async def obtener_cliente(cliente_id: UUID):
#     """
#     Obtiene un cliente por ID.
#     """
#     try:
#         # use_case = ObtenerClienteUseCase(cliente_repository)
#         # return use_case.ejecutar(cliente_id)
#         pass
#     except ExcepcionDominio as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Punto de extensión: implementar cuando se configure FastAPI y DI
