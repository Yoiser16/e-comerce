#!/bin/bash
# Script para crear una orden de prueba en el sistema
# Ejecutar: bash crear_orden_test.sh

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
API_URL="http://localhost:8000/api/v1/ordenes"
RANDOM_NUM=$RANDOM

# Generar datos aleatorios
NOMBRES=("Juan" "María" "Carlos" "Ana" "Pedro" "Laura" "Diego" "Sofia" "Luis" "Carmen")
APELLIDOS=("García" "Rodríguez" "Martínez" "López" "González" "Hernández" "Pérez" "Sánchez" "Ramírez" "Torres")
DEPARTAMENTOS=("Antioquia" "Cundinamarca" "Valle del Cauca" "Atlántico" "Santander" "Bolívar" "Tolima")
CIUDADES=("Medellín" "Bogotá" "Cali" "Barranquilla" "Bucaramanga" "Cartagena" "Ibagué")
BARRIOS=("El Poblado" "Chapinero" "San Fernando" "El Prado" "Cabecera" "Bocagrande" "Centenario")
PRODUCTOS=(
    '{"producto_id": "00000000-0000-0000-0000-000000000001", "nombre": "Lápiz Labial Mate", "cantidad": 2, "precio_unitario": 45000}'
    '{"producto_id": "00000000-0000-0000-0000-000000000002", "nombre": "Base de Maquillaje", "cantidad": 1, "precio_unitario": 89000}'
    '{"producto_id": "00000000-0000-0000-0000-000000000003", "nombre": "Máscara de Pestañas", "cantidad": 3, "precio_unitario": 52000}'
    '{"producto_id": "00000000-0000-0000-0000-000000000004", "nombre": "Rubor en Polvo", "cantidad": 1, "precio_unitario": 38000}'
    '{"producto_id": "00000000-0000-0000-0000-000000000005", "nombre": "Set de Brochas", "cantidad": 1, "precio_unitario": 125000}'
)

# Seleccionar valores aleatorios
NOMBRE="${NOMBRES[$RANDOM % ${#NOMBRES[@]}]}"
APELLIDO="${APELLIDOS[$RANDOM % ${#APELLIDOS[@]}]}"
DEPARTAMENTO="${DEPARTAMENTOS[$RANDOM % ${#DEPARTAMENTOS[@]}]}"
CIUDAD="${CIUDADES[$RANDOM % ${#CIUDADES[@]}]}"
BARRIO="${BARRIOS[$RANDOM % ${#BARRIOS[@]}]}"
EMAIL="${NOMBRE,,}.${APELLIDO,,}${RANDOM_NUM}@test.com"
TELEFONO="310${RANDOM:0:7}"
DIRECCION="Calle ${RANDOM:0:2} # ${RANDOM:0:2}-${RANDOM:0:2}"

# Generar items aleatorios (1-3 productos)
NUM_ITEMS=$((1 + RANDOM % 3))
ITEMS="["
SUBTOTAL=0

for ((i=0; i<NUM_ITEMS; i++)); do
    PRODUCTO="${PRODUCTOS[$RANDOM % ${#PRODUCTOS[@]}]}"
    if [ $i -gt 0 ]; then
        ITEMS+=","
    fi
    ITEMS+="$PRODUCTO"
    
    # Extraer precio para calcular subtotal
    PRECIO=$(echo $PRODUCTO | grep -oP '(?<="precio_unitario": )\d+')
    CANTIDAD=$(echo $PRODUCTO | grep -oP '(?<="cantidad": )\d+')
    SUBTOTAL=$((SUBTOTAL + PRECIO * CANTIDAD))
done
ITEMS+="]"

# Calcular totales
ENVIO=8000
TOTAL=$((SUBTOTAL + ENVIO))

# Crear JSON de la orden
JSON_DATA=$(cat <<EOF
{
  "email": "$EMAIL",
  "nombre": "$NOMBRE",
  "apellido": "$APELLIDO",
  "telefono": "$TELEFONO",
  "direccion": "$DIRECCION",
  "departamento": "$DEPARTAMENTO",
  "municipio": "$CIUDAD",
  "barrio": "$BARRIO",
  "notas": "Orden de prueba generada automáticamente",
  "items": $ITEMS,
  "subtotal": $SUBTOTAL,
  "envio": $ENVIO,
  "total": $TOTAL,
  "metodo_pago": "whatsapp"
}
EOF
)

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   🛒 CREANDO ORDEN DE PRUEBA${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Cliente:${NC} $NOMBRE $APELLIDO"
echo -e "${YELLOW}Email:${NC} $EMAIL"
echo -e "${YELLOW}Teléfono:${NC} $TELEFONO"
echo -e "${YELLOW}Dirección:${NC} $DIRECCION, $BARRIO, $CIUDAD, $DEPARTAMENTO"
echo -e "${YELLOW}Items:${NC} $NUM_ITEMS producto(s)"
echo -e "${YELLOW}Subtotal:${NC} \$$(printf "%'d" $SUBTOTAL)"
echo -e "${YELLOW}Envío:${NC} \$$(printf "%'d" $ENVIO)"
echo -e "${YELLOW}Total:${NC} \$$(printf "%'d" $TOTAL)"
echo ""
echo -e "${BLUE}Enviando petición a la API...${NC}"
echo ""

# Enviar petición a la API
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA")

# Separar el cuerpo de la respuesta del código HTTP
HTTP_BODY=$(echo "$RESPONSE" | head -n -1)
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)

# Verificar respuesta
if [ "$HTTP_CODE" == "200" ] || [ "$HTTP_CODE" == "201" ]; then
    ORDEN_ID=$(echo "$HTTP_BODY" | grep -oP '(?<="id": ")[^"]*' | head -1)
    ORDEN_CODIGO=$(echo "$HTTP_BODY" | grep -oP '(?<="codigo": ")[^"]*' | head -1)
    
    echo -e "${GREEN}✅ ¡ORDEN CREADA EXITOSAMENTE!${NC}"
    echo -e "${GREEN}   Código: $ORDEN_CODIGO${NC}"
    echo -e "${GREEN}   ID: $ORDEN_ID${NC}"
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo -e "Revisa el panel de administración para ver la nueva orden 🎉"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
else
    echo -e "${YELLOW}⚠️  Respuesta del servidor (HTTP $HTTP_CODE):${NC}"
    echo "$HTTP_BODY" | python3 -m json.tool 2>/dev/null || echo "$HTTP_BODY"
    echo ""
    echo -e "${YELLOW}Tip: Asegúrate de que el servidor esté corriendo en $API_URL${NC}"
fi
