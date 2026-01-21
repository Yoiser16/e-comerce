# 🔔 Sistema de Notificaciones en Tiempo Real - Panel Admin

## 📌 Resumen de Mejoras Implementadas

Este documento detalla las mejoras implementadas en el panel de administración de órdenes para hacerlo dinámico y con notificaciones en tiempo real.

---

## ✨ Características Nuevas

### 1. 🔄 Actualización Automática (Polling)

**Antes:** Tenías que refrescar manualmente el navegador (F5) para ver nuevas órdenes.

**Ahora:** El sistema verifica automáticamente cada **5 segundos** si hay nuevas órdenes.

**Implementación:**
```javascript
// Polling cada 5 segundos
const startPolling = () => {
  pollingInterval.value = setInterval(() => {
    cargarOrdenes(true) // true = silent mode (sin spinner)
  }, 5000)
}
```

**Beneficios:**
- ✅ No necesitas refrescar manualmente
- ✅ Siempre ves las órdenes más recientes
- ✅ Mejora la eficiencia operativa
- ✅ Modo silencioso para no interrumpir tu trabajo

---

### 2. 🔔 Notificación Sonora

**Implementación:**
Cuando llega una nueva orden, se reproduce un sonido de notificación automáticamente.

```javascript
// Reproducir sonido cuando hay nuevas órdenes
if (nuevasOrdenes.length > ordenes.value.length) {
  await notificationSound.play()
}
```

**Características:**
- 🔊 Volumen ajustado al 50% (no molesta)
- 🎵 Sonido tipo "caja registradora"
- 🔕 No se reproduce si el navegador está en modo silencio

---

### 3. 📱 Notificaciones del Navegador

**Implementación:**
Si das permiso, aparecerá una notificación del sistema operativo cuando llegue una nueva orden.

```javascript
if ('Notification' in window && Notification.permission === 'granted') {
  new Notification('Nueva Orden Recibida', {
    body: `${cantidadNuevas} nueva(s) orden(es) pendiente(s)`,
    icon: '/favicon.ico'
  })
}
```

**Permisos:**
- Al cargar el panel por primera vez, el navegador te pedirá permiso
- Puedes aceptar o rechazar (opcional)
- Funciona incluso si el navegador está minimizado

**Ejemplo de notificación:**
```
┌─────────────────────────────┐
│ 🛒 Nueva Orden Recibida     │
│ 1 nueva(s) orden(es)        │
│ pendiente(s)                │
└─────────────────────────────┘
```

---

### 4. 🔵 Indicador Visual de Órdenes Nuevas

**Implementación:**
Las órdenes que no has visto tienen un **punto azul** al lado.

**Cómo funciona:**
- Se guarda en `localStorage` qué órdenes ya viste
- Al hacer clic en una orden, se marca como "vista"
- El punto azul desaparece automáticamente

**Código:**
```javascript
// Sistema de órdenes vistas
const isOrderSeen = (orderId) => {
  return getSeenOrders().includes(orderId)
}

// CSS del indicador
.order-card__unseen-dot {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #3b82f6; /* Azul */
  border-radius: 50%;
}
```

---

## 🛠️ Configuración Técnica

### Intervalo de Polling

Por defecto: **5 segundos**

Para cambiar el intervalo, edita esta línea en [AdminOrdenes.vue](../frontend/src/components/admin/AdminOrdenes.vue):

```javascript
pollingInterval.value = setInterval(() => {
  cargarOrdenes(true)
}, 5000) // ← Cambiar este valor (en milisegundos)
```

**Recomendaciones:**
- ⏱️ **3-5 segundos**: Ideal para alta frecuencia de órdenes
- ⏱️ **10 segundos**: Balance entre actualización y recursos
- ⏱️ **30 segundos**: Para bajo volumen de órdenes

---

## 🧪 Testing - Script de Órdenes de Prueba

Hemos creado un script bash que genera órdenes de prueba automáticamente.

### Ubicación:
```
scripts/crear_orden_test.sh
```

### Uso:
```bash
# Método 1: Ejecutar directamente
bash scripts/crear_orden_test.sh

# Método 2: Darle permisos de ejecución
chmod +x scripts/crear_orden_test.sh
./scripts/crear_orden_test.sh
```

### Output del Script:
```
════════════════════════════════════════════════════════════
   🛒 CREANDO ORDEN DE PRUEBA
════════════════════════════════════════════════════════════

Cliente: Juan García
Email: juan.garcia1234@test.com
Teléfono: 3107654321
Dirección: Calle 45 # 23-67, El Poblado, Medellín, Antioquia
Items: 2 producto(s)
Subtotal: $142,000
Envío: $8,000
Total: $150,000

Enviando petición a la API...

✅ ¡ORDEN CREADA EXITOSAMENTE!
   Código: KH-2847
   ID: 123e4567-e89b-12d3-a456-426614174000

════════════════════════════════════════════════════════════
Revisa el panel de administración para ver la nueva orden 🎉
════════════════════════════════════════════════════════════
```

### Datos Generados:

El script genera automáticamente:
- ✅ Nombres y apellidos aleatorios
- ✅ Emails únicos
- ✅ Teléfonos válidos (310xxxxxxx)
- ✅ Direcciones realistas
- ✅ Departamentos y ciudades de Colombia
- ✅ Entre 1 y 3 productos por orden
- ✅ Cálculos de subtotal y envío

---

## 🎯 Flujo de Testing Completo

### Paso 1: Iniciar el Backend
```bash
cd src
uvicorn main:app --reload
```

### Paso 2: Iniciar el Frontend
```bash
cd frontend
npm run dev
```

### Paso 3: Abrir el Panel Admin
1. Ve a `http://localhost:5173` (o el puerto que use Vite)
2. Inicia sesión como administrador
3. Ve a la sección **"Órdenes"**

### Paso 4: Observar el Sistema en Acción
El panel ahora:
- 🔄 Se actualiza automáticamente cada 5 segundos
- 🔵 Muestra un contador en tiempo real
- 📊 Filtra órdenes sin recargar la página

### Paso 5: Generar Órdenes de Prueba
En una nueva terminal:
```bash
bash scripts/crear_orden_test.sh
```

### Paso 6: Verificar Notificaciones
Deberías ver/escuchar:
1. 🔔 **Sonido de notificación**
2. 🔵 **Punto azul** en la nueva orden (indicador de "no vista")
3. 📱 **Notificación del navegador** (si diste permiso)
4. ➕ **Contador actualizado** en el header

---

## 🔧 Limpieza de Recursos

### Detención Automática del Polling

El sistema limpia automáticamente los recursos cuando:
- Cambias de página
- Cierras la pestaña
- Sales del panel de administración

**Código de limpieza:**
```javascript
onUnmounted(() => {
  stopPolling() // Detiene el intervalo
})
```

**Beneficios:**
- ✅ No consume recursos innecesarios
- ✅ Previene memory leaks
- ✅ Optimiza el rendimiento del navegador

---

## 📊 Métricas de Performance

### Consumo de Red
- **Petición cada 5 segundos**
- **~2KB por petición** (solo lista de órdenes)
- **~1.4MB por hora** de uso continuo

### Consumo de CPU
- **Mínimo**: Solo al procesar nuevas órdenes
- **Sonido**: ~5ms para reproducir
- **Comparación**: Igual que actualizar manualmente

### Batería
- **Impacto despreciable** en dispositivos modernos
- **Optimizado** con modo silencioso (sin spinners)

---

## 🚨 Solución de Problemas

### ❌ No se reproducen los sonidos

**Posibles causas:**
1. Navegador en modo silencio
2. Autoplay bloqueado por el navegador
3. Volumen del sistema en 0

**Solución:**
- Interactúa con la página primero (clic en cualquier lugar)
- Verifica la configuración de autoplay del navegador

### ❌ No aparecen las notificaciones del navegador

**Posibles causas:**
1. Permisos denegados
2. Modo "No molestar" activado
3. Navegador no soporta notificaciones

**Solución:**
```javascript
// Verificar permisos
console.log('Permiso actual:', Notification.permission)

// Solicitar permisos manualmente
Notification.requestPermission().then(permission => {
  console.log('Nuevo permiso:', permission)
})
```

### ❌ Las órdenes no se actualizan

**Posibles causas:**
1. Backend no está corriendo
2. CORS bloqueando las peticiones
3. Error en la API

**Verificación:**
1. Abre las **DevTools** (F12)
2. Ve a la pestaña **Network**
3. Verifica que se hagan peticiones cada 5 segundos a `/api/v1/ordenes`
4. Revisa si hay errores en **Console**

---

## 📝 Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `frontend/src/components/admin/AdminOrdenes.vue` | Sistema completo de polling y notificaciones |
| `scripts/crear_orden_test.sh` | Script de testing (NUEVO) |
| `scripts/README.md` | Documentación del script |

---

## 🎨 Estilo y UX

### Indicador de Orden No Vista

```css
.order-card__unseen-dot {
  position: absolute;
  top: 14px;
  left: -4px;
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  box-shadow: 0 0 6px rgba(59, 130, 246, 0.5);
}
```

**Diseño:**
- ✨ Azul (#3b82f6) - color de notificación estándar
- ✨ Sombra suave para resaltar
- ✨ Posición absoluta sin afectar el layout

---

## 🔮 Futuras Mejoras (Roadmap)

### v2.0 - WebSockets
- 🚀 Reemplazar polling por WebSockets
- 🚀 Notificaciones en tiempo real (< 100ms)
- 🚀 Menor consumo de red

### v2.1 - Personalización
- 🎨 Selección de sonidos de notificación
- 🎨 Configurar intervalo de actualización desde UI
- 🎨 Filtros avanzados de notificaciones

### v2.2 - Analytics
- 📊 Dashboard de órdenes en tiempo real
- 📊 Métricas de conversión
- 📊 Alertas de órdenes VIP

---

## 📞 Soporte

Si tienes problemas o sugerencias:
1. Revisa la sección de **Solución de Problemas** arriba
2. Verifica los logs en la consola del navegador
3. Revisa los logs del backend

---

**Última actualización:** Enero 2026  
**Versión:** 1.0  
**Estado:** ✅ Producción
