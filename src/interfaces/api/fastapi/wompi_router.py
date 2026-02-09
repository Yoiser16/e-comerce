"""
Router de Wompi - Pasarela de Pagos Colombia
Endpoints para webhook de eventos y consulta de transacciones

Modo: Sandbox/Test
"""
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from asgiref.sync import sync_to_async
import hashlib
import hmac
import os

import django
django.setup()

router = APIRouter(prefix="/api/v1/wompi", tags=["Wompi Pagos"])


# ═══════════════════════════════════════════════════════════════════════════
# DTOs / Schemas
# ═══════════════════════════════════════════════════════════════════════════

class WompiEventData(BaseModel):
    """Schema para el payload del webhook de Wompi"""
    transaction: Optional[dict] = None


class WompiWebhookPayload(BaseModel):
    """Schema principal del webhook de Wompi"""
    event: str  # transaction.updated
    data: WompiEventData
    environment: str = "sandbox"  # sandbox or production
    signature: Optional[dict] = None
    timestamp: Optional[int] = None
    sent_at: Optional[str] = None


class TransactionStatusResponse(BaseModel):
    """Response para consulta de estado de transacción"""
    transaction_id: str
    reference: str
    status: str
    amount: float
    currency: str = "COP"
    payment_method: Optional[str] = None
    created_at: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN WOMPI
# ═══════════════════════════════════════════════════════════════════════════

WOMPI_CONFIG = {
    "public_key": os.getenv("WOMPI_PUBLIC_KEY", "pub_test_ZVH2hPZRCY7iVcPAyCCh53E5cS2SUFmW"),
    "private_key": os.getenv("WOMPI_PRIVATE_KEY", "prv_test_KCOpUn5CIvcopDAEkf79iKlim7B5LqcY"),
    "events_secret": os.getenv("WOMPI_EVENTS_SECRET", "test_events_WTxoTpg6pfpYUAKKklCpI9GzuMcTSXnk"),
    "integrity_secret": os.getenv("WOMPI_INTEGRITY_SECRET", "test_integrity_Zb8xdlPSUWmE9HmHjVCI10Y9vxaNuprK"),
    "environment": os.getenv("WOMPI_ENVIRONMENT", "sandbox"),
    "sandbox_url": "https://sandbox.wompi.co/v1",
    "production_url": "https://production.wompi.co/v1"
}


def get_wompi_api_url():
    if WOMPI_CONFIG["environment"] == "production":
        return WOMPI_CONFIG["production_url"]
    return WOMPI_CONFIG["sandbox_url"]


# ═══════════════════════════════════════════════════════════════════════════
# FIRMA DE INTEGRIDAD - Para checkout seguro
# ═══════════════════════════════════════════════════════════════════════════

class IntegritySignatureRequest(BaseModel):
    """Request para generar firma de integridad"""
    reference: str
    amount_in_cents: int
    currency: str = "COP"


@router.post("/integrity-signature")
async def generar_firma_integridad(data: IntegritySignatureRequest):
    """
    Genera la firma de integridad para el checkout de Wompi.
    
    La firma es SHA-256 de: reference + amountInCents + currency + integritySecret
    El secreto de integridad NUNCA se expone al frontend.
    """
    try:
        integrity_secret = WOMPI_CONFIG["integrity_secret"]
        if not integrity_secret:
            raise HTTPException(
                status_code=500,
                detail="Secreto de integridad no configurado"
            )
        
        # Concatenar: reference + amount_in_cents + currency + integrity_secret
        concat_string = f"{data.reference}{data.amount_in_cents}{data.currency}{integrity_secret}"
        
        # SHA-256
        signature = hashlib.sha256(concat_string.encode('utf-8')).hexdigest()
        
        print(f"🔐 Firma de integridad generada para ref: {data.reference}")
        
        return {
            "signature": signature,
            "reference": data.reference,
            "amount_in_cents": data.amount_in_cents,
            "currency": data.currency
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generando firma de integridad: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando firma: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════════════════
# WEBHOOK - Recibe eventos de Wompi
# ═══════════════════════════════════════════════════════════════════════════

@router.post("/webhook")
async def wompi_webhook(request: Request):
    """
    Endpoint para recibir webhooks de Wompi.
    
    Wompi envía un POST cuando una transacción cambia de estado.
    Eventos soportados:
    - transaction.updated: Cuando una transacción cambia de estado
    - nequi_token.updated: Cuando un token de Nequi cambia
    """
    try:
        body = await request.json()
        
        event = body.get("event", "")
        data = body.get("data", {})
        environment = body.get("environment", "sandbox")
        signature = body.get("signature", {})
        
        print(f"📩 Webhook Wompi recibido: {event} (env: {environment})")
        
        # Verificar firma del webhook si tenemos el secret configurado
        if WOMPI_CONFIG["events_secret"] and signature:
            is_valid = verify_webhook_signature(body, signature)
            if not is_valid:
                print("⚠️ Firma de webhook inválida - ignorando evento")
                raise HTTPException(status_code=401, detail="Firma inválida")
        
        if event == "transaction.updated":
            transaction = data.get("transaction", {})
            tx_id = transaction.get("id", "")
            tx_status = transaction.get("status", "")
            tx_reference = transaction.get("reference", "")
            tx_amount = transaction.get("amount_in_cents", 0)
            tx_payment_method = transaction.get("payment_method_type", "")
            
            print(f"💳 Transacción actualizada: {tx_id}")
            print(f"   Referencia: {tx_reference}")
            print(f"   Estado: {tx_status}")
            print(f"   Monto: ${tx_amount / 100:,.0f} COP")
            print(f"   Método: {tx_payment_method}")
            
            # Procesar según el estado
            if tx_status == "APPROVED":
                await process_approved_transaction(transaction)
            elif tx_status == "DECLINED":
                await process_declined_transaction(transaction)
            elif tx_status == "VOIDED":
                await process_voided_transaction(transaction)
            elif tx_status == "ERROR":
                print(f"❌ Error en transacción {tx_id}: {transaction.get('status_message', '')}")
            
        elif event == "nequi_token.updated":
            print(f"📱 Token Nequi actualizado")
        else:
            print(f"⚠️ Evento no manejado: {event}")
        
        # Siempre responder 200 para que Wompi no reintente
        return {"status": "ok", "message": f"Evento {event} procesado"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error procesando webhook Wompi: {e}")
        import traceback
        traceback.print_exc()
        # Aún así responder 200 para evitar reintentos
        return {"status": "error", "message": str(e)}


def verify_webhook_signature(body: dict, signature: dict) -> bool:
    """
    Verifica la firma del webhook de Wompi.
    
    Wompi usa HMAC-SHA256 para firmar los eventos.
    La firma se compone de: properties concatenadas + timestamp + events_secret
    """
    try:
        events_secret = WOMPI_CONFIG["events_secret"]
        if not events_secret:
            return True  # Sin secret configurado, aceptar todo (modo desarrollo)
        
        properties = signature.get("properties", [])
        checksum = signature.get("checksum", "")
        
        if not properties or not checksum:
            return True  # Sin datos de firma, aceptar
        
        # Construir string a firmar con los valores de las properties
        transaction = body.get("data", {}).get("transaction", {})
        values = []
        for prop in properties:
            keys = prop.split(".")
            value = transaction
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key, "")
                else:
                    value = ""
                    break
            values.append(str(value))
        
        timestamp = str(body.get("timestamp", ""))
        concat_string = "".join(values) + timestamp + events_secret
        
        computed_hash = hashlib.sha256(concat_string.encode()).hexdigest()
        
        return computed_hash == checksum
        
    except Exception as e:
        print(f"⚠️ Error verificando firma: {e}")
        return True  # En caso de error, aceptar (modo desarrollo)


async def process_approved_transaction(transaction: dict):
    """
    Procesa una transacción aprobada.
    Actualiza la orden correspondiente si existe.
    """
    from infrastructure.persistence.django.models import OrdenModel
    
    reference = transaction.get("reference", "")
    tx_id = transaction.get("id", "")
    
    if not reference:
        return
    
    try:
        def update_order():
            # Buscar orden por referencia en las notas o metodo_pago
            ordenes = OrdenModel.objects.filter(
                metodo_pago='wompi',
                notas_envio__icontains=reference
            )
            
            if ordenes.exists():
                orden = ordenes.first()
                if orden.estado == 'pendiente':
                    orden.estado = 'confirmada'
                    orden.notas_envio = (orden.notas_envio or '') + f" | Wompi TX: {tx_id} APROBADO"
                    orden.save()
                    try:
                        from infrastructure.notifications.email_service import send_order_status_email
                        from infrastructure.persistence.django.models import LineaOrdenModel

                        if orden.cliente:
                            lineas_orden = LineaOrdenModel.objects.filter(orden=orden).select_related('producto').prefetch_related('producto__imagenes')
                            productos_email = []
                            for linea in lineas_orden:
                                producto_data = {
                                    'nombre': linea.producto.nombre if linea.producto else 'Producto',
                                    'cantidad': linea.cantidad,
                                    'imagen': ''
                                }
                                if linea.producto:
                                    primera_imagen_obj = linea.producto.imagenes.filter(es_principal=True).first()
                                    if not primera_imagen_obj:
                                        primera_imagen_obj = linea.producto.imagenes.order_by('orden').first()

                                    if primera_imagen_obj:
                                        url_imagen = primera_imagen_obj.url
                                        producto_data['imagen'] = url_imagen if url_imagen.startswith('http') else f"http://localhost:8000{url_imagen}"

                                productos_email.append(producto_data)

                            direccion_completa = ", ".join(filter(None, [orden.direccion_envio, orden.municipio, orden.departamento]))
                            send_order_status_email(
                                email=orden.cliente.email,
                                nombre=f"{orden.cliente.nombre} {orden.cliente.apellido}".strip(),
                                codigo=orden.codigo,
                                estado='confirmada',
                                total=float(orden.total_monto),
                                direccion=direccion_completa,
                                productos=productos_email,
                                thread_id=orden.email_thread_id or None,
                            )
                    except Exception as err:
                        print(f"❌ Error enviando email confirmado por Wompi: {err}")
                    print(f"✅ Orden {orden.codigo} confirmada automáticamente por Wompi")
                    return orden
            return None
        
        await sync_to_async(update_order)()
        
    except Exception as e:
        print(f"❌ Error actualizando orden por webhook: {e}")


async def process_declined_transaction(transaction: dict):
    """Procesa una transacción rechazada"""
    reference = transaction.get("reference", "")
    print(f"🚫 Transacción rechazada - Ref: {reference}")
    print(f"   Motivo: {transaction.get('status_message', 'Sin motivo')}")


async def process_voided_transaction(transaction: dict):
    """Procesa una transacción anulada"""
    from infrastructure.persistence.django.models import OrdenModel, ProductoModel, LineaOrdenModel
    
    reference = transaction.get("reference", "")
    
    if not reference:
        return
    
    try:
        def void_order():
            ordenes = OrdenModel.objects.filter(
                metodo_pago='wompi',
                notas_envio__icontains=reference
            )
            
            if ordenes.exists():
                orden = ordenes.first()
                if orden.estado not in ['cancelada', 'completada']:
                    # Devolver stock
                    lineas = LineaOrdenModel.objects.filter(orden=orden).select_related('producto')
                    for linea in lineas:
                        if linea.producto:
                            producto = ProductoModel.objects.get(id=linea.producto_id)
                            producto.stock_actual += linea.cantidad
                            producto.save()
                            print(f"↩️ Stock devuelto: {producto.nombre} +{linea.cantidad}")
                    
                    orden.estado = 'cancelada'
                    orden.notas_envio = (orden.notas_envio or '') + f" | Wompi ANULADO"
                    orden.save()
                    print(f"❌ Orden {orden.codigo} cancelada por anulación Wompi")
            
        await sync_to_async(void_order)()
        
    except Exception as e:
        print(f"❌ Error procesando anulación: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# CONSULTA DE TRANSACCIÓN (proxy para el frontend)
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/transaction/{transaction_id}")
async def consultar_transaccion(transaction_id: str):
    """
    Consulta el estado de una transacción en Wompi.
    Actúa como proxy para evitar exponer la API directamente.
    """
    import httpx
    
    try:
        api_url = get_wompi_api_url()
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{api_url}/transactions/{transaction_id}")
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Error consultando transacción en Wompi"
                )
            
            data = response.json()
            tx = data.get("data", {})
            
            return TransactionStatusResponse(
                transaction_id=tx.get("id", ""),
                reference=tx.get("reference", ""),
                status=tx.get("status", "UNKNOWN"),
                amount=tx.get("amount_in_cents", 0) / 100,
                currency=tx.get("currency", "COP"),
                payment_method=tx.get("payment_method_type", None),
                created_at=tx.get("created_at", None)
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error consultando transacción: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error consultando transacción: {str(e)}"
        )


@router.get("/merchant")
async def obtener_info_merchant():
    """
    Obtiene información del comercio en Wompi (métodos de pago aceptados).
    Útil para mostrar en el frontend qué medios de pago están disponibles.
    """
    import httpx
    
    try:
        api_url = get_wompi_api_url()
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{api_url}/merchants/{WOMPI_CONFIG['public_key']}")
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Error consultando merchant en Wompi"
                )
            
            data = response.json()
            merchant = data.get("data", {})
            
            return {
                "name": merchant.get("name", ""),
                "legal_name": merchant.get("legal_name", ""),
                "accepted_payment_methods": merchant.get("accepted_payment_methods", []),
                "accepted_currencies": merchant.get("accepted_currencies", []),
                "public_key": WOMPI_CONFIG["public_key"]
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error consultando merchant: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error consultando merchant: {str(e)}"
        )
