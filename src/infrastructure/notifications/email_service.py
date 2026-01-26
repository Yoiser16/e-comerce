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
    "pendiente": "pendiente de pago",
    "confirmada": "aprobada",
    "en_proceso": "en proceso",
    "enviada": "enviada",
    "completada": "completada",
    "cancelada": "cancelada",
}


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
    text = (
        f"Hola {cliente},\n\n"
        f"Tu orden {codigo} ahora está *{estado_texto}*.\n"
        f"Total: {total_str}\n"
        f"Dirección de entrega: {direccion}\n\n"
        "Gracias por comprar con Kharis Distribuidora."
    )
    
    # HTML con imágenes de productos
    productos_html = ""
    if productos:
        productos_html = "<div style='margin: 20px 0;'><h3>Productos:</h3>"
        for p in productos:
            img_url = p.get('imagen', '')
            nombre = p.get('nombre', 'Producto')
            cantidad = p.get('cantidad', 1)
            img_tag = f'<img src="{img_url}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; margin-right: 10px; vertical-align: middle;">' if img_url else ''
            productos_html += f"""
            <div style='margin: 10px 0; display: flex; align-items: center;'>
                {img_tag}
                <span><strong>{nombre}</strong> x{cantidad}</span>
            </div>
            """
        productos_html += "</div>"
    
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #fafafa; border-radius: 8px;">
        <h2 style="color: #1A1A1A; border-bottom: 2px solid #D81B60; padding-bottom: 10px;">Kharis Distribuidora</h2>
        <p>Hola <strong>{cliente}</strong>,</p>
        <p>Tu orden <strong>{codigo}</strong> ahora está <strong style="color: #D81B60;">{estado_texto}</strong>.</p>
        {productos_html}
        <p><strong>Total:</strong> {total_str}<br/>
           <strong>Dirección de entrega:</strong> {direccion}</p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
        <p style="color: #7A7A7A; font-size: 14px;">Gracias por comprar con Kharis Distribuidora.</p>
    </div>
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
    """Envía un email al cliente sobre el estado de su orden.

    Falla de forma silenciosa (loguea) si la configuración de email no está lista.
    
    Args:
        email: Email del cliente
        nombre: Nombre del cliente
        codigo: Código de la orden
        estado: Estado de la orden
        total: Total de la orden
        direccion: Dirección de entrega
        productos: Lista de productos con 'nombre', 'cantidad', 'imagen'
        thread_id: Message-ID del primer email (para threading)
    
    Returns:
        Message-ID del email enviado (para threading) o None si falla
    """
    if not email:
        return None

    estado = estado.lower()

    try:
        subject = _build_subject(codigo, estado)
        text_body, html_body = _build_body(nombre, codigo, estado, total, direccion, productos)

        # Generar Message-ID único
        domain = getattr(settings, "EMAIL_HOST_USER", "kharis.local").split("@")[-1]
        msg_id = make_msgid(domain=domain)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", ""),
            to=[email],
        )
        msg.attach_alternative(html_body, "text/html")
        
        # Threading: Si hay thread_id, encadenar como respuesta
        if thread_id:
            msg.extra_headers['In-Reply-To'] = thread_id
            msg.extra_headers['References'] = thread_id
        
        # Asignar Message-ID
        msg.extra_headers['Message-ID'] = msg_id
        
        msg.send(fail_silently=True)
        return msg_id
        
    except Exception as exc:  # noqa: BLE001
        # No interrumpir el flujo de negocio por fallas de email
        try:
            if hasattr(settings, "LOGGER"):
                settings.LOGGER.warning("Fallo enviando email de estado", extra={"codigo": codigo, "estado": estado, "error": str(exc)})
        except Exception:
            pass
        return None
