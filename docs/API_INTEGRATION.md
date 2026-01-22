# 🔌 Guía de Integración API

Esta guía está dirigida a desarrolladores frontend y consumidores de la API.

## Base URL

`http://localhost:8000/api/v1`

## Flujo de Autenticación

### 1. Obtener Tokens

**POST** `/auth/login`

```json
// Request
{
  "email": "user@example.com",
  "password": "secure_password"
}

// Response
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "rol": "ADMIN", ... }
}
```

### 2. Usar Access Token

Incluir el header en cada petición protegida:
`Authorization: Bearer <access_token>`

### 3. Renovar Token (Refresh)

Cuando el servidor retorna `401 Unauthorized` (y no es por credenciales inválidas), usar el endpoint de refresh:

**POST** `/auth/refresh`
Body: `{ "refresh": "<refresh_token>" }`

## Endpoints Principales

### Clientes

- `GET /clientes`: Listar (Requiere rol LECTURA+)
- `POST /clientes`: Crear (Requiere rol OPERADOR+)
- `PUT /clientes/{id}`: Editar (Requiere rol OPERADOR+)

### Productos

- `GET /productos`: Listar
- `POST /productos`: Crear (OPERADOR+)
- `DELETE /productos/{id}`: Eliminar (ADMIN)

### Órdenes

1. **Crear Orden**: `POST /ordenes`
2. **Agregar Items**: `POST /ordenes/{id}/lineas`
3. **Confirmar**: `POST /ordenes/{id}/confirmar`

## Manejo de Errores

| Código | Significado | Causa Común |
|--------|-------------|-------------|
| **400** | Bad Request | Error de validación en datos enviados. |
| **401** | Unauthorized | Token faltante, expirado o inválido. |
| **403** | Forbidden | Usuario autenticado pero sin rol suficiente. |
| **404** | Not Found | Recurso no existe. |
| **429** | Too Many Requests | Exceso de peticiones (Rate Limit). |
| **500** | Internal Error | Error no controlado en backend. |

### Ejemplo de Error de Validación (400)

```json
{
  "field_name": ["Este campo es obligatorio."]
}
```
