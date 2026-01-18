# 🎉 CONFIGURACIÓN VPS COMPLETADA - BASE DE DATOS COMPARTIDA

## ✅ ESTADO: **FUNCIONANDO**

Tu backend e-commerce está ahora configurado para usar una **base de datos PostgreSQL compartida** en tu VPS. Tanto tú como tu compañero pueden trabajar conectándose a la misma base de datos.

---

## 📊 INFORMACIÓN DEL VPS

### 🖥️ Servidor
- **IP**: `72.61.73.245`
- **OS**: Ubuntu 24.04.3 LTS
- **SSH**: `root@72.61.73.245`
- **PostgreSQL**: Versión 16.11

### 🔓 Puertos Abiertos
- **22** - SSH
- **80** - HTTP
- **443** - HTTPS
- **5432** - PostgreSQL (BASE DE DATOS PÚBLICA)
- **8000** - API (opcional para despliegue)

---

## 🗄️ CREDENCIALES DE BASE DE DATOS

### PostgreSQL en VPS

```bash
Host: 72.61.73.245
Puerto: 5432
Base de datos: ecommerce_db
Usuario: ecommerce_user
Password: ecommerce_dev_2026!
```

### Cadena de Conexión

```
postgresql://ecommerce_user:ecommerce_dev_2026!@72.61.73.245:5432/ecommerce_db
```

### Para psql (terminal):
```bash
PGPASSWORD='ecommerce_dev_2026!' psql -h 72.61.73.245 -U ecommerce_user -d ecommerce_db
```

---

## 👥 USUARIOS DE LA APLICACIÓN

Estos usuarios ya están creados en la base de datos:

| Email | Password | Rol | Permisos |
|-------|----------|-----|----------|
| admin@ecommerce.com | Admin123! | ADMIN | Todos (crear, editar, eliminar) |
| operador@ecommerce.com | Operador123! | OPERADOR | Crear y editar (no eliminar) |
| lectura@ecommerce.com | Lectura123! | LECTURA | Solo lectura |

---

## 🚀 CÓMO EJECUTAR EL PROYECTO (PARA TI Y TU COMPAÑERO)

### 1. Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# O en Windows: venv\Scripts\activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar .env

Crear archivo `.env` en la raíz del proyecto con:

```env
# AMBIENTE
DJANGO_ENVIRONMENT=development
DJANGO_SECRET_KEY=34)6vobz_w#0v*4fqq-uyeo2cm@8zg++#1f$xpo$+-5*w9994c
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# BASE DE DATOS - VPS COMPARTIDO
DB_ENGINE=postgresql
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=ecommerce_dev_2026!
DB_HOST=72.61.73.245
DB_PORT=5432

# SSL
DB_SSL_MODE=disable
DB_CONN_MAX_AGE=0
```

### 5. Ejecutar el Servidor

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor (OPCIÓN 1 - FastAPI + Django)
cd s4. Ejecutar el Servidor

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor FastAPI + Django
cd src
python main.py
# Se5vidor en: http://localhostlhost:8000/admin

---

## 🧪 PROBAR LA API

Una vez iniciado el servidor, visita http://localhost:8000/docs para probar todos los endpoints de forma interactiva con Swagger UI.

---

## ⚠️ IMPORTANTE - TRABAJO EN EQUIPO

### ✅ VENTAJAS de la Base de Datos Compartida

1. **Datos sincronizados**: Ambos ven los mismos datos en tiempo real
2. **No hay conflictos**: No necesitan sincronizar bases de datos
3. **Pruebas reales**: Pueden probar flujos completos entre ambos
4. **Desarrollo más rápido**: No pierden tiempo en configuración local

### 🚨 CUIDADOS

1. **Comunicación**: Avisar antes de hacer cambios grandes en BD
2. **Migraciones**: Coordinar cuando van a ejecutar `python manage.py migrate`
3. **Datos de prueba**: No borren datos que el otro esté usando
4. **Respaldos**: El VPS hace backups automáticos, pero por si acaso

### 💡 BUENAS PRÁCTICAS

```bash
# ANTES de hacer cambios importantes:
# 1. Avisar a tu compañero
# 2. Hacer un backup (opcional)
ssh root@72.61.73.245 "pg_dump -U ecommerce_user ecommerce_db > backup_$(date +%Y%m%d).sql"

# COMUNICAR cuando:
# - Vas a ejecutar migraciones nuevas
# - Vas a cambiar estructura de tablas
# - Vas a borrar datos de prueba
```

---

## 🔧 COMANDOS ÚTILES

### Ver Estado de la BD

```bash
# Desde tu máquina (con psql instalado)
psql -h 72.61.73.245 -U ecommerce_user -d ecommerce_db -c "\dt"

# Ver cantidad de registros
psql -h 72.61.73.245 -U ecommerce_user -d ecommerce_db -c "
  SELECT 'Clientes' as tabla, COUNT(*) FROM ecommerce_persistence_clientemodel
  UNION ALL
  SELECT 'Productos', COUNT(*) FROM ecommerce_persistence_productomodel
  UNION ALL
  SELECT 'Órdenes', COUNT(*) FROM ecommerce_persistence_ordenmodel;
"
```

### Crear Datos de Prueba

```bash
```bash
# Ver tablas en la BD
PGPASSWORD='ecommerce_dev_2026!' psql -h 72.61.73.245 -U ecommerce_user -d ecommerce_db -c "\dt"

# Crear usuarios de demo
source venv/bin/activate
python manage.py crear_usuarios_demo

# S
### Configuración

1. **`.env`** (EN TU MÁQUINA)
   - Configuración con credenciales del VPS
   - ⚠️ NO COMMITEAR A GIT
   - Tu compañero debe crear su propio `.env` con las mismas credenciales

2. **`.env.example`**
   - Plantilla de ejemplo (sin credenciales)
   - Este SÍ se puede commitear

---

## 🎯 PRÓXIMOS PASOS PARA EL DESARROLLO

### Para ti:
1. ✅ Backend funcionando localmente conectado al VPS
2. ✅ Usuarios de prueba creados
3. 🔜 Empezar a desarrollar el frontend

### Para tu compañero:
1. Clonar el repositorio
2. Copiar las credenciales

**`.env`** (EN TU MÁQUINA)
- Configuración con credenciales del VPS
- ⚠️ NO COMMITEAR A GIT
- Tu compañero debe crear su propio `.env` con las mismas credenciales

**`.env.example`**
- Plantilla de ejemplo (sin credenciales)
suario: ecommerce_user
- Password: ecommerce_dev_2026!

### Setup Rápido:
1. Clona el repo
2. Crea entorno virtual: `python3 -m venv venv`
3. Activa: `source venv/bin/activate`
4. Instala: `pip install -r requirements.txt`
5. Crea `.env` (te paso el contenido abajo)
6. Ejecuta: `cd src && python main.py`
7. Ve a: http://localhost:8000/docs

### Contenido del .env:
```
DJANGO_ENVIRONMENT=development
DJANGO_SECRET_KEY=34)6vobz_w#0v*4fqq-uyeo2cm@8zg++#1f$xpo$+-5*w9994c
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=postgresql
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=ecommerce_dev_2026!
DB_HOST=72.61.73.245
DB_PORT=5432

DB_SSL_MODE=disable
DB_CONN_MAX_AGE=0
```

### Usuarios de Prueba:
- Admin: admin@ecommerce.com / Admin123!
- Operador: operador@ecommerce.com / Operador123!
- Lectura: lectura@ecommerce.com / Lectura123!

¡Listo para rockear! 🎸
```

---

## 🔒 SEGURIDAD (PARA PRODUCCIÓN FUTURA)

⚠️ **IMPORTANTE**: Esta configuración es para **DESARROLLO SOLAMENTE**.

### Antes de pasar a producción:
1. ✅ Cambiar todas las contraseñas
2. ✅ Configurar SSL en PostgreSQL
3. ✅ Restringir acceso por IP (no público)
4. ✅ Usar VPN o túnel SSH
5. ✅ Implementar certificados SSL
6. ✅ Configurar backup automático
7. ✅ Habilitar logs de auditoría

---

## 📞 SOPORTE

### Si algo no funciona:

1. **Verificar conexión a BD**:
   ```bash
   bash scripts/test_db_connection.sh
   ```

2. **Ver logs del servidor**:
   ```bash
   ssh root@72.61.73.245 "tail -f /var/log/postgresql/postgresql-16-main.log"
   ```

3. **Reiniciar PostgreSQL en VPS**:
   ```bash
   ssh root@72.61.73.245 "systemctl restart postgresql"
   ```

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [x] PostgreSQL instalado en VPS
- [x] Base de datos `ecommerce_db` creada
- [x] Usuario `ecommerce_user` con permisos
- [x] Puerto 5432 abierto en firewall
- [x] Configuración remota habilitada
- [x] Conexión probada desde máquina local
- [x] Migraciones ejecutadas
- [x] Usuarios de prueba creados
- [x] Servidor backend funcionando
- [x] Documentación completa

---
 logs del servidor**:
   ```bash
   ssh root@72.61.73.245 "tail -f /var/log/postgresql/postgresql-16-main.log"
   ```

2