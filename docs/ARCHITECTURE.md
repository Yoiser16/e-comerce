# 🏗️ Arquitectura del Sistema

## Visión General

La arquitectura está diseñada concéntricamente siguiendo los principios de **Clean Architecture**. Las dependencias fluyen **únicamente hacia adentro**, protegiendo el Dominio de cambios externos.

```
┌─────────────────────────────────────────────────────────────────┐
│                    📱 INTERFACES LAYER                          │
│         FastAPI Router │ Django Admin │ CLI Commands            │
├─────────────────────────────────────────────────────────────────┤
│                    ⚙️ APPLICATION LAYER                         │
│           Use Cases │ DTOs │ Commands │ Queries                 │
├─────────────────────────────────────────────────────────────────┤
│                    💎 DOMAIN LAYER (Núcleo)                     │
│    Entities │ Value Objects │ Repository Interfaces │ Events   │
├─────────────────────────────────────────────────────────────────┤
│                    🔌 INFRASTRUCTURE LAYER                      │
│      Django ORM │ PostgreSQL │ JWT │ Auditing │ External APIs   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
              Las dependencias fluyen HACIA ADENTRO
```

## Diagrama de Componentes

```mermaid
graph TD
    subgraph Presentation ["📱 Capa de Presentación"]
        API[FastAPI Router]
        Admin[Django Admin]
        CLI[Comandos CLI]
    end

    subgraph Application ["⚙️ Capa de Aplicación"]
        UseCases[Casos de Uso]
        DTOs[DTOs / Esquemas]
        Ports[Puertos / Interfaces]
    end

    subgraph Domain ["💎 Capa de Dominio"]
        Entities[Entidades y Agregados]
        VO[Value Objects]
        RepoInt[Interfaces de Repositorio]
        Events[Eventos de Dominio]
    end

    subgraph Infrastructure ["🔌 Capa de Infraestructura"]
        RepoImpl[Implementación Repos]
        ORM[Django ORM]
        Postgres[(PostgreSQL)]
        JWT[JWT Auth]
    end

    Presentation --> Application
    Application --> Domain
    Infrastructure --> Domain
    
    RepoImpl -. Implementa .-> RepoInt
    RepoImpl --> ORM
    ORM --> Postgres
    
    style Domain fill:#fff3e0,stroke:#ff6f00,stroke-width:2px
    style Application fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Infrastructure fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Presentation fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

## 🧠 Modelado de Dominio

### Entidades Principales

```mermaid
classDiagram
    class Cliente {
        -UUID id
        -String nombre
        -Email email
        -DocumentoIdentidad documento
        -bool activo
        +activar()
        +desactivar()
    }

    class Producto {
        -UUID id
        -String nombre
        -CodigoProducto codigo
        -Dinero precio
        -int stock
        +reducir_stock(cantidad)
        +aumentar_stock(cantidad)
    }

    class Orden {
        -UUID id
        -Cliente cliente
        -List~LineaOrden~ lineas
        -EstadoOrden estado
        -Dinero total
        +agregar_linea(producto, cantidad)
        +confirmar()
        +cancelar()
    }

    class Email {
        <<Value Object>>
        -String direccion
        +validar()
    }

    class Dinero {
        <<Value Object>>
        -Decimal monto
        -String moneda
        +sumar(otro)
        +multiplicar(factor)
    }

    Cliente *-- Email
    Cliente *-- DocumentoIdentidad
    Orden --> Cliente
    Orden *-- LineaOrden
    Producto *-- Dinero
```

### Ciclo de Vida de Órdenes

```mermaid
stateDiagram-v2
    [*] --> CREADA: Checkout
    CREADA --> CONFIRMADA: Pago Exitoso
    CREADA --> CANCELADA: Cancelar
    CONFIRMADA --> ENVIADA: Despachar
    CONFIRMADA --> CANCELADA: Cancelar Admin
    ENVIADA --> ENTREGADA: Confirmar Entrega
    ENTREGADA --> [*]
    CANCELADA --> [*]
```

## 💾 Base de Datos

### Esquema ER

```mermaid
erDiagram
    CLIENTES ||--o{ ORDENES : realiza
    ORDENES ||--|{ LINEAS_ORDEN : contiene
    PRODUCTOS ||--o{ LINEAS_ORDEN : referencia

    CLIENTES {
        uuid id PK
        string nombre
        string email UK
        string tipo_documento
        string numero_documento
        string telefono
        bool activo
        datetime created_at
    }

    PRODUCTOS {
        uuid id PK
        string codigo UK
        string nombre
        decimal precio
        int stock
        bool activo
        datetime created_at
    }

    ORDENES {
        uuid id PK
        uuid cliente_id FK
        decimal total
        enum estado
        datetime created_at
    }

    LINEAS_ORDEN {
        uuid id PK
        uuid orden_id FK
        uuid producto_id FK
        int cantidad
        decimal precio_unitario
        decimal subtotal
    }
```
