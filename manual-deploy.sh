#!/bin/bash

# ============================================================================
# DEPLOY RÁPIDO - Para actualizaciones de código (SIN configuración inicial)
# ============================================================================
# Uso: bash manual-deploy.sh
# 
# Este script es para DESPUÉS de que deploy.sh ya haya corrido.
# Solo actualiza cambios sin reinstalar todo.
# ============================================================================

set -e  # Salir si hay error

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuración
VPS_IP="72.61.15.15"
VPS_USER="root"
APP_PATH="/var/www/ecommerce"

print_step() {
    echo -e "${BLUE}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# ============================================================================
# MAIN
# ============================================================================

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🚀 DEPLOY RÁPIDO (ACTUALIZACIÓN)    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# PASO 1: Compilar frontend localmente
print_step "Compilando frontend en tu PC..."
cd frontend
npm run build > /dev/null 2>&1
cd ..
print_success "Frontend compilado (frontend/dist/)"
echo ""

# PASO 2: Sincronizar archivos con rsync
print_step "Sincronizando cambios al VPS..."
rsync -avz --progress --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '__pycache__' \
    --exclude '.env' \
    --exclude 'venv' \
    --exclude '.venv' \
    "." "root@${VPS_IP}:${APP_PATH}/" > /dev/null 2>&1
print_success "Archivos sincronizados"
echo ""

# PASO 3: Instalar deps Python en VPS (si cambió requirements.txt)
print_step "Actualizando dependencias Python en VPS..."
ssh $VPS_USER@$VPS_IP << 'EOF'
set -e
cd /var/www/ecommerce
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
EOF
print_success "Dependencias Python actualizadas"
echo ""

# PASO 4: Reiniciar servicio
print_step "Reiniciando servicio backend..."
ssh $VPS_USER@$VPS_IP << 'EOF'
systemctl restart ecommerce-backend
sleep 2
EOF
print_success "Servicio reiniciado"
echo ""

# PASO 5: Verificar estado
print_step "Verificando status..."
STATUS=$(ssh $VPS_USER@$VPS_IP "systemctl is-active ecommerce-backend")
if [ "$STATUS" = "active" ]; then
    print_success "Servicio activo y corriendo"
else
    print_error "Servicio NO está corriendo. Revisar logs:"
    print_error "ssh $VPS_USER@$VPS_IP 'tail -50 /var/log/ecommerce/error.log'"
fi
echo ""

# Resumen
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║    ✓ DEPLOY COMPLETADO EXITOSAMENTE   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Tu proyecto está en:"
echo -e "  ${BLUE}http://72.61.15.15:8888${NC}"
echo ""
echo "Comandos útiles:"
echo "  ssh root@72.61.15.15"
echo "  tail -f /var/log/ecommerce/error.log"
echo "  systemctl status ecommerce-backend"
echo ""
