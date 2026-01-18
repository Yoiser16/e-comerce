#!/bin/bash
# ============================================================
# SCRIPT DE INICIO RÁPIDO - E-COMMERCE BACKEND
# ============================================================

echo "🚀 E-Commerce Backend - Inicio Rápido"
echo "================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Debes ejecutar este script desde la raíz del proyecto"
    echo "   Ejemplo: bash scripts/start_server.sh"
    exit 1
fi

# Verificar .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "   Copiando desde .env.example..."
    cp .env.example .env
    echo "❗ IMPORTANTE: Edita el archivo .env con las credenciales correctas"
    echo "   DB_HOST=72.61.73.245"
    echo "   DB_PASSWORD=ecommerce_dev_2026!"
    echo ""
    read -p "¿Ya actualizaste el .env? (s/n): " respuesta
    if [ "$respuesta" != "s" ]; then
        echo "Por favor edita .env y vuelve a ejecutar este script"
        exit 1
    fi
fi

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar dependencias
if ! python -c "import django" 2>/dev/null; then
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt -q
    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya instaladas"
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Probar conexión a BD
echo ""
echo "🔍 Verificando conexión a base de datos..."
if bash scripts/test_db_connection.sh 2>/dev/null | grep -q "ecommerce_db"; then
    echo "✅ Conexión a base de datos exitosa"
else
    echo "⚠️  No se pudo verificar la conexión a BD"
    echo "   El servidor intentará conectarse de todas formas..."
fi

echo ""
echo "================================================"
echo "🌟 INFORMACIÓN DEL SERVIDOR"
echo "================================================"
echo ""
echo "📊 Base de datos: PostgreSQL en VPS"
echo "   Host: 72.61.73.245:5432"
echo "   DB: ecommerce_db"
echo ""
echo "👥 Usuarios de prueba:"
echo "   • admin@ecommerce.com / Admin123! (ADMIN)"
echo "   • operador@ecommerce.com / Operador123! (OPERADOR)"
echo "   • lectura@ecommerce.com / Lectura123! (LECTURA)"
echo ""
echo "🌐 URLs disponibles:"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • API Base: http://localhost:8000/api/v1"
echo "   • Admin: http://localhost:8000/admin"
echo ""
echo "================================================"
echo "🚀 Iniciando servidor..."
echo "================================================"
echo ""

# Cambiar a directorio src e iniciar servidor
cd src
python main.py
