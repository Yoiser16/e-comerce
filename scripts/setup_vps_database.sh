#!/bin/bash
# ============================================================
# SCRIPT DE CONFIGURACIÓN DE POSTGRESQL EN VPS
# Para desarrollo compartido de e-commerce backend
# ============================================================

VPS_HOST="72.61.73.245"
VPS_USER="root"
DB_NAME="ecommerce_db"
DB_USER="ecommerce_user"
DB_PASSWORD="ecommerce_dev_2026!"  # Cambiar si deseas

echo "🚀 Configurando PostgreSQL en VPS: $VPS_HOST"
echo "================================================"
echo ""

# Conectar al VPS y ejecutar todos los comandos
ssh ${VPS_USER}@${VPS_HOST} << 'ENDSSH'

echo "📋 Paso 1: Verificando sistema operativo..."
cat /etc/os-release | grep PRETTY_NAME
echo ""

echo "📦 Paso 2: Actualizando sistema..."
apt-get update -qq

echo "📥 Paso 3: Instalando PostgreSQL..."
apt-get install -y postgresql postgresql-contrib

echo "✅ Versión de PostgreSQL instalada:"
psql --version
echo ""

echo "🔧 Paso 4: Iniciando servicio PostgreSQL..."
systemctl start postgresql
systemctl enable postgresql
systemctl status postgresql --no-pager | head -5
echo ""

echo "👤 Paso 5: Creando base de datos y usuario..."
sudo -u postgres psql << 'ENDPG'
-- Crear usuario
CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_dev_2026!';

-- Crear base de datos
CREATE DATABASE ecommerce_db OWNER ecommerce_user;

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;

-- Configuración adicional para PostgreSQL 15+
\c ecommerce_db
GRANT ALL ON SCHEMA public TO ecommerce_user;

-- Verificar
\l
ENDPG

echo ""
echo "🌐 Paso 6: Configurando PostgreSQL para aceptar conexiones remotas..."

# Backup de configuraciones originales
cp /etc/postgresql/*/main/postgresql.conf /etc/postgresql/*/main/postgresql.conf.backup
cp /etc/postgresql/*/main/pg_hba.conf /etc/postgresql/*/main/pg_hba.conf.backup

# Encontrar la versión y configurar
PG_VERSION=$(ls /etc/postgresql/ | head -1)
PG_CONF="/etc/postgresql/${PG_VERSION}/main/postgresql.conf"
PG_HBA="/etc/postgresql/${PG_VERSION}/main/pg_hba.conf"

echo "📝 Configurando: $PG_CONF"

# Modificar postgresql.conf para escuchar en todas las interfaces
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"
# Si ya estaba descomentado
sed -i "s/listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

echo "📝 Configurando: $PG_HBA"

# Agregar regla para permitir conexiones remotas con password
echo "" >> "$PG_HBA"
echo "# Permitir conexiones remotas para desarrollo" >> "$PG_HBA"
echo "host    ecommerce_db    ecommerce_user    0.0.0.0/0    md5" >> "$PG_HBA"
echo "host    all             all               0.0.0.0/0    md5" >> "$PG_HBA"

echo "🔥 Paso 7: Configurando firewall (UFW)..."

# Instalar UFW si no está
apt-get install -y ufw

# Configurar firewall
ufw allow 22/tcp    # SSH
ufw allow 5432/tcp  # PostgreSQL
ufw allow 8000/tcp  # FastAPI (opcional)

# Habilitar UFW si no está activo
echo "y" | ufw enable 2>/dev/null || ufw reload

echo "📊 Estado del firewall:"
ufw status numbered

echo ""
echo "🔄 Paso 8: Reiniciando PostgreSQL..."
systemctl restart postgresql

echo "✅ Estado de PostgreSQL:"
systemctl status postgresql --no-pager | head -5

echo ""
echo "🎯 Paso 9: Verificando conexión local..."
sudo -u postgres psql -d ecommerce_db -c "SELECT version();"

echo ""
echo "================================================"
echo "✅ ¡CONFIGURACIÓN COMPLETADA!"
echo "================================================"
echo ""
echo "📋 CREDENCIALES:"
echo "   Host: 72.61.73.245"
echo "   Puerto: 5432"
echo "   Base de datos: ecommerce_db"
echo "   Usuario: ecommerce_user"
echo "   Password: ecommerce_dev_2026!"
echo ""
echo "🔗 Cadena de conexión:"
echo "   postgresql://ecommerce_user:ecommerce_dev_2026!@72.61.73.245:5432/ecommerce_db"
echo ""

ENDSSH

echo ""
echo "🧪 Paso 10: Probando conexión desde tu máquina local..."
echo "Esperando 3 segundos..."
sleep 3

# Probar conexión remota (requiere psql instalado localmente)
if command -v psql &> /dev/null; then
    echo "Intentando conectar..."
    PGPASSWORD="ecommerce_dev_2026!" psql -h 72.61.73.245 -U ecommerce_user -d ecommerce_db -c "SELECT current_database(), current_user, version();"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ ¡CONEXIÓN EXITOSA DESDE TU MÁQUINA!"
    else
        echo ""
        echo "⚠️  No se pudo conectar aún. Puede tomar unos segundos."
        echo "    Intenta manualmente con:"
        echo "    psql -h 72.61.73.245 -U ecommerce_user -d ecommerce_db"
    fi
else
    echo "⚠️  psql no está instalado localmente."
    echo "    Para probar la conexión, instala: apt-get install postgresql-client"
fi

echo ""
echo "================================================"
echo "📝 PRÓXIMOS PASOS:"
echo "================================================"
echo "1. Actualiza tu archivo .env:"
echo "   DB_HOST=72.61.73.245"
echo "   DB_NAME=ecommerce_db"
echo "   DB_USER=ecommerce_user"
echo "   DB_PASSWORD=ecommerce_dev_2026!"
echo ""
echo "2. Ejecuta las migraciones:"
echo "   python manage.py migrate"
echo ""
echo "3. Comparte estas credenciales con tu compañero"
echo ""
echo "🎉 ¡Listo para trabajar en equipo!"
