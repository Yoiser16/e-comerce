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
                'apellido': getattr(user, 'apellido', ''),
                'telefono': getattr(user, 'telefono', ''),
                'whatsapp': getattr(user, 'telefono', ''),  # Usar telefono como whatsapp por ahora
                'empresa': getattr(user, 'nombre_empresa', ''),
                'nit': getattr(user, 'nit_empresa', '') or getattr(user, 'numero_documento', ''),
                'cedula': getattr(user, 'numero_documento', ''),
                'tipo_documento': getattr(user, 'tipo_documento', ''),
                'tipoNegocio': getattr(user, 'tipo_negocio', '') or 'Mayorista',
                'rol': user.rol,
                'tipo': user.tipo,
                'es_mayorista': user.tipo == 'MAYORISTA'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error en login: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al procesar: {str(e)}")

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


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS: Recuperación de Contraseña
# ═══════════════════════════════════════════════════════════════════════════

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    codigo: str
    new_password: str

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """
    Solicita un código de recuperación de contraseña.
    Envía un email con el código al usuario si existe.
    """
    import logging
    logger = logging.getLogger("auth.forgot_password")
    
    from infrastructure.auth.models import Usuario
    from infrastructure.notifications.email_service import send_password_reset_code
    from django.utils import timezone
    import random
    from datetime import timedelta
    
    try:
        user = await sync_to_async(Usuario.objects.get)(email=request.email)
        
        # Generar código de 6 dígitos
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        def save_code():
            user.reset_code = code
            user.reset_code_expires = timezone.now() + timedelta(minutes=15)
            user.save(update_fields=['reset_code', 'reset_code_expires'])
            
        await sync_to_async(save_code)()
        
        # Enviar email — sync_to_async porque es I/O de red (SMTP)
        def do_send_email():
            send_password_reset_code(
                email=user.email,
                nombre=user.nombre,
                codigo=code
            )
        
        await sync_to_async(do_send_email)()
        logger.info(f"Código de recuperación enviado a {user.email}")
        
        return {"message": "Hemos enviado un código de recuperación a tu correo.", "sent": True}
        
    except Usuario.DoesNotExist:
        return {"message": "No encontramos una cuenta con ese correo electrónico.", "sent": False}
    except Exception as e:
        logger.error(f"Error en forgot-password: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al procesar la solicitud")


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """
    Restablece la contraseña usando el código de verificación.
    """
    from infrastructure.auth.models import Usuario
    from django.utils import timezone
    
    try:
        user = await sync_to_async(Usuario.objects.get)(email=request.email)
        
        # Validar código
        if not user.reset_code or user.reset_code != request.codigo:
            raise HTTPException(status_code=400, detail="Código inválido o expirado")
            
        # Validar expiración
        if not user.reset_code_expires or user.reset_code_expires < timezone.now():
            raise HTTPException(status_code=400, detail="El código ha expirado")
            
        def do_reset():
            user.set_password(request.new_password)
            user.reset_code = None
            user.reset_code_expires = None
            user.save()
            
        await sync_to_async(do_reset)()
        
        return {"message": "Contraseña actualizada correctamente. Ya puedes iniciar sesión."}
        
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=400, detail="Solicitud inválida")
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en reset-password: {e}")
        raise HTTPException(status_code=500, detail="Error al restablecer contraseña")


class RegisterRequest(BaseModel):
    nombre: str
    email: EmailStr
    password: str

@router.post("/register", response_model=LoginResponse)
async def register(request: RegisterRequest):
    """
    Registra un nuevo usuario (cliente).
    Los nuevos usuarios se crean con rol LECTURA por defecto.
    """
    from infrastructure.auth.models import Usuario
    from rest_framework_simplejwt.tokens import RefreshToken
    
    # Validaciones
    if len(request.password) < 6:
        raise HTTPException(
            status_code=400, 
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    # Verificar si el email ya existe
    exists = await sync_to_async(Usuario.objects.filter(email=request.email.lower()).exists)()
    if exists:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )
    
    try:
        # Crear usuario
        def create_user():
            user = Usuario.objects.create_user(
                email=request.email.lower(),
                password=request.password,
                nombre=request.nombre,
                rol='LECTURA'
            )
            return user
        
        user = await sync_to_async(create_user)()
        
        # Enviar email de bienvenida
        def send_welcome():
            from infrastructure.notifications.email_service import send_welcome_email
            send_welcome_email(
                email=user.email,
                nombre=user.nombre
            )
        
        # Enviar en background sin bloquear el registro
        try:
            await sync_to_async(send_welcome)()
        except Exception as e:
            # Log pero no fallar el registro si el email falla
            import logging
            logging.getLogger("auth.register").warning(f"Email de bienvenida no enviado: {e}")
        
        # Generar tokens
        def create_tokens():
            refresh = RefreshToken.for_user(user)
            return {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'nombre': user.nombre,
                    'rol': user.rol
                }
            }
        
        tokens = await sync_to_async(create_tokens)()
        return tokens
        
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        raise HTTPException(
            status_code=500,
            detail="No pudimos crear tu cuenta. Intenta de nuevo."
        )


# ===== LOGIN CON CÓDIGO DE ACCESO (Passwordless) =====

class SendLoginCodeRequest(BaseModel):
    email: EmailStr

class VerifyLoginCodeRequest(BaseModel):
    email: EmailStr
    codigo: str

@router.post("/send-login-code")
async def send_login_code(request: SendLoginCodeRequest):
    """
    Envía un código de acceso al email del usuario para login sin contraseña.
    Si el usuario no existe, lo crea automáticamente.
    """
    import logging
    logger = logging.getLogger("auth.login_code")
    
    from infrastructure.auth.models import Usuario
    from django.utils import timezone
    import random
    from datetime import timedelta
    
    try:
        # Buscar o crear usuario
        try:
            user = await sync_to_async(Usuario.objects.get)(email=request.email.lower())
        except Usuario.DoesNotExist:
            # Crear usuario nuevo sin contraseña
            def create_user():
                return Usuario.objects.create(
                    email=request.email.lower(),
                    nombre=request.email.split('@')[0].title(),
                    rol='LECTURA',
                    is_active=True
                )
            user = await sync_to_async(create_user)()
            logger.info(f"Nuevo usuario creado: {user.email}")
        
        # Generar código de 6 dígitos
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        def save_code():
            user.reset_code = code
            user.reset_code_expires = timezone.now() + timedelta(minutes=10)
            user.save(update_fields=['reset_code', 'reset_code_expires'])
            
        await sync_to_async(save_code)()
        
        # Enviar email con el código
        def do_send_email():
            from infrastructure.notifications.email_service import send_login_code_email
            send_login_code_email(
                email=user.email,
                nombre=user.nombre,
                codigo=code
            )
        
        await sync_to_async(do_send_email)()
        logger.info(f"Código de acceso enviado a {user.email}")
        
        return {"message": "Te enviamos un código de acceso a tu correo.", "sent": True}
        
    except Exception as e:
        logger.error(f"Error enviando código de login: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al enviar el código")


@router.post("/verify-login-code", response_model=LoginResponse)
async def verify_login_code(request: VerifyLoginCodeRequest):
    """
    Verifica el código de acceso y devuelve tokens JWT.
    """
    import logging
    logger = logging.getLogger("auth.login_code")
    
    from infrastructure.auth.models import Usuario
    from rest_framework_simplejwt.tokens import RefreshToken
    from django.utils import timezone
    
    try:
        user = await sync_to_async(Usuario.objects.get)(email=request.email.lower())
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=401, detail="Código inválido")
    
    # Verificar código
    def verify():
        if not user.reset_code or user.reset_code != request.codigo:
            return False, "Código inválido"
        if not user.reset_code_expires or user.reset_code_expires < timezone.now():
            return False, "El código ha expirado"
        # Limpiar código después de usar
        user.reset_code = None
        user.reset_code_expires = None
        user.save(update_fields=['reset_code', 'reset_code_expires'])
        return True, None
    
    valid, error_msg = await sync_to_async(verify)()
    if not valid:
        raise HTTPException(status_code=401, detail=error_msg)
    
    # Generar tokens
    def create_tokens():
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access['email'] = user.email
        access['nombre'] = user.nombre
        access['rol'] = user.rol
        
        return {
            'access': str(access),
            'refresh': str(refresh),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'nombre': user.nombre,
                'rol': user.rol
            }
        }
    
    tokens = await sync_to_async(create_tokens)()
    logger.info(f"Login exitoso con código para {user.email}")
    return tokens
