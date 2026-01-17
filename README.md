# Sistema Empresarial de Gestión - Clean Architecture

## Arquitectura

Este proyecto implementa **Clean Architecture / Hexagonal Architecture** estrictamente.

### Capas

```
src/
├── domain/          # Núcleo de negocio (sin dependencias externas)
├── application/     # Casos de uso y lógica de aplicación
├── infrastructure/  # Implementaciones técnicas (DB, logging, etc.)
├── interfaces/      # APIs y puntos de entrada
└── shared/          # Componentes compartidos
```

### Principios

- **Dominio puro**: Sin dependencias a frameworks
- **Inversión de dependencias**: Infraestructura depende del dominio
- **Separación de responsabilidades**: Cada capa tiene un propósito claro
- **Preparado para escalar**: Arquitectura event-driven lista para implementar

## Tecnologías Base

- Python 3.10+
- Django (backoffice y admin)
- FastAPI (APIs de alto rendimiento)
- MySQL (desacoplado por repositorios)

## Estructura de Dominio

### Entidades
- Cliente
- Producto
- Orden

### Value Objects
- Email
- Teléfono
- DocumentoIdentidad
- Dinero
- CodigoProducto
- LineaOrden

### Estados y Flujos
- Máquina de estados para Orden
- Transiciones validadas
- Eventos de dominio

## Próximos Pasos

1. Configurar Django y crear modelos ORM
2. Implementar repositorios concretos
3. Configurar FastAPI y endpoints
4. Implementar inyección de dependencias
5. Configurar base de datos MySQL
6. Implementar sistema de eventos
7. Agregar tests unitarios y de integración

## Ejecución

```bash
# Pendiente configuración de dependencias
python src/main.py
```

## Convenciones

- **Nombres de dominio**: Español
- **Código técnico**: Inglés (donde aplique)
- **Logging estructurado**: JSON
- **Auditoría completa**: Todas las operaciones críticas
