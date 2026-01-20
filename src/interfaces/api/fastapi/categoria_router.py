"""
Router de categorías - FastAPI
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from infrastructure.persistence.django.models import CategoriaModel

router = APIRouter(prefix="/api/v1/categorias", tags=["categorias"])


# DTOs / Schemas
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""
    descripcion_corta: Optional[str] = ""
    imagen: Optional[str] = None
    prioridad: int = 2
    orden: int = 0
    activo: bool = True
    mostrar_en_home: bool = True


class CrearCategoriaDTO(CategoriaBase):
    pass


class ActualizarCategoriaDTO(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    descripcion_corta: Optional[str] = None
    imagen: Optional[str] = None
    prioridad: Optional[int] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None
    mostrar_en_home: Optional[bool] = None


class CategoriaDTO(CategoriaBase):
    id: UUID
    slug: str
    fecha_creacion: datetime
    fecha_modificacion: datetime
    
    class Config:
        from_attributes = True


def categoria_to_dto(cat: CategoriaModel) -> dict:
    """Convierte modelo a diccionario"""
    return {
        "id": str(cat.id),
        "nombre": cat.nombre,
        "slug": cat.slug,
        "descripcion": cat.descripcion,
        "descripcion_corta": cat.descripcion_corta,
        "imagen": cat.imagen,
        "prioridad": cat.prioridad,
        "orden": cat.orden,
        "activo": cat.activo,
        "mostrar_en_home": cat.mostrar_en_home,
        "fecha_creacion": cat.fecha_creacion.isoformat(),
        "fecha_modificacion": cat.fecha_modificacion.isoformat()
    }


@router.get("/", response_model=List[dict])
def listar_categorias(
    solo_activas: bool = False,
    solo_home: bool = False
):
    """
    Lista todas las categorías.
    
    Args:
        solo_activas: Si True, solo devuelve categorías activas
        solo_home: Si True, solo devuelve las que se muestran en home
    """
    try:
        queryset = CategoriaModel.objects.all()
        
        if solo_activas:
            queryset = queryset.filter(activo=True)
        
        if solo_home:
            queryset = queryset.filter(mostrar_en_home=True)
        
        queryset = queryset.order_by('prioridad', 'orden', 'nombre')
        
        return [categoria_to_dto(cat) for cat in queryset]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/home", response_model=List[dict])
def listar_categorias_home():
    """
    Lista categorías para mostrar en el home del ecommerce.
    Solo activas y con mostrar_en_home=True.
    Ordenadas por prioridad.
    """
    try:
        categorias = CategoriaModel.objects.filter(
            activo=True,
            mostrar_en_home=True
        ).order_by('prioridad', 'orden')
        
        return [categoria_to_dto(cat) for cat in categorias]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{categoria_id}", response_model=dict)
def obtener_categoria(categoria_id: UUID):
    """
    Obtiene el detalle de una categoría por su ID.
    """
    try:
        categoria = CategoriaModel.objects.get(id=categoria_id)
        return categoria_to_dto(categoria)
    except CategoriaModel.DoesNotExist:
        raise HTTPException(
            status_code=404, 
            detail="Categoría no encontrada"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_categoria(datos: CrearCategoriaDTO):
    """
    Crea una nueva categoría.
    """
    try:
        from django.utils.text import slugify
        
        # Verificar nombre único
        if CategoriaModel.objects.filter(nombre=datos.nombre).exists():
            raise HTTPException(
                status_code=400,
                detail="Ya existe una categoría con ese nombre"
            )
        
        categoria = CategoriaModel.objects.create(
            nombre=datos.nombre,
            slug=slugify(datos.nombre),
            descripcion=datos.descripcion or "",
            descripcion_corta=datos.descripcion_corta or "",
            imagen=datos.imagen,
            prioridad=datos.prioridad,
            orden=datos.orden,
            activo=datos.activo,
            mostrar_en_home=datos.mostrar_en_home
        )
        
        return categoria_to_dto(categoria)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{categoria_id}", response_model=dict)
def actualizar_categoria(categoria_id: UUID, datos: ActualizarCategoriaDTO):
    """
    Actualiza una categoría existente.
    """
    try:
        from django.utils.text import slugify
        
        categoria = CategoriaModel.objects.get(id=categoria_id)
        
        # Actualizar campos que vienen
        if datos.nombre is not None:
            # Verificar unicidad si cambió el nombre
            if datos.nombre != categoria.nombre:
                if CategoriaModel.objects.filter(nombre=datos.nombre).exclude(id=categoria_id).exists():
                    raise HTTPException(
                        status_code=400,
                        detail="Ya existe una categoría con ese nombre"
                    )
            categoria.nombre = datos.nombre
            categoria.slug = slugify(datos.nombre)
        
        if datos.descripcion is not None:
            categoria.descripcion = datos.descripcion
        if datos.descripcion_corta is not None:
            categoria.descripcion_corta = datos.descripcion_corta
        if datos.imagen is not None:
            categoria.imagen = datos.imagen
        if datos.prioridad is not None:
            categoria.prioridad = datos.prioridad
        if datos.orden is not None:
            categoria.orden = datos.orden
        if datos.activo is not None:
            categoria.activo = datos.activo
        if datos.mostrar_en_home is not None:
            categoria.mostrar_en_home = datos.mostrar_en_home
        
        categoria.save()
        
        return categoria_to_dto(categoria)
    except CategoriaModel.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: UUID):
    """
    Elimina una categoría.
    """
    try:
        categoria = CategoriaModel.objects.get(id=categoria_id)
        categoria.delete()
        return None
    except CategoriaModel.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
