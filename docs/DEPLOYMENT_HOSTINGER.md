# ==============================================================================
# Guía de Deployment - Hostinger VPS
# Sistema E-commerce Clean Architecture
# ==============================================================================

## Requisitos Hostinger

**Plan mínimo recomendado**: VPS KVM 1 o superior
- 1 vCPU
- 4 GB RAM
- 50 GB SSD
- Ubuntu 22.04/24.04 LTS

**NO compatible con**: Hosting compartido (no soporta Python backend)

## 1. Preparación del Servidor

```bash
# Conectar por SSH
ssh root@tu-ip-hostinger

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install -y python3.12 python3.12-venv python3-pip nginx mysql-server supervisor git

# Crear usuario para la app
adduser ecommerce
usermod -aG sudo ecommerce
```

## 2. Configurar MySQL

```bash
# Acceder a MySQL
mysql -u root -p

# Crear base de datos y usuario
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 3. Clonar y Configurar Proyecto

```bash
# Cambiar a usuario ecommerce
su - ecommerce

# Clonar repositorio
cd /home/ecommerce
git clone https://tu-repo.git app
cd app

# Crear entorno virtual
python3.12 -m venv venv
source venv/bin/activate

# Instalar dependencias de producción
pip install -r requirements-prod.txt

# Configurar variables de entorno
cp .env.example .env
nano .env
```

## 4. Configurar .env para Producción

```env
AMBIENTE=production
DEBUG=False

# Base de datos Hostinger
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=tu_password_seguro
DB_ENGINE=mysql

# Seguridad
SECRET_KEY=genera-una-clave-segura-de-64-caracteres

# Server
API_HOST=0.0.0.0
API_PORT=8000
```

## 5. Configurar Supervisor (Process Manager)

```bash
# /etc/supervisor/conf.d/ecommerce.conf

[program:ecommerce-fastapi]
command=/home/ecommerce/app/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/home/ecommerce/app
user=ecommerce
autostart=true
autorestart=true
stderr_logfile=/var/log/ecommerce/fastapi.err.log
stdout_logfile=/var/log/ecommerce/fastapi.out.log
environment=AMBIENTE="production"

[program:ecommerce-django]
command=/home/ecommerce/app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8001 django_app.wsgi:application
directory=/home/ecommerce/app
user=ecommerce
autostart=true
autorestart=true
stderr_logfile=/var/log/ecommerce/django.err.log
stdout_logfile=/var/log/ecommerce/django.out.log
environment=AMBIENTE="production"
```

```bash
# Crear directorio de logs
sudo mkdir -p /var/log/ecommerce
sudo chown ecommerce:ecommerce /var/log/ecommerce

# Recargar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

## 6. Configurar Nginx (Reverse Proxy)

```nginx
# /etc/nginx/sites-available/ecommerce

server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # SSL (usar Certbot para generar)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    
    # Seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # API FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Django Admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        alias /home/ecommerce/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /home/ecommerce/app/media/;
        expires 7d;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 7. SSL con Certbot

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Auto-renovación (ya configurado por defecto)
sudo certbot renew --dry-run
```

## 8. Firewall

```bash
# Configurar UFW
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## 9. Comandos Útiles

```bash
# Ver logs
sudo tail -f /var/log/ecommerce/fastapi.out.log

# Reiniciar servicios
sudo supervisorctl restart all

# Estado de servicios
sudo supervisorctl status

# Actualizar código
cd /home/ecommerce/app
git pull
source venv/bin/activate
pip install -r requirements-prod.txt
sudo supervisorctl restart all
```

## 10. Backup MySQL

```bash
# Backup manual
mysqldump -u ecommerce_user -p ecommerce_db > backup_$(date +%Y%m%d).sql

# Cron para backup automático (agregar a crontab)
0 2 * * * mysqldump -u ecommerce_user -p'password' ecommerce_db > /home/ecommerce/backups/db_$(date +\%Y\%m\%d).sql
```
