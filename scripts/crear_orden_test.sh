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

# Obtener productos REALES de la API y crear JSON directamente con Python
echo -e "${BLUE}Obteniendo productos de la base de datos...${NC}"

# Usar Python para obtener y parsear productos de forma segura
PRODUCTOS_ARRAY=$(python3 << 'PYEOF'
import json
import urllib.request
import random

try:
    with urllib.request.urlopen("http://localhost:8000/api/v1/productos/") as response:
        data = json.loads(response.read().decode())
        productos = []
        for p in data[:10]:
            precio = p.get("precio", "0")
            if isinstance(precio, str):
                precio = float(precio.replace(" COP", "").replace(",", ""))
            productos.append({
                "producto_id": p.get("id", ""),
                "nombre": p.get("nombre", "Producto"),
                "cantidad": 1,
                "precio_unitario": int(precio)
            })
        # Seleccionar 1-3 productos aleatorios
        num_items = random.randint(1, min(3, len(productos)))
        selected = random.sample(productos, num_items)
        print(json.dumps(selected))
except Exception as e:
    print("[]")
PYEOF
)

# Verificar si obtuvimos productos
if [ "$PRODUCTOS_ARRAY" == "[]" ]; then
    echo -e "${YELLOW}⚠️ No se encontraron productos en la API. Usando productos de prueba...${NC}"
    PRODUCTOS_ARRAY='[{"producto_id": "00000000-0000-0000-0000-000000000001", "nombre": "Producto de Prueba", "cantidad": 1, "precio_unitario": 50000}]'
else
    NUM_PRODS=$(echo "$PRODUCTOS_ARRAY" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
    echo -e "${GREEN}✅ Se seleccionaron $NUM_PRODS productos reales${NC}"
fi

# Seleccionar valores aleatorios
NOMBRE="${NOMBRES[$RANDOM % ${#NOMBRES[@]}]}"
APELLIDO="${APELLIDOS[$RANDOM % ${#APELLIDOS[@]}]}"
DEPARTAMENTO="${DEPARTAMENTOS[$RANDOM % ${#DEPARTAMENTOS[@]}]}"
CIUDAD="${CIUDADES[$RANDOM % ${#CIUDADES[@]}]}"
BARRIO="${BARRIOS[$RANDOM % ${#BARRIOS[@]}]}"
EMAIL="${NOMBRE,,}.${APELLIDO,,}${RANDOM_NUM}@test.com"
TELEFONO="310${RANDOM:0:7}"
DIRECCION="Calle ${RANDOM:0:2} # ${RANDOM:0:2}-${RANDOM:0:2}"

# Los items ya están en PRODUCTOS_ARRAY (JSON válido)
ITEMS="$PRODUCTOS_ARRAY"

# Calcular subtotal con Python
SUBTOTAL=$(echo "$ITEMS" | python3 -c "import sys, json; items=json.load(sys.stdin); print(sum(i['precio_unitario']*i['cantidad'] for i in items))")
NUM_ITEMS=$(echo "$ITEMS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")

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
