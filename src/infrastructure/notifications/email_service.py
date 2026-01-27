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
                CONFIRMACIÓN DE PEDIDO #{codigo}
            </div>

            <div class="card">
                <p class="info-text">
                    Hola, <strong>{cliente}</strong>.<br>
                    Gracias por tu compra. Tu pedido está <strong>{estado_texto}</strong>.
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
