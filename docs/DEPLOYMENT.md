# 🚀 Guía de Despliegue y Configuración

## Requisitos Previos

- Python 3.14+
- PostgreSQL 18+
- pip o pipenv

## Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/Yoiser16/e-comerce.git
cd e-comerce
```

### 2. Configurar entorno virtual

```bash
# Crear entorno
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo de ejemplo y editarlo:

```bash
cp .env.example .env
```

Configuración básica requerida en `.env`:

```env
# Variables de Entorno (.env)
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=secret_password
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=tu-clave-secreta-segura
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Base de Datos

```bash
# Ejecutar migraciones
python manage.py migrate

# Crear usuarios de prueba (Admin, Operador, Lectura)
python manage.py crear_usuarios_demo
```

### 6. Ejecutar servidor

```bash
python manage.py runserver
```

---

## ☁️ Configuración en VPS (Producción)

### Información del Servidor

- **OS**: Ubuntu 24.04 LTS (Recomendado)
- **Base de Datos**: PostgreSQL 16+

### Conexión a Base de Datos Compartida

Si utilizas una instancia de PostgreSQL en un VPS compartido:

**Credenciales (Ejemplo)**:
- Host: `192.168.x.x` (IP Privada/Pública)
- Puerto: `5432`
- DB: `ecommerce_db`
- Usuario: `ecommerce_user`

**Cadena de conexión**:
`postgresql://ecommerce_user:******@192.168.x.x:5432/ecommerce_db`

### Comandos Útiles en VPS

**Verificar estado de BD**:
```bash
psql -h <VPS_IP> -U ecommerce_user -d ecommerce_db -c "\dt"
```

**Backups**:
```bash
# Backup manual
pg_dump -h <VPS_IP> -U ecommerce_user ecommerce_db > backup_$(date +%Y%m%d).sql
```

## 🏥 Mejoras Operativas para Producción

### Health Checks

El sistema expone endpoints para balanceadores de carga y orquestadores:

| Endpoint | Propósito |
|----------|-----------|
| `/health` | Estado general del sistema |
| `/ready` | Readiness probe (Kubernetes) |
| `/live` | Liveness probe (Kubernetes) |

### Configuración de Cache

El sistema soporta Redis para caché distribuido:

```env
REDIS_URL=redis://localhost:6379/1
CACHE_BACKEND=redis
```
