# 🎯 RESUMEN DEL BACKEND E-COMMERCE - GUÍA PARA FRONTEND

## 📌 INFORMACIÓN GENERAL

Este es un **backend completo de e-commerce** construido con:
- **Clean Architecture + DDD (Domain-Driven Design)**
- **FastAPI** para API REST de alto rendimiento
- **Django** para ORM y administración
- **PostgreSQL** como base de datos
- **JWT** para autenticación segura
- **RBAC** (Control de acceso por roles)

### ✅ Estado del Backend: **LISTO PARA USO**

El backend está completamente funcional con:
- ✅ Autenticación JWT con refresh tokens
- ✅ 3 entidades principales: Clientes, Productos, Órdenes
- ✅ Sistema de permisos por roles
- ✅ Rate limiting anti-abuso
- ✅ Auditoría automática de accesos
- ✅ Validaciones robustas de dominio

---

## 🚀 CÓMO EJECUTAR EL BACKEND

### 1. Configuración Inicial

```bash
# Navegar al proyecto
cd /home/kali/Escritorio/Ecom-pelo/e-comerce

# Crear entorno virtual (si tienes permisos)
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Base de Datos PostgreSQL

```bash
# Crear usuario y base de datos
sudo -u postgres psql

# En el prompt de PostgreSQL:
CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_pass123';
CREATE DATABASE ecommerce_db OWNER ecommerce_user;
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

### 3. Ejecutar Migraciones

```bash
# Aplicar migraciones de Django
python manage.py migrate

# Crear usuarios de prueba
python manage.py crear_usuarios_demo
```

### 4. Iniciar el Servidor

```bash
# Opción 1: Con FastAPI (Recomendado)
cd src
python main.py
# Servidor corriendo en: http://localhost:8000

# Opción 2: Con Django
python manage.py runserver
# Servidor corriendo en: http://127.0.0.1:8000
```

### 5. Documentación Interactiva

Una vez iniciado, visita:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔐 AUTENTICACIÓN PARA TU FRONTEND

### Usuarios de Prueba (Después de crear_usuarios_demo)

| Email | Password | Rol | Permisos |
|-------|----------|-----|----------|
| admin@ecommerce.com | Admin123! | ADMIN | Todos los permisos |
| operador@ecommerce.com | Operador123! | OPERADOR | Crear/Editar (no eliminar) |
| lectura@ecommerce.com | Lectura123! | LECTURA | Solo lectura |

### Flujo de Autenticación

#### 1. **LOGIN** - Obtener Tokens

```javascript
// POST /api/v1/auth/login
const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'admin@ecommerce.com',
    password: 'Admin123!'
  })
});

const data = await response.json();
/*
Respuesta:
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "uuid",
    "email": "admin@ecommerce.com",
    "nombre": "Admin",
    "rol": "ADMIN"
  }
}
*/

// Guardar tokens
localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);
localStorage.setItem('user', JSON.stringify(data.user));
```

#### 2. **USAR ACCESS TOKEN** en Peticiones

```javascript
const accessToken = localStorage.getItem('access_token');

const response = await fetch('http://localhost:8000/api/v1/productos', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});
```

#### 3. **REFRESH TOKEN** - Renovar Access Token

```javascript
// El access token expira en 15 minutos
// POST /api/v1/auth/refresh
const refreshToken = localStorage.getItem('refresh_token');

const response = await fetch('http://localhost:8000/api/v1/auth/refresh', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    refresh: refreshToken
  })
});

const data = await response.json();
// Actualizar tokens
localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);
```

#### 4. **LOGOUT** - Cerrar Sesión

```javascript
// POST /api/v1/auth/logout
const accessToken = localStorage.getItem('access_token');
const refreshToken = localStorage.getItem('refresh_token');

await fetch('http://localhost:8000/api/v1/auth/logout', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    refresh: refreshToken
  })
});

// Limpiar localStorage
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
localStorage.removeItem('user');
```

---

## 📡 API ENDPOINTS DISPONIBLES

### Base URL: `http://localhost:8000/api/v1`

### 🔐 Autenticación (`/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/login` | Iniciar sesión | No |
| POST | `/auth/refresh` | Renovar access token | No |
| POST | `/auth/logout` | Cerrar sesión | Sí |
| GET | `/auth/perfil` | Obtener perfil usuario | Sí |

### 👥 Clientes (`/clientes`)

| Método | Endpoint | Descripción | Rol Mínimo |
|--------|----------|-------------|------------|
| GET | `/clientes` | Listar todos los clientes | LECTURA |
| GET | `/clientes/{id}` | Obtener un cliente | LECTURA |
| POST | `/clientes` | Crear cliente | OPERADOR |
| PUT | `/clientes/{id}` | Actualizar cliente | OPERADOR |

**Ejemplo de Cliente:**
```json
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan@example.com",
  "tipo_documento": "DNI",
  "numero_documento": "12345678",
  "telefono": "+51987654321"
}
```

### 📦 Productos (`/productos`)

| Método | Endpoint | Descripción | Rol Mínimo |
|--------|----------|-------------|------------|
| GET | `/productos` | Listar todos los productos | LECTURA |
| GET | `/productos/{id}` | Obtener un producto | LECTURA |
| POST | `/productos` | Crear producto | OPERADOR |
| PUT | `/productos/{id}` | Actualizar producto | OPERADOR |
| DELETE | `/productos/{id}` | Eliminar producto | ADMIN |

**Ejemplo de Producto:**
```json
{
  "codigo": "PROD-001",
  "nombre": "Laptop HP",
  "descripcion": "Laptop HP 15 pulgadas",
  "precio_monto": 1500.00,
  "precio_moneda": "USD",
  "stock_actual": 25,
  "stock_minimo": 5
}
```

### 🛒 Órdenes (`/ordenes`)

| Método | Endpoint | Descripción | Rol Mínimo |
|--------|----------|-------------|------------|
| POST | `/ordenes` | Crear orden nueva | OPERADOR |
| POST | `/ordenes/{id}/lineas` | Agregar producto a orden | OPERADOR |
| POST | `/ordenes/{id}/confirmar` | Confirmar orden | OPERADOR |
| GET | `/ordenes/{id}` | Obtener detalles de orden | LECTURA |

**Flujo Completo de Orden:**

```javascript
// 1. Crear orden vacía
const ordenResponse = await fetch('/api/v1/ordenes', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    cliente_id: "uuid-del-cliente"
  })
});
const orden = await ordenResponse.json();

// 2. Agregar productos (líneas) a la orden
await fetch(`/api/v1/ordenes/${orden.id}/lineas`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    producto_id: "uuid-del-producto",
    cantidad: 2
  })
});

// 3. Confirmar la orden
await fetch(`/api/v1/ordenes/${orden.id}/confirmar`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
});
```

---

## 🎨 ESTRUCTURA DE DATOS PARA TU FRONTEND

### TypeScript/JavaScript Interfaces

```typescript
// Usuario
interface User {
  id: string;
  email: string;
  nombre: string;
  rol: 'ADMIN' | 'OPERADOR' | 'LECTURA';
}

// Token Response
interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

// Cliente
interface Cliente {
  id: string;
  nombre: string;
  apellido: string;
  email: string;
  tipo_documento: string;
  numero_documento: string;
  telefono?: string;
  activo: boolean;
  fecha_creacion: string;
  fecha_modificacion: string;
}

// Producto
interface Producto {
  id: string;
  codigo: string;
  nombre: string;
  descripcion: string;
  precio: string; // Formateado "1500.00 USD"
  precio_monto: number;
  precio_moneda: string;
  stock_actual: number;
  stock_minimo: number;
  activo: boolean;
  fecha_creacion: string;
  fecha_modificacion: string;
}

// Orden
interface Orden {
  id: string;
  cliente_id: string;
  estado: 'BORRADOR' | 'CONFIRMADA' | 'ENVIADA' | 'ENTREGADA' | 'CANCELADA';
  total: number;
  cantidad_items: number;
  lineas: LineaOrden[];
  activo: boolean;
  fecha_creacion: string;
  fecha_modificacion: string;
}

// Línea de Orden
interface LineaOrden {
  producto_id: string;
  cantidad: number;
  precio_unitario: number;
  subtotal: number;
}
```

---

## 🛡️ MANEJO DE ERRORES

### Códigos de Estado HTTP

| Código | Significado | Acción Frontend |
|--------|-------------|-----------------|
| 200 | OK | Mostrar datos |
| 201 | Creado | Redirigir o mostrar éxito |
| 400 | Bad Request | Mostrar errores de validación |
| 401 | No autenticado | Redirigir a login |
| 403 | Sin permisos | Mostrar mensaje de permisos |
| 404 | No encontrado | Mostrar "no encontrado" |
| 429 | Too Many Requests | Esperar y reintentar |
| 500 | Error del servidor | Mostrar error genérico |

### Estructura de Errores

```json
// Error 400 - Validación
{
  "detail": {
    "email": ["Este campo es obligatorio"],
    "precio_monto": ["El precio debe ser mayor a 0"]
  }
}

// Error 401 - No autenticado
{
  "detail": "Authentication credentials were not provided."
}

// Error 403 - Sin permisos
{
  "detail": "You do not have permission to perform this action."
}

// Error 404 - No encontrado
{
  "detail": "Cliente con ID xyz no encontrado"
}
```

### Interceptor de Axios (Recomendado)

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
});

// Request interceptor - Agregar token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Response interceptor - Manejar errores
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    
    // Si es 401 y no hemos intentado refresh aún
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Intentar refresh
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('/api/v1/auth/refresh', {
          refresh: refreshToken
        });
        
        // Guardar nuevo token
        localStorage.setItem('access_token', response.data.access);
        
        // Reintentar request original
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh falló - logout
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

---

## 🎯 FUNCIONALIDADES DISPONIBLES PARA TU FRONTEND

### ✅ Funcionalidades Implementadas

1. **Autenticación JWT**
   - Login/Logout
   - Refresh automático de tokens
   - Perfiles de usuario por rol

2. **Gestión de Clientes**
   - Crear, listar, ver detalles, actualizar
   - Validación de emails y documentos

3. **Gestión de Productos**
   - CRUD completo de productos
   - Control de stock
   - Validación de precios

4. **Gestión de Órdenes**
   - Crear órdenes
   - Agregar productos (líneas)
   - Confirmar órdenes
   - Estados de orden

5. **Seguridad**
   - Rate limiting
   - Auditoría de accesos
   - Validaciones de dominio

### 🎨 Pantallas Recomendadas para tu Frontend

#### 1. **Autenticación**
- [ ] Login
- [ ] Perfil de usuario
- [ ] Cambio de contraseña (por implementar en backend)

#### 2. **Dashboard**
- [ ] Resumen de ventas
- [ ] Productos con bajo stock
- [ ] Órdenes recientes

#### 3. **Clientes**
- [ ] Lista de clientes (tabla con búsqueda)
- [ ] Crear/Editar cliente (formulario)
- [ ] Detalle de cliente (con historial de órdenes)

#### 4. **Productos**
- [ ] Catálogo de productos (cards o tabla)
- [ ] Crear/Editar producto (formulario)
- [ ] Detalle de producto (con stock y precio)

#### 5. **Órdenes**
- [ ] Lista de órdenes (tabla con filtros)
- [ ] Crear orden (carrito de compra)
- [ ] Detalle de orden (con líneas y total)

---

## 🔍 VALIDACIONES IMPORTANTES DEL BACKEND

El backend valida automáticamente:

### Clientes
- ✅ Email válido (formato)
- ✅ Email único (no duplicados)
- ✅ Tipo de documento válido (DNI, RUC, etc.)
- ✅ Teléfono con formato internacional

### Productos
- ✅ Código único
- ✅ Precio > 0
- ✅ Stock >= 0
- ✅ Moneda válida

### Órdenes
- ✅ Cliente existe
- ✅ Producto existe y tiene stock
- ✅ Cantidad > 0
- ✅ No modificar orden confirmada

**Importante:** Tu frontend NO necesita replicar estas validaciones (aunque puede hacerlo para mejor UX). El backend siempre validará.

---

## 📚 RECURSOS ADICIONALES

### Scripts de Prueba Disponibles

```bash
# Probar autenticación
python scripts/test_api_auth.py

# Probar flujo de órdenes
python scripts/test_flujo_ordenes.py

# Probar rate limiting
python scripts/test_rate_limit.py

# Validar sistema completo
python scripts/validar_sistema.py
```

### Documentación Completa

Lee el [README.md](README.md) para:
- Arquitectura detallada del sistema
- Patrones de diseño implementados
- Configuración avanzada
- Despliegue en producción

---

## 🚀 PRÓXIMOS PASOS PARA TU FRONTEND

### 1. **Setup Inicial**
   - Instalar React/Vue/Angular
   - Configurar Axios o Fetch
   - Crear servicio de autenticación

### 2. **Implementar Login**
   - Formulario de login
   - Guardar tokens en localStorage
   - Interceptor para agregar Authorization header

### 3. **Crear Layout Principal**
   - Header con usuario logueado
   - Sidebar con navegación
   - Protección de rutas

### 4. **Páginas Básicas**
   - Dashboard
   - Lista de productos
   - Lista de clientes

### 5. **Funcionalidad de Carrito**
   - Agregar productos al carrito
   - Ver carrito
   - Crear orden desde carrito

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Necesito ejecutar Django y FastAPI por separado?**  
R: No, el archivo `src/main.py` integra ambos. Solo ejecuta `python src/main.py`.

**P: ¿Cómo cambio el puerto del servidor?**  
R: Edita `src/main.py` y cambia el parámetro `port=8000`.

**P: ¿El backend tiene CORS configurado?**  
R: Revisa `src/infrastructure/config/django_settings.py` y agrega tu dominio frontend a `CORS_ALLOWED_ORIGINS`.

**P: ¿Puedo usar este backend con móvil?**  
R: Sí, es una API REST estándar. Funciona con React Native, Flutter, etc.

**P: ¿Cómo agrego más endpoints?**  
R: Revisa la arquitectura en [README.md](README.md). Sigue el patrón existente en `src/interfaces/api/`.

---

## 📞 CONTACTO Y SOPORTE

- **Repositorio**: https://github.com/Yoiser16/e-comerce
- **Documentación API**: http://localhost:8000/docs (después de iniciar)
- **Admin Django**: http://localhost:8000/admin

---

**¡Tu backend está listo! 🎉 Ahora puedes concentrarte en construir un frontend increíble.**
