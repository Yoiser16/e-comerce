# E-Commerce - Clean Architecture

> Sistema empresarial de gestion de comercio electronico implementando Clean Architecture con Python, Django y PostgreSQL.

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.1-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Tabla de Contenidos

- [Vision General](#vision-general)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Diagramas UML](#diagramas-uml)
- [Tecnologias](#tecnologias)
- [Instalacion](#instalacion)
- [Configuracion](#configuracion)
- [Uso](#uso)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentacion](#documentacion)
- [Contribucion](#contribucion)

---

## Vision General

**E-Commerce** es un sistema empresarial diseñado con **Clean Architecture** (Arquitectura Hexagonal) que garantiza:

- **Independencia de frameworks**: El dominio no conoce Django, FastAPI ni PostgreSQL
- **Testeable**: Logica de negocio aislada y facilmente testeable
- **Mantenible**: Separacion clara de responsabilidades por capas
- **Escalable**: Preparado para event-driven architecture y microservicios

### Estado del Proyecto

```
[████████████████████░░░░] 80% - Fase 1: Persistencia con PostgreSQL

✅ Domain Layer completo
✅ Application Layer (Use Cases + DTOs)
✅ Infrastructure Layer (Repositories + ORM)
✅ PostgreSQL configurado y validado
✅ Sistema de auditoria y logging
⏳ FastAPI API endpoints
⏳ Autenticacion y autorizacion
⏳ Testing suite completo
```

---

## Arquitectura

### Clean Architecture - Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERFACES LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   FastAPI    │  │    Django    │  │     CLI      │         │
│  │   Routers    │  │    Admin     │  │   Commands   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Use Cases (Casos de Uso)                     │  │
│  │  • CrearClienteUseCase                                    │  │
│  │  • ObtenerClienteUseCase                                  │  │
│  │  • ActualizarClienteUseCase                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                DTOs (Data Transfer Objects)               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                        DOMAIN LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Entities    │  │Value Objects │  │ Repositories │         │
│  │  • Cliente   │  │  • Email     │  │ (Interfaces) │         │
│  │  • Producto  │  │  • Telefono  │  │              │         │
│  │  • Orden     │  │  • Dinero    │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │    Events    │  │  Exceptions  │  │   Policies   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Repositories │  │  PostgreSQL  │  │   Logging    │         │
│  │  (Impl)      │  │  Django ORM  │  │  Auditing    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Flujo de Dependencias

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  Interface  │ ────> │ Application │ ────> │   Domain    │
└─────────────┘       └─────────────┘       └─────────────┘
                             ▲                      ▲
                             │                      │
                      ┌──────┴──────┐              │
                      │Infrastructure│──────────────┘
                      └─────────────┘
```

**Regla de Oro**: Las dependencias SIEMPRE apuntan hacia el dominio.

---

## Estructura del Proyecto

```
e-comerce/
├── src/
│   ├── domain/                    # ⭐ NUCLEO DE NEGOCIO
│   │   ├── entities/              # Entidades del dominio
│   │   │   ├── base.py
│   │   │   ├── cliente.py         # ✅ Implementado
│   │   │   ├── orden.py
│   │   │   └── producto.py
│   │   ├── value_objects/         # Objetos de valor
│   │   │   ├── email.py           # ✅ Implementado
│   │   │   ├── telefono.py        # ✅ Implementado
│   │   │   ├── documento_identidad.py  # ✅ Implementado
│   │   │   ├── dinero.py
│   │   │   └── linea_orden.py
│   │   ├── repositories/          # Interfaces de repositorios
│   │   │   ├── cliente_repository.py  # ✅ Interface
│   │   │   ├── orden_repository.py
│   │   │   └── producto_repository.py
│   │   ├── events/                # Eventos de dominio
│   │   ├── exceptions/            # Excepciones de dominio
│   │   └── policies/              # Politicas de negocio
│   │
│   ├── application/               # ⚙️ CASOS DE USO
│   │   ├── use_cases/
│   │   │   ├── cliente_use_cases.py   # ✅ Implementado
│   │   │   └── orden_use_cases.py
│   │   ├── dto/                   # Data Transfer Objects
│   │   │   ├── cliente_dto.py     # ✅ Implementado
│   │   │   └── orden_dto.py
│   │   ├── commands/              # Comandos CQRS
│   │   └── queries/               # Queries CQRS
│   │
│   ├── infrastructure/            # 🔧 IMPLEMENTACIONES TECNICAS
│   │   ├── persistence/
│   │   │   ├── django/
│   │   │   │   ├── models.py      # ✅ ClienteModel
│   │   │   │   ├── migrations/    # ✅ 0001_initial
│   │   │   │   └── admin.py
│   │   │   └── repositories/
│   │   │       └── cliente_repository_impl.py  # ✅ Implementado
│   │   ├── config/
│   │   │   ├── django_settings.py     # ✅ Configuracion Django
│   │   │   └── database_config.py     # ✅ Config PostgreSQL
│   │   ├── logging/
│   │   │   └── logger_service.py      # ✅ Logging estructurado
│   │   ├── auditing/
│   │   │   └── servicio_auditoria.py  # ✅ Sistema de auditoria
│   │   └── management/
│   │       └── commands/
│   │           ├── validar_sistema.py     # ✅ Comando validacion
│   │           └── check_database.py      # ✅ Comando DB check
│   │
│   ├── interfaces/                # 🌐 PUNTOS DE ENTRADA
│   │   ├── api/
│   │   │   └── fastapi/
│   │   │       ├── app.py
│   │   │       └── cliente_router.py
│   │   └── permissions/
│   │
│   ├── shared/                    # 🔄 COMPARTIDO
│   │   ├── enums/
│   │   ├── constants/
│   │   ├── errors/
│   │   └── utils/
│   │
│   └── main.py                    # 🚀 Punto de entrada
│
├── docs/                          # 📚 DOCUMENTACION
│   ├── ESQUEMA_DATABASE.md        # ✅ Esquema PostgreSQL
│   ├── DATABASE_CONFIG.md         # ✅ Configuracion BD
│   └── DEPLOYMENT_HOSTINGER.md    # Guia deployment
│
├── scripts/                       # 🛠️ UTILIDADES
│   ├── validar_sistema.py
│   └── shell_commands.py
│
├── requirements.txt               # ✅ Dependencias
├── requirements-prod.txt
├── manage.py                      # ✅ Django CLI
├── .env.example                   # ✅ Variables de entorno
└── README.md                      # ✅ Este archivo
```

---

## Diagramas UML

Para ver los diagramas completos consulta: **[docs/UML_DIAGRAMS.md](docs/UML_DIAGRAMS.md)**

### Preview: Diagrama de Secuencia - Crear Cliente

```
FastAPI -> UseCase -> Repository -> Django ORM -> PostgreSQL
  │          │           │              │             │
  │ POST     │ validar   │ guardar()    │ INSERT      │
  │─────────>│──────────>│─────────────>│────────────>│
  │          │           │              │             │
  │<─────────│<──────────│<─────────────│<────────────│
  │ DTO      │ Domain    │ Auditoria    │ Commit      │
```

**Incluye:**
- Diagrama de Clases (Domain Layer)
- Diagramas de Secuencia (Use Cases)
- Diagrama de Componentes
- Diagrama ER (Base de Datos)
- Diagrama de Estados (Orden)
- Flujo de Datos por Capas

---

## Tecnologias

### Core

| Tecnologia | Version | Proposito |
|------------|---------|-----------|
| Python | 3.14+ | Lenguaje principal |
| Django | 6.0.1 | ORM, Admin, Migraciones |
| PostgreSQL | 18.1 | Base de datos produccion |
| FastAPI | 0.128.0 | API REST de alto rendimiento |

### Librerias Principales

```python
# requirements.txt
django>=6.0.0              # Framework web, ORM
psycopg[binary]>=3.2.0     # Driver PostgreSQL
fastapi>=0.115.0           # API framework
uvicorn[standard]>=0.32.0  # ASGI server
pydantic>=2.10.0           # Validacion de datos
python-dotenv>=1.0.0       # Variables de entorno
```

### Herramientas de Desarrollo

- **Black**: Formateo de codigo
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing framework
- **Coverage**: Code coverage

---

## Instalacion

### Prerequisitos

- Python 3.14 o superior
- PostgreSQL 14+ (instalado y corriendo)
- Git
- pip y venv

### Paso 1: Clonar Repositorio

```bash
git clone https://github.com/tu-usuario/e-comerce.git
cd e-comerce
```

### Paso 2: Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
# Desarrollo
pip install -r requirements.txt

# Produccion
pip install -r requirements-prod.txt
```

### Paso 4: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env
```

**Variables requeridas:**

```env
# Base de datos
DB_ENGINE=postgresql
DB_NAME=ecomerce_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_SSL_MODE=disable

# Django
DJANGO_SECRET_KEY=genera-una-clave-segura
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### Paso 5: Crear Base de Datos PostgreSQL

```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE ecomerce_db;

-- Crear usuario (si es necesario)
CREATE USER ecomerce_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE ecomerce_db TO ecomerce_user;

-- Salir
\\q
```

### Paso 6: Ejecutar Migraciones

```bash
python manage.py migrate
```

### Paso 7: Verificar Instalacion

```bash
# Verificar conexion a BD
python manage.py check_database

# Validar sistema completo
python manage.py validar_sistema

# Verificar Django
python manage.py check
```

**Salida esperada:**
```
================================================================================
VERIFICACION DE CONFIGURACION DE BASE DE DATOS
================================================================================
✅ Conexion exitosa
   Version PostgreSQL: PostgreSQL 18.1
📊 Tablas en la base de datos: 11
================================================================================
```

---

## Configuracion

### Configuracion de Base de Datos

Consulta la guia completa: **[docs/DATABASE_CONFIG.md](docs/DATABASE_CONFIG.md)**

**Configuracion por ambiente:**

- **Desarrollo**: SQLite o PostgreSQL local
- **Staging**: PostgreSQL con SSL
- **Produccion**: PostgreSQL con SSL verify-full

### Configuracion de Logging

```python
# src/infrastructure/config/django_settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

---

## Uso

### Comandos Django Management

```bash
# Validar sistema completo
python manage.py validar_sistema

# Verificar configuracion de BD
python manage.py check_database

# Crear superusuario para Django Admin
python manage.py createsuperuser

# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell interactivo
python manage.py shell
```

### Usar el Sistema en Python

```python
# Importar casos de uso
from application.use_cases.cliente_use_cases import CrearClienteUseCase
from application.dto.cliente_dto import CrearClienteDTO
from infrastructure.persistence.repositories.cliente_repository_impl import ClienteRepositoryImpl
from shared.enums.tipos_documento import TipoDocumento

# Inicializar
repo = ClienteRepositoryImpl()
use_case = CrearClienteUseCase(repo)

# Crear cliente
dto = CrearClienteDTO(
    nombre="Juan",
    apellido="Perez",
    email="juan.perez@example.com",
    tipo_documento=TipoDocumento.DNI,
    numero_documento="12345678",
    telefono="555-1234"
)

cliente = use_case.ejecutar(dto)
print(f"Cliente creado: {cliente.id}")
```

### FastAPI (Proximo)

```bash
# Ejecutar servidor de desarrollo
uvicorn src.main:app --reload --port 8000

# Documentacion interactiva
http://localhost:8000/docs
```

---

## Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html

# Solo tests de dominio
pytest tests/domain/

# Tests especificos
pytest tests/domain/entities/test_cliente.py -v
```

### Estructura de Tests

```
tests/
├── domain/
│   ├── entities/
│   │   ├── test_cliente.py
│   │   ├── test_producto.py
│   │   └── test_orden.py
│   ├── value_objects/
│   │   ├── test_email.py
│   │   ├── test_telefono.py
│   │   └── test_documento_identidad.py
│   └── repositories/
├── application/
│   └── use_cases/
│       └── test_cliente_use_cases.py
├── infrastructure/
│   └── persistence/
│       └── test_cliente_repository_impl.py
└── integration/
    └── test_cliente_flow.py
```

---

## Deployment

### Deployment en Hostinger VPS

Consulta la guia completa: **[docs/DEPLOYMENT_HOSTINGER.md](docs/DEPLOYMENT_HOSTINGER.md)**

**Resumen:**

1. Conectar por SSH al VPS
2. Instalar dependencias (Python, PostgreSQL, Nginx)
3. Clonar repositorio
4. Configurar variables de entorno
5. Ejecutar migraciones
6. Configurar Supervisor (process manager)
7. Configurar Nginx (reverse proxy)
8. Activar SSL con Let's Encrypt

### Docker (Opcional)

```bash
# Construir imagen
docker build -t ecommerce:latest .

# Ejecutar contenedor
docker run -p 8000:8000 ecommerce:latest

# Docker Compose
docker-compose up -d
```

---

## Documentacion

### Documentos Disponibles

| Documento | Descripcion |
|-----------|-------------|
| [README.md](README.md) | Este archivo - Documentacion principal |
| [docs/UML_DIAGRAMS.md](docs/UML_DIAGRAMS.md) | Diagramas UML completos |
| [docs/ESQUEMA_DATABASE.md](docs/ESQUEMA_DATABASE.md) | Esquema detallado de PostgreSQL |
| [docs/DATABASE_CONFIG.md](docs/DATABASE_CONFIG.md) | Configuracion de base de datos |
| [docs/DEPLOYMENT_HOSTINGER.md](docs/DEPLOYMENT_HOSTINGER.md) | Guia de deployment |

### Generar Documentacion API

```bash
# Con Sphinx
cd docs
make html

# Ver en navegador
open _build/html/index.html
```

---

## Contribucion

### Workflow de Desarrollo

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

### Convenciones de Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: nueva funcionalidad
fix: correccion de bug
docs: cambios en documentacion
style: formateo, puntos y comas
refactor: refactorizacion de codigo
test: agregar tests
chore: mantenimiento
```

### Code Style

```bash
# Formatear codigo
black src/

# Linting
flake8 src/

# Type checking
mypy src/
```

---

## Roadmap

### Fase 1: Persistencia (ACTUAL) - 80% Completo

- [x] Domain Layer completo
- [x] Application Layer (Use Cases + DTOs)
- [x] Infrastructure Layer (Repositories + ORM)
- [x] PostgreSQL configurado y validado
- [x] Sistema de auditoria y logging
- [ ] Completar entidades Producto y Orden

### Fase 2: API REST - Proximo

- [ ] Endpoints FastAPI para Cliente
- [ ] Autenticacion JWT
- [ ] Autorizacion basada en roles
- [ ] Documentacion OpenAPI
- [ ] Rate limiting

### Fase 3: Testing

- [ ] Tests unitarios (100% coverage Domain)
- [ ] Tests de integracion
- [ ] Tests end-to-end
- [ ] Performance testing

### Fase 4: Event-Driven Architecture

- [ ] Domain Events
- [ ] Event Bus
- [ ] Event Sourcing (opcional)
- [ ] CQRS completo

### Fase 5: Deployment y Monitoring

- [ ] CI/CD con GitHub Actions
- [ ] Docker containers
- [ ] Kubernetes (opcional)
- [ ] Monitoring con Prometheus
- [ ] Logging centralizado (ELK)

---

## Licencia

Este proyecto esta licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## Contacto

**Equipo de Desarrollo**
- Email: contacto@ecommerce.com
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

---

## Agradecimientos

- Clean Architecture de Robert C. Martin
- Domain-Driven Design de Eric Evans
- Comunidad de Python y Django

---

<div align="center">

**[⬆ Volver arriba](#e-commerce---clean-architecture)**

Hecho con ❤️ usando Clean Architecture

</div>
