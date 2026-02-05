"""
Router de Autenticación para FastAPI
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Dict
from asgiref.sync import sync_to_async
import requests
from os import getenv

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

GOOGLE_CLIENT_ID = getenv('VITE_GOOGLE_CLIENT_ID', '')

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access: str
    refresh: str
    user: Dict

class GoogleLoginRequest(BaseModel):
    id_token: str

class RefreshRequest(BaseModel):
    refresh: str

class RefreshResponse(BaseModel):
    access: str

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        from infrastructure.auth.models import Usuario
        from rest_framework_simplejwt.tokens import RefreshToken
        
        try:
            user = await sync_to_async(Usuario.objects.get)(email=request.email)
        except Usuario.DoesNotExist:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        if not await sync_to_async(user.check_password)(request.password):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        
        # Validar estado de mayoristas ANTES de verificar is_active
        # porque cuando se rechaza un mayorista, is_active se pone en False
        if user.tipo == 'MAYORISTA':
            estado = user.estado_mayorista
            if estado == 'PENDIENTE':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu solicitud está pendiente de aprobación. Te notificaremos cuando sea revisada."
                )
            elif estado == 'EN_REVISION':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu solicitud está siendo revisada. Te contactaremos pronto."
                )
            elif estado == 'RECHAZADO':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu solicitud de cuenta mayorista fue rechazada. Contacta a soporte para más información."
                )
            elif estado == 'SUSPENDIDO':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu cuenta de mayorista ha sido suspendida. Contacta a soporte."
                )
            elif estado != 'APROBADO':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu cuenta no está activa. Contacta a soporte."
                )
        
        # Para usuarios no mayoristas, verificar is_active
        if not user.is_active:
            raise HTTPException(status_code=401, detail="Usuario inactivo")
        
        def _gen_tokens():
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            access['email'] = user.email
            access['nombre'] = user.nombre
            access['rol'] = user.rol
            return {'refresh': str(refresh), 'access': str(access)}
        
        tokens = await sync_to_async(_gen_tokens)()
        
        return LoginResponse(
            access=tokens['access'],
            refresh=tokens['refresh'],
            user={
                'id': str(user.id), 
                'email': user.email, 
                'nombre': user.nombre, 
                'rol': user.rol,
                'tipo': user.tipo,
                'es_mayorista': user.tipo == 'MAYORISTA'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"❌ Error en login: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al procesar la solicitud")

@router.post("/login/google", response_model=LoginResponse)
async def login_google(request: GoogleLoginRequest):
    try:
        from infrastructure.auth.models import Usuario
        from rest_framework_simplejwt.tokens import RefreshToken
        
        resp = requests.post('https://oauth2.googleapis.com/tokeninfo', params={'id_token': request.id_token})
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Token Google inválido")
        
        info = resp.json()
        email = info.get('email')
        nombre = info.get('name', 'Usuario Google')
        
        if not email:
            raise HTTPException(status_code=400, detail="Email no encontrado")
        
        async def get_or_create():
            try:
                return await sync_to_async(Usuario.objects.get)(email=email)
            except Usuario.DoesNotExist:
                return await sync_to_async(Usuario.objects.create_user)(
                    email=email, password=getenv('GOOGLE_DEFAULT_PASSWORD', 'GoogleOAuth!'), 
                    nombre=nombre, rol='CLIENTE', is_active=True
                )
        
        user = await get_or_create()
        
        # Validar estado de mayoristas
        if user.tipo == 'MAYORISTA':
            estado = user.estado_mayorista
            if estado == 'PENDIENTE':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu solicitud está pendiente de aprobación. Te notificaremos cuando sea revisada."
                )
            elif estado == 'EN_REVISION':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu solicitud está siendo revisada. Te contactaremos pronto."
                )
            elif estado == 'RECHAZADO':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu solicitud de cuenta mayorista fue rechazada. Contacta a soporte para más información."
                )
            elif estado == 'SUSPENDIDO':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu cuenta de mayorista ha sido suspendida. Contacta a soporte."
                )
            elif estado != 'APROBADO':
                raise HTTPException(
                    status_code=403, 
                    detail="Tu cuenta no está activa. Contacta a soporte."
                )
        
        def _gen_tokens():
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            access['email'] = user.email
            access['nombre'] = user.nombre
            access['rol'] = user.rol
            return {'refresh': str(refresh), 'access': str(access)}
        
        tokens = await sync_to_async(_gen_tokens)()
        
        return LoginResponse(
            access=tokens['access'], refresh=tokens['refresh'],
            user={'id': str(user.id), 'email': user.email, 'nombre': user.nombre, 'rol': user.rol}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(request: RefreshRequest):
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
        def _refresh():
            return str(RefreshToken(request.refresh).access_token)
        return RefreshResponse(access=await sync_to_async(_refresh)())
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/logout")
async def logout():
    return {"mensaje": "Sesión cerrada"}

@router.get("/perfil")
async def get_perfil(user_id: str):
    try:
        from infrastructure.auth.models import Usuario
        user = await sync_to_async(Usuario.objects.get)(id=user_id)
        return {
            'id': str(user.id), 'email': user.email, 'nombre': user.nombre, 'rol': user.rol,
            'es_admin': user.es_admin, 'es_operador': user.es_operador, 'es_lectura': user.es_lectura,
            'puede_escribir': user.puede_escribir, 'puede_eliminar': user.puede_eliminar,
            'fecha_creacion': user.fecha_creacion.isoformat() if user.fecha_creacion else None
        }
    except Exception as e:
        from infrastructure.auth.models import Usuario
        if 'DoesNotExist' in str(type(e)):
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        raise HTTPException(status_code=500, detail=str(e))
