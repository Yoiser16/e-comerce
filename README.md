<div align="center">

# 🏢 Sistema E-Commerce Enterprise

### Clean Architecture • DDD • CQRS • High Performance

[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.1-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

[**Documentación**](docs/) • [**Despliegue**](docs/DEPLOYMENT.md) • [**API**](docs/API_INTEGRATION.md) • [**Arquitectura**](docs/ARCHITECTURE.md)

</div>

---

## 📋 Visión General

Sistema de comercio electrónico de nivel empresarial diseñado para alta escalabilidad y mantenibilidad. Implementado siguiendo estrictamente **Clean Architecture** y **Domain-Driven Design (DDD)** para desacoplar las reglas de negocio de la infraestructura tecnológica.

### Características Clave

- **Arquitectura Hexagonal**: Inversión de dependencias y separación por capas.
- **Seguridad Enterprise**: Autenticación JWT rotativa, RBAC, auditoría y protección anti-abuso.
- **Micro-ready**: Diseño modular preparado para descomposición en microservicios.
- **High Performance**: API pública servida por FastAPI sobre asgi.
- **Production Ready**: Configurado para despliegue seguro en entornos VPS/Cloud.

---

## 📚 Documentación Técnica

Toda la documentación detallada se encuentra en el directorio `docs/`:

| Documento | Descripción |
|-----------|-------------|
| [📄 ARQUITECTURA](docs/ARCHITECTURE.md) | Diagramas de componentes, modelos de dominio y esquema de base de datos. |
| [🚀 DESPLIEGUE](docs/DEPLOYMENT.md) | Guía de instalación local y configuración en producción (VPS). |
| [🔌 INTEGRACIÓN API](docs/API_INTEGRATION.md) | Guía para desarrolladores frontend y consumidores de la API. |
| [🔐 SEGURIDAD](docs/SECURITY.md) | Detalles de autenticación, roles (RBAC) y auditoría. |
| [🧪 TESTING](docs/TESTING.md) | Guía de ejecución de pruebas y validación del sistema. |

---

## 🚀 Quick Start (Local)

Para una guía detallada, ver [DEPLOYMENT.md](docs/DEPLOYMENT.md).

```bash
# 1. Clonar y configurar entorno
git clone https://github.com/Yoiser16/e-comerce.git
cd e-comerce
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar entorno
cp .env.example .env
# (Editar .env con tus credenciales locales)

# 4. Iniciar base de datos y servidor
python manage.py migrate
python manage.py crear_usuarios_demo
python manage.py runserver
```

---

## 🏛️ Estructura del Proyecto

```
e-commerce/
├── docs/                 # 📚 Documentación técnica detallada
├── src/
│   ├── domain/           # 💎 Reglas de negocio (Entities, VOs)
│   ├── application/      # ⚙️ Casos de uso y orquestación
│   ├── infrastructure/   # 🔌 Implementación (Django, Postgres, JWT)
│   └── interfaces/       # 📱 API Rest, Admin
├── scripts/              # 🛠️ Scripts de utilidad i QA
└── manage.py             # Entry point
```

---

<div align="center">
    <sub>Copyright © 2026. Todos los derechos reservados.</sub>
</div>
