"""
Router para subida de imágenes y videos de productos
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

# Extensiones permitidas para imágenes y videos
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg", ".mov"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS

MAX_IMAGE_SIZE = 5 * 1024 * 1024    # 5MB para imágenes
MAX_VIDEO_SIZE = 20 * 1024 * 1024   # 20MB para videos

@router.post("/imagen")
async def upload_imagen(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user_admin)
):
    """
    Sube una imagen o video de producto al servidor.
    Solo accesible para ADMIN y OPERADOR.
    
    Args:
        file: Archivo de imagen (JPG, PNG, WEBP, GIF) o video (MP4, WEBM, OGG, MOV)
        current_user: Usuario autenticado (inyectado por dependencia)
    
    Returns:
        Dict con URL del archivo subido
        
    Raises:
        HTTPException 400: Tipo de archivo no permitido o tamaño excedido
        HTTPException 500: Error al guardar el archivo
    """
    
    # Validar extensión
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido. Formatos permitidos - Imágenes: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}, Videos: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}"
        )
    
    # Leer contenido del archivo
    content = await file.read()
    
    # Validar tamaño según tipo de archivo
    if file_ext in ALLOWED_IMAGE_EXTENSIONS:
        if len(content) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Las imágenes no deben superar 5MB"
            )
    elif file_ext in ALLOWED_VIDEO_EXTENSIONS:
        if len(content) > MAX_VIDEO_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Los videos no deben superar 20MB"
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
    file_url = f"/static/uploads/productos/{unique_filename}"
    
    return {
        "url": file_url,
        "imagen_url": file_url,  # Mantener compatibilidad con frontend
        "filename": unique_filename
    }
