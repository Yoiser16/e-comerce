# 🎨 UML Diagrams - E-Commerce Clean Architecture

This document contains the architectural diagrams for the E-Commerce system.
You can view these diagrams natively on GitHub, GitLab, or using a Mermaid Preview plugin in VS Code.

## 📋 Table of Contents

- [Class Diagram - Domain Layer](#class-diagram---domain-layer)
- [Sequence Diagram - Create Client](#sequence-diagram---create-client)
- [Component Diagram](#component-diagram)
- [ER Diagram - Database](#er-diagram---database)
- [State Diagram - Order](#state-diagram---order)

---

## Class Diagram - Domain Layer

This diagram illustrates the **Client Aggregate** and its related Value Objects. Note the strict use of Value Objects for validation.

```mermaid
classDiagram
    class Cliente {
        -UUID id
        -String nombre
        -String apellido
        -Email email
        -DocumentoIdentidad documento
        -Telefono telefono
        -bool activo
        -DateTime fecha_creacion
        +activar()
        +desactivar()
        +actualizar_informacion()
        +cambiar_email()
    }

    class Email {
        <<Value Object>>
        -String valor
        +validar()
    }

    class DocumentoIdentidad {
        <<Value Object>>
        -TipoDocumento tipo
        -String numero
        +validar()
    }

    class Telefono {
        <<Value Object>>
        -String valor
        +validar()
    }

    %% Relationships
    Cliente *-- Email : uses
    Cliente *-- DocumentoIdentidad : uses
    Cliente *-- Telefono : optional

    %% Repository Interface
    class ClienteRepository {
        <<Interface>>
        +guardar(cliente)
        +buscar_por_id(id)
        +buscar_por_email(email)
    }

    ClienteRepository ..> Cliente : uses
```

---

## Sequence Diagram - Create Client

Shows the flow of data from the API endpoint down to the database and back, highlighting the **Clean Architecture** layers.

```mermaid
sequenceDiagram
    autonumber
    participant API as FastAPI Router
    participant UC as CreateClientUseCase
    participant DTO as CreateClientDTO
    participant Dom as Client Entity
    participant Repo as Repository Impl
    participant DB as PostgreSQL

    API->>DTO: Validate Request Data
    API->>UC: execute(dto)
    
    activate UC
    UC->>Dom: Create Client Entity
    Note right of Dom: Runs Business Rules<br/>(Validates Invariants)
    
    UC->>Repo: save(client)
    activate Repo
    Repo->>DB: INSERT INTO clients...
    DB-->>Repo: Success
    Repo-->>UC: Return Saved Entity
    deactivate Repo
    
    UC-->>API: Return Result DTO
    deactivate UC
    
    API-->>User: HTTP 201 Created
```

---

## Component Diagram

High-level overview of the architectural layers and their responsibilities.

```mermaid
graph TD
    subgraph Presentation [Presentation Layer]
        API[FastAPI Router]
        Admin[Django Admin]
        CLI[Manage.py Commands]
    end

    subgraph Application [Application Layer]
        UseCases[Use Cases]
        DTOs[Data Transfer Objects]
        Ports[Input Ports]
    end

    subgraph Domain [Domain Layer (Core)]
        Entities[Entities]
        VO[Value Objects]
        RepoInt[Repository Interfaces]
        Events[Domain Events]
    end

    subgraph Infrastructure [Infrastructure Layer]
        RepoImpl[Repository Implementations]
        ORM[Django ORM]
        Postgres[(PostgreSQL)]
        EmailSvc[Email Service]
    end

    Presentation --> Application
    Application --> Domain
    Infrastructure --> Domain
    
    RepoImpl -. implements .-> RepoInt
    RepoImpl --> ORM
    ORM --> Postgres
    
    style Domain fill:#ffecb3,stroke:#ff6f00,stroke-width:2px,color:black
    style Application fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:black
```

---

## ER Diagram - Database

The physical schema implementation in PostgreSQL.

```mermaid
erDiagram
    CLIENTES ||--o{ ORDENES : places
    ORDENES ||--|{ LINEAS_ORDEN : contains
    PRODUCTOS ||--o{ LINEAS_ORDEN : is_referenced_in

    CLIENTES {
        uuid id PK
        varchar nombre
        varchar apellido
        varchar email UK
        varchar documento UK
        boolean activo
        timestamp fecha_creacion
    }

    ORDENES {
        uuid id PK
        uuid cliente_id FK
        varchar numero_orden
        varchar estado
        decimal total
        timestamp fecha
    }

    LINEAS_ORDEN {
        uuid id PK
        uuid orden_id FK
        uuid producto_id FK
        integer cantidad
        decimal precio_unitario
    }

    PRODUCTOS {
        uuid id PK
        varchar codigo UK
        varchar nombre
        decimal precio
        integer stock
    }
```

---

## State Diagram - Order

The lifecycle of an Order entity, demonstrating domain logic constraints.

```mermaid
stateDiagram-v2
    [*] --> CREADA
    
    CREADA --> CONFIRMADA : pagar()
    CREADA --> CANCELADA : cancelar()
    
    CONFIRMADA --> ENVIADA : enviar()
    CONFIRMADA --> CANCELADA : cancelar()
    
    ENVIADA --> ENTREGADA : entregar()
    
    ENTREGADA --> [*]
    CANCELADA --> [*]

    note right of CONFIRMADA
        Stock is reserved
        Payment Verified
    end note
```

---

## Data Flow Architecture

```mermaid
graph LR
    User((User)) -->|HTTP Request| API[Interfaces]
    API -->|DTO| App[Application]
    App -->|Entity| Dom[Domain]
    Dom -->|Repository Interface| Infra[Infrastructure]
    Infra -->|SQL| DB[(Database)]
    
    classDef layer fill:#f9f9f9,stroke:#333,stroke-width:2px
    class API,App,Dom,Infra layer
```
