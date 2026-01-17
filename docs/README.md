# Indice de Documentacion - E-Commerce Clean Architecture

Documentacion completa del sistema organizada por temas.

---

## Documentacion Principal

### [README.md](../README.md)
**Documento principal del proyecto**

Contenido:
- Vision general del sistema
- Arquitectura Clean Architecture
- Diagramas de capas y flujo
- Estructura del proyecto
- Instalacion completa
- Configuracion
- Uso y comandos
- Testing
- Deployment
- Roadmap

---

## Diagramas y Arquitectura

### [UML_DIAGRAMS.md](UML_DIAGRAMS.md)
**Diagramas UML completos del sistema**

Incluye:
- Diagrama de Clases (Domain Layer)
- Diagrama de Secuencia (Crear Cliente)
- Diagrama de Componentes
- Diagrama ER (Base de Datos)
- Diagrama de Estados (Orden)
- Flujo de Datos por Capas

**Convenciones:**
```
<<Interface>>   = Interfaz abstracta
<<Entity>>      = Entidad de dominio
<<Value Object>> = Objeto de valor inmutable
PK / FK / UK    = Primary/Foreign/Unique Key
▲ / ◄─ / ───>   = Relaciones y flujos
```

---

## Base de Datos

### [ESQUEMA_DATABASE.md](ESQUEMA_DATABASE.md)
**Esquema detallado de PostgreSQL**

Contenido:
- Resumen general (11 tablas)
- Tabla `clientes` (detalles completos)
  - 10 columnas
  - 8 indices
  - 12 constraints
- Tablas de Django (autenticacion, admin, etc.)
- Mapeo Domain ↔ ORM
- Value Objects mapeados
- Reglas de negocio implementadas
- Queries SQL utiles

---

### [DATABASE_CONFIG.md](DATABASE_CONFIG.md)
**Guia completa de configuracion de base de datos**

Contenido:
- Vision general de arquitectura
- Componentes del sistema
  - DatabaseConfig class
  - Validaciones estrictas
  - Variables de entorno
- Configuracion por ambiente
  - Desarrollo
  - Staging
  - Produccion
- Comandos utiles
- Seguridad y best practices
- Troubleshooting

**Variables requeridas:**
```env
DB_ENGINE=postgresql
DB_NAME=ecomerce_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_SSL_MODE=disable
```

---

## Deployment

### [DEPLOYMENT_HOSTINGER.md](DEPLOYMENT_HOSTINGER.md)
**Guia paso a paso para deployment en Hostinger VPS**

Contenido:
- Requisitos del servidor
- Instalacion de dependencias
- Configuracion de PostgreSQL
- Configuracion de Nginx
- Configuracion de Supervisor
- SSL con Let's Encrypt
- Mantenimiento y actualizaciones

**Plan minimo:**
- VPS KVM 1 o superior
- 1 vCPU, 4 GB RAM, 50 GB SSD
- Ubuntu 22.04/24.04 LTS

---

## Scripts y Utilidades

### [scripts/README.md](../scripts/README.md)
**Documentacion de scripts de utilidad**

Scripts disponibles:
- `validar_sistema.py` - Validacion end-to-end
- `shell_commands.py` - Comandos pre-configurados

Comandos Django Management:
- `python manage.py validar_sistema`
- `python manage.py check_database`

---

## Mapa de Navegacion

```
📚 Documentacion
│
├── 📖 README.md (Principal)
│   ├── Vision general
│   ├── Arquitectura
│   ├── Instalacion
│   ├── Uso
│   └── Roadmap
│
├── 🎨 UML_DIAGRAMS.md
│   ├── Diagrama de Clases
│   ├── Diagrama de Secuencia
│   ├── Diagrama de Componentes
│   ├── Diagrama ER
│   └── Diagrama de Estados
│
├── 🗄️ Base de Datos
│   ├── ESQUEMA_DATABASE.md
│   │   ├── Tablas
│   │   ├── Indices
│   │   └── Constraints
│   │
│   └── DATABASE_CONFIG.md
│       ├── Configuracion
│       ├── Validaciones
│       └── Seguridad
│
├── 🚀 DEPLOYMENT_HOSTINGER.md
│   ├── Preparacion servidor
│   ├── Configuracion
│   ├── Nginx + SSL
│   └── Mantenimiento
│
└── 🛠️ scripts/README.md
    ├── validar_sistema.py
    ├── shell_commands.py
    └── Comandos Django
```

---

## Quick Links

| Necesito... | Ver documento |
|-------------|---------------|
| Empezar con el proyecto | [README.md](../README.md) |
| Entender la arquitectura | [README.md](../README.md#arquitectura) + [UML_DIAGRAMS.md](UML_DIAGRAMS.md) |
| Configurar base de datos | [DATABASE_CONFIG.md](DATABASE_CONFIG.md) |
| Ver esquema de tablas | [ESQUEMA_DATABASE.md](ESQUEMA_DATABASE.md) |
| Hacer deployment | [DEPLOYMENT_HOSTINGER.md](DEPLOYMENT_HOSTINGER.md) |
| Validar el sistema | [scripts/README.md](../scripts/README.md) |
| Ver diagramas UML | [UML_DIAGRAMS.md](UML_DIAGRAMS.md) |

---

## Convenciones de Documentacion

### Formato de Codigo

```python
# Bloques de codigo Python con syntax highlighting
def ejemplo():
    return "Codigo de ejemplo"
```

```bash
# Comandos de terminal
python manage.py migrate
```

```sql
-- Queries SQL
SELECT * FROM clientes;
```

### Indicadores Visuales

- ✅ Implementado / Completado
- ⏳ En progreso
- ❌ No implementado / Error
- ⚠️ Advertencia
- 📌 Nota importante
- 🔥 Critico
- 💡 Tip / Sugerencia

### Diagramas ASCII

Usamos diagramas ASCII para:
- Arquitectura de capas
- Flujos de datos
- Estructuras de directorios
- Relaciones entre componentes

---

## Actualizaciones

**Ultima actualizacion**: 16 de enero de 2026

**Changelog**:
- 2026-01-16: Reorganizacion completa de documentacion
- 2026-01-16: Agregados diagramas UML
- 2026-01-16: Migracion a PostgreSQL documentada
- 2026-01-16: Limpieza de archivos obsoletos

---

## Contribuir a la Documentacion

Para agregar o mejorar documentacion:

1. Mantener estructura consistente
2. Usar Markdown estandar
3. Agregar ejemplos de codigo
4. Incluir diagramas cuando ayude a la claridad
5. Actualizar este indice
6. Actualizar changelog

---

<div align="center">

**[⬆ README Principal](../README.md)**

</div>
