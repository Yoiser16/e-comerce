# Diagramas UML - E-Commerce Clean Architecture

## Tabla de Contenidos

- [Diagrama de Clases - Domain Layer](#diagrama-de-clases---domain-layer)
- [Diagrama de Secuencia - Crear Cliente](#diagrama-de-secuencia---crear-cliente)
- [Diagrama de Componentes](#diagrama-de-componentes)
- [Diagrama ER - Base de Datos](#diagrama-er---base-de-datos)

---

## Diagrama de Clases - Domain Layer

### Agregado Cliente

```
┌─────────────────────────────────────────────────────────────────┐
│                        <<Entity>>                                │
│                          Cliente                                 │
├─────────────────────────────────────────────────────────────────┤
│ - _id: UUID                                                      │
│ - _nombre: str                                                   │
│ - _apellido: str                                                 │
│ - _email: Email                    (Value Object)               │
│ - _documento: DocumentoIdentidad   (Value Object)               │
│ - _telefono: Optional[Telefono]    (Value Object)               │
│ - _activo: bool                                                  │
│ - _fecha_creacion: datetime                                      │
│ - _fecha_modificacion: datetime                                  │
├─────────────────────────────────────────────────────────────────┤
│ + __init__(nombre, apellido, email, documento, telefono=None)   │
│ + actualizar_informacion(nombre, apellido, telefono)            │
│ + cambiar_email(nuevo_email: Email)                             │
│ + activar()                                                      │
│ + desactivar()                                                   │
│ + nombre_completo() -> str                                       │
│ + validar_invariantes()                                          │
├─────────────────────────────────────────────────────────────────┤
│ Properties:                                                      │
│ + id: UUID                                                       │
│ + email: Email                                                   │
│ + documento: DocumentoIdentidad                                  │
│ + activo: bool                                                   │
└─────────────────────────────────────────────────────────────────┘
                           ▲
                           │ uses
          ┌────────────────┼────────────────┐
          │                │                │
     ┌────▼────┐     ┌─────▼────┐    ┌─────▼─────┐
     │  Email  │     │Documento │    │ Telefono  │
     │   (VO)  │     │Identidad │    │   (VO)    │
     └─────────┘     │   (VO)   │    └───────────┘
                     └──────────┘
```

### Value Objects

```
┌──────────────────────────────┐
│   <<Value Object>>           │
│        Email                 │
├──────────────────────────────┤
│ - _valor: str                │
├──────────────────────────────┤
│ + __init__(valor: str)       │
│ + validar()                  │
│ + valor() -> str             │
│ + __eq__(other) -> bool      │
└──────────────────────────────┘

┌──────────────────────────────┐
│   <<Value Object>>           │
│   DocumentoIdentidad         │
├──────────────────────────────┤
│ - _tipo: TipoDocumento       │
│ - _numero: str               │
├──────────────────────────────┤
│ + __init__(tipo, numero)     │
│ + validar()                  │
│ + tipo() -> TipoDocumento    │
│ + numero() -> str            │
│ + __eq__(other) -> bool      │
└──────────────────────────────┘

┌──────────────────────────────┐
│   <<Value Object>>           │
│        Telefono              │
├──────────────────────────────┤
│ - _valor: str                │
├──────────────────────────────┤
│ + __init__(valor: str)       │
│ + validar()                  │
│ + valor() -> str             │
│ + __eq__(other) -> bool      │
└──────────────────────────────┘
```

### Repository Interface (Domain)

```
┌─────────────────────────────────────────────────┐
│         <<Interface>>                           │
│       ClienteRepository                         │
├─────────────────────────────────────────────────┤
│ + guardar(cliente: Cliente) -> Cliente          │
│ + obtener_por_id(id: UUID) -> Optional[Cliente] │
│ + obtener_por_email(email: Email) -> Optional   │
│ + obtener_por_documento(doc) -> Optional        │
│ + buscar_por_nombre(nombre: str) -> List        │
│ + obtener_activos() -> List[Cliente]            │
│ + eliminar(id: UUID) -> bool                    │
└─────────────────────────────────────────────────┘
                    ▲
                    │ implements
                    │
┌───────────────────┴─────────────────────────────┐
│    ClienteRepositoryImpl                        │
│    (Infrastructure Layer)                       │
├─────────────────────────────────────────────────┤
│ - _logger: LoggerService                        │
│ - _auditoria: ServicioAuditoria                 │
├─────────────────────────────────────────────────┤
│ + guardar(cliente: Cliente) -> Cliente          │
│ + obtener_por_id(id: UUID) -> Optional[Cliente] │
│ + _to_domain(model: ClienteModel) -> Cliente    │
│ + _to_model(cliente: Cliente) -> ClienteModel   │
└─────────────────────────────────────────────────┘
```

---

## Diagrama de Secuencia - Crear Cliente

```
┌──────┐         ┌──────────┐         ┌───────────┐         ┌────────────┐         ┌──────────┐
│FastAPI│         │ UseCase  │         │Repository │         │Django Model│         │PostgreSQL│
└───┬──┘         └────┬─────┘         └─────┬─────┘         └──────┬─────┘         └────┬─────┘
    │                 │                     │                       │                     │
    │ POST /clientes  │                     │                       │                     │
    ├────────────────>│                     │                       │                     │
    │                 │                     │                       │                     │
    │                 │ 1. Validar DTO      │                       │                     │
    │                 ├─────────┐           │                       │                     │
    │                 │         │           │                       │                     │
    │                 │<────────┘           │                       │                     │
    │                 │                     │                       │                     │
    │                 │ 2. Crear entidad Cliente (Domain)          │                     │
    │                 ├──────────────┐      │                       │                     │
    │                 │              │      │                       │                     │
    │                 │<─────────────┘      │                       │                     │
    │                 │                     │                       │                     │
    │                 │ 3. guardar(cliente) │                       │                     │
    │                 ├────────────────────>│                       │                     │
    │                 │                     │                       │                     │
    │                 │                     │ 4. Verificar duplicados                     │
    │                 │                     ├──────────────────────>│                     │
    │                 │                     │                       │ SELECT email        │
    │                 │                     │                       ├────────────────────>│
    │                 │                     │                       │<────────────────────┤
    │                 │                     │<──────────────────────┤                     │
    │                 │                     │                       │                     │
    │                 │                     │ 5. _to_model()        │                     │
    │                 │                     ├───────────┐           │                     │
    │                 │                     │           │           │                     │
    │                 │                     │<──────────┘           │                     │
    │                 │                     │                       │                     │
    │                 │                     │ 6. model.save()       │                     │
    │                 │                     ├──────────────────────>│                     │
    │                 │                     │                       │ INSERT              │
    │                 │                     │                       ├────────────────────>│
    │                 │                     │                       │<────────────────────┤
    │                 │                     │<──────────────────────┤                     │
    │                 │                     │                       │                     │
    │                 │                     │ 7. Auditoria CREATE   │                     │
    │                 │                     ├───────────┐           │                     │
    │                 │                     │<──────────┘           │                     │
    │                 │                     │                       │                     │
    │                 │                     │ 8. Logging            │                     │
    │                 │                     ├───────────┐           │                     │
    │                 │                     │<──────────┘           │                     │
    │                 │                     │                       │                     │
    │                 │ 9. _to_domain()     │                       │                     │
    │                 │<────────────────────┤                       │                     │
    │                 │                     │                       │                     │
    │ 10. Return DTO  │                     │                       │                     │
    │<────────────────┤                     │                       │                     │
    │                 │                     │                       │                     │
```

---

## Diagrama de Componentes

```
┌────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   FastAPI    │  │    Django    │  │     CLI      │             │
│  │   Routers    │  │    Admin     │  │   Commands   │             │
│  └───────┬──────┘  └──────┬───────┘  └──────┬───────┘             │
└──────────┼────────────────┼──────────────────┼─────────────────────┘
           │                │                  │
           └────────────────┼──────────────────┘
                            │
┌───────────────────────────▼────────────────────────────────────────┐
│                     APPLICATION LAYER                              │
│  ┌──────────────────────────────────────────────────────┐          │
│  │              Use Cases (Business Logic)              │          │
│  │  • CrearClienteUseCase                               │          │
│  │  • ObtenerClienteUseCase                             │          │
│  │  • ActualizarClienteUseCase                          │          │
│  └──────────────────────────────────────────────────────┘          │
│  ┌──────────────────────────────────────────────────────┐          │
│  │              DTOs (Data Transfer Objects)            │          │
│  └──────────────────────────────────────────────────────┘          │
└──────────────────────────────┬─────────────────────────────────────┘
                               │
                               │ uses interfaces
                               │
┌──────────────────────────────▼─────────────────────────────────────┐
│                        DOMAIN LAYER                                │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐       │
│  │  Entities   │  │Value Objects│  │<<Interface>>         │       │
│  │  • Cliente  │  │  • Email    │  │ClienteRepository     │       │
│  │  • Producto │  │  • Telefono │  │ProductoRepository    │       │
│  │  • Orden    │  │  • Dinero   │  │OrdenRepository       │       │
│  └─────────────┘  └─────────────┘  └──────────────────────┘       │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐       │
│  │   Events    │  │ Exceptions  │  │      Policies        │       │
│  └─────────────┘  └─────────────┘  └──────────────────────┘       │
└────────────────────────────────────────────────────────────────────┘
                               ▲
                               │ implements
                               │
┌──────────────────────────────┴─────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                            │
│  ┌──────────────────────────────────────────────────────┐          │
│  │         Persistence (Repository Implementations)     │          │
│  │  • ClienteRepositoryImpl (Django ORM)                │          │
│  │  • ProductoRepositoryImpl                            │          │
│  │  • OrdenRepositoryImpl                               │          │
│  └──────────────────────────────────────────────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  PostgreSQL  │  │   Logging    │  │  Auditing    │             │
│  │  Django ORM  │  │   Service    │  │   Service    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└────────────────────────────────────────────────────────────────────┘
```

---

## Diagrama ER - Base de Datos

```
┌─────────────────────────────────────────┐
│             CLIENTES                    │
├─────────────────────────────────────────┤
│ PK  id                   UUID           │
│     nombre               VARCHAR(100)   │
│     apellido             VARCHAR(100)   │
│ UK  email                VARCHAR(254)   │
│     tipo_documento       VARCHAR(20)    │
│ UK  numero_documento     VARCHAR(50)    │
│     telefono             VARCHAR(20)    │
│ IDX activo               BOOLEAN        │
│     fecha_creacion       TIMESTAMPTZ    │
│     fecha_modificacion   TIMESTAMPTZ    │
└─────────────────────────────────────────┘
           │
           │ 1:N
           │
┌──────────▼──────────────────────────────┐
│             ORDENES                     │
├─────────────────────────────────────────┤
│ PK  id                   UUID           │
│ FK  cliente_id           UUID           │
│     numero_orden         VARCHAR(50)    │
│     estado               VARCHAR(20)    │
│     total                DECIMAL(10,2)  │
│     fecha_creacion       TIMESTAMPTZ    │
│     fecha_modificacion   TIMESTAMPTZ    │
└─────────────────────────────────────────┘
           │
           │ 1:N
           │
┌──────────▼──────────────────────────────┐
│          LINEAS_ORDEN                   │
├─────────────────────────────────────────┤
│ PK  id                   UUID           │
│ FK  orden_id             UUID           │
│ FK  producto_id          UUID           │
│     cantidad             INTEGER        │
│     precio_unitario      DECIMAL(10,2)  │
│     subtotal             DECIMAL(10,2)  │
└─────────────────────────────────────────┘
           │
           │ N:1
           │
┌──────────▼──────────────────────────────┐
│            PRODUCTOS                    │
├─────────────────────────────────────────┤
│ PK  id                   UUID           │
│     codigo               VARCHAR(50)    │
│     nombre               VARCHAR(200)   │
│     descripcion          TEXT           │
│     precio               DECIMAL(10,2)  │
│     stock                INTEGER        │
│     activo               BOOLEAN        │
│     fecha_creacion       TIMESTAMPTZ    │
│     fecha_modificacion   TIMESTAMPTZ    │
└─────────────────────────────────────────┘

LEYENDA:
  PK  = Primary Key
  FK  = Foreign Key
  UK  = Unique Key
  IDX = Index
```

---

## Diagrama de Estados - Orden

```
                        ┌──────────┐
                   ┌───>│ CREADA   │────┐
                   │    └──────────┘    │
                   │                    │ confirmar()
                   │ cancelar()         │
                   │                    ▼
                   │              ┌──────────┐
                   │              │CONFIRMADA│
                   │              └──────────┘
                   │                    │
                   │                    │ pagar()
                   │                    │
                   │                    ▼
                   │              ┌──────────┐
                   │              │  PAGADA  │
                   │              └──────────┘
                   │                    │
                   │                    │ enviar()
                   │                    │
┌──────────┐       │                    ▼
│CANCELADA │◄──────┼              ┌──────────┐
└──────────┘       │              │ ENVIADA  │
                   │              └──────────┘
                   │                    │
                   │                    │ entregar()
                   │                    │
                   │                    ▼
                   │              ┌──────────┐
                   └──────────────┤ENTREGADA │
                                  └──────────┘

TRANSICIONES VALIDAS:
  CREADA     -> CONFIRMADA | CANCELADA
  CONFIRMADA -> PAGADA | CANCELADA
  PAGADA     -> ENVIADA | CANCELADA
  ENVIADA    -> ENTREGADA
```

---

## Arquitectura de Capas - Flujo de Datos

```
                    ┌────────────────┐
                    │  HTTP Request  │
                    └───────┬────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │         INTERFACES LAYER              │
        │  ┌─────────────────────────────────┐  │
        │  │  FastAPI Router / Controller    │  │
        │  │  • Validacion request           │  │
        │  │  • Serializacion response       │  │
        │  └───────────┬─────────────────────┘  │
        └──────────────┼────────────────────────┘
                       │ DTO
                       ▼
        ┌───────────────────────────────────────┐
        │       APPLICATION LAYER               │
        │  ┌─────────────────────────────────┐  │
        │  │      Use Case                   │  │
        │  │  • Logica de aplicacion         │  │
        │  │  • Orquestacion                 │  │
        │  └───────────┬─────────────────────┘  │
        └──────────────┼────────────────────────┘
                       │ Domain Entity
                       ▼
        ┌───────────────────────────────────────┐
        │          DOMAIN LAYER                 │
        │  ┌─────────────────────────────────┐  │
        │  │   Business Logic                │  │
        │  │  • Validaciones de negocio      │  │
        │  │  • Reglas de dominio            │  │
        │  │  • Invariantes                  │  │
        │  └───────────┬─────────────────────┘  │
        └──────────────┼────────────────────────┘
                       │ via Repository Interface
                       ▼
        ┌───────────────────────────────────────┐
        │      INFRASTRUCTURE LAYER             │
        │  ┌─────────────────────────────────┐  │
        │  │  Repository Implementation      │  │
        │  │  • Mapeo Domain <-> ORM         │  │
        │  │  • Auditoria                    │  │
        │  │  • Logging                      │  │
        │  └───────────┬─────────────────────┘  │
        └──────────────┼────────────────────────┘
                       │ ORM Model
                       ▼
                ┌──────────────┐
                │  PostgreSQL  │
                └──────────────┘
```

---

**Convenciones de Diagramas:**
- `<<Interface>>`: Interfaz (abstracta)
- `<<Entity>>`: Entidad de dominio
- `<<Value Object>>`: Objeto de valor inmutable
- `PK`: Primary Key
- `FK`: Foreign Key
- `UK`: Unique Key
- `IDX`: Index
- `▲`: Implementa/Hereda
- `◄─`: Dependencia
- `───>`: Flujo/Navegacion
