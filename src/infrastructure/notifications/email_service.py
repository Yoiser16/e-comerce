"""
Servicio de notificaciones por email para cambios de estado de órdenes.
"""
from typing import Optional, List, Dict
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.utils import make_msgid
import time

# Mapeo de estados a texto amigable
ESTADO_HUMANO = {
    "pendiente": "pendiente de confirmación",
    "confirmada": "aprobada",
    "en_proceso": "en proceso",
    "enviada": "enviada",
    "completada": "completada",
    "cancelada": "cancelada",
}

# Mapeo de títulos para emails según estado
def _get_email_title(estado: str, codigo: str) -> str:
    """Generar título del email según el estado de la orden."""
    if estado == "pendiente":
        return f"SOLICITUD DE PEDIDO REGISTRADA #{codigo}"
    elif estado == "confirmada":
        return f"PEDIDO CONFIRMADO #{codigo}"
    elif estado == "en_proceso":
        return f"PEDIDO EN PROCESO #{codigo}"
    elif estado == "enviada":
        return f"PEDIDO ENVIADO #{codigo}"
    elif estado == "completada":
        return f"PEDIDO COMPLETADO #{codigo}"
    elif estado == "cancelada":
        return f"PEDIDO CANCELADO #{codigo}"
    else:
        return f"ESTADO DE PEDIDO #{codigo}"


def _build_subject(codigo: str, estado: str) -> str:
    estado_texto = ESTADO_HUMANO.get(estado, estado)
    return f"Tu orden {codigo} está {estado_texto}"


def _build_body(
    cliente: str, 
    codigo: str, 
    estado: str, 
    total: float, 
    direccion: str,
    productos: Optional[List[Dict]] = None
) -> tuple[str, str]:
    estado_texto = ESTADO_HUMANO.get(estado, estado)
    total_str = f"${total:,.0f} COP".replace(",", ".")
    
    # Texto plano
    if estado == "cancelada":
        text = (
            f"Hola {cliente},\n\n"
            f"Te informamos que tu orden {codigo} fue *{estado_texto}*.\n"
            f"Total: {total_str}\n"
            f"Dirección de entrega: {direccion}\n\n"
            "Si tienes dudas o necesitas ayuda, contáctanos."
        )
    else:
        text = (
            f"Hola {cliente},\n\n"
            f"Tu orden {codigo} ahora está *{estado_texto}*.\n"
            f"Total: {total_str}\n"
            f"Dirección de entrega: {direccion}\n\n"
            "Gracias por comprar con Kharis Distribuidora."
        )
    
    # HTML Estilo Floral - Kharis Distribuidora
    
    # Filas de productos
    filas_productos = ""
    if productos:
        for p in productos:
            nombre = p.get('nombre', 'Producto')
            cantidad = p.get('cantidad', 1)
            # Asumimos que el precio no viene en el dict de productos por defecto en la lógica anterior,
            # pero si estuviera, lo usamos. Si no, dejamos un placeholder o lo calculamos si es posible.
            # Ajuste: La lógica original no pasaba precio unitario en 'productos', solo nombre y cantidad.
            # Sin modificar lógica (backend), no tengo el precio unitario aquí. 
            # Usaré "$-" para indicar que no tengo el dato, o lo omitiré si no es crítico, 
            # pero el diseño lo pide. Asumiré que en el futuro se pasará o pondré un placeholder visual.
            # Para cumplir "no toques lógica", mostraré solo lo que hay disponible visualmente.
            precio_unit = p.get('precio_unitario', 0) 
            precio_fmt = f"${precio_unit:,.0f}" if precio_unit else "$-"
            
            filas_productos += f"""
            <tr>
                <td style="padding: 12px 0; border-bottom: 1px solid #eee; color: #333;">{nombre}</td>
                <td style="padding: 12px 0; border-bottom: 1px solid #eee; color: #333; text-align: center;">{cantidad}</td>
                <td style="padding: 12px 0; border-bottom: 1px solid #eee; color: #333; text-align: right;">{precio_fmt}</td>
            </tr>
            """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #F3F4F6; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 40px 20px; }}
            .card {{ background: #ffffff; border-radius: 16px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ width: 120px; margin-bottom: 10px; }}
            .brand-name {{ color: #D81B60; font-size: 24px; font-weight: bold; letter-spacing: 1px; margin: 0; }}
            .brand-subtitle {{ color: #D81B60; font-size: 14px; font-style: italic; margin-top: 0; }}
            .order-title {{ text-align: center; font-size: 20px; font-weight: bold; margin: 30px 0 20px; color: #111; letter-spacing: 0.5px; }}
            .info-text {{ color: #444; font-size: 15px; line-height: 1.5; margin-bottom: 25px; }}
            .product-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
            .product-table th {{ text-align: left; color: #888; font-size: 12px; font-weight: bold; padding-bottom: 10px; border-bottom: 2px solid #eee; text-transform: uppercase; }}
            .total-section {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #f3f3f3; }}
            .total-label {{ font-size: 14px; color: #666; margin-bottom: 5px; }}
            .total-amount {{ font-size: 28px; font-weight: 800; color: #111; letter-spacing: -0.5px; }}
            .footer {{ text-align: center; margin-top: 40px; color: #9CA3AF; font-size: 13px; }}
            .footer-links {{ display: flex; justify-content: center; gap: 20px; margin-top: 10px; }}
            .footer-link {{ display: flex; align-items: center; gap: 6px; color: #6B7280; text-decoration: none; }}
        </style>
    </head>
    <body style="background-color: #F3F4F6;">
        <div class="container">
            <!-- Header Logo (Simulado para ejemplo, idealmente usar URL real) -->
            <div class="header">
                 <!-- Placeholder de Logo Floral -->
                 <img src="https://i.ibb.co/wzr84d1c/kharis-logo-placeholder.png" alt="Kharis Distribuidora" style="width: 150px; height: auto;" />
            </div>

            <div class="order-title">
                {_get_email_title(estado, codigo)}
            </div>

            <div class="card">
                <p class="info-text">
                    Hola, <strong>{cliente}</strong>.<br>
                    {"Te informamos que tu pedido fue" if estado == "cancelada" else "Gracias por tu compra. Tu pedido está"}
                    <strong>{estado_texto}</strong>.
                </p>

                <table class="product-table">
                    <thead>
                        <tr>
                            <th style="width: 60%;">Producto</th>
                            <th style="width: 15%; text-align: center;">Cant.</th>
                            <th style="width: 25%; text-align: right;">Precio</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_productos}
                    </tbody>
                </table>

                <div class="total-section">
                    <div class="total-amount">TOTAL A PAGAR: {total_str}</div>
                </div>
            </div>

            <div class="footer">
                <div class="footer-links" style="text-align: center;">
                    <span style="margin: 0 10px;">📸 @KharisDistribuidora</span>
                    <span style="margin: 0 10px;">📍 Bello, Antioquia</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return text, html


def _build_b2b_status_body(nombre: str, estado: str, notas: str = "") -> tuple[str, str]:
    """Genera el cuerpo del email para cambios de estado B2B."""
    estado_titulo = {
        "APROBADO": "¡Tu cuenta mayorista ha sido APROBADA!",
        "RECHAZADO": "Actualización sobre tu solicitud mayorista",
        "SUSPENDIDO": "Aviso importante sobre tu cuenta mayorista"
    }.get(estado, "Actualización de estado")
    
    color_estado = {
        "APROBADO": "#10B981",  # Emerald 500
        "RECHAZADO": "#EF4444", # Red 500
        "SUSPENDIDO": "#F59E0B" # Amber 500
    }.get(estado, "#6B7280")

    mensaje_principal = ""
    accion_boton = ""
    
    if estado == "APROBADO":
        mensaje_principal = (
            f"Nos complace informarte que tu solicitud para ser Mayorista en Kharis Distribuidora ha sido <strong>APROBADA</strong>.<br><br>"
            "Ya puedes acceder al portal B2B con tu correo y contraseña para disfrutar de precios exclusivos."
        )
        accion_boton = '<a href="http://pro.localhost:5173/portal/login" style="display: inline-block; background-color: #C9A962; color: #000; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold;">Ingresar al Portal</a>'
    elif estado == "RECHAZADO":
        mensaje_principal = (
            "Hemos revisado tu solicitud para cuenta mayorista y lamentamos informarte que no ha sido aprobada en esta ocasión.<br><br>"
            f"<strong>Motivo:</strong> {notas or 'No especificado'}<br><br>"
            "Si crees que esto es un error o deseas rectificar información, por favor responde a este correo."
        )
    elif estado == "SUSPENDIDO":
        mensaje_principal = (
            "Tu cuenta de mayorista ha sido suspendida temporalmente.<br><br>"
            f"<strong>Motivo:</strong> {notas or 'Incumplimiento de términos'}<br><br>"
            "Por favor contáctanos para resolver esta situación."
        )

    text = f"Hola {nombre},\n\n{estado_titulo}\n\n{mensaje_principal.replace('<br>', '\n').replace('<strong>', '').replace('</strong>', '')}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #F3F4F6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                 <img src="https://i.ibb.co/wzr84d1c/kharis-logo-placeholder.png" alt="Kharis Distribuidora" style="width: 120px; height: auto;" />
            </div>
            
            <div style="background: #ffffff; border-radius: 16px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: {color_estado}; margin: 0; font-size: 24px;">{estado_titulo}</h2>
                </div>
                
                <p style="color: #444; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                    Hola <strong>{nombre}</strong>,<br><br>
                    {mensaje_principal}
                </p>
                
                <div style="text-align: center; margin-top: 30px;">
                    {accion_boton}
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px; color: #9CA3AF; font-size: 13px;">
                <p>© Kharis Distribuidora B2B</p>
            </div>
        </div>
    </body>
    </html>
    """
    return text, html


def _build_recovery_body(nombre: str, codigo: str) -> tuple[str, str]:
    """Genera el cuerpo del email para recuperación de contraseña."""
    text = (
        f"Hola {nombre},\n\n"
        f"Hemos recibido una solicitud para restablecer tu contraseña.\n"
        f"Tu código de verificación es: {codigo}\n\n"
        "Este código expira en 15 minutos.\n"
        "Si no solicitaste este cambio, puedes ignorar este correo."
    )
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #F3F4F6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                 <img src="https://i.ibb.co/wzr84d1c/kharis-logo-placeholder.png" alt="Kharis Distribuidora" style="width: 120px; height: auto;" />
            </div>
            
            <div style="background: #ffffff; border-radius: 16px; padding: 40px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #111; margin: 0 0 20px; text-align: center;">Recuperación de Contraseña</h2>
                
                <p style="color: #444; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                    Hola <strong>{nombre}</strong>,<br>
                    Usa el siguiente código para restablecer tu contraseña. Este código es válido por 15 minutos.
                </p>
                
                <div style="background-color: #F3F4F6; border-radius: 8px; padding: 20px; text-align: center; margin: 30px 0;">
                    <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #111;">{codigo}</span>
                </div>
                
                <p style="color: #666; font-size: 14px; text-align: center;">
                    Si no solicitaste este cambio, por favor ignora este correo.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return text, html


def send_order_status_email(
    *,
    email: Optional[str],
    nombre: str,
    codigo: str,
    estado: str,
    total: float,
    direccion: str,
    productos: Optional[List[Dict]] = None,
    thread_id: Optional[str] = None,
) -> Optional[str]:
    """Envía email de estado de orden."""
    if not email: return None
    try:
        subject = _build_subject(codigo, estado)
        text_body, html_body = _build_body(nombre, codigo, estado.lower(), total, direccion, productos)
        return _send_email_base(email, subject, text_body, html_body, thread_id)
    except Exception as exc:
        _log_error(f"Fallo enviando email orden {codigo}", exc)
        return None


def send_b2b_status_notification(
    *,
    email: str,
    nombre: str,
    estado: str,
    notas: str = ""
) -> Optional[str]:
    """Envía notificación de cambio de estado B2B."""
    if not email: return None
    try:
        subject = f"Actualización de tu cuenta Mayorista - Kharis"
        text_body, html_body = _build_b2b_status_body(nombre, estado, notas)
        return _send_email_base(email, subject, text_body, html_body)
    except Exception as exc:
        _log_error(f"Fallo enviando email B2B a {email}", exc)
        return None


def send_password_reset_code(
    *,
    email: str,
    nombre: str,
    codigo: str
) -> Optional[str]:
    """Envía código de recuperación de contraseña."""
    if not email: return None
    try:
        subject = "Código de recuperación de contraseña - Kharis"
        text_body, html_body = _build_recovery_body(nombre, codigo)
        return _send_email_base(email, subject, text_body, html_body)
    except Exception as exc:
        _log_error(f"Fallo enviando código a {email}", exc)
        return None


def _send_email_base(to_email: str, subject: str, text_body: str, html_body: str, thread_id: Optional[str] = None) -> Optional[str]:
    """Función base para envío de correos con threading."""
    try:
        domain = getattr(settings, "EMAIL_HOST_USER", "kharis.local").split("@")[-1]
        msg_id = make_msgid(domain=domain)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", ""),
            to=[to_email],
        )
        msg.attach_alternative(html_body, "text/html")
        
        if thread_id:
            msg.extra_headers['In-Reply-To'] = thread_id
            msg.extra_headers['References'] = thread_id
        
        msg.extra_headers['Message-ID'] = msg_id

        msg.send(fail_silently=True)
        return msg_id
    except Exception as exc:
        _log_error(f"Error base enviando email a {to_email}", exc)
        raise exc


def _log_error(msg: str, exc: Exception):
    try:
        if hasattr(settings, "LOGGER"):
            settings.LOGGER.warning(f"{msg}: {str(exc)}")
        else:
            print(f"⚠️ {msg}: {str(exc)}")
    except:
        pass
