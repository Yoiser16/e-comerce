"""
Manejadores de excepciones para FastAPI
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse

from domain.exceptions.dominio import (
    ExcepcionDominio,
    ValorInvalido,
    ReglaNegocioViolada,
    EntidadNoEncontrada,
    EstadoInvalido,
    OperacionNoPermitida
)


async def exception_handler_dominio(request: Request, exc: ExcepcionDominio) -> JSONResponse:
    """
    Manejador de excepciones de dominio.
    Convierte excepciones de dominio en respuestas HTTP apropiadas.
    """
    
    status_map = {
        ValorInvalido: status.HTTP_400_BAD_REQUEST,
        ReglaNegocioViolada: status.HTTP_409_CONFLICT,
        EntidadNoEncontrada: status.HTTP_404_NOT_FOUND,
        EstadoInvalido: status.HTTP_409_CONFLICT,
        OperacionNoPermitida: status.HTTP_403_FORBIDDEN,
    }
    
    # Busca el tipo exacto o una clase base
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    for exc_type, code in status_map.items():
        if isinstance(exc, exc_type):
            status_code = code
            break
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.codigo,
            "mensaje": exc.mensaje,
            "tipo": exc.__class__.__name__
        }
    )
