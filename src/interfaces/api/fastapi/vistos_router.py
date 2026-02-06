"""
Router de Productos Vistos - FastAPI

Endpoints para gestionar el historial de productos vistos por usuarios.
Similar a "Inspirado en lo último que viste" de MercadoLibre.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from infrastructure.persistence.django.models import ProductoVistoModel, ProductoModel


router = APIRouter(prefix="/api/v1/productos-vistos", tags=["productos-vistos"])


# === DTOs ===

class ProductoVistoDTO(BaseModel):
    id: UUID
    producto_id: UUID
    nombre: str
    categoria: str | None
    imagen_principal: str | None
    precio: float
    precio_mayorista: float | None
    stock: int
    fecha_visto: datetime
    veces_visto: int
    
    class Config:
        from_attributes = True


class RegistrarVistaRequest(BaseModel):
    producto_id: UUID
    usuario_id: Optional[UUID] = None
    email: Optional[str] = None


class RegistrarVistaResponse(BaseModel):
    message: str
    veces_visto: int


# === Endpoints ===

@router.get("/", response_model=List[ProductoVistoDTO])
def listar_vistos_recientemente(
    email: str,
    limit: int = 10
):
    """
    Lista los productos vistos recientemente por un usuario.
    
    Query Parameters:
    - email: Email del usuario
    - limit: Cantidad máxima de productos (default: 10)
    
    Retorna lista de productos ordenados por fecha de última vista (más reciente primero).
    """
    try:
        vistos = ProductoVistoModel.objects.filter(
            email=email
        ).select_related('producto', 'producto__categoria').order_by('-fecha_visto')[:limit]
        
        resultado = []
        for visto in vistos:
            producto = visto.producto
            if producto and producto.activo:
                resultado.append(ProductoVistoDTO(
                    id=visto.id,
                    producto_id=producto.id,
                    nombre=producto.nombre,
                    categoria=producto.categoria.nombre if producto.categoria else None,
                    imagen_principal=producto.imagen_principal,
                    precio=float(producto.monto_precio or 0),
                    precio_mayorista=float(producto.precio_mayorista) if producto.precio_mayorista else None,
                    stock=producto.stock_actual,
                    fecha_visto=visto.fecha_visto,
                    veces_visto=visto.veces_visto
                ))
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/registrar", response_model=RegistrarVistaResponse)
def registrar_vista(datos: RegistrarVistaRequest):
    """
    Registra que un usuario vio un producto.
    Si ya lo había visto, actualiza la fecha e incrementa el contador.
    
    Request Body:
    - producto_id: UUID del producto
    - usuario_id: UUID del usuario (opcional)
    - email: Email del usuario (requerido si no hay usuario_id)
    """
    try:
        if not datos.usuario_id and not datos.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe proporcionar usuario_id o email"
            )
        
        # Verificar que el producto existe
        try:
            producto = ProductoModel.objects.get(id=datos.producto_id, activo=True)
        except ProductoModel.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        # Buscar si ya existe un registro de vista
        filtro = {'producto': producto}
        if datos.email:
            filtro['email'] = datos.email
        elif datos.usuario_id:
            filtro['usuario_id'] = datos.usuario_id
            
        visto_existente = ProductoVistoModel.objects.filter(**filtro).first()
        
        if visto_existente:
            # Actualizar fecha e incrementar contador
            visto_existente.veces_visto += 1
            visto_existente.save()
            return RegistrarVistaResponse(
                message="Vista actualizada",
                veces_visto=visto_existente.veces_visto
            )
        
        # Crear nuevo registro de vista
        from uuid import uuid4
        nuevo_visto = ProductoVistoModel.objects.create(
            usuario_id=datos.usuario_id or uuid4(),  # Generar UUID si no hay
            email=datos.email,
            producto=producto
        )
        
        return RegistrarVistaResponse(
            message="Vista registrada",
            veces_visto=1
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/limpiar")
def limpiar_historial(email: str):
    """
    Limpia el historial de productos vistos de un usuario.
    """
    try:
        eliminados = ProductoVistoModel.objects.filter(email=email).delete()
        return {"message": f"Historial limpiado", "eliminados": eliminados[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
