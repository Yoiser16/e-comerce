"""
Serializers con Pydantic para validación de entrada
"""
# from pydantic import BaseModel, EmailStr, Field, validator
# from typing import Optional
# from uuid import UUID
# from datetime import datetime
#
#
# class ClienteCreateSchema(BaseModel):
#     """Schema para crear un cliente"""
#     nombre: str = Field(..., min_length=2, max_length=100)
#     apellido: str = Field(..., min_length=2, max_length=100)
#     email: EmailStr
#     tipo_documento: str
#     numero_documento: str = Field(..., min_length=5, max_length=50)
#     telefono: Optional[str] = Field(None, min_length=8, max_length=20)
#     
#     class Config:
#         schema_extra = {
#             "example": {
#                 "nombre": "Juan",
#                 "apellido": "Pérez",
#                 "email": "juan.perez@example.com",
#                 "tipo_documento": "DNI",
#                 "numero_documento": "12345678",
#                 "telefono": "+34612345678"
#             }
#         }
#
#
# class ClienteResponseSchema(BaseModel):
#     """Schema de respuesta para cliente"""
#     id: UUID
#     nombre: str
#     apellido: str
#     email: str
#     tipo_documento: str
#     numero_documento: str
#     telefono: Optional[str]
#     activo: bool
#     fecha_creacion: datetime
#     fecha_modificacion: datetime
#     
#     class Config:
#         orm_mode = True

# Punto de extensión: implementar cuando se configure FastAPI
