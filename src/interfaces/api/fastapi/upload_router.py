"""
Router para subida de imágenes de productos
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pathlib import Path
import uuid
from typing import Optional
from .dependencies import get_current_user_admin

router = APIRouter(prefix="/api/v1/upload", tags=["Upload"])

# Configuración de carpeta de uploads
UPLOAD_DIR = Path("static/uploads/productos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/imagen")
async def upload_imagen(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user_admin)
):
    """
    Sube una imagen de producto al servidor.
    Solo accesible para ADMIN y OPERADOR.
    
    Args:
        file: Archivo de imagen (JPG, PNG, WEBP, GIF)
        current_user: Usuario autenticado (inyectado por dependencia)
    
    Returns:
        Dict con URL de la imagen subida
        
    Raises:
        HTTPException 400: Tipo de archivo no permitido o tamaño excedido
        HTTPException 500: Error al guardar el archivo
    """
    
    # Validar extensión
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Usa: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Validar tamaño
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="El archivo no debe superar 5MB"
        )
    
    # Generar nombre único
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Guardar archivo
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar el archivo: {str(e)}"
        )
    
    # Retornar URL relativa
    imagen_url = f"/static/uploads/productos/{unique_filename}"
    
    return {
        "url": imagen_url,
        "imagen_url": imagen_url,
        "filename": unique_filename
    }
