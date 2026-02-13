# 🎯 Guía Rápida - Panel de Administración

## ✅ Estado Actual

El panel de administración está **completamente funcional** con las siguientes características:

### 📋 Funcionalidades Implementadas

#### 1. **Dashboard** (`/admin`)
- ✅ Estadísticas en tiempo real
- ✅ Ventas del mes
- ✅ Órdenes pendientes
- ✅ Stock bajo
- ✅ Clientes nuevos
- ✅ Últimas órdenes
- ✅ Productos con inventario crítico

#### 2. **Gestión de Productos** (`/admin/productos`)
- ✅ Listar todos los productos
- ✅ Crear nuevo producto
- ✅ Editar producto existente
- ✅ Eliminar producto (soft delete)
- ✅ Búsqueda y filtros
- ✅ Vista detallada con imagen

#### 3. **Gestión de Órdenes** (`/admin/ordenes`)
- ✅ Listar órdenes
- ✅ Filtrar por estado
- ✅ Ver detalles de orden
- ✅ Actualizar estado

#### 4. **Gestión de Clientes** (`/admin/clientes`)
- ✅ Listar clientes
- ✅ Ver perfil de cliente
- ✅ Ver historial de compras

#### 5. **Inventario** (`/admin/inventario`)
- ✅ Control de stock
- ✅ Alertas de stock bajo
- ✅ Actualización masiva

---

## 🚀 Cómo Usar el Panel de Administración

### Paso 1: Iniciar Sesión como Administrador

1. Ve a http://localhost:5173
2. Haz clic en el ícono de usuario (arriba a la derecha)
3. Haz clic en "INGRESAR CON CORREO"
4. Usa las credenciales:

```
Email:    admin@ecommerce.com
Password: Admin123!
```

5. **Automáticamente se abrirá una nueva pestaña** con el panel de administración en `/admin`

### Paso 2: Crear un Producto

#### Opción A: Desde el Dashboard
1. En el dashboard, haz clic en el botón **"Nuevo Producto"** (arriba a la derecha)
2. Esto te llevará a `/admin/productos/nuevo`

#### Opción B: Desde la Sección Productos
1. En el menú lateral, haz clic en **"Productos"**
2. Haz clic en **"Nuevo Producto"** (arriba a la derecha)

#### Opción C: Desde Acciones Rápidas
1. En el dashboard, ve a la sección **"Acciones Rápidas"** (al final)
2. Haz clic en el card de **"Nuevo Producto"**

### Paso 3: Llenar el Formulario de Producto

#### **Campos Obligatorios** (marcados con `*`):

1. **Código / SKU**: Identificador único (ej: `EXT-BR-24`)
   - No se puede modificar después de crear
   
2. **Nombre del Producto**: (ej: `Extensiones Brasileñas 24"`)

3. **Descripción**: Descripción detallada del producto

4. **Precio**: Monto en pesos colombianos (ej: `299000`)

5. **Moneda**: Por defecto COP (pesos colombianos)

#### **Campos Opcionales**:

- **Stock Actual**: Cantidad disponible (ej: `20`)
- **Stock Mínimo**: Alerta de inventario bajo (ej: `5`)
- **Categoría**: Extensiones, Pelucas, Cosméticos, etc.
- **Color**: Color del producto
- **Tipo**: Tipo de producto
- **Largo**: Longitud (para extensiones)
- **Origen**: País de origen
- **Método**: Método de aplicación
- **Calidad**: Grado de calidad
- **URL Imagen**: Link a la imagen del producto

### Paso 4: Guardar el Producto

1. Haz clic en **"Crear Producto"** (botón verde al final del formulario)
2. Verás un mensaje de éxito: "Producto creado correctamente"
3. Automáticamente serás redirigido a `/admin/productos`
4. El producto aparecerá en la lista

---

## 📊 Ejemplo de Producto para Prueba

```
Código: EXT-BR-001
Nombre: Extensiones Brasileñas Premium 24"
Descripción: Extensiones de cabello humano 100% brasileño, textura natural, color negro intenso. Ideal para dar volumen y largo.
Precio: 299000
Moneda: COP
Stock Actual: 15
Stock Mínimo: 5
Categoría: Extensiones
Color: Negro
Largo: 24 pulgadas
Origen: Brasil
Calidad: Premium
Método: Aplicación rápida
Imagen: https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400
```

---

## 🔧 Solución de Problemas

### ❌ "No puedo acceder al panel de admin"

**Problema**: Al intentar ir a `/admin` me redirige al home

**Solución**:
1. Asegúrate de estar logueado con una cuenta de administrador
2. Verifica que tu usuario tenga rol `ADMIN` o `OPERADOR`
3. Revisa la consola del navegador (F12) para ver errores

### ❌ "El botón Nuevo Producto no hace nada"

**Problema**: Al hacer clic en "Nuevo Producto" no pasa nada

**Solución**:
1. Verifica que estés autenticado (deberías ver tu nombre arriba a la derecha)
2. Revisa la consola del navegador (F12) para ver errores
3. Asegúrate de estar en la ruta `/admin` (no en `/` de la tienda)

### ❌ "Error al crear producto"

**Problema**: Al guardar aparece un error

**Soluciones posibles**:
1. **Campo código duplicado**: Cambia el código SKU por uno único
2. **Precio inválido**: Asegúrate de poner solo números (sin puntos ni comas)
3. **Backend no responde**: Verifica que el servidor backend esté corriendo en http://localhost:8000

Para verificar el backend:
```bash
# Deberías poder abrir esto en el navegador:
http://localhost:8000/docs
```

### ❌ "Los datos del dashboard aparecen en 0"

**Problema**: El dashboard muestra todo en cero

**Explicación**: Es normal si es la primera vez que usas el sistema. El dashboard muestra datos reales de la base de datos.

**Solución**:
1. Crea algunos productos desde `/admin/productos/nuevo`
2. Los datos se actualizarán automáticamente
3. Puedes refrescar la página para ver los cambios

---

## 🎨 Navegación del Panel Admin

```
/admin                          → Dashboard (inicio)
/admin/productos                → Lista de productos
/admin/productos/nuevo          → Crear producto
/admin/productos/:id/editar     → Editar producto
/admin/ordenes                  → Gestión de órdenes
/admin/clientes                 → Gestión de clientes
/admin/inventario               → Control de inventario
/admin/usuarios                 → Gestión de usuarios
/admin/config                   → Configuración
```

---

## 📱 Vista Móvil

El panel de administración está **100% optimizado para móviles**:
- ✅ Menú lateral colapsable
- ✅ Tablas con scroll horizontal
- ✅ Formularios responsivos
- ✅ Botones táctiles grandes

---

## 🔑 Roles de Usuario

| Rol | Acceso | Permisos |
|-----|--------|----------|
| **ADMIN** | Panel completo | Crear, editar, eliminar todo |
| **OPERADOR** | Panel completo | Crear, editar (NO eliminar) |
| **LECTURA** | Solo consulta | Ver datos (sin modificar) |
| **CLIENTE** | Tienda pública | Comprar productos |

---

## ✨ Características Especiales

### 🔍 Búsqueda Inteligente
- Busca por nombre, SKU o descripción
- Resultados en tiempo real
- Filtros por categoría y stock

### 📊 Estadísticas en Tiempo Real
- Cálculo automático de métricas
- Actualización al refrescar
- Gráficos visuales

### 🎯 Alertas de Stock
- Notificación cuando un producto tiene stock < 5
- Lista de productos críticos en dashboard
- Actualización en tiempo real

### 🚀 Rendimiento Optimizado
- Carga lazy de componentes
- Paginación automática
- Cache de datos

---

## 📞 Soporte

Si encuentras algún problema:

1. **Revisa la consola del navegador** (F12 → Console)
2. **Verifica que el backend esté corriendo** (http://localhost:8000/docs)
3. **Verifica que el frontend esté corriendo** (http://localhost:5173)
4. **Revisa el archivo** `.env` en la raíz del proyecto

---

**¡Listo! Tu panel de administración está completamente funcional** 🎉
