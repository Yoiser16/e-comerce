"""
Router de Favoritos - FastAPI

Endpoints para gestionar productos favoritos de usuarios.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from .dependencies import get_current_user_id, get_producto_repository
from infrastructure.persistence.django.models import FavoritoModel, ProductoModel
from domain.repositories.producto_repository import ProductoRepository


router = APIRouter(prefix="/api/v1/favoritos", tags=["favoritos"])


# === DTOs ===

class FavoritoDTO(BaseModel):
    id: UUID
    producto_id: UUID
    nombre: str
    imagen_principal: str | None
    precio_monto: float
    precio_moneda: str
    precio_mayorista: float | None
    sku: str | None
    stock_actual: int
    categoria_nombre: str | None
    fecha_agregado: datetime
    
    class Config:
        from_attributes = True


class AgregarFavoritoRequest(BaseModel):
    producto_id: UUID


class FavoritoResponse(BaseModel):
    message: str
    favorito_id: UUID | None = None


# === Endpoints ===

@router.get("/", response_model=List[FavoritoDTO])
def listar_favoritos(
    usuario_id: UUID = Depends(get_current_user_id)
):
    """
    Lista todos los favoritos del usuario autenticado.
    """
    try:
        favoritos = FavoritoModel.objects.filter(
            usuario_id=usuario_id
        ).select_related('producto')
        
        resultado = []
        for fav in favoritos:
            resultado.append(FavoritoDTO(
                id=fav.id,
                producto_id=fav.producto.id,
                nombre=fav.producto.nombre,
                imagen_principal=fav.producto.imagen_principal,
                precio_monto=float(fav.producto.monto_precio),
                precio_moneda=fav.producto.moneda_precio,
                precio_mayorista=float(fav.producto.precio_mayorista) if fav.producto.precio_mayorista else None,
                sku=fav.producto.sku,
                stock_actual=fav.producto.stock_actual,
                categoria_nombre=fav.producto.categoria.nombre if fav.producto.categoria else None,
                fecha_agregado=fav.fecha_agregado
            ))
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=FavoritoResponse, status_code=status.HTTP_201_CREATED)
def agregar_favorito(
    datos: AgregarFavoritoRequest,
    usuario_id: UUID = Depends(get_current_user_id)
):
    """
    Agrega un producto a favoritos.
    """
    try:
        # Verificar que el producto existe
        try:
            producto = ProductoModel.objects.get(id=datos.producto_id, activo=True)
        except ProductoModel.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        # Verificar si ya está en favoritos
        favorito_existente = FavoritoModel.objects.filter(
            usuario_id=usuario_id,
            producto=producto
        ).first()
        
        if favorito_existente:
            return FavoritoResponse(
                message="El producto ya está en favoritos",
                favorito_id=favorito_existente.id
            )
        
        # Crear favorito
        favorito = FavoritoModel.objects.create(
            usuario_id=usuario_id,
            producto=producto
        )
        
        return FavoritoResponse(
            message="Producto agregado a favoritos",
            favorito_id=favorito.id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{producto_id}", response_model=FavoritoResponse)
def eliminar_favorito(
    producto_id: UUID,
    usuario_id: UUID = Depends(get_current_user_id)
):
    """
    Elimina un producto de favoritos.
    """
    try:
        resultado = FavoritoModel.objects.filter(
            usuario_id=usuario_id,
            producto_id=producto_id
        ).delete()
        
        if resultado[0] == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorito no encontrado"
            )
        
        return FavoritoResponse(message="Producto eliminado de favoritos")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check/{producto_id}")
def verificar_favorito(
    producto_id: UUID,
    usuario_id: UUID = Depends(get_current_user_id)
):
    """
    Verifica si un producto está en favoritos.
    """
    try:
        existe = FavoritoModel.objects.filter(
            usuario_id=usuario_id,
            producto_id=producto_id
        ).exists()
        
        return {"es_favorito": existe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/toggle/{producto_id}", response_model=FavoritoResponse)
def toggle_favorito(
    producto_id: UUID,
    usuario_id: UUID = Depends(get_current_user_id)
):
    """
    Alterna el estado de favorito de un producto.
    Si está en favoritos lo quita, si no está lo agrega.
    """
    try:
        # Verificar si ya está en favoritos
        favorito_existente = FavoritoModel.objects.filter(
            usuario_id=usuario_id,
            producto_id=producto_id
        ).first()
        
        if favorito_existente:
            # Quitar de favoritos
            favorito_existente.delete()
            return FavoritoResponse(message="Producto eliminado de favoritos")
        else:
            # Verificar que el producto existe
            try:
                producto = ProductoModel.objects.get(id=producto_id, activo=True)
            except ProductoModel.DoesNotExist:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Producto no encontrado"
                )
            
            # Agregar a favoritos
            favorito = FavoritoModel.objects.create(
                usuario_id=usuario_id,
                producto=producto
            )
            return FavoritoResponse(
                message="Producto agregado a favoritos",
                favorito_id=favorito.id
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
