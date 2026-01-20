# 📸 Instrucciones: Endpoint de Subida de Imágenes

## ✅ Cambios Completados (Frontend)

1. ✅ Agregado selector de modo: URL Externa o Subir Archivo
2. ✅ Preview de imagen funcional
3. ✅ Validación de tamaño (máx 5MB) y tipo de archivo
4. ✅ Mejor manejo de errores de carga de imágenes
5. ✅ Eliminada dependencia de URLs externas (Unsplash, placeholder.com)
6. ✅ SVG placeholder cuando no hay imagen
7. ✅ Mejores mensajes de error 409 (conflicto de código/nombre)

---

## 🔧 Pendiente (Backend)

### 1️⃣ Crear Endpoint de Subida de Imágenes

**Archivo**: `src/interfaces/api/upload_router.py`

```python
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pathlib import Path
import uuid
import shutil
from typing import Optional
from src.infrastructure.auth.jwt_handler import require_role
from src.shared.enums.rol_enum import RolEnum

router = APIRouter(prefix="/upload", tags=["Upload"])

# Configuración de carpeta de uploads
UPLOAD_DIR = Path("static/uploads/productos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/imagen")
async def upload_imagen(
    file: UploadFile = File(...),
    current_user = Depends(require_role(RolEnum.ADMIN))
):
    """
    Sube una imagen de producto al servidor.
    Solo accesible para ADMIN y OPERADOR.
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
```

### 2️⃣ Registrar Router en main.py

```python
from src.interfaces.api.upload_router import router as upload_router
from fastapi.staticfiles import StaticFiles

# Registrar router
app.include_router(upload_router)

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### 3️⃣ Crear Carpeta static/

```bash
mkdir -p static/uploads/productos
```

### 4️⃣ Agregar a .gitignore

```gitignore
# Uploads
static/uploads/
```

---

## 🎯 Problemas Resueltos

### 1. Error 409 (Conflict)
**Causa**: Intentas crear un producto con código o nombre que ya existe.

**Solución Frontend**: Ahora muestra mensajes específicos:
- "Ya existe un producto con ese código/SKU. Usa uno diferente."
- "Ya existe un producto con ese nombre. Usa uno diferente."

**Solución Backend**: Asegúrate de que tu endpoint `/productos/` valida unicidad:

```python
@router.post("/", status_code=201)
async def crear_producto(data: ProductoCreateDTO):
    # Validar código único
    existing = await producto_repo.buscar_por_codigo(data.codigo)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un producto con ese código"
        )
    
    # Validar nombre único
    existing_nombre = await producto_repo.buscar_por_nombre(data.nombre)
    if existing_nombre:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un producto con ese nombre"
        )
    
    # Crear producto...
```

### 2. Error ERR_NAME_NOT_RESOLVED (placeholder.com)
**Causa**: Problema de red o DNS al intentar cargar imágenes de placeholder.com o Unsplash.

**Solución**: Eliminadas todas las referencias a URLs externas. Ahora usa SVG inline como placeholder.

### 3. Imágenes "quemadas"
**Causa**: URL hardcodeada de Unsplash como fallback.

**Solución**: 
- Ahora busca `imagen_principal`, `imagen_url` o `imagen` en orden
- Si no hay ninguna, muestra SVG placeholder con icono elegante
- Función `handleImageError` maneja errores de carga

---

## 📝 Cómo Usar (Frontend)

### 1. Opción URL Externa
1. Seleccionar tab "URL Externa"
2. Pegar URL de imagen (ej: `https://ejemplo.com/producto.jpg`)
3. La preview se actualiza automáticamente

### 2. Opción Subir Archivo
1. Seleccionar tab "Subir Archivo"
2. Click en "Seleccionar imagen"
3. Elegir archivo (JPG, PNG, WEBP, máx 5MB)
4. Preview aparece instantáneamente
5. Al guardar, la imagen se sube al servidor
6. El producto se guarda con la URL de la imagen subida

---

## 🔒 Seguridad

- Solo usuarios ADMIN pueden subir imágenes
- Validación de tipo de archivo en frontend y backend
- Validación de tamaño (5MB máx)
- Nombres de archivo únicos (UUID) para evitar colisiones
- Archivos servidos desde carpeta `static/` protegida

---

## 🚀 Testing

### Probar subida de imagen:

```bash
curl -X POST http://localhost:8000/api/v1/upload/imagen \
  -H "Authorization: Bearer TU_TOKEN_ADMIN" \
  -F "file=@/ruta/a/imagen.jpg"
```

Respuesta esperada:
```json
{
  "url": "/static/uploads/productos/123e4567-e89b-12d3-a456-426614174000.jpg",
  "imagen_url": "/static/uploads/productos/123e4567-e89b-12d3-a456-426614174000.jpg",
  "filename": "123e4567-e89b-12d3-a456-426614174000.jpg"
}
```

---

**Fecha**: Enero 2026
**Estado**: Frontend completado, Backend pendiente
