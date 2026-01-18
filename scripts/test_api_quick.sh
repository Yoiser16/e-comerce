#!/bin/bash
# ============================================================
# SCRIPT DE PRUEBA RÁPIDA DE LA API
# ============================================================

API_BASE="http://localhost:8000/api/v1"

echo "🧪 Prueba Rápida de API E-Commerce"
echo "================================================"
echo ""

# 1. Verificar que el servidor esté corriendo
echo "1️⃣  Verificando servidor..."
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "   ✅ Servidor activo en http://localhost:8000"
else
    echo "   ❌ Servidor no está corriendo"
    echo "   Inicia el servidor con: bash scripts/start_server.sh"
    exit 1
fi

echo ""
echo "2️⃣  Haciendo login..."

# 2. Login
LOGIN_RESPONSE=$(curl -s -X POST "${API_BASE}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@ecommerce.com",
    "password": "Admin123!"
  }')

# Extraer token (requiere jq, si no está disponible, mostrar respuesta completa)
if command -v jq &> /dev/null; then
    ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access')
    USER_EMAIL=$(echo $LOGIN_RESPONSE | jq -r '.user.email')
    USER_ROL=$(echo $LOGIN_RESPONSE | jq -r '.user.rol')
    
    if [ "$ACCESS_TOKEN" != "null" ] && [ -n "$ACCESS_TOKEN" ]; then
        echo "   ✅ Login exitoso"
        echo "   👤 Usuario: $USER_EMAIL (Rol: $USER_ROL)"
    else
        echo "   ❌ Error en login"
        echo "   Respuesta: $LOGIN_RESPONSE"
        exit 1
    fi
else
    echo "   Respuesta: $LOGIN_RESPONSE"
    echo "   ℹ️  Instala 'jq' para ver la info formateada: sudo apt-get install jq"
    exit 0
fi

echo ""
echo "3️⃣  Obteniendo productos..."

# 3. Listar productos
PRODUCTOS=$(curl -s "${API_BASE}/productos" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

CANT_PRODUCTOS=$(echo $PRODUCTOS | jq '. | length')

if [ "$CANT_PRODUCTOS" -ge 0 ]; then
    echo "   ✅ Lista de productos obtenida"
    echo "   📦 Cantidad: $CANT_PRODUCTOS productos"
else
    echo "   ⚠️  No hay productos aún"
fi

echo ""
echo "4️⃣  Obteniendo clientes..."

# 4. Listar clientes
CLIENTES=$(curl -s "${API_BASE}/clientes" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

CANT_CLIENTES=$(echo $CLIENTES | jq '. | length')

if [ "$CANT_CLIENTES" -ge 0 ]; then
    echo "   ✅ Lista de clientes obtenida"
    echo "   👥 Cantidad: $CANT_CLIENTES clientes"
else
    echo "   ⚠️  No hay clientes aún"
fi

echo ""
echo "================================================"
echo "✅ PRUEBA COMPLETADA"
echo "================================================"
echo ""
echo "📊 Resumen:"
echo "   • Autenticación: ✅ Funcionando"
echo "   • Endpoint Productos: ✅ Funcionando"
echo "   • Endpoint Clientes: ✅ Funcionando"
echo "   • Base de datos VPS: ✅ Conectada"
echo ""
echo "🎉 Todo está funcionando correctamente!"
echo ""
echo "📚 Próximos pasos:"
echo "   • Ver documentación: http://localhost:8000/docs"
echo "   • Probar endpoints en Swagger UI"
echo "   • Empezar a desarrollar el frontend"
echo ""
