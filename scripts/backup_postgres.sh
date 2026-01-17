#!/bin/bash
# ==============================================================================
# SCRIPT DE BACKUP AUTOMÁTICO PARA POSTGRESQL
# ==============================================================================
#
# Uso:
#   ./backup_postgres.sh
#
# Variables de entorno requeridas:
#   DB_HOST     - Host de PostgreSQL
#   DB_PORT     - Puerto (default: 5432)
#   DB_NAME     - Nombre de la base de datos
#   DB_USER     - Usuario de PostgreSQL
#   PGPASSWORD  - Password (o usar .pgpass)
#
# Variables opcionales:
#   BACKUP_DIR      - Directorio de backups (default: ./backups)
#   BACKUP_RETENTION_DAYS - Días de retención (default: 14)
#
# ==============================================================================

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

# Valores desde variables de entorno o defaults
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-ecommerce}"
DB_USER="${DB_USER:-postgres}"

BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"

# Timestamp para el nombre del archivo
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILENAME="backup_${DB_NAME}_${TIMESTAMP}.sql.gz"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILENAME}"

# ==============================================================================
# FUNCIONES
# ==============================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Verificando requisitos..."
    
    # Verificar pg_dump
    if ! command -v pg_dump &> /dev/null; then
        log_error "pg_dump no encontrado. Instalar postgresql-client"
        exit 1
    fi
    
    # Verificar gzip
    if ! command -v gzip &> /dev/null; then
        log_error "gzip no encontrado"
        exit 1
    fi
    
    # Verificar variables obligatorias
    if [ -z "$DB_NAME" ]; then
        log_error "DB_NAME no definido"
        exit 1
    fi
    
    if [ -z "$DB_USER" ]; then
        log_error "DB_USER no definido"
        exit 1
    fi
    
    # Verificar password (PGPASSWORD o .pgpass)
    if [ -z "$PGPASSWORD" ] && [ ! -f ~/.pgpass ]; then
        log_warn "PGPASSWORD no definido y ~/.pgpass no existe"
        log_warn "El backup puede fallar si se requiere autenticación"
    fi
    
    log_info "Requisitos OK"
}

create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log_info "Creando directorio de backups: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
    fi
}

perform_backup() {
    log_info "=============================================="
    log_info "Iniciando backup de PostgreSQL"
    log_info "=============================================="
    log_info "Host: $DB_HOST:$DB_PORT"
    log_info "Database: $DB_NAME"
    log_info "User: $DB_USER"
    log_info "Output: $BACKUP_PATH"
    log_info "=============================================="
    
    # Realizar backup con pg_dump
    # --no-owner: No incluir comandos de ownership
    # --no-acl: No incluir permisos
    # --clean: Incluir DROP antes de CREATE
    # --if-exists: Usar IF EXISTS en DROP
    pg_dump \
        -h "$DB_HOST" \
        -p "$DB_PORT" \
        -U "$DB_USER" \
        -d "$DB_NAME" \
        --no-owner \
        --no-acl \
        --clean \
        --if-exists \
        -F p \
        | gzip > "$BACKUP_PATH"
    
    # Verificar que el archivo se creó
    if [ -f "$BACKUP_PATH" ]; then
        BACKUP_SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
        log_info "Backup completado: $BACKUP_PATH ($BACKUP_SIZE)"
    else
        log_error "El archivo de backup no se creó"
        exit 1
    fi
}

cleanup_old_backups() {
    log_info "Limpiando backups antiguos (>${BACKUP_RETENTION_DAYS} días)..."
    
    # Contar backups antes de limpiar
    OLD_COUNT=$(find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +$BACKUP_RETENTION_DAYS 2>/dev/null | wc -l)
    
    if [ "$OLD_COUNT" -gt 0 ]; then
        find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +$BACKUP_RETENTION_DAYS -delete
        log_info "Eliminados $OLD_COUNT backups antiguos"
    else
        log_info "No hay backups antiguos para eliminar"
    fi
    
    # Mostrar backups actuales
    CURRENT_COUNT=$(find "$BACKUP_DIR" -name "backup_*.sql.gz" 2>/dev/null | wc -l)
    log_info "Backups actuales: $CURRENT_COUNT"
}

verify_backup() {
    log_info "Verificando integridad del backup..."
    
    # Verificar que gzip puede leer el archivo
    if gzip -t "$BACKUP_PATH" 2>/dev/null; then
        log_info "Integridad verificada: OK"
    else
        log_error "El archivo de backup está corrupto"
        exit 1
    fi
    
    # Verificar que contiene datos SQL
    if zcat "$BACKUP_PATH" | head -20 | grep -q "PostgreSQL"; then
        log_info "Contenido verificado: OK"
    else
        log_warn "El backup puede estar vacío o incompleto"
    fi
}

show_summary() {
    echo ""
    log_info "=============================================="
    log_info "RESUMEN DEL BACKUP"
    log_info "=============================================="
    log_info "Archivo: $BACKUP_FILENAME"
    log_info "Tamaño: $(du -h "$BACKUP_PATH" | cut -f1)"
    log_info "Ubicación: $BACKUP_PATH"
    log_info "Retención: $BACKUP_RETENTION_DAYS días"
    log_info "=============================================="
    echo ""
    log_info "Para restaurar:"
    log_info "  gunzip -c $BACKUP_PATH | psql -h \$DB_HOST -U \$DB_USER -d \$DB_NAME"
    log_info "=============================================="
}

# ==============================================================================
# MAIN
# ==============================================================================

main() {
    echo ""
    log_info "=========================================="
    log_info "  BACKUP POSTGRESQL - E-COMMERCE"
    log_info "  $(date '+%Y-%m-%d %H:%M:%S')"
    log_info "=========================================="
    echo ""
    
    check_requirements
    create_backup_dir
    perform_backup
    verify_backup
    cleanup_old_backups
    show_summary
    
    log_info "Backup completado exitosamente"
    exit 0
}

# Ejecutar
main "$@"
